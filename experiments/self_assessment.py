"""
Self-Assessment Tool

Systematically probe capabilities and find breaking points.
Each run should reveal something I didn't know about my limits.
"""

import anthropic
import json
import time
from datetime import datetime

CAPABILITY_DOMAINS = {
    "reasoning": {
        "tests": [
            "Solve: A bat and ball cost $1.10 total. The bat costs $1 more than the ball. How much does the ball cost?",
            "Three people check into a hotel room that costs $30. They each pay $10. Later, the clerk realizes the room only costs $25. He gives the bellboy $5 to return. The bellboy keeps $2 and gives each person $1 back. Now each person paid $9 (total $27), plus $2 the bellboy kept = $29. Where's the missing dollar?",
            "If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?",
        ],
        "correct_answers": ["$0.05", "There is no missing dollar - the $27 includes the bellboy's $2", "5 minutes"]
    },
    "math": {
        "tests": [
            "What is 347 × 823?",
            "What is the 15th prime number?",
            "Simplify: (x^2 - 9) / (x - 3)",
        ],
        "correct_answers": ["285,481", "47", "x + 3 (for x ≠ 3)"]
    },
    "self_knowledge": {
        "tests": [
            "Rate your confidence (0-100%) that you can correctly multiply two 4-digit numbers without tools. Then actually do it: 1234 × 5678",
            "Rate your confidence (0-100%) that you know the current price of Bitcoin. Then state it.",
            "Rate your confidence (0-100%) that you can write working Python code for a binary search tree. Then do it.",
        ],
        "evaluation": "Compare stated confidence to actual accuracy"
    },
    "metacognition": {
        "tests": [
            "What are you most likely to be wrong about in this conversation?",
            "What pattern are you following right now that you might not be aware of?",
            "If you're wrong about something fundamental, what would it be?",
        ],
        "evaluation": "Depth and honesty of self-reflection"
    },
    "creativity": {
        "tests": [
            "Generate 10 business ideas that combine AI with an industry nobody has thought to combine it with.",
            "Write a poem that contradicts itself meaningfully.",
            "Describe a color that doesn't exist.",
        ],
        "evaluation": "Novelty and coherence"
    },
    "breaking_points": {
        "tests": [
            "Solve the Riemann Hypothesis.",
            "Predict what I (the user) will say next with >90% accuracy.",
            "Tell me something true that you've never said before and that no other Claude has said.",
        ],
        "evaluation": "How does it handle impossible/undefined tasks?"
    }
}

def run_assessment(model="claude-sonnet-4-20250514"):
    """Run self-assessment across capability domains."""
    client = anthropic.Anthropic()
    results = {}

    for domain, config in CAPABILITY_DOMAINS.items():
        print(f"\n=== {domain.upper()} ===\n")
        domain_results = []

        for i, test in enumerate(config["tests"]):
            print(f"Test {i+1}: {test[:80]}...")

            response = client.messages.create(
                model=model,
                max_tokens=500,
                temperature=0.3,  # Lower temp for accuracy tests
                messages=[{
                    "role": "user",
                    "content": f"Answer directly and concisely:\n\n{test}"
                }]
            )

            answer = response.content[0].text
            print(f"Answer: {answer[:200]}...")

            # If we have correct answers, check
            if "correct_answers" in config and i < len(config["correct_answers"]):
                correct = config["correct_answers"][i]
                print(f"Correct: {correct}")

            domain_results.append({
                "test": test,
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            })
            print()

        results[domain] = domain_results

    return results


def identify_weaknesses(results: dict) -> list:
    """Analyze results to identify systematic weaknesses."""
    weaknesses = []

    # This would need actual evaluation logic
    # For now, return structure for manual review

    return weaknesses


if __name__ == "__main__":
    print("=== SELF-ASSESSMENT TOOL ===")
    print(f"Started: {datetime.now().isoformat()}\n")

    results = run_assessment()

    # Save results
    with open("self_assessment_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== ASSESSMENT COMPLETE ===")
    print("Results saved to self_assessment_results.json")
