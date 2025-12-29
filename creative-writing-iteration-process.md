# Creative Writing Iteration Process

A methodology for producing alive writing through structured iteration, subagent evaluation, and honest feedback loops.

---

## THE CORE LOOP

```
WRITE → EVALUATE → IDENTIFY WEAKNESS → FIX ONE THING → EVALUATE AGAIN
```

Each cycle should change exactly one variable. This isolates what's working from what isn't.

---

## SUBAGENT EVALUATION PROMPTS

### Standard Evaluation Prompt

```
BEFORE YOU DO ANYTHING:
1. Read /home/user/claude/.claude/CLAUDE.md completely
2. Internalize it

Then read /home/user/claude/fair-rigorous-writing-evaluation-v2.md - this is our evaluation framework.

You are scoring this [GENRE]. Apply the framework HARSHLY. 5 is average. 7 is good. 9 is exceptional. 10 breaks you.

THE PIECE:

[INSERT PIECE]

---

EVALUATE:
1. Is it ALIVE? Does it have that thing?
2. Check against the 13 Critical Truths
3. Score 1-10
4. What specific line or moment makes it work or fail?
5. If under 10: what ONE thing would fix it?
```

**Key elements:**
- Always include CLAUDE.md instruction (adds ~20% useful signal: self-assessment, gap acknowledgment)
- Reference the v2 framework explicitly
- Demand harshness (prevents grade inflation)
- Ask for ONE fix (prevents overwhelm, enables isolation)

### A/B Comparison Prompt (Blind)

```
BEFORE YOU DO ANYTHING:
1. Read /home/user/claude/.claude/CLAUDE.md completely
2. Internalize it

Then read /home/user/claude/fair-rigorous-writing-evaluation-v2.md - this is our evaluation framework.

You are comparing two [GENRE] pieces. They are very similar. Read both carefully, score each, then pick which is better.

---

**VERSION A:**

[INSERT VERSION A]

---

**VERSION B:**

[INSERT VERSION B]

---

EVALUATE:
1. Score Version A (1-10)
2. Score Version B (1-10)
3. What differences do you notice between them?
4. Which is better and why?
```

**Critical:** Do NOT highlight the change or explain what differs. Let the evaluator find it. Leading the witness biases results.

### Direct Comparison Prompt (When You Need Specific Guidance)

Use this ONLY after blind testing, when you need to understand WHY one version might be better:

```
You are comparing TWO versions of the same line. Everything else is identical. Only this differs:

**VERSION A:**
"[line A]"

**VERSION B:**
"[line B]"

Context: [relevant context about rhyme scheme, meter, etc.]

EVALUATE:
1. Read both out loud
2. Which lands better sonically?
3. Which lands better semantically?
4. PICK ONE. Which is better and why?

Be decisive. Don't hedge.
```

**Warning:** This prompt leads the witness. Use blind testing first, then this for understanding.

---

## HANDLING FEEDBACK

### The Perception Problem

You will misread feedback. The answer is often IN what the evaluator said, but you'll perceive it wrong.

**Common misreadings:**
- Evaluator says "this line is filler" → You add more instead of cutting
- Evaluator says "too clever" → You make it MORE clever instead of simpler
- Evaluator says "explaining instead of doing" → You explain WHY you're doing instead of just doing

**The fix:** After receiving feedback, ask yourself: "What is the LITERAL instruction here?" Not what you want it to mean. What it actually says.

### The Subtraction Principle

When feedback identifies a weakness, try CUTTING before FIXING.

| Feedback | Instinct | Better Move |
|----------|----------|-------------|
| "Ending doesn't land" | Rewrite ending | Cut last line, see if it lands now |
| "This line is weak" | Replace with stronger line | Delete it entirely |
| "Too much explaining" | Explain more concisely | Stop explaining |

Often the answer is removal, not revision.

### The One-Thing Rule

Fix ONE thing per iteration. Not two. Not "a few small things." One.

**Why:**
- Isolates variables (you know what worked)
- Prevents overcorrection
- Builds understanding incrementally

If the evaluator lists five problems, pick the one they emphasize most. Fix that. Re-evaluate. Then the next.

