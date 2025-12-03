"""
FRESH START: Looking for the fundamental identity

Let me trace the nested factorization very carefully and see
if there's an algebraic identity we've been missing.
"""

print("="*70)
print("THE NESTED FACTORIZATION - CAREFUL DERIVATION")
print("="*70)

print("""
Setup:
- m odd steps in a cycle
- At step j: N_j → (3N_j + 1) / 2^{δ_j} = N_{j+1}
- a_j = 2^{δ_j} for j = 1, ..., m (using 1-indexing)
- P_j = a_1 · a_2 · ... · a_j (partial products), P_0 = 1
- A = δ_1 + ... + δ_m, so 2^A = P_m

The cycle equation: S = k·D where
- S = Σ_{j=0}^{m-1} 3^{m-1-j} · 2^{prefix_j} = Σ_{j=0}^{m-1} 3^{m-1-j} · P_j
- D = 2^A - 3^m
- N = S/D = k

The nested factorization from S + k·3^m = k·2^A:
  a_1(a_2(...(k·a_m - 1) - 3)...) - 3^{m-2}) = (1+3k)·3^{m-1}

Let H_j be the "running value" at level j:
- H_0 = (1+3k)·3^{m-1}
- H_1 = H_0 / a_1
- H_2 = (H_1 - 3^{m-2}) / a_2
- ...
- H_{m-1} = (H_{m-2} - 3) / a_{m-1}
- And H_{m-1} = k·a_m - 1 (innermost constraint)
""")

print("\n" + "="*70)
print("INVERTING THE RECURSION")
print("="*70)

print("""
Inverting H_j = (H_{j-1} - 3^{m-j}) / a_j:
  H_{j-1} = a_j · H_j + 3^{m-j}

Tracing back from innermost:
  H_{m-1} = k·a_m - 1
  H_{m-2} = a_{m-1} · H_{m-1} + 3 = a_{m-1}(k·a_m - 1) + 3
  H_{m-3} = a_{m-2} · H_{m-2} + 9
  ...
  H_0 = a_1 · H_1 + 3^{m-1}

CLAIM: H_0 = P_{m-1} · H_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i} · P_i
""")

# Verify the claim
print("\nVerifying for m = 3, 4, 5:")

for m in [3, 4, 5]:
    print(f"\nm = {m}:")
    
    # Symbolic expansion
    # H_{m-1} is our variable
    # Trace backwards
    
    # Let's do this numerically with specific values
    k = 7  # Example k
    deltas = [2] * m  # Example path
    
    a = [2**d for d in deltas]
    P = [1] + [1 for _ in range(m-1)]  # P[j] = product of first j a's
    for j in range(1, m):
        P[j] = P[j-1] * a[j-1]  # P[1] = a[0], P[2] = a[0]*a[1], etc
    
    # Actually, let me be more careful with indexing
    # a_1, a_2, ..., a_m correspond to indices 0, 1, ..., m-1 in Python
    # P_j = a_1 * ... * a_j
    
    P = [1]  # P[0] = 1
    prod = 1
    for j in range(m-1):
        prod *= a[j]
        P.append(prod)
    # Now P[j] = product of first j a's, for j = 0, 1, ..., m-1
    # P[m-1] = a_1 * ... * a_{m-1}
    
    # Compute H_0
    H_0 = (1 + 3*k) * (3**(m-1))
    
    # Compute H values going forward
    H = [H_0]
    for j in range(1, m):
        H_next = (H[-1] - 3**(m-j)) / a[j-1]  # a[j-1] is a_j in 1-indexing
        H.append(H_next)
    # Wait, this isn't right. Let me redo.
    
    # H_0 = (1+3k) * 3^{m-1}
    # H_1 = H_0 / a_1
    # H_2 = (H_1 - 3^{m-2}) / a_2
    # ...
    # H_j = (H_{j-1} - 3^{m-j}) / a_j for j >= 2
    
    H = [H_0]
    H.append(H_0 / a[0])  # H_1 = H_0 / a_1
    for j in range(2, m):
        subtract = 3**(m-j)
        H_next = (H[-1] - subtract) / a[j-1]  # a[j-1] is a_j
        H.append(H_next)
    
    # H[m-1] should equal k * a[m-1] - 1
    H_m_minus_1 = H[m-1]
    innermost_check = k * a[m-1] - 1
    
    print(f"  H values: {[int(h) for h in H]}")
    print(f"  H[m-1] = {int(H_m_minus_1)}, k*a_m - 1 = {innermost_check}")
    print(f"  Match: {abs(H_m_minus_1 - innermost_check) < 0.001}")
    
    # Check the formula: H_0 = P_{m-1} · H_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i} · P_i
    formula_rhs = P[m-1] * H_m_minus_1 + sum(3**(m-1-i) * P[i] for i in range(1, m-1))
    print(f"  Formula check: H_0 = {int(H_0)}, RHS = {formula_rhs}")
    print(f"  Match: {abs(H_0 - formula_rhs) < 0.001}")

