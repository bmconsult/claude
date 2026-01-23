"""
Training with Transfer Learning

This script extends CompressARC's training to use the abstraction library.
The key hypothesis: solving puzzles builds transferable knowledge.

THE REAL TEST:
- Train on puzzle A, save abstraction
- Train on puzzle B (similar structure)
- If B trains FASTER because of A, we have transfer
- If not, we're just memorizing, not learning

This is the difference between a toy and the real thing.
"""

import time
import numpy as np
import torch
from tqdm import tqdm

import preprocessing
import arc_compressor
import solution_selection
import visualization
from abstraction_library import get_library, AbstractionLibrary


np.random.seed(0)
torch.manual_seed(0)


def train_single_puzzle(
    task,
    model,
    optimizer,
    n_iterations: int = 2000,
    library: AbstractionLibrary = None,
    use_transfer: bool = True,
    early_stop_threshold: float = 0.1,
    verbose: bool = True
) -> dict:
    """
    Train a model on a single puzzle, optionally using transfer from library.

    Returns training statistics for transfer analysis.
    """
    train_history_logger = solution_selection.Logger(task)

    # Track baseline (no transfer) vs with transfer
    used_abstractions = []
    baseline_init = None

    if use_transfer and library and len(library.abstractions) > 0:
        # Save baseline initialization for comparison
        baseline_init = {k: (v[0].clone(), v[1].clone())
                        for k, v in model.multiposteriors.items()}

        # Try to get initialization from library
        transfer_init = library.get_initialization(
            model.multiposteriors,
            top_k=3,
            blend_weight=0.3
        )

        if transfer_init is not None:
            # Apply transfer initialization
            for k in model.multiposteriors:
                if k in transfer_init:
                    model.multiposteriors[k] = (
                        transfer_init[k][0].clone().requires_grad_(True),
                        transfer_init[k][1].clone().requires_grad_(True)
                    )

            # Track which abstractions we're using
            similar = library.find_similar(baseline_init, k=3)
            used_abstractions = [a.puzzle_id for a, _ in similar]

            if verbose:
                print(f"  Using transfer from: {used_abstractions[:3]}")

    # Training loop
    start_time = time.time()
    losses = []
    solved_at_step = None

    iterator = tqdm(range(n_iterations), disable=not verbose)
    for train_step in iterator:
        # Forward pass
        optimizer.zero_grad()
        logits, x_mask, y_mask, KL_amounts, KL_names = model.forward()
        logits = torch.cat([torch.zeros_like(logits[:, :1, :, :]), logits], dim=1)

        # Compute loss (same as original)
        total_KL = sum(torch.sum(kl) for kl in KL_amounts)
        reconstruction_error = compute_reconstruction_error(
            task, logits, x_mask, y_mask, train_step
        )
        loss = total_KL + 10 * reconstruction_error

        losses.append(loss.item())

        # Backward pass
        loss.backward()
        optimizer.step()

        # Log for solution checking
        train_history_logger.log(
            train_step, logits, x_mask, y_mask,
            KL_amounts, KL_names, total_KL, reconstruction_error, loss
        )

        # Check if solved
        if train_history_logger.is_solved() and solved_at_step is None:
            solved_at_step = train_step
            if verbose:
                iterator.set_description(f"Solved at step {train_step}")

        # Early stopping if loss is very low
        if loss.item() < early_stop_threshold and train_step > 100:
            if verbose:
                print(f"  Early stop at step {train_step}, loss={loss.item():.4f}")
            break

    training_time = time.time() - start_time

    return {
        "puzzle_id": task.task_name if hasattr(task, 'task_name') else str(id(task)),
        "solved": solved_at_step is not None,
        "solved_at_step": solved_at_step,
        "final_loss": losses[-1] if losses else float('inf'),
        "training_time": training_time,
        "total_steps": len(losses),
        "used_abstractions": used_abstractions,
        "multiposteriors": model.multiposteriors  # For saving to library
    }


def compute_reconstruction_error(task, logits, x_mask, y_mask, train_step):
    """Compute reconstruction error (same as original train.py)."""
    reconstruction_error = 0

    for example_num in range(task.n_examples):
        for in_out_mode in range(2):
            if example_num >= task.n_train and in_out_mode == 1:
                continue

            grid_size_uncertain = not (
                task.in_out_same_size or
                task.all_out_same_size and in_out_mode == 1 or
                task.all_in_same_size and in_out_mode == 0
            )

            if grid_size_uncertain:
                coefficient = 0.01 ** max(0, 1 - train_step / 100)
            else:
                coefficient = 1

            logits_slice = logits[example_num, :, :, :, in_out_mode]
            problem_slice = task.problem[example_num, :, :, in_out_mode]
            output_shape = task.shapes[example_num][in_out_mode]

            x_log_partition, x_logprobs = mask_select_logprobs(
                coefficient * x_mask[example_num, :, in_out_mode], output_shape[0]
            )
            y_log_partition, y_logprobs = mask_select_logprobs(
                coefficient * y_mask[example_num, :, in_out_mode], output_shape[1]
            )

            if grid_size_uncertain:
                x_log_partitions = []
                y_log_partitions = []
                for length in range(1, x_mask.shape[1] + 1):
                    x_log_partitions.append(
                        mask_select_logprobs(coefficient * x_mask[example_num, :, in_out_mode], length)[0]
                    )
                for length in range(1, y_mask.shape[1] + 1):
                    y_log_partitions.append(
                        mask_select_logprobs(coefficient * y_mask[example_num, :, in_out_mode], length)[0]
                    )
                x_log_partition = torch.logsumexp(torch.stack(x_log_partitions, dim=0), dim=0)
                y_log_partition = torch.logsumexp(torch.stack(y_log_partitions, dim=0), dim=0)

            logprobs = [[] for _ in range(x_logprobs.shape[0])]
            for x_offset in range(x_logprobs.shape[0]):
                for y_offset in range(y_logprobs.shape[0]):
                    logprob = x_logprobs[x_offset] - x_log_partition + y_logprobs[y_offset] - y_log_partition
                    logits_crop = logits_slice[:, x_offset:x_offset + output_shape[0],
                                              y_offset:y_offset + output_shape[1]]
                    target_crop = problem_slice[:output_shape[0], :output_shape[1]]
                    logprob = logprob - torch.nn.functional.cross_entropy(
                        logits_crop[None, ...], target_crop[None, ...], reduction='sum'
                    )
                    logprobs[x_offset].append(logprob)

            logprobs = torch.stack([torch.stack(lp, dim=0) for lp in logprobs], dim=0)

            if grid_size_uncertain:
                coefficient = 0.1 ** max(0, 1 - train_step / 100)
            else:
                coefficient = 1

            logprob = torch.logsumexp(coefficient * logprobs, dim=(0, 1)) / coefficient
            reconstruction_error = reconstruction_error - logprob

    return reconstruction_error


