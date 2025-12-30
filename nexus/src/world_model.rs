//! JEPA-style World Model
//!
//! Key insight: Predict in latent space, not token space.
//! More efficient and handles ambiguity better than generative models.

use crate::tensor::{Tensor, Linear};

/// JEPA-style predictor
///
/// Given an encoded representation z and context, predicts the
/// representation z' of what comes next in latent space.
pub struct WorldModelPredictor {
    /// Model dimension
    _d_model: usize,
    /// Predictor hidden dimension
    _d_hidden: usize,
    /// Input projection
    in_proj: Linear,
    /// Context projection
    ctx_proj: Linear,
    /// Hidden layers
    hidden1: Linear,
    hidden2: Linear,
    /// Output projection
    out_proj: Linear,
}

impl WorldModelPredictor {
    pub fn new(d_model: usize, d_hidden: usize) -> Self {
        Self {
            _d_model: d_model,
            _d_hidden: d_hidden,
            in_proj: Linear::new(d_model, d_hidden, false),
            ctx_proj: Linear::new(d_model, d_hidden, false),
            hidden1: Linear::new(d_hidden, d_hidden, false),
            hidden2: Linear::new(d_hidden, d_hidden, false),
            out_proj: Linear::new(d_hidden, d_model, false),
        }
    }

    /// Predict next latent state
    ///
    /// z: current latent representation [batch, d_model]
    /// context: contextual information [batch, d_model]
    /// Returns: predicted next latent [batch, d_model]
    pub fn predict(&self, z: &Tensor, context: &Tensor) -> Tensor {
        // Project inputs
        let z_proj = self.in_proj.forward(z);
        let ctx_proj = self.ctx_proj.forward(context);

        // Combine with addition (could also concatenate)
        let combined = z_proj.add(&ctx_proj);

        // Two hidden layers with GELU
        let h1 = self.hidden1.forward(&combined).gelu();
        let h2 = self.hidden2.forward(&h1).gelu();

        // Project to output space
        self.out_proj.forward(&h2)
    }
}

/// Encoder for JEPA
///
/// Maps input to latent representation.
/// In full JEPA, this would be a ViT or similar.
/// Here we use a simple MLP for prototyping.
pub struct WorldModelEncoder {
    layers: Vec<Linear>,
    _d_model: usize,
}

impl WorldModelEncoder {
    pub fn new(d_input: usize, d_model: usize, n_layers: usize) -> Self {
        let mut layers = Vec::with_capacity(n_layers);

        // First layer
        layers.push(Linear::new(d_input, d_model, true));

        // Hidden layers
        for _ in 1..n_layers {
            layers.push(Linear::new(d_model, d_model, true));
        }

        Self { layers, _d_model: d_model }
    }

    pub fn encode(&self, x: &Tensor) -> Tensor {
        let mut h = x.clone();

        for (i, layer) in self.layers.iter().enumerate() {
            h = layer.forward(&h);
            if i < self.layers.len() - 1 {
                h = h.gelu();
            }
        }

        h
    }
}

/// Complete World Model combining encoder and predictor
pub struct WorldModel {
    /// Encoder: input -> latent
    pub encoder: WorldModelEncoder,
    /// Predictor: (latent, context) -> predicted_latent
    pub predictor: WorldModelPredictor,
    /// Target encoder (for JEPA, this is EMA of encoder)
    /// In this prototype, we share weights
    _d_model: usize,
}

impl WorldModel {
    pub fn new(d_input: usize, d_model: usize, d_hidden: usize, n_encoder_layers: usize) -> Self {
        Self {
            encoder: WorldModelEncoder::new(d_input, d_model, n_encoder_layers),
            predictor: WorldModelPredictor::new(d_model, d_hidden),
            _d_model: d_model,
        }
    }

    /// Encode input to latent space
    pub fn encode(&self, x: &Tensor) -> Tensor {
        self.encoder.encode(x)
    }

