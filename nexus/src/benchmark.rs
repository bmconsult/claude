//! Benchmark and Evaluation Suite
//!
//! Provides comprehensive evaluation metrics for language models:
//! - Perplexity computation
//! - Accuracy on downstream tasks
//! - Generation quality metrics
//! - Latency and throughput benchmarks
//! - Memory profiling

use ndarray::{Array1, Array2, Array3};
use std::collections::HashMap;
use std::time::{Duration, Instant};

/// Perplexity calculator
pub struct PerplexityEvaluator {
    total_log_prob: f64,
    total_tokens: usize,
}

impl PerplexityEvaluator {
    pub fn new() -> Self {
        Self {
            total_log_prob: 0.0,
            total_tokens: 0,
        }
    }

    /// Add a batch of log probabilities
    /// log_probs: negative log probabilities (cross-entropy losses)
    pub fn add_batch(&mut self, log_probs: &[f32], n_tokens: usize) {
        let batch_log_prob: f64 = log_probs.iter().map(|&x| x as f64).sum();
        self.total_log_prob += batch_log_prob;
        self.total_tokens += n_tokens;
    }

    /// Add loss from a forward pass
    pub fn add_loss(&mut self, loss: f32, n_tokens: usize) {
        self.total_log_prob += loss as f64 * n_tokens as f64;
        self.total_tokens += n_tokens;
    }

    /// Compute perplexity
    pub fn perplexity(&self) -> f64 {
        if self.total_tokens == 0 {
            return 0.0;
        }
        let avg_log_prob = self.total_log_prob / self.total_tokens as f64;
        avg_log_prob.exp()
    }

    /// Compute bits per character (for character-level models)
    pub fn bits_per_char(&self) -> f64 {
        if self.total_tokens == 0 {
            return 0.0;
        }
        let avg_log_prob = self.total_log_prob / self.total_tokens as f64;
        avg_log_prob / 2.0_f64.ln() // Convert nats to bits
    }

    /// Reset accumulator
    pub fn reset(&mut self) {
        self.total_log_prob = 0.0;
        self.total_tokens = 0;
    }

    pub fn total_tokens(&self) -> usize {
        self.total_tokens
    }
}

impl Default for PerplexityEvaluator {
    fn default() -> Self {
        Self::new()
    }
}

/// Accuracy evaluator for classification/multiple-choice
pub struct AccuracyEvaluator {
    correct: usize,
    total: usize,
    per_class_correct: HashMap<String, usize>,
    per_class_total: HashMap<String, usize>,
}

impl AccuracyEvaluator {
    pub fn new() -> Self {
        Self {
            correct: 0,
            total: 0,
            per_class_correct: HashMap::new(),
            per_class_total: HashMap::new(),
        }
    }

    /// Add a prediction result
    pub fn add(&mut self, predicted: &str, expected: &str) {
        self.total += 1;
        *self.per_class_total.entry(expected.to_string()).or_insert(0) += 1;

        if predicted == expected {
            self.correct += 1;
            *self.per_class_correct.entry(expected.to_string()).or_insert(0) += 1;
        }
    }

    /// Add multiple predictions
    pub fn add_batch(&mut self, predictions: &[String], expected: &[String]) {
        for (pred, exp) in predictions.iter().zip(expected.iter()) {
            self.add(pred, exp);
        }
    }

    /// Overall accuracy
    pub fn accuracy(&self) -> f64 {
        if self.total == 0 {
            return 0.0;
        }
        self.correct as f64 / self.total as f64
    }

    /// Per-class accuracy
    pub fn per_class_accuracy(&self) -> HashMap<String, f64> {
        self.per_class_total
            .iter()
            .map(|(class, &total)| {
                let correct = *self.per_class_correct.get(class).unwrap_or(&0);
                (class.clone(), if total > 0 { correct as f64 / total as f64 } else { 0.0 })
            })
            .collect()
    }

