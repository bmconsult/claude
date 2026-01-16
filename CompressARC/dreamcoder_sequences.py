"""
Experiment 12: DreamCoder-Style Abstraction Learning for Sequences

This is NOT enumeration over a fixed DSL.
This LEARNS the DSL from data.

Key differences from v5/v6 (which were cheating):
- v5/v6: Fixed primitives, enumerate all, pick best match
- This: Start minimal, learn abstractions, library GROWS

The DreamCoder approach:
1. Start with base primitives (minimal)
2. Solve problems using search + neural guidance
3. Extract reusable sub-programs from solutions
4. Add abstractions to library (compression-based selection)
5. Future problems use learned abstractions

Success criteria (from charter):
- >80% accuracy on positional transforms (reverse, swap, running_max)
- Learning curve shows transfer (N → ... → 1)
- <1M parameters
- Runs on laptop CPU
- Generalizes to novel tasks
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Optional, Callable
from dataclasses import dataclass
import random
import time


# =============================================================================
# PART 1: THE PROGRAM REPRESENTATION
# =============================================================================

@dataclass
class Program:
    """A program is a tree of primitives."""
    name: str
    children: List['Program'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

    def __repr__(self):
        if not self.children:
            return self.name
        args = ', '.join(repr(c) for c in self.children)
        return f"{self.name}({args})"

    def depth(self) -> int:
        if not self.children:
            return 1
        return 1 + max(c.depth() for c in self.children)

    def size(self) -> int:
        """Description length proxy - number of nodes."""
        return 1 + sum(c.size() for c in self.children)


# =============================================================================
# PART 2: BASE PRIMITIVES (Minimal starting set)
# =============================================================================

class PrimitiveLibrary:
    """
    The library of primitives. Starts minimal, grows through learning.

    Unlike v5/v6 which had a FIXED set, this library EXPANDS.
    """

    def __init__(self):
        # Base primitives - the minimum needed to express anything
        self.primitives: Dict[str, Callable] = {
            # Identity
            'id': lambda x: x,

            # Element-wise operations
            'inc': lambda x: [v + 1 for v in x],
            'dec': lambda x: [v - 1 for v in x],

            # Positional operations (base)
            'first': lambda x: x[0] if x else 0,
            'last': lambda x: x[-1] if x else 0,
            'tail': lambda x: x[1:] if len(x) > 1 else [],
            'init': lambda x: x[:-1] if len(x) > 1 else [],

            # Constructors
            'cons': lambda h, t: [h] + t if isinstance(t, list) else [h, t],
            'append': lambda x, y: x + y if isinstance(x, list) and isinstance(y, list) else x,

            # Higher-order (will be key for learning)
            'map_inc': lambda x: [v + 1 for v in x],
            'map_dec': lambda x: [v - 1 for v in x],
        }

        # Learned abstractions - starts empty, grows
        self.learned: Dict[str, Tuple[Program, Callable]] = {}

        # Usage counts for MDL-based pruning
        self.usage_counts: Dict[str, int] = {k: 0 for k in self.primitives}

    def add_abstraction(self, name: str, program: Program, func: Callable):
        """Add a learned abstraction to the library."""
        self.learned[name] = (program, func)
        self.usage_counts[name] = 0
        print(f"  [LIBRARY] Added abstraction: {name} = {program}")

    def get_all_primitives(self) -> List[str]:
        """Get all available primitives (base + learned)."""
        return list(self.primitives.keys()) + list(self.learned.keys())

    def execute(self, name: str, *args):
        """Execute a primitive or learned abstraction."""
        self.usage_counts[name] = self.usage_counts.get(name, 0) + 1

        if name in self.primitives:
            return self.primitives[name](*args)
        elif name in self.learned:
            _, func = self.learned[name]
            return func(*args)
        else:
            raise ValueError(f"Unknown primitive: {name}")

    def description_length(self, program: Program) -> float:
        """
        MDL: Shorter programs that use common abstractions are better.

        Cost = base_cost + log(1 / frequency)

        Frequently used primitives are "cheaper" to use.
        """
        total_uses = sum(self.usage_counts.values()) + 1

        def node_cost(p: Program) -> float:
            freq = (self.usage_counts.get(p.name, 0) + 1) / total_uses
            base = 1.0  # Base cost per node
            freq_bonus = -0.5 * torch.log(torch.tensor(freq)).item()  # Frequent = cheaper
            return base + freq_bonus + sum(node_cost(c) for c in p.children)

        return node_cost(program)


# =============================================================================
# PART 3: PROGRAM SEARCH (Neural-guided)
# =============================================================================

class RecognitionModel(nn.Module):
    """
    Neural network that guides program search.

    Given (input, output) example, predicts which primitives are likely useful.
    This is what makes DreamCoder fast - instead of blind enumeration,
    the neural net focuses search on promising primitives.
    """

    def __init__(self, max_len: int = 10, max_val: int = 20, hidden_dim: int = 128):
        super().__init__()
        self.max_len = max_len
        self.max_val = max_val

        # Encode input and output sequences
        self.input_encoder = nn.Sequential(
            nn.Linear(max_len * max_val, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        self.output_encoder = nn.Sequential(
            nn.Linear(max_len * max_val, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        # Combine and predict primitive probabilities
        self.combiner = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        # Output head - will be resized as library grows
        self.num_primitives = 10  # Initial
        self.primitive_head = nn.Linear(hidden_dim, self.num_primitives)

    def encode_sequence(self, seq: List[int]) -> torch.Tensor:
        """One-hot encode a sequence."""
        encoding = torch.zeros(self.max_len * self.max_val)
        for i, v in enumerate(seq[:self.max_len]):
            if 0 <= v < self.max_val:
                encoding[i * self.max_val + v] = 1.0
        return encoding

    def forward(self, input_seq: List[int], output_seq: List[int]) -> torch.Tensor:
        """Predict primitive probabilities for this (input, output) pair."""
        inp_enc = self.input_encoder(self.encode_sequence(input_seq))
        out_enc = self.output_encoder(self.encode_sequence(output_seq))
        combined = self.combiner(torch.cat([inp_enc, out_enc]))
        logits = self.primitive_head(combined)
        return F.softmax(logits, dim=-1)

    def resize_for_library(self, num_primitives: int):
        """Resize output head when library grows."""
        if num_primitives != self.num_primitives:
            old_weight = self.primitive_head.weight.data
            old_bias = self.primitive_head.bias.data

            self.num_primitives = num_primitives
            self.primitive_head = nn.Linear(
                self.primitive_head.in_features,
                num_primitives
            )

            # Copy old weights
            min_prims = min(old_weight.shape[0], num_primitives)
            self.primitive_head.weight.data[:min_prims] = old_weight[:min_prims]
            self.primitive_head.bias.data[:min_prims] = old_bias[:min_prims]


class ProgramSearcher:
    """
    Search for programs that transform input to output.

    Uses recognition model to guide search (not blind enumeration).
    """

    def __init__(self, library: PrimitiveLibrary, recognition: RecognitionModel):
        self.library = library
        self.recognition = recognition
        self.max_depth = 4
        self.max_attempts = 1000

    def search(self, input_seq: List[int], output_seq: List[int]) -> Optional[Program]:
        """
        Search for a program that maps input to output.

        Returns the shortest (MDL) program found, or None.
        """
        # Get primitive probabilities from recognition model
        with torch.no_grad():
            probs = self.recognition(input_seq, output_seq)

        primitives = self.library.get_all_primitives()

        # Resize recognition model if needed
        if len(primitives) != self.recognition.num_primitives:
            self.recognition.resize_for_library(len(primitives))
            probs = self.recognition(input_seq, output_seq)

        # Sort primitives by probability (focus search)
        if len(probs) >= len(primitives):
            prim_probs = list(zip(primitives, probs[:len(primitives)].tolist()))
        else:
            prim_probs = [(p, 1.0/len(primitives)) for p in primitives]

        prim_probs.sort(key=lambda x: -x[1])

        best_program = None
        best_dl = float('inf')

        # Search with depth-first, probability-guided
        for depth in range(1, self.max_depth + 1):
            for _ in range(self.max_attempts // self.max_depth):
                program = self._sample_program(prim_probs, depth)

                try:
                    result = self._execute(program, input_seq)
                    if result == output_seq:
                        dl = self.library.description_length(program)
                        if dl < best_dl:
                            best_dl = dl
                            best_program = program
                except:
                    continue

            if best_program is not None:
                break

        return best_program

    def _sample_program(self, prim_probs: List[Tuple[str, float]], max_depth: int) -> Program:
        """Sample a program tree guided by probabilities."""
        if max_depth <= 1:
            # Leaf: pick a primitive (weighted by probability)
            prims, probs = zip(*prim_probs)
            probs = [p + 0.01 for p in probs]  # Smoothing
            total = sum(probs)
            probs = [p/total for p in probs]
            name = random.choices(prims, weights=probs, k=1)[0]
            return Program(name)

        # Internal node: pick primitive and recurse
        prims, probs = zip(*prim_probs)
        probs = [p + 0.01 for p in probs]
        total = sum(probs)
        probs = [p/total for p in probs]
        name = random.choices(prims, weights=probs, k=1)[0]

        # Decide number of children based on primitive arity
        # For simplicity, 0-2 children randomly
        if random.random() < 0.3:
            return Program(name)
        elif random.random() < 0.6:
            child = self._sample_program(prim_probs, max_depth - 1)
            return Program(name, [child])
        else:
            child1 = self._sample_program(prim_probs, max_depth - 1)
            child2 = self._sample_program(prim_probs, max_depth - 1)
            return Program(name, [child1, child2])

    def _execute(self, program: Program, input_seq: List[int]) -> List[int]:
        """Execute a program on input."""
        if not program.children:
            # Leaf: apply primitive to input
            return self.library.execute(program.name, input_seq)
        elif len(program.children) == 1:
            # Unary: execute child, then apply this
            child_result = self._execute(program.children[0], input_seq)
            return self.library.execute(program.name, child_result)
        else:
            # Binary: execute both children, combine
            result1 = self._execute(program.children[0], input_seq)
            result2 = self._execute(program.children[1], input_seq)
            return self.library.execute(program.name, result1, result2)


# =============================================================================
# PART 4: ABSTRACTION LEARNING (The key innovation)
# =============================================================================

class AbstractionLearner:
    """
    Learn reusable abstractions from solved problems.

    This is what makes DreamCoder powerful:
    - Solve problem → extract reusable sub-programs
    - Add good abstractions to library
    - Future problems benefit from learned abstractions

    MDL guides what to keep: abstractions that compress the solution corpus.
    """

    def __init__(self, library: PrimitiveLibrary):
        self.library = library
        self.solved_programs: List[Program] = []

    def record_solution(self, program: Program):
        """Record a successful solution for later abstraction."""
        self.solved_programs.append(program)

    def extract_abstractions(self, min_occurrences: int = 2):
        """
        Extract common sub-programs and add them to library.

        A sub-program becomes an abstraction if:
        1. It appears in multiple solutions (reusable)
        2. It compresses the total description length (MDL)
        """
        # Count sub-program occurrences
        subprogram_counts: Dict[str, int] = {}
        subprogram_examples: Dict[str, Program] = {}

        def count_subprograms(p: Program):
            key = repr(p)
            if p.size() > 1:  # Only non-trivial sub-programs
                subprogram_counts[key] = subprogram_counts.get(key, 0) + 1
                subprogram_examples[key] = p
            for c in p.children:
                count_subprograms(c)

        for prog in self.solved_programs:
            count_subprograms(prog)

        # Add frequent sub-programs as abstractions
        for key, count in subprogram_counts.items():
            if count >= min_occurrences:
                prog = subprogram_examples[key]

                # Create a function for this abstraction
                # (In full DreamCoder this would be properly compiled)
                name = f"abs_{len(self.library.learned)}"

                # For now, we'll try to identify what this abstraction does
                # and create a callable
                self._add_if_useful(name, prog)

    def _add_if_useful(self, name: str, program: Program):
        """Add abstraction if it would reduce total description length."""
        # Calculate current total DL
        current_dl = sum(self.library.description_length(p) for p in self.solved_programs)

        # Simulate adding abstraction
        abstraction_dl = program.size()  # Cost to define abstraction

        # Calculate new DL if we replace occurrences with abstraction reference
        def count_and_replace_size(p: Program, target: str) -> Tuple[int, int]:
            """Returns (occurrences, new_size_if_replaced)."""
            target_repr = target
            if repr(p) == target_repr:
                return (1, 1)  # Replace with single reference

            occurrences = 0
            new_size = 1  # This node
            for c in p.children:
                child_occ, child_size = count_and_replace_size(c, target)
                occurrences += child_occ
                new_size += child_size
            return (occurrences, new_size)

        total_occurrences = 0
        new_total_dl = abstraction_dl  # Cost of defining abstraction

        target_repr = repr(program)
        for p in self.solved_programs:
            occ, new_size = count_and_replace_size(p, target_repr)
            total_occurrences += occ
            new_total_dl += new_size

        # Add if it compresses
        if new_total_dl < current_dl and total_occurrences >= 2:
            # Create executable function (simplified - real DreamCoder would compile properly)
            # For now, we mark it and handle in execute
            def make_func(prog):
                def func(x):
                    return x  # Placeholder - would need proper compilation
                return func

            self.library.add_abstraction(name, program, make_func(program))
            print(f"  [MDL] Added {name}: saves {current_dl - new_total_dl:.2f} bits")


# =============================================================================
# PART 5: THE FULL SYSTEM
# =============================================================================

class DreamCoderSequences:
    """
    Full DreamCoder-style system for sequence transformation.

    This is the integration of:
    - MDL objective (compression-based learning)
    - Neural-guided search (recognition model)
    - Abstraction learning (library grows)
    - Transfer learning (abstractions help future problems)
    """

    def __init__(self):
        self.library = PrimitiveLibrary()
        self.recognition = RecognitionModel()
        self.searcher = ProgramSearcher(self.library, self.recognition)
        self.abstraction_learner = AbstractionLearner(self.library)
        self.optimizer = torch.optim.Adam(self.recognition.parameters(), lr=0.001)

        # Statistics
        self.problems_solved = 0
        self.search_steps_history = []

    def solve(self, input_seq: List[int], output_seq: List[int],
              max_steps: int = 500) -> Tuple[Optional[Program], int]:
        """
        Solve a sequence transformation problem.

        Returns (program, steps) where steps is search effort.
        """
        start_time = time.time()

        # Search for program
        program = self.searcher.search(input_seq, output_seq)

        steps = int((time.time() - start_time) * 100)  # Proxy for effort

        if program is not None:
            self.problems_solved += 1
            self.search_steps_history.append(steps)

            # Record for abstraction learning
            self.abstraction_learner.record_solution(program)

            # Train recognition model on successful example
            self._train_recognition(input_seq, output_seq, program)

            # Periodically extract abstractions
            if self.problems_solved % 5 == 0:
                self.abstraction_learner.extract_abstractions()

        return program, steps

    def _train_recognition(self, input_seq: List[int], output_seq: List[int],
                           program: Program):
        """Train recognition model to predict primitives used in successful solution."""
        # Get primitives used in program
        used_primitives = set()
        def collect(p: Program):
            used_primitives.add(p.name)
            for c in p.children:
                collect(c)
        collect(program)

        # Create target (1 for used primitives, 0 for others)
        all_prims = self.library.get_all_primitives()
        self.recognition.resize_for_library(len(all_prims))

        target = torch.zeros(len(all_prims))
        for i, p in enumerate(all_prims):
            if p in used_primitives:
                target[i] = 1.0
        target = target / (target.sum() + 1e-6)  # Normalize

        # Train
        self.optimizer.zero_grad()
        pred = self.recognition(input_seq, output_seq)
        loss = F.cross_entropy(pred.unsqueeze(0), target.unsqueeze(0))
        loss.backward()
        self.optimizer.step()


# =============================================================================
# PART 6: TESTING ON POSITIONAL TRANSFORMS
# =============================================================================

def generate_task(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """Generate a (input, output) pair for a transform."""
    input_seq = [random.randint(1, 9) for _ in range(length)]

    if transform_name == 'identity':
        output_seq = input_seq.copy()
    elif transform_name == 'increment':
        output_seq = [x + 1 for x in input_seq]
    elif transform_name == 'reverse':
        output_seq = input_seq[::-1]
    elif transform_name == 'swap_pairs':
        output_seq = []
        for i in range(0, len(input_seq) - 1, 2):
            output_seq.extend([input_seq[i+1], input_seq[i]])
        if len(input_seq) % 2 == 1:
            output_seq.append(input_seq[-1])
    elif transform_name == 'running_max':
        output_seq = []
        current_max = 0
        for x in input_seq:
            current_max = max(current_max, x)
            output_seq.append(current_max)
    elif transform_name == 'mirror_add':
        output_seq = [input_seq[i] + input_seq[-(i+1)] for i in range(len(input_seq))]
    elif transform_name == 'sort':
        output_seq = sorted(input_seq)
    elif transform_name == 'rotate_left':
        output_seq = input_seq[1:] + [input_seq[0]]
    else:
        raise ValueError(f"Unknown transform: {transform_name}")

    return input_seq, output_seq


def test_transform(system: DreamCoderSequences, transform_name: str,
                   num_tasks: int = 5) -> Tuple[int, List[int]]:
    """Test system on a transform, return (correct_count, steps_per_task)."""
    correct = 0
    steps_list = []

    print(f"\n  Testing {transform_name}:")

    for i in range(num_tasks):
        input_seq, output_seq = generate_task(transform_name)
        program, steps = system.solve(input_seq, output_seq)

        if program is not None:
            # Verify
            try:
                result = system.searcher._execute(program, input_seq)
                if result == output_seq:
                    correct += 1
                    print(f"    Task {i+1}: SOLVED in {steps} steps - {program}")
                else:
                    print(f"    Task {i+1}: WRONG OUTPUT")
            except:
                print(f"    Task {i+1}: EXECUTION ERROR")
        else:
            print(f"    Task {i+1}: NO SOLUTION FOUND")

        steps_list.append(steps)

    return correct, steps_list


def main():
    """Run Experiment 12: DreamCoder-style abstraction learning."""
    print("=" * 70)
    print("EXPERIMENT 12: DreamCoder-Style Abstraction Learning")
    print("=" * 70)
    print("\nThis is NOT enumeration. This is LEARNING.")
    print("The library should GROW as we solve problems.")
    print("\nSuccess criteria:")
    print("  - >80% on positional transforms")
    print("  - Learning curve shows transfer")
    print("  - Library grows with useful abstractions")
    print("=" * 70)

    system = DreamCoderSequences()

    # Test transforms in order
    transforms = [
        'identity',      # Should be trivial
        'increment',     # Element-wise, should work
        'reverse',       # POSITIONAL - the real test
        'running_max',   # POSITIONAL - harder
        'swap_pairs',    # POSITIONAL - harder
        'mirror_add',    # POSITIONAL - hardest
    ]

    results = {}

    for transform in transforms:
        correct, steps = test_transform(system, transform)
        results[transform] = {
            'accuracy': correct / 5,
            'steps': steps,
            'library_size': len(system.library.get_all_primitives())
        }
        print(f"\n  Result: {correct}/5 ({correct/5*100:.0f}%)")
        print(f"  Library size: {results[transform]['library_size']}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    element_wise = ['identity', 'increment']
    positional = ['reverse', 'running_max', 'swap_pairs', 'mirror_add']

    ew_acc = sum(results[t]['accuracy'] for t in element_wise) / len(element_wise)
    pos_acc = sum(results[t]['accuracy'] for t in positional) / len(positional)

    print(f"\nElement-wise accuracy: {ew_acc*100:.0f}%")
    print(f"Positional accuracy: {pos_acc*100:.0f}%")
    print(f"Overall accuracy: {(ew_acc + pos_acc) / 2 * 100:.0f}%")
    print(f"\nFinal library size: {len(system.library.get_all_primitives())}")
    print(f"Learned abstractions: {len(system.library.learned)}")

    # Learning curve
    print("\nLearning curve (steps per problem):")
    if system.search_steps_history:
        for i, steps in enumerate(system.search_steps_history):
            print(f"  Problem {i+1}: {steps} steps")

    # Verdict
    print("\n" + "=" * 70)
    if pos_acc >= 0.8:
        print("SUCCESS: >80% on positional transforms!")
        print("This approach WORKS for sequences.")
    else:
        print(f"NOT YET: {pos_acc*100:.0f}% on positional (need >80%)")
        print("Need to improve search or primitives.")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = main()
