#!/usr/bin/env python3
"""
DECOMPOSE THE 11

The 11/3 comes from:
- 10/3 from gluon loops
- 1/3 from ghost loops

What do 10 and 1 mean for SU(3)?
"""

def H(n):
    return 3*n*n - 3*n + 1

print("=" * 80)
print("DECOMPOSING THE 11")
print("=" * 80)

# SU(3) data
N = 3
dim = N**2 - 1  # = 8
rank = N - 1    # = 2
roots = N*(N-1) # = 6

print(f"\nSU(3) structure:")
print(f"  dim(su(3)) = {dim}")
print(f"  rank = {rank}")
print(f"  roots = {roots}")
print()

# The 11 decomposition
gauge_total = 11
gluon_part = 10  # from (10/3) × 3
ghost_part = 1   # from (1/3) × 3

print(f"The gauge contribution: (11/3) × 3 = {gauge_total}")
print(f"  Gluon loops: (10/3) × 3 = {gluon_part}")
print(f"  Ghost loops: (1/3) × 3 = {ghost_part}")
print()

# Check if 10 = dim + rank
print("=" * 80)
print("CHECKING: Is 10 = dim + rank?")
print("=" * 80)
print(f"\n  dim + rank = {dim} + {rank} = {dim + rank}")
print(f"  Gluon contribution = {gluon_part}")
print(f"  Match: {dim + rank == gluon_part} ✓" if dim + rank == gluon_part else f"  No match ✗")
print()

# Check if this generalizes
print("Does 10 = dim + rank generalize to other SU(N)?")
print()
for n in range(2, 7):
    dim_n = n**2 - 1
    rank_n = n - 1
    gluon_n = 10 * n / 3
    expected = dim_n + rank_n
    match = "✓" if abs(gluon_n - expected) < 0.01 else "✗"
    print(f"  SU({n}): (10/3)×{n} = {gluon_n:.2f}, dim+rank = {expected} {match}")

print()
print("The identity (10/3)N = dim + rank ONLY holds for N = 3!")

# Solve for when (10/3)N = dim + rank = N² + N - 2
print()
print("Solving (10/3)N = N² + N - 2:")
print("  10N/3 = N² + N - 2")
print("  10N = 3N² + 3N - 6")
print("  3N² - 7N - 6 = 0")
print("  N = (7 ± √(49 + 72))/6 = (7 ± 11)/6")
print("  N = 18/6 = 3 ✓ or N = -4/6 (unphysical)")

# The ghost contribution
print()
print("=" * 80)
print("THE GHOST CONTRIBUTION: 1")
print("=" * 80)
print()
print("Ghost loops contribute: (1/3) × 3 = 1")
print()
print("What is 1 in terms of SU(3)?")
print("  - The identity element")
print("  - The trivial representation (dim = 1)")
print("  - The center of the weight lattice (origin)")
print("  - H_1 = 1 (the zeroth hexagonal number)")
print()
print("In the A_2 root system: H_2 = 6 + 1 = roots + center")
print("The '+1' is the origin (weight 0).")
print()
print("Speculation: Ghost contribution = 1 = 'the center'")

# Full decomposition
print()
print("=" * 80)
print("FULL DECOMPOSITION")
print("=" * 80)
print()
print("For SU(3) with n_f = 6:")
print()
print("  Gauge: (11/3) × 3 = 11")
print("       = (10/3 × 3) + (1/3 × 3)")
print("       = 10 + 1")
print("       = (dim + rank) + 1")
print(f"       = ({dim} + {rank}) + 1")
print("       = 11 ✓")
print()
print("  Matter: (2/3) × 6 = 4")
print("        = (2/3) × roots")
print(f"        = (2/3) × {roots}")
print("        = 4 ✓")
print()
print("  β = Gauge - Matter")
print("    = 11 - 4")
print("    = (dim + rank + 1) - (2/3 × roots)")
print(f"    = ({dim} + {rank} + 1) - (2/3 × {roots})")
print("    = 11 - 4")
print("    = 7")
print(f"    = H_2 = {H(2)} ✓")

# Alternative form
print()
print("=" * 80)
print("ALTERNATIVE FORM")
print("=" * 80)
print()
print("  β = (dim + rank + 1) - (2/3 × roots)")
print()
print("  Using roots = N(N-1), rank = N-1, dim = N²-1:")
print()
print("  β = (N²-1 + N-1 + 1) - (2/3)N(N-1)")
print("    = N² + N - 1 - (2/3)N(N-1)")
print("    = N² + N - 1 - (2N² - 2N)/3")
print("    = (3N² + 3N - 3 - 2N² + 2N)/3")
print("    = (N² + 5N - 3)/3")
print()
print("  For N = 3: (9 + 15 - 3)/3 = 21/3 = 7 = H_2 ✓")
print()

# When is this hexagonal?
print("When is β = (N² + 5N - 3)/3 a centered hexagonal number?")
print()
for n in range(2, 8):
    beta = (n**2 + 5*n - 3) / 3
    is_hex = any(abs(H(k) - beta) < 0.01 for k in range(1, 20))
    hex_k = next((k for k in range(1, 20) if abs(H(k) - beta) < 0.01), None)
    status = f"= H_{hex_k}" if hex_k else "not hex"
    print(f"  N = {n}: β = {beta:.2f} {status}")

print()
print("ONLY N = 3 gives hexagonal β!")

# The structure
print()
print("=" * 80)
print("THE STRUCTURE")
print("=" * 80)
print("""
For SU(3) specifically:

  Gluon contribution: 10 = dim + rank = 8 + 2
  Ghost contribution: 1 = ? (center/identity)
  Total gauge: 11 = dim + rank + 1

  Matter contribution: 4 = (2/3) × roots = (2/3) × 6

  Net: β = 11 - 4 = 7 = H_2 = roots + 1

PATTERN:
  - H_2 = roots + 1 = 6 + 1 = 7
  - Gauge = (dim + rank) + 1 = 10 + 1 = 11
  - Both have a "+1" term

The "+1" in H_2 is the center of the hexagon.
The "+1" in the gauge contribution is the ghost loop.

SPECULATION:
  Ghost contribution = center of weight lattice?

  Ghosts are needed for gauge invariance in the path integral.
  They "see" the entire gauge orbit, including the identity.
  The "+1" might represent this.
""")

# Summary
print("=" * 80)
print("WHAT WE NOW KNOW")
print("=" * 80)
print("""
PROVEN (for SU(3)):
  1. 11 = dim + rank + 1 = 8 + 2 + 1
  2. 10 = dim + rank (gluon contribution)
  3. 1 = ghost contribution
  4. This decomposition is UNIQUE to N = 3

  (10/3)N = dim + rank only for N = 3
  (11/3)N = dim + rank + 1 only for N = 3

INTERPRETED:
  β = (dim + rank + 1) - (2/3 × roots)
    = (geometry of gauge) - (matter screening)
    = 7 = H_2

THE REMAINING QUESTION:
  Why does the gluon loop integral give exactly dim + rank?
  Why does the ghost loop give exactly 1?

  These come from Feynman diagram calculations.
  The fact that they match geometric quantities for SU(3) is observed.
  A derivation would require connecting loop integrals to Lie algebra structure.
""")

print("=" * 80)
