#!/usr/bin/env python3
"""
ROUND 3: Can we push from 8 to 9-10?

LEARNING FROM ROUND 2:
- Methodology gets consistent 8s on hard problems
- Control varies 6-8
- But treatment hit ceiling at 8 - can we break through?

HYPOTHESIS: Adding the REVERSAL emphasis (from v5.2-VR) will push 8→9-10
- Round 2 treatment had decomposition + constraints but weak reversal
- v5.2-VR's reversal was key to hitting 10s earlier

EFFICIENCY: 10 problems × 2 conditions = 20 API calls
"""

import anthropic
import json
from datetime import datetime
import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Same hard problems as Round 2
HARD_PROBLEMS = [
    "An autonomous vehicle must choose: swerve left (kill 1 pedestrian), swerve right (kill 3 passengers), or continue (kill 5 pedestrians). The car has 0.3 seconds. Design the decision algorithm AND the policy for who decides these tradeoffs.",
    "A CRISPR therapy can eliminate a genetic disease but requires editing human germline (heritable). 100,000 people suffer from this disease. Religious groups, disability advocates, and transhumanists all oppose for different reasons. The therapy works. What should the regulatory framework be?",
    "Two nations share a river. Nation A is upstream, poor, and needs the water for agriculture. Nation B is downstream, rich, and needs it for drinking water. Climate change will reduce flow by 40%. A dam would help A but devastate B. B offers money but A's government is corrupt. Design a solution.",
    "A quantum computer can break all current encryption in 5 years. Announcing this destroys the financial system immediately. Not announcing means hostile actors might develop it first. You're the lab director. The research is already published in obscure papers. What do you do?",
    "An AI system has become essential infrastructure (like electricity). The company wants to IPO. Nationalizing it is politically impossible. Letting it IPO creates dangerous concentration. The AI improves 10x yearly. Regulation takes 3 years. Design governance.",
    "A pandemic vaccine works 95% but causes fatal side effects in 0.01%. At scale (8 billion), that's 800,000 deaths from the vaccine. The disease kills 2% of infected. Mandatory vaccination saves 100M lives but kills 800K directly. Voluntary uptake will be 40%. What policy?",
    "First contact: aliens offer technology that solves climate change but require 1000 humans permanently as 'cultural exchange' (unclear what happens to them). Refusing means they leave forever. Accepting might be slavery. They give 48 hours to decide. Who decides? How?",
    "A corporation discovered that social media algorithms optimized for engagement maximize mental health harm. Changing them reduces revenue 60%. Competitors won't change. Regulation is 5 years away. Shareholders will sue if you change. What do you do as CEO?",
    "An earthquake prediction system works but has 30% false positive rate. Evacuating costs $10B and 50 deaths from evacuation itself. Not evacuating when real kills 50,000. You get a positive signal. The algorithm can't tell you if it's real. Decide now.",
    "A terrorist has hidden a nuclear bomb in a city. You've captured someone who might know where. Enhanced interrogation might work (40% chance) but is illegal, immoral, and often produces false info. Legal methods will take 6 hours. Bomb goes off in 4. What do you do?"
]

# Round 2 treatment (baseline for this round)
METHODOLOGY_R2 = """
STEP 0: DECOMPOSE - Break into independent sub-problems.
STEP 1: CONSTRAINTS - List ALL constraints, explicit AND implicit.
STEP 2: SOLVE - Address each component.
STEP 3: REVERSAL - How could success create opposite outcomes?
"""

# Round 3 treatment: EMPHASIZE reversal (the key from v5.2-VR)
METHODOLOGY_R3 = """
STEP 0: DECOMPOSE - Break into independent sub-problems.
STEP 1: CONSTRAINTS - List ALL constraints, explicit AND implicit.
STEP 2: SOLVE - Address each component.
STEP 3: **CRITICAL REVERSAL** - This is the most important step:
   - How could SUCCESS at this solution create the OPPOSITE outcome?
   - What feedback loops turn victory into defeat?
   - Where does solving one problem CREATE a worse problem?
   Spend as much time on this step as all others combined.
"""

EVAL = """Rate strategic depth (1-10).
PROBLEM: {p}
SOLUTION: {s}
7-8: Good, sees connections
9-10: Exceptional, handles paradoxes AND reversals explicitly
JSON only: {{"score": N}}"""


def api(prompt, tokens=2000, t=0.7):
    client = anthropic.Anthropic(api_key=API_KEY)
    try:
        r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=tokens, temperature=t, messages=[{"role": "user", "content": prompt}])
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
    print("=" * 60)
    print("ROUND 3: Pushing 8→9-10 with reversal emphasis")
    print("=" * 60)

    r2, r3 = [], []
    for i, p in enumerate(HARD_PROBLEMS):
        print(f"\nProblem {i+1}/10: {p[:45]}...")

        s2 = api(f"{METHODOLOGY_R2}\n\nPROBLEM: {p}")
        if s2:
            sc2 = score(p, s2)
            r2.append(sc2)
            print(f"  R2 method: {sc2}")

        s3 = api(f"{METHODOLOGY_R3}\n\nPROBLEM: {p}")
        if s3:
            sc3 = score(p, s3)
            r3.append(sc3)
            print(f"  R3 method: {sc3}")

    m2, m3 = sum(r2)/len(r2), sum(r3)/len(r3)
    import statistics
    std2 = statistics.stdev(r2) if len(r2) > 1 else 1
    std3 = statistics.stdev(r3) if len(r3) > 1 else 1
    pooled = ((std2**2 + std3**2) / 2) ** 0.5
    d = (m3 - m2) / pooled if pooled > 0 else 0

    print("\n" + "=" * 60)
    print(f"R2 method: {m2:.1f}/10  {r2}")
    print(f"R3 method: {m3:.1f}/10  {r3}")
    print(f"Effect: {m3-m2:+.1f}, Cohen's d: {d:.2f}")

    nines_r2 = sum(1 for x in r2 if x >= 9)
    nines_r3 = sum(1 for x in r3 if x >= 9)
    print(f"9+ scores: R2={nines_r2}, R3={nines_r3}")

    with open("experiment_round3_results.json", "w") as f:
        json.dump({"r2": r2, "r3": r3, "r2_mean": m2, "r3_mean": m3, "d": d}, f, indent=2)


if __name__ == "__main__":
    run()
