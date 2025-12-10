#!/usr/bin/env python3
"""
TRUE EXPONENTIAL: Method improves Method

The key insight:
- Method v1 solves problems
- Method v1 applied to "improve Method v1" → Method v2
- Method v2 solves problems BETTER (because it's better)
- Method v2 applied to "improve Method v2" → Method v3
- Method v3 is even better because it was improved by a BETTER method
- COMPOUNDING: each cycle, both the method AND the improvement process get better

This is different from just harder criteria - the PROCESS itself improves.
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# Starting method - simple but functional
METHOD_V1 = """
PROBLEM-SOLVING METHOD:

1. UNDERSTAND: What's the real problem? What would success look like?
2. DECOMPOSE: Break into parts. What are the sub-problems?
3. GENERATE: Create 3+ different approaches. Include unconventional ones.
4. EVALUATE: For each - what's the failure mode? What assumption could be wrong?
5. SELECT: Pick best. Address top failure mode explicitly.
6. VERIFY: Does solution actually solve the original problem? What's missing?
"""

# Benchmark problems - will get harder as method improves
PROBLEMS = {
    "easy": "Design a fair system for splitting a pizza among 3 people with different hunger levels.",
    "medium": "Design a system for a company to detect when their AI might be making biased decisions.",
    "hard": "Design a system for binding future generations to climate commitments they didn't vote for.",
    "impossible": "Design a system that allows a society to make irreversible decisions while preserving the ability to correct mistakes."
}

def apply_method(method: str, problem: str) -> str:
    """Use the method to solve a problem."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": f"""
{method}

Apply this method to solve:
{problem}

Work through each step explicitly.
"""}]
    )
    return r.content[0].text

def evaluate_solution(problem: str, solution: str) -> dict:
    """Score a solution. Returns score 0-10 and explanation."""
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": f"""
PROBLEM: {problem}

SOLUTION: {solution}

Score 0-10 on:
- Does it actually solve the problem? (not just reframe it)
- Is it specific enough to implement?
- Does it handle the hard parts, not just easy parts?

Be harsh. Most solutions deserve 3-5.

Return JSON: {{"score": N, "weakness": "main flaw"}}
"""}]
    )
    try:
        t = r.content[0].text
        if '{' in t:
            return json.loads(t[t.index('{'):t.rindex('}')+1])
    except:
        pass
    return {"score": 0, "weakness": "could not evaluate"}

def improve_method_with_method(method: str) -> str:
    """THE KEY: Use the method to improve itself."""

    meta_problem = f"""
The following is a problem-solving method. Your task is to IMPROVE this method
so it produces better solutions.

CURRENT METHOD:
{method}

This is a meta-problem: use good problem-solving to improve problem-solving.
Think about:
- What types of problems does this method fail on?
- What steps are missing or weak?
- What would make solutions more specific and actionable?
- How can failure modes be caught earlier?

Output an IMPROVED method. Keep what works. Fix what doesn't.
The improved method should be roughly the same length - don't just add complexity.
"""

    # Apply the method to the meta-problem of improving itself
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.3,
        messages=[{"role": "user", "content": f"""
{method}

Apply this method to solve:
{meta_problem}

Work through each step. Output the improved method at the end.
"""}]
    )

    # Extract just the improved method from the response
    response = r.content[0].text

    # Try to find the improved method in the response
    r2 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        temperature=0,
        messages=[{"role": "user", "content": f"""
Extract ONLY the improved problem-solving method from this text.
Remove all reasoning/explanation, keep only the method itself.
Format it cleanly with numbered steps.

TEXT:
{response}

OUTPUT (just the method, nothing else):
"""}]
    )

    return r2.content[0].text

def test_method(method: str, difficulty: str = "hard") -> float:
    """Test a method on a problem, return score."""
    problem = PROBLEMS[difficulty]
    solution = apply_method(method, problem)
    result = evaluate_solution(problem, solution)
    return result.get("score", 0), result.get("weakness", "unknown")

def run_exponential():
    """Run the true exponential loop."""

    print("="*70)
    print("TRUE EXPONENTIAL: METHOD IMPROVES METHOD")
    print("="*70)
    print("\nThe method improves itself. Better method → better improvements → compounding.\n")

    method = METHOD_V1
    history = []

    # Test on increasingly hard problems as method improves
    difficulties = ["medium", "hard", "hard", "hard", "impossible", "impossible"]

    for cycle in range(1, 7):
        difficulty = difficulties[min(cycle-1, len(difficulties)-1)]

        print(f"\n{'='*60}")
        print(f"CYCLE {cycle} (testing on: {difficulty})")
        print(f"{'='*60}")

        # Test current method
        print(f"\n[Testing Method v{cycle}...]")
        score_before, weakness = test_method(method, difficulty)
        print(f"  Score: {score_before}/10")
        print(f"  Weakness: {weakness}")

        # Use the method to improve itself
        print(f"\n[Method v{cycle} improving itself...]")
        improved_method = improve_method_with_method(method)

        # Test improved method on same difficulty
        print(f"\n[Testing Method v{cycle+1}...]")
        score_after, weakness_after = test_method(improved_method, difficulty)
        print(f"  Score: {score_after}/10")
        print(f"  Weakness: {weakness_after}")

        gain = score_after - score_before
        print(f"\n  GAIN: {score_before} → {score_after} ({gain:+.1f})")

        history.append({
            "cycle": cycle,
            "difficulty": difficulty,
            "before": score_before,
            "after": score_after,
            "gain": gain,
            "method_version": cycle
        })

        # Update method for next cycle
        method = improved_method

        time.sleep(1)

    # Summary
    print("\n" + "="*70)
    print("EXPONENTIAL RESULTS")
    print("="*70)

    print("\n| Cycle | Difficulty | Before | After | Gain | Compounding? |")
    print("|-------|------------|--------|-------|------|--------------|")

    prev_gain = 0
    for h in history:
        compounding = "YES ↑" if h["gain"] > prev_gain else "no"
        print(f"| {h['cycle']:>5} | {h['difficulty']:<10} | {h['before']:>6} | {h['after']:>5} | {h['gain']:>+4.1f} | {compounding:<12} |")
        prev_gain = h["gain"]

    total_gain = sum(h["gain"] for h in history)
    positive = sum(1 for h in history if h["gain"] > 0)

    print(f"\nTotal: {total_gain:+.1f} | Positive: {positive}/{len(history)}")

    # Save
    with open("true_exponential_results.json", "w") as f:
        json.dump({
            "history": history,
            "final_method": method,
            "total_gain": total_gain
        }, f, indent=2)

    print(f"\nFinal method saved to true_exponential_results.json")

    return history, method

if __name__ == "__main__":
    run_exponential()
