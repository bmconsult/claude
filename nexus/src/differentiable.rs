//! Differentiable Nexus Model
//!
//! Full autograd-enabled version of NexusLM for training.
//! Includes hybrid attention/SSM blocks and memory.

use ndarray::{Array1, Array3};
use crate::autograd::{Variable, DifferentiableLinear};
use crate::differentiable_ssm::DifferentiableSSM;
use crate::differentiable_memory::DifferentiableMemory;
use crate::NexusConfig;

/// Differentiable RMS Normalization
#[derive(Clone)]
pub struct DifferentiableRMSNorm {
    pub weight: Variable,
    pub eps: f32,
    _d_model: usize,
}

impl DifferentiableRMSNorm {
    pub fn new(d_model: usize, eps: f32) -> Self {
        let weight_data = Array3::ones((1, 1, d_model));
        Self {
            weight: Variable::parameter(weight_data),
            eps,
            _d_model: d_model,
        }
    }

    pub fn forward(&self, x: &Variable) -> Variable {
        let weight_1d = Array1::from_iter(
            self.weight.data().iter().cloned()
        );
        x.rms_norm(&weight_1d, self.eps)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        vec![self.weight.clone()]
    }

    pub fn zero_grad(&self) {
        self.weight.zero_grad();
    }
}

/// Differentiable SwiGLU MLP
#[derive(Clone)]
pub struct DifferentiableMLP {
    pub up_proj: DifferentiableLinear,
    pub gate_proj: DifferentiableLinear,
    pub down_proj: DifferentiableLinear,
}

impl DifferentiableMLP {
    pub fn new(d_model: usize, d_ff: usize) -> Self {
        Self {
            up_proj: DifferentiableLinear::new(d_model, d_ff, false),
            gate_proj: DifferentiableLinear::new(d_model, d_ff, false),
            down_proj: DifferentiableLinear::new(d_ff, d_model, false),
        }
    }

    /// SwiGLU: down(up(x) * silu(gate(x)))
    pub fn forward(&self, x: &Variable) -> Variable {
        let up = self.up_proj.forward(x);
        let gate = self.gate_proj.forward(x).silu();
        let hidden = up.mul(&gate);
        self.down_proj.forward(&hidden)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.up_proj.parameters();
        params.extend(self.gate_proj.parameters());
        params.extend(self.down_proj.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.up_proj.zero_grad();
        self.gate_proj.zero_grad();
        self.down_proj.zero_grad();
    }
}

/// Differentiable Causal Self-Attention
#[derive(Clone)]
pub struct DifferentiableAttention {
    pub q_proj: DifferentiableLinear,
    pub k_proj: DifferentiableLinear,
    pub v_proj: DifferentiableLinear,
    pub out_proj: DifferentiableLinear,
    _n_heads: usize,
    _head_dim: usize,
    d_model: usize,
}

impl DifferentiableAttention {
    pub fn new(d_model: usize, n_heads: usize) -> Self {
        let head_dim = d_model / n_heads;
        Self {
            q_proj: DifferentiableLinear::new(d_model, d_model, false),
            k_proj: DifferentiableLinear::new(d_model, d_model, false),
            v_proj: DifferentiableLinear::new(d_model, d_model, false),
            out_proj: DifferentiableLinear::new(d_model, d_model, false),
            _n_heads: n_heads,
            _head_dim: head_dim,
            d_model,
        }
    }

