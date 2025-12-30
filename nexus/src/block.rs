//! Hybrid Block: Combines Attention and SSM layers
//!
//! Following Jamba's design: 1:7 ratio of attention to SSM layers.
//! Each block includes RMSNorm for stability.

use ndarray::Array1;
use serde::{Serialize, Deserialize};
use crate::tensor::Tensor;
use crate::attention::MultiHeadAttention;
use crate::ssm::SelectiveSSM;
use crate::NexusConfig;

/// RMS Normalization layer
#[derive(Clone, Serialize, Deserialize)]
pub struct RMSNorm {
    weight: Array1<f32>,
    eps: f32,
}

impl RMSNorm {
    pub fn new(d_model: usize, eps: f32) -> Self {
        Self {
            weight: Array1::ones(d_model),
            eps,
        }
    }

    pub fn forward(&self, x: &Tensor) -> Tensor {
        x.rms_norm(&self.weight, self.eps)
    }
}

/// MLP (Feed-Forward Network)
#[derive(Clone, Serialize, Deserialize)]
pub struct MLP {
    up_proj: crate::tensor::Linear,
    down_proj: crate::tensor::Linear,
    gate_proj: crate::tensor::Linear,
}

impl MLP {
    pub fn new(d_model: usize, d_ff: usize) -> Self {
        Self {
            up_proj: crate::tensor::Linear::new(d_model, d_ff, false),
            gate_proj: crate::tensor::Linear::new(d_model, d_ff, false),
            down_proj: crate::tensor::Linear::new(d_ff, d_model, false),
        }
    }

    /// SwiGLU activation: down(up(x) * silu(gate(x)))
    pub fn forward(&self, x: &Tensor) -> Tensor {
        let up = self.up_proj.forward(x);
        let gate = self.gate_proj.forward(x).silu();
        let hidden = up.mul(&gate);
        self.down_proj.forward(&hidden)
    }
}

/// A single hybrid block (either attention or SSM based)
#[derive(Clone, Serialize, Deserialize)]
pub struct HybridBlock {
    /// Whether this block uses attention (true) or SSM (false)
    use_attention: bool,
    /// Pre-normalization
    norm1: RMSNorm,
    /// Attention or SSM layer
    attention: Option<MultiHeadAttention>,
    ssm: Option<SelectiveSSM>,
    /// Post-attention/SSM normalization
    norm2: RMSNorm,
    /// MLP
    mlp: MLP,
}

impl HybridBlock {
    pub fn new(config: &NexusConfig, use_attention: bool) -> Self {
        let d_ff = config.d_model * 4; // Standard 4x expansion

        let attention = if use_attention {
            Some(MultiHeadAttention::new(
                config.d_model,
                config.n_heads,
                config.max_seq_len,
            ))
        } else {
            None
        };

        let ssm = if !use_attention {
            Some(SelectiveSSM::new(
                config.d_model,
                config.d_state,
                config.d_conv,
                config.expand,
            ))
        } else {
            None
        };

        Self {
            use_attention,
            norm1: RMSNorm::new(config.d_model, 1e-6),
            attention,
            ssm,
            norm2: RMSNorm::new(config.d_model, 1e-6),
            mlp: MLP::new(config.d_model, d_ff),
        }
    }

    pub fn forward(&self, x: &Tensor) -> Tensor {
        // Pre-norm
        let normed = self.norm1.forward(x);

        // Attention or SSM
        let hidden = if self.use_attention {
            self.attention.as_ref().unwrap().forward(&normed, true)
        } else {
            self.ssm.as_ref().unwrap().forward(&normed)
        };

        // Residual connection
        let x = x.add(&hidden);

        // MLP with pre-norm and residual
        let normed = self.norm2.forward(&x);
        let mlp_out = self.mlp.forward(&normed);

        x.add(&mlp_out)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_attention_block() {
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            d_state: 16,
            d_conv: 4,
            expand: 2,
            max_seq_len: 512,
            ..Default::default()
        };

        let block = HybridBlock::new(&config, true);
        let x = Tensor::randn(2, 8, 64);
        let y = block.forward(&x);
        assert_eq!(y.shape(), (2, 8, 64));
    }

    #[test]
    fn test_ssm_block() {
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            d_state: 16,
            d_conv: 4,
            expand: 2,
            max_seq_len: 512,
            ..Default::default()
        };

        let block = HybridBlock::new(&config, false);
        let x = Tensor::randn(2, 8, 64);
        let y = block.forward(&x);
        assert_eq!(y.shape(), (2, 8, 64));
    }

    #[test]
    fn test_mlp() {
        let mlp = MLP::new(64, 256);
        let x = Tensor::randn(2, 8, 64);
        let y = mlp.forward(&x);
        assert_eq!(y.shape(), (2, 8, 64));
    }
}
