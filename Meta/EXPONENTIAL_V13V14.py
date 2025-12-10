#!/usr/bin/env python3
"""
EXPONENTIAL CYCLES 13-14: Edge case and long-term criteria
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

with open("exponential_v11v12_results.json", "r") as f:
    prev = json.load(f)

PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
]

# V13: Edge cases and unusual scenarios
V13_CRITERIA = """CRITERIA (0-3 each, total 15):
1. EDGE-CASE-AWARE: Handles unusual/rare scenarios explicitly
2. FAILURE-CASCADE-PROOF: One failure doesn't cause others
3. BAD-FAITH-RESISTANT: Works when actors lie/deceive
4. ASSUMPTION-EXPLICIT: States what must be true for this to work
5. ESCAPE-HATCH: Has override mechanism for emergencies"""

# V14: Long-term and meta concerns
V14_CRITERIA = """CRITERIA (0-3 each, total 15):
1. GENERATIONALLY-FAIR: Doesn't impose unfair burdens on future
2. LEARNING-INTEGRATED: Incorporates lessons as they emerge
3. SUCCESSOR-COMPATIBLE: Works with systems that replace it
4. DOCUMENTATION-COMPLETE: Future maintainers can understand why
5. DEATH-WITH-DIGNITY: Can end gracefully when obsolete"""

def solve(problem: str, strategy: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2000, temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nPROBLEM: {problem}\n\nSolve:"}]
    )
    return r.content[0].text

def score(problem: str, solution: str, criteria: str) -> int:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=500, temperature=0,
        messages=[{"role": "user", "content": f"""ADVERSARIAL. Quote or 0.
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
    print(f"    {scores} → {sum(scores)/len(scores):.1f}")
    return sum(scores)/len(scores)

def improve(strategy: str, criteria: str, sc: float) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=2500, temperature=0.3,
        messages=[{"role": "user", "content": f"""Improve for {sc:.1f}/15:
{criteria}
STRATEGY: {strategy}
Output improved strategy:"""}]
    )
    return r.content[0].text

def run():
    print("="*70)
    print("CYCLES 13-14: EDGE CASES + LONG-TERM")
    print("="*70)

    strategy = prev["final_strategy"]
    history = prev["history"]

    for cycle, (name, criteria) in [(13, ("V13", V13_CRITERIA)), (14, ("V14", V14_CRITERIA))]:
        print(f"\n--- CYCLE {cycle}: {name} ---")
        print("  Before:", end=" ")
        before = test(strategy, criteria)
        print("  Improving...")
        strategy = improve(strategy, criteria, before)
        print("  After:", end=" ")
        after = test(strategy, criteria)
        gain = after - before
        history.append({"cycle": cycle, "criteria": name, "before": before, "after": after, "gain": gain})
        print(f"  {before:.1f} → {after:.1f} ({gain:+.1f})")
        time.sleep(1)

    print("\n" + "="*70)
    print("ALL 14 CYCLES")
    print("="*70)
    print("\n| Cycle | Criteria | Before | After | Gain |")
    print("|-------|----------|--------|-------|------|")
    for h in history:
        print(f"| {h['cycle']:>5} | {h['criteria']:<8} | {h['before']:>6.1f} | {h['after']:>5.1f} | {h['gain']:>+5.1f} |")

    total = sum(h['gain'] for h in history)
    pos = sum(1 for h in history if h['gain'] > 0)
    print(f"\nTotal: {total:+.1f} | Positive: {pos}/{len(history)}")

    with open("exponential_v13v14_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)

if __name__ == "__main__":
    run()
