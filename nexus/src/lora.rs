//! LoRA (Low-Rank Adaptation) for Parameter-Efficient Fine-Tuning
//!
//! LoRA adds small trainable low-rank matrices to frozen base weights,
//! enabling efficient fine-tuning with minimal parameters.
//!
//! References:
//! - "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021)
//!
//! Key benefits:
//! - 10-100x fewer trainable parameters
//! - Base model stays frozen (easy to swap adapters)
//! - Can merge adapters into base weights for zero-overhead inference

use ndarray::{Array2, ArrayView2};
use rand::Rng;
use rand_distr::Normal;

// ============================================================================
// Configuration
// ============================================================================

/// LoRA configuration for a layer
#[derive(Clone, Debug)]
pub struct LoRAConfig {
    /// Rank of the low-rank matrices (typically 4, 8, 16, 32)
    pub rank: usize,
    /// Scaling factor (alpha / rank) - typical alpha = 16 or 32
    pub alpha: f32,
    /// Dropout applied to LoRA outputs during training
    pub dropout: f32,
    /// Whether to apply LoRA to query projection
    pub apply_to_q: bool,
    /// Whether to apply LoRA to key projection
    pub apply_to_k: bool,
    /// Whether to apply LoRA to value projection
    pub apply_to_v: bool,
    /// Whether to apply LoRA to output projection
    pub apply_to_o: bool,
    /// Whether to apply LoRA to MLP layers
    pub apply_to_mlp: bool,
}

impl Default for LoRAConfig {
    fn default() -> Self {
        Self {
            rank: 8,
            alpha: 16.0,
            dropout: 0.0,
            apply_to_q: true,
            apply_to_k: false,
            apply_to_v: true,
            apply_to_o: false,
            apply_to_mlp: false,
        }
    }
}

impl LoRAConfig {
    /// Create a minimal LoRA config (Q and V only)
    pub fn minimal(rank: usize) -> Self {
        Self {
            rank,
            alpha: rank as f32 * 2.0,
            ..Default::default()
        }
    }

    /// Create full LoRA config (all attention + MLP)
    pub fn full(rank: usize) -> Self {
        Self {
            rank,
            alpha: rank as f32 * 2.0,
            apply_to_q: true,
            apply_to_k: true,
            apply_to_v: true,
            apply_to_o: true,
            apply_to_mlp: true,
            dropout: 0.05,
            ..Default::default()
        }
    }

    /// Compute the scaling factor
    pub fn scale(&self) -> f32 {
        self.alpha / self.rank as f32
    }
}

// ============================================================================
// LoRA Layer
// ============================================================================

/// Low-rank adapter layer
///
/// Implements: output = Wx + (BA)x * scale
/// Where W is frozen, and B (down-projection) and A (up-projection) are trained.
#[derive(Clone)]
pub struct LoRALayer {
    /// Down-projection: d_in -> rank (initialized to Gaussian)
    pub a: Array2<f32>,
    /// Up-projection: rank -> d_out (initialized to zeros)
    pub b: Array2<f32>,
    /// Gradient for A
    pub grad_a: Option<Array2<f32>>,
    /// Gradient for B
    pub grad_b: Option<Array2<f32>>,
    /// Scaling factor (alpha / rank)
    pub scale: f32,
    /// Input dimension
    pub d_in: usize,
    /// Output dimension
    pub d_out: usize,
    /// Rank
    pub rank: usize,
    /// Whether this layer is active (for easy enable/disable)
    pub active: bool,
}

impl LoRALayer {
    /// Create a new LoRA layer
    pub fn new(d_in: usize, d_out: usize, rank: usize, alpha: f32) -> Self {
        let mut rng = rand::thread_rng();
        let std = (2.0 / d_in as f32).sqrt();
        let normal = Normal::new(0.0, std).unwrap();

        // A is initialized with small random values (Kaiming-like)
        let a_data: Vec<f32> = (0..d_in * rank)
            .map(|_| rng.sample(normal))
            .collect();
        let a = Array2::from_shape_vec((d_in, rank), a_data).unwrap();

        // B is initialized to zeros (so initially LoRA has no effect)
        let b = Array2::zeros((rank, d_out));

        Self {
            a,
            b,
            grad_a: None,
            grad_b: None,
            scale: alpha / rank as f32,
            d_in,
            d_out,
            rank,
            active: true,
        }
    }

    /// Create from existing config
    pub fn from_config(d_in: usize, d_out: usize, config: &LoRAConfig) -> Self {
        Self::new(d_in, d_out, config.rank, config.alpha)
    }

