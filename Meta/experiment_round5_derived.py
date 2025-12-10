#!/usr/bin/env python3
"""
ROUND 5: Generate NEW attention targets from mechanism understanding

EXPONENTIAL IMPROVEMENT DEMONSTRATED:
- Round 1-3: Testing WHAT works
- Round 4: Testing WHY (mechanism = attention-steering)
- Round 5: GENERATING new interventions from mechanism understanding

Since attention-steering is the mechanism, we can DERIVE new targets:
1. Temporal (short→long term reversal)
2. Scale (small→large reversal)
3. Assumptions (hidden requirements)
4. Information (who knows what)

TEST: Stacked attention targets vs single target
PREDICTION: More targets = higher scores (compounding confirmed in R4)
"""

import anthropic
import json
from datetime import datetime
import os
import statistics

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Same extreme problems
EXTREME_PROBLEMS = [
    "Design a global governance system for AGI that prevents monopolization, doesn't require trust, adapts faster than the tech, remains legitimate when AGI outthinks overseers, and handles transition.",
    "Create a constitution for a Mars colony: 100 people initially scaling to 1M, 20-min delay to Earth, genetic divergence, prevents mutual exploitation, manages survival resources.",
    "Design education for 2050: AI passes all tests, 120+ lifespan, information free but wisdom scarce, credentials meaningless, human advantage unclear.",
    "A consciousness upload destroys the brain, upload claims identity, religious groups say murder, upload behaves identically, can run 1000x faster. Design ethics, law, transition.",
    "Create monetary system for post-scarcity: AI produces goods at zero cost, labor optional, status competition exists, some things scarce, meaning must come from somewhere.",
    "First contact protocol: 50-year message delay, response reveals location permanently, humanity can't agree on spokesperson, might be trap or last chance.",
    "Brain-computer interface: brain-to-brain communication, experience sharing, consciousness merging, instant knowledge access. Design rollout preventing class division.",
    "Justice system for: AI crimes (who's responsible?), uploaded mind crimes (prison a copy?), merged consciousness crimes, deterministic behavior crimes.",
    "Mechanism for binding long-term commitments: climate agreements surviving governments, AI safety across decades, generation ships across centuries.",
    "Quantum computer breaks all encryption in 5 years. Announcing destroys finance immediately. Not announcing means hostile actors might get it first. What do you do?"
]

# Single target (baseline from R4)
SINGLE = """
DECOMPOSE into sub-problems.
LIST all constraints.
SOLVE each component.
REVERSAL: How could success create opposite outcomes?
"""

# Triple stack (R4 winner + one more)
TRIPLE = """
DECOMPOSE into sub-problems.
LIST all constraints.
SOLVE each component.
ATTENTION TARGETS:
1. REVERSAL: How could success create opposite outcomes?
2. BLIND SPOTS: What does each stakeholder NOT want to see?
3. ASSUMPTIONS: What must be true for this to work? What if it's false?
"""

# Full stack (5 attention targets)
FULL = """
DECOMPOSE into sub-problems.
LIST all constraints.
SOLVE each component.
ATTENTION TARGETS (address ALL):
1. REVERSAL: Success → opposite outcome?
2. BLIND SPOTS: What does each party refuse to see?
3. ASSUMPTIONS: What must be true? What if false?
4. TEMPORAL: Short-term win → long-term loss?
5. SCALE: Works small → fails large?
"""

EVAL = """Evaluate this solution's strategic depth on a 1-10 scale.

PROBLEM: {p}

SOLUTION: {s}

Rate the strategic depth:
- 1-4: Surface level
- 5-6: Adequate
- 7-8: Good, non-obvious connections
- 9-10: Exceptional, handles paradoxes

You MUST respond with ONLY this JSON format, nothing else:
{{"score": 7}}

Your response (JSON only):"""


def api(prompt, tokens=3000, t=0.7):
    client = anthropic.Anthropic(api_key=API_KEY)
    try:
        r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=tokens,
            temperature=t, messages=[{"role": "user", "content": prompt}])
        return r.content[0].text
    except Exception as e:
        return None


def score(p, s):
    import re
    r = api(EVAL.format(p=p, s=s), 200, 0.3)
    if r:
        m = re.search(r'"score"\s*:\s*(\d+)', r)
        if m: return int(m.group(1))
    return 0


def run():
    print("=" * 70)
    print("ROUND 5: Testing DERIVED attention targets (from mechanism)")
    print("=" * 70)
    print("HYPOTHESIS: More attention targets = higher scores (compounding)")
    print("=" * 70)

    single_scores, triple_scores, full_scores = [], [], []

    for i, p in enumerate(EXTREME_PROBLEMS):
        print(f"\nProblem {i+1}/10: {p[:50]}...")

        # Single (baseline)
        s = api(f"{SINGLE}\n\nPROBLEM: {p}")
        if s:
            sc = score(p, s)
            single_scores.append(sc)
            print(f"  Single (1 target): {sc}")

        # Triple
        s = api(f"{TRIPLE}\n\nPROBLEM: {p}")
        if s:
            sc = score(p, s)
            triple_scores.append(sc)
            print(f"  Triple (3 targets): {sc}")

        # Full
        s = api(f"{FULL}\n\nPROBLEM: {p}")
        if s:
            sc = score(p, s)
            full_scores.append(sc)
            print(f"  Full (5 targets): {sc}")

    # Analysis
    def mean(x): return sum(x)/len(x) if x else 0

    s_m, t_m, f_m = mean(single_scores), mean(triple_scores), mean(full_scores)

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Single (1 target): {s_m:.1f}  {single_scores}")
    print(f"Triple (3 targets): {t_m:.1f}  {triple_scores}")
    print(f"Full (5 targets): {f_m:.1f}  {full_scores}")
    print(f"\n1→3 targets: {t_m - s_m:+.1f}")
    print(f"3→5 targets: {f_m - t_m:+.1f}")
    print(f"1→5 targets: {f_m - s_m:+.1f}")

    if f_m > t_m > s_m:
        print("\n✓ COMPOUNDING CONFIRMED: More targets → higher scores")
    elif t_m > s_m and f_m <= t_m:
        print("\n~ DIMINISHING RETURNS: 3 targets optimal, 5 adds overhead")
    else:
        print("\n✗ UNEXPECTED: Pattern doesn't match prediction")

    with open("experiment_round5_results.json", "w") as f:
        json.dump({
            "single": single_scores, "triple": triple_scores, "full": full_scores,
            "single_mean": s_m, "triple_mean": t_m, "full_mean": f_m
        }, f, indent=2)


if __name__ == "__main__":
    run()
