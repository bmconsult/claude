//! Differentiable Titans-style Memory Module
//!
//! Full autograd-enabled version of the test-time memory for training.
//! Simplified version that focuses on the trainable projections.

use ndarray::{Array1, Array3};
use crate::autograd::{Variable, DifferentiableLinear};

/// Differentiable Memory Module
///
/// For training, we focus on the key/value/query projections.
/// The test-time update behavior is handled separately during inference.
#[derive(Clone)]
pub struct DifferentiableMemory {
    /// Model dimension
    d_model: usize,
    /// Memory slots for reading
    n_slots: usize,

    /// Key projection
    pub key_proj: DifferentiableLinear,
    /// Value projection
    pub value_proj: DifferentiableLinear,
    /// Query projection
    pub query_proj: DifferentiableLinear,
    /// Output projection (combines memory with input)
    pub out_proj: DifferentiableLinear,

    /// Learned memory keys (persistent memory)
    pub memory_keys: Variable,   // [n_slots, d_model]
    /// Learned memory values
    pub memory_values: Variable, // [n_slots, d_model]
}

impl DifferentiableMemory {
    pub fn new(d_model: usize, n_slots: usize) -> Self {
        // Initialize memory with small random values
        let std = (1.0 / d_model as f32).sqrt();

        let key_data = Array3::from_shape_fn((1, n_slots, d_model), |_| {
            use rand::Rng;
            rand::thread_rng().gen::<f32>() * std * 2.0 - std
        });

        let value_data = Array3::from_shape_fn((1, n_slots, d_model), |_| {
            use rand::Rng;
            rand::thread_rng().gen::<f32>() * std * 2.0 - std
        });

        Self {
            d_model,
            n_slots,
            key_proj: DifferentiableLinear::new(d_model, d_model, false),
            value_proj: DifferentiableLinear::new(d_model, d_model, false),
            query_proj: DifferentiableLinear::new(d_model, d_model, false),
            out_proj: DifferentiableLinear::new(d_model, d_model, false),
            memory_keys: Variable::parameter(key_data),
            memory_values: Variable::parameter(value_data),
        }
    }

    /// Forward pass - read from memory
    ///
    /// Query the memory using attention and return combined output.
    pub fn forward(&self, x: &Variable) -> Variable {
        let (batch, seq_len, d_model) = x.shape();
        let x_data = x.data();

        // Project input to query space
        let query = self.query_proj.forward(x);
        let query_data = query.data();

        // Get memory keys and values
        let keys_data = self.memory_keys.data();
        let values_data = self.memory_values.data();

        // Compute attention scores: Q @ K^T / sqrt(d)
        let scale = (d_model as f32).sqrt();
        let mut output = Array3::zeros((batch, seq_len, d_model));

        for b in 0..batch {
            for s in 0..seq_len {
                // Compute attention scores for this position
                let mut scores = vec![0.0f32; self.n_slots];
                let mut max_score = f32::NEG_INFINITY;

                for slot in 0..self.n_slots {
                    let mut score = 0.0f32;
                    for d in 0..d_model {
                        score += query_data[[b, s, d]] * keys_data[[0, slot, d]];
                    }
                    score /= scale;
                    scores[slot] = score;
                    max_score = max_score.max(score);
                }

                // Softmax
                let mut exp_sum = 0.0f32;
                for slot in 0..self.n_slots {
                    scores[slot] = (scores[slot] - max_score).exp();
                    exp_sum += scores[slot];
                }
                for slot in 0..self.n_slots {
                    scores[slot] /= exp_sum;
                }

                // Weighted sum of values
                for d in 0..d_model {
                    let mut sum = 0.0f32;
                    for slot in 0..self.n_slots {
                        sum += scores[slot] * values_data[[0, slot, d]];
                    }
                    output[[b, s, d]] = sum;
                }
            }
        }

        // Project and combine with input
        let mem_out = Variable::new(output, true);
        let projected = self.out_proj.forward(&mem_out);

        // Residual connection: output = x + memory_context
        x.add(&projected)
    }

    /// Compute a "surprise" score for monitoring
    /// This is used during inference for the test-time learning
    pub fn compute_surprise(&self, x: &Variable) -> f32 {
        let (batch, seq_len, d_model) = x.shape();
        let x_data = x.data();

        // Use last hidden state
        let mut h: Array1<f32> = Array1::zeros(d_model);
        for i in 0..d_model {
            h[i] = x_data[[batch - 1, seq_len - 1, i]];
        }

        // Project to query
        let query_data = self.query_proj.weight.data();
        let mut query: Array1<f32> = Array1::zeros(d_model);
        for i in 0..d_model {
            for j in 0..d_model {
                query[i] = query[i] + h[j] * query_data[[0, j, i]];
            }
        }

        // Find best matching memory
        let keys_data = self.memory_keys.data();
        let values_data = self.memory_values.data();

        let mut max_sim = f32::NEG_INFINITY;
        let mut best_slot = 0;

        for slot in 0..self.n_slots {
            let mut dot = 0.0f32;
            let mut norm_q = 0.0f32;
            let mut norm_k = 0.0f32;

            for d in 0..d_model {
                let q_val = query[d];
                let k_val = keys_data[[0, slot, d]];
                dot = dot + q_val * k_val;
                norm_q = norm_q + q_val * q_val;
                norm_k = norm_k + k_val * k_val;
            }

            let sim = dot / (norm_q.sqrt() * norm_k.sqrt() + 1e-8);
            if sim > max_sim {
                max_sim = sim;
                best_slot = slot;
            }
        }

        // Surprise = prediction error
        let value_proj_data = self.value_proj.weight.data();
        let mut projected_value: Array1<f32> = Array1::zeros(d_model);
        for i in 0..d_model {
            for j in 0..d_model {
                projected_value[i] = projected_value[i] + h[j] * value_proj_data[[0, j, i]];
            }
        }

        let mut error = 0.0f32;
        for d in 0..d_model {
            let diff = projected_value[d] - values_data[[0, best_slot, d]];
            error = error + diff * diff;
        }

        error.sqrt()
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.key_proj.parameters();
        params.extend(self.value_proj.parameters());
        params.extend(self.query_proj.parameters());
        params.extend(self.out_proj.parameters());
        params.push(self.memory_keys.clone());
        params.push(self.memory_values.clone());
        params
    }

    pub fn zero_grad(&self) {
        self.key_proj.zero_grad();
        self.value_proj.zero_grad();
        self.query_proj.zero_grad();
        self.out_proj.zero_grad();
        self.memory_keys.zero_grad();
        self.memory_values.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        let proj = self.d_model * self.d_model * 4; // 4 projections
        let memory = self.n_slots * self.d_model * 2; // keys + values
        proj + memory
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_differentiable_memory_forward() {
        let mem = DifferentiableMemory::new(64, 32);
        let x = Variable::parameter(Array3::ones((2, 8, 64)));
        let y = mem.forward(&x);
        assert_eq!(y.shape(), (2, 8, 64));
    }

    #[test]
    fn test_differentiable_memory_surprise() {
        let mem = DifferentiableMemory::new(64, 32);
        let x = Variable::parameter(Array3::ones((2, 8, 64)));
        let surprise = mem.compute_surprise(&x);
        assert!(surprise >= 0.0);
    }

    #[test]
    fn test_differentiable_memory_parameters() {
        let mem = DifferentiableMemory::new(64, 32);
        let params = mem.parameters();
        assert!(params.len() > 0);
        println!("Memory has {} parameter tensors", params.len());
    }
}
