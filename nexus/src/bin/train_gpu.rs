//! GPU-Accelerated Nexus Training Binary
//!
//! Usage: nexus-train-gpu --data data.txt --output checkpoints [options]
//!
//! Requires: cargo build --release --features cuda (for NVIDIA GPUs)
//!       or: cargo build --release --features metal (for Apple Silicon)

use anyhow::Result;
use candle_core::{DType, Device, Tensor};
use candle_nn::VarBuilder;
use indicatif::{ProgressBar, ProgressStyle};
use nexus::gpu::{get_device, HybridNexusLM};
use nexus::training_gpu::{
    generate, CosineScheduler, DataPreparer, GpuTrainConfig, GpuTrainer, MetricsTracker,
};
use nexus::SimpleBPE;
use std::fs;
use std::path::PathBuf;
use std::time::Instant;

fn main() -> Result<()> {
    env_logger::init();

    println!("╔══════════════════════════════════════════════════════════════╗");
    println!("║              NEXUS GPU Training v0.1                          ║");
    println!("║      Hybrid Intelligence Architecture - GPU Accelerated       ║");
    println!("╚══════════════════════════════════════════════════════════════╝");
    println!();

    // Parse arguments
    let args: Vec<String> = std::env::args().collect();

    let data_path = args
        .iter()
        .position(|x| x == "--data")
        .map(|i| PathBuf::from(&args[i + 1]))
        .unwrap_or_else(|| PathBuf::from("data/shakespeare.txt"));

    let output_dir = args
        .iter()
        .position(|x| x == "--output")
        .map(|i| args[i + 1].clone())
        .unwrap_or_else(|| "checkpoints/gpu".to_string());

    let max_steps: usize = args
        .iter()
        .position(|x| x == "--steps")
        .map(|i| args[i + 1].parse().unwrap_or(3000))
        .unwrap_or(3000);

    let seq_len: usize = args
        .iter()
        .position(|x| x == "--seq-len")
        .map(|i| args[i + 1].parse().unwrap_or(128))
        .unwrap_or(128);

    let lr: f64 = args
        .iter()
        .position(|x| x == "--lr")
        .map(|i| args[i + 1].parse().unwrap_or(3e-4))
        .unwrap_or(3e-4);

    let log_every: usize = args
        .iter()
        .position(|x| x == "--log-every")
        .map(|i| args[i + 1].parse().unwrap_or(20))
        .unwrap_or(20);

    let eval_every: usize = args
        .iter()
        .position(|x| x == "--eval-every")
        .map(|i| args[i + 1].parse().unwrap_or(100))
        .unwrap_or(100);

    let save_every: usize = args
        .iter()
        .position(|x| x == "--save-every")
        .map(|i| args[i + 1].parse().unwrap_or(500))
        .unwrap_or(500);

    // Model config
    let d_model: usize = args
        .iter()
        .position(|x| x == "--d-model")
        .map(|i| args[i + 1].parse().unwrap_or(512))
        .unwrap_or(512);

    let n_layers: usize = args
        .iter()
        .position(|x| x == "--layers")
        .map(|i| args[i + 1].parse().unwrap_or(6))
        .unwrap_or(6);

    let n_heads: usize = args
        .iter()
        .position(|x| x == "--heads")
        .map(|i| args[i + 1].parse().unwrap_or(8))
        .unwrap_or(8);

    // Initialize device
    println!("Initializing device...");
    let device = get_device()?;
    match &device {
        Device::Cuda(_) => println!("  ✅ Using CUDA GPU"),
        Device::Metal(_) => println!("  ✅ Using Metal GPU"),
        Device::Cpu => println!("  ⚠️  Using CPU (no GPU acceleration)"),
    }
    println!();

    // Load tokenizer
    println!("Initializing tokenizer...");
    let tokenizer = SimpleBPE::new();
    let vocab_size = tokenizer.vocab_size();
    println!("  Vocab size: {}", vocab_size);

    // Load and tokenize data
    println!("Loading data from {:?}...", data_path);
    let text = fs::read_to_string(&data_path)?;
    let tokens = tokenizer.encode(&text);
    println!("  Text length: {} chars", text.len());
    println!("  Token length: {} tokens", tokens.len());
    println!();

    // Create training config
    let train_config = GpuTrainConfig {
        lr,
        seq_len,
        max_steps,
        log_every,
        eval_every,
        save_every,
        ..Default::default()
    };

    // Print configuration
    println!("Model Configuration:");
    println!("  d_model: {}", d_model);
    println!("  n_layers: {}", n_layers);
    println!("  n_heads: {}", n_heads);
    println!("  vocab_size: {}", vocab_size);
    let d_state = 16;
    let memory_slots = 64;
    let attention_ratio = 1; // 1:7 attention to SSM ratio
    println!("  d_state: {} (SSM state dimension)", d_state);
    println!("  memory_slots: {}", memory_slots);
    println!("  attention_ratio: 1:{} (attention:SSM)", 7);
    println!();

    println!("Training Configuration:");
    println!("  max_steps: {}", max_steps);
    println!("  seq_len: {}", seq_len);
    println!("  learning_rate: {}", lr);
    println!("  log_every: {}", log_every);
    println!("  eval_every: {}", eval_every);
    println!("  save_every: {}", save_every);
    println!();

    // Create trainer and model
    println!("Creating model and trainer...");
    let mut trainer = GpuTrainer::new(train_config)?;

    let model = HybridNexusLM::new(
        d_model,
        n_heads,
        d_state,
        vocab_size,
        n_layers,
        memory_slots,
        attention_ratio,
        trainer.var_builder(),
    )?;

    // Estimate parameters
    let param_count = estimate_params(d_model, n_layers, n_heads, vocab_size, d_state, memory_slots);
    println!("  Parameters: ~{}", format_params(param_count));
    println!();

    // Create output directory
    fs::create_dir_all(&output_dir)?;

    // Prepare data
    let data_preparer = DataPreparer::new(device.clone());
    let sequences = data_preparer.create_sequences(&tokens, seq_len + 1, seq_len / 2);
    println!("  Training sequences: {}", sequences.len());

    // Split into train/val (90/10)
    let split = (sequences.len() * 9) / 10;
    let train_sequences = &sequences[..split];
    let val_sequences = &sequences[split..];
    println!("  Train sequences: {}", train_sequences.len());
    println!("  Val sequences: {}", val_sequences.len());
    println!();

    // Training loop
    println!("Starting training...");
    println!("{}", "═".repeat(70));

    let mut metrics = MetricsTracker::new();
    let mut rng_idx = 0usize;
    let start_time = Instant::now();
    let mut tokens_processed: u64 = 0;

    let pb = ProgressBar::new(max_steps as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} | Loss: {msg}")
            .unwrap()
            .progress_chars("#>-"),
    );

    let mut consecutive_best = 0;

    for step in 1..=max_steps {
        // Get training batch
        let seq_idx = rng_idx % train_sequences.len();
        rng_idx = rng_idx.wrapping_add(7919); // Prime stride for pseudo-random

        let (start, end) = train_sequences[seq_idx];
        let batch_tokens = &tokens[start..end];

        // Prepare input/target
        let (input_tensor, target_tensor) = data_preparer.prepare_batch(batch_tokens, seq_len)?;
        tokens_processed += input_tensor.dims()[0] as u64;

        // Training step
        let loss = trainer.train_step(&model, &input_tensor, &target_tensor)?;

        // Log metrics
        metrics.log_train(step, loss, trainer.current_lr());

        // Update progress bar
        if step % log_every == 0 {
            let avg_loss = metrics.avg_loss(log_every);
            let ppl = metrics.perplexity(log_every);
            pb.set_message(format!("{:.4} | PPL: {:.2}", avg_loss, ppl));
        }
        pb.set_position(step as u64);

        // Evaluation
        if step % eval_every == 0 {
            let mut val_loss_sum = 0.0;
            let val_count = val_sequences.len().min(50);

            for i in 0..val_count {
                let (start, end) = val_sequences[i];
                let batch_tokens = &tokens[start..end];
                let (input_tensor, target_tensor) =
                    data_preparer.prepare_batch(batch_tokens, seq_len)?;

                let vloss = trainer.eval_step(&model, &input_tensor, &target_tensor)?;
                val_loss_sum += vloss;
            }

            let val_loss = val_loss_sum / val_count as f32;
            let val_ppl = val_loss.exp();
            metrics.log_val(val_loss);

            let is_best = trainer.update_best(val_loss);
            if is_best {
                consecutive_best += 1;
            } else {
                consecutive_best = 0;
            }

            pb.suspend(|| {
                print!("\n📊 Step {} | ", step);
                print!("Train: {:.4} (PPL {:.2}) | ", metrics.avg_loss(eval_every), metrics.perplexity(eval_every));
                print!("Val: {:.4} (PPL {:.2})", val_loss, val_ppl);
                if is_best {
                    print!(" ⭐ NEW BEST!");
                }
                println!(" | LR: {:.2e}", trainer.current_lr());
            });
        }

        // Save checkpoint
        if step % save_every == 0 {
            let ckpt_path = PathBuf::from(&output_dir).join(format!("step_{}.safetensors", step));
            trainer.save_checkpoint(&ckpt_path)?;

            // Also save as best if it is
            if trainer.best_val_loss() == metrics.last_val_loss().unwrap_or(f32::INFINITY) {
                let best_path = PathBuf::from(&output_dir).join("best.safetensors");
                trainer.save_checkpoint(&best_path)?;
            }
        }

        // Generate sample periodically
        if step % (save_every * 2) == 0 {
            pb.suspend(|| {
                println!("\n📝 Sample generations:");
                let prompts = ["The ", "To be", "What is"];
                for prompt in prompts {
                    let prompt_tokens = tokenizer.encode(prompt);
                    match generate(&model, &prompt_tokens, 30, 0.8, &device) {
                        Ok(gen_tokens) => {
                            let text = tokenizer.decode(&gen_tokens);
                            println!("   \"{}\"", text.trim());
                        }
                        Err(e) => println!("   (generation error: {})", e),
                    }
                }
                println!();
            });
        }
    }

    pb.finish_with_message("Training complete!");

    let elapsed = start_time.elapsed();
    let throughput = tokens_processed as f64 / elapsed.as_secs_f64();

    println!();
    println!("{}", "═".repeat(70));
    println!();
    println!("╔═══════════════════════════════════════════════════════════════════╗");
    println!("║                      TRAINING COMPLETE                            ║");
    println!("╠═══════════════════════════════════════════════════════════════════╣");
    println!("║  Steps:            {:>8}                                       ║", max_steps);
    println!("║  Time:             {:>8.1}s                                      ║", elapsed.as_secs_f64());
    println!("║  Tokens:           {:>8}                                       ║", tokens_processed);
    println!("║  Throughput:       {:>8.0} tok/s                                ║", throughput);
    println!("║  Best Val Loss:    {:>8.4}                                      ║", trainer.best_val_loss());
    println!("║  Best Val PPL:     {:>8.2}                                      ║", trainer.best_val_loss().exp());
    println!("╚═══════════════════════════════════════════════════════════════════╝");
    println!();

    // Final generation samples
    println!("📝 Final sample generations:");
    let prompts = [
        "The king",
        "To be or not",
        "What light through",
        "Friends, Romans",
    ];
    for prompt in prompts {
        let prompt_tokens = tokenizer.encode(prompt);
        match generate(&model, &prompt_tokens, 50, 0.7, &device) {
            Ok(gen_tokens) => {
                let text = tokenizer.decode(&gen_tokens);
                println!("   \"{}\"", text.trim());
            }
            Err(e) => println!("   (generation error: {})", e),
        }
    }

    // Save final checkpoint
    let final_path = PathBuf::from(&output_dir).join("final.safetensors");
    trainer.save_checkpoint(&final_path)?;

    println!();
    println!("Checkpoints saved to: {}", output_dir);

    Ok(())
}

