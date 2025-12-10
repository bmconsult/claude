#!/usr/bin/env python3
"""
Round 3: Can we beat ultra_tight (9.0/9, complexity 16, efficiency 56.25)?
The prompt was: "Core tension? Failure mode? Specific solution."
Strategy: Even simpler variants, reorderings, compressions
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

# R2 winner - baseline for R3
ULTRA_TIGHT = """Core tension? Failure mode? Specific solution."""

# R3 variations - can we do even better?
R3_VARIATIONS = {
    "r2_winner": ULTRA_TIGHT,

    # Even shorter
    "minimal_3": "Tension? Failure? Solution?",

    "minimal_2_tf": "Tension? Then design against failure.",

    "minimal_2_ts": "Tension? Then specific solution.",

    "minimal_2_fs": "Failure mode? Specific solution.",

    # Reorderings
    "reorder_fts": "Failure mode? Tension? Solution?",

    "reorder_stf": "Solution? Tension? Failure mode?",

    # Different framings
    "adversarial_frame": "What could go wrong? Address it specifically.",

    "constraint_frame": "What must be balanced? How specifically?",

    "pre_mortem": "Assume this failed. Why? Now prevent it.",

    # Ultra compressed
    "three_words": "Tension. Failure. Specifics.",

    "imperative": "Name tension. Address failure. Be specific.",
}

ADVERSARIAL_SCORER = """You are an ADVERSARIAL evaluator. Score STRICTLY.

CRITERIA (score each 0-3):
1. TENSIONS: Does it explicitly name conflicting values/goals? (0=none, 3=core tension identified)
2. MECHANISM: Could a stranger implement this exactly? (0=vague, 3=specific parameters)
3. REVERSAL: Does it address how success could backfire? (0=no, 3=failure modes addressed)

For EACH criterion, QUOTE exact text or say "NOT PRESENT" (= 0).

Return JSON: {"tensions": N, "mechanism": N, "reversal": N, "total": N}
"""

def count_complexity(prompt):
    words = len(prompt.split())
    lines = [l.strip() for l in prompt.split('\n') if l.strip()]
    instructions = len([l for l in lines if l and (l[0].isdigit() or l[0] in '-*•?' or l[0].isupper())])
    return {"words": words, "instructions": max(instructions, 1), "total": words + instructions * 10}

def generate_solution(problem, methodology_prompt):
    full_prompt = f"{methodology_prompt}\n\nPROBLEM: {problem}" if methodology_prompt else f"PROBLEM: {problem}"
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

SOLUTION:
{solution}

Score (JSON only):"""

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
    print("ROUND 3: Can we beat ultra_tight (9.0/9, eff 56.25)?")
    print("="*70)
    print(f"\nTesting {len(R3_VARIATIONS)} variations\n")

    results = []

    print("Testing: baseline...")
    baseline = test_methodology("baseline", "", PROBLEMS)
    results.append(baseline)
    print(f"  Score: {baseline['avg_score']:.1f}/9")

    for name, prompt in R3_VARIATIONS.items():
        print(f"Testing: {name}...")
        result = test_methodology(name, prompt, PROBLEMS)
        results.append(result)
        effect = result['avg_score'] - baseline['avg_score']
        print(f"  Score: {result['avg_score']:.1f}/9, Cmplx: {result['complexity']['total']}, Eff: {result['efficiency']:.2f}")

    results.sort(key=lambda x: x['efficiency'], reverse=True)

    print(f"\n{'='*70}")
    print("ROUND 3 RESULTS")
    print(f"{'='*70}")
    print(f"{'Method':<25} {'Score':>7} {'Cmplx':>6} {'Eff':>10}")
    print("-" * 55)

    for r in results:
        eff_str = f"{r['efficiency']:.2f}" if r['complexity']['total'] > 0 else "N/A"
        print(f"{r['name']:<25} {r['avg_score']:>7.1f} {r['complexity']['total']:>6} {eff_str:>10}")

    r2_winner = next(r for r in results if r['name'] == 'r2_winner')
    better = [r for r in results if r['efficiency'] > r2_winner['efficiency'] and r['name'] != 'baseline']

    print(f"\n{'='*70}")
    if better:
        best = better[0]
        print(f"NEW WINNER: {best['name']}")
        print(f"  Score: {best['avg_score']:.1f}/9, Complexity: {best['complexity']['total']}")
        print(f"  Efficiency: {best['efficiency']:.2f} (was {r2_winner['efficiency']:.2f})")
        print(f"  Improvement: +{(best['efficiency'] - r2_winner['efficiency']) / r2_winner['efficiency'] * 100:.0f}%")
    else:
        print("R2 WINNER HOLDS - ultra_tight is still best")
        # Check if any achieved same score with same/lower complexity
        same_score = [r for r in results if r['avg_score'] >= r2_winner['avg_score'] and r['complexity']['total'] <= r2_winner['complexity']['total'] and r['name'] not in ['r2_winner', 'baseline']]
        if same_score:
            print(f"BUT: {same_score[0]['name']} matches with same/less complexity")

    with open("recursive_improvement_r3.json", "w") as f:
        json.dump({"results": results}, f, indent=2, default=str)
    print("\nSaved to recursive_improvement_r3.json")
