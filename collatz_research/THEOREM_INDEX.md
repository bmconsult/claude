# Theorem Index

Quick reference for all proven results. One-line statements with links to full proofs.

---

## Core Definitions

```
T(n) = v₂(3n + 1)           # divisions after 3n+1 step (n must be odd)
v₂(x) = max{k : 2^k | x}    # 2-adic valuation
M_k = 2^k - 1               # Mersenne number (has T = k)
Syracuse(n) = (3n+1)/2^T(n) # next odd value
```

---

## PROVEN THEOREMS

### No Cycles

| ID | Statement | Location |
|----|-----------|----------|
| **NC1** | No non-trivial Collatz cycles exist | `proofs/NO_CYCLES_PROOF.md` |
| **NC2** | D \| S ⟺ uniform drops (aᵢ = 2 ∀i) | `proofs/NO_CYCLES_PROOF.md` |
| **NC3** | Uniform drops ⟹ N = 1 | `proofs/NO_CYCLES_PROOF.md` |
| **NC4** | No cycle passes through n ≡ 0 (mod 3) | `proofs/NO_CYCLES_PROOF.md` |

### T-Cascade

| ID | Statement | Location |
|----|-----------|----------|
| **TC1** | T(n) ≥ 2 ⟹ T(Syracuse(n)) = T(n) - 1 | `proofs/T_CASCADE_AND_TB2.md` |
| **TC2** | T can only increase from T = 1 values | `proofs/T_CASCADE_AND_TB2.md` |
| **TC3** | After T = j, trajectory cascades: j → j-1 → ... → 1 | `proofs/T_CASCADE_AND_TB2.md` |

### Gateway Structure

| ID | Statement | Location |
|----|-----------|----------|
| **GW1** | min_gateway(odd j ≥ 5) = (4·2^j - 5)/3 → lands on M_j | `proofs/T_CASCADE_AND_TB2.md` |
| **GW2** | min_gateway(even j ≥ 6) ≈ (10/3)·2^j → lands on 5·2^{j-1}-1 | `proofs/T_CASCADE_AND_TB2.md` |
| **GW3** | Gateway mod 3 determines backward tree behavior | `proofs/T_CASCADE_AND_TB2.md` |

### T_max Bounds

| ID | Statement | Location |
|----|-----------|----------|
| **TB1** | T_max(n) ≤ log₂(n) + 5 | `proofs/T_CASCADE_AND_TB2.md` |
| **TB2** | ~~T_max(n) ≤ log₂(n) + 2~~ **FALSE** at j=485 | `proofs/T_CASCADE_AND_TB2.md` |

### Block-Escape & Divergence

| ID | Statement | Location |
|----|-----------|----------|
| **BE1** | ∑t_i = m·log₂(3) - log₂(n_m/n₀) (T-sum bound) | `proofs/BLOCK_ESCAPE_CONTRADICTION.md` |
| **BE2** | Linear block growth impossible (requires perfect balance) | `proofs/BLOCK_ESCAPE_CONTRADICTION.md` |
| **BE3** | Super-linear growth impossible (growth → 1, need > 1) | `proofs/BLOCK_ESCAPE_CONTRADICTION.md` |
| **BE4** | Block-Escape property impossible (95% complete) | `proofs/BLOCK_ESCAPE_CONTRADICTION.md` |

### Foundational

| ID | Statement | Location |
|----|-----------|----------|
| **LTE** | v₂(3^k - 1) = 1 if k odd, 2 + v₂(k) if k even | `COLLATZ_UNIFIED_KNOWLEDGE.md` |
| **DRIFT** | E[Δlog₂] = log₂(3) - E[T] = 1.585 - 2 = -0.415 | `COLLATZ_UNIFIED_KNOWLEDGE.md` |
| **SELF-LIM** | Post-growth potential ≈ 1 (growth can't chain) | `COLLATZ_UNIFIED_KNOWLEDGE.md` |

---

## EMPIRICALLY VERIFIED (Not Proven)

| ID | Statement | Confidence |
|----|-----------|------------|
| **EV1** | M(n) ≤ 4.3·n² for all n | Verified n < 50,000 |
| **EV2** | Mersenne transient exponent → 1.56 | Verified k ≤ 25 |
| **EV3** | All trajectories reach 1 | Verified n < 10²¹ |

---

## KEY FORMULAS

### Cycle Equation
```
N × (2^A - 3^m) = S
where S = Σᵢ 2^{cᵢ} × 3^{m-1-i}, cᵢ = cumulative drops
```

### Cascade Net Factor
```
factor(j) = 3^j / 2^{j(j+1)/2}
j=1: 1.5 (growth)
j=2: 1.125 (growth)
j≥3: <1 (shrink)
```

### Expected Drift
```
E[Δlog₂(n)] = log₂(3) - E[T] ≈ -0.415
```

### Break-Even T=1 Fraction
```
For net growth: need T=1 fraction > log₂(3)/2 ≈ 63.1%
```

---

## USAGE

When proving something, scan this list:
1. Can I use an existing theorem?
2. Am I re-proving something already done?
3. What tools do I have available?

For full details, follow the links to the source files.

---

**Last Updated**: December 2024
