"""
TRANSFER LEARNING TEST v2

v1 FAILED: Weight similarity was ~0, no transfer.
v2: Use PUZZLE-LEVEL similarity (structural features).

THE HYPOTHESIS:
If we find puzzles with similar STRUCTURE (similar sizes, transformations),
we might be able to transfer learned representations between them.

APPROACH:
1. Pre-compute puzzle similarities
2. Group similar puzzles
3. Train on one puzzle in group
4. Test if it helps solve other puzzles in same group
"""

import time
import numpy as np
import torch
from collections import defaultdict

import preprocessing
import arc_compressor
from puzzle_similarity import extract_features, compute_similarity, PuzzleLibrary


def find_puzzle_groups(tasks, threshold=0.85):
    """
    Group puzzles by structural similarity.
    Returns groups where puzzles in same group should benefit from transfer.
    """
    features = [extract_features(t) for t in tasks]

    # Build similarity matrix
    n = len(tasks)
    similarities = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                similarities[i, j] = compute_similarity(features[i], features[j])

    # Find groups (simple greedy clustering)
    groups = []
    used = set()

    for i in range(n):
        if i in used:
            continue

        group = [i]
        used.add(i)

        for j in range(i + 1, n):
            if j not in used and similarities[i, j] > threshold:
                group.append(j)
                used.add(j)

        if len(group) > 1:
            groups.append({
                'indices': group,
                'puzzles': [tasks[idx].task_name for idx in group],
                'similarities': [similarities[group[0], idx] for idx in group]
            })

    return groups, similarities


def train_puzzle(task, init_multiposteriors=None, max_steps=300):
    """
    Train on a puzzle, optionally with transferred initialization.
    """
    model = arc_compressor.ARCCompressor(task)
    optimizer = torch.optim.Adam(model.weights_list, lr=0.01, betas=(0.5, 0.9))

    # If we have transferred initialization, try to apply it
    # (Note: This is tricky because multiposteriors have task-specific shapes)
    # For now, we'll just track if similar puzzles train faster naturally

    target_loss = 50.0
    for step in range(max_steps):
        optimizer.zero_grad()
        logits, x_mask, y_mask, KL_amounts, KL_names = model.forward()
        logits = torch.cat([torch.zeros_like(logits[:, :1, :, :]), logits], dim=1)

        total_KL = sum(torch.sum(kl) for kl in KL_amounts)
        loss = total_KL

        loss.backward()
        optimizer.step()

        if loss.item() < target_loss:
            return {
                'solved': True,
                'steps': step,
                'loss': loss.item(),
                'multiposteriors': model.multiposteriors
            }

    return {
        'solved': False,
        'steps': max_steps,
        'loss': loss.item(),
        'multiposteriors': model.multiposteriors
    }


def run_experiment():
    """
    Test if structurally similar puzzles have correlated difficulty.

    Even without direct weight transfer, if similar puzzles have similar
    training dynamics, it suggests structure matters and transfer could work.
    """
    print("=" * 60)
    print("TRANSFER LEARNING TEST v2")
    print("=" * 60)
    print("Using PUZZLE-LEVEL similarity (not weight similarity)")
    print("=" * 60)

    # Get more puzzles to find groups
    tasks = preprocessing.preprocess_tasks('training', list(range(50)))

    # Find similar puzzle groups
    print("\n1. Finding similar puzzle groups...")
    groups, sim_matrix = find_puzzle_groups(tasks, threshold=0.85)

    print(f"   Found {len(groups)} groups with 2+ similar puzzles")
    for i, g in enumerate(groups[:5]):  # Show first 5
        print(f"   Group {i+1}: {g['puzzles']} (sim: {g['similarities'][1:]}")

    if not groups:
        print("\nNo similar puzzle groups found. Try lower threshold.")
        return

    # Test hypothesis: Similar puzzles should have similar training dynamics
    print("\n2. Testing if similar puzzles have correlated difficulty...")
    print("   (If they do, transfer should be possible)")

    correlation_data = []

    for group in groups[:3]:  # Test first 3 groups
        print(f"\n   Group: {group['puzzles']}")

        steps_list = []
        for idx in group['indices']:
            task = tasks[idx]
            result = train_puzzle(task, max_steps=200)
            steps_list.append(result['steps'])
            print(f"      {task.task_name}: {result['steps']} steps")

        # Compute correlation within group
        if len(steps_list) > 1:
            variance = np.std(steps_list)
            mean = np.mean(steps_list)
            cv = variance / mean if mean > 0 else 0  # Coefficient of variation
            correlation_data.append({
                'group': group['puzzles'],
                'steps': steps_list,
                'mean': mean,
                'std': variance,
                'cv': cv
            })

    # Compare to random puzzles
    print("\n3. Comparing to random (non-similar) puzzles...")
    random_indices = [0, 10, 20, 30, 40]
    random_steps = []
    for idx in random_indices[:5]:
        task = tasks[idx]
        result = train_puzzle(task, max_steps=200)
        random_steps.append(result['steps'])
        print(f"      {task.task_name}: {result['steps']} steps")

    random_cv = np.std(random_steps) / np.mean(random_steps) if np.mean(random_steps) > 0 else 0

    # Analysis
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    if correlation_data:
        avg_cv_similar = np.mean([d['cv'] for d in correlation_data])
        print(f"\nCoefficient of Variation (lower = more consistent):")
        print(f"  Similar puzzle groups: {avg_cv_similar:.3f}")
        print(f"  Random puzzles:        {random_cv:.3f}")

        if avg_cv_similar < random_cv:
            print("\n✓ Similar puzzles have MORE CONSISTENT training dynamics!")
            print("  This suggests structure matters and transfer could work.")
        else:
            print("\n✗ Similar puzzles NOT more consistent than random.")
            print("  Structural similarity may not predict training difficulty.")

    # Detailed group analysis
    print("\n" + "-" * 40)
    print("Per-group breakdown:")
    for d in correlation_data:
        print(f"  {d['group']}")
        print(f"    Steps: {d['steps']}")
        print(f"    Mean: {d['mean']:.1f}, Std: {d['std']:.1f}")


if __name__ == "__main__":
    run_experiment()
