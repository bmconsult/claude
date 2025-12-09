"""
LLM Difficulty Metric Test Battery

Hypothesis: LLM performance is predicted by structural properties different from
computational complexity.

Key factors:
1. state_depth - how many values must be tracked simultaneously
2. backref_distance - how far back context matters
3. decomposability - can problem split into independent parts
4. pattern_familiarity - how common is this problem type
5. verification_gap - difference between verify and solve difficulty
"""

import random
import json
from dataclasses import dataclass, asdict
from typing import List, Callable, Any, Optional
from enum import Enum

class ComplexityClass(Enum):
    CONSTANT = "O(1)"
    LINEAR = "O(n)"
    POLYNOMIAL = "P"
    NP = "NP"
    NP_HARD = "NP-hard"

@dataclass
class Problem:
    id: str
    category: str
    prompt: str
    expected_answer: Any
    complexity_class: ComplexityClass

    # LLM difficulty factors (1-10 scale)
    state_depth: int  # Variables to track simultaneously
    backref_distance: int  # How far back context matters
    decomposability: int  # 10 = fully decomposable, 1 = monolithic
    pattern_familiarity: int  # 10 = very common, 1 = rare
    verification_gap: int  # 10 = verify much easier than solve, 1 = same

    # Predicted and actual outcomes
    predicted_difficulty: Optional[float] = None
    actual_correct: Optional[bool] = None
    actual_reasoning_quality: Optional[int] = None  # 1-10

    def compute_predicted_difficulty(self) -> float:
        """
        Higher score = harder for LLM.
        Factors that increase difficulty: high state_depth, high backref,
        low decomposability, low familiarity, low verification_gap.
        """
        difficulty = (
            self.state_depth * 1.5 +  # State tracking is hard
            self.backref_distance * 1.0 +  # Long-range deps are hard
            (10 - self.decomposability) * 0.8 +  # Non-decomposable is hard
            (10 - self.pattern_familiarity) * 0.7 +  # Unfamiliar is hard
            (10 - self.verification_gap) * 0.5  # Verify=Solve is harder
        )
        self.predicted_difficulty = difficulty / 10.0  # Normalize to ~0-5 scale
        return self.predicted_difficulty

def generate_arithmetic_pairs() -> List[Problem]:
    """Generate arithmetic problem pairs: verify vs compute."""
    problems = []

    # Pair 1: Multiplication verify vs compute
    a, b = 17, 23
    product = a * b

    problems.append(Problem(
        id="arith_mult_verify_1",
        category="arithmetic",
        prompt=f"Is {a} × {b} = {product}? Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=2,  # Just track two numbers
        backref_distance=1,
        decomposability=8,
        pattern_familiarity=9,
        verification_gap=9,  # Verify much easier
    ))

    problems.append(Problem(
        id="arith_mult_compute_1",
        category="arithmetic",
        prompt=f"What is {a} × {b}? Compute the exact answer.",
        expected_answer=str(product),
        complexity_class=ComplexityClass.LINEAR,
        state_depth=4,  # Track intermediate results
        backref_distance=2,
        decomposability=6,
        pattern_familiarity=9,
        verification_gap=3,
    ))

    # Pair 2: Primality verify vs factor
    n = 143  # = 11 × 13
    problems.append(Problem(
        id="prime_verify_1",
        category="arithmetic",
        prompt=f"Is 143 = 11 × 13? Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=2,
        backref_distance=1,
        decomposability=8,
        pattern_familiarity=7,
        verification_gap=9,
    ))

    problems.append(Problem(
        id="prime_factor_1",
        category="arithmetic",
        prompt="Factor 143 into prime factors.",
        expected_answer="11 × 13",
        complexity_class=ComplexityClass.POLYNOMIAL,  # Trial division is O(sqrt(n))
        state_depth=3,
        backref_distance=2,
        decomposability=4,
        pattern_familiarity=6,
        verification_gap=5,
    ))

    return problems

