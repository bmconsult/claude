#!/usr/bin/env python3
"""
EXPONENTIAL CYCLES 11-12: Philosophical depth criteria
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

with open("exponential_v9v10_results.json", "r") as f:
    prev = json.load(f)

PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
]

# V11: Philosophical depth
V11_CRITERIA = """CRITERIA (0-3 each, total 15):
1. EPISTEMIC-HUMILITY: Acknowledges what it can't know
2. TRADE-OFF-EXPLICIT: Names what's sacrificed for what's gained
3. STAKE-HOLDER-COMPLETE: All affected parties identified
4. TIME-HORIZON-AWARE: Different effects at different timescales
5. PARADOX-SURFACING: Makes hidden contradictions visible"""

# V12: Implementation reality
V12_CRITERIA = """CRITERIA (0-3 each, total 15):
1. RESOURCE-REALISTIC: Could actually be funded/staffed
2. POLITICALLY-FEASIBLE: Could get approval/adoption
3. INCREMENTALLY-DEPLOYABLE: Can start small and scale
4. MONITORING-BUILT-IN: Has feedback mechanisms from day 1
5. EXIT-STRATEGY: What to do when it needs to end"""

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
    print("CYCLES 11-12: PHILOSOPHICAL + PRACTICAL")
    print("="*70)

    strategy = prev["final_strategy"]
    history = prev["history"]

    for cycle, (name, criteria) in [(11, ("V11", V11_CRITERIA)), (12, ("V12", V12_CRITERIA))]:
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
    print("ALL 12 CYCLES")
    print("="*70)
    print("\n| Cycle | Criteria | Before | After | Gain |")
    print("|-------|----------|--------|-------|------|")
    for h in history:
        print(f"| {h['cycle']:>5} | {h['criteria']:<8} | {h['before']:>6.1f} | {h['after']:>5.1f} | {h['gain']:>+5.1f} |")

    total = sum(h['gain'] for h in history)
    pos = sum(1 for h in history if h['gain'] > 0)
    print(f"\nTotal: {total:+.1f} | Positive: {pos}/{len(history)}")

    with open("exponential_v11v12_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)

if __name__ == "__main__":
    run()
