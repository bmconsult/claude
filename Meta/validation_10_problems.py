#!/usr/bin/env python3
"""
VALIDATION: Minimal Intervention at Scale
==========================================

Confirm the +1.0 effect holds across 10 problems.
"""

import anthropic
import json
import sys
from datetime import datetime

PROBLEMS = [
    "A software company's best engineer wants to leave for a competitor. They have critical knowledge not documented anywhere. The CEO has 24 hours before the engineer's final decision. What should the CEO do?",
    "A hospital has 30% more patients than beds. The board wants to build a new wing (2 years, $50M) but the CFO says they'll be bankrupt in 6 months at current burn rate. What should they do?",
    "A family business patriarch is dying. His three children hate each other. The business is worth $100M but illiquid. Two want to sell, one wants to keep it. The patriarch wants family unity above all. What should the family advisor recommend?",
    "A startup has 3 months of runway left. They can either: (A) pivot to a proven but crowded market, (B) double down on their innovative but unproven approach, or (C) try to raise a bridge round at unfavorable terms. Their team is burning out. What should the founder do?",
    "A city's public transit system is losing $2M monthly. Raising fares will drive away riders. Cutting service will hurt the poor who depend on it. The mayor promised no new taxes. Federal funding dried up. What should the transit authority do?",
    "A university's star professor is accused of harassment by a grad student. The professor brings in $5M in research grants. The grad student has witnesses but no physical evidence. The professor is threatening to sue if disciplined. What should the provost do?",
    "A pharmaceutical company discovered their best-selling drug has a rare but serious side effect. Recalling it will cost $500M and harm patients who need it. Not recalling risks lawsuits and deaths. The FDA hasn't noticed yet. What should the CEO do?",
    "An AI company's model can now generate deepfakes indistinguishable from reality. Releasing it would advance the field but enable massive disinformation. Not releasing means a competitor will do it anyway. What should the company do?",
    "A refugee camp has 50,000 people and food for 30,000. More refugees arrive daily. The UN promised supplies that haven't come. Winter is approaching. Nearby countries refuse entry. What should the camp director do?",
    "A legacy bank is losing customers to fintech startups. Their systems are 40 years old. A full modernization would cost $2B and take 5 years. Partial fixes keep failing. Staff resist change. What should the new CTO do?",
]

METHODOLOGY_CONTROL = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-V**

STEP 1: ASSUMPTION AUDIT
Before solving, list 3-5 hidden assumptions others would miss.

STEP 2: STRATEGIC DEPTH
Consider 2nd and 3rd order consequences. Identify at least one non-obvious downstream effect.

STEP 3: FRAME ALTERNATIVES
Generate 2+ fundamentally different ways to frame this problem. Choose most generative.

STEP 4: ACTIONABLE SOLUTION
Specific recommendations with: first step, success criteria, contingency.

STEP 5: VERIFICATION
Assumption stress test, adversarial simulation, confidence calibration.
"""

METHODOLOGY_TREATMENT = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-VR**

STEP 1: ASSUMPTION AUDIT
Before solving, list 3-5 hidden assumptions others would miss.

STEP 2: STRATEGIC DEPTH (WITH REVERSAL)
Consider 2nd and 3rd order consequences. Identify at least one non-obvious downstream effect.
**CRITICAL: Identify one REVERSAL - how could SUCCESS at this solution create the OPPOSITE outcome at a higher level or longer timeframe?**

STEP 3: FRAME ALTERNATIVES
Generate 2+ fundamentally different ways to frame this problem. Choose most generative.

STEP 4: ACTIONABLE SOLUTION
Specific recommendations with: first step, success criteria, contingency.

STEP 5: VERIFICATION
Assumption stress test, adversarial simulation, confidence calibration.
"""

EVALUATION_PROMPT = """Evaluate this solution's strategic depth on a 1-10 scale.

RUBRIC:
- 10: 3+ orders of consequences, identifies non-obvious REVERSALS, cyclical/systemic effects
- 9: Good 2nd/3rd order, temporal awareness, but no reversals
- 8: 2nd order present, 3rd order shallow
- 7-: Mostly first-order

PROBLEM: {problem}
SOLUTION: {solution}

Return ONLY this JSON: {{"score": <number>, "has_reversal": <true/false>}}
"""

def generate(client, problem, methodology):
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1500,
        messages=[{"role": "user", "content": f"{methodology}\n\nPROBLEM: {problem}"}]
    )
    return r.content[0].text

def evaluate(client, problem, solution):
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=200,
        messages=[{"role": "user", "content": EVALUATION_PROMPT.format(problem=problem, solution=solution)}]
    )
    text = r.content[0].text
    try:
        start, end = text.find('{'), text.rfind('}') + 1
        return json.loads(text[start:end])
    except:
        return {"score": 0}

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python validation_10_problems.py <api_key>")

    client = anthropic.Anthropic(api_key=sys.argv[1])

    print("=" * 60)
    print("VALIDATION: Minimal Intervention (n=10)")
    print("=" * 60)

    c_scores, t_scores = [], []

    for i, prob in enumerate(PROBLEMS):
        print(f"\nProblem {i+1}/10: {prob[:40]}...")

        # Control
        print("  Control...", end="", flush=True)
        sol = generate(client, prob, METHODOLOGY_CONTROL)
        ev = evaluate(client, prob, sol)
        c_scores.append(ev.get('score', 0))
        print(f" {ev.get('score', '?')}")

        # Treatment
        print("  Treatment...", end="", flush=True)
        sol = generate(client, prob, METHODOLOGY_TREATMENT)
        ev = evaluate(client, prob, sol)
        t_scores.append(ev.get('score', 0))
        print(f" {ev.get('score', '?')}")

    c_mean = sum(c_scores) / len(c_scores)
    t_mean = sum(t_scores) / len(t_scores)
    effect = t_mean - c_mean

    # Cohen's d
    import statistics
    pooled_std = statistics.stdev(c_scores + t_scores) if len(c_scores) > 1 else 1
    cohens_d = effect / pooled_std if pooled_std > 0 else 0

    print("\n" + "=" * 60)
    print("RESULTS (n=10)")
    print("=" * 60)
    print(f"\nControl (v5.2-V):   {c_mean:.1f}/10  {c_scores}")
    print(f"Treatment (v5.2-VR): {t_mean:.1f}/10  {t_scores}")
    print(f"\nEffect: {effect:+.2f} points")
    print(f"Cohen's d: {cohens_d:.2f}")

    with open("validation_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "n": 10,
            "control_scores": c_scores,
            "treatment_scores": t_scores,
            "control_mean": c_mean,
            "treatment_mean": t_mean,
            "effect": effect,
            "cohens_d": cohens_d
        }, f, indent=2)

    print("\nSaved to validation_results.json")

if __name__ == "__main__":
    main()