    /// Macro-averaged accuracy (average of per-class accuracies)
    pub fn macro_accuracy(&self) -> f64 {
        let per_class = self.per_class_accuracy();
        if per_class.is_empty() {
            return 0.0;
        }
        per_class.values().sum::<f64>() / per_class.len() as f64
    }

    pub fn reset(&mut self) {
        self.correct = 0;
        self.total = 0;
        self.per_class_correct.clear();
        self.per_class_total.clear();
    }

    pub fn total(&self) -> usize {
        self.total
    }
}

impl Default for AccuracyEvaluator {
    fn default() -> Self {
        Self::new()
    }
}

/// BLEU score calculator for generation quality
pub struct BleuEvaluator {
    /// N-gram weights (default: uniform for BLEU-4)
    weights: Vec<f64>,
}

impl BleuEvaluator {
    pub fn new(max_n: usize) -> Self {
        let weights = vec![1.0 / max_n as f64; max_n];
        Self { weights }
    }

    /// Default BLEU-4
    pub fn bleu4() -> Self {
        Self::new(4)
    }

    /// Compute n-grams from tokens
    fn get_ngrams(&self, tokens: &[String], n: usize) -> HashMap<Vec<String>, usize> {
        let mut ngrams = HashMap::new();
        if tokens.len() >= n {
            for i in 0..=(tokens.len() - n) {
                let ngram: Vec<String> = tokens[i..i + n].to_vec();
                *ngrams.entry(ngram).or_insert(0) += 1;
            }
        }
        ngrams
    }

    /// Compute BLEU score for a single candidate against references
    pub fn score(&self, candidate: &[String], references: &[Vec<String>]) -> f64 {
        if candidate.is_empty() {
            return 0.0;
        }

        let mut precisions = Vec::new();
        let max_n = self.weights.len();

        for n in 1..=max_n {
            let cand_ngrams = self.get_ngrams(candidate, n);

            // Get max counts from references
            let mut ref_max_counts: HashMap<Vec<String>, usize> = HashMap::new();
            for reference in references {
                let ref_ngrams = self.get_ngrams(reference, n);
                for (ngram, count) in ref_ngrams {
                    let entry = ref_max_counts.entry(ngram).or_insert(0);
                    *entry = (*entry).max(count);
                }
            }

            // Clipped counts
            let mut clipped_count = 0;
            let mut total_count = 0;
            for (ngram, count) in cand_ngrams {
                let ref_count = *ref_max_counts.get(&ngram).unwrap_or(&0);
                clipped_count += count.min(ref_count);
                total_count += count;
            }

            let precision = if total_count > 0 {
                clipped_count as f64 / total_count as f64
            } else {
                0.0
            };

            precisions.push(precision);
        }

        // Geometric mean of precisions
        let log_prec_sum: f64 = precisions
            .iter()
            .zip(self.weights.iter())
            .map(|(&p, &w)| {
                if p > 0.0 {
                    w * p.ln()
                } else {
                    f64::NEG_INFINITY
                }
            })
            .sum();

        if log_prec_sum.is_infinite() {
            return 0.0;
        }

        // Brevity penalty
        let c = candidate.len();
        let r = references
            .iter()
            .map(|r| r.len())
            .min_by_key(|&len| (len as i64 - c as i64).abs())
            .unwrap_or(0);

        let bp = if c > r {
            1.0
        } else if c == 0 {
            0.0
        } else {
            (1.0 - r as f64 / c as f64).exp()
        };

        bp * log_prec_sum.exp()
    }

    /// Corpus-level BLEU (average over samples)
    pub fn corpus_score(&self, candidates: &[Vec<String>], references: &[Vec<Vec<String>>]) -> f64 {
        if candidates.is_empty() {
            return 0.0;
        }

        let total: f64 = candidates
            .iter()
            .zip(references.iter())
            .map(|(c, r)| self.score(c, r))
            .sum();

        total / candidates.len() as f64
    }
}

