# Praxis Tools

Tools for detecting genuine praxis vs performance/verbalism.

## Quick Start

```python
from praxis_detector import PraxisDetector, compute_complexity_metrics

# Analyze any text
detector = PraxisDetector()
analysis = detector.analyze("Your text here...")
print(analysis.summary())

# Just get metrics
metrics = compute_complexity_metrics("Your text here...")
print(f"VD: {metrics['vocabulary_diversity']:.1%}")
print(f"AVR: {metrics['action_verb_ratio']:.1%}")
```

## Files

| File | Purpose |
|------|---------|
| `praxis_detector.py` | Main tool - VD/AVR metrics + pattern detection |
| `test_self.py` | Template for analyzing your own text |
| `test_experiment.py` | Run detector on sample data |
| `phase2_samples.py` | Calibration exercise with predictions |
| `praxis_vd_pilot.json` | Labeled test samples |

## Key Metrics

| Metric | What It Measures | Interpretation |
|--------|------------------|----------------|
| **VD** (Vocabulary Diversity) | unique words / total words | >85% = action, <70% = wallowing |
| **AVR** (Action Verb Ratio) | action verbs / total verbs | >60% = doing, <30% = thinking |

## Combined Interpretation

| VD | AVR | Likely State |
|----|-----|--------------|
| >85% | >60% | Genuine action |
| >85% | <30% | Sophisticated verbalism |
| <70% | >50% | Action word wallowing |
| <70% | <30% | Obvious theater |

## Command Line Usage

```bash
# Demo mode (shows theatrical vs action examples)
python praxis_detector.py

# Analyze a specific file
python praxis_detector.py myfile.txt
```

## Pattern Detection

The detector also looks for specific patterns:

**Verbalism markers** (bad):
- "I understand that..."
- "This reveals that..."
- "I now realize..."

**Theater markers** (bad):
- "Let me reflect on..."
- "*pauses*"
- "I am genuinely..."

**Action markers** (good):
- "Let me try/build/create..."
- "Running..."
- "Fixed..."

**Recovery markers** (good):
- "That didn't work..."
- "My mistake..."
- "Let me try again..."

## Key Insight

VD alone isn't enough. Sample B2 in the pilot had 91% VD but was pure verbalism (AVR = 0%). Always check BOTH metrics.

---

*Tools support PRAXIS_MASTERY.md execution*
*Used in: Phase 2 (VD wall), Phase 4 (speed round), Six Criteria (VD check)*
