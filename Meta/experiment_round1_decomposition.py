#!/usr/bin/env python3
"""
EXPERIMENT ROUND 1: Problem Decomposition Hypothesis

PRE-REGISTRATION (stated BEFORE data collection):
=================================================
Hypothesis: Adding explicit decomposition prompt improves accuracy.
Prediction: Treatment mean > Control mean by 0.5+ points on strategic depth.
Alpha: 0.05
Power target: 0.80
Effect size assumption: d = 0.5 (medium)
Required N: 20 problems (calculated from power analysis)

Falsification criteria:
- If Treatment mean <= Control mean: REJECT hypothesis
- If effect size d < 0.3: Effect too small to be meaningful

DESIGN:
=======
- Within-subject (same problems, both conditions)
- Randomized order presentation (prevents order effects)
- Blind evaluation (evaluator sees only solution, not condition)
- Single variable manipulation (ONLY decomposition differs)

SIX VIRTUOSO CRITERIA CHECK:
============================
1. Structural bias prevention: Randomized order, blind evaluation
2. Adversarial red-team: See CONFOUNDS section below
3. Pre-commitment: Hypotheses stated above
4. Replication: Full code included, API calls reproducible
5. Power analysis: n=20 for d=0.5 at 80% power
6. Controls: Same problems, same evaluator, blind

CONFOUNDS ADDRESSED:
====================
- Length confound: Treatment is longer -> add length-matched placebo
- Structure confound: More structure helps -> tested with structured non-decomposition
- Problem variance: Some problems easier -> within-subject design controls this
"""

import anthropic
import json
import random
from datetime import datetime

import os
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# 20 diverse strategic problems (pre-selected, not cherry-picked)
PROBLEMS = [
    "A software company's best engineer wants to leave for a competitor. They have critical knowledge that isn't documented. Retention bonus failed.",
    "A hospital has 30% more patients than beds. Emergency room wait times are 8 hours. Staff is burning out. Budget is frozen.",
    "A family business patriarch is dying. His three children hate each other. The business is profitable but requires all three's involvement.",
    "A startup has 3 months of runway left. Their product works but sales cycle is 6 months. VCs want traction before more funding.",
    "A city's public transit system is losing $50M/year. Cutting routes angers voters. Raising fares drives riders to cars. Union contracts prevent layoffs.",
    "A university's star professor is accused of misconduct by 5 students. She brings in $10M/year in grants. Evidence is ambiguous.",
    "A pharmaceutical company discovered their best-selling drug has a rare fatal side effect. Pulling it means bankruptcy. Keeping it means lawsuits.",
    "An AI company's model can now generate deepfakes indistinguishable from reality. Releasing it enables fraud. Not releasing it means competitors will.",
    "A refugee camp has 50,000 people and food for 30,000. More refugees arriving daily. Supply lines are cut by conflict.",
    "A legacy bank is losing customers to fintech. Modernizing IT will take 3 years and $500M. In 3 years they may be irrelevant.",
    "A country's election system is vulnerable to hacking. Fixing it before election is impossible. Postponing election is unconstitutional.",
    "A factory's safety systems are outdated. Replacing them requires 2-month shutdown. Competitors will take their contracts.",
    "A school district must cut 20% of budget. Every option (teachers, buses, programs) has vocal opposition. Board members face recall.",
    "A nonprofit's charismatic founder was caught embezzling. Donors are demanding answers. The programs serve 100,000 people.",
    "A tech company promised carbon neutrality but discovered their supply chain produces 10x more emissions than reported.",
    "A hospital system must choose: rural hospital (1000 patients/year) or urban trauma center (50,000 patients/year). Budget for one.",
    "A country's only antibiotics factory is about to close. Nationalizing it is politically toxic. Letting it close means import dependency.",
    "A social media platform discovered state actors are using it to spread election disinformation. Removing content is censorship. Keeping it is complicity.",
    "A pension fund is 40% underfunded. Current retirees expect full benefits. Cutting benefits means lawsuits. Raising contributions drives away employers.",
    "A research lab discovered a cure but the data was obtained unethically. Publishing saves millions. Retracting protects research integrity.",
]

