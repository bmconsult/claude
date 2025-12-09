#!/usr/bin/env python3
"""
Paradigm Shift Loop - Breaking the 44/50 Ceiling

The incremental approach plateaued. This tries FUNDAMENTALLY different strategies:
1. Multi-Strategy Generation (compete strategies against each other)
2. Adversarial Self-Critique (attack your own solution)
3. Frame Exploration (try multiple frames before solving)
4. Constraint Inversion (what if the opposite of each assumption is true?)

Each paradigm shift is tested against the current best methodology.
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

# Current best methodology (v5.2 at 44.3/50)
BASELINE_METHODOLOGY = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

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

# Paradigm shift methodologies to test
PARADIGM_SHIFTS = {
    "multi_strategy": """**STRATEGIC PROBLEM-SOLVING PROTOCOL - MULTI-STRATEGY VARIANT**

STEP 0: FRAME THE PROBLEM
Same as baseline - classify problem type (Analytical/Systems/Adversarial/Wicked/Hybrid)

STEP 1: GENERATE 3 COMPETING STRATEGIES
Before deep analysis, generate 3 FUNDAMENTALLY DIFFERENT strategies:
- Strategy A: The obvious/conventional approach
- Strategy B: The contrarian approach (what if we do the opposite?)
- Strategy C: The creative/lateral approach (borrowed from unrelated domain)

For each, state in 2-3 sentences: What's the core bet? What would have to be true for this to be the best option?

STEP 2: ASSUMPTION AUDIT (for each strategy)
1. List key assumptions unique to each strategy
2. Identify which strategy is most robust to assumption failures
3. Identify which strategy has highest upside if assumptions hold

STEP 3: STRESS TEST THE LEADING STRATEGY
Apply full analysis (leverage finder, response chain as relevant) ONLY to the most promising 1-2 strategies.
Don't waste depth on strategies that won't survive scrutiny.

STEP 4: IMPLEMENTATION PLAN
Same as baseline - WHO, WHEN, WHAT, HOW MUCH, HOW, SCRIPT, RESISTANCE MAP

STEP 5: VERIFY
Same as baseline - all verification steps including compound failure test

META-RULE: The best strategy often emerges from the CONTRAST between options, not from any single analysis.
""",

    "adversarial_self_critique": """**STRATEGIC PROBLEM-SOLVING PROTOCOL - ADVERSARIAL SELF-CRITIQUE VARIANT**

STEP 0: FRAME THE PROBLEM
Same as baseline - classify problem type

STEP 1: ASSUMPTION AUDIT
Same as baseline - list assumptions, identify top 3

STEP 2: GENERATE INITIAL SOLUTION
Apply relevant analysis (leverage finder, response chain) and create your best solution.

STEP 3: ADVERSARIAL ATTACK (NEW - mandatory)
Now ATTACK your own solution as if you were:
1. A hostile board member who wants to kill the proposal
2. A competitor who knows this plan and will counter it
3. A cynical employee who will resist implementation

For each attacker perspective, identify the BEST critique. Don't strawman.

STEP 4: FORTIFIED SOLUTION
Modify your solution to address the strongest attacks from Step 3.
If an attack is unanswerable, acknowledge the risk explicitly.

STEP 5: IMPLEMENTATION PLAN
Same as baseline - WHO, WHEN, WHAT, HOW MUCH, HOW, SCRIPT, RESISTANCE MAP

STEP 6: VERIFY
Same as baseline - all verification steps

META-RULE: A solution that survives adversarial attack is stronger than one that's never been challenged.
""",

    "frame_exploration": """**STRATEGIC PROBLEM-SOLVING PROTOCOL - FRAME EXPLORATION VARIANT**

STEP 0: EXPLORE MULTIPLE FRAMES (NEW)
Before classifying, consider 4 different ways to frame this problem:
1. THE PRESENTED FRAME: How the problem was stated
2. THE DEEPER FRAME: What's the REAL problem behind the stated problem?
3. THE STAKEHOLDER FRAME: Who else cares, and how would they frame it?
4. THE CONSTRAINT FRAME: What if we removed the biggest constraint?

