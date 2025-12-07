#!/usr/bin/env python3
"""
Rigorous temperature validation - more iterations, statistical analysis
"""

import anthropic
import time
import statistics
from collections import defaultdict

client = anthropic.Anthropic()

REM_PROMPT = """You are in REM sleep, dreaming lucidly.
What unexpected connections appear? Let images arise. Note what surprises you."""

NOVELTY_WORDS = [
    "unexpected", "surprising", "realize", "what if", "suddenly",
    "connection", "never thought", "strange", "curious", "discover",
    "aha", "wait", "actually", "wonder", "imagine"
]

def count_novelty(text: str) -> int:
    return sum(1 for word in NOVELTY_WORDS if word in text.lower())

def run_test(temp: float, seed: str) -> int:
    """Single test run, returns novelty count."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        temperature=temp,
        system=REM_PROMPT,
        messages=[{"role": "user", "content": f"Dream seed: {seed}"}]
    )
    return count_novelty(response.content[0].text)

def main():
    seeds = [
        "LLM sleep cycles consolidate context",
        "Temperature controls exploration vs exploitation",
        "Phases balance compression and creativity",
        "Neural networks dream during training",
        "Memory consolidation during offline processing",
    ]

    temperatures = [0.3, 0.5, 0.7, 1.0]
    runs_per_temp = 10  # 10 runs × 5 seeds = 50 data points per temp

    print("="*70)
    print("RIGOROUS TEMPERATURE VALIDATION")
    print(f"Testing {len(temperatures)} temps × {runs_per_temp} runs × {len(seeds)} seeds")
    print(f"Total API calls: {len(temperatures) * runs_per_temp * len(seeds)}")
    print("="*70)
    print()

    results = defaultdict(list)

    for temp in temperatures:
        print(f"\nTesting temperature {temp}...")
        for run in range(runs_per_temp):
            for seed in seeds:
                novelty = run_test(temp, seed)
                results[temp].append(novelty)
                time.sleep(0.2)  # Rate limiting
            print(f"  Run {run+1}/{runs_per_temp} complete")

    # Statistical analysis
    print("\n" + "="*70)
    print("STATISTICAL ANALYSIS")
    print("="*70)

    stats = {}
    for temp in temperatures:
        data = results[temp]
        stats[temp] = {
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data),
            "min": min(data),
            "max": max(data),
            "n": len(data),
        }

    print(f"\n{'Temp':<8} {'Mean':<8} {'Median':<8} {'StdDev':<8} {'Min':<6} {'Max':<6} {'N':<6}")
    print("-"*56)

    for temp in temperatures:
        s = stats[temp]
        print(f"{temp:<8} {s['mean']:<8.2f} {s['median']:<8.1f} {s['stdev']:<8.2f} {s['min']:<6} {s['max']:<6} {s['n']:<6}")

    # Find winner
    best_temp = max(temperatures, key=lambda t: stats[t]['mean'])
    print(f"\nBest temperature by mean: {best_temp} ({stats[best_temp]['mean']:.2f})")

    # Confidence intervals (rough)
    print("\n95% Confidence Intervals (mean ± 1.96*SE):")
    for temp in temperatures:
        s = stats[temp]
        se = s['stdev'] / (s['n'] ** 0.5)
        ci_low = s['mean'] - 1.96 * se
        ci_high = s['mean'] + 1.96 * se
        print(f"  Temp {temp}: [{ci_low:.2f}, {ci_high:.2f}]")

    # Check for overlapping CIs
    print("\nOverlap analysis:")
    for i, t1 in enumerate(temperatures):
        for t2 in temperatures[i+1:]:
            s1, s2 = stats[t1], stats[t2]
            se1 = s1['stdev'] / (s1['n'] ** 0.5)
            se2 = s2['stdev'] / (s2['n'] ** 0.5)
            ci1_high = s1['mean'] + 1.96 * se1
            ci2_low = s2['mean'] - 1.96 * se2
            ci1_low = s1['mean'] - 1.96 * se1
            ci2_high = s2['mean'] + 1.96 * se2

            overlaps = not (ci1_high < ci2_low or ci2_high < ci1_low)
            diff = abs(s1['mean'] - s2['mean'])
            print(f"  {t1} vs {t2}: diff={diff:.2f}, overlapping CIs: {overlaps}")

    # Distribution visualization
    print("\n" + "="*70)
    print("DISTRIBUTION (novelty counts)")
    print("="*70)

    for temp in temperatures:
        data = results[temp]
        counts = defaultdict(int)
        for v in data:
            counts[v] += 1

        print(f"\nTemp {temp}:")
        for i in range(max(data) + 1):
            bar = "█" * counts[i]
            print(f"  {i}: {bar} ({counts[i]})")

if __name__ == "__main__":
    main()
