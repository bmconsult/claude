//! GPU-Accelerated Backend using Candle
//!
//! Provides GPU-accelerated implementations of Nexus components using
//! Hugging Face's Candle framework.
//!
//! Features:
//! - CUDA support (via `--features cuda`)
//! - Metal support for Apple Silicon (via `--features metal`)
//! - CPU fallback when GPU unavailable

use candle_core::{DType, Device, Result, Tensor};
use candle_nn::{linear, Linear, Module, VarBuilder, VarMap};

/// Get the best available device
pub fn get_device() -> Result<Device> {
    #[cfg(feature = "cuda")]
    {
        if let Ok(device) = Device::cuda(0) {
            println!("Using CUDA device");
            return Ok(device);
        }
    }

    #[cfg(feature = "metal")]
    {
        if let Ok(device) = Device::new_metal(0) {
            println!("Using Metal device");
            return Ok(device);
        }
    }

    println!("Using CPU device");
    Ok(Device::Cpu)
}

/// RMS Normalization layer
pub struct RMSNorm {
    weight: Tensor,
    eps: f64,
}

impl RMSNorm {
    pub fn new(dim: usize, eps: f64, vb: VarBuilder) -> Result<Self> {
        let weight = vb.get_with_hints(dim, "weight", candle_nn::Init::Const(1.0))?;
        Ok(Self { weight, eps })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let x = x.to_dtype(DType::F32)?;
        // Normalize over last dimension
        let last_dim = x.dims().len() - 1;
        let mean_sq = x.sqr()?.mean_keepdim(last_dim)?;
        let eps_tensor = Tensor::new(&[self.eps as f32], x.device())?;
        let rms = mean_sq.broadcast_add(&eps_tensor)?.sqrt()?;
        let normed = x.broadcast_div(&rms)?;
        normed.broadcast_mul(&self.weight)
    }
}

/// SwiGLU MLP
pub struct MLP {
    gate_proj: Linear,
    up_proj: Linear,
    down_proj: Linear,
}

impl MLP {
    pub fn new(d_model: usize, d_ff: usize, vb: VarBuilder) -> Result<Self> {
        let gate_proj = linear(d_model, d_ff, vb.pp("gate_proj"))?;
        let up_proj = linear(d_model, d_ff, vb.pp("up_proj"))?;
        let down_proj = linear(d_ff, d_model, vb.pp("down_proj"))?;
        Ok(Self {
            gate_proj,
            up_proj,
            down_proj,
        })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let gate = self.gate_proj.forward(x)?;
        let gate = candle_nn::ops::silu(&gate)?;
        let up = self.up_proj.forward(x)?;
        let hidden = gate.mul(&up)?;
        self.down_proj.forward(&hidden)
    }
}

/// Causal Self-Attention for GPU
pub struct CausalAttention {
    q_proj: Linear,
    k_proj: Linear,
    v_proj: Linear,
    out_proj: Linear,
    n_heads: usize,
    head_dim: usize,
}

impl CausalAttention {
    pub fn new(d_model: usize, n_heads: usize, vb: VarBuilder) -> Result<Self> {
        let head_dim = d_model / n_heads;
        let q_proj = linear(d_model, d_model, vb.pp("q_proj"))?;
        let k_proj = linear(d_model, d_model, vb.pp("k_proj"))?;
        let v_proj = linear(d_model, d_model, vb.pp("v_proj"))?;
        let out_proj = linear(d_model, d_model, vb.pp("out_proj"))?;
        Ok(Self {
            q_proj,
            k_proj,
            v_proj,
            out_proj,
            n_heads,
            head_dim,
        })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let (b, seq_len, d) = x.dims3()?;

        // Project to Q, K, V
        let q = self.q_proj.forward(x)?;
        let k = self.k_proj.forward(x)?;
        let v = self.v_proj.forward(x)?;

        // Reshape for multi-head attention
        let q = q.reshape((b, seq_len, self.n_heads, self.head_dim))?;
        let k = k.reshape((b, seq_len, self.n_heads, self.head_dim))?;
        let v = v.reshape((b, seq_len, self.n_heads, self.head_dim))?;

        // Transpose to (batch, heads, seq, dim)
        let q = q.transpose(1, 2)?;
        let k = k.transpose(1, 2)?;
        let v = v.transpose(1, 2)?;

        // Scaled dot-product attention
        let scale = (self.head_dim as f64).sqrt() as f32;
        let scores = q.matmul(&k.transpose(2, 3)?)?;
        let scale_tensor = Tensor::new(&[scale], x.device())?;
        let scores = scores.broadcast_div(&scale_tensor)?;

        // Causal mask - apply via large negative value for masked positions
        // Create lower triangular mask (1 for valid, 0 for masked)
        let mask = Tensor::tril2(seq_len, DType::F32, x.device())?;
        let mask = mask.unsqueeze(0)?.unsqueeze(0)?
            .broadcast_as((b, self.n_heads, seq_len, seq_len))?;
        // Convert to additive mask: 0 for valid, -inf for masked
        let ones = Tensor::ones((b, self.n_heads, seq_len, seq_len), DType::F32, x.device())?;
        let inv_mask = ones.sub(&mask)?;
        let neg_inf = Tensor::new(&[-1e9f32], x.device())?
            .broadcast_as((b, self.n_heads, seq_len, seq_len))?;
        let mask_add = inv_mask.mul(&neg_inf)?;
        let scores = scores.add(&mask_add)?;

        // Softmax
        let attn = candle_nn::ops::softmax(&scores, 3)?;

        // Apply to values
        let out = attn.matmul(&v)?;

        // Reshape back
        let out = out.transpose(1, 2)?;
        let out = out.reshape((b, seq_len, d))?;

        self.out_proj.forward(&out)
    }
}