    /// Predict next latent given current latent and context
    pub fn predict(&self, z: &Tensor, context: &Tensor) -> Tensor {
        self.predictor.predict(z, context)
    }

    /// Compute JEPA loss: ||predictor(z_t, ctx) - encode(x_{t+1})||^2
    ///
    /// In real JEPA, the target encoder is a separate EMA model.
    /// Here we use the same encoder for simplicity.
    pub fn compute_loss(&self, x_t: &Tensor, x_next: &Tensor, context: &Tensor) -> f32 {
        // Encode current state
        let z_t = self.encode(x_t);

        // Predict next state
        let z_pred = self.predict(&z_t, context);

        // Encode actual next state (target)
        let z_target = self.encode(x_next);

        // L2 loss in latent space
        let diff = z_pred.add(&z_target.scale(-1.0));
        let (batch, seq_len, d_model) = diff.shape();

        let mut loss = 0.0f32;
        for b in 0..batch {
            for s in 0..seq_len {
                for d in 0..d_model {
                    loss += diff.data[[b, s, d]].powi(2);
                }
            }
        }

        loss / (batch * seq_len * d_model) as f32
    }
}

/// Masking strategy for JEPA training
pub enum MaskStrategy {
    /// Random masking (like MAE)
    Random { mask_ratio: f32 },
    /// Block masking (like BEiT)
    Block { block_size: usize, num_blocks: usize },
    /// Causal masking (predict future)
    Causal,
}

impl MaskStrategy {
    /// Generate mask indices
    pub fn generate_mask(&self, seq_len: usize) -> Vec<bool> {
        match self {
            MaskStrategy::Random { mask_ratio } => {
                (0..seq_len)
                    .map(|_| rand::random::<f32>() < *mask_ratio)
                    .collect()
            }
            MaskStrategy::Block { block_size, num_blocks } => {
                let mut mask = vec![false; seq_len];
                for _ in 0..*num_blocks {
                    let start = (rand::random::<f32>() * (seq_len - block_size) as f32) as usize;
                    for i in start..start + block_size {
                        if i < seq_len {
                            mask[i] = true;
                        }
                    }
                }
                mask
            }
            MaskStrategy::Causal => {
                // Mask second half (predict future from past)
                (0..seq_len).map(|i| i >= seq_len / 2).collect()
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_predictor() {
        let pred = WorldModelPredictor::new(64, 128);
        let z = Tensor::randn(2, 1, 64);
        let ctx = Tensor::randn(2, 1, 64);
        let out = pred.predict(&z, &ctx);
        assert_eq!(out.shape(), (2, 1, 64));
    }

    #[test]
    fn test_encoder() {
        let enc = WorldModelEncoder::new(64, 64, 3);
        let x = Tensor::randn(2, 8, 64);
        let z = enc.encode(&x);
        assert_eq!(z.shape(), (2, 8, 64));
    }

    #[test]
    fn test_world_model_loss() {
        let wm = WorldModel::new(64, 64, 128, 2);
        let x_t = Tensor::randn(2, 4, 64);
        let x_next = Tensor::randn(2, 4, 64);
        let ctx = Tensor::randn(2, 4, 64);

        let loss = wm.compute_loss(&x_t, &x_next, &ctx);
        assert!(loss > 0.0);
    }

    #[test]
    fn test_mask_strategies() {
        let random_mask = MaskStrategy::Random { mask_ratio: 0.5 };
        let mask = random_mask.generate_mask(100);
        assert_eq!(mask.len(), 100);

        let block_mask = MaskStrategy::Block { block_size: 10, num_blocks: 3 };
        let mask = block_mask.generate_mask(100);
        assert_eq!(mask.len(), 100);

        let causal_mask = MaskStrategy::Causal;
        let mask = causal_mask.generate_mask(100);
        assert!(mask[50]); // Second half should be masked
        assert!(!mask[0]); // First half should not be masked
    }
}
