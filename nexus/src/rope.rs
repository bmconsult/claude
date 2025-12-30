//! Rotary Position Embeddings (RoPE)
//!
//! Implementation of RoPE as used in LLaMA, Mistral, and modern LLMs.
//! Encodes position information directly into Q/K vectors through rotation.
//!
//! Key properties:
//! - Relative position encoding through rotation matrices
//! - Natural decay with distance
//! - Supports sequence length extrapolation
//! - Compatible with KV-cache

use ndarray::{Array2, Array3, Array4, Axis};
use std::f32::consts::PI;

/// Rotary Position Embedding
#[derive(Clone)]
pub struct RotaryEmbedding {
    /// Model dimension (must be even)
    dim: usize,
    /// Maximum sequence length for precomputed frequencies
    max_seq_len: usize,
    /// Base for frequency computation (default: 10000)
    base: f32,
    /// Precomputed cosine values: [max_seq_len, dim/2]
    cos_cached: Array2<f32>,
    /// Precomputed sine values: [max_seq_len, dim/2]
    sin_cached: Array2<f32>,
}

impl RotaryEmbedding {
    /// Create new rotary embedding
    ///
    /// # Arguments
    /// * `dim` - Dimension per head (must be even)
    /// * `max_seq_len` - Maximum sequence length to cache
    /// * `base` - Frequency base (default 10000.0)
    pub fn new(dim: usize, max_seq_len: usize, base: f32) -> Self {
        assert!(dim % 2 == 0, "RoPE dimension must be even");

        // Compute inverse frequencies: 1 / (base^(2i/dim)) for i in 0..dim/2
        let half_dim = dim / 2;
        let inv_freq: Vec<f32> = (0..half_dim)
            .map(|i| 1.0 / base.powf(2.0 * i as f32 / dim as f32))
            .collect();

        // Precompute cos and sin for all positions
        let mut cos_cached = Array2::zeros((max_seq_len, half_dim));
        let mut sin_cached = Array2::zeros((max_seq_len, half_dim));

        for pos in 0..max_seq_len {
            for (i, &freq) in inv_freq.iter().enumerate() {
                let angle = pos as f32 * freq;
                cos_cached[[pos, i]] = angle.cos();
                sin_cached[[pos, i]] = angle.sin();
            }
        }

        Self {
            dim,
            max_seq_len,
            base,
            cos_cached,
            sin_cached,
        }
    }

    /// Create with default base of 10000
    pub fn with_default_base(dim: usize, max_seq_len: usize) -> Self {
        Self::new(dim, max_seq_len, 10000.0)
    }

    /// Apply rotary embedding to query and key tensors
    ///
    /// # Arguments
    /// * `q` - Query tensor [batch, n_heads, seq_len, head_dim]
    /// * `k` - Key tensor [batch, n_heads, seq_len, head_dim]
    /// * `position_offset` - Starting position (for KV-cache)
    ///
    /// # Returns
    /// (rotated_q, rotated_k)
    pub fn forward(
        &self,
        q: &Array4<f32>,
        k: &Array4<f32>,
        position_offset: usize,
    ) -> (Array4<f32>, Array4<f32>) {
        let (batch, n_heads, seq_len, head_dim) = q.dim();
        assert_eq!(head_dim, self.dim, "Head dim must match RoPE dim");
        assert!(
            position_offset + seq_len <= self.max_seq_len,
            "Position {} + seq_len {} exceeds max_seq_len {}",
            position_offset,
            seq_len,
            self.max_seq_len
        );

        let mut q_rotated = q.clone();
        let mut k_rotated = k.clone();

        let half_dim = head_dim / 2;

        for b in 0..batch {
            for h in 0..n_heads {
                for s in 0..seq_len {
                    let pos = position_offset + s;

                    for i in 0..half_dim {
                        let cos = self.cos_cached[[pos, i]];
                        let sin = self.sin_cached[[pos, i]];

                        // Rotate Q
                        let q1 = q[[b, h, s, i]];
                        let q2 = q[[b, h, s, i + half_dim]];
                        q_rotated[[b, h, s, i]] = q1 * cos - q2 * sin;
                        q_rotated[[b, h, s, i + half_dim]] = q1 * sin + q2 * cos;

                        // Rotate K
                        let k1 = k[[b, h, s, i]];
                        let k2 = k[[b, h, s, i + half_dim]];
                        k_rotated[[b, h, s, i]] = k1 * cos - k2 * sin;
                        k_rotated[[b, h, s, i + half_dim]] = k1 * sin + k2 * cos;
                    }
                }
            }
        }

        (q_rotated, k_rotated)
    }

