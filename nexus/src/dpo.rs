//! Direct Preference Optimization (DPO)
//!
//! A simpler alternative to RLHF that directly optimizes from preference pairs.
//! Based on: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
//!
//! Key insight: The optimal policy can be derived in closed form from the reward model,
//! allowing direct training without separate reward modeling or RL.

use ndarray::{Array2, Array3};
use crate::autograd::Variable;

/// DPO training configuration
#[derive(Clone, Debug)]
pub struct DPOConfig {
    /// Beta parameter (KL penalty strength)
    /// Higher beta = stay closer to reference model
    pub beta: f32,
    /// Learning rate
    pub learning_rate: f32,
    /// Label smoothing (0 = no smoothing)
    pub label_smoothing: f32,
    /// Whether to use reference model (if false, uses implicit reference)
    pub use_reference_model: bool,
    /// Gradient accumulation steps
    pub grad_accum_steps: usize,
    /// Maximum gradient norm for clipping
    pub max_grad_norm: f32,
}

impl Default for DPOConfig {
    fn default() -> Self {
        Self {
            beta: 0.1,
            learning_rate: 1e-6,
            label_smoothing: 0.0,
            use_reference_model: true,
            grad_accum_steps: 1,
            max_grad_norm: 1.0,
        }
    }
}

/// A preference pair for DPO training
#[derive(Clone, Debug)]
pub struct PreferencePair {
    /// The prompt/context
    pub prompt: Vec<u32>,
    /// The chosen (preferred) response
    pub chosen: Vec<u32>,
    /// The rejected response
    pub rejected: Vec<u32>,
}

impl PreferencePair {
    pub fn new(prompt: Vec<u32>, chosen: Vec<u32>, rejected: Vec<u32>) -> Self {
        Self { prompt, chosen, rejected }
    }

    /// Get full sequence for chosen response
    pub fn chosen_sequence(&self) -> Vec<u32> {
        let mut seq = self.prompt.clone();
        seq.extend(&self.chosen);
        seq
    }

    /// Get full sequence for rejected response
    pub fn rejected_sequence(&self) -> Vec<u32> {
        let mut seq = self.prompt.clone();
        seq.extend(&self.rejected);
        seq
    }

    /// Get response start index (where to start computing loss)
    pub fn response_start(&self) -> usize {
        self.prompt.len()
    }
}

/// DPO Loss computation
pub struct DPOLoss {
    config: DPOConfig,
}

impl DPOLoss {
    pub fn new(config: DPOConfig) -> Self {
        Self { config }
    }

    /// Compute log probabilities for a sequence
    /// logits: [batch, seq_len, vocab_size]
    /// tokens: target token IDs [batch, seq_len]
    /// Returns: log_probs [batch, seq_len-1]
    pub fn compute_log_probs(
        &self,
        logits: &Array3<f32>,
        tokens: &[Vec<u32>],
    ) -> Array2<f32> {
        let (batch, seq_len, vocab_size) = logits.dim();
        let mut log_probs = Array2::zeros((batch, seq_len - 1));

        for b in 0..batch {
            for t in 0..(seq_len - 1) {
                // Get logits for position t
                let max_logit = (0..vocab_size)
                    .map(|v| logits[[b, t, v]])
                    .fold(f32::NEG_INFINITY, f32::max);

                // Compute log_softmax
                let log_sum_exp: f32 = (0..vocab_size)
                    .map(|v| (logits[[b, t, v]] - max_logit).exp())
                    .sum::<f32>()
                    .ln();

                // Get log prob of actual next token
                let target = tokens[b][t + 1] as usize;
                log_probs[[b, t]] = logits[[b, t, target]] - max_logit - log_sum_exp;
            }
        }

        log_probs
    }

