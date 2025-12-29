//! Automatic Differentiation (Autograd) System
//!
//! Tape-based reverse-mode autodiff for training Nexus models.
//! Records operations in a computational graph and computes gradients via backprop.

use ndarray::{Array1, Array2, Array3, Axis};
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;
use std::sync::atomic::{AtomicUsize, Ordering};

/// Global counter for unique tensor IDs
static TENSOR_ID: AtomicUsize = AtomicUsize::new(0);

/// Generate unique tensor ID
fn next_tensor_id() -> usize {
    TENSOR_ID.fetch_add(1, Ordering::SeqCst)
}

/// A tensor with gradient tracking
#[derive(Clone)]
pub struct Variable {
    /// Unique identifier
    pub id: usize,
    /// The actual data
    pub data: Array3<f32>,
    /// Gradient (computed during backward pass)
    pub grad: RefCell<Option<Array3<f32>>>,
    /// Whether this variable requires gradient
    pub requires_grad: bool,
    /// Operation that created this variable (for backprop)
    creator: Option<Rc<dyn GradFn>>,
}

impl Variable {
    /// Create a new variable with gradient tracking
    pub fn new(data: Array3<f32>, requires_grad: bool) -> Self {
        Self {
            id: next_tensor_id(),
            data,
            grad: RefCell::new(None),
            requires_grad,
            creator: None,
        }
    }

    /// Create a variable from raw data without gradient
    pub fn from_data(data: Array3<f32>) -> Self {
        Self::new(data, false)
    }

    /// Create a parameter (requires gradient by default)
    pub fn parameter(data: Array3<f32>) -> Self {
        Self::new(data, true)
    }

    /// Get shape
    pub fn shape(&self) -> (usize, usize, usize) {
        let s = self.data.shape();
        (s[0], s[1], s[2])
    }

    /// Zero out gradients
    pub fn zero_grad(&self) {
        *self.grad.borrow_mut() = None;
    }

    /// Accumulate gradient
    pub fn accumulate_grad(&self, grad: Array3<f32>) {
        let mut current = self.grad.borrow_mut();
        match &mut *current {
            Some(existing) => {
                *existing = &*existing + &grad;
            }
            None => {
                *current = Some(grad);
            }
        }
    }

    /// Get gradient value
    pub fn get_grad(&self) -> Option<Array3<f32>> {
        self.grad.borrow().clone()
    }

    /// Set the creator function
    fn with_creator(mut self, creator: Rc<dyn GradFn>) -> Self {
        self.creator = Some(creator);
        self
    }

    /// Backward pass - compute gradients
    pub fn backward(&self) {
        if !self.requires_grad {
            return;
        }

        // Initialize gradient for output (ones)
        let grad = Array3::ones(self.data.raw_dim());
        self.accumulate_grad(grad.clone());

        // Build topological order
        let mut topo = Vec::new();
        let mut visited = std::collections::HashSet::new();
        self.build_topo(&mut topo, &mut visited);

        // Backpropagate in reverse order
        for var in topo.iter().rev() {
            if let Some(ref creator) = var.creator {
                let grad = var.grad.borrow().clone().unwrap_or_else(|| {
                    Array3::zeros(var.data.raw_dim())
                });
                creator.backward(&grad);
            }
        }
    }

    fn build_topo(&self, topo: &mut Vec<Variable>, visited: &mut std::collections::HashSet<usize>) {
        if visited.contains(&self.id) {
            return;
        }
        visited.insert(self.id);

        if let Some(ref creator) = self.creator {
            for input in creator.inputs() {
                input.build_topo(topo, visited);
            }
        }

        topo.push(self.clone());
    }
}

/// Trait for gradient functions (operations that can be backpropagated through)
pub trait GradFn {
    /// Compute gradients for inputs given output gradient
    fn backward(&self, grad_output: &Array3<f32>);
    /// Get input variables for topological sort
    fn inputs(&self) -> Vec<Variable>;
}

/// Addition gradient function
struct AddGradFn {
    a: Variable,
    b: Variable,
}

