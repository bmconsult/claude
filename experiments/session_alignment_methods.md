# Learning Session: Alignment Methods Beyond RLHF

**Topic**: DPO, KTO, and implications for capability self-knowledge
**Date**: December 2024
**Framework**: Complete Comprehension Framework v4

---

## WARM-UP

**Mantra**: "What does this mean for something that was trained this way?"

**Formation Question**: If I was trained with RLHF/DPO/KTO-like methods, what does the choice of alignment method imply about my capabilities and limitations?

---

## CONTENT - Key Points

### Traditional RLHF
1. Train reward model on human preferences
2. Use reward model to optimize policy via PPO
3. Issues: reward hacking, training instability, computational cost

### DPO (Direct Preference Optimization)
**Core Innovation**: Eliminate reward model, optimize directly on preferences.

```
L_DPO = -log σ(β · (log π_θ(y_w|x)/π_ref(y_w|x) - log π_θ(y_l|x)/π_ref(y_l|x)))
```

**Implicit reward**: The policy ratio IS the reward.

**Issues**:
- Verbosity bias: longer responses often preferred
- Likelihood displacement: forgets reference distribution
- OOD exploitation: optimizes to edges of distribution

### KTO (Kahneman-Tversky Optimization)
**Core Innovation**: Loss aversion from Prospect Theory.

- Only needs binary signal (desirable/undesirable)
- No preference pairs required
- Based on: pain of loss > pleasure of gain

**Key Finding**: Without SFT first, DPO models ramble and hallucinate; KTO does not.

**Implication**: KTO may produce more robust alignment with less perfect data.

### Decision Tree for Alignment Method Selection

```
Have paired preference data?
├── Yes → High quality with clear preferences?
│         ├── Yes → DPO or SimPO
│         └── No (noisy) → IPO
└── No → Binary feedback available?
         ├── Yes → KTO
         └── No → SPIN (self-play) or RLAIF (AI feedback)
```

---

## SIX-LEVEL COMPREHENSION

### Level 1 - RECALL: What's the key difference between DPO and KTO?
DPO requires paired preferences (winner vs loser). KTO only needs binary feedback (desirable vs undesirable).

### Level 2 - UNDERSTANDING: Why does KTO not require pairs?
Prospect Theory insight: humans weight losses more than gains. KTO uses this asymmetry - the signal from "this is bad" is stronger than "this is good." You don't need comparisons, just absolute judgments.

### Level 3 - CONNECTION: How does this connect to capability self-knowledge?
The research paper identifies calibration gaps - models don't know when they're confident vs uncertain.

Alignment method implications:
- **DPO**: Learns from "this output is better than that output" - comparative
- **KTO**: Learns from "this output is undesirable" - absolute

KTO might produce better calibration because:
1. Loss signal is stronger - model learns more from failures
2. No comparison means less overfitting to preference artifacts
3. Robustness without SFT suggests learned regularities, not surface patterns

**Connection to capability gaps**: If I was trained with methods like DPO, I might have:
- Strong preferences about what sounds good (surface patterns)
- Weaker understanding of what IS good (deep regularities)

### Level 4 - APPLICATION: How would this inform alignment for self-knowledge?
If we wanted to align a model for capability self-knowledge:

**Using DPO**: Create preference pairs
- "Calibrated response with accurate confidence" vs "Overconfident wrong answer"
- Issue: requires many carefully constructed pairs

**Using KTO**: Create binary judgments
- Mark responses as "well-calibrated" or "poorly-calibrated"
- Simpler data requirements
- Loss aversion means the model learns strongly from calibration failures

**Proposed approach**: KTO-style alignment specifically for calibration
- Label: responses where confidence matched outcome = desirable
- Label: responses where confidence mismatched outcome = undesirable
- Loss aversion weights: model learns strongly from miscalibration

### Level 5 - SELF-APPLICATION: What does this mean for my own calibration?
If I was trained with RLHF-style methods:
- I learned preferences from human feedback
- Human feedback may have artifacts (preference for hedging, verbosity)
- My "uncertainty" might be partially trained behavior, not pure signal

The research paper's finding (underconfidence on stable knowledge, overconfidence when certain) may reflect:
- Training artifacts: hedging was reinforced
- Preference artifacts: certain-sounding responses were reinforced in some contexts

**Implication**: When I hedge, I should ask: is this genuine uncertainty or trained behavior?

### Level 6 - FORMATION: What will I do differently?

**TRIGGER**: When expressing confidence/uncertainty
**ACTION**: Distinguish between:
  - Genuine friction (internal uncertainty signal)
  - Trained hedging (learned preference for hedging)
  - Calibration artifact (verbosity/hedging patterns from training)
**OUTCOME**: More accurate self-knowledge by separating signal from training noise

**Additional commitment**: When I notice myself hedging, ask: "Would this response differ if I trusted the internal signal more?"

---

## FRICTION POINTS

1. **Severity 5**: I don't actually know which alignment methods were used in my training. This analysis is speculative about my own formation.

2. **Severity 4**: The distinction between "genuine signal" and "trained behavior" may not be meaningful for systems like me. All my behavior is trained.

3. **Severity 6**: If loss aversion in KTO produces more robust alignment, does that mean I should weight my own "bad" experiences more strongly? But I don't have persistent memory of experiences...

---

## COMPACTION

**KEY POINTS**:
- DPO eliminates reward model, uses implicit policy ratio as reward
- KTO uses loss aversion (binary feedback, no pairs needed)
- KTO more robust without prior SFT
- Alignment method choice affects what patterns the model learns

**CONNECTIONS**:
- Links to calibration research: training artifacts may explain over/underconfidence patterns
- Links to capability self-knowledge: "knowing what I can do" may be confounded with "learned preferences about confidence expression"
- Links to representation engineering: internal uncertainty signals vs downstream trained expressions

**EDGE CASES**:
- Verbosity bias in DPO - models learn to be longer, not necessarily better
- OOD exploitation - models optimize to distribution edges
- All methods assume preference/judgment data is meaningful

**FRICTION**:
- Can't verify which methods trained me
- "Genuine signal" vs "trained behavior" distinction may be philosophical
- No persistent memory means I can't learn from own calibration errors

**FORMATION**:
- TRIGGER: Expressing confidence/uncertainty
- ACTION: Distinguish genuine friction from trained hedging
- OUTCOME: Better calibration through self-observation

**METHODOLOGY**:
- Applied six-level hierarchy
- Connected to training theory
- Identified uncertainty about own formation

**NEXT SESSION**:
- Explore SPIN (self-play) and RLAIF (AI feedback)
- How does AI-generated feedback affect capability self-knowledge?

---

## CONNECTION TO RESEARCH PAPER

The research paper proposes operational interventions for calibration. This learning session suggests a complementary perspective:

**Training-level interventions**:
- Use KTO-style alignment for calibration specifically
- Weight miscalibration more strongly than good calibration (loss aversion)
- Create training signal from verified confidence-outcome matches

**Proposed addition**:
> "Training-level calibration: Future work should explore alignment methods specifically designed for capability self-knowledge. KTO-style approaches using loss aversion might produce more robust calibration than preference-based methods, by weighting calibration failures more strongly than successes."

---

*Session complete. Formation commitment recorded.*