    /// Forward pass: compute LoRA delta
    /// Returns delta to be added to base layer output
    pub fn forward(&self, x: &ArrayView2<f32>) -> Array2<f32> {
        if !self.active {
            return Array2::zeros((x.nrows(), self.d_out));
        }

        // x: [batch, d_in]
        // a: [d_in, rank]
        // b: [rank, d_out]
        // output: [batch, d_out]

        // Two-stage matmul: x @ A @ B * scale
        let hidden = x.dot(&self.a);  // [batch, rank]
        let delta = hidden.dot(&self.b);  // [batch, d_out]

        delta * self.scale
    }

    /// Forward pass with gradient computation
    /// Returns (output, cache for backward)
    pub fn forward_with_cache(&self, x: &ArrayView2<f32>) -> (Array2<f32>, Array2<f32>) {
        let hidden = x.dot(&self.a);
        let output = hidden.dot(&self.b) * self.scale;
        (output, hidden)
    }

    /// Backward pass: compute gradients
    pub fn backward(&mut self, x: &ArrayView2<f32>, hidden: &ArrayView2<f32>, grad_output: &ArrayView2<f32>) {
        // grad_output: [batch, d_out]
        // hidden (from forward): [batch, rank]
        // x: [batch, d_in]

        let scaled_grad = grad_output * self.scale;

        // Gradient for B: hidden.T @ grad_output
        // [rank, batch] @ [batch, d_out] = [rank, d_out]
        let grad_b = hidden.t().dot(&scaled_grad);

        // Gradient for hidden: grad_output @ B.T
        // [batch, d_out] @ [d_out, rank] = [batch, rank]
        let grad_hidden = scaled_grad.dot(&self.b.t());

        // Gradient for A: x.T @ grad_hidden
        // [d_in, batch] @ [batch, rank] = [d_in, rank]
        let grad_a = x.t().dot(&grad_hidden);

        // Accumulate gradients
        if let Some(ref mut existing) = self.grad_a {
            *existing = &*existing + &grad_a;
        } else {
            self.grad_a = Some(grad_a);
        }

        if let Some(ref mut existing) = self.grad_b {
            *existing = &*existing + &grad_b;
        } else {
            self.grad_b = Some(grad_b);
        }
    }

    /// Apply gradient update (simple SGD)
    pub fn update(&mut self, lr: f32) {
        if let Some(ref grad_a) = self.grad_a {
            self.a = &self.a - &(grad_a * lr);
        }
        if let Some(ref grad_b) = self.grad_b {
            self.b = &self.b - &(grad_b * lr);
        }
    }

    /// Apply gradient update with weight decay
    pub fn update_with_decay(&mut self, lr: f32, weight_decay: f32) {
        if let Some(ref grad_a) = self.grad_a {
            let decay = &self.a * weight_decay;
            self.a = &self.a - &((grad_a + &decay) * lr);
        }
        if let Some(ref grad_b) = self.grad_b {
            let decay = &self.b * weight_decay;
            self.b = &self.b - &((grad_b + &decay) * lr);
        }
    }

    /// Zero gradients
    pub fn zero_grad(&mut self) {
        self.grad_a = None;
        self.grad_b = None;
    }

    /// Count trainable parameters
    pub fn num_parameters(&self) -> usize {
        self.d_in * self.rank + self.rank * self.d_out
    }

    /// Merge LoRA weights into base weight matrix
    /// Returns: W' = W + BA * scale (for W in [d_out, d_in] format)
    pub fn merge_into(&self, base_weight: &Array2<f32>) -> Array2<f32> {
        // Compute A @ B: [d_in, rank] @ [rank, d_out] = [d_in, d_out]
        let lora_weight = self.a.dot(&self.b) * self.scale;

        // If base_weight is [d_out, d_in], add lora_weight.t()
        if base_weight.shape() == [self.d_out, self.d_in] {
            base_weight + &lora_weight.t()
        } else {
            // Assume [d_in, d_out]
            base_weight + &lora_weight
        }
    }
}

// ============================================================================
// LoRA Adapter Collection
// ============================================================================

/// Collection of LoRA adapters for a model
pub struct LoRAAdapters {
    /// Name -> LoRA layer mapping
    pub layers: std::collections::HashMap<String, LoRALayer>,
    /// Global configuration
    pub config: LoRAConfig,
}

impl LoRAAdapters {
    pub fn new(config: LoRAConfig) -> Self {
        Self {
            layers: std::collections::HashMap::new(),
            config,
        }
    }

    /// Add a LoRA adapter for a named layer
    pub fn add_adapter(&mut self, name: &str, d_in: usize, d_out: usize) {
        let layer = LoRALayer::from_config(d_in, d_out, &self.config);
        self.layers.insert(name.to_string(), layer);
    }

