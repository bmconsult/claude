# Groove Algorithm Design: Motor-Prediction Music Generation

**Generated**: December 7, 2024
**Based on**: Music domain validation (motor-prediction boundary hypothesis)
**Purpose**: Apply theory to create practical groove generation algorithm

## The Theoretical Foundation

From the music hypothesis:
- **Groove exists at motor prediction boundary**
- Too predictable → boring (no engagement)
- Too unpredictable → ungroovable (no entrainment)
- The sweet spot: Predictable enough to entrain, surprising enough to engage

**Key insight**: Groove = entrainment + surprise at the motor prediction boundary

## Algorithm Design

### Core Architecture

```
INPUT: Base tempo, time signature, style parameters
OUTPUT: Groove pattern (MIDI or audio)

PROCESS:
1. Generate base prediction (what motor system expects)
2. Add structured surprises (syncopation, microtiming)
3. Maintain envelope of predictability (stay at boundary)
4. Evaluate groove metrics
5. Iterate
```

### Component 1: The Base Prediction Engine

Generates what the motor system "expects":

```python
def generate_base_pattern(tempo, time_sig, style):
    """
    Generate metrically regular pattern - the prediction target.

    This is what the listener's motor system will anticipate.
    The groove comes from departures from this baseline.
    """
    # Strong beats: downbeats, beat 1
    # Weak beats: off-beats
    # Style affects beat weighting (e.g., backbeat in rock)

    base = []
    for measure in range(num_measures):
        for beat in range(beats_per_measure):
            strength = get_beat_strength(beat, time_sig, style)
            base.append({
                'time': (measure * beats_per_measure + beat) * beat_duration,
                'strength': strength,
                'predicted_velocity': strength_to_velocity(strength)
            })
    return base
```

### Component 2: The Surprise Generator

Adds deviations that create groove:

```python
def add_groove_surprises(base_pattern, groove_params):
    """
    Add structured surprises to base pattern.

    Types of surprise:
    1. Syncopation: Shifting emphasis to weak beats
    2. Microtiming: Small timing deviations from grid
    3. Ghost notes: Quiet notes between main beats
    4. Velocity variation: Dynamic surprises
    """

    grooved = []
    for beat in base_pattern:
        # Syncopation: Sometimes shift strong to weak
        if should_syncopate(beat, groove_params):
            beat = shift_to_off_beat(beat)

        # Microtiming: Push or pull from grid
        timing_offset = calculate_microtiming(
            beat,
            groove_params['push_pull'],  # e.g., laid-back vs. on-top
            groove_params['swing_ratio']
        )
        beat['time'] += timing_offset

        # Ghost notes
        if should_add_ghost(beat, groove_params):
            ghosts = generate_ghost_notes(beat)
            grooved.extend(ghosts)

        # Velocity variation
        beat['velocity'] = add_velocity_variation(beat, groove_params)

        grooved.append(beat)

    return grooved
```

### Component 3: The Boundary Regulator

Keeps groove at prediction boundary:

```python
def regulate_boundary(pattern, boundary_params):
    """
    Ensure pattern stays at motor prediction boundary.

    Too predictable: Add more surprise
    Too surprising: Pull back toward regularity

    This is the key insight from the theory:
    Groove lives at the BOUNDARY, not at maximum surprise.
    """

    # Calculate current predictability
    predictability = calculate_predictability(pattern)

    # Target range (the boundary)
    target_low = boundary_params['min_predictability']
    target_high = boundary_params['max_predictability']

    if predictability > target_high:
        # Too predictable - add surprise
        pattern = increase_surprise(pattern)
    elif predictability < target_low:
        # Too surprising - add regularity
        pattern = increase_regularity(pattern)

    return pattern
```

### Component 4: Groove Metrics

Quantify groove quality:

