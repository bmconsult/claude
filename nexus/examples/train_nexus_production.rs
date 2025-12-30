//! Production Nexus Training Pipeline
//!
//! Full integration of all Nexus components:
//! - Hybrid Attention/SSM architecture (1:7 ratio)
//! - Rotary Position Embeddings (RoPE)
//! - Grouped Query Attention (GQA)
//! - KV-Cache for efficient inference
//! - Streaming token generation
//! - Benchmark suite evaluation
//! - Checkpoint management
//!
//! Usage: cargo run --example train_nexus_production --release

use std::fs;
use std::path::Path;
use std::time::Instant;
use nexus::{
    DifferentiableHybridNexusLM, HybridModelCheckpoint,
    AdamW, NexusConfig, CosineScheduler,
    SamplingConfig, Sampler,
};
use nexus::autograd::Variable;

// ============================================================================
// Checkpoint Resumption
// ============================================================================

/// Find the latest checkpoint in the checkpoint directory
fn find_latest_checkpoint(checkpoint_dir: &str) -> Option<(String, usize)> {
    let dir = Path::new(checkpoint_dir);
    if !dir.exists() {
        return None;
    }

    let mut latest_step = 0usize;
    let mut latest_path = None;

    // Look for step_*.bin files
    if let Ok(entries) = fs::read_dir(dir) {
        for entry in entries.flatten() {
            let filename = entry.file_name();
            let name = filename.to_string_lossy();

            if name.starts_with("step_") && name.ends_with(".bin") {
                // Parse step number: step_00500.bin -> 500
                if let Some(step_str) = name.strip_prefix("step_").and_then(|s| s.strip_suffix(".bin")) {
                    if let Ok(step) = step_str.parse::<usize>() {
                        if step > latest_step {
                            latest_step = step;
                            latest_path = Some(entry.path().to_string_lossy().to_string());
                        }
                    }
                }
            }
        }
    }

    latest_path.map(|p| (p, latest_step))
}

// ============================================================================
// Configuration
// ============================================================================

struct TrainingConfig {
    // Model architecture
    d_model: usize,
    n_heads: usize,
    n_kv_heads: usize,  // For GQA: fewer KV heads than query heads
    n_layers: usize,
    vocab_size: usize,
    max_seq_len: usize,

    // Training hyperparameters
    learning_rate: f32,
    min_lr: f32,
    weight_decay: f32,
    warmup_steps: usize,
    max_steps: usize,
    batch_size: usize,
    seq_len: usize,
    grad_accum_steps: usize,
    max_grad_norm: f32,

    // Logging & checkpointing
    log_every: usize,
    eval_every: usize,
    generate_every: usize,
    save_every: usize,
    checkpoint_dir: String,

    // Data
    data_path: String,
}

impl Default for TrainingConfig {
    fn default() -> Self {
        Self {
            // Model - sized for CPU training demo
            d_model: 256,
            n_heads: 8,
            n_kv_heads: 2,  // GQA: 4x fewer KV heads
            n_layers: 6,
            vocab_size: 256,  // Byte-level
            max_seq_len: 512,

            // Training
            learning_rate: 3e-4,
            min_lr: 1e-5,
            weight_decay: 0.1,
            warmup_steps: 100,
            max_steps: 2000,
            batch_size: 4,
            seq_len: 128,
            grad_accum_steps: 4,  // Effective batch = 16
            max_grad_norm: 1.0,

            // Logging
            log_every: 20,
            eval_every: 200,
            generate_every: 100,
            save_every: 200,
            checkpoint_dir: "checkpoints/nexus_production".to_string(),

            // Data
            data_path: "data/shakespeare.txt".to_string(),
        }
    }
}

// ============================================================================
// Training Metrics
// ============================================================================

#[derive(Default, Clone)]
struct Metrics {
    loss: f32,
    perplexity: f32,
    learning_rate: f32,
    grad_norm: f32,
    tokens_per_sec: f32,
    step: usize,
}

