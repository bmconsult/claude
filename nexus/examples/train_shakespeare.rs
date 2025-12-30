//! Train DifferentiableNexusLM on TinyShakespeare
//!
//! Full training with byte-level tokenization and cosine LR schedule.

use std::fs;
use std::time::Instant;
use nexus::{DifferentiableNexusLM, NexusConfig, AdamW};

/// Cosine learning rate schedule with warmup
fn get_lr(step: usize, warmup_steps: usize, max_steps: usize, max_lr: f32, min_lr: f32) -> f32 {
    if step < warmup_steps {
        // Linear warmup
        max_lr * (step as f32 / warmup_steps as f32)
    } else {
        // Cosine decay
        let progress = (step - warmup_steps) as f32 / (max_steps - warmup_steps) as f32;
        let cosine = 0.5 * (1.0 + (std::f32::consts::PI * progress).cos());
        min_lr + (max_lr - min_lr) * cosine
    }
}

fn main() -> anyhow::Result<()> {
    println!("╔══════════════════════════════════════════════════╗");
    println!("║   Nexus Shakespeare Training                     ║");
    println!("║   Full Transformer - Byte-level                  ║");
    println!("╚══════════════════════════════════════════════════╝\n");

    // Load data
    let data_path = "data/shakespeare.txt";
    let corpus = fs::read_to_string(data_path)?;
    println!("Loaded {} chars from {}", corpus.len(), data_path);

    // Byte-level tokenization (fast, 256 vocab)
    let tokens: Vec<u32> = corpus.bytes().map(|b| b as u32).collect();
    println!("Tokenized to {} tokens (byte-level)\n", tokens.len());

    // Training configuration - optimized for CPU
    let d_model = 192;
    let n_heads = 6;
    let n_layers = 4;
    let vocab_size = 256;  // byte-level
    let seq_len = 128;
    let batch_size = 8;
    let epochs = 2;
    let max_lr = 1e-3;
    let min_lr = 1e-5;
    let warmup_steps = 50;
    let log_interval = 20;
    let eval_interval = 100;

    let config = NexusConfig {
        d_model,
        n_heads,
        layers_per_block: n_layers,
        vocab_size,
        max_seq_len: seq_len,
        ..Default::default()
    };

    println!("Model Configuration:");
    println!("  d_model: {}", d_model);
    println!("  n_heads: {}", n_heads);
    println!("  n_layers: {}", n_layers);
    println!("  seq_len: {}", seq_len);
    println!("  batch_size: {}", batch_size);
    println!("  epochs: {}", epochs);
    println!("  max_lr: {}", max_lr);

    // Create model
    let model = DifferentiableNexusLM::new(config);
    let n_params = model.num_parameters();
    println!("  Parameters: {} ({:.2}M)\n", n_params, n_params as f32 / 1e6);

    // Create training batches
    let n_sequences = (tokens.len() - seq_len) / (seq_len / 2);  // 50% overlap
    let steps_per_epoch = n_sequences / batch_size;
    let total_steps = epochs * steps_per_epoch;

    println!("Training:");
    println!("  Sequences: {}", n_sequences);
    println!("  Steps/epoch: {}", steps_per_epoch);
    println!("  Total steps: {}\n", total_steps);

    // Optimizer
    let mut optimizer = AdamW::new(max_lr, 0.01);

    println!("Starting training...\n");
    let start = Instant::now();
    let mut global_step = 0;
    let mut running_loss = 0.0;
    let mut running_count = 0;

    for epoch in 0..epochs {
        let epoch_start = Instant::now();

        for step in 0..steps_per_epoch {
            // Get learning rate with schedule
            let lr = get_lr(global_step, warmup_steps, total_steps, max_lr, min_lr);

            // Create batch
            let mut batch_loss = 0.0;

            for b in 0..batch_size {
                let start_idx = ((step * batch_size + b) * (seq_len / 2)) % (tokens.len() - seq_len);
                let seq: Vec<u32> = tokens[start_idx..start_idx + seq_len].to_vec();

                model.zero_grad();

                // Forward pass
                let input_tokens: Vec<u32> = seq[..seq.len()-1].to_vec();
                let logits = model.forward(&input_tokens);

                // Compute loss
                let targets: Vec<usize> = seq[1..].iter().map(|&t| t as usize).collect();
                let (loss, loss_var) = logits.cross_entropy_loss(&targets);

                // Backward
                loss_var.backward();

                // Update with gradient clipping
                let params = model.parameters();
                for param in &params {
                    if let Some(grad) = param.get_grad() {
                        let param_data = param.data();

                        // Gradient clipping
                        let grad_norm: f32 = grad.iter().map(|x| x * x).sum::<f32>().sqrt();
                        let max_norm = 1.0;
                        let clipped_grad = if grad_norm > max_norm {
                            grad.mapv(|x| x * max_norm / grad_norm)
                        } else {
                            grad
                        };

                        // Scale by learning rate and batch size
                        let scaled_lr = lr / batch_size as f32;
                        let mut update = optimizer.get_update(param.id, &clipped_grad, &param_data);
                        update = &update * (scaled_lr / max_lr);  // Scale update by lr ratio
                        param.apply_update(&(-&update));
                    }
                }

                batch_loss += loss;
            }

            let avg_loss = batch_loss / batch_size as f32;
            running_loss += avg_loss;
            running_count += 1;
            global_step += 1;

            // Log progress
            if global_step % log_interval == 0 {
                let avg = running_loss / running_count as f32;
                let ppl = avg.exp();
                let elapsed = start.elapsed().as_secs_f32();
                let tokens_per_sec = (global_step * batch_size * seq_len) as f32 / elapsed;

                println!("Step {:5} | loss: {:.4} | ppl: {:7.2} | lr: {:.2e} | tok/s: {:.0}",
                         global_step, avg, ppl, lr, tokens_per_sec);

                running_loss = 0.0;
                running_count = 0;
            }

            // Generate sample
            if global_step % eval_interval == 0 {
                print!("  Sample: ");
                let prompt = "To be, or not to be";
                let prompt_tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
                let mut generated = prompt_tokens.clone();

                for _ in 0..50 {
                    let logits = model.forward(&generated);
                    let logits_data = logits.data();
                    let gen_len = generated.len();

                    // Sample with temperature
                    let temperature = 0.8;
                    let probs: Vec<f32> = (0..vocab_size)
                        .map(|v| logits_data[[0, gen_len - 1, v]] / temperature)
                        .collect();

                    let max_logit = probs.iter().cloned().fold(f32::NEG_INFINITY, f32::max);

                    // Top-k sampling (k=40)
                    let mut indices: Vec<usize> = (0..vocab_size).collect();
                    indices.sort_by(|&a, &b| probs[b].partial_cmp(&probs[a]).unwrap());

                    let top_k = 40;
                    let mut top_probs: Vec<f32> = indices[..top_k].iter()
                        .map(|&i| (probs[i] - max_logit).exp())
                        .collect();
                    let top_sum: f32 = top_probs.iter().sum();
                    for p in &mut top_probs {
                        *p /= top_sum;
                    }

                    // Sample
                    use rand::Rng;
                    let mut rng = rand::thread_rng();
                    let sample: f32 = rng.gen();
                    let mut cumsum = 0.0;
                    let mut next_token = indices[0] as u32;
                    for (i, &p) in top_probs.iter().enumerate() {
                        cumsum += p;
                        if sample <= cumsum {
                            next_token = indices[i] as u32;
                            break;
                        }
                    }

                    generated.push(next_token);
                }

                // Decode bytes to string
                let text: String = generated.iter()
                    .filter_map(|&b| {
                        if b < 128 { Some(b as u8 as char) } else { None }
                    })
                    .collect();
                println!("\"{}\"", text.chars().take(80).collect::<String>());
                println!();
            }
        }

        let epoch_time = epoch_start.elapsed().as_secs_f32();
        println!("\n--- Epoch {} completed in {:.1}s ---\n", epoch + 1, epoch_time);
    }

    let total_time = start.elapsed().as_secs_f32();
    println!("Training completed in {:.1}s", total_time);
    println!("Final tokens/sec: {:.0}", (total_steps * batch_size * seq_len) as f32 / total_time);

    // Save model
    println!("\n✓ Training complete!");

    Ok(())
}
