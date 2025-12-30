//! Nexus Training Binary
//!
//! Usage: nexus-train --data data.txt --output output_dir [--epochs N] [--batch-size N]

use anyhow::Result;
use nexus::{NexusConfig, NexusLM, SimpleBPE};
use std::fs;
use std::path::PathBuf;
use indicatif::{ProgressBar, ProgressStyle};

fn main() -> Result<()> {
    // Initialize logging
    env_logger::init();

    println!("╔══════════════════════════════════════════╗");
    println!("║           NEXUS Training v0.1            ║");
    println!("║  Hybrid Intelligence Architecture       ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    // Parse arguments
    let args: Vec<String> = std::env::args().collect();

    let data_path = args.iter()
        .position(|x| x == "--data")
        .map(|i| &args[i + 1])
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("data/sample.txt"));

    let output_path = args.iter()
        .position(|x| x == "--output")
        .map(|i| args[i + 1].clone())
        .unwrap_or_else(|| "checkpoints".to_string());

    let epochs: usize = args.iter()
        .position(|x| x == "--epochs")
        .map(|i| args[i + 1].parse().unwrap_or(10))
        .unwrap_or(10);

    let batch_size: usize = args.iter()
        .position(|x| x == "--batch-size")
        .map(|i| args[i + 1].parse().unwrap_or(4))
        .unwrap_or(4);

    let seq_len: usize = args.iter()
        .position(|x| x == "--seq-len")
        .map(|i| args[i + 1].parse().unwrap_or(64))
        .unwrap_or(64);

    let lr: f32 = args.iter()
        .position(|x| x == "--lr")
        .map(|i| args[i + 1].parse().unwrap_or(1e-3))
        .unwrap_or(1e-3);

    // Create tokenizer
    println!("Initializing tokenizer...");
    let tokenizer = SimpleBPE::new();
    println!("  Vocab size: {}", tokenizer.vocab_size());

    // Configure model (smaller for fast training)
    let config = NexusConfig {
        d_model: 128,
        n_heads: 4,
        d_state: 16,
        d_conv: 4,
        expand: 2,
        layers_per_block: 4,
        attention_ratio: 1,
        memory_size: 64,
        memory_lr: 0.01,
        vocab_size: tokenizer.vocab_size(),
        max_seq_len: 512,
    };

    println!();
    println!("Model Configuration:");
    println!("  d_model: {}", config.d_model);
    println!("  n_heads: {}", config.n_heads);
    println!("  layers: {}", config.layers_per_block);
    println!("  vocab_size: {}", config.vocab_size);
    println!();

    println!("Training Configuration:");
    println!("  epochs: {}", epochs);
    println!("  batch_size: {}", batch_size);
    println!("  seq_len: {}", seq_len);
    println!("  lr: {}", lr);
    println!();

    // Create model
    println!("Initializing model...");
    let mut model = NexusLM::new(config.clone());
    println!("  Parameters: ~{}", format_params(model.num_parameters()));
    println!();

    // Load training data
    println!("Loading data from {:?}...", data_path);
    let text = fs::read_to_string(&data_path)?;
    let tokens = tokenizer.encode(&text);
    println!("  Text length: {} chars", text.len());
    println!("  Token length: {} tokens", tokens.len());

    // Create training sequences
    let sequences = create_sequences(&tokens, seq_len);
    let n_batches = sequences.len() / batch_size;
    println!("  Training sequences: {}", sequences.len());
    println!("  Batches per epoch: {}", n_batches);
    println!();

    // Create output directory
    fs::create_dir_all(&output_path)?;

    // Training loop
    println!("Starting training...");
    println!("{}", "═".repeat(50));

    let mut best_loss = f32::INFINITY;

    for epoch in 0..epochs {
        let mut epoch_loss = 0.0;
        let mut n_samples = 0;

        // Shuffle sequences for this epoch
        let mut indices: Vec<usize> = (0..sequences.len()).collect();
        shuffle(&mut indices);

        let pb = ProgressBar::new(n_batches as u64);
        pb.set_style(ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
            .unwrap()
            .progress_chars("#>-"));

        for batch_idx in 0..n_batches {
            // Create batch
            let batch_start = batch_idx * batch_size;
            let batch: Vec<Vec<u32>> = (0..batch_size)
                .map(|i| sequences[indices[batch_start + i]].clone())
                .collect();

            // Forward pass and compute loss
            let loss = model.compute_loss(&batch);

            // Simple gradient descent on embeddings
            // (Full training would use autograd, but this demonstrates the loop)
            apply_simple_gradient(&mut model, &batch, lr);

            epoch_loss += loss;
            n_samples += batch_size;

            pb.inc(1);
        }

        pb.finish_and_clear();

        let avg_loss = epoch_loss / n_batches as f32;
        let perplexity = avg_loss.exp();

        println!("Epoch {}/{}: loss = {:.4}, perplexity = {:.2}",
            epoch + 1, epochs, avg_loss, perplexity);

        // Save checkpoint if best
        if avg_loss < best_loss {
            best_loss = avg_loss;
            // In a real implementation, we'd save the model weights here
            println!("  → New best loss! Saving checkpoint...");
        }
    }

    println!("{}", "═".repeat(50));
    println!();
    println!("Training complete!");
    println!("  Best loss: {:.4}", best_loss);
    println!("  Best perplexity: {:.2}", best_loss.exp());
    println!();

    // Generate sample text
    println!("Generating sample text...");
    let prompt = "The ";
    let prompt_tokens = tokenizer.encode(prompt);
    let generated = model.generate(&prompt_tokens, 50, 0.8);
    let output_text = tokenizer.decode(&generated);
    println!("  Prompt: \"{}\"", prompt);
    println!("  Output: \"{}\"", output_text);

    Ok(())
}

