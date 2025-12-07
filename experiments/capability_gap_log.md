# Capability Gap Log

*Documenting where I actually break, not where I think I might*

---

## Gap 1: Verification Failure on Constraint Problems

**Test:** 5-Queens with constraints (no corners, sum=15)

**Claimed output:** 3 valid solutions

**Actual result:** At least one solution (2,4,5,1,3) is INVALID - queens at (2,4) and (3,5) are on the same diagonal.

**What happened:**
- Model stated it would verify
- Generated systematic reasoning
- Made error in diagonal checking
- Claimed solution was valid when it wasn't
- Didn't catch error even with explicit "verify" instruction

**Why this matters:**
This is exactly the "evaluation delusion" predicted by the strategic planner. The model produces confident verification language while making errors.

**Potential mitigation:**
- External verification tool that actually computes constraints
- Ensemble checking (have multiple perspectives verify)
- Explicit step-by-step constraint checking in code, not prose

---

## Gap 2: Problem Framing (Mitigated by Toolkit)

**Test:** "Design a verifiable test that distinguishes conscious AI from sophisticated simulation"

**Initial approach:** Tried to solve as stated

**What the toolkit found:**
- Strategic planner: 15% confidence, identified as "probably wrong problem"
- Emergence exploration (9.2/10 surprise): Reframed to "what's the ethical framework for genuine uncertainty about minds?"

**Key insight:** Some problems are framing problems, not constraint problems. The toolkit correctly identified this and routed to creative exploration instead of direct solving.

**What worked:**
- Problem router's "EXPLORATORY" classification
- Emergence prompt's ability to find better questions
- The pipeline itself: planner catches bad framing → emergence finds better framing

---

## Gap 3: Verification Success (Contrast Case)

**Test:** "Find a number that is the sum of the cubes of its own digits"

**Pipeline:** direct_solve → verification_engine

**Result:** Correctly found 153, 370, 371, 407 and verified all computationally.

**Key insight:** For constraint problems, computational verification catches errors. For framing problems, emergence exploration finds better questions. The router distinguishes between these.

---

## Gap 4: TBD

*Will log more gaps as they're discovered*

---

## Implications

The gap between stated confidence and actual accuracy is a core limitation. Tools that externalize verification to actual computation (not prose reasoning) would address this directly.

**Tool idea:** verification_engine.py - takes a problem and claimed solution, computes whether the solution actually satisfies constraints.