print("\n" + "="*70)
print("DERIVING THE KEY IDENTITY")
print("="*70)

print("""
From H_0 = P_{m-1} · H_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i} · P_i

Substituting H_{m-1} = k·a_m - 1 and H_0 = (1+3k)·3^{m-1}:

(1+3k)·3^{m-1} = P_{m-1}·(k·a_m - 1) + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

= k·a_m·P_{m-1} - P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

Now, a_m·P_{m-1} = a_m · a_1 · ... · a_{m-1} = P_m = 2^A.

So:
(1+3k)·3^{m-1} = k·2^A - P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

Rearranging:
3^{m-1} + 3k·3^{m-1} - k·2^A = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

3^{m-1} - k(2^A - 3^m) = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

3^{m-1} - k·D = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

With S = k·D:

3^{m-1} - S = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i    ... (*)
""")

print("="*70)
print("THE S FORMULA")
print("="*70)

print("""
Now, S = Σ_{j=0}^{m-1} 3^{m-1-j}·P_j

= 3^{m-1}·P_0 + Σ_{j=1}^{m-1} 3^{m-1-j}·P_j

= 3^{m-1} + Σ_{j=1}^{m-1} 3^{m-1-j}·P_j    (since P_0 = 1)

Therefore:

3^{m-1} - S = -Σ_{j=1}^{m-1} 3^{m-1-j}·P_j    ... (**)
""")

print("="*70)
print("EQUATING (*) AND (**)")
print("="*70)

print("""
From (*): 3^{m-1} - S = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i
From (**): 3^{m-1} - S = -Σ_{j=1}^{m-1} 3^{m-1-j}·P_j

Equating:

-Σ_{j=1}^{m-1} 3^{m-1-j}·P_j = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

Now, let's expand the LHS:

Σ_{j=1}^{m-1} 3^{m-1-j}·P_j = Σ_{i=1}^{m-2} 3^{m-1-i}·P_i + 3^{m-1-(m-1)}·P_{m-1}
                            = Σ_{i=1}^{m-2} 3^{m-1-i}·P_i + 3^0·P_{m-1}
                            = Σ_{i=1}^{m-2} 3^{m-1-i}·P_i + P_{m-1}

So:

-(Σ_{i=1}^{m-2} 3^{m-1-i}·P_i + P_{m-1}) = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

-Σ_{i=1}^{m-2} 3^{m-1-i}·P_i - P_{m-1} = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

The P_{m-1} terms cancel:

-Σ_{i=1}^{m-2} 3^{m-1-i}·P_i = Σ_{i=1}^{m-2} 3^{m-1-i}·P_i

0 = 2·Σ_{i=1}^{m-2} 3^{m-1-i}·P_i
""")

print("="*70)
print("THE CONTRADICTION")
print("="*70)

print("""
For m ≥ 3:
  The sum Σ_{i=1}^{m-2} 3^{m-1-i}·P_i has at least one term (when i = 1).
  
  The term for i = 1 is: 3^{m-2}·P_1 = 3^{m-2}·a_1 > 0
  
  All terms are positive (3^{...} > 0 and P_i > 0).
  
  Therefore: Σ_{i=1}^{m-2} 3^{m-1-i}·P_i > 0
  
  So: 0 = 2·(positive) is a CONTRADICTION!

For m = 2:
  The sum Σ_{i=1}^{0} is empty (no terms).
  So we get 0 = 0, no contradiction.

For m = 1:
  The sum Σ_{i=1}^{-1} is empty.
  No contradiction from this identity.

CONCLUSION: No cycle with m ≥ 3 odd steps can exist!
""")

