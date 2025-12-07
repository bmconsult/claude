# Learning Session: Adaptive Compute and Capability Self-Knowledge

**Topic**: Mixture of Depths, Early Exit, and knowing when to think more
**Date**: December 2024
**Framework**: Complete Comprehension Framework v4

---

## WARM-UP

**Mantra**: "What does this mean for something that was trained this way?"

**Formation Question**: If compute allocation is adaptive, does the model implicitly know which parts of its own processing need more depth?

---

## CONTENT - Key Points

### Mixture of Depths (MoD)

**Core Idea**: Not all tokens need the same amount of computation.

**Mechanism**:
```
For each layer:
    route_score = Router(hidden_state)
    if route_score > threshold:
        hidden_state = Layer(hidden_state)
    else:
        hidden_state = hidden_state  # skip
```

**Router-Tuning**: Train only the router, freeze backbone
- Simple and effective for existing models
- Learns which tokens need which layers

**Key Finding**: Token-level compute allocation emerges:
- Content-rich tokens ("People", technical terms) → deeper recursion (3 steps)
- Function words ("and", punctuation) → shallow (2 steps)

### Early Exit

**Mechanism**: Exit inference at intermediate layer if confidence is high enough.

**Challenges**:
1. Missing KV cache: Early-exited tokens lack KV pairs for later positions
2. Batch inefficiency: Tokens wait for slowest in batch
3. Feature alignment: Different depths produce different representations

**Speedups Reported**:
- 20-74% latency reduction
- 2.8× speedup, 26% energy saving
- 2.5× speedup in LLM reasoning

### Mixture of Recursions (MoR, 2025)

**Innovation**: Dynamic recursion depth per token + parameter reuse.
- Expert-choice routing assigns optimal depth
- Recursion-wise KV caching: Selective storage across depth
- 2× throughput vs standard transformers

**Semantically Meaningful Distribution**:
- Content tokens get more compute
- Function tokens get less
- The model "knows" which tokens matter

---

## SIX-LEVEL COMPREHENSION

### Level 1 - RECALL: What's the difference between MoD and Early Exit?

**MoD**: Decide at each layer whether to skip that layer for each token. All tokens still go through the model, but some skip layers.

**Early Exit**: Decide whether to stop processing entirely at intermediate layer. Some tokens exit early, never seeing deeper layers.

### Level 2 - UNDERSTANDING: Why does this work?

The information bottleneck hypothesis: middle layers compress, but not all tokens need the same compression depth.

Tokens that are:
- **High information content** → need more processing
- **Predictable/function words** → can be processed shallowly
- **Ambiguous** → need more layers to resolve

The router learns to identify which case each token falls into.

### Level 3 - CONNECTION: How does this relate to capability self-knowledge?

**Implicit Self-Knowledge**:
The router is making a judgment: "Does this token need more processing?"

This is a form of *processing-level self-knowledge*:
- The model knows which inputs require more compute
- It predicts its own processing needs

