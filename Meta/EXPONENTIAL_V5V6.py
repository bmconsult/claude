#!/usr/bin/env python3
"""
EXPONENTIAL CYCLES 5-6: Push even harder criteria
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# Load from previous run
with open("exponential_full_results.json", "r") as f:
    prev = json.load(f)

PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
]

# Even harder criteria
V5_CRITERIA = """CRITERIA (0-3 each, total 15):
1. SKIN-IN-GAME: Decision-makers bear consequences of failure
2. SCALABLE: Works at 10x and 0.1x current scale
3. CULTURALLY-ROBUST: Works across different value systems
4. TRANSPARENT: Reasoning visible and auditable
5. MINIMAL-ATTACK-SURFACE: Few points of failure/exploitation"""

V6_CRITERIA = """CRITERIA (0-3 each, total 15):
1. SELF-CORRECTING: Detects and fixes own errors
2. POWER-DISTRIBUTED: No single point of control
3. KNOWLEDGE-GENERATING: Creates useful information over time
4. DIGNIFIED: Preserves human agency and respect
5. EVOLUTIONARY: Improves through variation and selection"""

def solve(problem: str, strategy: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2000, temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {problem}\n\nSolve:"}]
    )
    return r.content[0].text

def score(problem: str, solution: str, criteria: str) -> int:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=500, temperature=0,
        messages=[{"role": "user", "content": f"""ADVERSARIAL EVAL. Quote text or 0.

{criteria}

PROBLEM: {problem}
SOLUTION: {solution}

JSON: {{"c1":N,"c2":N,"c3":N,"c4":N,"c5":N,"total":N}}"""}]
    )
    try:
        t = r.content[0].text
        if '{' in t:
            return json.loads(t[t.index('{'):t.rindex('}')+1]).get("total", 0)
    except:
        pass
    return 0

def test(strategy: str, criteria: str) -> float:
    scores = [score(p, solve(p, strategy), criteria) for p in PROBLEMS]
    print(f"    Scores: {scores} → avg {sum(scores)/len(scores):.1f}")
    return sum(scores)/len(scores)

def improve(strategy: str, criteria: str, score: float) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2500, temperature=0.3,
        messages=[{"role": "user", "content": f"""Improve strategy for these criteria (current: {score:.1f}/15):

{criteria}

STRATEGY:
{strategy}

Output improved strategy with specific steps for each weak criterion:"""}]
    )
    return r.content[0].text

def run():
    print("="*70)
    print("EXPONENTIAL CYCLES 5-6: Even harder criteria")
    print("="*70)

    strategy = prev["final_strategy"]
    history = prev["history"]

    for cycle, (name, criteria) in [(5, ("V5", V5_CRITERIA)), (6, ("V6", V6_CRITERIA))]:
        print(f"\n{'='*70}")
        print(f"CYCLE {cycle}: {name} criteria")
        print("="*70)

        print("\n  Before:")
        before = test(strategy, criteria)

        print("\n  Improving...")
        strategy = improve(strategy, criteria, before)

        print("\n  After:")
        after = test(strategy, criteria)

        gain = after - before
        history.append({"cycle": cycle, "criteria": name, "before": before, "after": after, "gain": gain})
        print(f"\n  RESULT: {before:.1f} → {after:.1f} ({gain:+.1f})")

        time.sleep(1)

    print("\n" + "="*70)
    print("FULL EXPONENTIAL SUMMARY (6 CYCLES)")
    print("="*70)
    print("\n| Cycle | Criteria | Before | After | Gain |")
    print("|-------|----------|--------|-------|------|")
    for h in history:
        print(f"| {h['cycle']}     | {h['criteria']:<8} | {h['before']:>6.1f} | {h['after']:>5.1f} | {h['gain']:>+5.1f} |")

    total = sum(h['gain'] for h in history)
    positive = sum(1 for h in history if h['gain'] > 0)
    print(f"\nTotal gain: {total:+.1f}")
    print(f"Positive: {positive}/{len(history)}")

    with open("exponential_v5v6_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)

if __name__ == "__main__":
    run()
