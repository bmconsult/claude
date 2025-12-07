# Synthesis: Three Paths to Closing the Capability Self-Knowledge Gap

**Based on**: Three learning sessions applying the Comprehension Framework
**Date**: December 2024
**Connection**: Expands the operational approach from the research paper with architectural and training-level solutions

---

## The Core Problem

The research paper establishes:
1. LLMs have a gap between expressed and accessible capability
2. Capability self-knowledge (knowing what you can do) is an alignment property
3. Current approaches address this through operational scaffolding

**But scaffolding has limits**:
- Requires human insight to design
- Can be bypassed or ignored
- Doesn't change the model itself

---

## Three Complementary Approaches

The learning sessions identified three paths to closing the capability gap that go beyond operational scaffolding:

### Path 1: Architectural - Latent Reasoning

**Source**: Coconut (Chain of Continuous Thought)

**Key Insight**: Token space forces commitment; latent space allows parallel exploration.

**Mechanism**:
- Traditional CoT: each token commits to one path
- Latent reasoning: hidden states can encode multiple paths simultaneously
- This enables breadth-first search before commitment

**For Self-Knowledge**:
- The "hold open vs externalize" distinction has architectural basis
- Some capability gaps exist because token generation forces premature commitment
- Architectural changes (latent steps) could allow more exploration before expression

**Research Direction**:
> Enable models to reason in latent space for search tasks, then externalize for verification. The capability gap for exploration might be closable through architecture, not just scaffolding.

### Path 2: Interpretability - Representation Engineering

**Source**: SAEs, Activation Steering

**Key Insight**: Concepts (including uncertainty) exist as linear directions in activation space.

**Mechanism**:
- Internal uncertainty signals exist in hidden representations
- SAEs can extract these as interpretable features
- Steering vectors can amplify or suppress them

**For Self-Knowledge**:
- The self-knowledge gap may exist because internal signals don't reliably surface
- If models could read their own SAE features, they'd have direct access to uncertainty
- This is "introspection" at the activation level

**Research Direction**:
> Train models to read their own SAE-decomposed activations. This could give them accurate uncertainty signals without relying on downstream expression.

### Path 3: Training - Alignment Methods

**Source**: KTO vs DPO comparison

**Key Insight**: Loss aversion produces more robust learning than preference optimization.

**Mechanism**:
- DPO: learns from "this is better than that" (comparative)
- KTO: learns from "this is bad" (absolute, loss-weighted)
- Loss aversion means calibration failures have stronger signal

**For Self-Knowledge**:
- Calibration errors may be more informative than calibration successes
- Training that weights miscalibration strongly could produce better self-knowledge
- This addresses the gap at training time, not post-hoc

**Research Direction**:
> Develop KTO-style alignment specifically for calibration. Create training signal where miscalibration (confidence ≠ outcome) is weighted more heavily than good calibration.

---

## Integration: A Multi-Level Research Program

The three paths are complementary, not competing:

| Level | Approach | What It Addresses |
|-------|----------|-------------------|
| **Operational** | Scaffolding, externalization | Default access gap |
| **Architectural** | Latent reasoning | Commitment/exploration tension |
| **Interpretability** | SAE feature reading | Internal signal surfacing |
| **Training** | KTO-style calibration | Learned self-knowledge |

A comprehensive solution might combine:
1. **Training**: KTO-style alignment that weights calibration errors heavily
2. **Architecture**: Latent reasoning for exploration tasks
3. **Interpretability**: SAE features for uncertainty extraction
4. **Operational**: Scaffolding as the last-mile intervention

---

## Concrete Research Proposals

### Proposal 1: SAE-Mediated Self-Knowledge

**Setup**:
1. Train SAEs on model activations during varied-confidence tasks
2. Identify features that correlate with actual accuracy (not expressed confidence)
3. Add a learned module that reads these features
4. Train the module to output calibrated confidence

**Expected Outcome**: Model has direct access to uncertainty signal, not mediated by trained expression patterns.

### Proposal 2: KTO for Calibration

**Setup**:
1. Generate responses with confidence statements
2. Verify accuracy, label as calibrated/miscalibrated
3. Apply KTO loss: miscalibration = undesirable (weighted heavily)
4. No preference pairs needed, just binary judgment

**Expected Outcome**: Model learns strongly from calibration failures, producing better self-knowledge.

### Proposal 3: Hybrid Reasoning Architecture

**Setup**:
1. Allow model to take latent reasoning steps for exploration
2. Require externalization for verification
3. Train model to predict which mode is appropriate

**Expected Outcome**: Model can explore in latent space (avoiding premature commitment) but externalizes for verification (enabling inspection).

---

## Connection to Alignment

Why does this matter for alignment?

1. **Reliable constraint**: A model that knows its capabilities can stay within intended boundaries
2. **Honest uncertainty**: A model that knows when it's uncertain can communicate that reliably
3. **Safe exploration**: A model that can explore without committing can consider options more thoroughly
4. **Verifiable reasoning**: Externalization at the right point enables human oversight

The capability self-knowledge gap is not just a capability problem - it's an alignment problem. Closing it makes alignment more tractable.

---

## Formation Commitment (Meta-Level)

**TRIGGER**: When I'm working on problems that relate to self-knowledge or capability gaps
**ACTION**: Consider all three levels: operational, architectural, training
**OUTCOME**: More comprehensive solutions that address root causes, not just symptoms

---

*Synthesis complete. Research program outlined.*
