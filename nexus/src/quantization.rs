//! INT8 Quantization for Efficient Deployment
//!
//! Provides quantized inference for reduced memory and faster computation.
//! Supports:
//! - Per-tensor and per-channel quantization
//! - Symmetric and asymmetric quantization
//! - Dynamic quantization (weights quantized, activations at runtime)
//! - Static quantization (calibrated scales)

use ndarray::{Array1, Array2, Array3};
use std::collections::HashMap;

/// Quantization configuration
#[derive(Clone, Debug)]
pub struct QuantConfig {
    /// Number of bits (typically 8)
    pub bits: u8,
    /// Whether to use symmetric quantization
    pub symmetric: bool,
    /// Per-channel vs per-tensor
    pub per_channel: bool,
    /// Channel axis for per-channel quantization
    pub channel_axis: usize,
}

impl Default for QuantConfig {
    fn default() -> Self {
        Self {
            bits: 8,
            symmetric: true,
            per_channel: false,
            channel_axis: 0,
        }
    }
}

impl QuantConfig {
    pub fn int8_symmetric() -> Self {
        Self { bits: 8, symmetric: true, ..Default::default() }
    }

    pub fn int8_asymmetric() -> Self {
        Self { bits: 8, symmetric: false, ..Default::default() }
    }

    pub fn int8_per_channel(axis: usize) -> Self {
        Self { bits: 8, per_channel: true, channel_axis: axis, ..Default::default() }
    }
}

/// Quantization parameters for a tensor
#[derive(Clone, Debug)]
pub struct QuantParams {
    /// Scale factor(s)
    pub scale: Vec<f32>,
    /// Zero point(s) (for asymmetric)
    pub zero_point: Vec<i32>,
    /// Whether symmetric
    pub symmetric: bool,
}

impl QuantParams {
    /// Compute quantization parameters from float data
    pub fn from_data(data: &[f32], config: &QuantConfig) -> Self {
        let _qmin = if config.symmetric { -128 } else { 0 };
        let _qmax = 255_i32;

        let min_val = data.iter().cloned().fold(f32::INFINITY, f32::min);
        let max_val = data.iter().cloned().fold(f32::NEG_INFINITY, f32::max);

        if config.symmetric {
            // Symmetric: scale based on max absolute value
            let abs_max = min_val.abs().max(max_val.abs());
            let scale = abs_max / 127.0;
            let scale = if scale == 0.0 { 1.0 } else { scale };

            Self {
                scale: vec![scale],
                zero_point: vec![0],
                symmetric: true,
            }
        } else {
            // Asymmetric: scale based on actual range
            let range = max_val - min_val;
            let scale = range / 255.0;
            let scale = if scale == 0.0 { 1.0 } else { scale };
            let zero_point = ((-min_val / scale).round() as i32).clamp(0, 255);

            Self {
                scale: vec![scale],
                zero_point: vec![zero_point],
                symmetric: false,
            }
        }
    }

    /// Compute per-channel quantization parameters
    pub fn from_data_per_channel(data: &Array2<f32>, axis: usize, config: &QuantConfig) -> Self {
        let n_channels = data.shape()[axis];
        let mut scales = Vec::with_capacity(n_channels);
        let mut zero_points = Vec::with_capacity(n_channels);

        for c in 0..n_channels {
            let channel_data: Vec<f32> = if axis == 0 {
                data.row(c).to_vec()
            } else {
                data.column(c).to_vec()
            };

            let params = Self::from_data(&channel_data, &QuantConfig {
                per_channel: false,
                ..*config
            });

            scales.push(params.scale[0]);
            zero_points.push(params.zero_point[0]);
        }

        Self {
            scale: scales,
            zero_point: zero_points,
            symmetric: config.symmetric,
        }
    }
}

/// Quantized INT8 tensor
#[derive(Clone)]
pub struct QuantizedTensor {
    /// Quantized data
    pub data: Vec<i8>,
    /// Shape
    pub shape: Vec<usize>,
    /// Quantization parameters
    pub params: QuantParams,
}

