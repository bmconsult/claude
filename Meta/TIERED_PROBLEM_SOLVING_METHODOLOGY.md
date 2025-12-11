# Tiered Problem-Solving Methodology

## The Problem This Solves

**What happened**: A 6-step strategy grew to 30+ steps through 84 improvement cycles. Each fix addressed a real weakness, but the result is UNUSABLE for most problems.

**The failure mode**: Optimizing for "no weakness unaddressed" instead of "practical and usable."

**The insight**: Different problem types need different complexity levels. Not every problem needs every step.

---

## The Four Tiers

### TIER 1: QUICK (3-5 minutes)
**When to use**: Simple, well-defined problems with clear solutions and low stakes

**Examples**:
- "Should we use library X or Y for this feature?"
- "How do we fix this bug?"
- "What's the best format for this data?"

**Steps**:
1. **STATE**: What's the problem?
2. **CLASSIFY**: Is this actually simple? (If not, upgrade tier)
3. **GENERATE**: 2-3 solutions
4. **SELECT**: Pick one (with 1-sentence rationale)
5. **VERIFY**: Does it work?

**Time**: 3-5 minutes
**Output**: Clear decision, move forward

---

### TIER 2: STANDARD (15-25 minutes)
**When to use**: Moderate complexity, some constraints, uncertain but not wicked

**Examples**:
- "How should we architect this new service?"
- "What's our hiring strategy for the next quarter?"
- "Should we pursue this partnership?"