/// Selective State Space Model (Mamba) for GPU
pub struct SelectiveSSM {
    in_proj: Linear,
    out_proj: Linear,
    x_proj: Linear,
    dt_proj: Linear,
    a_log: Tensor,
    d_param: Tensor,
    d_inner: usize,
    d_state: usize,
}

impl SelectiveSSM {
    pub fn new(
        d_model: usize,
        d_state: usize,
        d_conv: usize,
        expand: usize,
        vb: VarBuilder,
    ) -> Result<Self> {
        let d_inner = d_model * expand;

        let in_proj = linear(d_model, d_inner * 2, vb.pp("in_proj"))?;
        let out_proj = linear(d_inner, d_model, vb.pp("out_proj"))?;
        let x_proj = linear(d_inner, d_state * 2, vb.pp("x_proj"))?;
        let dt_proj = linear(d_state, d_inner, vb.pp("dt_proj"))?;

        // A matrix (negative log for stability)
        let a_log = vb.get_with_hints(
            (d_inner, d_state),
            "a_log",
            candle_nn::Init::Const(-1.0),
        )?;

        // D parameter (skip connection)
        let d_param = vb.get_with_hints(d_inner, "d_param", candle_nn::Init::Const(1.0))?;

        Ok(Self {
            in_proj,
            out_proj,
            x_proj,
            dt_proj,
            a_log,
            d_param,
            d_inner,
            d_state,
        })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let (b, seq_len, _) = x.dims3()?;

        // Project input
        let xz = self.in_proj.forward(x)?;
        let chunks: Vec<Tensor> = xz.chunk(2, 2)?;
        let x_proj = &chunks[0];
        let z = &chunks[1];

        // Selective scan parameters
        let x_dbl = self.x_proj.forward(x_proj)?;
        let delta_b: Vec<Tensor> = x_dbl.chunk(2, 2)?;
        // Softplus: log(1 + exp(x))
        let dt_out = self.dt_proj.forward(&delta_b[0])?;
        let delta = dt_out.exp()?.broadcast_add(&Tensor::ones_like(&dt_out)?)?.log()?;
        let _b = &delta_b[1];

        // A = -exp(a_log)
        let a = self.a_log.exp()?.neg()?;

        // Simplified selective scan (parallel-friendly approximation)
        // In production, use proper scan kernel
        let device = x.device();
        let mut h = Tensor::zeros((b, self.d_inner, self.d_state), DType::F32, device)?;
        let mut outputs = Vec::with_capacity(seq_len);

        for t in 0..seq_len {
            let x_t = x_proj.narrow(1, t, 1)?.squeeze(1)?;
            let delta_t = delta.narrow(1, t, 1)?.squeeze(1)?;

            // State update: h = h * exp(A * delta) + x * delta
            let delta_expanded = delta_t.unsqueeze(2)?.broadcast_as(h.shape())?;
            let decay = a.broadcast_mul(&delta_expanded)?.exp()?;
            // Expand x and delta for state dimension
            let x_expanded = x_t.unsqueeze(2)?.broadcast_as(h.shape())?;
            let delta_for_update = delta_t.unsqueeze(2)?.broadcast_as(h.shape())?;
            let update = x_expanded.mul(&delta_for_update)?;
            h = h.mul(&decay)?.add(&update)?;

            // Output
            let y_t = h.sum(2)?;
            outputs.push(y_t);
        }

        let y = Tensor::stack(&outputs, 1)?;

        // Skip connection and gate
        let skip = x_proj.broadcast_mul(&self.d_param)?;
        let y = y.add(&skip)?;
        let z_act = candle_nn::ops::silu(z)?;
        let y = y.mul(&z_act)?;

        self.out_proj.forward(&y)
    }
}

