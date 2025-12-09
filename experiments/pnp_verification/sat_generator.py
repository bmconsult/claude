"""
SAT Instance Generator with Controlled Treewidth and Frustration

This module generates SAT instances with known structural properties
for testing the prediction: resolution length ≥ exp(tw × F_G / n)
"""

import random
from typing import List, Tuple, Set
from dataclasses import dataclass

@dataclass
class SATInstance:
    """A SAT instance with metadata"""
    clauses: List[Tuple[int, ...]]  # Each clause is tuple of literals (positive = true, negative = false)
    num_vars: int
    name: str
    expected_tw: str  # Description of expected treewidth
    expected_satisfiable: bool

def generate_random_3sat(n_vars: int, clause_ratio: float = 4.2) -> SATInstance:
    """
    Generate random 3-SAT at given clause-to-variable ratio.

    At ratio ~4.27, random 3-SAT undergoes phase transition.
    - Below 4.27: likely satisfiable
    - Above 4.27: likely unsatisfiable

    Treewidth: Θ(n) for random graphs
    """
    n_clauses = int(n_vars * clause_ratio)
    clauses = []

    for _ in range(n_clauses):
        # Pick 3 distinct variables
        vars_chosen = random.sample(range(1, n_vars + 1), 3)
        # Random signs
        clause = tuple(v * random.choice([1, -1]) for v in vars_chosen)
        clauses.append(clause)

    return SATInstance(
        clauses=clauses,
        num_vars=n_vars,
        name=f"random_3sat_n{n_vars}_r{clause_ratio}",
        expected_tw="Θ(n)",
        expected_satisfiable=(clause_ratio < 4.27)
    )

def generate_pigeonhole(n_holes: int) -> SATInstance:
    """
    Generate Pigeonhole Principle: n+1 pigeons into n holes.

    Variables: p_{i,j} = "pigeon i in hole j" for i in [1,n+1], j in [1,n]

    Constraints:
    1. Each pigeon in at least one hole: OR_j p_{i,j} for each i
    2. Each hole has at most one pigeon: ¬p_{i,j} ∨ ¬p_{k,j} for i < k

    Known: Requires exp(n) resolution proof (Haken 1985)
    Treewidth: Θ(n)
    F_G: Θ(n) - need all constraints to see contradiction
    """
    n_pigeons = n_holes + 1
    clauses = []

    def var(pigeon, hole):
        """Variable number for pigeon i in hole j"""
        return (pigeon - 1) * n_holes + hole

    # Each pigeon must be in some hole
    for i in range(1, n_pigeons + 1):
        clause = tuple(var(i, j) for j in range(1, n_holes + 1))
        clauses.append(clause)

    # No two pigeons in same hole
    for j in range(1, n_holes + 1):
        for i1 in range(1, n_pigeons + 1):
            for i2 in range(i1 + 1, n_pigeons + 1):
                clauses.append((-var(i1, j), -var(i2, j)))

    num_vars = n_pigeons * n_holes

    return SATInstance(
        clauses=clauses,
        num_vars=num_vars,
        name=f"pigeonhole_{n_holes}",
        expected_tw=f"Θ({n_holes})",
        expected_satisfiable=False
    )

