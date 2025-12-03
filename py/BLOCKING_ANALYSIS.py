"""
For composite m, Φ_m alone doesn't block all non-uniform.
But det = ∏_{d|m} Φ_d(4,3) should block everything.

Key question: Which factors are actually needed?

For m=4: det = Φ_1 · Φ_2 · Φ_4 = 1 · 7 · 25 = 175
For m=6: det = Φ_1 · Φ_2 · Φ_3 · Φ_6 = 1 · 7 · 37 · 13 = 3367

Let's see which factor blocks each non-uniform.
"""

from sympy import factorint, isprime, cyclotomic_poly, totient, divisors, symbols, gcd
import sympy

x = symbols('x')

def phi_d_value(d):
    """Compute Φ_d(4,3)."""
    phi_d = cyclotomic_poly(d, x)
    deg = totient(d)
    val = phi_d.subs(x, sympy.Rational(4, 3))
    return int(3**deg * val)

def compute_N(m, eps):
    """Compute N for a bridge ε (as rational * power of 2)."""
    # N = Σ 3^{m-1-i} · 2^{s_i} where s_i = 2i + ε_i
    # Scale by 2^{-min_s} to get integer
    min_eps = min(eps)
    min_s = min(2*i + eps[i] for i in range(m))
    
    N = 0
    for i in range(m):
        s_i = 2*i + eps[i]
        N += (3**(m-1-i)) * (2**(s_i - min_s))
    
    return N, min_s  # N_scaled, shift

def enumerate_bridges(m, max_height=4):
    """Enumerate valid bridges for m."""
    bridges = []
    
    def backtrack(pos, current):
        if pos == m:
            if current[-1] <= 1:
                bridges.append(tuple(current))
            return
        
        last = current[-1]
        for step in range(-1, max_height + 1):
            next_val = last + step
            if -max_height <= next_val <= max_height:
                remaining = m - 1 - pos
                if next_val - remaining <= 1:
                    current.append(next_val)
                    backtrack(pos + 1, current)
                    current.pop()
    
    backtrack(1, [0])
    return bridges

def analyze_blocking(m):
    """Analyze which Φ_d factors block each non-uniform bridge."""
    
    print(f"\n{'='*70}")
    print(f"m = {m}")
    print(f"{'='*70}")
    
    # Compute all Φ_d values
    divs = [d for d in divisors(m) if d > 1]
    phi_values = {d: phi_d_value(d) for d in divs}
    
    print(f"Divisors > 1: {divs}")
    print(f"Φ_d(4,3) values: {phi_values}")
    
    det = 1
    for d in divs:
        det *= phi_values[d]
    print(f"det = {det} = {factorint(det)}")
    
    bridges = enumerate_bridges(m)
    uniform = tuple([0] * m)
    non_uniform = [b for b in bridges if b != uniform]
    
    print(f"Total bridges: {len(bridges)}, non-uniform: {len(non_uniform)}")
    
    # For each non-uniform, find which Φ_d blocks it
    blocking_stats = {d: 0 for d in divs}
    all_blocked = True
    
    unblocked = []
    
    for eps in non_uniform:
        N, shift = compute_N(m, eps)
        
        blocked_by = []
        for d in divs:
            phi_d = phi_values[d]
            # Check if Φ_d | N (as integer, ignoring 2-power)
            if N % phi_d == 0:
                pass  # Not blocked by Φ_d
            else:
                blocked_by.append(d)
        
        if blocked_by:
            for d in blocked_by:
                blocking_stats[d] += 1
        else:
            all_blocked = False
            unblocked.append((eps, N))
    
    print(f"\nBlocking statistics (how many non-uniform each Φ_d blocks):")
    for d in divs:
        pct = 100 * blocking_stats[d] / len(non_uniform) if non_uniform else 0
        print(f"  Φ_{d}: blocks {blocking_stats[d]}/{len(non_uniform)} ({pct:.1f}%)")
    
    if unblocked:
        print(f"\n⚠ {len(unblocked)} UNBLOCKED non-uniform bridges!")
        for eps, N in unblocked[:10]:
            print(f"  ε = {eps}, N = {N}")
            # Check divisibility by each factor
            for d in divs:
                phi_d = phi_values[d]
                if N % phi_d == 0:
                    print(f"    Φ_{d} = {phi_d} DIVIDES N")
    else:
        print(f"\n✓ ALL non-uniform blocked!")
        
        # Find minimal blocking set
        print("\nFinding minimal blocking set...")
        from itertools import combinations
        
        for size in range(1, len(divs) + 1):
            for subset in combinations(divs, size):
                blocks_all = True
                for eps in non_uniform:
                    N, _ = compute_N(m, eps)
                    blocked = False
                    for d in subset:
                        if N % phi_values[d] != 0:
                            blocked = True
                            break
                    if not blocked:
                        blocks_all = False
                        break
                
                if blocks_all:
                    print(f"  Minimal blocking set: {subset}")
                    print(f"  Product: {sympy.prod([phi_values[d] for d in subset])}")
                    return subset
    
    return None

# Test for small composite m
for m in [4, 6, 8, 9, 10, 12]:
    analyze_blocking(m)

print("\n" + "="*70)
print("KEY INSIGHT")
print("="*70)

print("""
For composite m, we need MULTIPLE Φ_d factors working together.

The question is: can we prove algebraically that the combination always works?

Key observation: Each Φ_d tests a different "periodicity" of the bridge.

For m=6 with divisors 2, 3, 6:
- Φ_2 tests: do positions 0,2,4 vs 1,3,5 have equal weighted sums?
- Φ_3 tests: do positions 0,3 vs 1,4 vs 2,5 have equal weighted sums?  
- Φ_6 tests: the primitive 6th root constraint

Together these constrain all frequencies except 0.
""")
