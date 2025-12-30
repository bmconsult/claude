//! Nexus Training Binary
//!
//! Usage: nexus-train --config config.json --data data_dir --output output_dir

use anyhow::Result;
use nexus::{Nexus, NexusConfig};
use nexus::training::{Trainer, TrainConfig, DataLoader};
use ndarray::Array3;
use std::path::PathBuf;

fn main() -> Result<()> {
    // Initialize logging
    env_logger::init();

    println!("╔══════════════════════════════════════════╗");
    println!("║           NEXUS Training v0.1            ║");
    println!("║  Hybrid Intelligence Architecture       ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    // Parse arguments (simplified)
    let args: Vec<String> = std::env::args().collect();

    let config_path = args.iter()
        .position(|x| x == "--config")
        .map(|i| &args[i + 1])
        .map(PathBuf::from);

    let data_path = args.iter()
        .position(|x| x == "--data")
        .map(|i| &args[i + 1])
        .map(PathBuf::from);

    let output_path = args.iter()
        .position(|x| x == "--output")
        .map(|i| args[i + 1].clone())
        .unwrap_or_else(|| "output".to_string());

    // Load or create configs
    let model_config = if let Some(ref path) = config_path {
        let file = std::fs::File::open(path)?;
        serde_json::from_reader(file)?
    } else {
        println!("Using default model configuration");
        NexusConfig::default()
    };

    let train_config = TrainConfig::default();

    println!("Model Configuration:");
    println!("  d_model: {}", model_config.d_model);
    println!("  n_heads: {}", model_config.n_heads);
    println!("  layers: {}", model_config.layers_per_block);
    println!("  attention ratio: 1:{}", 7);
    println!();

    println!("Training Configuration:");
    println!("  lr: {}", train_config.lr);
    println!("  batch_size: {}", train_config.batch_size);
    println!("  epochs: {}", train_config.epochs);
    println!("  warmup_steps: {}", train_config.warmup_steps);
    println!();

    // Create model
    println!("Initializing model...");
    let mut model = Nexus::new(model_config.clone());
    println!("Model initialized!");
    println!();

    // Load or generate training data
    let train_data = if let Some(ref path) = data_path {
        println!("Loading data from {:?}...", path);
        load_data(path, &model_config)?
    } else {
        println!("Generating synthetic training data...");
        generate_synthetic_data(&model_config, 1000)
    };

    println!("Training samples: {}", train_data.len());
    println!();

    // Create data loader
    let mut train_loader = DataLoader::new(
        train_data,
        train_config.batch_size,
        true,  // shuffle
    );

    // Create trainer
    let mut trainer = Trainer::new(
        model_config,
        train_config,
        &output_path,
        Some(&format!("{}/train.log", output_path)),
    );

    // Train!
    println!("Starting training...");
    println!("{}", "═".repeat(50));
    trainer.train(&mut model, &mut train_loader);
    println!("{}", "═".repeat(50));

    println!();
    println!("Training complete!");
    println!("Checkpoints saved to: {}", output_path);

    Ok(())
}

fn load_data(_path: &PathBuf, config: &NexusConfig) -> Result<Vec<Array3<f32>>> {
    // In a real implementation, this would load tokenized text data
    // For now, generate synthetic data as placeholder
    println!("Data loading not yet implemented, using synthetic data");
    Ok(generate_synthetic_data(config, 1000))
}

fn generate_synthetic_data(config: &NexusConfig, n_samples: usize) -> Vec<Array3<f32>> {
    use rand_distr::{Normal, Distribution};

    let mut rng = rand::thread_rng();
    let normal = Normal::new(0.0, 1.0).unwrap();

    (0..n_samples)
        .map(|_| {
            Array3::from_shape_fn((1, 128, config.d_model), |_| {
                normal.sample(&mut rng) as f32
            })
        })
        .collect()
}