def generate_tseitin_grid(width: int, height: int) -> SATInstance:
    """
    Generate Tseitin formula on a grid graph with odd parity.

    Each edge has a variable. Each vertex has XOR constraint
    (sum of incident edges mod 2 = parity[v]).

    If sum of parities is odd, formula is unsatisfiable.

    Treewidth of grid: Θ(min(width, height))
    F_G on grid: Θ(n) if parities sum to 1
    """
    # Edge variables
    edges = {}
    var_count = 0

    # Horizontal edges
    for y in range(height):
        for x in range(width - 1):
            var_count += 1
            edges[(x, y, x+1, y)] = var_count

    # Vertical edges
    for y in range(height - 1):
        for x in range(width):
            var_count += 1
            edges[(x, y, x, y+1)] = var_count

    # For unsatisfiability: set total parity to 1 (odd)
    # We'll put parity 1 at (0,0) and 0 elsewhere
    clauses = []

    def get_edge_var(x1, y1, x2, y2):
        if (x1, y1, x2, y2) in edges:
            return edges[(x1, y1, x2, y2)]
        return edges[(x2, y2, x1, y1)]

    def add_xor_clauses(vars_list: List[int], parity: int):
        """Add clauses enforcing XOR of variables equals parity"""
        n = len(vars_list)
        # Need 2^(n-1) clauses for XOR
        for mask in range(1 << n):
            # Count negations
            neg_count = bin(mask).count('1')
            # Include clause if parity of negations equals desired parity
            if neg_count % 2 != parity:
                clause = tuple(
                    -vars_list[i] if (mask >> i) & 1 else vars_list[i]
                    for i in range(n)
                )
                clauses.append(clause)

    # Add XOR constraint for each vertex
    for y in range(height):
        for x in range(width):
            incident_vars = []
            # Check all four neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    incident_vars.append(get_edge_var(x, y, nx, ny))

            # Parity: 1 at origin, 0 elsewhere (makes total parity 1 = UNSAT)
            parity = 1 if (x == 0 and y == 0) else 0

            if incident_vars:  # Should always be non-empty for grid
                add_xor_clauses(incident_vars, parity)

    return SATInstance(
        clauses=clauses,
        num_vars=var_count,
        name=f"tseitin_grid_{width}x{height}",
        expected_tw=f"Θ({min(width, height)})",
        expected_satisfiable=False
    )

def generate_tree_formula(depth: int, branching: int = 2) -> SATInstance:
    """
    Generate formula on a tree structure.

    Treewidth: O(1) for trees
    Should have polynomial-size resolution proofs even if unsatisfiable.
    """
    # Build tree: each internal node has 'branching' children
    # Variables on edges
    var_count = 0
    clauses = []

    def build_tree(d: int, parent_var: int = None):
        nonlocal var_count, clauses

        if d == 0:
            return

        child_vars = []
        for _ in range(branching):
            var_count += 1
            child_vars.append(var_count)

        # Add implication from parent to at least one child
        if parent_var:
            # parent → (c1 ∨ c2 ∨ ...)
            clauses.append(tuple([-parent_var] + child_vars))
            # And each child implies contradiction at leaves

        for cv in child_vars:
            build_tree(d - 1, cv)

    # Start: at least one root must be true
    root_vars = []
    for _ in range(branching):
        var_count += 1
        root_vars.append(var_count)
    clauses.append(tuple(root_vars))

    for rv in root_vars:
        build_tree(depth - 1, rv)

    # Make unsatisfiable: all leaves must be false
    # Add unit clauses for all leaf variables
    n_internal = sum(branching**i for i in range(depth))
    for v in range(n_internal + 1, var_count + 1):
        clauses.append((-v,))

    return SATInstance(
        clauses=clauses,
        num_vars=var_count,
        name=f"tree_d{depth}_b{branching}",
        expected_tw="O(1)",
        expected_satisfiable=False
    )

def to_dimacs(instance: SATInstance) -> str:
    """Convert to DIMACS CNF format"""
    lines = [f"c {instance.name}"]
    lines.append(f"c Expected treewidth: {instance.expected_tw}")
    lines.append(f"c Expected satisfiable: {instance.expected_satisfiable}")
    lines.append(f"p cnf {instance.num_vars} {len(instance.clauses)}")

    for clause in instance.clauses:
        lines.append(" ".join(map(str, clause)) + " 0")

    return "\n".join(lines)


if __name__ == "__main__":
    # Generate test instances
    print("=== Random 3-SAT (n=20, ratio=5.0 - UNSAT region) ===")
    inst = generate_random_3sat(20, 5.0)
    print(f"Clauses: {len(inst.clauses)}, Vars: {inst.num_vars}")
    print(f"Expected tw: {inst.expected_tw}")
    print()

    print("=== Pigeonhole PHP(5) ===")
    inst = generate_pigeonhole(5)
    print(f"Clauses: {len(inst.clauses)}, Vars: {inst.num_vars}")
    print(f"Expected tw: {inst.expected_tw}")
    print()

    print("=== Tseitin on 4x4 Grid ===")
    inst = generate_tseitin_grid(4, 4)
    print(f"Clauses: {len(inst.clauses)}, Vars: {inst.num_vars}")
    print(f"Expected tw: {inst.expected_tw}")
    print()

    print("=== Tree Formula (depth=4) ===")
    inst = generate_tree_formula(4)
    print(f"Clauses: {len(inst.clauses)}, Vars: {inst.num_vars}")
    print(f"Expected tw: {inst.expected_tw}")
