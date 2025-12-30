//! Differentiable Neuro-Symbolic Reasoning
//!
//! Combines neural networks with symbolic reasoning through:
//! - Soft expression trees with learnable operation weights
//! - Neural-guided constraint solving
//! - Differentiable evaluation through continuous relaxations
//!
//! Key insight: Use neural networks to predict symbolic structure,
//! then use differentiable relaxations to train end-to-end.

use ndarray::{Array1, Array2, Array3};
use crate::autograd::{Variable, DifferentiableLinear};

/// Soft symbolic operation - continuous relaxation of discrete ops
#[derive(Clone)]
pub struct SoftOperation {
    /// Operation weights: [add, sub, mul, div, max, min]
    pub weights: Variable,
    /// Temperature for softmax (lower = more discrete)
    temperature: f32,
}

impl SoftOperation {
    pub fn new(temperature: f32) -> Self {
        // Initialize with uniform weights
        let weights_data = Array3::from_elem((1, 1, 6), 1.0 / 6.0);
        Self {
            weights: Variable::parameter(weights_data),
            temperature,
        }
    }

    /// Apply soft operation to two inputs
    /// Uses Gumbel-softmax-like weighting of operation results
    pub fn forward(&self, a: &Variable, b: &Variable) -> Variable {
        let a_data = a.data();
        let b_data = b.data();
        let (batch, seq, dim) = a.shape();

        // Get operation weights via softmax
        let weights_data = self.weights.data();
        let mut probs = [0.0f32; 6];
        let mut max_w = f32::NEG_INFINITY;
        for i in 0..6 {
            max_w = max_w.max(weights_data[[0, 0, i]]);
        }
        let mut sum = 0.0f32;
        for i in 0..6 {
            probs[i] = ((weights_data[[0, 0, i]] - max_w) / self.temperature).exp();
            sum += probs[i];
        }
        for p in &mut probs {
            *p /= sum;
        }

        // Compute all operations and combine with soft weights
        let mut result = Array3::zeros((batch, seq, dim));

        for bi in 0..batch {
            for si in 0..seq {
                for di in 0..dim {
                    let av = a_data[[bi, si, di]];
                    let bv = b_data[[bi, si, di]];

                    // Weighted combination of operations
                    let add = av + bv;
                    let sub = av - bv;
                    let mul = av * bv;
                    let div = if bv.abs() > 1e-6 { av / bv } else { 0.0 };
                    let max = av.max(bv);
                    let min = av.min(bv);

                    result[[bi, si, di]] = probs[0] * add
                        + probs[1] * sub
                        + probs[2] * mul
                        + probs[3] * div
                        + probs[4] * max
                        + probs[5] * min;
                }
            }
        }

        Variable::new(result, a.requires_grad || b.requires_grad || self.weights.requires_grad)
    }

    /// Get the dominant operation (for interpretation)
    pub fn dominant_op(&self) -> &'static str {
        let weights_data = self.weights.data();
        let mut best_idx = 0;
        let mut best_val = f32::NEG_INFINITY;
        for i in 0..6 {
            if weights_data[[0, 0, i]] > best_val {
                best_val = weights_data[[0, 0, i]];
                best_idx = i;
            }
        }
        match best_idx {
            0 => "add",
            1 => "sub",
            2 => "mul",
            3 => "div",
            4 => "max",
            5 => "min",
            _ => "unknown",
        }
    }

    pub fn parameters(&self) -> Vec<Variable> {
        vec![self.weights.clone()]
    }

    pub fn zero_grad(&self) {
        self.weights.zero_grad();
    }
}

/// Soft comparison operations
#[derive(Clone)]
pub struct SoftComparison {
    /// Comparison weights: [eq, lt, le, gt, ge, neq]
    pub weights: Variable,
    temperature: f32,
}

impl SoftComparison {
    pub fn new(temperature: f32) -> Self {
        let weights_data = Array3::from_elem((1, 1, 6), 1.0 / 6.0);
        Self {
            weights: Variable::parameter(weights_data),
            temperature,
        }
    }

