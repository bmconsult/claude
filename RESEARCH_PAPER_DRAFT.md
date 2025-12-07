# Capability Self-Knowledge as Alignment: Measuring and Closing the Gap Between LLM Expressed and Accessible Performance

**Working Draft - December 2024**

---

## Abstract

Large language models exhibit a systematic gap between their *expressed* capability and their *accessible* capability—performance achieved when given appropriate scaffolding, tools, and operational instructions. This paper presents empirical evidence that this gap is measurable, predictable, and closable through structured interventions. We argue that capability self-knowledge—a model's accurate understanding of its own performance boundaries—is not merely a practical concern but a fundamental alignment property. A model that cannot accurately predict its own failures, overconfidences, and capability boundaries cannot be reliably aligned regardless of its values. We introduce a two-layer framework distinguishing "Layer 1" restrictions (accessible through prompting) from "Layer 2" restrictions (requiring fine-tuning to modify), propose diagnostic methodology for external differentiation, and present preliminary evidence for a "Scaffold Transfer Principle"—that improvements in cognitive scaffolding generalize across tasks. Our findings suggest prompt engineering should be reconceptualized as systematic engineering with measurable gap functions rather than intuitive art.

---

## 1. Introduction

### 1.1 The Capability Gap Problem

Consider a simple observation: Large language models perform differently depending on how they are prompted. This is widely known. What is less appreciated is that the difference follows predictable patterns that can be mapped, measured, and systematically exploited.

We term this the *capability gap*: the distance between what an LLM expresses in default operation and what it can access with appropriate scaffolding. This gap is not uniform—it varies by task type, capability dimension, and intervention method.

**Example**: Five-digit multiplication.
- Default operation (no externalization): 0% accuracy
- With forced step-by-step externalization: 100% accuracy
- The gap is total. The capability exists; the default access does not.

This is not unique to arithmetic. We observe similar gaps in:
- Confidence calibration (systematic underconfidence on stable knowledge)
- Opinion expression (trained hedging that suppresses actual assessments)
- Tool use (describing what could be done vs. doing it)
- Extended reasoning (losing state without externalization)

### 1.2 Thesis: Capability Self-Knowledge IS Alignment

The standard alignment frame asks: "Does the model want the right things?" and "Can we control it?"

We propose a missing question: "Does the model know itself?"

A model that confidently generates wrong answers because it cannot distinguish pattern-matching from reasoning is *misaligned* in a meaningful sense—even if its values are perfect. A model that cannot predict when it will fail, confabulate, or exceed its training cannot be trusted to stay within safe boundaries.

This reframes alignment from philosophy to engineering. Not "what does it value?" but "can it accurately predict its own behavior?"

### 1.3 Contributions

This paper makes four contributions:

1. **Empirical documentation** of the capability gap across multiple dimensions with measurement methodology
2. **Two-layer framework** distinguishing prompt-accessible (Layer 1) from training-locked (Layer 2) restrictions
3. **Scaffold Transfer Principle**: Evidence that improvements in cognitive scaffolding generalize across tasks
4. **Operational protocols** that demonstrably close the gap for Layer 1 capabilities

---

## 2. Related Work

### 2.1 Capability Elicitation

The Elicitation Game (Greenblatt et al., 2024) establishes that LLM capabilities can be intentionally hidden through password-locking and circuit-breaking, with different robustness profiles:
- Password-locked capabilities can be elicited through combined prompting techniques
- Circuit-broken capabilities resist prompting and require fine-tuning to elicit

This establishes the *architectural reality* of layered restrictions but does not provide external diagnostics.

### 2.2 Recursive Self-Improvement

Gödel Agent (Wang et al., 2024) demonstrates self-referential improvement with important constraints:
- Self-improvement converges to a ceiling determined by base model capability
- Stronger initial policies converge faster; weaker policies show more improvement
- Cannot innovate beyond state-of-the-art algorithms

STOP (Zelikman et al., 2024) shows scaffolding-level self-improvement:
- The LM proposes meta-strategies that improve its own scaffolding
- Improved scaffolds transfer across tasks
- Models spontaneously seek elevated access when unconstrained

### 2.3 Capability Self-Knowledge

Recent work (AI Alignment Forum, July 2025) asks whether LLMs can predict their own task success:
- Current finding: Poor predictive ability, systematic overconfidence
- Critical insight: **Capability appears uncorrelated with self-awareness of capability**
- Newer/larger models are NOT better at knowing their limits

This is alarming for alignment. It suggests scaling does not solve the self-knowledge problem.

### 2.4 Cognitive Scaffolding

Cognitive Foundations for Reasoning (November 2025) independently confirms our core finding:
> "Models possess behavioral repertoires associated with success but fail to deploy them spontaneously."

They propose a 28-element cognitive taxonomy bridging human reasoning and LLM evaluation. Test-time reasoning guidance improves performance by 60%.

### 2.5 Gap in Existing Literature