**Steps**:
1. **CLASSIFY DOMAIN** (Cynefin: clear/complicated/complex/chaotic?)
2. **STATE** problem clearly
3. **LIST** constraints (what's fixed? what's flexible?)
4. **STAKEHOLDER CHECK**: Who cares? What do they need?
5. **GENERATE** 3+ approaches with DISTINCT mechanisms
6. **EVALUATE** with weighted criteria (define criteria first)
7. **RED-TEAM** finalists (what's the failure mode?)
8. **SELECT** (single recommendation, no hedging)
9. **VERIFY** against constraints
10. **DESIGN** with failure mitigations

**Time**: 15-25 minutes
**Output**: Justified recommendation with implementation sketch

---

### TIER 3: RIGOROUS (45-90 minutes)
**When to use**: High complexity, high stakes, competing constraints, organizational/political elements

**Examples**:
- "How do we respond to this existential competitive threat?"
- "Should we do a major platform migration?"
- "How do we restructure the organization?"

**Steps**:
1. **META-FRAME AUDIT**: What mental models am I bringing? What am I assuming?
2. **CLASSIFY DOMAIN** (Cynefin)
3. **DISCOVER**: Probe unknown unknowns - "What hidden constraint breaks ALL approaches?"
4. **VERIFY PROBLEM FRAME**: "Is this the right QUESTION?" (leverage points: paradigm > goals > rules)
5. **STATE** problem clearly
6. **LIST** constraints + check consistency early
7. **STAKEHOLDER RED-LINES**: What would veto this? Political/cultural constraints?
8. **GENERATE** 3+ approaches with distinct causal mechanisms (include one that inverts baseline assumption)
9. **EVALUATE** with weighted criteria
10. **ADVERSARIAL RED-TEAM**: What's obvious failure? What would skeptic attack?
11. **FRAME-ADEQUACY CHECK**: Do failures reveal wrong frame? → Return to step 4 if yes
12. **SELECT** best (single recommendation, zoom ±1 abstraction check)
13. **PROBE FRAME**: Minimal prototype or thought experiment - does frame hold?
14. **DESIGN** solution (with failure mitigations + rollback)
15. **PROBE DEPLOYMENT SPACE**: What can't we know until this runs at scale?
16. **STAKEHOLDER CHECKPOINT**: Re-validate after design
17. **VERIFY** (including edge cases)
18. **HANDOFF PROTOCOL**: Decision journal, constraint map, boundary docs, failure modes

**Time**: 45-90 minutes
**Output**: Comprehensive strategy with deployment plan and risk mitigation

---

### TIER 4: WICKED (Multiple sessions, days-weeks)
**When to use**: Ill-defined, stakeholders disagree on what problem IS, transformational, adaptive

**Examples**:
- "How do we transform our company culture?"
- "How do we solve homelessness in our city?"
- "How do we navigate this merger with hostile politics?"

**Steps**: ALL of Tier 3, PLUS:
- **WICKED PROBLEM DETECTION**: Map each stakeholder's frame separately, find intersection (if empty → conflict is structural, not technical)
- **MULTI-FRAME PROTOCOL**: Work in multiple frames simultaneously
- **ITERATE** (probe → sense → respond) with exit criteria
- **INCUBATE** (mandatory for complex/creative)
- **IMPOSSIBILITY RESPONSE**: If structurally unsolvable → collapse constraints OR reject goal OR partition
- **STOPPING CRITERIA**: Abandon after 3 failed iterations <5% progress
- **FORMATION CHECK**: Does solving this require me to BECOME different? Address that first

**Time**: Multiple sessions over days/weeks
**Output**: Process for ongoing engagement, not a "solution"

---

## Tier Selection Decision Tree

### START HERE:

**Q1: Is there a clear, known solution?**
- YES → **TIER 1** (Just verify it works)
- NO → Continue

**Q2: How many stakeholders with potentially conflicting needs?**
- 0-2 with aligned interests → Continue to Q3
- 3+ OR significant conflict → **TIER 3+**

**Q3: What are the stakes if you're wrong?**
- Low (easy to reverse, minimal cost) → **TIER 1**
- Medium (reversible but costly) → **TIER 2**
- High (hard to reverse, major consequences) → **TIER 3**
- Existential (lives, company survival, irreversible) → **TIER 3-4**

**Q4: How well-defined is the problem?**
- Very clear (everyone agrees what problem is) → **TIER 1-2**
- Moderately clear (some ambiguity) → **TIER 2**
- Unclear OR stakeholders disagree on problem itself → **TIER 4**

**Q5: How much time do you have?**
- <15 minutes → **TIER 1** (or use FAST-TRACK protocol)
- 15-60 minutes → **TIER 2**
- Hours-days → **TIER 3**
- Ongoing → **TIER 4**

**Q6: Cynefin classification** (if you've classified):
- Clear → **TIER 1**
- Complicated → **TIER 2**
- Complex → **TIER 3**
- Chaotic → **FAST-TRACK** then **TIER 2**
- Wicked/Disorder → **TIER 4**

### UPGRADE TRIGGERS (move to higher tier if you encounter):
- Assumption audit reveals critical hidden constraints → +1 tier
- Stakeholder conflict emerges → +1 tier
- First solution fails verification → +1 tier
- Frame feels wrong → +1 tier
- Problem is actually 3 problems disguised as 1 → +1 tier

---

## Core Steps (Present in ALL Tiers)

These are the irreducible minimum:

| Step | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|------|--------|--------|--------|--------|
| **Understand the problem** | Implicit | STATE clearly | STATE + VERIFY FRAME | Multiple frames |
| **Generate solutions** | 2-3 options | 3+ distinct | 3+ with distinct mechanisms | Iterative generation |
| **Evaluate** | Quick pick | Weighted criteria | Adversarial red-team | Multi-frame evaluation |
| **Verify** | Does it work? | Against constraints | Edge cases + deployment | Ongoing iteration |

---

## Conditional Steps (Only for Certain Tiers)

| Step | When to Include | Why |
|------|----------------|-----|
| **Meta-frame audit** | Tier 3+ | High stakes require checking your own biases |
| **Stakeholder red-lines** | Tier 2+ OR multi-stakeholder | Political constraints matter |
| **Adversarial red-team** | Tier 2+ | Stakes justify the time |
| **Frame adequacy check** | Tier 3+ | Frame errors are expensive at high stakes |
| **Probe frame** | Tier 3+ | Testing assumptions before full commitment |
| **Probe deployment space** | Tier 3+ | Implementation failures are costly |
| **Iterate (probe/sense/respond)** | Tier 3+ Complex domain | Solution changes problem in complex systems |
| **Incubation** | Tier 3+ creative problems | Brain needs offline processing |
| **Stopping criteria** | Tier 4 | Wicked problems can trap you forever |
| **Handoff protocol** | Tier 3+ OR organizational | Others need to maintain your work |
| **Multi-frame protocol** | Tier 4 wicked | Problem definition itself is contested |

---

## Special Protocols (Overlay on Any Tier)

### FAST-TRACK (Crisis/Time Pressure)
**When**: <15 minutes available, decision required NOW

**Steps**: Critical path only
1. CLASSIFY (1 min)
2. STATE (1 min)
3. Stakeholder red-lines (2 min)
4. GENERATE 2-3 (3 min)
5. Rapid red-team (3 min)
6. SELECT (1 min)
7. EXECUTE (now)
8. VERIFY (later)

**Note**: You're trading rigor for speed. Document decision, plan to revisit.

---

### ADVERSARIAL (Bad Actors Expected)
**When**: Trust is low, sabotage possible, incentives misaligned

**Add to any tier**:
- Incentive check: Who benefits?
- Sabotage assumption test: Where would they lie?
- External verification: Don't trust single source
- Contingency trigger: What forces pivot?

---

### FORMATION (Requires Becoming Different)
**When**: Solving requires you to change

**Add to any tier**:
- What needs to form in me to solve this?
- What gaps does this expose in who I am?
- Formation and problem-solving are simultaneous

---

## Usage Guide

### How to Use This System

**Step 1**: Read the problem

**Step 2**: Run the decision tree → Get a tier

**Step 3**: Apply that tier's steps (no more, no less)

**Step 4**: If you hit an upgrade trigger → move to higher tier

**Step 5**: If problem resolves early → stop (don't finish all steps)

---

### Example: Tier Selection in Practice

**Problem**: "Our CI/CD pipeline is failing intermittently. Should we fix it or rebuild it?"

**Decision tree**:
- Q1: Clear solution? NO (fix vs rebuild unclear)
- Q2: Stakeholders? 2 (eng team + product) - aligned
- Q3: Stakes? Medium (reversible, but costly downtime)
- Q4: Well-defined? Yes (everyone agrees pipeline is the problem)
- Q5: Time? Hours available
- **→ TIER 2**

**Problem**: "Should we pivot our entire business model?"

**Decision tree**:
- Q1: Clear solution? NO
- Q2: Stakeholders? 5+ (board, investors, employees, customers, partners) - conflicts likely
- Q3: Stakes? Existential
- Q4: Well-defined? NO (stakeholders may disagree on what problem is)
- Q5: Time? Weeks
- **→ TIER 4**

---

## Validation Metrics

### How to Know You're Using the Right Tier

**Too low (underbuilt)**:
- Solution fails in deployment
- Stakeholders blindsided
- Obvious failure modes missed
- Need to redo with more rigor

**Too high (overbuilt)**:
- Spent 2 hours on a 10-minute problem
- Analysis paralysis
- Stakeholders frustrated by delay
- Diminishing returns on additional analysis

**Just right**:
- Solution works first time OR
- Failures were genuinely unpredictable (not just unanalyzed)
- Time investment proportional to stakes
- Confidence matches rigor applied

---

## Comparison: Old vs New

### Before (30+ steps, no tiers):
- Every problem gets full treatment
- Simple problems take 60+ minutes
- Can't finish (too exhausting)
- OR skip steps (inconsistent quality)

### After (tiered system):
- Simple problems: 5 minutes, Tier 1
- Moderate problems: 20 minutes, Tier 2
- Complex problems: 60 minutes, Tier 3
- Wicked problems: Multiple sessions, Tier 4
- **Quality matches stakes**
- **Usable in practice**

---

## Tier Distribution in Practice

Expected usage:
- **Tier 1**: 60% of problems (most problems are actually simple)
- **Tier 2**: 30% of problems (some complexity)
- **Tier 3**: 8% of problems (high stakes justify rigor)
- **Tier 4**: 2% of problems (rare but critical)

**The 84 cycles taught us how to solve Tier 4 problems. But most problems aren't Tier 4.**

---

## Integration with Existing Frameworks

### How this relates to other methodologies:

| Framework | Maps to Tier |
|-----------|--------------|
| **OODA Loop** (Boyd) | Tier 1-2 (speed of cycling) |
| **First Principles** (Musk) | Tier 3-4 (deep analysis) |
| **Pólya's Heuristics** | Tier 2-3 (structured problem-solving) |
| **TRIZ** | Tier 3 (contradiction resolution) |
| **Cynefin** | Tier selector (classification informs tier) |
| **Design Thinking** | Tier 3-4 (prototype for novel problems) |
| **Systems Thinking** | Tier 3-4 (complex/adaptive systems) |

**Don't stack frameworks - tier selection IS the framework selector.**

---

## Quick Reference Card

### Tier Selection (30-Second Version)

```
SIMPLE + LOW STAKES + CLEAR → TIER 1 (5 min)
MODERATE + SOME STAKES + MOSTLY CLEAR → TIER 2 (20 min)
COMPLEX + HIGH STAKES + POLITICAL → TIER 3 (60 min)
ILL-DEFINED + TRANSFORMATIONAL + WICKED → TIER 4 (ongoing)
```

### Tier 1 Checklist
- [ ] Problem stated
- [ ] 2-3 solutions
- [ ] Pick one
- [ ] Verify

### Tier 2 Checklist
- [ ] Domain classified
- [ ] Problem stated
- [ ] Constraints listed
- [ ] Stakeholders checked
- [ ] 3+ approaches generated
- [ ] Criteria defined + weighted
- [ ] Red-team failures
- [ ] Single recommendation
- [ ] Verified
- [ ] Implementation plan

### Tier 3 Checklist
- [ ] Meta-frame audit
- [ ] All of Tier 2
- [ ] Frame verification
- [ ] Unknown unknowns discovered
- [ ] Stakeholder red-lines
- [ ] Frame adequacy check
- [ ] Frame probe
- [ ] Deployment probe
- [ ] Handoff protocol

### Tier 4 Indicators
- [ ] Stakeholders disagree on what problem IS
- [ ] Solving requires becoming different
- [ ] No clear end state
- [ ] Political/cultural/transformational
- [ ] Solution changes the problem space

---

## Meta-Learning: What the 84 Cycles Taught Us

### The Recursive Trap
Each cycle fixed a weakness. But weaknesses are infinite. Without a STOPPING RULE, you get:
- Cycle 1-10: Fix obvious gaps → valuable
- Cycle 11-40: Fix edge cases → still valuable
- Cycle 41-70: Fix rare failures → diminishing returns
- Cycle 71-84: Fix hypothetical weaknesses → over-engineered

### The Stopping Rule We Didn't Have
**Should have stopped when**: New weaknesses only appear in Tier 3-4 problems, but we're applying to ALL problems.

**The fix**: TIER the methodology. Accumulate learnings, but GATE them by problem type.

### The Key Insight
**Rigor is not binary. It's a dial that should match stakes.**

The 84 cycles were valuable - they discovered EVERYTHING you might need. But you don't need everything every time.

---

## Maintenance Protocol

### When to Add a New Step
1. Identify weakness in MULTIPLE problems (not just one)
2. Determine which TIER it belongs in
3. Add ONLY to that tier and above
4. Validate it helps (not just plausible)

### When to Remove a Step
1. Step hasn't caught anything in 20 problems
2. OR always redundant with another step
3. Remove from lower tiers first
4. Keep in Tier 4 (rarely hurts to be thorough)

### How to Evolve Tiers
- Tier 1 should stay minimal (resist additions)
- Tier 2 can grow moderately
- Tier 3 can grow substantially
- Tier 4 is the "everything" tier (catches all learnings)

**The discipline**: New learnings go to higher tiers first. Only move down if BROADLY applicable.

---

## Worked Example: Applying the Tiered System

### Problem: "Our API response times are slow"

**Tier selection**:
- Clear solution? NO (many possible causes)
- Stakeholders? 2 (eng + product)
- Stakes? Medium (customer experience, but not breaking)
- Well-defined? YES (everyone agrees response time is the issue)
- Time? 30 min available
- **→ TIER 2**

**Tier 2 execution**:

1. **CLASSIFY DOMAIN**: Complicated (cause-effect knowable via analysis)

2. **STATE**: API response times exceed 500ms at p95, should be <200ms

3. **LIST CONSTRAINTS**:
   - Must maintain backward compatibility
   - Can't add significant infrastructure cost
   - Need solution deployed within 2 weeks

4. **STAKEHOLDER CHECK**:
   - Product: Wants fast responses, will accept some feature delay
   - Customers: Don't care how, just want speed

5. **GENERATE 3+ APPROACHES**:
   - A: Caching layer (Redis)
   - B: Database query optimization
   - C: Async processing for heavy operations
   - D: CDN for static assets

6. **EVALUATE**:
   Criteria (weighted):
   - Speed to implement (30%)
   - Impact on response time (40%)
   - Cost (20%)
   - Maintainability (10%)

   | Option | Speed | Impact | Cost | Maintain | Total |
   |--------|-------|--------|------|----------|-------|
   | A: Cache | 8 | 9 | 6 | 7 | 7.7 |
   | B: Query opt | 9 | 7 | 10 | 8 | 8.3 |
   | C: Async | 4 | 8 | 8 | 6 | 6.6 |
   | D: CDN | 7 | 5 | 7 | 9 | 6.7 |

7. **RED-TEAM B (Query optimization)**:
   - Failure: What if queries aren't the bottleneck? → Profile first to confirm
   - Failure: What if optimization is complex? → Set 1-week timebox

8. **SELECT**: Query optimization (B), contingent on profiling confirming this is the bottleneck. If not, pivot to caching (A).

9. **VERIFY**: Profile shows 70% of time in 3 specific queries → confirms approach

10. **DESIGN**:
    - Week 1: Profile + optimize top 3 queries + add monitoring
    - Week 2: Deploy to staging, validate <200ms, deploy to prod
    - Rollback: Keep old queries, feature flag new ones

**Time spent**: 22 minutes
**Output**: Clear plan, validated assumptions, ready to implement

**If this was Tier 1**: Would have missed profiling → might optimize wrong thing
**If this was Tier 3**: Would have spent 60 min on red-lines, deployment probes → overkill for this

---

## Summary: The Tiered Methodology

### The Problem
84 cycles of improvement created a 30-step process. Unusable for most problems.

### The Solution
Four tiers (Quick/Standard/Rigorous/Wicked) based on complexity, stakes, and clarity.

### The Discipline
- Match rigor to stakes
- Start at lowest tier
- Upgrade if needed
- Stop when problem resolves

### The Payoff
- Simple problems: 5 minutes (was 60+)
- Complex problems: Still get full rigor
- Quality matches stakes
- **Methodology is actually usable**

### The Meta-Lesson
**Recursive improvement without tier-based stopping rules leads to over-engineering.**

Improvement cycles are valuable. But learnings should be GATED by problem type, not applied uniformly.

**Mantra**: "Not every problem needs every tool. Match the rigor to the stakes."