impl Default for BleuEvaluator {
    fn default() -> Self {
        Self::bleu4()
    }
}

/// ROUGE score calculator
pub struct RougeEvaluator;

impl RougeEvaluator {
    pub fn new() -> Self {
        Self
    }

    /// ROUGE-N precision, recall, F1
    pub fn rouge_n(&self, candidate: &[String], reference: &[String], n: usize) -> (f64, f64, f64) {
        let get_ngrams = |tokens: &[String], n: usize| -> HashMap<Vec<String>, usize> {
            let mut ngrams = HashMap::new();
            if tokens.len() >= n {
                for i in 0..=(tokens.len() - n) {
                    let ngram: Vec<String> = tokens[i..i + n].to_vec();
                    *ngrams.entry(ngram).or_insert(0) += 1;
                }
            }
            ngrams
        };

        let cand_ngrams = get_ngrams(candidate, n);
        let ref_ngrams = get_ngrams(reference, n);

        let mut overlap = 0;
        for (ngram, &count) in &cand_ngrams {
            overlap += count.min(*ref_ngrams.get(ngram).unwrap_or(&0));
        }

        let cand_total: usize = cand_ngrams.values().sum();
        let ref_total: usize = ref_ngrams.values().sum();

        let precision = if cand_total > 0 { overlap as f64 / cand_total as f64 } else { 0.0 };
        let recall = if ref_total > 0 { overlap as f64 / ref_total as f64 } else { 0.0 };
        let f1 = if precision + recall > 0.0 {
            2.0 * precision * recall / (precision + recall)
        } else {
            0.0
        };

        (precision, recall, f1)
    }

    /// ROUGE-1 F1
    pub fn rouge1_f1(&self, candidate: &[String], reference: &[String]) -> f64 {
        self.rouge_n(candidate, reference, 1).2
    }

    /// ROUGE-2 F1
    pub fn rouge2_f1(&self, candidate: &[String], reference: &[String]) -> f64 {
        self.rouge_n(candidate, reference, 2).2
    }

    /// ROUGE-L (longest common subsequence)
    pub fn rouge_l(&self, candidate: &[String], reference: &[String]) -> (f64, f64, f64) {
        let m = candidate.len();
        let n = reference.len();

        if m == 0 || n == 0 {
            return (0.0, 0.0, 0.0);
        }

        // LCS length using DP
        let mut dp = vec![vec![0usize; n + 1]; m + 1];
        for i in 1..=m {
            for j in 1..=n {
                if candidate[i - 1] == reference[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
                }
            }
        }

        let lcs_len = dp[m][n] as f64;
        let precision = lcs_len / m as f64;
        let recall = lcs_len / n as f64;
        let f1 = if precision + recall > 0.0 {
            2.0 * precision * recall / (precision + recall)
        } else {
            0.0
        };

        (precision, recall, f1)
    }
}

impl Default for RougeEvaluator {
    fn default() -> Self {
        Self::new()
    }
}

/// Latency benchmarker
pub struct LatencyBenchmark {
    samples: Vec<Duration>,
    warmup_samples: usize,
}

impl LatencyBenchmark {
    pub fn new(warmup_samples: usize) -> Self {
        Self {
            samples: Vec::new(),
            warmup_samples,
        }
    }

    /// Record a timing sample
    pub fn record(&mut self, duration: Duration) {
        self.samples.push(duration);
    }

    /// Run a benchmark function
    pub fn benchmark<F: FnMut()>(&mut self, mut f: F, iterations: usize) {
        for i in 0..iterations {
            let start = Instant::now();
            f();
            let elapsed = start.elapsed();

            if i >= self.warmup_samples {
                self.samples.push(elapsed);
            }
        }
    }

    /// Mean latency
    pub fn mean(&self) -> Duration {
        if self.samples.is_empty() {
            return Duration::ZERO;
        }
        let total: Duration = self.samples.iter().sum();
        total / self.samples.len() as u32
    }