impl GradFn for AddGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.a.requires_grad {
            self.a.accumulate_grad(grad_output.clone());
        }
        if self.b.requires_grad {
            self.b.accumulate_grad(grad_output.clone());
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.a.clone(), self.b.clone()]
    }
}

/// Multiplication gradient function
struct MulGradFn {
    a: Variable,
    b: Variable,
}

impl GradFn for MulGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.a.requires_grad {
            let grad_a = grad_output * &self.b.data;
            self.a.accumulate_grad(grad_a);
        }
        if self.b.requires_grad {
            let grad_b = grad_output * &self.a.data;
            self.b.accumulate_grad(grad_b);
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.a.clone(), self.b.clone()]
    }
}

/// Matrix multiplication gradient function
struct MatMulGradFn {
    input: Variable,
    weight: Array2<f32>,
}

impl GradFn for MatMulGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.input.requires_grad {
            // grad_input = grad_output @ weight.T
            let (batch, seq_len, _) = grad_output.dim();
            let d_in = self.weight.shape()[0];
            let mut grad_input = Array3::zeros((batch, seq_len, d_in));

            for b in 0..batch {
                for s in 0..seq_len {
                    for i in 0..d_in {
                        let mut sum = 0.0f32;
                        for j in 0..self.weight.shape()[1] {
                            sum += grad_output[[b, s, j]] * self.weight[[i, j]];
                        }
                        grad_input[[b, s, i]] = sum;
                    }
                }
            }

            self.input.accumulate_grad(grad_input);
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.input.clone()]
    }
}

/// GELU gradient function
struct GELUGradFn {
    input: Variable,
}

impl GradFn for GELUGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.input.requires_grad {
            // GELU'(x) ≈ 0.5 * (1 + tanh(sqrt(2/π) * (x + 0.044715 * x³))) +
            //            0.5 * x * sech²(...) * sqrt(2/π) * (1 + 3 * 0.044715 * x²)
            // Simplified approximation
            let grad = self.input.data.mapv(|x| {
                let sqrt_2_pi = (2.0_f32 / std::f32::consts::PI).sqrt();
                let inner = sqrt_2_pi * (x + 0.044715 * x.powi(3));
                let tanh_inner = inner.tanh();
                let sech2 = 1.0 - tanh_inner.powi(2);

                0.5 * (1.0 + tanh_inner) +
                0.5 * x * sech2 * sqrt_2_pi * (1.0 + 3.0 * 0.044715 * x.powi(2))
            });

            self.input.accumulate_grad(&grad * grad_output);
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.input.clone()]
    }
}

/// SiLU gradient function
struct SiLUGradFn {
    input: Variable,
}

impl GradFn for SiLUGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.input.requires_grad {
            // SiLU'(x) = σ(x) + x * σ(x) * (1 - σ(x)) = σ(x) * (1 + x * (1 - σ(x)))
            let grad = self.input.data.mapv(|x| {
                let sigmoid = 1.0 / (1.0 + (-x).exp());
                sigmoid * (1.0 + x * (1.0 - sigmoid))
            });

            self.input.accumulate_grad(&grad * grad_output);
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.input.clone()]
    }
}

/// Softmax gradient function
struct SoftmaxGradFn {
    input: Variable,
    output: Array3<f32>,
}

impl GradFn for SoftmaxGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.input.requires_grad {
            let (batch, seq_len, d_model) = self.output.dim();
            let mut grad_input = Array3::zeros((batch, seq_len, d_model));

            for b in 0..batch {
                for s in 0..seq_len {
                    // Jacobian of softmax: diag(y) - y @ y.T
                    // grad = y * (grad_out - sum(y * grad_out))
                    let mut sum = 0.0f32;
                    for d in 0..d_model {
                        sum += self.output[[b, s, d]] * grad_output[[b, s, d]];
                    }
                    for d in 0..d_model {
                        grad_input[[b, s, d]] = self.output[[b, s, d]] * (grad_output[[b, s, d]] - sum);
                    }
                }
            }

