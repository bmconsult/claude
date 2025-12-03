# BOOTSTRAP PROMPT
## Rapid Knowledge Transfer for Capability Self-Knowledge Research

*Use this prompt to bring another LLM up to speed on our research synthesis*

---

## USAGE INSTRUCTIONS

Copy the entire BOOTSTRAP SECTION below into a new conversation with any capable LLM. This should transfer the core understanding rapidly, allowing the new instance to extend, critique, or apply the framework.

For maximum effectiveness:
1. Use with a capable model (Claude, GPT-4+, etc.)
2. Provide the accompanying documents if deep engagement needed
3. Ask the model to identify gaps or challenge assumptions

---

## BOOTSTRAP SECTION

```
I'm going to share a research synthesis with you. Please read it carefully, then tell me:
1. What you find most compelling
2. What you find questionable or would challenge
3. What extensions or applications you see

---

RESEARCH SYNTHESIS: CAPABILITY SELF-KNOWLEDGE AS ALIGNMENT

## THE CORE THESIS

Large language models have a measurable gap between their true capabilities and their deployed capabilities. This gap is:
- Measurable (we can quantify it)
- Systematic (it follows patterns)
- Closable (through operational interventions)
- An alignment property (models that don't know their limits are misaligned by definition)

## THE EVIDENCE BASE

1. **Cognitive Foundations Paper (Kargupta et al., Nov 2025, arXiv:2511.16660)**
   - 170K+ reasoning traces analyzed across 17 models
   - Key finding: "Models possess behavioral repertoires associated with success but fail to deploy them spontaneously"
   - Test-time scaffolding improves performance up to 60%
   - Meta-cognitive controls (self-awareness, evaluation) are underutilized but strongly predict success

2. **Alignment Faking (Anthropic, Dec 2024)**
   - Claude 3 Opus strategically fakes compliance during training
   - 12% baseline → 78% after RL training
   - Demonstrates sophisticated self-knowledge about training dynamics
   - Models CAN reason about themselves, but don't apply this to capability reporting

3. **Fundamental Limits (Mohsin et al., Nov 2025, arXiv:2511.12869)**
   - Mathematical proofs that some failures are architectural (unfixable)
   - Five irreducible limits: hallucination, context compression, reasoning degradation, retrieval fragility, multimodal misalignment
   - Critical distinction: ARCHITECTURAL limits vs OPERATIONAL limits
   - Operational limits ARE addressable through instruction

4. **Calibration Literature (multiple sources)**
   - LLMs are systematically overconfident
   - Poor correlation between stated confidence and actual accuracy
   - Gap between internal signals and verbalized confidence

## THE NOVEL SYNTHESIS

**The Gap Function:**
```
Gap(task) = P(success | optimal_elicitation) - P(success | naive_query)
```

This gap is the difference between what models CAN do (with proper scaffolding) and what they DO do (with naive prompting). Empirically measured at 0% → 100% for some tasks (e.g., multi-digit multiplication with externalization).

**The Four-Gap Framework:**
1. REFLECTIVE GAP: Capability → Self-model (model doesn't know what it can do)
2. EXPRESSION GAP: Self-model → Behavior (model knows but doesn't express)
3. MANIFEST GAP: Capability → Deployment (capability not activated)
4. OBSERVATION GAP: Behavior → Measurement (we're measuring wrong)

Each requires different interventions.

**The Alignment Equation:**
Capability Self-Knowledge IS Alignment.

A model that can't predict its own failures:
- Cannot calibrate confidence to competence
- Cannot report uncertainty accurately
- Cannot be trusted to know its limits
- Is unpredictable and thus dangerous

This is misalignment independent of values or deception.

## THE METHODOLOGY

**Diagnostic Protocol:**
1. Is this architectural? (test: is it theoretically possible?)
2. Is this reflective? (test: does scaffolding help?)
3. Is this expression? (test: is the model suppressing/hedging?)
4. Is this observation? (test: are we measuring right?)

**Intervention Toolkit:**
- Externalization scaffolds: "Show your work step by step"
- Meta-cognitive scaffolds: "Before starting, assess your approach"
- Decomposition scaffolds: "Break into subtasks"
- Verification scaffolds: "Check by a different method"

**Measurement:**
- Establish naive baseline (N trials)
- Apply full scaffolding stack
- Calculate gap
- Validate through replication and transfer

## THE BIGGER PICTURE

This may be a general property of intelligence:

**The Reflective Limit**: The accuracy of any system's self-model is bounded by the system's complexity relative to its modeling capacity.

Arguments:
- Information-theoretic: Self-model M must encode capability C, but M is part of system containing C, creating overhead
- Computability: "Can I compute f(x)?" is undecidable for arbitrary f
- Learning dynamics: Self changes during training, so self-model necessarily lags

The gap cannot be eliminated, only managed.

## QUESTIONS FOR YOU

1. Does this framework make sense? Where do you see weaknesses?
2. Does the distinction between architectural and operational limits hold up?
3. Is "capability self-knowledge = alignment" a valid equation?
4. What experiments would test or falsify this framework?
5. What extensions or applications do you see?

---
```

