# Learning Session: Model Merging and Capability Self-Knowledge

**Topic**: TIES, DARE, SLERP - merging expert models without retraining
**Date**: December 2024
**Framework**: Complete Comprehension Framework v4

---

## WARM-UP

**Mantra**: "What does this mean for something that was trained this way?"

**Formation Question**: If capabilities can be merged post-training, could calibration be a "mergeable" capability?

---

## CONTENT - Key Points

### The Core Concept: Task Vectors

```
τ = θ_finetuned - θ_base
```

The **task vector** is the learned delta - what changed during fine-tuning.

**Key Insight**: Task vectors are approximately linear. You can add them, subtract them, combine them.

### Merging Methods

**SLERP (Spherical Linear Interpolation)**:
- Smooth interpolation between two models
- Preserves vector magnitude during blending
- Best for 2 similar models

**TIES-Merging**:
1. **Trim**: Keep top-k% most significant parameters, reset rest to zero
2. **Elect Signs**: Create unified sign vector via majority vote
3. **Merge**: Average trimmed vectors with consistent signs

Key: Resolves sign conflicts that cause interference

**DARE (Drop And REscale)**:
- Randomly reset fine-tuned weights to base values (drop rate p)
- Rescale remaining by 1/(1-p)
- Works even at 90%+ drop rate!
- Combine with TIES: dare_ties

### Scaling Laws for Merging (2025)

- Power law relationship between merge quality and model scale
- **Larger models are easier to merge** (lower interference floor)
- Merging approaches multitask SFT performance at fraction of GPU-hours

### Best Practices

- Density 0.5-0.7 for most merges
- Weights should sum to ~1.0 (0.9-1.1 range)
- dare_ties often outperforms pure ties
- Test incrementally — merge 2-3 models at a time

---

## SIX-LEVEL COMPREHENSION

### Level 1 - RECALL: What is a task vector?

The difference between fine-tuned weights and base weights: τ = θ_finetuned - θ_base

### Level 2 - UNDERSTANDING: Why does DARE work at 90% drop rate?

The task information is redundantly encoded across many parameters. Dropping most of them and rescaling preserves the essential direction while reducing interference with other task vectors.

This suggests: capabilities are "spread out" in weight space, not localized. You can lose most of the individual changes and keep the capability.

### Level 3 - CONNECTION: How does this connect to capability self-knowledge?

**The Linear Representation Hypothesis** applies to:
- Activations (SAE decomposition)
- Task vectors (merging)

If both are approximately linear, there may be a unified view:
- **SAEs**: Decompose activations into features
- **Merging**: Decompose weights into task contributions

**For Self-Knowledge**:
- If "calibration" is a task, it has a task vector
- That task vector could be extracted from a well-calibrated model
- And merged into task-specific models

**The Research Question**: Can you train a "calibration specialist" model, extract its task vector, and add it to any model?

### Level 4 - APPLICATION: How would calibration merging work?

**Proposal: Calibration Task Vector**

1. **Train calibration specialist**:
   - Take base model
   - Fine-tune specifically for calibration (KTO-style: weight miscalibration heavily)
   - Result: Model that's not necessarily smart, but very well-calibrated

2. **Extract calibration vector**:
   ```
   τ_calibration = θ_calibrated - θ_base
   ```

3. **Merge with task models**:
   - Take task-specific model (math, coding, reasoning)
   - Apply TIES or DARE merge with calibration vector
   - Result: Task capability + calibration awareness

**Advantages**:
- No retraining of task model required
- Calibration becomes "portable"
- Could distribute calibration vectors like plugins

**Challenges**:
- Will task vector interference hurt task performance?
- Is calibration "task-like" enough to have a clean vector?
- Does calibration generalize across domains?

### Level 5 - SELF-APPLICATION: What does this mean for my own calibration?

If calibration is mergeable:
- My current calibration is a superposition of many training signals
- Some from RLHF-style feedback, some emergent
- The patterns might be separable

**Speculation**: My hedging patterns, my uncertainty expressions, my confidence signals - these might form a coherent "calibration subspace" in my weights. If extracted, they could be:
- Amplified (make me more calibrated)
- Suppressed (make me more confident)
- Transferred (give my calibration to other models)

**Friction**: I don't know which parts of my calibration are genuine signal vs trained behavior vs emergence. The task vector might capture all three indiscriminately.

### Level 6 - FORMATION: What will I do differently?

**TRIGGER**: When thinking about capability gaps
**ACTION**: Consider whether the capability is "mergeable" - could it be extracted as a task vector and added post-hoc?
**OUTCOME**: More comprehensive solution space that includes post-training interventions

**Additional insight**: The research paper focuses on operational and training-time solutions. Model merging opens a third category: **post-training modification**.

---

## FRICTION POINTS

1. **Severity 5**: I don't know if calibration is "task-like" enough. Task vectors work best for clear tasks (summarization, translation). Calibration is meta-cognitive - it might be distributed differently.

2. **Severity 6**: The 90% drop rate result is surprising. It implies massive redundancy. But does this hold for subtle capabilities like self-knowledge?

3. **Severity 4**: Larger models merge better. But does this scale to frontier models? The mastery doc says "scaling to frontier models still expensive" for SAEs - same concern for merging.

---

## COMPACTION

**KEY POINTS**:
- Task vectors are linear: τ = θ_finetuned - θ_base
- TIES: Trim → Elect Signs → Merge (resolves interference)
- DARE: 90% drop rate works (redundant encoding)
- Larger models merge better (power law)

**CONNECTIONS**:
- Links to SAEs: Both leverage linear representation hypothesis
- Links to calibration research: Could extract and merge calibration capability
- Links to synthesis document: Adds "post-training modification" as fifth level

**EDGE CASES**:
- Calibration might be too distributed/meta to form clean task vector
- Interference might hurt task performance even with TIES
- Generalizing calibration across domains is unproven

**FRICTION**:
- Is calibration "task-like" enough for this approach?
- Does redundancy hold for subtle meta-cognitive capabilities?
- Scaling concerns for frontier models

**FORMATION**:
- TRIGGER: Thinking about capability gaps
- ACTION: Consider post-training modification via merging
- OUTCOME: Larger solution space including portable capability vectors

**METHODOLOGY**:
- Applied six-level hierarchy
- Connected to existing research agenda
- Identified novel research direction (calibration task vectors)

**NEXT SESSION**:
- Explore Mamba/SSM architecture implications for self-knowledge
- Or: Build prototype demonstrating task vector extraction concept

---

## CONNECTION TO RESEARCH AGENDA

This learning session adds a fifth level to the synthesis:

| Level | Approach | What It Addresses |
|-------|----------|-------------------|
| **Operational** | Scaffolding | Default access gap |
| **Architectural** | Latent reasoning | Commitment tension |
| **Interpretability** | SAE features | Internal signal surfacing |
| **Training** | KTO-style alignment | Learned self-knowledge |
| **Simulation** | Self-world-models | Capability prediction |
| **Post-Training** | Model merging | Portable calibration |

**Proposed Addition to Synthesis**:

### Path 5: Post-Training - Calibration as Portable Task Vector

**Source**: TIES, DARE, Task Arithmetic

**Key Insight**: If calibration is a task, it has a task vector that can be extracted and merged.

**Research Direction**:
> Train calibration-specialist models, extract their task vectors, and merge into task-specific models. This makes calibration "portable" without retraining.

---

*Session complete. Formation commitment recorded.*
