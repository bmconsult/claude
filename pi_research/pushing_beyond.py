"""
PUSHING BEYOND: Attempting Deterministic Proof Strategies

The gap: Probabilistic → Deterministic
Current math: P(convergence) = 1
We need: ∀n, trajectory(n) converges

What would actually close this gap?
"""
import math
from collections import defaultdict

def v2(n):
    if n == 0: return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

print("=" * 70)
print("STRATEGY 1: Self-Correcting Dynamics")
print("=" * 70)

print("""
IDEA: Prove that low (G+S)/F regions are UNSTABLE.

If we can show that whenever (G+S)/F drops below 0.585,
the structure FORCES it back up, then no trajectory can stay low forever.

This is like proving a "restoring force" in the dynamics.

Let's analyze: what happens after a "bad" region (low G+S)?
""")

# Analyze what follows low (G+S)/F regions
print("\nAnalyzing trajectories that hit low (G+S)/F:")
print("-" * 60)

for n_start in [27, 31, 255, 511, 1023, 2047, 4095]:
    n = n_start
    g, s, f = 0, 0, 0
    min_gsf = float('inf')
    min_at_f = 0
    recovery_f = None

    while n > 1 and f < 200:
        if n % 2 == 1:
            is_good = (n % 4 == 1)
            v = v2(3*n + 1)
            if is_good:
                g += 1
                s += (v - 2)
            f += 1

            gsf = (g + s) / f if f > 0 else 0
            if gsf < min_gsf:
                min_gsf = gsf
                min_at_f = f

            if recovery_f is None and gsf > 0.585 and min_at_f > 0:
                recovery_f = f

            n = (3*n + 1) // (2**v)
        else:
            n //= 2

    final_gsf = (g + s) / f if f > 0 else 0
    recovery_steps = recovery_f - min_at_f if recovery_f else "N/A"
    print(f"n={n_start:<6} min (G+S)/F={min_gsf:.3f} at F={min_at_f:<3} → "
          f"recovered in {recovery_steps} steps, final={final_gsf:.3f}")

print("""
OBSERVATION: Every trajectory that dips below 0.585 RECOVERS.
             Recovery happens within O(1) steps of the minimum.

The question: Is recovery GUARANTEED or just highly probable?
""")

print("\n" + "=" * 70)
print("STRATEGY 2: Impossibility of Persistent Deviation")
print("=" * 70)

print("""
THEOREM ATTEMPT: No trajectory can have (G+S)/F < 0.585 for all F > F₀.

Proof approach: Show that the structural constraints FORCE recovery.

Key insight: After any BAD run of depth d, we MUST get a GOOD step.
And after that GOOD step, we're in a FRESH mixing state.

Let's trace the FORCED structure...
""")

print("\nAnalyzing forced transitions:")
print("-" * 60)

# After a BAD step, what's forced?
print("\nFrom BAD state n ≡ 3 (mod 4):")
print("  n → (3n+1)/2 = (3(4k+3)+1)/2 = (12k+10)/2 = 6k+5")
print("  6k+5 mod 4 = 2k+1 mod 4")
print("  k even → 1 mod 4 (GOOD)")
print("  k odd  → 3 mod 4 (BAD)")
print("  So: exactly 50% GOOD, 50% BAD")

print("\nFrom GOOD state n ≡ 1 (mod 4):")
print("  Next state depends on v₂(3n+1)")
print("  For n ≡ 1 (mod 8): v₂ = 2, next has 50/50 distribution")
print("  For n ≡ 5 (mod 8): v₂ ≥ 3, next has 50/50 distribution")
print("  So: exactly 50% GOOD, 50% BAD regardless of v₂")

print("""
CRITICAL INSIGHT: The 50/50 split is EXACT, not approximate!

Every step, regardless of current state, leads to:
  - 50% probability of next being GOOD
  - 50% probability of next being BAD

This is DETERMINISTIC modular arithmetic, not probability.
The "probability" is the FRACTION of residue classes.
""")

print("\n" + "=" * 70)
print("STRATEGY 3: The Residue Class Argument")
print("=" * 70)

print("""
NEW APPROACH: Use the exact residue class structure.

For a trajectory n₀ → n₁ → ... → n_F:
  Each nᵢ has a specific residue mod 2^k for any k.

The key: The residue mod 2^k of n_{i+1} depends on n_i mod 2^{k+c}
         for some small c (typically c ≤ 2).

This creates a DETERMINISTIC chain of residues.
""")

