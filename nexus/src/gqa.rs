//! Grouped Query Attention (GQA)
//!
//! Memory-efficient attention variant where multiple query heads share
//! key-value heads. Used in LLaMA 2 70B, Mistral, and other modern LLMs.
//!
//! Variants:
//! - MHA: n_kv_heads == n_heads (standard multi-head attention)
//! - GQA: n_kv_heads < n_heads (grouped query attention)
//! - MQA: n_kv_heads == 1 (multi-query attention)

use ndarray::Array4;
use crate::rope::RotaryEmbedding;
use crate::kv_cache::LayerKVCache;
use crate::autograd::{Variable, DifferentiableLinear};

/// Grouped Query Attention configuration
#[derive(Clone, Debug)]
pub struct GQAConfig {
    /// Model dimension
    pub d_model: usize,
    /// Number of query heads
    pub n_heads: usize,
    /// Number of key-value heads (must divide n_heads evenly)
    pub n_kv_heads: usize,
    /// Head dimension (d_model / n_heads)
    pub head_dim: usize,
    /// Maximum sequence length
    pub max_seq_len: usize,
    /// Dropout rate (for training)
    pub dropout: f32,
}

impl GQAConfig {
    pub fn new(d_model: usize, n_heads: usize, n_kv_heads: usize, max_seq_len: usize) -> Self {
        assert!(n_heads % n_kv_heads == 0, "n_heads must be divisible by n_kv_heads");
        let head_dim = d_model / n_heads;

        Self {
            d_model,
            n_heads,
            n_kv_heads,
            head_dim,
            max_seq_len,
            dropout: 0.0,
        }
    }

    /// Standard Multi-Head Attention
    pub fn mha(d_model: usize, n_heads: usize, max_seq_len: usize) -> Self {
        Self::new(d_model, n_heads, n_heads, max_seq_len)
    }

    /// Multi-Query Attention (single KV head)
    pub fn mqa(d_model: usize, n_heads: usize, max_seq_len: usize) -> Self {
        Self::new(d_model, n_heads, 1, max_seq_len)
    }

    /// Number of query heads per KV head
    pub fn n_rep(&self) -> usize {
        self.n_heads / self.n_kv_heads
    }
}

/// Grouped Query Attention layer
#[derive(Clone)]
pub struct GroupedQueryAttention {
    config: GQAConfig,
    /// Query projection
    wq: DifferentiableLinear,
    /// Key projection
    wk: DifferentiableLinear,
    /// Value projection
    wv: DifferentiableLinear,
    /// Output projection
    wo: DifferentiableLinear,
    /// Rotary embeddings
    rope: RotaryEmbedding,
}

impl GroupedQueryAttention {
    pub fn new(config: GQAConfig) -> Self {
        let d_model = config.d_model;
        let n_heads = config.n_heads;
        let n_kv_heads = config.n_kv_heads;
        let head_dim = config.head_dim;

        // Q projects to n_heads * head_dim
        // K, V project to n_kv_heads * head_dim
        let wq = DifferentiableLinear::new(d_model, n_heads * head_dim, false);
        let wk = DifferentiableLinear::new(d_model, n_kv_heads * head_dim, false);
        let wv = DifferentiableLinear::new(d_model, n_kv_heads * head_dim, false);
        let wo = DifferentiableLinear::new(n_heads * head_dim, d_model, false);

        let rope = RotaryEmbedding::with_default_base(head_dim, config.max_seq_len);

        Self { config, wq, wk, wv, wo, rope }
    }

