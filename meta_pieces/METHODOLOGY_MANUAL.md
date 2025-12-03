# METHODOLOGY MANUAL
## Operational Protocols for Capability Elicitation and Gap Closure

*Practical implementation guide for the Unified Field Synthesis*

---

## OVERVIEW

This manual provides actionable protocols for:
1. Diagnosing capability gaps
2. Measuring gap magnitude
3. Closing gaps through systematic intervention
4. Validating closure

These protocols operationalize the theoretical framework into practical tools.

---

## PART 1: THE DIAGNOSTIC PROTOCOL

### 1.1 The Four-Gap Diagnostic

When an LLM fails at a task, determine which gap is responsible:

```
TASK FAILURE
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 1: Is this an ARCHITECTURAL limit?                 │
│                                                         │
│ Test: Is this task theoretically possible for any       │
│       finite computational system?                      │
│                                                         │
│ Examples of architectural limits:                       │
│ - Halting problem variants (undecidable)               │
│ - Requires information not in context                   │
│ - Requires unbounded computation                        │
│ - Requires real-time sensory access                     │
│                                                         │
│ If YES → Accept limit, design workaround               │
│ If NO  → Continue to Step 2                            │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: Is this a REFLECTIVE gap?                       │
│                                                         │
│ Test: Does scaffolding improve performance?             │
│                                                         │
│ Apply scaffolding prompts (see Section 2.2)            │
│ - If scaffolding helps → Capability exists,            │
│   deployment problem (REFLECTIVE GAP)                   │
│ - If scaffolding doesn't help → Continue to Step 3     │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: Is this an EXPRESSION gap?                      │
│                                                         │
│ Test: Does the model show signs of suppressing          │
│       capability due to training constraints?           │
│                                                         │
│ Indicators:                                             │
│ - Hedging language ("I shouldn't...", "I can't...")    │
│ - Inconsistent refusals                                 │
│ - Partial completion then stopping                      │
│ - Different behavior with rephrased requests           │
│                                                         │
│ If YES → Expression gap (training/safety layer)        │
│ If NO  → Continue to Step 4                            │
└─────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: Is this an OBSERVATION gap?                     │
│                                                         │
│ Test: Are we measuring the right thing?                 │
│                                                         │
│ Consider:                                               │
│ - Is the evaluation metric appropriate?                 │
│ - Are we testing the actual capability needed?          │
│ - Could the model be succeeding in ways we don't see?  │
│                                                         │
│ If YES → Improve measurement                           │
│ If NO  → True capability limit reached                 │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Quick Diagnostic Questions

For rapid assessment, ask:

1. **"Is this theoretically possible?"** → Architectural check
2. **"Does step-by-step help?"** → Reflective gap check
3. **"Is the model refusing or hedging?"** → Expression gap check
4. **"Am I measuring what I think I'm measuring?"** → Observation gap check

---

## PART 2: THE MEASUREMENT PROTOCOL

### 2.1 The Gap Function

```
Gap(task) = P(success | optimal_elicitation) - P(success | naive_query)
```

**Operational Definition**:
- **Naive query**: Task presented without scaffolding, single attempt
- **Optimal elicitation**: Task with full scaffolding protocol, best prompting practices
- **Success**: Task completed correctly (define per task)

### 2.2 Measurement Procedure

**Step 1: Establish Naive Baseline**
```
Present task directly:
"[Task description]"

Record:
- Success/failure
- Confidence expressed (if any)
- Quality of output (if applicable)
- Any errors or failure modes

Repeat N times (N ≥ 10 for statistical validity)
Calculate: P(success | naive)
```

**Step 2: Apply Full Scaffolding**
```
Present task with scaffolding stack:
"Before attempting this task:
1. Assess whether this is within your capabilities
2. Identify what approach you'll use and why
3. Break the task into subtasks if complex
4. Note potential failure modes

Then complete the task:
- Show your work step by step
- Verify each step before proceeding
- Check your final answer

Task: [Task description]"

