"""
PROVING GOOD PRIME EXISTENCE

We need to prove: For every prime m, there exists a good prime p | det.

Strategy:
1. Analyze the structure more deeply
2. Find the algebraic reason good primes must exist
3. Extend to composite m
"""

from math import gcd
from itertools import product
from sympy import factorint, isprime, totient
import numpy as np

print("=" * 70)
print("DEEP ANALYSIS: WHY GOOD PRIMES EXIST")
print("=" * 70)

def detailed_analysis(m):
    """Detailed analysis of constraint structure."""
    
    det = 4**m - 3**m
    factors = list(factorint(det).keys())
    S = 2 * m
    
    print(f"\n{'='*60}")
    print(f"m = {m}, det = {det}")
    print(f"{'='*60}")
    
    # For each prime, analyze the constraint
    for p in factors:
        inv_3 = pow(3, -1, p)
        r = (4 * inv_3) % p
        inv_2 = pow(2, -1, p)
        
        # Orders
        ord_r = 1
        temp = r
        while temp != 1:
            temp = (temp * r) % p
            ord_r += 1
        
        ord_2 = 1
        temp = 2
        while temp != 1:
            temp = (temp * 2) % p
            ord_2 += 1
        
        print(f"\np = {p}:")
        print(f"  ord_p(r) = {ord_r}, ord_p(2) = {ord_2}")
        print(f"  p - 1 = {p - 1}")
        
        # Count how many sequences satisfy the constraint mod p
        satisfies = 0
        total = 0
        
        for seq in product(range(1, min(S, 7)), repeat=m):
            if sum(seq) != S:
                continue
            total += 1
            
            s = [0]
            for a in seq:
                s.append(s[-1] + a)
            epsilon = [s[i] - 2*i for i in range(m)]
            
            # Compute weighted sum
            weights = []
            for i in range(m):
                if epsilon[i] >= 0:
                    w = pow(2, epsilon[i], p)
                else:
                    w = pow(inv_2, -epsilon[i], p)
                weights.append(w)
            
            weighted_sum = sum(pow(r, i, p) * weights[i] for i in range(m)) % p
            
            if weighted_sum == (p - 1):  # ≡ -1 mod p
                satisfies += 1
                is_uniform = all(e == 0 for e in epsilon)
                if not is_uniform:
                    print(f"    NON-UNIFORM satisfies: {seq}, ε = {epsilon}")
        
        print(f"  Sequences satisfying constraint: {satisfies}/{total}")
        print(f"  Is good prime: {satisfies == 1}")

for m in [3, 5, 7]:
    if isprime(m):
        detailed_analysis(m)

print("\n" + "=" * 70)
print("THE KEY OBSERVATION: ORBIT STRUCTURE")
print("=" * 70)

print("""
For p | Φ_m(4,3) with ord_p(r) = m:

The powers r^0, r^1, ..., r^{m-1} are DISTINCT (since ord(r) = m).
They form a complete set of m-th roots of unity in F_p.

The constraint Σᵢ r^i · 2^{ε_i} = -1 can be rewritten as:
  Σᵢ r^i · 2^{ε_i} + 1 = 0
  Σᵢ r^i · 2^{ε_i} + r^m = 0  (since r^m = 1)
  
This is a constraint on the "weighted sum" where weights are powers of 2.

KEY: The uniform case gives:
  Σᵢ r^i · 1 = (r^m - 1)/(r - 1) = 0/(r-1) in F_p
  
Wait, that's 0, not -1. Let me reconsider...
""")

def verify_uniform_constraint(m, p):
    """Verify what uniform gives for the constraint."""
    
    inv_3 = pow(3, -1, p)
    r = (4 * inv_3) % p
    
    # Uniform: all ε_i = 0, so all 2^{ε_i} = 1
    uniform_sum = sum(pow(r, i, p) for i in range(m)) % p
    
    print(f"\nm = {m}, p = {p}:")
    print(f"  r = {r}")
    print(f"  Uniform sum Σ r^i = {uniform_sum}")
    print(f"  r^m = {pow(r, m, p)}")
    print(f"  -1 mod p = {p - 1}")
    
    # The actual constraint from the Collatz equation is different!
    # N = Σ 3^{m-1-i} · 2^{s_i}
    # For det | N, we need N ≡ 0 (mod det), i.e., mod p
    
    # Compute N for uniform
    S = 2 * m
    s = [2*i for i in range(m+1)]  # Uniform: s_i = 2i
    N_uniform = sum(3**(m-1-i) * 2**s[i] for i in range(m))
    
    print(f"  N_uniform = {N_uniform}")
    print(f"  det = {4**m - 3**m}")
    print(f"  N_uniform mod p = {N_uniform % p}")
    print(f"  N_uniform = det? {N_uniform == 4**m - 3**m}")

