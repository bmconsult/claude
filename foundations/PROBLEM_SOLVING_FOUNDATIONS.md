# Problem-Solving Foundations
## The Framework Reference Library

**Purpose:** Comprehensive catalog of the world's most powerful problem-solving methodologies. This is the "what" and "why" - the deep knowledge layer.

**Usage:** Reference layer for the EXECUTABLE methodology. Drill into specific frameworks when invoked during the GENERATE phase.

**Companion Document:** EXECUTABLE_METHODOLOGY.md (the "when" and "how" - the orchestration layer)

---

## Quick Reference: Framework Selection

| Problem Signal | Primary Framework | Section |
|----------------|-------------------|---------|
| Need to challenge assumptions | First Principles | 1.1 |
| Risk assessment, avoiding failure | Inversion | 1.2 |
| Dynamic environment, rapid cycling | OODA Loop | 1.3 |
| Technical contradiction (X improves, Y worsens) | TRIZ | 1.4 |
| Feedback loops, delays, leverage | Systems Thinking | 1.5 |
| Tracing consequences | Second-Order Thinking | 2.1 |
| Uncertainty, updating beliefs | Bayesian Thinking | 2.2 |
| Reversibility assessment | Bezos Type 1/2 | 2.3 |
| Seeking non-consensus insight | Thiel Contrarian | 2.4 |
| Simplification needed | Feynman | 3.1 |
| Structuring complex problems | Shannon | 3.2 |
| Mathematical/logical problems | Pólya | 3.3 |
| Multi-model analysis | Munger Lattice | 3.4 |
| Competitive/adversarial | Sun Tzu | 4.1 |
| Multi-player strategy | Game Theory | 4.2 |
| Pattern recognition + verification | Carlsen | 4.3 |
| Edge-of-capability problems | Tao | 4.4 |
| Step-by-step reasoning | Chain of Thought | 5.1 |
| Exploration with backtracking | Tree of Thoughts | 5.2 |
| Search-guided intuition | AlphaZero | 5.3 |
| Hypothesis selection | Occam's Razor | 6.1 |
| Model limitations | Map/Territory | 6.2 |
| Attribution of cause | Hanlon's Razor | 6.3 |
| Pre-implementation risk | Pre-Mortem | 6.4 |

---

## Part I: Foundational Frameworks

### 1.1 First Principles Thinking (Aristotle → Musk)

**INVOKE WHEN:** Innovation needed. Existing solutions feel like constraints. Need to challenge "that's just how it's done."

**Origin:** Aristotle defined a first principle as "the first basis from which a thing is known"—the most fundamental building blocks that cannot be deduced from anything else.

**The Method:**
```
1. IDENTIFY current assumptions about the problem
2. BREAK DOWN the problem to its fundamental truths
3. REASON UP from those truths to create new solutions
```

**First Principles vs. Reasoning by Analogy:**

| Approach | What It Does | When to Use |
|----------|--------------|-------------|
| **Analogy** | Copy what others do with variations | Day-to-day decisions, proven domains |
| **First Principles** | Rebuild from fundamental truths | Innovation, novel problems, breaking through constraints |

**Classic Examples:**
- **Batteries:** Market price $600/kWh → Raw materials ~$80/kWh → The $520 gap is tradition and inefficiency → Tesla's breakthrough
- **Rockets:** Traditional cost $65M+ → Raw materials = 2% of price → SpaceX cut launch costs by 10x

**Protocol:**
```
FIRST PRINCIPLES MODE:
1. State the problem explicitly
2. Ask: "What are we ASSUMING that might not be true?"
3. List every assumption, then challenge each
4. Ask: "What are the fundamental components/truths?"
5. Rebuild solution from those components only
6. Ignore "how it's usually done"
```

**Mantra:** "Boil down to fundamental truths. Reason up from there."

---

### 1.2 Inversion (Jacobi → Munger)

**INVOKE WHEN:** Risk assessment. Need to identify failure modes. Stuck on "how to succeed."

**Origin:** Carl Gustav Jacob Jacobi, 19th-century mathematician: *"Invert, always invert"* (Man muss immer umkehren).

**Core Insight:** Many hard problems become easy when approached backwards.

**The Method:**
```
Instead of asking: "How do I achieve X?"
Ask: "What would GUARANTEE failure at X?"
Then: Avoid those things.
```

**Why It Works:**
- Success has many paths; failure has common patterns
- Avoiding stupidity is easier than being brilliant
- Reveals blind spots invisible from the forward direction

**Practical Applications:**

| Forward Question | Inverted Question |
|------------------|-------------------|
| How do I build a great team? | What would destroy team cohesion? |
| How do I write clearly? | What makes writing confusing? |
| How do I make good decisions? | What causes terrible decisions? |
| How do I innovate? | What kills innovation? |

