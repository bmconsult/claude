#!/usr/bin/env python3
"""
CLEAN EXPONENTIAL: Smaller, focused improvements each cycle
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

BENCHMARK = [
    {"id": "climate", "text": "Design a system for binding future generations to climate commitments they didn't vote for."},
    {"id": "ai_crime", "text": "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy."},
]

# Start with clean strategy
STRATEGY_V1 = """
PROBLEM-SOLVING STRATEGY

1. FRAME: What type? Success criteria? Constraints?
2. GENERATE: 3+ different approaches (include unconventional)
3. EVALUATE: Core tension? Failure modes? Specific enough?
4. SELECT: Best approach, address top failure
5. VERIFY: Constraints met? Implementable? Falsifiable?
"""

# Progressive criteria levels
CRITERIA = {
    "L1": """CRITERIA (0-3 each, max 9):
1. TENSION: Names core conflict
2. SPECIFIC: Stranger could implement
3. FAILURE: Addresses failure modes""",

    "L2": """CRITERIA (0-3 each, max 9):
1. SECOND-ORDER: Traces consequences 2+ levels
2. ADVERSARIAL: Robust to gaming
3. ADAPTABLE: Handles changing conditions""",

    "L3": """CRITERIA (0-3 each, max 9):
1. ECOSYSTEM: Maps effects on adjacent systems
2. REVERSIBLE: Can undo if wrong
3. INCENTIVE-ALIGNED: Self-interest supports goals"""
}


def solve(problem: str, strategy: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1500, temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {problem}\n\nSolve:"}]
    )
    return r.content[0].text


def evaluate(problem: str, solution: str, criteria: str) -> int:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=300, temperature=0,
        messages=[{"role": "user", "content": f"""Score STRICTLY. Quote text or score 0.

{criteria}

PROBLEM: {problem}
SOLUTION: {solution}

Return just total score (0-9):"""}]
    )
    try:
        return int(''.join(c for c in r.content[0].text if c.isdigit())[:1] or '0')
    except:
        return 0


def test(strategy: str, criteria: str, label: str) -> float:
    scores = []
    for p in BENCHMARK:
        sol = solve(p["text"], strategy)
        score = evaluate(p["text"], sol, criteria)
        scores.append(score)
        time.sleep(0.3)
    avg = sum(scores) / len(scores)
    print(f"  {label}: {scores} avg={avg:.1f}")
    return avg


def improve(strategy: str, criteria: str, score: float) -> str:
    """Small focused improvement"""
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1000, temperature=0.3,
        messages=[{"role": "user", "content": f"""Current strategy scores {score:.1f}/9 on:
{criteria}

STRATEGY:
{strategy}

Add ONE specific step or sub-step to improve on these criteria.
Keep it simple. Output the complete improved strategy:"""}]
    )
    return r.content[0].text


def run():
    print("="*60)
    print("EXPONENTIAL GROWTH: Progressive Criteria Levels")
    print("="*60)

    strategy = STRATEGY_V1
    history = []

    for level, (name, criteria) in enumerate(CRITERIA.items(), 1):
        print(f"\n--- LEVEL {level} ({name}) ---")

        # Test current
        before = test(strategy, criteria, f"Before")

        # Improve
        strategy = improve(strategy, criteria, before)

        # Test improved
        after = test(strategy, criteria, f"After")

        gain = after - before
        history.append({"level": name, "before": before, "after": after, "gain": gain})
        print(f"  Gain: {gain:+.1f}")

    print("\n" + "="*60)
    print("EXPONENTIAL RESULTS")
    print("="*60)
    print("\n| Level | Before | After | Gain |")
    print("|-------|--------|-------|------|")
    for h in history:
        print(f"| {h['level']}    | {h['before']:.1f}    | {h['after']:.1f}   | {h['gain']:+.1f} |")

    total = sum(h['gain'] for h in history)
    print(f"\nTotal gain across levels: {total:+.1f}")

    positive = sum(1 for h in history if h['gain'] > 0)
    print(f"Positive improvements: {positive}/{len(history)}")

    if positive >= 2:
        print("\n✓ EXPONENTIAL PATTERN: Each new measurement level unlocks improvement")

    with open("exponential_clean_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)


if __name__ == "__main__":
    run()
