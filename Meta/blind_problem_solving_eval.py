#!/usr/bin/env python3
"""
Blind evaluation of problem-solving solutions.
External Claude instance scores solutions without knowing which used protocols.
"""

import anthropic
import random
import json
from dataclasses import dataclass
from typing import List, Tuple

# Problems and solutions from the validation document
PROBLEMS = [
    {
        "id": 1,
        "name": "Supplier Exclusivity",
        "type": "Game Theory",
        "problem": """You're a supplier to two competing retailers. Each wants exclusive pricing. If you give exclusive to one:
- That retailer: +40% orders from them
- Other retailer: -100% orders (they drop you)
- Current: 50% of business from each

If you refuse exclusivity to both:
- 20% chance both drop you (they find alternatives)
- 80% chance status quo continues

What's your strategy?""",
        "baseline": """Analyzing the options:
- Give exclusive to Retailer A: +40% from A, lose B entirely. Net: 140% of half = 70% of original business
- Give exclusive to Retailer B: Same math. 70% of original.
- Refuse both: 80% chance of 100%, 20% chance of 0%. Expected: 80% of original.

Current = 50% from each = 100% total.
- Exclusive to A: 50% × 1.4 = 70% total (lose the 50% from B)
- Refuse both: 0.8 × 100% + 0.2 × 0% = 80%

So refusing both (80%) beats exclusive (70%).

But is this one-shot or repeated? If repeated:
- Refusing builds trust, maybe both stay long-term
- Exclusive creates dependency, risky

**Answer**: Refuse exclusivity. 80% expected value beats 70%, and preserves optionality.""",
        "protocol": """**ASSUMPTION AUDIT**:
- Assumes retailers are rational economic actors ← What if emotional/relationship factors?
- Assumes the 40%/100% numbers are accurate ← Could be negotiating tactics
- Assumes these are the only two retailers ← Could diversify to others
- Assumes one-shot decision ← This is ongoing relationship
- Assumes "finding alternatives" is binary ← Could be partial

**Critical assumption**: Is this a one-shot or repeated game?

**RESPONSE CHAIN**:
If I refuse both:
- Their response: Might accept (80%) or leave (20%)
- If they accept: Status quo, but they may resent and look for alternatives
- My counter: Strengthen relationships, add value beyond price
- Long-term: More stable than exclusivity lock-in

If I give exclusive to A:
- B's response: Drops me (certain)
- A's response: Increases orders 40%
- A's future move: They know I'm dependent, may squeeze margins
- Long-term: I'm captive to A's demands

**LEVERAGE FINDER**: The real leverage is reducing my dependency on either. Are there other potential customers? Can I diversify?

**SYNTHESIZED ANSWER**:
1. Refuse exclusivity (preserves optionality)
2. BUT immediately seek third customer to reduce concentration risk
3. Deepen relationship value (not just price) to reduce "find alternatives" risk

**VERIFY**:
- Math: 80% > 70% ✓
- Accounts for dynamics: Yes, added long-term and diversification
- Constraints: Feasible with current relationships
- What could be wrong: If I can't find third customer, still concentrated"""
    },
    {
        "id": 2,
        "name": "Sunk Cost",
        "type": "Clear-answer",
        "problem": """Your company has spent $5M over 2 years developing a product. Market research now shows:
- 30% chance of success if you spend $2M more to launch
- Success = $20M revenue
- Failure = $0
- Abandoning now = $0 additional cost, $0 revenue
- The $5M is gone either way

A new opportunity exists:
- Costs $2M
- 60% chance of $15M revenue
- 40% chance of $0

You only have $2M. What do you do?""",
        "baseline": """The $5M is sunk. Ignore it.

Option A (continue product):
- EV = 0.3 × $20M + 0.7 × $0 = $6M
- Cost = $2M
- Net EV = $4M

Option B (new opportunity):
- EV = 0.6 × $15M + 0.4 × $0 = $9M
- Cost = $2M
- Net EV = $7M

New opportunity has higher expected value ($7M vs $4M).

**Answer**: Abandon the current product, pursue new opportunity.""",
        "protocol": """**ASSUMPTION AUDIT**:
- $5M is sunk ← Correct, but may have learning value
- Success probabilities are accurate ← Who estimated these? Could be biased
- Revenues are independent ← What if product failure affects reputation for new opportunity?
- Only two options exist ← Could we do smaller version of product + new opportunity?
- "Success" is binary ← Could be partial success

**Critical insight**: The 30% vs 60% probabilities - where did these come from? If from the team that spent $5M, they may be optimistic about the product.

**RESPONSE CHAIN**: (Not strongly adversarial, but considering market response)
- If we launch product and fail: $2M lost, reputation impact?
- If new opportunity fails: $2M lost, but no sunk cost baggage
- Market perception: Pivot might signal agility

**LEVERAGE FINDER**: Key variable is probability accuracy. If product team is biased, true success rate might be <30%.

**SYNTHESIZED ANSWER**:
1. Question the 30% estimate - who made it? Any bias?
2. If probabilities are reliable: New opportunity (EV $7M > $4M)
3. Consider: Is there learning from product development that applies to new opportunity?
4. Decision: Pivot to new opportunity, but extract learnings from product development

**VERIFY**:
- Math: $7M > $4M ✓
- Sunk cost properly ignored: Yes ✓
- Added value: Questioned probability source, extracted learning value
- What could be wrong: If 30% is underestimate (team is conservative), calculation changes"""
    },
    {
        "id": 3,
        "name": "Subscription Dynamics",
        "type": "Systems",
        "problem": """A subscription service has:
- 10,000 subscribers at $10/month = $100K MRR
- 5% monthly churn
- Growth comes from referrals: each subscriber refers 0.1 new subscribers/month
- You can spend on: (A) reducing churn, (B) increasing referral rate

$10K budget. Option A reduces churn to 3%. Option B increases referrals to 0.15/subscriber.

Which investment has higher 12-month impact?""",
        "baseline": """Current state over 12 months:
- Start: 10,000
- Monthly: lose 5%, gain 0.1 per subscriber (= 10% referral rate)
- Net monthly change: +5%/month (10% - 5%)

Option A (3% churn): Net growth = 10% - 3% = 7%/month
Option B (15% referral): Net growth = 15% - 5% = 10%/month

Option B gives higher growth rate.

After 12 months:
- Option A: 10,000 × (1.07)^12 = 22,522
- Option B: 10,000 × (1.10)^12 = 31,384

**Answer**: Option B (increase referrals) - results in ~9,000 more subscribers after 12 months.""",
        "protocol": """**ASSUMPTION AUDIT**:
- Churn and referral rates are constant ← Likely change as you grow
- Effects are linear ← Might have diminishing returns
- $10K achieves stated results ← How certain?
- Options are mutually exclusive ← Could we do half and half?
- 12 months is right timeframe ← What about month 13+?

**LEVERAGE FINDER**:
```
Feedback loops:
R1: More subscribers → more referrals → more subscribers (growth engine)
R2: More subscribers → more word of mouth → brand strength → more referrals
B1: More subscribers → support burden → worse experience → more churn

Leverage analysis:
- Referral rate improvement COMPOUNDS through R1
- Churn reduction is LINEAR (just keeps more of what you have)
- Referral improvement has higher leverage
```

**VERIFY MATH**:
- Option A (3% churn, 10% referral): Net +7%/month, 12mo: 10,000 × 1.07^12 = 22,522
- Option B (5% churn, 15% referral): Net +10%/month, 12mo: 10,000 × 1.10^12 = 31,384
- Difference: 8,862 more subscribers with Option B ✓

**SYNTHESIZED ANSWER**:
1. Option B (referral investment) - mathematically superior AND higher leverage (compounds)
2. Caveat: Monitor churn - if it spikes due to growth, may need to shift
3. Long-term: Referral improvements compound; churn improvements are linear

**VERIFY**:
- Math confirmed ✓
- Systems analysis added (leverage reasoning)
- Constraints: $10K budget satisfied
- What could be wrong: If referral investment doesn't actually achieve 0.15 rate"""
    },
    {
        "id": 4,
        "name": "ICU Allocation",
        "type": "Wicked",
        "problem": """A hospital must allocate 100 ICU beds during a crisis:
- Elderly patients (65+): Higher mortality risk, shorter remaining life expectancy
- Younger patients (<40): Lower mortality risk, longer life expectancy
- Healthcare workers: Medium risk, but essential for treating others
- No "right" answer - ethical frameworks conflict

Propose an allocation framework and justify it.""",
        "baseline": """This is an ethical dilemma with no "correct" answer.

Possible frameworks:
1. **Utilitarian (maximize lives)**: Prioritize those most likely to survive
2. **Utilitarian (maximize life-years)**: Prioritize younger patients
3. **Egalitarian**: First-come-first-served or lottery
4. **Instrumental**: Prioritize healthcare workers (they save others)

I'd propose a tiered system:
1. First priority: Healthcare workers (instrumental value)
2. Second: Likelihood of survival (medical criteria)
3. Tiebreaker: Random/lottery (fairness)

**Answer**: Multi-criteria framework prioritizing healthcare workers, then survival likelihood, then lottery for ties. Justification: This maximizes total lives saved while maintaining fairness for equivalent cases.""",
        "protocol": """**ASSUMPTION AUDIT**:
- Must choose single framework ← Could use hybrid
- Categories are fixed ← What about healthcare workers who are elderly?
- Information is perfect ← Prognosis uncertain in crisis
- 100 beds is hard constraint ← Could we add capacity?
- Ethical frameworks are mutually exclusive ← Can we find common ground?

**LEVERAGE FINDER**: This is resource allocation during crisis.
```
Key dynamics:
- Healthcare workers treat others (multiplier effect)
- Capacity is fixed (zero-sum allocation)
- Information is imperfect (prognosis uncertainty)

Leverage points:
1. Healthcare worker preservation (treats more patients)
2. Triage accuracy (better predictions = better allocation)
3. Capacity expansion (changes the constraint)
```

**SYNTHESIZED FRAMEWORK**:

1. **First filter: Healthcare workers** (instrumental - preserving capacity to treat)
   - Not because their lives matter more, but because they're a scarce resource for saving others

2. **Second filter: Survival probability** (utilitarian - maximize lives saved)
   - Based on clinical criteria, not age alone
   - Age may correlate but isn't the criterion

3. **Third filter: Lottery among equivalent cases** (egalitarian fairness)
   - When prognosis is equivalent, random selection
   - Removes bias, maintains procedural fairness

4. **Process legitimacy additions**:
   - Decisions made by committee (not individual)
   - Criteria published in advance
   - Review mechanism for edge cases

**VERIFY**:
- Addresses all stakeholder groups: ✓
- Internally consistent: ✓
- Acknowledges tradeoffs: ✓
- Implementable: ✓
- What could be wrong: "Survival probability" estimates may be biased by age anyway"""
    },
    {
        "id": 5,
        "name": "Bank Competition",
        "type": "Adversarial",
        "problem": """You're a regional bank. A national bank announces:
- Free checking (you charge $5/month)
- 2% savings rate (you offer 0.5%)
- Launching in your market in 6 months

You have: Strong local relationships, $10M marketing budget, 6 months.
You cannot match their rates (scale disadvantage).

What's your response?""",
        "baseline": """National bank has: scale, rates, brand.
I have: relationships, local knowledge, 6 months, $10M.

Options:
1. Match rates (can't afford it)
2. Compete on service (hard to prove quickly)
3. Lock in customers (long-term contracts, switching costs)
4. Niche down (segments they won't serve well)

Strategy:
- Months 1-3: Aggressive retention - contact all customers, offer loyalty bonuses, lock in 2-year CDs at slightly better rates
- Months 4-6: Target their weaknesses - personal service, local business focus, community involvement
- Messaging: "We're your neighbors, not a 1-800 number"

**Answer**: Defensive retention first, then differentiation on service/local focus. Don't compete on rates.""",
        "protocol": """**ASSUMPTION AUDIT**:
- National bank will definitely enter ← Could they change plans?
- Their rates are sustainable ← Might be loss-leader, temporary
- My customers are at risk ← Some loyal, some price-sensitive (segment!)
- 6 months is the window ← Action before they arrive is better
- $10M is my only resource ← What about partnerships, community?

**Critical insight**: Not all my customers are equally at risk. Price-sensitive ones will leave; relationship-focused ones won't.

**RESPONSE CHAIN**:
National bank launches:
- Their move: Ads, competitive rates, new branches
- My response options:
  - Match rates (can't afford) → they escalate → I lose
  - Lock in customers → some stay, some leave
  - Differentiate → they ignore (I'm not a threat to them)
- Their counter to differentiation: Probably nothing (I'm 1% of their focus)

**LEVERAGE FINDER**:
```
Key dynamics:
- Customer switching has friction (inconvenience)
- National bank can't personalize (scale constraint)
- Community relationships are sticky

Leverage points:
1. Switching friction (lock-ins, integration)
2. Personal service (structural advantage)
3. Community identity (they can't replicate)
```

**SYNTHESIZED STRATEGY**:

**Segment customers**:
- Price-sensitive: Will leave. Don't overspend defending.
- Relationship-focused: Defensible. Invest here.
- Small business: Need personal service national bank won't provide.

**Actions by priority**:
1. **Immediate**: Personal outreach to top 20% of customers (relationship lock-in)
2. **Month 1-2**: Launch "Local Business Banking" with named relationship managers
3. **Month 3-4**: Community campaign - sponsor local events, emphasize "neighbor" positioning
4. **Month 5-6**: Lock-in offers for loyal customers (better rates for 2-year commitment)
5. **Accept losses**: Some customers will leave. Focus on keeping the profitable, loyal ones.

**VERIFY**:
- Addresses threat: ✓
- Feasible with $10M: ✓
- Accounts for competitive response: ✓ (they won't counter-attack a small player)
- What could be wrong: If their rates are permanent (not loss-leader), more customers may leave"""
    },
    {
        "id": 6,
        "name": "VC Decision",
        "type": "Uncertainty",
        "problem": """A startup is deciding whether to raise VC funding:
- VC offer: $5M for 25% equity, aggressive growth expectations
- Bootstrap: Slower growth, keep 100% equity
- Market window: Unknown - could be 2 years or 5 years
- Competition: Unknown - could emerge any time

Current: $500K ARR, profitable, growing 50% YoY

What factors should drive this decision? What would you recommend and why?""",
        "baseline": """Key factors:
- Growth speed vs. dilution tradeoff
- Market timing uncertainty
- Competitive threat level
- Personal goals of founders

Analysis:
- At 50% YoY, bootstrapped: 2 years = $1.125M, 5 years = $3.8M ARR
- With VC $5M, could accelerate to maybe 100%+ YoY
- But giving up 25% equity

The "right" answer depends on:
- Is this a winner-take-all market? (favors speed/VC)
- Are founders optimizing for control or scale? (personal)
- How confident in market window? (uncertainty)

**Answer**: Take VC if (1) market is winner-take-all OR (2) clear competitive threat emerging. Bootstrap if market is stable and founders prefer control. Need more information to decide definitively.""",
        "protocol": """**ASSUMPTION AUDIT**:
- VC offer is as stated ← What are the real terms? Board seats? Control provisions?
- Growth expectations are manageable ← Could become pressure to grow unsustainably
- Market window is binary ← Actually continuous, can adjust strategy
- Competition is purely threat ← Could be validation of market
- 50% YoY continues ← Not guaranteed
- "Profitable" is sustainable ← Check cash position

**LEVERAGE FINDER**:
```
Key dynamics:
- Winner-take-all vs. niche market (determines urgency)
- Capital as weapon (VC-backed competitors)
- Control/autonomy vs. resources

Leverage point: Information about market structure
```

**RESPONSE CHAIN**:
- If I take VC: Must grow fast → may compromise product → might win big or burn out
- Competitor response to my VC: May also raise, arms race
- If I bootstrap: Slower, but controlled → may get outrun or may find niche
- Competitor response to bootstrap: May ignore me (I'm not a threat)

**Key question**: Is this a market where one player dominates (network effects, etc.) or can multiple players coexist?

**SYNTHESIZED FRAMEWORK**:

**Take VC if**:
1. Strong network effects (winner-take-all)
2. Well-funded competitor already exists or likely
3. Speed of scaling is critical to capture market
4. Founders can handle loss of control

**Bootstrap if**:
1. Market can support multiple players
2. No imminent VC-backed competition
3. Profitability is sustainable and fundable
4. Founders prioritize control and sustainability

**Decision process**:
1. Research: Who else is funded in this space?
2. Analyze: Are there network effects?
3. Stress test: What happens if competitor raises $20M tomorrow?
4. Founders: What do YOU want?

**VERIFY**:
- Provides framework, not false certainty: ✓
- Identifies key factors: ✓
- Accounts for uncertainty: ✓
- What could be wrong: May not have good data on market structure"""
    }
]