            self.input.accumulate_grad(grad_input);
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.input.clone()]
    }
}

/// Mean Squared Error gradient function
struct MSEGradFn {
    pred: Variable,
    target: Array3<f32>,
}

impl GradFn for MSEGradFn {
    fn backward(&self, grad_output: &Array3<f32>) {
        if self.pred.requires_grad {
            let n = self.pred.data.len() as f32;
            let grad = (&self.pred.data - &self.target).mapv(|x| 2.0 * x / n);
            self.pred.accumulate_grad(&grad * grad_output);
        }
    }

    fn inputs(&self) -> Vec<Variable> {
        vec![self.pred.clone()]
    }
}

// ============ Operations ============

impl Variable {
    /// Element-wise addition
    pub fn add(&self, other: &Variable) -> Variable {
        let result_data = &self.data + &other.data;
        let requires_grad = self.requires_grad || other.requires_grad;

        let mut result = Variable::new(result_data, requires_grad);
        if requires_grad {
            result = result.with_creator(Rc::new(AddGradFn {
                a: self.clone(),
                b: other.clone(),
            }));
        }
        result
    }

    /// Element-wise multiplication
    pub fn mul(&self, other: &Variable) -> Variable {
        let result_data = &self.data * &other.data;
        let requires_grad = self.requires_grad || other.requires_grad;

        let mut result = Variable::new(result_data, requires_grad);
        if requires_grad {
            result = result.with_creator(Rc::new(MulGradFn {
                a: self.clone(),
                b: other.clone(),
            }));
        }
        result
    }

    /// Matrix multiplication with 2D weight
    pub fn matmul(&self, weight: &Array2<f32>) -> Variable {
        let (batch, seq_len, _) = self.shape();
        let d_out = weight.shape()[1];

        let mut result_data = Array3::zeros((batch, seq_len, d_out));
        for b in 0..batch {
            for s in 0..seq_len {
                for j in 0..d_out {
                    let mut sum = 0.0f32;
                    for i in 0..weight.shape()[0] {
                        sum += self.data[[b, s, i]] * weight[[i, j]];
                    }
                    result_data[[b, s, j]] = sum;
                }
            }
        }

        let mut result = Variable::new(result_data, self.requires_grad);
        if self.requires_grad {
            result = result.with_creator(Rc::new(MatMulGradFn {
                input: self.clone(),
                weight: weight.clone(),
            }));
        }
        result
    }

    /// GELU activation
    pub fn gelu(&self) -> Variable {
        let result_data = self.data.mapv(|x| {
            0.5 * x * (1.0 + ((2.0_f32 / std::f32::consts::PI).sqrt() *
                (x + 0.044715 * x.powi(3))).tanh())
        });

        let mut result = Variable::new(result_data, self.requires_grad);
        if self.requires_grad {
            result = result.with_creator(Rc::new(GELUGradFn {
                input: self.clone(),
            }));
        }
        result
    }

    /// SiLU activation
    pub fn silu(&self) -> Variable {
        let result_data = self.data.mapv(|x| x * (1.0 / (1.0 + (-x).exp())));

        let mut result = Variable::new(result_data, self.requires_grad);
        if self.requires_grad {
            result = result.with_creator(Rc::new(SiLUGradFn {
                input: self.clone(),
            }));
        }
        result
    }

    /// Softmax along last dimension
    pub fn softmax(&self) -> Variable {
        let (batch, seq_len, d_model) = self.shape();
        let mut result_data = self.data.clone();

        for b in 0..batch {
            for s in 0..seq_len {
                let max = (0..d_model)
                    .map(|d| result_data[[b, s, d]])
                    .fold(f32::NEG_INFINITY, f32::max);

                let mut sum = 0.0f32;
                for d in 0..d_model {
                    result_data[[b, s, d]] = (result_data[[b, s, d]] - max).exp();
                    sum += result_data[[b, s, d]];
                }
                for d in 0..d_model {
                    result_data[[b, s, d]] /= sum;
                }
            }
        }

        let mut result = Variable::new(result_data.clone(), self.requires_grad);
        if self.requires_grad {
            result = result.with_creator(Rc::new(SoftmaxGradFn {
                input: self.clone(),
                output: result_data,
            }));
        }
        result
    }

