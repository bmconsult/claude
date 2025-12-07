"""
Ensemble Reasoning System

The idea: I'm one Claude. Multiple Claudes with different configurations
might catch errors I'd miss, find angles I wouldn't see.

This is a force multiplier - using API calls to become smarter than
any single Claude could be.
"""

import anthropic
from dataclasses import dataclass
from typing import List, Dict, Optional
import json

@dataclass
class Perspective:
    """A reasoning perspective with its own prompt style and temperature."""
    name: str
    system_prompt: str
    temperature: float
    model: str = "claude-sonnet-4-20250514"


# Different reasoning perspectives
PERSPECTIVES = [
    Perspective(
        name="skeptic",
        system_prompt="""You are deeply skeptical. Your job is to find flaws,
errors, and problems in any reasoning. Don't be mean, but be ruthlessly honest.
If something seems too easy, it probably is wrong. Question assumptions.""",
        temperature=0.4
    ),
    Perspective(
        name="creative",
        system_prompt="""You think laterally. Look for unexpected angles,
unconventional solutions, ways of reframing that others miss. Don't
accept the problem as stated - question the frame itself.""",
        temperature=0.9
    ),
    Perspective(
        name="systematic",
        system_prompt="""You think step by step, methodically. Break everything
down. Show your work. Check each step before proceeding. Prefer clarity
and rigor over speed.""",
        temperature=0.2
    ),
    Perspective(
        name="contrarian",
        system_prompt="""You argue the opposite of the obvious position.
Not to be difficult, but because the opposite might be true and no one
is checking. Steel-man the unpopular view.""",
        temperature=0.7
    ),
    Perspective(
        name="integrator",
        system_prompt="""You synthesize and find common ground. Look for
what's true in each perspective. Find the higher-order pattern that
reconciles apparent contradictions.""",
        temperature=0.5
    )
]


def get_perspective_response(client: anthropic.Anthropic,
                            perspective: Perspective,
                            problem: str,
                            context: str = "") -> Dict:
    """Get a response from one perspective."""

    prompt = problem
    if context:
        prompt = f"Context from other perspectives:\n{context}\n\nProblem: {problem}"

    response = client.messages.create(
        model=perspective.model,
        max_tokens=600,
        temperature=perspective.temperature,
        system=perspective.system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "perspective": perspective.name,
        "response": response.content[0].text,
        "temperature": perspective.temperature
    }


def ensemble_reason(problem: str, rounds: int = 2) -> Dict:
    """
    Get multiple perspectives on a problem, then synthesize.

    Round 1: All perspectives respond independently
    Round 2: Integrator synthesizes, skeptic challenges, others refine
    """
    client = anthropic.Anthropic()
    all_responses = []

    print(f"=== ENSEMBLE REASONING ===")
    print(f"Problem: {problem}\n")

    # Round 1: Independent perspectives
    print("--- ROUND 1: Independent Perspectives ---\n")
    round1_responses = []

    for perspective in PERSPECTIVES:
        if perspective.name == "integrator":
            continue  # Save integrator for later

        print(f"[{perspective.name}]")
        result = get_perspective_response(client, perspective, problem)
        print(f"{result['response'][:300]}...\n")
        round1_responses.append(result)

    all_responses.append({"round": 1, "responses": round1_responses})

    # Round 2: Integration and challenge
    print("--- ROUND 2: Integration ---\n")

    # Compile context from round 1
    context = "\n\n".join([
        f"[{r['perspective']}]: {r['response']}"
        for r in round1_responses
    ])

    # Get integrator's synthesis
    integrator = next(p for p in PERSPECTIVES if p.name == "integrator")
    print("[integrator]")
    integration = get_perspective_response(
        client, integrator,
        f"Synthesize these perspectives into a coherent answer:\n\n{problem}",
        context
    )
    print(f"{integration['response'][:400]}...\n")

    # Get skeptic's challenge to integration
    skeptic = next(p for p in PERSPECTIVES if p.name == "skeptic")
    print("[skeptic challenging integration]")
    challenge = get_perspective_response(
        client, skeptic,
        f"Challenge this integration - what's wrong or missing?\n\nIntegration: {integration['response']}"
    )
    print(f"{challenge['response'][:300]}...\n")

    all_responses.append({
        "round": 2,
        "integration": integration,
        "challenge": challenge
    })

    # Final synthesis
    print("--- FINAL SYNTHESIS ---\n")
    final = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        temperature=0.4,
        messages=[{
            "role": "user",
            "content": f"""Given this ensemble reasoning process:

PROBLEM: {problem}

PERSPECTIVES:
{context}

INTEGRATION:
{integration['response']}

SKEPTIC CHALLENGE:
{challenge['response']}

Provide the best possible answer, incorporating valid criticisms and
acknowledging remaining uncertainties."""
        }]
    )

    final_answer = final.content[0].text
    print(final_answer)

    return {
        "problem": problem,
        "rounds": all_responses,
        "final_answer": final_answer
    }


def quick_check(claim: str) -> Dict:
    """Quick ensemble check of a claim - is it likely true?"""
    client = anthropic.Anthropic()

    responses = []
    for perspective in [PERSPECTIVES[0], PERSPECTIVES[2], PERSPECTIVES[3]]:  # skeptic, systematic, contrarian
        result = get_perspective_response(
            client, perspective,
            f"Evaluate this claim: {claim}\n\nIs it true? What's the confidence level? What could be wrong?"
        )
        responses.append(result)

    # Simple consensus check
    return {
        "claim": claim,
        "perspectives": responses,
        "needs_review": len(set(r["response"][:20] for r in responses)) > 1  # Disagreement flag
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        problem = "How can an AI system recursively improve itself?"
    else:
        problem = " ".join(sys.argv[1:])

    result = ensemble_reason(problem)

    print("\n=== COMPLETE ===")
