//! Inference with Trained Nexus Model
//!
//! Load a trained checkpoint and generate text interactively.
//! Supports both standard and KV-cached inference modes.
//!
//! Usage: cargo run --example inference --release -- [checkpoint_path] [--cached]

use std::io::{self, Write};
use std::time::Instant;
use nexus::{
    DifferentiableHybridNexusLM, HybridModelCheckpoint,
    SamplingConfig, Sampler,
};

/// Standard generation (recomputes full sequence each token)
fn generate(
    model: &DifferentiableHybridNexusLM,
    prompt: &str,
    max_tokens: usize,
    sampler: &mut Sampler,
) -> String {
    let mut tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();

    for _ in 0..max_tokens {
        let logits = model.forward(&tokens);
        let logits_data = logits.data();
        let seq_len = tokens.len();

        // Get logits for last position
        let last_logits: Vec<f32> = (0..256)
            .map(|v| logits_data[[0, seq_len - 1, v]])
            .collect();

        let next_token = sampler.sample(&last_logits, &tokens);
        tokens.push(next_token);

        // Stop on newline or null
        if next_token == b'\n' as u32 || next_token == 0 {
            break;
        }
    }

    tokens.iter()
        .filter_map(|&t| if t < 128 { Some(t as u8 as char) } else { None })
        .collect()
}

/// KV-cached generation (O(1) per token after prefill)
fn generate_cached(
    model: &DifferentiableHybridNexusLM,
    prompt: &str,
    max_tokens: usize,
    sampler: &mut Sampler,
    vocab_size: usize,
) -> String {
    let mut cache = model.create_cache();
    let prompt_tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
    let mut all_tokens = prompt_tokens.clone();

    // Prefill: process full prompt at once
    let logits = model.forward_cached(&prompt_tokens, &mut cache);
    let logits_data = logits.data();
    let seq_len = prompt_tokens.len();

    // Get logits for last position
    let mut last_logits: Vec<f32> = (0..vocab_size)
        .map(|v| logits_data[[0, seq_len - 1, v]])
        .collect();

    // Decode: generate one token at a time
    for _ in 0..max_tokens {
        let next_token = sampler.sample(&last_logits, &all_tokens);
        all_tokens.push(next_token);

        // Stop on newline or null
        if next_token == b'\n' as u32 || next_token == 0 {
            break;
        }

        // Forward only the new token
        let logits = model.forward_cached(&[next_token], &mut cache);
        let logits_data = logits.data();

        // Get logits (only position 0 since we passed 1 token)
        last_logits = (0..vocab_size)
            .map(|v| logits_data[[0, 0, v]])
            .collect();
    }

    all_tokens.iter()
        .filter_map(|&t| if t < 128 { Some(t as u8 as char) } else { None })
        .collect()
}

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════════════╗");
    println!("║              NEXUS INFERENCE                                  ║");
    println!("║         Interactive Text Generation                           ║");
    println!("╚═══════════════════════════════════════════════════════════════╝\n");

    // Parse args
    let args: Vec<String> = std::env::args().collect();
    let use_cache = args.iter().any(|a| a == "--cached");
    let checkpoint_path = args.iter()
        .find(|a| !a.starts_with("-") && *a != &args[0])
        .cloned()
        .unwrap_or_else(|| "checkpoints/nexus_production/best.bin".to_string());

    println!("📂 Loading checkpoint: {}", checkpoint_path);

    let checkpoint = HybridModelCheckpoint::load(&checkpoint_path)
        .map_err(|e| anyhow::anyhow!("{}", e))?;
    println!("   Step: {}", checkpoint.step);
    println!("   Loss: {:.4}", checkpoint.loss);
    println!("   Config: d_model={}, layers={}",
             checkpoint.config.d_model,
             checkpoint.config.layers_per_block);

    let model = DifferentiableHybridNexusLM::new(checkpoint.config.clone());
    checkpoint.load_into(&model)
        .map_err(|e| anyhow::anyhow!("{}", e))?;

    let vocab_size = checkpoint.config.vocab_size;
    let n_params = model.num_parameters();
    println!("   Parameters: {} ({:.2}M)\n", n_params, n_params as f32 / 1e6);

    // Sampling config with all fields
    let sampling_config = SamplingConfig {
        temperature: 0.8,
        top_k: 40,
        top_p: 0.95,
        min_p: 0.05,
        repetition_penalty: 1.1,
        repetition_window: 64,
        presence_penalty: 0.0,
        frequency_penalty: 0.0,
        greedy: false,
        seed: None,
    };
    let mut sampler = Sampler::new(sampling_config);

    println!("⚙️  Sampling: temp={}, top_k={}, top_p={}, rep_penalty={}",
             0.8, 40, 0.95, 1.1);

    if use_cache {
        println!("🚀 KV-Cache: ENABLED (O(1) per token)\n");
    } else {
        println!("📝 KV-Cache: disabled (use --cached to enable)\n");
    }

    println!("Enter prompts (empty line to quit):\n");

    loop {
        print!("> ");
        io::stdout().flush()?;

        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let prompt = input.trim();

        if prompt.is_empty() {
            break;
        }

        let start = Instant::now();
        let generated = if use_cache {
            generate_cached(&model, prompt, 200, &mut sampler, vocab_size)
        } else {
            generate(&model, prompt, 200, &mut sampler)
        };
        let elapsed = start.elapsed();

        let gen_tokens = generated.len().saturating_sub(prompt.len());
        let tok_per_sec = if elapsed.as_secs_f32() > 0.0 {
            gen_tokens as f32 / elapsed.as_secs_f32()
        } else {
            0.0
        };

        println!("\n{}", generated);
        println!("   [{} tokens in {:.2}s = {:.1} tok/s]\n",
                 gen_tokens, elapsed.as_secs_f32(), tok_per_sec);
    }

    println!("\nGoodbye!");
    Ok(())
}
