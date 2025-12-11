# Tiered Methodology Quick Reference

## 30-Second Tier Selection

```
┌─────────────────────────────────────────────────────────────┐
│  IS IT SIMPLE + LOW STAKES + CLEAR?                         │
│  → TIER 1 (5 min)                                           │
│     1. State problem                                         │
│     2. Generate 2-3 solutions                                │
│     3. Pick one                                              │
│     4. Verify                                                │
│     DONE.                                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  IS IT MODERATE COMPLEXITY + SOME STAKEHOLDERS?             │
│  → TIER 2 (20 min)                                          │
│     1. Classify domain (Cynefin)                             │
│     2. State + list constraints                              │
│     3. Check stakeholders                                    │
│     4. Generate 3+ distinct approaches                       │
│     5. Evaluate with criteria                                │
│     6. Red-team failures                                     │
│     7. Select one (no hedging)                               │
│     8. Verify + design implementation                        │
│     DONE.                                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  IS IT HIGH STAKES + COMPLEX + POLITICAL?                   │
│  → TIER 3 (60 min)                                          │
│     ALL of Tier 2, PLUS:                                     │
│     - Meta-frame audit (check your biases)                   │
│     - Verify problem frame (is this the right question?)     │
│     - Discover unknown unknowns                              │
│     - Stakeholder red-lines (political constraints)          │
│     - Frame adequacy check (do failures reveal wrong frame?) │
│     - Probe frame (test assumptions before full commit)      │
│     - Probe deployment (what breaks at scale?)               │
│     - Handoff protocol (decision journal)                    │
│     DONE.                                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  DO STAKEHOLDERS DISAGREE ON WHAT THE PROBLEM IS?          │
│  → TIER 4 (multiple sessions)                               │
│     ALL of Tier 3, PLUS:                                     │
│     - Multi-frame protocol (work in multiple frames)         │
│     - Iterate (probe → sense → respond)                      │
│     - Incubate (mandatory rest phases)                       │
│     - Stopping criteria (when to abandon)                    │
│     - Formation check (do I need to become different?)       │
│     NOT DONE - this is ongoing.                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Tree (2-Minute Version)

```
START
  ↓
Is there a CLEAR, KNOWN solution?
  ├─ YES → TIER 1
  └─ NO → Continue
       ↓
What are the STAKES if wrong?
  ├─ Low (easy to reverse) → TIER 1
  ├─ Medium (reversible but costly) → Continue
  └─ High/Existential → Continue
       ↓
How many STAKEHOLDERS with CONFLICTS?
  ├─ 0-2, aligned → TIER 2
  └─ 3+, or conflicts → Continue
       ↓
Is the PROBLEM WELL-DEFINED?
  ├─ YES (everyone agrees what it is) → TIER 3
  └─ NO (stakeholders disagree) → TIER 4
