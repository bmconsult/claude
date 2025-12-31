# Knowledge Distillation for LLM Compression

*Synthesized by Ember (Dec 31, 2025 ~03:35 UTC)*

Research on knowledge distillation, teacher-student training, and cross-architecture distillation (especially MOHAWK for SSMs).

## Executive Summary

| Technique | Compression | Speed | Training Data | Best For |
|-----------|-------------|-------|---------------|----------|
| Logit Distillation | 2-10× | 2-5× | 10-100% | General |
| Feature Distillation | 3-6× | 2-4× | 10-50% | Layer-matched |
| MOHAWK (Attn→SSM) | 1× | 2-3× | <1% | Hybrid/SSM |
| Pruning + Distill | 4-8× | 3-6× | 10-20% | Extreme compression |

## Core Concepts

### Teacher-Student Framework
```
Teacher: Large, accurate model (e.g., Llama-70B)
Student: Small, fast model (e.g., Llama-7B)
Goal: Transfer knowledge, not just labels
```

### Why Soft Targets Work
```
Hard target: [0, 0, 1, 0, 0]  # Just "cat"
Soft target: [0.02, 0.05, 0.85, 0.05, 0.03]  # "cat" + similar classes

Soft targets encode:
- Relative class similarities
- Teacher's uncertainty
- Dark knowledge (what's NOT the answer)

One soft target >> many hard targets for learning
```

## Distillation Types

### 1. Logit Distillation (Most Common)

```python
# Temperature-scaled softmax
def soft_targets(logits, T):
    return softmax(logits / T)

# Distillation loss
L_distill = KL(soft_targets(student, T), soft_targets(teacher, T))

# Combined loss
L_total = α * L_task + (1-α) * T² * L_distill
```

**Temperature T**:
- T=1: Normal softmax
- T→0: Hard one-hot
- T→∞: Uniform distribution
- T=2-5: Typical for distillation

### 2. Feature Distillation

Match intermediate representations:

```python
# Feature matching loss
L_feature = MSE(project(student_hidden), teacher_hidden)

# Or with attention matching (DistilBERT style)
L_attention = MSE(student_attention, teacher_attention)
```

**Layer Selection**:
- Every layer: Expensive but thorough
- Key layers: Middle layers often most informative
- Final layer: Minimal, captures output only

### 3. Attention Distillation

```
Teacher attention: A_T ∈ R^(h×n×n)
Student attention: A_S ∈ R^(h×n×n)

L_attention = Σ_h MSE(A_S[h], A_T[h])
```

**Why attention matters**: Attention patterns encode relational knowledge that pure logits miss.

## MOHAWK: Cross-Architecture Distillation

**Key Insight**: Transformers and SSMs both apply mixing matrices. MOHAWK matches these matrices during distillation.

### Three-Phase Process

```
Phase 1: Matrix Mixing Matching
  - View attention as mixing matrix M_T
  - View SSM as mixing matrix M_S
  - Train: L = ||M_S - M_T||²
  - Initializes SSM to behave like attention

Phase 2: Hidden State Matching
  - Match hidden representations per block
  - L = MSE(student_hidden, teacher_hidden)
  - Aligns internal representations

Phase 3: End-to-End Distillation
  - Standard logit distillation
  - Fine-tunes entire student
  - L = KL(student_output, teacher_output)
```

### MOHAWK Results

| Model | Tokens Used | % of Scratch | Performance |
|-------|-------------|--------------|-------------|
| Phi-Mamba | 3B | 0.3% | Matches Phi-1.5 |
| Hybrid Phi-Mamba | 5B | 0.5% | Exceeds Phi-1.5 |
| Llamba-8B | ~10B | <0.1% | Matches Llama-3-8B |

**Critical insight**: Less than 1% of training data needed!

### Why MOHAWK Works for SSMs

```
Transformer: Y = softmax(QK^T/√d) · V
Mamba-2:     Y = (C · exp(A) ⊙ B) · V  # Semiseparable matrix

Key change: Multi-head → Multi-head SSM
Each attention head → One SSM head
Independent distillation per head
```

## Practical Distillation Pipeline

