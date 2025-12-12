#!/usr/bin/env python3
"""
Binary search for minimal non-4-colorable subgraph using SAT.
We know: 450 is 4-colorable (all trials), 517 is NOT 4-colorable.
"""

from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import random
import time

def parse_graph(filename):
    vertices = set()
    adj = defaultdict(set)
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) < 2:
                continue
            v = int(parts[0])
            vertices.add(v)
            edge_str = parts[1]
            if edge_str:
                neighbors = [int(x) for x in edge_str.split(';') if x]
                for u in neighbors:
                    vertices.add(u)
                    adj[v].add(u)
                    adj[u].add(v)
    return vertices, adj

def is_4_colorable_sat(adj, vertices):
    """Check if graph is 4-colorable using SAT."""
    k = 4
    vertex_list = sorted(vertices)
    n = len(vertex_list)
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    # Each vertex has at least one color
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])

    # Each vertex has at most one color
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    # Adjacent vertices have different colors
    for v in vertex_list:
        v_idx = v_to_idx[v]
        for u in adj[v]:
            if u in vertices and u > v:
                u_idx = v_to_idx[u]
                for c in range(k):
                    cnf.append([-var(v_idx, c), -var(u_idx, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def test_size(adj, vertices, size, num_trials=10):
    """Test if random subgraphs of given size are 4-colorable."""
    vertex_list = list(vertices)
    colorable_count = 0

    for _ in range(num_trials):
        sample = set(random.sample(vertex_list, size))
        sample_adj = defaultdict(set)
        for v in sample:
            sample_adj[v] = adj[v] & sample

        if is_4_colorable_sat(sample_adj, sample):
            colorable_count += 1

    return colorable_count

def find_minimal_size(adj, vertices, lo=450, hi=517, trials=20):
    """Binary search for transition point."""
    print(f"Binary search between {lo} and {hi}")

    results = {}

    while hi - lo > 5:
        mid = (lo + hi) // 2

        start = time.time()
        count = test_size(adj, vertices, mid, trials)
        elapsed = time.time() - start

        success_rate = count / trials
        results[mid] = (count, trials)
        print(f"  Size {mid}: {count}/{trials} 4-colorable ({success_rate*100:.0f}%) [{elapsed:.1f}s]")

        if count == trials:
            # All 4-colorable at this size
            lo = mid
        else:
            # Some not 4-colorable
            hi = mid

    return lo, hi, results

def detailed_search(adj, vertices, lo, hi, trials=50):
    """Detailed search around transition point."""
    print(f"\nDetailed search from {lo} to {hi}")

    results = {}
    for size in range(lo, hi + 1, 2):
        start = time.time()
        count = test_size(adj, vertices, size, trials)
        elapsed = time.time() - start

        success_rate = count / trials
        results[size] = (count, trials)
        print(f"  Size {size}: {count}/{trials} 4-colorable ({success_rate*100:.0f}%) [{elapsed:.1f}s]")

    return results

def find_specific_non_4colorable(adj, vertices, target_size, max_attempts=1000):
    """Find a specific non-4-colorable subgraph of given size."""
    print(f"\nSearching for non-4-colorable subgraph of size {target_size}...")

    vertex_list = list(vertices)

    for attempt in range(max_attempts):
        sample = set(random.sample(vertex_list, target_size))
        sample_adj = defaultdict(set)
        for v in sample:
            sample_adj[v] = adj[v] & sample

        if not is_4_colorable_sat(sample_adj, sample):
            print(f"  Found after {attempt+1} attempts!")
            return sample

        if attempt % 100 == 99:
            print(f"    Tried {attempt+1} samples...")

    print(f"  No non-4-colorable subgraph found in {max_attempts} attempts")
    return None

def main():
    print("=" * 70)
    print("FINDING MINIMAL NON-4-COLORABLE SUBGRAPH")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"Full graph: {len(vertices)} vertices")

    # Binary search
    lo, hi, coarse_results = find_minimal_size(adj, vertices)

    # Detailed search
    detailed_results = detailed_search(adj, vertices, max(lo-10, 450), min(hi+10, 517))

    # Find transition point
    print("\n" + "=" * 70)
    print("TRANSITION ANALYSIS")
    print("=" * 70)

    all_results = {**coarse_results, **detailed_results}
    sorted_sizes = sorted(all_results.keys())

    for size in sorted_sizes:
        count, trials = all_results[size]
        bar = "=" * int(count / trials * 20)
        print(f"  {size}: {'■' * count}{'□' * (trials - count)} {count}/{trials}")

    # Find first size with any failures
    for size in sorted_sizes:
        count, trials = all_results[size]
        if count < trials:
            print(f"\nFirst size with non-4-colorable: {size}")
            print(f"  {trials - count}/{trials} were NOT 4-colorable")
            break

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)

if __name__ == "__main__":
    main()
