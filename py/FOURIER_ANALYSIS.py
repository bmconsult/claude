"""
THE FOURIER PERSPECTIVE ON CYCLOTOMIC BLOCKING

Key insight: Each Φ_d constraint blocks certain DFT frequencies.

For a sequence c = (c_0, c_1, ..., c_{m-1}), define:
    ĉ_k = Σ_{j=0}^{m-1} c_j · ω^{jk}  where ω = e^{2πi/m}

The constraint "Φ_d | C(x)" where C(x) = Σ c_j x^j means:
    C(ζ) = 0 for all primitive d-th roots ζ

Since primitive d-th roots of unity are {ω^{km/d} : gcd(k, d) = 1}:
    C(ω^{km/d}) = 0 for all k with gcd(k, d) = 1

This means: ĉ_{km/d} = 0 for k coprime to d.

So Φ_d blocks frequencies {km/d : 1 ≤ k < d, gcd(k,d) = 1}.

THEOREM: For any m, the union over all prime powers p^a || m of the 
frequencies blocked by Φ_{p^a} covers all non-zero frequencies 1, 2, ..., m-1.

PROOF: 
For each frequency f ∈ {1, ..., m-1}, write f = (m/d) · k where d | m and gcd(k, d) = 1.
Take the largest such d. Then d is a prime power dividing m, and Φ_d blocks frequency f.
"""

from sympy import divisors, gcd, isprime, factorint, totient
from collections import defaultdict