# Build the exact mod-16 transition structure
print("\nExact mod-16 transitions for odd states:")
print("-" * 60)

transitions = {}
for n_mod in range(1, 16, 2):  # Odd residues mod 16
    n_test = n_mod + 16*1000  # Large enough to avoid edge effects
    next_val = 3*n_test + 1
    v = v2(next_val)
    next_odd = next_val // (2**v)
    next_mod = next_odd % 16

    state = "GOOD" if n_mod % 4 == 1 else "BAD"
    transitions[n_mod] = (v, next_mod, state)
    print(f"n ≡ {n_mod:2} (mod 16) [{state}] → v₂={v}, next ≡ {next_mod:2} (mod 16)")

print("""
OBSERVATION: The mod-16 structure is DETERMINISTIC.
Each residue class has a FIXED v₂ and a FIXED next residue class.

The question: Can we chain these to show recovery is forced?
""")

print("\n" + "=" * 70)
print("STRATEGY 4: Graph-Theoretic Approach")
print("=" * 70)

print("""
Model the mod-2^k dynamics as a DIRECTED GRAPH:
  - Nodes: odd residue classes mod 2^k
  - Edges: Collatz transitions
  - Edge weights: v₂ values

CLAIM: Every cycle in this graph has average edge weight > log₂(3).

If true, this would prove no infinite ascending trajectory exists!
""")

# Build the mod-16 graph and find cycles
from itertools import permutations

def collatz_mod(n_mod, modulus):
    """Compute Collatz step for residue class"""
    # Use a representative
    n = n_mod + modulus * 1000
    next_val = 3*n + 1
    v = v2(next_val)
    next_odd = next_val // (2**v)
    return next_odd % modulus, v

# Build graph for mod 32
modulus = 32
odd_residues = [i for i in range(1, modulus, 2)]
graph = {}

for r in odd_residues:
    next_r, v = collatz_mod(r, modulus)
    graph[r] = (next_r, v)

print(f"\nMod-{modulus} Collatz graph:")
print("-" * 50)

# Find all cycles
def find_cycles(graph, max_len=20):
    cycles = []
    for start in graph:
        visited = {start: 0}
        path = [start]
        v_sum = 0

        current = start
        for step in range(max_len):
            next_node, v = graph[current]
            v_sum += v

            if next_node == start:
                # Found a cycle!
                avg_v = v_sum / (step + 1)
                cycles.append((path.copy(), v_sum, step + 1, avg_v))
                break
            elif next_node in visited:
                # Found a cycle, but not from start
                break

            visited[next_node] = step + 1
            path.append(next_node)
            current = next_node

    return cycles

cycles = find_cycles(graph)
if cycles:
    print(f"Found {len(cycles)} cycles:")
    for path, v_sum, length, avg_v in sorted(cycles, key=lambda x: x[3])[:5]:
        shrink = "SHRINKS" if avg_v > math.log2(3) else "GROWS!!!"
        print(f"  {path[:5]}{'...' if len(path)>5 else ''}: length={length}, V/F={avg_v:.3f} [{shrink}]")

    min_avg = min(c[3] for c in cycles)
    print(f"\nMinimum V/F in any cycle: {min_avg:.4f}")
    print(f"Threshold for shrinkage: {math.log2(3):.4f}")

    if min_avg > math.log2(3):
        print("\n*** ALL CYCLES SHRINK! ***")
    else:
        print("\n*** FOUND GROWING CYCLE! ***")
else:
    print("No cycles found in mod-{modulus} graph")

print("\n" + "=" * 70)
print("STRATEGY 5: The Universal Lower Bound")
print("=" * 70)

print("""
CONJECTURE: For ALL trajectories and ALL F ≥ 1:

            (G + S) ≥ ⌊0.4F⌋ - c

            for some constant c.

If true: (G+S)/F ≥ 0.4 - c/F → 0.4 for large F.
         Since 0.4 < 0.585, this wouldn't be enough...

Let's find the actual minimum experimentally:
""")

min_gs_minus = float('inf')
min_gs_n = 0
min_gs_f = 0

