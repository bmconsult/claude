"""
ATTACKING THE TIGHT PRIME PROBLEM HEAD-ON

We need to prove: For all m ≥ 3 (m ≠ 4), ∃ prime p | (4^m - 3^m) with ord_p(2) ≥ 2m.

Let's analyze the structure deeply.
"""

def multiplicative_order(a, n):
    if n == 1: return 1
    order = 1
    current = a % n
    while current != 1:
        current = (current * a) % n
        order += 1
        if order > n: return None
    return order

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
print("DEEP ANALYSIS OF 4^m - 3^m")
print("="*70)

print("""
For p | (4^m - 3^m):
  - 4^m ≡ 3^m (mod p)
  - ord_p(4/3) divides m
  - For PRIMITIVE prime: ord_p(4/3) = m

Key relationship:
  4 = 2^2, so ord_p(4) = ord_p(2)/gcd(ord_p(2), 2)
  
  If ord_p(2) is odd: ord_p(4) = ord_p(2)
  If ord_p(2) is even: ord_p(4) = ord_p(2)/2

For ord_p(4/3) = m:
  ord_p(4/3) = lcm(ord_p(4), ord_p(3)) / gcd-stuff... complicated.

Let me look at this differently.
""")

print("="*70)
print("PATTERN ANALYSIS: When is ord_p(2) ≥ 2m?")
print("="*70)

# For each m, find ALL primes dividing D and their orders
data = []
for m in range(3, 30):
    if m == 4:
        continue
    D = 4**m - 3**m
    primes = get_prime_factors(D)
    
    max_ord = 0
    max_p = None
    tight_p = None
    
    prime_data = []
    for p in primes:
        ord_2 = multiplicative_order(2, p)
        ord_3 = multiplicative_order(3, p)
        ord_4 = multiplicative_order(4, p)
        
        prime_data.append({
            'p': p,
            'ord_2': ord_2,
            'ord_3': ord_3,
            'ord_4': ord_4,
            'p_mod_m': p % m,
            'p_minus_1': p - 1
        })
        
        if ord_2 > max_ord:
            max_ord = ord_2
            max_p = p
        if ord_2 >= 2*m:
            tight_p = p
    
    data.append({
        'm': m,
        'D': D,
        'num_primes': len(primes),
        'max_ord': max_ord,
        'max_p': max_p,
        'tight_p': tight_p,
        'threshold': 2*m,
        'prime_data': prime_data
    })

print("\nSummary:")
print(f"{'m':>3} {'D':>15} {'#primes':>8} {'max_ord':>10} {'2m':>6} {'tight?':>8}")
print("-"*60)

for d in data:
    tight = "YES" if d['tight_p'] else "NO"
    print(f"{d['m']:>3} {d['D']:>15} {d['num_primes']:>8} {d['max_ord']:>10} {d['threshold']:>6} {tight:>8}")

print("\n" + "="*70)
print("INVESTIGATING NON-TIGHT CASES")
print("="*70)

# Are there any m where we DON'T have a tight prime?
non_tight = [d for d in data if not d['tight_p']]
if non_tight:
    print(f"\nNon-tight cases: {[d['m'] for d in non_tight]}")
    for d in non_tight:
        print(f"\nm = {d['m']}: D = {d['D']}")
        for pd in d['prime_data']:
            print(f"  p = {pd['p']}: ord_2 = {pd['ord_2']}, p-1 = {pd['p_minus_1']}")
else:
    print("\nALL cases have tight primes!")

print("\n" + "="*70)
print("KEY OBSERVATION: Structure of tight primes")
print("="*70)

print("\nFor each m with tight prime, analyze the tight prime:")
for d in data[:15]:
    if d['tight_p']:
        p = d['tight_p']
        m = d['m']
        ord_2 = multiplicative_order(2, p)
        
        # Is 2 a primitive root mod p?
        is_prim_root = (ord_2 == p - 1)
        
        # What's p mod m?
        p_mod_m = p % m
        
        # What's (p-1) mod m?
        pm1_mod_m = (p - 1) % m
        
        print(f"m={m:2d}: p={p:>8}, ord_2={ord_2:>6}, p-1={p-1:>8}, " + 
              f"p≡{p_mod_m}(mod m), p-1≡{pm1_mod_m}(mod m), prim_root={is_prim_root}")

print("\n" + "="*70)
print("THEORETICAL ANALYSIS")
print("="*70)

