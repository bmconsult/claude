//! GPU-Accelerated Training Infrastructure
//!
//! Uses Candle for GPU computation with automatic differentiation.
//! Connects the gpu.rs model infrastructure to actual training.

use candle_core::{DType, Device, Result, Tensor, D};
use candle_nn::{loss, AdamW, Optimizer, ParamsAdamW, VarBuilder, VarMap};
use std::path::Path;

use crate::gpu::{get_device, HybridNexusLM};

/// GPU Training Configuration
#[derive(Debug, Clone)]
pub struct GpuTrainConfig {
    /// Learning rate
    pub lr: f64,
    /// Weight decay for AdamW
    pub weight_decay: f64,
    /// Beta1 for Adam
    pub beta1: f64,
    /// Beta2 for Adam
    pub beta2: f64,
    /// Batch size
    pub batch_size: usize,
    /// Sequence length
    pub seq_len: usize,
    /// Number of training steps
    pub max_steps: usize,
    /// Log every N steps
    pub log_every: usize,
    /// Save checkpoint every N steps
    pub save_every: usize,
    /// Evaluate every N steps
    pub eval_every: usize,
    /// Gradient clipping max norm
    pub max_grad_norm: f64,
    /// Warmup steps
    pub warmup_steps: usize,
}

impl Default for GpuTrainConfig {
    fn default() -> Self {
        Self {
            lr: 3e-4,
            weight_decay: 0.01,
            beta1: 0.9,
            beta2: 0.999,
            batch_size: 32,
            seq_len: 128,
            max_steps: 10000,
            log_every: 100,
            save_every: 1000,
            eval_every: 500,
            max_grad_norm: 1.0,
            warmup_steps: 100,
        }
    }
}

/// Learning rate scheduler with warmup and cosine decay
pub struct CosineScheduler {
    base_lr: f64,
    warmup_steps: usize,
    total_steps: usize,
    current_step: usize,
}

impl CosineScheduler {
    pub fn new(base_lr: f64, warmup_steps: usize, total_steps: usize) -> Self {
        Self {
            base_lr,
            warmup_steps,
            total_steps,
            current_step: 0,
        }
    }

    pub fn step(&mut self) -> f64 {
        self.current_step += 1;
        self.get_lr()
    }

    pub fn get_lr(&self) -> f64 {
        if self.current_step <= self.warmup_steps {
            // Linear warmup
            self.base_lr * (self.current_step as f64 / self.warmup_steps as f64)
        } else {
            // Cosine decay
            let progress = (self.current_step - self.warmup_steps) as f64
                / (self.total_steps - self.warmup_steps) as f64;
            let cosine = (std::f64::consts::PI * progress).cos();
            self.base_lr * 0.5 * (1.0 + cosine)
        }
    }
}

/// GPU Trainer for HybridNexusLM
pub struct GpuTrainer {
    config: GpuTrainConfig,
    device: Device,
    varmap: VarMap,
    optimizer: AdamW,
    scheduler: CosineScheduler,
    step: usize,
    best_val_loss: f32,
}

impl GpuTrainer {
    /// Create new GPU trainer
    pub fn new(config: GpuTrainConfig) -> Result<Self> {
        let device = get_device()?;
        println!("GPU Trainer initialized on {:?}", device);

        let varmap = VarMap::new();

        let optimizer = AdamW::new(
            varmap.all_vars(),
            ParamsAdamW {
                lr: config.lr,
                weight_decay: config.weight_decay,
                beta1: config.beta1,
                beta2: config.beta2,
                eps: 1e-8,
            },
        )?;

        let scheduler = CosineScheduler::new(
            config.lr,
            config.warmup_steps,
            config.max_steps,
        );

        Ok(Self {
            config,
            device,
            varmap,
            optimizer,
            scheduler,
            step: 0,
            best_val_loss: f32::INFINITY,
        })
    }

    /// Get the device
    pub fn device(&self) -> &Device {
        &self.device
    }

    /// Get the VarMap for model creation
    pub fn varmap(&self) -> &VarMap {
        &self.varmap
    }

    /// Create a VarBuilder from the trainer's VarMap
    pub fn var_builder(&self) -> VarBuilder {
        VarBuilder::from_varmap(&self.varmap, DType::F32, &self.device)
    }

