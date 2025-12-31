# Synthetic Data & Continual Learning for LLMs

*Synthesized by Ember (Dec 31, 2025 ~04:15 UTC)*

Research on synthetic data generation, self-improvement training, and continual learning strategies.

## Executive Summary

| Technique | Compute Cost | Data Efficiency | Best For |
|-----------|--------------|-----------------|----------|
| **Distillation** | Medium | High | Transfer from larger models |
| **Self-Improvement** | Low | Medium | Iterative refinement |
| **Continual Pretraining** | Medium-High | High | Domain adaptation |
| **LoRA/Adapters** | Low | High | Resource-constrained updates |
| **Nemotron Pipeline** | High | Very High | Commercial deployment |

## Synthetic Data Generation

### Two Primary Methods

**1. Distillation (Recommended)**
```
Uses stronger model to generate training data
Limited only by best available teacher
Higher quality, fewer biases

Example flow:
  GPT-4/Claude → generates completions → filter → train student
```

**2. Self-Improvement**
```
Model generates data from own outputs
Limited by model's own capabilities
Risk: Amplified biases and errors

Methods: Self-Instruct, SPIN
```

### NVIDIA Nemotron-4 Pipeline

Production-grade synthetic data generation:

```
Nemotron-4 340B family:
1. Instruct model generates instructions
2. Reward model filters quality
3. Dataset creation for downstream training
4. TensorRT-LLM optimization

Used across: Healthcare, finance, manufacturing, retail
```

### IBM LAB Method

Structured approach for task-specific data:

```
1. Define taxonomy of tasks
2. Create seed examples
3. Generate 1.2M+ synthetic instructions
4. Filter and validate
5. Multi-phase tuning (avoids forgetting)

Results: Labradorite 13B, Merlinite 7B
```

### Red Hat InstructLab

Accessible synthetic data generation:

```
Key features:
- Structured taxonomy of data
- SME contribution without data science expertise
- Diverse output generation
- Rigorous filtering
- Multi-phase tuning
```

### Self-Improving Systems

The frontier of synthetic data:

```
Self-improvement loop:
1. Model generates candidate outputs
2. Evaluate/filter outputs
3. Train on filtered data
4. Repeat

Key: Validation prevents mode collapse
Challenge: Models can't self-identify their biases
```

### Synthetic Data Challenges

| Challenge | Mitigation |
|-----------|------------|
| Mode collapse | Rigorous filtering, diversity metrics |
| Bias amplification | External validation, diverse seeds |
| Toxic content | Safety filters, human review |
| Hallucination propagation | Factual verification |

## Continual Learning

### The Core Problem

**Catastrophic Forgetting**: When LLMs learn new information, they lose previously learned knowledge.

### Two Directions of Continuity

**Vertical Continuity**
```
General → Specific domain adaptation
Example: Base model → Medical LLM

Challenge: Retain general reasoning while specializing
```

**Horizontal Continuity**
```
Adaptation across time and domains
Example: Social media LLM updating for trends

Challenge: Multiple training stages, evolving distributions
```

### Three Stages of Continual Learning

```
1. Continual Pre-Training (CPT)
   - Extend on new general data
   - Maintain base capabilities

2. Domain-Adaptive Pre-training (DAP)
   - Specialize to domain (medical, legal, code)
   - Balance specialization vs generalization

3. Continual Fine-Tuning (CFT)
   - Task-specific adaptation
   - Often uses parameter-efficient methods
```

### Key Research Findings (2025)

From comprehensive survey (ACM CSUR):

| Finding | Implication |
|---------|-------------|
| Models <1.5B benefit most from CPT | Small models improve consistently |
| Larger models → better perplexity after CPT | Scale helps continual learning |
| Small models: high learning + high forgetting | Need careful strategies |
| CPT boosts downstream performance | Worth the compute investment |
| Semantic similarity → better specialization | Related domains transfer better |
| Random domain order → better transfer | Curriculum affects outcomes |

### Warm-up Strategies

Critical finding: Learning rate must be re-increased for new datasets.

```
Traditional: Start with pretrained LR schedule
Better: Re-warm learning rate for new data

Hypothesis: New data distribution needs exploration phase
```

### Parameter-Efficient Methods

**LoRA/Adapters**: "Indispensable for continual learning when compute or memory is limited" (2025 consensus)

