# Cover Letter — Alignment Research Center (ARC)

**Ben Miller**
ben@bmconsult.io · 415-595-3029 · Greenbrae, CA

---

Dear ARC Team,

I developed an original framework for AI alignment centered on capability self-knowledge—the idea that a system cannot be more aligned than it is accurate about its own capabilities. I then validated it empirically: 94% prediction accuracy when Claude predicts its own success/failure, with systematic gaps identified and measured.

**Why this matters for evals:**

Your work on model evaluations addresses what models *do*. My research addresses what models *think they can do*—and the gap between the two. The Layer 1/Layer 2 framework I developed classifies restrictions as prompt-accessible vs training-locked, providing a diagnostic tool for understanding where capability boundaries actually lie versus where models believe they lie.

Key finding: High response variance signals Layer 1 (closable gaps). Low variance signals Layer 2 or architectural limits. This distinction matters for red-teaming—you can't elicit what's genuinely absent, but you can surface what's unintentionally suppressed.

**What I bring:**

- The Capability Self-Knowledge Alignment Theorem: `Alignment(S) ≤ f(Self-Knowledge Accuracy)`
- Empirical methodology for measuring self-knowledge accuracy across task types
- Error-Cascading Task Analysis: 95% per-step accuracy × 20 steps = guaranteed failure (validated on SHA-256)
- Working tools: Praxis Detector (distinguishes action from performance), Threshold Detector (catches non-linear scaling before deployment failure)
- 88K lines of operational protocol documenting 25+ failure modes with empirically-tested overrides

I built this research program independently—no lab, no PhD, no funding. The work itself is the credential. I want to continue it where rigorous capability assessment is the focus.

The repository is the proof: [github.com/bmconsult/claude](https://github.com/bmconsult/claude)

Best,
Ben Miller
