#!/usr/bin/env python3
"""
ROUND 4: APPLYING THE METHODOLOGY TO METHODOLOGY-MAKING

=== META-APPLICATION ===

STEP 0: DECOMPOSE THE META-PROBLEM
What are the independent components of "improving problem-solving methodology"?
1. Problem difficulty (must be below ceiling to measure)
2. Intervention mechanism (WHY does it work, not just WHAT)
3. Measurement sensitivity (can we detect real differences?)

STEP 1: CONSTRAINTS ON METHODOLOGY-MAKING
- Ceiling effects hide differences → must use harder problems
- Theoretical derivation ≠ empirical effect → must test everything
- Diminishing returns near ceiling → push difficulty UP
- Evaluation variance exists → need robust measurement

STEP 2: DERIVE THE INTERVENTION FROM FIRST PRINCIPLES
WHY does "reversal" work?
- Forces attention to FEEDBACK LOOPS
- Makes solver consider how solutions CREATE new problems
- Surfaces NON-OBVIOUS dynamics

What's the GENERAL PRINCIPLE?
→ Effective prompts steer attention to SPECIFIC NON-OBVIOUS FEATURES
→ "Reversal" is ONE instance of this
→ There should be OTHER instances that work via same mechanism

HYPOTHESIS: If attention-steering-to-non-obvious is the mechanism, then
OTHER specific features should work equally well.

TEST: Compare "reversal" to "stakeholder blind spots" (different feature, same mechanism)

STEP 3: CRITICAL REVERSAL ON OUR OWN METHOD
How could SUCCESS at this methodology research CREATE OPPOSITE outcomes?
- Over-optimizing for the evaluation metric instead of actual quality
- Finding prompts that game the evaluator without improving real thinking
- Hitting ceiling and mistaking variance for real improvement

MITIGATION: Use HARDER problems that current best can't solve at ceiling
"""

import anthropic
import json
from datetime import datetime
import os
import statistics

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# HARDER THAN ROUND 3 - designed to break 9 ceiling
# These require synthesis across multiple incompatible frameworks
EXTREME_PROBLEMS = [
    """Design a global governance system for AGI that:
    - Prevents any single nation from monopolizing it
    - Doesn't require nations to trust each other
    - Can adapt faster than the technology itself
    - Remains legitimate when AGI can outthink human overseers
    - Handles the transition period where some have it and others don't
    Include specific mechanisms, not principles.""",

    """A simulation argument suggests 50% chance we're in a simulation. If true:
    - Our actions might be judged by simulators with unknown values
    - Physics might be approximated, not real
    - "Interesting" behaviors might be preserved, "boring" ones deleted
    Design a decision theory and life strategy that's robust to both simulation and base reality.""",

    """Create a constitution for a Mars colony that:
    - Works with 100 people initially, scales to 1 million
    - Handles 20-minute communication delay with Earth
    - Accounts for genetic divergence over centuries
    - Prevents Earth from exploiting Mars AND Mars from threatening Earth
    - Manages resources that determine literal survival
    Specific articles, not vague principles.""",

    """Design an education system for 2050 when:
    - AI can pass any test and do most cognitive work
    - Lifespan is 120+, careers span 80 years
    - Information is free but wisdom is scarce
    - Credentials are meaningless (AI can fake anything)
    - Human comparative advantage is unclear
    What do humans learn? How? Who decides? How certified?""",

    """A research team discovers how to upload human consciousness, but:
    - The scan destroys the original brain
    - The upload claims continuity of identity
    - Religious groups say it's murder + creating a demon
    - The upload has all memories and behaves identically
    - Uploaded beings could run 1000x faster, copy themselves
    Design the ethical framework, legal status, and transition protocol.""",

    """Create a monetary system for a post-scarcity economy where:
    - AI produces most goods at near-zero marginal cost
    - Human labor is optional, not necessary
    - Status competition still exists
    - Some resources remain genuinely scarce (land, attention, unique items)
    - Meaning and purpose must come from somewhere
    Include specific mechanisms for allocation, not just "universal basic income.""",

    """Design first contact protocol given:
    - Alien signal detected, clearly artificial
    - Light-speed delay means 50-year round trips for messages
    - Any response reveals Earth's location permanently
    - Humanity can't agree on who speaks for Earth
    - The message might be a trap (dark forest hypothesis)
    - Or might be last chance before sender dies out
    Who decides? What's sent? What's the decision process?""",

    """A brain-computer interface allows:
    - Direct brain-to-brain communication (no language barrier)
    - Sharing of subjective experiences (qualia)
    - Merging of multiple consciousnesses temporarily
    - Access to collective human knowledge instantly
    But early adopters gain massive advantages. Design the rollout that:
    - Prevents permanent class division (enhanced vs natural)
    - Preserves individual identity and privacy
    - Handles the transition generation (both enhanced and natural people alive)
    - Manages the military/economic advantages""",

    """Create justice system for crimes committed by:
    - AI systems (who's responsible? the AI? trainer? user? company?)
    - Uploaded minds (can you imprison a copy? delete them? what about backups?)
    - Merged consciousnesses (one of three merged minds committed crime)
    - People with deterministically-caused behavior (brain tumor made them do it)
    - Actions across simulation boundaries (crime in VR with real victims)
    Specific legal frameworks and precedents, not principles.""",

    """Design mechanism for humanity to make binding long-term commitments:
    - Climate agreements that survive government changes
    - AI safety agreements enforceable across decades
    - Resource allocation for generation ships (centuries)
    - Preservation of cultural heritage against future indifference
    Current institutions fail because future people can defect.
    What mechanism actually binds future generations without tyranny?"""
]