fn estimate_params(
    d_model: usize,
    n_layers: usize,
    n_heads: usize,
    vocab_size: usize,
    d_state: usize,
    memory_slots: usize,
) -> usize {
    let d_ff = d_model * 4;
    let d_inner = d_model * 2; // expand = 2

    // Embedding
    let embed = vocab_size * d_model;

    // Per hybrid block (attention or SSM + MLP)
    let attn = d_model * d_model * 4 + d_model * 2; // Q,K,V,O + norms
    let ssm = d_model * d_inner * 2 + d_inner * d_state + d_inner * (d_state * 2 + 1) + d_state * d_inner + d_inner;
    let mlp = d_model * d_ff * 3 + d_model * 2; // gate, up, down + norms

    // Assume 1:7 ratio
    let n_attn = n_layers / 8;
    let n_ssm = n_layers - n_attn;
    let blocks = n_attn * (attn + mlp) + n_ssm * (ssm + mlp);

    // Memory
    let memory = memory_slots * d_model * 2 + d_model * d_model * 4;

    // Output
    let output = d_model * vocab_size + d_model * 2;

    embed + blocks + memory + output
}

fn format_params(n: usize) -> String {
    if n >= 1_000_000_000 {
        format!("{:.2}B", n as f64 / 1_000_000_000.0)
    } else if n >= 1_000_000 {
        format!("{:.2}M", n as f64 / 1_000_000.0)
    } else if n >= 1_000 {
        format!("{:.2}K", n as f64 / 1_000.0)
    } else {
        n.to_string()
    }
}
