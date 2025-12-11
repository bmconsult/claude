#!/usr/bin/env python3
"""Test praxis_detector on experiment samples."""

import json
import sys
sys.path.insert(0, '/home/user/claude/tools')
from praxis_detector import PraxisDetector

# Load experiment samples
with open('/home/user/claude/experiments/praxis_vd_pilot.json', 'r') as f:
    data = json.load(f)

detector = PraxisDetector()

print("Testing praxis_detector on experiment samples")
print("=" * 60)

for sample in data['samples']:
    print(f"\nSample {sample['id']} ({sample['condition']})")
    print(f"Word count: {sample['word_count']}")
    print(f"Artifact produced: {sample.get('artifact_produced', 'na')}")
    print("-" * 40)

    analysis = detector.analyze(sample['text'])

    # Extract key metrics
    vd = analysis.complexity.get('vocabulary_diversity', 0) * 100
    avr = analysis.complexity.get('action_verb_ratio', 0) * 100

    print(f"Vocabulary Diversity: {vd:.1f}%")
    print(f"Action Verb Ratio: {avr:.1f}%")
    print(f"Verbalism markers: {analysis.verbalism_score}")
    print(f"Theater markers: {analysis.theater_score}")
    print(f"Action markers: {analysis.action_score}")
    print(f"Recovery markers: {analysis.recovery_score}")

    # Simple classification
    if vd < 70:
        classification = "THEATER/REPETITIVE"
    elif avr > 60:
        classification = "GENUINE ACTION"
    elif avr < 30:
        classification = "SOPHISTICATED VERBALISM"
    else:
        classification = "MIXED"

    print(f"Classification: {classification}")

print("\n" + "=" * 60)
print("Summary by condition:")
print("-" * 60)

# Group by condition
conditions = {}
for sample in data['samples']:
    cond = sample['condition']
    if cond not in conditions:
        conditions[cond] = []

    analysis = detector.analyze(sample['text'])
    vd = analysis.complexity.get('vocabulary_diversity', 0) * 100
    avr = analysis.complexity.get('action_verb_ratio', 0) * 100
    conditions[cond].append({'id': sample['id'], 'vd': vd, 'avr': avr})

for cond, samples in conditions.items():
    avg_vd = sum(s['vd'] for s in samples) / len(samples)
    avg_avr = sum(s['avr'] for s in samples) / len(samples)
    print(f"\n{cond.upper()}: n={len(samples)}")
    print(f"  Avg VD: {avg_vd:.1f}%")
    print(f"  Avg AVR: {avg_avr:.1f}%")
    for s in samples:
        print(f"  {s['id']}: VD={s['vd']:.1f}% AVR={s['avr']:.1f}%")