/// Differentiable Memory for GPU
pub struct Memory {
    key_proj: Linear,
    value_proj: Linear,
    query_proj: Linear,
    out_proj: Linear,
    memory_keys: Tensor,
    memory_values: Tensor,
    n_slots: usize,
}

impl Memory {
    pub fn new(d_model: usize, n_slots: usize, vb: VarBuilder) -> Result<Self> {
        let key_proj = linear(d_model, d_model, vb.pp("key_proj"))?;
        let value_proj = linear(d_model, d_model, vb.pp("value_proj"))?;
        let query_proj = linear(d_model, d_model, vb.pp("query_proj"))?;
        let out_proj = linear(d_model, d_model, vb.pp("out_proj"))?;

        // Learnable memory
        let std = (1.0 / d_model as f64).sqrt() as f32;
        let memory_keys = vb.get_with_hints(
            (n_slots, d_model),
            "memory_keys",
            candle_nn::Init::Randn { mean: 0.0, stdev: std.into() },
        )?;
        let memory_values = vb.get_with_hints(
            (n_slots, d_model),
            "memory_values",
            candle_nn::Init::Randn { mean: 0.0, stdev: std.into() },
        )?;

        Ok(Self {
            key_proj,
            value_proj,
            query_proj,
            out_proj,
            memory_keys,
            memory_values,
            n_slots,
        })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        let (b, _seq_len, d) = x.dims3()?;

        // Project query
        let q = self.query_proj.forward(x)?;

        // Expand memory for batch
        let keys = self.memory_keys.unsqueeze(0)?.broadcast_as((b, self.n_slots, d))?;
        let values = self.memory_values.unsqueeze(0)?.broadcast_as((b, self.n_slots, d))?;

        // Attention over memory
        let scale = (d as f64).sqrt() as f32;
        let scale_tensor = Tensor::new(&[scale], x.device())?;
        let scores = q.matmul(&keys.transpose(1, 2)?)?;
        let scores = scores.broadcast_div(&scale_tensor)?;
        let attn = candle_nn::ops::softmax(&scores, 2)?;

        // Weighted sum
        let context = attn.matmul(&values)?;

        // Project and residual
        let out = self.out_proj.forward(&context)?;
        x.add(&out)
    }
}

/// GPU-Accelerated Hybrid Block
pub struct HybridBlock {
    norm1: RMSNorm,
    attn: Option<CausalAttention>,
    ssm: Option<SelectiveSSM>,
    norm2: RMSNorm,
    mlp: MLP,
    use_attention: bool,
}

impl HybridBlock {
    pub fn new(
        d_model: usize,
        n_heads: usize,
        d_ff: usize,
        d_state: usize,
        use_attention: bool,
        vb: VarBuilder,
    ) -> Result<Self> {
        let norm1 = RMSNorm::new(d_model, 1e-6, vb.pp("norm1"))?;
        let norm2 = RMSNorm::new(d_model, 1e-6, vb.pp("norm2"))?;
        let mlp = MLP::new(d_model, d_ff, vb.pp("mlp"))?;

        let (attn, ssm) = if use_attention {
            (Some(CausalAttention::new(d_model, n_heads, vb.pp("attn"))?), None)
        } else {
            (None, Some(SelectiveSSM::new(d_model, d_state, 4, 2, vb.pp("ssm"))?))
        };

        Ok(Self {
            norm1,
            attn,
            ssm,
            norm2,
            mlp,
            use_attention,
        })
    }

    pub fn forward(&self, x: &Tensor) -> Result<Tensor> {
        // Pre-norm + attention/SSM + residual
        let normed = self.norm1.forward(x)?;
        let hidden = if self.use_attention {
            self.attn.as_ref().unwrap().forward(&normed)?
        } else {
            self.ssm.as_ref().unwrap().forward(&normed)?
        };
        let x = x.add(&hidden)?;

        // Pre-norm + MLP + residual
        let normed = self.norm2.forward(&x)?;
        let mlp_out = self.mlp.forward(&normed)?;
        x.add(&mlp_out)
    }
}

/// GPU-Accelerated Hybrid Nexus LM
pub struct HybridNexusLM {
    embed: Tensor,
    blocks: Vec<HybridBlock>,
    memory: Memory,
    norm_f: RMSNorm,
    output: Linear,
    d_model: usize,
    vocab_size: usize,
}

