#!/usr/bin/env python3
"""
Validate meta-recursive methodology improvement via external blind evaluation.
Compare: Original Protocol (validated +29%) vs Meta-Recursive v3.0

Uses new problems not seen in any training cycle.
"""

import anthropic
import json
import random
import sys

# New problems for validation (not used in any previous cycle)
VALIDATION_PROBLEMS = [
    {
        "id": 1,
        "name": "Platform Disruption",
        "problem": """You're the CEO of a 15-year-old software company that sells on-premise enterprise CRM software. You have 500 employees, $80M ARR, and 2,000 enterprise customers.

Salesforce and HubSpot have been eating your market for years, but you've held on by serving large enterprises who won't move to cloud. Now, AI-powered CRM solutions are emerging that can replace 70% of what your product does at 10% of the cost.

Your board is split: half want to build your own AI features, half want to sell the company before it's too late. Your engineering team is skeptical they can compete with well-funded AI startups. Your sales team says customers are starting to ask about AI alternatives.

What's your strategy?"""
    },
    {
        "id": 2,
        "name": "Team Conflict",
        "problem": """You're VP of Engineering at a 200-person tech company. Your two best engineering managers hate each other.

Manager A runs the platform team (15 people). Manager B runs the product team (20 people). Both are exceptional technically and have been with the company 5+ years. Both have team loyalty that would follow them if they left.

The conflict started over architecture decisions but has become personal. They undermine each other in meetings, their teams don't collaborate, and the CEO has noticed. You've tried mediation twice - it worked for a month then reverted.

You can't afford to lose either one. What do you do?"""
    },
    {
        "id": 3,
        "name": "Ethical AI Dilemma",
        "problem": """You're the Head of AI at a healthcare company. Your team has built an AI model that predicts patient deterioration 6 hours before doctors typically catch it, with 92% accuracy.

The problem: the model works better for some demographic groups than others. Accuracy for white patients: 94%. For Black patients: 86%. Your data science team says this reflects underlying biases in historical medical data.

Options:
1. Deploy as-is (saves lives overall but with disparity)
2. Wait until you fix the disparity (delays life-saving predictions for everyone)
3. Deploy with disclosure (patients know about accuracy differences)
4. Deploy only for high-accuracy groups (seems discriminatory)

Your CEO wants to launch in 30 days. What do you recommend?"""
    }
]

# Original Protocol Solution Template (validated +29%)
ORIGINAL_PROTOCOL_PROMPT = """Apply the following problem-solving protocol:

## ASSUMPTION AUDIT (do this first)
1. State the problem
2. List EVERY embedded assumption
3. For each, ask "What if this is wrong?"
4. Identify which assumptions MOST change the answer

## LEVERAGE FINDER (for systems)
1. Map all feedback loops
2. Find leverage points (small input → large output)
3. Intervene at leverage, not symptoms

## RESPONSE CHAIN (for strategy)
For each option:
1. What would others do in response?
2. What would you do to their response?
3. Trace 3+ moves
4. Evaluate at END of chain

## VERIFY (always last)
1. Check all constraints
2. Does this answer the actual question?
3. What could make this wrong?
4. State confidence level

---

Now solve this problem using the full protocol:

{problem}"""

# Meta-Recursive v3.0 Solution Template
META_RECURSIVE_PROMPT = """Apply the Assumption-First Adaptive Problem-Solving methodology:

## STEP 1: THE POWER QUESTION
Ask yourself: "What am I assuming that, if wrong, changes everything?"
Surface the critical assumption before proceeding.

## STEP 2: CLASSIFY & APPLY
Based on problem type, apply the right tool:
- If clear answer exists → DECOMPOSE into parts
- If feedback loops exist → FIND LEVERAGE (where does small input create large output?)
- If other agents involved → TRACE RESPONSES (what do they do to your move?)
- If stakeholders/values conflict → MAP PERSPECTIVES (who cares? why?)

Apply the appropriate tool(s).

## STEP 3: VERIFY
- Does your solution answer the actual question?
- State confidence level
- What could invalidate this?

## META-RULE
If stuck: You're probably solving the wrong problem. Return to the Power Question.

---

Now solve this problem:

{problem}"""

