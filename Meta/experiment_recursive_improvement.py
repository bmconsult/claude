#!/usr/bin/env python3
"""
Recursive Methodology Improvement Experiment

Goal: Find the SIMPLEST methodology that achieves MAXIMUM effect.
Each round should improve the efficiency ratio (effect/complexity), not just add more.

Metrics:
- Effect Size: (Treatment - Baseline) on adversarial scoring
- Complexity: Word count + instruction count
- Efficiency: Effect Size / Complexity
"""

import anthropic
import json
import time
from datetime import datetime

client = anthropic.Anthropic()

# Hard problems for testing
PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
    "Create governance for a space habitat: 1000 people, 50-year journey, no Earth contact.",
]

# Current v2 methodology (our baseline for improvement)
V2_METHODOLOGY = """
TENSIONS: Name [X] vs [Y] conflicts explicitly

REVERSAL: How could success backfire?
Rate probability (Low/Med/High).

STAKEHOLDERS: What does each party want / not want?
Rate influence (1-5).

MECHANISM: Specific parameters that pass "stranger test"
(Could someone unfamiliar implement exactly as written?)
"""

# Variations to test - some simpler, some different
VARIATIONS = {
    "v2_full": V2_METHODOLOGY,

    "minimal_tensions": """
Name the core tension. What tradeoff defines this problem?
Then solve it.
""",

    "minimal_reversal": """
How could your solution backfire?
Design against that failure mode.
""",

    "minimal_mechanism": """
Be specific enough that a stranger could implement your solution exactly.
No vague recommendations.
""",

    "combined_minimal": """
1. Name the core tension
2. How could success backfire?
3. Be specific enough for a stranger to implement
""",

    "just_adversarial": """
Assume a hostile critic will attack your solution.
What would they say? Address it preemptively.
""",

    "constraint_first": """
List the constraints that MUST be satisfied.
Your solution must satisfy ALL of them explicitly.
""",
}

ADVERSARIAL_SCORER = """You are an ADVERSARIAL evaluator. Score STRICTLY.

CRITERIA (score each 0-3):
1. TENSIONS: Does it explicitly name conflicting values/goals? (0=none named, 3=core tension identified and addressed)
2. MECHANISM: Could a stranger implement this exactly? (0=vague, 3=specific parameters)
3. REVERSAL: Does it address how success could backfire? (0=no, 3=specific failure modes addressed)

For EACH criterion, you MUST either:
A) QUOTE exact text that satisfies it, OR
B) Say "NOT PRESENT" (= 0 points)

DO NOT give credit for things that are "implied."

Return JSON: {"tensions": N, "mechanism": N, "reversal": N, "total": N, "quotes": {...}}
"""

def count_complexity(prompt):
    """Count words and distinct instructions"""
    words = len(prompt.split())
    # Count lines that look like instructions (numbered, bulleted, or imperative)
    lines = [l.strip() for l in prompt.split('\n') if l.strip()]
    instructions = len([l for l in lines if l and (l[0].isdigit() or l[0] in '-*•' or l[0].isupper())])
    return {"words": words, "instructions": max(instructions, 1), "total": words + instructions * 10}

def generate_solution(problem, methodology_prompt):
    """Generate a solution using given methodology"""
    if methodology_prompt:
        full_prompt = f"{methodology_prompt}\n\nPROBLEM: {problem}\n\nSOLUTION:"
    else:
        full_prompt = f"PROBLEM: {problem}\n\nSOLUTION:"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.content[0].text