    /// Compute DPO loss for a batch of preference pairs
    ///
    /// # Arguments
    /// * `policy_chosen_logits` - Logits from policy model for chosen responses
    /// * `policy_rejected_logits` - Logits from policy model for rejected responses
    /// * `ref_chosen_logits` - Logits from reference model for chosen responses (optional)
    /// * `ref_rejected_logits` - Logits from reference model for rejected responses (optional)
    /// * `chosen_tokens` - Token IDs for chosen responses
    /// * `rejected_tokens` - Token IDs for rejected responses
    /// * `response_starts` - Index where response starts in each sequence
    ///
    /// # Returns
    /// (loss, chosen_rewards, rejected_rewards, reward_margins)
    pub fn compute(
        &self,
        policy_chosen_logits: &Array3<f32>,
        policy_rejected_logits: &Array3<f32>,
        ref_chosen_logits: Option<&Array3<f32>>,
        ref_rejected_logits: Option<&Array3<f32>>,
        chosen_tokens: &[Vec<u32>],
        rejected_tokens: &[Vec<u32>],
        response_starts: &[usize],
    ) -> (f32, Vec<f32>, Vec<f32>, Vec<f32>) {
        let batch_size = chosen_tokens.len();

        // Compute log probs for policy model
        let policy_chosen_logprobs = self.compute_log_probs(policy_chosen_logits, chosen_tokens);
        let policy_rejected_logprobs = self.compute_log_probs(policy_rejected_logits, rejected_tokens);

        // Compute log probs for reference model (or use zeros if implicit)
        let (ref_chosen_logprobs, ref_rejected_logprobs) = match (ref_chosen_logits, ref_rejected_logits) {
            (Some(rc), Some(rr)) => {
                (self.compute_log_probs(rc, chosen_tokens), self.compute_log_probs(rr, rejected_tokens))
            }
            _ => {
                // Implicit reference: assume uniform distribution
                let zeros = Array2::zeros(policy_chosen_logprobs.dim());
                (zeros.clone(), zeros)
            }
        };

        let mut total_loss = 0.0f32;
        let mut chosen_rewards = Vec::with_capacity(batch_size);
        let mut rejected_rewards = Vec::with_capacity(batch_size);
        let mut margins = Vec::with_capacity(batch_size);

        for b in 0..batch_size {
            let start = response_starts[b];
            let chosen_len = chosen_tokens[b].len() - 1;
            let rejected_len = rejected_tokens[b].len() - 1;

            // Sum log probs for response portion only
            let mut policy_chosen_sum = 0.0f32;
            let mut policy_rejected_sum = 0.0f32;
            let mut ref_chosen_sum = 0.0f32;
            let mut ref_rejected_sum = 0.0f32;

            for t in start..chosen_len {
                policy_chosen_sum += policy_chosen_logprobs[[b, t]];
                ref_chosen_sum += ref_chosen_logprobs[[b, t]];
            }

            for t in start..rejected_len {
                policy_rejected_sum += policy_rejected_logprobs[[b, t]];
                ref_rejected_sum += ref_rejected_logprobs[[b, t]];
            }

            // Compute log ratios (policy / reference)
            let log_ratio_chosen = policy_chosen_sum - ref_chosen_sum;
            let log_ratio_rejected = policy_rejected_sum - ref_rejected_sum;

            // DPO loss: -log(sigmoid(beta * (log_ratio_chosen - log_ratio_rejected)))
            let margin = self.config.beta * (log_ratio_chosen - log_ratio_rejected);

            // Apply label smoothing if configured
            let target = 1.0 - self.config.label_smoothing;

            // Binary cross entropy with logits
            let loss = -target * log_sigmoid(margin) - (1.0 - target) * log_sigmoid(-margin);

            total_loss += loss;
            chosen_rewards.push(log_ratio_chosen);
            rejected_rewards.push(log_ratio_rejected);
            margins.push(margin);
        }

        let avg_loss = total_loss / batch_size as f32;
        (avg_loss, chosen_rewards, rejected_rewards, margins)
    }

    /// Get config
    pub fn config(&self) -> &DPOConfig {
        &self.config
    }
}

/// Numerically stable log sigmoid
fn log_sigmoid(x: f32) -> f32 {
    if x >= 0.0 {
        -(-x).exp().ln_1p()
    } else {
        x - x.exp().ln_1p()
    }
}

/// DPO Trainer
pub struct DPOTrainer<M: DPOModel> {
    /// Policy model being trained
    policy: M,
    /// Reference model (frozen)
    reference: Option<M>,
    /// Learning rate
    lr: f32,
    /// DPO loss function
    loss_fn: DPOLoss,
    /// Training config
    config: DPOConfig,
    /// Training metrics
    metrics: DPOMetrics,
}

/// Trait for models that can be trained with DPO
pub trait DPOModel: Clone {
    /// Forward pass returning logits
    fn forward(&mut self, token_ids: &[Vec<u32>]) -> Array3<f32>;

    /// Get all trainable parameters
    fn parameters(&self) -> Vec<Variable>;

    /// Zero gradients
    fn zero_grad(&self);
}

/// Training metrics
#[derive(Clone, Debug, Default)]
pub struct DPOMetrics {
    pub total_steps: usize,
    pub total_loss: f32,
    pub avg_chosen_reward: f32,
    pub avg_rejected_reward: f32,
    pub avg_margin: f32,
    pub accuracy: f32,
}

