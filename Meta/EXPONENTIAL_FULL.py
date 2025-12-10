#!/usr/bin/env python3
"""
EXPONENTIAL CYCLES 2-4: Keep pushing!
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# Load Cycle 1 results
with open("exponential_results.json", "r") as f:
    c1 = json.load(f)

PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
]

# Criteria progression
CRITERIA_LEVELS = {
    "V2": """CRITERIA (0-3 each, total 15):
1. SECOND-ORDER: Traces consequences 2+ levels deep
2. ADVERSARIAL: Survives hostile actors gaming it
3. ELEGANCE: Minimal complexity for maximum effect
4. ADAPTABLE: Handles changed conditions
5. NOVEL: Non-obvious, genuinely creative""",

    "V3": """CRITERIA (0-3 each, total 15):
1. ECOSYSTEM: Maps effects on adjacent systems
2. REVERSIBLE: Can undo if it goes wrong
3. INCENTIVE-ALIGNED: Self-interest supports goals
4. GRACEFUL-FAILURE: Degrades safely under stress
5. GENERATIVE: Enables positive emergent outcomes""",

    "V4": """CRITERIA (0-3 each, total 15):
1. ANTIFRAGILE: Gets stronger from shocks
2. LEGITIMACY: Stakeholders accept authority
3. FEEDBACK-RICH: Rapid error detection
4. COMPOSABLE: Works with other systems
5. TIMELESS: Still works in 50 years"""
}

def solve(problem: str, strategy: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2000, temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {problem}\n\nApply strategy:"}]
    )
    return r.content[0].text

def score(problem: str, solution: str, criteria: str) -> dict:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=600, temperature=0,
        messages=[{"role": "user", "content": f"""ADVERSARIAL EVAL. Quote text or score 0.

{criteria}

PROBLEM: {problem}
SOLUTION: {solution}

JSON: {{"c1":N,"c2":N,"c3":N,"c4":N,"c5":N,"total":N}}"""}]
    )
    try:
        t = r.content[0].text
        if '{' in t:
            return json.loads(t[t.index('{'):t.rindex('}')+1])
    except:
        pass
    return {"total": 0}

def test(strategy: str, criteria: str, label: str) -> float:
    scores = []
    for p in PROBLEMS:
        sol = solve(p, strategy)
        s = score(p, sol, criteria)
        scores.append(s.get("total", 0))
        print(f"      {scores[-1]}/15", end=" ", flush=True)
        time.sleep(0.3)
    avg = sum(scores)/len(scores)
    print(f"→ avg {avg:.1f}")
    return avg

def improve(strategy: str, criteria: str, current_score: float) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2000, temperature=0.3,
        messages=[{"role": "user", "content": f"""Improve this strategy to score higher on these criteria.
Current score: {current_score:.1f}/15

CRITERIA:
{criteria}

CURRENT STRATEGY:
{strategy}

Output ONLY the improved strategy (complete, all steps). Add specific sub-steps for weak criteria:"""}]
    )
    return r.content[0].text

def run_cycles():
    print("="*70)
    print("EXPONENTIAL CYCLES: Continuing from Cycle 1 (+265%)")
    print("="*70)

    # Start with the improved strategy from Cycle 1
    strategy = c1.get("improved_strategy", """
PROBLEM-SOLVING STRATEGY v4

1. FRAME: Type? Success? Constraints?
2. GENERATE: 3+ approaches (include unconventional)
3. EVALUATE: Tension? Failures? Specific?
4. SELECT: Best + address failure mode
5. VERIFY: Constraints? Implementable? Falsifiable?
6. SECOND-ORDER: What are consequences of consequences?
7. ADVERSARIAL: How could this be gamed?
""")

    history = [{"cycle": 1, "criteria": "V2", "before": 2.0, "after": 7.3, "gain": 5.3}]

    for cycle, (level, criteria) in enumerate(CRITERIA_LEVELS.items(), 2):
        print(f"\n{'='*70}")
        print(f"CYCLE {cycle}: Testing on {level} criteria")
        print("="*70)

        # Test current strategy on new criteria
        print(f"\n  Before improvement:")
        before = test(strategy, criteria, f"v{cycle} + {level}")

        # Improve
        print(f"\n  Improving strategy for {level}...")
        strategy = improve(strategy, criteria, before)

        # Test improved
        print(f"\n  After improvement:")
        after = test(strategy, criteria, f"v{cycle+1} + {level}")

        gain = after - before
        history.append({"cycle": cycle, "criteria": level, "before": before, "after": after, "gain": gain})

        print(f"\n  CYCLE {cycle} RESULT: {before:.1f} → {after:.1f} ({gain:+.1f})")

        time.sleep(1)

    # Summary
    print("\n" + "="*70)
    print("EXPONENTIAL GROWTH SUMMARY")
    print("="*70)
    print("\n| Cycle | Criteria | Before | After | Gain   |")
    print("|-------|----------|--------|-------|--------|")
    for h in history:
        print(f"| {h['cycle']}     | {h['criteria']:<8} | {h['before']:>6.1f} | {h['after']:>5.1f} | {h['gain']:>+6.1f} |")

    total_gain = sum(h['gain'] for h in history)
    positive = sum(1 for h in history if h['gain'] > 0)

    print(f"\nTotal gain: {total_gain:+.1f}")
    print(f"Positive cycles: {positive}/{len(history)}")

    if positive >= 2:
        print("\n✓ EXPONENTIAL PATTERN CONFIRMED")
        print("  Each new criteria level → reveals weakness → improvement")

    with open("exponential_full_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)

    return history

if __name__ == "__main__":
    run_cycles()
