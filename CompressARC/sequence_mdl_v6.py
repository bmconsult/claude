#!/usr/bin/env python3
"""
SEQUENCE MDL V6 - Composable Program Synthesis

Key insight: Real power comes from COMPOSING primitives.
- reverse + rotate = new transform
- sort + increment = new transform
- Composition is exponential in expressiveness

This version:
1. Has primitive operations
2. Composes them (up to depth 2 for now)
3. Enumerates compositions to find the right one
4. Caches learned compositions for transfer

This is exactly how ARC Compressor works at scale.
"""

import numpy as np
from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass
from itertools import product
import time

np.random.seed(42)


@dataclass
class SequenceTask:
    task_name: str
    train_pairs: List[Tuple[List[int], List[int]]]
    test_pairs: List[Tuple[List[int], List[int]]]


# =============================================================================
# PRIMITIVE OPERATIONS
# =============================================================================

PRIMITIVES: Dict[str, Callable] = {
    'id': lambda x: x.copy(),
    'rev': lambda x: x[::-1],
    'rot1': lambda x: x[1:] + x[:1],
    'rot2': lambda x: x[2:] + x[:2],
    'rot-1': lambda x: x[-1:] + x[:-1],
    'rot-2': lambda x: x[-2:] + x[:-2],
    'sort': lambda x: sorted(x),
    'rsort': lambda x: sorted(x, reverse=True),
    'inc': lambda x: [(v + 1) % 10 for v in x],
    'dec': lambda x: [(v - 1) % 10 for v in x],
    'dbl': lambda x: [(v * 2) % 10 for v in x],
    'first': lambda x: [x[0]] * len(x),
    'last': lambda x: [x[-1]] * len(x),
    'min': lambda x: [min(x)] * len(x),
    'max': lambda x: [max(x)] * len(x),
}


def compose(f: Callable, g: Callable) -> Callable:
    """Compose two functions: (f ∘ g)(x) = f(g(x))"""
    return lambda x: f(g(x))


def build_program_library(max_depth: int = 2) -> Dict[str, Callable]:
    """Build library of all programs up to given composition depth."""
    programs = {}

    # Depth 1: primitives
    for name, fn in PRIMITIVES.items():
        programs[name] = fn

    # Depth 2: compositions of two primitives
    if max_depth >= 2:
        for n1, f1 in PRIMITIVES.items():
            for n2, f2 in PRIMITIVES.items():
                name = f"{n1}({n2})"
                programs[name] = compose(f1, f2)

    # Depth 3: compositions of three (optional, exponential)
    if max_depth >= 3:
        for n1, f1 in PRIMITIVES.items():
            for n2, f2 in PRIMITIVES.items():
                for n3, f3 in PRIMITIVES.items():
                    name = f"{n1}({n2}({n3}))"
                    programs[name] = compose(f1, compose(f2, f3))

    return programs


class ComposableSynthesizer:
    """
    Program synthesizer with composition.

    Enumerates composed programs and finds one that fits.
    Uses MDL-like preference: shorter programs preferred.
    """

    def __init__(self, max_depth: int = 2):
        self.max_depth = max_depth
        self.programs = build_program_library(max_depth)
        self.learned_program: Optional[str] = None

        # Sort by complexity (shorter names = simpler programs)
        self.program_order = sorted(self.programs.keys(), key=lambda x: (x.count('('), len(x)))

    def fit(self, train_pairs: List[Tuple[List[int], List[int]]]) -> Optional[str]:
        """Find the simplest program that fits all training pairs."""

        for prog_name in self.program_order:
            prog_fn = self.programs[prog_name]

            try:
                # Test if this program works for all examples
                matches_all = True
                for input_seq, target_seq in train_pairs:
                    predicted = prog_fn(input_seq)
                    if predicted != target_seq:
                        matches_all = False
                        break

                if matches_all:
                    self.learned_program = prog_name
                    return prog_name

            except Exception:
                # Some compositions may fail (e.g., empty list)
                continue

        # No program works
        self.learned_program = None
        return None

    def predict(self, input_seq: List[int]) -> Optional[List[int]]:
        """Apply learned program to input."""
        if self.learned_program is None:
            return None

        try:
            return self.programs[self.learned_program](input_seq)
        except Exception:
            return None


class CompositionLibrary:
    """Library to cache and prioritize learned programs."""

    def __init__(self):
        self.programs: Dict[str, int] = {}  # program -> success count

    def add(self, program: str):
        self.programs[program] = self.programs.get(program, 0) + 1

    def get_priority_order(self) -> List[str]:
        """Get programs ordered by success frequency."""
        return sorted(self.programs.keys(), key=lambda x: -self.programs[x])


