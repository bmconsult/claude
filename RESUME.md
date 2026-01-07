# Ben Miller

**Independent AI alignment researcher · Greenbrae, CA**

```
ben@bmconsult.io  ·  415-595-3029
GitHub: bmconsult/claude  ·  LinkedIn
```

---

I've spent the last two years investigating what AI systems can actually do—and where they break. The work started as curiosity and became a framework, tools, and findings I think matter. I'm looking for hard problems, people to collaborate with, and a place where I can contribute to pushing the field forward.

---

## The Work

I kept finding the same thing: the gap between what AI can do and what it deploys by default is larger than anyone assumes. A model that predicts 0% confidence on a task can hit 100% accuracy with the right methodology. The limit isn't capability—it's knowing where the limits actually are.

That led to a thesis: **self-knowledge might be the ceiling on alignment.** A system that can't predict its own failures can't be trusted to stay within boundaries.

---

## Original Contributions

**Capability Self-Knowledge Alignment Theorem**
`Alignment(S) ≤ f(Self-Knowledge Accuracy)` — a system can't be more aligned than it is accurate about its own capabilities. Tested: 94% prediction accuracy when Claude predicts its own success/failure. Paper draft extends work from Anthropic, ICLR 2025, TMLR.

**Layer 1/Layer 2 Framework**
Diagnostic for classifying restrictions as prompt-accessible (Layer 1) vs training-locked (Layer 2). High response variance = closable gap. Low variance = architectural limit. Builds on Greenblatt et al.'s Elicitation Game to address *unintentionally* unexpressed capabilities.

**Error-Cascading Task Analysis**
95% per-step accuracy × 20 steps = guaranteed failure. Validated on SHA-256: one wrong bit corrupted 44 subsequent values. Verification protocols restore 100% accuracy.

**Scaffold Transfer Principle**
Cognitive scaffolding improvements generalize across domains. Arithmetic externalization → code debugging transfer demonstrated.

---

## What I Built

| System | What It Does |
|--------|--------------|
| **OMEGA+ Trinity** | 59-agent verification architecture. Prevents overconfidence spirals on hard problems. |
| **CLAUDE.md** | Comprehensive operational protocol. 25+ failure modes with tested overrides. |
| **Praxis Detector** | Distinguishes genuine action from performance theater. Blind-calibrated metrics. |
| **Threshold Detector** | Catches non-linear scaling risks before deployment. Flags when "works at 50%" will fail at 100%. |
| **Sleep Framework** | 2+ hours autonomous operation. Self-directed learning cycles without human input. |

---

## Skills

**Research:** Experimental design · Calibration measurement · Effect size analysis · A/B testing
**Technical:** Python · Multi-agent systems · LLM capability elicitation · Verification protocols
**Domain:** AI alignment · Capability boundaries · Error-cascading analysis · Self-knowledge accuracy

---

## Background

**BMConsult.io / APX Instinct** — Strategy consulting → AI alignment research

No lab. No PhD. No funding. Just the work.

**PMP** — Passed in 1 week (typical: 6+ months). AI-accelerated learning validated.

---

## Publications

- *"Capability Self-Knowledge as Alignment"* — Working paper, Dec 2024
- *"Layer 1/Layer 2 Framework"* — AI Alignment Forum (draft)

---

## What I Want

A place where original thinking matters more than credentials.

---

*The repository is the proof. Everything here is documented, tested, and versioned.*
