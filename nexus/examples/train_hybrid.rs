//! Train the full Hybrid Nexus model (Attention + SSM + Memory)
//!
//! This demonstrates training the complete architecture with:
//! - 1:7 Attention:SSM ratio (Jamba-style)
//! - Mamba-style selective state space layers
//! - Titans-style differentiable memory
//!
//! Usage: cargo run --example train_hybrid --release

use std::time::Instant;
use nexus::{
    DifferentiableHybridNexusLM, AdamW, Optimizer, NexusConfig,
};

fn main() {
    println!("═══════════════════════════════════════════════════════════════");
    println!("       Hybrid Nexus Training (Attention + SSM + Memory)");
    println!("═══════════════════════════════════════════════════════════════");

    // Training config - smaller for demo
    let config = NexusConfig {
        d_model: 128,       // Hidden dimension
        n_heads: 4,         // Attention heads
        d_state: 16,        // SSM state dimension
        d_conv: 4,          // SSM convolution width
        vocab_size: 256,    // Byte-level (ASCII)
        layers_per_block: 8,// 8 layers with 1:7 attn:SSM ratio
        attention_ratio: 1, // 1 attention per 8 layers
        memory_size: 64,    // Memory slots
        ..Default::default()
    };

    println!("\n Model Configuration:");
    println!("   d_model: {}", config.d_model);
    println!("   n_heads: {}", config.n_heads);
    println!("   d_state: {}", config.d_state);
    println!("   vocab_size: {}", config.vocab_size);
    println!("   layers: {} ({}:7 attn:SSM ratio)", config.layers_per_block, config.attention_ratio);
    println!("   memory_size: {}", config.memory_size);

    // Create model
    let model = DifferentiableHybridNexusLM::new(config.clone());
    let n_params = model.num_parameters();
    println!("   parameters: {}", n_params);

    // Count layer types
    let n_attn = model.blocks.iter().filter(|b| b.attn.is_some()).count();
    let n_ssm = model.blocks.iter().filter(|b| b.ssm.is_some()).count();
    println!("   attention layers: {}", n_attn);
    println!("   SSM layers: {}", n_ssm);

    // Simple training data
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
    let lr = 1e-3;
    let mut optimizer = AdamW::new(lr, 0.01);

    println!("\n Starting training...\n");

    let n_epochs = 100;
    let seq_len = 32;
    let mut total_tokens = 0;
    let start_time = Instant::now();

    for epoch in 0..n_epochs {
        let mut epoch_loss = 0.0;
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

            // Zero gradients
            model.zero_grad();

            // Forward pass (all but last token as input)
            let input_tokens: Vec<u32> = tokens[..tokens.len()-1].to_vec();
            let logits = model.forward(&input_tokens);

            // Compute cross-entropy loss using built-in
            let targets: Vec<usize> = tokens[1..].iter().map(|&t| t as usize).collect();
            let (loss, loss_var) = logits.cross_entropy_loss(&targets);

            // Backward pass
            loss_var.backward();

            // Update weights with gradient clipping
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

                    // Get update and apply
                    let update = optimizer.get_update(param.id, &clipped_grad, &param_data);
                    param.apply_update(&(-&update));
                }
            }

            epoch_loss += loss;
            n_batches += 1;
            total_tokens += tokens.len() - 1;
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
    println!("\n📝 Testing generation:\n");

    let prompts = vec!["Hello", "The", "Machine"];

    for prompt in prompts {
        print!("\"{}\" → ", prompt);

        let mut tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();

        // Generate 30 tokens
        for _ in 0..30 {
            let logits = model.forward(&tokens);
            let logits_data = logits.data();
            let seq = tokens.len();

            // Greedy sampling from last position
            let mut best_token = 0u32;
            let mut best_logit = f32::NEG_INFINITY;
            for v in 0..256 {
                if logits_data[[0, seq - 1, v]] > best_logit {
                    best_logit = logits_data[[0, seq - 1, v]];
                    best_token = v as u32;
                }
            }

            tokens.push(best_token);

            // Stop at newline
            if best_token == 10 {
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
    let checkpoint_path = format!("{}/hybrid_demo.bin", checkpoint_dir);

    println!("\n💾 Saving checkpoint to: {}", checkpoint_path);

    // Note: Need to create a checkpoint variant for hybrid model
    // For now, just show the model works
    println!("   (Checkpoint saving for hybrid model coming soon)");

    println!("\n✓ Hybrid architecture training demonstration complete!");
}
