"""
Complete Truth Table Census for MCSP Research

For n=4 (65536 truth tables), compute:
1. Exact minimum circuit size
2. Structural fingerprints
3. Classification by properties

This is Phase 1 of the P vs NP attack via MCSP/Magnification.
"""

from itertools import combinations, product
from functools import lru_cache
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
import numpy as np
from collections import defaultdict
import json
import time

@dataclass
class CircuitGate:
    """A gate in a Boolean circuit."""
    gate_type: str  # 'AND', 'OR', 'NOT', 'INPUT', 'CONST'
    inputs: Tuple[int, ...]  # Indices of input gates

@dataclass
class Circuit:
    """A Boolean circuit."""
    n_inputs: int
    gates: List[CircuitGate]
    output_gate: int

    def evaluate(self, x: Tuple[bool, ...]) -> bool:
        """Evaluate circuit on input x."""
        values = list(x)  # Gate values: inputs first

        for gate in self.gates[self.n_inputs:]:
            if gate.gate_type == 'AND':
                val = values[gate.inputs[0]] and values[gate.inputs[1]]
            elif gate.gate_type == 'OR':
                val = values[gate.inputs[0]] or values[gate.inputs[1]]
            elif gate.gate_type == 'NOT':
                val = not values[gate.inputs[0]]
            elif gate.gate_type == 'CONST':
                val = gate.inputs[0]  # 0 or 1
            else:
                raise ValueError(f"Unknown gate type: {gate.gate_type}")
            values.append(val)

        return values[self.output_gate]

    def size(self) -> int:
        """Number of non-input gates."""
        return len(self.gates) - self.n_inputs


def truth_table_to_int(tt: Tuple[bool, ...]) -> int:
    """Convert truth table to integer representation."""
    result = 0
    for i, v in enumerate(tt):
        if v:
            result |= (1 << i)
    return result


def int_to_truth_table(n: int, num_inputs: int) -> Tuple[bool, ...]:
    """Convert integer to truth table."""
    size = 2 ** num_inputs
    return tuple((n >> i) & 1 == 1 for i in range(size))


def get_all_inputs(n: int) -> List[Tuple[bool, ...]]:
    """Get all possible inputs for n-variable function."""
    return [tuple((i >> j) & 1 == 1 for j in range(n)) for i in range(2**n)]


def circuit_truth_table(circuit: Circuit) -> Tuple[bool, ...]:
    """Compute truth table of a circuit."""
    inputs = get_all_inputs(circuit.n_inputs)
    return tuple(circuit.evaluate(x) for x in inputs)


def enumerate_circuits_up_to_size(n_inputs: int, max_size: int):
    """
    Enumerate all circuits with n_inputs and at most max_size gates.
    This is the brute-force MCSP solver for small instances.
    """
    # Start with input gates
    input_gates = [CircuitGate('INPUT', (i,)) for i in range(n_inputs)]

    # For each size from 0 to max_size
    for size in range(max_size + 1):
        yield from enumerate_circuits_of_size(n_inputs, input_gates, size)


def enumerate_circuits_of_size(n_inputs: int, input_gates: List[CircuitGate], size: int):
    """Enumerate all circuits of exactly given size."""
    if size == 0:
        # Output is just an input or constant
        for i in range(n_inputs):
            yield Circuit(n_inputs, input_gates.copy(), i)
        return

    # Generate all possible circuits with 'size' additional gates
    # This is expensive but complete
    for gates_combo in generate_gate_combinations(n_inputs, size):
        circuit = Circuit(n_inputs, input_gates + list(gates_combo), n_inputs + size - 1)
        yield circuit


def generate_gate_combinations(n_inputs: int, n_gates: int):
    """Generate all valid combinations of n_gates gates."""
    if n_gates == 0:
        yield ()
        return

    # This is the hard part - enumerate all valid DAGs
    # For small n_gates, we can brute force
    gate_types = ['AND', 'OR', 'NOT']

    def generate_recursive(gates_so_far: List[CircuitGate], remaining: int):
        if remaining == 0:
            yield tuple(gates_so_far)
            return

        current_idx = n_inputs + len(gates_so_far)
        available_inputs = list(range(current_idx))

        for gtype in gate_types:
            if gtype == 'NOT':
                for inp in available_inputs:
                    new_gate = CircuitGate('NOT', (inp,))
                    yield from generate_recursive(gates_so_far + [new_gate], remaining - 1)
            else:  # AND or OR
                for inp1, inp2 in combinations(available_inputs, 2):
                    new_gate = CircuitGate(gtype, (inp1, inp2))
                    yield from generate_recursive(gates_so_far + [new_gate], remaining - 1)
                # Also allow same input twice (for AND/OR it's just the input, but valid)
                for inp in available_inputs:
                    new_gate = CircuitGate(gtype, (inp, inp))
                    yield from generate_recursive(gates_so_far + [new_gate], remaining - 1)

    yield from generate_recursive([], n_gates)


