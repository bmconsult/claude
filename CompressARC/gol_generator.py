#!/usr/bin/env python3
"""
Game of Life Puzzle Generator

Generates Conway's Game of Life puzzles in ARC format.
Used for Experiment 7: Cross-Domain Transfer.

GoL Rules:
- Live cell with 2-3 neighbors survives
- Dead cell with exactly 3 neighbors becomes alive
- All other cells die/stay dead

Format matches ARC:
- problem['train']: list of {'input': grid, 'output': grid}
- problem['test']: list of {'input': grid, 'output': grid}
- solution: list of output grids for test examples
"""

import numpy as np
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Use same Task class as ARC
import preprocessing


def apply_gol_rules(grid: np.ndarray) -> np.ndarray:
    """Apply Game of Life rules to a grid."""
    rows, cols = grid.shape
    result = np.zeros_like(grid)

    for i in range(rows):
        for j in range(cols):
            # Count neighbors (with wrapping at edges)
            neighbors = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    # No wrapping - out of bounds = dead
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni, nj] > 0:  # Any non-zero is "alive"
                            neighbors += 1

            # Apply rules
            is_alive = grid[i, j] > 0
            if is_alive and neighbors in [2, 3]:
                result[i, j] = 1  # Survives
            elif not is_alive and neighbors == 3:
                result[i, j] = 1  # Birth
            # else: stays 0 (dead)

    return result


def generate_gol_puzzle(
    size: Tuple[int, int] = (8, 8),
    density: float = 0.3,
    n_train: int = 3,
    seed: int = None
) -> Tuple[Dict, List]:
    """
    Generate a GoL puzzle in ARC format.

    Args:
        size: Grid dimensions (rows, cols)
        density: Probability of cell being alive initially
        n_train: Number of training examples
        seed: Random seed for reproducibility

    Returns:
        problem: Dict with 'train' and 'test' keys
        solution: List of output grids for test
    """
    if seed is not None:
        np.random.seed(seed)

    examples = []
    for _ in range(n_train + 1):  # +1 for test example
        # Generate random initial state
        input_grid = (np.random.random(size) < density).astype(int)
        # Apply GoL rules
        output_grid = apply_gol_rules(input_grid)
        examples.append({
            'input': input_grid.tolist(),
            'output': output_grid.tolist()
        })

    problem = {
        'train': examples[:-1],
        'test': [{'input': examples[-1]['input'], 'output': examples[-1]['output']}]
    }
    solution = [examples[-1]['output']]

    return problem, solution


def generate_gol_dataset(
    n_puzzles: int = 100,
    min_size: int = 5,
    max_size: int = 12,
    base_seed: int = 42
) -> Tuple[Dict[str, Dict], Dict[str, List]]:
    """
    Generate a dataset of GoL puzzles.

    Returns:
        challenges: Dict mapping puzzle_id to problem
        solutions: Dict mapping puzzle_id to solution
    """
    challenges = {}
    solutions = {}

    for i in range(n_puzzles):
        # Vary sizes
        rows = np.random.randint(min_size, max_size + 1)
        cols = np.random.randint(min_size, max_size + 1)

        puzzle_id = f"gol_{i:04d}"
        problem, solution = generate_gol_puzzle(
            size=(rows, cols),
            density=np.random.uniform(0.2, 0.5),
            seed=base_seed + i
        )

        challenges[puzzle_id] = problem
        solutions[puzzle_id] = solution

    return challenges, solutions


def save_gol_dataset(n_puzzles: int = 100, output_dir: str = "dataset"):
    """Save GoL dataset in ARC format."""
    challenges, solutions = generate_gol_dataset(n_puzzles)

    with open(f"{output_dir}/gol_challenges.json", 'w') as f:
        json.dump(challenges, f)

    with open(f"{output_dir}/gol_solutions.json", 'w') as f:
        json.dump(solutions, f)

    print(f"Saved {n_puzzles} GoL puzzles to {output_dir}/")
    return challenges, solutions


def load_gol_tasks(task_indices: List[int] = None) -> List:
    """
    Load GoL puzzles as Task objects (same as ARC).

    Args:
        task_indices: Which puzzles to load (by index), or None for all

    Returns:
        List of Task objects
    """
    try:
        with open('dataset/gol_challenges.json', 'r') as f:
            challenges = json.load(f)
        with open('dataset/gol_solutions.json', 'r') as f:
            solutions = json.load(f)
    except FileNotFoundError:
        print("GoL dataset not found. Generating...")
        challenges, solutions = save_gol_dataset(100)

    task_names = list(challenges.keys())

    if task_indices is None:
        task_indices = range(len(task_names))

    tasks = []
    for i in task_indices:
        if i < len(task_names):
            name = task_names[i]
            tasks.append(preprocessing.Task(
                name,
                challenges[name],
                solutions.get(name)
            ))

    return tasks


if __name__ == "__main__":
    # Generate and save dataset
    print("Generating Game of Life dataset...")
    save_gol_dataset(100)

    # Test loading
    print("\nTesting load...")
    tasks = load_gol_tasks([0, 1, 2])
    for task in tasks:
        print(f"  {task.task_name}: {task.n_train} train, {task.n_test} test")

    # Visualize one example
    print("\nExample GoL puzzle:")
    problem, solution = generate_gol_puzzle(size=(6, 6), seed=42)
    input_grid = np.array(problem['train'][0]['input'])
    output_grid = np.array(problem['train'][0]['output'])

    print("Input:")
    print(input_grid)
    print("\nOutput (after 1 GoL step):")
    print(output_grid)
