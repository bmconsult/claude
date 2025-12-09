#!/usr/bin/env python3
"""
Hybrid Methodology Test

Combines the best elements:
1. v5.2's verification and implementation rigor
2. Multi-strategy's competing approaches
3. Higher sample size for statistical validity
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

HYBRID_METHODOLOGY_V6 = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v6.0 (HYBRID)**

**STEP 0: GENERATE COMPETING STRATEGIES (NEW)**
Before any deep analysis, generate 3 FUNDAMENTALLY DIFFERENT approaches:
1. **Strategy A (Conventional)**: The obvious/expected approach
2. **Strategy B (Contrarian)**: What if we did the opposite of the obvious?
3. **Strategy C (Lateral)**: An approach borrowed from an unrelated domain

For each, state in 2 sentences: What's the core bet? What must be true for this to win?

**STEP 1: FRAME + SELECT**
What type of problem is this?
- Analytical: Clear answer exists, decomposable
- Systems: Feedback loops, dynamics, delays
- Adversarial: Other agents who will respond
- Wicked: Multiple stakeholders, value conflicts
- Hybrid: Multiple types

Based on framing, select the 1-2 most promising strategies from Step 0 for deep analysis.
State why you're selecting these (what makes them robust to the problem type).

**STEP 2: ASSUMPTION AUDIT (for selected strategies)**
1. List EVERY embedded assumption
2. For EACH, ask "What if this is wrong?"
3. Identify top 3 assumptions that most change the answer
4. Which strategy is most robust to assumption failures?

**STEP 3: DOMAIN-SPECIFIC ANALYSIS**
Apply only the relevant tools:
- **If Systems/Wicked**: Map ALL feedback loops, find leverage points
- **If Adversarial**: Trace 3+ response chains, evaluate at END of chain
- **If Analytical**: Decompose, solve sub-problems

**STEP 4: IMPLEMENTATION PLAN**
For your recommended solution:
1. WHO: Specific roles/people responsible
2. WHEN: Timeline with key milestones (weeks/months, not "soon")
3. WHAT: Success metrics and decision criteria
4. HOW MUCH: Resources with justification (cite comparables or state "NEEDS VALIDATION")
5. HOW: Exact mechanism of execution
6. SCRIPT: For interpersonal components, provide exact words
7. RESISTANCE MAP: 3 sources of resistance + countermeasures with thresholds

**STEP 5: VERIFY**
1. Check solution against ALL stated constraints
2. Does this actually answer the original question?
3. What could make this wrong?
4. COMPOUND FAILURE TEST: What if top 3 assumptions ALL wrong? What's backup?
5. INTERACTION STRESS TEST: How do assumption failures compound each other?
6. MONITOR: One measurable indicator + threshold for each top assumption
7. CONTINGENCY: Fallback if milestones slip 20%+
8. State confidence level explicitly

**META-RULE:**
- The best strategy often emerges from CONTRAST between options
- If stuck → you're solving the wrong problem → return to Step 0
- If Hybrid problem → apply MULTIPLE tools
"""

BASELINE_V52 = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

STEP 0: FRAME THE PROBLEM
What type of problem is this?
- Analytical: Clear answer exists, decomposable
- Systems: Feedback loops, dynamics, delays
- Adversarial: Other agents who will respond to your moves
- Wicked: Multiple stakeholders, value conflicts, no clean answer
- Hybrid: Multiple types (most real problems)

State your classification. If Hybrid, note all types that apply.

STEP 1: ASSUMPTION AUDIT (mandatory)
1. List EVERY embedded assumption
2. For EACH assumption, ask "What if this is wrong?"
3. Identify the top 3 assumptions that most change the answer
4. Keep these visible throughout your analysis

STEP 2: LEVERAGE FINDER (apply if Systems or Wicked)
1. Map ALL feedback loops (reinforcing and balancing)
2. Identify where small input creates large output
3. Prioritize high-leverage interventions over symptom treatment

