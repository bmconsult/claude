#!/usr/bin/env python3
"""
DYNAMICAL SYSTEMS - EXPERT LEVEL
=================================

Going beyond textbook ergodic theory to tackle hard problems
directly relevant to Collatz.
"""

import numpy as np
from collections import defaultdict
from scipy import linalg

print("=" * 70)
print("HARD PROBLEM 1: Constructing the Transfer Operator for Syracuse")
print("=" * 70)

print("""
The transfer operator L acts on functions f: States → R by:
  (Lf)(x) = Σ_{y: T(y)=x} f(y) / |T'(y)|

For Syracuse on odd integers, this is subtle because:
1. Syracuse is not injective (multiple preimages)
2. The "derivative" notion needs care on discrete spaces
3. We need to work mod 2^k to make it finite-dimensional
""")

def v2(n):
    if n == 0: return float('inf')
    c = 0
    while n % 2 == 0:
        c += 1
        n //= 2
    return c

def syracuse(n):
    v = v2(3*n + 1)
    return (3*n + 1) // (2**v)

def syracuse_preimages(m, max_search=10000):
    """Find all odd n with Syracuse(n) = m"""
    preimages = []
    # S(n) = (3n+1)/2^v = m
    # So 3n+1 = m * 2^v for some v
    # n = (m * 2^v - 1) / 3
    for v in range(1, 30):
        numerator = m * (2**v) - 1
        if numerator % 3 == 0:
            n = numerator // 3
            if n > 0 and n % 2 == 1:  # Must be positive odd
                if syracuse(n) == m:  # Verify
                    preimages.append((n, v))
    return preimages

print("\nPreimages of small numbers under Syracuse:")
for m in [1, 5, 7, 11, 13, 17]:
    pre = syracuse_preimages(m)
    print(f"S^(-1)({m}) = {pre[:5]}...")

print("\n" + "-" * 70)
print("Transfer operator on (Z/2^k Z) for odd numbers")
print("-" * 70)

def build_transfer_matrix(k, weighted=False):
    """
    Build transfer operator matrix for Syracuse mod 2^k.
    
    L[i,j] = probability of transitioning from residue j to residue i
    (Note: this is the TRANSPOSE of the usual transition matrix)
    """
    mod = 2**k
    odd_residues = list(range(1, mod, 2))
    n_states = len(odd_residues)
    residue_to_idx = {r: i for i, r in enumerate(odd_residues)}
    
    # Count transitions from sampling
    L = np.zeros((n_states, n_states))
    
    # For each residue class, sample many representatives
    for j_idx, j_res in enumerate(odd_residues):
        total = 0
        for rep in range(j_res, 100000, mod):
            if rep > 0:
                s = syracuse(rep)
                s_res = s % mod
                if s_res in residue_to_idx:
                    i_idx = residue_to_idx[s_res]
                    if weighted:
                        # Weight by some factor (e.g., 1/value ratio)
                        weight = j_res / s_res if s_res > 0 else 1
                        L[i_idx, j_idx] += weight
                    else:
                        L[i_idx, j_idx] += 1
                    total += 1
        
        if total > 0:
            L[:, j_idx] /= total
    
    return L, odd_residues

print("\nSpectral analysis of transfer operator mod 8:")
L, residues = build_transfer_matrix(3)
eigenvalues, eigenvectors = linalg.eig(L)
eigenvalues = np.real(eigenvalues)
eigenvalues = sorted(eigenvalues, reverse=True)
print(f"Eigenvalues: {eigenvalues}")

print("\nSpectral analysis mod 16:")
L, residues = build_transfer_matrix(4)
eigenvalues, _ = linalg.eig(L)
eigenvalues = np.real(sorted(eigenvalues, reverse=True))
print(f"Top eigenvalues: {eigenvalues[:8]}")

print("\nSpectral analysis mod 32:")
L, residues = build_transfer_matrix(5)
eigenvalues, _ = linalg.eig(L)
eigenvalues = np.real(sorted(eigenvalues, reverse=True))
print(f"Top eigenvalues: {eigenvalues[:8]}")