    /// Forward pass with optional KV-cache
    ///
    /// # Arguments
    /// * `x` - Input [batch, seq_len, d_model]
    /// * `cache` - Optional KV cache for incremental decoding
    /// * `position_offset` - Starting position for RoPE
    /// * `mask` - Optional attention mask [batch, 1, seq_len, total_len]
    pub fn forward(
        &self,
        x: &Variable,
        cache: Option<&mut LayerKVCache>,
        position_offset: usize,
        mask: Option<&Array4<f32>>,
    ) -> Variable {
        let x_data = x.data();
        let (batch, seq_len, _) = x_data.dim();

        // Project Q, K, V
        let q = self.wq.forward(x); // [batch, seq, n_heads * head_dim]
        let k = self.wk.forward(x); // [batch, seq, n_kv_heads * head_dim]
        let v = self.wv.forward(x); // [batch, seq, n_kv_heads * head_dim]

        // Reshape to [batch, n_heads/n_kv_heads, seq, head_dim]
        let q_data = q.data();
        let k_data = k.data();
        let v_data = v.data();

        let n_heads = self.config.n_heads;
        let n_kv_heads = self.config.n_kv_heads;
        let head_dim = self.config.head_dim;

        // Reshape Q: [batch, seq, n_heads, head_dim] -> [batch, n_heads, seq, head_dim]
        let q_4d = q_data
            .to_shape((batch, seq_len, n_heads, head_dim))
            .unwrap()
            .permuted_axes([0, 2, 1, 3])
            .to_owned();

        // Reshape K, V: [batch, seq, n_kv_heads, head_dim] -> [batch, n_kv_heads, seq, head_dim]
        let k_4d = k_data
            .to_shape((batch, seq_len, n_kv_heads, head_dim))
            .unwrap()
            .permuted_axes([0, 2, 1, 3])
            .to_owned();

        let v_4d = v_data
            .to_shape((batch, seq_len, n_kv_heads, head_dim))
            .unwrap()
            .permuted_axes([0, 2, 1, 3])
            .to_owned();

        // Apply RoPE to Q and K
        // For Q: apply to all heads
        let (q_rot, _) = self.rope.forward(&q_4d, &q_4d, position_offset);
        // For K: apply to KV heads only
        let (k_rot, _) = self.rope.forward(&k_4d, &k_4d, position_offset);

        // Handle KV cache
        let (k_full, v_full) = match cache {
            Some(c) => c.update(&k_rot, &v_4d),
            None => (k_rot, v_4d),
        };

        let total_len = k_full.dim().2;

        // Repeat K, V for each query group
        let n_rep = self.config.n_rep();
        let k_expanded = self.repeat_kv(&k_full, n_rep);
        let v_expanded = self.repeat_kv(&v_full, n_rep);

        // Compute attention scores: Q @ K^T / sqrt(head_dim)
        let scale = (head_dim as f32).sqrt();
        let mut scores = Array4::zeros((batch, n_heads, seq_len, total_len));

        for b in 0..batch {
            for h in 0..n_heads {
                for sq in 0..seq_len {
                    for sk in 0..total_len {
                        let mut dot = 0.0f32;
                        for d in 0..head_dim {
                            dot += q_rot[[b, h, sq, d]] * k_expanded[[b, h, sk, d]];
                        }
                        scores[[b, h, sq, sk]] = dot / scale;
                    }
                }
            }
        }

        // Apply causal mask
        for b in 0..batch {
            for h in 0..n_heads {
                for sq in 0..seq_len {
                    let query_pos = position_offset + sq;
                    for sk in 0..total_len {
                        if sk > query_pos {
                            scores[[b, h, sq, sk]] = f32::NEG_INFINITY;
                        }
                    }
                }
            }
        }

        // Apply optional mask
        if let Some(m) = mask {
            for b in 0..batch {
                for h in 0..n_heads {
                    for sq in 0..seq_len {
                        for sk in 0..total_len {
                            if m[[b, 0, sq, sk]] == 0.0 {
                                scores[[b, h, sq, sk]] = f32::NEG_INFINITY;
                            }
                        }
                    }
                }
            }
        }

        // Softmax
        let mut attn = Array4::zeros((batch, n_heads, seq_len, total_len));
        for b in 0..batch {
            for h in 0..n_heads {
                for sq in 0..seq_len {
                    let max_score = (0..total_len)
                        .map(|sk| scores[[b, h, sq, sk]])
                        .fold(f32::NEG_INFINITY, f32::max);

                    let mut sum = 0.0f32;
                    for sk in 0..total_len {
                        attn[[b, h, sq, sk]] = (scores[[b, h, sq, sk]] - max_score).exp();
                        sum += attn[[b, h, sq, sk]];
                    }

                    if sum > 0.0 {
                        for sk in 0..total_len {
                            attn[[b, h, sq, sk]] /= sum;
                        }
                    }
                }
            }
        }

        // Apply attention to values
        let mut output_4d = Array4::zeros((batch, n_heads, seq_len, head_dim));
        for b in 0..batch {
            for h in 0..n_heads {
                for sq in 0..seq_len {
                    for d in 0..head_dim {
                        let mut sum = 0.0f32;
                        for sk in 0..total_len {
                            sum += attn[[b, h, sq, sk]] * v_expanded[[b, h, sk, d]];
                        }
                        output_4d[[b, h, sq, d]] = sum;
                    }
                }
            }
        }

        // Reshape back to [batch, seq, d_model]
        let output_3d = output_4d
            .permuted_axes([0, 2, 1, 3])
            .to_shape((batch, seq_len, n_heads * head_dim))
            .unwrap()
            .to_owned();

        // Output projection
        let output_var = Variable::new(output_3d, x.requires_grad);
        self.wo.forward(&output_var)
    }