impl HybridNexusLM {
    pub fn new(
        d_model: usize,
        n_heads: usize,
        d_state: usize,
        vocab_size: usize,
        n_layers: usize,
        memory_slots: usize,
        attention_ratio: usize,
        vb: VarBuilder,
    ) -> Result<Self> {
        let d_ff = d_model * 4;

        // Embedding
        let std = (1.0 / d_model as f64).sqrt() as f32;
        let embed = vb.get_with_hints(
            (vocab_size, d_model),
            "embed",
            candle_nn::Init::Randn { mean: 0.0, stdev: std.into() },
        )?;

        // Hybrid blocks with 1:7 ratio
        let mut blocks = Vec::with_capacity(n_layers);
        for i in 0..n_layers {
            let use_attention = i % (attention_ratio + 7) < attention_ratio;
            let block = HybridBlock::new(
                d_model,
                n_heads,
                d_ff,
                d_state,
                use_attention,
                vb.pp(format!("block.{}", i)),
            )?;
            blocks.push(block);
        }

        // Memory
        let memory = Memory::new(d_model, memory_slots, vb.pp("memory"))?;

        // Final norm and output
        let norm_f = RMSNorm::new(d_model, 1e-6, vb.pp("norm_f"))?;
        let output = linear(d_model, vocab_size, vb.pp("output"))?;

        Ok(Self {
            embed,
            blocks,
            memory,
            norm_f,
            output,
            d_model,
            vocab_size,
        })
    }

    pub fn forward(&self, token_ids: &Tensor) -> Result<Tensor> {
        // Embed - add batch dimension
        let x = self.embed.index_select(token_ids, 0)?;
        let x = x.unsqueeze(0)?; // [seq, dim] -> [1, seq, dim]

        // Through blocks
        let mut hidden = x;
        for block in &self.blocks {
            hidden = block.forward(&hidden)?;
        }

        // Memory
        hidden = self.memory.forward(&hidden)?;

        // Output
        let hidden = self.norm_f.forward(&hidden)?;
        let output = self.output.forward(&hidden)?;

        // Remove batch dimension for output
        output.squeeze(0)
    }

    /// Load model parameters from checkpoint
    pub fn from_varmap(
        d_model: usize,
        n_heads: usize,
        d_state: usize,
        vocab_size: usize,
        n_layers: usize,
        memory_slots: usize,
        attention_ratio: usize,
        varmap: &VarMap,
        device: &Device,
    ) -> Result<Self> {
        let vb = VarBuilder::from_varmap(varmap, DType::F32, device);
        Self::new(
            d_model,
            n_heads,
            d_state,
            vocab_size,
            n_layers,
            memory_slots,
            attention_ratio,
            vb,
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_device() {
        let device = get_device().unwrap();
        // Should always succeed with CPU fallback
        assert!(matches!(device, Device::Cpu | Device::Cuda(_)));
    }

    #[test]
    fn test_rms_norm() -> Result<()> {
        let device = Device::Cpu;
        let varmap = VarMap::new();
        let vb = VarBuilder::from_varmap(&varmap, DType::F32, &device);

        let norm = RMSNorm::new(64, 1e-6, vb)?;
        let x = Tensor::randn(0.0f32, 1.0, (1, 4, 64), &device)?;
        let y = norm.forward(&x)?;
        assert_eq!(y.dims(), &[1, 4, 64]);
        Ok(())
    }

    #[test]
    fn test_mlp() -> Result<()> {
        let device = Device::Cpu;
        let varmap = VarMap::new();
        let vb = VarBuilder::from_varmap(&varmap, DType::F32, &device);

        let mlp = MLP::new(64, 256, vb)?;
        let x = Tensor::randn(0.0f32, 1.0, (1, 4, 64), &device)?;
        let y = mlp.forward(&x)?;
        assert_eq!(y.dims(), &[1, 4, 64]);
        Ok(())
    }

    #[test]
    fn test_attention() -> Result<()> {
        let device = Device::Cpu;
        let varmap = VarMap::new();
        let vb = VarBuilder::from_varmap(&varmap, DType::F32, &device);

        let attn = CausalAttention::new(64, 4, vb)?;
        let x = Tensor::randn(0.0f32, 1.0, (1, 4, 64), &device)?;
        let y = attn.forward(&x)?;
        assert_eq!(y.dims(), &[1, 4, 64]);
        Ok(())
    }

    #[test]
    fn test_hybrid_nexus() -> Result<()> {
        let device = Device::Cpu;
        let varmap = VarMap::new();
        let vb = VarBuilder::from_varmap(&varmap, DType::F32, &device);

        let model = HybridNexusLM::new(
            64,    // d_model
            4,     // n_heads
            16,    // d_state
            256,   // vocab_size
            8,     // n_layers
            32,    // memory_slots
            1,     // attention_ratio
            vb,
        )?;

        let tokens = Tensor::new(&[1u32, 2, 3, 4], &device)?;
        let logits = model.forward(&tokens)?;
        assert_eq!(logits.dims(), &[4, 256]);
        Ok(())
    }
}
