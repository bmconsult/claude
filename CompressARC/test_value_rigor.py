"""
Rigorous testing of value transform modules.
Tests: multiple trials, different random seeds, edge cases.
"""

import random
import torch
from value_modules import (
    ValueTransformSystem, apply_transform,
    ModularValueSystem, PointwiseModule, CumulativeModule, PairwiseModule
)


def test_multiple_trials():
    """Run multiple independent trials to verify consistency."""
    print("=" * 70)
    print("RIGOROUS VALUE TRANSFORM TESTING")
    print("=" * 70)

    transforms = [
        'identity', 'increment', 'double',
        'running_max', 'running_sum',
        'mirror_add', 'mirror_max'
    ]

    num_trials = 10
    num_test = 20

    print(f"\n{num_trials} independent trials per transform")
    print(f"{num_test} test examples per trial")
    print("-" * 70)

    results = {}

    for transform in transforms:
        successes = 0
        total_correct = 0

        for trial in range(num_trials):
            # Fresh system
            system = ValueTransformSystem(max_len=10)

            # Train on 15 examples
            for _ in range(15):
                inp = random.sample(range(1, 10), 5)
                out = apply_transform(transform, inp)
                system.add_example(inp, out)

            system.train_batch()

            # Test on 20 NEW examples
            correct = 0
            for _ in range(num_test):
                inp = random.sample(range(1, 10), 5)
                out = apply_transform(transform, inp)
                pred = system.predict(inp)
                if pred == out:
                    correct += 1

            total_correct += correct
            if correct == num_test:
                successes += 1

        accuracy = total_correct / (num_trials * num_test)
        results[transform] = {
            'successes': successes,
            'accuracy': accuracy
        }
        print(f"  {transform}: {successes}/{num_trials} trials at 100%, avg accuracy {accuracy*100:.0f}%")

    # Overall
    print("\n" + "=" * 70)
    total_successes = sum(r['successes'] for r in results.values())
    total_trials = num_trials * len(transforms)
    overall_acc = sum(r['accuracy'] for r in results.values()) / len(results)

    print(f"TOTAL: {total_successes}/{total_trials} trials at 100%")
    print(f"Overall average accuracy: {overall_acc*100:.0f}%")

    if total_successes == total_trials:
        print("\n✓ VERIFIED: 100% reliability across all transforms")
    else:
        print(f"\n✗ Reliability: {total_successes/total_trials*100:.0f}%")

    print("=" * 70)
    return results


def test_edge_cases():
    """Test edge cases."""
    print("\n" + "=" * 70)
    print("EDGE CASE TESTING")
    print("=" * 70)

    # Test running_max - a critical value transform
    system = ValueTransformSystem(max_len=10)

    # Train
    for _ in range(15):
        inp = random.sample(range(1, 10), 5)
        out = apply_transform('running_max', inp)
        system.add_example(inp, out)

    system.train_batch()

    print(f"\nLearned: {system.get_learned_structure()}")
    print("\nEdge cases for running_max:")

    cases = [
        ([5, 5, 5, 5, 5], "all same"),
        ([1, 2, 3, 4, 5], "ascending"),
        ([5, 4, 3, 2, 1], "descending"),
        ([1, 9, 1, 9, 1], "alternating"),
        ([9, 1, 1, 1, 1], "max at start"),
        ([1, 1, 1, 1, 9], "max at end"),
    ]

    correct = 0
    for inp, name in cases:
        out = apply_transform('running_max', inp)
        pred = system.predict(inp)
        match = "✓" if pred == out else "✗"
        if pred == out:
            correct += 1
        print(f"  {name}: {inp} → {pred} (expected {out}) {match}")

    print(f"\nEdge cases: {correct}/{len(cases)}")

    # Test mirror_add
    print("\n" + "-" * 70)
    system2 = ValueTransformSystem(max_len=10)

    # Train
    for _ in range(15):
        inp = random.sample(range(1, 10), 5)
        out = apply_transform('mirror_add', inp)
        system2.add_example(inp, out)

    system2.train_batch()

    print(f"\nLearned: {system2.get_learned_structure()}")
    print("\nEdge cases for mirror_add:")

    cases = [
        ([5, 5, 5, 5, 5], "all same"),
        ([1, 2, 3, 4, 5], "ascending"),
        ([1, 0, 0, 0, 1], "symmetric"),
        ([9, 1, 1, 1, 9], "ends heavy"),
        ([1, 9, 5, 9, 1], "middles heavy"),
    ]

    correct = 0
    for inp, name in cases:
        out = apply_transform('mirror_add', inp)
        pred = system2.predict(inp)
        match = "✓" if pred == out else "✗"
        if pred == out:
            correct += 1
        print(f"  {name}: {inp} → {pred} (expected {out}) {match}")

    print(f"\nEdge cases: {correct}/{len(cases)}")

    print("\n" + "=" * 70)


def test_different_lengths():
    """Test value transforms at different sequence lengths."""
    print("\n" + "=" * 70)
    print("DIFFERENT LENGTH TESTING")
    print("=" * 70)

    for transform in ['running_max', 'mirror_add', 'increment']:
        print(f"\n{transform}:")

        for length in [3, 4, 5, 6, 7]:
            system = ValueTransformSystem(max_len=10)

            # Train
            for _ in range(15):
                inp = random.sample(range(1, max(10, length+5)), length)
                out = apply_transform(transform, inp)
                system.add_example(inp, out)

            system.train_batch()

            # Test
            correct = 0
            for _ in range(20):
                inp = random.sample(range(1, max(10, length+5)), length)
                out = apply_transform(transform, inp)
                pred = system.predict(inp)
                if pred == out:
                    correct += 1

            print(f"  Length {length}: {correct}/20 ({correct/20*100:.0f}%)")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    test_multiple_trials()
    test_edge_cases()
    test_different_lengths()