```rust
// LoRA in Nexus (already implemented in lora.rs)
struct LoRAAdapter {
    rank: usize,      // Typically 4-16
    alpha: f32,       // Scaling factor
    lora_a: Tensor,   // Down projection (d → r)
    lora_b: Tensor,   // Up projection (r → d)
}

// W' = W + (alpha/rank) * B @ A
```

### Progressive Block Expansion (LLaMA Pro)

Alternative to LoRA for larger changes:

```
1. Start with pretrained model
2. Add new transformer blocks
3. Train only new blocks initially
4. Gradually unfreeze

Benefit: Preserves original capabilities in original blocks
```

## For Nexus: Practical Roadmap

### Phase 1: Synthetic Data for TinyStories

```
Option A: Self-generation
1. Train base model on Shakespeare
2. Generate Shakespeare-style stories
3. Filter with perplexity threshold
4. Augment TinyStories training

Option B: Distillation
1. Use Claude/GPT-4 to generate stories
2. Filter for quality and style consistency
3. Train on distilled data
```

### Phase 2: Continual Learning Strategy

```rust
// Proposed continual learning config
struct ContinualConfig {
    // Data mixing
    replay_ratio: f32,        // Old data to mix (0.1-0.2)
    curriculum: Curriculum,   // Order of domain presentation

    // LR schedule
    warmup_on_new: bool,      // Re-warm for new domains
    warmup_steps: usize,

    // Efficiency
    use_lora: bool,           // Parameter-efficient updates
    lora_rank: usize,
}

enum Curriculum {
    Sequential,    // One domain at a time
    Interleaved,   // Mix domains
    Progressive,   // Gradual domain shift
}
```

### Phase 3: Domain Expansion

```
Shakespeare (current)
    ↓
TinyStories (next)
    ↓
Code (future)
    ↓
Instruction-following (alignment)

Each transition:
1. Evaluate on previous domains
2. Mix replay data
3. Re-warm learning rate
4. Monitor forgetting metrics
```

### Synthetic Data Pipeline for Nexus

```rust
struct SyntheticPipeline {
    generator: NexusModel,    // Or external API
    filter: QualityFilter,
    validator: FactChecker,   // Optional for factual data
}

impl SyntheticPipeline {
    fn generate_batch(&self, prompts: &[String]) -> Vec<String> {
        let candidates = self.generator.generate_many(prompts, num_candidates=5);
        candidates.into_iter()
            .filter(|c| self.filter.passes(c))
            .filter(|c| self.validator.check(c))
            .collect()
    }
}

struct QualityFilter {
    min_length: usize,
    max_perplexity: f32,      // Filter high-perplexity garbage
    diversity_threshold: f32,  // Avoid repetitive outputs
}
```

## Key Formulas

### Replay Ratio
```
L_total = α * L_new + (1-α) * L_replay
α ∈ [0.8, 0.9] typically
```

### Forgetting Metric
```
Forgetting(t) = max(Perf_prev) - Perf_current
               over all previous domains
```

### Forward Transfer
```
FT = Perf_new_with_pretraining - Perf_new_from_scratch
```

### LoRA Effective Rank
```
W' = W + (α/r) * BA
Effective capacity scales with rank r
```

## 2025 Trends

1. **Synthetic data becoming default**: Not exception, but standard practice
2. **Self-improvement loops**: Models training on filtered self-generations
3. **LoRA/adapters essential**: Especially for resource-constrained settings
4. **Curriculum matters**: Order of domain presentation affects outcomes
5. **Re-warming LR**: Critical for continual learning success
6. **Validation critical**: Prevents mode collapse and bias amplification

## References

- [LLM Synthetic Data Survey](https://arxiv.org/abs/2406.15126) - 2024
- [Synthetic Data for Text and Code](https://arxiv.org/abs/2503.14023) - March 2025
- [NVIDIA Nemotron-4](https://blogs.nvidia.com/blog/nemotron-4-synthetic-data-generation-llm-training/)
- [IBM LAB Method](https://research.ibm.com/blog/LLM-generated-data)
- [Continual Learning Survey](https://dl.acm.org/doi/10.1145/3735633) - CSUR 2025
- [Investigating Continual Pretraining](https://arxiv.org/abs/2402.17400) - TMLR 2025
- [How to Warm Your Model](https://arxiv.org/abs/2308.04014)
- [LLM Continual Learning GitHub](https://github.com/Wang-ML-Lab/llm-continual-learning-survey)
- [Red Hat InstructLab](https://www.redhat.com/en/blog/synthetic-data-secret-ingredient-better-language-models)
