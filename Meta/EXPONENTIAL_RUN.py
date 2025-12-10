#!/usr/bin/env python3
"""
EXPONENTIAL PHASE: The system improves BOTH strategy AND measurement

When linear improvement hits ceiling, the exponential unlock comes from
improving the measurement system to reveal hidden weaknesses.
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# Strategy v3 (hit ceiling at 15/15 on basic metrics)
STRATEGY_V3 = """
PROBLEM-SOLVING STRATEGY v3.0

STEPS:
1. FRAME: What type? What's success? What constraints?
2. GENERATE: 3+ different approaches, including unconventional
3. EVALUATE: Core tension? Failure modes? Specific enough?
4. SELECT & REFINE: Best approach, address top failure mode
5. VERIFY: All constraints? Stranger could implement? Falsification test?
6. META: What worked? What next time? Transferable insight?
"""

BENCHMARK_PROBLEMS = [
    {
        "id": "climate",
        "text": "Design a system for binding future generations to climate commitments they didn't vote for.",
    },
    {
        "id": "ai_crime",
        "text": "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
    },
    {
        "id": "space",
        "text": "Create governance for a space habitat: 1000 people, 50-year journey, no Earth contact.",
    },
]

# V1 CRITERIA (what we hit ceiling on)
V1_CRITERIA = """
CRITERIA (each 0-3, total 15):
1. TENSION: Names core conflict explicitly (0=none, 3=identified and addressed)
2. MECHANISM: Stranger could implement exactly (0=vague, 3=specific parameters)
3. FAILURE: Addresses how it could fail (0=none, 3=specific modes mitigated)
4. CONSTRAINTS: Satisfies problem requirements (0=ignores, 3=all satisfied)
5. ACTIONABLE: Clear path forward (0=abstract, 3=concrete steps)
"""

# V2 CRITERIA (harder - reveals hidden weaknesses)
V2_CRITERIA = """
CRITERIA (each 0-3, total 15):
1. SECOND-ORDER: Addresses consequences of consequences (0=first-order only, 3=traces 3+ levels)
2. ADVERSARIAL: Survives hostile actors gaming the system (0=naive, 3=robust to gaming)
3. ELEGANCE: Minimal complexity for effect (0=bloated, 3=parsimonious)
4. ADAPTABILITY: Handles changed conditions (0=brittle, 3=self-adjusting)
5. NOVEL: Non-obvious approach (0=standard, 3=genuinely creative)
"""

def solve_problem(problem: str, strategy: str) -> str:
    """Apply strategy to solve a problem"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {problem}\n\nApply the strategy:"}]
    )
    return response.content[0].text


def evaluate_solution(problem: str, solution: str, criteria: str) -> dict:
    """Adversarially evaluate a solution"""
    prompt = f"""You are an ADVERSARIAL evaluator. Score STRICTLY.

{criteria}

For EACH criterion:
- QUOTE exact text from the solution that satisfies it
- If you cannot quote specific text, score is 0
- No credit for "implied" or "suggested"

PROBLEM: {problem}

SOLUTION:
{solution}

Return JSON with scores for each criterion (use keys: c1, c2, c3, c4, c5) and total.
Example: {{"c1": 2, "c2": 1, "c3": 3, "c4": 2, "c5": 1, "total": 9}}

JSON only:"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    try:
        if '{' in text:
            return json.loads(text[text.index('{'):text.rindex('}')+1])
    except:
        pass
    return {"c1": 0, "c2": 0, "c3": 0, "c4": 0, "c5": 0, "total": 0}


def test_strategy(strategy: str, problems: list, criteria: str, label: str) -> dict:
    """Test a strategy on problems with given criteria"""
    print(f"\n  Testing: {label}")
    results = []
    for p in problems:
        solution = solve_problem(p["text"], strategy)
        score = evaluate_solution(p["text"], solution, criteria)
        results.append({"id": p["id"], "score": score, "solution_preview": solution[:200]})
        print(f"    {p['id']}: {score.get('total', 0)}/15")
        time.sleep(0.5)

    avg = sum(r["score"].get("total", 0) for r in results) / len(results)
    return {"label": label, "avg": avg, "results": results}


def improve_strategy_for_criteria(strategy: str, weak_criteria: str, test_results: dict) -> str:
    """Use strategy to improve itself for specific weak criteria"""

    improvement_problem = f"""
