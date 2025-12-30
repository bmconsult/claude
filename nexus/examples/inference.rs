//! Inference with Trained Nexus Model
//!
//! Load a trained checkpoint and generate text interactively.
//!
//! Usage: cargo run --example inference --release -- [checkpoint_path]

use std::io::{self, Write};
use nexus::{
    DifferentiableHybridNexusLM, HybridModelCheckpoint,
    SamplingConfig, Sampler,
};

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

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════════════╗");
    println!("║              NEXUS INFERENCE                                  ║");
    println!("║         Interactive Text Generation                           ║");
    println!("╚═══════════════════════════════════════════════════════════════╝\n");

    // Get checkpoint path from args or use default
    let args: Vec<String> = std::env::args().collect();
    let checkpoint_path = if args.len() > 1 {
        args[1].clone()
    } else {
        "checkpoints/nexus_production/best.bin".to_string()
    };

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

    let n_params = model.num_parameters();
    println!("   Parameters: {} ({:.2}M)\n", n_params, n_params as f32 / 1e6);

    // Sampling config
    let sampling_config = SamplingConfig {
        temperature: 0.8,
        top_k: 40,
        top_p: 0.95,
        repetition_penalty: 1.1,
        greedy: false,
        seed: None,
    };
    let mut sampler = Sampler::new(sampling_config);

    println!("⚙️  Sampling: temp={}, top_k={}, top_p={}, rep_penalty={}\n",
             0.8, 40, 0.95, 1.1);

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

        let generated = generate(&model, prompt, 200, &mut sampler);
        println!("\n{}\n", generated);
    }

    println!("\nGoodbye!");
    Ok(())
}
