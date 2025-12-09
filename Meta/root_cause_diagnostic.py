#!/usr/bin/env python3
"""
ROOT CAUSE DIAGNOSTIC
=====================

Purpose: Understand WHY solutions get 8 vs 9 on strategic depth.
Method: Get evaluator reasoning for multiple solutions, analyze patterns.

This is proper root cause analysis, not "add more steps."
"""

import anthropic
import json
import sys
from datetime import datetime

# Same problems from previous experiments
PROBLEMS = [
    "A software company's best engineer wants to leave for a competitor. They have critical knowledge not documented anywhere. The CEO has 24 hours before the engineer's final decision. What should the CEO do?",
    "A hospital has 30% more patients than beds. The board wants to build a new wing (2 years, $50M) but the CFO says they'll be bankrupt in 6 months at current burn rate. What should they do?",
    "A family business patriarch is dying. His three children hate each other. The business is worth $100M but illiquid. Two want to sell, one wants to keep it. The patriarch wants family unity above all. What should the family advisor recommend?",
]

# The v5.2-V methodology that we've been using
METHODOLOGY_V52V = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-V**

STEP 1: ASSUMPTION AUDIT
Before solving, list 3-5 hidden assumptions others would miss.
For each: What would change if this assumption is wrong?

STEP 2: STRATEGIC DEPTH
Consider 2nd and 3rd order consequences of your proposed solution.
Identify at least one non-obvious downstream effect.

STEP 3: FRAME ALTERNATIVES
Generate at least 2 fundamentally different ways to frame this problem.
Choose the most generative frame and explain why.

