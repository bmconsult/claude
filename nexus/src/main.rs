//! Nexus CLI Entry Point
//!
//! This file provides a simple CLI for testing Nexus.
//! For training, use: cargo run --bin nexus-train
//! For inference, use: cargo run --bin nexus-infer

use nexus::{Nexus, NexusConfig, Tensor};

fn main() {
    println!("╔══════════════════════════════════════════╗");
    println!("║              NEXUS v0.1.0                ║");
    println!("║    Hybrid Intelligence Architecture      ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    // Create configuration
    let config = NexusConfig {
        d_model: 256,
        n_heads: 8,
        layers_per_block: 4,
        memory_size: 256,
        ..Default::default()
    };

    println!("Configuration:");
    println!("  d_model: {}", config.d_model);
    println!("  n_heads: {}", config.n_heads);
    println!("  layers: {}", config.layers_per_block);
    println!("  memory_size: {}", config.memory_size);
    println!();

    // Create model
    println!("Creating model...");
    let mut model = Nexus::new(config);
    println!("Model created with ~{} parameters", model.num_parameters());
    println!();

    // Run a forward pass
    println!("Running forward pass...");
    let input = Tensor::randn(1, 32, 256);
    println!("Input shape: {:?}", input.shape());

    let output = model.forward(&input, true);
    println!("Output shape: {:?}", output.shape());
    println!();

    // Memory statistics
    let stats = model.memory.stats();
    println!("Memory Statistics:");
    println!("  Entries: {}/{}", stats.num_entries, stats.capacity);
    println!("  Avg surprise: {:.4}", stats.avg_surprise);
    println!();

    // Run multiple forward passes to accumulate memory
    println!("Running 10 more forward passes to build memory...");
    for i in 0..10 {
        let input = Tensor::randn(1, 32, 256);
        let _ = model.forward(&input, true);
        if (i + 1) % 5 == 0 {
            let stats = model.memory.stats();
            println!("  After {} passes: {} memory entries", i + 1, stats.num_entries);
        }
    }
    println!();

    let final_stats = model.memory.stats();
    println!("Final Memory Statistics:");
    println!("  Entries: {}/{}", final_stats.num_entries, final_stats.capacity);
    println!("  Avg surprise: {:.4}", final_stats.avg_surprise);
    println!("  Avg age: {:.1}", final_stats.avg_age);
    println!();

    println!("Demo complete!");
    println!();
    println!("For training: cargo run --release --bin nexus-train");
    println!("For inference: cargo run --release --bin nexus-infer");
}
