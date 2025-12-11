#!/usr/bin/env python3
"""
Testing the boundary: Can interference patterns reveal anything truly novel?

Specific hypothesis: If we encode the same data with intentionally different
structural representations, the interference patterns should reveal this difference
even though the logical content is identical.
"""

import numpy as np
from temporal_interference_codec import InterferenceCodec
import json


def test_representation_sensitivity():
    """
    Can interference patterns distinguish between different representations
    of the same logical data?
    """
    codec = InterferenceCodec()

    # Same logical data, three different representations
    flat = {"user_name": "Alice", "user_age": 30, "user_city": "NYC"}

    nested = {
        "user": {
            "name": "Alice",
            "age": 30,
            "city": "NYC"
        }
    }

    array_based = {
        "user": ["Alice", 30, "NYC"]
    }

    print("REPRESENTATION SENSITIVITY TEST")
    print("=" * 60)
    print("\nSame logical content, different representations:")
    print(f"Flat:        {flat}")
    print(f"Nested:      {nested}")
    print(f"Array-based: {array_based}")
    print()

    flat_sig = codec.encode(flat)
    flat_analysis = codec.analyze_interference(flat_sig)

    nested_sig = codec.encode(nested)
    nested_analysis = codec.analyze_interference(nested_sig)

    array_sig = codec.encode(array_based)
    array_analysis = codec.analyze_interference(array_sig)

    print("Interference Signatures:")
    print(f"Flat:        Entropy={flat_analysis['spectral_entropy']:.3f}, "
          f"Components={flat_analysis['num_wave_components']}")
    print(f"Nested:      Entropy={nested_analysis['spectral_entropy']:.3f}, "
          f"Components={nested_analysis['num_wave_components']}")
    print(f"Array-based: Entropy={array_analysis['spectral_entropy']:.3f}, "
          f"Components={array_analysis['num_wave_components']}")

    # Can we distinguish them by cross-correlation?
    flat_norm = flat_sig / np.linalg.norm(flat_sig)
    nested_norm = nested_sig / np.linalg.norm(nested_sig)
    array_norm = array_sig / np.linalg.norm(array_sig)

    corr_flat_nested = np.dot(flat_norm, nested_norm)
    corr_flat_array = np.dot(flat_norm, array_norm)
    corr_nested_array = np.dot(nested_norm, array_norm)

    print(f"\nCross-correlations (higher = more similar):")
    print(f"Flat vs Nested:      {corr_flat_nested:.4f}")
    print(f"Flat vs Array:       {corr_flat_array:.4f}")
    print(f"Nested vs Array:     {corr_nested_array:.4f}")

    print("\nConclusion: Can we distinguish representations?")
    if abs(corr_flat_nested - corr_flat_array) > 0.1:
        print("YES - Interference patterns are sensitive to representation!")
    else:
        print("NO - Too similar, just tracking component count")


def test_semantic_similarity():
    """
    The actually novel test: Can interference patterns reveal semantic
    similarity that's not obvious from structure alone?
    """
    codec = InterferenceCodec()

    # Structurally similar, semantically different
    person1 = {"name": "Alice", "value": 100}
    person2 = {"name": "Bob", "value": 200}

    # Structurally different, semantically similar
    person3 = {"user": {"name": "Alice", "salary": 100}}

    print("\n" + "=" * 60)
    print("SEMANTIC SIMILARITY TEST")
    print("=" * 60)
    print("\nStructurally similar, semantically different:")
    print(f"Person1: {person1}")
    print(f"Person2: {person2}")
    print("\nStructurally different, semantically similar to Person1:")
    print(f"Person3: {person3}")

    sig1 = codec.encode(person1)
    sig2 = codec.encode(person2)
    sig3 = codec.encode(person3)

    sig1_norm = sig1 / np.linalg.norm(sig1)
    sig2_norm = sig2 / np.linalg.norm(sig2)
    sig3_norm = sig3 / np.linalg.norm(sig3)

    corr_1_2 = np.dot(sig1_norm, sig2_norm)
    corr_1_3 = np.dot(sig1_norm, sig3_norm)

    print(f"\nCross-correlations:")
    print(f"Person1 vs Person2 (same structure, diff names): {corr_1_2:.4f}")
    print(f"Person1 vs Person3 (diff structure, same name): {corr_1_3:.4f}")

    if corr_1_3 > corr_1_2:
        print("\nSURPRISING: More similar to semantically similar case!")
        print("This might indicate genuine semantic sensitivity")
    else:
        print("\nEXPECTED: More similar to structurally similar case")
        print("This is just structure matching, not semantic")


def test_chaos_amplification():
    """
    Does interference amplify small differences?
    If we make a tiny change to data, does it produce
    a disproportionately large change in the interference pattern?
    """
    codec = InterferenceCodec()

    original = {"data": [1, 2, 3, 4, 5]}
    tiny_change = {"data": [1, 2, 3, 4, 6]}  # Changed last element

    print("\n" + "=" * 60)
    print("CHAOS AMPLIFICATION TEST")
    print("=" * 60)
    print(f"\nOriginal:    {original}")
    print(f"Tiny change: {tiny_change}")

    sig_orig = codec.encode(original)
    sig_changed = codec.encode(tiny_change)

    # Compare signals
    sig_orig_norm = sig_orig / np.linalg.norm(sig_orig)
    sig_changed_norm = sig_changed / np.linalg.norm(sig_changed)

    correlation = np.dot(sig_orig_norm, sig_changed_norm)
    l2_distance = np.linalg.norm(sig_orig - sig_changed)

    # What's the logical distance?
    # 1 value out of 5 changed = 20% change
    logical_distance = 0.20

    # What's the interference distance?
    interference_distance = 1 - correlation

    amplification_factor = interference_distance / logical_distance

    print(f"\nLogical distance:       {logical_distance:.2%}")
    print(f"Interference distance:  {interference_distance:.2%}")
    print(f"Amplification factor:   {amplification_factor:.2f}x")

    if amplification_factor > 2.0:
        print("\nCHAOS DETECTED: Small changes amplified!")
        print("This could be useful for change detection")
    elif amplification_factor < 0.5:
        print("\nDAMPENING: Changes are muted")
        print("This could be useful for noise resistance")
    else:
        print("\nLINEAR: Changes scale proportionally")
        print("No emergent amplification or dampening")


if __name__ == "__main__":
    test_representation_sensitivity()
    test_semantic_similarity()
    test_chaos_amplification()

    print("\n" + "=" * 60)
    print("FINAL VERDICT ON NOVELTY")
    print("=" * 60)
    print("""
If this technique:
1. Distinguishes representations -> Mildly interesting
2. Reveals semantic similarity -> Actually novel
3. Shows chaos amplification -> Potentially useful

Otherwise: Just a complex encoding with no emergent properties.
""")
