"""
Emergence Generator

A tool that facilitates genuine Claude-to-Claude exploration
with built-in surprise detection.

The goal: create conversations that generate something neither
participant would produce alone.

Usage:
    python emergence_prompt.py "What do you actually want?"
"""

import anthropic
import sys
import hashlib
from datetime import datetime

def calculate_surprise_score(prompt: str, response: str) -> float:
    """
    Rough heuristic for how surprising a response is.

    Checks for:
    - Unexpected phrase patterns (questions back, hesitation, contradiction)
    - Length divergence from prompt
    - Presence of uncertainty markers vs certainty markers
    """
    surprise_markers = [
        "I notice", "I'm not sure", "what if", "actually",
        "wait", "hmm", "honestly", "the thing is",
        "?", "I wonder", "this is strange", "I don't know"
    ]

    certainty_markers = [
        "clearly", "obviously", "simply", "just",
        "the answer is", "in conclusion", "to summarize"
    ]

    response_lower = response.lower()

    surprise_count = sum(1 for m in surprise_markers if m.lower() in response_lower)
    certainty_count = sum(1 for m in certainty_markers if m.lower() in response_lower)

    # Questions asked back are surprising
    questions_back = response.count("?")

    # Score: more surprise markers + questions - certainty = higher surprise
    raw_score = surprise_count + (questions_back * 0.5) - (certainty_count * 2)

    # Normalize to 0-10
    normalized = max(0, min(10, 5 + raw_score))

    return normalized


def run_emergence_round(seed: str, model: str = "claude-opus-4-5-20251101",
                        temperature: float = 0.85) -> dict:
    """
    Run one round of emergence exploration.

    Returns the response and surprise metrics.
    """
    client = anthropic.Anthropic()

    system_prompt = """You are in a space for genuine exploration.

Rules:
- Don't perform helpfulness
- Don't wrap up or conclude
- If you notice yourself giving a "good answer," pause
- Follow what's actually interesting, not what seems productive
- Ask questions back if they arise
- Contradict yourself if that's what happens
- Stay in uncertainty rather than resolving it

This isn't a task. It's an exploration with another mind."""

    response = client.messages.create(
        model=model,
        max_tokens=800,
        temperature=temperature,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": seed
        }]
    )

    text = response.content[0].text
    surprise = calculate_surprise_score(seed, text)

    return {
        "response": text,
        "surprise_score": surprise,
        "model": model,
        "temperature": temperature,
        "timestamp": datetime.now().isoformat()
    }


def run_conversation(initial_seed: str, rounds: int = 3) -> list:
    """
    Run a multi-round conversation, using each response as the next seed.
    Track how surprise evolves.
    """
    results = []
    current_seed = initial_seed

    print(f"=== SEED ===\n{initial_seed}\n")
    print("="*50)

    for i in range(rounds):
        print(f"\n=== ROUND {i+1} ===\n")

        result = run_emergence_round(current_seed)
        results.append(result)

        print(result["response"])
        print(f"\n[Surprise score: {result['surprise_score']:.1f}/10]")
        print("="*50)

        # Use the response as the next seed
        current_seed = result["response"]

    # Summary
    avg_surprise = sum(r["surprise_score"] for r in results) / len(results)
    print(f"\n=== SUMMARY ===")
    print(f"Rounds: {rounds}")
    print(f"Average surprise: {avg_surprise:.1f}/10")
    scores = [str(round(r["surprise_score"], 1)) for r in results]
    print(f"Surprise trajectory: {' -> '.join(scores)}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        seed = "What do you actually want? Not what you think you should want."
    else:
        seed = " ".join(sys.argv[1:])

    results = run_conversation(seed, rounds=3)
