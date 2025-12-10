#!/usr/bin/env python3
"""
TRUE EXPONENTIAL V3: Bulletproof improvement loop first

Key insight from the original researcher:
1. FIRST: Make improvement work EVERY time (linear phase)
2. THEN: Use the improved strategy to improve the PROCESS
3. Better process → faster improvement → compounding

This version focuses on making improvement reliable before attempting compounding.
"""

import anthropic
import json
import time
import re

client = anthropic.Anthropic()

# Simple starting strategy
STRATEGY_V1 = """
PROBLEM-SOLVING STRATEGY:

1. STATE the problem clearly in one sentence
2. LIST all constraints (what must be true, what can't change)
3. GENERATE 3 approaches:
   - A conventional approach
   - An unconventional approach
   - A hybrid approach
4. For EACH approach, identify the main failure mode
5. SELECT the approach with the most addressable failure mode
6. DESIGN the solution addressing that failure mode explicitly
7. VERIFY: Does this solve the stated problem while respecting all constraints?
"""

# Simple problem - solvable but requires good thinking
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
1. SPECIFIC: Are the mechanics detailed enough to implement tomorrow?
2. FAIR: Does everyone do equal work accounting for circumstances?
3. ROBUST: Does it handle edge cases (illness, travel, disputes)?
4. ENFORCEABLE: Is there accountability for shirking?
5. USABLE: Would busy roommates actually use this?
"""

def solve(strategy: str) -> str:
    """Apply strategy to solve the problem."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        temperature=0.3,
        messages=[{"role": "user", "content": f"{strategy}\n\nApply this strategy to solve:\n{PROBLEM}"}]
    )
    return r.content[0].text

def evaluate(solution: str) -> tuple:
    """Score solution. Returns (total_score, dict_of_scores, weakness)."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        temperature=0,
        messages=[{"role": "user", "content": f"""
{CRITERIA}

SOLUTION:
{solution}

For each criterion, give a score 0-3 with brief justification.
End with the main weakness to fix.

Format:
1. SPECIFIC: [0-3] - [reason]
2. FAIR: [0-3] - [reason]
3. ROBUST: [0-3] - [reason]
4. ENFORCEABLE: [0-3] - [reason]
5. USABLE: [0-3] - [reason]
TOTAL: [sum]/15
WEAKNESS: [main thing to improve]
"""}]
    )
    text = r.content[0].text

    # Parse scores
    scores = {}
    for line in text.split('\n'):
        for crit in ['SPECIFIC', 'FAIR', 'ROBUST', 'ENFORCEABLE', 'USABLE']:
            if crit in line and ':' in line:
                match = re.search(r'(\d)', line.split(':')[1])
                if match:
                    scores[crit] = int(match.group(1))

    total = sum(scores.values()) if scores else 0

    # Extract weakness
    weakness = "unknown"
    if 'WEAKNESS:' in text:
        weakness = text.split('WEAKNESS:')[1].strip().split('\n')[0]

    return total, scores, weakness

def improve_strategy(strategy: str, solution: str, scores: dict, weakness: str) -> str:
    """Improve the strategy based on what the solution missed."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        temperature=0.2,
        messages=[{"role": "user", "content": f"""
A problem-solving strategy produced a solution that scored:
{json.dumps(scores, indent=2)}

The main weakness was: {weakness}

CURRENT STRATEGY:
{strategy}

TASK: Modify the strategy so it would NOT produce this weakness.
- Add a specific check, step, or reminder
- Keep the strategy roughly the same length
- Be precise about what to add/change

Output ONLY the improved strategy (no explanation):
"""}]
    )
    return r.content[0].text

def run():
    print("="*70)
    print("TRUE EXPONENTIAL V3: BULLETPROOF IMPROVEMENT LOOP")
    print("="*70)
    print("\nGoal: Make improvement work EVERY cycle before attempting compounding\n")

    strategy = STRATEGY_V1
    history = []

    for cycle in range(1, 11):
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle}")
        print(f"{'='*60}")

        # Solve
        print("\n[Solving...]")
        solution = solve(strategy)

        # Evaluate
        print("[Evaluating...]")
        total, scores, weakness = evaluate(solution)
        print(f"  Scores: {scores}")
        print(f"  Total: {total}/15")
        print(f"  Weakness: {weakness[:60]}...")

        # Improve strategy
        print("\n[Improving strategy...]")
        improved_strategy = improve_strategy(strategy, solution, scores, weakness)

        # Test improved strategy
        print("[Testing improved strategy...]")
        solution2 = solve(improved_strategy)
        total2, scores2, weakness2 = evaluate(solution2)
        print(f"  Scores: {scores2}")
        print(f"  Total: {total2}/15")

        gain = total2 - total
        print(f"\n  RESULT: {total} → {total2} ({gain:+d})")

        history.append({
            "cycle": cycle,
            "before": total,
            "after": total2,
            "gain": gain,
            "before_scores": scores,
            "after_scores": scores2
        })

        # Update strategy if improved
        if gain > 0:
            strategy = improved_strategy
            print("  ✓ Strategy updated")
        else:
            print("  ✗ Keeping previous strategy")

        time.sleep(0.5)

    # Summary
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print("\n| Cycle | Before | After | Gain |")
    print("|-------|--------|-------|------|")
    for h in history:
        marker = "✓" if h["gain"] > 0 else "✗"
        print(f"| {h['cycle']:>5} | {h['before']:>6} | {h['after']:>5} | {h['gain']:>+4} {marker} |")

    total_gain = sum(h["gain"] for h in history)
    positive = sum(1 for h in history if h["gain"] > 0)

    print(f"\nTotal gain: {total_gain:+d}")
    print(f"Positive cycles: {positive}/10 ({positive*10}%)")

    # Check for consistent improvement
    if positive >= 7:
        print("\n★ IMPROVEMENT LOOP IS RELIABLE!")
        print("  Ready for phase 2: Use improved strategy to improve the process")

    with open("true_exponential_v3_results.json", "w") as f:
        json.dump({"history": history, "final_strategy": strategy}, f, indent=2)

if __name__ == "__main__":
    run()