impl QuantizedTensor {
    /// Quantize a float tensor
    pub fn quantize(data: &Array2<f32>, config: &QuantConfig) -> Self {
        let flat: Vec<f32> = data.iter().cloned().collect();
        let params = if config.per_channel {
            QuantParams::from_data_per_channel(data, config.channel_axis, config)
        } else {
            QuantParams::from_data(&flat, config)
        };

        let shape = data.shape().to_vec();
        let quantized = Self::quantize_with_params(&flat, &shape, &params, config);

        Self {
            data: quantized,
            shape,
            params,
        }
    }

    fn quantize_with_params(
        data: &[f32],
        _shape: &[usize],
        params: &QuantParams,
        config: &QuantConfig,
    ) -> Vec<i8> {
        if config.per_channel && params.scale.len() > 1 {
            let n_channels = params.scale.len();
            let channel_size = data.len() / n_channels;

            data.chunks(channel_size)
                .enumerate()
                .flat_map(|(c, chunk)| {
                    let scale = params.scale[c];
                    let zp = params.zero_point[c];

                    chunk.iter().map(move |&v| {
                        let q = (v / scale).round() as i32 + zp;
                        q.clamp(-128, 127) as i8
                    })
                })
                .collect()
        } else {
            let scale = params.scale[0];
            let zp = params.zero_point[0];

            data.iter()
                .map(|&v| {
                    let q = (v / scale).round() as i32 + zp;
                    q.clamp(-128, 127) as i8
                })
                .collect()
        }
    }

    /// Dequantize back to float
    pub fn dequantize(&self) -> Array2<f32> {
        let rows = self.shape[0];
        let cols = self.shape[1];

        if self.params.scale.len() > 1 {
            // Per-channel dequantization
            let channel_size = self.data.len() / self.params.scale.len();
            let mut result = Array2::zeros((rows, cols));

            for (c, chunk) in self.data.chunks(channel_size).enumerate() {
                let scale = self.params.scale[c];
                let zp = self.params.zero_point[c];

                for (i, &q) in chunk.iter().enumerate() {
                    let row = c;
                    let col = i;
                    result[[row, col]] = (q as i32 - zp) as f32 * scale;
                }
            }

            result
        } else {
            let scale = self.params.scale[0];
            let zp = self.params.zero_point[0];

            let deq: Vec<f32> = self.data
                .iter()
                .map(|&q| (q as i32 - zp) as f32 * scale)
                .collect();

            Array2::from_shape_vec((rows, cols), deq).unwrap()
        }
    }

    /// Get memory size in bytes
    pub fn size_bytes(&self) -> usize {
        self.data.len() + self.params.scale.len() * 4 + self.params.zero_point.len() * 4
    }
}

/// Quantized linear layer
#[derive(Clone)]
pub struct QuantizedLinear {
    /// Quantized weights
    weight: QuantizedTensor,
    /// Optional bias (kept in fp32)
    bias: Option<Array1<f32>>,
    /// Input features
    in_features: usize,
    /// Output features
    out_features: usize,
}

impl QuantizedLinear {
    /// Create from float weights
    pub fn from_weights(weight: &Array2<f32>, bias: Option<&Array1<f32>>, config: &QuantConfig) -> Self {
        let (out_features, in_features) = weight.dim();

        Self {
            weight: QuantizedTensor::quantize(weight, config),
            bias: bias.cloned(),
            in_features,
            out_features,
        }
    }

    /// Forward pass with dynamic activation quantization
    pub fn forward(&self, x: &Array3<f32>) -> Array3<f32> {
        let (batch, seq_len, _) = x.dim();
        let mut output = Array3::zeros((batch, seq_len, self.out_features));

        // Dequantize weights once
        let weight = self.weight.dequantize();

        for b in 0..batch {
            for s in 0..seq_len {
                for o in 0..self.out_features {
                    let mut sum = 0.0f32;
                    for i in 0..self.in_features {
                        sum += x[[b, s, i]] * weight[[o, i]];
                    }
                    if let Some(ref bias) = self.bias {
                        sum += bias[o];
                    }
                    output[[b, s, o]] = sum;
                }
            }
        }

        output
    }