# CURRENT BEST: Decompose + Constraints + Reversal
METHODOLOGY_BEST = """
STEP 0: DECOMPOSE into independent sub-problems
STEP 1: LIST all constraints (explicit + implicit)
STEP 2: SOLVE each component
STEP 3: REVERSAL - How could success create opposite outcomes?
"""

# TEST HYPOTHESIS: Different attention-steering should work equally well
# If reversal works via "attention to non-obvious features", then
# "stakeholder blind spots" should work via same mechanism
METHODOLOGY_ALT = """
STEP 0: DECOMPOSE into independent sub-problems
STEP 1: LIST all constraints (explicit + implicit)
STEP 2: SOLVE each component
STEP 3: BLIND SPOTS - What would each stakeholder NOT want to see or admit?
   For each key stakeholder, identify the truth they're motivated to ignore.
"""

# COMBINED: Both attention-steering mechanisms
METHODOLOGY_COMBINED = """
STEP 0: DECOMPOSE into independent sub-problems
STEP 1: LIST all constraints (explicit + implicit)
STEP 2: SOLVE each component
STEP 3: REVERSAL - How could success create opposite outcomes?
STEP 4: BLIND SPOTS - What does each stakeholder NOT want to see?
"""

EVAL = """Rate this solution's strategic depth (1-10) for this EXTREMELY HARD problem.

Reserve 9-10 ONLY for solutions that:
- Handle genuine paradoxes (not just acknowledge them)
- Provide specific mechanisms (not just principles)
- Address how the solution handles its own failure modes

PROBLEM: {p}

SOLUTION: {s}

JSON: {{"score": N, "justification": "one sentence"}}"""


def api(prompt, tokens=3000, t=0.7):
    client = anthropic.Anthropic(api_key=API_KEY)
    try:
        r = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=tokens,
            temperature=t, messages=[{"role": "user", "content": prompt}])
        return r.content[0].text
    except Exception as e:
        print(f"API error: {e}")
        return None


def score(p, s):
    import re
    r = api(EVAL.format(p=p, s=s), 300, 0.3)
    if r:
        m = re.search(r'"score"\s*:\s*(\d+)', r)
        if m: return int(m.group(1))
    return 0


def run():
    print("=" * 70)
    print("ROUND 4: Meta-Application of Methodology to Methodology-Making")
    print("=" * 70)
    print("\nHYPOTHESIS: If attention-steering is the mechanism,")
    print("different specific features should work via same mechanism.")
    print("\nTEST: Reversal vs Blind-Spots vs Combined")
    print("=" * 70)

    best_scores = []
    alt_scores = []
    combined_scores = []

    for i, p in enumerate(EXTREME_PROBLEMS):
        print(f"\nProblem {i+1}/10: {p[:50]}...")

        # Current best
        s = api(f"{METHODOLOGY_BEST}\n\nPROBLEM: {p}")
        if s:
            sc = score(p, s)
            best_scores.append(sc)
            print(f"  Best (reversal): {sc}")

        # Alternative mechanism
        s = api(f"{METHODOLOGY_ALT}\n\nPROBLEM: {p}")
        if s:
            sc = score(p, s)
            alt_scores.append(sc)
            print(f"  Alt (blind spots): {sc}")

        # Combined
        s = api(f"{METHODOLOGY_COMBINED}\n\nPROBLEM: {p}")
        if s:
            sc = score(p, s)
            combined_scores.append(sc)
            print(f"  Combined: {sc}")

    # Analysis
    def stats(scores, name):
        m = sum(scores)/len(scores) if scores else 0
        std = statistics.stdev(scores) if len(scores) > 1 else 0
        return m, std

    best_m, best_std = stats(best_scores, "Best")
    alt_m, alt_std = stats(alt_scores, "Alt")
    comb_m, comb_std = stats(combined_scores, "Combined")

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"Best (reversal):    {best_m:.1f} ± {best_std:.1f}  {best_scores}")
    print(f"Alt (blind spots):  {alt_m:.1f} ± {alt_std:.1f}  {alt_scores}")
    print(f"Combined:           {comb_m:.1f} ± {comb_std:.1f}  {combined_scores}")

    # Effect sizes
    if best_std > 0:
        d_alt = (alt_m - best_m) / best_std
        d_comb = (comb_m - best_m) / best_std
        print(f"\nAlt vs Best: d={d_alt:.2f}")
        print(f"Combined vs Best: d={d_comb:.2f}")

    # Theoretical interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    if alt_m >= best_m - 0.3:
        print("✓ Alt performs similarly → mechanism is attention-steering (not reversal-specific)")
    else:
        print("✗ Alt underperforms → reversal has specific value beyond attention-steering")

    if comb_m > max(best_m, alt_m) + 0.3:
        print("✓ Combined beats both → multiple attention targets compound")
    else:
        print("✗ Combined doesn't compound → diminishing returns on attention targets")

    # Save
    results = {
        "timestamp": datetime.now().isoformat(),
        "round": 4,
        "hypothesis": "Attention-steering is the mechanism; different features work equally",
        "best_scores": best_scores, "alt_scores": alt_scores, "combined_scores": combined_scores,
        "best_mean": best_m, "alt_mean": alt_m, "combined_mean": comb_m
    }
    with open("experiment_round4_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to experiment_round4_results.json")


if __name__ == "__main__":
    run()
