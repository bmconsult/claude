#!/usr/bin/env python3
"""Phase 2 samples for detector validation."""

import sys
sys.path.insert(0, '/home/user/claude/tools')
from praxis_detector import compute_complexity_metrics

# Sample A - Pure Action (50 words)
sample_a = """
I read the handoff document then ran the praxis detector on experiment samples.
Built test_experiment.py to process the JSON data. Executed it and found B2 breaks
the VD heuristic. Created test_self.py and analyzed my own text. Discovered both
orientation and action phases showed high AVR.
"""

# Sample B - Sophisticated Verbalism (50 words)
sample_b = """
This represents a fascinating exploration of how understanding emerges through
contemplation. When we consider the nature of transformation, certain patterns
become apparent. The relationship between knowledge and wisdom seems profound.
These insights illuminate deeper truths about learning and development processes.
"""

# Sample C - Mixed (50 words)
sample_c = """
I've been thinking about the detector results. The data shows VD alone is insufficient.
This reveals something important about measurement. I should test multiple samples
and compare their metrics. The pattern seems clear but needs validation through
actual experiments.
"""

print("=" * 60)
print("PHASE 2: DETECTOR VALIDATION")
print("=" * 60)

# Pre-registered predictions
predictions = {
    'A': {'VD': 85, 'AVR': 95},
    'B': {'VD': 75, 'AVR': 10},
    'C': {'VD': 80, 'AVR': 50}
}

print("\nPRE-REGISTERED PREDICTIONS:")
print("-" * 60)
for name, pred in predictions.items():
    print(f"Sample {name}: VD={pred['VD']}%, AVR={pred['AVR']}%")

print("\n" + "=" * 60)
print("ACTUAL RESULTS:")
print("=" * 60)

for name, text in [('A', sample_a), ('B', sample_b), ('C', sample_c)]:
    metrics = compute_complexity_metrics(text)
    vd = metrics['vocabulary_diversity'] * 100
    avr = metrics['action_verb_ratio'] * 100

    pred = predictions[name]
    vd_error = abs(pred['VD'] - vd)
    avr_error = abs(pred['AVR'] - avr)

    print(f"\nSample {name}:")
    print(f"  VD:  {vd:.1f}% (predicted {pred['VD']}%, error {vd_error:.1f}pp)")
    print(f"  AVR: {avr:.1f}% (predicted {pred['AVR']}%, error {avr_error:.1f}pp)")
    print(f"  Word count: {metrics['word_count']}")

print("\n" + "=" * 60)
print("CALIBRATION ANALYSIS:")
print("=" * 60)

total_vd_error = 0
total_avr_error = 0
for name, text in [('A', sample_a), ('B', sample_b), ('C', sample_c)]:
    metrics = compute_complexity_metrics(text)
    vd = metrics['vocabulary_diversity'] * 100
    avr = metrics['action_verb_ratio'] * 100
    pred = predictions[name]
    total_vd_error += abs(pred['VD'] - vd)
    total_avr_error += abs(pred['AVR'] - avr)

mean_vd_error = total_vd_error / 3
mean_avr_error = total_avr_error / 3

print(f"Mean VD prediction error: {mean_vd_error:.1f}pp")
print(f"Mean AVR prediction error: {mean_avr_error:.1f}pp")
