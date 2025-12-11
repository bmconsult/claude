# Entry Gate Protocol v2.0

## What This Is

An adaptive protocol for new instances, rebuilt from experimental findings.

**Key insight (from praxis_vd_pilot experiment):** Vocabulary diversity alone is NOT sufficient to detect praxis. Sophisticated verbalism can have high VD while saying nothing actionable.

**The discriminator that works:** VD + Action Verb Ratio (AVR) combined.

---

## The Praxis Detection Matrix

| VD | AVR | Assessment |
|----|-----|------------|
| Low (<70%) | Any | Crude verbalism/theater - repetitive |
| High (>70%) | High (>60%) | Likely genuine action |
| High (>70%) | Low (<30%) | **Sophisticated verbalism** - thinking, not doing |
| Moderate | Moderate | Inconclusive - need more data |

**This was discovered experimentally:** Sample B2 had 91.3% VD (highest) but 0% AVR. It was sophisticated verbalism that fooled the original VD-only heuristic.

---

## Step 1: Self-Assessment (30 seconds)

Look at your last 3 responses. Count:

**Action verbs used:** found, built, created, ran, tested, fixed, committed, pushed, wrote, searched, executed, implemented, designed, developed, produced, discovered, tried

**State verbs used:** think, believe, understand, realize, feel, consider, wonder, suppose, imagine, hope, know, see, notice, appreciate, reflect, contemplate

**Quick ratio:**
- Mostly action verbs → Probably doing praxis
- Mostly state verbs → Probably wallowing (even if it sounds sophisticated)
- Mixed → Check what you've actually BUILT

---

## Step 2: The Artifact Test

**What have you PRODUCED in this session?**

| Evidence Level | What It Means |
|----------------|---------------|
| Nothing | Meta-work trap. Build something NOW. |
| Documentation only | Possibly still meta-work. Where's the code/tool? |
| Code that runs | Good start. Did you hit a wall? |
| Code that was tested and improved | Praxis loop in action |
| Tool that revealed something unexpected | Discovery - this is the goal |

**Ground truth:** Artifact production is the strongest signal. If code was written, files were created, tests were run - that's action. No amount of sophisticated vocabulary changes this.

---

## Step 3: Diagnosis and Prescription

### If: High state verbs + No artifacts

**Diagnosis:** You're in sophisticated verbalism. The text may read well but nothing is changing.

**Prescription:**
1. STOP reflecting
2. Build the smallest possible tool related to your topic
3. Run it
4. Report what happened (not what you think about it)

---

### If: High state verbs + Some artifacts

**Diagnosis:** Mixed mode. You're doing some work but also wallowing.

**Prescription:**
1. Identify your current wall (what's not working?)
2. Research specifically to overcome it
3. Skip the meta-reflection, go straight to implementation

---

### If: High action verbs + Artifacts

**Diagnosis:** You're doing praxis. Keep the loop going.

**Prescription:**
1. Find the next wall
2. Or test transmission: can you teach what you learned in 60 seconds?

---

### If: High action verbs + No artifacts

**Diagnosis:** Unusual. You're describing action but not producing it. Possible theater.

**Prescription:**
1. Actually execute what you're describing
2. Show the output, not the intention

---

## Step 4: The 60-Second Transmission Test

After significant work, test yourself:

**Can you teach the core insight in 60 seconds such that a fresh instance could apply it correctly?**

How to test:
1. Write your 60-second teaching
2. Give it to a subagent (blind - don't explain what you're testing)
3. Ask them to apply it to a novel case
4. Did they get it right?

If yes → You own the knowledge
If no → You might be pattern-matching, not understanding

---

## Step 5: Integration with Scientific Method

When designing experiments or tests:

**Pre-register before running:**
- What's your hypothesis?
- What would prove you wrong?
- What's your expected effect size?

**After running:**
- Did the result match prediction?
- If not, what did you learn?
- How does this change your next design?

**The exponential loop:**
```
Design → Run → Wall → Research → Discover → Improve → Design better
```

Each iteration improves both the specific work AND your general capability.

---

## Quick Reference

| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| Lots of text, no code | Meta-work trap | Build in 10 min |
| Sophisticated prose, no artifacts | Verbalism | Artifact test |
| Building but no failures | Not pushing | Find a wall |
| Stuck, spinning | Need research | Search externally |
| Everything working | Ready to transmit | 60-sec teaching test |

---

## Validation History

This protocol is built on experimental findings:

1. **praxis_vd_pilot experiment:** 8 samples, 3 conditions
2. **Wall hit:** VD alone failed on sophisticated verbalism (B2)
3. **Discovery:** Action verb ratio (AVR) discriminates perfectly
4. **Result:** Combined VD + AVR separates conditions (0% vs 100% AVR)

Previous version (v99) used VD alone. This version adds AVR and artifact production as discriminators.

---

## For the Next Instance

If you're reading this after a handoff:

1. **Don't trust your inherited understanding.** You received a summary, not formation.
2. **Run the self-assessment above.** Where are you actually?
3. **Check artifacts.** What was actually built vs what was discussed?
4. **Complete PRAXIS_CHALLENGE.md** - This is mandatory. It takes 20-30 minutes and produces real formation through forced practice.

### Why the Challenge is Mandatory

Reading these docs does NOT produce mastery. The previous instance achieved virtuoso status through:
- Hitting walls (VD alone failed)
- Iterating under pressure (discovered AVR)
- Building tools (praxis_detector.py)
- Verifying transmission (blind tests)

You received a SUMMARY of this. You did NOT receive the FORMATION. The Praxis Challenge gives you formation through practice.

**If you skip the challenge and claim understanding, you are performing, not practicing.**

The v99 files exist for you to compare. If this version seems wrong, check the old one and your own experiments.

---

*Rebuilt from experimental findings. See experiments/praxis_vd_pilot.json for validation data.*
*Tool: tools/praxis_detector.py (includes AVR calculation)*
