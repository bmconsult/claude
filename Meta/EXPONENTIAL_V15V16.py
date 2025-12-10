#!/usr/bin/env python3
"""
EXPONENTIAL CYCLES 15-16: Adversarial and meta-meta criteria
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

with open("exponential_v13v14_results.json", "r") as f:
    prev = json.load(f)

PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
]

# V15: Adversarial robustness
V15_CRITERIA = """CRITERIA (0-3 each, total 15):
1. CAPTURE-RESISTANT: Can't be co-opted by powerful interests
2. CRITICISM-INVITING: Makes it easy to identify flaws
3. TRANSPARENCY-ENFORCED: Hidden agendas become visible
4. CONCENTRATION-PREVENTING: Power naturally disperses
5. ACCOUNTABILITY-BUILT-IN: Someone is responsible for failures"""

# V16: Meta-meta level - about the strategy itself
V16_CRITERIA = """CRITERIA (0-3 each, total 15):
1. SELF-REFERENTIALLY-VALID: The strategy works on itself
2. IMPROVEMENT-PATHWAY-CLEAR: How to make it better is obvious
3. LIMITATION-HONEST: Acknowledges what it can't do
4. CONTEXT-AWARE: Knows when it applies and doesn't
5. ELEGANCE-MAINTAINED: Complexity hasn't exploded"""

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
    print("CYCLES 15-16: ADVERSARIAL + META-META")
    print("="*70)

    strategy = prev["final_strategy"]
    history = prev["history"]

    for cycle, (name, criteria) in [(15, ("V15", V15_CRITERIA)), (16, ("V16", V16_CRITERIA))]:
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
    print("ALL 16 CYCLES")
    print("="*70)
    print("\n| Cycle | Criteria | Before | After | Gain |")
    print("|-------|----------|--------|-------|------|")
    for h in history:
        print(f"| {h['cycle']:>5} | {h['criteria']:<8} | {h['before']:>6.1f} | {h['after']:>5.1f} | {h['gain']:>+5.1f} |")

    total = sum(h['gain'] for h in history)
    pos = sum(1 for h in history if h['gain'] > 0)
    print(f"\nTotal: {total:+.1f} | Positive: {pos}/{len(history)}")

    with open("exponential_v15v16_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)

if __name__ == "__main__":
    run()
