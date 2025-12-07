#!/usr/bin/env python3
"""
Deep temperature testing - finding the optimal REM temperature
"""

import anthropic
import time
import json
from collections import defaultdict

client = anthropic.Anthropic()

REM_LUCID_SYSTEM = """You are in REM sleep, dreaming. Dreams can be lucid.
You're aware you're dreaming. Explore freely while noticing connections.
What unexpected connections appear between the concept and distant domains?
Let images arise. Follow them. Note what surprises you."""

NOVELTY_WORDS = [
    "unexpected", "surprising", "realize", "what if", "suddenly",
    "connection", "never thought", "strange", "curious", "discover",
    "aha", "wait", "actually", "hmm", "wonder", "imagine"
]

NOISE_WORDS = [
    "I think", "probably", "maybe", "perhaps", "I'm not sure",
    "generally", "typically", "usually", "obviously"
]

def analyze_output(text: str) -> dict:
    """Analyze output for novelty indicators."""
    text_lower = text.lower()

    novelty_count = sum(1 for word in NOVELTY_WORDS if word in text_lower)
    noise_count = sum(1 for word in NOISE_WORDS if word in text_lower)

    # Count metaphors/imagery (rough heuristic)
    imagery_words = ["like", "as if", "imagine", "picture", "see", "vision"]
    imagery_count = sum(1 for word in imagery_words if word in text_lower)

    # Sentence variety (unique sentence starters)
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    unique_starters = len(set(s.split()[0] if s.split() else "" for s in sentences))

    return {
        "length": len(text),
        "novelty_count": novelty_count,
        "noise_count": noise_count,
        "imagery_count": imagery_count,
        "sentence_variety": unique_starters,
        "sentences": len(sentences),
        "signal_ratio": novelty_count / max(noise_count, 1)
    }

def test_temperature(temp: float, seed: str, runs: int = 3) -> list:
    """Test a specific temperature multiple times."""
    results = []

    for i in range(runs):
        start = time.time()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            temperature=temp,
            system=REM_LUCID_SYSTEM,
            messages=[{"role": "user", "content": f"Dream seed: {seed}\n\nDream:"}]
        )
        duration = (time.time() - start) * 1000

        content = response.content[0].text
        analysis = analyze_output(content)
        analysis["duration_ms"] = duration
        analysis["content"] = content
        results.append(analysis)

        time.sleep(0.5)  # Rate limiting

    return results

def main():
    seed = """
    LLM sleep cycles consolidate context through phases.
    N3 and REM are opposing forces - anti-collapse vs anti-rigidity.
    Temperature controls the exploration/exploitation balance.
    """

    # Test fine-grained temperature range
    temperatures = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    print("="*70)
    print("DEEP TEMPERATURE ANALYSIS")
    print("="*70)
    print(f"Testing {len(temperatures)} temperatures x 3 runs each")
    print()

    all_results = {}

    for temp in temperatures:
        print(f"Testing temperature {temp}...")
        results = test_temperature(temp, seed, runs=3)
        all_results[temp] = results

        avg_novelty = sum(r["novelty_count"] for r in results) / len(results)
        avg_signal = sum(r["signal_ratio"] for r in results) / len(results)
        avg_imagery = sum(r["imagery_count"] for r in results) / len(results)

        print(f"  Avg novelty: {avg_novelty:.1f} | Signal ratio: {avg_signal:.2f} | Imagery: {avg_imagery:.1f}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY - OPTIMAL TEMPERATURE ANALYSIS")
    print("="*70)

    print(f"\n{'Temp':<6} {'Novelty':<10} {'Signal':<10} {'Imagery':<10} {'Best Run'}")
    print("-"*50)

    best_temp = None
    best_score = 0

    for temp in temperatures:
        results = all_results[temp]
        avg_novelty = sum(r["novelty_count"] for r in results) / len(results)
        avg_signal = sum(r["signal_ratio"] for r in results) / len(results)
        avg_imagery = sum(r["imagery_count"] for r in results) / len(results)
        best_run = max(r["novelty_count"] for r in results)

        # Composite score
        score = avg_novelty * 2 + avg_signal + avg_imagery
        if score > best_score:
            best_score = score
            best_temp = temp

        print(f"{temp:<6} {avg_novelty:<10.1f} {avg_signal:<10.2f} {avg_imagery:<10.1f} {best_run}")

    print(f"\nOPTIMAL TEMPERATURE: {best_temp} (composite score: {best_score:.2f})")

    # Show best outputs
    print("\n" + "="*70)
    print("SAMPLE OUTPUTS AT DIFFERENT TEMPERATURES")
    print("="*70)

    for temp in [0.3, 0.5, 0.7, 1.0]:
        print(f"\n--- Temperature {temp} ---")
        print(all_results[temp][0]["content"][:300] + "...")

if __name__ == "__main__":
    main()
