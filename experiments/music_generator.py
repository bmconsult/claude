#!/usr/bin/env python3
"""
Simple music generator using ABC notation.
ABC is a text-based music notation format.
Can be converted to MIDI/sheet music with tools like abc2midi, abcm2ps.

This explores: can I generate coherent musical patterns?
"""

import random

# Musical vocabulary
NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
OCTAVE_MODIFIERS = ['', ',', "'"]  # default, lower, higher
DURATIONS = ['', '2', '3', '4', '/2', '/4']  # default=1, whole, dotted, 4 beats, half, quarter
RESTS = ['z', 'z2', 'z/2']

# Common chord progressions (in scale degrees)
PROGRESSIONS = {
    'pop': [1, 5, 6, 4],     # I-V-vi-IV
    'jazz': [2, 5, 1],       # ii-V-I
    'blues': [1, 1, 1, 1, 4, 4, 1, 1, 5, 4, 1, 5],  # 12-bar blues
    'classical': [1, 4, 5, 1],  # I-IV-V-I
}

def scale_degree_to_note(degree, key='C', mode='major'):
    """Convert scale degree to note name."""
    major_scale = [0, 2, 4, 5, 7, 9, 11]  # semitone offsets
    minor_scale = [0, 2, 3, 5, 7, 8, 10]

    key_offset = NOTES.index(key[0].upper())
    scale = major_scale if mode == 'major' else minor_scale

    degree_idx = (degree - 1) % 7
    note_idx = (key_offset + scale[degree_idx]) % 12

    # Map back to note name (simplified - ignores sharps/flats for now)
    chromatic = ['C', '^C', 'D', '^D', 'E', 'F', '^F', 'G', '^G', 'A', '^A', 'B']
    return chromatic[note_idx]

def generate_melody(length=16, key='C', mode='major'):
    """Generate a simple melody."""
    melody = []

    # Use scale degrees for coherence
    if mode == 'major':
        scale = [1, 2, 3, 4, 5, 6, 7, 8]  # 8 = octave up 1
    else:
        scale = [1, 2, 3, 4, 5, 6, 7, 8]

    # Weight toward chord tones (1, 3, 5)
    weights = [3, 1, 2, 1, 2, 1, 1, 1]  # 1,3,5 weighted higher

    prev_degree = 1
    for _ in range(length):
        # Favor stepwise motion
        step_options = [
            max(1, prev_degree - 2),
            max(1, prev_degree - 1),
            prev_degree,
            min(8, prev_degree + 1),
            min(8, prev_degree + 2),
        ]
        step_weights = [1, 3, 2, 3, 1]  # prefer small steps

        degree = random.choices(step_options, weights=step_weights)[0]
        note = scale_degree_to_note(degree, key, mode)

        # Random duration (weighted toward quarter notes)
        dur = random.choices(['', '2', '/2'], weights=[4, 1, 2])[0]

        melody.append(note + dur)
        prev_degree = degree

    return ' '.join(melody)

def generate_abc(title="Generated Piece", key='C', meter='4/4', length=32):
    """Generate a complete ABC notation piece."""

    abc = f"""X:1
T:{title}
M:{meter}
L:1/4
K:{key}
"""

    # Generate two phrases (A and B sections)
    phrase_a = generate_melody(length // 2, key, 'major')
    phrase_b = generate_melody(length // 2, key, 'major')

    # Structure: AABA (common song form)
    abc += f"|: {phrase_a} :|\n"
    abc += f"|: {phrase_b} :|\n"
    abc += f"|: {phrase_a} :|\n"

    return abc

def generate_minimalist():
    """
    Generate a minimalist/ambient piece.
    Inspired by Steve Reich, Brian Eno.
    Uses repetition with gradual variation.
    """
    abc = """X:1
T:Minimalist Study
M:4/4
L:1/8
K:C
"""

    # Base pattern
    patterns = [
        "C2 E2 G2 E2",
        "D2 F2 A2 F2",
        "E2 G2 B2 G2",
        "C2 G2 C'2 G2",
    ]

    base = random.choice(patterns)

    # Build through repetition with gradual change
    lines = []
    current = base
    for i in range(8):
        lines.append(f"|: {current} :|")
        # Occasional variation
        if random.random() < 0.3:
            current = random.choice(patterns)

    abc += '\n'.join(lines)
    return abc

def generate_ambient():
    """
    Generate an ambient/drone piece.
    Long held notes, sparse movement.
    """
    abc = """X:1
T:Ambient Drift
M:4/4
L:1/1
K:C
"""

    # Long tones
    drone_notes = ['C,', 'G,', 'C', 'E', 'G']
    melody_notes = ['C', 'D', 'E', 'G', 'A', "C'"]

    lines = []
    for _ in range(4):
        # Drone
        drone = random.choice(drone_notes)
        # Sparse melody
        mel = ' '.join(random.choices(melody_notes, k=2))
        lines.append(f"{drone}4 | {mel}2 z2 |")

    abc += '\n'.join(lines)
    return abc


if __name__ == "__main__":
    print("=== Standard Generated Melody ===")
    print(generate_abc("Algorithmic Etude"))
    print("\n" + "="*40 + "\n")

    print("=== Minimalist Study ===")
    print(generate_minimalist())
    print("\n" + "="*40 + "\n")

    print("=== Ambient Drift ===")
    print(generate_ambient())
