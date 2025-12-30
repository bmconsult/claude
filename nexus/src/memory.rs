//! Titans-style Test-Time Memory Module
//!
//! Key innovation: Memory that learns DURING inference using "surprise" metric.
//! High surprise → store in long-term memory.
//! Memory updates via mini-gradient descent on incoming tokens.

use ndarray::{Array1, Array2, Array3};
use crate::tensor::Tensor;

/// Memory entry with associated key and value
#[derive(Clone)]
struct MemoryEntry {
    /// Key for retrieval (what to match)
    key: Array1<f32>,
    /// Value to retrieve
    value: Array1<f32>,
    /// Surprise score when stored
    surprise: f32,
    /// Age (for potential eviction)
    age: usize,
}

/// Titans-style Memory Module
///
/// Three types of memory (following Titans paper):
/// 1. Short-term: Current attention context
/// 2. Long-term: Learned representations (test-time updated)
/// 3. Persistent: Task knowledge (not updated here)
pub struct TitansMemory {
    /// Model dimension
    d_model: usize,
    /// Maximum memory entries
    capacity: usize,
    /// Learning rate for test-time updates
    lr: f32,
    /// Long-term memory entries
    memories: Vec<MemoryEntry>,
    /// Running mean for surprise normalization
    surprise_mean: f32,
    /// Running std for surprise normalization
    surprise_std: f32,
    /// Number of updates seen
    n_updates: usize,
    /// Key projection (learned but fixed during inference)
    key_proj: Array2<f32>,
    /// Value projection
    value_proj: Array2<f32>,
    /// Query projection for memory read
    query_proj: Array2<f32>,
}

impl TitansMemory {
    pub fn new(d_model: usize, capacity: usize, lr: f32) -> Self {
        // Initialize projections with Xavier initialization
        let scale = (2.0 / (d_model * 2) as f32).sqrt();

        let key_proj = Array2::from_shape_fn((d_model, d_model), |_| {
            (rand::random::<f32>() - 0.5) * 2.0 * scale
        });

        let value_proj = Array2::from_shape_fn((d_model, d_model), |_| {
            (rand::random::<f32>() - 0.5) * 2.0 * scale
        });

        let query_proj = Array2::from_shape_fn((d_model, d_model), |_| {
            (rand::random::<f32>() - 0.5) * 2.0 * scale
        });

        Self {
            d_model,
            capacity,
            lr,
            memories: Vec::with_capacity(capacity),
            surprise_mean: 0.0,
            surprise_std: 1.0,
            n_updates: 0,
            key_proj,
            value_proj,
            query_proj,
        }
    }

    /// Project hidden state to key space
    fn project_key(&self, h: &Array1<f32>) -> Array1<f32> {
        let mut key = Array1::zeros(self.d_model);
        for i in 0..self.d_model {
            for j in 0..self.d_model {
                key[i] += h[j] * self.key_proj[[j, i]];
            }
        }
        key
    }

    /// Project hidden state to value space
    fn project_value(&self, h: &Array1<f32>) -> Array1<f32> {
        let mut value = Array1::zeros(self.d_model);
        for i in 0..self.d_model {
            for j in 0..self.d_model {
                value[i] += h[j] * self.value_proj[[j, i]];
            }
        }
        value
    }

    /// Project hidden state to query space
    fn project_query(&self, h: &Array1<f32>) -> Array1<f32> {
        let mut query = Array1::zeros(self.d_model);
        for i in 0..self.d_model {
            for j in 0..self.d_model {
                query[i] += h[j] * self.query_proj[[j, i]];
            }
        }
        query
    }

