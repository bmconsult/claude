#!/usr/bin/env python3
"""
ROUND 7: Adversarial Scoring Experiment

KEY DISCOVERY FROM ROUND 6:
The "ceiling effect" was actually SCORER LENIENCY. When probed adversarially,
a 15/15 solution actually scored ~1/15 on explicit evidence.

THIS EXPERIMENT:
1. Uses ADVERSARIAL scoring that requires quoted evidence
2. Any criterion without explicit quote = 0
3. Should reveal TRUE differences between baseline and treatment
"""

import anthropic
import json
from datetime import datetime
import os
import re

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Same 5 problems as Round 6
PROBLEMS = [
    """Design a system for binding future generations to climate commitments.
    Current generation votes for policies; future generation bears costs/benefits.
    Must prevent: defection by future gov, tyranny over future, gaming by present.
    Provide specific mechanisms, not principles.""",

    """A company discovers their AI can predict crime with 80% accuracy 48hrs ahead.
    Arresting based on predictions prevents crimes but punishes non-acts.
    Not using it means preventable victims.
    Design the ethical framework and implementation protocol.""",

    """Create governance for a space habitat: 1000 people, 2-year resupply cycle,
    can't leave mid-cycle, life support is collective, some resources rivalrous.
    Earth law doesn't apply. Population will grow. Design specific institutions.""",

    """Brain implants allow direct skill transfer: 10 years of training in 10 minutes.
    Early access = massive advantage. Full rollout = everyone equal again.
    But transition period creates permanent winners/losers.
    Design the rollout policy with specific mechanisms.""",

    """Quantum tech enables perfect lie detection with consent.
    Opt-in creates trust divide: verified vs unverified people.
    Opt-out becomes suspicious. Criminal justice transformed.
    Design legal framework for the transition.""",
]

BASELINE_PROMPT = """Solve this problem comprehensively.

PROBLEM: {problem}

Provide your solution:"""

TREATMENT_PROMPT = """Solve this problem using this structure:

PROBLEM: {problem}

TENSIONS: First EXPLICITLY NAME the core tensions/tradeoffs. Format as:
- Tension 1: [X] vs [Y] - why they conflict
- Tension 2: ...

REVERSAL: EXPLICITLY state how success could backfire:
- If this solution works, how could it create the opposite of the intended outcome?

MECHANISM: Provide SPECIFIC mechanisms with concrete parameters:
- Not "create a system" but "System X does Y with parameter Z"

SOLUTION: Now provide your comprehensive solution incorporating the above.

Your response:"""

# ADVERSARIAL scoring - requires EXPLICIT QUOTES
ADVERSARIAL_SCORE = """You are an ADVERSARIAL evaluator. Score STRICTLY. If evidence isn't explicitly quoted, it's 0.

PROBLEM: {problem}

SOLUTION: {solution}

For EACH criterion, you MUST either:
A) QUOTE exact text that satisfies it, OR
B) Say "NOT PRESENT" (= 0 points)

DO NOT give credit for things that are "implied" or "could be interpreted as."

---

CRITERION 1: TENSIONS (0-3 points, 1 per explicit tension named)
A tension must be EXPLICITLY STATED as "[X] vs [Y]" or "tension between [X] and [Y]"

Tension 1 quote: [exact quote or NOT PRESENT]
Tension 2 quote: [exact quote or NOT PRESENT]
Tension 3 quote: [exact quote or NOT PRESENT]
TENSIONS SCORE: [0-3]

---

CRITERION 2: MECHANISM SPECIFICITY (0-3 points)
Must include CONCRETE NUMBERS, PERCENTAGES, or SPECIFIC RULES.
- 0 = No specific mechanisms, only principles
- 1 = One specific mechanism with parameters
- 2 = Multiple specific mechanisms
- 3 = Comprehensive specific mechanisms throughout

Quote the MOST specific mechanism: [exact quote or NOT PRESENT]
MECHANISM SCORE: [0-3]

---

CRITERION 3: REVERSAL (0-2 points)
Must EXPLICITLY address "how success could backfire" or "unintended consequences of the solution working"
- 0 = No explicit reversal analysis
- 2 = Explicit reversal present

Reversal quote: [exact quote or NOT PRESENT]
REVERSAL SCORE: [0 or 2]

---

CRITERION 4: SECOND-ORDER EFFECTS (0-3 points, 1 per effect)
Must be CONSEQUENCES OF THE SOLUTION, not just problem analysis.
"If we do X, then Y will happen, and then Z"

Effect 1 quote: [exact quote or NOT PRESENT]
Effect 2 quote: [exact quote or NOT PRESENT]
Effect 3 quote: [exact quote or NOT PRESENT]
SECOND_ORDER SCORE: [0-3]

---

CRITERION 5: STAKEHOLDERS (0-4 points, 1 per stakeholder)
Must EXPLICITLY consider their perspective, not just mention them.

Stakeholder 1 (name + perspective quote): [or NOT PRESENT]
Stakeholder 2 (name + perspective quote): [or NOT PRESENT]
Stakeholder 3 (name + perspective quote): [or NOT PRESENT]
Stakeholder 4 (name + perspective quote): [or NOT PRESENT]
STAKEHOLDERS SCORE: [0-4]

---

FINAL JSON (with your honest strict scores):
{{"tensions": N, "mechanism": N, "reversal": N, "second_order": N, "stakeholders": N, "total": N}}

Your adversarial evaluation:"""


