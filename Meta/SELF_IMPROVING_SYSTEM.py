#!/usr/bin/env python3
"""
SELF-IMPROVING PROBLEM-SOLVING SYSTEM

This is a PROCESS with executable steps that:
1. Solves problems
2. Can be applied to "improve this process" as a problem
3. Measures improvement rigorously
4. Goes exponential by improving both strategy AND measurement

NOT a prompt. A SYSTEM.
"""

import anthropic
import json
import time
from datetime import datetime
from typing import Dict, List, Any

client = anthropic.Anthropic()

# =============================================================================
# THE STRATEGY (v1.0) - Executable steps for problem-solving
# =============================================================================

STRATEGY_V1 = """
PROBLEM-SOLVING STRATEGY v1.0

INPUT: A problem statement
OUTPUT: A solution with quality indicators

STEPS:
1. FRAME
   - What type of problem? (analytical/systems/wicked/optimization)
   - What would success look like?
   - What are the hard constraints?

2. GENERATE
   - Produce 3+ fundamentally different approaches
   - Include at least one that seems unconventional
   - Do NOT evaluate yet - just generate

3. EVALUATE
   - For each approach:
     a) Does it address the core tension?
     b) How could it fail? (pre-mortem)
     c) Is it specific enough to implement?
   - Score each 1-10 on feasibility and effectiveness

4. SELECT & REFINE
   - Choose best approach
   - Address top failure mode identified
   - Make implementation-specific

5. VERIFY
   - Does solution satisfy all constraints?
   - Would a stranger know exactly what to do?
   - What's the falsification test?

6. META
   - What worked in this problem-solving process?
   - What would I do differently next time?
   - Is there a transferable insight?
"""

# =============================================================================
# BENCHMARK PROBLEMS (Hard, diverse, measurable)
# =============================================================================

BENCHMARK_PROBLEMS = [
    {
        "id": "climate_binding",
        "problem": "Design a system for binding future generations to climate commitments they didn't vote for, while preserving democratic legitimacy.",
        "domain": "governance",
        "difficulty": "wicked"
    },
    {
        "id": "ai_prediction",
        "problem": "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy that balances public safety, civil liberties, and commercial viability.",
        "domain": "ethics/policy",
        "difficulty": "wicked"
    },
    {
        "id": "space_governance",
        "problem": "Create governance for a space habitat: 1000 people, 50-year journey, no Earth contact. Must handle succession, conflict, resource allocation, and cultural drift.",
        "domain": "systems",
        "difficulty": "complex"
    },
    {
        "id": "skill_transfer",
        "problem": "Brain implants allow direct skill transfer: 10 years of training in 10 minutes. Design the regulatory and social framework.",
        "domain": "policy",
        "difficulty": "wicked"
    },
    {
        "id": "lie_detection",
        "problem": "Quantum tech enables perfect lie detection with consent. Design rules for when it can/must/cannot be used across legal, employment, and personal contexts.",
        "domain": "ethics/law",
        "difficulty": "analytical"
    }
]

# =============================================================================
# EVALUATION CRITERIA (Adversarial, quote-based)
# =============================================================================

EVALUATION_PROMPT = """You are an ADVERSARIAL evaluator. Score this solution STRICTLY.

CRITERIA (each 0-3, total 15):

1. TENSION IDENTIFICATION (0-3)
   Does it explicitly name the core conflict/tradeoff?
   0 = No tension identified
   3 = Core tension named and directly addressed

2. MECHANISM SPECIFICITY (0-3)
   Could a stranger implement this exactly?
   0 = Vague principles only
   3 = Specific parameters, thresholds, processes

3. FAILURE AWARENESS (0-3)
   Does it address how the solution could fail?
   0 = No failure consideration
   3 = Specific failure modes identified and mitigated

4. CONSTRAINT SATISFACTION (0-3)
   Does it satisfy the problem's hard constraints?
   0 = Ignores constraints
   3 = All constraints explicitly satisfied

5. ACTIONABILITY (0-3)
   Is there a clear first step and path forward?
   0 = Abstract framework only
   3 = Concrete implementation path

RULES:
- For EACH criterion, you MUST quote exact text that satisfies it
- If you cannot quote, score is 0
- No credit for "implied" or "suggested"

PROBLEM: {problem}

SOLUTION:
{solution}

Respond with JSON only:
{{"tension": N, "mechanism": N, "failure": N, "constraints": N, "actionable": N, "total": N, "quotes": {{...}}}}
"""

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def solve_problem(problem: str, strategy: str) -> str:
    """Apply strategy to solve a problem"""
    prompt = f"""{strategy}

Now apply this strategy to solve:

PROBLEM: {problem}

Work through each step explicitly. Show your work."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def evaluate_solution(problem: str, solution: str) -> Dict:
    """Adversarially evaluate a solution"""
    prompt = EVALUATION_PROMPT.format(problem=problem, solution=solution)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    try:
        if '{' in text:
            return json.loads(text[text.index('{'):text.rindex('}')+1])
    except:
        pass
    return {"tension": 0, "mechanism": 0, "failure": 0, "constraints": 0, "actionable": 0, "total": 0}


def test_strategy(strategy: str, problems: List[Dict], label: str) -> Dict:
    """Test a strategy on benchmark problems"""
    print(f"\n{'='*60}")
    print(f"TESTING: {label}")
    print(f"{'='*60}")

    results = []
    for p in problems:
        print(f"  Solving: {p['id']}...", end=" ", flush=True)
        solution = solve_problem(p['problem'], strategy)
        score = evaluate_solution(p['problem'], solution)
        results.append({
            "problem_id": p['id'],
            "score": score,
            "solution": solution
        })
        print(f"Score: {score.get('total', 0)}/15")
        time.sleep(0.5)

    avg_score = sum(r['score'].get('total', 0) for r in results) / len(results)

    return {
        "strategy_label": label,
        "avg_score": avg_score,
        "max_possible": 15,
        "results": results
    }


def improve_strategy(current_strategy: str, test_results: Dict) -> str:
    """Use the strategy to improve itself"""

    improvement_problem = f"""
