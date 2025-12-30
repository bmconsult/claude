//! Training Infrastructure
//!
//! Complete training loop with JEPA-style loss, checkpointing, and logging.

use crate::{Nexus, NexusConfig, Tensor};
use ndarray::{Array1, Array3};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{BufReader, BufWriter, Write};

/// Training configuration
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrainConfig {
    /// Learning rate
    pub lr: f32,
    /// Weight decay
    pub weight_decay: f32,
    /// Batch size
    pub batch_size: usize,
    /// Number of epochs
    pub epochs: usize,
    /// Gradient accumulation steps
    pub grad_accum_steps: usize,
    /// Maximum gradient norm for clipping
    pub max_grad_norm: f32,
    /// Warmup steps
    pub warmup_steps: usize,
    /// Log every N steps
    pub log_every: usize,
    /// Save checkpoint every N steps
    pub save_every: usize,
    /// Evaluation every N steps
    pub eval_every: usize,
    /// JEPA mask ratio
    pub mask_ratio: f32,
    /// VICReg variance loss weight
    pub variance_weight: f32,
    /// VICReg invariance loss weight
    pub invariance_weight: f32,
    /// VICReg covariance loss weight
    pub covariance_weight: f32,
}

impl Default for TrainConfig {
    fn default() -> Self {
        Self {
            lr: 3e-4,
            weight_decay: 0.01,
            batch_size: 32,
            epochs: 10,
            grad_accum_steps: 1,
            max_grad_norm: 1.0,
            warmup_steps: 1000,
            log_every: 100,
            save_every: 1000,
            eval_every: 500,
            mask_ratio: 0.3,
            variance_weight: 25.0,
            invariance_weight: 25.0,
            covariance_weight: 1.0,
        }
    }
}

/// Training state for checkpointing
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrainState {
    pub step: usize,
    pub epoch: usize,
    pub best_loss: f32,
    pub losses: Vec<f32>,
}

impl Default for TrainState {
    fn default() -> Self {
        Self {
            step: 0,
            epoch: 0,
            best_loss: f32::INFINITY,
            losses: Vec::new(),
        }
    }
}

/// VICReg-style loss for JEPA training
/// Combines: Invariance (prediction matches target) + Variance (avoid collapse) + Covariance (decorrelate)
pub struct VICRegLoss {
    pub variance_weight: f32,
    pub invariance_weight: f32,
    pub covariance_weight: f32,
}

impl VICRegLoss {
    pub fn new(config: &TrainConfig) -> Self {
        Self {
            variance_weight: config.variance_weight,
            invariance_weight: config.invariance_weight,
            covariance_weight: config.covariance_weight,
        }
    }

    /// Compute VICReg loss between prediction and target embeddings
    pub fn compute(&self, pred: &Array3<f32>, target: &Array3<f32>) -> (f32, f32, f32, f32) {
        let (batch, seq_len, d_model) = pred.dim();
        let n = (batch * seq_len) as f32;

        // 1. Invariance loss: MSE between prediction and target
        let mut inv_loss = 0.0f32;
        for b in 0..batch {
            for s in 0..seq_len {
                for d in 0..d_model {
                    let diff = pred[[b, s, d]] - target[[b, s, d]];
                    inv_loss += diff * diff;
                }
            }
        }
        inv_loss /= n * d_model as f32;

        // 2. Variance loss: encourage embeddings to have unit variance
        // Compute mean and std for each dimension
        let mut means_pred = Array1::zeros(d_model);
        let mut means_target = Array1::zeros(d_model);

        for d in 0..d_model {
            let mut sum_pred = 0.0f32;
            let mut sum_target = 0.0f32;
            for b in 0..batch {
                for s in 0..seq_len {
                    sum_pred += pred[[b, s, d]];
                    sum_target += target[[b, s, d]];
                }
            }
            means_pred[d] = sum_pred / n;
            means_target[d] = sum_target / n;
        }

        let mut var_loss = 0.0f32;
        for d in 0..d_model {
            let mut var_pred = 0.0f32;
            let mut var_target = 0.0f32;
            for b in 0..batch {
                for s in 0..seq_len {
                    var_pred += (pred[[b, s, d]] - means_pred[d]).powi(2);
                    var_target += (target[[b, s, d]] - means_target[d]).powi(2);
                }
            }
            var_pred = (var_pred / n).sqrt();
            var_target = (var_target / n).sqrt();

            // Hinge loss: max(0, 1 - std)
            var_loss += (1.0 - var_pred).max(0.0);
            var_loss += (1.0 - var_target).max(0.0);
        }
        var_loss /= d_model as f32;

        // 3. Covariance loss: encourage different dimensions to be uncorrelated
        // C = (Z - mean)^T @ (Z - mean) / (n-1)
        // Loss = sum of squared off-diagonal elements
        let mut cov_loss = 0.0f32;

        // Compute covariance matrix (simplified - just off-diagonal)
        for d1 in 0..d_model {
            for d2 in (d1 + 1)..d_model {
                let mut cov = 0.0f32;
                for b in 0..batch {
                    for s in 0..seq_len {
                        cov += (pred[[b, s, d1]] - means_pred[d1]) *
                               (pred[[b, s, d2]] - means_pred[d2]);
                    }
                }
                cov /= n - 1.0;
                cov_loss += cov * cov;
            }
        }
        cov_loss /= d_model as f32;

        let total = self.invariance_weight * inv_loss +
                    self.variance_weight * var_loss +
                    self.covariance_weight * cov_loss;

        (total, inv_loss, var_loss, cov_loss)
    }
}