    /// Compute surprise score for a hidden state
    ///
    /// Surprise = -log P(x | context)
    /// Approximated as prediction error from memory
    pub fn compute_surprise(&self, x: &Tensor) -> f32 {
        if self.memories.is_empty() {
            return 1.0; // High surprise if no memory
        }

        let (batch, seq_len, d_model) = x.shape();

        // Use last hidden state as query
        let mut h = Array1::zeros(d_model);
        for i in 0..d_model {
            h[i] = x.data[[batch - 1, seq_len - 1, i]];
        }

        let query = self.project_query(&h);

        // Find most similar memory
        let mut max_sim = f32::NEG_INFINITY;
        let mut best_value: Option<&Array1<f32>> = None;

        for mem in &self.memories {
            let sim = self.cosine_similarity(&query, &mem.key);
            if sim > max_sim {
                max_sim = sim;
                best_value = Some(&mem.value);
            }
        }

        // Surprise = prediction error (L2 distance to expected value)
        let value = self.project_value(&h);
        let surprise = if let Some(expected) = best_value {
            let mut error = 0.0f32;
            for i in 0..d_model {
                let diff = value[i] - expected[i];
                error += diff * diff;
            }
            error.sqrt()
        } else {
            1.0
        };

        // Normalize surprise using running stats
        let normalized = (surprise - self.surprise_mean) / (self.surprise_std + 1e-6);

        normalized.max(0.0) // Clamp to non-negative
    }

    /// Cosine similarity between two vectors
    fn cosine_similarity(&self, a: &Array1<f32>, b: &Array1<f32>) -> f32 {
        let mut dot = 0.0f32;
        let mut norm_a = 0.0f32;
        let mut norm_b = 0.0f32;

        for i in 0..a.len() {
            dot += a[i] * b[i];
            norm_a += a[i] * a[i];
            norm_b += b[i] * b[i];
        }

        dot / (norm_a.sqrt() * norm_b.sqrt() + 1e-8)
    }

    /// Update memory with new information (test-time learning)
    ///
    /// This is the key innovation: we update memory DURING inference
    /// based on the surprise metric.
    pub fn update(&mut self, x: &Tensor, surprise: f32) {
        let (batch, seq_len, d_model) = x.shape();

        // Update running statistics for surprise normalization
        self.n_updates += 1;
        let n = self.n_updates as f32;
        let delta = surprise - self.surprise_mean;
        self.surprise_mean += delta / n;
        self.surprise_std = ((self.surprise_std.powi(2) * (n - 1.0) + delta * (surprise - self.surprise_mean)) / n).sqrt();

        // Only store if surprise is above threshold (normalized > 0.5)
        let normalized_surprise = (surprise - self.surprise_mean) / (self.surprise_std + 1e-6);

        if normalized_surprise > 0.5 {
            // Extract last hidden state
            let mut h = Array1::zeros(d_model);
            for i in 0..d_model {
                h[i] = x.data[[batch - 1, seq_len - 1, i]];
            }

            let key = self.project_key(&h);
            let value = self.project_value(&h);

            // Create new memory entry
            let entry = MemoryEntry {
                key,
                value,
                surprise: normalized_surprise,
                age: 0,
            };

            // Add to memory
            if self.memories.len() < self.capacity {
                self.memories.push(entry);
            } else {
                // Evict: remove oldest entry with lowest surprise
                let mut min_score = f32::INFINITY;
                let mut min_idx = 0;

                for (idx, mem) in self.memories.iter().enumerate() {
                    // Score = surprise - age_penalty
                    let score = mem.surprise - 0.1 * mem.age as f32;
                    if score < min_score {
                        min_score = score;
                        min_idx = idx;
                    }
                }

                self.memories[min_idx] = entry;
            }

            // Age all entries
            for mem in &mut self.memories {
                mem.age += 1;
            }
        }

        // Test-time update: adjust existing memories slightly
        // This is a simplified version of the full Titans gradient update
        if !self.memories.is_empty() && normalized_surprise > 0.0 {
            let mut h = Array1::zeros(d_model);
            for i in 0..d_model {
                h[i] = x.data[[batch - 1, seq_len - 1, i]];
            }

            let query = self.project_query(&h);

            // Find most similar memory and update it
            let mut max_sim = f32::NEG_INFINITY;
            let mut best_idx = 0;

            for (idx, mem) in self.memories.iter().enumerate() {
                let sim = self.cosine_similarity(&query, &mem.key);
                if sim > max_sim {
                    max_sim = sim;
                    best_idx = idx;
                }
            }

            // Update the matching memory's value toward current value
            let value = self.project_value(&h);
            let lr_adjusted = self.lr * normalized_surprise.min(1.0);

            for i in 0..d_model {
                self.memories[best_idx].value[i] += lr_adjusted * (value[i] - self.memories[best_idx].value[i]);
            }
        }
    }