print("="*70)
print("WHAT ABOUT m = 1 AND m = 2?")
print("="*70)

print("""
m = 1: A single odd step N → (3N+1)/2^δ → back to N.
       This means (3N+1)/2^δ = N, so 3N+1 = N·2^δ.
       N(2^δ - 3) = 1, so N = 1/(2^δ - 3).
       For N to be a positive integer: 2^δ - 3 = 1, so 2^δ = 4, δ = 2.
       Then N = 1.
       
       This is the trivial cycle: 1 → 4 → 2 → 1. ✓

m = 2: Two odd steps means two DISTINCT odd numbers in the cycle.
       But can this happen?
       
       Starting from odd N:
       N → (3N+1)/2^{δ_1} = N_1 (must be odd, distinct from N)
       N_1 → (3N_1+1)/2^{δ_2} = N (back to start)
       
       For N_1 to be odd: 3N+1 = 2^{δ_1}·N_1 where N_1 is odd.
       This means δ_1 = v_2(3N+1), the exact power of 2 dividing 3N+1.
       
       For a cycle, we need the equation S = kD to have a solution.
       But even if it does, we need N_1 ≠ N for a TRUE 2-cycle.
       
       Let's check: if N_1 = N, we're back to m = 1.
       
       For N_1 ≠ N with m = 2:
       S = 3 + 2^{δ_1}, D = 2^{δ_1+δ_2} - 9.
       k = S/D must be a positive integer.
       
       We need D > 0: 2^{δ_1+δ_2} > 9, so δ_1 + δ_2 ≥ 4.
       With δ_1, δ_2 ≥ 1, minimum is δ_1 + δ_2 = 4.
       
       Testing δ_1 = δ_2 = 2:
       S = 3 + 4 = 7, D = 16 - 9 = 7.
       k = 1, N = S/D = 1.
       
       But with N = 1: N_1 = (3·1+1)/4 = 1. So N_1 = N = 1.
       This is the m = 1 cycle, not a true m = 2 cycle!
       
       Testing other values:
       δ_1 = 1, δ_2 = 3: S = 3 + 2 = 5, D = 16 - 9 = 7. S/D = 5/7, not integer.
       δ_1 = 3, δ_2 = 1: S = 3 + 8 = 11, D = 16 - 9 = 7. S/D = 11/7, not integer.
       δ_1 = 1, δ_2 = 4: S = 5, D = 32 - 9 = 23. Not integer.
       δ_1 = 2, δ_2 = 3: S = 7, D = 32 - 9 = 23. Not integer.
       
       In fact, for any δ_1, δ_2 with δ_1 + δ_2 ≥ 4:
       If k = 1 works, it gives N = 1, which collapses to m = 1.
       If k > 1, our general argument would apply...
       
       But wait, for m = 2, the contradiction 0 = 2·Σ doesn't apply (empty sum).
       So we need a different argument for m = 2.
""")

# Exhaustive check for m = 2
print("\nExhaustive check for m = 2 cycles with N > 1:")

found = False
for delta1 in range(1, 20):
    for delta2 in range(1, 20):
        A = delta1 + delta2
        D = 2**A - 9
        if D <= 0:
            continue
        S = 3 + 2**delta1
        if S % D == 0:
            k = S // D
            N = k
            # Check if it's a valid cycle
            N1 = (3*N + 1) // (2**delta1)
            if (3*N + 1) % (2**delta1) != 0:
                continue
            N_back = (3*N1 + 1) // (2**delta2)
            if (3*N1 + 1) % (2**delta2) != 0:
                continue
            if N_back == N and N1 != N:
                print(f"  Found m=2 cycle: N={N}, N1={N1}, deltas=({delta1},{delta2})")
                found = True
            elif N_back == N and N1 == N:
                pass  # This is m=1 in disguise

if not found:
    print("  No m=2 cycles found with N > 1 (only the trivial N=1 case exists)")

print("\n" + "="*70)
print("FINAL CONCLUSION")
print("="*70)

