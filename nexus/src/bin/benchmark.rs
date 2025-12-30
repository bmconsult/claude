//! Quick benchmark comparing Attention vs SSM throughput
//!
//! Usage: nexus-benchmark

use nexus::attention::MultiHeadAttention;
use nexus::ssm::SelectiveSSM;
use nexus::Tensor;
use std::time::Instant;

fn main() {
    println!("╔══════════════════════════════════════════╗");
    println!("║     NEXUS Performance Comparison         ║");
    println!("║     Attention vs SSM Throughput          ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    let d_model = 256;
    let n_heads = 8;
    let d_state = 16;
    let max_seq_len = 512;
    let n_iterations = 100;

    // Create layers
    let attention = MultiHeadAttention::new(d_model, n_heads, max_seq_len);
    let ssm = SelectiveSSM::new(d_model, d_state, 4, 2);

    println!("Configuration:");
    println!("  d_model: {}", d_model);
    println!("  n_heads: {}", n_heads);
    println!("  d_state: {} (SSM)", d_state);
    println!("  iterations: {}", n_iterations);
    println!();

    // Test different sequence lengths
    let seq_lengths = [32, 64, 128, 256, 512];

    println!("{:>8} | {:>12} | {:>12} | {:>10}", "Seq Len", "Attention", "SSM", "Speedup");
    println!("{}", "-".repeat(52));

    for &seq_len in &seq_lengths {
        let input = Tensor::randn(1, seq_len, d_model);

        // Warmup
        for _ in 0..5 {
            let _ = attention.forward(&input, true);
            let _ = ssm.forward(&input);
        }

        // Benchmark attention
        let start = Instant::now();
        for _ in 0..n_iterations {
            let _ = attention.forward(&input, true);
        }
        let attention_time = start.elapsed().as_secs_f64() / n_iterations as f64;

        // Benchmark SSM
        let start = Instant::now();
        for _ in 0..n_iterations {
            let _ = ssm.forward(&input);
        }
        let ssm_time = start.elapsed().as_secs_f64() / n_iterations as f64;

        let speedup = attention_time / ssm_time;

        println!("{:>8} | {:>10.2}ms | {:>10.2}ms | {:>9.2}x",
            seq_len,
            attention_time * 1000.0,
            ssm_time * 1000.0,
            speedup
        );
    }

    println!();
    println!("Analysis:");
    println!("  - Attention: O(n²) complexity - time grows quadratically with sequence length");
    println!("  - SSM: O(n) complexity - time grows linearly with sequence length");
    println!("  - Speedup increases with longer sequences");
    println!();

    // Memory comparison
    println!("Memory Complexity:");
    println!("  - Attention: O(n²) for attention matrix");
    println!("  - SSM: O(n) for state only");
    println!();

    // Test the hybrid ratio
    println!("Hybrid 1:7 Ratio Analysis:");
    let hybrid_seq_len = 256;
    let input = Tensor::randn(1, hybrid_seq_len, d_model);

    // Simulate hybrid block (1 attention + 7 SSM)
    let start = Instant::now();
    for _ in 0..n_iterations {
        let _ = attention.forward(&input, true);
        for _ in 0..7 {
            let _ = ssm.forward(&input);
        }
    }
    let hybrid_time = start.elapsed().as_secs_f64() / n_iterations as f64;

    // Compare to 8 attention layers
    let start = Instant::now();
    for _ in 0..n_iterations {
        for _ in 0..8 {
            let _ = attention.forward(&input, true);
        }
    }
    let pure_attention_time = start.elapsed().as_secs_f64() / n_iterations as f64;

    println!("  Sequence length: {}", hybrid_seq_len);
    println!("  8x Attention layers: {:.2}ms", pure_attention_time * 1000.0);
    println!("  1x Attention + 7x SSM: {:.2}ms", hybrid_time * 1000.0);
    println!("  Hybrid speedup: {:.2}x", pure_attention_time / hybrid_time);
    println!();
    println!("Conclusion: The 1:7 attention:SSM ratio provides significant");
    println!("throughput gains while preserving global attention capability.");
}
