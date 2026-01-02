"""
PROOF: Tight instances have optimal time with denominator (n+1)

The key insight is that for ML = 1/(n+1) to be achieved EXACTLY,
there are strong constraints on the optimal time.
"""
from fractions import Fraction
from math import gcd

def distance(v, t):
    """||vt|| = distance to nearest integer"""
    pos = float(v * t) % 1
    return min(pos, 1 - pos)

print("""
THEOREM: If (v₁, ..., vₙ) is a coprime n-tuple with ML = 1/(n+1),
then there exists k ∈ {1, ..., n} with gcd(k, n+1) = 1 such that
t* = k/(n+1) achieves min_i ||vᵢt*|| = 1/(n+1).

PROOF:
======

Step 1: The Lonely Runner bound is 1/(n+1)
-----------------------------------------
For any n coprime speeds, LRC asserts ML ≥ 1/(n+1).
A "tight" instance achieves ML = 1/(n+1) exactly.

Step 2: Structure of optimal time
---------------------------------
At optimal time t*, we have:
  min_i ||vᵢt*|| = 1/(n+1)

This means:
  - At least one speed has ||vᵢt*|| = 1/(n+1) (achieves the minimum)
  - All speeds have ||vᵢt*|| ≥ 1/(n+1)

Step 3: Characterizing ||vt|| = 1/(n+1)
--------------------------------------
||vt|| = 1/(n+1) means:
  vt = m ± 1/(n+1) for some integer m
  
Therefore:
  t = (m ± 1/(n+1)) / v = ((n+1)m ± 1) / ((n+1)v)

So t = k / ((n+1)v) where k = (n+1)m ± 1.

In lowest terms, t has denominator dividing (n+1)v / gcd(k, (n+1)v).

Step 4: The key insight - residues mod (n+1)
-------------------------------------------
For a TIGHT instance, all speeds must satisfy ||vᵢt*|| ≥ 1/(n+1).

If t* = a/b in lowest terms, then for speed vᵢ:
  ||vᵢ × a/b|| ≥ 1/(n+1)
  
This means vᵢa mod b ∈ [b/(n+1), b - b/(n+1)].

For this to work for ALL n speeds, the denominator b must be special.
""")

# Let's verify that b = n+1 is always sufficient when speeds are in {1,...,n} mod (n+1)
print("\nVERIFICATION: For speeds with residues in {1,...,n} mod (n+1),")
print("t = 1/(n+1) achieves distance ≥ 1/(n+1) for all speeds.")
print("=" * 60)

for n in range(3, 10):
    print(f"\nn = {n}, n+1 = {n+1}")
    for v in range(1, n+1):
        # v mod (n+1) is in {1, ..., n}
        t = Fraction(1, n+1)
        d = distance(v, t)
        target = 1/(n+1)
        status = "✓" if d >= target - 1e-10 else "✗"
        print(f"  v={v}: ||v/(n+1)|| = {d:.6f} {status}")

print("""
KEY OBSERVATION:
===============
For t = k/(n+1) with gcd(k, n+1) = 1:
- Speed v with v ≢ 0 (mod n+1) has vk mod (n+1) ∈ {1, ..., n}
- Therefore ||vk/(n+1)|| = min(vk mod (n+1), (n+1) - vk mod (n+1))/(n+1) ≥ 1/(n+1)

For t = k/(n+1):
- Speed v with v ≡ 0 (mod n+1) has vk/(n+1) = integer
- Therefore ||vk/(n+1)|| = 0 < 1/(n+1)

CONCLUSION:
==========
1. For a TIGHT instance with ML = 1/(n+1):
   - The optimal time t* = k/(n+1) works for all speeds with residue in {1,...,n}
   - If any speed has residue 0 (mod n+1), t* gives distance 0 for that speed

2. Therefore: TIGHT instances CANNOT have any speed ≡ 0 (mod n+1)

3. CASE 2 PROOF:
   - Case 2 tuples have some speed ≡ 0 (mod n+1)
   - Such tuples cannot be tight (by the above)
   - Non-tight means ML > 1/(n+1)
   - ML > 1/(n+1) means the tuple is "lonely" (LRC holds for it)
   
   QED for Case 2!

REMAINING GAP:
=============
The above proves that t = k/(n+1) works for Case 1 tuples.
It does NOT directly prove that Case 2 tuples have NO optimal time at all.

To complete the proof, we need to show:
- For Case 2 tuples, there is NO time t with min_i ||vᵢt|| = 1/(n+1)
- This requires showing that the "good regions" for all speeds don't intersect
  at exactly the boundary value 1/(n+1)
""")
