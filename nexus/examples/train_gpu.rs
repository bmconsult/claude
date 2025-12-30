//! GPU Training Example using Candle
//!
//! Demonstrates training the Hybrid Nexus model on GPU (or CPU fallback)
//! using Candle's autograd and optimization.
//!
//! Usage:
//!   cargo run --example train_gpu --release
//!   cargo run --example train_gpu --release --features cuda   # For NVIDIA GPU
//!   cargo run --example train_gpu --release --features metal  # For Apple Silicon

use std::time::Instant;
use candle_core::{DType, Device, Result, Tensor};
use candle_nn::{VarMap, VarBuilder, Optimizer, AdamW, ParamsAdamW};

use nexus::gpu::{get_device, HybridNexusLM};

fn main() -> Result<()> {
    println!("═══════════════════════════════════════════════════════════════");
    println!("       GPU Training - Hybrid Nexus with Candle");
    println!("═══════════════════════════════════════════════════════════════");

    // Get best available device
    let device = get_device()?;
    println!("\nDevice: {:?}", device);

    // Model configuration (smaller for demo)
    let d_model = 128;
    let n_heads = 4;
    let d_state = 16;
    let vocab_size = 256;  // Byte-level
    let n_layers = 8;      // 1:7 attention:SSM ratio
    let memory_slots = 32;
    let attention_ratio = 1;

    // Create model with VarMap for training
    let varmap = VarMap::new();
    let vb = VarBuilder::from_varmap(&varmap, DType::F32, &device);

    let model = HybridNexusLM::new(
        d_model,
        n_heads,
        d_state,
        vocab_size,
        n_layers,
        memory_slots,
        attention_ratio,
        vb,
    )?;

    // Count parameters
    let n_params: usize = varmap.all_vars().iter().map(|v| v.elem_count()).sum();
    println!("\nModel Configuration:");
    println!("  d_model: {}", d_model);
    println!("  n_heads: {}", n_heads);
    println!("  n_layers: {} (1:{} attn:SSM)", n_layers, n_layers - attention_ratio);
    println!("  memory_slots: {}", memory_slots);
    println!("  parameters: {}", n_params);

    // Training data
    let texts = vec![
        "Hello world! This is a test of the Nexus hybrid architecture.",
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning models can learn from data.",
        "Neural networks process information in layers.",
        "State space models handle long sequences efficiently.",
        "Attention mechanisms capture global dependencies.",
        "Memory augmented networks remember previous context.",
        "Hybrid architectures combine the best of both worlds.",
    ];

    // Create optimizer
    let params = ParamsAdamW {
        lr: 1e-3,
        weight_decay: 0.01,
        ..Default::default()
    };
    let mut optimizer = AdamW::new(varmap.all_vars(), params)?;

    println!("\nStarting training...\n");

    let n_epochs = 50;
    let seq_len = 32;
    let mut total_tokens = 0usize;
    let start_time = Instant::now();

    for epoch in 0..n_epochs {
        let mut epoch_loss = 0.0f32;
        let mut n_batches = 0;

        for text in &texts {
            // Convert to tokens (byte-level)
            let tokens: Vec<u32> = text.bytes()
                .take(seq_len)
                .map(|b| b as u32)
                .collect();

            if tokens.len() < 4 {
                continue;
            }

            // Input: all but last token, Target: all but first token
            let input_tokens: Vec<u32> = tokens[..tokens.len()-1].to_vec();
            let target_tokens: Vec<u32> = tokens[1..].to_vec();

            let input = Tensor::new(&input_tokens[..], &device)?;
            let targets = Tensor::new(&target_tokens[..], &device)?.to_dtype(DType::U32)?;

            // Forward pass
            let logits = model.forward(&input)?;  // [seq, vocab]

            // Cross-entropy loss
            let loss = candle_nn::loss::cross_entropy(&logits, &targets)?;

            // Backward pass
            optimizer.backward_step(&loss)?;

            let loss_val = loss.to_scalar::<f32>()?;
            epoch_loss += loss_val;
            n_batches += 1;
            total_tokens += input_tokens.len();
        }

        epoch_loss /= n_batches as f32;

        if (epoch + 1) % 10 == 0 || epoch == 0 {
            let elapsed = start_time.elapsed().as_secs_f32();
            let tok_per_sec = total_tokens as f32 / elapsed;
            println!(
                "Epoch {:3}/{} | Loss: {:.4} | {:.0} tok/s",
                epoch + 1, n_epochs, epoch_loss, tok_per_sec
            );
        }
    }

    let elapsed = start_time.elapsed().as_secs_f32();
    let tok_per_sec = total_tokens as f32 / elapsed;

    println!("\n═══════════════════════════════════════════════════════════════");
    println!("   Training complete!");
    println!("   Total time: {:.1}s", elapsed);
    println!("   Tokens processed: {}", total_tokens);
    println!("   Throughput: {:.0} tok/s", tok_per_sec);
    println!("═══════════════════════════════════════════════════════════════");

    // Test generation
    println!("\nTesting generation:\n");

    let prompts = vec!["Hello", "The", "Machine"];

    for prompt in prompts {
        print!("\"{}\" -> ", prompt);

        let mut tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();

        // Generate 30 tokens
        for _ in 0..30 {
            let input = Tensor::new(&tokens[..], &device)?;
            let logits = model.forward(&input)?;

            // Get last position
            let seq_len = tokens.len();
            let last_logits = logits.narrow(0, seq_len - 1, 1)?.squeeze(0)?;  // [vocab]

            // Greedy sampling
            let next_token = last_logits
                .argmax(0)?
                .to_scalar::<u32>()?;

            tokens.push(next_token);

            // Stop at newline
            if next_token == 10 {
                break;
            }
        }

        // Decode
        let text: String = tokens.iter()
            .filter_map(|&b| {
                if b < 128 { Some(b as u8 as char) } else { None }
            })
            .collect();
        println!("\"{}\"", text);
    }

    // Save checkpoint
    let checkpoint_dir = "checkpoints";
    std::fs::create_dir_all(checkpoint_dir).ok();
    let checkpoint_path = format!("{}/gpu_hybrid.safetensors", checkpoint_dir);

    println!("\nSaving checkpoint to: {}", checkpoint_path);
    varmap.save(&checkpoint_path)?;
    println!("Checkpoint saved!");

    println!("\nGPU training demonstration complete!");

    Ok(())
}
