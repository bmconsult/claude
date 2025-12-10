#!/usr/bin/env python3
"""
TRUE EXPONENTIAL V5: Push for 90%+

Key changes from V4 (67%):
1. 5 attempts per cycle (was 3)
2. 3 evals for stability (was 2)
3. Better improvement prompting
"""

import anthropic
import json
import time
import re

client = anthropic.Anthropic()

STRATEGY_V1 = """
PROBLEM-SOLVING STRATEGY:

1. STATE the problem in one clear sentence
2. LIST all constraints (must be true, can't change)
3. GENERATE 3 approaches: conventional, unconventional, hybrid
4. For EACH: identify main failure mode
5. SELECT approach with most addressable failure mode
6. DESIGN solution explicitly addressing that failure mode
7. VERIFY: solves original problem? respects all constraints?
"""

PROBLEM = """
Design a fair system for 4 roommates to share household chores.
Requirements:
- Everyone does roughly equal work over time
- Handles different schedules (some work weekends, etc.)
- Handles when someone is sick or traveling
- Prevents gaming/shirking
- Simple enough that busy people will actually use it
"""

CRITERIA = """
Score 0-3 on each (total 15):
1. SPECIFIC: Mechanics detailed enough to implement tomorrow?
2. FAIR: Everyone does equal work accounting for circumstances?
3. ROBUST: Handles edge cases (illness, travel, disputes)?
4. ENFORCEABLE: Accountability for shirking?
5. USABLE: Would busy roommates actually use this?
"""

def solve(strategy: str) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        temperature=0.3,
        messages=[{"role": "user", "content": f"{strategy}\n\nApply this strategy:\n{PROBLEM}"}]
    )
    return r.content[0].text

def evaluate_once(solution: str) -> int:
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0.1,
        messages=[{"role": "user", "content": f"""{CRITERIA}

SOLUTION: {solution}

Score each criterion 0-3. Output ONLY JSON: {{"s":1,"f":2,"r":2,"e":1,"u":3,"total":9}}"""}]
    )
    try:
        t = r.content[0].text
        if '{' in t:
            return json.loads(t[t.index('{'):t.rindex('}')+1]).get("total", 0)
    except:
        pass
    return 0

def evaluate(solution: str) -> tuple:
    """Stable eval: median of 3."""
    scores = [evaluate_once(solution) for _ in range(3)]
    scores.sort()
    return scores[1]  # median

def improve(strategy: str, score: int) -> str:
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        temperature=0.4,
        messages=[{"role": "user", "content": f"""
This strategy scored {score}/15. Improve it.

STRATEGY:
{strategy}

CRITERIA it's evaluated on:
{CRITERIA}

Make ONE specific change to improve the weakest area.
Keep same length. Output ONLY the improved strategy:
"""}]
    )
    return r.content[0].text

def run():
    print("="*70)
    print("TRUE EXPONENTIAL V5: 5 ATTEMPTS, 3 EVALS - TARGETING 90%+")
    print("="*70)

    strategy = STRATEGY_V1
    best_strategy = strategy
    best_score = 0
    history = []

    for cycle in range(1, 13):
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle}")
        print(f"{'='*60}")

        # Test current (3 evals)
        print("\n[Testing (3 evals)...]")
        solution = solve(strategy)
        current = evaluate(solution)
        print(f"  Score: {current}/15")

        # 5 attempts
        print(f"\n[5 improvement attempts...]")
        attempts = []
        for i in range(5):
            imp = improve(strategy, current)
            sol = solve(imp)
            sc = evaluate(sol)
            attempts.append((imp, sc))
            print(f"  {i+1}: {sc}/15", end=" ")
        print()

        best_imp, best_sc = max(attempts, key=lambda x: x[1])
        print(f"  Best: {best_sc}/15")

        gain = best_sc - current
        print(f"\n  RESULT: {current} → {best_sc} ({gain:+.0f})")

        if gain > 0:
            strategy = best_imp
            print("  ✓ Updated")
            if best_sc > best_score:
                best_score = best_sc
                best_strategy = best_imp
                print(f"  ★ New best: {best_score}")
        else:
            print("  ✗ Kept previous")

        history.append({
            "cycle": cycle,
            "before": current,
            "after": best_sc,
            "gain": gain,
            "positive": gain > 0
        })

        time.sleep(0.5)

    # Summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)

    print("\n| Cycle | Before | After | Gain |")
    print("|-------|--------|-------|------|")
    for h in history:
        m = "✓" if h["positive"] else "✗"
        print(f"| {h['cycle']:>5} | {h['before']:>6} | {h['after']:>5} | {h['gain']:>+4.0f} {m} |")

    total = sum(h["gain"] for h in history)
    pos = sum(1 for h in history if h["positive"])
    pct = pos / len(history) * 100

    print(f"\nTotal: {total:+.0f} | Positive: {pos}/{len(history)} ({pct:.0f}%)")
    print(f"Best: {best_score}/15")

    if pct >= 90:
        print("\n★★★ 90%+ ACHIEVED! Ready for exponential!")
    elif pct >= 61.8:
        print("\n★★ Above 61.8% - Compounding territory")
    else:
        print("\n★ Below threshold")

    with open("true_exponential_v5_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy, "best_strategy": best_strategy, "best_score": best_score, "positive_rate": pct}, f, indent=2)

if __name__ == "__main__":
    run()
