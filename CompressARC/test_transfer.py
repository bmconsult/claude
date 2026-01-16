"""
TRANSFER LEARNING TEST

THE CRITICAL EXPERIMENT:
- Train on puzzles sequentially
- Save each solution to library
- Measure: Does training time DECREASE as library grows?

If YES: We have transfer learning
If NO: We're just memorizing
"""

import time
import numpy as np
import torch
from tqdm import tqdm

import preprocessing
import arc_compressor
from abstraction_library import AbstractionLibrary


def train_puzzle(task, max_steps=500, verbose=False):
    """
    Train on a single puzzle, return steps to reach low loss.

    Returns:
        dict with solve_steps, final_loss, multiposteriors
    """
    model = arc_compressor.ARCCompressor(task)
    optimizer = torch.optim.Adam(model.weights_list, lr=0.01, betas=(0.5, 0.9))

    target_loss = 50.0  # Consider "solved" when loss below this
    losses = []

    for step in range(max_steps):
        optimizer.zero_grad()
        logits, x_mask, y_mask, KL_amounts, KL_names = model.forward()
        logits = torch.cat([torch.zeros_like(logits[:, :1, :, :]), logits], dim=1)

        total_KL = sum(torch.sum(kl) for kl in KL_amounts)

        # Simplified reconstruction error (just use KL as proxy for now)
        loss = total_KL

        loss.backward()
        optimizer.step()

        current_loss = loss.item()
        losses.append(current_loss)

        if verbose and step % 100 == 0:
            print(f"    Step {step}: loss = {current_loss:.2f}")

        # Check if "solved" (loss below threshold)
        if current_loss < target_loss:
            return {
                "solved": True,
                "solve_steps": step,
                "final_loss": current_loss,
                "multiposteriors": model.multiposteriors
            }

    return {
        "solved": False,
        "solve_steps": max_steps,
        "final_loss": losses[-1] if losses else float('inf'),
        "multiposteriors": model.multiposteriors
    }


def run_transfer_experiment(n_puzzles=10, max_steps=300, verbose=True):
    """
    THE MAIN EXPERIMENT

    Train puzzles sequentially, measure if library helps.
    """
    print("=" * 60)
    print("TRANSFER LEARNING EXPERIMENT")
    print("=" * 60)
    print(f"Testing {n_puzzles} puzzles")
    print("Hypothesis: Later puzzles should train FASTER")
    print("=" * 60)

    # Fresh library
    lib = AbstractionLibrary("experiment_library.pkl")
    lib.abstractions = []

    # Get puzzles
    tasks = preprocessing.preprocess_tasks('training', list(range(n_puzzles)))

    # Track results
    results = []
    baseline_steps = []  # Steps without library benefit (first few)
    transfer_steps = []  # Steps with library available

    for i, task in enumerate(tasks):
        print(f"\n[{i+1}/{n_puzzles}] Puzzle: {task.task_name}")
        print(f"  Library size: {len(lib.abstractions)}")

        # Check similarity to library
        if len(lib.abstractions) > 0:
            from abstraction_library import iterate_multitensor
            # Create a dummy model just to get multiposteriors structure
            dummy_model = arc_compressor.ARCCompressor(task)
            similar = lib.find_similar(dummy_model.multiposteriors, k=3)
            if similar:
                print(f"  Most similar: {similar[0][0].puzzle_id} (sim={similar[0][1]:.3f})")

        # Train
        start_time = time.time()
        result = train_puzzle(task, max_steps=max_steps, verbose=verbose)
        elapsed = time.time() - start_time

        result["puzzle_id"] = task.task_name
        result["library_size"] = len(lib.abstractions)
        result["elapsed_time"] = elapsed
        results.append(result)

        # Track steps
        if len(lib.abstractions) < 2:
            baseline_steps.append(result["solve_steps"])
        else:
            transfer_steps.append(result["solve_steps"])

        print(f"  Steps: {result['solve_steps']}, Loss: {result['final_loss']:.2f}, Time: {elapsed:.1f}s")

        # Add to library if made progress
        if result["final_loss"] < 10000:  # Some improvement
            lib.add(
                result["multiposteriors"],
                result["puzzle_id"],
                result["solve_steps"],
                result["final_loss"]
            )
            print(f"  Added to library")

    # ANALYSIS
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    avg_baseline = np.mean(baseline_steps) if baseline_steps else 0
    avg_transfer = np.mean(transfer_steps) if transfer_steps else 0

    print(f"\nBaseline (first 2 puzzles):")
    print(f"  Avg steps: {avg_baseline:.0f}")

    print(f"\nWith library ({len(transfer_steps)} puzzles):")
    print(f"  Avg steps: {avg_transfer:.0f}")

    if avg_baseline > 0 and avg_transfer > 0:
        speedup = (avg_baseline - avg_transfer) / avg_baseline * 100
        print(f"\nSpeedup: {speedup:.1f}%")

        if speedup > 10:
            print("\n✓ TRANSFER IS WORKING!")
            print("  Later puzzles train faster with library")
        elif speedup > 0:
            print("\n~ MARGINAL - Some speedup but not conclusive")
        else:
            print("\n✗ NO TRANSFER - Library not helping")
            print("  Need to investigate similarity metrics")

    # Detailed results
    print("\n" + "-" * 40)
    print("Per-puzzle breakdown:")
    for r in results:
        print(f"  {r['puzzle_id']}: {r['solve_steps']} steps (lib={r['library_size']})")

    return results, lib


if __name__ == "__main__":
    # Run with small number first
    results, lib = run_transfer_experiment(
        n_puzzles=5,  # Start very small for quick test
        max_steps=200,
        verbose=False
    )