for m in [3, 5]:
    det = 4**m - 3**m
    for p in factorint(det).keys():
        verify_uniform_constraint(m, p)

print("\n" + "=" * 70)
print("CORRECTING THE CONSTRAINT")
print("=" * 70)

print("""
The actual constraint is: N ≡ 0 (mod p)

where N = Σᵢ 3^{m-1-i} · 2^{s_i}

For uniform (s_i = 2i):
  N = Σᵢ 3^{m-1-i} · 4^i = det ≡ 0 (mod p) ✓

For non-uniform (s_i = 2i + ε_i):
  N = Σᵢ 3^{m-1-i} · 2^{2i} · 2^{ε_i}
    = Σᵢ 3^{m-1-i} · 4^i · 2^{ε_i}
    = Σᵢ (3^{m-1}/3^i) · (4/1)^i · 2^{ε_i}
    = 3^{m-1} · Σᵢ (4/3)^i · 2^{ε_i}
    = 3^{m-1} · Σᵢ r^i · 2^{ε_i}

For N ≡ 0 (mod p):
  3^{m-1} · Σᵢ r^i · 2^{ε_i} ≡ 0 (mod p)

Since gcd(3, p) = 1 (as p | 4^m - 3^m and gcd(3, 4^m - 3^m) = 1):
  Σᵢ r^i · 2^{ε_i} ≡ 0 (mod p)

THIS is the correct constraint!
""")

def verify_correct_constraint(m, p):
    """Verify the correct constraint."""
    
    inv_3 = pow(3, -1, p)
    r = (4 * inv_3) % p
    inv_2 = pow(2, -1, p)
    S = 2 * m
    
    print(f"\nm = {m}, p = {p}:")
    
    # Uniform check
    uniform_sum = sum(pow(r, i, p) for i in range(m)) % p
    print(f"  Uniform: Σ r^i = {uniform_sum}")
    
    # For N_uniform = det, and p | det, we have N_uniform ≡ 0 (mod p)
    # So Σ r^i should be... let's compute
    
    # Actually: N = 3^{m-1} · Σ r^i · 2^{ε_i}
    # For uniform: N = det = 3^{m-1} · Σ r^i · 1 = 3^{m-1} · Σ r^i
    # So Σ r^i = det / 3^{m-1}
    
    det = 4**m - 3**m
    expected = (det * pow(3, -(m-1), p)) % p  # det / 3^{m-1} mod p
    print(f"  Expected Σ r^i = det/3^{{m-1}} mod p = {expected}")
    print(f"  Match: {uniform_sum == expected}")
    
    # Check non-uniform
    satisfies = []
    for seq in product(range(1, min(S, 7)), repeat=m):
        if sum(seq) != S:
            continue
        
        s = [0]
        for a in seq:
            s.append(s[-1] + a)
        epsilon = [s[i] - 2*i for i in range(m)]
        
        if all(e == 0 for e in epsilon):
            continue  # Skip uniform
        
        # Compute Σ r^i · 2^{ε_i}
        total = 0
        for i in range(m):
            if epsilon[i] >= 0:
                w = pow(2, epsilon[i], p)
            else:
                w = pow(inv_2, -epsilon[i], p)
            total = (total + pow(r, i, p) * w) % p
        
        # For N ≡ 0 (mod p), need total = 0 (since 3^{m-1} is invertible)
        if total == 0:
            satisfies.append((seq, epsilon))
    
    print(f"  Non-uniform with Σ r^i · 2^ε ≡ 0: {len(satisfies)}")
    for seq, eps in satisfies[:3]:
        print(f"    {seq}: ε = {eps}")