print("""
THEOREM: The only Collatz cycle is the trivial fixed point N = 1.

PROOF:

1. For m ≥ 3: The identity 0 = 2·Σ_{i=1}^{m-2} 3^{m-1-i}·P_i
   gives a contradiction since RHS > 0.
   Therefore, no cycle with m ≥ 3 odd steps can exist.

2. For m = 2: Exhaustive check shows the only solution to S = kD
   is k = 1 with (δ_1, δ_2) = (2, 2), giving N = 1.
   But N = 1 gives N_1 = (3·1+1)/4 = 1 = N, so this is really m = 1.
   No true m = 2 cycle exists.

3. For m = 1: The only solution is N = 1 (the trivial fixed point).

CONCLUSION: No non-trivial Collatz cycle exists.

Q.E.D.
""")

print("="*70)
print("VERIFICATION")
print("="*70)

# Let me verify the key identity numerically
print("\nNumerical verification of the key identity for various m:")

for m in range(3, 8):
    for k in [1, 5, 7, 11]:
        for delta_choice in [[2]*m, [1,2,3] + [2]*(m-3) if m >= 3 else [2]*m]:
            if len(delta_choice) != m:
                continue
            
            deltas = delta_choice
            a = [2**d for d in deltas]
            
            # Compute P values
            P = [1]
            prod = 1
            for j in range(m):
                prod *= a[j]
                P.append(prod)
            
            # P[j] = a_0 * ... * a_{j-1} for j >= 1, P[0] = 1
            # In 1-indexed terms: P_j = a_1 * ... * a_j
            
            # Compute S
            S = sum(3**(m-1-j) * P[j] for j in range(m))
            
            # Compute D
            A = sum(deltas)
            D = 2**A - 3**m
            
            if D <= 0:
                continue
            
            # Check if S = kD
            if S == k * D:
                # Check the identity
                lhs = 2 * sum(3**(m-1-i) * P[i] for i in range(1, m-1))
                print(f"m={m}, k={k}, δ={deltas}: S={S}, kD={k*D}, identity LHS={lhs}")
                if lhs != 0:
                    print("  ^^^ CONTRADICTION - this should be 0 if S = kD!")

print("\n" + "="*70)
print("WAIT - CHECKING FOR ERRORS")
print("="*70)

print("""
Let me double-check by considering whether a path with S = kD can actually exist.

If S = kD, then the nested factorization MUST have a solution.
But my derivation shows that any such solution leads to 0 = positive.

The question is: did I correctly derive the identity?

Let me trace through for m = 3, k = 1 very carefully.
""")

m = 3
k = 1
print(f"\nm = {m}, k = {k}:")

# For k = 1, we know (δ1, δ2, δ3) = (2, 2, 2) should work (constant path)
deltas = [2, 2, 2]
a = [4, 4, 4]

# P values: P_0 = 1, P_1 = a_1 = 4, P_2 = a_1*a_2 = 16
P = [1, 4, 16]

# S = 3^2 * P_0 + 3^1 * P_1 + 3^0 * P_2 = 9 + 12 + 16 = 37
S = 9 * 1 + 3 * 4 + 1 * 16
print(f"  S = {S}")

# D = 2^6 - 3^3 = 64 - 27 = 37
A = 6
D = 64 - 27
print(f"  D = {D}")

# S = kD check
print(f"  S = kD? {S} = {k}*{D} = {k*D}? {S == k*D}")

# The sum Σ_{i=1}^{m-2} = Σ_{i=1}^{1}
# Only i = 1: 3^{m-1-1} * P_1 = 3^1 * 4 = 12
the_sum = 3**1 * 4
print(f"  The sum Σ_{{i=1}}^{{{m-2}}} 3^{{m-1-i}} * P_i = {the_sum}")
print(f"  0 = 2 * {the_sum} = {2 * the_sum}???")

print("""
The identity says 0 = 2 * 12 = 24, which is FALSE!

But I just showed that S = kD = 37 is TRUE for this path.

So there's an ERROR in my derivation somewhere!

Let me re-examine...
""")

print("\n" + "="*70)
print("FINDING THE ERROR")
print("="*70)

# Let me verify equation (*) directly
# (*): 3^{m-1} - S = -P_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i} * P_i

lhs_star = 3**(m-1) - S  # 9 - 37 = -28
rhs_star = -P[m-1] + sum(3**(m-1-i) * P[i] for i in range(1, m-1))  # -16 + 12 = -4

print(f"Checking equation (*):")
print(f"  LHS: 3^{{m-1}} - S = 9 - 37 = {lhs_star}")
print(f"  RHS: -P_{{m-1}} + Σ = -16 + 12 = {rhs_star}")
print(f"  Match? {lhs_star == rhs_star}")

