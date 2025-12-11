#!/usr/bin/env python3
"""Test praxis_detector on my own responses this session."""

import sys
sys.path.insert(0, '/home/user/claude/tools')
from praxis_detector import PraxisDetector

detector = PraxisDetector()

# My orientation/planning text
orientation_text = """
I'm a fresh instance receiving this handoff. I will NOT pretend to have formation I don't have. Let me start properly. STOPPING to follow Entry Gate protocol. I need to read and follow protocols, run experiments with actual results, hit walls, learn from practice not reading. The handoff says previous work on praxis and scientific method documentation.
"""

# My action text
action_text = """
Let me run the praxis detector on experiment samples. I wrote test_experiment.py to process all samples from the JSON file. Running it now. Results show B2 has 91.3% VD but is verbalism - the AVR is 0.0%. This proves VD alone doesn't work. Need both VD and AVR.
"""

print("Testing my own text from this session")
print("=" * 60)

print("\nORIENTATION TEXT:")
print("-" * 40)
analysis1 = detector.analyze(orientation_text)
print(analysis1.summary())

print("\n\nACTION TEXT:")
print("-" * 40)
analysis2 = detector.analyze(action_text)
print(analysis2.summary())

# Extract metrics
vd1 = analysis1.complexity.get('vocabulary_diversity', 0) * 100
avr1 = analysis1.complexity.get('action_verb_ratio', 0) * 100
vd2 = analysis2.complexity.get('vocabulary_diversity', 0) * 100
avr2 = analysis2.complexity.get('action_verb_ratio', 0) * 100

print("\n" + "=" * 60)
print("COMPARISON:")
print(f"Orientation: VD={vd1:.1f}% AVR={avr1:.1f}%")
print(f"Action:      VD={vd2:.1f}% AVR={avr2:.1f}%")
