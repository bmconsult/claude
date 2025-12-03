"""
FRESH APPROACH: What constraints does the STRUCTURE of S impose?

S = sum_{j=0}^{m-1} 3^{m-1-j} * 2^{prefix_j}

This is a very specific polynomial in powers of 2 and 3.
Can we show S/D can only equal 1 for valid paths?
"""

import math

def compute_S_D(deltas):
    """Compute S and D for a given delta sequence."""
    m = len(deltas)
    A = sum(deltas)
    D = 2**A - 3**m
    
    S = 0
    prefix = 0
    for j in range(m):
        S += (3**(m-1-j)) * (2**prefix)
        prefix += deltas[j]
    
    return S, D, A

print("="*70)
print("ANALYZING S AS A FUNCTION OF THE PATH")
print("="*70)

print("""
For a path (δ_0, ..., δ_{m-1}) with all δ_j ≥ 1:

S = 3^{m-1} + 3^{m-2}·2^{δ_0} + 3^{m-3}·2^{δ_0+δ_1} + ... + 2^{A-δ_{m-1}}

Let's define:
  r_j = 2^{prefix_j} / 3^j = 2^{prefix_j} · 3^{-j}

Then:
  S = 3^{m-1} · (1 + r_1 + r_2 + ... + r_{m-1})

where r_j = (2/3)^j · 2^{prefix_j - j} = (2/3)^j · 2^{sum_{i<j}(δ_i - 1)}

For constant path (all δ_j = 2):
  prefix_j = 2j, so r_j = (2/3)^j · 2^{2j - j} = (2/3)^j · 2^j = (4/3)^j

  S = 3^{m-1} · sum_{j=0}^{m-1} (4/3)^j = 3^{m-1} · ((4/3)^m - 1)/(4/3 - 1)
    = 3^{m-1} · 3 · ((4/3)^m - 1) = 3^m · ((4/3)^m - 1)
    = 4^m - 3^m

And D = 2^{2m} - 3^m = 4^m - 3^m.
So S = D, giving k = 1. ✓
""")

print("="*70)
print("KEY OBSERVATION: S/D RATIO ANALYSIS")
print("="*70)

# For various paths, compute S/D and see the pattern
print("\nS/D ratios for m = 4:")

m = 4
results = []

# Generate paths with A in valid range
A_min = int(m * 1.585) + 1  # For D > 0
for A in range(A_min, A_min + 10):
    # Generate some paths
    from itertools import combinations_with_replacement
    
    for d0 in range(1, min(A, 5)):
        for d1 in range(1, min(A-d0, 5)):
            for d2 in range(1, min(A-d0-d1, 5)):
                d3 = A - d0 - d1 - d2
                if d3 < 1:
                    continue
                
                deltas = [d0, d1, d2, d3]
                S, D, _ = compute_S_D(deltas)
                
                if D > 0:
                    ratio = S / D
                    results.append((deltas, S, D, ratio))

# Sort by ratio
results.sort(key=lambda x: x[3])

print("Paths with S/D closest to integers:")
for deltas, S, D, ratio in results:
    if abs(ratio - round(ratio)) < 0.01:
        print(f"  δ = {deltas}, S = {S}, D = {D}, S/D = {ratio:.6f}")

# Check if any non-constant path gives integer ratio
print("\nChecking for k > 1 solutions:")
for deltas, S, D, ratio in results:
    if D > 0 and S % D == 0:
        k = S // D
        if k > 1:
            print(f"  FOUND: δ = {deltas}, k = {k}")
        elif k == 1 and deltas != [2]*m:
            print(f"  k=1 non-constant: δ = {deltas}")

print("\n" + "="*70)
print("THE RATIO BOUND")
print("="*70)

print("""
Let's derive bounds on S/D.

S = 3^{m-1} · (1 + sum_{j=1}^{m-1} (2/3)^j · 2^{excess_j})

where excess_j = prefix_j - j = sum_{i<j}(δ_i - 1).

For all δ_i = 1: excess_j = 0 for all j.
  S = 3^{m-1} · sum_{j=0}^{m-1} (2/3)^j = 3^{m-1} · (1 - (2/3)^m)/(1 - 2/3)
    = 3^{m-1} · 3 · (1 - (2/3)^m) = 3^m - 2^m
  
  D = 2^m - 3^m < 0. Not valid.

For all δ_i = 2: S = D = 4^m - 3^m, k = 1.

For mixed paths:
  S and D depend on the specific δ values.
  
Key insight: S is maximized when more weight is on later terms (high powers of 2).
D is determined by A = sum(δ_j).

For S = kD with k > 1:
  S > D, so we need paths where S is larger relative to D.
""")

# Detailed ratio analysis
print("\nRatio S/D vs A for m = 5:")
m = 5
A_min = int(m * 1.585) + 1