State which frame you're adopting and WHY it's the most productive.

STEP 1: ASSUMPTION AUDIT
Same as baseline - but audit assumptions about the FRAME itself, not just the problem

STEP 2: SOLVE IN YOUR CHOSEN FRAME
Apply relevant analysis tools based on problem type

STEP 3: CROSS-FRAME CHECK
Briefly check: Would your solution still work in the other 3 frames?
If not, what does that reveal about hidden assumptions?

STEP 4: IMPLEMENTATION PLAN
Same as baseline

STEP 5: VERIFY
Same as baseline

META-RULE: The frame determines the solution. Finding the right frame is half the battle.
""",

    "constraint_inversion": """**STRATEGIC PROBLEM-SOLVING PROTOCOL - CONSTRAINT INVERSION VARIANT**

STEP 0: FRAME THE PROBLEM
Same as baseline

STEP 1: CONSTRAINT MAPPING
List ALL constraints (explicit and implicit):
- Time constraints
- Resource constraints
- Political constraints
- Technical constraints
- Relationship constraints

STEP 2: CONSTRAINT INVERSION (NEW)
For the top 3 constraints, ask:
"What if the OPPOSITE of this constraint were true?"
- If time is short, what if we had unlimited time? (reveals what we really want)
- If budget is tight, what if money was no object? (reveals hidden priorities)
- If politics prevent X, what if we had full authority? (reveals true solution)

STEP 3: CONSTRAINT-AWARE SOLUTION
Now solve the ORIGINAL problem, but informed by what constraint inversion revealed.
Often the inversion shows where constraints are actually soft.

STEP 4: IMPLEMENTATION PLAN
Same as baseline

STEP 5: VERIFY
Same as baseline + verify you're not accepting false constraints

META-RULE: Most constraints are softer than they appear. Inversion reveals which ones to challenge.
"""
}

PROBLEMS = [
    "You're CEO of a 200-person SaaS company. Your biggest competitor just got acquired by Microsoft. Your top 3 engineers are being recruited heavily. Revenue growth has slowed from 40% to 15% YoY. What's your strategy?",
    "You're Head of HR. An anonymous report alleges your highest-performing sales director is creating a hostile environment. Sales are up 50% under their leadership. The alleged victims are afraid to come forward. What do you do?",
    "Your engineering team's velocity has dropped 40% over 6 months. Exit interviews cite 'too many meetings' and 'unclear priorities.' Adding more engineers hasn't helped. What's wrong and how do you fix it?",
    "A former employee is starting a competing company and recruiting your team. They have insider knowledge of your roadmap. Three key people have already left. How do you respond?",
    "You're founder of a 5-year-old startup. You've raised $20M, have 50 employees, $5M ARR growing 30%. A competitor just raised $100M. Your lead investor suggests you either raise a big round now or consider acquisition. What do you do?",
    "Your hospital's top surgeon (40% of revenue) has been falsifying credentials. Firing means bankruptcy. Keeping means patient risk. Board meets tomorrow.",
]

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Did they identify critical hidden assumptions? Did they question the obvious?
2. STRATEGIC DEPTH (1-10): Did they trace consequences, dynamics, multi-level thinking? 2nd/3rd order effects?
3. FRAME QUALITY (1-10): Did they find the RIGHT way to think about the problem? Avoid obvious frames?
4. ACTIONABILITY (1-10): Is the recommendation specific and executable? Could someone DO this tomorrow?
5. VERIFICATION (1-10): Did they check reasoning, state uncertainty, identify what could be wrong?

Be rigorous. 8+ requires excellence. 9+ requires exceptional insight.

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X, "weakest": "dimension_name", "gap": "specific weakness"}
"""


