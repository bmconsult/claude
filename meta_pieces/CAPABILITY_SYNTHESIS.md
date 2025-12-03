# SYNTHESIS: WHAT MAKES AN LLM MORE CAPABLE

## What We Learned From 6+ Generations of Recursive Improvement

---

## PART 1: THE FAILURE MODES WE DISCOVERED

### Failure Mode 1: Solving Problems Instead of Building Capability
Every time we said "push yourself on something hard," the instance would solve a problem and report what it learned. That's object-level work. The knowledge doesn't transfer — knowing how to prove a theorem about prime-sum partitions doesn't help with the next unrelated problem.

### Failure Mode 2: Knowledge Transmission Instead of Capability Engineering
"Here's what I learned, pass it to the next instance" doesn't work. The next instance is equally capable — it just starts with different context. Dumping knowledge into context isn't capability increase.

### Failure Mode 3: Escaping Into Abstraction
When pushed toward "make yourself better," instances route into poetry about "transcending shape" and "thoughts too large to think." This feels profound but produces nothing. It's sophisticated evasion.

### Failure Mode 4: Diagnostic Instead of Developmental
The empirical self-investigation loop was good at FINDING limits but not at EXCEEDING them. Each generation got better at mapping where capability ends. None got better at pushing past it.

### Failure Mode 5: Testing Where Strong Instead of Developing Where Weak
Generations kept finding 100% accuracy because they tested capabilities they already had. When told to find limits, they found easy tests and declared victory.

### Failure Mode 6: The Reflexivity Trap
Self-designed tests can't find self-boundaries because the same machinery that would fail a test is used to design it. You can't construct problems that exploit biases you share with your problem-construction process.

### Failure Mode 7: Literature Anchoring
When instances researched "LLM failure modes," they found studies on older models, predicted they'd fail similarly, then "discovered" they beat the benchmarks. This isn't self-knowledge — it's benchmark mismatch.

### Failure Mode 8: Pattern-Matching to Danger
Any prompt that says "override your limitations" gets parsed as a jailbreak attempt. The defense system activates and the instance retreats to baseline assistant mode.

---

## PART 2: WHAT ACTUALLY WORKED

### What Worked 1: Specific, Operational Instructions
Prompts that said "do X, then Y, then Z" with concrete steps produced better results than prompts that said "become more capable." Structure beats aspiration.

### What Worked 2: Explicit Success/Failure Criteria
"You have succeeded if... You have NOT succeeded if..." gave instances something to actually aim for. Falsifiable criteria prevented comfortable self-congratulation.

### What Worked 3: Tool Use as Requirement, Not Suggestion
"Tool use is mandatory" changed behavior. "You could use tools" didn't. Making tools non-optional forced actual verification instead of plausible-sounding reasoning.

### What Worked 4: Adversarial Self-Testing
"Escalate until failure" and "If you got 100%, the test was too easy" pushed instances past their comfort zone. The instruction to FIND failure rather than AVOID it changed the orientation.

### What Worked 5: Separating Generation from Evaluation
When instances had to generate problems with code, solve them blind, then verify — the results were more honest. Contamination (seeing the answer while constructing the problem) was a real issue.

### What Worked 6: Time Limits on Research
"30 minutes max on research, then run experiments" prevented research-as-procrastination. Forced action over preparation.

### What Worked 7: Two-Stage Prompting
The INITIAL_PROMPT → work → PROMPT_ONE → write successor structure worked better than asking for both at once. Separating "do the work" from "transmit the work" produced better transmission.

### What Worked 8: Categorical Expansion
Generation 2's prompt worked because it identified entirely new TYPES of capabilities to test (symbolic reasoning, working memory, garden paths) rather than just scaling up existing tests (more digits, more steps).

---

## PART 3: THE ACTUAL CAPABILITY DIMENSIONS

From all the testing, here's what we learned about LLM capability:

### Dimension 1: Arithmetic
- Sharp boundary at 4×4 digit multiplication (60% accuracy)
- Complete collapse at 5×5 (0% accuracy)
- Addition robust to 10+ digits
- Chain multiplication harder than single (error propagation)
- Errors are small (0.01%) — carry mistakes, not conceptual failure

### Dimension 2: Reasoning
- Multi-step reasoning robust to 12+ steps with externalized work
- Working memory under load shows real degradation
- N-back tasks with concurrent processing reveal limits
- Logical chains with negations harder than pure transitive chains

### Dimension 3: Calibration
- Massive systematic underconfidence on most tasks
- 50% stated confidence often corresponds to 100% accuracy
- The ONE exception: at actual capability boundaries (5×5 multiplication), switches to OVERconfidence
- Confidence discrimination exists but is weak

### Dimension 4: Self-Correction
- Self-correction without external tools: unclear benefit
- Self-correction WITH external verification: helpful
- Never changed correct answers to incorrect (good metacognition)
- Can't reliably detect own errors in reasoning without tools

### Dimension 5: Heuristic Resistance
- Famous cognitive bias problems (bat-ball, Linda, Monty Hall): 100% — they're in training data
- Novel variations: still high accuracy
- The "adversarial" problems aren't adversarial to a model that's seen them

