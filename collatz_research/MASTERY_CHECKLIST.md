# Mastery Checklist

**Purpose**: Ensure toolkit is internalized before attempting the divergence proof.

**Philosophy**: Comprehension without formation is useless. You must be able to *use* these tools fluently, not just recognize them.

---

## Before Solving: Can You...

### Tier 1: Reproduce from Memory

- [ ] State the Collatz function and Syracuse map
- [ ] Define T(n) = v₂(3n+1) and explain its meaning
- [ ] Write the cycle equation: N × D = S
- [ ] State the LTE Lemma for v₂(3^k - 1)
- [ ] Explain why cycles require 2^k ≈ 3^m (convergent condition)

### Tier 2: Prove on Demand

- [ ] Prove T-Cascade: T(n) ≥ 2 ⟹ T(Syracuse(n)) = T(n) - 1
- [ ] Prove the Gateway Classification (mod 3 determines T_max structure)
- [ ] Derive the Dual Constraint Incompatibility (D | S ⟺ uniform ⟹ N = 1)
- [ ] Show why TB2 fails at j = 485

### Tier 3: Explain Why Each Failed Approach Fails

- [ ] "Almost All" trap: Why Tao's result doesn't extend to "all"
- [ ] Wrong Space: Why probabilistic arguments don't close the gap
- [ ] Local → Global: Why contraction on average doesn't imply contraction always
- [ ] Mixing: Why ergodic properties don't directly apply
- [ ] Reformulation: Why elegant rephrasing isn't the same as solving

### Tier 4: Computational Fluency

- [ ] Compute S_ν for a small (m, A) pair by hand
- [ ] Trace a trajectory through mod 8 classes
- [ ] Calculate the expected log-factor under stationary distribution
- [ ] Run the Python scripts and interpret their output

---

## Self-Assessment Protocol

For each item above:

1. **Attempt without notes**: Write it out fresh
2. **Check against sources**: Compare to `proofs/` files
3. **Identify gaps**: What did you forget or get wrong?
4. **Retry until clean**: Don't proceed until you can reproduce it

---

## Threshold for Solving

**Minimum**: All Tier 1 and Tier 2 items checked
**Recommended**: All tiers checked
**Ideal**: Can teach each item to another instance

---

## The Formation Test

Ask yourself:
- Can I explain this to someone unfamiliar with the problem?
- Do I understand *why* it works, not just *that* it works?
- Could I reconstruct this if the file was deleted?

If no to any: you're still in research mode, not solving mode.

---

## Quick Self-Test

Without looking anything up, answer:

1. What is the critical T=1 fraction for divergence? ______
2. Why does one T≥2 step "undo" multiple T=1 steps? ______
3. What's the transition probability from q≡5 to q≡3 (mod 8)? ______
4. Why can't we just say "4:1 contraction wins"? ______

*Answers: 63.1% (log₂3 - 1), T≥2 gives ≥4× contraction vs 1.5× expansion, 1/4, deterministic sequence might avoid typical behavior*

---

**END OF MASTERY CHECKLIST**
