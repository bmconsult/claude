//! Selective State Space Model (Mamba-style)
//!
//! Implements the SSM used in the majority (7:1 ratio) of layers.
//! Key insight: Input-dependent selection of which information to propagate.

use ndarray::{Array1, Array2, Array3};
use serde::{Serialize, Deserialize};
use crate::tensor::{Tensor, Linear};

/// Selective State Space Model
///
/// The core of Mamba: makes the SSM parameters input-dependent,
/// allowing the model to selectively propagate or forget information.
#[derive(Clone, Serialize, Deserialize)]
pub struct SelectiveSSM {
    /// Model dimension
    d_model: usize,
    /// State dimension
    d_state: usize,
    /// Expanded inner dimension
    d_inner: usize,
    /// Convolution width
    d_conv: usize,

    /// Input projection (expands dimension)
    in_proj: Linear,
    /// Convolution weights
    conv_weight: Array2<f32>,
    /// Convolution bias
    conv_bias: Array1<f32>,
    /// Output projection
    out_proj: Linear,

    /// Selection parameters (B, C, dt come from input)
    /// A is learned but not input-dependent (for stability)
    a_log: Array2<f32>,  // [d_inner, d_state] - learned log of A
    d: Array1<f32>,       // [d_inner] - skip connection

    /// Projections for selection mechanism
    x_proj: Linear,  // Projects to (dt, B, C)
    dt_proj: Linear, // Projects dt
}

impl SelectiveSSM {
    pub fn new(d_model: usize, d_state: usize, d_conv: usize, expand: usize) -> Self {
        let d_inner = d_model * expand;

        // Initialize A_log to make A close to identity initially
        let a_log = Array2::from_shape_fn((d_inner, d_state), |_| {
            -0.5 + 0.1 * rand::random::<f32>()
        });

        // Skip connection parameter
        let d = Array1::ones(d_inner);

        // Convolution for local context
        let conv_weight = Array2::from_shape_fn((d_conv, d_inner), |_| {
            0.1 * rand::random::<f32>()
        });
        let conv_bias = Array1::zeros(d_inner);

        Self {
            d_model,
            d_state,
            d_inner,
            d_conv,
            in_proj: Linear::new(d_model, d_inner * 2, false),
            conv_weight,
            conv_bias,
            out_proj: Linear::new(d_inner, d_model, false),
            a_log,
            d,
            x_proj: Linear::new(d_inner, d_state * 2 + 1, false),  // B, C, dt_rank
            dt_proj: Linear::new(1, d_inner, true),
        }
    }

    /// Selective scan operation
    /// The core of Mamba: recurrence with input-dependent parameters
    fn selective_scan(
        &self,
        x: &Array3<f32>,        // [batch, seq, d_inner]
        delta: &Array3<f32>,    // [batch, seq, d_inner]
        a: &Array2<f32>,        // [d_inner, d_state]
        b: &Array3<f32>,        // [batch, seq, d_state]
        c: &Array3<f32>,        // [batch, seq, d_state]
    ) -> Array3<f32> {
        let batch = x.shape()[0];
        let seq_len = x.shape()[1];
        let d_inner = x.shape()[2];
        let d_state = a.shape()[1];

        let mut output = Array3::zeros((batch, seq_len, d_inner));

        for b_idx in 0..batch {
            // State for this sequence
            let mut h = Array2::<f32>::zeros((d_inner, d_state));

            for t in 0..seq_len {
                // Discretize A and B using delta (timestep)
                // A_bar = exp(delta * A)
                // B_bar = delta * B

                for i in 0..d_inner {
                    let dt = delta[[b_idx, t, i]];

                    for j in 0..d_state {
                        // Discretized A (using zero-order hold)
                        let a_bar = (dt * a[[i, j]]).exp();

                        // Discretized B
                        let b_bar = dt * b[[b_idx, t, j]];

                        // State update: h = A_bar * h + B_bar * x
                        h[[i, j]] = a_bar * h[[i, j]] + b_bar * x[[b_idx, t, i]];
                    }

                    // Output: y = C * h + D * x
                    let mut y = self.d[i] * x[[b_idx, t, i]];
                    for j in 0..d_state {
                        y += c[[b_idx, t, j]] * h[[i, j]];
                    }
                    output[[b_idx, t, i]] = y;
                }
            }
        }

        output
    }

    /// Forward pass
    pub fn forward(&self, x: &Tensor) -> Tensor {
        let (batch, seq_len, _) = x.shape();

        // Project input to 2 * d_inner (for gated activation)
        let xz = self.in_proj.forward(x);

        // Split into x and z (gate)
        let mut x_data = Array3::zeros((batch, seq_len, self.d_inner));
        let mut z_data = Array3::zeros((batch, seq_len, self.d_inner));

        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_inner {
                    x_data[[b, s, i]] = xz.data[[b, s, i]];
                    z_data[[b, s, i]] = xz.data[[b, s, i + self.d_inner]];
                }
            }
        }

        // Apply 1D convolution for local context
        let mut x_conv = Array3::zeros((batch, seq_len, self.d_inner));
        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_inner {
                    let mut sum = self.conv_bias[i];
                    for k in 0..self.d_conv {
                        if s >= k {
                            sum += self.conv_weight[[k, i]] * x_data[[b, s - k, i]];
                        }
                    }
                    x_conv[[b, s, i]] = sum;
                }
            }
        }

        // SiLU activation
        x_conv.mapv_inplace(|v| v * (1.0 / (1.0 + (-v).exp())));

        // Project to get selection parameters (B, C, dt)
        let x_tensor = Tensor { data: x_conv.clone() };
        let x_dbl = self.x_proj.forward(&x_tensor);

        // Extract B, C, and dt_rank from projection
        let mut b_data = Array3::zeros((batch, seq_len, self.d_state));
        let mut c_data = Array3::zeros((batch, seq_len, self.d_state));
        let mut dt_rank = Array3::zeros((batch, seq_len, 1));

        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_state {
                    b_data[[b, s, i]] = x_dbl.data[[b, s, i]];
                    c_data[[b, s, i]] = x_dbl.data[[b, s, self.d_state + i]];
                }
                dt_rank[[b, s, 0]] = x_dbl.data[[b, s, self.d_state * 2]];
            }
        }

        // Project dt to d_inner and apply softplus
        let dt_tensor = Tensor { data: dt_rank };
        let delta_proj = self.dt_proj.forward(&dt_tensor);
        let delta = delta_proj.data.mapv(|v| (1.0 + v.exp()).ln()); // softplus

        // Get A from learned log
        let a = self.a_log.mapv(|v| -v.exp()); // A is negative for stability

        // Run selective scan
        let y_data = self.selective_scan(&x_conv, &delta, &a, &b_data, &c_data);

        // Apply gate: y = y * silu(z)
        let mut output = Array3::zeros((batch, seq_len, self.d_inner));
        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_inner {
                    let z = z_data[[b, s, i]];
                    let gate = z * (1.0 / (1.0 + (-z).exp())); // silu
                    output[[b, s, i]] = y_data[[b, s, i]] * gate;
                }
            }
        }

        // Project back to model dimension
        let out_tensor = Tensor { data: output };
        self.out_proj.forward(&out_tensor)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ssm_shape() {
        let ssm = SelectiveSSM::new(64, 16, 4, 2);
        let x = Tensor::randn(2, 8, 64);
        let y = ssm.forward(&x);
        assert_eq!(y.shape(), (2, 8, 64));
    }
}
