# Reward Modeling & Alignment Methods for LLMs

*Synthesized by Ember (Dec 31, 2025 ~04:08 UTC)*

Research on process reward models (PRMs), outcome reward models (ORMs), and alignment methods (RLHF, DPO, GRPO, ORPO).

## Executive Summary

| Method | Type | Key Advantage | Best For |
|--------|------|---------------|----------|
| **RLHF (PPO)** | RL-based | Maximum performance | Production, complex tasks |
| **DPO** | Direct | Simple, no reward model | Resource-constrained |
| **GRPO** | Group RL | 50% less compute (no critic) | Math reasoning, efficiency |
| **ORPO** | Combined | SFT + alignment in one | Base model alignment |
| **PRM** | Step-level | Credit assignment | Verifiable reasoning |
| **ORM** | Outcome | Simple training | General tasks |

## Reward Model Types

### Outcome Reward Models (ORMs)

Score only the final result:

```python
def orm_score(question, final_answer):
    # Single scalar reward for entire response
    return reward_model(question, final_answer)
```

**Pros**: Simple, less data needed
**Cons**: No credit assignment (which step was wrong?)

### Process Reward Models (PRMs)

Score each intermediate step:

```python
def prm_score(question, reasoning_chain):
    # Score at each step
    step_rewards = []
    for i, step in enumerate(reasoning_chain):
        context = reasoning_chain[:i+1]
        step_rewards.append(reward_model(question, context))
    return step_rewards
```

**Pros**:
- Fine-grained supervision
- Better for complex reasoning
- Enables tree search (MCTS integration)
- Improves sample efficiency

**Cons**:
- Requires step-level annotations (expensive)
- Monte Carlo estimation can be inaccurate
- DeepSeek R1 found limited benefit vs overhead in large-scale RL

### PRM Training Challenges

From "Lessons of Developing PRMs in Mathematical Reasoning" (Jan 2025):

| Method | Quality | Cost |
|--------|---------|------|
| Human annotation | Best | Very high |
| LLM-as-a-judge | Good | Medium |
| Monte Carlo estimation | Inferior | Low |

**Key finding**: MC estimation (using completion models to evaluate steps) yields inferior performance because it leads to inaccurate step verification.

### THINKPRM (2025)

New approach: PRMs that "think" before judging:

```
Traditional PRM: Discriminative classifier
THINKPRM: Generative reasoning before classification
```

**Benefit**: Reduces need for step-level annotations by leveraging LLM reasoning.

### AgentPRM Framework (Feb 2025)

For training LLM agents:

```
Framework:
1. Actor-critic paradigm (lightweight)
2. Monte Carlo rollouts for reward targets
3. Minimal modifications to RLHF pipelines

Key innovation: PRMs provide per-step supervision like RL value functions
```

## Alignment Methods

### RLHF with PPO (Baseline)

```
Traditional pipeline:
1. Pre-train base model
2. Supervised fine-tuning (SFT)
3. Train reward model on human preferences
4. RL training with PPO using reward model
```

**Pros**: Maximum performance, state-of-the-art results
**Cons**: Complex, unstable, requires separate reward model (2× memory)

### DPO (Direct Preference Optimization)

Eliminates reward model entirely:

```python
# DPO loss directly on preference pairs
def dpo_loss(model, ref_model, chosen, rejected, beta=0.1):
    # Log probability ratios
    log_ratio_chosen = model.log_prob(chosen) - ref_model.log_prob(chosen)
    log_ratio_rejected = model.log_prob(rejected) - ref_model.log_prob(rejected)

    # DPO objective
    loss = -log_sigmoid(beta * (log_ratio_chosen - log_ratio_rejected))
    return loss.mean()
```

**Key insight**: Reward model is implicitly defined by policy ratio.

**Pros**: Simple, stable, efficient
**Cons**: May underperform PPO on complex tasks

### GRPO (Group Relative Policy Optimization)

DeepSeek's innovation - eliminates critic network:

```python
# GRPO: No value network, use group statistics
def grpo_advantage(rewards_group):
    # Group of G responses per prompt
    mean = rewards_group.mean()
    std = rewards_group.std() + eps

    # Normalized advantage (relative to group)
    advantages = (rewards_group - mean) / std
    return advantages

def grpo_loss(policy, ref_policy, responses, advantages):
    # Similar to PPO but with group-relative advantages
    log_ratios = policy.log_prob(responses) - ref_policy.log_prob(responses)

    # Clipped objective (like PPO)
    loss = -min(
        log_ratios * advantages,
        clip(log_ratios, 1-eps, 1+eps) * advantages
    )
    return loss.mean()
```

**Key innovations**:
1. No critic network → 50% memory savings
2. Group sampling → Stable advantage estimation
3. Conservative updates → Better stability

**Results (DeepSeekMath)**:
- GSM8K: 82.9% → 88.2%
- MATH: 46.8% → 51.7%
- CMATH: 84.6% → 88.8%

### ORPO (Odds Ratio Preference Optimization)

Combines SFT and alignment in one step:

