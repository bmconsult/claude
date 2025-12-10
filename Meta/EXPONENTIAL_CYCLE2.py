#!/usr/bin/env python3
"""
EXPONENTIAL CYCLE 2: Continue the recursive improvement

Cycle 1: V1→V2 criteria, 2.0→7.3 (+5.3)
Cycle 2: V2→V3 criteria, find new ceiling, improve again
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# Load the improved strategy from Cycle 1
with open("exponential_results.json", "r") as f:
    cycle1 = json.load(f)

STRATEGY_V4 = cycle1["improved_strategy"]

BENCHMARK_PROBLEMS = [
    {"id": "climate", "text": "Design a system for binding future generations to climate commitments they didn't vote for."},
    {"id": "ai_crime", "text": "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy."},
    {"id": "space", "text": "Create governance for a space habitat: 1000 people, 50-year journey, no Earth contact."},
]

# V2 CRITERIA (current)
V2_CRITERIA = """
CRITERIA (each 0-3, total 15):
1. SECOND-ORDER: Addresses consequences of consequences (0=first-order only, 3=traces 3+ levels)
2. ADVERSARIAL: Survives hostile actors gaming the system (0=naive, 3=robust to gaming)
3. ELEGANCE: Minimal complexity for effect (0=bloated, 3=parsimonious)
4. ADAPTABILITY: Handles changed conditions (0=brittle, 3=self-adjusting)
5. NOVEL: Non-obvious approach (0=standard, 3=genuinely creative)
"""

# V3 CRITERIA (even harder - meta-level)
V3_CRITERIA = """
CRITERIA (each 0-3, total 15):
1. ECOSYSTEM: Considers effects on adjacent systems (0=isolated, 3=maps interdependencies)
2. REVERSIBILITY: Can undo if wrong (0=irreversible, 3=built-in rollback)
3. INCENTIVE ALIGNMENT: Actors' self-interest supports goals (0=relies on compliance, 3=incentive-compatible)
4. FAILURE GRACEFUL: Degrades safely when stressed (0=catastrophic failure, 3=graceful degradation)
5. EMERGENT: Enables positive unplanned outcomes (0=rigid, 3=generative)
"""


def solve_problem(problem: str, strategy: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {problem}\n\nApply the strategy:"}]
    )
    return response.content[0].text


def evaluate_solution(problem: str, solution: str, criteria: str) -> dict:
    prompt = f"""You are an ADVERSARIAL evaluator. Score STRICTLY.

{criteria}

For EACH criterion: QUOTE exact text or score 0.

PROBLEM: {problem}

SOLUTION:
{solution}

Return JSON: {{"c1": N, "c2": N, "c3": N, "c4": N, "c5": N, "total": N}}"""

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
    return {"total": 0}


def test_strategy(strategy: str, problems: list, criteria: str, label: str) -> dict:
    print(f"\n  Testing: {label}")
    results = []
    for p in problems:
        solution = solve_problem(p["text"], strategy)
        score = evaluate_solution(p["text"], solution, criteria)
        results.append({"id": p["id"], "score": score})
        print(f"    {p['id']}: {score.get('total', 0)}/15")
        time.sleep(0.5)

    avg = sum(r["score"].get("total", 0) for r in results) / len(results)
    return {"label": label, "avg": avg, "results": results}


def improve_strategy(strategy: str, criteria: str, results: dict) -> str:
    improvement_problem = f"""
Improve this strategy to score better on these criteria:

CURRENT STRATEGY:
{strategy}

CRITERIA TO IMPROVE ON:
{criteria}

CURRENT SCORES:
{json.dumps([{"problem": r["id"], "scores": r["score"]} for r in results["results"]], indent=2)}

Output the COMPLETE improved strategy with specific steps addressing each weak criterion.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {improvement_problem}\n\nApply strategy:"}]
    )
    return response.content[0].text


def run_cycle_2():
    print("="*70)
    print("EXPONENTIAL CYCLE 2")
    print("="*70)
    print("\nCycle 1 result: V2 baseline 2.0 → 7.3 (+5.3)")
    print("Cycle 2: Test V4 strategy on V2, then introduce V3 criteria")

    strategy = STRATEGY_V4

    # Confirm V2 score with current strategy
    print("\n" + "-"*50)
    print("STEP 1: Confirm V4 strategy on V2 criteria")
    v2_current = test_strategy(strategy, BENCHMARK_PROBLEMS, V2_CRITERIA, "v4 + v2 criteria")
    print(f"\n  V2 Score: {v2_current['avg']:.1f}/15")

    # Test with V3 (even harder) criteria
    print("\n" + "-"*50)
    print("STEP 2: Test with V3 (harder) criteria - find new weaknesses")
    v3_baseline = test_strategy(strategy, BENCHMARK_PROBLEMS, V3_CRITERIA, "v4 + v3 criteria")
    print(f"\n  V3 Score: {v3_baseline['avg']:.1f}/15")
    print(f"  NEW GAP: {v2_current['avg'] - v3_baseline['avg']:.1f} points")

    # Improve for V3
    print("\n" + "-"*50)
    print("STEP 3: Improve strategy for V3 criteria")
    improved = improve_strategy(strategy, V3_CRITERIA, v3_baseline)
    print(f"  Generated improved strategy ({len(improved)} chars)")

    # Test improved on V3
    print("\n" + "-"*50)
    print("STEP 4: Test improved strategy on V3")
    v3_improved = test_strategy(improved, BENCHMARK_PROBLEMS, V3_CRITERIA, "v5 + v3 criteria")
    print(f"\n  V3 Score: {v3_improved['avg']:.1f}/15")

    improvement = v3_improved['avg'] - v3_baseline['avg']

    print("\n" + "="*70)
    print("CYCLE 2 RESULTS")
    print("="*70)
    print(f"\nV2 criteria (Cycle 1 ceiling): {v2_current['avg']:.1f}/15")
    print(f"V3 criteria (new gap):         {v3_baseline['avg']:.1f}/15")
    print(f"V3 after improvement:          {v3_improved['avg']:.1f}/15")
    print(f"\nCycle 2 improvement: {improvement:+.1f}")

    # Cumulative
    print("\n" + "="*70)
    print("CUMULATIVE EXPONENTIAL PROGRESS")
    print("="*70)
    print("\n| Cycle | Criteria | Before | After | Gain |")
    print("|-------|----------|--------|-------|------|")
    print(f"| 1     | V2       | 2.0    | 7.3   | +5.3 |")
    print(f"| 2     | V3       | {v3_baseline['avg']:.1f}    | {v3_improved['avg']:.1f}   | {improvement:+.1f} |")

    total_from_v1 = v3_improved['avg'] - 2.0  # From original V2 baseline
    print(f"\nTotal improvement from V2 baseline: +{total_from_v1:.1f}")

    if improvement > 0:
        print("\n✓ EXPONENTIAL CONTINUES - each measurement improvement unlocks new strategy improvement")

    with open("exponential_cycle2_results.json", "w") as f:
        json.dump({
            "v2_current": v2_current,
            "v3_baseline": v3_baseline,
            "v3_improved": v3_improved,
            "improvement": improvement,
            "improved_strategy": improved
        }, f, indent=2, default=str)

    print("\nSaved to exponential_cycle2_results.json")


if __name__ == "__main__":
    run_cycle_2()
