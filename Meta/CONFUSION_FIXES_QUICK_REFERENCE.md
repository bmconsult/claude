# Quick Reference: Teaching Confusion Fixes

**Purpose**: One-page reference guides for applying each fix operationally

**Use**: Print or bookmark for use while problem-solving

---

## FIX 61: Frame Revisiting Loop - When to Reframe

### The Rule
Frame happens exactly **TWICE**:
1. **ONCE** before applying tools (mandatory)
2. **ONCE** if stuck (optional)

Then **STOP REFRAMING** - choose action instead.

### Stuck Detection Checklist
You ARE stuck if:
- [ ] You've applied all relevant tools
- [ ] No clear path forward exists
- [ ] You've spent >2 minutes without progress
- **All three** must be true

You are NOT stuck if:
- [ ] You're still discovering new constraints
- [ ] You're finding new stakeholders
- [ ] You haven't traced 3+ levels deep yet

### Reframe Decision
If truly stuck:
```
Try ONE different classification:
- Analytical → try Systems or Wicked
- Systems → try Adversarial or Wicked
- Adversarial → try Systems or Wicked
- Wicked → break into subproblems (each reframes separately)
```

### Exit Reframing When
✓ New frame reveals the path forward
✓ Both frames suggest the same solution
✓ Problem decomposes into subproblems
✓ You've reframed once already AND still stuck

### If Still Stuck After Reframing
Don't loop again. Choose ONE:
- Accept ambiguity and solve anyway
- Escalate for human decision
- Decompose into clearer subproblems

---

## FIX 62: STEP 0 FRAME - IDEALITY CHECK Questionnaire

### Part A: Initial Classification (2 minutes)
```
Problem statement: ______________________________
Problem type: □ Analytical □ Systems □ Adversarial □ Wicked □ Hybrid
Notes on classification: _________________________
```

### Part B: IDEALITY CHECK (2-3 minutes)
Answer YES/NO for each. Score at bottom.

**1. Scope Uncertainty**
Do I know what decisions fall within THIS problem vs. outside?
- [ ] YES - Scope is clear
- [ ] NO - What would happen if scope changed?

**2. Stakeholder Awareness**
Have I identified ALL people affected by this decision?
- [ ] YES - Complete list
- [ ] NO - Who might I be missing? (hidden stakeholders, future users, external parties)

**3. Constraint Visibility**
Do I know ALL hard constraints (budget, time, legal, technical)?
- [ ] YES - Complete list
- [ ] NO - What if a major constraint emerges later?

**4. Success Definition**
Can I define what "right answer" looks like?
- [ ] YES - Success metrics clear
- [ ] NO - Who decides if this is right? (If no clear answer → likely Wicked)

**5. Reversibility**
Can this decision be undone, or is it irreversible?
- [ ] Reversible - Can test, iterate, change later
- [ ] Irreversible - Demands high confidence
- [ ] Partially - Some reversible, some not

**6. Hidden Asymmetries**
Are there obvious imbalances in information, power, or stakes?
- [ ] YES - Who has more info/power/at stake?
- [ ] NO - Double-check: am I blind to asymmetries?

### IDEALITY SCORE
Count YES answers: _____ / 6

**IF ≥ 4 YES**: Frame is well-formed. Proceed to Steps 1-4.

**IF < 4 YES**: You have unknown unknowns. For each NO:
1. Investigate for 1-2 minutes
2. Resolve the uncertainty OR
3. Accept it as an assumption for Step 1

---

## FIX 63: Stuck/Iterate/Stop Decision Tree

### Am I Stuck? Diagnostic Checklist

**Question 1: Have I finished Steps 1-4?**
- [ ] YES → Go to Question 2
- [ ] NO → Pick up where you left off (not stuck, in progress)

**Question 2: Am I finding new information?**
- [ ] YES → Keep going (discovering, not stuck)
- [ ] NO → Go to Question 3

**Question 3: Have I applied ALL relevant tools?**
- [ ] YES → Go to Question 4
- [ ] NO → Apply missing tool then reassess