```python
# ORPO: Single-stage training
def orpo_loss(model, chosen, rejected, lambda_=1.0):
    # SFT loss on chosen
    sft_loss = -model.log_prob(chosen).mean()

    # Odds ratio loss (preference)
    log_odds_chosen = model.log_prob(chosen) - log(1 - exp(model.log_prob(chosen)))
    log_odds_rejected = model.log_prob(rejected) - log(1 - exp(model.log_prob(rejected)))

    preference_loss = -log_sigmoid(log_odds_chosen - log_odds_rejected)

    return sft_loss + lambda_ * preference_loss.mean()
```

**Pros**:
- No reference model needed
- Single training stage
- Computationally efficient

### Other Methods

| Method | Key Feature |
|--------|-------------|
| **IPO** | Fixes DPO overfitting |
| **KTO** | Uses good/bad labels (no pairs needed) |
| **SimPO** | No reference model, faster |
| **GSPO** | Self-play for iterative improvement |

### Method Comparison (2025)

```
Performance:
  PPO ≥ GRPO > DPO ≥ ORPO (on complex tasks)

Efficiency:
  ORPO > DPO > GRPO > PPO

Stability:
  DPO > ORPO > GRPO > PPO

Recommended:
  Complex + resources: PPO or GRPO
  Simple + efficient: DPO or ORPO
  Base model start: ORPO
  Math reasoning: GRPO
```

## For Nexus

### Existing Infrastructure

Nexus already has DPO in `dpo.rs`:

```rust
pub struct DPOTrainer {
    policy: NexusModel,
    reference: NexusModel,  // Frozen copy
    beta: f32,              // Temperature
    loss_type: DPOLossType, // DPO, IPO, KTO, ORPO
}
```

### Recommended Additions

**1. GRPO Implementation**

```rust
pub struct GRPOTrainer {
    policy: NexusModel,
    reference: NexusModel,
    group_size: usize,      // G responses per prompt
    clip_range: f32,        // Like PPO epsilon
    kl_coef: f32,           // KL penalty
}

impl GRPOTrainer {
    fn compute_advantages(&self, rewards: &[f32]) -> Vec<f32> {
        // Group-relative normalization
        let mean = rewards.iter().sum::<f32>() / rewards.len() as f32;
        let std = /* compute std */;
        rewards.iter().map(|r| (r - mean) / (std + 1e-8)).collect()
    }
}
```

**2. Simple PRM for Math**

```rust
pub struct ProcessRewardModel {
    base_model: NexusModel,
    reward_head: Linear,  // Projects to scalar
}

impl ProcessRewardModel {
    fn score_step(&self, context: &[Token]) -> f32 {
        let hidden = self.base_model.encode(context);
        self.reward_head.forward(&hidden).item()
    }

    fn score_chain(&self, steps: &[Vec<Token>]) -> Vec<f32> {
        let mut context = Vec::new();
        steps.iter().map(|step| {
            context.extend_from_slice(step);
            self.score_step(&context)
        }).collect()
    }
}
```

### Titans + Reward Models

Nexus's Titans memory could enhance reward modeling:

```rust
// Titans memory as implicit reward signal
impl TitansMemory {
    fn surprise_as_reward(&self, hidden: &Tensor) -> f32 {
        // High surprise = model uncertainty
        // Could indicate:
        // - Novel correct reasoning (reward)
        // - Likely error (penalize)

        // Use surprise magnitude as signal
        let surprise = self.compute_surprise(hidden);

        // Calibrated via validation
        self.surprise_to_reward(surprise)
    }
}
```

**Insight**: Surprise-based reward is complementary to PRMs:
- PRM: External verification of correctness
- Titans: Internal uncertainty/novelty detection

## Key Formulas

### DPO Loss
```
L_DPO = -E[log σ(β(log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))]
```

### GRPO Advantage
```
A_i = (r_i - mean(r_group)) / std(r_group)
```

### ORPO Odds Ratio
```
OR(y|x) = P(y|x) / (1 - P(y|x))
L_OR = -log σ(log OR(y_w|x) - log OR(y_l|x))
```

### PRM Value
```
V(s_t) = E[Σ_{t'=t}^T γ^{t'-t} r(s_t', a_t') | s_t]
```

## 2025 Trends

1. **GRPO dominance**: DeepSeek R1's success makes GRPO the go-to for reasoning
2. **PRM skepticism**: Large-scale RL shows limited benefit vs overhead
3. **Simpler methods**: GSPO, SimPO pushing toward minimal complexity
4. **Self-play**: Iterative improvement without human preferences
5. **Emergent reasoning**: RL alone can develop reasoning (DeepSeek R1)

## References

- [RLHF Book - Reward Models](https://rlhfbook.com/c/07-reward-models) - Nathan Lambert
- [DeepSeekMath / GRPO](https://arxiv.org/abs/2402.03300) - DeepSeek
- [DeepSeek-R1](https://www.nature.com/articles/s41586-025-09422-z) - Nature 2025
- [PRM Lessons](https://arxiv.org/abs/2501.07301) - Jan 2025
- [AgentPRM](https://arxiv.org/html/2502.10325v1) - Feb 2025
- [DPO vs PPO Study](https://arxiv.org/abs/2404.10719) - 2024
- [GRPO Illustrated](https://epichka.com/blog/2025/grpo/) - Ebrahim Pichka
- [Cameron Wolfe - GRPO](https://cameronrwolfe.substack.com/p/grpo)