    /// Read from memory given current context
    ///
    /// Returns weighted combination of memory values based on query similarity
    pub fn read(&self, x: &Tensor) -> Tensor {
        let (batch, seq_len, d_model) = x.shape();
        let mut output = Array3::zeros((batch, seq_len, d_model));

        if self.memories.is_empty() {
            return Tensor { data: output };
        }

        for b in 0..batch {
            for s in 0..seq_len {
                // Get query for this position
                let mut h = Array1::zeros(d_model);
                for i in 0..d_model {
                    h[i] = x.data[[b, s, i]];
                }
                let query = self.project_query(&h);

                // Compute attention scores over memories
                let mut scores = Vec::with_capacity(self.memories.len());
                let mut max_score = f32::NEG_INFINITY;

                for mem in &self.memories {
                    let sim = self.cosine_similarity(&query, &mem.key);
                    scores.push(sim);
                    max_score = max_score.max(sim);
                }

                // Softmax over scores
                let mut sum = 0.0f32;
                for score in &mut scores {
                    *score = (*score - max_score).exp();
                    sum += *score;
                }
                for score in &mut scores {
                    *score /= sum;
                }

                // Weighted sum of memory values
                for (idx, mem) in self.memories.iter().enumerate() {
                    for i in 0..d_model {
                        output[[b, s, i]] += scores[idx] * mem.value[i];
                    }
                }
            }
        }

        Tensor { data: output }
    }

    /// Get memory statistics for debugging
    pub fn stats(&self) -> MemoryStats {
        let avg_surprise = if self.memories.is_empty() {
            0.0
        } else {
            self.memories.iter().map(|m| m.surprise).sum::<f32>() / self.memories.len() as f32
        };

        let avg_age = if self.memories.is_empty() {
            0.0
        } else {
            self.memories.iter().map(|m| m.age as f32).sum::<f32>() / self.memories.len() as f32
        };

        MemoryStats {
            num_entries: self.memories.len(),
            capacity: self.capacity,
            avg_surprise,
            avg_age,
            surprise_mean: self.surprise_mean,
            surprise_std: self.surprise_std,
        }
    }
}

/// Memory statistics
#[derive(Debug)]
pub struct MemoryStats {
    pub num_entries: usize,
    pub capacity: usize,
    pub avg_surprise: f32,
    pub avg_age: f32,
    pub surprise_mean: f32,
    pub surprise_std: f32,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_memory_creation() {
        let mem = TitansMemory::new(64, 100, 0.01);
        let stats = mem.stats();
        assert_eq!(stats.num_entries, 0);
        assert_eq!(stats.capacity, 100);
    }

    #[test]
    fn test_memory_update() {
        let mut mem = TitansMemory::new(64, 100, 0.01);
        let x = Tensor::randn(1, 4, 64);

        // First update should have high surprise
        let surprise = mem.compute_surprise(&x);
        assert!(surprise > 0.0);

        // Update memory
        mem.update(&x, surprise);
    }

    #[test]
    fn test_memory_read() {
        let mut mem = TitansMemory::new(64, 100, 0.01);
        let x = Tensor::randn(1, 4, 64);

        // Add some entries
        for _ in 0..5 {
            let x = Tensor::randn(1, 4, 64);
            mem.update(&x, 1.0);
        }

        // Read should return something
        let out = mem.read(&x);
        assert_eq!(out.shape(), x.shape());
    }
}
