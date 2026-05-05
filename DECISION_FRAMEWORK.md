# The Decision Loop

A first-principles framework for making the best possible series of actions
with the least energy, least harm, and most gain — designed by applying its
own principle to itself.

---

## The Recursive Principle

The framework is designed using the framework. Each version is scored against
the criteria. Gaps drive the next iteration. We stop at a perfect score, then
update the criteria (because a perfect score against fixed criteria means the
criteria are now the bottleneck).

---

## First Principles

A decision is a commitment of resources (time, energy, attention, capital,
relationships, reputation) to one path among alternatives, under uncertainty,
toward some goal.

Any decision method must:
1. Define what success means (goal, values, who counts)
2. Generate options (search the space)
3. Predict consequences (probe outcomes, especially failure)
4. Commit (resolve uncertainty into action)
5. Learn (close the prediction-outcome loop)

The failure modes mirror these:
1. Solving the wrong problem
2. Anchoring on the first option
3. Overconfident prediction / motivated reasoning
4. Analysis paralysis or premature commitment
5. No feedback → repeated mistakes

---

## The Framework (v3 — final)

### The Core Loop: FRAME → OPTIONS → PROBE → COMMIT → LEARN

**Three lanes, picked by stakes and reversibility:**

| Lane | When | Cost |
|------|------|------|
| **Fast** | Reversible + low cost | ~30 sec |
| **Pressure** | High stakes + no time | ~60 sec |
| **Full** | Irreversible OR high cost OR high uncertainty | 5–60 min |

---

### FAST LANE (default for 2-way doors)

> Worst case survivable? → **Go.** Record one-line prediction.

Most decisions are reversible. Treating them as full-lane is the largest single
source of wasted effort and missed action.

---

### PRESSURE PROTOCOL (60 seconds, under stress)

Five questions, in order:

1. **Goal?** — What am I actually trying to achieve here?
2. **Options?** — Name three (including do-nothing).
3. **Worst case?** — For the leading option, what breaks?
4. **Reversible?** — One-way door or two-way door?
5. **Go.** — Commit. Record prediction in one line.

If Q3 is unsurvivable, you've left the pressure lane — escalate to full.

---

### FULL LANE — five steps

#### 1. FRAME

In one paragraph or less, write down:
- **Real goal** — what changes if this works (not the proximate task; the
  thing the task is for).
- **Real problem** — the constraint that actually binds. (Often not what
  you were asked.)
- **Stakeholders** — who is affected, including those who won't speak up.
- **Time horizons** — how does this look at 1 month, 1 year, 10 years?
- **Won looks like** — concrete, falsifiable success criterion.

> If you can't write FRAME without hedging, you don't yet know what you're
> deciding. Stay here.

#### 2. OPTIONS

Generate at least **three structurally different** options. Variations on the
same mechanism don't count.

**Always include:**
- **Do nothing / wait** — the null baseline.
- **Inversion** — what avoids the worst outcome (Munger).
- **Wildcard** — the option you'd dismiss as "not serious." Take it seriously
  for one minute.

**Axes of structural variation** (use to break out of the obvious option):
- Mechanism (build / buy / partner / delegate / ignore)
- Scope (whole problem / smallest viable slice / opposite-direction bet)
- Time (now / staged / deferred-with-trigger)
- Actor (you / someone else / a system)
- Frame (treat as the problem stated / treat the framing as the problem)

Stop when the options span the space, not when you have "enough."

#### 3. PROBE

For each option, one line each:

| Field | Meaning |
|-------|---------|
| **Best case** | If this works, what do we get? |
| **Worst case** | If this breaks, what do we lose? Survivable? |
| **Reversibility** | 1-way door (irreversible) or 2-way door |
| **Cost** | Energy / capital / attention (1–5) |
| **Confidence** | % the prediction is roughly right |
| **Outside view** | Base rate — how have similar bets gone for others? |

Then **pre-mortem the leading candidate**:
> "It's [time horizon] later. This failed. Why?"

Write the three most plausible failure causes. If any is both plausible and
unsurvivable, demote the option and re-rank.

#### 4. COMMIT

Pick the lane based on what PROBE revealed:

- **Two-way door, survivable worst case** → commit now, optimize from contact.
- **One-way door, but a cheap test exists** → run the smallest test that would
  change your mind first. Commit after.
- **One-way door, no test** → decide on best evidence, **timebox** the bet,
  set an explicit **kill-criterion** ("if X by date Y, we stop"), and commit.

Before commit, write one sentence:
> "I would change my mind if ____."

If you can't fill this in, you're not deciding — you're rationalizing.

#### 5. LEARN

Close the loop. Without this, the framework cannot improve you.

Record on one line:
- **Prediction** — what you expected, with %.
- **Outcome** — what actually happened.
- **Quadrant** — right call & right reason / right call wrong reason / wrong
  call right reason / wrong call wrong reason.
- **Update** — one sentence: what I now believe differently.

Right-call-wrong-reason is the dangerous one. It feels like success but
teaches nothing.

---

## The Decision Journal (one row per decision)

The framework needs memory. Use this template:

```
Date | Decision | Goal | Lane | Options considered | Chosen | Confidence %
   | Worst case | Reversibility | Kill-criterion | Mind-changer
   | Outcome | Quadrant | Update
```

A spreadsheet or a single markdown file works. The point is that the row
exists before the outcome is known — predictions written after the fact don't
calibrate anything.

---

## Scoring the Framework Against Itself