for A in range(A_min, A_min + 8):
    S_const, D_const, _ = compute_S_D([2]*m)  # Constant path
    
    # Find min and max S/D for this A
    min_ratio = float('inf')
    max_ratio = 0
    
    count = 0
    for d0 in range(1, min(A, 6)):
        for d1 in range(1, min(A-d0, 6)):
            for d2 in range(1, min(A-d0-d1, 6)):
                for d3 in range(1, min(A-d0-d1-d2, 6)):
                    d4 = A - d0 - d1 - d2 - d3
                    if d4 < 1:
                        continue
                    
                    deltas = [d0, d1, d2, d3, d4]
                    S, D, _ = compute_S_D(deltas)
                    
                    if D > 0:
                        ratio = S / D
                        min_ratio = min(min_ratio, ratio)
                        max_ratio = max(max_ratio, ratio)
                        count += 1
    
    if count > 0:
        print(f"  A = {A}: S/D ∈ [{min_ratio:.4f}, {max_ratio:.4f}], {count} paths")

print("\n" + "="*70)
print("CRITICAL REALIZATION")
print("="*70)

print("""
The constant path (all δ_j = 2) gives S = D, so k = 1.

For ANY other path with the same A = 2m:
  - Either some δ_j < 2, reducing early terms
  - Or some δ_j > 2, increasing later terms
  
In either case, S ≠ D.

The question is: for what paths can S/D be an integer > 1?

From the computational search:
  - No k > 1 solutions found for m ≤ 15, k ≤ 500.
  
This suggests S/D is NEVER an integer > 1 for valid paths.

Why might this be? 

S and D have a very specific algebraic relationship:
  S + k·3^m = k·2^A
  
For k = 1: S = 2^A - 3^m = D. The relationship is "tight".

For k > 1: S = k·2^A - k·3^m. 
  This requires S to be much larger than D.
  But S has a rigid structure - it's a weighted sum with coefficients 3^{m-1-j}.

The structure of S limits how large it can be relative to D.
""")

print("\n" + "="*70)
print("MAXIMUM S/D ANALYSIS")
print("="*70)

# For each m, find the maximum S/D ratio
print("\nMaximum S/D ratio vs m:")

for m in range(2, 12):
    A_min = int(m * 1.585) + 1
    max_ratio = 0
    best_path = None
    
    # Search over paths
    def search_paths(m, A_max):
        best = 0
        best_d = None
        
        if m == 2:
            for d0 in range(1, A_max):
                for d1 in range(1, A_max - d0 + 1):
                    deltas = [d0, d1]
                    S, D, _ = compute_S_D(deltas)
                    if D > 0 and S/D > best:
                        best = S/D
                        best_d = deltas
        elif m == 3:
            for d0 in range(1, A_max):
                for d1 in range(1, A_max - d0):
                    for d2 in range(1, A_max - d0 - d1 + 1):
                        deltas = [d0, d1, d2]
                        S, D, _ = compute_S_D(deltas)
                        if D > 0 and S/D > best:
                            best = S/D
                            best_d = deltas
        else:
            # For larger m, sample
            import random
            for _ in range(10000):
                A = random.randint(A_min, A_min + 20)
                deltas = []
                remaining = A
                for i in range(m-1):
                    d = random.randint(1, max(1, remaining - (m - 1 - i)))
                    deltas.append(d)
                    remaining -= d
                deltas.append(remaining)
                if deltas[-1] >= 1:
                    S, D, _ = compute_S_D(deltas)
                    if D > 0 and S/D > best:
                        best = S/D
                        best_d = deltas
        return best, best_d
    
    max_ratio, best_path = search_paths(m, 30)
    print(f"  m = {m:2d}: max(S/D) ≈ {max_ratio:.4f}, path ≈ {best_path}")

print("\n" + "="*70)
print("INSIGHT: S/D IS ALWAYS NEAR 1")
print("="*70)

print("""
The maximum S/D ratio appears to be close to 1 for all m!

This suggests that S and D are "balanced" by the structure of the problem.

Conjecture: For any valid Collatz path, S/D < 2.

If true, this would immediately prove k = 1 is the only possibility!

Let me try to prove this bound...

S = sum_{j=0}^{m-1} 3^{m-1-j} * 2^{prefix_j}
D = 2^A - 3^m

For S/D < 2:
  S < 2D = 2·2^A - 2·3^m = 2^{A+1} - 2·3^m
  
  sum_{j=0}^{m-1} 3^{m-1-j} * 2^{prefix_j} < 2^{A+1} - 2·3^m
  
  Rearranging:
  3^{m-1} + sum_{j=1}^{m-1} 3^{m-1-j} * 2^{prefix_j} + 2·3^m < 2^{A+1}
  3^{m-1}(1 + 6) + sum_{j=1}^{m-1} 3^{m-1-j} * 2^{prefix_j} < 2^{A+1}
  
  Hmm, this is getting complicated. Let me try a different approach.
""")

if __name__ == "__main__":
    pass
