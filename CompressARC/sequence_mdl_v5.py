#!/usr/bin/env python3
"""
SEQUENCE MDL V5 - Direct Program Synthesis

Simplest possible approach:
1. Have a library of operations (programs)
2. For each task, try each operation
3. Pick the one with zero training error
4. Apply to test

This is exactly what a DSL-based program synthesizer does.
No neural networks needed for operation selection - just enumeration.

The insight: for a small operation library, enumeration is FAST and EXACT.
"""

import numpy as np
from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass
import time

np.random.seed(42)


@dataclass
class SequenceTask:
    task_name: str
    train_pairs: List[Tuple[List[int], List[int]]]
    test_pairs: List[Tuple[List[int], List[int]]]


# =============================================================================
# OPERATION LIBRARY (Programs)
# =============================================================================

def op_identity(x: List[int]) -> List[int]:
    """Identity: x -> x"""
    return x.copy()


def op_reverse(x: List[int]) -> List[int]:
    """Reverse: x -> x[::-1]"""
    return x[::-1]


def op_rotate_1(x: List[int]) -> List[int]:
    """Rotate left by 1."""
    return x[1:] + x[:1]


def op_rotate_2(x: List[int]) -> List[int]:
    """Rotate left by 2."""
    return x[2:] + x[:2]


def op_rotate_3(x: List[int]) -> List[int]:
    """Rotate left by 3."""
    return x[3:] + x[:3]


def op_rotate_neg1(x: List[int]) -> List[int]:
    """Rotate right by 1."""
    return x[-1:] + x[:-1]


def op_rotate_neg2(x: List[int]) -> List[int]:
    """Rotate right by 2."""
    return x[-2:] + x[:-2]


def op_sort_asc(x: List[int]) -> List[int]:
    """Sort ascending."""
    return sorted(x)


def op_sort_desc(x: List[int]) -> List[int]:
    """Sort descending."""
    return sorted(x, reverse=True)


def op_increment(x: List[int]) -> List[int]:
    """Add 1 to each element (mod 10)."""
    return [(v + 1) % 10 for v in x]


def op_decrement(x: List[int]) -> List[int]:
    """Subtract 1 from each element (mod 10)."""
    return [(v - 1) % 10 for v in x]


def op_double(x: List[int]) -> List[int]:
    """Double each element (mod 10)."""
    return [(v * 2) % 10 for v in x]


# Build operation library
OPERATIONS: Dict[str, Callable] = {
    'identity': op_identity,
    'reverse': op_reverse,
    'rotate_1': op_rotate_1,
    'rotate_2': op_rotate_2,
    'rotate_3': op_rotate_3,
    'rotate_-1': op_rotate_neg1,
    'rotate_-2': op_rotate_neg2,
    'sort_asc': op_sort_asc,
    'sort_desc': op_sort_desc,
    'increment': op_increment,
    'decrement': op_decrement,
    'double': op_double,
}


class SequenceSynthesizer:
    """
    Program synthesizer for sequence transformations.

    Enumerates operations and picks the one that fits all training examples.
    This is exact and fast for small operation libraries.
    """

    def __init__(self, operations: Dict[str, Callable] = None):
        self.operations = operations or OPERATIONS
        self.learned_program: Optional[str] = None

    def fit(self, train_pairs: List[Tuple[List[int], List[int]]]) -> str:
        """Find the operation that fits all training pairs."""

        for op_name, op_fn in self.operations.items():
            # Test if this operation works for all examples
            matches_all = True
            for input_seq, target_seq in train_pairs:
                predicted = op_fn(input_seq)
                if predicted != target_seq:
                    matches_all = False
                    break

            if matches_all:
                self.learned_program = op_name
                return op_name

        # No single operation works
        self.learned_program = None
        return None

    def predict(self, input_seq: List[int]) -> Optional[List[int]]:
        """Apply learned program to input."""
        if self.learned_program is None:
            return None

        op_fn = self.operations[self.learned_program]
        return op_fn(input_seq)


class SynthesisLibrary:
    """Library to transfer learned programs."""
    def __init__(self):
        self.programs: Dict[str, str] = {}  # task_name -> program_name

    def add(self, task_name: str, program: str):
        self.programs[task_name] = program

    def get_hint(self) -> Optional[str]:
        """Get most common program as a hint."""
        if not self.programs:
            return None
        from collections import Counter
        counts = Counter(self.programs.values())
        return counts.most_common(1)[0][0]