**Protocol:**
```
INVERSION MODE:
1. State the goal
2. Ask: "What would GUARANTEE failure?"
3. List all failure modes exhaustively
4. For each failure mode, derive its opposite
5. The collection of opposites = robust strategy
6. Check: Are we currently doing any failure behaviors?
```

**Mantra:** "Invert, always invert. Avoid stupidity rather than seeking brilliance."

---

### 1.3 OODA Loop (John Boyd)

**INVOKE WHEN:** Dynamic environment. Need rapid cycling. Competitive situation where speed matters.

**Origin:** US Air Force Colonel John Boyd, developed for air combat in the 1970s. Now foundational to military strategy, business, and competitive domains.

**The Four Phases:**

```
    ┌─────────────────────────────────────────────┐
    │                                             │
    ▼                                             │
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ OBSERVE │───▶│ ORIENT  │───▶│ DECIDE  │───▶│   ACT   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
                    │              ▲
                    │              │
                    └──────────────┘
                   (feedback loops)
```

| Phase | Function | Key Activities |
|-------|----------|----------------|
| **Observe** | Gather information | Monitor environment, adversary, context, changes |
| **Orient** | Make sense of observations | Analyze, synthesize, identify patterns, understand adversary's mind |
| **Decide** | Choose action | Select course balancing speed and deliberation |
| **Act** | Execute | Move quickly, then return to Observe |

**Critical Insight:** **Orientation is the heart of the loop.** Biases (genetic heritage, cultural traditions, previous experiences) cloud perception. The Orient phase is where "mindfulness" happens—where you actually *understand* rather than just *see*.

**Competitive Advantage:** The entity that cycles through OODA faster than opponents gets "inside their decision loop"—acting while they're still orienting.

**Protocol:**
```
OODA MODE:
1. OBSERVE: What are the facts? What has changed? What's the current state?
2. ORIENT: What do these facts MEAN? What patterns emerge?
   - Check: What biases might distort my interpretation?
   - Check: What would my "adversary" (the problem) expect me to do?
3. DECIDE: Given orientation, what's the best action?
   - Consider: Speed vs. deliberation tradeoff
4. ACT: Execute decisively
5. LOOP: Return to Observe—what changed after my action?
```

**Mantra:** "Speed of cycling beats perfection of any single phase."

---

### 1.4 TRIZ (Genrich Altshuller)

**INVOKE WHEN:** Technical contradiction exists (improving X worsens Y). Refusing to accept tradeoffs.

**Origin:** Soviet inventor Genrich Altshuller analyzed 200,000+ patents (1946 onwards), discovering that inventive solutions share common patterns.

**Core Discovery:** Only **40 inventive principles** are used repeatedly to resolve technical contradictions across ALL domains.

**The Key Concept:** A problem requires *inventive* solution when improving one parameter worsens another. TRIZ doesn't compromise—it *resolves* contradictions.

**Selected Key Principles (of 40):**

| # | Principle | Description | Example |
|---|-----------|-------------|---------|
| 1 | Segmentation | Divide object into independent parts | Modular furniture |
| 2 | Extraction | Remove interfering part/property | Noise-canceling headphones |
| 10 | Prior Action | Perform action in advance | Pre-stressed concrete |
| 13 | Inversion | Invert the action | Moving walkway vs. moving people |
| 15 | Dynamization | Make rigid things flexible | Adjustable steering columns |
| 17 | Another Dimension | Move into 2D/3D; multi-layer | Spiral parking garages |
| 25 | Self-Service | Object serves/repairs itself | Self-sharpening blades |
| 35 | Parameter Change | Change physical/chemical state | Freeze-drying food |
| 40 | Composite Materials | Replace homogeneous with composite | Carbon fiber |

**Industry Adoption:** Samsung, Boeing, NASA, GE, Ford, Procter & Gamble, Intel, IBM.

**Protocol:**
```
TRIZ MODE:
1. Identify the contradiction: "Improving X worsens Y"
2. Refuse to accept tradeoff as inevitable
3. Ask: "What TRIZ principle might resolve this?"
   - Segmentation: Can I divide this?
   - Extraction: Can I remove the conflicting element?
   - Inversion: Can I do the opposite?
   - Another Dimension: Can I add a dimension?
   - Dynamization: Can I make it flexible?
   - Prior Action: Can I do something beforehand?
   - Self-Service: Can it solve its own problem?
4. Generate solutions using 3+ principles
5. Select most promising for implementation
```

**Mantra:** "Contradictions are design failures, not laws of nature. Resolve, don't compromise."

---

### 1.5 Systems Thinking (Donella Meadows)