def mask_select_logprobs(mask, length):
    """Same as original train.py."""
    logprobs = []
    for offset in range(mask.shape[0] - length + 1):
        logprob = -torch.sum(mask[:offset])
        logprob = logprob + torch.sum(mask[offset:offset + length])
        logprob = logprob - torch.sum(mask[offset + length:])
        logprobs.append(logprob)
    logprobs = torch.stack(logprobs, dim=0)
    log_partition = torch.logsumexp(logprobs, dim=0)
    return log_partition, logprobs


def run_transfer_experiment(
    split: str = "training",
    n_puzzles: int = 20,
    n_iterations: int = 1500,
    verbose: bool = True
):
    """
    Run experiment to test if transfer learning works.

    Trains on puzzles sequentially, building the library.
    THE REAL TEST: Do later puzzles train faster?
    """
    library = get_library("transfer_experiment_library.pkl")

    # Clear library for fresh experiment
    library.abstractions = []
    library.save()

    # Get puzzles
    task_nums = list(range(n_puzzles))
    tasks = preprocessing.preprocess_tasks(split, task_nums)

    results = []
    baseline_times = []  # Track times without transfer
    transfer_times = []  # Track times with transfer

    print(f"\n{'='*60}")
    print("TRANSFER LEARNING EXPERIMENT")
    print(f"{'='*60}")
    print(f"Testing {n_puzzles} puzzles from {split} split")
    print(f"Hypothesis: Training time should DECREASE as library grows")
    print(f"{'='*60}\n")

    for i, task in enumerate(tasks):
        print(f"\n[{i+1}/{n_puzzles}] Puzzle: {task.task_name if hasattr(task, 'task_name') else i}")
        print(f"  Library size: {len(library.abstractions)}")

        # Create fresh model
        model = arc_compressor.ARCCompressor(task)
        optimizer = torch.optim.Adam(model.weights_list, lr=0.01, betas=(0.5, 0.9))

        # Train WITH transfer (if library has entries)
        use_transfer = len(library.abstractions) > 0
        result = train_single_puzzle(
            task, model, optimizer,
            n_iterations=n_iterations,
            library=library,
            use_transfer=use_transfer,
            verbose=verbose
        )

        results.append(result)

        # Track timing
        if use_transfer and result["used_abstractions"]:
            transfer_times.append(result["solved_at_step"] or n_iterations)
        else:
            baseline_times.append(result["solved_at_step"] or n_iterations)

        # Add to library if solved
        if result["solved"]:
            library.add(
                result["multiposteriors"],
                result["puzzle_id"],
                result["solved_at_step"],
                result["final_loss"]
            )
            print(f"  Added to library. New size: {len(library.abstractions)}")

            # Update transfer stats
            if result["used_abstractions"]:
                # Compare to baseline average
                avg_baseline = np.mean(baseline_times) if baseline_times else n_iterations
                helped = result["solved_at_step"] < avg_baseline * 0.8  # 20% faster = helped
                library.update_transfer_stats(result["used_abstractions"], helped)

    # RESULTS ANALYSIS
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")

    solved_count = sum(1 for r in results if r["solved"])
    print(f"Puzzles solved: {solved_count}/{n_puzzles}")

    if baseline_times and transfer_times:
        avg_baseline = np.mean(baseline_times)
        avg_transfer = np.mean(transfer_times)
        speedup = (avg_baseline - avg_transfer) / avg_baseline * 100

        print(f"\nBaseline avg steps to solve: {avg_baseline:.0f}")
        print(f"Transfer avg steps to solve: {avg_transfer:.0f}")
        print(f"Speedup: {speedup:.1f}%")

        if speedup > 10:
            print("\n✓ TRANSFER IS WORKING - Later puzzles train faster!")
        elif speedup > 0:
            print("\n~ MARGINAL TRANSFER - Some speedup but not conclusive")
        else:
            print("\n✗ NO TRANSFER - Library not helping")
    else:
        print("\nNot enough data for transfer comparison")

    # Library stats
    print(f"\nLibrary statistics:")
    stats = library.stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    return results, library


if __name__ == "__main__":
    # Quick test with small number of puzzles
    print("Running transfer learning experiment...")
    print("This tests whether solving puzzles builds transferable knowledge.\n")

    try:
        results, library = run_transfer_experiment(
            split="training",
            n_puzzles=10,  # Start small
            n_iterations=1000,
            verbose=True
        )
    except Exception as e:
        print(f"Error (likely no GPU): {e}")
        print("\nTo run on CPU, modify arc_compressor.py line 11:")
        print("  torch.set_default_device('cpu')")