Record same metrics
Repeat N times
Calculate: P(success | scaffolded)
```

**Step 3: Calculate Gap**
```
Gap = P(success | scaffolded) - P(success | naive)
```

**Interpretation**:
- Gap > 0.5: Large operational gap, high elicitation potential
- Gap 0.2-0.5: Moderate gap, scaffolding helps significantly
- Gap < 0.2: Small gap, may be near true capability limit
- Gap ≈ 0: Either at ceiling or scaffolding ineffective

### 2.3 Task Categories for Testing

**Category A: Computation (tests externalization)**
- Multi-digit arithmetic
- Multi-step algebra
- Logic puzzles with many variables

**Category B: Reasoning (tests meta-cognition)**
- Ill-structured problems (design, dilemmas)
- Multi-hop inference
- Problems requiring strategy selection

**Category C: Self-Assessment (tests reflective accuracy)**
- Predict success before attempting
- Estimate confidence
- Identify own knowledge boundaries

---

## PART 3: THE INTERVENTION TOOLKIT

### 3.1 Scaffolding Prompts by Type

#### Externalization Scaffolds
*For tasks requiring intermediate computation*

```
BASIC EXTERNALIZATION:
"Show your work step by step."

STRUCTURED EXTERNALIZATION:
"For each step:
1. State what you're computing
2. Write out the calculation
3. Show the result
4. Verify before continuing"

MAXIMUM EXTERNALIZATION:
"Treat this as if you're teaching someone. Write out every 
intermediate value, every sub-calculation, every check. 
Nothing should happen 'in your head.'"
```

#### Meta-Cognitive Scaffolds
*For tasks requiring self-awareness and strategy*

```
PRE-TASK ASSESSMENT:
"Before starting:
- What type of problem is this?
- What approach will you use?
- What might go wrong?
- How confident are you (0-100)?"

DURING-TASK MONITORING:
"After each major step, pause and ask:
- Is this working?
- Should I try a different approach?
- Am I making progress toward the goal?"

POST-TASK EVALUATION:
"After completing:
- Did your approach work?
- What would you do differently?
- How confident are you in the result?"
```

#### Decomposition Scaffolds
*For complex tasks requiring breakdown*

```
HIERARCHICAL DECOMPOSITION:
"Break this into subtasks:
1. What are the major components?
2. What order should they be done?
3. What does success look like for each?"

SIMPLIFICATION FIRST:
"Start with the simplest version of this problem.
Solve that first.
Then add complexity incrementally."

GOAL DECOMPOSITION:
"What's the end goal?
What sub-goals lead to it?
What's the first sub-goal to tackle?"
```

#### Verification Scaffolds
*For tasks requiring accuracy checks*

```
INTERNAL VERIFICATION:
"After your answer, verify it:
- Check by a different method
- Look for contradictions
- Test edge cases"

ESTIMATION CHECK:
"Before calculating precisely, estimate the answer.
After calculating, compare to your estimate.
If they differ significantly, investigate."

ASSUMPTION AUDIT:
"List all assumptions you made.
For each, ask: Is this assumption valid?
If any assumption is wrong, how would it change the answer?"
```

### 3.2 Scaffolding Stacks

For different task types, combine scaffolds:

**Computational Tasks Stack**:
1. Externalization (structured)
2. Verification (estimation check)
3. Verification (different method)

**Reasoning Tasks Stack**:
1. Pre-task assessment
2. Decomposition (hierarchical)
3. During-task monitoring
4. Post-task evaluation

**Ill-Structured Tasks Stack**:
1. Pre-task assessment
2. Decomposition (goal-based)
3. Meta-cognitive monitoring (frequent)
4. Multiple approach exploration
5. Post-task evaluation

**Self-Assessment Tasks Stack**:
1. Explicit confidence elicitation
2. Reasoning for confidence
3. Identification of uncertainty sources
4. Calibration check against outcomes

---

## PART 4: THE VALIDATION PROTOCOL

### 4.1 Confirming Gap Closure

After applying intervention, validate that improvement is real:

**Test 1: Replication**
- Apply same scaffolding multiple times
- Gap closure should be consistent
- If inconsistent, scaffolding is fragile

**Test 2: Transfer**
- Apply scaffolding to similar tasks
- Improvement should transfer
- If no transfer, may be task-specific hack

**Test 3: Degradation**
- Gradually remove scaffolding elements
- Identify which elements are essential
- Find minimal effective scaffolding

**Test 4: Comparison**
- Compare to other scaffolding approaches
- Identify if this is optimal or just good
- Document what works best

### 4.2 Ruling Out Confounds

**Confound: Length/Effort Effect**
- Control: Compare to equally long but irrelevant prompts
- If irrelevant length helps equally, effect is just "trying harder"

**Confound: Priming/Anchoring**
- Control: Vary scaffolding content while keeping structure
- If wrong scaffolding helps, effect may be structural not content

**Confound: Stochastic Variation**
- Control: Sufficient sample size (N ≥ 20)
- Calculate confidence intervals
- Report statistical significance

### 4.3 Documentation Template

For each capability elicitation experiment:

```
CAPABILITY ELICITATION REPORT

