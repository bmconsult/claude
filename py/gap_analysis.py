"""
IDENTIFYING THE PRECISE GAP

What do we have? What do we need?
"""

print("="*70)
print("WHAT WE HAVE (PROVEN)")
print("="*70)

print("""
1. δ = 0 impossible: v₂(3n+1) ≥ 1 always. DONE.

2. k even impossible: S odd, D odd, kD even. DONE.

3. k ≡ 0 (mod 3) impossible: S ≢ 0 (mod 3), kD ≡ 0. DONE.

4. k = 1 only constant: Induction on nested factorization. DONE.

5. k > 1 with ω_k = 1: Innermost gives a_m = 4/k. DONE.
   (This covers k = 5, 85, 341, 5461, ... where 1+3k = 2^v)

6. k > 1 with ω_k > 1: ???
""")

print("="*70)
print("THE PRECISE GAP")
print("="*70)

print("""
For k > 1 with ω_k > 1:

The nested factorization at innermost level requires:
  a_m = (3·ω^{(m-1)} + 1) / k

For a_m to be a power of 2:
  odd_part(3·ω^{(m-1)} + 1) must divide k
  
If odd_part(3·ω^{(m-1)} + 1) = k, then a_m = 2^{v_m} where v_m = v₂(3ω^{(m-1)} + 1).

So we need: k = ω^{(m)} where ω^{(m)} = odd_part(3·ω^{(m-1)} + 1).

THE GAP: Prove that k never appears in the ω-sequence starting from ω_k.

i.e., For all m ≥ 1: ω^{(m)} ≠ k where ω^{(0)} = ω_k = odd_part(1+3k).
""")

print("="*70)
print("WHAT WOULD CLOSE THE GAP")
print("="*70)

print("""
Option A: Show ω^{(m)} ≠ k directly via number theory.

Option B: Show the constraints are inconsistent in another way.

Option C: Find a different characterization that avoids this issue.

Let me explore each...
""")

# Option A: Analyze when k can appear in ω-sequence
print("\n" + "="*70)
print("OPTION A: When can k appear in its own ω-sequence?")
print("="*70)

def odd_part(n):
    while n % 2 == 0:
        n //= 2
    return n

def v2(n):
    c = 0
    while n % 2 == 0:
        c += 1
        n //= 2
    return c

# For k to appear at position m in its ω-sequence:
# ω^{(m)} = k means 3·ω^{(m-1)} + 1 = k·2^v for some v ≥ 0
# So ω^{(m-1)} = (k·2^v - 1)/3

# Tracing back: we need ω_k → ... → ω^{(m-1)} = (k·2^v - 1)/3 → k

# Let's see what values (k·2^v - 1)/3 can take:

