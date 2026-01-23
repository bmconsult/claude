#!/usr/bin/env python3
"""
EXPERIMENT 7: Cross-Domain Transfer

Tests whether MDL abstractions transfer between domains (ARC ↔ Game of Life).

This is the critical test for "better than LLMs":
- If transfer works across domains → domain-general intelligence
- If not → domain-specific pattern matching

Usage:
    python test_cross_domain.py --phase 1   # GoL cold baseline
    python test_cross_domain.py --phase 2   # ARC→GoL transfer
    python test_cross_domain.py --phase 3   # GoL→GoL learning curve
    python test_cross_domain.py --phase 4   # GoL→ARC transfer
    python test_cross_domain.py --all       # Run all phases
"""

import os
import sys
import json
import time
import pickle
import argparse
import shutil
from typing import Dict, List

import torch
import numpy as np

import preprocessing
import arc_compressor
import gol_generator

# Import from solve.py
from solve import AbstractionLibrary, LibraryEntry, solve_puzzle, solve_and_learn


LIBRARY_PATH = "abstraction_library.pkl"
ARC_LIBRARY_PATH = "arc_library_backup.pkl"
GOL_LIBRARY_PATH = "gol_library_backup.pkl"


def phase1_gol_baseline(n_puzzles: int = 10):
    """
    Phase 1: Solve GoL puzzles from scratch (no transfer).
    Establishes baseline for comparison.
    """
    print("=" * 60)
    print("PHASE 1: GoL COLD BASELINE (no transfer)")
    print("=" * 60)

    # Clear library
    if os.path.exists(LIBRARY_PATH):
        os.remove(LIBRARY_PATH)

    tasks = gol_generator.load_gol_tasks(list(range(n_puzzles)))
    print(f"Loaded {len(tasks)} GoL puzzles\n")

    results = []
    total_steps = 0

    for i, task in enumerate(tasks):
        print(f"[{i+1}/{n_puzzles}] {task.task_name}")

        # Solve WITHOUT library (fresh each time)
        library = AbstractionLibrary()  # Empty library each puzzle
        start = time.time()
        result = solve_puzzle(task, library)
        elapsed = time.time() - start

        status = "SOLVED" if result['solved'] else "FAILED"
        print(f"  {status} in {result['steps']} steps ({elapsed:.1f}s)")

        if result['solved']:
            total_steps += result['steps']
            results.append(result['steps'])

    print("\n" + "=" * 60)
    print("PHASE 1 RESULTS: GoL Baseline")
    print("=" * 60)
    print(f"Solved: {len(results)}/{n_puzzles}")
    if results:
        print(f"Average steps: {np.mean(results):.1f}")
        print(f"Total steps: {total_steps}")

    return results


def phase2_arc_to_gol(n_puzzles: int = 10):
    """
    Phase 2: Use ARC-trained weights on GoL puzzles.
    Tests cross-domain transfer.
    """
    print("=" * 60)
    print("PHASE 2: ARC → GoL TRANSFER")
    print("=" * 60)

    # First, train on ARC to build library
    print("\nStep 1: Building ARC library (10 puzzles)...")
    if os.path.exists(LIBRARY_PATH):
        os.remove(LIBRARY_PATH)

    arc_tasks = preprocessing.preprocess_tasks('training', list(range(10)))
    library = AbstractionLibrary()

    for i, task in enumerate(arc_tasks):
        result = solve_and_learn(task, library, verbose=False)
        print(f"  ARC [{i+1}/10]: {result['steps']} steps")

    # Save ARC library
    shutil.copy(LIBRARY_PATH, ARC_LIBRARY_PATH)
    print(f"\nARC library saved: {len(library.entries)} patterns")

    # Now test on GoL with ARC weights
    print(f"\nStep 2: Testing GoL with ARC transfer...")
    gol_tasks = gol_generator.load_gol_tasks(list(range(n_puzzles)))

    results = []
    for i, task in enumerate(gol_tasks):
        print(f"[{i+1}/{n_puzzles}] {task.task_name}")

        start = time.time()
        result = solve_puzzle(task, library)  # Use ARC library
        elapsed = time.time() - start

        transfer_info = ""
        if result['transfer_from']:
            pct = 100 * result['weights_transferred'] / result['weights_total']
            transfer_info = f" (transfer from ARC: {pct:.1f}% weights)"

        status = "SOLVED" if result['solved'] else "FAILED"
        print(f"  {status} in {result['steps']} steps{transfer_info}")

        if result['solved']:
            results.append(result['steps'])

    print("\n" + "=" * 60)
    print("PHASE 2 RESULTS: ARC → GoL Transfer")
    print("=" * 60)
    print(f"Solved: {len(results)}/{n_puzzles}")
    if results:
        print(f"Average steps with ARC transfer: {np.mean(results):.1f}")

    return results


