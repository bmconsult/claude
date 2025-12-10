#!/usr/bin/env python3
"""
Compute S_ν distributions for Collatz cycle analysis.

S_ν = Σᵢ 3^{m-1-i} · 2^{bᵢ} where b₁ < b₂ < ... < bₘ = A

For each m, we compute:
1. D = 2^A - 3^m (the modulus)
2. All valid ν-sequences (ordered subsets ending at A)
3. Distribution of S_ν mod D
4. Statistical tests for uniformity
"""

from itertools import combinations
from collections import Counter
import math

def compute_D(A, m):
    """Compute D = 2^A - 3^m"""
    return (1 << A) - (3 ** m)

def compute_S_nu(b_sequence, m):
    """
    Compute S_ν = Σᵢ 3^{m-1-i} · 2^{bᵢ}
    b_sequence = (b₁, b₂, ..., bₘ) with b₁ < b₂ < ... < bₘ
    """
    S = 0
    for i, b_i in enumerate(b_sequence):
        # i goes 0 to m-1, so power of 3 is 3^{m-1-i}
        S += (3 ** (m - 1 - i)) * (1 << b_i)
    return S

def enumerate_sequences(A, m):
    """
    Enumerate all valid ν-sequences.
    These are m-element subsets of {1, 2, ..., A} where the largest element is A.
    Equivalently: choose m-1 elements from {1, ..., A-1}, then append A.
    """
    # Choose m-1 positions from {1, 2, ..., A-1}
    for combo in combinations(range(1, A), m - 1):
        yield combo + (A,)

def analyze_distribution(m, A=None):
    """
    Analyze S_ν distribution for given m.
    If A not specified, use A = ceil(m * log2(3)) + 1
    """
    if A is None:
        # A/m ≈ log₂(3) ≈ 1.585, so A ≈ 1.585*m
        A = int(math.ceil(m * math.log2(3))) + 1

    D = compute_D(A, m)

    if D <= 0:
        print(f"m={m}, A={A}: D = {D} <= 0, skipping")
        return None

    # Count S_ν mod D for each sequence
    residue_counts = Counter()
    total_sequences = 0

    for b_seq in enumerate_sequences(A, m):
        S_nu = compute_S_nu(b_seq, m)
        residue = S_nu % D
        residue_counts[residue] += 1
        total_sequences += 1

    # Compute statistics
    num_residues_hit = len(residue_counts)
    expected_per_residue = total_sequences / D if D > 0 else 0

    # Chi-squared statistic for uniformity
    chi_squared = 0
    for r in range(D):
        observed = residue_counts.get(r, 0)
        expected = expected_per_residue
        if expected > 0:
            chi_squared += (observed - expected) ** 2 / expected

    # Entropy
    entropy = 0
    for count in residue_counts.values():
        if count > 0:
            p = count / total_sequences
            entropy -= p * math.log2(p)

    max_entropy = math.log2(D) if D > 1 else 0

    # Check if 0 is hit (would indicate potential cycle)
    zero_count = residue_counts.get(0, 0)

    results = {
        'm': m,
        'A': A,
        'D': D,
        'total_sequences': total_sequences,
        'num_residues_hit': num_residues_hit,
        'coverage': num_residues_hit / D if D > 0 else 0,
        'expected_per_residue': expected_per_residue,
        'chi_squared': chi_squared,
        'entropy': entropy,
        'max_entropy': max_entropy,
        'entropy_ratio': entropy / max_entropy if max_entropy > 0 else 0,
        'zero_count': zero_count,
        'zero_expected': expected_per_residue,
        'residue_counts': residue_counts
    }

    return results

def print_results(results):
    """Pretty print analysis results"""
    if results is None:
        return

    print(f"\n{'='*60}")
    print(f"m = {results['m']}, A = {results['A']}")
    print(f"{'='*60}")
    print(f"D = 2^{results['A']} - 3^{results['m']} = {results['D']}")
    print(f"Total ν-sequences: {results['total_sequences']} = C({results['A']-1}, {results['m']-1})")
    print(f"Residues hit: {results['num_residues_hit']} / {results['D']} = {results['coverage']:.4f}")
    print(f"Expected per residue: {results['expected_per_residue']:.4f}")
    print(f"χ² statistic: {results['chi_squared']:.2f} (df = {results['D']-1})")
    print(f"Entropy: {results['entropy']:.4f} / {results['max_entropy']:.4f} = {results['entropy_ratio']:.4f}")
    print(f"Zero count: {results['zero_count']} (expected: {results['zero_expected']:.4f})")

    # Distribution summary
    counts = list(results['residue_counts'].values())
    if counts:
        print(f"Count range: [{min(counts)}, {max(counts)}]")
        print(f"Count mean: {sum(counts)/len(counts):.2f}")

    # Uniformity assessment
    if results['entropy_ratio'] > 0.99:
        print("Assessment: HIGHLY UNIFORM (entropy > 99% of max)")
    elif results['entropy_ratio'] > 0.95:
        print("Assessment: APPROXIMATELY UNIFORM (entropy > 95% of max)")
    elif results['entropy_ratio'] > 0.90:
        print("Assessment: MODERATELY UNIFORM (entropy > 90% of max)")
    else:
        print("Assessment: NON-UNIFORM (entropy < 90% of max)")

def main():
    """Run analysis for m = 3 to 12"""
    print("S_ν Distribution Analysis for Collatz Cycles")
    print("=" * 60)

    all_results = []

    for m in range(3, 13):
        # Compute appropriate A
        A = int(math.ceil(m * math.log2(3))) + 1

        # Check feasibility
        num_seq = math.comb(A - 1, m - 1)
        D = compute_D(A, m)

        if D <= 0:
            print(f"\nm={m}: D <= 0, skipping")
            continue

        if num_seq > 10_000_000:
            print(f"\nm={m}: {num_seq} sequences too large, skipping")
            continue

        results = analyze_distribution(m, A)
        if results:
            all_results.append(results)
            print_results(results)

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'m':>3} {'A':>3} {'D':>10} {'#seq':>10} {'coverage':>8} {'entropy%':>9} {'zero':>5}")
    print("-" * 80)
    for r in all_results:
        print(f"{r['m']:>3} {r['A']:>3} {r['D']:>10} {r['total_sequences']:>10} "
              f"{r['coverage']:>8.4f} {r['entropy_ratio']*100:>8.2f}% {r['zero_count']:>5}")

    return all_results

if __name__ == "__main__":
    results = main()
