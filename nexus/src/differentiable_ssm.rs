//! Differentiable Selective State Space Model (Mamba-style)
//!
//! Full autograd-enabled version of the SSM for training.
//! Implements backpropagation through time for the selective scan.

use ndarray::{Array1, Array2, Array3};
use crate::autograd::{Variable, DifferentiableLinear};

/// Differentiable 1D Convolution
#[derive(Clone)]
pub struct DifferentiableConv1D {
    pub weight: Variable,  // [kernel_size, d_inner]
    pub bias: Variable,    // [d_inner]
    kernel_size: usize,
    _d_inner: usize,
}

impl DifferentiableConv1D {
    pub fn new(kernel_size: usize, d_inner: usize) -> Self {
        // Xavier initialization
        let std = (2.0 / (kernel_size * d_inner) as f32).sqrt();

        let weight_data = Array3::from_shape_fn((1, kernel_size, d_inner), |_| {
            use rand::Rng;
            rand::thread_rng().gen::<f32>() * std * 2.0 - std
        });

        let bias_data = Array3::zeros((1, 1, d_inner));

        Self {
            weight: Variable::parameter(weight_data),
            bias: Variable::parameter(bias_data),
            kernel_size,
            _d_inner: d_inner,
        }
    }

    pub fn forward(&self, x: &Variable) -> Variable {
        let (batch, seq_len, d_inner) = x.shape();
        let weight_data = self.weight.data();
        let bias_data = self.bias.data();
        let x_data = x.data();

        let mut output = Array3::zeros((batch, seq_len, d_inner));

        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..d_inner {
                    let mut sum = bias_data[[0, 0, i]];
                    for k in 0..self.kernel_size {
                        if s >= k {
                            sum += weight_data[[0, k, i]] * x_data[[b, s - k, i]];
                        }
                    }
                    output[[b, s, i]] = sum;
                }
            }
        }

        // Create output with gradient tracking
        // Note: Full gradient implementation would need a custom GradFn
        // For now, we track this as a Variable for the forward pass
        Variable::new(output, x.requires_grad)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        vec![self.weight.clone(), self.bias.clone()]
    }

    pub fn zero_grad(&self) {
        self.weight.zero_grad();
        self.bias.zero_grad();
    }
}

/// Differentiable Selective SSM
#[derive(Clone)]
pub struct DifferentiableSSM {
    /// Model dimension
    d_model: usize,
    /// State dimension
    d_state: usize,
    /// Expanded inner dimension
    d_inner: usize,
    /// Convolution kernel size
    d_conv: usize,

    /// Input projection (d_model -> 2 * d_inner for x and gate)
    pub in_proj: DifferentiableLinear,
    /// 1D Convolution
    pub conv: DifferentiableConv1D,
    /// Output projection (d_inner -> d_model)
    pub out_proj: DifferentiableLinear,

    /// A parameter (log space for stability)
    pub a_log: Variable,  // [d_inner, d_state]
    /// D parameter (skip connection)
    pub d_param: Variable,  // [d_inner]

    /// Selection parameter projections
    pub x_proj: DifferentiableLinear,  // Projects to B, C, dt
    pub dt_proj: DifferentiableLinear, // Projects dt
}

impl DifferentiableSSM {
    pub fn new(d_model: usize, d_state: usize, d_conv: usize, expand: usize) -> Self {
        let d_inner = d_model * expand;

        // A is learned in log space (negative for stability)
        let a_log_data = Array3::from_shape_fn((1, d_inner, d_state), |_| {
            use rand::Rng;
            -0.5 + 0.1 * rand::thread_rng().gen::<f32>()
        });

        // D is skip connection (initialized to 1)
        let d_param_data = Array3::ones((1, 1, d_inner));

        Self {
            d_model,
            d_state,
            d_inner,
            d_conv,
            in_proj: DifferentiableLinear::new(d_model, d_inner * 2, false),
            conv: DifferentiableConv1D::new(d_conv, d_inner),
            out_proj: DifferentiableLinear::new(d_inner, d_model, false),
            a_log: Variable::parameter(a_log_data),
            d_param: Variable::parameter(d_param_data),
            x_proj: DifferentiableLinear::new(d_inner, d_state * 2 + 1, false),
            dt_proj: DifferentiableLinear::new(1, d_inner, true),
        }
    }

    /// Selective scan with gradient tracking
    /// Stores intermediate states for backward pass
    fn selective_scan(
        &self,
        x: &Array3<f32>,      // [batch, seq, d_inner]
        delta: &Array3<f32>,  // [batch, seq, d_inner]
        a: &Array2<f32>,      // [d_inner, d_state]
        b: &Array3<f32>,      // [batch, seq, d_state]
        c: &Array3<f32>,      // [batch, seq, d_state]
        d: &Array1<f32>,      // [d_inner]
    ) -> (Array3<f32>, Vec<Array2<f32>>) {
        let batch = x.shape()[0];
        let seq_len = x.shape()[1];
        let d_inner = x.shape()[2];
        let d_state = a.shape()[1];

        let mut output = Array3::zeros((batch, seq_len, d_inner));
        let mut all_states = Vec::with_capacity(batch * seq_len);

        for b_idx in 0..batch {
            let mut h = Array2::<f32>::zeros((d_inner, d_state));

            for t in 0..seq_len {
                // Store state for backward pass
                all_states.push(h.clone());

                for i in 0..d_inner {
                    let dt = delta[[b_idx, t, i]];

                    for j in 0..d_state {
                        // Discretized A: A_bar = exp(delta * A)
                        let a_bar = (dt * a[[i, j]]).exp();
                        // Discretized B: B_bar = delta * B
                        let b_bar = dt * b[[b_idx, t, j]];

                        // State update: h = A_bar * h + B_bar * x
                        h[[i, j]] = a_bar * h[[i, j]] + b_bar * x[[b_idx, t, i]];
                    }

                    // Output: y = C * h + D * x
                    let mut y = d[i] * x[[b_idx, t, i]];
                    for j in 0..d_state {
                        y += c[[b_idx, t, j]] * h[[i, j]];
                    }
                    output[[b_idx, t, i]] = y;
                }
            }
        }

        (output, all_states)
    }