def phase3_gol_learning_curve(n_puzzles: int = 25):
    """
    Phase 3: GoL→GoL transfer (same domain).
    Should show same learning curve as ARC (157→20→3→1).
    """
    print("=" * 60)
    print("PHASE 3: GoL → GoL LEARNING CURVE")
    print("=" * 60)

    # Clear library
    if os.path.exists(LIBRARY_PATH):
        os.remove(LIBRARY_PATH)

    library = AbstractionLibrary()
    tasks = gol_generator.load_gol_tasks(list(range(n_puzzles)))
    print(f"Loaded {len(tasks)} GoL puzzles\n")

    results = []
    for i, task in enumerate(tasks):
        print(f"[{i+1}/{n_puzzles}]", end="")
        result = solve_and_learn(task, library, verbose=True)
        results.append(result)

    # Save GoL library
    shutil.copy(LIBRARY_PATH, GOL_LIBRARY_PATH)

    print("\n" + "=" * 60)
    print("PHASE 3 RESULTS: GoL Learning Curve")
    print("=" * 60)

    solved = sum(1 for r in results if r['solved'])
    print(f"Solved: {solved}/{n_puzzles}")

    # Show learning curve
    print("\nLearning curve:")
    for i, r in enumerate(results[:10]):
        transfer = "TRANSFER" if r['transfer_from'] else "SCRATCH"
        print(f"  Puzzle {i+1}: {r['steps']:3d} steps ({transfer})")

    if len(results) > 10:
        remaining = [r['steps'] for r in results[10:] if r['solved']]
        if remaining:
            print(f"  Puzzles 11-{n_puzzles}: avg {np.mean(remaining):.1f} steps")

    return results


def phase4_gol_to_arc(n_puzzles: int = 10):
    """
    Phase 4: Use GoL-trained weights on ARC puzzles.
    Tests bidirectional transfer.
    """
    print("=" * 60)
    print("PHASE 4: GoL → ARC TRANSFER")
    print("=" * 60)

    # Load GoL library (from phase 3)
    if not os.path.exists(GOL_LIBRARY_PATH):
        print("ERROR: Run phase 3 first to build GoL library")
        return []

    shutil.copy(GOL_LIBRARY_PATH, LIBRARY_PATH)
    library = AbstractionLibrary()
    print(f"Loaded GoL library: {len(library.entries)} patterns\n")

    # Test on ARC
    arc_tasks = preprocessing.preprocess_tasks('training', list(range(n_puzzles)))

    results = []
    for i, task in enumerate(arc_tasks):
        print(f"[{i+1}/{n_puzzles}] {task.task_name}")

        start = time.time()
        result = solve_puzzle(task, library)  # Use GoL library
        elapsed = time.time() - start

        transfer_info = ""
        if result['transfer_from']:
            pct = 100 * result['weights_transferred'] / result['weights_total']
            transfer_info = f" (transfer from GoL: {pct:.1f}% weights)"

        status = "SOLVED" if result['solved'] else "FAILED"
        print(f"  {status} in {result['steps']} steps{transfer_info}")

        if result['solved']:
            results.append(result['steps'])

    print("\n" + "=" * 60)
    print("PHASE 4 RESULTS: GoL → ARC Transfer")
    print("=" * 60)
    print(f"Solved: {len(results)}/{n_puzzles}")
    if results:
        print(f"Average steps with GoL transfer: {np.mean(results):.1f}")

    return results


def run_all():
    """Run all phases and summarize."""
    print("\n" + "=" * 60)
    print("EXPERIMENT 7: CROSS-DOMAIN TRANSFER")
    print("=" * 60)
    print("Testing if MDL abstractions transfer between ARC and Game of Life\n")

    # Run all phases
    baseline = phase1_gol_baseline(10)
    print("\n")

    arc_to_gol = phase2_arc_to_gol(10)
    print("\n")

    gol_curve = phase3_gol_learning_curve(25)
    print("\n")

    gol_to_arc = phase4_gol_to_arc(10)

    # Final summary
    print("\n" + "=" * 60)
    print("EXPERIMENT 7: FINAL SUMMARY")
    print("=" * 60)

    baseline_avg = np.mean(baseline) if baseline else float('inf')
    arc_to_gol_avg = np.mean(arc_to_gol) if arc_to_gol else float('inf')
    gol_to_arc_avg = np.mean(gol_to_arc) if gol_to_arc else float('inf')

    print(f"\nGoL Baseline (no transfer):     {baseline_avg:.1f} avg steps")
    print(f"GoL with ARC transfer:          {arc_to_gol_avg:.1f} avg steps")

    if baseline_avg > 0:
        speedup = (baseline_avg - arc_to_gol_avg) / baseline_avg * 100
        print(f"ARC→GoL speedup:                {speedup:.1f}%")

    print(f"\nARC with GoL transfer:          {gol_to_arc_avg:.1f} avg steps")
    print(f"ARC baseline (from exp 5):      ~157 steps")

    if gol_to_arc_avg < 157:
        speedup = (157 - gol_to_arc_avg) / 157 * 100
        print(f"GoL→ARC speedup:                {speedup:.1f}%")

    # Verdict
    print("\n" + "-" * 60)
    if arc_to_gol_avg < baseline_avg * 0.5 and gol_to_arc_avg < 100:
        print("VERDICT: SUCCESS - Cross-domain transfer works!")
        print("The MDL abstractions are DOMAIN-GENERAL.")
    elif arc_to_gol_avg < baseline_avg * 0.8:
        print("VERDICT: PARTIAL - Some cross-domain transfer")
        print("Abstractions partially generalize across domains.")
    else:
        print("VERDICT: FAILED - No significant cross-domain transfer")
        print("Abstractions are domain-specific.")
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="Experiment 7: Cross-Domain Transfer")
    parser.add_argument('--phase', type=int, choices=[1, 2, 3, 4],
                        help='Run specific phase')
    parser.add_argument('--all', action='store_true',
                        help='Run all phases')
    parser.add_argument('--n', type=int, default=10,
                        help='Number of puzzles per phase')

    args = parser.parse_args()

    if args.all:
        run_all()
    elif args.phase == 1:
        phase1_gol_baseline(args.n)
    elif args.phase == 2:
        phase2_arc_to_gol(args.n)
    elif args.phase == 3:
        phase3_gol_learning_curve(args.n)
    elif args.phase == 4:
        phase4_gol_to_arc(args.n)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
