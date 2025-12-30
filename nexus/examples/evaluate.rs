//! Nexus Model Evaluation Suite
//!
//! Comprehensive benchmarks for trained Nexus models:
//! - Perplexity on held-out data
//! - Text generation quality
//! - Inference speed benchmarks
//! - Memory usage analysis
//!
//! Usage: cargo run --example evaluate --release -- [checkpoint_path]

use std::fs;
use std::time::Instant;
use nexus::{
    DifferentiableHybridNexusLM, HybridModelCheckpoint,
    SamplingConfig, Sampler,
};

// ============================================================================
// Evaluation Metrics
// ============================================================================

#[derive(Default)]
struct EvalMetrics {
    // Perplexity metrics
    val_loss: f32,
    val_perplexity: f32,

    // Generation metrics
    tokens_generated: usize,
    generation_time_ms: f32,
    tokens_per_sec: f32,

    // Model info
    n_parameters: usize,
    checkpoint_step: usize,
}

impl EvalMetrics {
    fn display(&self) {
        println!("╔═══════════════════════════════════════════════════════════════════╗");
        println!("║                    EVALUATION RESULTS                             ║");
        println!("╠═══════════════════════════════════════════════════════════════════╣");
        println!("║  Model Parameters:     {:>10}                                ║", self.n_parameters);
        println!("║  Checkpoint Step:      {:>10}                                ║", self.checkpoint_step);
        println!("╠═══════════════════════════════════════════════════════════════════╣");
        println!("║  PERPLEXITY METRICS                                               ║");
        println!("║  ─────────────────                                                ║");
        println!("║  Validation Loss:      {:>10.4}                                ║", self.val_loss);
        println!("║  Validation PPL:       {:>10.2}                                ║", self.val_perplexity);
        println!("╠═══════════════════════════════════════════════════════════════════╣");
        println!("║  INFERENCE SPEED                                                  ║");
        println!("║  ───────────────                                                  ║");
        println!("║  Tokens Generated:     {:>10}                                ║", self.tokens_generated);
        println!("║  Generation Time:      {:>10.1} ms                             ║", self.generation_time_ms);
        println!("║  Throughput:           {:>10.1} tok/s                          ║", self.tokens_per_sec);
        println!("╚═══════════════════════════════════════════════════════════════════╝");
    }
}

// ============================================================================
// Perplexity Evaluation
// ============================================================================

fn evaluate_perplexity(
    model: &DifferentiableHybridNexusLM,
    data: &[u32],
    seq_len: usize,
    n_samples: usize,
) -> (f32, f32) {
    let mut total_loss = 0.0;
    let mut total_tokens = 0;

    println!("  Evaluating perplexity on {} samples...", n_samples);

    for i in 0..n_samples {
        let start = (i * seq_len) % (data.len().saturating_sub(seq_len));
        if start + seq_len > data.len() {
            continue;
        }

        let tokens: Vec<u32> = data[start..start + seq_len].to_vec();
        let input: Vec<u32> = tokens[..tokens.len()-1].to_vec();
        let logits = model.forward(&input);
        let targets: Vec<usize> = tokens[1..].iter().map(|&t| t as usize).collect();
        let (loss, _) = logits.cross_entropy_loss(&targets);

        total_loss += loss * (tokens.len() - 1) as f32;
        total_tokens += tokens.len() - 1;

        if (i + 1) % 20 == 0 {
            println!("    Progress: {}/{}", i + 1, n_samples);
        }
    }

    let avg_loss = total_loss / total_tokens as f32;
    let perplexity = avg_loss.exp();

    (avg_loss, perplexity)
}

// ============================================================================
// Text Generation Benchmark
// ============================================================================

