//! Basic tensor operations for Nexus
//!
//! A minimal tensor implementation for prototyping.
//! In production, this would use a proper ML framework.

use ndarray::{Array1, Array2, Array3, Axis, s};
use rand_distr::{Distribution, Normal};
use serde::{Serialize, Deserialize};

/// A simple tensor wrapper around ndarray
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Tensor {
    /// Shape: [batch, seq_len, d_model] for 3D, [batch, d_model] for 2D
    pub data: Array3<f32>,
}

impl Tensor {
    /// Create a new tensor filled with zeros
    pub fn zeros(batch: usize, seq_len: usize, d_model: usize) -> Self {
        Self {
            data: Array3::zeros((batch, seq_len, d_model)),
        }
    }

    /// Create a tensor with random normal initialization
    pub fn randn(batch: usize, seq_len: usize, d_model: usize) -> Self {
        let mut rng = rand::thread_rng();
        let normal = Normal::new(0.0, 0.02).unwrap();

        let data = Array3::from_shape_fn((batch, seq_len, d_model), |_| {
            normal.sample(&mut rng)
        });

        Self { data }
    }

    /// Get tensor shape
    pub fn shape(&self) -> (usize, usize, usize) {
        let s = self.data.shape();
        (s[0], s[1], s[2])
    }

    /// Matrix multiplication: [B, S, D] @ [D, D'] -> [B, S, D']
    pub fn matmul(&self, weight: &Array2<f32>) -> Self {
        let (batch, seq_len, _) = self.shape();
        let d_out = weight.shape()[1];

        let mut result = Array3::zeros((batch, seq_len, d_out));

        for b in 0..batch {
            for s in 0..seq_len {
                let row = self.data.slice(s![b, s, ..]);
                let out = row.dot(weight);
                result.slice_mut(s![b, s, ..]).assign(&out);
            }
        }

        Self { data: result }
    }

    /// Element-wise addition
    pub fn add(&self, other: &Tensor) -> Self {
        Self {
            data: &self.data + &other.data,
        }
    }

    /// Element-wise multiplication
    pub fn mul(&self, other: &Tensor) -> Self {
        Self {
            data: &self.data * &other.data,
        }
    }

    /// Scale by a scalar
    pub fn scale(&self, s: f32) -> Self {
        Self {
            data: &self.data * s,
        }
    }

    /// Softmax along the last dimension
    pub fn softmax(&self) -> Self {
        let (batch, seq_len, _) = self.shape();
        let mut result = self.data.clone();

        for b in 0..batch {
            for s in 0..seq_len {
                let mut row = result.slice_mut(s![b, s, ..]);
                let max = row.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                row.mapv_inplace(|x| (x - max).exp());
                let sum: f32 = row.iter().sum();
                row.mapv_inplace(|x| x / sum);
            }
        }

        Self { data: result }
    }

    /// RMS Normalization (used in modern transformers)
    pub fn rms_norm(&self, weight: &Array1<f32>, eps: f32) -> Self {
        let (batch, seq_len, d_model) = self.shape();
        let mut result = self.data.clone();

        for b in 0..batch {
            for s in 0..seq_len {
                let row = result.slice(s![b, s, ..]);
                let rms = (row.iter().map(|x| x * x).sum::<f32>() / d_model as f32 + eps).sqrt();

                let mut out_row = result.slice_mut(s![b, s, ..]);
                for (i, w) in weight.iter().enumerate() {
                    out_row[i] = out_row[i] / rms * w;
                }
            }
        }

        Self { data: result }
    }

    /// SiLU activation (used in Mamba)
    pub fn silu(&self) -> Self {
        Self {
            data: self.data.mapv(|x| x * (1.0 / (1.0 + (-x).exp()))),
        }
    }

    /// GELU activation
    pub fn gelu(&self) -> Self {
        Self {
            data: self.data.mapv(|x| {
                0.5 * x * (1.0 + ((2.0_f32 / std::f32::consts::PI).sqrt() * (x + 0.044715 * x.powi(3))).tanh())
            }),
        }
    }

    /// Mean along sequence dimension
    pub fn mean_seq(&self) -> Array2<f32> {
        self.data.mean_axis(Axis(1)).unwrap()
    }

    /// Compute L2 norm for surprise metric
    pub fn l2_norm(&self) -> f32 {
        self.data.iter().map(|x| x * x).sum::<f32>().sqrt()
    }

    /// Transpose last two dimensions (for attention)
    pub fn transpose_last(&self) -> Self {
        let (batch, seq_len, d_model) = self.shape();
        let mut result = Array3::zeros((batch, d_model, seq_len));

        for b in 0..batch {
            for s in 0..seq_len {
                for d in 0..d_model {
                    result[[b, d, s]] = self.data[[b, s, d]];
                }
            }
        }

        Self { data: result }
    }

    /// Slice along sequence dimension
    pub fn slice_seq(&self, start: usize, end: usize) -> Self {
        Self {
            data: self.data.slice(s![.., start..end, ..]).to_owned(),
        }
    }
}

/// Linear layer (weight matrix)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Linear {
    pub weight: Array2<f32>,
    pub bias: Option<Array1<f32>>,
}

impl Linear {
    pub fn new(in_features: usize, out_features: usize, use_bias: bool) -> Self {
        let mut rng = rand::thread_rng();
        let std = (2.0 / (in_features + out_features) as f32).sqrt();
        let normal = Normal::new(0.0, std).unwrap();

        let weight = Array2::from_shape_fn((in_features, out_features), |_| {
            normal.sample(&mut rng)
        });

        let bias = if use_bias {
            Some(Array1::zeros(out_features))
        } else {
            None
        };

        Self { weight, bias }
    }

    pub fn forward(&self, x: &Tensor) -> Tensor {
        let mut result = x.matmul(&self.weight);

        if let Some(ref bias) = self.bias {
            let (batch, seq_len, d_model) = result.shape();
            for b in 0..batch {
                for s in 0..seq_len {
                    for d in 0..d_model {
                        result.data[[b, s, d]] += bias[d];
                    }
                }
            }
        }

        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_creation() {
        let t = Tensor::zeros(2, 4, 8);
        assert_eq!(t.shape(), (2, 4, 8));
    }

    #[test]
    fn test_softmax() {
        let t = Tensor::randn(1, 1, 4);
        let s = t.softmax();
        let sum: f32 = s.data.iter().sum();
        assert!((sum - 1.0).abs() < 1e-5);
    }

    #[test]
    fn test_linear() {
        let linear = Linear::new(8, 16, true);
        let x = Tensor::randn(2, 4, 8);
        let y = linear.forward(&x);
        assert_eq!(y.shape(), (2, 4, 16));
    }
}