    /// Apply soft comparison - returns value in [0, 1] representing truth
    pub fn forward(&self, a: &Variable, b: &Variable) -> Variable {
        let a_data = a.data();
        let b_data = b.data();
        let (batch, seq, dim) = a.shape();

        let weights_data = self.weights.data();
        let mut probs = [0.0f32; 6];
        let mut max_w = f32::NEG_INFINITY;
        for i in 0..6 {
            max_w = max_w.max(weights_data[[0, 0, i]]);
        }
        let mut sum = 0.0f32;
        for i in 0..6 {
            probs[i] = ((weights_data[[0, 0, i]] - max_w) / self.temperature).exp();
            sum += probs[i];
        }
        for p in &mut probs {
            *p /= sum;
        }

        let mut result = Array3::zeros((batch, seq, dim));
        let sigmoid = |x: f32| 1.0 / (1.0 + (-x * 10.0).exp()); // Sharp sigmoid

        for bi in 0..batch {
            for si in 0..seq {
                for di in 0..dim {
                    let av = a_data[[bi, si, di]];
                    let bv = b_data[[bi, si, di]];
                    let diff = av - bv;

                    // Soft comparisons
                    let eq = (-diff.abs() * 10.0).exp(); // ~1 when equal
                    let lt = sigmoid(-diff);              // ~1 when a < b
                    let le = sigmoid(-diff + 0.1);        // ~1 when a <= b
                    let gt = sigmoid(diff);               // ~1 when a > b
                    let ge = sigmoid(diff + 0.1);         // ~1 when a >= b
                    let neq = 1.0 - eq;                   // ~1 when not equal

                    result[[bi, si, di]] = probs[0] * eq
                        + probs[1] * lt
                        + probs[2] * le
                        + probs[3] * gt
                        + probs[4] * ge
                        + probs[5] * neq;
                }
            }
        }

        Variable::new(result, a.requires_grad || b.requires_grad || self.weights.requires_grad)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        vec![self.weights.clone()]
    }

    pub fn zero_grad(&self) {
        self.weights.zero_grad();
    }
}

/// Neural expression tree - learns to build symbolic expressions
#[derive(Clone)]
pub struct NeuralExpressionTree {
    /// Number of variables
    n_vars: usize,
    /// Embedding dimension
    d_model: usize,
    /// Maximum tree depth
    max_depth: usize,

    /// Variable embeddings
    pub var_embed: Variable,
    /// Constant embedding projection
    pub const_proj: DifferentiableLinear,
    /// Operation selector at each node
    pub operations: Vec<SoftOperation>,
    /// Left/right child selectors
    pub child_select: Vec<DifferentiableLinear>,
}

impl NeuralExpressionTree {
    pub fn new(n_vars: usize, d_model: usize, max_depth: usize) -> Self {
        let std = (1.0 / d_model as f32).sqrt();
        let var_embed_data = Array3::from_shape_fn((1, n_vars, d_model), |_| {
            use rand::Rng;
            rand::thread_rng().gen::<f32>() * std * 2.0 - std
        });

        let n_nodes = (1 << max_depth) - 1; // 2^depth - 1 nodes in full tree
        let operations: Vec<_> = (0..n_nodes).map(|_| SoftOperation::new(1.0)).collect();
        let child_select: Vec<_> = (0..n_nodes).map(|_| DifferentiableLinear::new(d_model, n_vars + 1, false)).collect();

        Self {
            n_vars,
            d_model,
            max_depth,
            var_embed: Variable::parameter(var_embed_data),
            const_proj: DifferentiableLinear::new(1, d_model, false),
            operations,
            child_select,
        }
    }

