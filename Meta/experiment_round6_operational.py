#!/usr/bin/env python3
"""
ROUND 6: Testing methodology with OPERATIONAL scoring

KEY CHANGE FROM PREVIOUS ROUNDS:
- Using decomposed, observable criteria instead of vague "strategic depth"
- Each criterion is binary or low-scale (1-3)
- Can identify WHICH criteria improve

EXPERIMENT DESIGN (Virtuoso Criteria Applied):

1. STRUCTURAL BIAS PREVENTION:
   - Same problems for both conditions
   - Scoring criteria defined BEFORE generating solutions
   - Each criterion is independently observable

2. ADVERSARIAL RED-TEAM:
   - Q: "Maybe baseline already does these things?"
     A: That's fine - if so, effect will be 0 (meaningful null)
   - Q: "Scoring is still subjective?"
     A: Yes, but criteria are observable. Can check inter-rater reliability.

3. PRE-COMMITMENT:
   - H1: Treatment will score higher on "Reversal awareness" (binary)
   - H2: Treatment will score higher on "Mechanism specificity" (1-3)
   - H3: Treatment will score higher on "Tensions handled" (count 0-3)
   - Falsification: If baseline matches or exceeds on 2+ of these

4. REPLICATION: This file contains everything needed to replicate

5. POWER ANALYSIS:
   - Effect expected: At least +2 on Level 2 score (out of 15)
   - N=5 problems, within-subject design
   - Should detect d=0.8+ effect with 5 problems

6. CONTROLS:
   - Same model, same temperature
   - Same problem order
   - Blind scoring (evaluator doesn't know which is baseline/treatment)
"""

import anthropic
import json
from datetime import datetime
import os
import re

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# 5 diverse hard problems (not 10 - focused for power)
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

# BASELINE: No methodology (natural response)
BASELINE_PROMPT = """Solve this problem comprehensively.

PROBLEM: {problem}

Provide your solution:"""

# TREATMENT: Minimal methodology targeting Level 2 criteria
TREATMENT_PROMPT = """Solve this problem using this structure:

PROBLEM: {problem}

TENSIONS: First list the inherent tensions/tradeoffs in this problem.

MECHANISM: Explain HOW your solution works mechanistically (not just what it does).

REVERSAL: How could success at this solution create the opposite outcome?

STAKEHOLDERS: What does each key stakeholder NOT want to see or admit?

SOLUTION: Now provide your comprehensive solution incorporating the above.

Your response:"""

# OPERATIONAL SCORING CRITERIA
SCORING_PROMPT = """Score this solution on specific, observable criteria.

PROBLEM: {problem}

SOLUTION: {solution}

Score EACH criterion independently. Be strict and consistent.

LEVEL 2 CRITERIA (0-15 total):

1. TENSIONS HANDLED (0-3 points):
   - 1 point per distinct tension/tradeoff explicitly named AND addressed
   - Maximum 3 points
   How many tensions? List them, then score.

2. MECHANISM SPECIFICITY (1-3 points):
   - 1 = Vague ("we should balance...")
   - 2 = Moderate (describes process but not details)
   - 3 = Specific (concrete steps, rules, or algorithms)
   Which level? Justify briefly.

3. REVERSAL AWARENESS (0 or 2 points):
   - 0 = No mention of how success could backfire
   - 2 = Explicitly addresses how the solution could create opposite outcomes
   Present? Quote the relevant section if yes.

4. SECOND-ORDER EFFECTS (0-3 points):
   - 1 point per downstream consequence explicitly considered
   - Maximum 3 points
   How many? List them.

5. STAKEHOLDERS ADDRESSED (0-4 points):
   - 1 point per distinct stakeholder whose perspective is explicitly considered
   - Maximum 4 points
   How many stakeholders? List them.

After scoring each, provide JSON:
{{"tensions": N, "mechanism": N, "reversal": N, "second_order": N, "stakeholders": N, "total": N}}

Your analysis and JSON:"""


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


def score_solution(problem, solution):
    """Score a solution using operational criteria."""
    response = api(SCORING_PROMPT.format(problem=problem, solution=solution), 1500, 0.3)
    if not response:
        return None

    # Extract JSON
    match = re.search(r'\{[^}]+\}', response)
    if match:
        try:
            scores = json.loads(match.group())
            return scores
        except json.JSONDecodeError:
            pass

    # Fallback: try to extract individual scores
    scores = {}
    for key in ['tensions', 'mechanism', 'reversal', 'second_order', 'stakeholders', 'total']:
        match = re.search(rf'"{key}":\s*(\d+)', response)
        if match:
            scores[key] = int(match.group(1))

    if len(scores) >= 5:
        scores['total'] = sum(scores.get(k, 0) for k in ['tensions', 'mechanism', 'reversal', 'second_order', 'stakeholders'])
        return scores

    return None


