//! Nexus Inference Binary
//!
//! Usage: nexus-infer --model checkpoint.json --input "text to process"

use anyhow::Result;
use nexus::{Nexus, NexusConfig, Tensor};
use ndarray::Array3;

fn main() -> Result<()> {
    println!("╔══════════════════════════════════════════╗");
    println!("║          NEXUS Inference v0.1            ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    // Parse arguments
    let args: Vec<String> = std::env::args().collect();

    let model_path = args.iter()
        .position(|x| x == "--model")
        .map(|i| &args[i + 1]);

    let input_text = args.iter()
        .position(|x| x == "--input")
        .map(|i| &args[i + 1]);

    // Load or create model
    let config = NexusConfig::default();
    let mut model = Nexus::new(config);

    if let Some(path) = model_path {
        println!("Loading model from: {}", path);
        // Would load checkpoint here
    } else {
        println!("Using fresh model (no checkpoint loaded)");
    }

    // Process input
    if let Some(text) = input_text {
        println!("Input: {}", text);
        println!();

        // Tokenize and embed (placeholder)
        let input_tensor = text_to_tensor(text, &model);

        // Forward pass with memory updates
        println!("Processing...");
        let output = model.forward(&input_tensor, true);

        // Display output statistics
        let (batch, seq_len, d_model) = output.shape();
        let mean: f32 = output.data.iter().sum::<f32>() / output.data.len() as f32;
        let std: f32 = (output.data.iter()
            .map(|x| (x - mean).powi(2))
            .sum::<f32>() / output.data.len() as f32).sqrt();

        println!("Output shape: ({}, {}, {})", batch, seq_len, d_model);
        println!("Output mean: {:.4}", mean);
        println!("Output std: {:.4}", std);

        // Memory statistics
        let mem_stats = model.memory.stats();
        println!();
        println!("Memory Statistics:");
        println!("  Entries: {}/{}", mem_stats.num_entries, mem_stats.capacity);
        println!("  Avg surprise: {:.4}", mem_stats.avg_surprise);
        println!("  Avg age: {:.1}", mem_stats.avg_age);

    } else {
        println!("No input provided. Use --input \"your text here\"");
    }

    Ok(())
}

fn text_to_tensor(text: &str, model: &Nexus) -> Tensor {
    // Placeholder tokenization - in real implementation would use tokenizers crate
    let d_model = model.config.d_model;
    let seq_len = text.len().min(512);

    use rand_distr::{Normal, Distribution};

    let mut rng = rand::thread_rng();
    let normal = Normal::new(0.0, 1.0).unwrap();

    // Generate random embeddings (placeholder for real tokenization)
    let data = Array3::from_shape_fn((1, seq_len, d_model), |_| {
        normal.sample(&mut rng) as f32
    });

    Tensor { data }
}