RUBRIC = """You are evaluating problem-solving responses. Score each solution on these criteria (1-10 scale):

1. **Completeness** (1-10): Does it address all key factors in the problem?
   - 1-3: Missing major considerations
   - 4-6: Covers basics, some gaps
   - 7-10: Addresses all key factors

2. **Correctness** (1-10): Is the logic and reasoning sound?
   - 1-3: Logical errors, wrong conclusions
   - 4-6: Minor errors, mostly sound
   - 7-10: Logically rigorous, valid

3. **Depth** (1-10): Does it trace consequences, consider dynamics?
   - 1-3: Surface-level only
   - 4-6: Some deeper analysis
   - 7-10: Multi-level, traces consequences

4. **Practicality** (1-10): Is it actionable and implementable?
   - 1-3: Unimplementable
   - 4-6: Could work with issues
   - 7-10: Clearly actionable

5. **Insight** (1-10): Does it surface non-obvious considerations?
   - 1-3: Obvious conclusions only
   - 4-6: Some non-obvious elements
   - 7-10: Novel, non-obvious insights

For each solution, provide:
1. Score for each dimension
2. Brief justification for each score
3. Total score (sum of 5 dimensions, max 50)

IMPORTANT: Evaluate each solution on its own merits. You don't know how these solutions were generated - just assess their quality."""