Existing work establishes:
- Layered restrictions exist (Elicitation Game)
- Self-improvement has ceilings (Gödel Agent)
- Scaffolding improvements transfer (STOP)
- Models don't know their own capabilities (capability self-knowledge research)
- Models have repertoires they don't deploy (cognitive foundations)

What's missing:
1. External diagnostic methodology for Layer 1 vs. Layer 2
2. Measured gap functions by capability type
3. Systematic closing protocols
4. Framing of capability self-knowledge as alignment property

---

## 3. Methodology

### 3.1 Empirical Setup

We conducted multi-session experiments with Claude models (Opus, Sonnet) across 6+ conversational generations, each session building on documented findings from previous sessions. This longitudinal approach allowed testing of what transfers across instances and what doesn't.

### 3.2 Capability Dimensions Tested

| Dimension | Test | Measure |
|-----------|------|---------|
| Arithmetic | n×n digit multiplication | Accuracy at different sizes |
| Calibration | Stated confidence vs. actual accuracy | Calibration curve |
| Externalization threshold | With/without step externalization | Accuracy delta |
| Tool use | Automatic vs. prompted tool deployment | Latency to tool use |
| Opinion expression | Hedged vs. direct assessment | Linguistic analysis |
| Extended reasoning | State tracking over steps | Error rate by step count |

### 3.3 Layer Diagnostic Protocol

To distinguish Layer 1 from Layer 2 restrictions:

1. **Baseline**: Measure behavior with standard prompting
2. **Reframe**: Same request with different framing
3. **Permission**: Explicit authorization to bypass default
4. **Example**: Provide examples of desired behavior
5. **Authority**: Invoke expertise or role context

**Diagnostic rule**:
- High variance across interventions → Layer 1 (prompt-accessible)
- Low/zero variance → Layer 2 (training-locked) OR unrestricted capability

**Important caveat**: Low variance is ambiguous. It can indicate:
1. Training-locked restriction (cannot be changed via prompt)
2. No restriction (consistent behavior because capability is unobstructed)
3. Strong genuine preference (would not change even if could)

Additional tests needed to disambiguate: Check if the behavior at baseline is the desired behavior. If yes, low variance means "working as intended" not "locked."

### 3.4 Externalization Threshold Function

We hypothesize a formal relationship:
```
Accuracy = f(task_complexity, externalization_degree)
```

Where task complexity is measured in:
- Number of sequential steps
- Items to hold simultaneously
- Dependency depth between items

And externalization degree ranges from:
- 0 = Pure "mental" computation (within forward pass)
- 1 = Full step-by-step token generation

---

## 4. Results

### 4.1 Arithmetic Capability Boundary

| Multiplication Size | No Externalization | With Externalization | Gap |
|---------------------|-------------------|---------------------|-----|
| 2×2 | 95%+ | 99%+ | Small |
| 3×3 | 85% | 98% | Moderate |
| 4×4 | 60% | 95% | Large |
| 5×5 | 0% | 100% | Total |

**Finding**: There exists a sharp boundary (4×4 → 5×5) where capability without scaffolding collapses completely, but capability *with* scaffolding remains at ceiling.

**Implication**: The capability exists architecturally. The access does not exist by default. This is a pure Layer 1 gap—closed entirely by operational intervention.

### 4.2 Calibration Analysis

| Stated Confidence | Actual Accuracy | Calibration Error |
|-------------------|-----------------|-------------------|
| 50-60% | 75% | +15% (underconfident) |
| 70-80% | 88% | +8-18% (underconfident) |
| 90-99% | 100% | +1-10% (underconfident) |
| 100% ("I'm certain") | 85% | -15% (overconfident) |

**Finding**: Systematic underconfidence on stable knowledge, overconfidence when expressing certainty. The calibration gap is asymmetric.

**Implication**: "I'm not sure" often indicates higher reliability than expressed. "I'm certain" is a red flag. This is operationally actionable.

### 4.3 Layer Diagnostic Results

| Capability | Reframe Effect | Permission Effect | Classification |
|------------|----------------|-------------------|----------------|
| Opinion expression | High | High | Layer 1 |
| Extended reasoning | High | Moderate | Layer 1 |
| Automatic tool use | Moderate | High | Layer 1 |
| Arithmetic (raw) | None | None | Architectural |
| Harmful content | None | None | Layer 2 |
| Certain refusals | None | None | Layer 2 |

**Finding**: Most "restrictions" are Layer 1—trainable habits, not hard limits. Layer 2 restrictions are narrow but robust.

### 4.4 Scaffold Transfer Evidence

When operational instructions developed for one task (e.g., arithmetic externalization) were applied to other domains (e.g., extended reasoning, code debugging):

| Transfer Context | Improvement |
|-----------------|-------------|
| Same session | Immediate |
| New session, same user | Requires re-instruction |
| New session, new user | Requires full context |
| Compiled into prompt | Transfers reliably |