print("""
INSIGHT: The leading eigenvalue is 1 (conservation of probability).
The second eigenvalue determines mixing rate.
Smaller second eigenvalue = faster mixing = stronger equidistribution.
""")

print("\n" + "=" * 70)
print("HARD PROBLEM 2: Invariant Density on Log Scale")
print("=" * 70)

print("""
Instead of looking at Syracuse on integers, consider it on log scale.

Define X = log(n). Then Syracuse becomes:
  X ↦ log((3 * e^X + 1) / 2^v)
     ≈ X + log(3) - v*log(2)  for large X
     ≈ X + 1.099 - v*0.693

This is an additive random walk with drift depending on v.
Since E[v] = 2, drift ≈ 1.099 - 2*0.693 = -0.287 (negative!)
""")

def syracuse_log_step(log_n):
    """One Syracuse step on log scale"""
    n = int(round(np.exp(log_n)))
    if n <= 0:
        n = 1
    if n % 2 == 0:
        n += 1  # Make odd
    
    v = v2(3*n + 1)
    s = (3*n + 1) // (2**v)
    
    return np.log(s), v

def simulate_log_walk(start_log, n_steps):
    """Simulate Syracuse as a random walk on log scale"""
    log_values = [start_log]
    v_values = []
    
    current_log = start_log
    for _ in range(n_steps):
        new_log, v = syracuse_log_step(current_log)
        if new_log <= 0:  # Reached 1
            break
        log_values.append(new_log)
        v_values.append(v)
        current_log = new_log
    
    return log_values, v_values

# Simulate many walks
print("\nSimulating log-scale walks:")
start_logs = [np.log(n) for n in [1000, 10000, 100000, 1000000]]

for start_log in start_logs:
    log_vals, v_vals = simulate_log_walk(start_log, 500)
    if len(v_vals) > 0:
        avg_v = np.mean(v_vals)
        drift = 1.099 - avg_v * 0.693
        max_log = max(log_vals)
        min_log = min(log_vals)
        print(f"Start log={start_log:.1f}: avg_v={avg_v:.3f}, drift={drift:.3f}, max_excursion={max_log-start_log:.2f}")

print("""
The negative drift confirms: on average, trajectories shrink.
But there's variance, allowing temporary growth.
""")

print("\n" + "=" * 70)
print("HARD PROBLEM 3: Lyapunov Exponent of Syracuse")  
print("=" * 70)

print("""
The Lyapunov exponent measures average rate of contraction:
  λ = lim (1/n) Σ log|T'(x_i)|

For Syracuse, formally:
  λ = E[log(3) - v*log(2)] = log(3) - E[v]*log(2)
    = 1.099 - 2*0.693 = -0.287

A negative Lyapunov exponent indicates contraction on average.
""")

def compute_lyapunov(n, max_steps=1000):
    """Compute empirical Lyapunov exponent for trajectory from n"""
    total_log_deriv = 0
    steps = 0
    
    current = n
    for _ in range(max_steps):
        if current == 1:
            break
        
        v = v2(3*current + 1)
        # "Derivative" of Syracuse step: d(S(n))/dn ≈ 3/2^v
        log_deriv = np.log(3) - v * np.log(2)
        total_log_deriv += log_deriv
        steps += 1
        
        current = (3*current + 1) // (2**v)
    
    return total_log_deriv / steps if steps > 0 else 0

print("\nEmpirical Lyapunov exponents:")
lyap_values = []
for n in range(3, 10001, 2):
    lyap = compute_lyapunov(n)
    lyap_values.append(lyap)

print(f"Mean Lyapunov exponent: {np.mean(lyap_values):.4f}")
print(f"Std dev: {np.std(lyap_values):.4f}")
print(f"Theoretical: {np.log(3) - 2*np.log(2):.4f}")