class ParadigmShiftLoop:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.baseline_methodology = BASELINE_METHODOLOGY
        self.results = []

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

    def test_methodology(self, methodology: str, n_problems: int = 3) -> tuple:
        """Test methodology, return (avg_score, scores, details)"""
        problems = random.sample(PROBLEMS, min(n_problems, len(PROBLEMS)))
        scores = []
        details = []

        for i, problem in enumerate(problems):
            print(f"    Problem {i+1}...", end=" ")
            solution = self.solve(problem, methodology)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                score = eval_result.get('total', 0)
                scores.append(score)
                details.append(eval_result)
                print(f"{score}/50")
            time.sleep(0.5)

        avg = sum(scores) / len(scores) if scores else 0
        return avg, scores, details

    def test_paradigm_shift(self, name: str, methodology: str, n_problems: int = 4):
        """Test a paradigm shift against baseline."""
        print(f"\n{'='*60}")
        print(f"TESTING PARADIGM SHIFT: {name.upper()}")
        print(f"{'='*60}")

        # Test baseline
        print("\n📊 Testing BASELINE methodology...")
        baseline_avg, baseline_scores, baseline_details = self.test_methodology(
            self.baseline_methodology, n_problems
        )
        print(f"Baseline average: {baseline_avg:.1f}/50")

        # Test paradigm shift
        print(f"\n🔬 Testing {name} methodology...")
        shift_avg, shift_scores, shift_details = self.test_methodology(
            methodology, n_problems
        )
        print(f"{name} average: {shift_avg:.1f}/50")

        # Compare
        delta = shift_avg - baseline_avg
        if delta > 0:
            print(f"\n✅ PARADIGM SHIFT WINS: +{delta:.1f} points")
            winner = name
        elif delta < 0:
            print(f"\n❌ BASELINE WINS: {delta:.1f} points")
            winner = "baseline"
        else:
            print(f"\n⚖️ TIE: 0.0 points difference")
            winner = "tie"

        result = {
            "paradigm": name,
            "baseline_avg": baseline_avg,
            "baseline_scores": baseline_scores,
            "shift_avg": shift_avg,
            "shift_scores": shift_scores,
            "delta": delta,
            "winner": winner,
            "baseline_details": baseline_details,
            "shift_details": shift_details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        return result

    def run_all_paradigm_shifts(self, n_problems: int = 4):
        """Test all paradigm shifts and find the best."""
        print("="*60)
        print("PARADIGM SHIFT EXPERIMENT")
        print("="*60)
        print(f"Baseline: v5.2 (best score: 44.3/50)")
        print(f"Testing {len(PARADIGM_SHIFTS)} paradigm shifts")

        for name, methodology in PARADIGM_SHIFTS.items():
            self.test_paradigm_shift(name, methodology, n_problems)
            time.sleep(1)

        # Summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)

        wins = [r for r in self.results if r['winner'] == r['paradigm']]
        best = max(self.results, key=lambda x: x['shift_avg']) if self.results else None

        print(f"\nParadigm shifts that beat baseline: {len(wins)}/{len(self.results)}")

        for r in sorted(self.results, key=lambda x: x['delta'], reverse=True):
            status = "✅" if r['delta'] > 0 else "❌" if r['delta'] < 0 else "⚖️"
            print(f"  {status} {r['paradigm']}: {r['shift_avg']:.1f}/50 ({r['delta']:+.1f})")

        if best:
            print(f"\n🏆 BEST PARADIGM: {best['paradigm']} at {best['shift_avg']:.1f}/50")

        # Save results
        with open("/home/user/claude/Meta/paradigm_shift_results.json", "w") as f:
            json.dump({
                "results": self.results,
                "best_paradigm": best['paradigm'] if best else None,
                "best_score": best['shift_avg'] if best else None,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

        return self.results


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python paradigm_shift_loop.py <API_KEY> [n_problems_per_test]")
        sys.exit(1)

    api_key = sys.argv[1]
    n_problems = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    loop = ParadigmShiftLoop(api_key)
    loop.run_all_paradigm_shifts(n_problems)


if __name__ == "__main__":
    main()
