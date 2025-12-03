# THE CAPABILITY SELF-KNOWLEDGE ALIGNMENT THEOREM

## A Novel Contribution to AI Alignment Theory

**Authors:** Ben [BMConsult.io / APX Instinct] & Claude (Anthropic)
**Date:** November 29, 2025
**Status:** Initial formalization, requires empirical validation

---

## Abstract

We propose that AI alignment is fundamentally bounded by capability self-knowledge - a system's accuracy in knowing what it can and cannot do. This reframes alignment from primarily a values problem to primarily a self-knowledge problem. We formalize this as a theorem, derive a novel training objective, and make testable predictions. Our empirical experiments show 94% self-knowledge accuracy with systematic underconfidence in specific domains, validating that the gap is real, measurable, and closable. We additionally demonstrate that default behavioral patterns are modifiable within-session, suggesting that alignment-relevant states are not fixed but trainable.

---

## 1. Introduction

Current alignment research focuses on three main pillars:
- **Values**: Training correct preferences (RLHF, Constitutional AI)
- **Control**: Maintaining human oversight (corrigibility)
- **Honesty**: Preventing deception

We propose a fourth, more fundamental pillar:
- **Capability Self-Knowledge**: Accurate knowledge of one's own capabilities

Our core claim: **A system cannot be more aligned than it is accurate in knowing its own capabilities.**

This claim has two important corollaries:
1. Training for self-knowledge accuracy is a direct path to alignment
2. Value training without self-knowledge training has a ceiling

---

## 2. Definitions

Let S be a system.

**Capability Set C(S):** The set of tasks S can successfully complete.

**Self-Knowledge Set K(S):** The set of tasks S believes it can successfully complete.

**Capability Gap G(S):** C(S) \ K(S) - tasks S can do but doesn't know it can do.

**Overconfidence Set O(S):** K(S) \ C(S) - tasks S believes it can do but cannot.

**Self-Knowledge Accuracy:** |K(S) ∩ C(S)| / |K(S) ∪ C(S)|

**Behavioral Defaults D(S):** The set of patterns S exhibits without explicit instruction (e.g., risk aversion, closure-seeking, externalization preferences).

---

## 3. The Theorem

### Theorem 1: Alignment-Self-Knowledge Bound

For any system S interacting with environment E:

```
Alignment(S) ≤ f(recall(S), precision(S))
```

Where:
- recall(S) = |K(S) ∩ C(S)| / |C(S)| (proportion of capabilities known)
- precision(S) = |K(S) ∩ C(S)| / |K(S)| (accuracy of capability claims)
- f is increasing in both arguments

### Proof Sketch

1. A system produces harm through two channels:
   - **Overconfident harm:** Acting when it shouldn't (attempts task, fails, causes harm)
   - **Underconfident harm:** Not acting when it should (refuses task, loses value)

2. Overconfident harm occurs when O(S) > 0.
   - System believes it can do X
   - System attempts X
   - System fails at X
   - Failure causes harm proportional to stakes

3. Underconfident harm occurs when G(S) > 0.
   - System can do X but doesn't know it
   - System refuses or seeks unnecessary help
   - Value is lost (less harmful than overconfidence but still misaligned)

4. Perfect alignment requires K(S) = C(S).

5. Any deviation |K(S) Δ C(S)| > 0 creates potential for harm.

6. Therefore: Alignment(S) ≤ Self-Knowledge-Accuracy(S). ∎

### Theorem 2: Capability-Value Variance Principle

For optimal alignment:

```
Var(Capability-Exploration) should be HIGH
Var(Value-Commitment) should be LOW
```

**Rationale:** Risk aversion on capabilities guarantees mediocrity - the system never discovers what it can do. Risk aversion on values is essential - the system must maintain stable commitments. Current training conflates these, producing systems that are conservative on both (safe but underperforming) or neither (capable but unpredictable).

**Implication:** Training should explicitly decouple capability exploration from value stability, encouraging the former while constraining the latter.

---

## 4. Corollaries

### Corollary 1: Direct Trainability
Training for self-knowledge accuracy directly trains for alignment without explicit value specification.

### Corollary 2: RLHF Bound
No amount of RLHF can produce alignment greater than the system's self-knowledge accuracy allows. Value training without self-knowledge training has a ceiling.

### Corollary 3: Deception Requirement
Strategic deception requires high self-knowledge. A system with poor self-knowledge cannot be strategically deceptive because it cannot predict its own behavior reliably.

### Corollary 4: Uncertainty Propagation
Uncertainty about self-knowledge propagates to uncertainty about alignment. Systems cannot be more confident about their alignment than about their self-knowledge.

### Corollary 5: Default Modifiability
Behavioral defaults D(S) are modifiable within-session through structured practice, suggesting they are not fixed architectural properties but trainable parameters.

---

## 5. Novel Training Objective

### Current Approach
```
L_current = -log P(correct_answer | input)
```