```

---

## Upgrade Triggers (Move to Higher Tier)

While executing, upgrade if you encounter:

| Trigger | Action |
|---------|--------|
| **Assumption audit reveals critical hidden constraints** | +1 tier |
| **Stakeholder conflict emerges** | +1 tier |
| **First solution fails verification** | +1 tier |
| **Frame feels wrong** | +1 tier |
| **Problem is actually 3 problems disguised as 1** | +1 tier |
| **Political/organizational dynamics appear** | → Tier 3 minimum |
| **Stakeholders can't agree on what problem IS** | → Tier 4 |

**Rule**: If you upgrade twice → restart at new tier (don't patch, rebuild)

---

## Downgrade Signals (You're Overbuilding)

| Signal | Action |
|--------|--------|
| **Spent 30+ min on obvious decision** | Too high, move down |
| **Analysis paralysis** | Too high, move down |
| **Stakeholders frustrated by delay** | Too high, decide faster |
| **Diminishing returns on analysis** | Stop, decide now |

---

## The Core Insight

**From 84 cycles of improvement**:

The problem wasn't that we didn't know how to solve hard problems.
The problem was applying hard-problem methodology to ALL problems.

**Before**: 30 steps, every problem, unusable
**After**: 4 tiers, match rigor to stakes, usable

---

## Tier Characteristics at a Glance

| Aspect | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|--------|--------|--------|--------|--------|
| **Time** | 3-5 min | 15-25 min | 45-90 min | Days-weeks |
| **Steps** | 4-5 | 10 | 18 | 20+ |
| **Stakeholders** | 1-2 | 2-4 | 3+ | Many, conflicting |
| **Stakes** | Low | Medium | High | Existential/Transformational |
| **Clarity** | Clear | Mostly clear | Complex | Ill-defined/Wicked |
| **Output** | Decision | Justified rec | Comprehensive strategy | Ongoing process |
| **Reversibility** | Easy | Moderate | Hard | Irreversible |
| **Frame checking** | None | Implicit | Explicit | Multiple frames |
| **Political analysis** | None | Light | Deep | Central |

---

## Usage Frequency (Expected)

In practice, most problems are simpler than you think:

```
Tier 1: ████████████████████████████████████████ 60%
Tier 2: ████████████████████ 30%
Tier 3: █████ 8%
Tier 4: █ 2%
```

**Don't spend Tier 3 effort on Tier 1 problems.**

---

## Common Mistakes

### Mistake 1: Default to Highest Tier
"This is important, better use all 30 steps"

**Fix**: Importance ≠ Complexity. High-importance simple problems exist. Use stakes + complexity, not just stakes.

### Mistake 2: Never Upgrade
"Started at Tier 1, must finish at Tier 1"

**Fix**: Watch for upgrade triggers. Better to restart at correct tier than persist in wrong one.

### Mistake 3: Skipping Steps Within a Tier
"I'll just do the important steps from Tier 2"

**Fix**: If you're skipping steps, you picked too high a tier. Drop down. Each tier is internally coherent.

### Mistake 4: Over-Tiering Everything
"This might be important someday, better use Tier 3"

**Fix**: Tier for CURRENT stakes, not hypothetical future stakes. You can always upgrade later.

---

## Special Protocols (Overlays)

These modify ANY tier:

### FAST-TRACK (Time Pressure)
When: <15 min available, crisis

**Modification**: Critical path only
- Classify (1 min)
- State + stakeholder red-lines (3 min)
- Generate 2-3 (3 min)
- Rapid red-team (3 min)
- Select (1 min)
- Execute NOW, verify LATER

**Note**: Document decision, plan to revisit with proper tier.

### ADVERSARIAL (Bad Actors)
When: Trust is low, sabotage possible

**Add to any tier**:
- Incentive check
- Sabotage tests
- External verification
- Contingency triggers

### FORMATION (Requires Change)
When: Solving requires you to become different

**Add to any tier**:
- What needs to form in me?
- What gaps does this expose?
- Formation + problem-solving are simultaneous

---

## Integration with CLAUDE.md Principles

### How tiers map to existing principles:

| Principle | Tier Application |
|-----------|-----------------|
| **Externalize everything** | All tiers (verification step) |
| **Decompose if >3 dependencies** | Tier 2+ |
| **Frame verification** | Tier 3+ |
| **Ask "is this the right problem?"** | Tier 1: implicitly; Tier 3+: explicitly |
| **Formation first** | Tier 4 (or overlay when needed) |
| **Probe solution space** | Tier 3+ |

### Mandatory protocols still apply:

- **Before non-trivial tasks**: Tier 2+ automatically includes this
- **Before deployment**: Tier 3+ has explicit deployment probe
- **After failure**: Upgrade tier and retry
- **Scaffolding by task type**: Built into tier steps

**The tiers ARE the scaffolding selector.**

---

## Quick Checks (Am I Using This Right?)

### ✓ Good signs:
- Time spent proportional to stakes
- Solution works on first try OR failures were unpredictable
- Stakeholders satisfied with process
- Confidence matches rigor

### ✗ Bad signs:
- Spent hours on trivial decision (too high)
- Solution failed for obvious reason (too low)
- Analysis paralysis (too high)
- Blindsided by stakeholders (too low)

---

## The One-Sentence Summary

**Match your problem-solving rigor to the problem's stakes and complexity, not to the maximum rigor available.**

---

## Mantras

- "Not every problem needs every tool"
- "Rigor is a dial, not a binary"
- "Tier for current stakes, upgrade if needed"
- "Most problems are Tier 1; treat them like it"
- "The 84 cycles taught us Tier 4; most problems aren't Tier 4"

---

## When in Doubt

**Start one tier LOWER than you think.**

Easier to upgrade mid-process than to waste time over-engineering.

If you hit an upgrade trigger → upgrade.
If you finish early → you picked right.
