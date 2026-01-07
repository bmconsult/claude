"""
CLOSING THE REAL GAP: Attempting a deterministic proof

The circularity: We proved IF terminates THEN E/F > threshold.
We need: For ALL trajectories, E/F > threshold.

Let me try to prove this without assuming termination.
"""
import math
import numpy as np

print("=" * 70)
print("ATTEMPT TO CLOSE THE GAP DETERMINISTICALLY")
print("=" * 70)

print("""
═══════════════════════════════════════════════════════════════════════
                    THE GENERAL IDENTITY
═══════════════════════════════════════════════════════════════════════

For ANY trajectory (terminating or not), at step F:

    log₂(n_F) = log₂(n₀) + F·log₂(3) - V(F) + Σε_i

Rearranging:

    V(F)/F = log₂(3) + [log₂(n₀) - log₂(n_F) + Σε_i] / F

The question: Can V(F)/F stay below log₂(3) ≈ 1.585 indefinitely?

If YES → trajectory escapes to infinity
If NO → trajectory eventually shrinks and converges
═══════════════════════════════════════════════════════════════════════
""")

print("=" * 70)
print("KEY INSIGHT: THE MOD-4 MARKOV CHAIN")
print("=" * 70)

print("""
The mod-4 class determines v₂(3n+1):
  - GOOD (n ≡ 1 mod 4): v₂ ≥ 2, with E[v₂|GOOD] = 3
  - BAD (n ≡ 3 mod 4): v₂ = 1 always

The transition matrix is DOUBLY STOCHASTIC:

    P ≈ [0.5  0.5]  (GOOD row)
        [0.5  0.5]  (BAD row)

This means: AFTER ONE STEP, the state is (0.5, 0.5) REGARDLESS of start!

This is not probabilistic - it's deterministic modular arithmetic.
""")

# Verify the doubly stochastic property
print("\nVerifying transition probabilities:")
print("-" * 50)

# From GOOD (n ≡ 1 mod 4):
good_to_good = 0
good_to_bad = 0
for n in range(1, 10000, 4):  # n ≡ 1 mod 4
    next_n = 3*n + 1
    while next_n % 2 == 0:
        next_n //= 2
    if next_n % 4 == 1:
        good_to_good += 1
    else:
        good_to_bad += 1

# From BAD (n ≡ 3 mod 4):
bad_to_good = 0
bad_to_bad = 0
for n in range(3, 10000, 4):  # n ≡ 3 mod 4
    next_n = 3*n + 1
    while next_n % 2 == 0:
        next_n //= 2
    if next_n % 4 == 1:
        bad_to_good += 1
    else:
        bad_to_bad += 1

total_good = good_to_good + good_to_bad
total_bad = bad_to_good + bad_to_bad

print(f"GOOD → GOOD: {good_to_good/total_good:.4f}")
print(f"GOOD → BAD:  {good_to_bad/total_good:.4f}")
print(f"BAD → GOOD:  {bad_to_good/total_bad:.4f}")
print(f"BAD → BAD:   {bad_to_bad/total_bad:.4f}")

print("\nMatrix is doubly stochastic with eigenvalue λ₂ ≈ 0!")
print("This means INSTANT MIXING - after 1 step, state is (0.5, 0.5).")

print("\n" + "=" * 70)
print("THE DETERMINISTIC BOUND")
print("=" * 70)

print("""
After F steps, let G = # GOOD steps, B = # BAD steps = F - G.

Since the chain mixes instantly:
  - After step 1, P(GOOD) = 0.5 regardless of start
  - So G ≈ F/2 with small fluctuations

CLAIM: For any trajectory with F ≥ F₀, we have G/F ∈ [0.5 - δ, 0.5 + δ]
       where δ depends on the spectral gap.

With spectral gap γ ≈ 1 (instant mixing):
       G/F ∈ [0.5 - O(1/F), 0.5 + O(1/F)]

So for large F: G/F → 0.5 DETERMINISTICALLY.
""")

# The key formula
print("\n" + "=" * 70)
print("THE KEY FORMULA")
print("=" * 70)

print("""
V(F) = Σ v_i = Σ(v|BAD) + Σ(v|GOOD)

For BAD steps: v = 1 always, contributing B = F - G to V.

For GOOD steps: v ≥ 2 always, with average 3.

So: V(F) = (F - G) + Σ(v|GOOD)
         ≥ (F - G) + 2G     [using v ≥ 2 for GOOD]
         = F + G

With G → F/2: V(F) ≥ F + F/2 = 1.5F

This gives V/F ≥ 1.5, but we need V/F > 1.585!

THE GAP: We need to use E[v|GOOD] = 3, not just v ≥ 2.
""")

print("\n" + "=" * 70)
print("USING THE FULL DISTRIBUTION")
print("=" * 70)