PROBLEM: Improve this problem-solving strategy to achieve higher scores.

CURRENT STRATEGY:
{current_strategy}

CURRENT PERFORMANCE:
- Average score: {test_results['avg_score']:.1f}/15
- Per-problem scores: {[r['score'].get('total', 0) for r in test_results['results']]}

SCORING CRITERIA (what we're measured on):
1. Tension identification (naming core conflicts)
2. Mechanism specificity (stranger could implement)
3. Failure awareness (pre-mortem thinking)
4. Constraint satisfaction (meets requirements)
5. Actionability (clear next steps)

WEAKEST AREAS (analyze the results):
{json.dumps([{
    'problem': r['problem_id'],
    'scores': r['score']
} for r in test_results['results']], indent=2)}

YOUR TASK:
Analyze what's causing low scores and modify the strategy to fix it.
Output the COMPLETE improved strategy (all steps, ready to use).
Keep what works. Fix what doesn't. Don't add complexity without clear benefit.
"""

    # Apply current strategy to the improvement problem
    improved = solve_problem(improvement_problem, current_strategy)

    # Extract just the strategy part (look for the strategy structure)
    # This is a simple extraction - in production you'd want better parsing
    return improved


def run_improvement_cycle(
    strategy: str,
    problems: List[Dict],
    cycle_num: int
) -> Dict:
    """Run one cycle: test → improve → test again"""

    print(f"\n{'#'*60}")
    print(f"CYCLE {cycle_num}")
    print(f"{'#'*60}")

    # Test current strategy
    before = test_strategy(strategy, problems, f"v{cycle_num}.0 (before)")

    # Improve strategy using itself
    print(f"\n  Improving strategy using itself...")
    improved_strategy = improve_strategy(strategy, before)

    # Test improved strategy
    after = test_strategy(improved_strategy, problems, f"v{cycle_num}.1 (after)")

    # Calculate improvement
    delta = after['avg_score'] - before['avg_score']

    print(f"\n  CYCLE {cycle_num} RESULT:")
    print(f"    Before: {before['avg_score']:.1f}/15")
    print(f"    After:  {after['avg_score']:.1f}/15")
    print(f"    Delta:  {delta:+.1f}")
    print(f"    Improved: {'YES' if delta > 0 else 'NO'}")

    return {
        "cycle": cycle_num,
        "before": before,
        "after": after,
        "delta": delta,
        "improved": delta > 0,
        "new_strategy": improved_strategy if delta > 0 else strategy
    }


def run_linear_proof(n_cycles: int = 3) -> Dict:
    """Prove linear improvement over multiple cycles"""

    print("\n" + "="*60)
    print("LINEAR IMPROVEMENT PROOF")
    print("="*60)
    print(f"Running {n_cycles} cycles to prove consistent improvement")

    strategy = STRATEGY_V1
    history = []

    for i in range(1, n_cycles + 1):
        result = run_improvement_cycle(strategy, BENCHMARK_PROBLEMS[:3], i)  # Use 3 problems for speed
        history.append(result)

        if result['improved']:
            strategy = result['new_strategy']

        time.sleep(1)

    # Analyze results
    improvements = [h['delta'] for h in history]
    consistent = all(d > 0 for d in improvements)

    print("\n" + "="*60)
    print("LINEAR PROOF RESULTS")
    print("="*60)
    print(f"Cycles: {n_cycles}")
    print(f"Improvements: {improvements}")
    print(f"Consistent gains: {consistent}")
    print(f"Total improvement: {sum(improvements):+.1f}")

    if consistent:
        print("\n✓ LINEAR IMPROVEMENT PROVEN")
        print("  Ready for exponential phase (improve strategy AND methodology)")
    else:
        print("\n✗ LINEAR IMPROVEMENT NOT YET PROVEN")
        print("  Need to debug before going exponential")

    return {
        "n_cycles": n_cycles,
        "history": history,
        "improvements": improvements,
        "consistent": consistent,
        "final_strategy": strategy
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("="*60)
    print("SELF-IMPROVING PROBLEM-SOLVING SYSTEM")
    print("="*60)
    print("\nThis system:")
    print("1. Has a STRATEGY (executable steps)")
    print("2. Tests on BENCHMARK problems")
    print("3. Uses strategy to IMPROVE ITSELF")
    print("4. Proves LINEAR improvement before going exponential")

    # Run the linear proof
    results = run_linear_proof(n_cycles=3)

    # Save results
    with open("self_improving_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("\nResults saved to self_improving_results.json")
