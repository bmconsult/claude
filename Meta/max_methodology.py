#!/usr/bin/env python3
"""
MAXIMUM METHODOLOGY - Push to theoretical ceiling

Aggressive strategies:
1. Recursive Refinement: Solve → Critique → Improve → Repeat
2. Expert Ensemble: Multiple legendary strategists, select best
3. Higher sample size for statistical validity
4. Track individual dimension scores to find weakest link
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

# The optimized v5.2 baseline
METHODOLOGY_V52 = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

STEP 0: FRAME THE PROBLEM
- Analytical / Systems / Adversarial / Wicked / Hybrid
- State classification

STEP 1: ASSUMPTION AUDIT
- List ALL assumptions
- "What if wrong?" for each
- Top 3 that most change answer

STEP 2: LEVERAGE FINDER (Systems/Wicked)
- Map feedback loops
- Find high-leverage points

STEP 3: RESPONSE CHAIN (Adversarial)
- Trace 3+ moves
- Evaluate at END

STEP 4: IMPLEMENTATION PLAN
1. WHO - Specific roles
2. WHEN - Timeline with milestones
3. WHAT - Success metrics
4. HOW MUCH - Resources + justification
5. HOW - Exact mechanism
6. SCRIPT - Exact words for interpersonal
7. RESISTANCE MAP - 3 sources + countermeasures + thresholds

STEP 5: VERIFY
1. Check ALL constraints
2. Does this answer the question?
3. What could make this wrong?
4. COMPOUND FAILURE TEST - all top 3 assumptions wrong
5. INTERACTION STRESS TEST - how failures compound
6. MONITOR indicators
7. CONTINGENCY for slippage
8. Confidence level

META-RULE: Hybrid → multiple tools | Stuck → wrong frame → Step 0
"""

# Recursive refinement methodology
RECURSIVE_REFINEMENT = """**RECURSIVE REFINEMENT PROTOCOL**

PHASE 1: INITIAL SOLUTION
Apply v5.2 methodology to generate your best solution.

PHASE 2: ADVERSARIAL CRITIQUE
Now attack your own solution:
- What's the fatal flaw a hostile board member would find?
- What would a competitor do to counter this?
- Where will implementation actually fail?

Identify the TOP 3 WEAKNESSES.

PHASE 3: FORTIFY
Modify your solution to address each weakness. Be specific.

PHASE 4: FINAL VERIFICATION
- Does the fortified solution still answer the original question?
- Is it still actionable?
- State final confidence level.

Output your FORTIFIED solution as your answer.
"""

# Expert ensemble - legendary strategists
EXPERT_ENSEMBLE = """**EXPERT ENSEMBLE PROTOCOL**

Generate solutions from 3 different strategic perspectives:

**PERSPECTIVE 1 - THE OPERATOR (Andy Grove)**
Focus on: Execution, metrics, operational excellence
Ask: "What are the key operational indicators? Where's the 10x leverage?"

**PERSPECTIVE 2 - THE DISRUPTOR (Clayton Christensen)**
Focus on: Disruption patterns, jobs-to-be-done, asymmetric competition
Ask: "What job is really being hired for? Where's the disruptive opportunity?"

**PERSPECTIVE 3 - THE GAME THEORIST (John Nash)**
Focus on: Equilibria, incentives, strategic interactions
Ask: "What's the Nash equilibrium? How do incentives align or misalign?"

For each perspective, generate a 2-3 sentence strategy.

Then SYNTHESIZE: What elements from each perspective should be combined?

Output your SYNTHESIZED solution with implementation details (WHO, WHEN, WHAT, HOW).
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
    "You're negotiating a major partnership. The other side knows you need this deal more than they do. Your alternative options are limited. How do you get a fair deal?",
    "A key supplier just went bankrupt. You have 2 weeks of inventory. Alternative suppliers require 6-week lead time. Stopping production loses your biggest customer forever. What do you do?",
]

EVAL_RUBRIC = """Score this solution RIGOROUSLY on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Did they identify critical hidden assumptions? Question the obvious? Find non-obvious assumptions?
   - 7 = Good assumption identification
   - 8 = Excellent, found non-obvious assumptions
   - 9 = Exceptional, found assumptions others would miss
   - 10 = World-class insight into hidden assumptions

2. STRATEGIC DEPTH (1-10): Did they trace 2nd/3rd order consequences? Consider dynamics? Think multiple levels?
   - 7 = Good strategic thinking
   - 8 = Excellent multi-order analysis
   - 9 = Exceptional strategic depth
   - 10 = Grandmaster-level strategic thinking

3. FRAME QUALITY (1-10): Did they find the RIGHT way to think about this? Avoid obvious/cliche frames?
   - 7 = Good framing
   - 8 = Excellent, non-obvious frame
   - 9 = Exceptional reframe that unlocks new solutions
   - 10 = Brilliant frame that transforms the problem

4. ACTIONABILITY (1-10): Is this specific and executable TOMORROW? Not vague platitudes?
   - 7 = Good specificity
   - 8 = Excellent, could execute immediately
   - 9 = Exceptional detail and clarity
   - 10 = Perfect implementation blueprint

5. VERIFICATION (1-10): Did they check reasoning? State uncertainty? Identify failure modes?
   - 7 = Good verification
   - 8 = Excellent stress-testing
   - 9 = Exceptional failure mode analysis
   - 10 = Bulletproof verification