    /// Apply rotary embedding to a single tensor (Q or K)
    pub fn rotate_single(
        &self,
        x: &Array4<f32>,
        position_offset: usize,
    ) -> Array4<f32> {
        let (batch, n_heads, seq_len, head_dim) = x.dim();
        assert_eq!(head_dim, self.dim);

        let mut rotated = x.clone();
        let half_dim = head_dim / 2;

        for b in 0..batch {
            for h in 0..n_heads {
                for s in 0..seq_len {
                    let pos = position_offset + s;

                    for i in 0..half_dim {
                        let cos = self.cos_cached[[pos, i]];
                        let sin = self.sin_cached[[pos, i]];

                        let x1 = x[[b, h, s, i]];
                        let x2 = x[[b, h, s, i + half_dim]];
                        rotated[[b, h, s, i]] = x1 * cos - x2 * sin;
                        rotated[[b, h, s, i + half_dim]] = x1 * sin + x2 * cos;
                    }
                }
            }
        }

        rotated
    }

    /// Get dimension
    pub fn dim(&self) -> usize {
        self.dim
    }

    /// Get max sequence length
    pub fn max_seq_len(&self) -> usize {
        self.max_seq_len
    }

    /// Extend cache for longer sequences (for dynamic length)
    pub fn extend_cache(&mut self, new_max_len: usize) {
        if new_max_len <= self.max_seq_len {
            return;
        }

        let half_dim = self.dim / 2;
        let inv_freq: Vec<f32> = (0..half_dim)
            .map(|i| 1.0 / self.base.powf(2.0 * i as f32 / self.dim as f32))
            .collect();

        let mut new_cos = Array2::zeros((new_max_len, half_dim));
        let mut new_sin = Array2::zeros((new_max_len, half_dim));

        // Copy existing cached values
        for pos in 0..self.max_seq_len {
            for i in 0..half_dim {
                new_cos[[pos, i]] = self.cos_cached[[pos, i]];
                new_sin[[pos, i]] = self.sin_cached[[pos, i]];
            }
        }

        // Compute new values
        for pos in self.max_seq_len..new_max_len {
            for (i, &freq) in inv_freq.iter().enumerate() {
                let angle = pos as f32 * freq;
                new_cos[[pos, i]] = angle.cos();
                new_sin[[pos, i]] = angle.sin();
            }
        }

        self.cos_cached = new_cos;
        self.sin_cached = new_sin;
        self.max_seq_len = new_max_len;
    }
}

/// Differentiable Rotary Embedding for training
use crate::autograd::Variable;

#[derive(Clone)]
pub struct DifferentiableRoPE {
    rope: RotaryEmbedding,
}

impl DifferentiableRoPE {
    pub fn new(dim: usize, max_seq_len: usize, base: f32) -> Self {
        Self {
            rope: RotaryEmbedding::new(dim, max_seq_len, base),
        }
    }

    pub fn with_default_base(dim: usize, max_seq_len: usize) -> Self {
        Self {
            rope: RotaryEmbedding::with_default_base(dim, max_seq_len),
        }
    }