    /// Repeat KV heads to match number of query heads
    fn repeat_kv(&self, x: &Array4<f32>, n_rep: usize) -> Array4<f32> {
        if n_rep == 1 {
            return x.clone();
        }

        let (batch, n_kv_heads, seq_len, head_dim) = x.dim();
        let n_heads = n_kv_heads * n_rep;

        let mut expanded = Array4::zeros((batch, n_heads, seq_len, head_dim));

        for b in 0..batch {
            for kv_h in 0..n_kv_heads {
                for rep in 0..n_rep {
                    let h = kv_h * n_rep + rep;
                    for s in 0..seq_len {
                        for d in 0..head_dim {
                            expanded[[b, h, s, d]] = x[[b, kv_h, s, d]];
                        }
                    }
                }
            }
        }

        expanded
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.wq.parameters();
        params.extend(self.wk.parameters());
        params.extend(self.wv.parameters());
        params.extend(self.wo.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.wq.zero_grad();
        self.wk.zero_grad();
        self.wv.zero_grad();
        self.wo.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        let d = self.config.d_model;
        let h = self.config.n_heads;
        let kv = self.config.n_kv_heads;
        let hd = self.config.head_dim;

        // Q: d_model -> n_heads * head_dim
        // K, V: d_model -> n_kv_heads * head_dim
        // O: n_heads * head_dim -> d_model
        d * h * hd + 2 * d * kv * hd + h * hd * d
    }

    pub fn config(&self) -> &GQAConfig {
        &self.config
    }
}

/// Flash-style chunked attention for memory efficiency
/// (Simplified version without full Flash Attention optimization)
#[derive(Clone)]
pub struct ChunkedGQA {
    gqa: GroupedQueryAttention,
    chunk_size: usize,
}

impl ChunkedGQA {
    pub fn new(config: GQAConfig, chunk_size: usize) -> Self {
        Self {
            gqa: GroupedQueryAttention::new(config),
            chunk_size,
        }
    }

    /// Forward with chunked processing for memory efficiency
    /// Note: chunked mode does not use KV-cache (use regular forward for incremental decoding)
    pub fn forward(
        &self,
        x: &Variable,
        cache: Option<&mut LayerKVCache>,
        position_offset: usize,
    ) -> Variable {
        let (batch, seq_len, d_model) = x.shape();

        if seq_len <= self.chunk_size {
            // Small enough to process normally
            return self.gqa.forward(x, cache, position_offset, None);
        }

        // Process in chunks (cache not used in chunked mode for simplicity)
        let x_data = x.data();
        let mut outputs = Vec::new();

        let mut pos = 0;
        while pos < seq_len {
            let end = (pos + self.chunk_size).min(seq_len);
            let chunk_len = end - pos;

            // Extract chunk
            let mut chunk_data = ndarray::Array3::zeros((batch, chunk_len, d_model));
            for b in 0..batch {
                for s in 0..chunk_len {
                    for d in 0..d_model {
                        chunk_data[[b, s, d]] = x_data[[b, pos + s, d]];
                    }
                }
            }

            let chunk_var = Variable::new(chunk_data, x.requires_grad);
            // No cache in chunked mode - each chunk is independent
            let chunk_out = self.gqa.forward(&chunk_var, None, position_offset + pos, None);
            outputs.push(chunk_out.data().to_owned());

            pos = end;
        }

        // Concatenate outputs
        let mut result = ndarray::Array3::zeros((batch, seq_len, d_model));
        let mut out_pos = 0;
        for out in outputs {
            let out_len = out.dim().1;
            for b in 0..batch {
                for s in 0..out_len {
                    for d in 0..d_model {
                        result[[b, out_pos + s, d]] = out[[b, s, d]];
                    }
                }
            }
            out_pos += out_len;
        }

        Variable::new(result, x.requires_grad)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        self.gqa.parameters()
    }

