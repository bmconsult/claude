"""
Abstraction Library for CompressARC

This module implements transfer learning for MDL-based puzzle solving.
The core idea: successful puzzle solutions contain reusable abstractions.

When we solve puzzle A, the learned representation (multiposteriors) encodes
"what made this puzzle solvable." If puzzle B shares underlying structure,
initializing B with A's representation should make B faster to solve.

THE TEST: Training time decreases as library grows (for structurally similar problems).
If this doesn't happen, we're not learning transferable abstractions.
"""

import numpy as np
import torch
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import pickle
from pathlib import Path


@dataclass
class Abstraction:
    """
    A stored abstraction from a solved puzzle.

    Contains the learned representation that made the puzzle solvable,
    along with metadata for retrieval and tracking.
    """
    # The learned representation (flattened)
    representation: torch.Tensor

    # Metadata
    puzzle_id: str
    solve_time_steps: int
    final_loss: float

    # Transfer tracking
    times_used: int = 0
    times_helped: int = 0
    times_hurt: int = 0

    @property
    def transfer_score(self) -> float:
        """How useful is this abstraction for transfer?"""
        if self.times_used == 0:
            return 0.5  # Unknown
        return self.times_helped / (self.times_helped + self.times_hurt + 1e-6)


def iterate_multitensor(multitensor):
    """
    Iterate over all valid dims in a MultiTensor.
    Yields (dims, value) pairs.
    """
    for dims in multitensor.multitensor_system:
        value = multitensor[dims]
        if value is not None:
            yield (tuple(dims), value)


class AbstractionLibrary:
    """
    Stores and retrieves abstractions for transfer learning.
    """

    def __init__(self, save_path: str = "abstraction_library.pkl"):
        self.abstractions: List[Abstraction] = []
        self.save_path = Path(save_path)

        if self.save_path.exists():
            self.load()

    def add(self,
            multiposteriors,
            puzzle_id: str,
            solve_time_steps: int,
            final_loss: float):
        """Add a solved puzzle's representation to the library."""
        representation = self._flatten_multiposteriors(multiposteriors)

        abstraction = Abstraction(
            representation=representation,
            puzzle_id=puzzle_id,
            solve_time_steps=solve_time_steps,
            final_loss=final_loss
        )

        self.abstractions.append(abstraction)
        self.save()

    def _flatten_multiposteriors(self, multiposteriors) -> torch.Tensor:
        """Convert multiposteriors MultiTensor to a single vector."""
        flattened = []

        for dims, value in iterate_multitensor(multiposteriors):
            if value is not None:
                # value is (mean, local_capacity_adjustment) tuple
                mean, local_cap = value
                flattened.append(mean.detach().cpu().flatten())
                flattened.append(local_cap.detach().cpu().flatten())

        if not flattened:
            return torch.zeros(1)

        return torch.cat(flattened)

    def find_similar(self,
                     multiposteriors,
                     k: int = 5) -> List[Tuple[Abstraction, float]]:
        """Find the k most similar abstractions in the library."""
        if not self.abstractions:
            return []

        query = self._flatten_multiposteriors(multiposteriors)

        similarities = []
        for abstraction in self.abstractions:
            lib_rep = abstraction.representation
            min_size = min(len(query), len(lib_rep))

            if min_size == 0:
                continue

            q = query[:min_size]
            r = lib_rep[:min_size]

            # Cosine similarity
            norm_q = torch.norm(q)
            norm_r = torch.norm(r)
            if norm_q > 1e-6 and norm_r > 1e-6:
                sim = torch.dot(q, r) / (norm_q * norm_r)
                sim = sim.item()
            else:
                sim = 0.0

            # Penalize size mismatch
            size_penalty = min(len(query), len(lib_rep)) / max(len(query), len(lib_rep))
            sim *= size_penalty

            similarities.append((abstraction, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:k]

    def get_initialization_blend(self,
                                  template_multiposteriors,
                                  top_k: int = 3,
                                  blend_weight: float = 0.3) -> Optional[List[Tuple[Any, float]]]:
        """
        Get similar abstractions for blending.
        Returns list of (abstraction, similarity) tuples if library has entries.
        """
        similar = self.find_similar(template_multiposteriors, k=top_k)

        if not similar:
            return None

        # Filter by positive similarity and transfer score
        useful = [(a, s) for a, s in similar
                  if s > 0 and a.transfer_score >= 0.3]

        return useful if useful else None

    def update_transfer_stats(self,
                              used_abstraction_ids: List[str],
                              helped: bool):
        """Update transfer statistics after solving a puzzle."""
        for abstraction in self.abstractions:
            if abstraction.puzzle_id in used_abstraction_ids:
                abstraction.times_used += 1
                if helped:
                    abstraction.times_helped += 1
                else:
                    abstraction.times_hurt += 1

        self.save()

    def save(self):
        """Save library to disk."""
        with open(self.save_path, 'wb') as f:
            pickle.dump(self.abstractions, f)

    def load(self):
        """Load library from disk."""
        try:
            with open(self.save_path, 'rb') as f:
                self.abstractions = pickle.load(f)
        except Exception:
            self.abstractions = []

    def stats(self) -> dict:
        """Get library statistics."""
        if not self.abstractions:
            return {"size": 0}

        transfer_scores = [a.transfer_score for a in self.abstractions if a.times_used > 0]

        return {
            "size": len(self.abstractions),
            "total_uses": sum(a.times_used for a in self.abstractions),
            "avg_transfer_score": np.mean(transfer_scores) if transfer_scores else 0,
            "best_abstractions": sorted(
                [(a.puzzle_id, a.transfer_score) for a in self.abstractions if a.times_used > 0],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }


# Singleton
_library = None

def get_library(save_path: str = "abstraction_library.pkl") -> AbstractionLibrary:
    """Get or create the global abstraction library."""
    global _library
    if _library is None:
        _library = AbstractionLibrary(save_path)
    return _library
