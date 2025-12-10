#!/usr/bin/env python3
"""
TRUE EXPONENTIAL V2: Bootstrap on solvable problems first

Key fix: Start with problems that CAN be solved, measure improvement,
then escalate difficulty as method gets better.

The method must prove it can improve before we trust it to improve itself.
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# Starting method - simple
METHOD_V1 = """
PROBLEM-SOLVING METHOD:

1. UNDERSTAND: What's the actual problem? What does success look like?
2. CONSTRAINTS: What must be true? What can't we change?
3. GENERATE: 3 different approaches, including one unconventional
4. EVALUATE: For each - main failure mode? What assumption might be wrong?
5. SELECT: Pick best, explicitly address top failure mode
6. VERIFY: Does it solve the original problem? Test against constraints.
"""

# Problems that are SOLVABLE but require good thinking
# Scored on specificity, completeness, and addressing edge cases
PROBLEMS = [
    {
        "level": 1,
        "problem": "Design a system for a 4-person household to fairly share one car.",
        "criteria": "Specific scheduling, handles conflicts, handles emergencies, handles unequal needs"
    },
    {
        "level": 2,
        "problem": "Design a peer review system for a small company (20 people) that's fair and useful.",
        "criteria": "Reduces bias, produces actionable feedback, doesn't create perverse incentives, handles conflicts of interest"
    },
    {
        "level": 3,
        "problem": "Design a system for a city to allocate limited parking permits fairly.",
        "criteria": "Handles competing legitimate needs, prevents gaming, balances efficiency and equity, has enforcement"
    },
    {
        "level": 4,
        "problem": "Design a system for allocating scarce medical resources (like organs) that balances urgency, likelihood of success, and fairness.",
        "criteria": "Explicit tradeoffs stated, handles edge cases, prevents gaming, addresses the hard ethical tensions directly"
    },
    {
        "level": 5,
        "problem": "Design a system that allows a democratic society to make long-term commitments (50+ years) while remaining democratically accountable.",
        "criteria": "Actually addresses the tension between commitment and accountability, doesn't just punt to 'balance', has concrete mechanisms"
    }
]

def apply_method(method: str, problem: str) -> str:
    """Use method to solve problem."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        temperature=0.3,
        messages=[{"role": "user", "content": f"{method}\n\nApply this method:\n{problem}"}]
    )
    return r.content[0].text

def evaluate(problem: str, criteria: str, solution: str) -> tuple:
    """Score solution 0-10 with specific feedback."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        temperature=0,
        messages=[{"role": "user", "content": f"""
PROBLEM: {problem}
CRITERIA: {criteria}
SOLUTION: {solution}

Score 0-10. Be specific about what's missing.
Give partial credit for partial solutions.

JSON: {{"score": N, "missing": "what's not addressed"}}
"""}]
    )
    try:
        t = r.content[0].text
        if '{' in t:
            d = json.loads(t[t.index('{'):t.rindex('}')+1])
            return d.get("score", 0), d.get("missing", "unknown")
    except:
        pass
    return 0, "eval failed"

def improve_method(method: str, problem: str, solution: str, score: int, missing: str) -> str:
    """Use the method to improve itself based on what's missing."""
    meta_problem = f"""
A problem-solving method produced this result:

PROBLEM: {problem}
SOLUTION SCORE: {score}/10
WHAT'S MISSING: {missing}

The current method is:
{method}

TASK: Improve the method so it would NOT miss what was missed.
Be specific. Add a step, modify a step, or add a check.
Keep the method roughly the same length - don't bloat.
Output ONLY the improved method.
"""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": f"{method}\n\nApply this method to solve:\n{meta_problem}"}]
    )
    return r.content[0].text

def run():
    print("="*70)
    print("TRUE EXPONENTIAL V2: BOOTSTRAP ON SOLVABLE PROBLEMS")
    print("="*70)

    method = METHOD_V1
    history = []
    current_level = 1

    for cycle in range(1, 11):
        # Select problem at current difficulty
        prob = next((p for p in PROBLEMS if p["level"] == current_level), PROBLEMS[-1])

        print(f"\n{'='*60}")
        print(f"CYCLE {cycle} | Level {current_level}: {prob['problem'][:50]}...")
        print(f"{'='*60}")

        # Test method
        print("\n[Solving...]")
        solution = apply_method(method, prob["problem"])
        score, missing = evaluate(prob["problem"], prob["criteria"], solution)
        print(f"  Score: {score}/10")
        print(f"  Missing: {missing[:80]}...")

        # Improve method based on what's missing
        print("\n[Improving method...]")
        improved = improve_method(method, prob["problem"], solution, score, missing)

        # Test improved method on SAME problem
        print("\n[Testing improved method...]")
        solution2 = apply_method(improved, prob["problem"])
        score2, missing2 = evaluate(prob["problem"], prob["criteria"], solution2)
        print(f"  Score: {score2}/10")
        print(f"  Missing: {missing2[:80]}...")

        gain = score2 - score
        print(f"\n  GAIN: {score} → {score2} ({gain:+.1f})")

        history.append({
            "cycle": cycle,
            "level": current_level,
            "before": score,
            "after": score2,
            "gain": gain
        })

        # Level up if doing well
        if score2 >= 7 and current_level < 5:
            current_level += 1
            print(f"\n  ★ LEVEL UP to {current_level}!")

        # Update method
        method = improved
        time.sleep(0.5)

    # Summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print("\n| Cycle | Level | Before | After | Gain |")
    print("|-------|-------|--------|-------|------|")
    for h in history:
        print(f"| {h['cycle']:>5} | {h['level']:>5} | {h['before']:>6} | {h['after']:>5} | {h['gain']:>+4.1f} |")

    total = sum(h["gain"] for h in history)
    positive = sum(1 for h in history if h["gain"] > 0)
    print(f"\nTotal: {total:+.1f} | Positive: {positive}/{len(history)}")

    # Check for compounding
    gains = [h["gain"] for h in history]
    if len(gains) >= 3:
        early_avg = sum(gains[:3]) / 3
        late_avg = sum(gains[-3:]) / 3
        print(f"\nEarly avg gain: {early_avg:+.2f}")
        print(f"Late avg gain: {late_avg:+.2f}")
        if late_avg > early_avg:
            print("★ COMPOUNDING DETECTED: Later cycles improving faster!")

    with open("true_exponential_v2_results.json", "w") as f:
        json.dump({"history": history, "final_method": method}, f, indent=2)

if __name__ == "__main__":
    run()
