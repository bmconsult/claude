#!/usr/bin/env python3
"""
Round 2: Can we beat combined_minimal (9.0/9, complexity 49, efficiency 18.37)?
Strategy: Test even simpler variants - drop instructions, different wordings
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
    "Create governance for a space habitat: 1000 people, 50-year journey, no Earth contact.",
]

# R1 winner - our baseline for R2
COMBINED_MINIMAL = """
1. Name the core tension
2. How could success backfire?
3. Be specific enough for a stranger to implement
"""

# R2 variations - can we do better with less?
R2_VARIATIONS = {
    "r1_winner": COMBINED_MINIMAL,

    # Drop one instruction at a time
    "tension_plus_specific": """
1. Name the core tension
2. Be specific enough for a stranger to implement
""",

    "tension_plus_reversal": """
1. Name the core tension
2. How could success backfire?
""",

    "reversal_plus_specific": """
1. How could success backfire?
2. Be specific enough for a stranger to implement
""",

    # Single instruction - ultra minimal
    "just_tension": "Name the core tension, then solve it.",

    "just_specific": "Be specific enough for a stranger to implement exactly.",

    "just_reversal": "Consider how success could backfire, then design against it.",

    # Rewordings - same idea, tighter
    "ultra_tight": """Core tension? Failure mode? Specific solution.""",

    "question_form": """
What's the tradeoff?
How could this fail?
What exactly would you do?
""",

    # Merged single instruction
    "all_in_one": "Name the core tension, address how success could backfire, and be specific enough that a stranger could implement exactly what you propose.",
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

Return JSON: {"tensions": N, "mechanism": N, "reversal": N, "total": N}
"""

def count_complexity(prompt):
    words = len(prompt.split())
    lines = [l.strip() for l in prompt.split('\n') if l.strip()]
    instructions = len([l for l in lines if l and (l[0].isdigit() or l[0] in '-*•?' or l[0].isupper())])
    return {"words": words, "instructions": max(instructions, 1), "total": words + instructions * 10}

def generate_solution(problem, methodology_prompt):
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
        if '{' in text:
            start = text.index('{')
            end = text.rindex('}') + 1
            return json.loads(text[start:end])
    except:
        pass
    return {"tensions": 0, "mechanism": 0, "reversal": 0, "total": 0}

def test_methodology(name, prompt, problems):
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
        "efficiency": avg_total / max(complexity["total"], 1) * 100,
        "scores": scores
    }

if __name__ == "__main__":
    print("="*70)
    print("ROUND 2: Can we beat combined_minimal (9.0/9, eff 18.37)?")
    print("="*70)
    print(f"\nTesting {len(R2_VARIATIONS)} variations on {len(PROBLEMS)} problems\n")

    results = []

    # Test baseline first
    print("Testing: baseline (no methodology)...")
    baseline = test_methodology("baseline", "", PROBLEMS)
    results.append(baseline)
    print(f"  Score: {baseline['avg_score']:.1f}/9")

    for name, prompt in R2_VARIATIONS.items():
        print(f"Testing: {name}...")
        result = test_methodology(name, prompt, PROBLEMS)
        results.append(result)
        effect = result['avg_score'] - baseline['avg_score']
        print(f"  Score: {result['avg_score']:.1f}/9, Complexity: {result['complexity']['total']}, Effect: {effect:+.1f}, Eff: {result['efficiency']:.2f}")

    # Sort by efficiency
    results.sort(key=lambda x: x['efficiency'], reverse=True)

    print(f"\n{'='*70}")
    print("ROUND 2 RESULTS (sorted by efficiency)")
    print(f"{'='*70}")
    print(f"{'Method':<25} {'Score':>7} {'Effect':>7} {'Cmplx':>6} {'Eff':>8}")
    print("-" * 60)

    baseline_score = baseline['avg_score']
    for r in results:
        effect = r['avg_score'] - baseline_score
        eff_str = f"{r['efficiency']:.2f}" if r['complexity']['total'] > 0 else "N/A"
        print(f"{r['name']:<25} {r['avg_score']:>7.1f} {effect:>+7.1f} {r['complexity']['total']:>6} {eff_str:>8}")

    # Find if anything beats R1 winner
    r1_winner = next(r for r in results if r['name'] == 'r1_winner')
    better = [r for r in results if r['efficiency'] > r1_winner['efficiency'] and r['name'] != 'baseline']

    print(f"\n{'='*70}")
    if better:
        print(f"NEW WINNER: {better[0]['name']}")
        print(f"  Score: {better[0]['avg_score']:.1f}/9")
        print(f"  Complexity: {better[0]['complexity']['total']}")
        print(f"  Efficiency: {better[0]['efficiency']:.2f} (was {r1_winner['efficiency']:.2f})")
        print(f"  Improvement: +{(better[0]['efficiency'] - r1_winner['efficiency']) / r1_winner['efficiency'] * 100:.0f}% efficiency")
    else:
        print("R1 WINNER HOLDS - combined_minimal is still best")
        print("Consider: We may have found the efficient frontier")

    with open("recursive_improvement_r2.json", "w") as f:
        json.dump({"results": results, "baseline": baseline}, f, indent=2, default=str)

    print("\nSaved to recursive_improvement_r2.json")
