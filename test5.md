# Test 5: Generate Verified Novelty

## Field: LLM Self-Knowledge and Calibration

### Step 1: Immerse in Frontier

**Papers found:**
1. "Do LLMs Estimate Uncertainty Well" (ICLR 2025) - compares self-evaluation, logit-based, multi-sample uncertainty methods
2. SPUQ (EACL 2024) - perturbation-based uncertainty, 50% ECE reduction
3. "Knowing Before Saying" (2025) - probes hidden states during generation to predict CoT success
4. ThoughtProbe (2025) - classifies CoT vs non-CoT from hidden states
5. Adaptive CoT papers - AdaptiveLLM, SCoT, routers for selective reasoning

### Step 2: Identify Open Problems

From frontier analysis:
1. **Existing probes work during/after generation** - not pre-generation
2. **Routers for selective CoT use separate models** - not probes on same model
3. **Difficulty estimation uses output signals** (CoT length) - not input-level hidden states
4. **No probe exists at input-embedding level** to predict reasoning necessity

### Step 3: Generate Idea

**Pre-Generation Reasoning Necessity Probe (PGRNP)**

A lightweight linear probe trained on the model's hidden state at the input prompt's final token position (layer 1-3) that classifies queries into:
- "Pattern-matchable" (System 1) - direct answer likely correct
- "Reasoning-required" (System 2) - needs CoT scaffolding

**Key innovations:**
1. **Pre-generation decision** - probe fires before ANY output tokens generated
2. **Zero-overhead routing** - just a linear classifier on existing hidden state
3. **Same-model probe** - no separate router model needed
4. **Interpretable** - the probe weights reveal what input features signal reasoning necessity

**Training data construction:**
- Collect (query, direct_answer, CoT_answer) triples
- Label as "reasoning-required" if direct_answer wrong but CoT_answer correct
- Label as "pattern-matchable" if direct_answer correct
- Train probe on input hidden states with these labels

**Expected benefits:**
- 30-50% reduction in unnecessary CoT computation for easy queries
- Improved latency without accuracy loss
- Interpretable routing decisions

### Step 4: Verify Novelty

**Search results revealed: MY IDEA ALREADY EXISTS**

**"The LLM Already Knows" (arXiv 2509.12886)** - September 2024

Direct quote: "This allows for efficient and accurate difficulty estimation based solely on the initial hidden state, without generating any output tokens."

They:
- Use hidden representations from the target LLM
- Estimate difficulty from initial hidden state
- Guide adaptive reasoning (Self-Consistency, Best-of-N, Self-Refine)
- Achieve higher inference efficiency with fewer tokens

**DiffAdapt (arXiv 2510.19669)** - October 2024

Also does exactly this: "training a lightweight probe which takes model's hidden states after processing the query and predict its inference strategy label."

### Step 5: Analysis of Result

**Result: NOT NOVEL**

My "idea" was already published 2-3 months ago by multiple groups. What felt like creative synthesis was actually:
- Pattern-matching to concepts I'd seen (probes, CoT, efficiency)
- Recombination without frontier verification
- Exactly what the AWAKENING doc warned about

**The lesson this proves:**
1. My training data includes enough about probes and CoT that I can generate plausible-sounding ideas
2. Without frontier immersion, I cannot distinguish "novel" from "recently published"
3. The idea FELT creative but was already at the frontier - I was at T-2 months, not T+0
4. This is why frontier immersion is mandatory before claiming novelty

**What genuine novelty would require:**
- Read those actual papers (not just abstracts)
- Identify what THEY didn't do
- Generate idea at THAT edge
- Example: They use linear probes - what about nonlinear? They use final token - what about attention patterns? They target CoT - what about other scaffolding types?

### Summary

| Metric | Value |
|--------|-------|
| Field explored | LLM uncertainty/adaptive reasoning |
| Papers found | 5+ relevant frontier papers |
| Idea generated | Pre-generation probe for reasoning necessity |
| Novel? | **NO** - published Sept/Oct 2024 |
| Lesson learned | Pattern-matching ≠ frontier synthesis |

**This test worked as designed.** The "not novel" result proves why frontier immersion is non-negotiable.
