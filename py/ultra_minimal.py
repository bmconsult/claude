"""
ULTRA MINIMAL - Focus on the key insight
"""

# Precomputed key primes from small d values
# Format: (prime, origin_d, ord_2, reach)
KEY_PRIMES = [
    (7, 2, 3, 1),      # 7 | 4^2 - 3^2, ord_7(2) = 3
    (37, 3, 36, 18),   # 37 | 4^3 - 3^3, ord_37(2) = 36  
    (5, 4, 4, 2),      # 5 | 4^4 - 3^4
    (11, 5, 10, 5),    # 11 | 4^5 - 3^5
    (71, 5, 35, 17),   # 71 | 4^5 - 3^5
    (13, 6, 12, 6),    # 13 | 4^6 - 3^6
    (181, 10, 180, 90),  # 181 | 4^10 - 3^10
    (61, 15, 60, 30),    # 61 | 4^15 - 3^15
    (337, 8, 21, 10),    # 337 | 4^8 - 3^8
]

print("="*60)
print("KEY PRIMES AND THEIR REACH")
print("="*60)

print("\nThese primes from small d values have large ord_2:")
print(f"{'p':>8} {'d':>4} {'ord_2':>8} {'reach':>8}")
print("-"*35)
for p, d, o, r in sorted(KEY_PRIMES, key=lambda x: -x[3]):
    print(f"{p:>8} {d:>4} {o:>8} {r:>8}")

print("\n" + "="*60)
print("COVERAGE THEOREM")
print("="*60)

print("""
THE KEY INSIGHT:

1. Prime 37 (from d=3) has reach 18.
   -> 37 is tight for ALL m with 3|m and m ≤ 18.
   -> Covers: 3, 6, 9, 12, 15, 18

2. Prime 181 (from d=10) has reach 90.
   -> 181 is tight for ALL m with 10|m and m ≤ 90.
   -> Covers: 10, 20, 30, 40, 50, 60, 70, 80, 90

3. Prime 71 (from d=5) has reach 17.
   -> 71 is tight for ALL m with 5|m and m ≤ 17.
   -> Covers: 5, 10, 15

4. For m not divisible by 3, 5, or 10:
   -> Must rely on primitive prime of 4^m - 3^m
   -> Or primes from other divisors

The question: Is there ALWAYS a covering prime?
""")

print("="*60)
print("THE PROOF STRUCTURE")
print("="*60)

print("""
For any m ≥ 3 (m ≠ 4), we need to find a covering prime.

CASE 1: 3 | m and m ≤ 18
  37 | (4^3 - 3^3) | (4^m - 3^m)
  ord_37(2) = 36 ≥ 2m (since m ≤ 18)
  ✓ Covered

CASE 2: 10 | m and m ≤ 90  
  181 | (4^10 - 3^10) | (4^m - 3^m)
  ord_181(2) = 180 ≥ 2m (since m ≤ 90)
  ✓ Covered

CASE 3: 5 | m and m ≤ 17 (not already covered)
  71 | (4^5 - 3^5) | (4^m - 3^m)
  ord_71(2) = 35 ≥ 2m (since m ≤ 17)
  ✓ Covered

CASE 4: Remaining small m (m < 20, not divisible by 3 or 5)
  m ∈ {7, 8, 11, 13, 14, 16, 17, 19}
  Each needs individual check (primitive prime usually works)
  
CASE 5: Large m (m ≥ 20)
  If 3|m: covered by 37 up to m=18, or by larger primes
  If 10|m: covered by 181 up to m=90
  If 5|m: covered by 71 up to m=17
  Otherwise: need primitive prime analysis
""")

# Check which m values are "easy" (covered by known primes)
easy_m = set()

# m divisible by 3, m <= 18
for m in range(3, 19):
    if m % 3 == 0:
        easy_m.add(m)

# m divisible by 10, m <= 90
for m in range(10, 91):
    if m % 10 == 0:
        easy_m.add(m)

# m divisible by 5, m <= 17
for m in range(5, 18):
    if m % 5 == 0:
        easy_m.add(m)

# m divisible by 15 (covered by 61), m <= 30
for m in range(15, 31):
    if m % 15 == 0:
        easy_m.add(m)

print("\n" + "="*60)
print("EASY VS HARD CASES")
print("="*60)