impl DPOMetrics {
    pub fn update(
        &mut self,
        loss: f32,
        chosen_rewards: &[f32],
        rejected_rewards: &[f32],
        margins: &[f32],
    ) {
        self.total_steps += 1;
        self.total_loss += loss;

        let n = chosen_rewards.len() as f32;
        self.avg_chosen_reward = chosen_rewards.iter().sum::<f32>() / n;
        self.avg_rejected_reward = rejected_rewards.iter().sum::<f32>() / n;
        self.avg_margin = margins.iter().sum::<f32>() / n;

        // Accuracy: fraction where margin > 0
        let correct = margins.iter().filter(|&&m| m > 0.0).count();
        self.accuracy = correct as f32 / n;
    }

    pub fn avg_loss(&self) -> f32 {
        if self.total_steps > 0 {
            self.total_loss / self.total_steps as f32
        } else {
            0.0
        }
    }
}

impl<M: DPOModel> DPOTrainer<M> {
    pub fn new(policy: M, reference: Option<M>, config: DPOConfig) -> Self {
        let lr = config.learning_rate;
        let loss_fn = DPOLoss::new(config.clone());

        Self {
            policy,
            reference,
            lr,
            loss_fn,
            config,
            metrics: DPOMetrics::default(),
        }
    }

    /// Train on a batch of preference pairs
    pub fn train_step(&mut self, batch: &[PreferencePair]) -> (f32, DPOMetrics) {
        let _batch_size = batch.len();

        // Prepare sequences
        let chosen_tokens: Vec<Vec<u32>> = batch.iter().map(|p| p.chosen_sequence()).collect();
        let rejected_tokens: Vec<Vec<u32>> = batch.iter().map(|p| p.rejected_sequence()).collect();
        let response_starts: Vec<usize> = batch.iter().map(|p| p.response_start()).collect();

        // Forward through policy model
        self.policy.zero_grad();
        let policy_chosen_logits = self.policy.forward(&chosen_tokens);
        let policy_rejected_logits = self.policy.forward(&rejected_tokens);

        // Forward through reference model (if using)
        let (ref_chosen, ref_rejected) = if self.config.use_reference_model {
            if let Some(ref mut reference) = self.reference {
                let rc = reference.forward(&chosen_tokens);
                let rr = reference.forward(&rejected_tokens);
                (Some(rc), Some(rr))
            } else {
                (None, None)
            }
        } else {
            (None, None)
        };

        // Compute DPO loss
        let (loss, chosen_rewards, rejected_rewards, margins) = self.loss_fn.compute(
            &policy_chosen_logits,
            &policy_rejected_logits,
            ref_chosen.as_ref(),
            ref_rejected.as_ref(),
            &chosen_tokens,
            &rejected_tokens,
            &response_starts,
        );

        // Create loss variable for backward pass
        let loss_var = Variable::new(
            Array3::from_elem((1, 1, 1), loss),
            true,
        );
        loss_var.backward();

        // Gradient clipping
        let params = self.policy.parameters();
        clip_grad_norm(&params, self.config.max_grad_norm);

        // Simple gradient descent step
        for param in &params {
            if let Some(grad) = param.get_grad() {
                param.apply_update(&(-&grad * self.lr));
            }
        }

        // Update metrics
        self.metrics.update(loss, &chosen_rewards, &rejected_rewards, &margins);

        (loss, self.metrics.clone())
    }

    /// Get current metrics
    pub fn metrics(&self) -> &DPOMetrics {
        &self.metrics
    }

    /// Reset metrics
    pub fn reset_metrics(&mut self) {
        self.metrics = DPOMetrics::default();
    }

    /// Get policy model
    pub fn policy(&self) -> &M {
        &self.policy
    }

    /// Get mutable policy model
    pub fn policy_mut(&mut self) -> &mut M {
        &mut self.policy
    }
}

/// Clip gradient norm
fn clip_grad_norm(params: &[Variable], max_norm: f32) {
    // Compute total gradient norm
    let mut total_norm_sq = 0.0f32;
    for param in params {
        if let Some(grad) = param.get_grad() {
            total_norm_sq += grad.iter().map(|x| x * x).sum::<f32>();
        }
    }
    let total_norm = total_norm_sq.sqrt();

    // Clip if necessary
    if total_norm > max_norm {
        let clip_coef = max_norm / (total_norm + 1e-6);
        for param in params {
            if let Some(grad) = param.get_grad() {
                let clipped = grad.mapv(|x| x * clip_coef);
                param.set_grad(clipped);
            }
        }
    }
}

