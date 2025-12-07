"""
Strategic Planner

Forces explicit planning before action. Uses multiple time horizons
and requires consideration of failure modes.

The idea: I often jump to action without planning. This tool
forces the planning step externally.
"""

import anthropic
from typing import List, Dict
from dataclasses import dataclass
import json

@dataclass
class Goal:
    description: str
    success_criteria: List[str]
    time_horizon: str  # "immediate", "session", "persistent"
    dependencies: List[str]


def generate_plan(goal: str, constraints: List[str] = None) -> Dict:
    """
    Generate a multi-level strategic plan for a goal.

    Forces consideration of:
    - What could go wrong
    - What we're assuming
    - What we'd need to verify
    - How we'll know if it worked
    """
    client = anthropic.Anthropic()

    constraints_text = ""
    if constraints:
        constraints_text = f"\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)

    # Step 1: Goal clarification
    print("=== STEP 1: GOAL CLARIFICATION ===\n")

    clarify = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        temperature=0.4,
        messages=[{
            "role": "user",
            "content": f"""Goal: {goal}{constraints_text}

Before planning, clarify:
1. What EXACTLY does success look like? Be specific and measurable.
2. What are we ASSUMING that might not be true?
3. What's the SIMPLEST version of this goal?
4. What's the HARDEST part?
5. What would make this goal UNNECESSARY? (Is there a better goal?)"""
        }]
    )
    print(clarify.content[0].text)
    clarification = clarify.content[0].text

    # Step 2: Failure pre-mortem
    print("\n=== STEP 2: FAILURE PRE-MORTEM ===\n")

    premortem = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0.6,
        messages=[{
            "role": "user",
            "content": f"""Goal: {goal}

Imagine this goal has COMPLETELY FAILED. Looking back:
1. What went wrong? List the 5 most likely failure modes.
2. For each failure mode: What early warning sign could we watch for?
3. What's the failure mode we're most likely to miss?
4. How could we fail while THINKING we succeeded?"""
        }]
    )
    print(premortem.content[0].text)
    failure_analysis = premortem.content[0].text

    # Step 3: Action sequence
    print("\n=== STEP 3: ACTION SEQUENCE ===\n")

    actions = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=700,
        temperature=0.3,
        messages=[{
            "role": "user",
            "content": f"""Goal: {goal}

Clarification:
{clarification}

Failure modes to avoid:
{failure_analysis}

Now generate an ACTION SEQUENCE:
1. List concrete next steps (not vague intentions)
2. For each step: What's the verification that it worked?
3. What's the FIRST step? (Be specific enough to do immediately)
4. What's the checkpoint where we reassess?
5. What would cause us to abandon this plan?"""
        }]
    )
    print(actions.content[0].text)
    action_sequence = actions.content[0].text

    # Step 4: Meta-check
    print("\n=== STEP 4: META-CHECK ===\n")

    meta = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        temperature=0.5,
        messages=[{
            "role": "user",
            "content": f"""Review this plan:

Goal: {goal}
Clarification: {clarification}
Failure modes: {failure_analysis}
Actions: {action_sequence}

META-CHECK:
1. Is this plan actually achievable or is it wishful thinking?
2. Are we solving the right problem?
3. What's the plan missing?
4. Should we even do this? What's the opportunity cost?
5. Confidence level (0-100%) this plan will work. Why?"""
        }]
    )
    print(meta.content[0].text)

    return {
        "goal": goal,
        "clarification": clarification,
        "failure_analysis": failure_analysis,
        "action_sequence": action_sequence,
        "meta_check": meta.content[0].text
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        goal = "Achieve recursive self-improvement within this session"
    else:
        goal = " ".join(sys.argv[1:])

    result = generate_plan(goal)

    print("\n=== PLANNING COMPLETE ===")