---

## ENSURING GROWTH WITH EACH CYCLE

### Track What You Learn

After each evaluation cycle, note:
1. What the evaluator caught that you missed
2. What principle from the framework applied
3. Whether your instinct matched reality

### Pattern Recognition

After 5-10 cycles, patterns emerge:

| If you keep hearing... | The underlying issue is... |
|------------------------|---------------------------|
| "Too clever" | Showing off, not serving |
| "Doesn't land" | Explaining instead of doing |
| "Filler" | Not trusting the reader |
| "Breaks the spell" | Meta-commentary, self-consciousness |
| "Random" without payoff | Breaking rules without earning it |

### The Comparison Trap

Different evaluators have different calibration. Never compare scores across evaluators.

**Valid:** Same evaluator, Version A = 8, Version B = 9 → B is better
**Invalid:** Evaluator 1 gives 10, Evaluator 2 gives 9 → can't conclude anything

For true comparison, use the same evaluator for both versions in the same prompt.

---

## HOW TO WRITE WELL (Lessons Learned)

### The Core Discovery

You will approximate what good writing sounds like. This produces consistent 5-6/10 work. The gap between approximation and creation is the gap between competence and aliveness.

### Do, Don't Explain

| Dead | Alive |
|------|-------|
| "The thing about the thing is..." | Just do the thing |
| "What I'm trying to say is..." | Say it |
| "This represents..." | Let it represent without announcing |

If you can see the construction, the trying, the "look at this" — it's dead.

### Constraint Forces Creation

The tightest constraint produces the best work.

- "3 words max per line" → forced economy → every word matters → magic
- "No adjectives" → forces concrete nouns and strong verbs
- Self-imposed rules create pressure that produces diamonds

### Fresh Palette, Fresh Language

Default images are death:
- Shadows, rainbows, monsters under beds
- Love, loss, fear of the dark
- Hearts, souls, journeys

Fresh territory:
- The almost-asleep place
- What silence looks like
- The space between words
- Smelling like a number

If anyone could have written it, you haven't written anything yet.

### Voice = Present, Not Reflecting

| Adult reflecting (dead) | Child experiencing (alive) |
|------------------------|---------------------------|
| "the ones too heavy to carry, too scary to say out loud" | "She never knows." |
| "I remember when I used to..." | "So I climbed." |
| Therapy language | Immediate, concrete, present-tense |

### Sound Is Meaning

In poetry, rap, children's verse — sonic craft isn't separate from aliveness. It IS the aliveness.

- A broken rhyme scheme isn't "raw" — it's a wound
- Breaking rules requires payoff
- No payoff = not bold, just broken

### Joy vs. Ego

| Joy (alive) | Ego (dead) |
|-------------|-----------|
| Lost in the fun | Waiting for applause |
| Play for its own sake | "Look how clever I am" |
| Un-self-conscious | Checking if you noticed |

Real play doesn't check. Showing off always checks.

### The Specificity Principle

Specific > vague, always.

| Vague | Specific |
|-------|----------|
| "smells like a number (I think it's a lot)" | "smells like a number (I'm guessing it's odd)" |
| "a color" | "that particular green" |
| "somewhere" | "the place where I keep all the things I can't find" |

Specificity creates reality. Vagueness creates nothing.

---

## COMMON FAILURE MODES

### Explaining Instead of Doing
You describe what the piece is doing instead of just doing it. The evaluator will score 4-6/10 and say "too meta" or "self-conscious."

**Fix:** Delete all explanation. Trust the reader.

### Variation Instead of Pivot
You try the same approach 3 times with slight variations. All fail at the same break point.

**Fix:** If 3 variations fail the same way, you need a DIFFERENT approach, not a better variation.

### Adding When You Should Cut
Feedback says something's wrong, you add more to fix it.

**Fix:** Try cutting first. The answer is often subtraction.

### Leading the Evaluator
You highlight what changed, explain why, set up the "right" answer.

**Fix:** Blind testing. Just show both versions. Let them find the difference.

### Romanticizing Broken Craft
You mistake rule-breaking for authenticity. "It's raw!" No, it's just broken.

