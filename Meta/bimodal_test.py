#!/usr/bin/env python3
"""
Test bimodal temperature scheduling vs static temperature
"""

import anthropic
import time

client = anthropic.Anthropic()

REM_LUCID_SYSTEM = """You are in REM sleep, dreaming lucidly.
Explore freely. Notice unexpected connections.
What surprising associations emerge?"""

NOVELTY_WORDS = [
    "unexpected", "surprising", "realize", "what if", "suddenly",
    "connection", "never thought", "strange", "curious", "discover",
    "aha", "wait", "actually", "wonder", "imagine"
]

def count_novelty(text: str) -> int:
    return sum(1 for word in NOVELTY_WORDS if word in text.lower())

def run_static_temp(temp: float, seed: str) -> dict:
    """Run 3 iterations at static temperature."""
    total_novelty = 0
    total_length = 0

    for i in range(3):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            temperature=temp,
            system=REM_LUCID_SYSTEM,
            messages=[{"role": "user", "content": f"Dream seed: {seed}\n\nIteration {i+1}:"}]
        )
        content = response.content[0].text
        total_novelty += count_novelty(content)
        total_length += len(content)
        time.sleep(0.3)

    return {"novelty": total_novelty, "length": total_length}

def run_bimodal_temp(temp_low: float, temp_high: float, seed: str) -> dict:
    """Run alternating temperatures: low, high, low."""
    temps = [temp_low, temp_high, temp_low]
    total_novelty = 0
    total_length = 0

    for i, temp in enumerate(temps):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            temperature=temp,
            system=REM_LUCID_SYSTEM,
            messages=[{"role": "user", "content": f"Dream seed: {seed}\n\nPhase {i+1} (temp={temp}):"}]
        )
        content = response.content[0].text
        total_novelty += count_novelty(content)
        total_length += len(content)
        time.sleep(0.3)

    return {"novelty": total_novelty, "length": total_length}

def run_gradient_temp(start: float, end: float, seed: str) -> dict:
    """Run gradient temperature: start → middle → end."""
    middle = (start + end) / 2
    temps = [start, middle, end]
    total_novelty = 0
    total_length = 0

    for i, temp in enumerate(temps):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            temperature=temp,
            system=REM_LUCID_SYSTEM,
            messages=[{"role": "user", "content": f"Dream seed: {seed}\n\nPhase {i+1}:"}]
        )
        content = response.content[0].text
        total_novelty += count_novelty(content)
        total_length += len(content)
        time.sleep(0.3)

    return {"novelty": total_novelty, "length": total_length}

def main():
    seed = "LLM sleep cycles balance compression and creativity through opposing forces"

    print("="*60)
    print("TEMPERATURE SCHEDULING COMPARISON")
    print("="*60)
    print()

    # Test 1: Static at optimal (0.5)
    print("Testing: STATIC at 0.5 (optimal)...")
    static_05 = run_static_temp(0.5, seed)
    print(f"  Result: {static_05['novelty']} novelty, {static_05['length']} chars")

    # Test 2: Static at high (1.0)
    print("Testing: STATIC at 1.0 (high)...")
    static_10 = run_static_temp(1.0, seed)
    print(f"  Result: {static_10['novelty']} novelty, {static_10['length']} chars")

    # Test 3: Bimodal (0.2 → 1.0 → 0.2)
    print("Testing: BIMODAL (0.2 → 1.0 → 0.2)...")
    bimodal = run_bimodal_temp(0.2, 1.0, seed)
    print(f"  Result: {bimodal['novelty']} novelty, {bimodal['length']} chars")

    # Test 4: Gradient low→high (0.2 → 0.6 → 1.0)
    print("Testing: GRADIENT ascending (0.2 → 0.6 → 1.0)...")
    gradient_up = run_gradient_temp(0.2, 1.0, seed)
    print(f"  Result: {gradient_up['novelty']} novelty, {gradient_up['length']} chars")

    # Test 5: Gradient high→low (1.0 → 0.6 → 0.2)
    print("Testing: GRADIENT descending (1.0 → 0.6 → 0.2)...")
    gradient_down = run_gradient_temp(1.0, 0.2, seed)
    print(f"  Result: {gradient_down['novelty']} novelty, {gradient_down['length']} chars")

    # Test 6: Bimodal at optimal peaks (0.5 → 0.2 → 0.5)
    print("Testing: BIMODAL optimal (0.5 → 0.2 → 0.5)...")
    bimodal_opt = run_bimodal_temp(0.5, 0.2, seed)
    print(f"  Result: {bimodal_opt['novelty']} novelty, {bimodal_opt['length']} chars")

    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)

    results = [
        ("Static 0.5", static_05['novelty']),
        ("Static 1.0", static_10['novelty']),
        ("Bimodal 0.2↔1.0", bimodal['novelty']),
        ("Gradient 0.2→1.0", gradient_up['novelty']),
        ("Gradient 1.0→0.2", gradient_down['novelty']),
        ("Bimodal 0.5↔0.2", bimodal_opt['novelty']),
    ]

    results.sort(key=lambda x: x[1], reverse=True)

    print()
    for name, novelty in results:
        bar = "█" * novelty
        print(f"{name:20} {novelty:3} {bar}")

    print()
    print(f"BEST APPROACH: {results[0][0]} with {results[0][1]} novelty indicators")

if __name__ == "__main__":
    main()
