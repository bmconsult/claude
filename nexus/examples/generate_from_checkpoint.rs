//! Generate text from a saved checkpoint
//!
//! Usage: cargo run --example generate_from_checkpoint --release -- <checkpoint_path> [prompt]

use std::env;
use std::error::Error;
use nexus::{DifferentiableNexusLM, ModelCheckpoint};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();

    let checkpoint_path = args.get(1)
        .unwrap_or_else(|| {
            eprintln!("Usage: {} <checkpoint_path> [prompt]", args[0]);
            eprintln!("Example: {} checkpoints/final.bin \"To be or not\"", args[0]);
            std::process::exit(1);
        });

    let prompt = args.get(2)
        .map(|s| s.as_str())
        .unwrap_or("To be, or not to be");

    println!("Loading checkpoint from: {}", checkpoint_path);

    // Load checkpoint
    let checkpoint = ModelCheckpoint::load(checkpoint_path)?;
    println!("  Step: {}", checkpoint.step);
    println!("  Loss: {:.4}", checkpoint.loss);
    println!("  Config: {}d, {}h, {}L, {}V",
             checkpoint.config.d_model,
             checkpoint.config.n_heads,
             checkpoint.config.layers_per_block,
             checkpoint.config.vocab_size);

    // Create model and load weights
    let model = DifferentiableNexusLM::new(checkpoint.config.clone());
    checkpoint.load_into(&model).map_err(|e| -> Box<dyn Error> { e.into() })?;
    println!("\n✓ Model loaded\n");

    // Generate from prompt
    println!("Prompt: \"{}\"", prompt);
    println!("Generating...\n");

    // Tokenize (byte-level)
    let prompt_tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
    let mut generated = prompt_tokens.clone();

    // Generate 200 tokens
    let max_new_tokens = 200;
    let temperature = 0.8;
    let top_k = 40;
    let vocab_size = checkpoint.config.vocab_size;

    for _ in 0..max_new_tokens {
        // Forward pass
        let logits = model.forward(&generated);
        let logits_data = logits.data();
        let seq_len = generated.len();

        // Apply temperature
        let probs: Vec<f32> = (0..vocab_size)
            .map(|v| logits_data[[0, seq_len - 1, v]] / temperature)
            .collect();

        let max_logit = probs.iter().cloned().fold(f32::NEG_INFINITY, f32::max);

        // Top-k sampling
        let mut indices: Vec<usize> = (0..vocab_size).collect();
        indices.sort_by(|&a, &b| probs[b].partial_cmp(&probs[a]).unwrap());

        let mut top_probs: Vec<f32> = indices[..top_k.min(vocab_size)].iter()
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

        // Stop at newline after some output
        if next_token == 10 && generated.len() > prompt_tokens.len() + 10 {
            break;
        }
    }

    // Decode bytes to string
    let text: String = generated.iter()
        .filter_map(|&b| {
            if b < 128 { Some(b as u8 as char) } else { None }
        })
        .collect();

    let line = "─".repeat(60);
    println!("{}", line);
    println!("{}", text);
    println!("{}", line);
    println!("\n({} tokens generated)", generated.len() - prompt_tokens.len());

    Ok(())
}