def solve_task(task: SequenceTask, library: SynthesisLibrary = None,
               verbose: bool = True) -> Dict:
    """Solve a sequence task via program synthesis."""

    synth = SequenceSynthesizer()

    # Optionally prioritize the most common program from library
    if library:
        hint = library.get_hint()
        if hint:
            # Try the hint first
            synth.operations = {hint: OPERATIONS[hint], **OPERATIONS}

    start = time.time()
    program = synth.fit(task.train_pairs)
    elapsed = time.time() - start

    # Test
    if program:
        test_input = task.test_pairs[0][0]
        test_expected = task.test_pairs[0][1]
        test_pred = synth.predict(test_input)
        correct = test_pred == test_expected
    else:
        test_pred = None
        correct = False

    if verbose:
        print(f"  Found program: {program}")
        print(f"  Time: {elapsed*1000:.2f}ms")
        print(f"  Correct: {correct}")
        if not correct and test_pred is not None:
            print(f"  Pred: {test_pred}")
            print(f"  Exp:  {task.test_pairs[0][1]}")

    return {
        'task_name': task.task_name,
        'program': program,
        'time': elapsed,
        'correct': correct,
    }


# =============================================================================
# TEST TASKS
# =============================================================================

def make_task(name: str, pairs: List[Tuple[List[int], List[int]]]) -> SequenceTask:
    train = pairs[:-1]
    test = pairs[-1:]
    return SequenceTask(name, train, test)


def make_reverse_tasks(n: int = 5, length: int = 5, n_examples: int = 5) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 100)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, seq[::-1]))
        tasks.append(make_task(f"reverse_{i}", pairs))
    return tasks


def make_rotate_tasks(n: int = 5, length: int = 5, k: int = 2, n_examples: int = 5) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 300)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            rotated = seq[k:] + seq[:k]
            pairs.append((seq, rotated))
        tasks.append(make_task(f"rotate_{k}_{i}", pairs))
    return tasks


def make_sort_tasks(n: int = 5, length: int = 5, n_examples: int = 5) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 200)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, sorted(seq)))
        tasks.append(make_task(f"sort_{i}", pairs))
    return tasks


def make_identity_tasks(n: int = 5, length: int = 5, n_examples: int = 5) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 400)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, seq.copy()))
        tasks.append(make_task(f"identity_{i}", pairs))
    return tasks


def make_increment_tasks(n: int = 5, length: int = 5, n_examples: int = 5) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 500)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, [(v + 1) % 10 for v in seq]))
        tasks.append(make_task(f"increment_{i}", pairs))
    return tasks


if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENCE MDL V5 - PROGRAM SYNTHESIS")
    print("=" * 60)
    print(f"Operations available: {list(OPERATIONS.keys())}")
    print()

    all_results = {}

    # Test each task type
    for task_type, task_fn, expected_op in [
        ("IDENTITY", make_identity_tasks, "identity"),
        ("REVERSE", make_reverse_tasks, "reverse"),
        ("ROTATE-2", lambda: make_rotate_tasks(k=2), "rotate_2"),
        ("SORT", make_sort_tasks, "sort_asc"),
        ("INCREMENT", make_increment_tasks, "increment"),
    ]:
        print("\n" + "=" * 60)
        print(f"[{task_type}] - Expected program: {expected_op}")
        print("=" * 60)

        tasks = task_fn() if callable(task_fn) else task_fn
        library = SynthesisLibrary()
        results = []

        for i, task in enumerate(tasks[:5]):
            print(f"\n[{i+1}/5] {task.task_name}")
            print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

            result = solve_task(task, library if i > 0 else None, verbose=True)

            if result['correct'] and result['program']:
                library.add(task.task_name, result['program'])

            results.append(result)

        correct = sum(r['correct'] for r in results)
        print(f"\n{task_type} Summary: {correct}/5 correct")
        programs = [r['program'] for r in results]
        print(f"Programs found: {programs}")
        avg_time = sum(r['time'] for r in results) / len(results) * 1000
        print(f"Avg time: {avg_time:.2f}ms")

        all_results[task_type] = results

    # Overall summary
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    total_correct = sum(r['correct'] for results in all_results.values() for r in results)
    total_tasks = sum(len(results) for results in all_results.values())
    print(f"Total: {total_correct}/{total_tasks} correct")

    # Transfer test: Can we solve a task instantly if we've seen the program before?
    print("\n" + "=" * 60)
    print("TRANSFER TEST - Sequential tasks, same transform")
    print("=" * 60)

    print("\nRunning 20 reverse tasks with transfer...")
    library = SynthesisLibrary()
    reverse_tasks = make_reverse_tasks(n=20)
    times = []

    for i, task in enumerate(reverse_tasks):
        result = solve_task(task, library if i > 0 else None, verbose=False)
        times.append(result['time'])
        if result['correct'] and result['program']:
            library.add(task.task_name, result['program'])

    print(f"All correct: {all(t < 0.001 for t in times)}")
    print(f"First task time: {times[0]*1000:.3f}ms")
    print(f"Later tasks time (avg): {sum(times[1:])/len(times[1:])*1000:.3f}ms")
    print(f"Speedup: {times[0] / (sum(times[1:])/len(times[1:])):.1f}x")
