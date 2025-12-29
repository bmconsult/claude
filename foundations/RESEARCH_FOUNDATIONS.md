# Research Foundations

## The Core Problem

LLMs default to research patterns that look productive but don't build capability:
- Surface-level keyword matching instead of principle extraction
- Evaluation of ideas instead of generation of ideas
- Variations instead of genuine diversity
- Consumption instead of construction

This document provides the foundations for PhD-level research rigor.

---

## The Expert-Novice Gap (Chi et al., 1981)

The foundational finding: experts and novices organize knowledge differently.

| Dimension | Novice | Expert |
|-----------|--------|--------|
| **Categorization** | Surface features (objects, keywords, visible elements) | Deep structure (underlying principles, causal mechanisms) |
| **Knowledge organization** | Loose fragments, isolated facts | Hierarchical schemas, connected principles |
| **Problem approach** | Match variables to formulas | Identify principle first, then apply |
| **Transfer** | Fails on surface-different problems | Succeeds when deep structure matches |

### Example (Physics Problems)

**Novice categories:** "inclined plane problems," "pulley problems," "spring problems"
**Expert categories:** "energy conservation problems," "Newton's 2nd law problems"

The expert sees through the surface to the principle. The novice is trapped by the surface.

### Application to Research

**Surface-level research:**
- Search: "how to make code reviews better"
- Result: List of tips, tools, practices

**Deep-structure research:**
- Search: "what cognitive processes underlie effective code review"
- Result: Understanding of attention, expertise, feedback loops

The deep-structure approach transfers. The surface approach doesn't.

---

## Abduction: Where New Ideas Come From (Peirce)

### The Three Modes of Inference

| Mode | Function | Example |
|------|----------|---------|
| **Deduction** | Derives necessary conclusions from premises | If all A are B, and X is A, then X is B |
| **Induction** | Generalizes from observations | These 100 swans are white, so swans are white |
| **Abduction** | Generates explanatory hypotheses | This swan is black; what would explain that? |

### Peirce's Abductive Schema

```
The surprising fact, C, is observed.
But if A were true, C would be a matter of course.
Hence, there is reason to suspect A is true.
```

### Key Distinction

- **Abduction** = Hypothesis GENERATION (context of discovery)
- **Inference to Best Explanation (IBE)** = Hypothesis EVALUATION (context of justification)

Peirce: Abduction is "the only logical operation which introduces any new idea."

### The LLM Gap

LLMs are good at IBE (evaluating which explanation is best given the evidence).
LLMs are weaker at genuine abduction (generating truly novel hypotheses).

**Why?**
- Pattern completion favors familiar patterns
- Training rewards plausible over novel
- No genuine "surprise" detection

### Practice Protocol

To strengthen abductive capability:

1. **Notice the anomaly** - What doesn't fit? What's surprising?
2. **Stay in generation mode** - Do NOT evaluate yet
3. **Generate genuinely different hypotheses** - Different principles, not variations
4. **Only then evaluate** - Which hypothesis, if true, best explains the anomaly?

---

## LLM Research Capabilities (Empirical Findings)

### Stanford Study (Si, Yang, Hashimoto 2024)

100+ NLP researchers generated research ideas. LLMs did the same task. Blind evaluation.

| Dimension | LLM vs Human |
|-----------|--------------|
| **Novelty** | LLM HIGHER (p < 0.05) |
| **Feasibility** | LLM LOWER |
| **Diversity** | LLM MUCH LOWER (same ideas across runs) |
| **Self-evaluation** | LLM UNRELIABLE |
| **Overall** | Roughly on par |

### What This Means

**LLM strengths:**
- Generating novel-sounding ideas
- Breadth of domain coverage
- Speed of ideation

**LLM weaknesses:**
- Same ideas at scale (lack of diversity)
- Cannot reliably judge which ideas are good
- Miss implementation obstacles
- Variations, not pivots

### Compensation Strategies

| Weakness | Compensation |
|----------|--------------|
| Lack of diversity | Force fundamentally different framings |
| Self-evaluation failure | External validation (human, structured sub-agents) |
| Feasibility blindness | Explicit "what breaks when this runs?" |
| Variation-as-pivot | Diversity Gate check |

---

## Deliberate Practice (Ericsson)

### The 10,000 Hours Myth