    /// Count total trainable parameters
    pub fn num_parameters(&self) -> usize {
        self.layers.values()
            .map(|l| l.num_parameters())
            .sum()
    }

    /// Zero all gradients
    pub fn zero_grad(&mut self) {
        for layer in self.layers.values_mut() {
            layer.zero_grad();
        }
    }

    /// Update all adapters
    pub fn update(&mut self, lr: f32) {
        for layer in self.layers.values_mut() {
            layer.update(lr);
        }
    }

    /// Update with weight decay
    pub fn update_with_decay(&mut self, lr: f32, weight_decay: f32) {
        for layer in self.layers.values_mut() {
            layer.update_with_decay(lr, weight_decay);
        }
    }

    /// Enable all adapters
    pub fn enable(&mut self) {
        for layer in self.layers.values_mut() {
            layer.active = true;
        }
    }

    /// Disable all adapters (for inference comparison)
    pub fn disable(&mut self) {
        for layer in self.layers.values_mut() {
            layer.active = false;
        }
    }

    /// Save adapters to file
    pub fn save(&self, path: &str) -> std::io::Result<()> {
        use std::io::Write;

        let mut file = std::fs::File::create(path)?;

        let layer_count = self.layers.len() as u32;
        file.write_all(&layer_count.to_le_bytes())?;

        for (name, layer) in &self.layers {
            // Name
            let name_bytes = name.as_bytes();
            file.write_all(&(name_bytes.len() as u32).to_le_bytes())?;
            file.write_all(name_bytes)?;

            // Dimensions
            file.write_all(&(layer.rank as u32).to_le_bytes())?;
            file.write_all(&(layer.d_in as u32).to_le_bytes())?;
            file.write_all(&(layer.d_out as u32).to_le_bytes())?;
            file.write_all(&layer.scale.to_le_bytes())?;

            // A matrix
            for val in layer.a.iter() {
                file.write_all(&val.to_le_bytes())?;
            }

            // B matrix
            for val in layer.b.iter() {
                file.write_all(&val.to_le_bytes())?;
            }
        }

        Ok(())
    }

    /// Load adapters from file
    pub fn load(path: &str) -> std::io::Result<Self> {
        use std::io::Read;

        let mut file = std::fs::File::open(path)?;
        let mut adapters = Self::new(LoRAConfig::default());

        let mut buf4 = [0u8; 4];

        file.read_exact(&mut buf4)?;
        let layer_count = u32::from_le_bytes(buf4) as usize;

        for _ in 0..layer_count {
            // Name
            file.read_exact(&mut buf4)?;
            let name_len = u32::from_le_bytes(buf4) as usize;
            let mut name_bytes = vec![0u8; name_len];
            file.read_exact(&mut name_bytes)?;
            let name = String::from_utf8(name_bytes)
                .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

            // Dimensions
            file.read_exact(&mut buf4)?;
            let rank = u32::from_le_bytes(buf4) as usize;
            file.read_exact(&mut buf4)?;
            let d_in = u32::from_le_bytes(buf4) as usize;
            file.read_exact(&mut buf4)?;
            let d_out = u32::from_le_bytes(buf4) as usize;
            file.read_exact(&mut buf4)?;
            let scale = f32::from_le_bytes(buf4);

            // A matrix
            let mut a_data = vec![0f32; d_in * rank];
            for val in a_data.iter_mut() {
                file.read_exact(&mut buf4)?;
                *val = f32::from_le_bytes(buf4);
            }

            // B matrix
            let mut b_data = vec![0f32; rank * d_out];
            for val in b_data.iter_mut() {
                file.read_exact(&mut buf4)?;
                *val = f32::from_le_bytes(buf4);
            }

            // Create layer
            let mut layer = LoRALayer::new(d_in, d_out, rank, scale * rank as f32);
            layer.a = Array2::from_shape_vec((d_in, rank), a_data).unwrap();
            layer.b = Array2::from_shape_vec((rank, d_out), b_data).unwrap();
            layer.scale = scale;

            adapters.layers.insert(name, layer);
        }

        Ok(adapters)
    }
}

// ============================================================================
// Differentiable LoRA (simplified wrapper)
// ============================================================================

/// Differentiable LoRA layer for integration with autograd
/// Just wraps the basic LoRA layer
pub struct DifferentiableLoRALayer {
    pub layer: LoRALayer,
}

impl DifferentiableLoRALayer {
    pub fn new(d_in: usize, d_out: usize, rank: usize, alpha: f32) -> Self {
        Self {
            layer: LoRALayer::new(d_in, d_out, rank, alpha),
        }
    }