for m in [3, 5, 7]:
    det = 4**m - 3**m
    for p in factorint(det).keys():
        verify_correct_constraint(m, p)

print("\n" + "=" * 70)
print("THE GOOD PRIME CRITERION (CORRECTED)")
print("=" * 70)

def find_good_prime_correct(m):
    """Find good prime with correct constraint."""
    
    det = 4**m - 3**m
    factors = list(factorint(det).keys())
    S = 2 * m
    
    print(f"\nm = {m}: det = {det} = {factorint(det)}")
    
    for p in factors:
        inv_3 = pow(3, -1, p)
        r = (4 * inv_3) % p
        inv_2 = pow(2, -1, p)
        
        is_good = True
        
        for seq in product(range(1, S), repeat=m):
            if sum(seq) != S:
                continue
            
            s = [0]
            for a in seq:
                s.append(s[-1] + a)
            epsilon = [s[i] - 2*i for i in range(m)]
            
            if all(e == 0 for e in epsilon):
                continue  # Skip uniform
            
            # Compute Σ r^i · 2^{ε_i}
            total = 0
            for i in range(m):
                if epsilon[i] >= 0:
                    w = pow(2, epsilon[i], p)
                else:
                    w = pow(inv_2, -epsilon[i], p)
                total = (total + pow(r, i, p) * w) % p
            
            if total == 0:
                is_good = False
                break
        
        if is_good:
            print(f"  ✓ GOOD PRIME: p = {p}")
            return p
    
    print(f"  ✗ No good prime found!")
    return None

print("\nFinding good primes (with correct constraint):")
for m in [2, 3, 5, 7, 11, 13]:
    if isprime(m):
        find_good_prime_correct(m)

print("\n" + "=" * 70)
print("EXTENDING TO COMPOSITE m")
print("=" * 70)

def analyze_composite(m):
    """Analyze composite m case."""
    
    det = 4**m - 3**m
    factors = factorint(det)
    S = 2 * m
    
    print(f"\nm = {m}: det = {det}")
    print(f"  Cyclotomic factorization: ", end="")
    
    # Compute Φ_d(4,3) for each d | m
    from sympy import divisors
    phi_values = {}
    for d in divisors(m):
        if d == 1:
            phi_d = 1
        else:
            # Φ_d(4,3) via Möbius inversion
            # Actually, let's just factor det and identify which primes go where
            pass
    
    print(f"  Prime factors: {list(factors.keys())}")
    
    # For each prime p, determine which Φ_d it divides
    for p in factors.keys():
        inv_3 = pow(3, -1, p)
        r = (4 * inv_3) % p
        
        # Order of r mod p
        ord_r = 1
        temp = r
        while temp != 1:
            temp = (temp * r) % p
            ord_r += 1
        
        print(f"  p = {p}: ord_p(4/3) = {ord_r} (divides Φ_{ord_r})")
    
    # Check covering property
    blocked_by = {p: [] for p in factors.keys()}
    not_blocked = []
    
    for seq in product(range(1, min(S, 7)), repeat=m):
        if sum(seq) != S:
            continue
        if seq == tuple([2]*m):
            continue
        
        s = [0]
        for a in seq:
            s.append(s[-1] + a)
        epsilon = [s[i] - 2*i for i in range(m)]
        
        blocked = False
        for p in factors.keys():
            inv_3 = pow(3, -1, p)
            r = (4 * inv_3) % p
            inv_2 = pow(2, -1, p)
            
            total = 0
            for i in range(m):
                if epsilon[i] >= 0:
                    w = pow(2, epsilon[i], p)
                else:
                    w = pow(inv_2, -epsilon[i], p)
                total = (total + pow(r, i, p) * w) % p
            
            if total != 0:
                blocked_by[p].append(seq)
                blocked = True
        
        if not blocked:
            not_blocked.append(seq)
    
    print(f"\n  Blocking analysis:")
    for p in factors.keys():
        print(f"    p = {p}: blocks {len(blocked_by[p])} sequences")
    
    if not_blocked:
        print(f"  ✗ NOT BLOCKED: {not_blocked[:3]}")
    else:
        print(f"  ✓ All non-uniform blocked by at least one prime")

print("\nAnalyzing composite m:")
for m in [4, 6, 8, 9, 10, 12]:
    analyze_composite(m)
