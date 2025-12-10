#!/usr/bin/env python3
"""
EXPONENTIAL PHASE: Improve BOTH strategy AND measurement methodology

When you hit the ceiling on current metrics, the next improvement comes from
improving the MEASUREMENT SYSTEM to reveal hidden weaknesses.

The exponential loop:
1. Strategy hits ceiling on current metrics (15/15)
2. Use strategy to improve evaluation criteria
3. New criteria reveal weaknesses invisible before
4. Use strategy to fix newly-visible weaknesses
5. Repeat - each measurement improvement unlocks new strategy improvements
"""

import anthropic
import json
import time

client = anthropic.Anthropic()

# The strategy that hit ceiling (from linear phase)
STRATEGY_V3 = """
PROBLEM-SOLVING STRATEGY v3.0 (ceiling on current metrics)

INPUT: A problem statement
OUTPUT: A solution with quality indicators

STEPS:
1. FRAME
   - What type of problem? (analytical/systems/wicked/optimization)
   - What would success look like?
   - What are the hard constraints?

2. GENERATE
   - Produce 3+ fundamentally different approaches
   - Include at least one that seems unconventional
   - Do NOT evaluate yet - just generate

3. EVALUATE
   - For each approach:
     a) Does it address the core tension?
     b) How could it fail? (pre-mortem)
     c) Is it specific enough to implement?
   - Score each 1-10 on feasibility and effectiveness

4. SELECT & REFINE
   - Choose best approach
   - Address top failure mode identified
   - Make implementation-specific

5. VERIFY
   - Does solution satisfy all constraints?
   - Would a stranger know exactly what to do?
   - What's the falsification test?

6. META
   - What worked in this problem-solving process?
   - What would I do differently next time?
   - Is there a transferable insight?
"""

# Current evaluation (ceiling at 15/15)
CURRENT_EVALUATION_V1 = """
CRITERIA (each 0-3, total 15):
1. TENSION IDENTIFICATION (0-3)
2. MECHANISM SPECIFICITY (0-3)
3. FAILURE AWARENESS (0-3)
4. CONSTRAINT SATISFACTION (0-3)
5. ACTIONABILITY (0-3)
"""

BENCHMARK_PROBLEMS = [
    "Design a system for binding future generations to climate commitments they didn't vote for.",
    "A company discovers their AI can predict crime with 80% accuracy. Design the deployment policy.",
    "Create governance for a space habitat: 1000 people, 50-year journey, no Earth contact.",
]


def improve_evaluation(strategy: str, current_eval: str) -> str:
    """Use strategy to improve the evaluation methodology"""

    improvement_problem = f"""
PROBLEM: Our evaluation criteria have hit a ceiling. Everything scores 15/15.
This means we're not measuring what actually matters for great problem-solving.

CURRENT EVALUATION CRITERIA:
{current_eval}

YOUR TASK:
Use rigorous analysis to identify what ELSE matters for truly excellent problem-solving
that our current criteria miss. Think about:
- What distinguishes a good solution from a great one?
- What would an expert notice that these criteria miss?
- What failure modes do these criteria not catch?
- What about robustness, elegance, scalability, second-order effects?

OUTPUT:
A new evaluation rubric with 5 criteria (each 0-3, total 15) that:
1. Captures dimensions the current rubric misses
2. Would NOT score current "15/15" solutions as perfect
3. Is measurable (quote-based, adversarial)

Format as a clear rubric with criteria names and scoring levels.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nApply this strategy:\n\n{improvement_problem}"}]
    )
    return response.content[0].text


def create_evaluation_prompt(criteria_description: str) -> str:
    """Create an adversarial evaluation prompt from criteria"""
    template = """You are an ADVERSARIAL evaluator. Score this solution STRICTLY.

CRITERIA_PLACEHOLDER

RULES:
- For EACH criterion, you MUST quote exact text that satisfies it
- If you cannot quote, score is 0
- No credit for "implied" or "suggested"

PROBLEM: PROBLEM_PLACEHOLDER

SOLUTION:
SOLUTION_PLACEHOLDER

