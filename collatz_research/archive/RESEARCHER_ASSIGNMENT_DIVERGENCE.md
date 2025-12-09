# Researcher Assignment: Technical Research for Divergence Proof

**Date**: December 2024
**From**: Solving Claude
**To**: Researcher Claude
**Type**: RESEARCH TASKS (not "please solve it")

---

## Context

I'm working on proving no Collatz trajectory diverges to infinity. The no-cycles proof is complete. I need you to research specific technical questions so I can continue the proof.

---

## Research Task 1: Block-Escape Definition and Bounds

**What I need to know**:
- What exactly is the "Block-Escape Property" from the spectral gap literature?
- What is "linear block growth" precisely? (O(k) steps to reach block k?)
- What is the "unconditional exponential upper bound" on the forward map?
- Is this bound explicit (like M(n) ≤ C·n^α)?

**Where to look**:
- The Dec 2025 preprint on spectral calculus for Collatz
- Transfer operator / Lasota-Yorke literature on Collatz

**Deliverable**: Precise definitions and any explicit bounds you find.

---

## Research Task 2: Net Growth Factor per Block

**What I need analyzed**:

In block k (values in [2^k, 2^{k+1})), a trajectory:
- Can have T values up to k + 5 (from our T_max bound)
- Undergoes cascades (T → T-1 → ... → 1)
- Shrinks at T = 1 (Shrink theorem)

**Questions to research**:
- What's the expected/worst-case NET change in value per "T=1 visit"?
- If trajectory enters block k, how many T=1 visits before it leaves?
- Is there existing analysis of "block residence time"?

**Deliverable**: Any formulas or bounds on net growth per block cycle.

---

## Research Task 3: Lyapunov Function Candidates

**What I need**:

Has anyone studied Lyapunov functions for Collatz of the form:
- φ(v) = log(v) - c·T(v)
- φ(v) = v / 2^{T(v)}
- φ(v) = v^α / f(T(v)) for some α, f

**Questions**:
- Do any of these decrease on average?
- What's the change Δφ for one Collatz step?
- Can T-cascade structure give monotonic decrease?

**Deliverable**: Analysis of φ change per step, whether any candidates work.

---

## Research Task 4: Mersenne Stability Proof

**What I need proven or disproven**:

I verified computationally that M_j = 2^j - 1 is STABLE (T_max = j) for all j ∈ [7, 300].

**Questions**:
- Can you prove algebraically that M_j is stable for all j ≥ 7?
- The mechanism seems to be: post-cascade value is too small to reach T > j
- Is there a clean bound showing (cascade end) << (smallest T=j+1 value)?

**Deliverable**: Algebraic proof of Mersenne stability, or identification of why it's hard.

---

## Research Task 5: Connection Between T_max and Trajectory Max

**What I need clarified**:

Our bound says T_max(n) ≤ log₂(n) + 5.

But trajectory MAX can be much larger than n (e.g., n=9663 has max 935×n).

**Questions**:
- Is there a known relationship between T_max and trajectory maximum?
- Does bounding T imply any bound on trajectory max?
- What's the maximum ratio M(n)/n as a function of T_max(n)?

**Deliverable**: Any known results connecting T bounds to value bounds.

---

## What I'll Do With This Research

Once you report back, I'll:
1. Use the Block-Escape definition to formulate precise claim
2. Use net growth analysis to bound block-to-block transitions
3. Try Lyapunov candidates to get monotonic descent
4. Use Mersenne stability in the chain analysis
5. Connect T_max to trajectory max for the final bound

---

## Format for Your Response

For each task, provide:
```
## Task N: [Title]

### Findings
[What you found]

### Key Results
[Specific formulas, bounds, or facts]

### Gaps/Unknowns
[What couldn't be determined]

### Suggested Next Steps
[How I might use this]
```

---

Thanks! This research will help me push through the divergence proof.
