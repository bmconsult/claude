#!/usr/bin/env python3
"""
TRUE EXPONENTIAL V4: Push to 90%+ positive cycles

Key insight from golden ratio thresholds:
- Below 38.2% → collapse
- 38.2% - 61.8% → survival mode (we were here at 60%)
- Above 61.8% → compounding begins
- 90%+ → biological homeostasis, true stability

Strategy to reach 90%+:
1. MULTIPLE ATTEMPTS: Try 3 improvements, pick best
2. STABLE EVALUATION: Average 2 evals to reduce variance
3. SMART SELECTION: Only update if gain > 0, keep best seen
"""

import anthropic
import json
import time
import re

client = anthropic.Anthropic()

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

def evaluate_once(solution: str) -> tuple:
    """Single evaluation. Returns (total, scores_dict, weakness)."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        temperature=0.1,  # Lower temp for more consistent evals
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

    scores = {}
    for crit in ['SPECIFIC', 'FAIR', 'ROBUST', 'ENFORCEABLE', 'USABLE']:
        for line in text.split('\n'):
            if crit in line and ':' in line:
                match = re.search(r'(\d)', line.split(':')[1])
                if match:
                    scores[crit] = int(match.group(1))
                    break

    total = sum(scores.values()) if len(scores) == 5 else 0

    weakness = "unknown"
    if 'WEAKNESS:' in text:
        weakness = text.split('WEAKNESS:')[1].strip().split('\n')[0]

    return total, scores, weakness

def evaluate(solution: str) -> tuple:
    """Stable evaluation: average of 2 evals."""
    t1, s1, w1 = evaluate_once(solution)
    t2, s2, w2 = evaluate_once(solution)

    # Average the totals
    avg_total = (t1 + t2) / 2

    # Use the weakness from the lower-scoring eval (more informative)
    weakness = w1 if t1 <= t2 else w2

    return avg_total, weakness

def improve_strategy(strategy: str, weakness: str) -> str:
    """Generate one improved strategy."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        temperature=0.3,
        messages=[{"role": "user", "content": f"""
A problem-solving strategy produced solutions with this main weakness:
{weakness}

CURRENT STRATEGY:
{strategy}

TASK: Modify the strategy to prevent this weakness.
- Add a specific check, step, or reminder that addresses it
- Keep roughly the same length - don't bloat
- Be precise about what to add/change

Output ONLY the improved strategy (no explanation):
"""}]
    )
    return r.content[0].text

def try_improvements(strategy: str, weakness: str, n_attempts: int = 3) -> list:
    """Try multiple improvements, return list of (improved_strategy, score)."""
    attempts = []
    for i in range(n_attempts):
        improved = improve_strategy(strategy, weakness)
        solution = solve(improved)
        score, _ = evaluate(solution)
        attempts.append((improved, score))
        time.sleep(0.3)
    return attempts

def run():
    print("="*70)
    print("TRUE EXPONENTIAL V4: TARGETING 90%+ POSITIVE CYCLES")
    print("="*70)
    print("\nStrategy: Multiple attempts + stable evaluation + smart selection\n")
    print("Thresholds: <38.2% collapse | 38.2-61.8% survival | >61.8% compound | >90% stable\n")

    strategy = STRATEGY_V1
    best_strategy = strategy
    best_score = 0
    history = []

    for cycle in range(1, 13):  # 12 cycles to get good statistics
        print(f"\n{'='*60}")
        print(f"CYCLE {cycle}")
        print(f"{'='*60}")

        # Test current strategy (stable eval)
        print("\n[Testing current strategy (2 evals)...]")
        solution = solve(strategy)
        current_score, weakness = evaluate(solution)
        print(f"  Score: {current_score:.1f}/15")
        print(f"  Weakness: {weakness[:60]}...")

        # Try 3 improvements, pick best
        print(f"\n[Trying 3 improvements...]")
        attempts = try_improvements(strategy, weakness, n_attempts=3)

        # Find best attempt
        best_attempt = max(attempts, key=lambda x: x[1])
        best_improved, improved_score = best_attempt

        print(f"  Attempt scores: {[f'{a[1]:.1f}' for a in attempts]}")
        print(f"  Best attempt: {improved_score:.1f}/15")

        gain = improved_score - current_score
        print(f"\n  RESULT: {current_score:.1f} → {improved_score:.1f} ({gain:+.1f})")

        # Update if improved
        if gain > 0:
            strategy = best_improved
            print("  ✓ Strategy updated")
            if improved_score > best_score:
                best_score = improved_score
                best_strategy = best_improved
                print(f"  ★ New best score: {best_score:.1f}")
        else:
            print("  ✗ Keeping previous strategy")

        history.append({
            "cycle": cycle,
            "before": current_score,
            "after": improved_score,
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
        marker = "✓" if h["positive"] else "✗"
        print(f"| {h['cycle']:>5} | {h['before']:>6.1f} | {h['after']:>5.1f} | {h['gain']:>+5.1f} {marker} |")

    total_gain = sum(h["gain"] for h in history)
    positive = sum(1 for h in history if h["positive"])
    pct = positive / len(history) * 100

    print(f"\nTotal gain: {total_gain:+.1f}")
    print(f"Positive cycles: {positive}/{len(history)} ({pct:.0f}%)")
    print(f"Best score achieved: {best_score:.1f}/15")

    # Threshold analysis
    print("\n" + "-"*40)
    if pct >= 90:
        print("★★★ 90%+ ACHIEVED! Ready for exponential phase!")
    elif pct >= 61.8:
        print("★★ Above 61.8% - Compounding territory!")
    elif pct >= 38.2:
        print("★ Above 38.2% - Survival mode")
    else:
        print("⚠ Below 38.2% - System degrading")

    with open("true_exponential_v4_results.json", "w") as f:
        json.dump({
            "history": history,
            "final_strategy": strategy,
            "best_strategy": best_strategy,
            "best_score": best_score,
            "positive_rate": pct
        }, f, indent=2)

if __name__ == "__main__":
    run()