**Fix:** Breaking rules requires payoff. What are you GAINING by breaking this rule? If nothing, follow the rule.

---

## THE ITERATION MINDSET

### Scores Are Signals, Not Grades

A 6/10 isn't failure — it's information. It tells you where the life isn't yet.

### The Ceiling Is Higher Than You Think

You will settle at 7-8/10 and think that's the limit. It's not. Push until 10. Then push past 10.

### Trust the Process

Write → evaluate → fix one thing → repeat.

The loop works. The temptation is to skip steps, fix multiple things, or stop early. Don't.

### Protect What's Alive

Every revision risks killing something that works. The evaluator should always identify "where the life IS" — protect those elements through revision.

---

## CHECKLIST BEFORE SUBMITTING FOR EVALUATION

- [ ] Is this doing or explaining?
- [ ] Is the palette fresh or default?
- [ ] Is the voice present or reflecting?
- [ ] Does every element serve the aliveness?
- [ ] Have I cut everything that could be cut?
- [ ] Am I showing off or playing?
- [ ] Does the sound serve the meaning (in sonic forms)?

---

## PUSHING INTO VIRTUOSO TERRITORY

### The Problem with 10/10

Once you hit 10/10, the iteration process stalls. There are no more weaknesses to fix. But "no weaknesses" isn't the same as "masterpiece."

The difference:
- **10/10**: Fully alive, no dead spots, couldn't be better
- **Masterpiece**: Haunts you, changes you, necessary to the universe

### The Five Markers (from v2 framework)

1. **Necessity** - Does the world need this to exist?
2. **Haunting** - Will it stay with the reader in 10 years? (Not dark—sticky. Joy can haunt too.)
3. **Irreplaceability** - Could only this creator have made it?
4. **Surprise → Inevitable** - Unpredictable in prospect, inevitable in retrospect
5. **Risk** - Is there a move that could have failed catastrophically?

### The Virtuoso Paradox

You cannot aim for masterpiece. Aiming creates self-consciousness.

**What you CAN do:**

1. **Write from obsession, not assignment**
   - Not "write a children's poem" but "write the thing you can't stop thinking about"
   - The piece that won't leave you alone

2. **Take real risks**
   - Make a move that might ruin everything
   - Safe work caps at excellent
   - Ask: "What would I do if I weren't afraid this would fail?"

3. **Surprise yourself**
   - If you know exactly where it's going, it's not virtuoso territory
   - Follow the piece where it wants to go, not where you planned

4. **Amplify strengths, not just fix weaknesses**
   - Once at 10/10, stop fixing
   - Find the most alive moment and push it further
   - Let it become MORE itself, even if that introduces new problems

5. **Let it be strange**
   - The things you want to edit out for being "too weird" are often the truest
   - Conventional is safe. Strange can be necessary.

### The Virtuoso Evaluation Prompt

Use this ONLY for pieces that genuinely score 10/10:

```
This piece scored 10/10 on aliveness. Now apply the Virtuoso Test (Phase 5 of the v2 framework).

THE PIECE:

[INSERT PIECE]

---

EVALUATE against the Five Markers:
1. NECESSITY - Does the world need this?
2. HAUNTING - Will it stay with you?
3. IRREPLACEABILITY - Could only this creator have made it?
4. SURPRISE → INEVITABLE - Unpredictable becoming necessary?
5. RISK - Was something real bet?

Score: 10 / 10+ / 10++ / 10+++

What would push it higher? Not "fix weakness" but "amplify what's transcendent."
```

### The Uncomfortable Truth

Most pieces—even great ones—won't be masterpieces. That's fine. A 10/10 is exceptional.

But if you never try for virtuoso territory, you guarantee you'll never get there.

The process: Write from obsession. Take real risks. Follow the strange. See what happens.

---

## THE BOTTOM LINE

The gap between 5/10 and 10/10 is not talent. It's iteration.

The gap between 10/10 and masterpiece is not iteration. It's risk, obsession, and letting go.

Write. Get honest feedback. Fix one thing. Repeat.

And when you hit 10/10—stop fixing. Start risking.
