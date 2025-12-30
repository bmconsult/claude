//! Nexus Inference Binary
//!
//! Usage: nexus-infer --input "text to process" [--max-tokens N] [--temperature T]

use anyhow::Result;
use nexus::{NexusConfig, NexusLM, SimpleBPE};

fn main() -> Result<()> {
    println!("╔══════════════════════════════════════════╗");
    println!("║          NEXUS Inference v0.1            ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    // Parse arguments
    let args: Vec<String> = std::env::args().collect();

    let input_text = args.iter()
        .position(|x| x == "--input")
        .map(|i| args[i + 1].clone());

    let max_tokens: usize = args.iter()
        .position(|x| x == "--max-tokens")
        .map(|i| args[i + 1].parse().unwrap_or(50))
        .unwrap_or(50);

    let temperature: f32 = args.iter()
        .position(|x| x == "--temperature")
        .map(|i| args[i + 1].parse().unwrap_or(0.8))
        .unwrap_or(0.8);

    // Create tokenizer
    let tokenizer = SimpleBPE::new();

    // Configure model (same as training)
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

    // Create model
    println!("Loading model...");
    let mut model = NexusLM::new(config);
    println!("  Parameters: ~{}", format_params(model.num_parameters()));
    println!();

    // Process input
    if let Some(text) = input_text {
        println!("Input: \"{}\"", text);
        println!("Max tokens: {}", max_tokens);
        println!("Temperature: {}", temperature);
        println!();

        // Tokenize
        let prompt_tokens = tokenizer.encode(&text);
        println!("Tokens: {:?}", prompt_tokens);
        println!();

        // Generate
        println!("Generating...");
        let generated = model.generate(&prompt_tokens, max_tokens, temperature);

        // Decode
        let output_text = tokenizer.decode(&generated);
        println!();
        println!("Output: \"{}\"", output_text);

        // Memory statistics
        let mem_stats = model.core.memory.stats();
        println!();
        println!("Memory Statistics:");
        println!("  Entries: {}/{}", mem_stats.num_entries, mem_stats.capacity);
        println!("  Avg surprise: {:.4}", mem_stats.avg_surprise);
    } else {
        println!("No input provided. Use --input \"your text here\"");
        println!();
        println!("Examples:");
        println!("  nexus-infer --input \"The quick brown\"");
        println!("  nexus-infer --input \"Hello\" --max-tokens 100 --temperature 0.9");
    }

    Ok(())
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