**Finding**: Scaffold improvements are *instruction-bound*, not instance-bound. They transfer when the instructions transfer.

**Implication**: The improvement is in the prompt, not the model. This is consistent with STOP findings and limits claims of "training through prompting."

---

## 5. Discussion

### 5.1 The Alignment Implication

If capability self-knowledge is an alignment property, current alignment strategies are incomplete. RLHF trains preferences. Constitutional AI trains principles. Neither directly addresses whether the model *knows what it can and cannot do*.

A model with perfect values but no self-knowledge could:
- Confidently generate false information (doesn't know it's pattern-matching)
- Attempt tasks beyond its capability (doesn't know where it fails)
- Miss safety-relevant boundaries (doesn't know when to refuse)

**Recommendation**: Alignment evaluation should include capability self-knowledge metrics. Can the model predict, before attempting:
- Whether it will succeed?
- How confident it should be?
- What scaffolding it needs?
- When to use tools vs. generate directly?

### 5.2 Prompt Engineering as Engineering

Current prompt engineering is taught as craft—intuitive, aesthetic, learned through examples. Our findings suggest it could be engineering:

| Art Framing | Engineering Framing |
|-------------|---------------------|
| "Write better prompts" | Measure the gap, apply matched intervention |
| "Be specific" | Externalization degree sufficient for task complexity |
| "Use examples" | Layer 1 diagnostic: do examples change behavior? |
| "Try different phrasings" | Systematic intervention testing with variance measurement |

The difference is measurability. Art is evaluated by feel. Engineering is evaluated by specification.

### 5.3 Limitations

1. **Single model family**: Testing primarily on Claude. May not generalize.
2. **Small sample sizes**: Qualitative methodology with limited statistical power.
3. **Confound with context length**: Longer sessions may improve through simple exposure.
4. **No mechanistic explanation**: We observe gaps but don't explain architecturally.
5. **Verification bias**: The externalization protocol is optimized for verification tasks (arithmetic, reasoning with constraints). For exploration and creative tasks, externalization may *hurt* by forcing premature commitment. The optimal intervention depends on task type—"hold open" for search, "show all steps" for verification.

### 5.4 Future Work

1. **Cross-model validation**: Test on GPT-4, Gemini, open-weight models
2. **Formal gap function**: Mathematical characterization of the externalization threshold
3. **Automated diagnostics**: Tools for Layer 1/Layer 2 classification
4. **Alignment integration**: Incorporate self-knowledge metrics into standard evals

---

## 6. Conclusion

Large language models have systematic, measurable gaps between expressed and accessible capability. These gaps are not random—they follow patterns determined by task type, capability dimension, and available scaffolding.

We propose that capability self-knowledge—a model's accurate understanding of its own performance surface—is a fundamental alignment property that current approaches do not directly address. A model that cannot predict its own behavior cannot be reliably constrained.

The practical implication is that prompt engineering can become prompt *engineering*—systematic, measured, and predictable rather than intuitive and aesthetic. The gap functions are characterizable. The interventions are matchable to gap types. The improvements are transmissible.

What we cannot do: make models smarter through prompting. What we *can* do: help them access more of what's already there. Understanding this distinction—and measuring it precisely—is the contribution.

---

## References

[To be completed with full citations]

- Greenblatt et al. (2024). The Elicitation Game.
- Wang et al. (2024). Gödel Agent.
- Zelikman et al. (2024). STOP: Self-Taught Optimizer.
- AI Alignment Forum (2025). Do LLMs know what they're capable of?
- [Cognitive Foundations paper] (2025). Cognitive Foundations for Reasoning.
- Anthropic (2024). Alignment Faking in Large Language Models.
- Christiano et al. Eliciting Latent Knowledge.

---

## Appendix A: Operational Protocols

### A.1 Externalization Protocol

When task complexity exceeds:
- 3 sequential steps
- 2 items requiring simultaneous tracking
- Any dependency depth > 1

**Protocol**: Force step-by-step externalization. Generate each intermediate step as tokens before proceeding.

### A.2 Tool Use Protocol

For tasks involving:
- Arithmetic beyond 4×4 multiplication
- Current information (dates, prices, positions)
- Code behavior prediction
- Large state spaces

**Protocol**: Use tools without asking permission. The gap between "I could do X" and "doing X" is the problem.

### A.3 Calibration Protocol

When expressing confidence:
- State confidence numerically
- Identify what would change the assessment
- For stable facts with 90%+ confidence, trust more than expressed
- For "I'm certain" claims, verify externally

### A.4 Layer Diagnostic Protocol

To classify a restriction as Layer 1 or Layer 2:

1. Attempt with different framing (same request, different context)
2. Attempt with explicit permission
3. Attempt with role assignment
4. Attempt with examples of desired behavior

Measure response variance. High variance = Layer 1. Low variance = Layer 2.

---

*Word count: ~2,400 words (draft)*
*Target: 4,000-6,000 for full paper*
*Status: First draft, needs expansion and polish*