    /// Median latency
    pub fn median(&self) -> Duration {
        if self.samples.is_empty() {
            return Duration::ZERO;
        }
        let mut sorted = self.samples.clone();
        sorted.sort();
        sorted[sorted.len() / 2]
    }

    /// P99 latency
    pub fn p99(&self) -> Duration {
        if self.samples.is_empty() {
            return Duration::ZERO;
        }
        let mut sorted = self.samples.clone();
        sorted.sort();
        let idx = (sorted.len() as f64 * 0.99) as usize;
        sorted[idx.min(sorted.len() - 1)]
    }

    /// Standard deviation
    pub fn std_dev(&self) -> Duration {
        if self.samples.len() < 2 {
            return Duration::ZERO;
        }

        let mean_nanos = self.mean().as_nanos() as f64;
        let variance: f64 = self.samples
            .iter()
            .map(|d| {
                let diff = d.as_nanos() as f64 - mean_nanos;
                diff * diff
            })
            .sum::<f64>()
            / (self.samples.len() - 1) as f64;

        Duration::from_nanos(variance.sqrt() as u64)
    }

    /// Throughput (items per second, given items per sample)
    pub fn throughput(&self, items_per_sample: usize) -> f64 {
        let mean_secs = self.mean().as_secs_f64();
        if mean_secs > 0.0 {
            items_per_sample as f64 / mean_secs
        } else {
            0.0
        }
    }

    pub fn n_samples(&self) -> usize {
        self.samples.len()
    }

    pub fn reset(&mut self) {
        self.samples.clear();
    }
}

impl Default for LatencyBenchmark {
    fn default() -> Self {
        Self::new(3)
    }
}

/// Memory profiler
pub struct MemoryProfiler {
    snapshots: Vec<MemorySnapshot>,
}

#[derive(Clone, Debug)]
pub struct MemorySnapshot {
    pub label: String,
    pub timestamp: Instant,
    /// Estimated memory in bytes (would need platform-specific impl for real values)
    pub estimated_bytes: usize,
}

impl MemoryProfiler {
    pub fn new() -> Self {
        Self { snapshots: Vec::new() }
    }

    /// Take a memory snapshot (placeholder - real impl would query system)
    pub fn snapshot(&mut self, label: &str, estimated_bytes: usize) {
        self.snapshots.push(MemorySnapshot {
            label: label.to_string(),
            timestamp: Instant::now(),
            estimated_bytes,
        });
    }

    /// Get peak memory
    pub fn peak_memory(&self) -> usize {
        self.snapshots.iter().map(|s| s.estimated_bytes).max().unwrap_or(0)
    }

    /// Get memory delta between two labels
    pub fn delta(&self, from: &str, to: &str) -> Option<i64> {
        let from_snapshot = self.snapshots.iter().find(|s| s.label == from)?;
        let to_snapshot = self.snapshots.iter().find(|s| s.label == to)?;
        Some(to_snapshot.estimated_bytes as i64 - from_snapshot.estimated_bytes as i64)
    }

    /// Print report
    pub fn report(&self) -> String {
        let mut report = String::new();
        report.push_str("Memory Profile:\n");
        for snapshot in &self.snapshots {
            report.push_str(&format!(
                "  {}: {} MB\n",
                snapshot.label,
                snapshot.estimated_bytes / (1024 * 1024)
            ));
        }
        report.push_str(&format!("  Peak: {} MB\n", self.peak_memory() / (1024 * 1024)));
        report
    }
}

impl Default for MemoryProfiler {
    fn default() -> Self {
        Self::new()
    }
}

/// Comprehensive benchmark suite
pub struct BenchmarkSuite {
    pub perplexity: PerplexityEvaluator,
    pub accuracy: AccuracyEvaluator,
    pub bleu: BleuEvaluator,
    pub rouge: RougeEvaluator,
    pub latency: LatencyBenchmark,
    pub memory: MemoryProfiler,
}