STEP 3: RESPONSE CHAIN (apply if Adversarial)
1. For each option, trace what others would do in response
2. Then what you'd do to their response
3. Trace 3+ moves minimum
4. Evaluate outcomes at the END of the chain, not after your first move

STEP 4: IMPLEMENTATION PLAN (mandatory)
For your recommended solution, specify:
1. WHO: Specific roles/people responsible
2. WHEN: Timeline with key milestones
3. WHAT: Success metrics and decision criteria
4. HOW MUCH: Required resources with justification
5. HOW: Exact mechanism of execution
6. SCRIPT: Exact words for interpersonal components
7. RESISTANCE MAP: 3 sources of resistance + countermeasures with thresholds

STEP 5: VERIFY (mandatory)
1. Check solution against ALL stated constraints
2. Does this actually answer the original question?
3. What could make this answer wrong?
4. COMPOUND FAILURE TEST: What if top 3 assumptions ALL wrong?
5. INTERACTION STRESS TEST: How do assumption failures compound each other?
6. MONITOR: Measurable indicator + threshold for each top assumption
7. CONTINGENCY: Fallback if milestones slip 20%+
8. State confidence level explicitly

META-RULE:
If problem is Hybrid → apply MULTIPLE tools
If stuck → you're solving the wrong problem → return to Step 0
"""

PROBLEMS = [
    "You're CEO of a 200-person SaaS company. Your biggest competitor just got acquired by Microsoft. Your top 3 engineers are being recruited heavily. Revenue growth has slowed from 40% to 15% YoY. What's your strategy?",
    "You're Head of HR. An anonymous report alleges your highest-performing sales director is creating a hostile environment. Sales are up 50% under their leadership. The alleged victims are afraid to come forward. What do you do?",
    "Your engineering team's velocity has dropped 40% over 6 months. Exit interviews cite 'too many meetings' and 'unclear priorities.' Adding more engineers hasn't helped. What's wrong and how do you fix it?",
    "A former employee is starting a competing company and recruiting your team. They have insider knowledge of your roadmap. Three key people have already left. How do you respond?",
    "You're founder of a 5-year-old startup. You've raised $20M, have 50 employees, $5M ARR growing 30%. A competitor just raised $100M. Your lead investor suggests you either raise a big round now or consider acquisition. What do you do?",
    "Your hospital's top surgeon (40% of revenue) has been falsifying credentials. Firing means bankruptcy. Keeping means patient risk. Board meets tomorrow.",
    "You run a successful restaurant chain (15 locations). A new food delivery app is demanding 30% commission or they'll delist you. 40% of your orders come through them. What do you do?",
    "Your AI startup has built a tool that can detect lies with 85% accuracy. Law enforcement wants to buy it. Civil liberties groups are protesting. Your investors are split. What's your decision?",
]

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Did they identify critical hidden assumptions?
2. STRATEGIC DEPTH (1-10): Did they trace consequences, dynamics, 2nd/3rd order effects?
3. FRAME QUALITY (1-10): Did they find the RIGHT way to think about the problem?
4. ACTIONABILITY (1-10): Is the recommendation specific and executable tomorrow?
5. VERIFICATION (1-10): Did they check reasoning, state uncertainty, identify what could be wrong?

Be rigorous. 8+ requires excellence. 9+ requires exceptional insight.

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X, "weakest": "dimension_name", "gap": "specific weakness"}
"""