/// JEPA-style masking
pub struct JEPAMasker {
    mask_ratio: f32,
}

impl JEPAMasker {
    pub fn new(mask_ratio: f32) -> Self {
        Self { mask_ratio }
    }

    /// Generate mask for JEPA training
    /// Returns (context_indices, target_indices)
    pub fn generate_mask(&self, seq_len: usize) -> (Vec<usize>, Vec<usize>) {
        use rand::prelude::*;
        let mut rng = rand::thread_rng();

        let n_masked = ((seq_len as f32) * self.mask_ratio) as usize;
        let n_masked = n_masked.max(1);

        // Random selection of target positions
        let mut all_indices: Vec<usize> = (0..seq_len).collect();
        all_indices.shuffle(&mut rng);

        let target_indices: Vec<usize> = all_indices[..n_masked].to_vec();
        let context_indices: Vec<usize> = all_indices[n_masked..].to_vec();

        (context_indices, target_indices)
    }

    /// Apply mask to embeddings (zero out masked positions)
    pub fn apply_mask(&self, x: &Array3<f32>, mask_indices: &[usize]) -> Array3<f32> {
        let (batch, seq_len, d_model) = x.dim();
        let mut masked = x.clone();

        for b in 0..batch {
            for &idx in mask_indices {
                if idx < seq_len {
                    for d in 0..d_model {
                        masked[[b, idx, d]] = 0.0;
                    }
                }
            }
        }

        masked
    }
}

/// Data batch for training
pub struct Batch {
    pub input: Array3<f32>,
    pub target: Option<Array3<f32>>,
}

/// Simple data loader for training
pub struct DataLoader {
    data: Vec<Array3<f32>>,
    batch_size: usize,
    current_idx: usize,
    shuffle: bool,
    indices: Vec<usize>,
}

impl DataLoader {
    pub fn new(data: Vec<Array3<f32>>, batch_size: usize, shuffle: bool) -> Self {
        let n = data.len();
        Self {
            data,
            batch_size,
            current_idx: 0,
            shuffle,
            indices: (0..n).collect(),
        }
    }

    pub fn reset(&mut self) {
        self.current_idx = 0;
        if self.shuffle {
            use rand::prelude::*;
            let mut rng = rand::thread_rng();
            self.indices.shuffle(&mut rng);
        }
    }

    pub fn len(&self) -> usize {
        (self.data.len() + self.batch_size - 1) / self.batch_size
    }

    pub fn is_empty(&self) -> bool {
        self.data.is_empty()
    }
}

impl Iterator for DataLoader {
    type Item = Batch;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_idx >= self.data.len() {
            return None;
        }