fn benchmark_generation(
    model: &DifferentiableHybridNexusLM,
    prompts: &[&str],
    max_tokens: usize,
    sampling_config: &SamplingConfig,
) -> (Vec<String>, f32, usize) {
    let mut generated = Vec::new();
    let mut total_tokens = 0;
    let start = Instant::now();

    for prompt in prompts {
        let mut tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
        let mut sampler = Sampler::new(sampling_config.clone());
        let initial_len = tokens.len();

        for _ in 0..max_tokens {
            let logits = model.forward(&tokens);
            let logits_data = logits.data();
            let seq_len = tokens.len();

            let last_logits: Vec<f32> = (0..256)
                .map(|v| logits_data[[0, seq_len - 1, v]])
                .collect();

            let next_token = sampler.sample(&last_logits, &tokens);
            tokens.push(next_token);

            if next_token == b'\n' as u32 || next_token == 0 {
                break;
            }
        }

        total_tokens += tokens.len() - initial_len;

        let text: String = tokens.iter()
            .filter_map(|&b| if b < 128 { Some(b as u8 as char) } else { None })
            .collect();
        generated.push(text);
    }

    let elapsed = start.elapsed().as_secs_f32() * 1000.0;
    (generated, elapsed, total_tokens)
}

// ============================================================================
// Quality Analysis
// ============================================================================

fn analyze_generation_quality(generations: &[String]) {
    println!("\n📝 Generation Quality Analysis:");
    println!("   ────────────────────────────\n");

    for (i, gen) in generations.iter().enumerate() {
        let word_count = gen.split_whitespace().count();
        let char_count = gen.len();
        let has_punctuation = gen.contains('.') || gen.contains(',') || gen.contains('!') || gen.contains('?');
        let has_caps = gen.chars().any(|c| c.is_uppercase());

        println!("   Sample {}:", i + 1);
        println!("   \"{}\"", gen.chars().take(100).collect::<String>().trim());
        if gen.len() > 100 {
            println!("   ...[truncated]");
        }
        println!("   Words: {} | Chars: {} | Punctuation: {} | Capitalization: {}",
                 word_count, char_count,
                 if has_punctuation { "✓" } else { "✗" },
                 if has_caps { "✓" } else { "✗" });
        println!();
    }
}

// ============================================================================
// Repetition Analysis
// ============================================================================

fn analyze_repetition(text: &str) -> f32 {
    let words: Vec<&str> = text.split_whitespace().collect();
    if words.len() < 2 {
        return 0.0;
    }

    let mut repetitions = 0;
    for i in 1..words.len() {
        if words[i] == words[i-1] {
            repetitions += 1;
        }
    }

    repetitions as f32 / (words.len() - 1) as f32
}

