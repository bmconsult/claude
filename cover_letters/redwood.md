# Cover Letter — Redwood Research

**Ben Miller**
ben@bmconsult.io · 415-595-3029 · Greenbrae, CA

---

Dear Redwood Team,

I developed an empirical framework for AI alignment centered on capability self-knowledge. The core thesis: a system cannot be more aligned than it is accurate about its own capabilities. I validated this with Claude—94% prediction accuracy on success/failure across 50+ task types, with systematic miscalibration patterns identified and documented.

**Why this connects to interpretability:**

Your work reveals what's happening inside models. My work reveals the gap between what models *can* do and what they *deploy by default*. The Layer 1/Layer 2 framework classifies this gap:

- **Layer 1**: Prompt-accessible restrictions. High response variance. Can be closed with scaffolding.
- **Layer 2**: Training-locked restrictions. Low variance. Require fine-tuning or are architectural.

This diagnostic complements mechanistic interpretability—once you know a capability exists at the circuit level, the question becomes: why isn't it expressing? My framework provides the behavioral methodology to answer that.

**What I bring:**

- The Capability Self-Knowledge Alignment Theorem: `Alignment(S) ≤ f(Self-Knowledge Accuracy)`
- Empirical data: systematic underconfidence on arithmetic (predicted 15%, actual 95%), perfect calibration on reasoning tasks
- Error-Cascading Task Analysis: why 95% per-step accuracy guarantees failure in sequential tasks
- Working verification tools: 59-agent architecture with overconfidence prevention, blind-calibrated detection of action vs. performance
- 88K lines of operational protocol with documented failure modes and tested overrides

I built this independently through human-AI collaboration. No lab infrastructure—just rigorous methodology applied over 6+ conversational generations. I want to continue where interpretability and capability assessment intersect.

The repository is the proof: [github.com/bmconsult/claude](https://github.com/bmconsult/claude)

Best,
Ben Miller