```python
def calculate_groove_metrics(pattern):
    """
    Metrics based on theory:

    1. Entrainment potential: Can motor system lock on?
    2. Surprise score: How much deviation from prediction?
    3. Boundary distance: How close to prediction boundary?
    4. Fractal dimension: Self-similarity across timescales?
    """

    metrics = {}

    # Entrainment: Phase-locking potential
    # Higher = easier to entrain
    metrics['entrainment'] = calculate_phase_lock_potential(pattern)

    # Surprise: Information content above baseline
    metrics['surprise'] = calculate_pattern_entropy(pattern) - baseline_entropy

    # Boundary distance: Optimal is 0
    optimal_predictability = get_boundary_target()
    actual_predictability = calculate_predictability(pattern)
    metrics['boundary_distance'] = abs(actual_predictability - optimal_predictability)

    # Fractal: Self-similarity (good grooves are fractal)
    metrics['fractal_dimension'] = calculate_fractal_dimension(pattern)

    # Combined groove score
    metrics['groove_score'] = combine_metrics(metrics)

    return metrics
```

## Style-Specific Parameters

Different styles occupy different positions on the boundary:

| Style | Syncopation | Microtiming | Ghost Notes | Swing |
|-------|-------------|-------------|-------------|-------|
| Funk | High | Medium push | Many | Low |
| Jazz swing | Medium | Medium pull | Few | High |
| Hip-hop | Medium | Strong pull (laid-back) | Some | Low |
| House | Low | Tight to grid | Few | Low |
| Reggae | High (off-beat) | Pull | Medium | Low |
| Bossa nova | Medium | Subtle push-pull | Many | Medium |

## Implementation Notes

### Key Libraries
- `pretty_midi`: MIDI manipulation
- `librosa`: Audio analysis
- `numpy`: Numerical computation

### Testable Predictions

If the theory is correct:

1. **Patterns at boundary** should get higher "groove ratings" from listeners
2. **Moving off boundary** (more predictable OR more surprising) should reduce ratings
3. **Different styles** should occupy different but identifiable boundary positions
4. **Cross-cultural similarity**: The boundary should be similar across cultures (motor systems are universal)

### Validation Approach

1. Generate patterns at different boundary positions
2. Human subject rating (groove-o-meter)
3. Map ratings to boundary distance
4. Should see: Peak ratings at boundary, falling off on both sides

## The Bigger Picture

This isn't just a groove generator - it's a **boundary navigation system**.

The same architecture could generate:
- Melodies at expectation boundary
- Harmonies at resolution boundary
- Song structures at predictability boundary

**Music generation = boundary navigation in multiple dimensions simultaneously.**

## Minimum Viable Implementation

```python
# Simplified groove generator

import random
import math

def simple_groove(tempo_bpm=120, bars=4, surprise_level=0.3):
    """
    Generate a simple groove pattern.

    surprise_level: 0.0 = metronomic, 1.0 = chaotic
                    0.3 is near the boundary
    """
    beat_ms = 60000 / tempo_bpm
    sixteenth = beat_ms / 4

    pattern = []

    for bar in range(bars):
        for beat in range(16):  # 16th notes
            base_time = bar * 4 * beat_ms + beat * sixteenth

            # Base strength (1 and 3 are strong in 4/4)
            if beat % 4 == 0:
                strength = 1.0
            elif beat % 2 == 0:
                strength = 0.7
            else:
                strength = 0.4

            # Add surprise at boundary
            if random.random() < surprise_level:
                # Syncopation: boost weak beat
                if strength < 0.7:
                    strength = min(1.0, strength + 0.4)
                # Microtiming: push or pull
                timing_offset = random.gauss(0, sixteenth * 0.1)
                base_time += timing_offset
                # Velocity variation
                strength *= random.gauss(1.0, 0.1)

            # Only include notes above threshold
            if strength > 0.3:
                pattern.append({
                    'time': base_time,
                    'velocity': int(min(127, max(1, strength * 100)))
                })

    return pattern

# Demo
if __name__ == "__main__":
    groove = simple_groove(tempo_bpm=90, bars=2, surprise_level=0.3)
    print(f"Generated {len(groove)} notes")
    for note in groove[:8]:
        print(f"  Time: {note['time']:.0f}ms, Velocity: {note['velocity']}")
```

---

*This design applies the motor-prediction boundary theory to practical music generation. The key insight: Don't maximize surprise or regularity - navigate to the boundary between them.*

*Potential application: Royalty-free groove generation, practice tools, game music, AI DJ systems.*