def score_solution(problem, solution):
    """Score using adversarial evaluation"""
    prompt = f"""{ADVERSARIAL_SCORER}

PROBLEM: {problem}

SOLUTION TO SCORE:
{solution}

Score now (JSON only):"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    try:
        # Extract JSON
        if '{' in text:
            start = text.index('{')
            end = text.rindex('}') + 1
            return json.loads(text[start:end])
    except:
        pass
    return {"tensions": 0, "mechanism": 0, "reversal": 0, "total": 0}

def test_methodology(name, prompt, problems):
    """Test a methodology variant"""
    complexity = count_complexity(prompt) if prompt else {"words": 0, "instructions": 0, "total": 0}
    scores = []

    for problem in problems:
        solution = generate_solution(problem, prompt)
        score = score_solution(problem, solution)
        scores.append(score)
        time.sleep(0.5)

    avg_total = sum(s.get('total', 0) for s in scores) / len(scores)

    return {
        "name": name,
        "complexity": complexity,
        "avg_score": avg_total,
        "max_possible": 9,
        "efficiency": avg_total / max(complexity["total"], 1) * 100,  # Normalize
        "scores": scores
    }

def run_recursive_round(variations, problems, round_num):
    """Run one round of testing all variations"""
    print(f"\n{'='*70}")
    print(f"ROUND {round_num}: Testing {len(variations)} methodology variations")
    print(f"{'='*70}\n")

    results = []

    # Always test baseline (no methodology)
    print("Testing: baseline (no methodology)...")
    baseline = test_methodology("baseline", "", problems)
    results.append(baseline)
    print(f"  Score: {baseline['avg_score']:.1f}/9, Complexity: 0, Efficiency: N/A")

    for name, prompt in variations.items():
        print(f"Testing: {name}...")
        result = test_methodology(name, prompt, problems)
        results.append(result)
        effect = result['avg_score'] - baseline['avg_score']
        print(f"  Score: {result['avg_score']:.1f}/9, Complexity: {result['complexity']['total']}, Effect: {effect:+.1f}, Efficiency: {result['efficiency']:.2f}")

    # Sort by efficiency (effect per complexity unit)
    # But only consider those that actually improve over baseline
    effective = [r for r in results if r['avg_score'] > baseline['avg_score']]
    effective.sort(key=lambda x: x['efficiency'], reverse=True)

    print(f"\n{'='*70}")
    print("ROUND RESULTS (sorted by efficiency)")
    print(f"{'='*70}")
    print(f"{'Method':<20} {'Score':>8} {'Effect':>8} {'Complex':>8} {'Efficiency':>10}")
    print("-" * 60)

    for r in sorted(results, key=lambda x: x['efficiency'], reverse=True):
        effect = r['avg_score'] - baseline['avg_score']
        eff_str = f"{r['efficiency']:.2f}" if r['complexity']['total'] > 0 else "N/A"
        print(f"{r['name']:<20} {r['avg_score']:>8.1f} {effect:>+8.1f} {r['complexity']['total']:>8} {eff_str:>10}")

    return {
        "round": round_num,
        "baseline": baseline,
        "results": results,
        "best_efficiency": effective[0] if effective else None,
        "best_score": max(results, key=lambda x: x['avg_score'])
    }

if __name__ == "__main__":
    print("RECURSIVE METHODOLOGY IMPROVEMENT")
    print("Goal: Maximize (Effect Size / Complexity)")
    print(f"Testing on {len(PROBLEMS)} problems\n")

    round1 = run_recursive_round(VARIATIONS, PROBLEMS, 1)

    # Save results
    with open("recursive_improvement_r1.json", "w") as f:
        json.dump(round1, f, indent=2, default=str)

    print(f"\n{'='*70}")
    print("INSIGHTS FOR NEXT ROUND")
    print(f"{'='*70}")

    if round1['best_efficiency']:
        best = round1['best_efficiency']
        print(f"Most efficient: {best['name']}")
        print(f"  Score: {best['avg_score']:.1f}/9")
        print(f"  Complexity: {best['complexity']['total']}")
        print(f"  Efficiency: {best['efficiency']:.2f}")
        print(f"\nNext round should: Combine best elements, test even simpler variants")

    print("\nSaved to recursive_improvement_r1.json")
