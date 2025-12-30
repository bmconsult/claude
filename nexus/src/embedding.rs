//! Embedding layer for converting token IDs to dense vectors
//!
//! Includes both token embeddings and positional encodings.

use ndarray::{Array2, Array3, s};
use rand_distr::{Normal, Distribution};
use serde::{Deserialize, Serialize};

/// Token embedding layer with positional encoding
#[derive(Clone, Serialize, Deserialize)]
pub struct Embedding {
    /// Token embedding matrix: vocab_size × d_model
    pub token_embed: Array2<f32>,
    /// Positional encoding: max_seq_len × d_model
    pub pos_embed: Array2<f32>,
    /// Vocabulary size
    pub vocab_size: usize,
    /// Model dimension
    pub d_model: usize,
    /// Maximum sequence length
    pub max_seq_len: usize,
}

impl Embedding {
    /// Create new embedding layer with random initialization
    pub fn new(vocab_size: usize, d_model: usize, max_seq_len: usize) -> Self {
        let mut rng = rand::thread_rng();

        // Xavier/Glorot initialization for embeddings
        let std = (2.0 / (vocab_size + d_model) as f32).sqrt();
        let normal = Normal::new(0.0, std).unwrap();

        let token_embed = Array2::from_shape_fn((vocab_size, d_model), |_| {
            normal.sample(&mut rng)
        });

        // Sinusoidal positional encoding (from "Attention Is All You Need")
        let pos_embed = Self::sinusoidal_encoding(max_seq_len, d_model);

        Self {
            token_embed,
            pos_embed,
            vocab_size,
            d_model,
            max_seq_len,
        }
    }

    /// Create sinusoidal positional encoding
    fn sinusoidal_encoding(max_len: usize, d_model: usize) -> Array2<f32> {
        let mut encoding = Array2::zeros((max_len, d_model));

        for pos in 0..max_len {
            for i in 0..d_model {
                let angle = pos as f32 / 10000_f32.powf((2 * (i / 2)) as f32 / d_model as f32);
                if i % 2 == 0 {
                    encoding[[pos, i]] = angle.sin();
                } else {
                    encoding[[pos, i]] = angle.cos();
                }
            }
        }

        encoding
    }

    /// Forward pass: convert token IDs to embeddings
    ///
    /// # Arguments
    /// * `token_ids` - Token IDs, shape (batch_size, seq_len)
    ///
    /// # Returns
    /// Embeddings of shape (batch_size, seq_len, d_model)
    pub fn forward(&self, token_ids: &[Vec<u32>]) -> Array3<f32> {
        let batch_size = token_ids.len();
        let seq_len = token_ids[0].len();

        assert!(seq_len <= self.max_seq_len,
            "Sequence length {} exceeds maximum {}", seq_len, self.max_seq_len);

        let mut output = Array3::zeros((batch_size, seq_len, self.d_model));

        for (b, tokens) in token_ids.iter().enumerate() {
            for (t, &token_id) in tokens.iter().enumerate() {
                let tid = (token_id as usize).min(self.vocab_size - 1);

                // Token embedding + positional encoding
                for d in 0..self.d_model {
                    output[[b, t, d]] = self.token_embed[[tid, d]] + self.pos_embed[[t, d]];
                }
            }
        }

        output
    }

    /// Forward pass from single flat sequence
    pub fn forward_single(&self, token_ids: &[u32]) -> Array3<f32> {
        self.forward(&[token_ids.to_vec()])
    }

    /// Unembed: project from d_model back to vocab logits
    ///
    /// Uses tied weights (transpose of token embedding)
    pub fn unembed(&self, hidden: &Array3<f32>) -> Array3<f32> {
        let (batch_size, seq_len, _d_model) = hidden.dim();

        let mut logits = Array3::zeros((batch_size, seq_len, self.vocab_size));

        for b in 0..batch_size {
            for t in 0..seq_len {
                for v in 0..self.vocab_size {
                    let mut sum = 0.0;
                    for d in 0..self.d_model {
                        sum += hidden[[b, t, d]] * self.token_embed[[v, d]];
                    }
                    logits[[b, t, v]] = sum;
                }
            }
        }

        logits
    }

    /// Get embedding for a single token (for weight tying)
    pub fn get_token_embedding(&self, token_id: u32) -> ndarray::ArrayView1<'_, f32> {
        let tid = (token_id as usize).min(self.vocab_size - 1);
        self.token_embed.slice(s![tid, ..])
    }

    /// Number of parameters
    pub fn num_parameters(&self) -> usize {
        // Only count token embeddings (positional is deterministic)
        self.vocab_size * self.d_model
    }
}

/// Learnable positional embedding (alternative to sinusoidal)
#[derive(Clone, Serialize, Deserialize)]
pub struct LearnedPositionalEmbedding {
    /// Position embedding matrix: max_seq_len × d_model
    pub embed: Array2<f32>,
    pub max_seq_len: usize,
    pub d_model: usize,
}

impl LearnedPositionalEmbedding {
    /// Create new learnable positional embedding
    pub fn new(max_seq_len: usize, d_model: usize) -> Self {
        let mut rng = rand::thread_rng();
        let std = 0.02; // Small initialization
        let normal = Normal::new(0.0, std).unwrap();

        let embed = Array2::from_shape_fn((max_seq_len, d_model), |_| {
            normal.sample(&mut rng)
        });

        Self { embed, max_seq_len, d_model }
    }

    /// Get positional embeddings for a sequence
    pub fn forward(&self, seq_len: usize) -> ndarray::ArrayView2<'_, f32> {
        self.embed.slice(s![..seq_len, ..])
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_embedding_creation() {
        let embed = Embedding::new(100, 64, 512);
        assert_eq!(embed.vocab_size, 100);
        assert_eq!(embed.d_model, 64);
        assert_eq!(embed.token_embed.dim(), (100, 64));
        assert_eq!(embed.pos_embed.dim(), (512, 64));
    }

    #[test]
    fn test_embedding_forward() {
        let embed = Embedding::new(100, 64, 512);

        // Batch of 2 sequences, length 10
        let tokens = vec![
            vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            vec![10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        ];

        let output = embed.forward(&tokens);
        assert_eq!(output.dim(), (2, 10, 64));
    }

    #[test]
    fn test_embedding_single() {
        let embed = Embedding::new(100, 64, 512);

        let tokens = vec![5, 10, 15, 20];
        let output = embed.forward_single(&tokens);
        assert_eq!(output.dim(), (1, 4, 64));
    }

    #[test]
    fn test_unembed() {
        let embed = Embedding::new(100, 64, 512);

        let hidden = Array3::zeros((1, 4, 64));
        let logits = embed.unembed(&hidden);
        assert_eq!(logits.dim(), (1, 4, 100)); // vocab_size logits
    }

    #[test]
    fn test_positional_encoding_properties() {
        let embed = Embedding::new(100, 64, 512);

        // Sinusoidal encoding should have values in [-1, 1]
        for val in embed.pos_embed.iter() {
            assert!(*val >= -1.0 && *val <= 1.0);
        }
    }

    #[test]
    fn test_num_parameters() {
        let embed = Embedding::new(32000, 512, 8192);
        // 32000 * 512 = 16,384,000 parameters
        assert_eq!(embed.num_parameters(), 32000 * 512);
    }
}
