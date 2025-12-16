#!/usr/bin/env python3
"""
Agent 32: Gap Verification
Specifically test the claims and gaps identified in FORMALIZATION_HITTING_TIME_PROOF.md
"""

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def syracuse_map(n):
    """S(n) = next odd number in trajectory"""
    if n % 2 == 0:
        raise ValueError("Syracuse map only defined for odd n")
    result = 3 * n + 1
    while result % 2 == 0:
        result //= 2
    return result

def collatz_seq(n):
    seq = [n]
    while n != 1:
        n = collatz_step(n)
        seq.append(n)
    return seq

def mod4_values(seq):
    return [x for x in seq if x % 4 == 1]

print("=" * 80)
print("AGENT 32: GAP VERIFICATION")
print("Testing specific claims from FORMALIZATION_HITTING_TIME_PROOF.md")
print("=" * 80)
print()

# CLAIM 1: Lemma 10.1 - If m ≡ 1 (mod 4) and m ≥ 5, then S(m) < m
print("CLAIM 1: Lemma 10.1 - If m ≡ 1 (mod 4), then S(m) < m")
print("-" * 80)

test_mod4_values = [x for x in range(1, 1001) if x % 4 == 1 and x > 1]
lemma_holds = True

for m in test_mod4_values:
    s_m = syracuse_map(m)
    if s_m >= m:
        print(f"✗ COUNTEREXAMPLE: m={m}, S(m)={s_m}, S(m) >= m")
        lemma_holds = False

print(f"Tested {len(test_mod4_values)} values m ≡ 1 (mod 4) with m ≥ 5")
if lemma_holds:
    print("✓ Lemma 10.1 VERIFIED: S(m) < m for all tested values")
else:
    print("✗ Lemma 10.1 FAILED")
print()

# CLAIM 2: The descent claim - the next ≡1 (mod 4) value is smaller
print("CLAIM 2: Theorem 10.3 - Sequence of ≡1 (mod 4) values is decreasing")
print("-" * 80)

counterexamples = []

for n in range(1, 1001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)

    # Check if strictly decreasing
    if len(mod4_seq) > 1:
        for i in range(len(mod4_seq) - 1):
            if mod4_seq[i+1] >= mod4_seq[i]:
                counterexamples.append((n, mod4_seq[i], mod4_seq[i+1]))
                break  # Only record first violation per n

print(f"Found {len(counterexamples)} counterexamples where vᵢ₊₁ ≥ vᵢ")
print()
print("First 30 counterexamples:")
for n, v_i, v_next in counterexamples[:30]:
    print(f"  n={n:4d}: {v_i:6d} → {v_next:6d} (increased by {v_next - v_i})")
print()

# SPECIFIC COUNTEREXAMPLE FROM PROOF: n = 9
print("SPECIFIC COUNTEREXAMPLE MENTIONED IN PROOF: n = 9")
print("-" * 80)

n = 9
seq = collatz_seq(n)
mod4_seq = mod4_values(seq)

print(f"Full sequence: {seq}")
print(f"Values ≡ 1 (mod 4): {mod4_seq}")
print()

if mod4_seq == [9, 17]:
    print("✓ CONFIRMED: n=9 gives mod-4 sequence [9, 17] with 17 > 9")
else:
    print(f"⚠ Unexpected: got {mod4_seq}")
print()

# Trace the path from 9 to 17
print("Detailed trace from 9 to 17:")
in_path = False
for i, val in enumerate(seq):
    if val == 9:
        in_path = True
    if in_path:
        mod4_status = " ≡1 (mod 4)" if val % 4 == 1 else ""
        print(f"  {i:2d}: {val:4d}{mod4_status}")
        if val == 17 and val != 9:
            break
print()

# ANALYSIS: How common is the increase pattern?
print("ANALYSIS: How common are increases in mod-4 sequences?")
print("-" * 80)

increase_count = 0
total_transitions = 0
numbers_with_increases = 0
numbers_tested = 0

for n in range(1, 10001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)

    if len(mod4_seq) > 1:
        numbers_tested += 1
        has_increase = False
        for i in range(len(mod4_seq) - 1):
            total_transitions += 1
            if mod4_seq[i+1] > mod4_seq[i]:
                increase_count += 1
                has_increase = True
        if has_increase:
            numbers_with_increases += 1

print(f"Numbers tested: {numbers_tested}")
print(f"Numbers with at least one increase: {numbers_with_increases} ({100*numbers_with_increases/numbers_tested:.1f}%)")
print(f"Total transitions: {total_transitions}")
print(f"Transitions that increase: {increase_count} ({100*increase_count/total_transitions:.2f}%)")
print()

# WHAT THE PROOF ACTUALLY SHOWS
print("WHAT THE PROOF ACTUALLY SHOWS:")
print("-" * 80)
print("✓ PROVEN: All trajectories hit n ≡ 1 (mod 4)")
print("✓ PROVEN: S(m) < m when m ≡ 1 (mod 4)")
print("✗ NOT PROVEN: The sequence of ≡1 (mod 4) values is decreasing")
print("✗ FAILED: Theorem 10.3 (claimed descent) is FALSE")
print()

print("IMPLICATION:")
print("-" * 80)
print("The hitting time proof is VALID for showing all trajectories hit ≡1 (mod 4).")
print("However, this does NOT prove trajectories reach 1, because the sequence of")
print("≡1 (mod 4) values can INCREASE, not just decrease.")
print()

# Additional finding: Do sequences eventually decrease after some increases?
print("DEEPER QUESTION: Do sequences eventually start decreasing?")
print("-" * 80)

never_decreases = []
for n in range(1, 1001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)

    if len(mod4_seq) > 2:
        # Check if there's ever a decrease
        has_decrease = any(mod4_seq[i+1] < mod4_seq[i] for i in range(len(mod4_seq)-1))
        if not has_decrease:
            never_decreases.append((n, mod4_seq))

print(f"Numbers where mod-4 sequence NEVER decreases: {len(never_decreases)}")
if never_decreases:
    print("Examples:")
    for n, seq in never_decreases[:10]:
        print(f"  n={n}: {seq}")
else:
    print("(All sequences eventually decrease)")
print()

# But they all reach 1!
print("OBSERVATION: All sequences reach 1 despite non-monotonicity!")
print("-" * 80)
print("This means descent happens, but through a more complex mechanism")
print("than simple monotonic decrease in the ≡1 (mod 4) values.")
print()

print("=" * 80)
print("GAP VERIFICATION COMPLETE")
print("=" * 80)