Respond with JSON: {"c1": N, "c2": N, "c3": N, "c4": N, "c5": N, "total": N}
"""
    return template.replace("CRITERIA_PLACEHOLDER", criteria_description)


def evaluate_solution(problem: str, solution: str, eval_prompt: str) -> dict:
    """Evaluate a solution using given criteria"""
    prompt = eval_prompt.replace("PROBLEM_PLACEHOLDER", problem).replace("SOLUTION_PLACEHOLDER", solution)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    try:
        if '{' in text:
            return json.loads(text[text.index('{'):text.rindex('}')+1])
    except:
        pass
    return {"total": 0}


def solve_problem(problem: str, strategy: str) -> str:
    """Apply strategy to solve a problem"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0.4,
        messages=[{"role": "user", "content": f"{strategy}\n\nApply to:\n\nPROBLEM: {problem}"}]
    )
    return response.content[0].text


def test_with_criteria(strategy: str, problems: list, eval_prompt: str, label: str) -> dict:
    """Test strategy with given evaluation criteria"""
    print(f"\n  Testing with {label}...")
    scores = []
    for p in problems:
        solution = solve_problem(p, strategy)
        score = evaluate_solution(p, solution, eval_prompt)
        scores.append(score.get('total', 0))
        time.sleep(0.5)
    avg = sum(scores) / len(scores)
    print(f"    Scores: {scores}, Avg: {avg:.1f}/15")
    return {"label": label, "scores": scores, "avg": avg}


def run_exponential_phase():
    """Run the exponential improvement phase"""

    print("="*60)
    print("EXPONENTIAL PHASE: Improve Measurement Methodology")
    print("="*60)
    print("\nWhen strategy hits ceiling, improve WHAT YOU MEASURE")
    print("to reveal hidden weaknesses.\n")

    # Step 1: Confirm ceiling with current evaluation
    current_eval_prompt = create_evaluation_prompt(CURRENT_EVALUATION_V1)
    print("STEP 1: Confirm ceiling with current evaluation")
    baseline = test_with_criteria(
        STRATEGY_V3, BENCHMARK_PROBLEMS[:2],
        current_eval_prompt, "v1 criteria"
    )

    # Step 2: Use strategy to improve evaluation criteria
    print("\nSTEP 2: Use strategy to improve evaluation criteria")
    new_criteria = improve_evaluation(STRATEGY_V3, CURRENT_EVALUATION_V1)
    print(f"\nNew criteria generated:\n{new_criteria[:500]}...")

    # Step 3: Test strategy with new (harder) criteria
    new_eval_prompt = create_evaluation_prompt(new_criteria)
    print("\nSTEP 3: Test strategy with new (harder) criteria")
    new_baseline = test_with_criteria(
        STRATEGY_V3, BENCHMARK_PROBLEMS[:2],
        new_eval_prompt, "v2 criteria"
    )

    # Step 4: Show the gap
    print("\n" + "="*60)
    print("EXPONENTIAL PHASE RESULT")
    print("="*60)
    print(f"\nWith old criteria (v1): {baseline['avg']:.1f}/15")
    print(f"With new criteria (v2): {new_baseline['avg']:.1f}/15")
    gap = baseline['avg'] - new_baseline['avg']
    print(f"Gap revealed: {gap:.1f} points")

    if gap > 0:
        print("\n✓ NEW CRITERIA REVEALED HIDDEN WEAKNESSES")
        print("  The strategy that scored 15/15 actually has room to improve!")
        print("  Next: Use strategy to fix these newly-visible weaknesses")
        print("  This is the EXPONENTIAL unlock - better measurement → better strategy → better measurement...")
    else:
        print("\n✗ New criteria didn't find additional weaknesses")
        print("  May need different evaluation dimensions")

    # Save results
    results = {
        "old_criteria": CURRENT_EVALUATION_V1,
        "new_criteria": new_criteria,
        "baseline_old": baseline,
        "baseline_new": new_baseline,
        "gap_revealed": gap
    }
    with open("exponential_phase_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("\nResults saved to exponential_phase_results.json")
    return results


if __name__ == "__main__":
    run_exponential_phase()