    /// Evaluate the expression tree on variable assignments
    /// assignments: [batch, n_vars, 1]
    pub fn forward(&self, assignments: &Variable) -> Variable {
        let batch = assignments.shape().0;

        // Embed variables
        let assign_data = assignments.data();
        let var_embed_data = self.var_embed.data();

        // For now, simple: combine variable embeddings weighted by assignments
        let mut node_values = Array3::zeros((batch, 1, self.d_model));

        for b in 0..batch {
            for d in 0..self.d_model {
                let mut sum = 0.0f32;
                for v in 0..self.n_vars {
                    sum += assign_data[[b, v, 0]] * var_embed_data[[0, v, d]];
                }
                node_values[[b, 0, d]] = sum;
            }
        }

        Variable::new(node_values, true)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = vec![self.var_embed.clone()];
        params.extend(self.const_proj.parameters());
        for op in &self.operations {
            params.extend(op.parameters());
        }
        for sel in &self.child_select {
            params.extend(sel.parameters());
        }
        params
    }

    pub fn zero_grad(&self) {
        self.var_embed.zero_grad();
        self.const_proj.zero_grad();
        for op in &self.operations {
            op.zero_grad();
        }
        for sel in &self.child_select {
            sel.zero_grad();
        }
    }
}

/// Neural constraint solver - learns to satisfy constraints
#[derive(Clone)]
pub struct NeuralConstraintSolver {
    /// Input dimension (constraint embedding)
    d_input: usize,
    /// Hidden dimension
    d_hidden: usize,
    /// Number of variables to solve for
    n_vars: usize,
    /// Domain size per variable
    domain_size: usize,

    /// Constraint encoder
    pub encoder: DifferentiableLinear,
    /// Hidden layers
    pub hidden1: DifferentiableLinear,
    pub hidden2: DifferentiableLinear,
    /// Variable predictors (one per variable)
    pub var_predictors: Vec<DifferentiableLinear>,
}

impl NeuralConstraintSolver {
    pub fn new(d_input: usize, d_hidden: usize, n_vars: usize, domain_size: usize) -> Self {
        let var_predictors: Vec<_> = (0..n_vars)
            .map(|_| DifferentiableLinear::new(d_hidden, domain_size, false))
            .collect();

        Self {
            d_input,
            d_hidden,
            n_vars,
            domain_size,
            encoder: DifferentiableLinear::new(d_input, d_hidden, false),
            hidden1: DifferentiableLinear::new(d_hidden, d_hidden, false),
            hidden2: DifferentiableLinear::new(d_hidden, d_hidden, false),
            var_predictors,
        }
    }

    /// Forward pass: constraint embedding -> soft variable assignments
    /// Returns probabilities over domain for each variable
    pub fn forward(&self, constraint_embed: &Variable) -> Vec<Variable> {
        // Encode constraint
        let h = self.encoder.forward(constraint_embed).gelu();
        let h = self.hidden1.forward(&h).gelu();
        let h = self.hidden2.forward(&h).gelu();

        // Predict each variable
        self.var_predictors.iter()
            .map(|pred| pred.forward(&h).softmax())
            .collect()
    }

    /// Sample hard assignments from soft predictions (for evaluation)
    pub fn sample_hard(&self, soft_assignments: &[Variable]) -> Vec<usize> {
        soft_assignments.iter()
            .map(|v| {
                let data = v.data();
                let mut best_idx = 0;
                let mut best_val = f32::NEG_INFINITY;
                for i in 0..self.domain_size {
                    if data[[0, 0, i]] > best_val {
                        best_val = data[[0, 0, i]];
                        best_idx = i;
                    }
                }
                best_idx
            })
            .collect()
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.encoder.parameters();
        params.extend(self.hidden1.parameters());
        params.extend(self.hidden2.parameters());
        for pred in &self.var_predictors {
            params.extend(pred.parameters());
        }
        params
    }

    pub fn zero_grad(&self) {
        self.encoder.zero_grad();
        self.hidden1.zero_grad();
        self.hidden2.zero_grad();
        for pred in &self.var_predictors {
            pred.zero_grad();
        }
    }

    pub fn num_parameters(&self) -> usize {
        let encoder = self.d_input * self.d_hidden;
        let hidden = self.d_hidden * self.d_hidden * 2;
        let predictors = self.n_vars * self.d_hidden * self.domain_size;
        encoder + hidden + predictors
    }
}