# Optimized version using dynamic programming / memoization
_circuit_cache: Dict[Tuple[int, int], Set[int]] = {}

def compute_all_functions_up_to_size(n_inputs: int, max_size: int) -> Dict[int, int]:
    """
    Compute minimum circuit size for all truth tables.
    Returns dict: truth_table_int -> minimum_size
    """
    # Functions achievable with size s
    achievable: Dict[int, int] = {}  # tt -> min size

    # Size 0: just inputs and constants
    all_inputs = get_all_inputs(n_inputs)

    for i in range(n_inputs):
        # Input i as output
        tt = tuple(x[i] for x in all_inputs)
        tt_int = truth_table_to_int(tt)
        if tt_int not in achievable:
            achievable[tt_int] = 0

        # Negation of input i
        tt_neg = tuple(not x[i] for x in all_inputs)
        tt_neg_int = truth_table_to_int(tt_neg)
        if tt_neg_int not in achievable:
            achievable[tt_neg_int] = 1  # One NOT gate

    # Constants
    all_false = (False,) * (2**n_inputs)
    all_true = (True,) * (2**n_inputs)
    achievable[truth_table_to_int(all_false)] = 0
    achievable[truth_table_to_int(all_true)] = 0

    # Build up by size
    prev_layer = set(achievable.keys())

    for size in range(1, max_size + 1):
        print(f"  Computing size {size}... ({len(achievable)} functions found so far)")
        new_functions = set()

        # Combine functions from previous layers
        all_found = list(achievable.keys())

        # NOT gate on any previous function
        for tt_int in prev_layer:
            tt = int_to_truth_table(tt_int, n_inputs)
            tt_neg = tuple(not v for v in tt)
            tt_neg_int = truth_table_to_int(tt_neg)
            if tt_neg_int not in achievable:
                achievable[tt_neg_int] = size
                new_functions.add(tt_neg_int)

        # AND/OR of functions with sizes summing to size-1
        for s1 in range(size):
            s2 = size - 1 - s1
            funcs1 = [tt for tt, s in achievable.items() if s == s1]
            funcs2 = [tt for tt, s in achievable.items() if s == s2]

            for tt1_int in funcs1:
                tt1 = int_to_truth_table(tt1_int, n_inputs)
                for tt2_int in funcs2:
                    if s1 == s2 and tt2_int <= tt1_int:
                        continue  # Avoid duplicates
                    tt2 = int_to_truth_table(tt2_int, n_inputs)

                    # AND
                    tt_and = tuple(a and b for a, b in zip(tt1, tt2))
                    tt_and_int = truth_table_to_int(tt_and)
                    if tt_and_int not in achievable:
                        achievable[tt_and_int] = size
                        new_functions.add(tt_and_int)

                    # OR
                    tt_or = tuple(a or b for a, b in zip(tt1, tt2))
                    tt_or_int = truth_table_to_int(tt_or)
                    if tt_or_int not in achievable:
                        achievable[tt_or_int] = size
                        new_functions.add(tt_or_int)

        prev_layer = new_functions

        if len(achievable) == 2**(2**n_inputs):
            print(f"  All functions found at size {size}")
            break

    return achievable


def compute_fingerprints(tt: Tuple[bool, ...], n: int) -> Dict:
    """Compute structural fingerprints of a truth table."""
    tt_list = list(tt)
    N = len(tt)

    # 1. Hamming weight (number of 1s)
    weight = sum(tt_list)

    # 2. Balance
    balance = abs(weight - N/2) / (N/2)

    # 3. Is it symmetric (invariant under input permutation)?
    # For n=4, check all 24 permutations... simplified: check some
    is_symmetric = check_symmetric(tt, n)

    # 4. Is it monotone?
    is_monotone = check_monotone(tt, n)

    # 5. Sensitivity (max influence)
    influences = []
    for i in range(n):
        flip_mask = 1 << i
        changes = sum(1 for j in range(N) if tt_list[j] != tt_list[j ^ flip_mask])
        influences.append(changes / N)
    max_influence = max(influences)
    avg_influence = sum(influences) / n

    # 6. Fourier sparsity estimate (simplified)
    # Full Fourier would need all 2^n coefficients

    # 7. Linear structure
    has_linear_structure = any(
        all(tt_list[j] == tt_list[j ^ a] for j in range(N))
        for a in range(1, N)
    )

    # 8. Degree over F_2 (simplified - check if function is affine)
    is_affine = check_affine(tt, n)

    return {
        'weight': weight,
        'balance': balance,
        'is_symmetric': is_symmetric,
        'is_monotone': is_monotone,
        'max_influence': max_influence,
        'avg_influence': avg_influence,
        'has_linear_structure': has_linear_structure,
        'is_affine': is_affine,
    }