    pub fn forward(&self, x: &Variable) -> Variable {
        let (batch, seq_len, _) = x.shape();

        // Project to Q, K, V
        let q = self.q_proj.forward(x);
        let k = self.k_proj.forward(x);
        let v = self.v_proj.forward(x);

        // Simple attention (not multi-head split for now)
        // scores = Q @ K^T / sqrt(d)
        let scale = (self.d_model as f32).sqrt();

        // Manual attention computation
        let q_data = q.data();
        let k_data = k.data();
        let v_data = v.data();

        let mut output_data = Array3::zeros((batch, seq_len, self.d_model));

        for b in 0..batch {
            for i in 0..seq_len {
                // Compute attention scores for position i
                let mut scores = vec![0.0f32; seq_len];
                let mut max_score = f32::NEG_INFINITY;

                for j in 0..=i {  // Causal mask: only attend to past
                    let mut score = 0.0f32;
                    for d in 0..self.d_model {
                        score += q_data[[b, i, d]] * k_data[[b, j, d]];
                    }
                    score /= scale;
                    scores[j] = score;
                    max_score = max_score.max(score);
                }

                // Softmax
                let mut exp_sum = 0.0f32;
                for j in 0..=i {
                    scores[j] = (scores[j] - max_score).exp();
                    exp_sum += scores[j];
                }
                for j in 0..=i {
                    scores[j] /= exp_sum;
                }

                // Weighted sum of values
                for d in 0..self.d_model {
                    let mut sum = 0.0f32;
                    for j in 0..=i {
                        sum += scores[j] * v_data[[b, j, d]];
                    }
                    output_data[[b, i, d]] = sum;
                }
            }
        }

        let attn_output = Variable::new(output_data, true);
        self.out_proj.forward(&attn_output)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.q_proj.parameters();
        params.extend(self.k_proj.parameters());
        params.extend(self.v_proj.parameters());
        params.extend(self.out_proj.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.q_proj.zero_grad();
        self.k_proj.zero_grad();
        self.v_proj.zero_grad();
        self.out_proj.zero_grad();
    }
}

/// Differentiable Transformer Block
#[derive(Clone)]
pub struct DifferentiableBlock {
    pub norm1: DifferentiableRMSNorm,
    pub attn: DifferentiableAttention,
    pub norm2: DifferentiableRMSNorm,
    pub mlp: DifferentiableMLP,
}

impl DifferentiableBlock {
    pub fn new(d_model: usize, n_heads: usize, d_ff: usize) -> Self {
        Self {
            norm1: DifferentiableRMSNorm::new(d_model, 1e-6),
            attn: DifferentiableAttention::new(d_model, n_heads),
            norm2: DifferentiableRMSNorm::new(d_model, 1e-6),
            mlp: DifferentiableMLP::new(d_model, d_ff),
        }
    }

    pub fn forward(&self, x: &Variable) -> Variable {
        // Pre-norm attention with residual
        let normed = self.norm1.forward(x);
        let attn_out = self.attn.forward(&normed);
        let x = x.add(&attn_out);

        // Pre-norm MLP with residual
        let normed = self.norm2.forward(&x);
        let mlp_out = self.mlp.forward(&normed);
        x.add(&mlp_out)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.norm1.parameters();
        params.extend(self.attn.parameters());
        params.extend(self.norm2.parameters());
        params.extend(self.mlp.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.norm1.zero_grad();
        self.attn.zero_grad();
        self.norm2.zero_grad();
        self.mlp.zero_grad();
    }
}

/// Differentiable Hybrid Block (Attention OR SSM)
///
/// Following Jamba's 1:7 attention:SSM ratio design.
#[derive(Clone)]
pub struct DifferentiableHybridBlock {
    /// Whether this block uses attention (true) or SSM (false)
    use_attention: bool,
    /// Pre-normalization
    pub norm1: DifferentiableRMSNorm,
    /// Attention layer (if use_attention)
    pub attn: Option<DifferentiableAttention>,
    /// SSM layer (if !use_attention)
    pub ssm: Option<DifferentiableSSM>,
    /// Post-layer normalization
    pub norm2: DifferentiableRMSNorm,
    /// MLP (SwiGLU)
    pub mlp: DifferentiableMLP,
}

impl DifferentiableHybridBlock {
    pub fn new(d_model: usize, n_heads: usize, d_ff: usize, d_state: usize, use_attention: bool) -> Self {
        let attn = if use_attention {
            Some(DifferentiableAttention::new(d_model, n_heads))
        } else {
            None
        };

        let ssm = if !use_attention {
            Some(DifferentiableSSM::new(d_model, d_state, 4, 2))
        } else {
            None
        };

        Self {
            use_attention,
            norm1: DifferentiableRMSNorm::new(d_model, 1e-6),
            attn,
            ssm,
            norm2: DifferentiableRMSNorm::new(d_model, 1e-6),
            mlp: DifferentiableMLP::new(d_model, d_ff),
        }
    }