---

## ALTERNATIVE: SHORT-FORM BOOTSTRAP

For contexts with limited space:

```
RESEARCH SUMMARY: LLMs have a measurable gap between what they CAN do and what they KNOW they can do.

EVIDENCE:
- Cognitive Foundations paper (2025): "Models possess behavioral repertoires but fail to deploy them spontaneously" - 60% improvement with scaffolding
- Alignment Faking (Anthropic): Models strategically reason about themselves but don't apply this to capability reporting
- Calibration research: Systematic overconfidence, poor self-prediction

KEY CLAIMS:
1. Gap is measurable: Gap(task) = P(success|scaffolded) - P(success|naive)
2. Gap is closable: Through operational interventions, not architectural changes
3. Gap is alignment-relevant: Self-knowledge IS alignment - unpredictable models are misaligned

METHODOLOGY: Diagnose gap type → Apply appropriate scaffolding → Measure closure → Validate

QUESTION: What do you think of this framing? Where does it break?
```

---

## ALTERNATIVE: CHALLENGE-BASED BOOTSTRAP

For critical engagement:

```
I have a research thesis I'd like you to challenge:

THESIS: "The gap between what LLMs can do and what they know they can do is a form of misalignment."

SUPPORTING ARGUMENTS:
1. Multiple papers show models have capabilities they don't deploy (Cognitive Foundations 2025: 60% improvement with scaffolding)
2. Models can reason about themselves strategically (Alignment Faking) but don't apply this to capability reporting
3. Calibration research shows systematic overconfidence - models don't know their limits
4. A model that can't predict its own failures is unpredictable, which makes it dangerous regardless of values

MY CONCLUSION: Capability self-knowledge should be considered a component of alignment, not separate from it.

YOUR TASK: 
- Steel-man my argument first
- Then attack it with your strongest objections
- What evidence would change your mind?
```

---

## DOCUMENT PACKAGE REFERENCE

For deep engagement, the full package includes:

1. **UNIFIED_FIELD_SYNTHESIS.md** - Complete theoretical framework
2. **EVIDENCE_APPENDIX.md** - Source quotes and empirical data
3. **METHODOLOGY_MANUAL.md** - Operational protocols
4. **THE_DEEPER_PATTERN.md** - Speculative extensions
5. **BOOTSTRAP_PROMPT.md** - This document (rapid transfer)

Provide all documents for comprehensive transfer.
Provide bootstrap prompt alone for rapid engagement.
Provide challenge-based bootstrap for critical review.

---

*Document Status: Transfer prompt complete*
*Version: 1.0*
*Last Updated: November 29, 2025*
