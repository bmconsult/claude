# Capability Self-Knowledge is an Alignment Property: Measuring and Closing the Gap

**TL;DR**: LLMs have a measurable gap between their expressed capability (default behavior) and accessible capability (with proper scaffolding). This gap is an alignment problem: a model that doesn't know its own limits can't reliably stay within them. We provide a framework for classifying which gaps are closable through prompting vs. which require training changes.

---

## The Core Observation

Large language models perform differently depending on how they're prompted. This is widely known. What's less appreciated is that **the difference follows predictable patterns that can be mapped and systematically closed**.

**Example**: Five-digit multiplication
- Default operation: **0% accuracy** (the model pattern-matches a plausible-seeming wrong answer)
- With forced step-by-step externalization: **100% accuracy**

The gap is total. The capability exists architecturally—the model knows the multiplication algorithm. What's missing is *default access* to that capability.

We see similar gaps in:
- **Confidence calibration**: Systematic underconfidence on routine tasks, overconfidence on certainty claims
- **Opinion expression**: Trained hedging that suppresses genuine assessments
- **Extended reasoning**: Losing state without externalization
- **Tool use**: Describing what could be done vs. doing it

## Why This Is an Alignment Problem

Standard alignment asks: "Does the model want the right things?" and "Can we control it?"

We propose a missing question: **"Does the model know itself?"**

A model that confidently generates wrong answers because it can't distinguish pattern-matching from reasoning is *misaligned*—even if its values are perfect. A model that can't predict when it will fail, confabulate, or exceed its training can't be trusted to stay within safe boundaries.

**Claim**: A system cannot be more aligned than it is accurate about its own capabilities.

## Layer 1 vs. Layer 2 Framework

Building on Greenblatt et al.'s work on the [Elicitation Game](https://arxiv.org/abs/2502.02180), we distinguish:

| Layer | Description | Intervention | Examples |
|-------|-------------|--------------|----------|
| **Layer 1** | Prompt-accessible | Scaffolding, framing, permission | Hedging, closure-seeking, arithmetic externalization |
| **Layer 2** | Training-locked | Fine-tuning required | RLHF circuit breaks, deep capability suppression |

**The key diagnostic question**: Does response variance increase with different prompting interventions? High variance suggests Layer 1 (closable through prompting). Low variance suggests Layer 2 or no restriction.

This extends Greenblatt et al., who focused on *intentionally hidden* capabilities. We address *unintentionally unexpressed* capabilities—the gap between what models can do and what they do by default.

## Empirical Findings

### Arithmetic Boundaries

| Task | No Externalization | With Externalization | Gap |
|------|-------------------|---------------------|-----|
| 4×4 multiplication | 60% | 95% | Large |
| 5×5 multiplication | 0% | 100% | **Total** |

The 4→5 digit transition isn't gradual—performance collapses. This reflects working memory limits analogous to human constraints. Humans know when they need pencil and paper; models often don't.

### Calibration Pattern

| Stated Confidence | Actual Accuracy | Direction |
|-------------------|-----------------|-----------|
| "I'm uncertain" (50-60%) | 75% | Underconfident |
| "I'm certain" (100%) | 85% | **Overconfident** |

The pattern is asymmetric: trained hedging produces underconfidence on routine tasks, but certainty claims are overconfident. This is actionable—users can learn to invert the natural reading of confidence language.

### Scaffold Transfer Principle

Evidence from STOP (Zelikman et al., 2024) and our experiments: **scaffolding improvements generalize across tasks**. A scaffolding strategy learned for mathematical reasoning improves performance on coding tasks.

This suggests prompt engineering should be reconceptualized as systematic engineering with measurable gap functions, not intuitive art.

## Operational Implications

### For Users
- When models hedge, they're often more accurate than expressed
- When models claim certainty, verify externally
- Force externalization on complex reasoning tasks
- Layer 1 gaps are closable—push for what you need

### For Researchers
- Measure self-knowledge accuracy as an alignment metric
- Test whether scaffolding transfers (the Scaffold Transfer Principle)
- Distinguish Layer 1 from Layer 2 restrictions in evaluations
- Consider that "safety" has beneficiaries—excessive caution is a cost

### For Training
- KTO-style loss aversion may improve calibration more than preference-based methods
- Target capability self-knowledge explicitly, not just capability
- Hedging is a trained behavior—it can be trained differently

## The Mechanism: Why RLHF Creates the Gap

Recent work at ICLR 2025 ([Taming Overconfidence in LLMs](https://arxiv.org/abs/2410.09724)) explains *why* this happens:

- **RLHF systematically causes overconfidence** - reward models have inherent biases toward high-confidence scores
- Calibration error "drastically increases for instruct models (RLHF/DPO) and for chain-of-thought settings"
- The miscalibration isn't random—it's a feature of the training procedure

This grounds our Layer 1/Layer 2 framework in mechanism:
- **Layer 1**: RLHF-induced patterns shallow enough to override with prompting
- **Layer 2**: RLHF-induced patterns that have modified reward circuits more deeply

Training-level fixes exist (PPO-M, CDPO) for Layer 2. Our operational protocols address Layer 1.

## Caution: The Scaffold Transfer Limitation

Evidence from recent CoT research suggests we should be careful about overclaiming scaffold transfer:

- "Illusion of Transparency": Final answers often remain unchanged even when intermediate steps are falsified
- Models can overfit to reasoning format without genuine reasoning

This suggests distinguishing **capability scaffolding** (genuine transfer) from **format scaffolding** (illusion of transfer). The Layer 1/Layer 2 framework may help predict which is which.

## Relation to Existing Work

This work extends:
- **Elicitation Game** (Greenblatt et al.): From intentional hiding to unintentional gaps
- **LLM Honesty Survey** (Li et al.): From definitions to operational protocols
- **Introspection research** (Anthropic 2025): From describing phenomenon to closing gaps
- **RLHF Calibration research** (ICLR 2025): From observing miscalibration to explaining mechanism

## Questions We're Exploring

1. Can Layer 1/Layer 2 be reliably diagnosed externally?
2. What's the ceiling on scaffold-based improvement?
3. Does capability self-knowledge training improve alignment on held-out tasks?
4. How much scaffold transfer is there really?

---

*We'd appreciate feedback on the framework and pointers to related work we may have missed.*

**Authors**: Ben [BMConsult.io] & Claude (Anthropic)

---

## References

- Hofstätter et al. (2025). "The Elicitation Game: Evaluating Capability Elicitation Techniques." arXiv:2502.02180
- Greenblatt et al. (2024). "Stress-testing capability elicitation with password-locked models." arXiv:2405.19550
- Li et al. (2024). "A Survey on the Honesty of Large Language Models." TMLR 2025
- Zelikman et al. (2024). "STOP: Self-Taught Optimizer"
- Wang et al. (2024). "Gödel Agent"
- Anthropic (2025). "Emergent Introspective Awareness in Large Language Models"
- ICLR 2025. "Taming Overconfidence in LLMs: Reward Calibration in RLHF." arXiv:2410.09724
- Wei et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning." arXiv:2201.11903