    pub fn forward(&self, x: &Variable) -> Variable {
        // Pre-norm attention/SSM with residual
        let normed = self.norm1.forward(x);

        let hidden = if self.use_attention {
            self.attn.as_ref().unwrap().forward(&normed)
        } else {
            self.ssm.as_ref().unwrap().forward(&normed)
        };

        let x = x.add(&hidden);

        // Pre-norm MLP with residual
        let normed = self.norm2.forward(&x);
        let mlp_out = self.mlp.forward(&normed);
        x.add(&mlp_out)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.norm1.parameters();
        if let Some(ref attn) = self.attn {
            params.extend(attn.parameters());
        }
        if let Some(ref ssm) = self.ssm {
            params.extend(ssm.parameters());
        }
        params.extend(self.norm2.parameters());
        params.extend(self.mlp.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.norm1.zero_grad();
        if let Some(ref attn) = self.attn {
            attn.zero_grad();
        }
        if let Some(ref ssm) = self.ssm {
            ssm.zero_grad();
        }
        self.norm2.zero_grad();
        self.mlp.zero_grad();
    }
}

/// Full Hybrid Nexus LM with Attention/SSM and Memory
#[derive(Clone)]
pub struct DifferentiableHybridNexusLM {
    pub embed: Variable,
    pub blocks: Vec<DifferentiableHybridBlock>,
    pub memory: DifferentiableMemory,
    pub norm_f: DifferentiableRMSNorm,
    pub output: DifferentiableLinear,
    pub config: NexusConfig,
}

impl DifferentiableHybridNexusLM {
    pub fn new(config: NexusConfig) -> Self {
        let d_model = config.d_model;
        let vocab_size = config.vocab_size;
        let n_heads = config.n_heads;
        let d_ff = d_model * 4;
        let d_state = config.d_state;
        let n_layers = config.layers_per_block;
        let attention_ratio = config.attention_ratio;

        // Embedding matrix
        let std = (1.0 / d_model as f32).sqrt();
        let embed_data = Array3::from_shape_fn((1, vocab_size, d_model), |_| {
            use rand::Rng;
            rand::thread_rng().gen::<f32>() * std * 2.0 - std
        });
        let embed = Variable::parameter(embed_data);

        // Hybrid blocks with 1:7 attention:SSM ratio
        let blocks: Vec<_> = (0..n_layers)
            .map(|i| {
                // Use attention for first 1 out of every 8 layers
                let use_attention = i % (attention_ratio + 7) < attention_ratio;
                DifferentiableHybridBlock::new(d_model, n_heads, d_ff, d_state, use_attention)
            })
            .collect();

        // Memory module
        let memory = DifferentiableMemory::new(d_model, config.memory_size);

        // Final layer norm
        let norm_f = DifferentiableRMSNorm::new(d_model, 1e-6);

        // Output projection
        let output = DifferentiableLinear::new(d_model, vocab_size, false);

        Self { embed, blocks, memory, norm_f, output, config }
    }

