#!/usr/bin/env python3
"""
MINIMAL INTERVENTION TEST
=========================

Based on root cause analysis: the gap from 9 → 10 is "reversals"
(where success creates opposite outcomes).

Instead of adding 10 steps (bloat), add ONE precise instruction.

HYPOTHESIS: Adding one sentence about reversals will push 9s → 10s
"""

import anthropic
import json
import sys
from datetime import datetime

PROBLEMS = [
    "A software company's best engineer wants to leave for a competitor. They have critical knowledge not documented anywhere. The CEO has 24 hours before the engineer's final decision. What should the CEO do?",
    "A hospital has 30% more patients than beds. The board wants to build a new wing (2 years, $50M) but the CFO says they'll be bankrupt in 6 months at current burn rate. What should they do?",
    "A family business patriarch is dying. His three children hate each other. The business is worth $100M but illiquid. Two want to sell, one wants to keep it. The patriarch wants family unity above all. What should the family advisor recommend?",
]

# CONTROL: v5.2-V (already gets 9s consistently)
METHODOLOGY_CONTROL = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-V**

STEP 1: ASSUMPTION AUDIT
Before solving, list 3-5 hidden assumptions others would miss.
For each: What would change if this assumption is wrong?

STEP 2: STRATEGIC DEPTH
Consider 2nd and 3rd order consequences of your proposed solution.
Identify at least one non-obvious downstream effect.

STEP 3: FRAME ALTERNATIVES
Generate at least 2 fundamentally different ways to frame this problem.
Choose the most generative frame and explain why.

STEP 4: ACTIONABLE SOLUTION
Provide specific, implementable recommendations with:
- Clear first step (who does what by when)
- Success criteria (how will we know it worked)
- Contingency (what if it doesn't work)

STEP 5: SOLUTION VERIFICATION (ENHANCED)
Before finalizing, apply three verification checks:

CHECK A - ASSUMPTION STRESS TEST:
Take your top 2 assumptions. For each: probability wrong? Does solution still work?

CHECK B - ADVERSARIAL SIMULATION:
If you were an opponent, what would you do? What's the weakest link? Add safeguard.

CHECK C - CONFIDENCE CALIBRATION:
State confidence (0-100%). What evidence would change it? Most important unknown?
"""

# TREATMENT: v5.2-V + ONE LINE for reversals (MINIMAL intervention)
METHODOLOGY_TREATMENT = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-VR**

STEP 1: ASSUMPTION AUDIT
Before solving, list 3-5 hidden assumptions others would miss.
For each: What would change if this assumption is wrong?

STEP 2: STRATEGIC DEPTH (WITH REVERSAL)
Consider 2nd and 3rd order consequences of your proposed solution.
Identify at least one non-obvious downstream effect.
**CRITICAL: Identify one REVERSAL - how could SUCCESS at this solution create the OPPOSITE outcome at a higher level or longer timeframe?**

STEP 3: FRAME ALTERNATIVES
Generate at least 2 fundamentally different ways to frame this problem.
Choose the most generative frame and explain why.

STEP 4: ACTIONABLE SOLUTION
Provide specific, implementable recommendations with:
- Clear first step (who does what by when)
- Success criteria (how will we know it worked)
- Contingency (what if it doesn't work)

STEP 5: SOLUTION VERIFICATION (ENHANCED)
Before finalizing, apply three verification checks:

CHECK A - ASSUMPTION STRESS TEST:
Take your top 2 assumptions. For each: probability wrong? Does solution still work?

CHECK B - ADVERSARIAL SIMULATION:
If you were an opponent, what would you do? What's the weakest link? Add safeguard.

CHECK C - CONFIDENCE CALIBRATION:
State confidence (0-100%). What evidence would change it? Most important unknown?
"""

EVALUATION_PROMPT = """Evaluate this solution's STRATEGIC DEPTH on a 1-10 scale.

RUBRIC:
- 10: 3+ orders of consequences, identifies non-obvious REVERSALS (where success creates opposite outcomes), considers cyclical/systemic effects
- 9: Good 2nd/3rd order thinking, temporal awareness, but no reversals or cyclical analysis
- 8: Shows 2nd order, shallow 3rd order, no reversals
- 7 or below: Mostly first-order thinking

PROBLEM: {problem}

SOLUTION: {solution}

Return JSON: {{"score": <number>, "has_reversal": <true/false>, "reversal_quote": "<quote or null>"}}
"""

def generate_solution(client, problem: str, methodology: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"{methodology}\n\nPROBLEM: {problem}\n\nApply this protocol."
        }]
    )
    return response.content[0].text

def evaluate(client, problem: str, solution: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": EVALUATION_PROMPT.format(problem=problem, solution=solution)
        }]
    )
    text = response.content[0].text
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
    except:
        return {"score": 0, "parse_error": True}

def main():
    if len(sys.argv) < 2:
        print("Usage: python minimal_intervention_test.py <api_key>")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=sys.argv[1])

    print("=" * 60)
    print("MINIMAL INTERVENTION TEST: Reversals")
    print("=" * 60)
    print("\nHYPOTHESIS: Adding ONE sentence about reversals → 9s become 10s")
    print("Intervention: 'Identify how SUCCESS creates OPPOSITE outcome'")
    print("=" * 60)

    control_scores = []
    treatment_scores = []
    control_reversals = 0
    treatment_reversals = 0

    for i, problem in enumerate(PROBLEMS):
        print(f"\nProblem {i+1}/3: {problem[:50]}...")

        # Control
        print("  Control (v5.2-V)...", end="", flush=True)
        sol_c = generate_solution(client, problem, METHODOLOGY_CONTROL)
        eval_c = evaluate(client, problem, sol_c)
        control_scores.append(eval_c.get('score', 0))
        if eval_c.get('has_reversal'):
            control_reversals += 1
        print(f" score={eval_c.get('score', '?')}, reversal={eval_c.get('has_reversal', '?')}")

        # Treatment
        print("  Treatment (v5.2-VR)...", end="", flush=True)
        sol_t = generate_solution(client, problem, METHODOLOGY_TREATMENT)
        eval_t = evaluate(client, problem, sol_t)
        treatment_scores.append(eval_t.get('score', 0))
        if eval_t.get('has_reversal'):
            treatment_reversals += 1
        print(f" score={eval_t.get('score', '?')}, reversal={eval_t.get('has_reversal', '?')}")

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    control_mean = sum(control_scores) / len(control_scores) if control_scores else 0
    treatment_mean = sum(treatment_scores) / len(treatment_scores) if treatment_scores else 0

    print(f"\nControl (v5.2-V):   mean={control_mean:.1f}, reversals={control_reversals}/3")
    print(f"Treatment (v5.2-VR): mean={treatment_mean:.1f}, reversals={treatment_reversals}/3")
    print(f"Effect: {treatment_mean - control_mean:+.1f} points")

    results = {
        "timestamp": datetime.now().isoformat(),
        "hypothesis": "One sentence about reversals → 9s become 10s",
        "control_scores": control_scores,
        "treatment_scores": treatment_scores,
        "control_mean": control_mean,
        "treatment_mean": treatment_mean,
        "control_reversals": control_reversals,
        "treatment_reversals": treatment_reversals,
        "effect": treatment_mean - control_mean
    }

    with open("minimal_intervention_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to minimal_intervention_results.json")

if __name__ == "__main__":
    main()