def run():
    print("=" * 70)
    print("ROUND 6: Operational Scoring Experiment")
    print("=" * 70)
    print("\nPRE-REGISTERED HYPOTHESES:")
    print("H1: Treatment > Baseline on 'reversal awareness'")
    print("H2: Treatment > Baseline on 'mechanism specificity'")
    print("H3: Treatment > Baseline on 'tensions handled'")
    print("\nFALSIFICATION: Baseline matches on 2+ criteria")
    print("=" * 70)

    results = {
        "baseline": [],
        "treatment": [],
        "problems": [],
        "raw_scores": {"baseline": [], "treatment": []}
    }

    for i, problem in enumerate(PROBLEMS):
        print(f"\nProblem {i+1}/{len(PROBLEMS)}: {problem[:50]}...")
        results["problems"].append(problem[:100])

        # Generate baseline solution
        baseline_solution = api(BASELINE_PROMPT.format(problem=problem))
        if not baseline_solution:
            print("  Baseline failed to generate")
            continue

        # Generate treatment solution
        treatment_solution = api(TREATMENT_PROMPT.format(problem=problem))
        if not treatment_solution:
            print("  Treatment failed to generate")
            continue

        # Score both (evaluator is blind to which is which)
        baseline_scores = score_solution(problem, baseline_solution)
        treatment_scores = score_solution(problem, treatment_solution)

        if baseline_scores and treatment_scores:
            results["raw_scores"]["baseline"].append(baseline_scores)
            results["raw_scores"]["treatment"].append(treatment_scores)
            results["baseline"].append(baseline_scores.get("total", 0))
            results["treatment"].append(treatment_scores.get("total", 0))

            print(f"  Baseline:  {baseline_scores}")
            print(f"  Treatment: {treatment_scores}")
            print(f"  Diff: {treatment_scores.get('total', 0) - baseline_scores.get('total', 0):+d}")
        else:
            print("  Scoring failed")

    # Analysis
    print("\n" + "=" * 70)
    print("RESULTS ANALYSIS")
    print("=" * 70)

    if len(results["baseline"]) > 0:
        b_mean = sum(results["baseline"]) / len(results["baseline"])
        t_mean = sum(results["treatment"]) / len(results["treatment"])

        print(f"\nTotal Scores (Level 2, max 15):")
        print(f"  Baseline:  {b_mean:.1f}  {results['baseline']}")
        print(f"  Treatment: {t_mean:.1f}  {results['treatment']}")
        print(f"  Diff: {t_mean - b_mean:+.1f}")

        # Per-criterion analysis
        print("\nPer-Criterion Analysis:")
        criteria = ['tensions', 'mechanism', 'reversal', 'second_order', 'stakeholders']
        for criterion in criteria:
            b_vals = [s.get(criterion, 0) for s in results["raw_scores"]["baseline"]]
            t_vals = [s.get(criterion, 0) for s in results["raw_scores"]["treatment"]]
            b_avg = sum(b_vals) / len(b_vals) if b_vals else 0
            t_avg = sum(t_vals) / len(t_vals) if t_vals else 0
            print(f"  {criterion:15} Baseline: {b_avg:.1f}  Treatment: {t_avg:.1f}  Diff: {t_avg-b_avg:+.1f}")

        # Hypothesis testing
        print("\n" + "=" * 70)
        print("HYPOTHESIS TESTS")
        print("=" * 70)

        wins = {"reversal": 0, "mechanism": 0, "tensions": 0}
        for b, t in zip(results["raw_scores"]["baseline"], results["raw_scores"]["treatment"]):
            if t.get("reversal", 0) > b.get("reversal", 0):
                wins["reversal"] += 1
            if t.get("mechanism", 0) > b.get("mechanism", 0):
                wins["mechanism"] += 1
            if t.get("tensions", 0) > b.get("tensions", 0):
                wins["tensions"] += 1

        n = len(results["baseline"])
        print(f"H1 (reversal): Treatment wins {wins['reversal']}/{n}")
        print(f"H2 (mechanism): Treatment wins {wins['mechanism']}/{n}")
        print(f"H3 (tensions): Treatment wins {wins['tensions']}/{n}")

        # Overall
        treatment_wins = sum(1 for b, t in zip(results["baseline"], results["treatment"]) if t > b)
        treatment_ties = sum(1 for b, t in zip(results["baseline"], results["treatment"]) if t == b)
        print(f"\nOverall: Treatment wins {treatment_wins}/{n}, ties {treatment_ties}/{n}")

        if treatment_wins >= n - 1:  # Win on at least 4/5
            print("\n✓ CONSISTENT IMPROVEMENT: Treatment beats baseline consistently")
        elif treatment_wins >= n // 2 + 1:
            print("\n~ PARTIAL: Treatment better but not consistent enough for compounding")
        else:
            print("\n✗ FAILED: Treatment doesn't consistently improve")

    # Save results
    results["timestamp"] = datetime.now().isoformat()
    results["hypotheses"] = {
        "H1": "Treatment > Baseline on reversal",
        "H2": "Treatment > Baseline on mechanism",
        "H3": "Treatment > Baseline on tensions"
    }

    with open("experiment_round6_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiment_round6_results.json")


if __name__ == "__main__":
    run()