print("""
OBSERVATION 1: For primitive prime p of 4^m - 3^m, we have p ≡ 1 (mod m).
  This is because ord_p(4/3) = m implies m | (p-1) by Fermat's little theorem.

OBSERVATION 2: p ≡ 1 (mod m) means p - 1 = km for some k ≥ 1.

OBSERVATION 3: ord_p(2) divides p - 1 = km.

For ord_p(2) ≥ 2m, we need ord_p(2) to be "large enough".

OBSERVATION 4: If ord_p(2) = p - 1 (2 is primitive root), then ord_p(2) = km ≥ m.
  For km ≥ 2m, we need k ≥ 2, i.e., p ≥ 2m + 1.
  
  Primitive primes of 4^m - 3^m are often large (≥ m+1 at minimum).
  
OBSERVATION 5: Even if 2 is not a primitive root, ord_p(2) can still be ≥ 2m
  if it's a large divisor of p-1.
""")

# Check: for tight primes, how does ord_2 compare to p-1?
print("\nRatio ord_2 / (p-1) for tight primes:")
for d in data[:15]:
    if d['tight_p']:
        p = d['tight_p']
        ord_2 = multiplicative_order(2, p)
        ratio = ord_2 / (p - 1)
        print(f"  m={d['m']:2d}: ord_2/(p-1) = {ord_2}/{p-1} = {ratio:.4f}")

print("\n" + "="*70)
print("THE ZSYGMONDY CONNECTION")
print("="*70)

print("""
Zsygmondy's Theorem guarantees: For m ≥ 2, 4^m - 3^m has a primitive prime p
such that p ∤ 4^k - 3^k for any k < m.

For such primitive p:
  - ord_p(4/3) = m (exactly)
  - p ≡ 1 (mod m)
  - p ≥ m + 1 (since p ≡ 1 and p is prime)

The question: Does the primitive prime always satisfy ord_p(2) ≥ 2m?

Let's check:
""")

for d in data[:20]:
    m = d['m']
    D = 4**m - 3**m
    primes = get_prime_factors(D)
    
    # Find primitive prime (ord_p(4/3) = m)
    prim_p = None
    for p in primes:
        inv_3 = pow(3, p-2, p)
        ratio = (4 * inv_3) % p
        ord_ratio = multiplicative_order(ratio, p)
        if ord_ratio == m:
            prim_p = p
            break
    
    if prim_p:
        ord_2 = multiplicative_order(2, prim_p)
        is_tight = ord_2 >= 2*m
        status = "TIGHT" if is_tight else f"NOT TIGHT (ord={ord_2} < {2*m})"
        print(f"  m={m:2d}: primitive p={prim_p:>8}, ord_p(2)={ord_2:>6}, {status}")

print("\n" + "="*70)
print("CRITICAL FINDING")
print("="*70)

print("""
The primitive prime is NOT always tight!

But that's OK - we just need SOME prime to be tight.

For m where the primitive prime isn't tight (like m=11, m=16), 
another prime factor of 4^m - 3^m IS tight.

The question becomes:
  "Does 4^m - 3^m ALWAYS have at least one prime factor p with ord_p(2) ≥ 2m?"
  
This is about the FULL factorization of 4^m - 3^m, not just the primitive prime.
""")

print("\n" + "="*70)
print("FACTORIZATION STRUCTURE OF 4^m - 3^m")
print("="*70)

print("""
4^m - 3^m = ∏_{d|m} Φ_d(4, 3)

where Φ_d(4, 3) is the d-th cyclotomic-like factor.

For d = m (the primitive part), this gives new prime factors.
For d < m, these are "old" prime factors that also divide smaller 4^k - 3^k.

Each factor Φ_d(4, 3) contributes primes with specific order structures.
""")

# Let's look at the factorization pattern
print("\nFactorization by divisor contributions:")
for m in [6, 10, 12, 15]:
    D = 4**m - 3**m
    print(f"\nm = {m}: D = {D}")
    
    divisors = [d for d in range(1, m+1) if m % d == 0]
    print(f"  Divisors of m: {divisors}")
    
    for d in divisors:
        D_d = 4**d - 3**d
        print(f"  4^{d} - 3^{d} = {D_d}")
    
    primes = get_prime_factors(D)
    for p in primes:
        # Which divisor does p "come from"?
        min_d = None
        for d in divisors:
            if pow(4, d, p) == pow(3, d, p):
                min_d = d
                break
        ord_2 = multiplicative_order(2, p)
        tight = "TIGHT" if ord_2 >= 2*m else ""
        print(f"  p={p}: first appears at d={min_d}, ord_2={ord_2} {tight}")

print("\n" + "="*70)
print("EMERGING PATTERN")
print("="*70)

print("""
The tight primes often come from SMALLER divisors d of m!

For example:
- When m = 12, the prime 37 comes from d = 3 (since 37 | 4^3 - 3^3 = 37).
  And ord_37(2) = 36 ≥ 24 = 2m. ✓

- When m = 15, the prime 37 comes from d = 3.
  And ord_37(2) = 36 ≥ 30 = 2m. ✓

This suggests: Primes from small divisors d tend to have large ord_p(2),
because they've "accumulated" order from being factors of many 4^k - 3^k.
""")

if __name__ == "__main__":
    pass