BE HARSH. 8+ is rare. 9+ is exceptional. 10 is almost never given.

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X, "weakest": "dimension_name", "strongest": "dimension_name", "gap": "specific weakness"}
"""


class MaxMethodology:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.results = []

    def solve(self, problem: str, methodology: str, temperature: float = 0.7) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=temperature,
            messages=[{"role": "user", "content": f"Apply this methodology:\n\n{methodology}\n\n---\n\nPROBLEM:\n{problem}"}]
        )
        return response.content[0].text

    def evaluate(self, problem: str, solution: str) -> Optional[Dict]:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            temperature=0.3,  # Lower temp for consistent evaluation
            messages=[{"role": "user", "content": f"{EVAL_RUBRIC}\n\nPROBLEM:\n{problem}\n\nSOLUTION:\n{solution}"}]
        )
        try:
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            return json.loads(text[json_start:json_end])
        except:
            return None

    def recursive_refine(self, problem: str, initial_solution: str) -> str:
        """Apply recursive refinement to improve solution."""
        prompt = f"""Here is a strategic problem and an initial solution.

PROBLEM:
{problem}

INITIAL SOLUTION:
{initial_solution}

---

Now apply RECURSIVE REFINEMENT:

1. CRITIQUE: What are the top 3 weaknesses or blind spots in this solution?

2. FORTIFY: For each weakness, specify exactly how to address it.

3. OUTPUT: Write the IMPROVED solution incorporating all fixes. Be specific and actionable.

Output the improved solution:"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def test_methodology(self, name: str, methodology: str, n_problems: int = 6,
                         use_refinement: bool = False) -> Dict:
        """Test methodology with optional recursive refinement."""
        print(f"\n{'='*60}")
        print(f"TESTING: {name}")
        if use_refinement:
            print("  + Recursive Refinement")
        print(f"{'='*60}")

        problems = random.sample(PROBLEMS, min(n_problems, len(PROBLEMS)))
        scores = []
        dimension_totals = {
            'assumption_surfacing': [],
            'strategic_depth': [],
            'frame_quality': [],
            'actionability': [],
            'verification': []
        }

        for i, problem in enumerate(problems):
            print(f"\n  Problem {i+1}/{n_problems}:")
            print(f"    Generating solution...", end=" ")

            solution = self.solve(problem, methodology)

            if use_refinement:
                print("refining...", end=" ")
                solution = self.recursive_refine(problem, solution)

            print("evaluating...", end=" ")
            eval_result = self.evaluate(problem, solution)

            if eval_result:
                total = eval_result.get('total', 0)
                scores.append(total)
                for dim in dimension_totals:
                    if dim in eval_result:
                        dimension_totals[dim].append(eval_result[dim])

                weakest = eval_result.get('weakest', 'unknown')
                print(f"{total}/50 (weakest: {weakest})")
            else:
                print("eval failed")

            time.sleep(0.5)

        avg = sum(scores) / len(scores) if scores else 0

        print(f"\n  RESULTS:")
        print(f"    Average: {avg:.1f}/50")
        print(f"    Range: {min(scores)}-{max(scores)}/50")
        print(f"    Scores: {scores}")

        print(f"\n  DIMENSIONS:")
        dim_avgs = {}
        for dim, vals in dimension_totals.items():
            if vals:
                dim_avg = sum(vals) / len(vals)
                dim_avgs[dim] = dim_avg
                print(f"    {dim}: {dim_avg:.1f}/10")

        return {
            "name": name,
            "avg": avg,
            "scores": scores,
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "dimension_avgs": dim_avgs,
            "use_refinement": use_refinement
        }

    def run_max_test(self, n_problems: int = 6):
        """Run maximum methodology test."""
        print("="*60)
        print("🚀 MAXIMUM METHODOLOGY TEST")
        print("="*60)
        print(f"Testing on {n_problems} problems each")
        print("Goal: Break the 44/50 ceiling")

        configs = [
            ("Baseline v5.2", METHODOLOGY_V52, False),
            ("v5.2 + Recursive Refinement", METHODOLOGY_V52, True),
            ("Expert Ensemble", EXPERT_ENSEMBLE, False),
            ("Expert Ensemble + Refinement", EXPERT_ENSEMBLE, True),
        ]

        all_results = []
        for name, methodology, use_refinement in configs:
            result = self.test_methodology(name, methodology, n_problems, use_refinement)
            all_results.append(result)
            time.sleep(1)

        # Summary
        print("\n" + "="*60)
        print("🏆 FINAL RANKINGS")
        print("="*60)

        sorted_results = sorted(all_results, key=lambda x: x['avg'], reverse=True)

        for i, r in enumerate(sorted_results):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
            ref = " +R" if r.get('use_refinement') else ""
            print(f"{medal} {r['name']}{ref}: {r['avg']:.1f}/50 (range: {r['min']}-{r['max']})")

        best = sorted_results[0]
        print(f"\n🎯 BEST: {best['name']} at {best['avg']:.1f}/50")
        print(f"   Peak individual score: {best['max']}/50")

        # Dimension analysis
        print("\n📊 DIMENSION ANALYSIS (best methodology):")
        if best.get('dimension_avgs'):
            dims = sorted(best['dimension_avgs'].items(), key=lambda x: x[1])
            print(f"   Weakest: {dims[0][0]} ({dims[0][1]:.1f}/10)")
            print(f"   Strongest: {dims[-1][0]} ({dims[-1][1]:.1f}/10)")

        # Save results
        output = {
            "results": all_results,
            "best": best['name'],
            "best_avg": best['avg'],
            "best_max": best['max'],
            "timestamp": datetime.now().isoformat()
        }

        with open("/home/user/claude/Meta/max_methodology_results.json", "w") as f:
            json.dump(output, f, indent=2)

        return all_results


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python max_methodology.py <API_KEY> [n_problems]")
        sys.exit(1)

    api_key = sys.argv[1]
    n_problems = int(sys.argv[2]) if len(sys.argv) > 2 else 6

    test = MaxMethodology(api_key)
    test.run_max_test(n_problems)


if __name__ == "__main__":
    main()