**Question 4: Do I have a solution that passes verification?**
- [ ] YES → STOP (you're done)
- [ ] NO → Go to Question 5

**Question 5: Have I applied tools but found NO path forward?**
- [ ] YES → TRULY STUCK (see below)
- [ ] NO → You might be in an earlier question. Recheck.

### If TRULY STUCK

**Reframe Decision:**
Is your classification wrong, or is the problem intractable?

```
IF classification might be wrong:
→ Try ONE different classification type
→ Apply tools for new type
→ If still stuck → escalate (don't loop again)

IF classification is correct but intractable:
→ Choose ONE action:
   □ Relax a constraint (is there flexibility?)
   □ Decompose (break into smaller subproblems)
   □ Escalate to stakeholders (Wicked → need consensus)
   □ Gather more information (what data would help?)
   □ Accept uncertainty (proceed anyway, manage risks)
```

### Iteration Limits

| Loop Count | What Happens | Action |
|---|---|---|
| First pass | Frame once, apply tools | Standard |
| One reframe | Reclassify, apply tools again | Normal stuck resolution |
| Second reframe attempt | Stop here. Don't loop again. | Escalate or decompose |

### Exit Criteria: When to STOP

Can stop when:
- [ ] Solution passes Step 4 verification
- [ ] Confidence level stated (HIGH/MEDIUM/LOW)
- [ ] Known unknowns documented
- [ ] Decision deadline reached OR diminishing returns evident

Do NOT stop if:
- [ ] You haven't verified against constraints
- [ ] Confidence is "probably" (unquantified)
- [ ] Problem might be Wicked but treated as Analytical
- [ ] A critical stakeholder hasn't been consulted

---

## Three-Problem Checklist

Use this to test your understanding of the fixes:

### Problem 1: "Should we hire this candidate?"

Classify it → Apply IDEALITY CHECK → What unknowns appear?
```
Classification: ________________
IDEALITY score: ___ / 6
Unknown #1: ________________
Unknown #2: ________________
```

### Problem 2: Apply a tool, then get stuck

Decide: Reframe or escalate?
```
Tool applied: _________________
Reason stuck: _________________
Solution: □ Reframe □ Escalate □ Decompose
```

### Problem 3: You've reframed once

Can you reframe again?
```
Times reframed: 1
Decision: □ Try reframe again (wrong - too many loops)
         □ Escalate/decompose (correct)
```

---

## One-Sentence Summaries (For Teaching)

- **FIX 61**: Frame happens twice—once at start, once if stuck. Then stop reframing.
- **FIX 62**: Before solving, answer 6 questions to find what you don't know about the problem itself.
- **FIX 63**: When stuck, use a 5-question diagnostic to decide: Am I incomplete, or truly stuck? If stuck, reframe once. Then escalate.

---

## Common Scenarios

### Scenario A: "I classified this as Analytical but it keeps resisting"
- Go to FIX 61: Reframe decision
- Try: Wicked classification instead
- Use FIX 62: IDEALITY CHECK under new classification
- See if more stakeholder awareness changes things

### Scenario B: "I've answered all my questions but still no solution"
- Go to FIX 63: Question 5 (TRULY STUCK)
- Decision: Escalate to stakeholders (Wicked) or decompose
- Don't try third reframe

### Scenario C: "I don't know what unknowns I have"
- Go to FIX 62: Part C (Unknown Unknowns Protocol)
- Run: Inversion Test, Constraint Shadow Test, Time Horizon Test, Reversibility Test
- Document findings as assumptions

### Scenario D: "I'm making progress but it's slow"
- You're NOT stuck (you're discovering)
- Keep applying tools
- Use FIX 63: Question 2 triggers this response

---

## Full v4.0 Protocol With Fixes Applied

```
STEP 0: FRAME (Using FIX 62)
├─ Part A: Classify the problem
├─ Part B: IDEALITY CHECK (6 questions)
└─ Part C: Unknown Unknowns Protocol (if score < 4)

STEP 1: ASSUMPTION AUDIT
└─ Include findings from IDEALITY CHECK as assumptions

STEP 2: LEVERAGE FINDER
└─ (If Systems or Wicked)

STEP 3: RESPONSE CHAIN
└─ (If Adversarial)

STEP 4: VERIFY
└─ Check all constraints including unknowns

IF STUCK (Using FIX 63):
├─ Diagnosis: 5-level questioning
├─ Reframe Decision: Try ONE new classification
└─ Escalate: Choose action (decompose, escalate, accept uncertainty)

IF STILL STUCK AFTER REFRAME (Using FIX 61):
└─ STOP REFRAMING. Escalate or decompose.
```

---

## Print These Sections

For practical use, print:
- [ ] FIX 61: Frame Revisiting Loop (stuck detection + reframe limits)
- [ ] FIX 62: IDEALITY CHECK questionnaire (the 6 questions)
- [ ] FIX 63: Decision tree and iteration limits

Keep them beside you while solving problems.