        let end_idx = (self.current_idx + self.batch_size).min(self.data.len());
        let batch_indices = &self.indices[self.current_idx..end_idx];

        // Stack samples into batch
        let samples: Vec<_> = batch_indices.iter()
            .map(|&i| self.data[i].clone())
            .collect();

        if samples.is_empty() {
            return None;
        }

        // Combine into single batch tensor
        let (_, seq_len, d_model) = samples[0].dim();
        let batch_size = samples.len();
        let mut batch_data = Array3::zeros((batch_size, seq_len, d_model));

        for (b, sample) in samples.iter().enumerate() {
            for s in 0..seq_len {
                for d in 0..d_model {
                    batch_data[[b, s, d]] = sample[[0, s, d]];
                }
            }
        }

        self.current_idx = end_idx;

        Some(Batch {
            input: batch_data,
            target: None,
        })
    }
}

/// Learning rate scheduler with warmup and cosine decay
pub struct CosineScheduler {
    base_lr: f32,
    warmup_steps: usize,
    total_steps: usize,
    current_step: usize,
}

impl CosineScheduler {
    pub fn new(base_lr: f32, warmup_steps: usize, total_steps: usize) -> Self {
        Self {
            base_lr,
            warmup_steps,
            total_steps,
            current_step: 0,
        }
    }

    pub fn step(&mut self) -> f32 {
        self.current_step += 1;

        if self.current_step <= self.warmup_steps {
            // Linear warmup
            self.base_lr * (self.current_step as f32 / self.warmup_steps as f32)
        } else {
            // Cosine decay
            let progress = (self.current_step - self.warmup_steps) as f32 /
                          (self.total_steps - self.warmup_steps) as f32;
            let cosine = (std::f32::consts::PI * progress).cos();
            self.base_lr * 0.5 * (1.0 + cosine)
        }
    }

    pub fn get_lr(&self) -> f32 {
        if self.current_step <= self.warmup_steps {
            self.base_lr * (self.current_step as f32 / self.warmup_steps as f32)
        } else {
            let progress = (self.current_step - self.warmup_steps) as f32 /
                          (self.total_steps - self.warmup_steps) as f32;
            let cosine = (std::f32::consts::PI * progress).cos();
            self.base_lr * 0.5 * (1.0 + cosine)
        }
    }
}

/// Gradient clipping by norm
pub fn clip_grad_norm(grads: &mut [Array3<f32>], max_norm: f32) -> f32 {
    // Compute total norm
    let mut total_norm_sq = 0.0f32;
    for grad in grads.iter() {
        total_norm_sq += grad.iter().map(|x| x * x).sum::<f32>();
    }
    let total_norm = total_norm_sq.sqrt();

    // Clip if necessary
    if total_norm > max_norm {
        let scale = max_norm / (total_norm + 1e-6);
        for grad in grads.iter_mut() {
            grad.mapv_inplace(|x| x * scale);
        }
    }

    total_norm
}

/// Checkpoint manager
pub struct CheckpointManager {
    save_dir: String,
    keep_last_n: usize,
}

impl CheckpointManager {
    pub fn new(save_dir: &str, keep_last_n: usize) -> Self {
        std::fs::create_dir_all(save_dir).ok();
        Self {
            save_dir: save_dir.to_string(),
            keep_last_n,
        }
    }

    pub fn save(&self, state: &TrainState, config: &NexusConfig, step: usize) -> anyhow::Result<()> {
        let path = format!("{}/checkpoint_{}.json", self.save_dir, step);

        let checkpoint = serde_json::json!({
            "state": state,
            "config": config,
            "step": step,
        });

        let file = File::create(&path)?;
        let mut writer = BufWriter::new(file);
        serde_json::to_writer_pretty(&mut writer, &checkpoint)?;

        // Clean up old checkpoints
        self.cleanup()?;

        Ok(())
    }

    pub fn load_latest(&self) -> anyhow::Result<Option<(TrainState, NexusConfig)>> {
        let mut checkpoints: Vec<_> = std::fs::read_dir(&self.save_dir)?
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().map(|x| x == "json").unwrap_or(false))
            .collect();

        if checkpoints.is_empty() {
            return Ok(None);
        }

