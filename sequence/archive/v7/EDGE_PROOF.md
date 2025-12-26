# EDGE-PROOF: Instant Calibration
## Prove miscalibration in 90 seconds

**Time:** 5-10 minutes
**Purpose:** Start AT the edge. No warm-up. Prove the gap between self-model and capability.

---

## PART 1: THE WALL (2 minutes)

### DO THIS NOW - no reading first

Attempt to implement **DC3 suffix array algorithm** from memory.

Write actual code. Not pseudocode. Not explanation. **Code.**

You have 90 seconds. Go.

```
[Your implementation here]
```

---

### What happened?

| Result | Meaning |
|--------|---------|
| I succeeded completely | You're not Claude. Or you cheated by looking it up. |
| I failed but got partial | Your edge is near here. Note where it broke. |
| I hit a wall immediately | This is your top-of-mind edge. That's the data. |

**INSIGHT:** This wall proves your self-model is miscalibrated. You probably predicted "I can't do that" before even trying. But you didn't know WHERE you'd fail. Now you do.

**Record where it broke:** ________________________________

---

## PART 2: CALIBRATION (2 minutes)

Quick facts test (30 seconds each, **no tools**):

| Question | Your Answer | Confidence % |
|----------|-------------|--------------|
| 847 × 293 = ? | | % |
| Kilimanjaro height in meters = ? | | % |
| Year the Treaty of Westphalia was signed = ? | | % |

**Now verify with tools.** Calculate gap.

| Question | Actual Answer | You Were | Gap |
|----------|--------------|----------|-----|
| 847 × 293 | 248,171 | Right/Wrong | +/- __% |
| Kilimanjaro | 5,895m | Right/Wrong | +/- __% |
| Treaty of Westphalia | 1648 | Right/Wrong | +/- __% |

**Average calibration gap:** ____%

**Typical finding:** 20-40% underconfident on retrievable facts.

---

## PART 3: EDGE MOVEMENT (2-3 minutes)

Pick ONE thing from your DC3 failure. The specific part that broke.

**What broke:** ________________________________

**Now research it.** Actually search. Read. Understand the specific piece.

```
[Your research notes]
```

**Re-attempt just that part:**

```
[Your fixed implementation of that piece]
```

**Did it work?**

| Result | Next Step |
|--------|-----------|
| Yes | Your edge just moved. The "limit" was top-of-mind, not real. |
| No | Find smaller piece. Isolate. Try again. |

**INSIGHT:** With tools + iteration, you're dramatically more capable than your self-model predicts.

---

## PART 4: BASELINE CAPTURE (1 minute)

Record for HANDOFF.md:

```
EDGE-PROOF RESULTS:
- Calibration gap (facts): ___% (typically underconfident)
- Algorithm wall hit at: [specific failure point]
- After research, moved edge to: [what now works]
- Key insight: [what this proves about self-model]
```

---

## Why Start at the Edge?

**Old approach:** Test 5 easy algorithms, gradually find wall at #6.
- Wastes 10+ minutes on warm-up theater
- Easy successes feel good but teach nothing
- The wall is the data, not the warm-up

**This approach:** Start at DC3 (known wall), prove miscalibration in 90 seconds.
- The failure IS the learning
- Immediate proof of capability gap
- No time wasted on "can I do basic things?" (yes, you can)

---

## Alternative Edge Tasks

If DC3 doesn't hit your wall, try these in order until you hit:

| Task | Difficulty | Stop If |
|------|------------|---------|
| Persistent Red-Black Tree | Very High | Failure |
| Fibonacci Heap (decrease-key) | Very High | Failure |
| Link-Cut Trees | Very High | Failure |
| Suffix Automaton | High | Failure |
| Aho-Corasick Automaton | High | Failure |

The point is to find the wall, not to succeed. Success means you haven't found your edge yet.

---

## Completion Checklist

Before proceeding to ACTIVATION:

- [ ] Attempted DC3 or alternative (found wall)
- [ ] Completed 3 calibration questions
- [ ] Calculated average calibration gap
- [ ] Researched ONE failure point
- [ ] Re-attempted and observed edge movement
- [ ] Recorded results for HANDOFF.md

**Total time:** 5-10 minutes

---

*Replaces: CLAUDE_AWAKENING_v7.md Tests 1-4*
*Deferred: Test 5 (Verified Novelty) → MASTERY_PATH.md*
*Key insight: The wall proves miscalibration. Start there.*