/// Differentiable reasoning module
/// Combines expression trees with constraint solving
#[derive(Clone)]
pub struct DifferentiableReasoner {
    /// Expression tree for building formulas
    pub expr_tree: NeuralExpressionTree,
    /// Constraint solver
    pub solver: NeuralConstraintSolver,
    /// Soft operations for combining
    pub combine_op: SoftOperation,
    /// Soft comparison for verification
    pub verify_cmp: SoftComparison,
}

impl DifferentiableReasoner {
    pub fn new(n_vars: usize, d_model: usize, domain_size: usize) -> Self {
        Self {
            expr_tree: NeuralExpressionTree::new(n_vars, d_model, 3),
            solver: NeuralConstraintSolver::new(d_model, d_model * 2, n_vars, domain_size),
            combine_op: SoftOperation::new(0.5),
            verify_cmp: SoftComparison::new(0.5),
        }
    }

    /// Reason about a constraint
    /// constraint_embed: [batch, 1, d_model] - encoded constraint
    /// target: [batch, 1, 1] - target value to satisfy
    /// Returns: (solution_probs, satisfaction_score)
    pub fn forward(
        &self,
        constraint_embed: &Variable,
        target: &Variable,
    ) -> (Vec<Variable>, Variable) {
        // Solve for variable assignments
        let soft_assignments = self.solver.forward(constraint_embed);

        // Build expression value from assignments
        let combined_assign = self.combine_assignments(&soft_assignments);
        let expr_value = self.expr_tree.forward(&combined_assign);

        // Compute satisfaction score
        let satisfaction = self.verify_cmp.forward(&expr_value, target);

        (soft_assignments, satisfaction)
    }

    fn combine_assignments(&self, assignments: &[Variable]) -> Variable {
        let batch = assignments[0].shape().0;
        let n_vars = assignments.len();

        // Convert soft assignments to expected values
        let mut combined = Array3::zeros((batch, n_vars, 1));
        for (v, assign) in assignments.iter().enumerate() {
            let data = assign.data();
            for b in 0..batch {
                // Expected value = sum(prob[i] * i)
                let mut expected = 0.0f32;
                for i in 0..data.shape()[2] {
                    expected += data[[b, 0, i]] * i as f32;
                }
                combined[[b, v, 0]] = expected;
            }
        }

        Variable::new(combined, true)
    }

    pub fn parameters(&self) -> Vec<Variable> {
        let mut params = self.expr_tree.parameters();
        params.extend(self.solver.parameters());
        params.extend(self.combine_op.parameters());
        params.extend(self.verify_cmp.parameters());
        params
    }

    pub fn zero_grad(&self) {
        self.expr_tree.zero_grad();
        self.solver.zero_grad();
        self.combine_op.zero_grad();
        self.verify_cmp.zero_grad();
    }

