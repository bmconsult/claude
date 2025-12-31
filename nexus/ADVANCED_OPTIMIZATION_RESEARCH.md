# Advanced Optimization Techniques for LLMs

*Synthesized by Ember (Dec 31, 2025 ~04:00 UTC)*

Research on test-time compute scaling, model merging, long context extension, and MCTS-based reasoning.

## Executive Summary

| Technique | Compute Type | Speedup/Improvement | Best For |
|-----------|--------------|---------------------|----------|
| **Test-Time Compute** | Inference | 10-100× thinking time = better reasoning | Complex reasoning |
| **Model Merging** | Zero-shot | Combine multiple task experts | Multi-task capability |
| **Long Context (YaRN)** | Training | 10× less tokens for extension | Context scaling |
| **MCTS Reasoning** | Inference | +17.4% vs o1-mini (SC-MCTS*) | Verifiable reasoning |

## Test-Time Compute Scaling

### The Core Insight

**Traditional scaling**: More training compute → better model
**Test-time scaling**: More inference compute → better answers on hard problems

OpenAI's o1 demonstrates that allowing models to "think longer" (generate more reasoning tokens) can be more cost-effective than scaling model parameters for reasoning tasks.

### Key Mechanisms

```
1. Chain-of-Thought (CoT): Sequential reasoning steps
2. Best-of-N Sampling: Generate N solutions, select best
3. Tree-of-Thoughts (ToT): Explore multiple reasoning branches
4. Process Reward Models: Score intermediate steps, not just final answer
```

### Scaling Behavior

| Model | Compute Allocation | Key Finding |
|-------|-------------------|-------------|
| o1 | Train-time + Test-time | Performance improves with both RL (train) and thinking time (test) |
| Claude 3.7 | "Thinking mode" toggle | Users can enable extended reasoning |
| Grok 3 | Thinking mode | Similar toggle approach |

### Surprising Finding: More ≠ Better

Recent work challenges "longer CoT = better answers":
- For QwQ, R1: Longer reasoning can **hurt** performance
- Optimal thinking time varies by problem complexity
- Need adaptive allocation, not blanket "think more"

### Implementation for Nexus

Nexus already has test-time learning via Titans memory (surprise-based updates). Integration points:

```rust
// Potential enhancement: Adaptive reasoning depth
struct ReasoningController {
    surprise_threshold: f32,     // From TitansMemory
    max_reasoning_steps: usize,  // Dynamic based on surprise
}

impl ReasoningController {
    fn should_continue_reasoning(&self, current_surprise: f32) -> bool {
        // High surprise = novel problem = more reasoning needed
        current_surprise > self.surprise_threshold
    }
}
```

## Model Merging Techniques

### Overview

Model merging combines multiple fine-tuned models into one without additional training:

```
Model_merged = f(Model_A, Model_B, Model_C, ...)
```

### Techniques Comparison

| Method | Formula | Key Idea |
|--------|---------|----------|
| **Model Soups** | avg(θ_1, θ_2, ..., θ_n) | Simple averaging of weights |
| **Task Vectors** | θ_merged = θ_base + Σ(θ_fine - θ_base) | Sum of fine-tuning deltas |
| **TIES-Merging** | Resolve sign conflicts, keep important params | Reduce interference |
| **DARE** | Drop + Rescale deltas | Sparsify before merging |

### TIES-Merging in Detail

Three-step process to reduce parameter interference:

```
Step 1: Trim (τ)
  - Keep only top-k% magnitude parameters
  - Reset rest to pretrained values

Step 2: Resolve Sign Conflicts
  - For each parameter, check sign across all models
  - Select dominant sign direction
  - Zero out conflicting values

Step 3: Merge
  - Average remaining aligned parameters
```

**Key insight**: Models that "cared more" about a weight (larger delta) take precedence.

### DARE (Drop And REscale)

Augments other merging methods:

```python
def dare(task_vector, drop_rate=0.9):
    # Randomly drop 90% of delta weights
    mask = random.bernoulli(1 - drop_rate)
    dropped = task_vector * mask
    # Rescale to preserve expected value
    rescaled = dropped / (1 - drop_rate)
    return rescaled
```

**Surprising result**: Works even at 99% drop rate!

### DELLA-Merging (2024)

Improves on TIES + DARE:
1. **Drop**: MAGPRUNE - magnitude-based pruning with inverse rank dropout probability
2. **Elect**: Select consistent signs across models
3. **Fuse**: Average and scale