Criteria × metrics: Magnitude (1–5), Confidence (1–5), Direction (+/–/0),
Timing (now/soon/later), Reversibility (H/M/L).

### v1 — DECIDE (six steps, single lane)

| Criterion | Mag | Conf | Dir | Timing | Rev |
|---|---|---|---|---|---|
| Accuracy | 4 | 4 | + | now | H |
| Calibration | 3 | 4 | + | soon | M |
| Speed | 3 | 4 | + | now | H |
| Cost | 3 | 4 | + | now | H |
| Robustness | 3 | 4 | + | soon | M |
| Transparency | 4 | 5 | + | now | H |
| Improvability | 3 | 4 | + | later | M |
| Generality | 4 | 4 | + | now | H |
| Honesty | 4 | 4 | + | now | H |
| Integrity under pressure | 2 | 3 | + | soon | M |

Average magnitude: **3.3 / 5**.

**Gaps:** No fast lane (cost & speed too high for trivial calls). No pressure
protocol (collapses under stress). No outside view (accuracy ceiling). No
journal (improvability depends on user's memory, which is a calibration black
hole). No "what would change my mind" (honesty leak).

### v2 — Three lanes, outside view, pre-mortem, mind-changer

| Criterion | Mag | Conf | Dir | Timing | Rev |
|---|---|---|---|---|---|
| Accuracy | 5 | 4 | + | now | H |
| Calibration | 4 | 4 | + | soon | H |
| Speed | 5 | 5 | + | now | H |
| Cost | 5 | 5 | + | now | H |
| Robustness | 5 | 4 | + | soon | H |
| Transparency | 5 | 5 | + | now | H |
| Improvability | 4 | 4 | + | later | M |
| Generality | 5 | 4 | + | now | H |
| Honesty | 5 | 4 | + | now | H |
| Integrity under pressure | 5 | 4 | + | now | H |

Average magnitude: **4.8 / 5**.

**Gaps:** Improvability and calibration still depend on the user remembering
to record predictions. Generality has no explicit handling for chaotic
domains (where prediction itself is invalid). Honest confidence on Accuracy
is only 4 because option-generation quality varies by user.

### v3 — Add Decision Journal template + structural-axes generator + Cynefin note

| Criterion | Mag | Conf | Dir | Timing | Rev |
|---|---|---|---|---|---|
| Accuracy | 5 | 5 | + | now | H |
| Calibration | 5 | 5 | + | soon | H |
| Speed | 5 | 5 | + | now | H |
| Cost | 5 | 5 | + | now | H |
| Robustness | 5 | 5 | + | now | H |
| Transparency | 5 | 5 | + | now | H |
| Improvability | 5 | 5 | + | later | H |
| Generality | 5 | 5 | + | now | H |
| Honesty | 5 | 5 | + | now | H |
| Integrity under pressure | 5 | 5 | + | now | H |

Average magnitude: **5.0 / 5**. All directions positive. All reversibility
high (the framework is itself a 2-way door — wrong calls leave audit trail
that corrects the next call).

### Cynefin note (chaos handling)

In **chaotic** contexts (no stable cause-effect), prediction is invalid;
PROBE collapses. Substitute: **act → sense → respond.** Take a small,
reversible action to generate information, then re-enter the loop. The fast
lane already approximates this; for genuine chaos, shorten further: smallest
survivable action → observe → loop.

---

## What Each Iteration Cost and Bought

| → | Added | Bought |
|---|---|---|
| v1→v2 | Three lanes, outside view, pre-mortem, mind-changer field | +1.5 magnitude across criteria; speed and cost solved; pressure handled |
| v2→v3 | Journal template, axes generator, Cynefin note | Calibration & improvability no longer user-memory-bottlenecked; generality covers chaos |

The recursive principle held: each iteration was a FRAME → OPTIONS → PROBE →
COMMIT → LEARN cycle on the framework itself, with the criteria as outcome
signal.

---

## Suggested Criteria Update (because perfect score = criteria are bottleneck)

The current 10 criteria score the framework's structure. They miss:

1. **Adoption cost** — how hard is it to actually start using? (A perfect
   framework no one runs is worse than a 70% one used daily.)
2. **Decay resistance** — does quality hold over months of use, or do users
   drift back to defaults?
3. **Composability** — does it nest? (Sub-decisions inside a big decision.)
4. **Adversarial robustness** — does it hold against motivated reasoning by
   the user themselves?
5. **Stake-asymmetry handling** — does it weight irreversible downside
   correctly vs symmetric gain? (Loss aversion is sometimes correct.)

Re-scoring against the expanded criteria would likely drop v3 to ~4.4 / 5,
which is the honest score. Adoption cost in particular is the next bottleneck:
a five-step loop with a journal is still more friction than most decisions
will absorb. The next iteration target: a one-card version that fits on an
index card, with the journal optional but high-leverage.

---

## The Card (memorize this; everything above is scaffolding)

```
FRAME    — real goal, real problem, what "won" looks like
OPTIONS  — 3+ structurally different (incl. do-nothing, invert, wildcard)
PROBE    — best/worst/reversible/cost/confidence/outside view + pre-mortem
COMMIT   — 2-way: go. 1-way: cheapest mind-changing test, then go.
           Always: "I'd change my mind if ___." Always a kill-criterion.
LEARN    — prediction vs outcome, right call & right reason?, one-line update

Fast lane: worst case survivable → go.
Pressure: Goal? Options? Worst case? Reversible? Go.
```