def create_evaluation_prompt(problem: dict, solution_a: str, solution_b: str) -> str:
    """Create the prompt for blind evaluation."""
    return f"""{RUBRIC}

---

## Problem: {problem['name']}

{problem['problem']}

---

## Solution A:

{solution_a}

---

## Solution B:

{solution_b}

---

Please evaluate both solutions using the rubric above. Provide scores and justifications for each dimension, then total scores.

Format your response as JSON:
{{
  "solution_a": {{
    "completeness": {{"score": X, "justification": "..."}},
    "correctness": {{"score": X, "justification": "..."}},
    "depth": {{"score": X, "justification": "..."}},
    "practicality": {{"score": X, "justification": "..."}},
    "insight": {{"score": X, "justification": "..."}},
    "total": X
  }},
  "solution_b": {{
    "completeness": {{"score": X, "justification": "..."}},
    "correctness": {{"score": X, "justification": "..."}},
    "depth": {{"score": X, "justification": "..."}},
    "practicality": {{"score": X, "justification": "..."}},
    "insight": {{"score": X, "justification": "..."}},
    "total": X
  }}
}}"""


def run_blind_evaluation(api_key: str):
    """Run blind evaluation on all problems."""
    client = anthropic.Anthropic(api_key=api_key)

    results = []

    for problem in PROBLEMS:
        # Randomize order - flip a coin for each problem
        baseline_is_a = random.choice([True, False])

        if baseline_is_a:
            solution_a = problem["baseline"]
            solution_b = problem["protocol"]
            mapping = {"A": "baseline", "B": "protocol"}
        else:
            solution_a = problem["protocol"]
            solution_b = problem["baseline"]
            mapping = {"A": "protocol", "B": "baseline"}

        prompt = create_evaluation_prompt(problem, solution_a, solution_b)

        print(f"\n{'='*60}")
        print(f"Evaluating Problem {problem['id']}: {problem['name']} ({problem['type']})")
        print(f"Order: A={mapping['A']}, B={mapping['B']}")
        print(f"{'='*60}")

        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text
            print(f"\nRaw response:\n{response_text}\n")

            # Try to parse JSON from response
            # Find JSON block
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                scores = json.loads(json_str)

                # Map back to baseline/protocol
                if baseline_is_a:
                    baseline_score = scores["solution_a"]["total"]
                    protocol_score = scores["solution_b"]["total"]
                    baseline_details = scores["solution_a"]
                    protocol_details = scores["solution_b"]
                else:
                    baseline_score = scores["solution_b"]["total"]
                    protocol_score = scores["solution_a"]["total"]
                    baseline_details = scores["solution_b"]
                    protocol_details = scores["solution_a"]

                result = {
                    "problem_id": problem["id"],
                    "problem_name": problem["name"],
                    "problem_type": problem["type"],
                    "baseline_score": baseline_score,
                    "protocol_score": protocol_score,
                    "difference": protocol_score - baseline_score,
                    "baseline_details": baseline_details,
                    "protocol_details": protocol_details,
                    "order": mapping
                }
                results.append(result)

                print(f"Baseline: {baseline_score}/50")
                print(f"Protocol: {protocol_score}/50")
                print(f"Difference: {protocol_score - baseline_score:+d}")
            else:
                print("ERROR: Could not parse JSON from response")

        except Exception as e:
            print(f"ERROR evaluating problem {problem['id']}: {e}")

    return results