// ============================================================================
// Main
// ============================================================================

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════════════════╗");
    println!("║              NEXUS MODEL EVALUATION SUITE                         ║");
    println!("╚═══════════════════════════════════════════════════════════════════╝\n");

    // Parse checkpoint path from args or use default
    let args: Vec<String> = std::env::args().collect();
    let checkpoint_path = if args.len() > 1 {
        args[1].clone()
    } else {
        "checkpoints/nexus_production/best.bin".to_string()
    };

    // Load checkpoint
    println!("📂 Loading checkpoint: {}", checkpoint_path);
    let checkpoint = HybridModelCheckpoint::load(&checkpoint_path)
        .map_err(|e| anyhow::anyhow!("Failed to load checkpoint: {}", e))?;

    println!("   Step: {} | Training Loss: {:.4}", checkpoint.step, checkpoint.loss);

    // Create model and load weights
    let model = DifferentiableHybridNexusLM::new(checkpoint.config.clone());
    checkpoint.load_into(&model)
        .map_err(|e| anyhow::anyhow!("Failed to load weights: {}", e))?;
    println!("   ✓ Loaded {} parameters\n", model.num_parameters());

    // Load validation data
    println!("📂 Loading validation data...");
    let corpus = fs::read_to_string("data/shakespeare.txt")?;
    let tokens: Vec<u32> = corpus.bytes().map(|b| b as u32).collect();
    let split = (tokens.len() as f32 * 0.9) as usize;
    let val_tokens = &tokens[split..];
    println!("   {} validation tokens\n", val_tokens.len());

    // Initialize metrics
    let mut metrics = EvalMetrics {
        n_parameters: model.num_parameters(),
        checkpoint_step: checkpoint.step,
        ..Default::default()
    };

    // ========================================================================
    // Perplexity Evaluation
    // ========================================================================

    println!("═══════════════════════════════════════════════════════════════════");
    println!("  PERPLEXITY EVALUATION");
    println!("═══════════════════════════════════════════════════════════════════\n");

    let (val_loss, val_ppl) = evaluate_perplexity(&model, val_tokens, 128, 100);
    metrics.val_loss = val_loss;
    metrics.val_perplexity = val_ppl;

    println!("\n  Results:");
    println!("    Loss:       {:.4}", val_loss);
    println!("    Perplexity: {:.2}\n", val_ppl);

    // ========================================================================
    // Generation Benchmark
    // ========================================================================

    println!("═══════════════════════════════════════════════════════════════════");
    println!("  GENERATION BENCHMARK");
    println!("═══════════════════════════════════════════════════════════════════\n");

    let sampling_config = SamplingConfig {
        temperature: 0.8,
        top_k: 40,
        top_p: 0.95,
        repetition_penalty: 1.1,
        greedy: false,
        seed: Some(42),
    };

    let prompts = [
        "HAMLET: ",
        "To be, or not to be",
        "What light through yonder",
        "Friends, Romans, countrymen",
        "All the world's a stage",
        "The quality of mercy",
        "Now is the winter of",
        "O Romeo, Romeo",
    ];

    println!("  Generating {} samples with max 80 tokens each...\n", prompts.len());

    let (generations, gen_time, gen_tokens) = benchmark_generation(
        &model, &prompts, 80, &sampling_config
    );

    metrics.tokens_generated = gen_tokens;
    metrics.generation_time_ms = gen_time;
    metrics.tokens_per_sec = gen_tokens as f32 / (gen_time / 1000.0);

    analyze_generation_quality(&generations);

    // ========================================================================
    // Repetition Analysis
    // ========================================================================

    println!("═══════════════════════════════════════════════════════════════════");
    println!("  REPETITION ANALYSIS");
    println!("═══════════════════════════════════════════════════════════════════\n");

    let mut total_rep = 0.0;
    for (i, gen) in generations.iter().enumerate() {
        let rep_rate = analyze_repetition(gen);
        total_rep += rep_rate;
        println!("   Sample {}: {:.1}% consecutive word repetition", i + 1, rep_rate * 100.0);
    }
    let avg_rep = total_rep / generations.len() as f32;
    println!("\n   Average repetition rate: {:.1}%", avg_rep * 100.0);
    println!("   (Lower is better, <5% is good, <2% is excellent)\n");

    // ========================================================================
    // Inference Speed Benchmark
    // ========================================================================

    println!("═══════════════════════════════════════════════════════════════════");
    println!("  INFERENCE SPEED BENCHMARK");
    println!("═══════════════════════════════════════════════════════════════════\n");

    // Single token latency
    let prompt: Vec<u32> = "The ".bytes().map(|b| b as u32).collect();
    let start = Instant::now();
    for _ in 0..100 {
        let _ = model.forward(&prompt);
    }
    let single_latency = start.elapsed().as_secs_f32() * 1000.0 / 100.0;
    println!("   Single forward pass (4 tokens):  {:.2} ms", single_latency);

    // Longer sequence latency
    let long_prompt: Vec<u32> = "To be, or not to be, that is the question"
        .bytes().map(|b| b as u32).collect();
    let start = Instant::now();
    for _ in 0..50 {
        let _ = model.forward(&long_prompt);
    }
    let long_latency = start.elapsed().as_secs_f32() * 1000.0 / 50.0;
    println!("   Single forward pass (42 tokens): {:.2} ms", long_latency);
    println!("   Tokens/sec (short prompt):       {:.0}", 4.0 / (single_latency / 1000.0));
    println!("   Tokens/sec (long prompt):        {:.0}\n", 42.0 / (long_latency / 1000.0));

    // ========================================================================
    // Final Summary
    // ========================================================================

    println!();
    metrics.display();

    // Quality assessment
    println!("\n📊 Quality Assessment:");
    if metrics.val_perplexity < 10.0 {
        println!("   ⭐ Excellent - Perplexity < 10");
    } else if metrics.val_perplexity < 20.0 {
        println!("   ✓ Good - Perplexity < 20");
    } else if metrics.val_perplexity < 50.0 {
        println!("   ○ Moderate - Perplexity < 50");
    } else {
        println!("   ✗ Needs more training - Perplexity >= 50");
    }

    if avg_rep < 0.02 {
        println!("   ⭐ Excellent repetition control (<2%)");
    } else if avg_rep < 0.05 {
        println!("   ✓ Good repetition control (<5%)");
    } else {
        println!("   ○ Some repetition present (>=5%)");
    }

    println!("\n✅ Evaluation complete!");

    Ok(())
}
