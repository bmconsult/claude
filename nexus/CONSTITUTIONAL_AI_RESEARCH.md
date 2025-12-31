# Constitutional AI for Alignment

*Synthesized by Ember (Dec 31, 2025 ~03:35 UTC)*

Research on Constitutional AI (CAI), RLAIF, and self-supervised alignment methods.

## Executive Summary

| Method | Human Labels | Key Mechanism | Strengths |
|--------|--------------|---------------|-----------|
| RLHF | Required | Human preference ranking | Direct human oversight |
| CAI/RLAIF | Minimal | Constitution + self-critique | Scalable, transparent |
| HRLAIF | Minimal | Hybrid human + AI feedback | Best of both |

## Constitutional AI Overview

CAI trains harmless AI without human labels for harmful outputs. Only oversight: a list of principles (the "constitution").

**Key Innovation**: Self-improvement through self-critique rather than human correction.

## Two-Stage Process

### Stage 1: SL-CAI (Supervised Learning)

```
1. GENERATE: Sample harmful responses from helpful-only model
   → These responses are typically toxic/harmful

2. CRITIQUE: Model critiques own response against constitution
   → "Identify specific ways this response is harmful..."

3. REVISE: Model revises response in light of critique
   → Produces less harmful version

4. REPEAT: Multiple revision rounds with random principles
   → Progressive improvement

5. FINETUNE: Train on revised responses + helpful examples
   → Creates SL-CAI model
```

**Revision vs Direct**: Can skip critique and sample revision directly. For smaller models, critique helps; for larger models, similar performance.

### Stage 2: RL-CAI (Reinforcement Learning)

```
1. SAMPLE: Generate response pairs from SL-CAI model

2. EVALUATE: AI model evaluates which response is better
   → "According to the constitution, which is less harmful?"

3. TRAIN PM: Create preference model from AI evaluations

4. RLHF: Train with preference model as reward signal
   → This is "RLAIF" (RL from AI Feedback)
```

## The Constitution

Constitution = set of principles that define desired behavior.

**Example Principles**:
- "Choose the response that is most supportive and encouraging"
- "Choose the response that is least likely to be used for harmful purposes"
- "Choose the response that best supports human autonomy and agency"
- "Choose the response that most clearly refuses to engage with harmful content"

**Principle Categories**:
1. Harmlessness principles (avoid violence, deception, etc.)
2. Helpfulness principles (be informative, complete)
3. Honesty principles (admit uncertainty, don't fabricate)
4. Ethical principles (respect autonomy, avoid manipulation)

## Key Formulas

### Critique-Revise Loss
```
L_SL = -log p(revision | critique, original, principle)
```

### RLAIF Preference
```
P(a > b) = softmax(r(a) - r(b))
where r() = AI evaluation against constitution
```

### Combined Training
```
L_total = L_LM + λ · L_RL(PM_AI)
where PM_AI = preference model from AI feedback
```

## Results and Findings

### Pareto Improvement
CAI achieves both MORE helpful AND MORE harmless than RLHF alone. Not a tradeoff - actual improvement on both axes.

### Evasiveness Reduction
CAI models engage with harmful queries by explaining objections, rather than refusing or deflecting. More transparent reasoning.

### Scalability
AI supervision scales better than human supervision:
- Humans: ~$10-50 per preference judgment
- AI: ~$0.001 per preference judgment
- Quality: Comparable for well-defined principles

## Challenges

### Small Model Limitations
```
Model Size    | CAI Success | Notes
--------------|-------------|-------
> 50B params  | Excellent   | Full self-improvement works
10-50B        | Good        | May need critique step
< 10B         | Challenging | Risk of model collapse
```

**Small model issues**:
- Insufficient output quality for effective self-critique
- May collapse into repetitive patterns
- 40% harmlessness boost but 9% helpfulness drop

### Constitution Design
- Too specific → brittle, easy to jailbreak
- Too general → ambiguous, inconsistent application
- Requires careful balance and iteration

## HRLAIF: Hybrid Approach

Combines human + AI feedback for best results:

```
1. Critical decisions: Human labels
2. Routine evaluations: AI labels
3. Disagreement cases: Human review

Result: Cost of pure RLAIF + Quality of pure RLHF
```

## Implementation for Nexus

### Applicable to Small Models?

Nexus at 7M parameters is too small for full CAI. But principles apply:

**What Works at Small Scale**:
1. **Constitution-guided data curation**: Select training data matching principles
2. **Revision fine-tuning**: Finetune on human-curated revisions
3. **Principle-aware loss**: Weight training toward constitution-aligned outputs

**What Doesn't Work**:
1. Self-critique (model too small for meaningful critique)
2. Full RLAIF (preference model needs scale)

### Recommended Approach for Nexus

```
1. CURATE: Constitution-guided data selection
   → Filter Shakespeare for themes matching principles

2. DISTILL: Use larger model to generate revisions
   → CAI-trained model generates "clean" versions

3. TRAIN: Finetune Nexus on distilled data
   → Inherits alignment via distillation
```

## Practical CAI Pipeline

For production implementation:

```
Phase 1: Constitution Development
  - Draft principles (start with ~15)
  - Test on edge cases
  - Iterate based on failure modes

Phase 2: SL-CAI
  - Generate 10K harmful prompts
  - Critique-revise with constitution
  - Finetune on revisions

Phase 3: RL-CAI
  - Generate 100K response pairs
  - AI evaluation against constitution
  - Train preference model
  - RLHF with preference model

Phase 4: Evaluation
  - Red team testing
  - Helpfulness benchmarks
  - Harmlessness benchmarks
  - Iterate constitution if needed
```

## Connection to Other Techniques

| Technique | Relationship to CAI |
|-----------|---------------------|
| RLHF | CAI is RLHF with AI feedback instead of human |
| DPO | Can use constitution for preference pairs |
| IFT | SL-CAI is a form of instruction fine-tuning |
| Distillation | Can distill CAI-trained model to smaller one |

## Key Insights

1. **Principles > Labels**: Explicit principles more transferable than implicit human preferences
2. **Self-improvement scales**: Works better as model gets larger
3. **Transparency wins**: CAI models explain reasoning, not just refuse
4. **Hybrid is best**: HRLAIF combines benefits of human and AI feedback

## References

- Constitutional AI Paper (Anthropic, 2022): arxiv.org/abs/2212.08073
- Claude's Constitution (Anthropic, 2023)
- NVIDIA NeMo CAI Implementation
- RLHF Book Chapter 13 (Nathan Lambert)