class HybridTest:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def solve(self, problem: str, methodology: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3500,
            messages=[{"role": "user", "content": f"Apply this methodology:\n\n{methodology}\n\n---\n\nPROBLEM:\n{problem}"}]
        )
        return response.content[0].text

    def evaluate(self, problem: str, solution: str) -> Optional[Dict]:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": f"{EVAL_RUBRIC}\n\nPROBLEM:\n{problem}\n\nSOLUTION:\n{solution}"}]
        )
        try:
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            return json.loads(text[json_start:json_end])
        except:
            return None

    def test_methodology(self, name: str, methodology: str, n_problems: int = 5) -> Dict:
        """Test a methodology on n problems."""
        print(f"\n{'='*60}")
        print(f"TESTING: {name}")
        print(f"{'='*60}")

        problems = random.sample(PROBLEMS, min(n_problems, len(PROBLEMS)))
        scores = []
        dimension_scores = {
            'assumption_surfacing': [],
            'strategic_depth': [],
            'frame_quality': [],
            'actionability': [],
            'verification': []
        }

        for i, problem in enumerate(problems):
            print(f"  Problem {i+1}/{n_problems}...", end=" ")
            solution = self.solve(problem, methodology)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                total = eval_result.get('total', 0)
                scores.append(total)
                for dim in dimension_scores:
                    if dim in eval_result:
                        dimension_scores[dim].append(eval_result[dim])
                print(f"{total}/50")
            time.sleep(0.5)

        avg = sum(scores) / len(scores) if scores else 0
        print(f"\nAverage: {avg:.1f}/50")
        print(f"Min: {min(scores)}/50  Max: {max(scores)}/50")

        # Dimension breakdown
        print("\nDimension breakdown:")
        for dim, dim_scores in dimension_scores.items():
            if dim_scores:
                dim_avg = sum(dim_scores) / len(dim_scores)
                print(f"  {dim}: {dim_avg:.1f}/10")

        return {
            "name": name,
            "avg": avg,
            "scores": scores,
            "min": min(scores),
            "max": max(scores),
            "dimension_avgs": {d: sum(s)/len(s) if s else 0 for d, s in dimension_scores.items()}
        }

    def run_comparison(self, n_problems: int = 5):
        """Compare baseline v5.2 vs hybrid v6.0"""
        print("="*60)
        print("HYBRID METHODOLOGY COMPARISON TEST")
        print("="*60)
        print(f"Testing each methodology on {n_problems} problems")
        print("Higher sample size for statistical validity")

        baseline_result = self.test_methodology("BASELINE v5.2", BASELINE_V52, n_problems)
        time.sleep(1)
        hybrid_result = self.test_methodology("HYBRID v6.0", HYBRID_METHODOLOGY_V6, n_problems)

        # Summary
        print("\n" + "="*60)
        print("FINAL COMPARISON")
        print("="*60)

        delta = hybrid_result['avg'] - baseline_result['avg']
        if delta > 0:
            winner = "HYBRID v6.0"
            symbol = "✅"
        elif delta < 0:
            winner = "BASELINE v5.2"
            symbol = "❌"
        else:
            winner = "TIE"
            symbol = "⚖️"

        print(f"\n{symbol} {winner} wins by {abs(delta):.1f} points")
        print(f"\nBASELINE v5.2: {baseline_result['avg']:.1f}/50 (range: {baseline_result['min']}-{baseline_result['max']})")
        print(f"HYBRID v6.0:   {hybrid_result['avg']:.1f}/50 (range: {hybrid_result['min']}-{hybrid_result['max']})")

        print("\nDimension comparison (Hybrid - Baseline):")
        for dim in baseline_result['dimension_avgs']:
            b = baseline_result['dimension_avgs'].get(dim, 0)
            h = hybrid_result['dimension_avgs'].get(dim, 0)
            diff = h - b
            symbol = "+" if diff > 0 else ""
            print(f"  {dim}: {symbol}{diff:.1f}")

        # Save results
        results = {
            "baseline": baseline_result,
            "hybrid": hybrid_result,
            "delta": delta,
            "winner": winner,
            "timestamp": datetime.now().isoformat()
        }

        with open("/home/user/claude/Meta/hybrid_comparison_results.json", "w") as f:
            json.dump(results, f, indent=2)

        return results


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python hybrid_methodology_test.py <API_KEY> [n_problems]")
        sys.exit(1)

    api_key = sys.argv[1]
    n_problems = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    test = HybridTest(api_key)
    test.run_comparison(n_problems)


if __name__ == "__main__":
    main()
