//! Differentiable JEPA-style World Model
//!
//! Key insight: Predict in latent space, not token space.
//! Uses autograd Variable for end-to-end training.

use ndarray::Array3;
use crate::autograd::{Variable, DifferentiableLinear};

/// Differentiable JEPA-style predictor
///
/// Given an encoded representation z and context, predicts the
/// representation z' of what comes next in latent space.
#[derive(Clone)]
pub struct DifferentiableWorldModelPredictor {
    d_model: usize,
    d_hidden: usize,
    /// Input projection
    in_proj: DifferentiableLinear,
    /// Context projection
    ctx_proj: DifferentiableLinear,
    /// Hidden layers
    hidden1: DifferentiableLinear,
    hidden2: DifferentiableLinear,
    /// Output projection
    out_proj: DifferentiableLinear,
}

impl DifferentiableWorldModelPredictor {
    pub fn new(d_model: usize, d_hidden: usize) -> Self {
        Self {
            d_model,
            d_hidden,
            in_proj: DifferentiableLinear::new(d_model, d_hidden, false),
            ctx_proj: DifferentiableLinear::new(d_model, d_hidden, false),
            hidden1: DifferentiableLinear::new(d_hidden, d_hidden, false),
            hidden2: DifferentiableLinear::new(d_hidden, d_hidden, false),
            out_proj: DifferentiableLinear::new(d_hidden, d_model, false),
        }
    }

    /// Predict next latent state
    ///
    /// z: current latent representation [batch, seq, d_model]
    /// context: contextual information [batch, seq, d_model]
    /// Returns: predicted next latent [batch, seq, d_model]
    pub fn predict(&self, z: &Variable, context: &Variable) -> Variable {
        // Project inputs
        let z_proj = self.in_proj.forward(z);
        let ctx_proj = self.ctx_proj.forward(context);

        // Combine with addition
        let combined = z_proj.add(&ctx_proj);

        // Two hidden layers with GELU
        let h1 = self.hidden1.forward(&combined).gelu();
        let h2 = self.hidden2.forward(&h1).gelu();

        // Project to output space
        self.out_proj.forward(&h2)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.in_proj.parameters();
        params.extend(self.ctx_proj.parameters());
        params.extend(self.hidden1.parameters());
        params.extend(self.hidden2.parameters());
        params.extend(self.out_proj.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.in_proj.zero_grad();
        self.ctx_proj.zero_grad();
        self.hidden1.zero_grad();
        self.hidden2.zero_grad();
        self.out_proj.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        let d = self.d_model;
        let h = self.d_hidden;
        // in_proj + ctx_proj + hidden1 + hidden2 + out_proj
        d * h + d * h + h * h + h * h + h * d
    }
}

/// Differentiable Encoder for JEPA
///
/// Maps input to latent representation.
#[derive(Clone)]
pub struct DifferentiableWorldModelEncoder {
    layers: Vec<DifferentiableLinear>,
    d_model: usize,
}

impl DifferentiableWorldModelEncoder {
    pub fn new(d_input: usize, d_model: usize, n_layers: usize) -> Self {
        let mut layers = Vec::with_capacity(n_layers);

        // First layer
        layers.push(DifferentiableLinear::new(d_input, d_model, true));

        // Hidden layers
        for _ in 1..n_layers {
            layers.push(DifferentiableLinear::new(d_model, d_model, true));
        }

        Self { layers, d_model }
    }

    pub fn encode(&self, x: &Variable) -> Variable {
        let mut h = x.clone();

        for (i, layer) in self.layers.iter().enumerate() {
            h = layer.forward(&h);
            if i < self.layers.len() - 1 {
                h = h.gelu();
            }
        }

        h
    }

    pub fn parameters(&self) -> Vec<Variable> {
        self.layers.iter().flat_map(|l| l.parameters()).collect()
    }

    pub fn zero_grad(&self) {
        for layer in &self.layers {
            layer.zero_grad();
        }
    }

    pub fn num_parameters(&self) -> usize {
        self.layers.len() * self.d_model * self.d_model
    }
}

/// Complete Differentiable World Model combining encoder and predictor
#[derive(Clone)]
pub struct DifferentiableWorldModel {
    /// Encoder: input -> latent
    pub encoder: DifferentiableWorldModelEncoder,
    /// Predictor: (latent, context) -> predicted_latent
    pub predictor: DifferentiableWorldModelPredictor,
    /// Model dimension
    _d_model: usize,
}

impl DifferentiableWorldModel {
    pub fn new(d_input: usize, d_model: usize, d_hidden: usize, n_encoder_layers: usize) -> Self {
        Self {
            encoder: DifferentiableWorldModelEncoder::new(d_input, d_model, n_encoder_layers),
            predictor: DifferentiableWorldModelPredictor::new(d_model, d_hidden),
            _d_model: d_model,
        }
    }

    /// Encode input to latent space
    pub fn encode(&self, x: &Variable) -> Variable {
        self.encoder.encode(x)
    }

    /// Predict next latent given current latent and context
    pub fn predict(&self, z: &Variable, context: &Variable) -> Variable {
        self.predictor.predict(z, context)
    }