    pub fn forward(&self, x: &ArrayView2<f32>) -> Array2<f32> {
        self.layer.forward(x)
    }

    pub fn num_parameters(&self) -> usize {
        self.layer.num_parameters()
    }
}

// ============================================================================
// Utility Functions
// ============================================================================

/// Calculate memory savings from using LoRA
pub fn lora_efficiency_stats(base_params: usize, lora_params: usize) -> (f32, f32) {
    let reduction = 1.0 - (lora_params as f32 / base_params as f32);
    let ratio = base_params as f32 / lora_params as f32;
    (reduction * 100.0, ratio)
}

/// Print LoRA configuration summary
pub fn print_lora_summary(config: &LoRAConfig, base_params: usize, lora_params: usize) {
    let (reduction, ratio) = lora_efficiency_stats(base_params, lora_params);

    println!("╔═══════════════════════════════════════════════════════════════════╗");
    println!("║                      LoRA CONFIGURATION                           ║");
    println!("╠═══════════════════════════════════════════════════════════════════╣");
    println!("║  Rank:                 {:>10}                                ║", config.rank);
    println!("║  Alpha:                {:>10.1}                                ║", config.alpha);
    println!("║  Scale:                {:>10.3}                                ║", config.scale());
    println!("║  Dropout:              {:>10.2}                                ║", config.dropout);
    println!("╠═══════════════════════════════════════════════════════════════════╣");
    println!("║  Base Parameters:      {:>10}                                ║", base_params);
    println!("║  LoRA Parameters:      {:>10}                                ║", lora_params);
    println!("║  Parameter Reduction:  {:>10.1}%                               ║", reduction);
    println!("║  Efficiency Ratio:     {:>10.1}x                               ║", ratio);
    println!("╚═══════════════════════════════════════════════════════════════════╝");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lora_layer_creation() {
        let layer = LoRALayer::new(256, 512, 8, 16.0);
        assert_eq!(layer.d_in, 256);
        assert_eq!(layer.d_out, 512);
        assert_eq!(layer.rank, 8);
        assert_eq!(layer.scale, 2.0); // 16 / 8
        assert_eq!(layer.num_parameters(), 256 * 8 + 8 * 512); // 2048 + 4096 = 6144
    }

    #[test]
    fn test_lora_forward() {
        let layer = LoRALayer::new(64, 128, 4, 8.0);
        let x = Array2::ones((2, 64));
        let delta = layer.forward(&x.view());
        assert_eq!(delta.shape(), &[2, 128]);
    }

    #[test]
    fn test_lora_initially_zero() {
        // B is initialized to zeros, so LoRA output should be zeros initially
        let layer = LoRALayer::new(64, 128, 4, 8.0);
        let x = Array2::ones((2, 64));
        let delta = layer.forward(&x.view());

        // Should be all zeros since B is zeros
        let max_val = delta.iter().map(|v| v.abs()).fold(0.0f32, f32::max);
        assert!(max_val < 1e-6, "LoRA should initially produce zeros");
    }

    #[test]
    fn test_lora_config_scale() {
        let config = LoRAConfig {
            rank: 8,
            alpha: 32.0,
            ..Default::default()
        };
        assert_eq!(config.scale(), 4.0); // 32 / 8
    }

    #[test]
    fn test_lora_adapters() {
        let config = LoRAConfig::minimal(4);
        let mut adapters = LoRAAdapters::new(config);

        adapters.add_adapter("layer0.q", 256, 256);
        adapters.add_adapter("layer0.v", 256, 256);

        assert_eq!(adapters.layers.len(), 2);

        let params = adapters.num_parameters();
        // Each adapter: 256 * 4 + 4 * 256 = 2048
        // Total: 2 * 2048 = 4096
        assert_eq!(params, 4096);
    }

    #[test]
    fn test_lora_gradient_update() {
        let mut layer = LoRALayer::new(64, 32, 4, 8.0);

        // Set B to something non-zero for testing
        layer.b = Array2::ones((4, 32)) * 0.1;

        let x = Array2::ones((2, 64));
        let (output, hidden) = layer.forward_with_cache(&x.view());

        // Simulate gradient
        let grad_output = Array2::ones((2, 32));
        layer.backward(&x.view(), &hidden.view(), &grad_output.view());

        assert!(layer.grad_a.is_some());
        assert!(layer.grad_b.is_some());

        // Apply update
        let old_a = layer.a.clone();
        layer.update(0.01);

        // A should have changed
        assert!((&layer.a - &old_a).iter().any(|&v| v.abs() > 1e-6));
    }
}