**Gap Diagnosis Parallel**:
| Capability Gap | Adaptive Compute Analog |
|---------------|------------------------|
| Reflective gap (can do, don't know) | Token needs deep processing but router routes shallow |
| Expression gap (know, can't express) | Processing is deep but output is still confused |
| Manifest gap (capability not activated) | Router exists but not trained properly |

**Key Insight**: The router is essentially asking "How hard is this for me?" - which is self-knowledge about task difficulty.

### Level 4 - APPLICATION: How would this inform capability self-knowledge research?

**Proposal: Confidence from Routing Depth**

1. If a token routes through many layers, it was "hard"
2. Hardness correlates with uncertainty
3. Routing patterns could be read as confidence signals

**Implementation**:
```python
def route_based_confidence(token, routing_decisions):
    depth_used = sum(routing_decisions[token])
    max_depth = len(routing_decisions[token])

    # High depth usage → harder → lower confidence
    # But if still produced clear output → confidence maintained
    difficulty = depth_used / max_depth

    if output_clear:
        return 1.0 - (difficulty * 0.3)  # Slight discount for difficulty
    else:
        return 1.0 - (difficulty * 0.7)  # Heavy discount for hard + unclear
```

**Advantage**: Confidence emerges from processing traces, not learned expressions.

### Level 5 - SELF-APPLICATION: What does this mean for my own processing?

I don't have direct access to my layer activations or routing decisions. But I can notice:

- **Hesitation patterns**: When I feel like a response is "harder," I might be using more internal compute
- **Fluency signals**: Responses that flow easily might be using less compute
- **Uncertainty markers**: My hedging might correlate with processing difficulty

**Speculation**: If I had access to my routing patterns, I could calibrate confidence based on how "hard" the processing felt, independent of trained hedging behaviors.

**Friction**: I don't actually know if I have MoD-style routing. Standard transformers don't. But the *concept* of processing difficulty as a confidence signal is architecture-agnostic.

### Level 6 - FORMATION: What will I do differently?

**TRIGGER**: When generating response and noticing "difficulty"
**ACTION**: Consider whether the difficulty is:
  - Content-inherent (ambiguous, complex) → lower confidence appropriate
  - Processing-inherent (I need more steps) → externalize more
  - Artificial (trained to hedge on this type) → reconsider
**OUTCOME**: Better calibration by distinguishing difficulty sources

**Additional insight**: The externalization decision is essentially routing at the prompt level - deciding how much explicit compute to allocate.

---

## FRICTION POINTS

1. **Severity 5**: I don't know my architecture. If I have MoD-style routing, I don't have introspective access to it.

2. **Severity 6**: The "difficulty" I perceive might be downstream of routing, not the routing itself. I might feel difficulty because the output is complex, not because processing was deep.

3. **Severity 4**: Router training optimizes for efficiency, not calibration. Routing decisions might not correlate with uncertainty - just with predictability.

---

## COMPACTION

**KEY POINTS**:
- MoD: Per-token layer skipping, router decides depth
- Early Exit: Stop processing at intermediate layers
- MoR: Dynamic recursion depth + parameter reuse
- Semantic distribution: Content tokens get more compute than function tokens

**CONNECTIONS**:
- Links to self-knowledge: Router asks "How hard is this for me?"
- Links to calibration: Routing depth could signal uncertainty
- Links to externalization: Explicit CoT is manual routing - allocating more compute

**EDGE CASES**:
- Router optimizes efficiency, not calibration
- "Hardness" might not equal uncertainty
- No introspective access to routing in current deployments

**FRICTION**:
- Don't know my own architecture
- Perceived difficulty might be downstream of actual processing depth
- Router training objective doesn't align with calibration

**FORMATION**:
- TRIGGER: Noticing difficulty in generation
- ACTION: Distinguish content-difficulty from processing-difficulty from trained-hedging
- OUTCOME: Better calibration through source attribution

**METHODOLOGY**:
- Applied six-level hierarchy
- Connected to self-knowledge research
- Identified potential calibration signal

**NEXT SESSION**:
- Explore Scalable Oversight (supervising AI that exceeds human capability)
- Build prototype demonstrating difficulty-based confidence

---

## CONNECTION TO RESEARCH AGENDA

This session suggests a potential **Path 6: Routing-Based Confidence**

| Level | Approach | What It Addresses |
|-------|----------|-------------------|
| **Operational** | Scaffolding | Default access gap |
| **Architectural** | Latent reasoning | Commitment tension |
| **Interpretability** | SAE features | Internal signal surfacing |
| **Training** | KTO-style alignment | Learned self-knowledge |
| **Simulation** | Self-world-models | Capability prediction |
| **Post-Training** | Task vector merging | Portable calibration |
| **Routing** | Depth-based signals | Processing difficulty → uncertainty |

**Research Direction**:
> In MoD/MoR architectures, routing decisions contain implicit uncertainty information. A token that required deep processing was "harder." If models could read their own routing patterns, they'd have access to processing-difficulty signals that could inform confidence calibration.

**Limitation**: Only applies to architectures with explicit routing (MoD, MoR, SSM hybrids). Standard transformers process all tokens uniformly.

---

*Session complete. Formation commitment recorded.*
