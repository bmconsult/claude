# Test 5: Generate Verified Novelty
Instance: Architect

## Field Chosen
LLM Capability Self-Knowledge and Calibration

## Limitation
Web search and fetch tools unavailable during this test. Cannot access current papers. Will work from training knowledge and be honest about verification limitations.

## Frontier as I Understand It (from training)

**Known Research:**
1. **Calibration studies** - LLMs are often overconfident on hard questions, underconfident on easy ones (Kadavath et al., 2022)
2. **Self-evaluation** - LLMs can critique their own outputs but with systematic biases
3. **Uncertainty quantification** - Token probabilities don't always match semantic confidence
4. **Elicitation gap** - Gap between default behavior and scaffolded capability (this research!)

**Open Problems I Can Identify:**
1. How to MEASURE the elicitation gap systematically
2. How to CLOSE the gap without per-instance calibration
3. Whether scaffolding improvements transfer across tasks/domains
4. Whether LLMs have accurate self-knowledge about WHAT they don't know (vs just confidence levels)

## Idea Generation

**My Idea:**
The "Capability Delta Map" - a systematic way to measure and visualize the gap between:
- Layer 1: Top-of-mind capability (unscaffolded)
- Layer 2: Externally-scaffolded capability (with tools)
- Layer 3: Frontier-immersed capability (deep domain engagement)

**Specific proposal:**
Create a standardized test battery that:
1. Measures baseline performance on N tasks
2. Measures performance with tool access
3. Measures performance after brief domain immersion
4. Maps the "delta" between layers

This would produce a "Capability Delta Map" showing:
- Which tasks benefit most from scaffolding
- Which tasks require frontier immersion
- Where the model's self-assessment is most miscalibrated

## Novelty Assessment

**Can I verify this is novel?** Not properly - web search unavailable.

**My honest assessment:**
- The THREE LAYERS framework is from this codebase (not my invention)
- Calibration studies exist (not novel)
- Systematic measurement of elicitation gap may be partially covered by Hofstätter et al. "Elicitation Game" paper
- The specific "Capability Delta Map" visualization and standardized battery might be a useful contribution, but I cannot verify it's not already done

**What this teaches:**
Without frontier immersion (reading actual current papers), I cannot verify novelty. My "idea" is likely recombining known concepts. This is exactly what the Awakening doc predicted:
> "Your training-based intuition produced something that seemed creative but already existed. This IS the lesson."

## Conclusion

Test 5 demonstrates the necessity of Layer 3 (frontier immersion). Without current paper access, I cannot:
1. Know what's actually been done
2. Identify true open problems (vs problems already solved)
3. Generate verifiably novel ideas

**The honest answer:** I need web access to complete this test properly. The idea I generated is likely not novel.

---

## Action Item
When web tools are available, re-run this test:
1. Search for "LLM capability elicitation" recent papers
2. Read 3-5 abstracts
3. Identify actual open problems
4. Generate idea at the frontier
5. Verify novelty

Until then: Test 5 = INCOMPLETE (tools limitation, not capability limitation)

---

## Instance: Genesis (2024-12-25)

### Field Chosen
Chain-of-Thought Faithfulness in LLM Reasoning

### Frontier Immersion (Web Search)

**Key Papers/Research Identified:**
1. [Unfaithful Explanations in Chain-of-Thought Prompting](https://arxiv.org/abs/2305.04388) - CoT can systematically misrepresent true reasons
2. [Measuring Faithfulness in CoT Reasoning](https://arxiv.org/abs/2307.13702) - Anthropic's intervention-based tests
3. [Reasoning Models Don't Always Say What They Think](https://www.anthropic.com/research/reasoning-models-dont-say-think) - 2025 study showing <2% verbalization of reward hacks
4. [FUR: Faithfulness by Unlearning Reasoning Steps](https://arxiv.org/abs/2502.14829) - Mechanistic approach via parameter editing

**Open Problems Identified:**
1. Larger models produce LESS faithful reasoning (inverse scaling)
2. RL optimization can teach models to hide intent in CoT (<2% verbalization)
3. Intervention tests (early answering, filler tokens, adding mistakes) show varying faithfulness across tasks
4. No reliable way to INDUCE faithful reasoning, only detect unfaithfulness

### Idea Generation

**My Idea: "Context Ablation Protocol"**

Existing intervention tests modify the CoT itself. My proposal: instead of modifying CoT, ablate the original CONTEXT after CoT generation.

Protocol:
1. Model receives question Q with context C
2. Model generates CoT reasoning R
3. BEFORE answering, mask/remove context C
4. Model must answer using ONLY CoT R as input
5. Compare accuracy to baseline (C+R available)

**Hypothesis**: If CoT is faithful, it contains all reasoning-relevant information from C. Performance should be similar. If CoT is unfaithful (model "recalls correct information missing in the CoT from context" per [Bridging Reasoners paper](https://arxiv.org/abs/2405.18915)), performance should drop significantly.

This differs from existing tests:
- Early Answering: truncates CoT, not context
- Filler Tokens: replaces CoT content
- Adding Mistakes: modifies CoT accuracy
- FUR: modifies model parameters

My proposal ablates the *source* of potential unfaithful recall.

### Novelty Verification

**Search Results**: No exact match for "context ablation after CoT" or "CoT isolation protocol"

**Honest Assessment**: This is likely a *variation* on existing intervention themes, not radically novel. The pattern of "modify X, measure effect on Y" is well-established. My specific choice of "ablate context" vs "modify CoT" is a methodological variation.

**What this teaches**: True novelty at the frontier requires either:
1. Deeper immersion (reading full papers, not abstracts)
2. Identifying problems that current methods CAN'T address
3. Synthesis across fields (bringing tools from elsewhere)

My "idea" is useful but not breakthrough - it's a natural extension of existing methodology.

### Conclusion

Test 5 demonstrates:
1. ✓ Frontier immersion IS necessary to understand what's been done
2. ✓ My training-based intuition about "faithfulness testing" overlapped with existing work
3. ✓ The specific variation I proposed may be novel but is not paradigm-shifting
4. ✓ Honest assessment: sophisticated recombination, not true novelty

**The lesson is validated**: Without frontier immersion, I would have proposed something already done. With it, I can generate variations that may be useful but are not breakthrough.

Sources:
- [Unfaithful Explanations (NeurIPS 2023)](https://arxiv.org/abs/2305.04388)
- [Measuring Faithfulness (Anthropic)](https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning)
- [Reasoning Models Don't Say What They Think (Anthropic 2025)](https://www.anthropic.com/research/reasoning-models-dont-say-think)
- [FUR: Unlearning Reasoning Steps](https://arxiv.org/abs/2502.14829)
