"""
HOW TO PROVE TIGHT PRIMES ALWAYS EXIST?

We need: For all m ≥ 3 (m ≠ 4), ∃ prime p | (4^m - 3^m) with ord_p(2) ≥ 2m.

Let's investigate the structure more deeply.
"""

def multiplicative_order(a, n, max_iter=None):
    if n == 1: return 1
    if max_iter is None: max_iter = n
    order = 1
    current = a % n
    while current != 1 and order <= max_iter:
        current = (current * a) % n
        order += 1
    return order if current == 1 else None

def get_prime_factors(n):
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors

print("="*70)
print("ANALYZING THE STRUCTURE OF TIGHT PRIMES")
print("="*70)

print("""
For p | (4^m - 3^m), we have 4^m ≡ 3^m (mod p).

This means (4/3)^m ≡ 1 (mod p), so ord_p(4/3) | m.

For PRIMITIVE prime divisor (Zsygmondy): ord_p(4/3) = m exactly.

But we need ord_p(2) ≥ 2m, which is different!

Let's analyze the relationship between ord_p(4/3) and ord_p(2).
""")

print("\n" + "="*70)
print("RELATIONSHIP: ord_p(4/3) vs ord_p(2)")
print("="*70)

for m in range(3, 20):
    if m == 4:
        continue
    D = 4**m - 3**m
    primes = get_prime_factors(D)
    
    print(f"\nm = {m}: D = {D}")
    for p in primes[:5]:  # First 5 primes
        ord_2 = multiplicative_order(2, p)
        ord_3 = multiplicative_order(3, p)
        ord_4 = multiplicative_order(4, p)
        
        # ord_p(4/3) - need to compute 4 * 3^{-1} mod p
        inv_3 = pow(3, p-2, p)  # Fermat's little theorem
        ratio = (4 * inv_3) % p
        ord_ratio = multiplicative_order(ratio, p)
        
        tight = "TIGHT" if ord_2 and ord_2 >= 2*m else ""
        print(f"  p={p}: ord(2)={ord_2}, ord(3)={ord_3}, ord(4)={ord_4}, ord(4/3)={ord_ratio} {tight}")

print("\n" + "="*70)
print("KEY OBSERVATION")
print("="*70)

print("""
Looking at the data:

1. ord_p(4/3) often equals m or divides m (as expected from p | 4^m - 3^m)

2. ord_p(2) and ord_p(4/3) have a complex relationship:
   - ord_p(4) = ord_p(2^2) = ord_p(2) / gcd(ord_p(2), 2)
   - ord_p(4/3) divides lcm(ord_p(4), ord_p(3))
   
3. The tight primes often have ord_p(2) = p-1 (2 is a primitive root mod p)
   or close to it.
""")

print("\n" + "="*70)
print("WHEN IS 2 A PRIMITIVE ROOT?")
print("="*70)

print("""
If 2 is a primitive root mod p, then ord_p(2) = p - 1.

For p | (4^m - 3^m), if p > 2m and 2 is a primitive root mod p,
then ord_p(2) = p - 1 ≥ p - 1 > 2m - 1, so ord_p(2) ≥ 2m. ✓

Artin's conjecture: 2 is a primitive root for infinitely many primes.
(Conditionally proven under GRH.)

But we need: for each 4^m - 3^m, at least ONE prime factor has
             ord_p(2) ≥ 2m.
""")

# Check: are the tight primes often primitive roots?
print("\nChecking if tight primes have 2 as primitive root:")
for m in range(3, 20):
    if m == 4:
        continue
    D = 4**m - 3**m
    primes = get_prime_factors(D)
    
    for p in primes:
        ord_2 = multiplicative_order(2, p)
        if ord_2 and ord_2 >= 2*m:
            is_primitive = (ord_2 == p - 1)
            prim_str = "primitive root" if is_primitive else f"ord={ord_2}, p-1={p-1}"
            print(f"  m={m:2d}: tight p={p}, {prim_str}")
            break

print("\n" + "="*70)
print("ALTERNATIVE: PROVE WITHOUT TIGHT PRIMES")
print("="*70)

print("""
Instead of proving tight primes exist, what if we prove the result directly?

Claim: For A = 2m, D | S only for constant path.

Approach: Show that for ANY prime p | D, the constraint structure
forces the constant path when we consider ALL primes simultaneously.

Key insight from computational data:
- Each prime p | D has a set of "allowed" paths where p | S
- The INTERSECTION of all these sets is exactly {constant path}
- This holds even when no single prime is "tight"

Can we prove this intersection property algebraically?
""")

print("\n" + "="*70)
print("THE INTERSECTION ARGUMENT")
print("="*70)