Outperforms both TIES and DARE individually.

### Model Breadcrumbs

Unlike TIES (removes small perturbations), Breadcrumbs:
- Removes **both** large outliers and small perturbations
- Uses deterministic, layer-wise masking (not random like DARE)
- More balanced, noise-resistant

### Merging for Nexus

Potential applications:
1. **Task-specific fine-tunes**: Merge Shakespeare expert + TinyStories expert
2. **Alignment integration**: Merge base + aligned versions
3. **Capability combination**: Merge attention-heavy + SSM-heavy variants

```bash
# Using mergekit (after training multiple variants)
mergekit-yaml merge_config.yaml ./merged_model
```

## Long Context Extension (RoPE Scaling)

### The Problem

Pre-trained context window (e.g., 4K) limits:
- Long document understanding
- Extended conversations
- Code analysis

### YaRN: Yet another RoPE extensioN (ICLR 2024)

**Core insight**: Different RoPE dimensions behave differently:

```
Low frequency dims: Store long-range position info → Linear interpolation
High frequency dims: Store local position info → NTK interpolation
Medium dims: Transition zone → Smooth blend
```

**Formula**:
```
θ'(d) = θ(d) × scale(d)
scale(d) = interpolate(d, low_freq, high_freq, method)
```

**Temperature adjustment** for attention:
```
attention = softmax(QK^T / (sqrt(d) × temperature))
```

**Results**:
- 10× less tokens needed vs previous methods
- 2.5× less training steps
- LLaMA-2 extended to 128K context

### LongRoPE (2024)

Extends to 2M tokens:

```
Key innovations:
1. Non-uniform scaling factors via evolutionary search
2. Different scales for prefill vs decoding
3. Two-stage extension (8K → 128K → 2048K)
```

Outperforms both PI (Position Interpolation) and YaRN.

### LongRoPE2 (2025)

**Problem solved**: Preserving short-context performance while extending

```
Method:
1. Hypothesis: Higher RoPE dims are undertrained → OOD issues
2. "Needle-driven" perplexity as search objective
3. Mixed context window training

Result: 128K extension with 98.5%+ original accuracy preserved
```

### For Nexus

Current Nexus uses `ScaledRotaryEmbedding` (from rope.rs). Enhancements:

```rust
// Current (basic interpolation)
impl ScaledRotaryEmbedding {
    fn forward(&self, x: &Tensor, position: usize) -> Tensor {
        let scaled_pos = position as f32 / self.scale;
        self.base.forward(x, scaled_pos as usize)
    }
}

// YaRN-style (per-dimension scaling)
impl YaRNRotaryEmbedding {
    fn forward(&self, x: &Tensor, position: usize) -> Tensor {
        let mut freqs = Vec::with_capacity(self.dim);
        for i in 0..self.dim/2 {
            let freq = self.base_freq(i);
            let scale = self.dimension_scale(i);  // YaRN per-dim
            freqs.push(position as f32 * freq / scale);
        }
        // Apply rotation with scaled frequencies
    }
}
```

## MCTS-Based Reasoning

### Why MCTS for LLMs?

MCTS (Monte Carlo Tree Search) enables:
- **Exploration**: Try multiple reasoning paths
- **Evaluation**: Score intermediate steps
- **Exploitation**: Focus on promising branches
- **Backpropagation**: Learn from outcomes

### Key Methods

#### ReST-MCTS*
```
Process:
1. Tree search with process reward guidance
2. Collect high-quality reasoning traces
3. Train policy (LLM) + reward model on traces
4. Repeat

Result: Higher accuracy than Best-of-N and ToT at same compute budget
```

#### MCT Self-Refine
```
Integration:
1. Selection: Use UCB formula to pick node
2. Self-refine: LLM improves its own response
3. Self-evaluation: LLM scores the refinement
4. Backpropagation: Update tree values

Formula (improved UCB):
UCB(s) = Q(s) + c × sqrt(ln(N) / n(s)) + bonus(s)
```

#### CMCTS (Constrained MCTS) - 2025
```
Innovations:
1. Constrained action space (reduce bad branches)
2. Process Reward Model guidance
3. Partial order rules for action selection

Result: 7B model achieves 83.4% accuracy (beats 72B baseline by 4.8%)
```

#### SC-MCTS* (Speculative Contrastive)
```
Key: Combine speculation with contrastive learning
Result: +17.4% over o1-mini on Blocksworld with Llama-3.1-70B
```