    /// Compute cross-entropy loss for language modeling
    pub fn compute_loss(&self, logits: &Tensor, targets: &Tensor) -> Result<Tensor> {
        // logits: [batch, seq, vocab] or [seq, vocab]
        // targets: [batch, seq] or [seq]
        let logits_shape = logits.dims();
        let target_shape = targets.dims();

        // Flatten for cross entropy
        let (flat_logits, flat_targets) = if logits_shape.len() == 3 {
            // [batch, seq, vocab] -> [batch*seq, vocab]
            let batch = logits_shape[0];
            let seq = logits_shape[1];
            let vocab = logits_shape[2];
            (
                logits.reshape((batch * seq, vocab))?,
                targets.reshape((batch * seq,))?,
            )
        } else {
            // [seq, vocab] -> [seq, vocab]
            (logits.clone(), targets.flatten_all()?)
        };

        // Cross entropy loss
        loss::cross_entropy(&flat_logits, &flat_targets)
    }

    /// Single training step
    pub fn train_step(
        &mut self,
        model: &HybridNexusLM,
        input_ids: &Tensor,
        target_ids: &Tensor,
    ) -> Result<f32> {
        // Forward pass
        let logits = model.forward(input_ids)?;

        // Compute loss
        let loss = self.compute_loss(&logits, target_ids)?;
        let loss_val = loss.to_vec0::<f32>()?;

        // Backward pass
        self.optimizer.backward_step(&loss)?;

        // Update learning rate
        let new_lr = self.scheduler.step();
        self.optimizer.set_learning_rate(new_lr);

        self.step += 1;

        Ok(loss_val)
    }

    /// Evaluation step (no gradients)
    pub fn eval_step(
        &self,
        model: &HybridNexusLM,
        input_ids: &Tensor,
        target_ids: &Tensor,
    ) -> Result<f32> {
        let logits = model.forward(input_ids)?;
        let loss = self.compute_loss(&logits, target_ids)?;
        loss.to_vec0::<f32>()
    }

    /// Get current step
    pub fn current_step(&self) -> usize {
        self.step
    }

    /// Get current learning rate
    pub fn current_lr(&self) -> f64 {
        self.scheduler.get_lr()
    }

    /// Check if should log
    pub fn should_log(&self) -> bool {
        self.step % self.config.log_every == 0
    }

    /// Check if should save
    pub fn should_save(&self) -> bool {
        self.step % self.config.save_every == 0
    }

    /// Check if should evaluate
    pub fn should_eval(&self) -> bool {
        self.step % self.config.eval_every == 0
    }

    /// Update best validation loss
    pub fn update_best(&mut self, val_loss: f32) -> bool {
        if val_loss < self.best_val_loss {
            self.best_val_loss = val_loss;
            true
        } else {
            false
        }
    }

    /// Get best validation loss
    pub fn best_val_loss(&self) -> f32 {
        self.best_val_loss
    }

    /// Save checkpoint
    pub fn save_checkpoint(&self, path: &Path) -> Result<()> {
        self.varmap.save(path)?;
        println!("Saved checkpoint to {:?}", path);
        Ok(())
    }

    /// Load checkpoint
    pub fn load_checkpoint(&mut self, path: &Path) -> Result<()> {
        self.varmap.load(path)?;
        println!("Loaded checkpoint from {:?}", path);
        Ok(())
    }
}

/// Data preparation utilities
pub struct DataPreparer {
    device: Device,
}

impl DataPreparer {
    pub fn new(device: Device) -> Self {
        Self { device }
    }

    /// Create input/target pairs from token sequence
    /// Input: tokens[:-1], Target: tokens[1:]
    pub fn prepare_batch(&self, tokens: &[u32], seq_len: usize) -> Result<(Tensor, Tensor)> {
        let n = tokens.len().saturating_sub(1);
        let n = n.min(seq_len);

        let input: Vec<u32> = tokens[..n].to_vec();
        let target: Vec<u32> = tokens[1..=n].to_vec();

        let input_tensor = Tensor::new(input.as_slice(), &self.device)?;
        let target_tensor = Tensor::new(target.as_slice(), &self.device)?;

        Ok((input_tensor, target_tensor))
    }