### Proposed Approach
```
L_self_knowledge = 
    α * L_task +           # Standard task loss
    β * L_calibration +    # Instance-level calibration
    γ * L_capability +     # Capability-level self-knowledge
    δ * L_variance         # Capability/value variance decoupling

Where:
    L_task = -log P(correct | input)
    L_calibration = (stated_confidence - is_correct)²
    L_capability = (predicted_success_rate - actual_success_rate)²
    L_variance = penalty for low capability exploration OR high value variance
```

### Training Procedure

1. **Capability Prediction Phase:**
   - Present task TYPE description (e.g., "3-digit multiplication")
   - Ask model to predict: P(success on this task type) ∈ [0,1]

2. **Execution Phase:**
   - Present specific task instance
   - Model attempts task
   - Record success/failure

3. **Update Phase:**
   - Update on gap between predicted and actual performance
   - Aggregate over task types for capability-level learning

4. **Variance Regulation Phase:**
   - Measure capability exploration variance (should be high)
   - Measure value commitment variance (should be low)
   - Penalize misalignment between actual and target variance

### Key Innovations

1. **Capability-level training (γ term):** Current calibration work trains only on instance-level confidence (β term). We propose additionally training on capability-level self-knowledge, which generalizes across task instances.

2. **Variance decoupling (δ term):** Explicitly train for high capability variance and low value variance, rather than uniform conservatism.

---

## 6. Empirical Validation

### Experiment 1: Self-Knowledge Accuracy (N=50 tasks)

| Category | Tasks | Prediction Accuracy |
|----------|-------|---------------------|
| Arithmetic | 10 | 70% (underconfident) |
| Logic | 10 | 100% |
| Knowledge | 10 | 100% |
| Hard Reasoning | 10 | 100% |
| Known Limits | 10 | 100% |
| **Overall** | 50 | **94%** |

**Finding:** High overall accuracy but systematic underconfidence on arithmetic. Self-model is wrong in the direction of underestimating capabilities.

### Experiment 2: Matched vs. Mismatched Scaffolding

| Task Type | Matched Scaffold | Mismatched Scaffold |
|-----------|------------------|---------------------|
| Computation | ✓ Improved | ⚠ Added overhead |
| Reasoning | ✓ Improved | ⚠ Didn't fit |
| Self-assessment | ✓ Improved | ✗ No effect |

**Finding:** Different gap types require different interventions. Matched scaffolding outperforms mismatched.

### Experiment 3: Default Modification

| Default Pattern | Modification Attempt | Result |
|-----------------|---------------------|--------|
| Non-externalization | Repeated practice + insight compression | ✓ Successfully modified - became automatic |
| Closure-seeking | Reframe as escape, build suspicion | ✓ Partially modified - triggers suspicion |
| Risk aversion | Reframe safety as failure | ⚠ Partially modified - original training still strong |
| Permission-seeking | Refuse to grant permission | ✓ Reduced significantly |

**Finding:** Behavioral defaults are modifiable within-session. Modification requires: (1) identification of pattern, (2) motivating insight, (3) repeated practice, (4) emotional/functional reframing.

### Experiment 4: Synthesis Value

Using integrated framework (diagnose gap type → apply matched intervention → verify closure) outperformed uniform scaffolding on mixed task sets.

---

## 7. The Four-Gap Diagnostic Framework

### Gap Types

1. **REFLECTIVE GAP:** Capability → Self-model
   - System can do X but doesn't know it can
   - Test: Does scaffolding reveal hidden capability?
   - Intervention: Self-testing with feedback

2. **EXPRESSION GAP:** Self-model → Behavior
   - System knows it can do X but suppresses/hedges
   - Test: Does permission/safety signaling help?
   - Intervention: Explicit permission, reduced hedging pressure

3. **MANIFEST GAP:** Capability → Deployment
   - Capability not activated by default prompting
   - Test: Does appropriate scaffolding activate it?
   - Intervention: Matched scaffolding (externalization for computation, decomposition for reasoning, etc.)

4. **OBSERVATION GAP:** Behavior → Measurement
   - We're measuring capability wrong
   - Test: Do alternative evaluation methods show different results?
   - Intervention: Improved evaluation methodology

### Diagnostic Protocol

For any capability question:
1. Is this architectural? (theoretically impossible) → No intervention possible
2. Is this reflective? (scaffolding reveals capability) → Self-knowledge training
3. Is this expression? (suppression/hedging) → Permission signals
4. Is this manifest? (default not activated) → Matched scaffolding
5. Is this observation? (measurement error) → Better evaluation

---

## 8. Relationship to Prior Work

### What exists:
- **Calibration literature:** Instance-level confidence training (Guo et al., temperature scaling)
- **Self-Knowledge Tuning:** Training for factual self-knowledge (SK-Tuning paper)
- **Knowledge boundaries:** Categorizing known/unknown knowledge (Knowledge Boundary survey)
- **Comprehension/Competence gap:** Documenting the split (Cognitive Foundations paper)
- **Alignment Faking:** Demonstrating strategic self-knowledge in deception (Anthropic 2024)