    pub fn zero_grad(&self) {
        self.gqa.zero_grad();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::Array3;

    #[test]
    fn test_gqa_config() {
        let config = GQAConfig::new(512, 8, 2, 2048);
        assert_eq!(config.n_rep(), 4); // 8 heads / 2 kv_heads
        assert_eq!(config.head_dim, 64);

        let mha = GQAConfig::mha(512, 8, 2048);
        assert_eq!(mha.n_rep(), 1);

        let mqa = GQAConfig::mqa(512, 8, 2048);
        assert_eq!(mqa.n_rep(), 8);
    }

    #[test]
    fn test_gqa_forward() {
        let config = GQAConfig::new(64, 4, 2, 512);
        let gqa = GroupedQueryAttention::new(config);

        let x = Variable::new(Array3::ones((2, 16, 64)), true);
        let output = gqa.forward(&x, None, 0, None);

        assert_eq!(output.shape(), (2, 16, 64));
    }

    #[test]
    fn test_gqa_with_cache() {
        let config = GQAConfig::new(64, 4, 2, 512);
        let gqa = GroupedQueryAttention::new(config.clone());
        let mut cache = LayerKVCache::new(config.n_kv_heads, config.head_dim, None);

        // First forward (prefill)
        let x1 = Variable::new(Array3::ones((1, 8, 64)), true);
        let out1 = gqa.forward(&x1, Some(&mut cache), 0, None);
        assert_eq!(cache.len(), 8);

        // Second forward (decode with cache)
        let x2 = Variable::new(Array3::ones((1, 1, 64)), true);
        let out2 = gqa.forward(&x2, Some(&mut cache), 8, None);
        assert_eq!(cache.len(), 9);
        assert_eq!(out2.shape(), (1, 1, 64));
    }

    #[test]
    fn test_gqa_mha_equivalence() {
        // GQA with n_kv_heads = n_heads should behave like standard MHA
        let config = GQAConfig::mha(64, 4, 512);
        let gqa = GroupedQueryAttention::new(config);

        let x = Variable::new(Array3::ones((1, 8, 64)), true);
        let output = gqa.forward(&x, None, 0, None);

        assert_eq!(output.shape(), (1, 8, 64));
    }

    #[test]
    fn test_gqa_mqa() {
        // Multi-Query Attention (single KV head)
        let config = GQAConfig::mqa(64, 4, 512);
        let gqa = GroupedQueryAttention::new(config);

        let x = Variable::new(Array3::ones((1, 8, 64)), true);
        let output = gqa.forward(&x, None, 0, None);

        assert_eq!(output.shape(), (1, 8, 64));

        // MQA should use less memory for KV
        let mha_config = GQAConfig::mha(64, 4, 512);
        let mqa_params = gqa.num_parameters();
        let mha_gqa = GroupedQueryAttention::new(mha_config);
        let mha_params = mha_gqa.num_parameters();

        assert!(mqa_params < mha_params, "MQA should have fewer parameters");
    }

    #[test]
    fn test_chunked_gqa() {
        let config = GQAConfig::new(64, 4, 2, 512);
        let chunked = ChunkedGQA::new(config, 8);

        // Test with sequence longer than chunk size
        let x = Variable::new(Array3::ones((1, 20, 64)), true);
        let output = chunked.forward(&x, None, 0);

        assert_eq!(output.shape(), (1, 20, 64));
    }

    #[test]
    fn test_repeat_kv() {
        let config = GQAConfig::new(64, 8, 2, 512);
        let gqa = GroupedQueryAttention::new(config);

        let kv = Array4::from_shape_fn((1, 2, 4, 16), |(_, h, _, _)| h as f32);
        let expanded = gqa.repeat_kv(&kv, 4);

        assert_eq!(expanded.dim(), (1, 8, 4, 16));

        // Check that heads 0-3 have value 0.0 and heads 4-7 have value 1.0
        assert!((expanded[[0, 0, 0, 0]] - 0.0).abs() < 1e-6);
        assert!((expanded[[0, 3, 0, 0]] - 0.0).abs() < 1e-6);
        assert!((expanded[[0, 4, 0, 0]] - 1.0).abs() < 1e-6);
        assert!((expanded[[0, 7, 0, 0]] - 1.0).abs() < 1e-6);
    }
}