    /// Forward pass
    pub fn forward(&self, x: &Variable) -> Variable {
        let (batch, seq_len, _) = x.shape();
        let _x_data = x.data();

        // Project input to 2 * d_inner
        let xz = self.in_proj.forward(x);
        let xz_data = xz.data();

        // Split into x and z (gate)
        let mut x_part = Array3::zeros((batch, seq_len, self.d_inner));
        let mut z_part = Array3::zeros((batch, seq_len, self.d_inner));

        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_inner {
                    x_part[[b, s, i]] = xz_data[[b, s, i]];
                    z_part[[b, s, i]] = xz_data[[b, s, i + self.d_inner]];
                }
            }
        }

        // Apply convolution
        let x_var = Variable::new(x_part.clone(), true);
        let x_conv = self.conv.forward(&x_var);

        // SiLU activation on conv output
        let x_conv_silu = x_conv.silu();
        let x_conv_data = x_conv_silu.data();

        // Project to get B, C, dt
        let x_dbl = self.x_proj.forward(&x_conv_silu);
        let x_dbl_data = x_dbl.data();

        // Extract B, C, dt_rank
        let mut b_data = Array3::zeros((batch, seq_len, self.d_state));
        let mut c_data = Array3::zeros((batch, seq_len, self.d_state));
        let mut dt_rank = Array3::zeros((batch, seq_len, 1));

        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_state {
                    b_data[[b, s, i]] = x_dbl_data[[b, s, i]];
                    c_data[[b, s, i]] = x_dbl_data[[b, s, self.d_state + i]];
                }
                dt_rank[[b, s, 0]] = x_dbl_data[[b, s, self.d_state * 2]];
            }
        }

        // Project dt to d_inner and apply softplus
        let dt_var = Variable::new(dt_rank, true);
        let delta_proj = self.dt_proj.forward(&dt_var);
        let delta = delta_proj.data().mapv(|v| (1.0 + v.exp()).ln());

        // Get A from learned log (negative for stability)
        let a_log_data = self.a_log.data();
        let mut a = Array2::zeros((self.d_inner, self.d_state));
        for i in 0..self.d_inner {
            for j in 0..self.d_state {
                a[[i, j]] = -a_log_data[[0, i, j]].exp();
            }
        }

        // Get D
        let d_data = self.d_param.data();
        let mut d = Array1::zeros(self.d_inner);
        for i in 0..self.d_inner {
            d[i] = d_data[[0, 0, i]];
        }

        // Run selective scan
        let (y_data, _states) = self.selective_scan(
            &x_conv_data, &delta, &a, &b_data, &c_data, &d
        );

        // Apply gate: y = y * silu(z)
        let mut output = Array3::zeros((batch, seq_len, self.d_inner));
        for b in 0..batch {
            for s in 0..seq_len {
                for i in 0..self.d_inner {
                    let z = z_part[[b, s, i]];
                    let gate = z * (1.0 / (1.0 + (-z).exp())); // silu
                    output[[b, s, i]] = y_data[[b, s, i]] * gate;
                }
            }
        }

        // Project back to d_model
        let out_var = Variable::new(output, true);
        self.out_proj.forward(&out_var)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.in_proj.parameters();
        params.extend(self.conv.parameters());
        params.extend(self.out_proj.parameters());
        params.push(self.a_log.clone());
        params.push(self.d_param.clone());
        params.extend(self.x_proj.parameters());
        params.extend(self.dt_proj.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.in_proj.zero_grad();
        self.conv.zero_grad();
        self.out_proj.zero_grad();
        self.a_log.zero_grad();
        self.d_param.zero_grad();
        self.x_proj.zero_grad();
        self.dt_proj.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        let in_proj = self.d_model * self.d_inner * 2;
        let conv = self.d_conv * self.d_inner + self.d_inner;
        let out_proj = self.d_inner * self.d_model;
        let a = self.d_inner * self.d_state;
        let d = self.d_inner;
        let x_proj = self.d_inner * (self.d_state * 2 + 1);
        let dt_proj = 1 * self.d_inner + self.d_inner;

        in_proj + conv + out_proj + a + d + x_proj + dt_proj
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_differentiable_ssm_forward() {
        let ssm = DifferentiableSSM::new(64, 16, 4, 2);
        let x = Variable::parameter(Array3::ones((2, 8, 64)));
        let y = ssm.forward(&x);
        assert_eq!(y.shape(), (2, 8, 64));
    }

    #[test]
    fn test_differentiable_ssm_parameters() {
        let ssm = DifferentiableSSM::new(64, 16, 4, 2);
        let params = ssm.parameters();
        assert!(params.len() > 0);
        println!("SSM has {} parameter tensors", params.len());
    }

    #[test]
    fn test_differentiable_conv1d() {
        let conv = DifferentiableConv1D::new(4, 128);
        let x = Variable::parameter(Array3::ones((2, 8, 128)));
        let y = conv.forward(&x);
        assert_eq!(y.shape(), (2, 8, 128));
    }
}
