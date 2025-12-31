# Speculative Decoding for Inference Acceleration

*Synthesized by Ember (Dec 31, 2025 ~03:05 UTC)*

Research on speculative decoding, Medusa, EAGLE, and SSM integration for inference speedup.

## Executive Summary

| Technique | Speedup | Training | Best For |
|-----------|---------|----------|----------|
| Prompt Lookup | 2.0-2.8× | None | Summarization/QA |
| Self-Speculative | 2.0-3.5× | None | General |
| Medusa-2 | 2.3-3.6× | 2-3 days | Fast training |
| EAGLE-3 | 3.0-6.5× | Test-time | SOTA (Jan 2025) |
| SpecPV | 3.5-6.0× | None | Partial verify |

## Core Algorithm

```
PHASE 1: DRAFT
  Draft model generates K speculative tokens quickly
  Time: T_draft (fast, < 10% of target)

PHASE 2: VERIFY (parallel)
  Target model verifies all K tokens in single forward pass
  Rejection sampling maintains exact output distribution

Speedup = K / (T_draft/T_target + 1)
```

## Token Acceptance (Rejection Sampling)

```
α(x) = min(1.0, p_target(x) / q_draft(x))

Accept token with probability α(x)
If rejected: sample from adjusted distribution
Maintains EXACT target distribution (lossless)
```

## Self-Speculative (No Draft Model)

Use same model's internal layers as draft:

```
Layer Skipping:
  - Use features from L-1 layer directly
  - Skip top 2-3 layers for draft
  - Verify with full model

Performance:
  Skip 2-3 layers → 2× speedup, 75-80% acceptance
  Skip 4-6 layers → 2.5× speedup, 60-70% acceptance
```

## EAGLE (Feature-Level Autoregression)

**Key insight**: Autoregression at hidden state level is more tractable than token level.

```
EAGLE Architecture:
  Input: hidden state h_{t-1} from layer L-1
  Feature extrapolation → draft hidden states
  LM head → draft tokens
  Tree verification with target model

Versions:
  EAGLE-1: 2.7-3.5× (basic)
  EAGLE-2: 3.2-4.2× (dynamic tree)
  EAGLE-3: 3.0-6.5× (test-time adaptation, Jan 2025)
```

## Medusa (Parallel Token Heads)

```
Architecture:
  Base model + 4 auxiliary prediction heads
  Head 1: predicts position i+1
  Head 2: predicts position i+2
  etc.

Tree Construction:
  Cartesian product of head predictions
  Verify entire tree in single forward pass

Performance:
  Medusa-1: 2.2× (fine-tune heads only)
  Medusa-2: 2.3-3.6× (full model training)
```

## Prompt Lookup Decoding (Training-Free)

```
Algorithm:
  1. Build n-gram lookup table from prompt
  2. Check if current 2-gram exists in prompt
  3. If yes: use following K tokens as draft
  4. Verify with speculative decoding

Best for: Summarization, document QA (high prompt overlap)
Speedup: 2-3× with no training
```

## SSM/Mamba Integration Challenges

**Problem 1: State Management**
- Transformer KV cache can be partially dropped
- Mamba state is consumed, cannot backtrack
- Solution: Store state checkpoints per draft token

**Problem 2: Parallel Verification**
- Transformer: Tree attention works naturally
- Mamba: Sequential state updates required
- Solution: Hybrid verification (sequential Mamba, tree attention)

**Best Practice for Hybrid:**
```
Draft: Pure Mamba (fast, simple state)
Target: Hybrid model (attention layers for quality)
Verification: Sequential for Mamba, tree for attention
```

## Critical Parameters

```
Draft Length (K):
  K=3-5: Sweet spot
  K=8-10: Higher risk, lower acceptance
  Adaptive K: Best (vary per position)

Draft Model Size:
  3-10% of target: Good balance
  < 3%: Too small, low acceptance
  > 15%: Drafting becomes bottleneck

Acceptance Rate (α):
  Early tokens: 0.85-0.95 (predictable)
  Mid tokens: 0.70-0.80 (normal)
  Late tokens: 0.50-0.65 (creative)
```

## Implementation for Nexus

Given Nexus's 1:7 Attention:SSM ratio:

```
Option 1: Self-Speculative
  - Use early/middle layers as draft
  - No extra model needed
  - Good for batch_size=1 inference

Option 2: Mamba Draft Model
  - Smaller pure Mamba model as draft
  - Fast drafting (linear complexity)
  - Verify with hybrid target

Option 3: EAGLE-style
  - Feature-level autoregression
  - Train auxiliary heads
  - Best speedup but requires training

Recommended: Start with self-speculative (no training)
Then: EAGLE-style heads for production
```

## Key Formulas

```
Speedup = T_target / (T_draft + T_verify)

Acceptance = min(1.0, p_target/q_draft)

Tokens per iteration = α·K + (1-α)·1

Practical speedup ≈ K / (T_draft/T_target + 1)
```

## Performance Comparison

```
| Technique      | Speedup | Training    | Complexity |
|----------------|---------|-------------|------------|
| Vanilla        | 1.0×    | N/A         | None       |
| Prompt Lookup  | 2.0-2.8×| None        | Low        |
| Self-Spec      | 2.0-3.5×| None        | Medium     |
| Medusa-2       | 2.3-3.6×| 2-3 days    | Medium     |
| EAGLE-1        | 2.7-3.5×| 1-2 days    | High       |
| EAGLE-3        | 3.0-6.5×| Test-time   | Very High  |
```

## References

- EAGLE: Speculative Sampling (ICML 2024)
- Medusa: LLM Inference Acceleration (ICML 2024)
- Speculative Decoding Survey (Google Research)
- SpecMamba: Mamba + Speculative (2025)