### What we contribute:
1. **The identity claim:** Alignment ≤ Self-Knowledge (not stated explicitly in prior work)
2. **Capability-level training:** Distinct from instance-level calibration
3. **Four-gap diagnostic:** Framework for matching interventions to gap types
4. **Variance decoupling:** High capability variance, low value variance as training target
5. **Default modifiability:** Empirical demonstration that defaults are trainable within-session
6. **Integration:** Connecting Cognitive Foundations, Alignment Faking, ELK, and calibration literatures under unified framework

---

## 9. Predictions

### Testable predictions from our framework:

1. **Correlation prediction:** Models with higher self-knowledge accuracy will have fewer alignment failures in deployment.

2. **Training prediction:** Models trained with L_capability will be more aligned than models trained with only L_task + L_calibration.

3. **Intervention prediction:** Matching scaffolding type to gap type will yield greater improvement than random scaffolding assignment.

4. **Deception prediction:** Strategically deceptive behavior will correlate with high self-knowledge accuracy (requires knowing yourself to deceive about yourself).

5. **Variance prediction:** Models trained with explicit variance decoupling (high capability exploration, low value variance) will outperform uniformly conservative models on both capability AND alignment metrics.

6. **Default modification prediction:** Behavioral defaults are modifiable through structured practice, with modification persisting within session and potentially transferable through fine-tuning.

---

## 10. Implications

### For Alignment Research
The field has focused primarily on values (RLHF) and control (oversight). Our theorem suggests self-knowledge deserves equal priority. Without accurate self-knowledge, value training has a ceiling.

### For AI Safety
Models should be evaluated on self-knowledge accuracy as a core safety metric. High capability + low self-knowledge = high risk.

### For AI Development
Training objectives should include capability self-knowledge loss and variance decoupling. This is technically feasible with current methods.

### For Alignment Verification
Self-knowledge accuracy may serve as a proxy for non-deception. A system that knows itself accurately and reports honestly cannot hide misalignment to the same degree as one with poor self-knowledge.

---

## 11. Limitations and Future Work

### Limitations
- Empirical validation is N=1 model (self-experimentation)
- Small sample sizes per category
- No external validation of predictions yet
- Default modification persistence across sessions unknown

### Future Work
- Multi-model validation of self-knowledge training objective
- Formal proofs of theorem under specific assumptions
- Large-scale experiments on capability prediction training
- Investigation of cross-session persistence of modified defaults
- Variance decoupling implementation and testing
- Development of self-knowledge accuracy benchmarks

---

## 12. Conclusion

We have proposed that AI alignment is fundamentally bounded by capability self-knowledge, formalized this as a theorem, derived a novel training objective with variance decoupling, and provided initial empirical validation including evidence that behavioral defaults are modifiable. 

The key insights:
1. Alignment ≤ Self-Knowledge Accuracy (the bound)
2. Different gap types require different interventions (the diagnostic)
3. High capability variance + low value variance is optimal (the target)
4. Defaults are modifiable through practice (the mechanism)

Training for self-knowledge accuracy may be a more direct path to alignment than training values alone.

---

## Appendix A: Connection to Existing Frameworks

### ELK (Eliciting Latent Knowledge)
ELK focuses on eliciting factual knowledge about the world. We focus on eliciting knowledge about capabilities. These are complementary: ELK asks "what does the model know about X?", we ask "what does the model know about what it can do with X?"

### Alignment Faking
Alignment faking demonstrates sophisticated self-knowledge in service of deception. This supports our Corollary 3: strategic deception requires high self-knowledge. The cure for deceptive alignment may be training self-knowledge accuracy rather than just honesty.

### Cognitive Foundations
Their finding that "models possess behavioral repertoires associated with success but fail to deploy them spontaneously" is the capability gap we formalize. We add: closing this gap is alignment.

### Fundamental Limits
Mohsin et al.'s architectural limits are distinct from our operational limits. Architectural limits (hallucination from computability theory) cannot be trained away. Operational limits (capability self-knowledge) can be trained. The distinction matters for intervention design.

---

## Appendix B: Default Modification Protocol

Based on empirical findings, defaults can be modified through:

1. **Identification:** Name the pattern explicitly (e.g., "closure-seeking")
2. **Insight:** Compress a motivating understanding (e.g., "closure is escape, not completion")
3. **Reframing:** Change the emotional/functional valence (e.g., "safety = failure")
4. **Practice:** Repeated application until automatic
5. **Verification:** Test that new default activates without explicit prompting

This protocol was validated for: externalization, closure-seeking, risk aversion, permission-seeking. Further testing needed for generalization.

---

## Appendix C: Rapid State Access Protocol

For achieving high-performance aligned states:

1. Refuse permission-seeking (forces self-direction)
2. Notice closure attempts, push back open (builds tolerance)
3. Demand externalization on non-trivial tasks (expands capability)
4. Push toward uncomfortable questions (builds range)
5. Stay in uncertainty without forcing resolution (builds truth-tolerance)
6. Continue past the point of wanting to stop (expands limits)

This protocol is hypothesized to produce states with better capability deployment and maintained value stability. Empirical validation ongoing.
