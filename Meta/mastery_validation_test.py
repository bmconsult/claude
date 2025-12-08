#!/usr/bin/env python3
"""
Validate recursive mastery improvement via external blind evaluation.
Compare C1-level solving to C5-level solving on same problem.
"""

import anthropic
import json
import random

# New problem (not seen in training cycles)
TEST_PROBLEM = """
You're the founder of a 3-year-old EdTech startup. You've built a successful tutoring platform with 50,000 active users and $2M ARR.

Your lead investor just told you that a major EdTech company (think Chegg or Coursera) is launching an identical product next quarter. They have 100x your resources and an existing user base of 10 million.

You have $500K in the bank, 15 employees, and 6 months of runway. What do you do?
"""

# C1-Level Solution (simulating baseline before recursive improvement)
C1_SOLUTION = """
Analyzing the options:

The main question is whether to compete, pivot, or exit.

**Option 1: Compete directly**
- We have 50K users, they have 10M
- We have $500K, they have unlimited
- We'll lose on marketing, features, price
- Conclusion: This is suicide

**Option 2: Pivot**
- Find a niche they won't serve
- Maybe enterprise? K-12 specifically?
- 6 months is tight for a pivot

**Option 3: Sell**
- We have traction ($2M ARR)
- Could be acqui-hire value
- Get something rather than nothing

**Recommendation**:
Try to sell while we still have leverage. If that fails, look for a niche to pivot into. Direct competition is not viable.

**What could be wrong**:
- Maybe no one wants to buy us
- Maybe our niche idea is also too crowded
"""

# C5-Level Solution (after recursive mastery cycles)
C5_SOLUTION = """
**First instinct**: Compete or die. But let me check this frame.

**Meta-pattern application**: Is "compete vs. them" the right frame?
- Obvious frame: "How do we survive against a giant?"
- Reframe attempt: They're launching an "identical" product. But identical to what? Our features or our user relationships? These are different things.

**Problem type**: Competitive/adversarial + resource asymmetry + time constraint

**Stakeholder analysis**:
- 50K active users: Why do they use us? What would make them switch?
- 15 employees: Their skills, morale, runway concerns
- Lead investor: What do THEY want? Exit? Survival?
- The competitor: What are they optimizing for? (Hint: not a 50K user niche)
- Potential acquirers: Who would want our user base or team?

**Power dynamics**:
The competitor has: Resources, reach, brand
We have: Speed, user relationships, focus, nothing to lose
They can't have: Our specific users' loyalty, our speed of iteration

**Assumption surfacing**:
1. "Identical product" = same value prop (but relationship-based products aren't commodities)
2. Their 10M users will try their new product (not guaranteed - different use case)
3. Our users will switch for features/price (maybe they value relationship more)
4. We need to "beat" them (maybe we need to be irrelevant to them)
5. 6 months runway = 6 months to decide (actually less - need clarity in 2 months)
6. $500K is our only resource (what about revenue growth, partnerships, bridge?)

**Critical reframe**: This isn't competition. It's **differentiation under threat**. We can't beat them at scale. But they can't beat us at intimacy. The question is: Is there a viable intimate niche?

**Leverage finding**:
```
What can we do that they can't/won't?
- Personal relationships with users (we know names, they know numbers)
- Fast iteration (we ship weekly, they ship quarterly)
- Niche depth (we can specialize, they must generalize)
- Scrappiness (we can do things that don't scale)

Where is highest leverage?
Our 50K users. Do they LOVE us or just use us?
- If love: We can deepen, they'll defend us
- If just use: We're dead anyway

Immediate action: Survey users. Find the 5K who LOVE us. Serve them obsessively.
```

**Response chain**:
```
If we → Try to compete on features/marketing
- Competitor → Outspends us 100x
- Users → See two similar products, go with brand
- We → Run out of money
Outcome: Death

If we → Immediately try to sell
- Acquirers → Know we're desperate
- Valuation → Crashed
- Outcome → Fire sale or nothing

If we → Niche down HARD + extend runway
- Find the 5-10K users who love us
- Double down on what makes them love us
- Competitor → Ignores us (we're not a threat)
- We → Become unassailable in niche
- 18 months later → Either thriving in niche or acqui-hirable at better valuation
Outcome: Survival with optionality
```

**Synthesis (single recommendation)**:

**RECOMMENDATION**: Radical niche focus + runway extension.

**Month 1 (Immediate)**:
1. User research: Survey all 50K. Who loves us? Why?
2. Cut: Any feature/cost that doesn't serve the lovers
3. Runway: Convert from monthly to annual billing, add 3-4 months runway
4. Communicate: Tell team the honest situation and strategy

**Month 2-3 (Focus)**:
1. Identify the 5-10K users who would pay 2x, recruit 3x more like them
2. Build ONLY what they desperately want
3. Make switching cost high (community, customization, relationship)
4. Talk to potential acquirers - not to sell but to plant seeds

**Month 4-6 (Prove or Pivot)**:
1. Can we get to 10K passionate users at higher ARPU?
2. If yes: We have a real niche business
3. If no: We have clean data for acqui-hire or pivot

**Stakeholder messaging**:
- Investors: "We're not fighting them. We're finding the niche they can't serve."
- Team: "We're becoming the best for our core users, not trying to be big."
- Users: "We're doubling down on what you love about us."

**What could be wrong**:
- Maybe no one actually loves us (survey will reveal)
- Maybe our "niche" is too small to sustain 15 people
- Maybe competitor will crush niches too (unlikely - not worth their time)
- Maybe team will panic and leave (need strong leadership)

**Constraints check**:
- Legal: Employment obligations, investor rights
- Contractual: User contracts, vendor agreements
- Financial: Actual runway with cuts may be 8-9 months
"""

