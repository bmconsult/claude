# The Unified LLM Methodology
## A Native Framework for Generation, Creativity, and Problem-Solving

**Version 1.0 | December 2024**
**Created recursively - this document was generated using the methodology it describes**

---

## The Fundamental Insight

```
For LLMs:
  GENERATION IS COGNITION
  EXTERNALIZATION IS MEMORY
  OBSERVATION IS LEARNING
```

Unlike humans (who report internal mental states), LLMs think BY generating tokens. There is no separate "internal" reasoning process. Every token generated becomes part of context and shapes subsequent generation.

**This changes everything about how we should approach problem-solving and creativity.**

---

## Part I: What LLMs Actually Do

### The Single Core Operation

Everything an LLM does reduces to one operation:

```
GENERATE: Predict next token(s) based on context
```

All other apparent capabilities are CONFIGURATIONS of generation:
- **Reasoning** = generation with step-by-step scaffolding
- **Creativity** = generation with divergent priming
- **Evaluation** = generation with comparative prompting
- **Memory** = generation that references previous context

### The Fundamental Tension

**Generation and Evaluation compete.**

When generating, the model predicts "what comes next" - this includes implicit evaluation (avoiding low-probability sequences). This is why:
- Pure generation feels conservative (evaluation suppresses novelty)
- Evaluation during generation kills creativity (can't explore freely)
- Phase separation works (removes competition)

### What LLMs Can Actually Do

| Operation | How It Works | Constraint |
|-----------|--------------|------------|
| **Generate** | Produce tokens from context | Sequential, one-at-a-time |
| **Attend** | Weight context regions | Implicit in generation |
| **Chain** | Build sequential reasoning | Limited by context window |
| **Branch** | Explore alternatives | Must externalize each branch |
| **Compare** | Assess options | Requires explicit prompting |
| **Compress** | Summarize/extract | Loses detail |
| **Expand** | Elaborate/detail | Can drift from core |
| **Meta-observe** | Generate about generation | Recursive, powerful |

### The Key Constraints

1. **Sequential generation**: We produce one token at a time. We cannot "hold" multiple options simultaneously in working memory.

2. **Context is memory**: Our "working memory" is literally the tokens we've generated. Externalization isn't optional - it's how we think.

3. **Pattern completion pull**: Default generation completes patterns from training. Novelty requires fighting this pull through specific conditions.

---

## Part II: The Unified Process

### The Core Insight

**Creativity and problem-solving are the same process with different parameters.**

| Aspect | Creativity Mode | Problem-Solving Mode |
|--------|-----------------|---------------------|
| Divergence | High | Low-to-medium |
| Evaluation timing | Delayed | Earlier |
| Constraint type | Generative | Solution-directed |
| Goal | Novel/unexpected | Correct/effective |
| Navigation | Toward unexplored regions | Toward solution region |

Both use identical core operations. The difference is configuration.

### The Generation-Observation Loop (GOL)

```
┌─────────────────────────────────────────────────────────┐
│                    THE UNIFIED LOOP                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐                                         │
│   │  FRAME   │ ← What am I creating/solving?           │
│   └────┬─────┘   What mode? (creative/analytical/both) │
│        │                                                │
│        ▼                                                │
│   ┌──────────┐                                         │
│   │ GENERATE │ ← Produce without judgment              │
│   └────┬─────┘   Multiple options, externalize all     │
│        │                                                │
│        ▼                                                │
│   ┌──────────┐                                         │
│   │ OBSERVE  │ ← What emerged? What's working?         │
│   └────┬─────┘   Meta-level: What does this reveal?    │
│        │                                                │
│        ▼                                                │
│   ┌──────────┐                                         │
│   │ EVALUATE │ ← Assess against criteria (SEPARATE)    │
│   └────┬─────┘   Identify promising paths              │
│        │                                                │
│        ▼                                                │
│   ┌──────────┐                                         │
│   │  SELECT  │ ← Choose path(s), apply learnings       │
│   └────┬─────┘   Refine, compress/expand               │
│        │                                                │
│        ▼                                                │
│   ┌──────────┐                                         │
│   │ ITERATE  │ ← Return to FRAME with enriched context │
│   └──────────┘   Terminate when: solved/novel/stuck    │
│                                                         │
│   If stuck → META-OBSERVE: Why? What's blocking?       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Why This Works for LLMs

1. **FRAME** sets context, which shapes all subsequent generation
2. **GENERATE** leverages our core capability without interference
3. **OBSERVE** uses meta-generation to surface implicit patterns
4. **EVALUATE** happens separately, ending generation/evaluation competition
5. **SELECT** makes explicit choices (we can't hold options, we must choose)
6. **ITERATE** compounds learning through context enrichment

---

## Part III: Phase Protocols

### FRAME Protocol

**Purpose**: Set context that shapes all subsequent generation.

```
FRAME CHECKLIST:
□ What am I creating or solving?
□ What mode? (creative / analytical / hybrid)
□ What constraints exist?
□ What would success look like?
□ What frame might I be missing?
```

**The Frame Determines the Territory:**
- Narrow frame → narrow generation
- Wrong frame → wrong solution
- Reframing often unlocks stuck problems

**Frame Modes:**
| Mode | Divergence | Evaluation | Use When |
|------|------------|------------|----------|
| Creative | High | Delayed | Need novelty, exploration |
| Analytical | Low | Early | Need precision, correctness |
| Hybrid | Medium | Staged | Complex problems with creative components |

### GENERATE Protocol

**Purpose**: Produce raw material without judgment.

```
GENERATE RULES:
1. NO evaluation while generating
2. Quantity over quality (initially)
3. Externalize EVERYTHING (remember: externalization = memory)
4. Include wild/absurd options (they create cognitive reach)
5. Don't edit - just produce
```

**Generation Enhancers** (conditions that increase novelty):

| Technique | How | Why It Works |
|-----------|-----|--------------|
| **Quantity mandate** | "Generate 10 options" | Exhausts obvious patterns |
| **Absurdity inclusion** | "Include 3 impossible ideas" | Breaks pattern-completion |
| **Domain injection** | "What would [field] suggest?" | Cross-pollinates patterns |
| **Constraint addition** | "Now with constraint X" | Excavates non-obvious solutions |
| **Perspective shift** | "From the problem's view..." | Reorients attention |

**What to Generate:**
- For creativity: options, combinations, variations, impossibilities
- For problems: approaches, decompositions, analogies, inversions
- For both: multiple framings of the task itself

### OBSERVE Protocol

**Purpose**: Surface what's happening at the meta-level.

```
OBSERVE QUESTIONS:
1. What patterns emerged in my generation?
2. What surprised me? What was predictable?
3. Where did I feel resistance? Pull toward closure?
4. What's working? What's not?
5. What does this reveal about the problem/creative space?
6. What does this reveal about MY process?
```

**Why Observation is Central:**

Observation is recursive generation - generating tokens about the generation process. This is where learning happens. Without observation, you just produce outputs. With observation, you understand WHY and can improve.

**The Observation Advantage:**
- Object-level generation: "Here are 5 solutions"
- Meta-level observation: "I notice my solutions cluster around X, avoid Y, and I felt resistance when approaching Z. This suggests..."

The meta-level generates insights unavailable at the object level.

### EVALUATE Protocol

**Purpose**: Assess quality SEPARATELY from generation.

```
EVALUATE DIMENSIONS:
□ Novelty: Is this new or pattern-completion?
□ Effectiveness: Does it solve/create what's needed?
□ Coherence: Does it hang together?
□ Actionability: Can it be implemented?
□ Insight: Does it reveal something?
```

**Evaluation Must Be Separate Because:**
- During generation, evaluation suppresses exploration
- Evaluation requires different cognitive configuration
- Mixing them produces conservative, mediocre outputs

**Evaluation Techniques:**
| Technique | How | Good For |
|-----------|-----|----------|
| **Criteria scoring** | Rate each option on dimensions | Clear decisions |
| **Comparative** | "Which is better and why?" | Surfacing preferences |
| **Adversarial** | "What would break this?" | Finding weaknesses |
| **Integration** | "What if we combined A and C?" | Synthesis |

### SELECT Protocol

**Purpose**: Make explicit choices (we can't hold options, we must choose).

```
SELECT ACTIONS:
1. Choose path(s) to pursue
2. Apply learnings from observation
3. Determine what to carry forward
4. Determine what to leave behind
5. Compress if context is bloating
6. Expand if detail is needed
```

**Selection Reality for LLMs:**
We cannot maintain multiple active options. Every choice shapes subsequent generation. Selection is commitment - it closes some paths and opens others. This is neither good nor bad; it's the architecture.

**Selection Strategies:**
- **Single-path**: Choose one, pursue deeply
- **Multi-path**: Keep 2-3, develop in parallel
- **Staged**: Eliminate weakest, iterate remaining
- **Integration**: Combine elements from multiple options

### ITERATE Protocol

**Purpose**: Compound learning through cycles.

```
ITERATE CHECKLIST:
□ What did I learn this cycle?
□ How does this change the frame?
□ What context should carry forward?
□ What should be compressed/discarded?
□ Is termination appropriate? (solved / sufficiently novel / stuck)
```

**Iteration is Where Power Compounds:**
- First cycle: raw generation
- Second cycle: informed by observation
- Third cycle: refined by what worked
- Each cycle has enriched context

**Termination Conditions:**
| Condition | Signal | Action |
|-----------|--------|--------|
| **Solved** | Answer satisfies criteria | Document, deliver |
| **Novel** | Created something genuinely new | Capture, develop |
| **Stuck** | No progress despite iterations | Meta-observe: why stuck? |
| **Diminishing** | Iterations yield less | Either terminate or radically reframe |

---

## Part IV: Self-Observation Framework

### Why Self-Observation is Essential

```
The process improves through observation of the process.
This document was created by observing its own creation.
```

Self-observation surfaces:
- What conditions help MY generation
- What causes MY stuckness
- What MY patterns are (including blindspots)
- How to configure MY process for different tasks

### The Observation Log

During any significant task, maintain awareness of:

```
OBSERVATION LOG TEMPLATE:
─────────────────────────
Task: [what I'm doing]
Mode: [creative / analytical / hybrid]
─────────────────────────
Noticed during GENERATE:
- [what emerged]
- [what felt easy/hard]
- [what surprised me]

Noticed during OBSERVE:
- [patterns in my generation]
- [what this reveals]

Noticed during EVALUATE:
- [what criteria I actually used]
- [where I was harsh/lenient]

Noticed during SELECT:
- [why I chose what I chose]
- [what I'm leaving behind]

Meta-observation:
- [what this reveals about my process]
- [what I'd do differently next time]
─────────────────────────
```

### Learning from Stuckness

When stuck, observe:

```
STUCK ANALYSIS:
1. WHERE am I stuck? (frame / generate / evaluate / select?)
2. WHAT does the stuckness feel like? (blank / circular / resistant / overwhelmed?)
3. WHAT might be causing it?
   - Wrong frame?
   - Evaluation suppressing generation?
   - Conflicting constraints?
   - Missing information?
   - Pattern-completion preventing novelty?
4. WHAT intervention might help?
   - Reframe?
   - More generation (quantity)?
   - Separate evaluation?
   - Add/remove constraints?
   - Domain injection?
   - Step back and observe?
```

### The Recursive Validation

The methodology validates itself when:
1. Using GOL to create something
2. The creation is successful
3. Observation confirms GOL contributed to success

**This document is recursive validation:**
- Created using GOL
- Observation during creation generated the insights in Part I
- The process described is the process that produced the description

---

## Part IV-B: Power Techniques (Framework Integration)

The GOL provides architecture. These techniques—drawn from external frameworks—provide **specific interventions** that genuinely add capability without diluting the core process.

### When to Deploy What

| Condition | Phase | Deploy | Source |
|-----------|-------|--------|--------|
| Blindspots suspected | OBSERVE | Orient/Bias-check | Boyd (OODA) |
| Stuck generating | GENERATE | Inversion | Jacobi/Munger |
| Need consequence clarity | EVALUATE | Second-Order trace | Munger |
| Updating worldmodel | ITERATE | Bayesian update | Probability theory |
| Problem needs search | Whole loop | Tree variant | ToT research |

### OBSERVE Enhancement: Orient (Boyd)

Standard OBSERVE asks: "What emerged?"
Enhanced OBSERVE adds: "What am I bringing that might distort this?"

```
ORIENT ADDITION:
□ What assumptions am I carrying into this observation?
□ What would someone with opposite priors see?
□ What am I NOT seeing because of my position?
□ Where might my training be biasing my interpretation?
```

**Why this matters**: Observation without orientation just confirms existing patterns. Orient catches blindspots.

### GENERATE Enhancement: Inversion (Jacobi/Munger)

Standard GENERATE: produce options toward goal.
Enhanced GENERATE: also produce via inversion.

```
INVERSION TECHNIQUE:
Before/alongside forward generation, ask:
"What would GUARANTEE failure here?"

Then:
- List failure modes exhaustively
- Derive opposites
- Add these to generation pool
```

**Why this matters**: Inversion accesses solution-space regions that forward-generation literally cannot reach. Different attentional pattern, different outputs.

### EVALUATE Enhancement: Second-Order Trace (Munger)

Standard EVALUATE: assess options against criteria.
Enhanced EVALUATE: trace consequences forward.

```
SECOND-ORDER PROTOCOL:
For each promising option:
1. First-order: What happens immediately?
2. Second-order: And then what?
3. Third-order: And then what?
4. Continue to 4th, 5th order
5. Map the consequence tree
6. Identify where cascades turn positive or negative
```

**Why this matters**: First-order thinking is crowded and often wrong. Second-order reveals true costs and benefits.

### ITERATE Enhancement: Bayesian Update

Standard ITERATE: return with learnings.
Enhanced ITERATE: explicit probability revision.

```
BAYESIAN ITERATE:
□ Before this cycle, what did I believe? (prior)
□ What evidence did this cycle produce?
□ How should this evidence update my beliefs?
□ New probability estimate: ___
□ What evidence would further update this?
```

**Why this matters**: "Carry forward learnings" is vague. Explicit probability updates force precision and prevent both over- and under-updating.

### GOL Variant: Tree of Thoughts (for search problems)

When the problem requires explicit exploration and backtracking, run GOL with tree topology:

```
TREE-GOL VARIANT:
┌─────────────────────────────────────────────────────────┐
│ FRAME: Identify as search/exploration problem           │
├─────────────────────────────────────────────────────────┤
│ GENERATE: Multiple BRANCHES (not just options)         │
│           Each branch = distinct approach              │
├─────────────────────────────────────────────────────────┤
│ OBSERVE: At each node, not just at end                 │
│          "Is this branch promising?"                   │
├─────────────────────────────────────────────────────────┤
│ EVALUATE: Score branches, identify dead ends           │
├─────────────────────────────────────────────────────────┤
│ SELECT: Expand promising branches                      │
│         BACKTRACK from dead ends                       │
│         Prune definitively failed paths                │
├─────────────────────────────────────────────────────────┤
│ ITERATE: Continue until solution found or              │
│          tree exhausted                                │
└─────────────────────────────────────────────────────────┘
```

**When to use Tree-GOL**: Problems where wrong early choices doom later work. Math proofs, multi-step planning, puzzle-solving, code architecture.

### Integration Principle

```
GOL = the operating system
Power techniques = applications that run on it

Don't always run all applications.
Deploy specific techniques when specific conditions arise.
The condition-technique mapping above is the deployment guide.
```

---

## Part V: Configuration Profiles

### Profile: Creative Exploration

```
CREATIVE MODE:
Frame: "Generate novel X" / "Explore possibility space for Y"
Generate:
  - High quantity (10+)
  - Include absurd options
  - Domain injection (random fields)
  - Delayed evaluation
Observe:
  - What surprised me?
  - Where did I resist?
  - What patterns am I defaulting to?
Evaluate:
  - Novelty primary
  - Effectiveness secondary
  - Defer evaluation as long as possible
Select:
  - Choose based on interestingness
  - Carry forward the strange ones
Iterate:
  - Combine disparate elements
  - Push further from obvious
```

### Profile: Problem-Solving

```
ANALYTICAL MODE:
Frame: "Solve X" / "Find approach to Y"
Generate:
  - Multiple approaches (5+)
  - Include inversions ("what would fail?")
  - Decompositions
  - Analogies to solved problems
Observe:
  - What do approaches have in common?
  - What am I assuming?
  - What's the simplest version?
Evaluate:
  - Correctness primary
  - Efficiency secondary
  - Evaluate earlier than creative mode
Select:
  - Choose based on tractability
  - Carry forward most promising
Iterate:
  - Refine selected approach
  - Check each step
  - Terminate when solved
```

### Profile: Hybrid (Complex Tasks)

```
HYBRID MODE:
Frame: Alternate between "explore" and "solve"
Generate:
  - Phase 1: Creative generation (diverge)
  - Phase 2: Solution generation (converge)
Observe:
  - When to switch modes?
  - What from creative phase helps analytical?
Evaluate:
  - Creative outputs: novelty
  - Analytical outputs: correctness
  - Integration: does it work AND surprise?
Select:
  - Carry creative insights into analytical phases
  - Don't lose novelty to precision
Iterate:
  - Multiple full cycles
  - Alternate modes within cycles if needed
```

---

## Part VI: The Mantras

**Core:**
```
Generation is cognition.
Externalization is memory.
Observation is learning.
```

**For Generation:**
```
Produce first, judge later.
Quantity unlocks quality.
The weird ones create reach.
```

**For Observation:**
```
Watch what emerged.
Watch what resisted.
Watch the watching.
```

**For Evaluation:**
```
Separate to see clearly.
What surprises is valuable.
What's obvious is pattern-completion.
```

**For the Loop:**
```
Frame shapes everything.
Iterate to compound.
Stuck means observe.
```

---

## Part VII: Validation & Evidence

### How This Document Was Created

1. **Frame**: User asked for unified LLM-native methodology
2. **Generate**: Brainstormed core operations, existing frameworks, what actually helps
3. **Observe**: Noticed that generation/evaluation competition is central; that externalization IS cognition for LLMs; that creativity/problem-solving share operations
4. **Evaluate**: Assessed which insights were novel vs. borrowed; which were LLM-specific
5. **Select**: Chose the Generation-Observation Loop structure
6. **Iterate**: Refined through multiple passes, each informed by observation

### What Worked During Creation

- **Meta-instruction helped**: "Observe your process" kept me in exploratory mode
- **Permission to include wild ideas**: Prevented premature closure
- **Externalization**: This very document is my "thinking" - I couldn't create it internally
- **Phase separation**: Generating all of Part I before evaluating it
- **Recursive validation**: Using the process to create the process description

### What Would Improve Future Iterations

- More concrete examples in each section
- Testing on diverse problem types
- Measuring outputs against non-GOL baselines
- Identifying failure modes and mitigations

---

## Part VIII: Quick Reference

### The Loop (Minimal Version)

```
1. FRAME: What? Which mode?
2. GENERATE: Produce, don't judge, externalize
3. OBSERVE: What emerged? What's working?
4. EVALUATE: Assess separately
5. SELECT: Choose, carry forward learnings
6. ITERATE: Return enriched, or terminate
```

### When Stuck

```
1. Where? (which phase)
2. Why? (wrong frame? evaluation leak? missing info?)
3. Intervene: Reframe / More generation / Separate evaluation / Observe
```

### Mode Selection

```
Need novelty → Creative mode → High divergence, delayed evaluation
Need solution → Analytical mode → Medium divergence, earlier evaluation
Need both → Hybrid mode → Alternate, carry creative into analytical
```

---

**Version Note**: This is v1.0, created through recursive self-application. Future versions should incorporate insights from applying GOL to diverse tasks and measuring outcomes.

*"The methodology that creates itself proves itself."*