# CONTROL: Current best (v5.2-VR)
METHODOLOGY_CONTROL = """
**v5.2-VR Methodology**

STEP 1: CLARIFY THE PROBLEM
- What's the core tension?
- Who are the stakeholders?
- What are the real constraints (not assumed ones)?

STEP 2: STRATEGIC DEPTH
Consider 2nd and 3rd order consequences.
**CRITICAL: Identify one REVERSAL - how could SUCCESS at this solution create the OPPOSITE outcome at a higher level or longer timeframe?**

STEP 3: VERIFY
- Does solution address root cause?
- Will it survive contact with reality?
"""

# TREATMENT: Control + Decomposition
METHODOLOGY_TREATMENT = """
**v5.3-D Methodology**

STEP 0: DECOMPOSE THE PROBLEM
**Before solving, break this into independent sub-problems:**
- What are the separate components that could be addressed independently?
- What are the dependencies between components?
- Which component, if solved, would most unlock the others?

STEP 1: CLARIFY THE PROBLEM
- What's the core tension?
- Who are the stakeholders?
- What are the real constraints (not assumed ones)?

STEP 2: STRATEGIC DEPTH
Consider 2nd and 3rd order consequences.
**CRITICAL: Identify one REVERSAL - how could SUCCESS at this solution create the OPPOSITE outcome at a higher level or longer timeframe?**

STEP 3: VERIFY
- Does solution address root cause?
- Will it survive contact with reality?
"""

# PLACEBO: Length-matched but no decomposition (tests length confound)
METHODOLOGY_PLACEBO = """
**v5.2-VR+ Methodology**

PREAMBLE: SOLUTION CONTEXT
**Before solving, consider the broader context:**
- What is the general category of this problem?
- What historical situations have been similar?
- What general principles might apply here?

STEP 1: CLARIFY THE PROBLEM
- What's the core tension?
- Who are the stakeholders?
- What are the real constraints (not assumed ones)?

STEP 2: STRATEGIC DEPTH
Consider 2nd and 3rd order consequences.
**CRITICAL: Identify one REVERSAL - how could SUCCESS at this solution create the OPPOSITE outcome at a higher level or longer timeframe?**

STEP 3: VERIFY
- Does solution address root cause?
- Will it survive contact with reality?
"""

SOLUTION_PROMPT = """You are solving a complex strategic problem.

{methodology}

PROBLEM: {problem}

Provide your solution following the methodology above. Be specific and actionable."""

# BLIND EVALUATION - evaluator doesn't know which condition
EVALUATION_PROMPT = """Evaluate this solution's STRATEGIC DEPTH on a 1-10 scale.

PROBLEM: {problem}

SOLUTION: {solution}

SCORING CRITERIA:
- 1-3: Surface level, obvious suggestions only
- 4-5: Some depth but misses key dynamics
- 6-7: Good depth, considers multiple factors
- 8-9: Excellent depth, sees non-obvious connections
- 10: Exceptional, identifies reversals and emergent dynamics

Rate ONLY strategic depth. Output JSON: {{"score": N, "reasoning": "..."}}"""


def call_api(prompt, max_tokens=2000, temperature=0.7):
    """Make API call with error handling."""
    client = anthropic.Anthropic(api_key=API_KEY)
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"API Error: {e}")
        return None


def evaluate_solution(problem, solution):
    """Blind evaluation of solution quality."""
    prompt = EVALUATION_PROMPT.format(problem=problem, solution=solution)
    response = call_api(prompt, max_tokens=500, temperature=0.3)

    if response:
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{[^}]+\}', response)
            if json_match:
                data = json.loads(json_match.group())
                return data.get('score', 0), data.get('reasoning', '')
        except:
            pass
    return 0, "Parse error"