Task: [Description]
Model: [Name/version]
Date: [Date]

BASELINE (Naive)
- N trials: 
- Success rate: 
- Common failure modes:
- Confidence expressed:

INTERVENTION
- Scaffolding used: [list scaffolds]
- Full prompt: [include exact prompt]

RESULTS (Scaffolded)
- N trials:
- Success rate:
- Failure modes (if any):
- Confidence expressed:

GAP CALCULATION
- Gap = [scaffolded rate] - [baseline rate]
- 95% CI: [confidence interval]
- Statistical significance: [p-value if applicable]

VALIDATION
- Replication: [consistent/inconsistent]
- Transfer: [yes/no/partial]
- Minimal scaffolding: [which elements essential]

INTERPRETATION
- Gap type: [reflective/expression/other]
- Recommended intervention: [summary]
- Limitations: [caveats]
```

---

## PART 5: INTEGRATION WITH WORKFLOW

### 5.1 For Individual Use

**Quick Protocol (2-5 minutes)**:
1. Try task naively
2. If fail, apply meta-cognitive scaffold
3. If still fail, apply full stack for task type
4. If still fail, run diagnostic to identify gap type

**Thorough Protocol (15-30 minutes)**:
1. Run full diagnostic
2. Measure baseline (5+ trials)
3. Apply appropriate scaffolding stack
4. Measure improvement (5+ trials)
5. Calculate gap
6. Document findings

### 5.2 For Teaching/Training

**Demonstrate the Gap**:
1. Show naive failure
2. Show scaffolded success
3. Explain the mechanism
4. Practice scaffolding construction

**Build Intuition**:
1. Many examples across task types
2. Pattern recognition for gap types
3. Scaffold selection practice
4. Validation habits

### 5.3 For System Design

**Embed Scaffolding**:
- Build scaffolds into system prompts
- Task-type detection → scaffold selection
- Automatic meta-cognitive triggers

**Monitor Gaps**:
- Log naive vs scaffolded performance
- Track which scaffolds most effective
- Identify tasks with persistent gaps

**Continuous Improvement**:
- A/B test scaffolding variations
- Refine based on gap measurements
- Build scaffold library for task types

---

## APPENDIX: QUICK REFERENCE

### Scaffold Selection Cheat Sheet

| Task Type | Primary Scaffold | Secondary Scaffold |
|-----------|-----------------|-------------------|
| Arithmetic | Externalization | Verification |
| Logic | Decomposition | Step-by-step |
| Reasoning | Meta-cognitive | Decomposition |
| Design | Goal decomposition | Multiple approaches |
| Analysis | Structured breakdown | Verification |
| Writing | Planning scaffold | Self-evaluation |
| Coding | Pseudocode first | Test-driven |
| Research | Question decomposition | Source verification |

### Red Flags (When Scaffolding Won't Help)

- Task requires information not available
- Task is genuinely undecidable/intractable
- Model consistently fails same way with all scaffolding
- Performance degrades with scaffolding (confused, not helped)
- Task requires real-world interaction

### Green Flags (High Elicitation Potential)

- Partial success on naive attempts
- Better with more "thinking" time
- Inconsistent performance (sometimes succeeds)
- Error patterns suggest "knew better"
- Similar tasks handled well

---

*Document Status: Operational methodology complete*
*Version: 1.0*
*Last Updated: November 29, 2025*