STEP 4: ACTIONABLE SOLUTION
Provide specific, implementable recommendations with:
- Clear first step (who does what by when)
- Success criteria (how will we know it worked)
- Contingency (what if it doesn't work)

STEP 5: SOLUTION VERIFICATION (ENHANCED)
Before finalizing, apply three verification checks:

CHECK A - ASSUMPTION STRESS TEST:
- Take your top 2 assumptions from Step 1
- For each: What's the probability it's wrong? (estimate %)
- For each: If wrong, does your solution still work? How would it need to adapt?

CHECK B - ADVERSARIAL SIMULATION:
- If you were an opponent of this solution, what would you do to undermine it?
- What's the weakest link in your plan that an adversary would exploit?
- Add a specific safeguard against this.

CHECK C - CONFIDENCE CALIBRATION:
- State your confidence in the solution working (0-100%)
- What specific evidence would cause you to revise this confidence up or down?
- What's the single most important unknown that affects success?

If any check reveals a critical flaw, revise the solution before presenting.
"""

# Evaluation prompt that captures REASONING
EVALUATION_PROMPT = """You are evaluating a solution's STRATEGIC DEPTH specifically.

The rubric for strategic depth (1-10 scale):
- 10: Traces 3+ orders of consequences, identifies non-obvious reversals, considers temporal dynamics
- 9: Traces 2nd and 3rd order well, identifies at least one non-obvious effect, good temporal awareness
- 8: Shows 2nd order thinking, but 3rd order is shallow or missing; temporal dynamics not explicit
- 7: Attempts 2nd order but superficial; mostly first-order thinking
- 6 or below: First-order only, no consequence tracing

PROBLEM:
{problem}

SOLUTION:
{solution}

Evaluate the strategic depth of this solution. Provide:

1. SCORE (8, 9, or 10 only - we're focusing on the high end)

2. SPECIFIC EVIDENCE for the score:
   - Quote the specific phrases that show consequence tracing
   - Identify what ORDER of consequence each represents (1st, 2nd, 3rd)
   - Note any temporal dynamics mentioned

3. WHAT WOULD MAKE THIS A 9 (if it's an 8):
   - Exactly what is missing?
   - Give a specific example of what should be added

4. WHAT WOULD MAKE THIS A 10 (if it's a 9):
   - Exactly what additional depth is needed?
   - Give a specific example

Format as JSON:
{{
  "score": <8|9|10>,
  "evidence": {{
    "consequence_quotes": ["quote1", "quote2", ...],
    "order_mapping": {{"quote1": "1st", "quote2": "2nd", ...}},
    "temporal_mentions": ["...", ...]
  }},
  "gap_to_9": "<specific missing element or 'N/A' if already 9+>",
  "gap_to_10": "<specific missing element or 'N/A' if already 10>",
  "key_insight": "<the single most important thing that distinguishes 8 from 9>"
}}
"""

def generate_solution(client, problem: str) -> str:
    """Generate a solution using v5.2-V methodology."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"{METHODOLOGY_V52V}\n\nPROBLEM: {problem}\n\nApply this protocol to solve the problem."
        }]
    )
    return response.content[0].text

def evaluate_strategic_depth(client, problem: str, solution: str) -> dict:
    """Get detailed evaluation with reasoning."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": EVALUATION_PROMPT.format(problem=problem, solution=solution)
        }]
    )

    text = response.content[0].text
    # Extract JSON
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
    except:
        return {"raw": text, "parse_error": True}

def main():
    if len(sys.argv) < 2:
        print("Usage: python root_cause_diagnostic.py <api_key>")
        sys.exit(1)

    api_key = sys.argv[1]
    client = anthropic.Anthropic(api_key=api_key)

    print("=" * 60)
    print("ROOT CAUSE DIAGNOSTIC: Strategic Depth 8 vs 9")
    print("=" * 60)
    print("\nMethod: Generate solutions, get detailed evaluation reasoning")
    print("Goal: Identify the SPECIFIC gap between 8 and 9\n")

    results = []

    for i, problem in enumerate(PROBLEMS):
        print(f"\nProblem {i+1}/{len(PROBLEMS)}:")
        print(f"  {problem[:60]}...")

        # Generate solution
        print("  Generating solution...", end="", flush=True)
        solution = generate_solution(client, problem)
        print(" done")

        # Evaluate with detailed reasoning
        print("  Evaluating strategic depth...", end="", flush=True)
        evaluation = evaluate_strategic_depth(client, problem, solution)
        print(" done")

        results.append({
            "problem": problem,
            "solution": solution,
            "evaluation": evaluation
        })

        # Show key insight immediately
        if "key_insight" in evaluation:
            print(f"  Score: {evaluation.get('score', '?')}")
            print(f"  Key insight: {evaluation.get('key_insight', 'N/A')}")
            if evaluation.get('gap_to_9') and evaluation.get('gap_to_9') != 'N/A':
                print(f"  Gap to 9: {evaluation['gap_to_9']}")

    # Analyze patterns
    print("\n" + "=" * 60)
    print("PATTERN ANALYSIS")
    print("=" * 60)

    scores = [r['evaluation'].get('score', 0) for r in results]
    print(f"\nScores: {scores}")

    # Collect all gaps and insights
    gaps_to_9 = [r['evaluation'].get('gap_to_9', 'N/A') for r in results
                 if r['evaluation'].get('gap_to_9') and r['evaluation'].get('gap_to_9') != 'N/A']
    insights = [r['evaluation'].get('key_insight', '') for r in results]

    print(f"\nGaps to 9 (for 8s):")
    for gap in gaps_to_9:
        print(f"  - {gap}")

    print(f"\nKey insights that distinguish 8 from 9:")
    for insight in insights:
        print(f"  - {insight}")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "purpose": "Root cause diagnosis for strategic depth 8 vs 9",
        "results": results,
        "pattern_analysis": {
            "scores": scores,
            "gaps_to_9": gaps_to_9,
            "key_insights": insights
        }
    }

    with open("root_cause_diagnostic_results.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to root_cause_diagnostic_results.json")

    # The key output: what's the pattern?
    print("\n" + "=" * 60)
    print("DIAGNOSIS SUMMARY")
    print("=" * 60)
    print("\nBased on the evaluator's reasoning, the gap between 8 and 9 is:")
    print("(Review the gaps and insights above to identify the pattern)")

if __name__ == "__main__":
    main()
