#!/usr/bin/env python3
"""
TRUE EXPONENTIAL V7: Dynamic Ceiling Detection + Aggressive Attempts

V6 Problem: Fixed thresholds (12/13) were too high.
V6 ceiling was at 11, but we only gave 3 attempts (since 11 < 12).
Result: 42% positive vs V4's 67%

V7 Solution:
1. LOWER baseline: 5 attempts minimum (not 3)
2. DYNAMIC detection: Track failures per score level
   - If 2+ failures at a level → that's the ceiling → 7 attempts
3. CONSERVATIVE thresholds: ≥10 = 5 attempts, but dynamic overrides

Key insight: Better to waste attempts than miss improvements.
"""

import anthropic
import json
import time
import re
from collections import defaultdict

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

def evaluate(solution: str) -> int:
    """Stable eval: median of 3."""
    scores = [evaluate_once(solution) for _ in range(3)]
    scores.sort()
    return scores[1]  # median

def improve(strategy: str, score: int) -> str:
    # Different prompts based on score level
    if score >= 12:
        prompt = f"""
This high-scoring strategy ({score}/15) needs SUBTLE refinement.

STRATEGY:
{strategy}

The strategy is already good. Make ONE SMALL, PRECISE change.
Don't add steps. Don't remove good things.
Just sharpen or clarify one weak point.

Output ONLY the improved strategy:
"""
    else:
        prompt = f"""
This strategy scored {score}/15. Improve it.

STRATEGY:
{strategy}

CRITERIA it's evaluated on:
{CRITERIA}

Make ONE specific change to improve the weakest area.
Keep same length. Output ONLY the improved strategy:
"""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.content[0].text

# Track failures per score level for dynamic ceiling detection
failure_tracker = defaultdict(int)

def get_attempts(score: int) -> int:
    """
    Dynamic ceiling detection + aggressive baseline.

    V6 lesson: Fixed thresholds fail when ceiling shifts.
    V7: Track failures per level, increase attempts dynamically.
    """
    # Dynamic: If 2+ failures at this level (or adjacent), it's ceiling territory
    nearby_failures = failure_tracker.get(score, 0) + failure_tracker.get(score - 1, 0)
    if nearby_failures >= 2:
        return 7  # Detected ceiling, max attempts

    # Conservative baseline (V6 used 3, we use 5 minimum)
    if score < 10:
        return 5   # Easy-ish, but still need room
    else:
        return 7   # At or above 10, always max attempts

def track_failure(score: int, positive: bool):
    """Track failures for dynamic ceiling detection."""
    if not positive:
        failure_tracker[score] += 1

def run():
    print("="*70)
    print("TRUE EXPONENTIAL V7: DYNAMIC CEILING + AGGRESSIVE ATTEMPTS")
    print("="*70)
    print("\nV6 problem: Fixed thresholds too high (ceiling at 11, threshold at 12)")
    print("V7 fix: 5 min attempts, 7 at ≥10, dynamic ceiling detection\n")

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

        # Adaptive attempts based on dynamic ceiling detection
        n_attempts = get_attempts(current)
        print(f"\n[{n_attempts} improvement attempts...]")

        attempts = []
        for i in range(n_attempts):
            imp = improve(strategy, current)
            sol = solve(imp)
            sc = evaluate(sol)
            attempts.append((imp, sc))
            print(f"  {i+1}: {sc}/15", end=" ")
        print()

        best_imp, best_sc = max(attempts, key=lambda x: x[1])
        print(f"  Best: {best_sc}/15")

        gain = best_sc - current
        positive = gain > 0
        print(f"\n  RESULT: {current} -> {best_sc} ({gain:+.0f})")

        # Track for dynamic ceiling detection
        track_failure(current, positive)

        if positive:
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
            "positive": positive,
            "attempts": n_attempts
        })

        time.sleep(0.5)

    # Summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)

    print("\n| Cycle | Before | After | Gain | Attempts |")
    print("|-------|--------|-------|------|----------|")
    for h in history:
        m = "✓" if h["positive"] else "✗"
        print(f"| {h['cycle']:>5} | {h['before']:>6} | {h['after']:>5} | {h['gain']:>+4.0f} {m} | {h['attempts']:>8} |")

    total = sum(h["gain"] for h in history)
    pos = sum(1 for h in history if h["positive"])
    pct = pos / len(history) * 100

    print(f"\nTotal: {total:+.0f} | Positive: {pos}/{len(history)} ({pct:.0f}%)")
    print(f"Best: {best_score}/15")

    # Breakdown by baseline
    low_base = [h for h in history if h["before"] < 10]
    med_base = [h for h in history if 10 <= h["before"] < 12]
    high_base = [h for h in history if h["before"] >= 12]

    if low_base:
        low_pos = sum(1 for h in low_base if h["positive"])
        print(f"\nBaseline < 10: {low_pos}/{len(low_base)} positive ({100*low_pos/len(low_base):.0f}%)")
    if med_base:
        med_pos = sum(1 for h in med_base if h["positive"])
        print(f"Baseline 10-11: {med_pos}/{len(med_base)} positive ({100*med_pos/len(med_base):.0f}%)")
    if high_base:
        high_pos = sum(1 for h in high_base if h["positive"])
        print(f"Baseline >= 12: {high_pos}/{len(high_base)} positive ({100*high_pos/len(high_base):.0f}%)")

    # Version comparison
    print("\n" + "-"*50)
    print("VERSION COMPARISON:")
    print("-"*50)
    print("V4: 67% (3 attempts, median eval)")
    print("V6: 42% (adaptive 3-7, but thresholds too high)")
    print(f"V7: {pct:.0f}% (5-7 attempts, dynamic ceiling)")

    if pct >= 90:
        print("\n★★★ 90%+ ACHIEVED! Ready for exponential!")
    elif pct >= 67:
        print("\n★★ Improved over V4/V6!")
    elif pct >= 61.8:
        print("\n★★ Above 61.8% - Compounding territory")
    else:
        print("\n★ Below threshold - need more refinement")

    with open("true_exponential_v7_results.json", "w") as f:
        json.dump({
            "history": history,
            "final_strategy": strategy,
            "best_strategy": best_strategy,
            "best_score": best_score,
            "positive_rate": pct,
            "failure_tracker": dict(failure_tracker)
        }, f, indent=2)

if __name__ == "__main__":
    run()
