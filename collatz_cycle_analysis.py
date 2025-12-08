#!/usr/bin/env python3
"""
Collatz Cycle Analysis Tool

Analyzes potential cycles at convergents (k, q) where 2^k ≈ 3^q.

For a hypothetical q-odd-step cycle with k total divisions:
  n × (2^k - 3^q) = C

where C is the correction term from +1 contributions.

Three levels of constraint:
1. C ≡ 0 (mod D) where D = 2^k - 3^q  [NECESSARY]
2. C divisible by all foreign primes of D  [NECESSARY]
3. k-sequence compatible with resulting n  [SUFFICIENT]

Usage:
  python collatz_cycle_analysis.py [k] [q]

Example:
  python collatz_cycle_analysis.py 8 5
"""

import sys
from math import comb, gcd, log2
from functools import reduce

def prime_factors(n):
    """Return prime factors of |n| as dict {p: exponent}"""
    n = abs(n)
    if n <= 1:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def foreign_primes(n):
    """Return list of prime factors of n that are not 2 or 3"""
    factors = prime_factors(n)
    return [p for p in factors.keys() if p not in (2, 3)]

def enumerate_k_sequences(k_total, q):
    """
    Enumerate all k-sequences [k_1, ..., k_q] where:
    - sum = k_total
    - each k_i >= 1
    - length = q
    """
    if k_total < q:
        return

    def helper(remaining, num_left, current):
        if num_left == 0:
            if remaining == 0:
                yield tuple(current)
            return
        min_val = 1
        max_val = remaining - (num_left - 1)
        for val in range(min_val, max_val + 1):
            yield from helper(remaining - val, num_left - 1, current + [val])

    yield from helper(k_total, q, [])

def compute_C(k_sequence):
    """
    Compute correction term C for a given k-sequence.

    C = Σᵢ 3^{q-i-1} × 2^{k - Σⱼ≤ᵢ kⱼ}
    """
    q = len(k_sequence)
    k = sum(k_sequence)
    C = 0
    cumsum = 0
    for i, ki in enumerate(k_sequence):
        cumsum += ki
        weight = (3 ** (q - i - 1)) * (2 ** (k - cumsum))
        C += weight
    return C

def compute_C_mod_p(k_sequence, p):
    """Compute C mod p efficiently using modular arithmetic"""
    q = len(k_sequence)
    k = sum(k_sequence)
    C_mod = 0
    cumsum = 0
    for i, ki in enumerate(k_sequence):
        cumsum += ki
        weight_mod = pow(3, q - i - 1, p) * pow(2, k - cumsum, p) % p
        C_mod = (C_mod + weight_mod) % p
    return C_mod

def verify_cycle(n, k_sequence):
    """
    Verify if n actually forms a cycle with the given k-sequence.

    Returns (is_valid, trajectory, error_msg)
    """
    if n <= 0:
        return False, [], f"n={n} is not positive"

    current = n
    trajectory = [current]

    for i, ki in enumerate(k_sequence):
        # Apply 3n+1
        current = 3 * current + 1
        trajectory.append(current)

        # Check if we can divide by 2 exactly ki times
        v2 = 0
        temp = current
        while temp % 2 == 0:
            v2 += 1
            temp //= 2

        if v2 < ki:
            return False, trajectory, f"At step {i+1}: ν₂({current}) = {v2} < k_{i+1} = {ki}"

        # Apply divisions
        for j in range(ki):
            current //= 2
            trajectory.append(current)

    if current == n:
        return True, trajectory, "Cycle closes!"
    else:
        return False, trajectory, f"Does not return: ended at {current}, started at {n}"