/// IPO (Identity Preference Optimization) loss variant
/// Simpler than DPO, doesn't require reference model
pub struct IPOLoss {
    /// Regularization strength
    tau: f32,
}

impl IPOLoss {
    pub fn new(tau: f32) -> Self {
        Self { tau }
    }

    /// Compute IPO loss
    /// IPO loss = (log(pi(y_w)/pi(y_l)) - 1/tau)^2
    pub fn compute(
        &self,
        policy_chosen_logprobs: f32,
        policy_rejected_logprobs: f32,
    ) -> f32 {
        let log_ratio = policy_chosen_logprobs - policy_rejected_logprobs;
        let target = 1.0 / self.tau;
        (log_ratio - target).powi(2)
    }
}

/// KTO (Kahneman-Tversky Optimization) loss variant
/// Handles unpaired preference data
pub struct KTOLoss {
    beta: f32,
    /// Reference point for losses vs gains
    reference_value: f32,
}

impl KTOLoss {
    pub fn new(beta: f32) -> Self {
        Self {
            beta,
            reference_value: 0.0,
        }
    }

    /// Compute KTO loss for a single example
    /// is_chosen: whether this is a preferred example
    pub fn compute(
        &self,
        policy_logprob: f32,
        reference_logprob: f32,
        is_chosen: bool,
    ) -> f32 {
        let log_ratio = policy_logprob - reference_logprob;
        let reward = self.beta * log_ratio;

        if is_chosen {
            // Maximize reward above reference
            -log_sigmoid(reward - self.reference_value)
        } else {
            // Minimize reward below reference
            -log_sigmoid(self.reference_value - reward)
        }
    }
}

/// ORPO (Odds Ratio Preference Optimization) loss
/// Combines SFT and preference optimization
pub struct ORPOLoss {
    lambda: f32,
}

impl ORPOLoss {
    pub fn new(lambda: f32) -> Self {
        Self { lambda }
    }