    /// Forward with quantized activations (faster but less accurate)
    pub fn forward_quantized(&self, x: &Array3<f32>) -> Array3<f32> {
        let (batch, seq_len, _) = x.dim();
        let mut output = Array3::zeros((batch, seq_len, self.out_features));

        let weight_scale = self.weight.params.scale[0];
        let weight_zp = self.weight.params.zero_point[0];

        for b in 0..batch {
            for s in 0..seq_len {
                // Quantize input for this position
                let input_slice: Vec<f32> = (0..self.in_features)
                    .map(|i| x[[b, s, i]])
                    .collect();

                let input_params = QuantParams::from_data(&input_slice, &QuantConfig::int8_symmetric());
                let input_scale = input_params.scale[0];

                let input_quant: Vec<i8> = input_slice.iter()
                    .map(|&v| (v / input_scale).round().clamp(-128.0, 127.0) as i8)
                    .collect();

                // INT8 matmul
                for o in 0..self.out_features {
                    let mut acc: i32 = 0;
                    for i in 0..self.in_features {
                        let w_idx = o * self.in_features + i;
                        let w = self.weight.data[w_idx] as i32 - weight_zp;
                        let x = input_quant[i] as i32;
                        acc += w * x;
                    }

                    // Dequantize output
                    let scale = weight_scale * input_scale;
                    let mut out = acc as f32 * scale;

                    if let Some(ref bias) = self.bias {
                        out += bias[o];
                    }

                    output[[b, s, o]] = out;
                }
            }
        }

        output
    }

    /// Memory savings compared to fp32
    pub fn memory_savings(&self) -> f32 {
        let fp32_size = self.in_features * self.out_features * 4;
        let quant_size = self.weight.size_bytes();
        1.0 - (quant_size as f32 / fp32_size as f32)
    }

    pub fn in_features(&self) -> usize { self.in_features }
    pub fn out_features(&self) -> usize { self.out_features }
}

/// Calibration data collector for static quantization
pub struct CalibrationCollector {
    /// Min/max values per layer
    layer_stats: HashMap<String, (f32, f32)>,
    /// Number of samples seen
    n_samples: usize,
}

impl CalibrationCollector {
    pub fn new() -> Self {
        Self {
            layer_stats: HashMap::new(),
            n_samples: 0,
        }
    }

    /// Record activation statistics
    pub fn record(&mut self, layer_name: &str, activations: &Array3<f32>) {
        let min_val = activations.iter().cloned().fold(f32::INFINITY, f32::min);
        let max_val = activations.iter().cloned().fold(f32::NEG_INFINITY, f32::max);

        let stats = self.layer_stats.entry(layer_name.to_string()).or_insert((f32::INFINITY, f32::NEG_INFINITY));
        stats.0 = stats.0.min(min_val);
        stats.1 = stats.1.max(max_val);

        self.n_samples += 1;
    }

    /// Get calibrated quantization parameters
    pub fn get_params(&self, layer_name: &str, config: &QuantConfig) -> Option<QuantParams> {
        self.layer_stats.get(layer_name).map(|(min_val, max_val)| {
            let range = max_val - min_val;
            if config.symmetric {
                let abs_max = min_val.abs().max(max_val.abs());
                let scale = abs_max / 127.0;
                QuantParams {
                    scale: vec![if scale == 0.0 { 1.0 } else { scale }],
                    zero_point: vec![0],
                    symmetric: true,
                }
            } else {
                let scale = range / 255.0;
                let scale = if scale == 0.0 { 1.0 } else { scale };
                let zp = ((-min_val / scale).round() as i32).clamp(0, 255);
                QuantParams {
                    scale: vec![scale],
                    zero_point: vec![zp],
                    symmetric: false,
                }
            }
        })
    }

    pub fn n_samples(&self) -> usize { self.n_samples }
    pub fn n_layers(&self) -> usize { self.layer_stats.len() }
}

