#!/usr/bin/env python3
"""
Compute Gowers U² norms for S_ν distribution (pure Python, no numpy).
"""

from itertools import combinations
import math
import cmath

def compute_S_nu_distribution(m, A):
    """Return distribution f(r) as dict"""
    D = (1 << A) - (3 ** m)
    if D <= 0:
        return None, None, D
    
    # Count S_ν mod D
    counts = {}
    N = 0
    
    for combo in combinations(range(1, A), m - 1):
        b_seq = combo + (A,)
        S = sum((3 ** (m - 1 - i)) * (1 << b_seq[i]) for i in range(m))
        r = S % D
        counts[r] = counts.get(r, 0) + 1
        N += 1
    
    return counts, N, D

def compute_dft(counts, N, D):
    """Compute DFT of f - 1/D at frequencies α = 1, ..., D-1"""
    # ĝ(α) = Σ_r (f(r) - 1/D) * e^{-2πi αr/D}
    #      = (1/N) Σ_r counts[r] * e^{-2πi αr/D} - (1/D) Σ_r e^{-2πi αr/D}
    # The second sum = 0 for α ≠ 0
    # So ĝ(α) = (1/N) Σ_r counts[r] * e^{-2πi αr/D} for α ≠ 0
    
    g_hat = []
    for alpha in range(1, D):  # α = 1, ..., D-1
        total = 0
        for r, count in counts.items():
            phase = cmath.exp(-2j * math.pi * alpha * r / D)
            total += count * phase
        g_hat.append(total / N)  # f̂(α) = (1/N) Σ counts * phase
    
    return g_hat

def compute_gowers_U2(g_hat, D):
    """Compute ||g||_{U²}⁴ = (1/D) Σ |ĝ(α)|⁴"""
    sum_fourth = sum(abs(g)**4 for g in g_hat)
    U2_fourth = sum_fourth / D
    U2 = U2_fourth ** 0.25
    return U2, U2_fourth

def compute_character_sums(g_hat, N, D):
    """C(α) = N * ĝ(α), check |C(α)| ≤ √N"""
    C_values = [abs(g * N) for g in g_hat]
    max_C = max(C_values)
    avg_C = sum(C_values) / len(C_values)
    sqrt_N = math.sqrt(N)
    return max_C, avg_C, sqrt_N, max_C / sqrt_N

def main():
    print("Gowers U² Norm Analysis for S_ν Distribution")
    print("=" * 80)
    
    results = []
    
    for m in range(3, 11):  # limit to m≤10 for speed without numpy
        A = int(math.ceil(m * math.log2(3))) + 1
        
        counts, N, D = compute_S_nu_distribution(m, A)
        if counts is None:
            continue
        
        if N > 50000 or D > 100000:
            print(f"m={m}: N={N}, D={D} too large for pure Python DFT, skipping")
            continue
        
        print(f"\nm={m}, A={A}, N={N}, D={D} ... computing DFT", end="", flush=True)
        g_hat = compute_dft(counts, N, D)
        print(" done")
        
        U2, U2_fourth = compute_gowers_U2(g_hat, D)
        max_C, avg_C, sqrt_N, ratio = compute_character_sums(g_hat, N, D)
        
        zero_count = counts.get(0, 0)
        
        results.append({
            'm': m, 'A': A, 'N': N, 'D': D,
            'U2': U2, 'max_C': max_C, 'sqrt_N': sqrt_N, 'ratio': ratio,
            'zero': zero_count
        })
        
        print(f"  ||g||_U² = {U2:.6f}")
        print(f"  max|C(α)| = {max_C:.2f}, √N = {sqrt_N:.2f}, ratio = {ratio:.4f}")
        status = "✓ SQUARE-ROOT CANCEL" if ratio < 1 else ("~ near" if ratio < 2 else "✗ no cancel")
        print(f"  Status: {status}")
        print(f"  Zero count: {zero_count}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"{'m':>3} {'N':>7} {'D':>8} {'||g||_U²':>10} {'|C|/√N':>8} {'zero':>5}")
    print("-" * 50)
    for r in results:
        print(f"{r['m']:>3} {r['N']:>7} {r['D']:>8} {r['U2']:>10.6f} {r['ratio']:>8.4f} {r['zero']:>5}")
    
    # Trend analysis
    if len(results) >= 3:
        print("\n" + "=" * 80)
        print("TREND ANALYSIS")
        print("=" * 80)
        
        # Simple exponential fit: log(U2) = a*m + b
        m_vals = [r['m'] for r in results]
        log_u2 = [math.log(r['U2']) for r in results]
        
        n = len(m_vals)
        sum_m = sum(m_vals)
        sum_log = sum(log_u2)
        sum_m2 = sum(m**2 for m in m_vals)
        sum_m_log = sum(m_vals[i]*log_u2[i] for i in range(n))
        
        slope = (n*sum_m_log - sum_m*sum_log) / (n*sum_m2 - sum_m**2)
        intercept = (sum_log - slope*sum_m) / n
        
        print(f"Fit: log(||g||_U²) ≈ {slope:.4f}*m + {intercept:.4f}")
        decay_rate = math.exp(slope)
        print(f"     ||g||_U² ≈ {math.exp(intercept):.4f} × {decay_rate:.4f}^m")
        
        if slope < 0:
            print(f"\n✓ U² DECREASES exponentially with m!")
            print(f"  Decay rate: {decay_rate:.4f} per step")
            print(f"  Extrapolated U²(m=50) ≈ {math.exp(intercept + slope*50):.2e}")
            print(f"  Extrapolated U²(m=100) ≈ {math.exp(intercept + slope*100):.2e}")
    
    return results

if __name__ == "__main__":
    results = main()