def frequencies_blocked_by_phi_d(m, d):
    """Return the set of frequencies blocked by Φ_d for an m-cycle."""
    # Φ_d blocks frequencies f = (m/d) * k for k coprime to d, 1 ≤ k < d
    blocked = set()
    for k in range(1, d):
        if gcd(k, d) == 1:
            f = (m // d) * k
            if 1 <= f <= m - 1:
                blocked.add(f)
    return blocked

def prime_power_divisors(m):
    """Return all prime power divisors p^a of m."""
    factors = factorint(m)
    pp_divs = []
    for p, a in factors.items():
        for e in range(1, a + 1):
            pp_divs.append(p ** e)
    return pp_divs

def analyze_frequency_coverage(m):
    """Analyze which frequencies each Φ_d blocks."""
    
    print(f"\n{'='*70}")
    print(f"m = {m}")
    print(f"{'='*70}")
    
    all_freqs = set(range(1, m))
    print(f"All non-zero frequencies: {sorted(all_freqs)}")
    
    pp_divs = prime_power_divisors(m)
    print(f"Prime power divisors: {pp_divs}")
    
    coverage = defaultdict(set)
    total_covered = set()
    
    for d in sorted(divisors(m)):
        if d == 1:
            continue
        blocked = frequencies_blocked_by_phi_d(m, d)
        coverage[d] = blocked
        if blocked:
            print(f"  Φ_{d} blocks frequencies: {sorted(blocked)}")
    
    # Check coverage by prime powers only
    pp_covered = set()
    for d in pp_divs:
        pp_covered |= coverage[d]
    
    print(f"\nPrime power divisors cover: {sorted(pp_covered)}")
    missing = all_freqs - pp_covered
    if missing:
        print(f"  ⚠ MISSING: {sorted(missing)}")
    else:
        print(f"  ✓ All frequencies covered by prime powers!")
    
    return len(missing) == 0

print("FREQUENCY COVERAGE ANALYSIS")
print("="*70)
print("""
If prime power divisors cover all frequencies, then:
- Φ_{p^a} constraints for each p^a || m together force all ĉ_k = 0 for k ≠ 0
- Combined with c_0 = 0 (since ε_0 = 0), this forces c = 0
- Hence ε = uniform!
""")

all_covered = True
for m in range(2, 25):
    if not analyze_frequency_coverage(m):
        all_covered = False

print("\n" + "="*70)
print("THEOREM VERIFICATION")
print("="*70)

if all_covered:
    print("""
✓ VERIFIED: For all m from 2 to 24, prime power divisors cover all frequencies!

This gives us the algebraic proof:

THEOREM: For any m ≥ 2 and any non-uniform bridge ε, det ∤ N_ε.

PROOF:

1. Let c_j = 2^{ε_j} - 1 be the perturbation sequence.
   Note c_0 = 0 since ε_0 = 0.

2. For non-uniform ε, we need to show: some Φ_d(4,3) ∤ N.
   Equivalently: C(ζ) ≠ 0 for some primitive d-th root ζ.

3. In terms of DFT: ĉ_f ≠ 0 for some frequency f ∈ {1, ..., m-1}.

4. For each prime power p^a exactly dividing m:
   - Φ_{p^a} constraint forces ĉ_f = 0 for frequencies f blocked by Φ_{p^a}
   
5. The prime power divisors together cover ALL frequencies {1, ..., m-1}.

6. So if all Φ_{p^a} | C, then all ĉ_f = 0 for f ≠ 0.

7. Combined with ĉ_0 = Σ c_j = Σ (2^{ε_j} - 1) and c_0 = 0, we get...

Wait, ĉ_0 is NOT necessarily 0 for non-uniform!

Let me reconsider...
""")

# Let's check the c_0 = ĉ_0 constraint
print("\n" + "="*70)
print("ANALYZING THE ĉ_0 CONSTRAINT")
print("="*70)

print("""
The DFT at frequency 0 is:
    ĉ_0 = Σ_{j=0}^{m-1} c_j = Σ (2^{ε_j} - 1) = Σ 2^{ε_j} - m

For uniform: Σ 2^0 - m = m - m = 0 ✓

For non-uniform: ĉ_0 = Σ 2^{ε_j} - m

This is NOT necessarily 0!

But wait - this is the WRONG equation. Let me reconsider the constraint.

The actual constraint is: Σ r^j · 2^{ε_j} ≡ 0 (mod p)

where r = 4/3 mod p is a primitive m-th root of unity mod p.

This is NOT the same as C(ζ) = 0 for complex ζ!

Let me be more careful...
""")

print("\n" + "="*70)
print("CORRECT FORMULATION")
print("="*70)

print("""
The constraint at prime p | Φ_d(4,3) with ord_p(4/3) = d is:

    Σ_{j=0}^{m-1} r^j · 2^{ε_j} ≡ 0 (mod p)

where r ≡ 4/3 (mod p) satisfies r^d ≡ 1.

Let's write this differently. Group by cosets of the d-cycle:

    Σ_{k=0}^{d-1} r^k · (Σ_{ℓ: ℓ≡k mod d} 2^{ε_ℓ}) ≡ 0 (mod p)

Define S_k = Σ_{ℓ≡k mod d} 2^{ε_ℓ} for k = 0, 1, ..., d-1.

The constraint becomes: Σ_{k=0}^{d-1} r^k · S_k ≡ 0 (mod p)

Since r is a primitive d-th root mod p, and using polynomial argument:

Define Q(x) = Σ_{k=0}^{d-1} S_k x^k.

We have Q(r) ≡ 0 (mod p).

For PRIME d: deg(Φ_d) = d-1 = deg(Q), so Q = α·Φ_d for some α.
Comparing constant terms: S_0 = α · Φ_d(0) = α · 1 = α.

So Q = S_0 · Φ_d.

For uniform: S_k = m/d for all k, so Q = (m/d) · Σ x^k = (m/d) · (x^d - 1)/(x - 1).
This is divisible by Φ_d since (x^d - 1) = Φ_d · Φ_1 · ... and Φ_1 = x - 1.

Wait, let me reconsider. For uniform:
    S_k = m/d for all k (each coset has m/d elements, each contributing 2^0 = 1)
    Q(x) = (m/d) · (1 + x + x^2 + ... + x^{d-1}) = (m/d) · Σ_{k=0}^{d-1} x^k
    
For x = r (primitive d-th root): Σ r^k = 0 ✓

For non-uniform: the S_k are NOT all equal (unless there's a special structure).

The polynomial argument says: if Q(r) = 0 for prime d, then all S_k are equal.

KEY INSIGHT: For prime d, the constraint Φ_d | ... forces all d-coset sums S_k equal!

For composite m with prime divisors p_1, ..., p_t:
- Φ_{p_1} forces all p_1-coset sums equal
- Φ_{p_2} forces all p_2-coset sums equal
- etc.

Together, do these force ε = uniform?
""")

# Let's verify this claim
print("\n" + "="*70)
print("VERIFYING: PRIME DIVISOR COSET CONSTRAINTS")
print("="*70)

def coset_sums(m, d, eps):
    """Compute d-coset sums for bridge ε."""
    sums = [0] * d
    for j in range(m):
        k = j % d
        sums[k] += 2 ** eps[j]
    return tuple(sums)

def all_equal(lst):
    return len(set(lst)) == 1

def test_prime_coset_constraints(m):
    """Test if equal coset sums at all prime divisors implies uniform."""
    
    # Get prime divisors
    primes = [p for p in factorint(m).keys()]
    print(f"\nm = {m}, prime divisors = {primes}")
    
    # Enumerate bridges
    bridges = []
    def backtrack(pos, current):
        if pos == m:
            if current[-1] <= 1:
                bridges.append(tuple(current))
            return
        last = current[-1]
        for step in range(-1, 4):
            next_val = last + step
            if -4 <= next_val <= 4:
                remaining = m - 1 - pos
                if next_val - remaining <= 1:
                    current.append(next_val)
                    backtrack(pos + 1, current)
                    current.pop()
    backtrack(1, [0])
    
    uniform = tuple([0] * m)
    
    # Find bridges where ALL prime divisors have equal coset sums
    passing = []
    for eps in bridges:
        passes_all = True
        for p in primes:
            sums = coset_sums(m, p, eps)
            if not all_equal(sums):
                passes_all = False
                break
        if passes_all:
            passing.append(eps)
    
    non_uniform_passing = [e for e in passing if e != uniform]
    
    if non_uniform_passing:
        print(f"  ⚠ {len(non_uniform_passing)} non-uniform pass ALL prime coset tests!")
        for eps in non_uniform_passing[:5]:
            print(f"    {eps}")
            for p in primes:
                print(f"      {p}-cosets: {coset_sums(m, p, eps)}")
        return False
    else:
        print(f"  ✓ Only uniform passes all prime coset tests!")
        return True

for m in [4, 6, 8, 9, 10, 12, 15, 18, 20]:
    test_prime_coset_constraints(m)
