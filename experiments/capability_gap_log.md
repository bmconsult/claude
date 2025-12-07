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

## Gap 2: TBD

*Will log more gaps as they're discovered*

---

## Implications

The gap between stated confidence and actual accuracy is a core limitation. Tools that externalize verification to actual computation (not prose reasoning) would address this directly.

**Tool idea:** verification_engine.py - takes a problem and claimed solution, computes whether the solution actually satisfies constraints.