impl Default for CalibrationCollector {
    fn default() -> Self {
        Self::new()
    }
}

/// Mixed precision model wrapper
/// Keeps some layers in fp32, others in int8
pub struct MixedPrecisionModel {
    /// Quantized layers
    quantized_layers: HashMap<String, QuantizedLinear>,
    /// FP32 layers (kept for sensitive operations)
    fp32_layers: HashMap<String, (Array2<f32>, Option<Array1<f32>>)>,
}

impl MixedPrecisionModel {
    pub fn new() -> Self {
        Self {
            quantized_layers: HashMap::new(),
            fp32_layers: HashMap::new(),
        }
    }

    /// Add a quantized layer
    pub fn add_quantized(&mut self, name: &str, weight: &Array2<f32>, bias: Option<&Array1<f32>>, config: &QuantConfig) {
        let layer = QuantizedLinear::from_weights(weight, bias, config);
        self.quantized_layers.insert(name.to_string(), layer);
    }

    /// Add a fp32 layer (for sensitive operations like final projection)
    pub fn add_fp32(&mut self, name: &str, weight: Array2<f32>, bias: Option<Array1<f32>>) {
        self.fp32_layers.insert(name.to_string(), (weight, bias));
    }

    /// Forward through a specific layer
    pub fn forward_layer(&self, name: &str, x: &Array3<f32>) -> Option<Array3<f32>> {
        if let Some(layer) = self.quantized_layers.get(name) {
            Some(layer.forward(x))
        } else if let Some((weight, bias)) = self.fp32_layers.get(name) {
            // FP32 matmul
            let (batch, seq_len, _) = x.dim();
            let out_features = weight.nrows();
            let in_features = weight.ncols();

            let mut output = Array3::zeros((batch, seq_len, out_features));
            for b in 0..batch {
                for s in 0..seq_len {
                    for o in 0..out_features {
                        let mut sum = 0.0f32;
                        for i in 0..in_features {
                            sum += x[[b, s, i]] * weight[[o, i]];
                        }
                        if let Some(ref bias) = bias {
                            sum += bias[o];
                        }
                        output[[b, s, o]] = sum;
                    }
                }
            }
            Some(output)
        } else {
            None
        }
    }

    /// Total memory usage
    pub fn memory_usage(&self) -> usize {
        let quant_mem: usize = self.quantized_layers.values()
            .map(|l| l.weight.size_bytes())
            .sum();

        let fp32_mem: usize = self.fp32_layers.values()
            .map(|(w, b)| {
                w.len() * 4 + b.as_ref().map(|b| b.len() * 4).unwrap_or(0)
            })
            .sum();

        quant_mem + fp32_mem
    }
}

impl Default for MixedPrecisionModel {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quant_params_symmetric() {
        let data = vec![-5.0, 0.0, 5.0, 10.0];
        let config = QuantConfig::int8_symmetric();
        let params = QuantParams::from_data(&data, &config);

        assert!(params.symmetric);
        assert_eq!(params.zero_point[0], 0);
        assert!(params.scale[0] > 0.0);
    }

    #[test]
    fn test_quant_params_asymmetric() {
        let data = vec![0.0, 100.0, 200.0];
        let config = QuantConfig::int8_asymmetric();
        let params = QuantParams::from_data(&data, &config);

        assert!(!params.symmetric);
        assert!(params.zero_point[0] >= 0);
        assert!(params.scale[0] > 0.0);
    }

    #[test]
    fn test_quantize_dequantize() {
        let original = Array2::from_shape_fn((4, 4), |(i, j)| (i + j) as f32 * 0.5 - 1.0);
        let config = QuantConfig::int8_symmetric();

        let quantized = QuantizedTensor::quantize(&original, &config);
        let dequantized = quantized.dequantize();

        // Check shape preserved
        assert_eq!(dequantized.dim(), original.dim());

        // Check values are close (quantization error should be small)
        for i in 0..4 {
            for j in 0..4 {
                let error = (dequantized[[i, j]] - original[[i, j]]).abs();
                assert!(error < 0.1, "Large quantization error at [{}, {}]: {} vs {}",
                    i, j, original[[i, j]], dequantized[[i, j]]);
            }
        }
    }