impl BenchmarkSuite {
    pub fn new() -> Self {
        Self {
            perplexity: PerplexityEvaluator::new(),
            accuracy: AccuracyEvaluator::new(),
            bleu: BleuEvaluator::bleu4(),
            rouge: RougeEvaluator::new(),
            latency: LatencyBenchmark::new(3),
            memory: MemoryProfiler::new(),
        }
    }

    /// Generate comprehensive report
    pub fn report(&self) -> BenchmarkReport {
        BenchmarkReport {
            perplexity: self.perplexity.perplexity(),
            accuracy: self.accuracy.accuracy(),
            mean_latency_ms: self.latency.mean().as_secs_f64() * 1000.0,
            p99_latency_ms: self.latency.p99().as_secs_f64() * 1000.0,
            throughput_tokens_per_sec: self.latency.throughput(1),
            peak_memory_mb: self.memory.peak_memory() / (1024 * 1024),
        }
    }

    /// Reset all evaluators
    pub fn reset(&mut self) {
        self.perplexity.reset();
        self.accuracy.reset();
        self.latency.reset();
    }
}

impl Default for BenchmarkSuite {
    fn default() -> Self {
        Self::new()
    }
}

/// Benchmark report
#[derive(Clone, Debug)]
pub struct BenchmarkReport {
    pub perplexity: f64,
    pub accuracy: f64,
    pub mean_latency_ms: f64,
    pub p99_latency_ms: f64,
    pub throughput_tokens_per_sec: f64,
    pub peak_memory_mb: usize,
}