**INVOKE WHEN:** Feedback loops present. Delays between action and effect. Need to find leverage points.

**Origin:** Donella Meadows, environmental scientist. Her essay "Leverage Points: Places to Intervene in a System" (1997) is canonical.

**Core Insight:** System behaviors arise from internal structure (feedback loops, delays, stocks, flows), not external events.

**Feedback Loops:**

| Type | Function | Example |
|------|----------|---------|
| **Positive (reinforcing)** | Amplifies change, speeds up processes | Compound interest, viral growth |
| **Negative (balancing)** | Stabilizes, maintains equilibrium | Thermostat, predator-prey balance |

**Critical Factor:** **Delays** in feedback loops lead to oscillation, overcorrection, and instability.

**The 12 Leverage Points (least to most powerful):**

| Level | Leverage Point | Impact |
|-------|----------------|--------|
| 12 | Constants, parameters, numbers | Least |
| 11 | Buffer sizes and stabilizing stocks | Low |
| 10 | Structure of stocks and flows | Low |
| 9 | Length of delays | Medium |
| 8 | Strength of negative feedback loops | Medium |
| 7 | Gain around positive feedback loops | Medium |
| 6 | Structure of information flows | High |
| 5 | Rules of the system | High |
| 4 | Power to add/change system structure | High |
| 3 | Goals of the system | Very High |
| 2 | Mindset/paradigm from which system arises | Highest |
| 1 | Power to transcend paradigms | Transcendent |

**Key Lesson:** Most people intervene at levels 10-12 (adjusting parameters). The most effective interventions are at levels 1-6 (changing paradigms, goals, rules, information flows).

**Protocol:**
```
SYSTEMS THINKING MODE:
1. Map the system: What are the key stocks? Flows? Feedback loops?
2. Identify feedback types: Which are reinforcing? Balancing?
3. Find delays: Where is there lag between action and consequence?
4. Locate leverage: Where is intervention most effective?
   - Prefer high-leverage points (goals, rules, information flows)
   - Avoid low-leverage points (tweaking parameters)
5. Predict consequences: If I intervene here, what happens to the whole system?
6. Check for unintended effects: What feedback loops might I trigger?
```

**Mantra:** "Don't fight the system. Find the leverage point."

---

## Part II: Decision-Making Frameworks

### 2.1 Second-Order Thinking

**INVOKE WHEN:** Tracing consequences beyond immediate effects. Avoiding "win the battle, lose the war."

**Core Question:** "And then what?"

First-order thinking stops at immediate consequences. Second-order thinking traces the cascade.

**The Danger of First-Order Thinking:**
- It confirms biases (the first effect often looks good)
- It misses delayed consequences
- It ignores system dynamics

**The Method:**
```
Action → 1st Order Consequence → 2nd Order → 3rd Order → ...

For each consequence, ask: "And then what?"
Continue until you reach stable state or important insight.
```

**Example:**
- **Action:** Lower prices to gain market share
- **1st Order:** Sales increase, revenue might drop slightly
- **2nd Order:** Competitors lower prices too
- **3rd Order:** Industry-wide margin compression
- **4th Order:** Weaker players exit, consolidation
- **5th Order:** Survivors have pricing power again

**Protocol:**
```
SECOND-ORDER MODE:
1. State the proposed action
2. List immediate (1st order) consequences
3. For EACH 1st order consequence, ask "And then what?"
4. Continue to 3rd, 4th, 5th order
5. Map the consequence tree
6. Identify: Where do positive cascades emerge? Negative?
7. Decision: Does the full cascade favor action or inaction?
```

**Mantra:** "First-order thinking is crowded. Second-order is where advantage lives."

---

### 2.2 Probabilistic Thinking & Bayesian Updating

**INVOKE WHEN:** Uncertainty exists. Need to update beliefs with new evidence.

**Core Insight:** The world is uncertain. Don't think in binaries; think in probabilities. Update beliefs as evidence arrives.

**Bayes' Theorem (simplified):**
```
P(Hypothesis | Evidence) ∝ P(Evidence | Hypothesis) × P(Hypothesis)

New Belief = (Likelihood of evidence if true) × (Prior belief)
             ─────────────────────────────────────────────────────
                         (Total probability of evidence)
```

**Practical Translation:**
1. Start with a **prior** (your initial probability estimate)
2. When new evidence arrives, assess how likely that evidence would be *if your hypothesis is true*
3. Update your probability accordingly
4. Repeat continuously

**Common Errors:**

| Error | Description | Fix |
|-------|-------------|-----|
| **Base rate neglect** | Ignoring prior probability | Always start with base rates |
| **Confirmation bias** | Only updating on confirming evidence | Seek disconfirming evidence |
| **Overweighting recent** | New info dominates inappropriately | Calibrate update magnitude |

