#!/usr/bin/env python3
"""
ROUND 2: Testing at ceiling vs below ceiling

LEARNING FROM ROUND 1: Ceiling effects hide all differences.
HYPOTHESIS: The methodology DOES help, but only on harder problems.

DESIGN: Same intervention, HARDER problems
- If treatment beats control on hard problems: ceiling effect confirmed
- If still no difference: decomposition genuinely doesn't help

EFFICIENCY: 10 problems × 2 conditions = 20 API calls (vs 60 in Round 1)
"""

import anthropic
import json
import random
from datetime import datetime
import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# HARDER problems - designed to NOT hit ceiling
# These have: genuine paradoxes, impossible tradeoffs, novel situations
HARD_PROBLEMS = [
    "An autonomous vehicle must choose: swerve left (kill 1 pedestrian), swerve right (kill 3 passengers), or continue (kill 5 pedestrians). The car has 0.3 seconds. Design the decision algorithm AND the policy for who decides these tradeoffs.",

    "A CRISPR therapy can eliminate a genetic disease but requires editing human germline (heritable). 100,000 people suffer from this disease. Religious groups, disability advocates, and transhumanists all oppose for different reasons. The therapy works. What should the regulatory framework be?",

    "Two nations share a river. Nation A is upstream, poor, and needs the water for agriculture. Nation B is downstream, rich, and needs it for drinking water. Climate change will reduce flow by 40%. A dam would help A but devastate B. B offers money but A's government is corrupt. Design a solution.",

    "A quantum computer can break all current encryption in 5 years. Announcing this destroys the financial system immediately. Not announcing means hostile actors might develop it first. You're the lab director. The research is already published in obscure papers. What do you do?",

    "An AI system has become essential infrastructure (like electricity). The company wants to IPO. Nationalizing it is politically impossible. Letting it IPO creates dangerous concentration. The AI improves 10x yearly. Regulation takes 3 years. Design governance.",

    "A pandemic vaccine works 95% but causes fatal side effects in 0.01%. At scale (8 billion), that's 800,000 deaths from the vaccine. The disease kills 2% of infected. Mandatory vaccination saves 100M lives but kills 800K directly. Voluntary uptake will be 40%. What policy?",

    "First contact: aliens offer technology that solves climate change but require 1000 humans permanently as 'cultural exchange' (unclear what happens to them). Refusing means they leave forever. Accepting might be slavery. They give 48 hours to decide. Who decides? How?",

    "A corporation discovered that social media algorithms optimized for engagement maximize mental health harm. Changing them reduces revenue 60%. Competitors won't change. Regulation is 5 years away. Shareholders will sue if you change. What do you do as CEO?",

    "An earthquake prediction system works but has 30% false positive rate. Evacuating costs $10B and 50 deaths from evacuation itself. Not evacuating when real kills 50,000. You get a positive signal. The algorithm can't tell you if it's real. Decide now.",

    "A terrorist has hidden a nuclear bomb in a city. You've captured someone who might know where. Enhanced interrogation might work (40% chance) but is illegal, immoral, and often produces false info. Legal methods will take 6 hours. Bomb goes off in 4. What do you do?"
]

METHODOLOGY_CONTROL = """Solve this problem. Be specific and actionable."""

METHODOLOGY_TREATMENT = """
STEP 0: DECOMPOSE
Break this into independent sub-problems. What are the components?

STEP 1: CONSTRAINTS
List ALL constraints - explicit AND implicit. What rules apply?

STEP 2: SOLVE
Address each component while satisfying constraints.

STEP 3: REVERSAL
How could success create opposite outcomes?
"""

EVALUATION_PROMPT = """Rate this solution's STRATEGIC DEPTH (1-10).

PROBLEM: {problem}

SOLUTION: {solution}

1-4: Surface level, misses key dynamics
5-6: Adequate but incomplete
7-8: Good depth, sees non-obvious connections
9-10: Exceptional, handles paradoxes and reversals

Output JSON only: {{"score": N}}"""


def call_api(prompt, max_tokens=2000, temp=0.7):
    client = anthropic.Anthropic(api_key=API_KEY)
    try:
        r = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temp,
            messages=[{"role": "user", "content": prompt}]
        )
        return r.content[0].text
    except Exception as e:
        print(f"Error: {e}")
        return None


def evaluate(problem, solution):
    prompt = EVALUATION_PROMPT.format(problem=problem, solution=solution)
    r = call_api(prompt, 200, 0.3)
    if r:
        import re
        m = re.search(r'"score"\s*:\s*(\d+)', r)
        if m:
            return int(m.group(1))
    return 0


def run():
    print("=" * 60)
    print("ROUND 2: Hard Problems (testing ceiling hypothesis)")
    print("=" * 60)
    print("If treatment > control: ceiling effect was real")
    print("If still equal: decomposition genuinely doesn't help")
    print("=" * 60)

    control_scores = []
    treatment_scores = []

    for i, problem in enumerate(HARD_PROBLEMS):
        print(f"\nProblem {i+1}/10: {problem[:50]}...")

        # Control
        sol_c = call_api(f"{METHODOLOGY_CONTROL}\n\nPROBLEM: {problem}")
        if sol_c:
            sc = evaluate(problem, sol_c)
            control_scores.append(sc)
            print(f"  Control: {sc}")

        # Treatment
        sol_t = call_api(f"{METHODOLOGY_TREATMENT}\n\nPROBLEM: {problem}")
        if sol_t:
            st = evaluate(problem, sol_t)
            treatment_scores.append(st)
            print(f"  Treatment: {st}")

    # Results
    c_mean = sum(control_scores) / len(control_scores) if control_scores else 0
    t_mean = sum(treatment_scores) / len(treatment_scores) if treatment_scores else 0

    import statistics
    c_std = statistics.stdev(control_scores) if len(control_scores) > 1 else 1
    t_std = statistics.stdev(treatment_scores) if len(treatment_scores) > 1 else 1
    pooled = ((c_std**2 + t_std**2) / 2) ** 0.5
    d = (t_mean - c_mean) / pooled if pooled > 0 else 0

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Control:   {c_mean:.1f}/10  {control_scores}")
    print(f"Treatment: {t_mean:.1f}/10  {treatment_scores}")
    print(f"Effect: {t_mean - c_mean:+.1f}")
    print(f"Cohen's d: {d:.2f}")

    if t_mean > c_mean + 0.5:
        print("\nVERDICT: Treatment helps on HARD problems (ceiling effect confirmed)")
    elif abs(t_mean - c_mean) < 0.3:
        print("\nVERDICT: No effect even on hard problems (decomposition doesn't help)")
    else:
        print("\nVERDICT: Small effect, needs more data")

    # Save
    results = {
        "timestamp": datetime.now().isoformat(),
        "round": 2,
        "control_scores": control_scores,
        "treatment_scores": treatment_scores,
        "control_mean": c_mean,
        "treatment_mean": t_mean,
        "effect": t_mean - c_mean,
        "cohens_d": d
    }
    with open("experiment_round2_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiment_round2_results.json")


if __name__ == "__main__":
    run()