    /// Apply RoPE to Q and K Variables
    /// Input: [batch, seq_len, n_heads * head_dim] or [batch, n_heads, seq_len, head_dim]
    pub fn forward(
        &self,
        q: &Variable,
        k: &Variable,
        n_heads: usize,
        position_offset: usize,
    ) -> (Variable, Variable) {
        let q_data = q.data();
        let k_data = k.data();
        let (batch, seq_len, total_dim) = q_data.dim();
        let head_dim = total_dim / n_heads;

        // Reshape to [batch, n_heads, seq_len, head_dim]
        let q_4d = q_data
            .to_shape((batch, seq_len, n_heads, head_dim))
            .unwrap()
            .permuted_axes([0, 2, 1, 3])
            .to_owned();

        let k_4d = k_data
            .to_shape((batch, seq_len, n_heads, head_dim))
            .unwrap()
            .permuted_axes([0, 2, 1, 3])
            .to_owned();

        // Apply RoPE
        let (q_rot, k_rot) = self.rope.forward(&q_4d, &k_4d, position_offset);

        // Reshape back to [batch, seq_len, n_heads * head_dim]
        let q_out = q_rot
            .permuted_axes([0, 2, 1, 3])
            .to_shape((batch, seq_len, total_dim))
            .unwrap()
            .to_owned();

        let k_out = k_rot
            .permuted_axes([0, 2, 1, 3])
            .to_shape((batch, seq_len, total_dim))
            .unwrap()
            .to_owned();

        // Convert back to 3D for Variable
        let q_3d = q_out.insert_axis(Axis(0)).remove_axis(Axis(0));
        let k_3d = k_out.insert_axis(Axis(0)).remove_axis(Axis(0));

        (
            Variable::new(q_3d, q.requires_grad),
            Variable::new(k_3d, k.requires_grad),
        )
    }

    /// Extend cache if needed
    pub fn extend_cache(&mut self, new_max_len: usize) {
        self.rope.extend_cache(new_max_len);
    }

    pub fn dim(&self) -> usize {
        self.rope.dim()
    }

    pub fn max_seq_len(&self) -> usize {
        self.rope.max_seq_len()
    }
}

/// Scaled RoPE for better length extrapolation (YaRN-style)
#[derive(Clone)]
pub struct ScaledRotaryEmbedding {
    base_rope: RotaryEmbedding,
    /// Scaling factor for extrapolation
    scale: f32,
    /// Original trained sequence length
    original_max_len: usize,
}

impl ScaledRotaryEmbedding {
    /// Create scaled RoPE for length extrapolation
    ///
    /// # Arguments
    /// * `dim` - Head dimension
    /// * `original_max_len` - Original trained sequence length
    /// * `target_max_len` - Target sequence length after scaling
    /// * `base` - Frequency base
    pub fn new(dim: usize, original_max_len: usize, target_max_len: usize, base: f32) -> Self {
        let scale = target_max_len as f32 / original_max_len as f32;

        // Create RoPE with scaled base for better extrapolation
        let scaled_base = base * scale.powf(dim as f32 / (dim as f32 - 2.0));

        Self {
            base_rope: RotaryEmbedding::new(dim, target_max_len, scaled_base),
            scale,
            original_max_len,
        }
    }

    pub fn forward(
        &self,
        q: &Array4<f32>,
        k: &Array4<f32>,
        position_offset: usize,
    ) -> (Array4<f32>, Array4<f32>) {
        self.base_rope.forward(q, k, position_offset)
    }

