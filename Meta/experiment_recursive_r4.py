#!/usr/bin/env python3
"""
Round 4: Can we beat three_words (9.0/9, complexity 13, efficiency 69.23)?
The prompt was: "Tension. Failure. Specifics."
Strategy: 2-word variants, 1-word variants, symbol-based
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

R3_WINNER = "Tension. Failure. Specifics."

R4_VARIATIONS = {
    "r3_winner": R3_WINNER,

    # 2-word variants (drop one element)
    "two_tf": "Tension. Failure.",
    "two_ts": "Tension. Specifics.",
    "two_fs": "Failure. Specifics.",

    # Different 2-word combos
    "two_tradeoff": "Tradeoff. Specifics.",
    "two_risk": "Risks. Solutions.",
    "two_problem": "Problem. Specific-solution.",

    # 1-word variants
    "one_specific": "Specifics.",
    "one_tradeoffs": "Tradeoffs.",
    "one_risks": "Risks.",

    # Ultra-compressed
    "symbols": "⚖️→❌→✓",  # balance, fail, check
    "acronym": "TFS",  # Tension Failure Specifics

    # Alternative 3-word
    "three_alt": "Tradeoff. Risk. Solution.",
    "three_verbs": "Balance. Prevent. Specify.",
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
        "prompt": prompt,
        "complexity": complexity,
        "avg_score": avg_total,
        "efficiency": avg_total / max(complexity["total"], 1) * 100,
        "scores": scores
    }

if __name__ == "__main__":
    print("="*70)
    print("ROUND 4: Can we beat three_words (9.0/9, eff 69.23)?")
    print("="*70)
    print(f"\nTesting {len(R4_VARIATIONS)} variations\n")

    results = []

    print("Testing: baseline...")
    baseline = test_methodology("baseline", "", PROBLEMS)
    results.append(baseline)
    print(f"  Score: {baseline['avg_score']:.1f}/9")

    for name, prompt in R4_VARIATIONS.items():
        print(f"Testing: {name}...")
        result = test_methodology(name, prompt, PROBLEMS)
        results.append(result)
        print(f"  Score: {result['avg_score']:.1f}/9, Cmplx: {result['complexity']['total']}, Eff: {result['efficiency']:.2f}")

    results.sort(key=lambda x: x['efficiency'], reverse=True)

    print(f"\n{'='*70}")
    print("ROUND 4 RESULTS")
    print(f"{'='*70}")
    print(f"{'Method':<20} {'Score':>7} {'Cmplx':>6} {'Eff':>10} Prompt")
    print("-" * 70)

    for r in results[:15]:  # Top 15
        eff_str = f"{r['efficiency']:.2f}" if r['complexity']['total'] > 0 else "N/A"
        prompt_preview = r.get('prompt', '')[:25] if r.get('prompt') else ''
        print(f"{r['name']:<20} {r['avg_score']:>7.1f} {r['complexity']['total']:>6} {eff_str:>10} {prompt_preview}")

    r3_winner = next(r for r in results if r['name'] == 'r3_winner')
    better = [r for r in results if r['efficiency'] > r3_winner['efficiency'] and r['name'] != 'baseline']

    print(f"\n{'='*70}")
    if better:
        best = better[0]
        print(f"NEW WINNER: {best['name']}")
        print(f"  Prompt: {best['prompt']}")
        print(f"  Score: {best['avg_score']:.1f}/9, Complexity: {best['complexity']['total']}")
        print(f"  Efficiency: {best['efficiency']:.2f} (was {r3_winner['efficiency']:.2f})")
        print(f"  Improvement: +{(best['efficiency'] - r3_winner['efficiency']) / r3_winner['efficiency'] * 100:.0f}%")
    else:
        print("R3 WINNER HOLDS - 'Tension. Failure. Specifics.' is optimal")
        print("This may be the efficient frontier.")

    with open("recursive_improvement_r4.json", "w") as f:
        json.dump({"results": results}, f, indent=2, default=str)
    print("\nSaved to recursive_improvement_r4.json")
