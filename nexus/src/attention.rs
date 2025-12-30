//! Multi-Head Attention with Rotary Position Embeddings (RoPE)
//!
//! Implements the attention mechanism used sparingly (1:7 ratio) in the hybrid architecture.

use ndarray::{Array2, Array3};
use serde::{Serialize, Deserialize};
use crate::tensor::{Tensor, Linear};

/// Rotary Position Embedding
#[derive(Clone, Serialize, Deserialize)]
pub struct RoPE {
    /// Precomputed cos values
    cos: Array2<f32>,
    /// Precomputed sin values
    sin: Array2<f32>,
    /// Maximum sequence length
    max_seq_len: usize,
    /// Head dimension
    head_dim: usize,
}

impl RoPE {
    pub fn new(head_dim: usize, max_seq_len: usize, base: f32) -> Self {
        let mut cos = Array2::zeros((max_seq_len, head_dim));
        let mut sin = Array2::zeros((max_seq_len, head_dim));

        for pos in 0..max_seq_len {
            for i in 0..head_dim / 2 {
                let freq = 1.0 / base.powf(2.0 * i as f32 / head_dim as f32);
                let angle = pos as f32 * freq;
                cos[[pos, i]] = angle.cos();
                cos[[pos, i + head_dim / 2]] = angle.cos();
                sin[[pos, i]] = angle.sin();
                sin[[pos, i + head_dim / 2]] = angle.sin();
            }
        }

        Self { cos, sin, max_seq_len, head_dim }
    }

    /// Apply rotary embedding to query/key
    pub fn apply(&self, x: &Tensor, offset: usize) -> Tensor {
        let (batch, seq_len, d_model) = x.shape();
        let mut result = x.data.clone();

        for b in 0..batch {
            for s in 0..seq_len {
                let pos = s + offset;
                if pos >= self.max_seq_len {
                    continue;
                }

                for h in 0..d_model / self.head_dim {
                    let base = h * self.head_dim;
                    for i in 0..self.head_dim / 2 {
                        let x0 = x.data[[b, s, base + i]];
                        let x1 = x.data[[b, s, base + i + self.head_dim / 2]];

                        result[[b, s, base + i]] =
                            x0 * self.cos[[pos, i]] - x1 * self.sin[[pos, i]];
                        result[[b, s, base + i + self.head_dim / 2]] =
                            x0 * self.sin[[pos, i]] + x1 * self.cos[[pos, i]];
                    }
                }
            }
        }

        Tensor { data: result }
    }
}

/// Multi-Head Attention
#[derive(Clone, Serialize, Deserialize)]
pub struct MultiHeadAttention {
    /// Number of heads
    n_heads: usize,
    /// Dimension per head
    head_dim: usize,
    /// Query projection
    q_proj: Linear,
    /// Key projection
    k_proj: Linear,
    /// Value projection
    v_proj: Linear,
    /// Output projection
    o_proj: Linear,
    /// Rotary position embedding
    rope: RoPE,
    /// Scale factor
    scale: f32,
}

impl MultiHeadAttention {
    pub fn new(d_model: usize, n_heads: usize, max_seq_len: usize) -> Self {
        let head_dim = d_model / n_heads;
        let scale = (head_dim as f32).sqrt().recip();

        Self {
            n_heads,
            head_dim,
            q_proj: Linear::new(d_model, d_model, false),
            k_proj: Linear::new(d_model, d_model, false),
            v_proj: Linear::new(d_model, d_model, false),
            o_proj: Linear::new(d_model, d_model, false),
            rope: RoPE::new(head_dim, max_seq_len, 10000.0),
            scale,
        }
    }

    /// Forward pass
    /// x: [batch, seq_len, d_model]
    /// Returns: [batch, seq_len, d_model]
    pub fn forward(&self, x: &Tensor, causal_mask: bool) -> Tensor {
        let (batch, seq_len, _) = x.shape();

        // Project to Q, K, V
        let q = self.q_proj.forward(x);
        let k = self.k_proj.forward(x);
        let v = self.v_proj.forward(x);

        // Apply RoPE to Q and K
        let q = self.rope.apply(&q, 0);
        let k = self.rope.apply(&k, 0);

        // Reshape for multi-head: [batch, seq, n_heads, head_dim]
        // Then compute attention scores
        let mut attn_output = Array3::zeros((batch, seq_len, self.n_heads * self.head_dim));

        for b in 0..batch {
            for h in 0..self.n_heads {
                let head_start = h * self.head_dim;
                let head_end = head_start + self.head_dim;

                // Extract Q, K, V for this head
                // scores[i, j] = Q[i] · K[j]
                let mut scores = Array2::zeros((seq_len, seq_len));

                for i in 0..seq_len {
                    for j in 0..seq_len {
                        let mut dot = 0.0f32;
                        for d in head_start..head_end {
                            dot += q.data[[b, i, d]] * k.data[[b, j, d]];
                        }
                        scores[[i, j]] = dot * self.scale;

                        // Causal mask
                        if causal_mask && j > i {
                            scores[[i, j]] = f32::NEG_INFINITY;
                        }
                    }
                }

                // Softmax over keys
                for i in 0..seq_len {
                    let max = scores.row(i).iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                    let mut sum = 0.0f32;
                    for j in 0..seq_len {
                        scores[[i, j]] = (scores[[i, j]] - max).exp();
                        sum += scores[[i, j]];
                    }
                    for j in 0..seq_len {
                        scores[[i, j]] /= sum;
                    }
                }

                // Apply attention: output = scores @ V
                for i in 0..seq_len {
                    for d in 0..self.head_dim {
                        let mut sum = 0.0f32;
                        for j in 0..seq_len {
                            sum += scores[[i, j]] * v.data[[b, j, head_start + d]];
                        }
                        attn_output[[b, i, head_start + d]] = sum;
                    }
                }
            }
        }

        // Output projection
        let attn = Tensor { data: attn_output };
        self.o_proj.forward(&attn)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_attention_shape() {
        let attn = MultiHeadAttention::new(64, 4, 512);
        let x = Tensor::randn(2, 8, 64);
        let y = attn.forward(&x, true);
        assert_eq!(y.shape(), (2, 8, 64));
    }

    #[test]
    fn test_rope() {
        let rope = RoPE::new(32, 512, 10000.0);
        let x = Tensor::randn(1, 4, 64);
        let y = rope.apply(&x, 0);
        assert_eq!(y.shape(), x.shape());
    }
}