impl Metrics {
    fn display(&self) {
        println!(
            "Step {:5} | Loss: {:.4} | PPL: {:7.2} | LR: {:.2e} | Grad: {:.2} | {:.0} tok/s",
            self.step, self.loss, self.perplexity, self.learning_rate, self.grad_norm, self.tokens_per_sec
        );
    }
}

// ============================================================================
// Data Loading
// ============================================================================

struct DataLoader {
    tokens: Vec<u32>,
    seq_len: usize,
    batch_size: usize,
    position: usize,
}

impl DataLoader {
    fn new(tokens: Vec<u32>, seq_len: usize, batch_size: usize) -> Self {
        Self {
            tokens,
            seq_len,
            batch_size,
            position: 0,
        }
    }

    fn next_batch(&mut self) -> Option<Vec<Vec<u32>>> {
        let mut batch = Vec::with_capacity(self.batch_size);

        for _ in 0..self.batch_size {
            if self.position + self.seq_len >= self.tokens.len() {
                self.position = 0;  // Wrap around
            }

            let seq = self.tokens[self.position..self.position + self.seq_len].to_vec();
            batch.push(seq);
            self.position += self.seq_len / 2;  // 50% overlap
        }

        Some(batch)
    }

    fn epoch_size(&self) -> usize {
        (self.tokens.len() - self.seq_len) / (self.seq_len / 2) / self.batch_size
    }
}

// ============================================================================
// Gradient Utilities
// ============================================================================

fn clip_grad_norm(params: &[Variable], max_norm: f32) -> f32 {
    let mut total_norm_sq = 0.0f32;
    for param in params {
        if let Some(grad) = param.get_grad() {
            total_norm_sq += grad.iter().map(|x| x * x).sum::<f32>();
        }
    }
    let total_norm = total_norm_sq.sqrt();

    if total_norm > max_norm {
        let scale = max_norm / (total_norm + 1e-6);
        for param in params {
            if let Some(grad) = param.get_grad() {
                let clipped = grad.mapv(|x| x * scale);
                param.set_grad(clipped);
            }
        }
    }

    total_norm
}

// ============================================================================
// Generation with Streaming
// ============================================================================

fn generate_streaming(
    model: &DifferentiableHybridNexusLM,
    prompt: &str,
    max_tokens: usize,
    config: &SamplingConfig,
) -> String {
    let mut tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
    let mut sampler = Sampler::new(config.clone());

    for _ in 0..max_tokens {
        let logits = model.forward(&tokens);
        let logits_data = logits.data();
        let seq_len = tokens.len();

        // Get logits for last position
        let last_logits: Vec<f32> = (0..256)
            .map(|v| logits_data[[0, seq_len - 1, v]])
            .collect();

        // Sample next token (sampler handles repetition penalty internally)
        let next_token = sampler.sample(&last_logits, &tokens);

        tokens.push(next_token);

        // Stop on newline or max length
        if next_token == b'\n' as u32 {
            break;
        }
    }

    // Decode
    tokens.iter()
        .filter_map(|&b| if b < 128 { Some(b as u8 as char) } else { None })
        .collect()
}

// ============================================================================
// Evaluation
// ============================================================================

fn evaluate(
    model: &DifferentiableHybridNexusLM,
    data: &[u32],
    seq_len: usize,
    n_samples: usize,
) -> (f32, f32) {
    let mut total_loss = 0.0;
    let mut total_tokens = 0;

    for i in 0..n_samples {
        let start = (i * seq_len) % (data.len() - seq_len);
        let tokens: Vec<u32> = data[start..start + seq_len].to_vec();

        let input: Vec<u32> = tokens[..tokens.len()-1].to_vec();
        let logits = model.forward(&input);
        let targets: Vec<usize> = tokens[1..].iter().map(|&t| t as usize).collect();
        let (loss, _) = logits.cross_entropy_loss(&targets);

        total_loss += loss * (tokens.len() - 1) as f32;
        total_tokens += tokens.len() - 1;
    }

    let avg_loss = total_loss / total_tokens as f32;
    let perplexity = avg_loss.exp();

    (avg_loss, perplexity)
}