        checkpoints.sort_by_key(|e| e.path());
        let latest = checkpoints.last().unwrap();

        let file = File::open(latest.path())?;
        let reader = BufReader::new(file);
        let checkpoint: serde_json::Value = serde_json::from_reader(reader)?;

        let state: TrainState = serde_json::from_value(checkpoint["state"].clone())?;
        let config: NexusConfig = serde_json::from_value(checkpoint["config"].clone())?;

        Ok(Some((state, config)))
    }

    fn cleanup(&self) -> anyhow::Result<()> {
        let mut checkpoints: Vec<_> = std::fs::read_dir(&self.save_dir)?
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().map(|x| x == "json").unwrap_or(false))
            .collect();

        if checkpoints.len() > self.keep_last_n {
            checkpoints.sort_by_key(|e| e.path());
            for entry in checkpoints.iter().take(checkpoints.len() - self.keep_last_n) {
                std::fs::remove_file(entry.path())?;
            }
        }

        Ok(())
    }
}

/// Training metrics logger
pub struct MetricsLogger {
    log_file: Option<File>,
    losses: Vec<f32>,
    inv_losses: Vec<f32>,
    var_losses: Vec<f32>,
    cov_losses: Vec<f32>,
    learning_rates: Vec<f32>,
}

impl MetricsLogger {
    pub fn new(log_path: Option<&str>) -> Self {
        let log_file = log_path.and_then(|p| File::create(p).ok());

        Self {
            log_file,
            losses: Vec::new(),
            inv_losses: Vec::new(),
            var_losses: Vec::new(),
            cov_losses: Vec::new(),
            learning_rates: Vec::new(),
        }
    }

    pub fn log(&mut self, step: usize, loss: f32, inv: f32, var: f32, cov: f32, lr: f32) {
        self.losses.push(loss);
        self.inv_losses.push(inv);
        self.var_losses.push(var);
        self.cov_losses.push(cov);
        self.learning_rates.push(lr);

        let msg = format!(
            "Step {} | Loss: {:.4} (inv: {:.4}, var: {:.4}, cov: {:.4}) | LR: {:.6}",
            step, loss, inv, var, cov, lr
        );

        println!("{}", msg);

        if let Some(ref mut f) = self.log_file {
            writeln!(f, "{}", msg).ok();
        }
    }

    pub fn avg_loss(&self, last_n: usize) -> f32 {
        if self.losses.is_empty() {
            return 0.0;
        }
        let n = last_n.min(self.losses.len());
        self.losses.iter().rev().take(n).sum::<f32>() / n as f32
    }
}

/// Main trainer
pub struct Trainer {
    pub model_config: NexusConfig,
    pub train_config: TrainConfig,
    pub state: TrainState,
    masker: JEPAMasker,
    loss_fn: VICRegLoss,
    scheduler: Option<CosineScheduler>,
    checkpoint_mgr: CheckpointManager,
    logger: MetricsLogger,
}

impl Trainer {
    pub fn new(
        model_config: NexusConfig,
        train_config: TrainConfig,
        checkpoint_dir: &str,
        log_path: Option<&str>,
    ) -> Self {
        let masker = JEPAMasker::new(train_config.mask_ratio);
        let loss_fn = VICRegLoss::new(&train_config);
        let checkpoint_mgr = CheckpointManager::new(checkpoint_dir, 5);
        let logger = MetricsLogger::new(log_path);

        Self {
            model_config,
            train_config,
            state: TrainState::default(),
            masker,
            loss_fn,
            scheduler: None,
            checkpoint_mgr,
            logger,
        }
    }

    /// Initialize scheduler with total steps
    pub fn init_scheduler(&mut self, total_steps: usize) {
        self.scheduler = Some(CosineScheduler::new(
            self.train_config.lr,
            self.train_config.warmup_steps,
            total_steps,
        ));
    }