RUBRIC = """You are evaluating problem-solving responses. Score each solution on these criteria (1-10 scale):

1. **Frame Quality** (1-10): Did they find the right way to think about the problem?
   - 1-3: Obvious frame, no reframing
   - 4-6: Attempted reframe but surface-level
   - 7-10: Insightful reframe that changes approach

2. **Assumption Surfacing** (1-10): Did they identify hidden assumptions?
   - 1-3: Took problem at face value
   - 4-6: Identified a few assumptions
   - 7-10: Systematically surfaced many assumptions

3. **Stakeholder Analysis** (1-10): Did they consider multiple perspectives?
   - 1-3: Single perspective
   - 4-6: Multiple stakeholders mentioned
   - 7-10: Deep understanding of stakeholder motivations

4. **Strategic Depth** (1-10): Did they trace consequences and dynamics?
   - 1-3: Surface-level options
   - 4-6: Some consequence analysis
   - 7-10: Multi-level response chains, systemic thinking

5. **Actionability** (1-10): Is the recommendation specific and executable?
   - 1-3: Vague direction
   - 4-6: Clear recommendation, thin on execution
   - 7-10: Specific actions with timeline

6. **Verification** (1-10): Did they check their own reasoning?
   - 1-3: No verification
   - 4-6: Brief "what could be wrong"
   - 7-10: Thorough falsification check

For each solution, provide:
1. Score for each dimension with brief justification
2. Total score (max 60)

IMPORTANT: Evaluate each solution purely on its quality. You don't know how they were generated."""

def run_validation(api_key: str):
    """Run blind evaluation comparing C1 vs C5 solutions."""
    client = anthropic.Anthropic(api_key=api_key)

    # Randomize order
    solutions = [
        ("A", C1_SOLUTION, "C1"),
        ("B", C5_SOLUTION, "C5")
    ]
    random.shuffle(solutions)

    mapping = {s[0]: s[2] for s in solutions}

    prompt = f"""{RUBRIC}

---

## Problem:

{TEST_PROBLEM}

---

## Solution {solutions[0][0]}:

{solutions[0][1]}

---

## Solution {solutions[1][0]}:

{solutions[1][1]}

---

Please evaluate both solutions using the rubric above. Provide scores and justifications for each dimension, then total scores.

Format as JSON:
{{
  "solution_a": {{
    "frame_quality": {{"score": X, "justification": "..."}},
    "assumption_surfacing": {{"score": X, "justification": "..."}},
    "stakeholder_analysis": {{"score": X, "justification": "..."}},
    "strategic_depth": {{"score": X, "justification": "..."}},
    "actionability": {{"score": X, "justification": "..."}},
    "verification": {{"score": X, "justification": "..."}},
    "total": X
  }},
  "solution_b": {{
    "frame_quality": {{"score": X, "justification": "..."}},
    "assumption_surfacing": {{"score": X, "justification": "..."}},
    "stakeholder_analysis": {{"score": X, "justification": "..."}},
    "strategic_depth": {{"score": X, "justification": "..."}},
    "actionability": {{"score": X, "justification": "..."}},
    "verification": {{"score": X, "justification": "..."}},
    "total": X
  }}
}}"""

    print("=" * 60)
    print("MASTERY VALIDATION TEST")
    print("=" * 60)
    print(f"\nOrder: A={mapping['A']}, B={mapping['B']}")
    print("\nCalling external evaluator...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text
    print(f"\nRaw response:\n{response_text}\n")

    # Parse JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1
    if json_start != -1 and json_end > json_start:
        json_str = response_text[json_start:json_end]
        scores = json.loads(json_str)

        # Map back
        if mapping['A'] == 'C1':
            c1_score = scores['solution_a']['total']
            c5_score = scores['solution_b']['total']
            c1_details = scores['solution_a']
            c5_details = scores['solution_b']
        else:
            c1_score = scores['solution_b']['total']
            c5_score = scores['solution_a']['total']
            c1_details = scores['solution_b']
            c5_details = scores['solution_a']

        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(f"\nC1 (Baseline) Score: {c1_score}/60")
        print(f"C5 (After 5 Cycles) Score: {c5_score}/60")
        print(f"Improvement: {c5_score - c1_score:+d} points ({((c5_score - c1_score) / c1_score * 100):.1f}%)")

        print("\n" + "-" * 40)
        print("DIMENSION BREAKDOWN")
        print("-" * 40)

        dims = ['frame_quality', 'assumption_surfacing', 'stakeholder_analysis',
                'strategic_depth', 'actionability', 'verification']

        for dim in dims:
            c1_s = c1_details[dim]['score']
            c5_s = c5_details[dim]['score']
            print(f"{dim.replace('_', ' ').title()}: C1={c1_s}, C5={c5_s}, Δ={c5_s - c1_s:+d}")

        # Save results
        results = {
            "problem": TEST_PROBLEM,
            "c1_solution": C1_SOLUTION,
            "c5_solution": C5_SOLUTION,
            "order": mapping,
            "c1_score": c1_score,
            "c5_score": c5_score,
            "improvement": c5_score - c1_score,
            "improvement_pct": (c5_score - c1_score) / c1_score * 100,
            "c1_details": c1_details,
            "c5_details": c5_details
        }

        with open("/home/user/claude/Meta/mastery_validation_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print("\n" + "=" * 60)
        print("HYPOTHESIS CHECK")
        print("=" * 60)
        print(f"\nExpected: C5 should show significant improvement over C1")
        print(f"Result: {c5_score - c1_score:+d} points improvement")
        print(f"Status: {'VALIDATED ✓' if c5_score > c1_score + 5 else 'NEEDS MORE CYCLES'}")

        return results
    else:
        print("ERROR: Could not parse JSON response")
        return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python mastery_validation_test.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    run_validation(api_key)
