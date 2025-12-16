#!/usr/bin/env python3
"""
Agent 36: Visualization and Deep Analysis
Analyze patterns in counter-examples
"""

import json
from collections import Counter
import math

def load_data():
    """Load counter-example data"""
    with open('/home/user/claude/agent_36_counter_examples.json', 'r') as f:
        return json.load(f)

def analyze_increase_patterns(data):
    """Analyze patterns in increases"""
    increasers = data['top_increasers']

    print("="*80)
    print("PATTERN ANALYSIS")
    print("="*80)
    print()

    # Distribution of worst ratios
    worst_ratios = [inc['worst_ratio'] for inc in increasers]

    print(f"Statistics on worst increase ratios:")
    print(f"  Mean: {sum(worst_ratios)/len(worst_ratios):.4f}")
    sorted_ratios = sorted(worst_ratios)
    print(f"  Median: {sorted_ratios[len(sorted_ratios)//2]:.4f}")
    mean = sum(worst_ratios)/len(worst_ratios)
    std = math.sqrt(sum((x-mean)**2 for x in worst_ratios)/len(worst_ratios))
    print(f"  Std Dev: {std:.4f}")
    print(f"  Min: {min(worst_ratios):.4f}")
    print(f"  Max: {max(worst_ratios):.4f}")
    print()

    # Distribution of number of increases
    num_increases = [inc['num_increases'] for inc in increasers]

    print(f"Statistics on number of increases per number:")
    print(f"  Mean: {sum(num_increases)/len(num_increases):.4f}")
    sorted_nums = sorted(num_increases)
    print(f"  Median: {sorted_nums[len(sorted_nums)//2]:.4f}")
    print(f"  Min: {min(num_increases)}")
    print(f"  Max: {max(num_increases)}")
    print()

    # Histogram of num_increases
    increase_counter = Counter(num_increases)
    print("Distribution of number of increases:")
    for k in sorted(increase_counter.keys())[:20]:
        print(f"  {k} increases: {increase_counter[k]} numbers ({100*increase_counter[k]/len(increasers):.2f}%)")
    print()

    # Analyze specific increase ratios
    specific_ratios = Counter()
    for inc in increasers:
        for increase in inc['increases']:
            ratio = increase['ratio']
            # Round to identify common patterns
            if ratio < 2:
                bucket = round(ratio, 4)
            elif ratio < 10:
                bucket = round(ratio, 2)
            else:
                bucket = int(ratio)
            specific_ratios[bucket] += 1

    print("Most common increase ratios (top 20):")
    for ratio, count in specific_ratios.most_common(20):
        print(f"  {ratio}×: {count} occurrences")
    print()

    # Look for the magic ratios
    print("Special ratio analysis:")
    print(f"  Ratio ≈ 1.125 (9/8): {specific_ratios.get(1.125, 0) + specific_ratios.get(1.1250, 0)} occurrences")
    print(f"  Ratio ≈ 1.6875 (27/16): {specific_ratios.get(1.6875, 0) + specific_ratios.get(1.69, 0)} occurrences")
    print(f"  Ratio ≈ 2.53125 (81/32): {specific_ratios.get(2.53, 0) + specific_ratios.get(2.5313, 0)} occurrences")
    print(f"  Ratio ≈ 2.8477 (729/256): {specific_ratios.get(2.85, 0) + specific_ratios.get(2.8477, 0) + specific_ratios.get(2.8476, 0)} occurrences")
    print(f"  Ratio ≈ 3.797 (243/64): {specific_ratios.get(3.80, 0) + specific_ratios.get(3.7969, 0)} occurrences")
    print()