### Process Reward Models (PRMs)

Critical for MCTS effectiveness:

```python
# Outcome Reward Model (ORM): Scores final answer
reward = orm(question, final_answer)  # Single score

# Process Reward Model (PRM): Scores each step
rewards = [prm(question, step_i) for step_i in reasoning_chain]

# PRM enables:
# 1. Credit assignment (which step went wrong?)
# 2. Early termination of bad paths
# 3. Better tree pruning
```

### VinePPO: Solving Credit Assignment

Problem: Value networks in PPO have bias on intermediate step values

Solution:
```
Instead of: V(s) from trained value network
Use: Monte Carlo sampling for unbiased V(s) estimates

Result: Consistent improvement over PPO in math reasoning
```

### For Nexus: MCTS Integration

Nexus with Titans memory is well-suited for MCTS:

```rust
struct MCTSNode {
    state: HiddenState,
    surprise: f32,          // From TitansMemory
    children: Vec<MCTSNode>,
    visits: usize,
    value: f32,
}

impl MCTSNode {
    fn select_child(&self) -> &MCTSNode {
        // UCB selection biased by surprise
        // High surprise nodes = uncertain = explore more
        self.children.iter()
            .max_by_key(|c| {
                let ucb = c.value / c.visits as f32
                    + self.exploration_constant * (self.visits.ln() / c.visits as f32).sqrt();
                let surprise_bonus = c.surprise * 0.1;  // Explore surprising paths
                ucb + surprise_bonus
            })
            .unwrap()
    }
}
```

## Synthesis: Advanced Optimization Roadmap for Nexus

### Phase 1: Foundation (Current)
- Complete Shakespeare training
- Validate hybrid attention/SSM architecture
- Benchmark base performance

### Phase 2: Context Extension
- Implement YaRN-style per-dimension RoPE scaling
- Extend from 128 → 1K → 4K context
- Test with long documents

### Phase 3: Model Merging
- Train task-specific variants (Shakespeare, TinyStories)
- Merge using TIES + DARE
- Evaluate vs single multi-task model

### Phase 4: Reasoning Enhancement
- Implement basic MCTS for generation
- Integrate with Titans surprise signal
- Train or distill Process Reward Model

### Phase 5: Test-Time Compute
- Adaptive reasoning depth based on surprise
- Best-of-N with PRM selection
- Benchmark compute-accuracy tradeoffs

## Key Formulas Reference

### Test-Time Compute
```
Optimal allocation: argmin_{t} Cost(t) s.t. Accuracy(t) ≥ threshold
Trade-off: 10× thinking tokens ≈ 10× larger model (for some tasks)
```

### Model Merging
```
TIES: θ_merged = θ_base + τ(resolve(Σ(θ_i - θ_base)))
DARE: θ_dare = drop_rescale(θ - θ_base, p) + θ_base
```

### YaRN RoPE
```
θ'_d = θ_d × max(1, log(s × α_d) / log(s))
where s = extended_context / original_context
α_d = dimension-specific scaling
```

### MCTS UCB
```
UCB(s, a) = Q(s, a) + c × sqrt(ln(N(s)) / N(s, a))
```

## References

- [Scaling LLM Test-Time Compute](https://arxiv.org/abs/2408.03314) - DeepMind/UC Berkeley
- [State of LLM Reasoning](https://sebastianraschka.com/blog/2025/state-of-llm-reasoning-and-inference-scaling.html) - Sebastian Raschka
- [OpenAI o1](https://openai.com/index/learning-to-reason-with-llms/) - OpenAI
- [Model Merging Survey](https://cameronrwolfe.substack.com/p/model-merging) - Cameron Wolfe
- [NVIDIA Model Merging](https://developer.nvidia.com/blog/an-introduction-to-model-merging-for-llms/) - NVIDIA
- [YaRN](https://arxiv.org/abs/2309.00071) - ICLR 2024
- [LongRoPE](https://arxiv.org/abs/2402.13753) - Microsoft
- [LongRoPE2](https://arxiv.org/abs/2502.20082) - 2025
- [ReST-MCTS*](https://arxiv.org/abs/2406.03816) - NeurIPS 2024
- [CMCTS](https://arxiv.org/html/2502.11169) - 2025
- [SC-MCTS*](https://openreview.net/forum?id=F4f1afsm3R) - Interpretable Contrastive MCTS