def check_symmetric(tt: Tuple[bool, ...], n: int) -> bool:
    """Check if function is symmetric (depends only on Hamming weight of input)."""
    inputs = get_all_inputs(n)
    by_weight = defaultdict(set)
    for i, x in enumerate(inputs):
        weight = sum(x)
        by_weight[weight].add(tt[i])

    return all(len(vals) == 1 for vals in by_weight.values())


def check_monotone(tt: Tuple[bool, ...], n: int) -> bool:
    """Check if function is monotone (x <= y implies f(x) <= f(y))."""
    N = len(tt)
    for i in range(N):
        for j in range(N):
            if (i & j) == i:  # i is subset of j (as bit vectors)
                if tt[i] and not tt[j]:
                    return False
    return True


def check_affine(tt: Tuple[bool, ...], n: int) -> bool:
    """Check if function is affine (linear + constant) over F_2."""
    N = len(tt)
    # Affine means f(x) = a·x + b for some vector a and bit b
    # Equivalently: f(x⊕y⊕z) = f(x)⊕f(y)⊕f(z) for all x,y,z

    # Quick check: sample a few triples
    import random
    for _ in range(min(100, N**2)):
        i, j, k = random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1)
        if tt[i ^ j ^ k] != (tt[i] ^ tt[j] ^ tt[k]):
            return False
    return True  # Likely affine


def run_census(n: int = 4, max_size: int = 10):
    """Run complete census for n-variable functions."""
    print(f"Running truth table census for n={n}")
    print(f"Total functions: {2**(2**n)}")
    print()

    # Compute minimum circuit sizes
    print("Computing minimum circuit sizes...")
    start = time.time()
    sizes = compute_all_functions_up_to_size(n, max_size)
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
    print(f"Functions with known size: {len(sizes)}")
    print()

    # Distribution of sizes
    size_dist = defaultdict(int)
    for s in sizes.values():
        size_dist[s] += 1

    print("Size distribution:")
    for s in sorted(size_dist.keys()):
        print(f"  Size {s}: {size_dist[s]} functions")
    print()

    # Compute fingerprints for all functions
    print("Computing fingerprints...")
    census_data = []

    for tt_int in range(2**(2**n)):
        tt = int_to_truth_table(tt_int, n)
        size = sizes.get(tt_int, -1)  # -1 if not computed
        fps = compute_fingerprints(tt, n)
        fps['tt_int'] = tt_int
        fps['circuit_size'] = size
        census_data.append(fps)

    # Analyze correlations
    print("\nAnalyzing correlations with circuit size...")

    # By property
    for prop in ['is_symmetric', 'is_monotone', 'is_affine']:
        with_prop = [d for d in census_data if d.get(prop)]
        without_prop = [d for d in census_data if not d.get(prop)]

        avg_with = np.mean([d['circuit_size'] for d in with_prop if d['circuit_size'] >= 0]) if with_prop else 0
        avg_without = np.mean([d['circuit_size'] for d in without_prop if d['circuit_size'] >= 0]) if without_prop else 0

        print(f"  {prop}:")
        print(f"    With property: {len(with_prop)} funcs, avg size {avg_with:.2f}")
        print(f"    Without: {len(without_prop)} funcs, avg size {avg_without:.2f}")

    # Find hardest functions
    print("\nHardest functions:")
    sorted_by_size = sorted(census_data, key=lambda d: -d['circuit_size'])
    for d in sorted_by_size[:10]:
        print(f"  tt={d['tt_int']:6d}, size={d['circuit_size']}, "
              f"weight={d['weight']}, symm={d['is_symmetric']}, mono={d['is_monotone']}")

    # Save results
    with open(f'census_n{n}.json', 'w') as f:
        json.dump(census_data, f, indent=2)

    print(f"\nCensus saved to census_n{n}.json")

    return census_data


if __name__ == "__main__":
    # Start with n=3 (only 256 functions) as a quick test
    print("=" * 60)
    print("Testing with n=3")
    print("=" * 60)
    run_census(n=3, max_size=5)

    print("\n" + "=" * 60)
    print("Full census for n=4")
    print("=" * 60)
    run_census(n=4, max_size=8)