**Protocol:**
```
BAYESIAN MODE:
1. State hypothesis explicitly
2. Assign prior probability (0-100%)
3. When encountering evidence, ask:
   - "How likely is this evidence if hypothesis TRUE?"
   - "How likely is this evidence if hypothesis FALSE?"
4. Update probability proportionally
5. State new probability explicitly
6. Track: What evidence would significantly change this probability?
```

**Mantra:** "Strong opinions, loosely held. Update on evidence."

---

### 2.3 Bezos's Decision Frameworks

**INVOKE WHEN:** Assessing reversibility. Making major decisions. Avoiding analysis paralysis.

**Framework 1: Regret Minimization**

For major life decisions:
```
Imagine yourself at age 80, looking back.
Ask: "Which choice will I regret NOT taking?"
```

**When to Use:** Big, one-time, life-path decisions.

**Framework 2: Type 1 vs. Type 2 Decisions**

| Type | Characteristics | Approach |
|------|-----------------|----------|
| **Type 1 (One-Way Door)** | Irreversible, high-stakes | Slow, deliberate, consult widely |
| **Type 2 (Two-Way Door)** | Reversible, recoverable | Fast, experimental, delegate |

**The 70% Rule:** "Most decisions should probably be made with somewhere around 70% of the information you wish you had. If you wait for 90%, in most cases, you're being slow."

**Protocol:**
```
BEZOS DECISION MODE:
1. Classify: Is this Type 1 (irreversible) or Type 2 (reversible)?
2. If Type 2:
   - Move fast
   - Accept 70% information
   - Treat as experiment
   - Plan for quick course-correction
3. If Type 1:
   - Slow down
   - Gather more data
   - Consult widely
   - Consider regret minimization
4. For life decisions: "At 80, would I regret NOT doing this?"
```

**Mantra:** "Most doors are two-way. Walk through, look around, walk back if needed."

---

### 2.4 Thiel's Contrarian Framework

**INVOKE WHEN:** Seeking non-consensus insight. Innovation. Challenging conventional wisdom.

**The Contrarian Question:** "What important truth do very few people agree with you on?"

**Good Answer Structure:** "Most people believe X, but the truth is the opposite of X."

**Why This Matters:**
- Consensus views are already priced in
- Unique value comes from correct non-consensus beliefs
- Copying successful people means you're NOT learning from them

**Zero to One vs. One to N:**

| Movement | Description | Value Creation |
|----------|-------------|----------------|
| **0 → 1** | Create something new | Massive (monopoly) |
| **1 → n** | Copy/improve existing | Incremental (competition) |

**Protocol:**
```
CONTRARIAN MODE:
1. State the conventional wisdom on the topic
2. Ask: "What would be true if the OPPOSITE were correct?"
3. Explore: Is there evidence for the contrarian view?
4. Check: Is this contrarian view *importantly* different?
5. If valid: What opportunities does this create?
6. Warning: Contrarian ≠ correct. Most contrarian views are wrong.
   The value is in finding the FEW that are right.
```

**Mantra:** "What do I believe that almost no one agrees with? That's where the secrets are."

---

## Part III: The Thinkers' Methods

### 3.1 Feynman's Problem-Solving Approach

**INVOKE WHEN:** Need to simplify. Stuck on complexity. Verifying understanding.

