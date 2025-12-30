//! Train DifferentiableNexusLM on real text
//!
//! This example demonstrates training the full NexusLM architecture
//! with autograd on real text data using tiktoken tokenization.

use std::time::Instant;
use nexus::{DifferentiableNexusLM, NexusConfig, TiktokenBPE, AdamW};

fn main() -> anyhow::Result<()> {
    println!("╔══════════════════════════════════════════════════╗");
    println!("║   Nexus Transformer Training                     ║");
    println!("║   Full Architecture with Autograd                ║");
    println!("╚══════════════════════════════════════════════════╝\n");

    // Training configuration
    let d_model = 128;
    let n_heads = 4;
    let n_layers = 4;
    let vocab_size = 512;  // Small vocab for demo
    let seq_len = 64;
    let epochs = 100;
    let lr = 0.001;

    let config = NexusConfig {
        d_model,
        n_heads,
        layers_per_block: n_layers,
        vocab_size,
        max_seq_len: seq_len,
        ..Default::default()
    };

    println!("Configuration:");
    println!("  d_model: {}", d_model);
    println!("  n_heads: {}", n_heads);
    println!("  n_layers: {}", n_layers);
    println!("  vocab_size: {}", vocab_size);
    println!("  seq_len: {}", seq_len);
    println!("  lr: {}", lr);

    // Create model
    let model = DifferentiableNexusLM::new(config);
    println!("  Parameters: {}\n", model.num_parameters());

    // Training data - Shakespeare sample
    let corpus = r#"
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die: to sleep;
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to, 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep: perchance to dream: ay, there's the rub;
For in that sleep of death what dreams may come
When we have shuffled off this mortal coil,
Must give us pause: there's the respect
That makes calamity of so long life;
"#;

    // Tokenize with simple byte encoding for demo (maps bytes to 0-255)
    let tokens: Vec<u32> = corpus.bytes().map(|b| b as u32).collect();
    println!("Training on: {} chars, {} tokens", corpus.len(), tokens.len());

    // Create training sequences
    let mut sequences: Vec<Vec<u32>> = Vec::new();
    for i in 0..tokens.len().saturating_sub(seq_len) {
        if i % 16 == 0 {  // Don't overlap too much
            sequences.push(tokens[i..i+seq_len].to_vec());
        }
    }
    println!("Training sequences: {}\n", sequences.len());

    // Optimizer
    let mut optimizer = AdamW::new(lr, 0.01);

    println!("Training...\n");
    let start = Instant::now();
    let mut prev_loss = f32::MAX;

    for epoch in 0..epochs {
        let mut epoch_loss = 0.0;
        let mut n_batches = 0;

        for seq in &sequences {
            model.zero_grad();

            // Forward pass
            let input_tokens = &seq[..seq.len()-1];
            let logits = model.forward(&input_tokens.iter().map(|&x| x).collect::<Vec<_>>());

            // Compute cross-entropy loss
            let targets: Vec<usize> = seq[1..].iter().map(|&t| t as usize).collect();
            let (loss, loss_var) = logits.cross_entropy_loss(&targets);

            // Backward pass
            loss_var.backward();

            // Update weights
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

                    let update = optimizer.get_update(param.id, &clipped_grad, &param_data);
                    param.apply_update(&(-&update));
                }
            }

            epoch_loss += loss;
            n_batches += 1;
        }

        let avg_loss = epoch_loss / n_batches as f32;

        if epoch % 10 == 0 || epoch == epochs - 1 {
            let perplexity = avg_loss.exp();
            let delta = if prev_loss < f32::MAX { prev_loss - avg_loss } else { 0.0 };
            println!("Epoch {:3}: loss={:.4}, ppl={:.2}, Δ={:+.4}",
                     epoch + 1, avg_loss, perplexity, delta);
            prev_loss = avg_loss;
        }
    }

    let elapsed = start.elapsed();
    println!("\nTraining completed in {:.2}s ({:.2} epochs/sec)",
             elapsed.as_secs_f32(),
             epochs as f32 / elapsed.as_secs_f32());

    // Test generation
    println!("\n--- Generation Test ---");
    let prompt = "To be";
    let prompt_tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();

    print!("Prompt: \"{}\" -> ", prompt);

    // Greedy generation
    let mut generated = prompt_tokens.clone();
    for _ in 0..50 {
        let logits = model.forward(&generated);
        let logits_data = logits.data();
        let (_, seq_len, vocab_size) = logits_data.dim();

        // Get argmax of last position
        let mut max_idx = 0;
        let mut max_val = f32::NEG_INFINITY;
        for v in 0..vocab_size {
            let val = logits_data[[0, seq_len - 1, v]];
            if val > max_val {
                max_val = val;
                max_idx = v;
            }
        }
        generated.push(max_idx as u32);

        // Stop at newline
        if max_idx == 10 {
            break;
        }
    }

    // Decode
    let output: String = generated.iter()
        .map(|&b| b as u8 as char)
        .collect();
    println!("\"{}\"", output);

    println!("\n✓ Full NexusLM training complete!");

    Ok(())
}