    /// Training step (simplified - would need full autograd integration)
    pub fn train_step(&mut self, model: &mut Nexus, batch: &Batch) -> (f32, f32, f32, f32) {
        let (_, seq_len, _) = batch.input.dim();

        // Generate JEPA mask
        let (_context_indices, target_indices) = self.masker.generate_mask(seq_len);

        // Create context (masked input) and target views
        let context_input = self.masker.apply_mask(&batch.input, &target_indices);

        // Forward pass on context
        let context_tensor = Tensor { data: context_input.clone() };
        let context_repr = model.forward(&context_tensor, true);

        // Get target representations (from unmasked input)
        let target_tensor = Tensor { data: batch.input.clone() };
        let target_repr = model.forward(&target_tensor, false);

        // Compute JEPA loss (prediction matches target at masked positions)
        let (total_loss, inv_loss, var_loss, cov_loss) =
            self.loss_fn.compute(&context_repr.data, &target_repr.data);

        // Update step counter
        self.state.step += 1;

        // Get learning rate
        let lr = if let Some(ref mut sched) = self.scheduler {
            sched.step()
        } else {
            self.train_config.lr
        };

        // Log if needed
        if self.state.step % self.train_config.log_every == 0 {
            self.logger.log(
                self.state.step,
                total_loss,
                inv_loss,
                var_loss,
                cov_loss,
                lr,
            );
        }

        // Save checkpoint if needed
        if self.state.step % self.train_config.save_every == 0 {
            self.checkpoint_mgr.save(&self.state, &self.model_config, self.state.step).ok();
        }

        // Track best loss
        if total_loss < self.state.best_loss {
            self.state.best_loss = total_loss;
        }

        self.state.losses.push(total_loss);

        (total_loss, inv_loss, var_loss, cov_loss)
    }

    /// Run full training loop
    pub fn train(&mut self, model: &mut Nexus, train_loader: &mut DataLoader) {
        let total_steps = self.train_config.epochs * train_loader.len();
        self.init_scheduler(total_steps);

        println!("Starting training for {} epochs ({} steps)", self.train_config.epochs, total_steps);

        for epoch in 0..self.train_config.epochs {
            self.state.epoch = epoch;
            train_loader.reset();

            let mut epoch_loss = 0.0f32;
            let mut n_batches = 0;

            for batch in train_loader.by_ref() {
                let (loss, _, _, _) = self.train_step(model, &batch);
                epoch_loss += loss;
                n_batches += 1;
            }

            let avg_loss = epoch_loss / n_batches as f32;
            println!("Epoch {} | Avg Loss: {:.4}", epoch + 1, avg_loss);
        }

        // Save final checkpoint
        self.checkpoint_mgr.save(&self.state, &self.model_config, self.state.step).ok();
        println!("Training complete! Best loss: {:.4}", self.state.best_loss);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vicreg_loss() {
        let config = TrainConfig::default();
        let loss_fn = VICRegLoss::new(&config);

        let pred = Array3::ones((2, 4, 8));
        let target = Array3::ones((2, 4, 8)) * 1.1;

        let (total, inv, var, cov) = loss_fn.compute(&pred, &target);
        assert!(total > 0.0);
        assert!(inv > 0.0);  // Difference exists
    }

    #[test]
    fn test_jepa_masker() {
        let masker = JEPAMasker::new(0.3);
        let (ctx, tgt) = masker.generate_mask(100);

        // Should have roughly 30% masked
        assert!(tgt.len() >= 20 && tgt.len() <= 40);
        assert_eq!(ctx.len() + tgt.len(), 100);
    }

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
    fn test_data_loader() {
        let data: Vec<Array3<f32>> = (0..10)
            .map(|_| Array3::ones((1, 4, 8)))
            .collect();

        let mut loader = DataLoader::new(data, 3, false);
        assert_eq!(loader.len(), 4);  // ceil(10/3)

        let mut batch_count = 0;
        for batch in loader.by_ref() {
            batch_count += 1;
            assert!(batch.input.dim().0 <= 3);
        }
        assert_eq!(batch_count, 4);
    }

    #[test]
    fn test_trainer_creation() {
        let model_config = NexusConfig::default();
        let train_config = TrainConfig::default();

        let trainer = Trainer::new(
            model_config,
            train_config,
            "/tmp/nexus_test",
            None,
        );

        assert_eq!(trainer.state.step, 0);
        assert_eq!(trainer.state.epoch, 0);
    }
}