def analyze_mod4_sequences(data):
    """Analyze properties of mod4 sequences"""
    increasers = data['top_increasers'][:1000]  # Top 1000

    print("="*80)
    print("MOD4 SEQUENCE ANALYSIS")
    print("="*80)
    print()

    # Sequence lengths
    seq_lengths = [len(inc['mod4_sequence']) for inc in increasers]

    print(f"Statistics on mod4 sequence lengths:")
    print(f"  Mean: {sum(seq_lengths)/len(seq_lengths):.4f}")
    sorted_lens = sorted(seq_lengths)
    print(f"  Median: {sorted_lens[len(sorted_lens)//2]:.4f}")
    print(f"  Min: {min(seq_lengths)}")
    print(f"  Max: {max(seq_lengths)}")
    print()

    # Peak position analysis
    print("Peak position in sequence (where max occurs):")
    peak_positions = []
    peak_position_ratios = []

    for inc in increasers:
        seq = inc['mod4_sequence']
        max_val = max(seq)
        peak_idx = seq.index(max_val)
        peak_positions.append(peak_idx)
        peak_position_ratios.append(peak_idx / len(seq))

    print(f"  Mean position: {sum(peak_positions)/len(peak_positions):.2f}")
    sorted_pos = sorted(peak_positions)
    print(f"  Median position: {sorted_pos[len(sorted_pos)//2]:.2f}")
    print(f"  Mean ratio (position/length): {sum(peak_position_ratios)/len(peak_position_ratios):.4f}")
    sorted_ratios = sorted(peak_position_ratios)
    print(f"  Median ratio: {sorted_ratios[len(sorted_ratios)//2]:.4f}")
    print()

    # Growth before peak
    print("Growth from start to peak:")
    growth_ratios = []
    for inc in increasers:
        seq = inc['mod4_sequence']
        start = seq[0]
        peak = max(seq)
        growth_ratios.append(peak / start)

    print(f"  Mean: {sum(growth_ratios)/len(growth_ratios):.4f}×")
    sorted_growth = sorted(growth_ratios)
    print(f"  Median: {sorted_growth[len(sorted_growth)//2]:.4f}×")
    print(f"  Max: {max(growth_ratios):.4f}×")
    print()

def find_special_patterns(data):
    """Look for special patterns in the data"""
    increasers = data['top_increasers']

    print("="*80)
    print("SPECIAL PATTERN SEARCH")
    print("="*80)
    print()

    # Numbers with many increases
    print("Numbers with most increases:")
    many_increases = sorted(increasers, key=lambda x: x['num_increases'], reverse=True)[:10]
    for i, inc in enumerate(many_increases, 1):
        print(f"  {i}. n={inc['n']}: {inc['num_increases']} increases, worst ratio {inc['worst_ratio']:.4f}×")
    print()

    # Numbers with largest absolute jumps
    print("Largest absolute jumps:")
    largest_jumps = []
    for inc in increasers:
        for increase in inc['increases']:
            largest_jumps.append((inc['n'], increase['from'], increase['to'], increase['difference']))
    largest_jumps.sort(key=lambda x: x[3], reverse=True)

    for i, (n, from_val, to_val, diff) in enumerate(largest_jumps[:10], 1):
        print(f"  {i}. n={n}: {from_val} → {to_val} (+{diff:,})")
    print()

    # Numbers that hit very high peaks relative to starting value
    print("Highest peak/start ratios:")
    peak_ratios = []
    for inc in increasers:
        seq = inc['mod4_sequence']
        start = seq[0]
        peak = max(seq)
        peak_ratios.append((inc['n'], start, peak, peak/start))
    peak_ratios.sort(key=lambda x: x[3], reverse=True)

    for i, (n, start, peak, ratio) in enumerate(peak_ratios[:10], 1):
        print(f"  {i}. n={n}: {start} → {peak} ({ratio:.4f}×)")
    print()