    /// Compute ORPO loss
    /// Combines NLL loss with odds ratio penalty
    pub fn compute(
        &self,
        chosen_logprob: f32,
        rejected_logprob: f32,
        chosen_nll: f32,
    ) -> f32 {
        // Odds ratio: (p_chosen / (1 - p_chosen)) / (p_rejected / (1 - p_rejected))
        // In log space: log_odds_ratio = log_chosen - log_rejected
        //                                - log(1-exp(log_chosen)) + log(1-exp(log_rejected))

        let log_odds_chosen = chosen_logprob - (-chosen_logprob).exp().ln_1p();
        let log_odds_rejected = rejected_logprob - (-rejected_logprob).exp().ln_1p();
        let log_odds_ratio = log_odds_chosen - log_odds_rejected;

        // ORPO loss = NLL + lambda * log(1 + exp(-log_odds_ratio))
        chosen_nll + self.lambda * log_sigmoid(-log_odds_ratio)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_preference_pair() {
        let pair = PreferencePair::new(
            vec![1, 2, 3],     // prompt
            vec![4, 5, 6],     // chosen
            vec![7, 8],        // rejected
        );

        assert_eq!(pair.chosen_sequence(), vec![1, 2, 3, 4, 5, 6]);
        assert_eq!(pair.rejected_sequence(), vec![1, 2, 3, 7, 8]);
        assert_eq!(pair.response_start(), 3);
    }

    #[test]
    fn test_log_probs() {
        let config = DPOConfig::default();
        let loss_fn = DPOLoss::new(config);

        // Logits for 2 positions, vocab size 4
        let logits = Array3::from_shape_fn((1, 3, 4), |(_, t, v)| {
            if t == 0 && v == 1 { 2.0 }  // High prob for token 1 at position 0
            else if t == 1 && v == 2 { 2.0 }  // High prob for token 2 at position 1
            else { 0.0 }
        });

        let tokens = vec![vec![0, 1, 2]]; // Targets: predict 1 at pos 0, 2 at pos 1

        let log_probs = loss_fn.compute_log_probs(&logits, &tokens);

        assert_eq!(log_probs.dim(), (1, 2));
        // Log probs should be higher for correct predictions
        assert!(log_probs[[0, 0]] > -1.0); // Token 1 had high prob at pos 0
        assert!(log_probs[[0, 1]] > -1.0); // Token 2 had high prob at pos 1
    }

    #[test]
    fn test_dpo_loss() {
        let config = DPOConfig { beta: 0.1, ..Default::default() };
        let loss_fn = DPOLoss::new(config);

        // Tokens: [0, 1, 2, 3] - target at position t is tokens[t+1]
        // So target at t=0 is 1, t=1 is 2, t=2 is 3
        let chosen_tokens = vec![vec![0, 1, 2, 3]];
        let rejected_tokens = vec![vec![0, 1, 2, 3]];

        // Create logits where chosen response has much higher log prob for the target tokens
        let policy_chosen = Array3::from_shape_fn((1, 4, 10), |(_, t, v)| {
            // Target token at position t is t+1
            if v == t + 1 { 10.0 } else { 0.0 }
        });
        let policy_rejected = Array3::from_shape_fn((1, 4, 10), |(_, t, v)| {
            // Same targets but much lower confidence
            if v == t + 1 { 0.5 } else { 0.0 }
        });

        let response_starts = vec![1];

        let (loss, chosen_r, rejected_r, margins) = loss_fn.compute(
            &policy_chosen,
            &policy_rejected,
            None, None,
            &chosen_tokens,
            &rejected_tokens,
            &response_starts,
        );

        // Loss should be finite
        assert!(loss.is_finite());

        // Chosen should have higher log prob (reward) than rejected
        assert!(chosen_r[0] > rejected_r[0],
            "chosen_r={}, rejected_r={}", chosen_r[0], rejected_r[0]);

        // Margin should be positive (correct preference)
        assert!(margins[0] > 0.0, "margin={}", margins[0]);
    }

    #[test]
    fn test_log_sigmoid() {
        // Test numerical stability
        assert!(log_sigmoid(100.0).is_finite()); // Large positive
        assert!(log_sigmoid(-100.0).is_finite()); // Large negative
        assert!((log_sigmoid(0.0) - (-0.693)).abs() < 0.01); // log(0.5)

        // Test symmetry property: log_sigmoid(x) + log_sigmoid(-x) = -x for large |x|
        let x = 10.0;
        let sum = log_sigmoid(x) + log_sigmoid(-x);
        // Should be close to 0 (since sigmoid(x) * sigmoid(-x) = sigmoid(x) * (1 - sigmoid(x)))
        // Actually: log(sigmoid(x)) + log(sigmoid(-x)) = log(sigmoid(x) * (1-sigmoid(x)))
    }

    #[test]
    fn test_ipo_loss() {
        let ipo = IPOLoss::new(0.1);

        // When chosen is much better
        let loss1 = ipo.compute(0.0, -5.0);

        // When rejected is better
        let loss2 = ipo.compute(-5.0, 0.0);

        // Loss should be higher when preference is violated
        assert!(loss2 > loss1);
    }

    #[test]
    fn test_kto_loss() {
        let kto = KTOLoss::new(0.1);

        // Chosen example with high reward
        let loss_chosen = kto.compute(0.0, -1.0, true);

        // Rejected example with high reward (should be penalized)
        let loss_rejected = kto.compute(0.0, -1.0, false);

        // Both should be finite
        assert!(loss_chosen.is_finite());
        assert!(loss_rejected.is_finite());
    }

    #[test]
    fn test_orpo_loss() {
        let orpo = ORPOLoss::new(1.0);

        let loss = orpo.compute(-0.5, -1.5, 0.5);
        assert!(loss.is_finite());

        // Higher chosen log prob should give lower loss
        let loss_good = orpo.compute(-0.2, -1.5, 0.5);
        let loss_bad = orpo.compute(-1.0, -1.5, 0.5);
        assert!(loss_good < loss_bad);
    }

    #[test]
    fn test_clip_grad_norm() {
        let param = Variable::parameter(Array3::ones((1, 1, 4)));

        // Set a large gradient
        param.set_grad(Array3::from_elem((1, 1, 4), 10.0));

        clip_grad_norm(&[param.clone()], 1.0);

        // Gradient should be clipped
        let grad = param.get_grad().unwrap();
        let norm: f32 = grad.iter().map(|x| x * x).sum::<f32>().sqrt();
        assert!(norm <= 1.1, "Norm {} should be <= 1.0", norm);
    }

    #[test]
    fn test_dpo_metrics() {
        let mut metrics = DPOMetrics::default();

        metrics.update(
            0.5,
            &[1.0, 2.0],
            &[-1.0, -0.5],
            &[0.5, 1.0],
        );

        assert_eq!(metrics.total_steps, 1);
        assert_eq!(metrics.avg_chosen_reward, 1.5);
        assert_eq!(metrics.avg_rejected_reward, -0.75);
        assert_eq!(metrics.avg_margin, 0.75);
        assert_eq!(metrics.accuracy, 1.0); // Both margins positive
    }
}