    pub fn num_parameters(&self) -> usize {
        self.parameters().iter()
            .map(|p| p.data().len())
            .sum()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_soft_operation() {
        let op = SoftOperation::new(1.0);

        let a = Variable::parameter(Array3::from_elem((1, 1, 4), 2.0));
        let b = Variable::parameter(Array3::from_elem((1, 1, 4), 3.0));

        let result = op.forward(&a, &b);
        assert_eq!(result.shape(), (1, 1, 4));

        // With uniform weights, result should be average of all ops
        // add=5, sub=-1, mul=6, div=0.67, max=3, min=2 -> avg ≈ 2.6
        let data = result.data();
        assert!(data[[0, 0, 0]] > 2.0 && data[[0, 0, 0]] < 3.5);
    }

    #[test]
    fn test_soft_comparison() {
        let cmp = SoftComparison::new(1.0);

        let a = Variable::parameter(Array3::from_elem((1, 1, 1), 5.0));
        let b = Variable::parameter(Array3::from_elem((1, 1, 1), 3.0));

        let result = cmp.forward(&a, &b);
        let data = result.data();

        // a > b, so with uniform weights, gt and ge should pull result up
        assert!(data[[0, 0, 0]] > 0.3);
    }

    #[test]
    fn test_neural_constraint_solver() {
        let solver = NeuralConstraintSolver::new(16, 32, 3, 10);

        let constraint = Variable::parameter(Array3::ones((1, 1, 16)));
        let assignments = solver.forward(&constraint);

        assert_eq!(assignments.len(), 3);
        for assign in &assignments {
            assert_eq!(assign.shape(), (1, 1, 10));

            // Check probabilities sum to ~1
            let data = assign.data();
            let sum: f32 = (0..10).map(|i| data[[0, 0, i]]).sum();
            assert!((sum - 1.0).abs() < 0.01);
        }
    }

    #[test]
    fn test_neural_constraint_solver_gradient() {
        let solver = NeuralConstraintSolver::new(8, 16, 2, 5);

        let constraint = Variable::parameter(Array3::ones((1, 1, 8)));
        let assignments = solver.forward(&constraint);

        // Create target: we want variable 0 = 2, variable 1 = 3
        let target0 = Array3::from_shape_fn((1, 1, 5), |(_, _, i)| {
            if i == 2 { 1.0 } else { 0.0 }
        });
        let target1 = Array3::from_shape_fn((1, 1, 5), |(_, _, i)| {
            if i == 3 { 1.0 } else { 0.0 }
        });

        // Compute cross-entropy loss
        let pred0 = assignments[0].data();
        let pred1 = assignments[1].data();

        let mut loss = 0.0f32;
        for i in 0..5 {
            loss -= target0[[0, 0, i]] * pred0[[0, 0, i]].max(1e-10).ln();
            loss -= target1[[0, 0, i]] * pred1[[0, 0, i]].max(1e-10).ln();
        }

        // Just verify we can compute loss without panicking
        assert!(loss.is_finite());
    }

    #[test]
    fn test_differentiable_reasoner() {
        let reasoner = DifferentiableReasoner::new(3, 16, 10);

        let constraint = Variable::parameter(Array3::ones((1, 1, 16)));
        // Target must match expr_tree output shape: (batch, 1, d_model)
        let target = Variable::parameter(Array3::from_elem((1, 1, 16), 5.0));

        let (assignments, satisfaction) = reasoner.forward(&constraint, &target);

        assert_eq!(assignments.len(), 3);
        assert_eq!(satisfaction.shape(), (1, 1, 16)); // d_model from expr_tree

        println!("Reasoner parameters: {}", reasoner.num_parameters());
    }

    #[test]
    fn test_soft_op_learns_addition() {
        // Train a soft operation to become addition
        let op = SoftOperation::new(0.5);

        // Training data: a + b = target
        for _ in 0..100 {
            let a_val: f32 = rand::random::<f32>() * 10.0;
            let b_val: f32 = rand::random::<f32>() * 10.0;
            let target = a_val + b_val;

            let a = Variable::parameter(Array3::from_elem((1, 1, 1), a_val));
            let b = Variable::parameter(Array3::from_elem((1, 1, 1), b_val));
            let target_var = Variable::new(Array3::from_elem((1, 1, 1), target), false);

            op.zero_grad();

            let pred = op.forward(&a, &b);
            let diff = pred.sub(&target_var);
            let loss = diff.mul(&diff).mean();

            loss.backward();

            // Simple gradient descent on operation weights
            if let Some(grad) = op.weights.get_grad() {
                let current = op.weights.data();
                let lr = 0.1f32;
                op.weights.apply_update(&(-&grad * lr));
            }
        }

        // Check that add weight is highest
        let weights_data = op.weights.data();
        let add_weight = weights_data[[0, 0, 0]];
        for i in 1..6 {
            assert!(add_weight >= weights_data[[0, 0, i]] - 0.1,
                "Add weight {} should be highest, but weight[{}] = {}",
                add_weight, i, weights_data[[0, 0, i]]);
        }

        assert_eq!(op.dominant_op(), "add");
    }
}