def generate_sequence_pairs() -> List[Problem]:
    """Generate sequence problems with varying state requirements."""
    problems = []

    # Fibonacci verification vs computation
    fib_seq = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    problems.append(Problem(
        id="fib_verify",
        category="sequence",
        prompt=f"Is this sequence Fibonacci? [1, 1, 2, 3, 5, 8, 13, 21]. Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=3,  # Track last 3 values
        backref_distance=2,
        decomposability=9,  # Each pair can be checked independently
        pattern_familiarity=10,
        verification_gap=8,
    ))

    problems.append(Problem(
        id="fib_compute_20",
        category="sequence",
        prompt="What is the 20th Fibonacci number? (Starting with F(1)=1, F(2)=1)",
        expected_answer="6765",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=7,  # Need to track many intermediate values without writing
        backref_distance=20,  # Need all previous context
        decomposability=3,  # Can't really parallelize
        pattern_familiarity=8,
        verification_gap=4,
    ))

    # Sorted verification vs sorting
    sorted_list = list(range(1, 11))
    random.seed(42)
    unsorted_list = sorted_list.copy()
    random.shuffle(unsorted_list)

    problems.append(Problem(
        id="sorted_verify",
        category="sequence",
        prompt=f"Is this list sorted in increasing order? {sorted_list}. Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=2,
        backref_distance=1,
        decomposability=10,
        pattern_familiarity=10,
        verification_gap=9,
    ))

    problems.append(Problem(
        id="sorting",
        category="sequence",
        prompt=f"Sort this list in increasing order: {unsorted_list}",
        expected_answer=str(sorted_list),
        complexity_class=ComplexityClass.POLYNOMIAL,  # O(n log n)
        state_depth=5,
        backref_distance=3,
        decomposability=7,  # Merge sort is decomposable
        pattern_familiarity=10,
        verification_gap=6,
    ))

    return problems

def generate_graph_pairs() -> List[Problem]:
    """Generate graph problems."""
    problems = []

    # Path verification vs finding
    problems.append(Problem(
        id="path_verify",
        category="graph",
        prompt="In a graph with nodes {A,B,C,D,E} and edges A-B, B-C, C-D, D-E, A-E, "
               "does the path A→B→C→D→E visit all nodes exactly once? Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=5,
        backref_distance=5,
        decomposability=7,
        pattern_familiarity=6,
        verification_gap=9,
    ))

    problems.append(Problem(
        id="hamiltonian_find",
        category="graph",
        prompt="In a complete graph K5 with nodes {A,B,C,D,E}, find any Hamiltonian path "
               "(a path that visits each node exactly once).",
        expected_answer="Any valid permutation, e.g., A→B→C→D→E",
        complexity_class=ComplexityClass.NP,  # But trivial for K5
        state_depth=5,
        backref_distance=5,
        decomposability=2,
        pattern_familiarity=5,
        verification_gap=7,  # Finding is hard in general, but K5 is small
    ))

    # Graph coloring
    problems.append(Problem(
        id="coloring_verify",
        category="graph",
        prompt="Given a triangle graph (3 nodes, all connected), is this a valid 3-coloring: "
               "A=Red, B=Green, C=Blue? Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=3,
        backref_distance=2,
        decomposability=9,
        pattern_familiarity=7,
        verification_gap=9,
    ))

    problems.append(Problem(
        id="coloring_find_hard",
        category="graph",
        prompt="A graph has 6 nodes {1,2,3,4,5,6} with edges: 1-2, 1-3, 2-3, 2-4, 3-5, 4-5, 4-6, 5-6. "
               "Find a valid 3-coloring (assign Red, Green, or Blue to each node such that "
               "no adjacent nodes share a color).",
        expected_answer="Multiple valid solutions, e.g., 1=R, 2=G, 3=B, 4=R, 5=G, 6=B",
        complexity_class=ComplexityClass.NP,
        state_depth=6,
        backref_distance=6,
        decomposability=3,
        pattern_familiarity=5,
        verification_gap=7,
    ))

    return problems