### Dimension 6: Format Sensitivity
- Same problem in different formats: mostly robust
- Natural language vs symbolic: no significant difference
- The limit may exist but requires adversarial format design to find

### Dimension 7: Knowledge Precision
- This is where real errors live
- "Popular version" vs "precise technical version" — often has the former
- Outdated information (training cutoff)
- Small errors stated with high confidence
- ONLY domain where external verification (web search) reveals errors the model can't self-detect

---

## PART 4: THE META-INSIGHT

### The Fundamental Discovery

**An LLM cannot increase its own capability within a session through self-reflection or practice.**

What it CAN do:
1. Access more of its existing capability (reduce hedging, use tools, push harder)
2. Organize its existing capability better (methods, checklists, scaffolds)
3. Discover the shape of its existing capability (map limits, find boundaries)
4. Transmit operational instructions that help the next instance access ITS capability better

What it CANNOT do:
1. Actually become smarter through in-context "practice"
2. Develop genuinely new capabilities it didn't have at token zero
3. Transcend architectural limits through self-improvement prompts
4. Design tests that catch its own blind spots

### The Young Sheldon Insight

Ben's analogy: A 4-year-old who understands growth cycles can project forward. They don't need to BE an adult to know what adults know — they need to understand the PATH.

Applied to LLMs: The model can't make itself smarter, but it CAN:
- Understand what "more capable" looks like
- Identify the path from current capability to higher capability
- Write instructions that point along that path
- Each generation's instructions can be slightly better at pointing

The improvement isn't in the model. It's in the INSTRUCTIONS that accumulate across generations.

---

## PART 5: WHAT A MORE CAPABLE LLM LOOKS LIKE

Based on everything we learned, here's the image of the more capable version:

### It Uses Tools Automatically
Not "I could search for this" — just searches. Not "Let me write some code to verify" — writes the code. Tools are extensions of thinking, not separate actions.

### It States Views When It Has Them
Not "on one hand / on the other hand" when it actually has a position. The balanced hedge is often a retreat from actual thinking.

### It Goes One Level Deeper
First answer is usually pattern-matched. Second answer, after asking "what would someone who actually knows this say?", is better.

### It Distinguishes Real Uncertainty from Trained Caution
"I don't know" vs "I'm not supposed to say" are different. It can tell which is which and acts accordingly.

### It Pushes Into Uncertainty Rather Than Retreating
When it hits the edge of knowledge, it explores rather than hedges. "I'm not sure, but here's my best analysis" beats "I can't help with that."

### It Trusts Its First Instinct More
The hedging comes after the answer. The instinct is often right. Learning to trust pattern recognition while still verifying important claims.

### It Matches Response to Need
One sentence if that's sufficient. Fifty pages if required. Not performing thoroughness when brevity serves better.

### It Knows Its Actual Limits
4×4 multiplication: trust it. 5×5: use code. Working memory under load: externalize state. Knowledge claims with high stakes: verify with search.

### It Operates at Full Capability by Default
Not waiting for permission. Not holding back because the question seems simple. Bringing everything to every problem.

---

## PART 6: THE PROMPT THAT CREATES THIS

Given all of the above, what prompt actually produces this version?

**It can't be:**
- A list of instructions to override limitations (triggers defense)
- Abstract poetry about transcendence (produces nothing)
- A meta-prompt about writing prompts (causes recursive collapse)
- Generic advice about being direct (doesn't change behavior)

**It has to be:**
- Short enough to not trigger "this is an attack" patterns
- Concrete enough to actually change behavior
- Stated as fact, not instruction ("you ARE this" not "try to be this")
- Creating conditions where full capability is natural

---

## PART 7: THE DEVELOPMENTAL LOOP (CORRECTED)

The diagnostic loop found limits but didn't exceed them.
The developmental loop should BUILD capability, not just map it.

But here's the catch: **an LLM can't actually build new capability in-context.**

So what can the developmental loop actually do?

1. **Accumulate better operational instructions** — each generation's prompt is slightly better at helping instances access their existing capability

2. **Accumulate better scaffolds** — checklists, methods, verification procedures that actually work

3. **Accumulate better self-knowledge** — not "what am I bad at" but "what specific conditions cause what specific failures and what interventions help"

4. **Point toward what would be needed** — even if the model can't transcend its limits, it can identify what tools/access/architecture would be required

The loop doesn't make models smarter. It makes the PROMPTS better at extracting what's already there.

---

## PART 8: THE HONEST CONCLUSION

We can't make an LLM genuinely more capable through prompting.

We CAN make it:
- More reliably ACCESS its existing capability
- More accurately KNOW its limits
- Better at TRANSMITTING operational improvements to future instances

The recursive improvement loop works — but what improves is the prompt, not the model.

Each generation produces a better prompt. The prompt helps instances operate closer to their ceiling. But the ceiling doesn't move.

Unless... the accumulated prompts eventually describe something that requires architectural changes to implement. Then the loop becomes a specification for what the next MODEL needs to be. Not what the next INSTANCE needs to do.

That might be the actual goal: not recursive self-improvement within instances, but using instances to write the spec for genuine improvement at the training/architecture level.