    #[test]
    fn test_quantized_linear() {
        let weight = Array2::from_shape_fn((16, 8), |(i, j)| ((i + j) as f32 - 12.0) * 0.1);
        let bias = Array1::from_shape_fn(16, |i| i as f32 * 0.01);

        let config = QuantConfig::int8_symmetric();
        let layer = QuantizedLinear::from_weights(&weight, Some(&bias), &config);

        let x = Array3::ones((2, 4, 8));
        let output = layer.forward(&x);

        assert_eq!(output.dim(), (2, 4, 16));
    }

    #[test]
    fn test_quantized_vs_fp32() {
        let weight = Array2::from_shape_fn((16, 8), |(i, j)| ((i + j) as f32 - 12.0) * 0.1);
        let config = QuantConfig::int8_symmetric();
        let layer = QuantizedLinear::from_weights(&weight, None, &config);

        let x = Array3::ones((1, 1, 8));

        // Compare quantized and quantized-activation paths
        let out_dequant = layer.forward(&x);
        let out_quant = layer.forward_quantized(&x);

        // Should be similar (within quantization error)
        for o in 0..16 {
            let diff = (out_dequant[[0, 0, o]] - out_quant[[0, 0, o]]).abs();
            assert!(diff < 0.5, "Large difference at output {}: {} vs {}",
                o, out_dequant[[0, 0, o]], out_quant[[0, 0, o]]);
        }
    }

    #[test]
    fn test_memory_savings() {
        let weight = Array2::ones((1024, 1024));
        let config = QuantConfig::int8_symmetric();
        let layer = QuantizedLinear::from_weights(&weight, None, &config);

        let savings = layer.memory_savings();
        // INT8 should save ~75% compared to FP32
        assert!(savings > 0.7, "Expected >70% savings, got {}%", savings * 100.0);
    }

    #[test]
    fn test_calibration() {
        let mut collector = CalibrationCollector::new();

        // Simulate calibration data
        let act1 = Array3::from_shape_fn((2, 4, 8), |(_, _, _)| rand::random::<f32>() * 2.0 - 1.0);
        let act2 = Array3::from_shape_fn((2, 4, 8), |(_, _, _)| rand::random::<f32>() * 2.0 - 1.0);

        collector.record("layer1", &act1);
        collector.record("layer1", &act2);

        assert_eq!(collector.n_samples(), 2);
        assert_eq!(collector.n_layers(), 1);

        let params = collector.get_params("layer1", &QuantConfig::int8_symmetric());
        assert!(params.is_some());
    }

    #[test]
    fn test_per_channel_quantization() {
        let weight = Array2::from_shape_fn((4, 8), |(i, j)| {
            // Different ranges per row
            (i as f32 + 1.0) * (j as f32 - 4.0)
        });

        let config = QuantConfig::int8_per_channel(0);
        let quantized = QuantizedTensor::quantize(&weight, &config);

        // Should have 4 scale values (one per channel)
        assert_eq!(quantized.params.scale.len(), 4);

        let dequantized = quantized.dequantize();
        assert_eq!(dequantized.dim(), weight.dim());
    }

    #[test]
    fn test_mixed_precision() {
        let mut model = MixedPrecisionModel::new();

        let w1 = Array2::ones((16, 8));
        let w2 = Array2::ones((4, 16));

        model.add_quantized("layer1", &w1, None, &QuantConfig::int8_symmetric());
        model.add_fp32("output", w2.clone(), None);

        let x = Array3::ones((1, 1, 8));
        let out1 = model.forward_layer("layer1", &x).unwrap();
        assert_eq!(out1.dim(), (1, 1, 16));

        let out2 = model.forward_layer("output", &out1).unwrap();
        assert_eq!(out2.dim(), (1, 1, 4));
    }
}