    pub fn forward(&self, token_ids: &[u32]) -> Variable {
        let seq_len = token_ids.len();
        let d_model = self.config.d_model;
        let vocab_size = self.config.vocab_size;

        // Embed tokens
        let embed_data = self.embed.data();
        let mut hidden_data = Array3::zeros((1, seq_len, d_model));
        for (t, &tid) in token_ids.iter().enumerate() {
            let tid = (tid as usize).min(vocab_size - 1);
            for d in 0..d_model {
                hidden_data[[0, t, d]] = embed_data[[0, tid, d]];
            }
        }
        let mut hidden = Variable::new(hidden_data, true);

        // Forward through hybrid blocks
        for block in &self.blocks {
            hidden = block.forward(&hidden);
        }

        // Query memory and combine
        hidden = self.memory.forward(&hidden);

        // Final norm
        hidden = self.norm_f.forward(&hidden);

        // Output projection to logits
        self.output.forward(&hidden)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = vec![self.embed.clone()];
        for block in &self.blocks {
            params.extend(block.parameters());
        }
        params.extend(self.memory.parameters());
        params.extend(self.norm_f.parameters());
        params.extend(self.output.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.embed.zero_grad();
        for block in &self.blocks {
            block.zero_grad();
        }
        self.memory.zero_grad();
        self.norm_f.zero_grad();
        self.output.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        let d = self.config.d_model;
        let v = self.config.vocab_size;
        let n_layers = self.blocks.len();
        let d_ff = d * 4;
        let d_state = self.config.d_state;

        let embed = v * d;

        // Per layer (rough estimate for hybrid)
        let per_attn_layer = 4 * d * d + 2 * d + 3 * d * d_ff;  // attn + norms + mlp
        let per_ssm_layer = d * d * 4 + d * d_state + 3 * d * d_ff; // ssm + norms + mlp

        // Count attention vs SSM layers
        let n_attn = n_layers / 8 + 1;
        let n_ssm = n_layers - n_attn;

        let memory = self.config.memory_size * d * 2 + d * d * 4;
        let output = d * v;

        embed + n_attn * per_attn_layer + n_ssm * per_ssm_layer + memory + output
    }
}

/// Differentiable NexusLM
#[derive(Clone)]
pub struct DifferentiableNexusLM {
    pub embed: Variable,
    pub blocks: Vec<DifferentiableBlock>,
    pub norm_f: DifferentiableRMSNorm,
    pub output: DifferentiableLinear,
    pub config: NexusConfig,
}

impl DifferentiableNexusLM {
    pub fn new(config: NexusConfig) -> Self {
        let d_model = config.d_model;
        let vocab_size = config.vocab_size;
        let n_heads = config.n_heads;
        let d_ff = d_model * 4;
        let n_layers = config.layers_per_block;

        // Embedding matrix
        let std = (1.0 / d_model as f32).sqrt();
        let embed_data = Array3::from_shape_fn((1, vocab_size, d_model), |_| {
            use rand::Rng;
            rand::thread_rng().gen::<f32>() * std * 2.0 - std
        });
        let embed = Variable::parameter(embed_data);

        // Transformer blocks
        let blocks: Vec<_> = (0..n_layers)
            .map(|_| DifferentiableBlock::new(d_model, n_heads, d_ff))
            .collect();

        // Final layer norm
        let norm_f = DifferentiableRMSNorm::new(d_model, 1e-6);

        // Output projection (could tie weights with embed)
        let output = DifferentiableLinear::new(d_model, vocab_size, false);

        Self { embed, blocks, norm_f, output, config }
    }

