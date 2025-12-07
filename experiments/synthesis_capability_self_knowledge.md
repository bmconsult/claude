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

### Path 4: Simulation - World Models for Self-Prediction

**Source**: WebDreamer, NVIDIA Cosmos, Meta V-JEPA 2

**Key Insight**: A world model predicts how state changes given actions. Turn this inward: predict how *my own outputs* change given different approaches.

**Mechanism**:
- WebDreamer: LLM "dreams" outcomes of candidate actions before executing
- Simulates state transitions in natural language
- Evaluates progress toward goal
- 4-5× more efficient than tree search while maintaining accuracy

**For Self-Knowledge**:
- The capability gap often manifests as: "I don't know if I can do X until I try"
- A self-simulation layer could predict response quality before committing
- This is metacognitive simulation: imagining my own performance

**Concrete Implementation**:
1. Before answering, generate lightweight "drafts" of possible approaches
2. Evaluate each draft: "Would this actually work? What would go wrong?"
3. Use the prediction to either commit, externalize more, or hedge appropriately
4. Calibrate the predictor against actual outcomes

**The Key Difference from Latent Reasoning**:
- Latent reasoning (Coconut): Reason without committing tokens
- Self-simulation: Commit provisional tokens, evaluate them, then commit real answer
- One is exploration in hidden space; the other is exploration in output space

**Research Direction**:
> Train models to simulate their own outputs before committing. Use the simulation-reality gap as a training signal for calibration. A model that can predict its own failures is a model with genuine self-knowledge.

**Connection to Grokking**:
The mastery document notes grokking may reflect two competing circuits: memorization (dense) and generalization (sparse). The capability gap might be not knowing which circuit is responding.

Self-simulation could reveal this: if I simulate my answer and it feels "memorized" vs "reasoned," that's a self-knowledge signal. The simulation layer could learn to detect which circuit is active.

### Path 5: Post-Training - Calibration as Portable Task Vector

**Source**: TIES, DARE, Task Arithmetic

**Key Insight**: If calibration is a task, it has a task vector that can be extracted and merged.

**Mechanism**:
- Task vectors are linear: τ = θ_finetuned - θ_base
- TIES-Merging resolves sign conflicts between task vectors
- DARE shows 90% of weights can be dropped (redundant encoding)
- Larger models merge better (power law relationship)

**For Self-Knowledge**:
- Train a "calibration specialist" model (good at knowing its limits, not necessarily at tasks)
- Extract its task vector: τ_calibration = θ_calibrated - θ_base
- Merge into task-specific models via TIES or dare_ties
- Result: Task capability + calibration without retraining

**Advantages**:
- No retraining of deployed models
- Calibration becomes "portable" like a plugin
- Could distribute calibration patches

**Challenges**:
- Calibration might be too "meta" to form clean task vector
- Interference with task performance is possible
- Cross-domain generalization unproven

**Research Direction**:
> Train calibration-specialist models, extract their task vectors, and merge into task-specific models. This makes calibration "portable" - deployable post-hoc without retraining.

---

## Integration: A Multi-Level Research Program

The five paths are complementary, not competing:

| Level | Approach | What It Addresses |
|-------|----------|-------------------|
| **Operational** | Scaffolding, externalization | Default access gap |
| **Architectural** | Latent reasoning | Commitment/exploration tension |
| **Interpretability** | SAE feature reading | Internal signal surfacing |
| **Training** | KTO-style calibration | Learned self-knowledge |
| **Simulation** | Self-world-models | Capability prediction before commitment |
| **Post-Training** | Task vector merging | Portable calibration |

A comprehensive solution might combine:
1. **Training**: KTO-style alignment that weights calibration errors heavily
2. **Architecture**: Latent reasoning for exploration tasks
3. **Interpretability**: SAE features for uncertainty extraction
4. **Simulation**: Self-models for predicting own capability
5. **Post-Training**: Merge calibration vectors into deployed models
6. **Operational**: Scaffolding as the last-mile intervention

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

### Proposal 4: Self-Simulation for Capability Prediction

**Setup**:
1. Before answering substantive questions, generate lightweight draft responses
2. Apply a learned "outcome predictor" to each draft
3. Train predictor on: draft → {actual_quality, actual_correctness}
4. Use predictions to adjust confidence and approach selection

**Training Signal**:
- Generate drafts with varied approaches (brief, detailed, hedged, confident)
- Complete each to full response, evaluate against ground truth
- Predictor learns: "drafts that look like X tend to succeed/fail"

**Meta-Level**:
- This is a world model where the "world" is the model's own response generation
- The model becomes an observer of its own tendencies
- Calibration emerges from accurate self-prediction

**Expected Outcome**: Model can answer "will I succeed at this?" before trying, by simulating its own attempt and evaluating the simulation.

**Connection to Grokking**: If the simulation layer can detect memorization vs generalization circuits, it provides direct access to the capability gap.

### Proposal 5: Portable Calibration via Task Vector Merging

**Setup**:
1. Fine-tune base model specifically for calibration (not task performance)
2. Use KTO-style training: weight miscalibration errors heavily
3. Extract calibration task vector: τ_cal = θ_calibrated - θ_base
4. Apply TIES-Merging or dare_ties to task-specific models

**The Calibration Specialist**:
- A model trained not to be smart, but to know its limits
- Every training signal is about calibration: "Did your confidence match the outcome?"
- Produces clean task vector isolating calibration capability

**Merging Protocol**:
```
θ_final = θ_task + α·TIES(τ_cal, density=0.5)
```
- α controls calibration strength
- TIES resolves sign conflicts
- Task performance preserved, calibration added

**Expected Outcome**: Post-hoc calibration injection without retraining task models. Calibration becomes a distributable patch.

**Validation**:
- Measure calibration before/after merge
- Measure task performance before/after (interference check)
- Test cross-domain: calibration trained on math, applied to coding

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