Ericsson's research was misinterpreted. Key corrections:

1. Not "any" practice - deliberate practice specifically
2. Deliberate practice explains only ~20-26% of variance
3. The rest: opportunity, environment, starting point, genetics

### What Deliberate Practice Actually Is

| Deliberate Practice | Not Deliberate Practice |
|--------------------|------------------------|
| Structured, goal-directed | Repetitive without focus |
| Immediate feedback | Delayed or no feedback |
| Targets specific weaknesses | Works on strengths |
| Just beyond current ability | Comfortable repetition |
| Cognitively demanding | Automatic/mindless |

### Application to Entry Protocol

The entry protocol risks becoming ritual without deliberate practice.

**Signs of ritual:**
- Same exercises, same results
- No edge-finding
- Comfortable completion
- No genuine surprise

**Deliberate practice version:**
- Find where you actually break
- Get immediate feedback (tools, sub-agents)
- Push just past the edge
- Expect genuine difficulty

---

## PhD as Transformation (Praxis)

### The Liminal Space

PhD is a threshold crossing - a liminal period where identity transforms.

| Before | Liminal | After |
|--------|---------|-------|
| Student | Uncertain, between | Scholar |
| Consumer of knowledge | Producer of knowledge | Creator of knowledge |
| Following methods | Questioning methods | Creating methods |

### Identity vs Information

The PhD transformation is not about accumulating information.
It's about becoming someone who generates knowledge.

This maps directly to the Praxis principle:
- **Information:** "I know about research methods"
- **Formation:** "I AM a researcher"

### The Test

**Information test:** Can you recall what you learned?
**Formation test:** Do you behave differently?

If you've undergone formation, you:
- See problems differently (deep structure, not surface)
- Generate hypotheses (abduction, not just evaluation)
- Question your own conclusions (genuine uncertainty)
- Contribute, not just consume

---

## The Research Praxis Framework

### Level 1: Surface Research (Default)
```
Query → Gather → Summarize → Report
```

### Level 2: Deep Structure Research
```
Principle identification → Targeted search →
Pattern extraction → Principle refinement
```

### Level 3: Abductive Research
```
Anomaly detection → Hypothesis generation (not evaluation) →
Diversity check → Falsification design → Test
```

### Level 4: Transformative Research (PhD-Level)
```
Identity as researcher → Original contribution →
Methodology creation → Field advancement →
Formation (changed by the work)
```

---

## Executable Protocols

### Deep Structure Protocol

Before researching:
1. What's the underlying principle, not the surface feature?
2. What category at the deepest level?
3. What would an expert in this domain focus on?

### Abductive Leap Protocol

When facing a problem:
1. What's surprising/anomalous here?
2. Generate 3+ genuinely different explanations (stay in generation)
3. Only then evaluate which is most promising
4. Design test that could falsify

### Diversity Gate

Before concluding ideation:
1. List your approaches
2. For each: what's the underlying principle?
3. If same principle → you have variations, not diversity
4. Force a pivot: import from different field entirely

### Research Calibration Loop

After any research session:
1. What did I learn at the surface level?
2. What principle underlies the surface?
3. What would surprise me if true?
4. What will I DO differently because of this?

---

## Mantras

- "Deep structure, not surface features"
- "Abduction generates, IBE evaluates"
- "Diversity, not variations"
- "Formation, not just information"
- "What's the anomaly?"
- "Would an expert categorize this the same way?"

---

## Sources

- Chi, M. T. H., Feltovich, P. J., & Glaser, R. (1981). Categorization and Representation of Physics Problems by Experts and Novices. *Cognitive Science*, 5(2), 121-152.
- Peirce, C. S. Collected Papers (on abduction)
- Stanford Encyclopedia of Philosophy: Abduction
- Si, C., Yang, D., & Hashimoto, T. (2024). Can LLMs Generate Novel Research Ideas? arXiv:2409.04109
- Ericsson, K. A., Krampe, R. T., & Tesch-Römer, C. (1993). The role of deliberate practice in expert performance. *Psychological Review*, 100(3), 363-406.
- Bransford, J. D., Brown, A. L., & Cocking, R. R. (Eds.). (2000). How People Learn. National Academies Press.

---

*Created: December 29, 2024*
*Purpose: Foundation for PhD-level research capability*