def analyze_convergent(k, q, verbose=True):
    """
    Analyze a convergent (k, q) for potential cycles.

    Returns dict with analysis results.
    """
    D = 2**k - 3**q

    result = {
        'k': k,
        'q': q,
        'D': D,
        'foreign_primes': [],
        'num_sequences': 0,
        'divisibility_candidates': [],
        'valid_cycles': [],
        'status': 'unknown'
    }

    if verbose:
        print(f"\n{'='*70}")
        print(f"CONVERGENT (k={k}, q={q})")
        print(f"{'='*70}")
        print(f"D = 2^{k} - 3^{q} = {D}")

    if D <= 0:
        result['status'] = 'invalid_D'
        if verbose:
            print(f"D ≤ 0: Not valid for positive cycles")
        return result

    if D == 1:
        result['status'] = 'trivial'
        if verbose:
            print(f"D = 1: Trivial cycle (n=1)")
        return result

    fp = foreign_primes(D)
    result['foreign_primes'] = fp

    if verbose:
        factors = prime_factors(D)
        factor_strs = [f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items())]
        print(f"Factorization: {' × '.join(factor_strs)}")
        print(f"Foreign primes: {fp if fp else 'None'}")

    # Count sequences
    num_seq = comb(k-1, q-1) if k >= q else 0
    result['num_sequences'] = num_seq

    if verbose:
        print(f"Number of k-sequences: {num_seq}")

    if num_seq > 10_000_000:
        result['status'] = 'too_many_sequences'
        if verbose:
            print(f"Too many sequences to enumerate")
        return result

    # Find candidates where C ≡ 0 (mod D)
    candidates = []
    for k_seq in enumerate_k_sequences(k, q):
        C = compute_C(k_seq)
        if C % D == 0:
            n = C // D
            candidates.append((k_seq, C, n))

    result['divisibility_candidates'] = candidates

    if verbose:
        print(f"\nCandidates with C ≡ 0 (mod D): {len(candidates)}")

    if not candidates:
        result['status'] = 'ruled_out_divisibility'
        if verbose:
            print(f"✓ RULED OUT: No k-sequence has C divisible by D")
        return result

    # Verify each candidate
    valid_cycles = []
    for k_seq, C, n in candidates:
        is_valid, trajectory, msg = verify_cycle(n, k_seq)
        if verbose:
            print(f"\n  k-seq {k_seq}, n={n}: {msg}")
            if len(trajectory) <= 20:
                print(f"    Trajectory: {' → '.join(map(str, trajectory))}")
        if is_valid:
            valid_cycles.append((k_seq, n, trajectory))

    result['valid_cycles'] = valid_cycles

    if valid_cycles:
        result['status'] = 'cycles_found'
        if verbose:
            print(f"\n⚠ FOUND {len(valid_cycles)} VALID CYCLE(S)!")
    else:
        result['status'] = 'ruled_out_verification'
        if verbose:
            print(f"\n✓ RULED OUT: All candidates fail cycle verification")

    return result

def get_convergents(n_terms=15):
    """Get convergents to log_2(3)"""
    x = log2(3)
    cf = []
    for _ in range(n_terms):
        cf.append(int(x))
        frac = x - int(x)
        if frac < 1e-10:
            break
        x = 1/frac

    convs = []
    p_prev, p_curr = 0, 1
    q_prev, q_curr = 1, 0
    for a in cf:
        p_new = a * p_curr + p_prev
        q_new = a * q_curr + q_prev
        convs.append((p_new, q_new))
        p_prev, p_curr = p_curr, p_new
        q_prev, q_curr = q_curr, q_new
    return convs

def main():
    if len(sys.argv) == 3:
        k, q = int(sys.argv[1]), int(sys.argv[2])
        analyze_convergent(k, q)
    else:
        print("COLLATZ CYCLE ANALYSIS")
        print("="*70)
        print("\nAnalyzing convergents to log_2(3)...")

        convs = get_convergents()

        print("\nConvergent | D | Status")
        print("-"*70)

        for k, q in convs[:10]:
            result = analyze_convergent(k, q, verbose=False)
            D_str = str(result['D'])[:20] + "..." if len(str(result['D'])) > 20 else str(result['D'])
            print(f"({k:3d},{q:3d}) | {D_str:25s} | {result['status']}")

        print("\n" + "="*70)
        print("Detailed analysis of positive convergents:")

        for k, q in convs[:10]:
            D = 2**k - 3**q
            if D > 0:
                analyze_convergent(k, q)

if __name__ == "__main__":
    main()