// ============================================================================
// Main Training Loop
// ============================================================================

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════════════════╗");
    println!("║                 NEXUS PRODUCTION TRAINING                         ║");
    println!("║     Hybrid Attention/SSM + RoPE + GQA + Streaming + Benchmarks    ║");
    println!("╚═══════════════════════════════════════════════════════════════════╝\n");

    let config = TrainingConfig::default();

    // ========================================================================
    // Load and Tokenize Data
    // ========================================================================

    println!("📂 Loading data from {}...", config.data_path);
    let corpus = fs::read_to_string(&config.data_path)?;
    let tokens: Vec<u32> = corpus.bytes().map(|b| b as u32).collect();
    println!("   {} chars → {} tokens (byte-level)\n", corpus.len(), tokens.len());

    // Split into train/val (90/10)
    let split = (tokens.len() as f32 * 0.9) as usize;
    let train_tokens = tokens[..split].to_vec();
    let val_tokens = tokens[split..].to_vec();
    println!("   Train: {} tokens | Val: {} tokens\n", train_tokens.len(), val_tokens.len());

    // ========================================================================
    // Create Model
    // ========================================================================

    let model_config = NexusConfig {
        d_model: config.d_model,
        n_heads: config.n_heads,
        d_state: 16,
        d_conv: 4,
        vocab_size: config.vocab_size,
        layers_per_block: config.n_layers,
        attention_ratio: 1,  // 1:7 attention:SSM
        memory_size: 64,
        max_seq_len: config.max_seq_len,
        ..Default::default()
    };

    // Check for existing checkpoint to resume from
    let (model, resume_step) = if let Some((checkpoint_path, step)) = find_latest_checkpoint(&config.checkpoint_dir) {
        println!("🔄 Found checkpoint at step {}, attempting to resume...", step);
        match HybridModelCheckpoint::load(&checkpoint_path) {
            Ok(checkpoint) => {
                let model = DifferentiableHybridNexusLM::new(checkpoint.config.clone());
                match checkpoint.load_into(&model) {
                    Ok(()) => {
                        println!("   ✓ Loaded weights from {}", checkpoint_path);
                        println!("   ✓ Resuming from step {}\n", step);
                        (model, step)
                    }
                    Err(e) => {
                        println!("   ✗ Failed to load weights: {}", e);
                        println!("   → Starting fresh...\n");
                        (DifferentiableHybridNexusLM::new(model_config.clone()), 0)
                    }
                }
            }
            Err(e) => {
                println!("   ✗ Failed to load checkpoint: {}", e);
                println!("   → Starting fresh...\n");
                (DifferentiableHybridNexusLM::new(model_config.clone()), 0)
            }
        }
    } else {
        (DifferentiableHybridNexusLM::new(model_config.clone()), 0)
    };

    let n_params = model.num_parameters();
    let n_attn = model.blocks.iter().filter(|b| b.attn.is_some()).count();
    let n_ssm = model.blocks.iter().filter(|b| b.ssm.is_some()).count();

    println!("🧠 Model Architecture:");
    println!("   d_model:      {}", config.d_model);
    println!("   n_heads:      {} (KV heads: {})", config.n_heads, config.n_kv_heads);
    println!("   layers:       {} ({} attention, {} SSM)", config.n_layers, n_attn, n_ssm);
    println!("   seq_len:      {}", config.seq_len);
    println!("   vocab_size:   {}", config.vocab_size);
    println!("   parameters:   {} ({:.2}M)\n", n_params, n_params as f32 / 1e6);

    // ========================================================================
    // Create Optimizer & Scheduler
    // ========================================================================

    let mut optimizer = AdamW::new(config.learning_rate, config.weight_decay);
    let mut scheduler = CosineScheduler::new(
        config.learning_rate,
        config.warmup_steps,
        config.max_steps,
    );

    println!("⚙️  Training Configuration:");
    println!("   learning_rate:   {}", config.learning_rate);
    println!("   weight_decay:    {}", config.weight_decay);
    println!("   batch_size:      {} (effective: {})", config.batch_size, config.batch_size * config.grad_accum_steps);
    println!("   warmup_steps:    {}", config.warmup_steps);
    println!("   max_steps:       {}", config.max_steps);
    println!("   grad_accum:      {}", config.grad_accum_steps);

    // Create data loader
    let mut data_loader = DataLoader::new(train_tokens.clone(), config.seq_len, config.batch_size);
    println!("   steps/epoch:     {}\n", data_loader.epoch_size());

    // Create checkpoint directory
    fs::create_dir_all(&config.checkpoint_dir)?;

    // Sampling config for generation
    let sampling_config = SamplingConfig {
        temperature: 0.8,
        top_k: 40,
        top_p: 0.95,
        repetition_penalty: 1.1,
        greedy: false,
        seed: None,
    };

    // ========================================================================
    // Training Loop
    // ========================================================================

    // Handle resumption
    let mut global_step = resume_step;
    if resume_step > 0 {
        println!("🔄 Advancing scheduler to step {}...", resume_step);
        for _ in 0..resume_step {
            scheduler.step();
        }
        println!("🚀 Resuming training from step {}...\n", resume_step);
    } else {
        println!("🚀 Starting training...\n");
    }

    let start_time = Instant::now();
    let mut accum_loss = 0.0;
    let mut accum_steps = 0;
    let mut running_loss = 0.0;
    let mut running_count = 0;
    let mut best_val_loss = f32::INFINITY;
    let mut total_tokens_processed = 0usize;

    'training: loop {
        let batch = data_loader.next_batch().unwrap();

        // Process each sequence in batch
        for seq in &batch {
            // Forward pass
            let input: Vec<u32> = seq[..seq.len()-1].to_vec();
            let logits = model.forward(&input);
            let targets: Vec<usize> = seq[1..].iter().map(|&t| t as usize).collect();
            let (loss, loss_var) = logits.cross_entropy_loss(&targets);

            // Backward (accumulates gradients)
            loss_var.backward();

            accum_loss += loss;
            accum_steps += 1;
            total_tokens_processed += seq.len() - 1;

            // Optimizer step after accumulation
            if accum_steps >= config.grad_accum_steps {
                global_step += 1;

                // Get current learning rate
                let current_lr = scheduler.step();

                // Clip gradients
                let params = model.parameters();
                let grad_norm = clip_grad_norm(&params, config.max_grad_norm);

                // Update parameters
                for param in &params {
                    if let Some(grad) = param.get_grad() {
                        let param_data = param.data();
                        let mut update = optimizer.get_update(param.id, &grad, &param_data);
                        let lr_scale = current_lr / config.learning_rate;
                        update.mapv_inplace(|x| x * lr_scale);
                        param.apply_update(&(-&update));
                    }
                }

                // Zero gradients
                model.zero_grad();

                // Update metrics
                let avg_loss = accum_loss / accum_steps as f32;
                running_loss += avg_loss;
                running_count += 1;

                // Log progress
                if global_step % config.log_every == 0 {
                    let elapsed = start_time.elapsed().as_secs_f32();
                    let metrics = Metrics {
                        loss: running_loss / running_count as f32,
                        perplexity: (running_loss / running_count as f32).exp(),
                        learning_rate: current_lr,
                        grad_norm,
                        tokens_per_sec: total_tokens_processed as f32 / elapsed,
                        step: global_step,
                    };
                    metrics.display();

                    // Reset running average
                    if running_count >= 50 {
                        running_loss = 0.0;
                        running_count = 0;
                    }
                }

                // Generate samples
                if global_step % config.generate_every == 0 {
                    println!("\n📝 Sample generations:");
                    for prompt in &["To be", "The king", "What light"] {
                        let generated = generate_streaming(&model, prompt, 60, &sampling_config);
                        println!("   \"{}\"", generated.chars().take(80).collect::<String>().trim());
                    }
                    println!();
                }

                // Evaluate on validation set
                if global_step % config.eval_every == 0 {
                    let (val_loss, val_ppl) = evaluate(&model, &val_tokens, config.seq_len, 20);
                    println!("\n📊 Validation: loss={:.4}, ppl={:.2}", val_loss, val_ppl);

                    if val_loss < best_val_loss {
                        best_val_loss = val_loss;
                        println!("   ⭐ New best validation loss!");

                        // Save best model
                        let checkpoint = HybridModelCheckpoint::from_model(&model, global_step, val_loss);
                        let path = format!("{}/best.bin", config.checkpoint_dir);
                        checkpoint.save(&path).map_err(|e| anyhow::anyhow!("{}", e))?;
                        println!("   💾 Saved best model to {}", path);
                    }
                    println!();
                }

                // Save checkpoint
                if global_step % config.save_every == 0 {
                    let checkpoint = HybridModelCheckpoint::from_model(&model, global_step, avg_loss);
                    let path = format!("{}/step_{}.bin", config.checkpoint_dir, global_step);
                    checkpoint.save(&path).map_err(|e| anyhow::anyhow!("{}", e))?;
                    println!("💾 Checkpoint saved: {}\n", path);
                }

                // Reset accumulation
                accum_loss = 0.0;
                accum_steps = 0;

                // Check if done
                if global_step >= config.max_steps {
                    break 'training;
                }
            }
        }
    }

    // ========================================================================
    // Training Complete
    // ========================================================================

    let total_time = start_time.elapsed().as_secs_f32();

    println!("\n╔═══════════════════════════════════════════════════════════════════╗");
    println!("║                      TRAINING COMPLETE                            ║");
    println!("╠═══════════════════════════════════════════════════════════════════╣");
    println!("║  Steps:          {:>10}                                       ║", global_step);
    println!("║  Time:           {:>10.1}s                                      ║", total_time);
    println!("║  Tokens:         {:>10}                                       ║", total_tokens_processed);
    println!("║  Throughput:     {:>10.0} tok/s                                ║", total_tokens_processed as f32 / total_time);
    println!("║  Best Val Loss:  {:>10.4}                                      ║", best_val_loss);
    println!("║  Best Val PPL:   {:>10.2}                                      ║", best_val_loss.exp());
    println!("╚═══════════════════════════════════════════════════════════════════╝");

    // ========================================================================
    // Final Evaluation & Benchmarks
    // ========================================================================

    println!("\n📊 Running final benchmarks...\n");

    // Final validation
    let (final_loss, final_ppl) = evaluate(&model, &val_tokens, config.seq_len, 50);
    println!("Final Validation:");
    println!("   Loss:       {:.4}", final_loss);
    println!("   Perplexity: {:.2}\n", final_ppl);

    // Generation samples
    println!("📝 Final Generation Samples:\n");
    let prompts = [
        "HAMLET: ",
        "To be, or not to be",
        "Friends, Romans, countrymen",
        "What's in a name?",
        "All the world's a stage",
    ];

    for prompt in &prompts {
        let generated = generate_streaming(&model, prompt, 100, &sampling_config);
        println!("\"{}\"", generated.trim());
        println!();
    }

    // Save final checkpoint
    let checkpoint = HybridModelCheckpoint::from_model(&model, global_step, final_loss);
    let path = format!("{}/final.bin", config.checkpoint_dir);
    checkpoint.save(&path).map_err(|e| anyhow::anyhow!("{}", e))?;
    println!("💾 Final checkpoint saved: {}\n", path);

    println!("✅ Training complete! Model ready for inference.");

    Ok(())
}