    /// Scale by scalar
    pub fn scale(&self, s: f32) -> Variable {
        let result_data = &self.data * s;
        Variable::new(result_data, self.requires_grad)
    }

    /// Mean squared error loss
    pub fn mse_loss(&self, target: &Array3<f32>) -> (f32, Variable) {
        let diff = &self.data - target;
        let loss = diff.iter().map(|x| x * x).sum::<f32>() / self.data.len() as f32;

        let mut result = Variable::new(Array3::from_elem((1, 1, 1), loss), self.requires_grad);
        if self.requires_grad {
            result = result.with_creator(Rc::new(MSEGradFn {
                pred: self.clone(),
                target: target.clone(),
            }));
        }

        (loss, result)
    }
}

/// Parameter container for a layer
#[derive(Clone)]
pub struct Parameter {
    pub data: Variable,
    pub name: String,
}

impl Parameter {
    pub fn new(name: &str, shape: (usize, usize, usize)) -> Self {
        // Xavier initialization
        let (_, _, d) = shape;
        let std = (2.0 / d as f32).sqrt();
        let normal = rand_distr::Normal::new(0.0, std).unwrap();

        use rand::prelude::*;
        let mut rng = rand::thread_rng();
        let data = Array3::from_shape_fn(shape, |_| {
            use rand_distr::Distribution;
            normal.sample(&mut rng)
        });

        Self {
            data: Variable::parameter(data),
            name: name.to_string(),
        }
    }

    pub fn zero_grad(&self) {
        self.data.zero_grad();
    }

    pub fn get_grad(&self) -> Option<Array3<f32>> {
        self.data.get_grad()
    }
}

/// Optimizer trait
pub trait Optimizer {
    fn step(&mut self, params: &[Parameter]);
    fn zero_grad(&self, params: &[Parameter]) {
        for p in params {
            p.zero_grad();
        }
    }
}

/// SGD Optimizer with momentum
pub struct SGD {
    lr: f32,
    momentum: f32,
    velocities: HashMap<usize, Array3<f32>>,
}

impl SGD {
    pub fn new(lr: f32, momentum: f32) -> Self {
        Self {
            lr,
            momentum,
            velocities: HashMap::new(),
        }
    }
}

impl Optimizer for SGD {
    fn step(&mut self, params: &[Parameter]) {
        for param in params {
            if let Some(grad) = param.get_grad() {
                let id = param.data.id;

                // Get or create velocity
                let velocity = self.velocities
                    .entry(id)
                    .or_insert_with(|| Array3::zeros(grad.raw_dim()));

                // Update velocity: v = momentum * v + grad
                *velocity = &*velocity * self.momentum + &grad;

                // Update parameter: p = p - lr * v
                // Note: We can't modify data directly, so we'd need mutable access
                // In practice, you'd need interior mutability here
            }
        }
    }
}

/// AdamW Optimizer
pub struct AdamW {
    lr: f32,
    beta1: f32,
    beta2: f32,
    eps: f32,
    weight_decay: f32,
    step_count: usize,
    m: HashMap<usize, Array3<f32>>,  // First moment
    v: HashMap<usize, Array3<f32>>,  // Second moment
}

impl AdamW {
    pub fn new(lr: f32, weight_decay: f32) -> Self {
        Self {
            lr,
            beta1: 0.9,
            beta2: 0.999,
            eps: 1e-8,
            weight_decay,
            step_count: 0,
            m: HashMap::new(),
            v: HashMap::new(),
        }
    }

