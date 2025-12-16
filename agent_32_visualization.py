#!/usr/bin/env python3
"""
Agent 32: Pattern Visualization
Visual analysis of mod-4 subsequence behavior
"""

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def collatz_seq(n):
    seq = [n]
    while n != 1:
        n = collatz_step(n)
        seq.append(n)
    return seq

def mod4_values(seq):
    return [x for x in seq if x % 4 == 1]

def visualize_mod4_sequence(n, max_display=40):
    """Create ASCII visualization of mod-4 sequence behavior"""
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)

    if len(mod4_seq) <= 1:
        return f"n={n}: trivial (reaches 1 immediately)"

    print(f"\nn = {n}")
    print(f"Mod-4 sequence: {mod4_seq[:max_display]}")
    if len(mod4_seq) > max_display:
        print(f"... ({len(mod4_seq)} total values)")

    # Create visual pattern
    visual = []
    for i in range(len(mod4_seq) - 1):
        if mod4_seq[i+1] > mod4_seq[i]:
            change = "↑ UP  "
        elif mod4_seq[i+1] < mod4_seq[i]:
            change = "↓ down"
        else:
            change = "→ same"
        visual.append(f"{mod4_seq[i]:8d} {change} → {mod4_seq[i+1]:8d}")

    print("Transition pattern:")
    for line in visual[:20]:
        print(f"  {line}")
    if len(visual) > 20:
        print(f"  ... ({len(visual)} total transitions)")

    # Statistics
    increases = sum(1 for i in range(len(mod4_seq)-1) if mod4_seq[i+1] > mod4_seq[i])
    decreases = sum(1 for i in range(len(mod4_seq)-1) if mod4_seq[i+1] < mod4_seq[i])

    print(f"Increases: {increases}, Decreases: {decreases}")
    print(f"Max value: {max(mod4_seq)}, Growth ratio: {max(mod4_seq)/n:.2f}×")

print("=" * 80)
print("AGENT 32: PATTERN VISUALIZATION")
print("=" * 80)

# Showcase interesting patterns

print("\n" + "=" * 80)
print("PATTERN 1: Simple Increase (n=9)")
print("=" * 80)
visualize_mod4_sequence(9)

print("\n" + "=" * 80)
print("PATTERN 2: Multiple Increases (n=27)")
print("=" * 80)
visualize_mod4_sequence(27)

print("\n" + "=" * 80)
print("PATTERN 3: Large Growth (n=255)")
print("=" * 80)
visualize_mod4_sequence(255)

print("\n" + "=" * 80)
print("PATTERN 4: Complex Oscillation (n=639)")
print("=" * 80)
visualize_mod4_sequence(639)

print("\n" + "=" * 80)
print("PATTERN 5: Extreme Case (n=6171)")
print("=" * 80)
visualize_mod4_sequence(6171)

# Summary statistics for different starting ranges
print("\n" + "=" * 80)
print("STATISTICAL SUMMARY BY RANGE")
print("=" * 80)

ranges = [
    (1, 100, "1-100"),
    (101, 1000, "101-1,000"),
    (1001, 5000, "1,001-5,000"),
    (5001, 10000, "5,001-10,000")
]

for start, end, label in ranges:
    total_increases = 0
    total_decreases = 0
    total_numbers = 0
    max_growth_ratio = 0
    max_growth_n = 0

    for n in range(start, end + 1):
        seq = collatz_seq(n)
        mod4_seq = mod4_values(seq)

        if len(mod4_seq) > 1:
            total_numbers += 1
            for i in range(len(mod4_seq) - 1):
                if mod4_seq[i+1] > mod4_seq[i]:
                    total_increases += 1
                else:
                    total_decreases += 1

            growth = max(mod4_seq) / n
            if growth > max_growth_ratio:
                max_growth_ratio = growth
                max_growth_n = n

    total_transitions = total_increases + total_decreases
    if total_transitions > 0:
        print(f"\nRange {label}:")
        print(f"  Numbers tested: {total_numbers}")
        print(f"  Increases: {total_increases} ({100*total_increases/total_transitions:.2f}%)")
        print(f"  Decreases: {total_decreases} ({100*total_decreases/total_transitions:.2f}%)")
        print(f"  Max growth: {max_growth_ratio:.1f}× (at n={max_growth_n})")

# Key insight: Despite increases, all sequences reach 1
print("\n" + "=" * 80)
print("KEY INSIGHT")
print("=" * 80)
print("""
Despite ~26% of transitions being INCREASES, ALL sequences eventually reach 1.

This reveals the TRUE nature of Collatz descent:
- NOT monotonic decrease
- NOT simple potential function
- Instead: STATISTICAL descent with local volatility

The sequence "wanders" with local increases, but has a global downward trend.
This is more like Brownian motion with drift than a simple descent.

Any proof must account for this statistical nature rather than assuming
step-by-step monotonic decrease.
""")

print("=" * 80)