print("\nPossible predecessors of k under ω-map:")
for k in [7, 11, 13, 17, 19, 23]:
    if k % 3 == 0:
        continue
    print(f"\nk = {k}:")
    predecessors = []
    for v in range(1, 20):
        num = k * (2**v) - 1
        if num % 3 == 0 and (num // 3) % 2 == 1 and num // 3 > 0:
            pred = num // 3
            predecessors.append((pred, v))
            if len(predecessors) <= 5:
                print(f"  v={v}: predecessor = {pred}")
    
    # Check if any predecessor appears in the forward ω-sequence from ω_k
    omega_k = odd_part(1 + 3*k)
    sequence = [omega_k]
    current = omega_k
    for _ in range(50):
        if current == 1:
            break
        current = odd_part(3*current + 1)
        sequence.append(current)
    
    print(f"  ω-sequence from ω_k={omega_k}: {sequence[:15]}...")
    
    # Check if k appears
    if k in sequence:
        print(f"  !!! k={k} APPEARS at position {sequence.index(k)}")
    else:
        print(f"  k={k} does NOT appear in sequence")
    
    # Check if any predecessor appears
    for pred, v in predecessors[:10]:
        if pred in sequence:
            pos = sequence.index(pred)
            print(f"  Predecessor {pred} appears at position {pos}")
            print(f"  This would give cycle length m = {pos + 1}")

print("\n" + "="*70)
print("KEY INSIGHT")
print("="*70)

print("""
For k to appear in its own ω-sequence at position m:
  ω^{(m)} = k

This means k must be "reachable" from ω_k in exactly m steps.

But ω_k = odd_part(1+3k), and the map ω → odd_part(3ω+1) is deterministic.

CRITICAL OBSERVATION:
The ω-sequence is exactly the Collatz iteration on ODD numbers.

If k appeared in its own ω-sequence, then starting from ω_k,
the Collatz iteration would return to k.

But ω_k = odd_part(1+3k) ≠ k for k > 1 (proven earlier).

So this would mean: k → ω_k → ... → k, a Collatz cycle involving k!

BUT: If such a cycle existed, then N = k would be in a Collatz cycle,
which is what we're trying to disprove!

THIS IS CIRCULAR - we can't use "k not in a cycle" to prove "k not in a cycle".
""")

print("\n" + "="*70)
print("OPTION B: Find inconsistency elsewhere")
print("="*70)

print("""
The nested factorization must satisfy:
  a_1 · g_1 = (1+3k) · 3^{m-1}

At each level j, we need:
  a_j | divisor of current expression

AND we need the path to be "consistent" - the a_j values we're forced
to choose must actually produce a valid cycle.

Let me check: for the innermost equation to have a_m = power of 2,
and for all the intermediate constraints to work out.

The key is: even if k = ω^{(m)}, the VALUES a_1, ..., a_m must form
a consistent Collatz path, not just any sequence of powers of 2.
""")

# Check if forced path gives valid Collatz path
print("\nChecking path consistency for k = 7:")

k = 7
omega = odd_part(1 + 3*k)
print(f"ω_k = {omega}")

# Build forced a sequence
v0 = v2(1 + 3*k)
a_seq = [2**v0]
omega_seq = [omega]

for j in range(10):
    if omega == 1:
        a_seq.append(4)  # Once ω=1, v=2 always
        omega = 1
    else:
        next_val = 3*omega + 1
        v = v2(next_val)
        omega = odd_part(next_val)
        a_seq.append(2**v)
    omega_seq.append(omega)
    
print(f"Forced a sequence: {a_seq}")
print(f"ω sequence: {omega_seq}")

# For this to be a valid Collatz path, we need:
# Starting from some N, applying Collatz with these δ values returns to N.

# The path (a_1, ..., a_m) corresponds to δ_j = log2(a_j).
# A = sum of δ_j, D = 2^A - 3^m, S = weighted sum.
# Valid cycle requires S = kD and S/D = k.

# For k = 7, m = 5 (since sequence hits 1 at position 4):
m = 5
deltas = [v2(a) for a in a_seq[:m]]
A = sum(deltas)
D = 2**A - 3**m

S = 0
prefix = 0
for j in range(m):
    S += (3**(m-1-j)) * (2**prefix)
    prefix += deltas[j]

print(f"\nFor m = {m}:")
print(f"  δ = {deltas}")
print(f"  A = {A}")
print(f"  D = {D}")
print(f"  S = {S}")
print(f"  S/D = {S/D if D != 0 else 'undefined'}")
print(f"  Need S/D = k = {k}")

print("\n" + "="*70)
print("OPTION C: A DIFFERENT APPROACH")  
print("="*70)

print("""
What if instead of the nested factorization, we look at the problem
from a COMPLETELY different angle?

The Collatz function on odd n: T(n) = odd_part(3n+1)

A cycle exists iff T^m(n) = n for some m ≥ 1.

We've been analyzing the algebraic constraints on S and D.

But what about the DYNAMICS of T?

Key property: T(n) ≈ 3n/2^v where v = v₂(3n+1).

On average, v ≈ 1 or 2, so T(n) ≈ 3n/2 or 3n/4.

For a cycle: T^m(n) = n, so the product of all ratios must be 1:
  ∏ (3/2^{v_j}) = 1
  3^m / 2^A = 1
  3^m = 2^A

But 3^m = 2^A has NO solutions for m, A ≥ 1!

This is the fundamental obstruction.

Wait - but we knew D = 2^A - 3^m > 0 is required, not 2^A = 3^m.

The cycle equation S = kD shows that S "makes up the difference" between
2^A and k·3^m.

For k = 1: S = D = 2^A - 3^m, so S + 3^m = 2^A.

Hmm, this is just restating what we know.

Let me think about this more carefully...
""")

print("\n" + "="*70)
print("THE REAL INSIGHT")
print("="*70)

print("""
The nested factorization shows:
  S + k·3^m = k·2^A

For constant path (all a_j = 4):
  S = (4^m - 3^m) (geometric series)
  (4^m - 3^m) + k·3^m = k·4^m
  4^m - 3^m + k·3^m = k·4^m
  4^m + (k-1)·3^m = k·4^m
  4^m = k·4^m - (k-1)·3^m
  4^m = k(4^m - 3^m) + 3^m
  
Hmm, let me just verify: for constant path, A = 2m.
  S = 4^m - 3^m (verified earlier)
  D = 4^m - 3^m
  S = D, so k = 1. ✓

For non-constant path to give k > 1:
  S = kD > D
  
So S > 2^A - 3^m.

Also S < 2^A (sum of positive terms less than 2^A).

So: 2^A - 3^m < S < 2^A
    -3^m < S - 2^A < 0
    0 < 2^A - S < 3^m

And S = kD = k(2^A - 3^m), so:
  2^A - S = 2^A - k(2^A - 3^m) = 2^A - k·2^A + k·3^m = 2^A(1-k) + k·3^m

For k > 1: 2^A(1-k) < 0, so 2^A - S = 2^A(1-k) + k·3^m could be positive or negative.

For 2^A - S > 0: k·3^m > (k-1)·2^A
For 2^A - S < 3^m: 2^A(1-k) + k·3^m < 3^m
                   (k-1)·3^m < (k-1)·2^A
                   3^m < 2^A (which is required for D > 0)

So the constraint 0 < 2^A - S < 3^m becomes:
  (k-1)·2^A < k·3^m < k·2^A
  
Dividing by 2^A:
  k - 1 < k·(3/2)^m·(1/2)^{A-m} < k
  
Hmm, this doesn't immediately give a contradiction for k > 1.

Let me try the A = m·log₂(3) + ε boundary...
""")

if __name__ == "__main__":
    pass