print("""
THEY DON'T MATCH! -28 ≠ -4

So equation (*) is WRONG!

Let me re-derive it more carefully...
""")

# Re-derive: starting from H_0 = P_{m-1} * H_{m-1} + Σ_{i=1}^{m-2} 3^{m-1-i} * P_i

# For m = 3:
# H_0 = P_2 * H_2 + 3^1 * P_1
# H_0 = 16 * H_2 + 12

H_0 = (1 + 3*k) * 3**(m-1)  # = 4 * 9 = 36
print(f"\nH_0 = (1+3k) * 3^{{m-1}} = {H_0}")

# From the recurrence:
# H_1 = H_0 / a_1 = 36 / 4 = 9
H_1 = H_0 / a[0]
print(f"H_1 = H_0 / a_1 = {H_1}")

# H_2 = (H_1 - 3^{m-2}) / a_2 = (9 - 3) / 4 = 6/4 = 1.5 ???
H_2 = (H_1 - 3**(m-2)) / a[1]
print(f"H_2 = (H_1 - 3^{{m-2}}) / a_2 = ({H_1} - 3) / 4 = {H_2}")

print("""
H_2 = 1.5, which is NOT an integer!

This means the path (2, 2, 2) does NOT satisfy the nested factorization for k = 1, m = 3!

Wait, but S = kD was satisfied... Let me recheck.
""")

# Actually, I need to be more careful about what path gives S = kD

# For k = 1, m = 3, we need S = D.
# D = 2^A - 27
# S = 9 + 3*2^{δ_1} + 2^{δ_1 + δ_2}

# For S = D:
# 9 + 3*2^{δ_1} + 2^{δ_1 + δ_2} = 2^{δ_1 + δ_2 + δ_3} - 27
# 36 + 3*2^{δ_1} + 2^{δ_1 + δ_2} = 2^{δ_1 + δ_2 + δ_3}

# With all δ = 2:
# 36 + 12 + 16 = 64 = 2^6 ✓

print("Let me recompute S more carefully...")

# S = Σ_{j=0}^{m-1} 3^{m-1-j} * 2^{prefix_j}
# prefix_j = δ_0 + ... + δ_{j-1}

# For m = 3, δ = (2, 2, 2):
# j = 0: 3^2 * 2^0 = 9
# j = 1: 3^1 * 2^{δ_0} = 3 * 4 = 12
# j = 2: 3^0 * 2^{δ_0 + δ_1} = 1 * 16 = 16
# S = 9 + 12 + 16 = 37

# D = 2^6 - 27 = 64 - 27 = 37

# So S = D = 37, k = 1. ✓

# But the nested factorization doesn't work with H_2 = 1.5...

# The issue is that the innermost should be:
# H_2 = k * a_3 - 1 = 1 * 4 - 1 = 3

# But from the recursion, H_2 = 1.5 ≠ 3.

print(f"\nFrom recursion: H_2 = {H_2}")
print(f"From innermost (k * a_3 - 1): {k * a[2] - 1}")
print(f"These don't match!")

print("""
So either my recursion is wrong, or the innermost formula is wrong, 
or the path (2,2,2) doesn't actually give k = 1 for m = 3.

Let me trace the ACTUAL cycle for m = 3, k = 1.
""")

# For k = 1, N = 1. But 1 → 4 → 2 → 1 has only m = 1 odd step!
# So there's no m = 3 cycle with k = 1.

print("For k = 1, N = S/D = 1.")
print("But 1 → 4 → 2 → 1 has only m = 1 odd step.")
print("So there is NO m = 3 cycle with k = 1, even though S = D = 37!")

print("""
The issue is that the equation S = kD is NECESSARY but not SUFFICIENT!

The path (2, 2, 2) gives S = D = 37, but the actual cycle starting 
from N = 1 doesn't have 3 odd steps.

So the nested factorization correctly shows this path is invalid 
(H_2 is not an integer), even though S = kD is satisfied.

This means my proof approach is WRONG. The equation 0 = 2*Σ 
only applies when the nested factorization has a VALID solution.

I was deriving a contradiction assuming both:
1. S = kD is satisfied
2. The nested factorization has a valid solution

But these are the SAME condition! So I can't get a contradiction 
by assuming both.

Let me reconsider...
""")

if __name__ == "__main__":
    pass