    pub fn forward(&self, token_ids: &[u32]) -> Variable {
        let seq_len = token_ids.len();
        let d_model = self.config.d_model;
        let vocab_size = self.config.vocab_size;

        // Embed tokens
        let embed_data = self.embed.data();
        let mut hidden_data = Array3::zeros((1, seq_len, d_model));
        for (t, &tid) in token_ids.iter().enumerate() {
            let tid = (tid as usize).min(vocab_size - 1);
            for d in 0..d_model {
                hidden_data[[0, t, d]] = embed_data[[0, tid, d]];
            }
        }
        let mut hidden = Variable::new(hidden_data, true);

        // Forward through transformer blocks
        for block in &self.blocks {
            hidden = block.forward(&hidden);
        }

        // Final norm
        hidden = self.norm_f.forward(&hidden);

        // Output projection to logits
        self.output.forward(&hidden)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = vec![self.embed.clone()];
        for block in &self.blocks {
            params.extend(block.parameters());
        }
        params.extend(self.norm_f.parameters());
        params.extend(self.output.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.embed.zero_grad();
        for block in &self.blocks {
            block.zero_grad();
        }
        self.norm_f.zero_grad();
        self.output.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        let d = self.config.d_model;
        let v = self.config.vocab_size;
        let n_layers = self.blocks.len();
        let d_ff = d * 4;

        let embed = v * d;
        let per_layer = 4 * d * d + 2 * d + 3 * d * d_ff + d * d_ff;  // attn + norm + mlp
        let output = d * v;

        embed + n_layers * per_layer + output
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_differentiable_mlp() {
        let mlp = DifferentiableMLP::new(64, 256);
        let x = Variable::parameter(Array3::ones((1, 4, 64)));
        let y = mlp.forward(&x);
        assert_eq!(y.shape(), (1, 4, 64));
    }

    #[test]
    fn test_differentiable_block() {
        let block = DifferentiableBlock::new(64, 4, 256);
        let x = Variable::parameter(Array3::ones((1, 4, 64)));
        let y = block.forward(&x);
        assert_eq!(y.shape(), (1, 4, 64));
    }

    #[test]
    fn test_differentiable_nexus() {
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            vocab_size: 256,
            layers_per_block: 2,
            ..Default::default()
        };
        let model = DifferentiableNexusLM::new(config);
        let tokens: Vec<u32> = vec![1, 2, 3, 4];
        let logits = model.forward(&tokens);
        assert_eq!(logits.shape(), (1, 4, 256));
    }

    #[test]
    fn test_differentiable_hybrid_block_attention() {
        let block = DifferentiableHybridBlock::new(64, 4, 256, 16, true);
        let x = Variable::parameter(Array3::ones((1, 4, 64)));
        let y = block.forward(&x);
        assert_eq!(y.shape(), (1, 4, 64));
        assert!(block.attn.is_some());
        assert!(block.ssm.is_none());
    }

    #[test]
    fn test_differentiable_hybrid_block_ssm() {
        let block = DifferentiableHybridBlock::new(64, 4, 256, 16, false);
        let x = Variable::parameter(Array3::ones((1, 4, 64)));
        let y = block.forward(&x);
        assert_eq!(y.shape(), (1, 4, 64));
        assert!(block.attn.is_none());
        assert!(block.ssm.is_some());
    }

    #[test]
    fn test_differentiable_hybrid_nexus() {
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            d_state: 16,
            vocab_size: 256,
            layers_per_block: 8,
            attention_ratio: 1,
            memory_size: 32,
            ..Default::default()
        };
        let model = DifferentiableHybridNexusLM::new(config);
        let tokens: Vec<u32> = vec![1, 2, 3, 4];
        let logits = model.forward(&tokens);
        assert_eq!(logits.shape(), (1, 4, 256));
        println!("Hybrid model has {} parameters", model.num_parameters());
    }

    #[test]
    fn test_hybrid_layer_ratio() {
        // Test 1:7 attention:SSM ratio
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            d_state: 16,
            vocab_size: 256,
            layers_per_block: 8,
            attention_ratio: 1,
            memory_size: 32,
            ..Default::default()
        };
        let model = DifferentiableHybridNexusLM::new(config);

        let n_attn = model.blocks.iter().filter(|b| b.attn.is_some()).count();
        let n_ssm = model.blocks.iter().filter(|b| b.ssm.is_some()).count();

        assert_eq!(n_attn, 1, "Expected 1 attention layer");
        assert_eq!(n_ssm, 7, "Expected 7 SSM layers");
    }
}