def print_summary(results: list):
    """Print summary of results."""
    print("\n" + "="*80)
    print("BLIND EVALUATION RESULTS SUMMARY")
    print("="*80)

    print("\n| Problem | Type | Baseline | Protocol | Δ |")
    print("|---------|------|----------|----------|---|")

    total_baseline = 0
    total_protocol = 0

    for r in results:
        print(f"| {r['problem_name']} | {r['problem_type']} | {r['baseline_score']} | {r['protocol_score']} | {r['difference']:+d} |")
        total_baseline += r['baseline_score']
        total_protocol += r['protocol_score']

    n = len(results)
    avg_baseline = total_baseline / n if n > 0 else 0
    avg_protocol = total_protocol / n if n > 0 else 0
    avg_diff = avg_protocol - avg_baseline

    print(f"| **Average** | - | **{avg_baseline:.1f}** | **{avg_protocol:.1f}** | **{avg_diff:+.1f}** |")

    print("\n" + "="*80)
    print("HYPOTHESIS CHECK")
    print("="*80)

    threshold = 5
    passed = avg_diff > threshold

    print(f"\nPre-registered threshold: Protocol > Baseline + {threshold} points")
    print(f"Actual difference: {avg_diff:+.1f} points")
    print(f"Result: {'PASSED ✓' if passed else 'FAILED ✗'}")

    # Check consistency
    protocol_wins = sum(1 for r in results if r['difference'] > 0)
    print(f"\nProtocol won on {protocol_wins}/{n} problems")

    return {
        "avg_baseline": avg_baseline,
        "avg_protocol": avg_protocol,
        "avg_diff": avg_diff,
        "passed_threshold": passed,
        "protocol_wins": protocol_wins,
        "total_problems": n
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python blind_problem_solving_eval.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]

    print("Starting blind evaluation...")
    print("External Claude instance will score solutions without knowing which used protocols.")
    print()

    results = run_blind_evaluation(api_key)

    if results:
        summary = print_summary(results)

        # Save full results
        with open("/home/user/claude/Meta/blind_eval_results.json", "w") as f:
            json.dump({
                "results": results,
                "summary": summary
            }, f, indent=2)

        print(f"\nFull results saved to blind_eval_results.json")