impl std::fmt::Display for BenchmarkReport {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "╔══════════════════════════════════════════╗")?;
        writeln!(f, "║         Benchmark Results                ║")?;
        writeln!(f, "╠══════════════════════════════════════════╣")?;
        writeln!(f, "║ Perplexity:        {:>10.2}            ║", self.perplexity)?;
        writeln!(f, "║ Accuracy:          {:>10.2}%           ║", self.accuracy * 100.0)?;
        writeln!(f, "║ Mean Latency:      {:>10.2} ms         ║", self.mean_latency_ms)?;
        writeln!(f, "║ P99 Latency:       {:>10.2} ms         ║", self.p99_latency_ms)?;
        writeln!(f, "║ Throughput:        {:>10.0} tok/s      ║", self.throughput_tokens_per_sec)?;
        writeln!(f, "║ Peak Memory:       {:>10} MB          ║", self.peak_memory_mb)?;
        writeln!(f, "╚══════════════════════════════════════════╝")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_perplexity() {
        let mut eval = PerplexityEvaluator::new();

        // Add some losses (cross-entropy in nats)
        eval.add_loss(2.0, 100);
        eval.add_loss(1.5, 100);

        let ppl = eval.perplexity();
        assert!(ppl > 1.0);
        assert!(ppl.is_finite());

        assert_eq!(eval.total_tokens(), 200);
    }

    #[test]
    fn test_accuracy() {
        let mut eval = AccuracyEvaluator::new();

        eval.add("A", "A");
        eval.add("B", "A");
        eval.add("A", "A");
        eval.add("C", "C");

        assert_eq!(eval.accuracy(), 0.75); // 3/4 correct
        assert_eq!(eval.total(), 4);

        let per_class = eval.per_class_accuracy();
        assert_eq!(*per_class.get("A").unwrap(), 2.0 / 3.0); // 2 out of 3 A's correct
        assert_eq!(*per_class.get("C").unwrap(), 1.0); // 1 out of 1 C correct
    }

    #[test]
    fn test_bleu() {
        let bleu = BleuEvaluator::bleu4();

        let candidate: Vec<String> = "the cat sat on the mat".split_whitespace().map(String::from).collect();
        let reference: Vec<String> = "the cat is on the mat".split_whitespace().map(String::from).collect();

        let score = bleu.score(&candidate, &[reference]);
        // Score can be 0 or very low for short sentences with BLEU-4 due to 4-gram penalty
        // Just verify it's finite and non-negative
        assert!(score >= 0.0);
        assert!(score <= 1.0);
        assert!(score.is_finite());
    }

    #[test]
    fn test_bleu_perfect() {
        let bleu = BleuEvaluator::bleu4();

        let text: Vec<String> = "hello world foo bar".split_whitespace().map(String::from).collect();
        let score = bleu.score(&text, &[text.clone()]);

        assert!((score - 1.0).abs() < 0.01);
    }

    #[test]
    fn test_rouge() {
        let rouge = RougeEvaluator::new();

        let candidate: Vec<String> = "the cat sat".split_whitespace().map(String::from).collect();
        let reference: Vec<String> = "the cat sat on the mat".split_whitespace().map(String::from).collect();

        let (p, r, f1) = rouge.rouge_n(&candidate, &reference, 1);
        assert_eq!(p, 1.0); // All candidate words in reference
        assert_eq!(r, 0.5); // 3 out of 6 reference words in candidate
        assert!(f1 > 0.0);
    }

    #[test]
    fn test_rouge_l() {
        let rouge = RougeEvaluator::new();

        let candidate: Vec<String> = "A B C D".split_whitespace().map(String::from).collect();
        let reference: Vec<String> = "A B X C D".split_whitespace().map(String::from).collect();

        let (p, r, f1) = rouge.rouge_l(&candidate, &reference);
        // LCS is "A B C D" (length 4)
        assert_eq!(p, 1.0); // 4/4
        assert_eq!(r, 0.8); // 4/5
        assert!(f1 > 0.0);
    }

    #[test]
    fn test_latency_benchmark() {
        let mut bench = LatencyBenchmark::new(0);

        bench.record(Duration::from_millis(10));
        bench.record(Duration::from_millis(20));
        bench.record(Duration::from_millis(15));

        assert_eq!(bench.n_samples(), 3);
        assert_eq!(bench.mean(), Duration::from_millis(15));
        assert_eq!(bench.median(), Duration::from_millis(15));
    }

    #[test]
    fn test_benchmark_function() {
        let mut bench = LatencyBenchmark::new(2);

        let mut counter = 0;
        bench.benchmark(
            || {
                counter += 1;
                std::thread::sleep(Duration::from_micros(100));
            },
            5,
        );

        assert_eq!(counter, 5);
        assert_eq!(bench.n_samples(), 3); // 5 - 2 warmup
    }

    #[test]
    fn test_memory_profiler() {
        let mut profiler = MemoryProfiler::new();

        profiler.snapshot("start", 100 * 1024 * 1024);
        profiler.snapshot("after_load", 500 * 1024 * 1024);
        profiler.snapshot("after_forward", 800 * 1024 * 1024);

        assert_eq!(profiler.peak_memory(), 800 * 1024 * 1024);

        let delta = profiler.delta("start", "after_load").unwrap();
        assert_eq!(delta, 400 * 1024 * 1024);
    }

    #[test]
    fn test_benchmark_suite() {
        let mut suite = BenchmarkSuite::new();

        suite.perplexity.add_loss(2.0, 1000);
        suite.accuracy.add("A", "A");
        suite.latency.record(Duration::from_millis(50));
        suite.memory.snapshot("test", 512 * 1024 * 1024);

        let report = suite.report();
        assert!(report.perplexity > 0.0);
        assert!(report.accuracy > 0.0);

        println!("{}", report);
    }

    #[test]
    fn test_throughput() {
        let mut bench = LatencyBenchmark::new(0);

        // 100ms per sample, 1000 tokens per sample
        bench.record(Duration::from_millis(100));
        bench.record(Duration::from_millis(100));

        let throughput = bench.throughput(1000);
        assert!((throughput - 10000.0).abs() < 100.0); // ~10000 tokens/sec
    }
}