def theoretical_predictions(data):
    """Make theoretical predictions based on patterns"""
    print("="*80)
    print("THEORETICAL PREDICTIONS")
    print("="*80)
    print()

    print("Based on observed patterns, we predict:")
    print()

    print("1. INCREASE RATIOS:")
    print("   Common ratios appear to be powers of 3 divided by powers of 2:")
    print("   - 9/8 = 1.125")
    print("   - 27/16 = 1.6875")
    print("   - 81/32 = 2.53125")
    print("   - 243/64 = 3.796875")
    print("   - Pattern: 3^k / 2^m for various k, m")
    print()

    print("2. MECHANISM:")
    print("   When n ≡ 1 (mod 4), next mod4≡1 value is (3n+1)/2^k")
    print("   where k = ν₂(3n+1) is the 2-adic valuation.")
    print("   ")
    print("   For large jumps, need k to be SMALL (high 2-adic valuation).")
    print("   This happens when 3n+1 has few factors of 2.")
    print()

    print("3. WORST CASE CONSTRUCTION:")
    print("   To maximize increases, want:")
    print("   - n ≡ 1 (mod 4) such that ν₂(3n+1) is minimal")
    print("   - This creates the largest (3n+1)/2^k relative to n")
    print()

    print("4. PREDICTION FOR LARGER RANGES:")
    print("   Expect to find:")
    print("   - Increases > 1000× in range 100k-1M")
    print("   - Increases > 10000× in range 1M-10M")
    print("   - No theoretical upper bound on increase ratio")
    print()

    print("5. UNBOUNDED GROWTH?")
    print("   CONJECTURE: Cannot have unbounded growth because:")
    print("   - Would require infinitely many increases")
    print("   - Or a cycle not passing through 1")
    print("   - Both contradict Collatz conjecture")
    print("   ")
    print("   BUT: Proving bounds on finite growth is the HARD PART.")
    print()

def create_ascii_visualizations(data):
    """Create ASCII art visualizations"""
    increasers = data['top_increasers']

    print("="*80)
    print("ASCII VISUALIZATIONS")
    print("="*80)
    print()

    # Distribution of worst ratios (log scale histogram)
    print("Distribution of Worst Increase Ratios (log₁₀ scale):")
    worst_ratios = [inc['worst_ratio'] for inc in increasers]
    log_ratios = [math.log10(r) for r in worst_ratios]

    # Create histogram bins
    min_log = min(log_ratios)
    max_log = max(log_ratios)
    num_bins = 20
    bin_width = (max_log - min_log) / num_bins
    bins = [0] * num_bins

    for lr in log_ratios:
        bin_idx = min(int((lr - min_log) / bin_width), num_bins - 1)
        bins[bin_idx] += 1

    max_count = max(bins)
    for i, count in enumerate(bins):
        bin_start = min_log + i * bin_width
        bin_end = min_log + (i + 1) * bin_width
        bar = '#' * int(60 * count / max_count)
        print(f"  {bin_start:5.2f}-{bin_end:5.2f}: {bar} ({count})")
    print()

    # Worst case sequence visualization
    print("Worst Case Trajectory (n=77671):")
    worst_case = increasers[0]
    seq = worst_case['mod4_sequence']

    print(f"  Length: {len(seq)}, Peak: {max(seq):,}, Start: {seq[0]:,}")
    print()
    print("  Log₁₀ values:")

    log_seq = [math.log10(v) for v in seq]
    min_log_seq = min(log_seq)
    max_log_seq = max(log_seq)

    for i, (val, log_val) in enumerate(zip(seq[:20], log_seq[:20])):  # First 20
        bar_len = int(60 * (log_val - min_log_seq) / (max_log_seq - min_log_seq))
        bar = '█' * bar_len
        marker = '▲' if i < len(seq)-1 and seq[i+1] > val else '▼'
        print(f"  {i:2d}: {bar} {marker} {val:,}")

    if len(seq) > 20:
        print(f"  ... ({len(seq) - 20} more steps)")
    print()

def main():
    print("Loading data...")
    data = load_data()

    print(f"Loaded {len(data['top_increasers'])} top increasers\n")

    analyze_increase_patterns(data)
    analyze_mod4_sequences(data)
    find_special_patterns(data)
    theoretical_predictions(data)

    create_ascii_visualizations(data)

    print("\nAnalysis complete!")

if __name__ == '__main__':
    main()