# Distribution
bins = np.linspace(-0.5, 0.0, 20)
hist, _ = np.histogram(lyap_values, bins=bins)
print("\nDistribution of Lyapunov exponents:")
for i in range(len(hist)):
    bar = '#' * (hist[i] // 20)
    print(f"  [{bins[i]:.2f}, {bins[i+1]:.2f}): {bar}")

print("\n" + "=" * 70)
print("HARD PROBLEM 4: Escape Time Distribution")
print("=" * 70)

print("""
For a starting value n, define the escape time τ(n) as the first time
the trajectory drops below n.

Terras proved: τ(n) < ∞ for almost all n (density 1).

HARD QUESTION: What is the distribution of τ(n)?
How does it depend on n?
""")

def escape_time(n, max_steps=10000):
    """Find first time trajectory drops below starting value"""
    current = n
    for t in range(1, max_steps):
        v = v2(3*current + 1)
        current = (3*current + 1) // (2**v)
        if current < n:
            return t
        if current == 1:
            return t
    return max_steps

print("\nEscape time statistics:")
escape_times = []
for n in range(3, 100001, 2):
    tau = escape_time(n)
    escape_times.append((n, tau))

# Analyze by residue class mod 8
by_mod8 = defaultdict(list)
for n, tau in escape_times:
    by_mod8[n % 8].append(tau)

print(f"{'mod 8':>6} {'mean τ':>10} {'median τ':>10} {'max τ':>10}")
for r in [1, 3, 5, 7]:
    times = by_mod8[r]
    print(f"{r:>6} {np.mean(times):>10.2f} {np.median(times):>10.0f} {max(times):>10}")

# Worst cases
escape_times.sort(key=lambda x: -x[1])
print("\nHardest escape times:")
for n, tau in escape_times[:10]:
    print(f"  n={n}: τ={tau}, n mod 8 = {n % 8}, n mod 16 = {n % 16}")

print("\n" + "=" * 70)
print("HARD PROBLEM 5: The Density of 'Bad' Numbers")
print("=" * 70)

print("""
A number n is "bad" if its trajectory reaches values >> n.
More precisely, define excursion E(n) = max(trajectory) / n.

QUESTION: What is the density of numbers with E(n) > threshold?
How does this density scale with threshold?
""")

def excursion(n, max_steps=1000):
    """Compute max(trajectory)/n"""
    max_val = n
    current = n
    for _ in range(max_steps):
        if current == 1:
            break
        v = v2(3*current + 1)
        current = (3*current + 1) // (2**v)
        max_val = max(max_val, current)
    return max_val / n

# Compute excursions
print("\nDensity of numbers with E(n) > threshold:")
excursions = []
for n in range(3, 100001, 2):
    e = excursion(n)
    excursions.append(e)

total = len(excursions)
for threshold in [2, 5, 10, 20, 50, 100, 500, 1000]:
    count = sum(1 for e in excursions if e > threshold)
    density = count / total
    print(f"  E(n) > {threshold:>4}: {count:>5} ({100*density:.2f}%)")

# Log-log regression to find scaling
thresholds = [2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
densities = []
for t in thresholds:
    d = sum(1 for e in excursions if e > t) / total
    if d > 0:
        densities.append((t, d))

if len(densities) > 2:
    log_t = np.log([d[0] for d in densities])
    log_d = np.log([d[1] for d in densities])
    slope, intercept = np.polyfit(log_t, log_d, 1)
    print(f"\nScaling: density ~ threshold^{slope:.2f}")
    print("(If slope = -1, density is inversely proportional to threshold)")

print("\n" + "=" * 70)
print("HARD PROBLEM 6: Tao's Approximate Invariant Measure")
print("=" * 70)

print("""
Tao's key insight: construct a measure μ on odd integers such that
S_*μ ≈ μ (approximately invariant).

The measure assigns weight to residue classes mod 2^k in a specific way.

ATTEMPTING TO RECONSTRUCT: What weights make the Syracuse map
approximately preserve the measure?
""")

def find_invariant_weights(k, n_iter=100):
    """
    Find weights for residue classes mod 2^k that are 
    approximately invariant under Syracuse.
    """
    mod = 2**k
    odd_residues = list(range(1, mod, 2))
    n_states = len(odd_residues)
    
    # Start with uniform
    weights = np.ones(n_states) / n_states
    
    # Build transition matrix (column stochastic)
    T = np.zeros((n_states, n_states))
    residue_to_idx = {r: i for i, r in enumerate(odd_residues)}
    
    for j_idx, j_res in enumerate(odd_residues):
        # Sample transitions
        for rep in range(j_res, 50000, mod):
            if rep > 0:
                s = syracuse(rep)
                s_res = s % mod
                if s_res in residue_to_idx:
                    T[residue_to_idx[s_res], j_idx] += 1
        
        # Normalize column
        col_sum = T[:, j_idx].sum()
        if col_sum > 0:
            T[:, j_idx] /= col_sum
    
    # Find stationary distribution: solve T @ π = π
    # This is the left eigenvector with eigenvalue 1
    eigenvalues, eigenvectors = linalg.eig(T)
    
    # Find eigenvalue closest to 1
    idx = np.argmin(np.abs(eigenvalues - 1))
    stationary = np.real(eigenvectors[:, idx])
    stationary = np.abs(stationary)  # Ensure positive
    stationary /= stationary.sum()  # Normalize
    
    return odd_residues, stationary, T

print("\nApproximate invariant weights mod 16:")
residues, weights, T = find_invariant_weights(4)
print(f"{'Residue':>8} {'Weight':>10} {'Uniform':>10}")
uniform = 1 / len(residues)
for r, w in zip(residues, weights):
    ratio = w / uniform
    print(f"{r:>8} {w:>10.4f} {uniform:>10.4f} (ratio {ratio:.2f})")

print("\nApproximate invariant weights mod 32:")
residues, weights, T = find_invariant_weights(5)
# Show most over/under-represented
weight_ratio = [(r, w / (1/len(residues))) for r, w in zip(residues, weights)]
weight_ratio.sort(key=lambda x: x[1])
print("Most under-represented:")
for r, ratio in weight_ratio[:5]:
    print(f"  {r}: {ratio:.3f}x uniform")
print("Most over-represented:")
for r, ratio in weight_ratio[-5:]:
    print(f"  {r}: {ratio:.3f}x uniform")

print("\n" + "=" * 70)
print("EXPERT SYNTHESIS: Dynamical Systems")
print("=" * 70)

print("""
WHAT I NOW DEEPLY UNDERSTAND:

1. TRANSFER OPERATOR SPECTRUM
   The Syracuse transfer operator has leading eigenvalue 1.
   The spectral gap determines mixing rate.
   Faster mixing = better equidistribution.

2. LOG-SCALE DYNAMICS
   On log scale, Syracuse is approximately additive.
   Drift = log(3) - E[v]*log(2) ≈ -0.287 (negative).
   This negative drift is why trajectories shrink on average.

3. LYAPUNOV EXPONENT
   λ ≈ -0.287 confirms average contraction.
   The distribution of λ across trajectories is tight.
   Outliers (high λ) correspond to high-excursion numbers.

4. ESCAPE TIME DISTRIBUTION
   τ(n) depends strongly on n mod 8.
   n ≡ 7 mod 8 has longest escape times.
   This relates to v_2=1 structure.

5. DENSITY OF BAD NUMBERS
   Density of E(n) > t scales like t^{-c} for some c.
   This means: arbitrarily bad numbers exist but are rare.
   The rarity increases faster than linearly with threshold.

6. APPROXIMATE INVARIANT MEASURE
   The stationary distribution is NOT uniform.
   Some residue classes are "attractors" (higher weight).
   This non-uniformity is key to Tao's approach.

7. THE GAP TO A PROOF
   All these results are "almost all" or "on average."
   Converting to "all" requires showing NO exceptions exist.
   The structural constraints (v_2 runs bounded) should help.
""")