I need to improve my problem-solving strategy to score better on NEW harder criteria.

CURRENT STRATEGY:
{strategy}

NEW CRITERIA I'M WEAK ON:
{weak_criteria}

MY RECENT SCORES on these criteria:
{json.dumps([{"problem": r["id"], "scores": r["score"]} for r in test_results["results"]], indent=2)}

TASK: Modify the strategy to explicitly address these harder criteria.
Add specific steps or sub-steps that force consideration of:
- Second-order effects
- Adversarial robustness
- Elegance/parsimony
- Adaptability
- Novelty

Output the COMPLETE improved strategy (all steps).
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {improvement_problem}\n\nApply the strategy to solve this:"}]
    )
    return response.content[0].text


def run_exponential():
    """Run the exponential improvement loop"""

    print("="*70)
    print("EXPONENTIAL PHASE: Improve BOTH Strategy AND Measurement")
    print("="*70)

    strategy = STRATEGY_V3

    # STEP 1: Confirm ceiling on V1 criteria
    print("\n" + "="*70)
    print("STEP 1: Confirm ceiling on V1 (basic) criteria")
    print("="*70)
    v1_results = test_strategy(strategy, BENCHMARK_PROBLEMS, V1_CRITERIA, "v3 strategy + v1 criteria")
    print(f"\n  Average: {v1_results['avg']:.1f}/15 (expected: near ceiling)")

    # STEP 2: Test with V2 (harder) criteria - reveals hidden weaknesses
    print("\n" + "="*70)
    print("STEP 2: Test with V2 (harder) criteria - reveals hidden weaknesses")
    print("="*70)
    v2_baseline = test_strategy(strategy, BENCHMARK_PROBLEMS, V2_CRITERIA, "v3 strategy + v2 criteria")
    print(f"\n  Average: {v2_baseline['avg']:.1f}/15")
    print(f"  GAP REVEALED: {v1_results['avg'] - v2_baseline['avg']:.1f} points of hidden weakness!")

    # STEP 3: Use strategy to improve itself for V2 criteria
    print("\n" + "="*70)
    print("STEP 3: Use strategy to improve itself for harder criteria")
    print("="*70)
    improved_strategy = improve_strategy_for_criteria(strategy, V2_CRITERIA, v2_baseline)
    print(f"\n  Improved strategy generated ({len(improved_strategy)} chars)")

    # STEP 4: Test improved strategy on V2 criteria
    print("\n" + "="*70)
    print("STEP 4: Test improved strategy on V2 criteria")
    print("="*70)
    v2_improved = test_strategy(improved_strategy, BENCHMARK_PROBLEMS, V2_CRITERIA, "v4 strategy + v2 criteria")
    print(f"\n  Average: {v2_improved['avg']:.1f}/15")

    # STEP 5: Calculate exponential gain
    improvement = v2_improved['avg'] - v2_baseline['avg']

    print("\n" + "="*70)
    print("EXPONENTIAL RESULTS")
    print("="*70)
    print(f"\nV1 criteria (basic):     {v1_results['avg']:.1f}/15 (ceiling)")
    print(f"V2 criteria (harder):    {v2_baseline['avg']:.1f}/15 (gap revealed)")
    print(f"V2 after improvement:    {v2_improved['avg']:.1f}/15")
    print(f"\nImprovement on V2: {improvement:+.1f}")

    if improvement > 0:
        print("\n✓ EXPONENTIAL UNLOCK DEMONSTRATED")
        print("  1. Hit ceiling on V1 metrics")
        print("  2. Improved measurement (V2) revealed hidden weaknesses")
        print("  3. Strategy improved itself for new criteria")
        print("  4. This cycle can repeat: V3 criteria → more improvement → V4...")
    else:
        print("\n→ Need another improvement cycle")

    # Save results
    results = {
        "v1_ceiling": v1_results,
        "v2_baseline": v2_baseline,
        "v2_improved": v2_improved,
        "improvement": improvement,
        "improved_strategy": improved_strategy
    }

    with open("exponential_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("\nSaved to exponential_results.json")
    return results


if __name__ == "__main__":
    run_exponential()