    /// Compute JEPA loss: ||predictor(z_t, ctx) - stop_grad(encode(x_{t+1}))||^2
    ///
    /// In real JEPA, the target encoder uses stop-gradient (or EMA).
    /// We implement this by detaching the target.
    pub fn compute_loss(&self, x_t: &Variable, x_next: &Variable, context: &Variable) -> (f32, Variable) {
        // Encode current state
        let z_t = self.encode(x_t);

        // Predict next state
        let z_pred = self.predict(&z_t, context);

        // Encode actual next state (target) - detach for stop gradient
        let z_target = self.encode(x_next).detach();

        // L2 loss in latent space
        let diff = z_pred.sub(&z_target);
        let sq = diff.mul(&diff);

        // Mean over all dimensions
        let data = sq.data();
        let (batch, seq_len, d_model) = sq.shape();
        let n = (batch * seq_len * d_model) as f32;

        let loss_val: f32 = data.iter().sum::<f32>() / n;

        // Create loss variable for backward
        let loss_var = sq.mean();

        (loss_val, loss_var)
    }

    /// Forward pass: encode, predict, return (z_current, z_predicted)
    pub fn forward(&self, x_t: &Variable, context: &Variable) -> (Variable, Variable) {
        let z_t = self.encode(x_t);
        let z_pred = self.predict(&z_t, context);
        (z_t, z_pred)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.encoder.parameters();
        params.extend(self.predictor.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.encoder.zero_grad();
        self.predictor.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        self.encoder.num_parameters() + self.predictor.num_parameters()
    }
}

/// Masking strategy for JEPA training
#[derive(Clone, Debug)]
pub enum MaskStrategy {
    /// Random masking (like MAE)
    Random { mask_ratio: f32 },
    /// Block masking (like BEiT)
    Block { block_size: usize, num_blocks: usize },
    /// Causal masking (predict future)
    Causal,
}

impl MaskStrategy {
    /// Generate mask indices (true = masked)
    pub fn generate_mask(&self, seq_len: usize) -> Vec<bool> {
        use rand::Rng;
        let mut rng = rand::thread_rng();

        match self {
            MaskStrategy::Random { mask_ratio } => {
                (0..seq_len)
                    .map(|_| rng.gen::<f32>() < *mask_ratio)
                    .collect()
            }
            MaskStrategy::Block { block_size, num_blocks } => {
                let mut mask = vec![false; seq_len];
                for _ in 0..*num_blocks {
                    let start = (rng.gen::<f32>() * (seq_len.saturating_sub(*block_size)) as f32) as usize;
                    for i in start..std::cmp::min(start + block_size, seq_len) {
                        mask[i] = true;
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

    /// Apply mask to a Variable, replacing masked positions with zeros
    pub fn apply_mask(&self, x: &Variable, mask: &[bool]) -> Variable {
        let data = x.data();
        let (batch, seq_len, d_model) = x.shape();

        let mut masked = Array3::zeros((batch, seq_len, d_model));
        for b in 0..batch {
            for s in 0..seq_len {
                if !mask.get(s).copied().unwrap_or(false) {
                    for d in 0..d_model {
                        masked[[b, s, d]] = data[[b, s, d]];
                    }
                }
            }
        }

        Variable::new(masked, x.requires_grad())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_predictor() {
        let pred = DifferentiableWorldModelPredictor::new(64, 128);
        let z = Variable::parameter(Array3::ones((2, 4, 64)));
        let ctx = Variable::parameter(Array3::ones((2, 4, 64)));
        let out = pred.predict(&z, &ctx);
        assert_eq!(out.shape(), (2, 4, 64));
    }

    #[test]
    fn test_encoder() {
        let enc = DifferentiableWorldModelEncoder::new(64, 64, 3);
        let x = Variable::parameter(Array3::ones((2, 8, 64)));
        let z = enc.encode(&x);
        assert_eq!(z.shape(), (2, 8, 64));
    }

    #[test]
    fn test_world_model_forward() {
        let wm = DifferentiableWorldModel::new(64, 64, 128, 2);
        let x = Variable::parameter(Array3::ones((2, 4, 64)));
        let ctx = Variable::parameter(Array3::ones((2, 4, 64)));

        let (z, z_pred) = wm.forward(&x, &ctx);
        assert_eq!(z.shape(), (2, 4, 64));
        assert_eq!(z_pred.shape(), (2, 4, 64));
    }

    #[test]
    fn test_world_model_loss() {
        let wm = DifferentiableWorldModel::new(64, 64, 128, 2);
        let x_t = Variable::parameter(Array3::ones((2, 4, 64)));
        let x_next = Variable::parameter(Array3::ones((2, 4, 64)) * 2.0);
        let ctx = Variable::parameter(Array3::ones((2, 4, 64)));

        let (loss, loss_var) = wm.compute_loss(&x_t, &x_next, &ctx);
        assert!(loss > 0.0);

        // Test backward
        loss_var.backward();
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

    #[test]
    fn test_apply_mask() {
        let x = Variable::parameter(Array3::ones((1, 4, 8)));
        let mask = vec![false, true, false, true]; // Mask positions 1 and 3

        let masked = MaskStrategy::Random { mask_ratio: 0.5 }.apply_mask(&x, &mask);
        let data = masked.data();

        // Position 0 should be 1s
        assert_eq!(data[[0, 0, 0]], 1.0);
        // Position 1 should be 0s (masked)
        assert_eq!(data[[0, 1, 0]], 0.0);
        // Position 2 should be 1s
        assert_eq!(data[[0, 2, 0]], 1.0);
        // Position 3 should be 0s (masked)
        assert_eq!(data[[0, 3, 0]], 0.0);
    }

    #[test]
    fn test_parameters() {
        let wm = DifferentiableWorldModel::new(64, 64, 128, 2);
        let params = wm.parameters();
        assert!(!params.is_empty());
        println!("World model has {} parameter tensors, {} total params",
                 params.len(), wm.num_parameters());
    }
}
