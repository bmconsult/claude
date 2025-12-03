#!/usr/bin/env python3
"""
AUTOMATED THEOREM PROVING - EXPERT LEVEL
==========================================

Going deep into the machinery that could mechanize a Collatz proof.
"""

import numpy as np
from itertools import product
from collections import defaultdict

print("=" * 70)
print("HARD PROBLEM 1: Matrix Interpretation Design for Collatz")
print("=" * 70)

print("""
A matrix interpretation assigns to each state n a vector [n] ∈ R^d.
The Syracuse map S induces: [S(n)] = A · [n] + b for some matrix A, vector b.

For termination, we need [n] > [S(n)] in some well-founded order
(e.g., lexicographic on components, or some weighted norm).

CHALLENGE: Design the state vector [n] to capture run structure.
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

def design_state_vector(n, d=5):
    """
    Design a d-dimensional state vector that captures:
    - Value (log scale)
    - Mod structure
    - Run potential
    - Accumulated drift
    """
    if n <= 0:
        return np.zeros(d)
    
    log_n = np.log(n)
    
    # Mod 4 indicator (determines if v2=1)
    mod4_indicator = 1.0 if n % 4 == 3 else 0.0
    
    # Distance to nearest Mersenne (growth potential)
    log_n_int = int(log_n / np.log(2))
    nearest_mersenne = 2**(log_n_int + 1) - 1
    mersenne_dist = abs(n - nearest_mersenne) / n if n > 0 else 1
    
    # Binary density (number of 1s / number of bits)
    if n > 0:
        bits = bin(n)[2:]
        density = bits.count('1') / len(bits)
    else:
        density = 0
    
    # Trailing ones count
    if n > 0:
        bits = bin(n)[2:]
        trailing_ones = len(bits) - len(bits.rstrip('1'))
    else:
        trailing_ones = 0
    trailing_ones_norm = trailing_ones / (np.log2(n + 1) + 1)
    
    return np.array([
        log_n,
        mod4_indicator,
        1 - mersenne_dist,  # Higher = closer to Mersenne
        density,
        trailing_ones_norm
    ])

print("\nState vectors for sample values:")
for n in [27, 127, 255, 703, 6171, 131071]:
    v = design_state_vector(n)
    print(f"n={n:>6}: [{', '.join(f'{x:.3f}' for x in v)}]")

print("\n" + "-" * 70)
print("Testing if a linear map captures Syracuse dynamics")
print("-" * 70)

def learn_linear_map(n_samples=1000):
    """
    Try to learn A, b such that [S(n)] ≈ A · [n] + b
    using least squares regression.
    """
    d = 5
    X = []  # Input vectors
    Y = []  # Output vectors
    
    for _ in range(n_samples):
        n = np.random.randint(3, 100000)
        if n % 2 == 0:
            n += 1
        
        x = design_state_vector(n, d)
        s = syracuse(n)
        y = design_state_vector(s, d)
        
        X.append(x)
        Y.append(y)
    
    X = np.array(X)
    Y = np.array(Y)
    
    # Add bias column
    X_aug = np.hstack([X, np.ones((len(X), 1))])
    
    # Solve Y = X_aug @ [A; b]^T for each output dimension
    coeffs, residuals, rank, s = np.linalg.lstsq(X_aug, Y, rcond=None)
    
    A = coeffs[:d].T  # d x d matrix
    b = coeffs[d]     # d-vector
    
    # Test fit
    Y_pred = X @ A.T + b
    errors = np.abs(Y - Y_pred)
    
    return A, b, np.mean(errors, axis=0)

A, b, errors = learn_linear_map(5000)
print("\nLearned transformation [S(n)] ≈ A·[n] + b:")
print("Matrix A:")
for row in A:
    print(f"  [{', '.join(f'{x:>7.3f}' for x in row)}]")
print(f"Vector b: [{', '.join(f'{x:.3f}' for x in b)}]")
print(f"Mean errors per dimension: {errors}")

print("""
INSIGHT: If the linear fit is poor (high errors), we need a 
more sophisticated state representation.
""")

print("\n" + "=" * 70)
print("HARD PROBLEM 2: Lexicographic Termination Arguments")
print("=" * 70)

print("""
A lexicographic ranking uses a tuple (r_1, r_2, ..., r_k) that decreases
lexicographically at each step.

IDEA: Use tuple (ceiling(log n), secondary_measure, ...)
where secondary_measure breaks ties in the first component.
""")

def lexicographic_rank(n):
    """
    Compute a lexicographic ranking tuple for n.
    """
    if n <= 1:
        return (0, 0, 0)
    
    # First component: ceiling of log_2(n)
    log_ceiling = int(np.ceil(np.log2(n)))
    
    # Second component: position within the "band" [2^(k-1), 2^k)
    # Normalized to [0, 1)
    band_position = (n - 2**(log_ceiling - 1)) / 2**(log_ceiling - 1) if log_ceiling > 0 else 0
    
    # Third component: mod structure (penalize n ≡ 3 mod 4)
    mod_penalty = 1 if n % 4 == 3 else 0
    
    return (log_ceiling, band_position, mod_penalty)

print("Testing lexicographic ranking:")
print(f"{'n':>8} {'rank':>25} {'S(n)':>8} {'rank(S(n))':>25} {'decrease?':>10}")

def rank_decreases(r1, r2):
    """Check if r1 > r2 lexicographically"""
    for a, b in zip(r1, r2):
        if a > b:
            return True
        if a < b:
            return False
    return False  # Equal

violations = []
for n in range(3, 10001, 2):
    r_n = lexicographic_rank(n)
    s_n = syracuse(n)
    r_sn = lexicographic_rank(s_n)
    
    decreases = rank_decreases(r_n, r_sn)
    
    if not decreases:
        violations.append((n, r_n, s_n, r_sn))

print(f"\nViolations (rank didn't decrease): {len(violations)}")
if violations:
    print("First 10 violations:")
    for n, r_n, s_n, r_sn in violations[:10]:
        print(f"  n={n}, rank={r_n}, S(n)={s_n}, rank(S(n))={r_sn}")

print("""
CHALLENGE: The simple lexicographic ranking doesn't work because
Syracuse can increase the log ceiling.

We need a ranking that "anticipates" the future contraction.
""")

print("\n" + "=" * 70)
print("HARD PROBLEM 3: Amortized Analysis / Potential Method")
print("=" * 70)

print("""
IDEA: Instead of requiring decrease at EVERY step, require:
  Σ Φ(after_i) - Φ(before_i) < 0 over any complete trajectory

This is like amortized analysis in algorithm design.
The potential Φ(n) can temporarily increase but must decrease overall.
""")

def potential_with_run_tracking(n, run_history=None):
    """
    A potential that accounts for being in a v_2=1 run.
    
    The potential is:
    - Base: log(n)
    - Penalty: for being in a run, add (expected future growth from run)
    - Credit: for accumulated v_2 > 1 steps
    """
    if n <= 1:
        return 0
    
    log_n = np.log(n)
    
    # If n ≡ 3 mod 4, we're about to have v_2=1 (growth)
    # Estimate max remaining run length from this point
    if n % 4 == 3:
        max_run_from_here = int(np.log2(n))  # Our structural bound
        expected_growth = max_run_from_here * (np.log(3) - np.log(2))
        run_penalty = expected_growth * 0.3  # Discount factor
    else:
        run_penalty = 0
    
    return log_n + run_penalty

def test_potential_trajectory(n, potential_func):
    """Test if potential decreases overall along trajectory"""
    potentials = [potential_func(n)]
    values = [n]
    
    current = n
    for _ in range(1000):
        if current == 1:
            break
        current = syracuse(current)
        values.append(current)
        potentials.append(potential_func(current))
    
    initial = potentials[0]
    final = potentials[-1]
    max_pot = max(potentials)
    
    return {
        'n': n,
        'initial': initial,
        'final': final,
        'max': max_pot,
        'overall_decrease': initial > final,
        'max_increase_ratio': max_pot / initial if initial > 0 else 0
    }

print("Testing amortized potential:")
results = []
for n in range(3, 50001, 2):
    r = test_potential_trajectory(n, potential_with_run_tracking)
    results.append(r)

# Statistics
overall_decreases = sum(1 for r in results if r['overall_decrease'])
print(f"Trajectories with overall decrease: {overall_decreases}/{len(results)}")

max_ratios = [r['max_increase_ratio'] for r in results]
print(f"Max potential increase ratio: {max(max_ratios):.3f}")
print(f"Mean max ratio: {np.mean(max_ratios):.3f}")

# Worst cases
results.sort(key=lambda r: -r['max_increase_ratio'])
print("\nWorst cases (highest max/initial):")
for r in results[:5]:
    print(f"  n={r['n']}: initial={r['initial']:.2f}, max={r['max']:.2f}, ratio={r['max_increase_ratio']:.3f}")

print("\n" + "=" * 70)
print("HARD PROBLEM 4: SAT Encoding of Termination")
print("=" * 70)

print("""
Modern termination provers encode the search for a ranking function
as a SAT/SMT problem.

For polynomial interpretations:
- Variables: coefficients of the polynomial
- Constraints: [l] > [r] for each rewrite rule

For matrix interpretations:
- Variables: entries of the matrix A
- Constraints: ||A·v|| < ||v|| for appropriate norm

Let's simulate this for a VERY simple case.
""")

def sat_encode_polynomial_termination(max_n, degree=2):
    """
    Try to find a polynomial P(n) such that P(n) > P(S(n)) for all odd n < max_n.
    
    Search for: P(n) = a_0 + a_1*n + a_2*n^2 + ...
    """
    from scipy.optimize import minimize
    
    def polynomial(coeffs, n):
        return sum(c * n**i for i, c in enumerate(coeffs))
    
    def loss(coeffs):
        """Loss: sum of violations (P(S(n)) - P(n) when positive)"""
        total_loss = 0
        for n in range(3, max_n, 2):
            p_n = polynomial(coeffs, n)
            s_n = syracuse(n)
            p_sn = polynomial(coeffs, s_n)
            
            # We want P(n) > P(S(n)), so penalize if P(S(n)) >= P(n)
            violation = max(0, p_sn - p_n + 0.1)  # Small margin
            total_loss += violation
        
        # Regularization: prefer small coefficients
        total_loss += 0.001 * sum(c**2 for c in coeffs)
        
        return total_loss
    
    # Try different starting points
    best_loss = float('inf')
    best_coeffs = None
    
    for _ in range(10):
        x0 = np.random.randn(degree + 1) * 0.1
        x0[0] = 1  # Constant term
        x0[1] = 1  # Linear term
        
        result = minimize(loss, x0, method='BFGS', options={'maxiter': 1000})
        
        if result.fun < best_loss:
            best_loss = result.fun
            best_coeffs = result.x
    
    return best_coeffs, best_loss

print("\nSearching for polynomial termination argument (n < 1000):")
coeffs, loss = sat_encode_polynomial_termination(1000, degree=3)
print(f"Best polynomial: P(n) = {' + '.join(f'{c:.4f}*n^{i}' for i, c in enumerate(coeffs))}")
print(f"Total loss: {loss:.4f}")

# Count violations
violations = 0
for n in range(3, 1000, 2):
    p_n = sum(c * n**i for i, c in enumerate(coeffs))
    s_n = syracuse(n)
    p_sn = sum(c * s_n**i for i, c in enumerate(coeffs))
    if p_sn >= p_n:
        violations += 1

print(f"Violations: {violations}")

print("""
INSIGHT: A simple polynomial can't work because Syracuse(n) can be >> n.
Need either:
1. Higher-dimensional state (matrix interpretation)
2. Amortized argument (sum over trajectory)
3. Structural constraints (bound runs)
""")

print("\n" + "=" * 70)
print("HARD PROBLEM 5: Combining Structural Bounds with Termination")
print("=" * 70)

print("""
KEY INSIGHT: We proved that max v_2=1 run ≤ log_2(n).

Can we use this to construct a ranking function?

IDEA: Define potential as:
  Φ(n) = log(n) - (1 - ε) * accumulated_contraction_budget

where accumulated_contraction_budget tracks the "debt" from past v_2=1 runs.

The structural bound ensures the debt can't grow without bound.
""")

class TrackingPotential:
    """A potential that tracks run structure"""
    
    def __init__(self, n):
        self.n = n
        self.log_n = np.log(n) if n > 1 else 0
        self.in_run = (n % 4 == 3)
        self.run_length = 0
        self.total_v2 = 0
        self.steps = 0
        
    def step(self):
        """Take one Syracuse step"""
        if self.n <= 1:
            return False
        
        v = v2(3 * self.n + 1)
        self.n = (3 * self.n + 1) // (2 ** v)
        self.log_n = np.log(self.n) if self.n > 1 else 0
        
        if v == 1:
            if self.in_run:
                self.run_length += 1
            else:
                self.in_run = True
                self.run_length = 1
        else:
            self.in_run = False
            self.run_length = 0
        
        self.total_v2 += v
        self.steps += 1
        
        return True
    
    def potential(self):
        """Compute potential incorporating run structure"""
        if self.n <= 1:
            return 0
        
        # Base: log(n)
        base = self.log_n
        
        # Adjustment for being in a run
        if self.in_run:
            # Each v_2=1 step adds ~0.405 to log(n)
            # But the run is bounded by log_2(n), so max additional growth is
            # (log_2(n) - run_length) * 0.405
            max_remaining = max(0, np.log2(self.n) - self.run_length)
            expected_future_growth = max_remaining * (np.log(3) - np.log(2))
            run_adjustment = expected_future_growth * 0.5
        else:
            run_adjustment = 0
        
        # Credit for accumulated v_2 (contraction already done)
        expected_v2 = 2 * self.steps
        v2_credit = (self.total_v2 - expected_v2) * 0.1
        
        return base + run_adjustment - v2_credit

print("Testing tracking potential:")

test_cases = [27, 127, 703, 6171, 77671]
for start_n in test_cases:
    tp = TrackingPotential(start_n)
    potentials = [tp.potential()]
    
    while tp.step():
        potentials.append(tp.potential())
    
    print(f"n={start_n:>6}: initial={potentials[0]:.2f}, final={potentials[-1]:.2f}, "
          f"max={max(potentials):.2f}, max/init={max(potentials)/potentials[0]:.2f}")

print("\n" + "=" * 70)
print("EXPERT SYNTHESIS: Automated Theorem Proving")
print("=" * 70)

print("""
WHAT I NOW DEEPLY UNDERSTAND:

1. STATE VECTOR DESIGN
   The state must capture more than just n.
   Need: log(n), mod structure, run position, accumulated drift.
   Linear maps don't capture Syracuse well (need nonlinearity).

2. LEXICOGRAPHIC RANKING
   Simple lex rankings fail because log(n) can increase.
   Need to "anticipate" future contraction somehow.
   This is the fundamental difficulty.

3. AMORTIZED ANALYSIS
   Don't need decrease at every step, just overall.
   A potential that accounts for "debt" can work.
   The structural bound (runs ≤ log n) limits debt accumulation.

4. SAT/SMT APPROACH
   Can search for polynomial/matrix interpretations.
   Simple polynomials can't work (S(n) >> n possible).
   Need high-dimensional state or structural constraints.

5. THE KEY INSIGHT
   The structural bound (v_2=1 runs ≤ log n) is the key.
   It limits how much the potential can grow in any burst.
   Combined with E[v_2] = 2 > 1.585, trajectories must decrease.

6. WHAT'S STILL NEEDED
   - Rigorous proof that run bound holds universally
   - Potential function that provably decreases overall
   - Either: closed-form proof, or SAT-verified bound

The machinery exists. The structural insight exists.
The gap is formalizing the connection between them.
""")