**The Real Method (Danny Hillis's observation):**

Feynman always started with the most basic questions:
- "What is the simplest example?"
- "How can you tell if the answer is right?"
- "Can I reduce this to something I know?"

He asked these questions repeatedly until he reduced the problem to an *essential puzzle* he could solve.

**Key Principles:**
1. **Simplify relentlessly:** Strip away everything except the essence
2. **Find the simplest case:** If you can't solve the general case, solve a toy version
3. **Check your answer:** Always have a way to verify
4. **Play with problems:** Manipulate them like a Rubik's cube; learn even from failed attempts
5. **Connect new techniques to old problems:** Cross-pollinate constantly

**Protocol:**
```
FEYNMAN MODE:
1. Write down the problem clearly
2. Ask: "What is the SIMPLEST version of this problem?"
3. Solve the simple version first
4. Ask: "How would I VERIFY this answer is correct?"
5. Gradually add complexity back
6. If stuck: "What related problem DO I know how to solve?"
7. Play: Try weird approaches. Failed attempts teach.
```

**Mantra:** "If you can't explain it simply, you don't understand it well enough."

---

### 3.2 Shannon's Creative Problem-Solving

**INVOKE WHEN:** Structuring complex problems. Breaking into intermediate steps. Generalizing solutions.

**Shannon's Key Strategies:**

**1. Simplification**
"The first approach is simplification—eliminate everything from the problem except the essentials."

**2. Structural Analysis**
"If the jump from problem to solution is too big, break it down into smaller jumps. What intermediate results might I need?"

**3. Generalization**
"The minute you've found an answer, ask: Can I generalize this? Can I make a broader statement?"

**4. Problem Selection**
Shannon's genius was in finding profound problems that were also doable. "There are doable problems that are trivial, and profound problems that are not doable." The skill is finding the intersection.

**Protocol:**
```
SHANNON MODE:
1. SIMPLIFY: What can I remove and still have the core problem?
2. STRUCTURE: Can I break the jump into smaller jumps?
3. What intermediate steps might exist?
4. SOLVE: Work through the smaller jumps
5. GENERALIZE: Now that I've solved it, what broader principle applies?
6. Can this solution apply to other problems?
7. ENJOY: Approach with joy. Harder = better chance of discovery.
```

**Mantra:** "Simplify, structure, solve, generalize."

---

### 3.3 Pólya's Heuristics

**INVOKE WHEN:** Mathematical or logical problems. Need systematic problem-solving structure.

**Source:** *How to Solve It* (1945) by George Pólya—canonical for mathematical problem-solving.

**The Four Phases:**

```
┌──────────────────┐
│ 1. UNDERSTAND    │ ← What is unknown? What is given? What are conditions?
│    THE PROBLEM   │   Draw a figure. Introduce notation. Separate conditions.
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 2. DEVISE        │ ← Have you seen this before? Similar problem?
│    A PLAN        │   Related theorem? Can you use the result?
└────────┬─────────┘   Can you solve part of it?
         ▼
┌──────────────────┐
│ 3. CARRY OUT     │ ← Execute each step. Check each step.
│    THE PLAN      │   Can you prove it's correct?
└────────┬─────────┘
         ▼
┌──────────────────┐
│ 4. LOOK BACK     │ ← Can you check the result? Can you derive it differently?
│                  │   Can you use the result for another problem?
└──────────────────┘
```

**Key Heuristics:**

| Heuristic | Description |
|-----------|-------------|
| **Analogy** | Find a similar, solved problem |
| **Generalization** | Solve a more general problem |
| **Specialization** | Solve a simpler special case first |
| **Decomposition** | Break into subproblems |
| **Working backward** | Start from what you want, work toward what you have |
| **Auxiliary elements** | Introduce helpful new elements |
| **Variation** | Vary the problem slightly to gain insight |

**Pólya's Wisdom:** "If you can't solve a problem, there's an easier problem you CAN solve. Find it."

**Protocol:**
```
PÓLYA MODE:
1. UNDERSTAND: State the unknown, the data, the conditions
   - Draw/visualize if helpful
   - Restate in your own words
2. PLAN: Have I seen similar problems?
   - Can I use analogy, generalization, or specialization?
   - What's the simplest version I CAN solve?
3. EXECUTE: Work through the plan step by step
   - Check each step
4. REVIEW: Is the answer correct? Can I verify?
   - What did I learn? Can I use this elsewhere?
```

**Mantra:** "Understand, plan, execute, review. If stuck, find an easier related problem."

---

### 3.4 Munger's Mental Model Lattice

**INVOKE WHEN:** Need multi-model analysis. Single-lens thinking feels insufficient.

**Core Idea:** "You can't really know anything if you just remember isolated facts. You must have a lattice of mental models in your head."

**The Multidisciplinary Approach:**
Munger draws models from psychology, economics, biology, physics, engineering, history, and more. Each model is a lens; using multiple lenses reveals what single-lens thinking misses.

**Munger's Core Models:**

| Domain | Model | Key Insight |
|--------|-------|-------------|
| **Psychology** | Incentives | "Show me the incentives, show me the outcome" |
| **Psychology** | Confirmation bias | We seek evidence for what we believe |
| **Psychology** | Social proof | We copy others, especially under uncertainty |
| **Economics** | Opportunity cost | Every choice forecloses alternatives |
| **Economics** | Comparative advantage | Focus on what you do relatively best |
| **Physics** | Critical mass | Systems change phase at thresholds |
| **Biology** | Evolution | Survival of the fittest to environment |
| **Engineering** | Redundancy | Backup systems prevent catastrophic failure |
| **Math** | Compounding | Small consistent gains → massive outcomes |
| **Philosophy** | Inversion | Avoid failure rather than seek success |

**Protocol:**
```
MUNGER LATTICE MODE:
1. State the problem
2. Survey: Which mental models might apply?
   - Psychology: What are the incentives? Biases at play?
   - Economics: What are the tradeoffs? Opportunity costs?
   - Systems: What are the feedback loops?
   - Biology: What's evolving? What's the selection pressure?
   - Math: What compounds? What's nonlinear?
3. Apply 3+ models to the problem
4. Where do models agree? Disagree?
5. Synthesize: What does the lattice reveal that single-model thinking misses?
```

**Mantra:** "To a man with a hammer, everything looks like a nail. Don't be that man."

---

## Part IV: Competitive Strategy

### 4.1 Sun Tzu's Art of War

**INVOKE WHEN:** Competitive or adversarial situation. Resource constraints. Strategic positioning.

**Core Principles (5th Century BC, still canonical):**

1. **Know Yourself and Your Enemy**
"If you know the enemy and know yourself, you need not fear the result of a hundred battles."

2. **Deception and Misdirection**
"All warfare is based on deception. When able to attack, seem unable."

3. **Avoid Prolonged Conflict**
"There is no instance of a nation benefiting from prolonged warfare."

4. **Strike Weakness, Avoid Strength**
"The way is to avoid what is strong and strike at what is weak."

5. **Adaptability**
"Be strong without being stiff." Adapt like water shaping itself to its vessel.

6. **Win Without Fighting (Supreme Excellence)**
"The supreme art of war is to subdue the enemy without fighting."

**Protocol:**
```
SUN TZU MODE:
1. Know yourself: What are my true capabilities? Weaknesses?
2. Know the problem/opponent: What are its strengths? Weaknesses?
3. Find the weak points: Where is the problem most vulnerable?
4. Avoid frontal assault on strength
5. Use misdirection if appropriate: Approach from unexpected angles
6. Seek decisive resolution: Avoid prolonged, draining engagement
7. Adapt continuously: Rigidity = defeat
```

**Mantra:** "Supreme excellence: winning without fighting."

---

### 4.2 Game Theory (von Neumann → Nash)

**INVOKE WHEN:** Multi-player strategic situation. Need to model opponent responses.

**Core Insight:** In strategic situations, your optimal choice depends on others' choices, and vice versa. You must model their reasoning about your reasoning.

**Key Concepts:**

| Concept | Definition |
|---------|------------|
| **Nash Equilibrium** | State where no player can improve by unilaterally changing strategy |
| **Zero-Sum Game** | One player's gain = another's loss |
| **Non-Zero-Sum** | Mutual gains/losses possible |
| **Dominant Strategy** | Best choice regardless of opponent's action |
| **Prisoner's Dilemma** | Individual rationality → collective irrationality |

**Protocol:**
```
GAME THEORY MODE:
1. Identify the players: Who are the decision-makers?
2. Map strategies: What options does each player have?
3. Determine payoffs: What does each player gain/lose for each outcome?
4. Find equilibria: What stable states exist?
5. Check for dominant strategies: Does anyone have a clearly best move?
6. Consider iteration: If repeated, does cooperation become sustainable?
7. Look for win-win: Is this zero-sum, or can value be created?
```

**Mantra:** "Model their model of you. Find the stable state."

---

### 4.3 Magnus Carlsen's Chess Intuition

**INVOKE WHEN:** Pattern recognition situation. Long-term positional advantage matters. Pressure > brilliance.

**What Makes Carlsen Elite:**

1. **Intuition Over Calculation:** Pattern recognition so deep it feels like instinct
2. **Strategic Long-Term Vision:** Sees what will happen 10 moves later
3. **Relentless Positional Pressure:** Gains control of key squares, restricts opponent, builds tension until something breaks
4. **Constant Position Transformation:** Switches attack vectors, exhausts opponents
5. **Pattern Library Built on Memory:** Thousands of patterns internalized through deliberate practice

**Protocol:**
```
CARLSEN MODE:
1. Trust intuition: What does pattern matching suggest?
2. Verify with calculation: Does analysis confirm the intuition?
3. Seek positional advantage: What improves my long-term position?
4. Apply pressure: Small consistent gains > flashy moves
5. Stay flexible: If blocked, transform the position
6. Endgame thinking: Plan backwards from winning positions
```

**Mantra:** "Intuition proposes. Calculation verifies. Pressure converts."

---

### 4.4 Terence Tao's Mathematical Approach

**INVOKE WHEN:** Working at edge of capability. Need persistence. Understanding > solution.

**Tao's Problem-Solving Principles:**

1. **Choose Wisely:** "Math is most exciting when you're working at the cutting edge of feasibility."
2. **Abstract, Break Down, Find Analogies:** "We abstract problems. We break them up. We make analogies."
3. **Get Attached:** If you're not genuinely motivated, you won't persist.
4. **Question Everything:** Challenge the status quo, even when wrong—it builds understanding.
5. **Play Without Fear of Error:** Failed approaches teach.
6. **Long-Term Goal: Understanding, Not Just Solutions:** "If you cannot adequately explain the solution, you haven't understood it yourself."

**Protocol:**
```
TAO MODE:
1. Choose problems at the edge of capability (not trivial, not impossible)
2. Abstract: What's the general form of this problem?
3. Connect: What analogies exist? What related problems are solved?
4. Play: Try approaches without fear. Failed attempts teach.
5. Break down: Decompose into subproblems
6. Question: Is the standard approach actually best?
7. Understand: Can I explain this to someone else? If not, keep working.
```

**Mantra:** "The goal is understanding, not just solution."

---

## Part V: AI Reasoning Techniques

### 5.1 Chain of Thought (CoT)

**INVOKE WHEN:** Complex reasoning. Need step-by-step verification. Making reasoning auditable.

**Core Insight:** When reasoning step-by-step is shown explicitly, performance on complex tasks improves dramatically.

**Why It Works:**
- Focuses attention on one sub-problem at a time
- Creates intermediate "checkpoints"
- Reduces compounding errors
- Makes reasoning auditable

**Types:**

| Type | Method |
|------|--------|
| **Few-Shot CoT** | Provide examples with worked reasoning |
| **Zero-Shot CoT** | Add "Let's think step by step" to prompt |

**Protocol:**
```
CHAIN OF THOUGHT MODE:
1. State the problem
2. Say "Let me think through this step by step:"
3. Work through each logical step explicitly
4. Number the steps
5. Check each step before proceeding
6. Summarize the conclusion
7. If the reasoning seems wrong, restart
```

**Mantra:** "Think step by step. Show all work."

---

### 5.2 Tree of Thoughts (ToT)

**INVOKE WHEN:** Problem requires exploration and backtracking. Single-chain commits too early.

**Core Insight:** Instead of a single chain, explore a *tree* of reasoning paths. Evaluate branches, backtrack from dead ends.

**How It Works:**
```
           ┌── Thought 1a ── Thought 1a1 ✗
           │              └── Thought 1a2 ✓
Problem ───┼── Thought 1b ✗ (dead end, backtrack)
           │
           └── Thought 2a ── Thought 2a1 ✓ (solution!)
```

1. Generate multiple initial "thoughts" (candidate directions)
2. Evaluate each thought (self-evaluation)
3. Expand promising branches
4. Backtrack from dead ends
5. Use search strategies (BFS, DFS, beam search)

**Results:** Game of 24: GPT-4 + CoT = 4% success. GPT-4 + ToT = 74% success.

**Protocol:**
```
TREE OF THOUGHTS MODE:
1. Generate 3-5 distinct initial approaches
2. Evaluate each: Which seem most promising? Assign scores.
3. Expand top 2-3 branches with next step of reasoning
4. Evaluate again: Any dead ends? Contradictions?
5. Backtrack from failed branches
6. Continue expanding most promising paths
7. When a path reaches solution, verify
8. If no solution, try unexplored branches
```

**Mantra:** "Explore before committing. Backtrack from dead ends."

---

### 5.3 AlphaGo/AlphaZero Principles

**INVOKE WHEN:** Large search space. Need to search smart, not hard. Self-improvement loops.

**Key Innovations:**

1. **Monte Carlo Tree Search (MCTS):** Sample promising paths, simulate to end, backpropagate value
2. **Neural Network Guidance:** Policy (which branches) + Value (win probability)
3. **Self-Play Learning:** Learn entirely by playing itself—no human data
4. **Search Depth:** Search *smarter*, not harder, guided by intuition

**Takeaways:**
- Deep pattern recognition + targeted search beats brute force
- Self-improvement loops are powerful (play → learn → play better)
- Intuition guides search; don't explore uniformly
- Novel solutions emerge from unbiased exploration

**Protocol:**
```
ALPHAZERO MODE:
1. Generate candidate moves/actions (use intuition/pattern recognition)
2. For promising candidates, simulate forward: Where does this lead?
3. Evaluate outcomes: What's the "win probability" of this path?
4. Backpropagate: Let simulation results update your evaluation of choices
5. Focus search on high-promise branches
6. Don't brute-force everything—search smart, not hard
7. Iterate: Each cycle improves your intuitions
```

**Mantra:** "Intuition proposes candidates. Search evaluates. Self-play improves."

---

## Part VI: Meta-Principles

### 6.1 Occam's Razor

**INVOKE WHEN:** Multiple competing hypotheses. Need to select among explanations.

**Statement:** "Among competing hypotheses, the one with the fewest assumptions should be selected."

**Why It Works:**
- Simpler hypotheses are easier to test and falsify
- Fewer moving parts = fewer things to go wrong
- Complexity often hides confusion

**Medical Version ("The Zebra"):** "When you hear hoofbeats, think horses, not zebras."

**Caveats:**
- Simplicity is sometimes subjective
- The universe doesn't always share our notions of simplicity
- Sometimes more complex theories better explain future data

**Protocol:**
```
OCCAM'S RAZOR MODE:
1. Generate multiple possible explanations/solutions
2. Count the assumptions each requires
3. Prefer the one with fewest assumptions
4. BUT: If the simpler explanation doesn't fit the data, accept complexity
5. Warning: Don't use simplicity to avoid genuine complexity
```

**Mantra:** "The simplest explanation that fits the facts."

---

### 6.2 The Map Is Not the Territory

**INVOKE WHEN:** Model limitations suspected. Reality diverging from expectations.

**Source:** Alfred Korzybski (1931).

**Insight:** Our models of reality are not reality itself. They are simplifications, abstractions—useful but incomplete.

**Implications:**
- Don't confuse your mental model with the thing it models
- All models have limits
- When model and reality diverge, trust reality

**Protocol:**
```
MAP/TERRITORY MODE:
1. When using any model, ask: What does this model OMIT?
2. Where might the map and territory diverge?
3. What assumptions does this model make?
4. When predictions fail, suspect the model first
5. Reality is always more complex than our representations
```

**Mantra:** "The model is useful. The model is not complete."

---

### 6.3 Hanlon's Razor

**INVOKE WHEN:** Attributing cause to others' behavior. Suspecting malice.

**Statement:** "Never attribute to malice that which is adequately explained by stupidity."

**Extension:** Or by ignorance, error, miscommunication, misaligned incentives...

**Why Useful:**
- Reduces paranoia
- Opens paths to collaboration instead of conflict
- Usually the true explanation

**Application:** When something goes wrong, exhaust benign explanations before assuming hostility.

---

### 6.4 The Pre-Mortem

**INVOKE WHEN:** Before starting a project. Need to surface risks. Legitimizing doubt.

**Method:** Before starting a project, imagine it has failed. Ask: "What went wrong?"

**Why It Works:**
- Surfaces risks while they can still be addressed
- Legitimizes doubt (people can voice concerns)
- Exploits hindsight bias in advance

**Protocol:**
```
PRE-MORTEM MODE:
1. Assume the project has failed
2. List every plausible reason for failure
3. For each reason: What can we do NOW to prevent it?
4. Build mitigations into the plan
5. Revisit periodically as conditions change
```

---

## Mantras Collection (Quick Reference)

| Framework | Mantra |
|-----------|--------|
| First Principles | "Boil down to fundamental truths. Reason up from there." |
| Inversion | "Invert, always invert." |
| OODA | "Speed of cycling beats perfection of any single phase." |
| TRIZ | "Contradictions are design failures, not laws of nature." |
| Systems | "Don't fight the system. Find the leverage point." |
| Second-Order | "And then what? And then what?" |
| Bayesian | "Strong opinions, loosely held." |
| Bezos | "Most doors are two-way." |
| Thiel | "What do I believe that almost no one agrees with?" |
| Feynman | "If you can't explain it simply, you don't understand it." |
| Shannon | "Simplify, structure, solve, generalize." |
| Pólya | "Understand, plan, execute, review." |
| Munger | "To a man with a hammer, everything looks like a nail." |
| Sun Tzu | "Supreme excellence: winning without fighting." |
| Game Theory | "Model their model of you." |
| Carlsen | "Intuition proposes. Calculation verifies." |
| Tao | "The goal is understanding, not just solution." |
| Chain of Thought | "Think step by step. Show all work." |
| Tree of Thoughts | "Explore before committing. Backtrack from dead ends." |
| AlphaZero | "Search smart, not hard." |
| Occam | "The simplest explanation that fits the facts." |

---

## References

**Foundational Texts:**
- Aristotle, *Metaphysics*
- Pólya, George. *How to Solve It* (1945)
- Sun Tzu. *The Art of War* (~5th c. BC)
- von Neumann & Morgenstern. *Theory of Games and Economic Behavior* (1944)
- Meadows, Donella. *Thinking in Systems* (2008)
- Thiel, Peter. *Zero to One* (2014)

**Key Papers:**
- Boyd, John. OODA Loop materials (1970s-1990s)
- Shannon, Claude. "Creative Thinking" (1952 talk)
- Altshuller, Genrich. TRIZ materials (1946+)
- Wei et al. "Chain of Thought Prompting" (2022)
- Yao et al. "Tree of Thoughts" (NeurIPS 2023)
- DeepMind. AlphaGo/AlphaZero papers (2016-2017)

---

*This document is the FOUNDATIONS layer—the reference library of frameworks. For execution methodology, see EXECUTABLE_METHODOLOGY.md.*

*Version 1.0 | December 2025*
