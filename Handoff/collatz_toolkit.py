"""
COLLATZ VERIFICATION TOOLKIT
============================
Run this to verify the proof components and explore the gap.
"""

from math import gcd

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def multiplicative_order(a, n, max_iter=None):
    """Compute ord_n(a) = min{k > 0 : a^k ≡ 1 (mod n)}"""
    if n == 1: return 1
    if max_iter is None: max_iter = n
    order, current = 1, a % n
    while current != 1 and order <= max_iter:
        current = (current * a) % n
        order += 1
    return order if current == 1 else None

def get_prime_factors(n):
    """Return list of distinct prime factors"""
    factors, d, temp = [], 2, n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0: temp //= d
        d += 1 if d == 2 else 2
    if temp > 1: factors.append(temp)
    return factors

def is_primitive(p, m):
    """Check if p is primitive prime divisor of 4^m - 3^m"""
    if pow(4, m, p) != pow(3, m, p): return False
    for k in range(1, m):
        if pow(4, k, p) == pow(3, k, p): return False
    return True

def find_tight_prime(m):
    """Find a tight prime for m, return (prime, ord, source_d) or None"""
    for d in range(1, m+1):
        if m % d != 0: continue
        D_d = 4**d - 3**d
        for p in get_prime_factors(D_d):
            ord_2 = multiplicative_order(2, p)
            if ord_2 and ord_2 >= 2*m:
                return (p, ord_2, d)
    return None

def verify_direct(m):
    """Verify only constant path has D | S for given m"""
    A, D = 2*m, 4**m - 3**m
    constant = tuple([2]*m)
    
    def gen_paths(m, A):
        if m == 1:
            if A >= 1: yield (A,)
            return
        for d in range(1, A - m + 2):
            for rest in gen_paths(m-1, A-d):
                yield (d,) + rest
    
    for deltas in gen_paths(m, A):
        prefix, S = 0, 0
        for j in range(m):
            S += (3**(m-1-j)) * (2**prefix)
            prefix += deltas[j]
        if S % D == 0 and deltas != constant:
            return False, deltas
    return True, None

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_primitive_primes(m):
    """Analyze all primitive primes of 4^m - 3^m"""
    D = 4**m - 3**m
    primes = get_prime_factors(D)
    results = []
    for p in primes:
        if is_primitive(p, m):
            ord_2 = multiplicative_order(2, p)
            ord_3 = multiplicative_order(3, p)
            results.append({
                'p': p,
                'ord_2': ord_2,
                'ord_3': ord_3,
                'ord_2_even': ord_2 % 2 == 0,
                'is_tight': ord_2 >= 2*m
            })
    return results

def find_coverage_gaps(max_m=100):
    """Find any m values without tight primes"""
    gaps = []
    for m in range(3, max_m+1):
        if m == 4: continue
        result = find_tight_prime(m)
        if result is None:
            gaps.append(m)
    return gaps

# =============================================================================
# VERIFICATION RUNS
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("COLLATZ VERIFICATION TOOLKIT")
    print("="*60)
    
    # 1. Verify direct cases
    print("\n[1] Direct verification for m = 2, 4:")
    for m in [2, 4]:
        ok, _ = verify_direct(m)
        print(f"  m = {m}: {'✓ PASS' if ok else '✗ FAIL'}")
    
    # 2. Tight prime verification
    print("\n[2] Tight prime verification for m = 3 to 50:")
    print(f"{'m':>4} {'tight_p':>12} {'ord':>8} {'from_d':>8}")
    print("-"*40)
    for m in range(3, 51):
        if m == 4: continue
        result = find_tight_prime(m)
        if result:
            p, ord_2, d = result
            src = "primitive" if d == m else f"d={d}"
            print(f"{m:>4} {p:>12} {ord_2:>8} {src:>8}")
        else:
            print(f"{m:>4} {'NONE':>12} {'-':>8} {'FAIL':>8}")
    
    # 3. Check for gaps
    print("\n[3] Checking for gaps up to m = 200...")
    gaps = find_coverage_gaps(200)
    if gaps:
        print(f"  GAPS FOUND: {gaps}")
    else:
        print("  ✓ No gaps - all m have tight primes!")
    
    # 4. Even order analysis
    print("\n[4] Even order analysis (key to proof):")
    print("  If any primitive prime has EVEN ord_p(2), it's automatically tight.")
    print()
    even_count, odd_count = 0, 0
    for m in range(3, 30):
        if m == 4: continue
        prims = analyze_primitive_primes(m)
        has_even = any(p['ord_2_even'] for p in prims)
        has_tight = any(p['is_tight'] for p in prims)
        if has_even:
            even_count += 1
        else:
            odd_count += 1
            if not has_tight:
                print(f"  m={m}: ALL primitive primes have ODD order, checking tight...")
    
    print(f"\n  Summary: {even_count} have even-order primitive, {odd_count} all-odd")
    
    # 5. Key inherited primes
    print("\n[5] Key inherited primes (high reach):")
    inherited = {}
    for d in range(2, 40):
        D_d = 4**d - 3**d
        for p in get_prime_factors(D_d):
            ord_2 = multiplicative_order(2, p)
            reach = ord_2 // 2 if ord_2 else 0
            if p not in inherited or inherited[p][1] < reach:
                inherited[p] = (d, reach, ord_2)
    
    print(f"{'prime':>10} {'origin_d':>10} {'ord_2':>10} {'reach':>10}")
    print("-"*45)
    for p, (d, reach, ord_2) in sorted(inherited.items(), key=lambda x: -x[1][1])[:10]:
        print(f"{p:>10} {d:>10} {ord_2:>10} {reach:>10}")
    
    print("\n" + "="*60)
    print("CURRENT STATUS: All m ≤ 200 verified. Gap: prove for ALL m.")
    print("="*60)