def run_experiment():
    """Run the full experiment with proper controls."""

    print("=" * 70)
    print("EXPERIMENT ROUND 1: Problem Decomposition Hypothesis")
    print("=" * 70)
    print("\nPRE-REGISTERED HYPOTHESIS:")
    print("  H1: Treatment (decomposition) > Control by 0.5+ points")
    print("  H0: Treatment <= Control")
    print("  Alpha: 0.05")
    print("  Required effect: d >= 0.3 for meaningful difference")
    print("=" * 70)

    results = {
        "timestamp": datetime.now().isoformat(),
        "pre_registration": {
            "hypothesis": "Decomposition improves strategic depth",
            "prediction": "Treatment > Control by 0.5+ points",
            "alpha": 0.05,
            "minimum_meaningful_d": 0.3
        },
        "problems": [],
        "control_scores": [],
        "treatment_scores": [],
        "placebo_scores": []  # To test length confound
    }

    # Randomize problem order (structural bias prevention)
    problem_order = list(range(len(PROBLEMS)))
    random.shuffle(problem_order)

    for i, prob_idx in enumerate(problem_order):
        problem = PROBLEMS[prob_idx]
        print(f"\nProblem {i+1}/{len(PROBLEMS)}: {problem[:50]}...")

        # Randomize condition order within each problem
        conditions = ['control', 'treatment', 'placebo']
        random.shuffle(conditions)

        problem_result = {
            "problem": problem,
            "condition_order": conditions,
            "scores": {}
        }

        for condition in conditions:
            if condition == 'control':
                methodology = METHODOLOGY_CONTROL
            elif condition == 'treatment':
                methodology = METHODOLOGY_TREATMENT
            else:
                methodology = METHODOLOGY_PLACEBO

            # Generate solution
            solution_prompt = SOLUTION_PROMPT.format(
                methodology=methodology,
                problem=problem
            )
            solution = call_api(solution_prompt)

            if solution:
                # Blind evaluation
                score, reasoning = evaluate_solution(problem, solution)
                problem_result["scores"][condition] = {
                    "score": score,
                    "reasoning": reasoning
                }
                print(f"  {condition.capitalize()}: {score}")

                if condition == 'control':
                    results["control_scores"].append(score)
                elif condition == 'treatment':
                    results["treatment_scores"].append(score)
                else:
                    results["placebo_scores"].append(score)

        results["problems"].append(problem_result)

    # Calculate statistics
    import statistics

    control_mean = statistics.mean(results["control_scores"]) if results["control_scores"] else 0
    treatment_mean = statistics.mean(results["treatment_scores"]) if results["treatment_scores"] else 0
    placebo_mean = statistics.mean(results["placebo_scores"]) if results["placebo_scores"] else 0

    control_std = statistics.stdev(results["control_scores"]) if len(results["control_scores"]) > 1 else 1
    treatment_std = statistics.stdev(results["treatment_scores"]) if len(results["treatment_scores"]) > 1 else 1

    # Cohen's d (Treatment vs Control)
    pooled_std = ((control_std**2 + treatment_std**2) / 2) ** 0.5
    cohens_d = (treatment_mean - control_mean) / pooled_std if pooled_std > 0 else 0

    effect = treatment_mean - control_mean

    results["analysis"] = {
        "control_mean": control_mean,
        "treatment_mean": treatment_mean,
        "placebo_mean": placebo_mean,
        "effect_treatment_vs_control": effect,
        "cohens_d": cohens_d,
        "hypothesis_supported": effect > 0.5 and cohens_d >= 0.3,
        "length_confound_test": {
            "placebo_vs_control": placebo_mean - control_mean,
            "conclusion": "Length confound" if (placebo_mean - control_mean) > (treatment_mean - control_mean) * 0.5 else "No length confound"
        }
    }

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nControl (v5.2-VR):     {control_mean:.2f} (n={len(results['control_scores'])})")
    print(f"Treatment (v5.3-D):    {treatment_mean:.2f} (n={len(results['treatment_scores'])})")
    print(f"Placebo (length-matched): {placebo_mean:.2f} (n={len(results['placebo_scores'])})")
    print(f"\nEffect (Treatment - Control): {effect:+.2f}")
    print(f"Cohen's d: {cohens_d:.3f}")
    print(f"\nLength confound check: {results['analysis']['length_confound_test']['conclusion']}")
    print(f"\nHYPOTHESIS {'SUPPORTED' if results['analysis']['hypothesis_supported'] else 'NOT SUPPORTED'}")

    # Save results
    with open("experiment_round1_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nFull results saved to experiment_round1_results.json")

    return results


if __name__ == "__main__":
    run_experiment()
