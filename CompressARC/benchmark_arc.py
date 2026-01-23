#!/usr/bin/env python3
"""
Benchmark the integrated solver on real ARC puzzles.

Runs on the 400 training puzzles and reports:
- Overall accuracy
- Accuracy by method (Hopfield, synthesis, fallback)
- Failure analysis (what types of puzzles fail)
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict
import time

from integrated_solver import IntegratedARCSolver


def load_puzzle(path: Path) -> Dict:
    """Load an ARC puzzle from JSON."""
    with open(path) as f:
        return json.load(f)


def run_benchmark(data_dir: str, max_puzzles: int = None, verbose: bool = True):
    """
    Run benchmark on ARC puzzles.

    Args:
        data_dir: Path to ARC training data
        max_puzzles: Limit number of puzzles (for quick testing)
        verbose: Print per-puzzle results
    """
    data_path = Path(data_dir)
    puzzle_files = sorted(data_path.glob("*.json"))

    if max_puzzles:
        puzzle_files = puzzle_files[:max_puzzles]

    print("=" * 70)
    print(f"ARC BENCHMARK: {len(puzzle_files)} puzzles")
    print("=" * 70)

    solver = IntegratedARCSolver(hdc_dim=5000)

    results = {
        'solved': [],
        'failed': [],
        'by_method': defaultdict(list),
        'errors': [],
    }

    start_time = time.time()

    for i, puzzle_file in enumerate(puzzle_files):
        puzzle_id = puzzle_file.stem
        puzzle = load_puzzle(puzzle_file)

        # Get training pairs
        train_pairs = []
        for example in puzzle.get('train', []):
            inp = np.array(example['input'])
            out = np.array(example['output'])
            train_pairs.append((inp, out))

        # Get test case(s)
        test_cases = puzzle.get('test', [])

        puzzle_solved = True
        methods_used = []

        for test_idx, test_case in enumerate(test_cases):
            test_input = np.array(test_case['input'])
            expected_output = np.array(test_case['output'])

            try:
                # Clear Hopfield memory between puzzles (each puzzle is independent)
                solver.hopfield.clear()
                solver.total_attempts = 0
                solver.solved_by_hopfield = 0
                solver.solved_by_synthesis = 0
                solver.solved_by_fallback = 0

                predicted, method, confidence = solver.solve(test_input, train_pairs)

                if predicted is not None and predicted.shape == expected_output.shape and np.array_equal(predicted, expected_output):
                    methods_used.append(method)
                else:
                    puzzle_solved = False
                    methods_used.append(f"WRONG:{method}")

            except Exception as e:
                puzzle_solved = False
                methods_used.append(f"ERROR:{str(e)[:30]}")
                results['errors'].append((puzzle_id, str(e)))

        if puzzle_solved:
            results['solved'].append(puzzle_id)
            for m in methods_used:
                results['by_method'][m].append(puzzle_id)
            if verbose:
                print(f"  ✓ {puzzle_id} via {methods_used[0]}")
        else:
            results['failed'].append(puzzle_id)
            if verbose:
                print(f"  ✗ {puzzle_id} ({methods_used})")

        # Progress
        if (i + 1) % 50 == 0:
            elapsed = time.time() - start_time
            pct = 100 * len(results['solved']) / (i + 1)
            print(f"\n  Progress: {i+1}/{len(puzzle_files)} - {pct:.1f}% solved - {elapsed:.1f}s elapsed\n")

    # Summary
    total_time = time.time() - start_time
    total = len(puzzle_files)
    solved = len(results['solved'])

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nSolved: {solved}/{total} ({100*solved/total:.1f}%)")
    print(f"Time: {total_time:.1f}s ({total_time/total:.2f}s per puzzle)")

    print(f"\nBy method:")
    for method, puzzles in sorted(results['by_method'].items()):
        print(f"  {method}: {len(puzzles)}")

    if results['errors']:
        print(f"\nErrors: {len(results['errors'])}")
        for pid, err in results['errors'][:5]:
            print(f"  {pid}: {err[:50]}")

    # Analyze some failures
    print(f"\nSample failures (first 10):")
    for pid in results['failed'][:10]:
        print(f"  {pid}")

    return results


def analyze_failure(puzzle_id: str, data_dir: str):
    """Analyze why a specific puzzle failed."""
    path = Path(data_dir) / f"{puzzle_id}.json"
    puzzle = load_puzzle(path)

    print(f"\n=== Analyzing {puzzle_id} ===")

    # Show training examples
    for i, ex in enumerate(puzzle.get('train', [])):
        inp = np.array(ex['input'])
        out = np.array(ex['output'])
        print(f"\nTrain {i}: {inp.shape} → {out.shape}")
        print(f"Input:\n{inp}")
        print(f"Output:\n{out}")

    # Show test
    for i, ex in enumerate(puzzle.get('test', [])):
        inp = np.array(ex['input'])
        out = np.array(ex['output'])
        print(f"\nTest {i}: {inp.shape} → {out.shape}")
        print(f"Input:\n{inp}")
        print(f"Expected:\n{out}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='ARC-AGI-master/data/training',
                       help='Path to ARC training data')
    parser.add_argument('--max', type=int, default=None,
                       help='Max puzzles to test')
    parser.add_argument('--analyze', type=str, default=None,
                       help='Analyze specific puzzle ID')
    parser.add_argument('--quiet', action='store_true',
                       help='Less verbose output')
    args = parser.parse_args()

    if args.analyze:
        analyze_failure(args.analyze, args.data)
    else:
        results = run_benchmark(args.data, max_puzzles=args.max, verbose=not args.quiet)