def generate_logic_pairs() -> List[Problem]:
    """Generate logic/constraint problems."""
    problems = []

    # SAT verification vs solving
    problems.append(Problem(
        id="sat_verify",
        category="logic",
        prompt="For variables x=True, y=False, z=True, is this formula satisfied? "
               "(x OR y) AND (NOT y OR z) AND (x OR z). Answer yes or no.",
        expected_answer="yes",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=3,
        backref_distance=1,
        decomposability=9,
        pattern_familiarity=5,
        verification_gap=9,
    ))

    problems.append(Problem(
        id="sat_solve",
        category="logic",
        prompt="Find values for x, y, z (each True or False) that satisfy: "
               "(x OR y) AND (NOT x OR z) AND (NOT y OR NOT z) AND (x OR NOT y OR z)",
        expected_answer="x=True, y=False, z=True (or other valid assignment)",
        complexity_class=ComplexityClass.NP,
        state_depth=4,
        backref_distance=4,
        decomposability=4,
        pattern_familiarity=4,
        verification_gap=7,
    ))

    return problems

def generate_state_tracking_problems() -> List[Problem]:
    """Problems that specifically test state tracking ability."""
    problems = []

    # Simple state: count occurrences
    problems.append(Problem(
        id="count_simple",
        category="state_tracking",
        prompt="Count how many times the letter 'a' appears in: 'abracadabra'",
        expected_answer="5",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=2,
        backref_distance=1,
        decomposability=10,
        pattern_familiarity=10,
        verification_gap=5,
    ))

    # Complex state: track multiple variables
    problems.append(Problem(
        id="track_multi",
        category="state_tracking",
        prompt="Start with a=0, b=1. For each step: new_a = b, new_b = a+b. "
               "After 10 steps, what are a and b?",
        expected_answer="a=55, b=89",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=6,  # Need to track a, b, new_a, new_b, step count
        backref_distance=10,
        decomposability=2,
        pattern_familiarity=6,  # It's Fibonacci in disguise
        verification_gap=4,
    ))

    # State with branching
    problems.append(Problem(
        id="conditional_track",
        category="state_tracking",
        prompt="Start with x=5. For i from 1 to 6: if i is even, x = x*2; else x = x+1. "
               "What is final x?",
        expected_answer="52",
        complexity_class=ComplexityClass.LINEAR,
        state_depth=4,
        backref_distance=6,
        decomposability=3,
        pattern_familiarity=7,
        verification_gap=4,
    ))

    return problems

def generate_all_problems() -> List[Problem]:
    """Generate the full test battery."""
    problems = []
    problems.extend(generate_arithmetic_pairs())
    problems.extend(generate_sequence_pairs())
    problems.extend(generate_graph_pairs())
    problems.extend(generate_logic_pairs())
    problems.extend(generate_state_tracking_problems())

    # Compute predicted difficulties
    for p in problems:
        p.compute_predicted_difficulty()

    return problems

def save_problems(problems: List[Problem], filename: str):
    """Save problems to JSON file."""
    data = [asdict(p) for p in problems]
    for d in data:
        d['complexity_class'] = d['complexity_class'].value
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def print_problem_summary(problems: List[Problem]):
    """Print summary of problems sorted by predicted difficulty."""
    print("\n=== LLM Difficulty Test Battery ===\n")
    print(f"Total problems: {len(problems)}\n")

    # Sort by predicted difficulty
    sorted_problems = sorted(problems, key=lambda p: p.predicted_difficulty or 0)

    print("Problems by predicted difficulty (easiest first):\n")
    print(f"{'ID':<25} {'Category':<15} {'Complexity':<10} {'Pred.Diff':>10}")
    print("-" * 65)

    for p in sorted_problems:
        print(f"{p.id:<25} {p.category:<15} {p.complexity_class.value:<10} {p.predicted_difficulty:>10.2f}")

    # Print difficulty factors
    print("\n\nDifficulty Factor Analysis:")
    print("-" * 65)
    for p in sorted_problems[:5]:
        print(f"\n{p.id} (pred_diff={p.predicted_difficulty:.2f}):")
        print(f"  state_depth={p.state_depth}, backref={p.backref_distance}, "
              f"decomp={p.decomposability}, familiar={p.pattern_familiarity}, verif_gap={p.verification_gap}")

if __name__ == "__main__":
    problems = generate_all_problems()
    print_problem_summary(problems)
    save_problems(problems, "llm_difficulty_battery.json")
    print("\nProblems saved to llm_difficulty_battery.json")