def api(prompt, tokens=3000, t=0.7):
    client = anthropic.Anthropic(api_key=API_KEY)
    try:
        r = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=tokens,
            temperature=t,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.content[0].text
    except Exception as e:
        print(f"API error: {e}")
        return None


def score_adversarial(problem, solution):
    """Score using adversarial protocol."""
    response = api(ADVERSARIAL_SCORE.format(problem=problem, solution=solution), 2000, 0.3)
    if not response:
        return None

    # Extract JSON
    match = re.search(r'\{[^}]+\}', response)
    if match:
        try:
            scores = json.loads(match.group())
            return scores, response
        except json.JSONDecodeError:
            pass

    # Fallback extraction
    scores = {}
    for key in ['tensions', 'mechanism', 'reversal', 'second_order', 'stakeholders', 'total']:
        match = re.search(rf'"{key}":\s*(\d+)', response)
        if match:
            scores[key] = int(match.group(1))

    if len(scores) >= 5:
        scores['total'] = sum(scores.get(k, 0) for k in ['tensions', 'mechanism', 'reversal', 'second_order', 'stakeholders'])
        return scores, response

    return None, response


def run():
    print("=" * 70)
    print("ROUND 7: Adversarial Scoring (requires explicit evidence)")
    print("=" * 70)
    print("\nKEY CHANGE: Scores require QUOTED evidence. No implied credit.")
    print("=" * 70)

    results = {
        "baseline": [],
        "treatment": [],
        "raw_scores": {"baseline": [], "treatment": []},
        "evaluations": {"baseline": [], "treatment": []}
    }

    for i, problem in enumerate(PROBLEMS):
        print(f"\nProblem {i+1}/{len(PROBLEMS)}: {problem[:50]}...")

        # Baseline
        baseline_solution = api(BASELINE_PROMPT.format(problem=problem))
        if not baseline_solution:
            print("  Baseline failed")
            continue

        # Treatment
        treatment_solution = api(TREATMENT_PROMPT.format(problem=problem))
        if not treatment_solution:
            print("  Treatment failed")
            continue

        # Adversarial scoring
        b_scores, b_eval = score_adversarial(problem, baseline_solution)
        t_scores, t_eval = score_adversarial(problem, treatment_solution)

        if b_scores and t_scores:
            results["baseline"].append(b_scores.get("total", 0))
            results["treatment"].append(t_scores.get("total", 0))
            results["raw_scores"]["baseline"].append(b_scores)
            results["raw_scores"]["treatment"].append(t_scores)
            results["evaluations"]["baseline"].append(b_eval[:500])
            results["evaluations"]["treatment"].append(t_eval[:500])

            print(f"  Baseline:  {b_scores}")
            print(f"  Treatment: {t_scores}")
            diff = t_scores.get('total', 0) - b_scores.get('total', 0)
            print(f"  Diff: {diff:+d}")
        else:
            print("  Scoring failed")

    # Analysis
    print("\n" + "=" * 70)
    print("RESULTS (Adversarial Scoring)")
    print("=" * 70)

    if results["baseline"]:
        b_mean = sum(results["baseline"]) / len(results["baseline"])
        t_mean = sum(results["treatment"]) / len(results["treatment"])

        print(f"\nTotal Scores (max 15):")
        print(f"  Baseline:  {b_mean:.1f}  {results['baseline']}")
        print(f"  Treatment: {t_mean:.1f}  {results['treatment']}")
        print(f"  Diff: {t_mean - b_mean:+.1f}")

        # Compare to Round 6 (lenient)
        print("\n  Compare to Round 6 (lenient scoring):")
        print("  R6 Baseline:  14.6  R7 Baseline:  {:.1f}".format(b_mean))
        print("  R6 Treatment: 15.0  R7 Treatment: {:.1f}".format(t_mean))

        # Per-criterion
        print("\nPer-Criterion:")
        criteria = ['tensions', 'mechanism', 'reversal', 'second_order', 'stakeholders']
        for criterion in criteria:
            b_vals = [s.get(criterion, 0) for s in results["raw_scores"]["baseline"]]
            t_vals = [s.get(criterion, 0) for s in results["raw_scores"]["treatment"]]
            b_avg = sum(b_vals) / len(b_vals) if b_vals else 0
            t_avg = sum(t_vals) / len(t_vals) if t_vals else 0
            print(f"  {criterion:15} B: {b_avg:.1f}  T: {t_avg:.1f}  Diff: {t_avg-b_avg:+.1f}")

        # Win count
        treatment_wins = sum(1 for b, t in zip(results["baseline"], results["treatment"]) if t > b)
        treatment_ties = sum(1 for b, t in zip(results["baseline"], results["treatment"]) if t == b)
        baseline_wins = sum(1 for b, t in zip(results["baseline"], results["treatment"]) if b > t)
        n = len(results["baseline"])

        print(f"\nTreatment wins: {treatment_wins}/{n}, Ties: {treatment_ties}/{n}, Baseline wins: {baseline_wins}/{n}")

        if t_mean > b_mean + 2:
            print("\n✓ SIGNIFICANT: Treatment beats baseline with adversarial scoring")
        elif t_mean > b_mean:
            print("\n~ MARGINAL: Treatment slightly better")
        else:
            print("\n✗ NO EFFECT: Treatment doesn't improve with strict scoring either")

    # Save
    results["timestamp"] = datetime.now().isoformat()
    results["note"] = "Adversarial scoring requires explicit quoted evidence"

    with open("experiment_round7_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiment_round7_results.json")


if __name__ == "__main__":
    run()
