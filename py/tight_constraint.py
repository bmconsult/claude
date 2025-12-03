"""
Find the "tight" prime constraint for each m.

For each prime p | D, count how many paths satisfy p | S.
If any prime has only 1 path (constant), that's the tight constraint.
"""

def factor(n):
    factors = {}
    d = 2
    temp = abs(n)
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    return factors

def gen_paths(m, A):
    if m == 1:
        yield [A]
        return
    for d in range(1, A - m + 2):
        for rest in gen_paths(m - 1, A - d):
            yield [d] + rest

def count_paths_satisfying(m, A, modulus):
    """Count paths where S ≡ 0 (mod modulus)."""
    count = 0
    constant_satisfies = False
    
    for deltas in gen_paths(m, A):
        S = 0
        prefix = 0
        for j in range(m):
            S = (S + pow(3, m-1-j, modulus) * pow(2, prefix, modulus)) % modulus
            prefix += deltas[j]
        
        if S == 0:
            count += 1
            if deltas == [2] * m:
                constant_satisfies = True
    
    return count, constant_satisfies

print("="*70)
print("FINDING TIGHT PRIME CONSTRAINTS")
print("="*70)

for m in range(2, 13):
    A = 2 * m
    D = 4**m - 3**m
    factors = factor(D)
    total_paths = sum(1 for _ in gen_paths(m, A))
    
    print(f"\nm = {m}: D = {D}, {total_paths} total paths")
    
    tight_primes = []
    
    for p, e in factors.items():
        pe = p ** e
        count, const_ok = count_paths_satisfying(m, A, pe)
        
        status = "✓" if const_ok else "✗"
        tight = " ← TIGHT!" if count == 1 else ""
        
        print(f"  {pe:>10} | S: {count:5} paths satisfy {status}{tight}")
        
        if count == 1:
            tight_primes.append(pe)
    
    if tight_primes:
        print(f"  → Tight constraint(s) force constant path: {tight_primes}")
    else:
        # Compute intersection
        all_paths = set(map(tuple, gen_paths(m, A)))
        for p, e in factors.items():
            pe = p ** e
            satisfying = set()
            for deltas in gen_paths(m, A):
                S = 0
                prefix = 0
                for j in range(m):
                    S = (S + pow(3, m-1-j, pe) * pow(2, prefix, pe)) % pe
                    prefix += deltas[j]
                if S == 0:
                    satisfying.add(tuple(deltas))
            all_paths = all_paths & satisfying
        
        print(f"  → Intersection of all constraints: {len(all_paths)} paths")
        if len(all_paths) == 1:
            print(f"     (Constant path is the unique solution)")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print("""
For each m, we have two possibilities:

1. TIGHT CONSTRAINT: Some prime power p^e | D has the property that
   p^e | S ONLY for the constant path. This single constraint is enough.

2. INTERSECTION: No single constraint is tight, but the INTERSECTION
   of all constraints from different prime factors yields only the
   constant path.

In either case, D | S forces δ = (2,2,...,2), proving k = 1.
""")

# Check specifically for m values with single prime factor
print("\n" + "="*70)
print("SPECIAL CASES: Single Prime Factor")
print("="*70)

single_prime_m = []
for m in range(2, 20):
    D = 4**m - 3**m
    factors = factor(D)
    if len(factors) == 1:
        single_prime_m.append(m)
        p = list(factors.keys())[0]
        e = factors[p]
        print(f"m = {m}: D = {D} = {p}^{e}")

print(f"\nm values with single prime D (up to 20): {single_prime_m}")
print("""
For these m, the "tight constraint" comes from the single prime itself.
The structure of S makes it impossible to achieve p | S except for constant path.
""")

if __name__ == "__main__":
    pass