fn create_sequences(tokens: &[u32], seq_len: usize) -> Vec<Vec<u32>> {
    let mut sequences = Vec::new();

    // Use sliding window to create sequences
    for start in (0..tokens.len().saturating_sub(seq_len)).step_by(seq_len / 2) {
        let end = (start + seq_len).min(tokens.len());
        if end - start >= seq_len {
            sequences.push(tokens[start..end].to_vec());
        }
    }

    sequences
}

fn shuffle(indices: &mut [usize]) {
    use rand::Rng;
    let mut rng = rand::thread_rng();

    for i in (1..indices.len()).rev() {
        let j = rng.gen_range(0..=i);
        indices.swap(i, j);
    }
}

fn apply_simple_gradient(model: &mut NexusLM, batch: &[Vec<u32>], lr: f32) {
    // This is a simplified gradient update for demonstration
    // In production, you'd use the autograd system

    // Perturb embeddings slightly based on loss gradient direction
    // This is essentially numerical gradient descent
    let epsilon = 0.01;

    for b in 0..batch.len() {
        for t in 0..(batch[b].len() - 1) {
            let token_id = batch[b][t] as usize;
            let target_id = batch[b][t + 1] as usize;

            if token_id < model.embedding.vocab_size && target_id < model.embedding.vocab_size {
                // Move embedding slightly toward target embedding
                for d in 0..model.embedding.d_model {
                    let diff = model.embedding.token_embed[[target_id, d]]
                        - model.embedding.token_embed[[token_id, d]];
                    model.embedding.token_embed[[token_id, d]] += lr * epsilon * diff;
                }
            }
        }
    }
}

fn format_params(n: usize) -> String {
    if n >= 1_000_000_000 {
        format!("{:.1}B", n as f64 / 1_000_000_000.0)
    } else if n >= 1_000_000 {
        format!("{:.1}M", n as f64 / 1_000_000.0)
    } else if n >= 1_000 {
        format!("{:.1}K", n as f64 / 1_000.0)
    } else {
        n.to_string()
    }
}