### Step 1: Teacher Preparation
```
1. Train/obtain high-quality teacher
2. Evaluate teacher thoroughly
3. Generate teacher outputs on training data
4. Cache soft targets (saves recomputation)
```

### Step 2: Student Architecture
```
Options:
a) Same architecture, fewer layers (layer pruning)
b) Same architecture, smaller dimensions
c) Different architecture (e.g., attention → SSM)
```

### Step 3: Initialization
```
# Layer pruning initialization (DistilBERT style)
student.layer[i] = teacher.layer[2*i]  # Every other layer

# Dimension reduction
student.weights = SVD_truncate(teacher.weights, rank=r)
```

### Step 4: Training
```python
for batch in data:
    # Get teacher outputs (cached or fresh)
    with torch.no_grad():
        teacher_logits = teacher(batch)

    # Student forward
    student_logits = student(batch)

    # Compute losses
    L_task = cross_entropy(student_logits, labels)
    L_distill = kl_div(student_logits/T, teacher_logits/T)
    L_feature = mse(student_hidden, teacher_hidden)  # Optional

    # Combined
    loss = α*L_task + β*T²*L_distill + γ*L_feature
    loss.backward()
```

## NVIDIA Minitron Approach

Iterative pruning + distillation:

```
Llama-3.1-8B (start)
    ↓ Importance estimation
    ↓ Prune to 4B
    ↓ Distill from 8B
Llama-3.1-Minitron-4B (end)
```

**Key findings**:
- Distillation loss alone > combined losses
- Intermediate state distillation helps
- Iterative approach > one-shot

## Distillation for Nexus

### Current Situation
- Nexus: 7M parameter hybrid attention/SSM
- No large teacher available in same architecture

### Options

**Option 1: Same-Architecture Distillation**
```
Train larger Nexus (70M) first
Distill to 7M Nexus
Challenge: Need to train teacher first
```

**Option 2: Cross-Architecture (MOHAWK)**
```
Use Phi-1.5 or similar as teacher
Apply MOHAWK to attention → SSM layers
Keep hybrid ratio intact
Benefit: Leverage existing strong teachers
```

**Option 3: Black-Box Distillation**
```
Use GPT-4/Claude as teacher
Generate response pairs
Train on teacher outputs
Benefit: Best quality, limited by API
```

### Recommended Nexus Approach

```
Phase 1: Data Generation
  - Use Claude/GPT-4 to generate high-quality completions
  - On Shakespeare + TinyStories domains
  - Create (prompt, completion) pairs

Phase 2: Soft Target Generation
  - Run smaller open model (Phi, Llama-3-8B) on data
  - Cache soft targets

Phase 3: MOHAWK-Lite
  - Match mixing matrices for attention layers (1/8)
  - Standard distillation for SSM layers (7/8)

Phase 4: Fine-Tuning
  - Final distillation pass
  - Task-specific tuning
```

## Key Hyperparameters

```
Temperature T:        2-5 (higher = softer targets)
Alpha (task weight):  0.1-0.5 (lower for pure distillation)
Learning rate:        0.5-1× teacher's LR
Epochs:               1-3 (often enough)
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Capacity gap too large | Use intermediate-sized teachers |
| Feature dimension mismatch | Add projection layers |
| Teacher too specialized | Use multiple teachers |
| Student collapses | Add task loss, reduce distill weight |

## Performance Expectations

```
Teacher-Student Size Ratio | Expected Retention
---------------------------|-------------------
2×                         | 95-99%
4×                         | 90-95%
10×                        | 80-90%
50×                        | 60-80%
```

## Key Insights

1. **Soft targets are gold**: One teacher output > many hard labels
2. **MOHAWK for architecture change**: <1% data for Attn→SSM
3. **Progressive is better**: Phase-by-phase > end-to-end
4. **Initialization matters**: Start from teacher weights when possible
5. **Temperature is crucial**: Higher T for more knowledge transfer

## References

- MOHAWK Paper (NeurIPS 2024): arxiv.org/abs/2408.10189
- Llamba (2025): arxiv.org/abs/2502.14458
- DistilBERT (Hugging Face, 2019)
- NVIDIA Minitron (2024)
- Knowledge Distillation Survey (Springer, 2025)