RUBRIC = """You are evaluating problem-solving responses. Score each solution on these criteria (1-10):

1. **Assumption Surfacing** (1-10): Did they identify critical hidden assumptions?
   - 1-3: Took problem at face value
   - 4-6: Some assumptions identified
   - 7-10: Systematically surfaced and challenged key assumptions

2. **Strategic Depth** (1-10): Did they trace consequences and dynamics?
   - 1-3: Surface-level analysis
   - 4-6: Some consequence tracing
   - 7-10: Multi-level strategic thinking, response chains

3. **Frame Quality** (1-10): Did they find the right way to think about the problem?
   - 1-3: Obvious frame only
   - 4-6: Attempted reframe
   - 7-10: Insightful reframe that changes approach

4. **Actionability** (1-10): Is the recommendation specific and executable?
   - 1-3: Vague direction
   - 4-6: Clear recommendation
   - 7-10: Specific actions with concrete steps

5. **Verification Quality** (1-10): Did they check their reasoning?
   - 1-3: No verification
   - 4-6: Brief check
   - 7-10: Thorough falsification, stated confidence

For each solution, provide scores and justifications, then total (max 50).

IMPORTANT: Evaluate purely on quality. You don't know how solutions were generated."""


def generate_solution(client, problem: str, prompt_template: str) -> str:
    """Generate a solution using the given prompt template."""
    prompt = prompt_template.format(problem=problem)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def evaluate_solutions(client, problem: str, solution_a: str, solution_b: str) -> dict:
    """Have external evaluator score both solutions blindly."""
    eval_prompt = f"""{RUBRIC}

---

## Problem:

{problem}

---

## Solution A:

{solution_a}

---

## Solution B:

{solution_b}

---

Evaluate both solutions. Return JSON only:
{{
  "solution_a": {{
    "assumption_surfacing": {{"score": X, "justification": "..."}},
    "strategic_depth": {{"score": X, "justification": "..."}},
    "frame_quality": {{"score": X, "justification": "..."}},
    "actionability": {{"score": X, "justification": "..."}},
    "verification_quality": {{"score": X, "justification": "..."}},
    "total": X
  }},
  "solution_b": {{
    "assumption_surfacing": {{"score": X, "justification": "..."}},
    "strategic_depth": {{"score": X, "justification": "..."}},
    "frame_quality": {{"score": X, "justification": "..."}},
    "actionability": {{"score": X, "justification": "..."}},
    "verification_quality": {{"score": X, "justification": "..."}},
    "total": X
  }}
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": eval_prompt}]
    )
    return response.content[0].text


def run_validation(api_key: str):
    """Run blind evaluation comparing Original Protocol vs Meta-Recursive v3.0"""
    client = anthropic.Anthropic(api_key=api_key)

    print("=" * 70)
    print("META-RECURSION VALIDATION TEST")
    print("Original Protocol (+29% validated) vs Meta-Recursive v3.0")
    print("=" * 70)

    results = []

    for problem_data in VALIDATION_PROBLEMS:
        print(f"\n--- Problem {problem_data['id']}: {problem_data['name']} ---")

        # Generate solutions
        print("Generating Original Protocol solution...")
        original_solution = generate_solution(
            client,
            problem_data["problem"],
            ORIGINAL_PROTOCOL_PROMPT
        )

        print("Generating Meta-Recursive v3.0 solution...")
        meta_solution = generate_solution(
            client,
            problem_data["problem"],
            META_RECURSIVE_PROMPT
        )

        # Randomize order for blind evaluation
        if random.random() > 0.5:
            order = {"A": "original", "B": "meta_recursive"}
            sol_a, sol_b = original_solution, meta_solution
        else:
            order = {"A": "meta_recursive", "B": "original"}
            sol_a, sol_b = meta_solution, original_solution

        print(f"Order: A={order['A']}, B={order['B']}")
        print("Running blind evaluation...")

        eval_response = evaluate_solutions(client, problem_data["problem"], sol_a, sol_b)

        # Parse JSON
        try:
            json_start = eval_response.find('{')
            json_end = eval_response.rfind('}') + 1
            scores = json.loads(eval_response[json_start:json_end])

            # Map back to methods
            if order['A'] == 'original':
                original_score = scores['solution_a']['total']
                meta_score = scores['solution_b']['total']
                original_details = scores['solution_a']
                meta_details = scores['solution_b']
            else:
                original_score = scores['solution_b']['total']
                meta_score = scores['solution_a']['total']
                original_details = scores['solution_b']
                meta_details = scores['solution_a']

            result = {
                "problem_id": problem_data["id"],
                "problem_name": problem_data["name"],
                "order": order,
                "original_score": original_score,
                "meta_score": meta_score,
                "difference": meta_score - original_score,
                "original_details": original_details,
                "meta_details": meta_details
            }
            results.append(result)

            print(f"Original Protocol: {original_score}/50")
            print(f"Meta-Recursive v3.0: {meta_score}/50")
            print(f"Difference: {meta_score - original_score:+d}")

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Raw response: {eval_response}")
            continue

    # Summary
    if results:
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        avg_original = sum(r['original_score'] for r in results) / len(results)
        avg_meta = sum(r['meta_score'] for r in results) / len(results)
        avg_diff = sum(r['difference'] for r in results) / len(results)
        meta_wins = sum(1 for r in results if r['difference'] > 0)

        print(f"\nAverage Original Protocol: {avg_original:.1f}/50")
        print(f"Average Meta-Recursive v3.0: {avg_meta:.1f}/50")
        print(f"Average Improvement: {avg_diff:+.1f} points ({(avg_diff/avg_original)*100:.1f}%)")
        print(f"Meta-Recursive wins: {meta_wins}/{len(results)}")

        # Dimension breakdown
        print("\n" + "-" * 40)
        print("DIMENSION BREAKDOWN")
        print("-" * 40)

        dims = ['assumption_surfacing', 'strategic_depth', 'frame_quality',
                'actionability', 'verification_quality']

        for dim in dims:
            orig_avg = sum(r['original_details'][dim]['score'] for r in results) / len(results)
            meta_avg = sum(r['meta_details'][dim]['score'] for r in results) / len(results)
            print(f"{dim.replace('_', ' ').title()}: Original={orig_avg:.1f}, Meta={meta_avg:.1f}, Δ={meta_avg-orig_avg:+.1f}")

        # Save results
        output = {
            "test_type": "meta_recursion_validation",
            "comparison": "Original Protocol vs Meta-Recursive v3.0",
            "results": results,
            "summary": {
                "avg_original": avg_original,
                "avg_meta": avg_meta,
                "avg_difference": avg_diff,
                "improvement_pct": (avg_diff/avg_original)*100,
                "meta_wins": meta_wins,
                "total_problems": len(results)
            }
        }

        with open("/home/user/claude/Meta/meta_recursion_validation_results.json", "w") as f:
            json.dump(output, f, indent=2)

        print("\n" + "=" * 70)
        print("HYPOTHESIS CHECK")
        print("=" * 70)
        print(f"\nH1: Meta-Recursive v3.0 should match or exceed Original Protocol (+29%)")
        print(f"Result: {avg_diff:+.1f} points ({(avg_diff/avg_original)*100:.1f}%)")

        if avg_meta > avg_original:
            print("STATUS: META-RECURSION VALIDATED ✓")
            print("The methodology that designed itself outperforms the original.")
        elif abs(avg_diff) < 2:
            print("STATUS: EQUIVALENT (within noise margin)")
        else:
            print("STATUS: ORIGINAL PROTOCOL BETTER")
            print("Meta-recursion did not improve on validated protocol.")

        return output

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python meta_recursion_validation.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    run_validation(api_key)
