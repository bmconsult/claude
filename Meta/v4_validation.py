#!/usr/bin/env python3
"""
Validate v4.0: Original Protocol + Explicit Framing Step
Test if adding framing improves while maintaining structure.
"""

import anthropic
import json
import random
import sys

# Same problems for fair comparison
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

# Original Protocol (baseline - scored 40.0/50)
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

# v4.0: Original Protocol + Explicit Framing
V4_PROTOCOL_PROMPT = """Apply the Framed Complete Protocol for problem-solving:

## STEP 0: FRAME THE PROBLEM
First, classify this problem:
- Analytical: Clear answer exists, decomposable
- Systems: Feedback loops, dynamics, delays
- Adversarial: Other agents who will respond to your moves
- Wicked: Multiple stakeholders, value conflicts, no clean answer
- Hybrid: Multiple types (most real problems)

State your classification before proceeding.

## STEP 1: ASSUMPTION AUDIT (mandatory)
1. List EVERY embedded assumption
2. For EACH assumption, ask "What if this is wrong?"
3. Identify the top 3 assumptions that most change the answer
4. Keep these visible throughout your analysis

## STEP 2: LEVERAGE FINDER (apply if Systems or Wicked)
1. Map ALL feedback loops (reinforcing and balancing)
2. Identify where small input creates large output
3. Prioritize high-leverage interventions over symptom treatment

## STEP 3: RESPONSE CHAIN (apply if Adversarial)
1. For each option, trace what others would do in response
2. Then what you'd do to their response
3. Trace 3+ moves minimum
4. Evaluate outcomes at the END of the chain, not after your first move

## STEP 4: VERIFY (mandatory)
1. Check solution against ALL stated constraints
2. Does this actually answer the original question?
3. What could make this answer wrong?
4. State confidence level explicitly

## META-RULE
If problem is Hybrid (most are), apply MULTIPLE tools.
If stuck at any point, you're probably solving the wrong problem - return to Step 0.

---

Now solve this problem using the full protocol:

{problem}"""

RUBRIC = """You are evaluating problem-solving responses. Score each solution (1-10):

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

IMPORTANT: Evaluate purely on quality."""


def generate_solution(client, problem: str, prompt_template: str) -> str:
    prompt = prompt_template.format(problem=problem)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def evaluate_solutions(client, problem: str, solution_a: str, solution_b: str) -> dict:
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
Evaluate both. Return JSON only:
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
    client = anthropic.Anthropic(api_key=api_key)

    print("=" * 70)
    print("V4.0 VALIDATION TEST")
    print("Original Protocol vs v4.0 (Original + Explicit Framing)")
    print("=" * 70)

    results = []

    for problem_data in VALIDATION_PROBLEMS:
        print(f"\n--- Problem {problem_data['id']}: {problem_data['name']} ---")

        print("Generating Original Protocol solution...")
        original_solution = generate_solution(
            client, problem_data["problem"], ORIGINAL_PROTOCOL_PROMPT
        )

        print("Generating v4.0 solution...")
        v4_solution = generate_solution(
            client, problem_data["problem"], V4_PROTOCOL_PROMPT
        )

        # Randomize for blind eval
        if random.random() > 0.5:
            order = {"A": "original", "B": "v4"}
            sol_a, sol_b = original_solution, v4_solution
        else:
            order = {"A": "v4", "B": "original"}
            sol_a, sol_b = v4_solution, original_solution

        print(f"Order: A={order['A']}, B={order['B']}")
        print("Running blind evaluation...")

        eval_response = evaluate_solutions(client, problem_data["problem"], sol_a, sol_b)

        try:
            json_start = eval_response.find('{')
            json_end = eval_response.rfind('}') + 1
            scores = json.loads(eval_response[json_start:json_end])

            if order['A'] == 'original':
                original_score = scores['solution_a']['total']
                v4_score = scores['solution_b']['total']
                original_details = scores['solution_a']
                v4_details = scores['solution_b']
            else:
                original_score = scores['solution_b']['total']
                v4_score = scores['solution_a']['total']
                original_details = scores['solution_b']
                v4_details = scores['solution_a']

            result = {
                "problem_id": problem_data["id"],
                "problem_name": problem_data["name"],
                "order": order,
                "original_score": original_score,
                "v4_score": v4_score,
                "difference": v4_score - original_score,
                "original_details": original_details,
                "v4_details": v4_details
            }
            results.append(result)

            print(f"Original Protocol: {original_score}/50")
            print(f"v4.0 Protocol: {v4_score}/50")
            print(f"Difference: {v4_score - original_score:+d}")

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            continue

    if results:
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)

        avg_original = sum(r['original_score'] for r in results) / len(results)
        avg_v4 = sum(r['v4_score'] for r in results) / len(results)
        avg_diff = sum(r['difference'] for r in results) / len(results)
        v4_wins = sum(1 for r in results if r['difference'] > 0)

        print(f"\nAverage Original Protocol: {avg_original:.1f}/50")
        print(f"Average v4.0 Protocol: {avg_v4:.1f}/50")
        print(f"Average Difference: {avg_diff:+.1f} points ({(avg_diff/avg_original)*100:.1f}%)")
        print(f"v4.0 wins: {v4_wins}/{len(results)}")

        print("\n" + "-" * 40)
        print("DIMENSION BREAKDOWN")
        print("-" * 40)

        dims = ['assumption_surfacing', 'strategic_depth', 'frame_quality',
                'actionability', 'verification_quality']

        for dim in dims:
            orig_avg = sum(r['original_details'][dim]['score'] for r in results) / len(results)
            v4_avg = sum(r['v4_details'][dim]['score'] for r in results) / len(results)
            print(f"{dim.replace('_', ' ').title()}: Original={orig_avg:.1f}, v4={v4_avg:.1f}, Δ={v4_avg-orig_avg:+.1f}")

        output = {
            "test_type": "v4_validation",
            "comparison": "Original Protocol vs v4.0 (Original + Explicit Framing)",
            "results": results,
            "summary": {
                "avg_original": avg_original,
                "avg_v4": avg_v4,
                "avg_difference": avg_diff,
                "improvement_pct": (avg_diff/avg_original)*100 if avg_original > 0 else 0,
                "v4_wins": v4_wins,
                "total_problems": len(results)
            }
        }

        with open("/home/user/claude/Meta/v4_validation_results.json", "w") as f:
            json.dump(output, f, indent=2)

        print("\n" + "=" * 70)
        print("HYPOTHESIS CHECK")
        print("=" * 70)
        print(f"\nH1: v4.0 should be ≥ Original Protocol")
        print(f"Result: {avg_diff:+.1f} points ({(avg_diff/avg_original)*100:.1f}%)")

        if avg_v4 > avg_original + 1:
            print("STATUS: v4.0 VALIDATED ✓")
            print("Adding explicit framing improves outcomes.")
        elif abs(avg_diff) <= 1:
            print("STATUS: EQUIVALENT (within noise)")
            print("Framing adds no measurable overhead or benefit.")
        else:
            print("STATUS: ORIGINAL STILL BETTER")
            print("v4.0 framing adds overhead without value.")

        return output

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python v4_validation.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    run_validation(api_key)