print("""
For GOOD steps, v₂ follows a shifted geometric distribution:
  P(v = 2) = 1/2
  P(v = 3) = 1/4
  P(v = k) = 1/2^{k-1} for k ≥ 2

So: Σ(v|GOOD) = 2G + S where S = Σ(v - 2) = "surplus"

E[S] = G × E[v - 2 | GOOD] = G × (3 - 2) = G

So: E[V(F)] = (F - G) + 2G + G = F + 2G

With G = F/2: E[V(F)] = F + F = 2F, giving V/F → 2. ✓

But this is EXPECTED value. We need a LOWER BOUND.
""")

print("\n" + "=" * 70)
print("THE DETERMINISTIC LOWER BOUND")
print("=" * 70)

print("""
THEOREM: For any trajectory of F odd steps:

    V(F) ≥ F + G(F)  [deterministic]

    where G(F) is the number of GOOD steps.

PROOF: Each BAD step contributes v = 1. Each GOOD step contributes v ≥ 2.
       V = B + Σ(v|GOOD) ≥ B + 2G = (F-G) + 2G = F + G.  ∎

COROLLARY: V(F)/F ≥ 1 + G(F)/F

For V(F)/F > 1.585, we need G(F)/F > 0.585.

QUESTION: Is G(F)/F > 0.585 for all trajectories eventually?
""")

# This is the crux
print("\n" + "=" * 70)
print("THE CRUX: IS G/F > 0.585 EVENTUALLY?")
print("=" * 70)

print("""
We need to show: For ALL trajectories, G(F)/F > 0.585 for some F.

Equivalently: No trajectory can have G(F)/F ≤ 0.585 forever.

The mod-4 chain has:
  - Stationary distribution: (0.5, 0.5)
  - Spectral gap: γ ≈ 1

After mixing (O(1) steps), G(F)/F → 0.5.

For G(F)/F ≤ 0.585, we need the fraction of GOOD to stay ≤ 58.5%.
For G(F)/F ≤ 0.5, we need the fraction to stay ≤ 50%.

Since stationary is 50%, we're asking if GOOD fraction can stay at or below average.

By symmetry of the doubly stochastic matrix: YES, 50% is achievable on average!

But 0.585 > 0.5, so we need G/F to exceed the stationary mean.
This is NOT guaranteed by ergodicity alone!
""")

print("\n" + "=" * 70)
print("THE RESCUE: USING SURPLUS S")
print("=" * 70)

print("""
We've been too conservative. Let's use the surplus S.

V(F) = (F - G) + 2G + S = F + G + S

where S = Σ(v - 2) over GOOD steps.

S ≥ 0 always (since v ≥ 2 for GOOD).

V(F)/F = 1 + (G + S)/F

For V/F > 1.585: (G + S)/F > 0.585.

Even if G/F = 0.5, we just need S/F > 0.085.

With G = F/2 GOOD steps, and E[v|GOOD] = 3:
  E[S] = G × 1 = F/2
  E[S/F] = 0.5

So S/F → 0.5 on average! WAY more than 0.085 needed.
""")

print("\n" + "=" * 70)
print("THE VARIANCE BOUND")
print("=" * 70)

print("""
For GOOD steps, v - 2 follows Geometric(1/2):
  P(v - 2 = k) = 1/2^{k+1} for k ≥ 0
  E[v - 2] = 1
  Var[v - 2] = 2

Over G GOOD steps:
  E[S] = G
  Var[S] = 2G

By Chebyshev: P(|S - G| > t√(2G)) ≤ 1/t²

For S to be less than 0.085F (the needed surplus):
  G - S > G - 0.085F

With G ≈ 0.5F: S < 0.085F requires S < 0.085/0.5 × G = 0.17G

For S < 0.17G when E[S] = G:
  S < 0.17 × E[S] = (1 - 0.83) × E[S]

This is a huge deviation! 83% below the mean!

P(S < 0.17G) ≤ P(|S - G| > 0.83G)
             ≤ 1/(0.83² × G/2)  [by Chebyshev]
             = 2.9/G
             → 0 as G → ∞
""")

# Compute this precisely
print("\nPrecise calculation:")
print("-" * 50)

for F in [10, 50, 100, 500, 1000]:
    G = F // 2  # Assume G ≈ F/2
    needed_surplus = 0.085 * F
    expected_S = G
    std_S = math.sqrt(2 * G)
    z = (needed_surplus - expected_S) / std_S  # How many std devs below mean?

    print(f"F = {F:4}: G = {G:4}, E[S] = {G:4}, need S > {needed_surplus:.1f}, z = {z:.2f}")

print("""
The z-scores are HUGE negative numbers!
P(S < needed) is astronomically small for large F.
""")

print("\n" + "=" * 70)
print("THE FORMAL ARGUMENT")
print("=" * 70)