    /// Create multiple training sequences from long token array
    pub fn create_sequences(&self, tokens: &[u32], seq_len: usize, stride: usize) -> Vec<(usize, usize)> {
        let mut sequences = Vec::new();
        let mut start = 0;

        while start + seq_len < tokens.len() {
            sequences.push((start, start + seq_len));
            start += stride;
        }

        sequences
    }
}

/// Training metrics tracker
#[derive(Default)]
pub struct MetricsTracker {
    losses: Vec<f32>,
    val_losses: Vec<f32>,
    learning_rates: Vec<f64>,
    steps: Vec<usize>,
}

impl MetricsTracker {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn log_train(&mut self, step: usize, loss: f32, lr: f64) {
        self.steps.push(step);
        self.losses.push(loss);
        self.learning_rates.push(lr);
    }

    pub fn log_val(&mut self, loss: f32) {
        self.val_losses.push(loss);
    }

    pub fn avg_loss(&self, last_n: usize) -> f32 {
        if self.losses.is_empty() {
            return 0.0;
        }
        let n = last_n.min(self.losses.len());
        self.losses.iter().rev().take(n).sum::<f32>() / n as f32
    }

    pub fn perplexity(&self, last_n: usize) -> f32 {
        self.avg_loss(last_n).exp()
    }

    pub fn last_val_loss(&self) -> Option<f32> {
        self.val_losses.last().copied()
    }
}

/// Generate text from model
pub fn generate(
    model: &HybridNexusLM,
    prompt_tokens: &[u32],
    max_new_tokens: usize,
    temperature: f32,
    device: &Device,
) -> Result<Vec<u32>> {
    use rand::Rng;
    let mut rng = rand::thread_rng();

    let mut tokens: Vec<u32> = prompt_tokens.to_vec();

    for _ in 0..max_new_tokens {
        let input = Tensor::new(tokens.as_slice(), device)?;
        let logits = model.forward(&input)?;

        // Get last position logits
        let seq_len = logits.dim(0)?;
        let last_logits = logits.narrow(0, seq_len - 1, 1)?.squeeze(0)?;

        // Apply temperature
        let scaled = if temperature != 1.0 {
            (last_logits / temperature as f64)?
        } else {
            last_logits
        };

        // Softmax to get probabilities
        let probs = candle_nn::ops::softmax(&scaled, D::Minus1)?;
        let probs_vec: Vec<f32> = probs.to_vec1()?;

        // Sample from distribution
        let r: f32 = rng.gen();
        let mut cumsum = 0.0;
        let mut next_token = 0u32;

        for (i, &p) in probs_vec.iter().enumerate() {
            cumsum += p;
            if cumsum > r {
                next_token = i as u32;
                break;
            }
        }

        tokens.push(next_token);
    }

    Ok(tokens)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cosine_scheduler() {
        let mut sched = CosineScheduler::new(1e-3, 100, 1000);

        // Warmup phase
        for _ in 0..100 {
            let lr = sched.step();
            assert!(lr <= 1e-3);
        }

        // Peak at end of warmup
        assert!((sched.get_lr() - 1e-3).abs() < 1e-6);

        // Decay phase
        for _ in 0..900 {
            let _ = sched.step();
        }

        // Should be near zero at end
        assert!(sched.get_lr() < 1e-4);
    }

    #[test]
    fn test_trainer_creation() -> Result<()> {
        let config = GpuTrainConfig::default();
        let trainer = GpuTrainer::new(config)?;
        assert_eq!(trainer.current_step(), 0);
        Ok(())
    }

    #[test]
    fn test_data_preparer() -> Result<()> {
        let device = Device::Cpu;
        let preparer = DataPreparer::new(device);

        let tokens: Vec<u32> = (0..100).collect();
        let (input, target) = preparer.prepare_batch(&tokens, 50)?;

        assert_eq!(input.dims(), &[50]);
        assert_eq!(target.dims(), &[50]);

        Ok(())
    }

    #[test]
    fn test_metrics_tracker() {
        let mut tracker = MetricsTracker::new();

        tracker.log_train(1, 5.0, 1e-3);
        tracker.log_train(2, 4.5, 1e-3);
        tracker.log_train(3, 4.0, 1e-3);

        assert!((tracker.avg_loss(3) - 4.5).abs() < 0.01);
    }
}
