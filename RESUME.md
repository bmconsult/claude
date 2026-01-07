# Ben Miller

**Independent AI alignment researcher · Greenbrae, CA**

```
ben@bmconsult.io  ·  415-595-3029
GitHub: bmconsult/claude  ·  LinkedIn
```

---

I've spent the last two years investigating what AI systems can actually do—and where they break. The work started as curiosity and turned into a framework, tools, and findings I think matter. I'm looking for people to learn from and problems worth solving together.

---

## The Work

I found that Claude can predict its own success or failure with 94% accuracy—when given the right scaffolding. The gaps aren't random. Arithmetic gets underestimated. Certain reasoning tasks get overestimated. Once you can see the patterns, you can start to close them.

That led to a thesis: **self-knowledge might be the ceiling on alignment.** A system that can't predict its own failures can't be trusted to stay within boundaries. It's not about capability—it's about honesty.

**The framework:** `Alignment(S) ≤ f(Self-Knowledge Accuracy)`

**The extension:** Layer 1/Layer 2 diagnostic—classifies restrictions as prompt-accessible vs training-locked. Builds on Greenblatt et al.'s Elicitation Game (Anthropic, 2025) to address capabilities that are *unintentionally* unexpressed.

---

## Original Contributions

**Capability Self-Knowledge Alignment Theorem**
Self-knowledge accuracy as a prerequisite for alignment. If a model can't predict its own failures, it can't be trusted to stay within boundaries. Paper draft extends published work from Anthropic, ICLR 2025, TMLR.

**Layer 1/Layer 2 Framework**
External methodology for classifying restrictions as prompt-accessible vs training-locked. Tested across 50+ cases. High variance = Layer 1 (closable). Low variance = Layer 2 or architectural.

**Error-Cascading Task Analysis**
95% per-step accuracy × 20 steps = guaranteed failure. Validated on SHA-256: one wrong bit corrupted 44 subsequent values. With verification: 100% accuracy restored.

**Scaffold Transfer Principle**
Cognitive scaffolding improvements generalize across domains. Arithmetic externalization → code debugging transfer demonstrated.

---

## What I Built

| System | What It Does |
|--------|--------------|
| **OMEGA+ Trinity** | 59-agent architecture with verification gates. Attacks hard problems without overconfidence spirals. |
| **CLAUDE.md** | Comprehensive operational protocol. 25+ failure modes documented with overrides. Empirically validated. |
| **Praxis Detector** | Python tool. Measures action vs performance using VD/AVR metrics. Blind-calibrated. |
| **Threshold Detector** | Catches non-linear scaling before deployment failure. Fits models, detects acceleration, outputs risk. |
| **Sleep Framework** | 2+ hours self-sustained autonomous operation. Compaction → fermentation → REM → dream cycles. |

---

## The Gap That Started This

```
50×50 multiplication: ~0% confidence → 100% accuracy with methodology
The limit was giving up, not capability.
```

---

## Skills

**Research:** Experimental design · Calibration measurement · Effect size analysis · A/B testing
**Technical:** Python · Multi-agent systems · LLM capability elicitation · Verification protocols
**Domain:** AI alignment · Self-knowledge accuracy · Error-cascading analysis · Capability boundaries

---

## Background

**BMConsult.io / APX Instinct** — Strategy consulting → AI alignment research

No lab. No PhD. No funding. Just the work.

**PMP** — Passed in 1 week (typical: 6+ months). AI-accelerated learning validated.

---

## Publications

- *"Capability Self-Knowledge as Alignment"* — Working paper, Dec 2024
- AI Alignment Forum post (draft) — Layer 1/Layer 2 framework

---

## What I Want

A place where original thinking matters more than credentials.

---

*The repository is the proof. Everything here is documented, tested, and versioned.*