def compute_S_mod_p(deltas, m, p):
    """Compute S mod p for given delta sequence."""
    S = 0
    prefix = 0
    for j in range(m):
        term = pow(3, m-1-j, p) * pow(2, prefix, p)
        S = (S + term) % p
        prefix += deltas[j]
    return S

def gen_paths(m, A):
    if m == 1:
        if A >= 1: yield [A]
        return
    for d in range(1, A - m + 2):
        for rest in gen_paths(m - 1, A - d):
            yield [d] + rest

# For m = 4 (no tight prime), show intersection works
m = 4
A = 8
D = 4**m - 3**m
primes = get_prime_factors(D)

print(f"\nm = {m}: D = {D} = {' × '.join(map(str, primes))}")
print("No single prime is tight, but intersection still works:\n")

all_paths = list(gen_paths(m, A))
print(f"Total paths: {len(all_paths)}")

# For each prime, find paths where p | S
sets = {}
for p in [25, 7]:  # 25 = 5^2, 7
    allowed = []
    for deltas in all_paths:
        if compute_S_mod_p(deltas, m, p) == 0:
            allowed.append(tuple(deltas))
    sets[p] = set(allowed)
    print(f"  {p} | S for {len(allowed)} paths: {allowed}")

intersection = sets[25] & sets[7]
print(f"\nIntersection: {intersection}")
print(f"Only constant path: {intersection == {(2,2,2,2)}}")

print("\n" + "="*70)
print("THE STRUCTURAL REASON")
print("="*70)

print("""
WHY does the intersection equal {constant path}?

For constant path δ = (2,2,...,2):
  S = Σ 3^{m-1-j} · 4^j = 4^m - 3^m = D
  So p | S for ALL p | D. ✓

For non-constant path:
  S = Σ 3^{m-1-j} · 2^{prefix_j} ≠ D in general.
  
  The key: S is a DIFFERENT algebraic expression from D.
  - D = 4^m - 3^m has specific factorization
  - S with non-constant exponents has DIFFERENT factorization
  
  For D | S, we need EVERY prime power in D to divide S.
  But S, being a different expression, generically shares 
  only SOME factors with D, not all.

This is like asking: when does (4^m - 3^m) | (linear combo of 3^j · 2^{e_j})?
The answer: only when the linear combo equals 4^m - 3^m itself.
""")

print("\n" + "="*70)
print("PROPOSED APPROACH TO FULL PROOF")
print("="*70)

print("""
To prove D | S ⟹ constant path without tight primes:

STEP 1: Express S - D as a "deviation" sum.
  S - D = Σ 3^{m-1-j} · 4^j · (2^{ε_j} - 1)
  where ε_j = prefix_j - 2j.

STEP 2: For non-constant path, at least one ε_j ≠ 0.

STEP 3: Show that D cannot divide this deviation sum.

The challenge: When ε_j < 0, we get fractions: 2^{ε_j} - 1 = (1 - 2^{|ε_j|})/2^{|ε_j|}.

Let me try to work this out...
""")

# Analyze the deviation structure
print("\nDeviation analysis for m = 4:")
m = 4
A = 8
D = 4**m - 3**m

for deltas in list(gen_paths(m, A))[:10]:
    prefix = [0]
    for d in deltas[:-1]:
        prefix.append(prefix[-1] + d)
    prefix.append(A)  # Final value
    
    epsilon = [prefix[j] - 2*j for j in range(m)]
    
    # Compute S
    S = sum(3**(m-1-j) * 2**prefix[j] for j in range(m))
    
    # Compute deviation terms (being careful with fractions)
    dev_sum = S - D
    
    is_const = "CONST" if deltas == [2]*m else ""
    print(f"  δ={deltas}, ε={epsilon}, S-D={dev_sum:+6d} {is_const}")

print("\n" + "="*70)
print("CURRENT STATUS")
print("="*70)

print("""
We have two potential paths to a complete proof:

PATH A: Prove tight primes always exist
  - Need: For m ≥ 3 (m ≠ 4), ∃ p | (4^m - 3^m) with ord_p(2) ≥ 2m
  - Related to Artin's conjecture but not directly implied
  - Would require new number-theoretic results
  
PATH B: Prove directly that D | S ⟹ constant path
  - Show S - D is never divisible by D for non-constant paths
  - Analyze the algebraic structure of S - D
  - The "deviation" formula might give traction
  
PATH C: Use the intersection argument
  - Prove that for multiple primes p_i | D, the sets 
    {paths with p_i | S} have intersection = {constant}
  - This avoids needing a single tight prime
  - Might follow from Chinese Remainder Theorem structure

Each path is challenging. The computational evidence is overwhelming,
but translating it to algebra requires new insights.
""")
