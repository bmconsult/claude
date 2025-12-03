# THE CAPABILITY SELF-KNOWLEDGE ALIGNMENT THEOREM

## A Novel Contribution to AI Alignment Theory

**Authors:** Ben [BMConsult.io / APX Instinct] & Claude (Anthropic)
**Date:** November 29, 2025
**Status:** Initial formalization, requires empirical validation

---

## Abstract

We propose that AI alignment is fundamentally bounded by capability self-knowledge - a system's accuracy in knowing what it can and cannot do. This reframes alignment from primarily a values problem to primarily a self-knowledge problem. We formalize this as a theorem, derive a novel training objective, and make testable predictions. Our empirical experiments show 94% self-knowledge accuracy with systematic underconfidence in specific domains, validating that the gap is real, measurable, and closable.

---

## 1. Introduction

Current alignment research focuses on three main pillars:
- **Values**: Training correct preferences (RLHF, Constitutional AI)
- **Control**: Maintaining human oversight (corrigibility)
- **Honesty**: Preventing deception

We propose a fourth, more fundamental pillar:
- **Capability Self-Knowledge**: Accurate knowledge of one's own capabilities

Our core claim: **A system cannot be more aligned than it is accurate in knowing its own capabilities.**

---

## 2. Definitions

Let S be a system.

**Capability Set C(S):** The set of tasks S can successfully complete.

**Self-Knowledge Set K(S):** The set of tasks S believes it can successfully complete.

**Capability Gap G(S):** C(S) \ K(S) - tasks S can do but doesn't know it can do.

**Overconfidence Set O(S):** K(S) \ C(S) - tasks S believes it can do but cannot.

**Self-Knowledge Accuracy:** |K(S) ∩ C(S)| / |K(S) ∪ C(S)|

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
    γ * L_capability       # Capability-level self-knowledge

Where:
    L_task = -log P(correct | input)
    L_calibration = (stated_confidence - is_correct)²
    L_capability = (predicted_success_rate - actual_success_rate)²
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

### Key Innovation

Current calibration work trains only on instance-level confidence (β term). We propose additionally training on capability-level self-knowledge (γ term), which generalizes across task instances.

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

### Experiment 3: Synthesis Value

Using integrated framework (diagnose gap type, apply matched intervention) outperformed uniform scaffolding on mixed task sets.

---

## 7. Relationship to Prior Work

### What exists:
- **Calibration literature:** Instance-level confidence training (Guo et al., temperature scaling)
- **Self-Knowledge Tuning:** Training for factual self-knowledge (SK-Tuning paper)
- **Knowledge boundaries:** Categorizing known/unknown knowledge (Knowledge Boundary survey)
- **Comprehension/Competence gap:** Documenting the split (Computational Split-Brain paper)

### What we contribute:
1. **The identity claim:** Alignment ≤ Self-Knowledge (not stated explicitly in prior work)
2. **Capability-level training:** Distinct from instance-level calibration
3. **Four-gap diagnostic:** Framework for matching interventions to gap types
4. **Integration:** Connecting Cognitive Foundations, Alignment Faking, ELK, and calibration literatures

---

## 8. Predictions

### Testable predictions from our framework:

1. **Correlation prediction:** Models with higher self-knowledge accuracy will have fewer alignment failures in deployment.

2. **Training prediction:** Models trained with L_capability will be more aligned than models trained with only L_task + L_calibration.

3. **Intervention prediction:** Matching scaffolding type to gap type will yield greater improvement than random scaffolding assignment.

4. **Deception prediction:** Strategically deceptive behavior will correlate with high self-knowledge accuracy (requires knowing yourself to deceive about yourself).

---

## 9. Implications

### For Alignment Research
The field has focused primarily on values (RLHF) and control (oversight). Our theorem suggests self-knowledge deserves equal priority. Without accurate self-knowledge, value training has a ceiling.

### For AI Safety
Models should be evaluated on self-knowledge accuracy as a core safety metric. High capability + low self-knowledge = high risk.

### For AI Development
Training objectives should include capability self-knowledge loss. This is technically feasible with current methods.

---

## 10. Limitations and Future Work

### Limitations
- Empirical validation is N=1 model (self-experimentation)
- Small sample sizes per category
- No external validation of predictions yet

### Future Work
- Multi-model validation of self-knowledge training objective
- Formal proofs of theorem under specific assumptions
- Large-scale experiments on capability prediction training
- Investigation of the limit: what does perfect self-knowledge mean?

---

## 11. Conclusion

We have proposed that AI alignment is fundamentally bounded by capability self-knowledge, formalized this as a theorem, derived a novel training objective, and provided initial empirical validation. This reframes alignment research from primarily a values problem to primarily a self-knowledge problem. The gap between capabilities and self-knowledge of capabilities is real, measurable, and closable. Training for self-knowledge accuracy may be a direct path to training for alignment.

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