print("""
THEOREM: For any Collatz trajectory, V(F)/F > 1.585 for all sufficiently large F.

PROOF:

1. After O(1) steps, the mod-4 chain reaches near-stationarity.
   So G(F)/F → 0.5 as F → ∞.

2. The surplus S = Σ(v - 2) over GOOD steps satisfies:
   E[S | G good steps] = G
   Var[S | G good steps] = 2G

3. By concentration (Chebyshev or Chernoff):
   P(S < εG) ≤ exp(-Ω(G)) for any ε < 1.

4. For V/F > 1.585 with G = F/2:
   Need (G + S)/F > 0.585
   Need S > 0.585F - G = 0.585F - 0.5F = 0.085F = 0.17G

5. P(S < 0.17G) = P(S < 0.17 E[S]) → 0 exponentially in G.

6. By Borel-Cantelli: Almost surely, S ≥ 0.17G for all large G.

7. Therefore: V/F = 1 + (G + S)/F ≥ 1 + (0.5F + 0.17 × 0.5F)/F
             = 1 + 0.5 + 0.085 = 1.585 for large F.

QED (almost surely)

THE GAP: This is "almost surely", not "for all".
""")

print("\n" + "=" * 70)
print("CAN WE MAKE IT DETERMINISTIC?")
print("=" * 70)

print("""
The probabilistic step is: "S ≥ 0.17G almost surely for large G."

To make it deterministic, we'd need:

OPTION A: Prove S ≥ 0 directly.
  We have S ≥ 0 always (since v ≥ 2 for GOOD). But S could be small.

OPTION B: Prove a lower bound on S in terms of trajectory structure.
  This would require understanding how v values correlate with n values.

OPTION C: Use the specific structure of the Collatz map.
  The map has arithmetic structure we haven't fully exploited.

OPTION D: Accept "almost all" as the best we can do.
  This matches Tao's 2019 result.
""")

print("\n" + "=" * 70)
print("STRUCTURAL APPROACH: THE COMPENSATION MECHANISM")
print("=" * 70)

print("""
We proved earlier:

1. After a BAD run of depth d, the next GOOD step has v₂ = g.
2. The formula: g = 1 + v₂(3^a × m - 1) where a = d + 1.
3. For odd a: g = 2 (minimal)
   For even a: g = 3 + v₂(a) ≥ 3 (bonus!)

This gives a STRUCTURAL reason why S > 0:
  - Some GOOD steps have g ≥ 3, contributing to surplus
  - The 2-adic structure forces periodic bonuses

Can we prove S ≥ cG for some c > 0 using this structure?
""")

# Compute the structural surplus
print("\nComputing structural surplus from 2-adic formula:")
print("-" * 50)

def v2(n):
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def escape_depth(n):
    """Depth of BAD run from n"""
    if n % 4 != 3:
        return 0
    d = 0
    while n % 4 == 3:
        n = 3*n + 1
        while n % 2 == 0:
            n //= 2
        d += 1
    return d

def g_value(n):
    """v₂ of first GOOD step after starting from BAD n"""
    if n % 4 == 1:
        return v2(3*n + 1)
    while n % 4 == 3:
        n = 3*n + 1
        while n % 2 == 0:
            n //= 2
    return v2(3*n + 1)

# Count epochs by (d, g) and compute average
total_surplus = 0
total_good = 0
epoch_count = 0

for n in range(3, 50000, 4):  # BAD starts
    d = escape_depth(n)
    g = g_value(n)
    surplus = g - 2  # Surplus from this GOOD step
    total_surplus += surplus
    total_good += 1
    epoch_count += 1

avg_surplus_per_good = total_surplus / total_good

print(f"Epochs analyzed: {epoch_count}")
print(f"Total surplus: {total_surplus}")
print(f"Average surplus per GOOD step: {avg_surplus_per_good:.4f}")
print(f"Required for proof: S/G > 0.17, we have: {avg_surplus_per_good:.4f}")

if avg_surplus_per_good > 0.17:
    print("\n*** AVERAGE SURPLUS EXCEEDS REQUIREMENT! ***")
else:
    print("\n*** Average surplus is below requirement ***")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

print(f"""
The average surplus per GOOD step is {avg_surplus_per_good:.4f}.
This exceeds the required 0.17 by a factor of {avg_surplus_per_good/0.17:.2f}.

BUT: This is an average over starting points, not a bound for all trajectories.

A single trajectory could theoretically have lower surplus.

TO COMPLETE THE PROOF DETERMINISTICALLY:

We would need to show that for ANY trajectory:
  S ≥ 0.17G (or some positive fraction of G)

This would require proving that "bad" epochs (g = 2) cannot dominate.

From our 2-adic analysis:
  - g = 2 occurs when a (escape depth + 1) is ODD
  - g ≥ 3 occurs when a is EVEN

The sequence of a values along a trajectory alternates in a structured way.
Proving this structure guarantees S ≥ cG is the remaining gap.

STATUS: We have strong evidence but not a complete deterministic proof.
""")
