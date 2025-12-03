# Collatz Proof: Quick Reference Card

## The Core Equation
```
Any cycle with m odd numbers satisfies:  N = S / D

where:
  D = 2^A - 3^m
  S = Σ_{j=0}^{m-1} 3^{m-1-j} · 2^{prefix_j}
  A = sum of δ_j (total even steps)
```

## The Constant Path
```
δ = (2, 2, ..., 2)  →  A = 2m
prefix_j = 2j
S = Σ 3^{m-1-j} · 4^j = 4^m - 3^m = D
k = S/D = 1  (trivial cycle)
```

## Tight Prime Lemma
```
If p | D and ord_p(2) ≥ 2m:
  → All 2^0, 2^1, ..., 2^{2m-1} distinct mod p
  → S ≡ 0 (mod p) ONLY for constant path
  → D | S implies k = 1
```

## Even Order Criterion ⭐
```
For primitive prime p | (4^m - 3^m):
  ord_p(4) ≥ m  (since ord_p(4/3) = m)
  
If ord_p(2) is EVEN:
  ord_p(4) = ord_p(2) / 2
  ord_p(2) = 2 · ord_p(4) ≥ 2m  ✓ TIGHT!
```

## The Gap
```
NEED TO PROVE:
  ∀m ≥ 3 (m ≠ 4), ∃ prime p | (4^m - 3^m) with ord_p(2) ≥ 2m

EQUIVALENTLY:
  ∀m ≥ 3 (m ≠ 4), some primitive prime has EVEN ord_p(2)
```

## Key Primes
```
p = 37  (d=3):  ord = 36, covers m ≤ 18 with 3|m
p = 71  (d=5):  ord = 35, covers m ≤ 17 with 5|m  
p = 181 (d=10): ord = 180, covers m ≤ 90 with 10|m
```

## Proof Status
```
✓ Framework (N = S/D)
✓ Tight Prime Lemma
✓ m = 2, 4 (direct check)
✓ m ≤ 200 (verified)
⚠ All m (gap: tight prime existence)
```