def solve_task(task: SequenceTask, library: CompositionLibrary = None,
               max_depth: int = 2, verbose: bool = True) -> Dict:
    """Solve a sequence task via composed program synthesis."""

    synth = ComposableSynthesizer(max_depth)

    # Prioritize known programs if library available
    if library and library.programs:
        priority = library.get_priority_order()
        synth.program_order = priority + [p for p in synth.program_order if p not in priority]

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
        complexity = program.count('(') + 1 if program else 0
        print(f"  Program: {program} (complexity: {complexity})")
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


def make_transform_tasks(name: str, transform: Callable, n: int = 5, length: int = 5, n_examples: int = 5, seed_offset: int = 0) -> List[SequenceTask]:
    """Generic task generator for any transform."""
    tasks = []
    for i in range(n):
        np.random.seed(i + seed_offset)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            try:
                pairs.append((seq, transform(seq)))
            except:
                continue
        if pairs:
            tasks.append(make_task(f"{name}_{i}", pairs))
    return tasks


if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENCE MDL V6 - COMPOSABLE PROGRAM SYNTHESIS")
    print("=" * 60)
    print(f"Primitives: {list(PRIMITIVES.keys())}")
    programs = build_program_library(max_depth=2)
    print(f"Total programs (depth ≤ 2): {len(programs)}")
    print()

    # Define test transforms - including COMPOSED ones!
    test_cases = [
        # Simple (depth 1)
        ("IDENTITY", lambda x: x.copy(), "id"),
        ("REVERSE", lambda x: x[::-1], "rev"),
        ("SORT", lambda x: sorted(x), "sort"),
        ("INCREMENT", lambda x: [(v+1)%10 for v in x], "inc"),

        # Composed (depth 2)
        ("REVERSE+SORT", lambda x: sorted(x)[::-1], "rev(sort)"),
        ("SORT+REVERSE", lambda x: sorted(x[::-1]), "sort(rev)"),
        ("INCREMENT+REVERSE", lambda x: [(v+1)%10 for v in x[::-1]], "inc(rev)"),
        ("REVERSE+INCREMENT", lambda x: [(v+1)%10 for v in x][::-1], "rev(inc)"),
        ("DOUBLE+SORT", lambda x: sorted([(v*2)%10 for v in x]), "sort(dbl)"),
        ("SORT+DOUBLE", lambda x: [(v*2)%10 for v in sorted(x)], "dbl(sort)"),
    ]

    all_results = {}

    for task_name, transform, expected_prog in test_cases:
        print("\n" + "=" * 60)
        print(f"[{task_name}] - Expected: {expected_prog}")
        print("=" * 60)

        tasks = make_transform_tasks(task_name.lower(), transform, n=3, seed_offset=hash(task_name) % 1000)
        library = CompositionLibrary()
        results = []

        for i, task in enumerate(tasks):
            print(f"\n[{i+1}/{len(tasks)}] {task.task_name}")
            print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

            result = solve_task(task, library if i > 0 else None, verbose=True)

            if result['correct'] and result['program']:
                library.add(result['program'])

            results.append(result)

        correct = sum(r['correct'] for r in results)
        print(f"\n{task_name} Summary: {correct}/{len(results)} correct")
        programs_found = [r['program'] for r in results]
        print(f"Programs: {programs_found}")

        all_results[task_name] = results

    # Overall summary
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    total_correct = sum(r['correct'] for results in all_results.values() for r in results)
    total_tasks = sum(len(results) for results in all_results.values())
    print(f"Total: {total_correct}/{total_tasks} correct")

    # Show program library stats
    print(f"\nProgram library size: {len(programs)}")
    print(f"  Depth 1 (primitives): {len(PRIMITIVES)}")
    print(f"  Depth 2 (compositions): {len(programs) - len(PRIMITIVES)}")

    # Transfer test with compositions
    print("\n" + "=" * 60)
    print("TRANSFER TEST - Composed transform")
    print("=" * 60)

    # reverse + increment: x[::-1] then +1 each
    transform = lambda x: [(v+1)%10 for v in x[::-1]]
    tasks = make_transform_tasks("rev_inc", transform, n=10, seed_offset=999)

    library = CompositionLibrary()
    times = []
    correct_count = 0

    for i, task in enumerate(tasks):
        result = solve_task(task, library if i > 0 else None, verbose=False)
        times.append(result['time'])
        if result['correct']:
            correct_count += 1
            if result['program']:
                library.add(result['program'])

    print(f"Transform: reverse then increment")
    print(f"Correct: {correct_count}/{len(tasks)}")
    print(f"First task: {times[0]*1000:.2f}ms")
    print(f"Later tasks (avg): {sum(times[1:])/len(times[1:])*1000:.2f}ms")
    if times[1:]:
        speedup = times[0] / (sum(times[1:])/len(times[1:]))
        print(f"Speedup: {speedup:.1f}x")
