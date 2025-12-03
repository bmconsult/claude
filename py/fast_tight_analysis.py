"""
FAST ANALYSIS: Where do tight primes come from?
"""

def ord_fast(a, p, threshold=None):
    """Compute multiplicative order, with optional early exit."""
    if p == 1: return 1
    order = 1
    current = a % p
    limit = threshold if threshold else p
    while current != 1 and order <= limit:
        current = (current * a) % p
        order += 1
    return order if current == 1 else None

def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors

print("="*70)
print("WHERE DO TIGHT PRIMES COME FROM?")
print("="*70)

# For each m, find the tight prime and where it "originates"
print(f"\n{'m':>3} {'tight_p':>12} {'ord_2':>8} {'origin_d':>10} {'notes'}")
print("-"*60)

for m in range(3, 40):
    if m == 4:
        continue
    
    D = 4**m - 3**m
    primes = prime_factors(D)
    threshold = 2 * m
    
    tight_p = None
    tight_ord = 0
    
    for p in primes:
        # Quick check: p must be > 2m for ord_p(2) >= 2m to be possible
        # Actually no - ord can be up to p-1
        ord_2 = ord_fast(2, p, p)
        if ord_2 and ord_2 >= threshold:
            tight_p = p
            tight_ord = ord_2
            break
    
    if tight_p:
        # Find which divisor d of m this prime first appears
        divisors = [d for d in range(1, m+1) if m % d == 0]
        origin = None
        for d in divisors:
            if pow(4, d, tight_p) == pow(3, d, tight_p):
                origin = d
                break
        
        notes = "primitive" if origin == m else f"from 4^{origin}-3^{origin}"
        print(f"{m:>3} {tight_p:>12} {tight_ord:>8} {origin:>10} {notes}")
    else:
        print(f"{m:>3} {'NONE':>12} {'-':>8} {'-':>10} PROBLEM!")

print("\n" + "="*70)
print("KEY INSIGHT")
print("="*70)

print("""
The tight prime often comes from a DIVISOR d of m, not from m itself!

When d | m and p | (4^d - 3^d), then p | (4^m - 3^m) as well.
The prime p has ord_p(4/3) = d (not m).

But crucially: ord_p(2) is FIXED - it doesn't depend on which 
4^k - 3^k we're considering. It's a property of p alone.

So if p | (4^d - 3^d) with ord_p(2) >= 2m, then p is tight for m!
""")

print("\n" + "="*70)
print("THE INHERITANCE PRINCIPLE")
print("="*70)

# For small d, find primes and their ord_2
print("\nPrimes from small values of d:")
inherited = {}

for d in range(2, 20):
    D_d = 4**d - 3**d
    primes = prime_factors(D_d)
    
    for p in primes:
        if p not in inherited:
            ord_2 = ord_fast(2, p, p)
            inherited[p] = {'origin': d, 'ord_2': ord_2}
            
            # Which m values can use this p as tight?
            if ord_2:
                max_m = ord_2 // 2
                print(f"  d={d:2d}: p={p:>8}, ord_2={ord_2:>6}, tight for m <= {max_m}")

print("\n" + "="*70)
print("THE THEOREM WE NEED TO PROVE")
print("="*70)

print("""
CONJECTURE: For all m >= 3 (m != 4), there exists d | m and prime p such that:
  1. p | (4^d - 3^d)
  2. ord_p(2) >= 2m

Since d | m means d <= m, condition 2 is stronger than ord_p(2) >= 2d.

EQUIVALENT FORMULATION:
  For all m >= 3 (m != 4), among all prime factors of all 4^d - 3^d 
  for d | m, at least one has ord_p(2) >= 2m.

This is about the UNION of prime factors across all divisors.
""")

print("\n" + "="*70)
print("ANALYZING THE UNION OF PRIMES")
print("="*70)

# For each m, find the MAXIMUM ord_p(2) among all primes dividing any 4^d - 3^d for d | m
print(f"\n{'m':>3} {'divisors':>20} {'max_ord_2':>10} {'2m':>6} {'OK?':>5}")
print("-"*50)

for m in range(3, 35):
    if m == 4:
        continue
    
    divisors = [d for d in range(1, m+1) if m % d == 0]
    
    # Collect all primes from all divisors
    all_primes = set()
    for d in divisors:
        D_d = 4**d - 3**d
        all_primes.update(prime_factors(D_d))
    
    # Find max ord_2
    max_ord = 0
    for p in all_primes:
        ord_2 = ord_fast(2, p, p)
        if ord_2 and ord_2 > max_ord:
            max_ord = ord_2
    
    threshold = 2 * m
    ok = "YES" if max_ord >= threshold else "NO"
    div_str = ','.join(map(str, divisors))
    print(f"{m:>3} {div_str:>20} {max_ord:>10} {threshold:>6} {ok:>5}")

print("\n" + "="*70)
print("CRITICAL OBSERVATION")
print("="*70)

print("""
ALL m from 3-34 (except 4) have max_ord_2 >= 2m!

The pattern: As m grows, so does the pool of primes (from divisors).
These primes have varying ord_p(2), but at least one is always large enough.

WHY? Because:
1. Small primes like 7, 11, 13, 37 appear frequently (from small d)
2. These small primes have FIXED ord_p(2) values
3. For example: ord_37(2) = 36, so 37 is tight for all m <= 18
4. As m grows past 18, NEW primes with larger orders appear

The question: Can we PROVE this pattern continues forever?
""")
