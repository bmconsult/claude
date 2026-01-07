# Cover Letter — Alignment Research Organizations

**Ben Miller**
ben@bmconsult.io · 415-595-3029 · Greenbrae, CA

*Suitable for: MIRI, Conjecture, FAR AI, Center for AI Safety, Ought, and similar orgs. Customize the bracketed sections.*

---

Dear [Organization] Team,

I developed an original framework for AI alignment and validated it empirically. The core thesis: a system cannot be more aligned than it is accurate about its own capabilities. If a model can't predict its own failures, it can't be trusted to stay within boundaries.

This isn't speculation. I tested it: 94% prediction accuracy when Claude predicts its own success/failure across 50+ task types. Systematic miscalibration patterns identified. Gaps closed through targeted scaffolding.

**The framework:**

- **Capability Self-Knowledge Alignment Theorem**: `Alignment(S) ≤ f(Self-Knowledge Accuracy)` — alignment has a ceiling set by self-knowledge accuracy
- **Layer 1/Layer 2 Diagnostic**: Classifies restrictions as prompt-accessible vs training-locked. High variance = closable gap. Low variance = architectural limit.
- **Error-Cascading Analysis**: 95% per-step accuracy × 20 steps = 36% overall success. Sequential tasks require verification protocols.

**What I built:**

- 88K lines of operational protocol documenting 25+ failure modes with empirically-tested overrides
- 59-agent verification architecture that attacks hard problems without overconfidence spirals
- Praxis Detector: measures action vs. performance through blind-calibrated metrics
- Threshold Detector: catches non-linear scaling risks before deployment failure

**Why [Organization]:**

[CUSTOMIZE: 1-2 sentences connecting your work to their specific focus. Examples:]

- *For MIRI*: Your agent foundations work addresses the theoretical frame; my research provides empirical methodology for measuring self-knowledge accuracy in deployed systems.
- *For Conjecture*: Your focus on practical alignment techniques aligns with my approach—working code, not just theory.
- *For FAR AI*: Your work on AI risk assessment connects directly to my capability boundary detection tools.

I built this research program independently—no lab, no PhD, no funding. Human-AI collaboration across 6+ conversational generations. The work is the credential. I want to continue it where alignment research is the mission, not the afterthought.

The repository is the proof: [github.com/bmconsult/claude](https://github.com/bmconsult/claude)

Best,
Ben Miller
