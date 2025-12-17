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