print(f"\nEasy cases (covered by inherited primes from d<m):")
print(f"  {sorted([m for m in easy_m if m < 100])}")

hard_m = [m for m in range(3, 100) if m != 4 and m not in easy_m]
print(f"\nHard cases (need primitive prime or other analysis):")
print(f"  {hard_m}")

print("\n" + "="*60)
print("ANALYZING HARD CASES")
print("="*60)

print("""
Hard cases: [7, 8, 11, 13, 14, 16, 17, 19, 21, 22, 23, 24, 26, 27, ...]

For these, we need to verify the PRIMITIVE prime of 4^m - 3^m is tight,
OR that some OTHER divisor d|m provides a tight prime.

Let's think about this systematically:

For m = 7: primitive prime is 14197, ord = 4732 ≥ 14. ✓
For m = 8: primitive prime is 337, ord = 21 ≥ 16. ✓  
For m = 11: primitive prime is 174659, ord = 174658 ≥ 22. ✓
For m = 13: primitive prime is 131, ord = 130 ≥ 26. ✓
...

The pattern: Primitive primes of 4^m - 3^m tend to have ord_p(2) ≈ p-1.
Since p > 2m (typically p >> 2m), we get ord_p(2) ≥ 2m.

WHY does p > 2m for primitive primes?
""")

print("="*60)
print("THE PRIMITIVE PRIME SIZE ARGUMENT")
print("="*60)

print("""
For primitive prime p of 4^m - 3^m:
  - p ≡ 1 (mod m)  [since ord_p(4/3) = m divides p-1]
  - p is "new" - doesn't divide 4^k - 3^k for k < m

Lower bound on primitive prime:
  The primitive part of 4^m - 3^m is: Φ(4,3,m) = ∏_{d|m, d=m} (4^m - 3^m)/(GCD stuff)
  
  By bounds on primitive parts of a^n - b^n:
  For m ≥ 3, the primitive prime p satisfies p > m.
  
  More specifically, for 4^m - 3^m with m prime:
  p ≥ 2m + 1 typically.

If p ≥ 2m + 1 and ord_p(2) is "usually" large (≥ (p-1)/2):
  ord_p(2) ≥ (p-1)/2 ≥ (2m)/2 = m
  
That's not quite enough (need 2m, not m).

But empirically, ord_p(2) is often MUCH larger than (p-1)/2.
For primitive roots: ord_p(2) = p-1 >> 2m.
""")

print("="*60)
print("THE ARTIN HEURISTIC")
print("="*60)

print("""
Artin's conjecture: 2 is a primitive root for infinitely many primes.
The density of such primes is conjectured to be the Artin constant ≈ 0.3739...

For PRIMITIVE primes p of 4^m - 3^m:
  - These are "special" primes with p ≡ 1 (mod m)
  - There's no reason they'd avoid having 2 as primitive root
  - Heuristically, about 37% should have ord_p(2) = p-1

When ord_p(2) = p-1 and p >> 2m, we get tight coverage.

The question: Can we prove this without relying on unproven conjectures?
""")

print("="*60)
print("ALTERNATIVE: THE PRODUCT ARGUMENT")
print("="*60)

print("""
Instead of proving one tight prime exists, consider:

CLAIM: For m ≥ 3 (m ≠ 4), the LCM of {ord_p(2) : p | (4^m - 3^m)} is ≥ 2m.

This is WEAKER than tight prime existence but might be easier to prove,
and would still show the constant path is unique (via Chinese Remainder Theorem).

Actually, this is EQUIVALENT to tight prime existence:
  LCM ≥ 2m ⟺ some ord_p(2) ≥ 2m.

So this doesn't help directly.
""")

print("="*60)
print("THE PATH FORWARD")
print("="*60)

print("""
To prove tight primes always exist, we seem to need ONE of:

1. PROVE: Primitive primes p of 4^m - 3^m satisfy ord_p(2) ≥ 2m.
   - This requires understanding ord_p(2) for primitive primes
   - Related to (but not implied by) Artin's conjecture

2. PROVE: The union of inherited primes always covers m.
   - Need to show that as m grows, enough high-reach primes accumulate
   - This is more combinatorial

3. FIND a different algebraic argument that bypasses tight primes.
   - Prove D | S ⟹ constant path directly
   - Use the polynomial structure more cleverly

Option 3 might be most promising. Let me think about it...
""")