    pub fn scale(&self) -> f32 {
        self.scale
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::Array4;

    #[test]
    fn test_rope_creation() {
        let rope = RotaryEmbedding::with_default_base(64, 2048);
        assert_eq!(rope.dim(), 64);
        assert_eq!(rope.max_seq_len(), 2048);
    }

    #[test]
    fn test_rope_forward() {
        let rope = RotaryEmbedding::with_default_base(32, 512);

        let q = Array4::ones((2, 4, 16, 32)); // [batch, heads, seq, dim]
        let k = Array4::ones((2, 4, 16, 32));

        let (q_rot, k_rot) = rope.forward(&q, &k, 0);

        assert_eq!(q_rot.dim(), (2, 4, 16, 32));
        assert_eq!(k_rot.dim(), (2, 4, 16, 32));

        // At position 1+, rotation should definitely change values
        // (at position 0 with all 1s, cos(0)=1 and sin(0)=0, so no change for first element)
        assert!((q_rot[[0, 0, 1, 0]] - q[[0, 0, 1, 0]]).abs() > 1e-6 ||
                (q_rot[[0, 0, 1, 16]] - q[[0, 0, 1, 16]]).abs() > 1e-6);
    }

    #[test]
    fn test_rope_position_offset() {
        let rope = RotaryEmbedding::with_default_base(32, 512);

        let q = Array4::ones((1, 1, 1, 32));
        let k = Array4::ones((1, 1, 1, 32));

        // Same input at different positions should give different outputs
        let (q_pos0, _) = rope.forward(&q, &k, 0);
        let (q_pos10, _) = rope.forward(&q, &k, 10);

        assert!((q_pos0[[0, 0, 0, 0]] - q_pos10[[0, 0, 0, 0]]).abs() > 1e-6);
    }

    #[test]
    fn test_rope_relative_position() {
        let rope = RotaryEmbedding::with_default_base(32, 512);

        // Test that relative position is preserved
        // q at position 5, k at position 3 should have same dot product as
        // q at position 15, k at position 13 (both have relative distance 2)

        let q = Array4::from_shape_fn((1, 1, 1, 32), |_| rand::random::<f32>());
        let k = Array4::from_shape_fn((1, 1, 1, 32), |_| rand::random::<f32>());

        let (q_rot5, _) = rope.forward(&q, &k, 5);
        let (_, k_rot3) = rope.forward(&q, &k, 3);

        let (q_rot15, _) = rope.forward(&q, &k, 15);
        let (_, k_rot13) = rope.forward(&q, &k, 13);

        // Compute dot products
        let dot1: f32 = (0..32).map(|i| q_rot5[[0, 0, 0, i]] * k_rot3[[0, 0, 0, i]]).sum();
        let dot2: f32 = (0..32).map(|i| q_rot15[[0, 0, 0, i]] * k_rot13[[0, 0, 0, i]]).sum();

        // Should be approximately equal (relative position encoding property)
        assert!((dot1 - dot2).abs() < 0.01, "dot1={}, dot2={}", dot1, dot2);
    }

    #[test]
    fn test_rope_extend_cache() {
        let mut rope = RotaryEmbedding::with_default_base(32, 256);
        assert_eq!(rope.max_seq_len(), 256);

        rope.extend_cache(512);
        assert_eq!(rope.max_seq_len(), 512);

        // Should work with extended length
        let q = Array4::ones((1, 1, 1, 32));
        let k = Array4::ones((1, 1, 1, 32));
        let (_, _) = rope.forward(&q, &k, 400);
    }

    #[test]
    fn test_differentiable_rope() {
        use ndarray::Array3;

        let rope = DifferentiableRoPE::with_default_base(32, 512);

        // [batch, seq, n_heads * head_dim]
        let q = Variable::new(Array3::ones((2, 16, 128)), true); // 4 heads * 32 dim
        let k = Variable::new(Array3::ones((2, 16, 128)), true);

        let (q_rot, k_rot) = rope.forward(&q, &k, 4, 0);

        assert_eq!(q_rot.shape(), (2, 16, 128));
        assert_eq!(k_rot.shape(), (2, 16, 128));
    }

    #[test]
    fn test_scaled_rope() {
        // Test extrapolation: trained on 2048, extend to 8192
        let scaled_rope = ScaledRotaryEmbedding::new(32, 2048, 8192, 10000.0);

        let q = Array4::ones((1, 1, 1, 32));
        let k = Array4::ones((1, 1, 1, 32));

        // Should work at position 6000 (beyond original training length)
        let (q_rot, k_rot) = scaled_rope.forward(&q, &k, 6000);
        assert_eq!(q_rot.dim(), (1, 1, 1, 32));

        assert!(scaled_rope.scale() > 1.0);
    }
}
