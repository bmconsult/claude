"""
Puzzle-Level Similarity for Transfer Learning

v1 FAILED because we compared learned weights, which are in different spaces.

v2: Compare puzzle INPUTS - structural features that define what kind of
problem this is, not how we solved it.

Key insight: Transfer should happen between puzzles with similar STRUCTURE,
not similar SOLUTIONS. Two puzzles that both involve "rotation + color flip"
should benefit from shared knowledge, even if their grid sizes differ.
"""

import numpy as np
import torch
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class PuzzleFeatures:
    """
    Structural features of a puzzle that determine what kind of problem it is.
    """
    puzzle_id: str

    # Grid features
    input_size: Tuple[int, int]  # (height, width) of input
    output_size: Tuple[int, int]  # (height, width) of output
    size_change: str  # 'same', 'expand', 'shrink', 'complex'

    # Color features
    num_colors: int
    color_preserved: bool  # Do same colors appear in input and output?

    # Pattern features (basic)
    has_symmetry: bool
    has_repetition: bool
    input_density: float  # Fraction of non-background cells

    # Transformation hints
    is_rotation: bool
    is_reflection: bool
    is_translation: bool

    def to_vector(self) -> np.ndarray:
        """Convert to feature vector for similarity computation."""
        return np.array([
            self.input_size[0] / 30,  # Normalized
            self.input_size[1] / 30,
            self.output_size[0] / 30,
            self.output_size[1] / 30,
            1.0 if self.size_change == 'same' else 0.0,
            1.0 if self.size_change == 'expand' else 0.0,
            1.0 if self.size_change == 'shrink' else 0.0,
            self.num_colors / 10,
            1.0 if self.color_preserved else 0.0,
            1.0 if self.has_symmetry else 0.0,
            1.0 if self.has_repetition else 0.0,
            self.input_density,
            1.0 if self.is_rotation else 0.0,
            1.0 if self.is_reflection else 0.0,
            1.0 if self.is_translation else 0.0,
        ], dtype=np.float32)


def extract_features(task) -> PuzzleFeatures:
    """
    Extract structural features from a puzzle task.
    """
    # Get first training example
    example = task.unprocessed_problem['train'][0]
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])

    # Grid sizes
    input_size = input_grid.shape
    output_size = output_grid.shape

    # Size change
    if input_size == output_size:
        size_change = 'same'
    elif output_size[0] > input_size[0] or output_size[1] > input_size[1]:
        size_change = 'expand'
    elif output_size[0] < input_size[0] or output_size[1] < input_size[1]:
        size_change = 'shrink'
    else:
        size_change = 'complex'

    # Colors
    input_colors = set(input_grid.flatten())
    output_colors = set(output_grid.flatten())
    all_colors = input_colors | output_colors
    num_colors = len(all_colors - {0})  # Exclude background
    color_preserved = input_colors == output_colors

    # Density
    input_density = np.sum(input_grid != 0) / input_grid.size

    # Simple symmetry check
    has_symmetry = (
        np.array_equal(input_grid, np.flip(input_grid, axis=0)) or
        np.array_equal(input_grid, np.flip(input_grid, axis=1))
    )

    # Simple repetition check (any 2x2 pattern appears multiple times)
    has_repetition = False
    if input_grid.shape[0] >= 2 and input_grid.shape[1] >= 2:
        patterns = set()
        for i in range(input_grid.shape[0] - 1):
            for j in range(input_grid.shape[1] - 1):
                pattern = tuple(input_grid[i:i+2, j:j+2].flatten())
                if pattern in patterns and pattern != (0, 0, 0, 0):
                    has_repetition = True
                    break
                patterns.add(pattern)

    # Transformation hints (very basic)
    is_rotation = False
    is_reflection = False
    is_translation = False

    if input_size == output_size:
        # Check for rotation
        if np.array_equal(output_grid, np.rot90(input_grid)):
            is_rotation = True
        # Check for reflection
        if (np.array_equal(output_grid, np.flip(input_grid, axis=0)) or
            np.array_equal(output_grid, np.flip(input_grid, axis=1))):
            is_reflection = True

    return PuzzleFeatures(
        puzzle_id=task.task_name,
        input_size=input_size,
        output_size=output_size,
        size_change=size_change,
        num_colors=num_colors,
        color_preserved=color_preserved,
        has_symmetry=has_symmetry,
        has_repetition=has_repetition,
        input_density=input_density,
        is_rotation=is_rotation,
        is_reflection=is_reflection,
        is_translation=is_translation
    )


def compute_similarity(features1: PuzzleFeatures, features2: PuzzleFeatures) -> float:
    """
    Compute similarity between two puzzles based on their structural features.

    Returns value in [0, 1] where 1 = identical structure.
    """
    v1 = features1.to_vector()
    v2 = features2.to_vector()

    # Euclidean distance, converted to similarity
    distance = np.linalg.norm(v1 - v2)
    max_distance = np.sqrt(len(v1))  # Maximum possible distance
    similarity = 1.0 - (distance / max_distance)

    return float(similarity)


class PuzzleLibrary:
    """
    Library of solved puzzles for transfer learning.

    Uses PUZZLE-LEVEL similarity (structural features) not weight similarity.
    """

    def __init__(self):
        self.entries: List[Dict[str, Any]] = []

    def add(self, task, multiposteriors, solve_steps: int, final_loss: float):
        """Add a solved puzzle to the library."""
        features = extract_features(task)

        self.entries.append({
            'features': features,
            'multiposteriors': multiposteriors,
            'solve_steps': solve_steps,
            'final_loss': final_loss,
            'times_used': 0,
            'times_helped': 0
        })

    def find_similar(self, task, k: int = 5) -> List[Tuple[Dict, float]]:
        """Find k most similar puzzles in library."""
        if not self.entries:
            return []

        query_features = extract_features(task)

        similarities = []
        for entry in self.entries:
            sim = compute_similarity(query_features, entry['features'])
            similarities.append((entry, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]

    def get_transfer_candidates(self, task, threshold: float = 0.7) -> List[Dict]:
        """Get entries similar enough to potentially help."""
        similar = self.find_similar(task, k=3)
        return [entry for entry, sim in similar if sim > threshold]

    def __len__(self):
        return len(self.entries)


def test_similarity():
    """Test that similarity works correctly."""
    import preprocessing

    # Get a few puzzles
    tasks = preprocessing.preprocess_tasks('training', list(range(10)))

    # Extract features
    features_list = [extract_features(t) for t in tasks]

    print("Puzzle Feature Comparison:")
    print("-" * 60)

    for i, f1 in enumerate(features_list[:5]):
        print(f"\n{f1.puzzle_id}:")
        print(f"  Size: {f1.input_size} -> {f1.output_size} ({f1.size_change})")
        print(f"  Colors: {f1.num_colors}, preserved: {f1.color_preserved}")
        print(f"  Patterns: sym={f1.has_symmetry}, rep={f1.has_repetition}")

        # Find most similar
        sims = []
        for j, f2 in enumerate(features_list):
            if i != j:
                sim = compute_similarity(f1, f2)
                sims.append((f2.puzzle_id, sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        print(f"  Most similar: {sims[0][0]} ({sims[0][1]:.3f})")


if __name__ == "__main__":
    test_similarity()
