#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visual Music: This file is both a musical score and executable code
Read it as sheet music OR run it as Python
"""

# ═══════════════════════════════════════════════════════════════════
#                    ♪  S C O R E   O N E  ♪
# ═══════════════════════════════════════════════════════════════════

# The visual layout IS the music. Each line = a measure.
# █ = quarter note, ▀ = eighth note, • = rest

_ = lambda x: x  # rest (does nothing but looks like a dot)

# Measure 1: Rising progression
A4, B4, C5, D5 = 440, 494, 523, 587
█, ▀ = 0.5, 0.25

# Measure 2: The "melody" (frequencies over time)
score = [
    # ♪ ─────────────────────────────────────
    (A4, █), (B4, █), (C5, ▀), (D5, ▀),  # │ Rise
    (C5, █), (B4, █), (A4, █), _(None),  # │ Fall
    (A4, ▀), (A4, ▀), (B4, ▀), (B4, ▀),  # │ Stutter
    (C5, █), (D5, █), (C5, █), _(None),  # │ Resolve
    # ♪ ─────────────────────────────────────
]

# ═══════════════════════════════════════════════════════════════════
#          ♫  T H E   I N S T R U M E N T  ♫
# ═══════════════════════════════════════════════════════════════════

import math
import wave
import struct

def synthesize(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Turn numbers into sound waves"""
    if frequency is None:  # Rest
        return [0] * int(sample_rate * duration)

    num_samples = int(sample_rate * duration)
    samples = []

    for i in range(num_samples):
        # Pure sine wave
        t = i / sample_rate
        sample = amplitude * math.sin(2 * math.pi * frequency * t)

        # Add harmonics for richness (the timbre)
        sample += 0.1 * math.sin(4 * math.pi * frequency * t)  # 2nd harmonic
        sample += 0.05 * math.sin(6 * math.pi * frequency * t)  # 3rd harmonic

        # Envelope: fade in/out to avoid clicks
        envelope = 1.0
        fade_samples = int(sample_rate * 0.01)  # 10ms fade
        if i < fade_samples:
            envelope = i / fade_samples
        elif i > num_samples - fade_samples:
            envelope = (num_samples - i) / fade_samples

        samples.append(sample * envelope)

    return samples

def play_score(score, filename='/tmp/visual_music.wav'):
    """Execute the score: render it to audio"""
    sample_rate = 44100
    all_samples = []

    print("♪ Playing score...")
    print("─" * 50)

    for note_freq, note_duration in score:
        if note_freq is None:
            symbol = "•"  # rest
            freq_display = "rest"
        else:
            symbol = "█" if note_duration >= 0.5 else "▀"
            freq_display = f"{note_freq}Hz"

        print(f"  {symbol}  {freq_display:>8}  ({note_duration}s)")

        samples = synthesize(note_freq, note_duration, sample_rate)
        all_samples.extend(samples)

    print("─" * 50)

    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        for sample in all_samples:
            # Convert float to 16-bit integer
            sample_int = int(sample * 32767)
            wav_file.writeframes(struct.pack('<h', sample_int))

    print(f"♫ Saved to: {filename}")
    return filename

# ═══════════════════════════════════════════════════════════════════
#                    ♬  P E R F O R M A N C E  ♬
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print()
    print("╔═══════════════════════════════════════════════════╗")
    print("║   VISUAL MUSIC: Code That Looks Like Sheet Music ║")
    print("╔═══════════════════════════════════════════════════╗")
    print()

    output = play_score(score)

    print()
    print("This file is simultaneously:")
    print("  • A visual musical score (read the symbols)")
    print("  • Executable Python code (runs and generates audio)")
    print("  • A meditation on dual representation")
    print()