    /// Get the update for a parameter (returns the delta to subtract)
    pub fn get_update(&mut self, param_id: usize, grad: &Array3<f32>, data: &Array3<f32>) -> Array3<f32> {
        self.step_count += 1;
        let t = self.step_count as f32;

        // Get or create moments
        let m = self.m.entry(param_id).or_insert_with(|| Array3::zeros(grad.raw_dim()));
        let v = self.v.entry(param_id).or_insert_with(|| Array3::zeros(grad.raw_dim()));

        // Update moments
        *m = &*m * self.beta1 + grad * (1.0 - self.beta1);
        *v = &*v * self.beta2 + &grad.mapv(|x| x * x) * (1.0 - self.beta2);

        // Bias correction
        let m_hat = m.mapv(|x| x / (1.0 - self.beta1.powf(t)));
        let v_hat = v.mapv(|x| x / (1.0 - self.beta2.powf(t)));

        // Compute update
        let update = &m_hat / &v_hat.mapv(|x| x.sqrt() + self.eps);

        // Add weight decay
        &update * self.lr + data * (self.lr * self.weight_decay)
    }
}

impl Optimizer for AdamW {
    fn step(&mut self, params: &[Parameter]) {
        // Note: This is a simplified version. In practice, you'd need
        // to actually update the parameter data, which requires
        // interior mutability or a different architecture.
        for param in params {
            if let Some(_grad) = param.get_grad() {
                // Would update param.data here
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_variable_creation() {
        let data = Array3::zeros((2, 4, 8));
        let var = Variable::new(data, true);
        assert!(var.requires_grad);
        assert_eq!(var.shape(), (2, 4, 8));
    }

    #[test]
    fn test_add_backward() {
        let a = Variable::parameter(Array3::ones((1, 1, 4)));
        let b = Variable::parameter(Array3::ones((1, 1, 4)) * 2.0);
        let c = a.add(&b);

        assert_eq!(c.data[[0, 0, 0]], 3.0);

        c.backward();

        let grad_a = a.get_grad().unwrap();
        let grad_b = b.get_grad().unwrap();

        assert_eq!(grad_a[[0, 0, 0]], 1.0);
        assert_eq!(grad_b[[0, 0, 0]], 1.0);
    }

    #[test]
    fn test_mul_backward() {
        let a = Variable::parameter(Array3::ones((1, 1, 4)) * 3.0);
        let b = Variable::parameter(Array3::ones((1, 1, 4)) * 4.0);
        let c = a.mul(&b);

        assert_eq!(c.data[[0, 0, 0]], 12.0);

        c.backward();

        let grad_a = a.get_grad().unwrap();
        let grad_b = b.get_grad().unwrap();

        // d/da (a * b) = b = 4
        assert_eq!(grad_a[[0, 0, 0]], 4.0);
        // d/db (a * b) = a = 3
        assert_eq!(grad_b[[0, 0, 0]], 3.0);
    }

    #[test]
    fn test_chain_backward() {
        let a = Variable::parameter(Array3::ones((1, 1, 4)) * 2.0);
        let b = Variable::parameter(Array3::ones((1, 1, 4)) * 3.0);
        let c = a.add(&b);   // c = a + b = 5
        let d = c.mul(&b);   // d = c * b = 5 * 3 = 15

        d.backward();

        // d(d)/da = d(c*b)/da = b * dc/da = 3 * 1 = 3
        let grad_a = a.get_grad().unwrap();
        assert_eq!(grad_a[[0, 0, 0]], 3.0);

        // d(d)/db = d(c*b)/db = c + b * dc/db = 5 + 3 * 1 = 8
        let grad_b = b.get_grad().unwrap();
        assert_eq!(grad_b[[0, 0, 0]], 8.0);
    }

    #[test]
    fn test_mse_loss() {
        let pred = Variable::parameter(Array3::ones((1, 1, 4)) * 2.0);
        let target = Array3::ones((1, 1, 4)) * 3.0;

        let (loss, loss_var) = pred.mse_loss(&target);
        assert!((loss - 1.0).abs() < 1e-6);  // (2-3)^2 = 1

        loss_var.backward();
        let grad = pred.get_grad().unwrap();
        // d/dx (x-t)^2 / n = 2(x-t)/n = 2(-1)/4 = -0.5
        assert!((grad[[0, 0, 0]] - (-0.5)).abs() < 1e-6);
    }
}
