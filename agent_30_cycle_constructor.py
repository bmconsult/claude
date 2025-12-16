#!/usr/bin/env python3
"""
Agent 30: Cycle Constructor
Most dangerous attack: Try to construct a cycle in ≡1 (mod 4) restricted dynamics.
If successful, Collatz is FALSE.
"""

from typing import List, Set, Optional, Tuple, Dict
from collections import defaultdict
import sys

def collatz_step(n: int) -> int:
    """Single Collatz step."""
    return n // 2 if n % 2 == 0 else 3 * n + 1

def next_mod4_class1(m: int, max_steps: int = 10000) -> Optional[int]:
    """
    Given m ≡ 1 (mod 4), find the next value ≡ 1 (mod 4) in its trajectory.
    Returns None if reaches 1 or cycles back to m.
    """
    if m == 1:
        return 1  # 1 maps to itself

    current = collatz_step(m)
    steps = 0

    while steps < max_steps:
        if current == 1:
            return 1
        if current == m:
            return m  # Cycle detected!
        if current % 2 == 1 and current % 4 == 1:
            return current
        current = collatz_step(current)
        steps += 1

    return None  # Did not find next ≡1 (mod 4) within max_steps

def build_mod4_restricted_graph(max_n: int) -> Dict[int, int]:
    """
    Build the directed graph of ≡1 (mod 4) restricted dynamics.
    Returns: dict mapping m → F(m) where F(m) is next ≡1 (mod 4) value.
    """
    graph = {}

    for m in range(1, max_n, 4):  # All m ≡ 1 (mod 4)
        if m % 2 == 0:
            continue
        next_val = next_mod4_class1(m)
        if next_val is not None:
            graph[m] = next_val

    return graph

def find_cycles_in_graph(graph: Dict[int, int]) -> List[List[int]]:
    """
    Find all cycles in the directed graph.
    Uses path-following with cycle detection.
    """
    cycles = []
    visited_global = set()

    for start in graph.keys():
        if start in visited_global:
            continue

        # Follow path from start, tracking what we've seen
        path = []
        seen_in_path = {}
        current = start

        while current not in visited_global:
            if current not in graph:
                # Path leaves the graph
                visited_global.update(path)
                break

            if current in seen_in_path:
                # Found a cycle!
                cycle_start_idx = seen_in_path[current]
                cycle = path[cycle_start_idx:]

                if len(cycle) > 1 or (len(cycle) == 1 and cycle[0] != 1):
                    cycles.append(cycle)

                visited_global.update(path)
                break

            seen_in_path[current] = len(path)
            path.append(current)

            next_val = graph[current]
            if next_val == 1:
                # Reached 1 (trivial fixed point)
                visited_global.update(path)
                break

            current = next_val

    return cycles

def analyze_cycle_candidates(graph: Dict[int, int]) -> None:
    """
    Look for potential cycle candidates by analyzing the graph structure.
    """
    print("\n" + "="*70)
    print("ANALYSIS: Looking for Cycle Candidates")
    print("="*70)

    # Find nodes that map to larger values (potential cycle members)
    growth_nodes = [(m, graph[m]) for m in graph if graph[m] > m and graph[m] != 1]
    growth_nodes.sort(key=lambda x: x[1]/x[0], reverse=True)

    print(f"\nFound {len(growth_nodes)} nodes that map to larger values")
    print("\nTop 20 growth nodes (candidates for cycle membership):")
    for i, (m, f_m) in enumerate(growth_nodes[:20], 1):
        ratio = f_m / m
        print(f"{i:2d}. {m:6d} → {f_m:6d} (ratio: {ratio:.3f})")

    # Check if any of these form cycles
    print("\nChecking if any growth nodes participate in cycles...")
    for m, f_m in growth_nodes[:100]:
        # Try to follow the trajectory and see if it cycles
        path = [m]
        current = f_m
        seen = {m}

        for _ in range(1000):
            if current == 1:
                break
            if current in seen:
                # Potential cycle!
                cycle_start = path.index(current)
                cycle = path[cycle_start:]
                if len(cycle) > 1:
                    print(f"\n🚨 POTENTIAL CYCLE FOUND: {cycle}")
                break

            seen.add(current)
            path.append(current)

            if current not in graph:
                break
            current = graph[current]

def inverse_graph_analysis(graph: Dict[int, int], max_n: int) -> None:
    """
    Build inverse graph: which values map TO a given value?
    Cycles would show up as strongly connected components.
    """
    print("\n" + "="*70)
    print("ANALYSIS: Inverse Graph (Predecessors)")
    print("="*70)

    inverse = defaultdict(list)
    for m, f_m in graph.items():
        inverse[f_m].append(m)

    # Find values with multiple predecessors (potential cycle hubs)
    multi_pred = [(v, preds) for v, preds in inverse.items() if len(preds) > 1]
    multi_pred.sort(key=lambda x: len(x[1]), reverse=True)

    print(f"\nValues with multiple predecessors: {len(multi_pred)}")
    print("\nTop 10 (potential cycle hubs):")
    for i, (v, preds) in enumerate(multi_pred[:10], 1):
        print(f"{i:2d}. {v:6d} has {len(preds):3d} predecessors")
        if len(preds) <= 5:
            print(f"     Predecessors: {preds}")