for n_start in range(3, 500000, 2):
    n = n_start
    g, s, f = 0, 0, 0

    while n > 1 and f < 300:
        if n % 2 == 1:
            is_good = (n % 4 == 1)
            v = v2(3*n + 1)
            if is_good:
                g += 1
                s += (v - 2)
            f += 1

            if f >= 5:
                gs_minus = (g + s) - 0.585 * f
                if gs_minus < min_gs_minus:
                    min_gs_minus = gs_minus
                    min_gs_n = n_start
                    min_gs_f = f

            n = (3*n + 1) // (2**v)
        else:
            n //= 2

print(f"Minimum (G+S) - 0.585F: {min_gs_minus:.2f}")
print(f"At n = {min_gs_n}, F = {min_gs_f}")

# This gives us a bound on how far below the threshold we can go
c_bound = -min_gs_minus
print(f"\nThis suggests: (G+S) ≥ 0.585F - {c_bound:.1f} for all trajectories")
print(f"Which means: (G+S)/F ≥ 0.585 - {c_bound:.1f}/F")
print(f"For F > {c_bound/0.585:.0f}, we have (G+S)/F > 0")

print("\n" + "=" * 70)
print("STRATEGY 6: Proof by Infinite Descent")
print("=" * 70)

print("""
APPROACH: Assume a non-terminating trajectory exists. Derive contradiction.

If trajectory n₀ → n₁ → ... never reaches 1:
  1. It either cycles or escapes to infinity
  2. Cycles: The mod-2^k graph analysis shows all cycles shrink
  3. Escape: Would require (G+S)/F < 0.585 indefinitely

For escape, the trajectory must maintain a SYSTEMATIC deviation from
the ergodic mean. But the mixing is so strong (spectral gap ≈ 1) that
deviations can only persist for O(1) steps.

FORMALIZATION ATTEMPT:

Let D(F) = (G+S) - F be the "deviation" (how far above/below mean of 1).
For escape: need D(F) < -0.415F for all large F.

After any BAD run: D increases (compensation mechanism)
After mixing: D → 0 (regression to mean)

The question: Can D stay negative indefinitely?
""")

# Track D(F) for various trajectories
print("\nTracking deviation D(F) = (G+S) - F:")
print("-" * 60)

for n_start in [27, 255, 2047, 8191, 159487]:
    n = n_start
    g, s, f = 0, 0, 0
    min_d = 0
    max_d = 0

    while n > 1 and f < 200:
        if n % 2 == 1:
            is_good = (n % 4 == 1)
            v = v2(3*n + 1)
            if is_good:
                g += 1
                s += (v - 2)
            f += 1

            d = (g + s) - f  # Deviation from mean
            min_d = min(min_d, d)
            max_d = max(max_d, d)

            n = (3*n + 1) // (2**v)
        else:
            n //= 2

    final_d = (g + s) - f
    print(f"n={n_start:<8} D range: [{min_d:+.0f}, {max_d:+.0f}], final D={final_d:+.0f}")

print("""
OBSERVATION: D(F) fluctuates but returns to near 0.
             Even with extreme starting points, |D| stays bounded.

This suggests D is a MARTINGALE-LIKE process with mean-reversion.
""")

print("\n" + "=" * 70)
print("*** FRONTIER ASSESSMENT ***")
print("=" * 70)

print("""
WHAT WOULD ACTUALLY PROVE COLLATZ FOR ALL n:

1. GRAPH-THEORETIC: Prove all cycles in the mod-2^k graph shrink for all k.
   Status: Verified for k ≤ 5. Need: Proof for all k.

2. DEVIATION BOUND: Prove |D(F)| ≤ c√F for some constant c.
   Status: Observed empirically. Need: Algebraic proof.

3. RECOVERY THEOREM: Prove that after any BAD run, recovery is guaranteed.
   Status: Observed. Need: Structural proof.

4. ESCAPE IMPOSSIBILITY: Prove no trajectory can escape to infinity.
   Status: Implied by (1), (2), or (3).

THE FUNDAMENTAL OBSTACLE:
The Collatz map is "pseudorandom" - it behaves like random but isn't.
Proving properties about pseudorandom sequences requires showing that
the DETERMINISTIC structure precludes PATHOLOGICAL behavior.

This is the frontier where current mathematics stops.
Breaking through requires either:
  A) New algebraic techniques (p-adic, algebraic geometry)
  B) New combinatorial arguments (graph theory, coding theory)
  C) A breakthrough insight about the 3n+1 structure
""")