def backwards_search_for_cycles(graph: Dict[int, int]) -> None:
    """
    Try to construct a cycle by working backwards from promising candidates.
    """
    print("\n" + "="*70)
    print("ATTACK: Backwards Search for Cycles")
    print("="*70)

    # Strategy: Start from values that map to themselves or nearly so
    print("\nSearching for fixed points (besides 1)...")
    for m in graph:
        if graph[m] == m and m != 1:
            print(f"🚨 FIXED POINT FOUND: {m} → {m}")

    # Search for 2-cycles
    print("\nSearching for 2-cycles (m → n → m)...")
    for m in graph:
        f_m = graph.get(m)
        if f_m and f_m in graph:
            f_f_m = graph[f_m]
            if f_f_m == m and m != f_m:
                print(f"🚨 2-CYCLE FOUND: {m} ⟷ {f_m}")

    # Search for 3-cycles
    print("\nSearching for 3-cycles (m → n → p → m)...")
    for m in graph:
        f_m = graph.get(m)
        if f_m and f_m in graph:
            f_f_m = graph[f_m]
            if f_f_m and f_f_m in graph:
                f_f_f_m = graph[f_f_m]
                if f_f_f_m == m and m != f_m != f_f_m:
                    print(f"🚨 3-CYCLE FOUND: {m} → {f_m} → {f_f_m} → {m}")

# MAIN ATTACK SEQUENCE

print("="*70)
print("CYCLE CONSTRUCTOR ATTACK")
print("="*70)
print("\nObjective: Find a cycle in ≡1 (mod 4) restricted dynamics")
print("If successful, Collatz is FALSE.")
print()

# Build graph for small values
print("Building restricted graph for n ≤ 50,000...")
graph = build_mod4_restricted_graph(50001)
print(f"Graph size: {len(graph)} nodes")

# Find cycles using Floyd's algorithm
print("\n" + "="*70)
print("ATTACK 1: Floyd's Cycle Detection")
print("="*70)

cycles = find_cycles_in_graph(graph)

if cycles:
    print(f"\n🚨🚨🚨 CYCLES FOUND: {len(cycles)} 🚨🚨🚨")
    for i, cycle in enumerate(cycles, 1):
        print(f"\nCycle {i}: {cycle}")
        print(f"Cycle length: {len(cycle)}")
        if 1 not in cycle:
            print("⚠️  NON-TRIVIAL CYCLE - COLLATZ IS FALSE!")
else:
    print("\n✓ No cycles found (besides 1 → 1)")

# Analyze potential cycle candidates
analyze_cycle_candidates(graph)

# Inverse graph analysis
inverse_graph_analysis(graph, 50001)

# Backwards search
backwards_search_for_cycles(graph)

# Final statistics
print("\n" + "="*70)
print("FINAL STATISTICS")
print("="*70)

reaches_1 = sum(1 for m, f_m in graph.items() if f_m == 1)
increases = sum(1 for m, f_m in graph.items() if f_m > m and f_m != 1)
decreases = sum(1 for m, f_m in graph.items() if f_m < m)

print(f"Total nodes: {len(graph)}")
print(f"Nodes mapping to 1: {reaches_1} ({100*reaches_1/len(graph):.1f}%)")
print(f"Nodes with F(m) > m: {increases} ({100*increases/len(graph):.1f}%)")
print(f"Nodes with F(m) < m: {decreases} ({100*decreases/len(graph):.1f}%)")

# Check connectivity to 1
print("\n" + "="*70)
print("CONNECTIVITY ANALYSIS")
print("="*70)

def reaches_1_eventually(m: int, graph: Dict[int, int], max_depth: int = 10000) -> Tuple[bool, int]:
    """Check if m reaches 1 in the restricted graph."""
    current = m
    depth = 0
    seen = set()

    while depth < max_depth:
        if current == 1:
            return True, depth
        if current in seen:
            return False, depth  # Cycle detected
        seen.add(current)
        if current not in graph:
            return False, depth  # Graph incomplete
        current = graph[current]
        depth += 1

    return False, max_depth

# Test connectivity
sample_size = min(100, len(graph))
sample_nodes = list(graph.keys())[:sample_size]

all_reach_1 = True
max_depth_to_1 = 0

for m in sample_nodes:
    reaches, depth = reaches_1_eventually(m, graph)
    if not reaches:
        print(f"⚠️  Node {m} does NOT reach 1 (or graph incomplete)")
        all_reach_1 = False
    else:
        max_depth_to_1 = max(max_depth_to_1, depth)

if all_reach_1:
    print(f"✓ All sampled nodes ({sample_size}) reach 1")
    print(f"  Max depth to 1: {max_depth_to_1}")
else:
    print(f"⚠️  Some nodes do not reach 1 in restricted graph")

print("\n" + "="*70)
print("ATTACK CONCLUSION")
print("="*70)
print("""
If cycles were found (besides 1→1): Collatz is FALSE ⚠️
If no cycles found: Attack failed, Collatz might be true ✓

The absence of cycles in computational range suggests:
- Cycles are either non-existent, or
- Cycles require astronomical values

Combined with hitting time theorem, this is evidence (not proof) that
all trajectories eventually reach 1.
""")
