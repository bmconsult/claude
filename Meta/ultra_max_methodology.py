#!/usr/bin/env python3
"""
ULTRA-MAX METHODOLOGY - Multiple refinement iterations + targeted improvement

Key strategies:
1. Multiple refinement rounds (solve → refine → refine → refine)
2. Target weak dimensions explicitly (verification, actionability)
3. Best-of-N selection
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

METHODOLOGY_V52 = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

STEP 0: FRAME THE PROBLEM
- Analytical / Systems / Adversarial / Wicked / Hybrid

STEP 1: ASSUMPTION AUDIT
- List ALL assumptions, "What if wrong?", Top 3

STEP 2: LEVERAGE FINDER (Systems/Wicked)
- Map feedback loops, find high-leverage points

STEP 3: RESPONSE CHAIN (Adversarial)
- Trace 3+ moves, evaluate at END

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
4. COMPOUND FAILURE TEST
5. INTERACTION STRESS TEST
6. MONITOR indicators
7. CONTINGENCY for slippage
8. Confidence level

META-RULE: Hybrid → multiple tools | Stuck → wrong frame → Step 0
"""

TARGETED_REFINEMENT = """**TARGETED REFINEMENT PROTOCOL**

You are refining an existing solution. Focus on these specific weaknesses:

1. **VERIFICATION** - The solution may lack rigorous stress-testing. Add:
   - Specific failure scenarios and countermeasures
   - Explicit confidence levels with justification
   - What evidence would prove this approach WRONG?
   - Pre-mortem: "It's 6 months later and this failed. Why?"

2. **ACTIONABILITY** - The solution may be too vague. Add:
   - SPECIFIC next steps for Monday morning
   - Named individuals or roles responsible
   - Exact metrics with numerical thresholds
   - Timeline with dates, not "soon" or "later"

3. **STRATEGIC DEPTH** - The solution may be shallow. Add:
   - 2nd and 3rd order consequences
   - How competitors/stakeholders will respond
   - Feedback loops that could accelerate or derail

CRITIQUE the solution on these 3 dimensions, then OUTPUT the IMPROVED version.
Be specific. No vague platitudes.
"""

PROBLEMS = [
    "You're CEO of a 200-person SaaS company. Your biggest competitor just got acquired by Microsoft. Your top 3 engineers are being recruited heavily. Revenue growth has slowed from 40% to 15% YoY. What's your strategy?",
    "You're Head of HR. An anonymous report alleges your highest-performing sales director is creating a hostile environment. Sales are up 50% under their leadership. The alleged victims are afraid to come forward. What do you do?",
    "Your engineering team's velocity has dropped 40% over 6 months. Exit interviews cite 'too many meetings' and 'unclear priorities.' Adding more engineers hasn't helped. What's wrong and how do you fix it?",
    "A former employee is starting a competing company and recruiting your team. They have insider knowledge of your roadmap. Three key people have already left. How do you respond?",
    "You're founder of a 5-year-old startup. You've raised $20M, have 50 employees, $5M ARR growing 30%. A competitor just raised $100M. Your lead investor suggests you either raise a big round now or consider acquisition. What do you do?",
    "Your hospital's top surgeon (40% of revenue) has been falsifying credentials. Firing means bankruptcy. Keeping means patient risk. Board meets tomorrow.",
    "A key supplier just went bankrupt. You have 2 weeks of inventory. Alternative suppliers require 6-week lead time. Stopping production loses your biggest customer forever. What do you do?",
    "You're negotiating a major partnership. The other side knows you need this deal more than they do. Your alternative options are limited. How do you get a fair deal?",
]

EVAL_RUBRIC = """Score this solution RIGOROUSLY on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Critical hidden assumptions identified?
2. STRATEGIC DEPTH (1-10): 2nd/3rd order effects, dynamics, multi-level?
3. FRAME QUALITY (1-10): Right way to think about problem? Non-obvious?
4. ACTIONABILITY (1-10): Specific and executable TOMORROW? Named people, dates?
5. VERIFICATION (1-10): Stress-tested? Failure modes identified? Confidence stated?

BE HARSH. 8+ is rare. 9+ exceptional. 10 almost never.

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X, "weakest": "dimension_name"}
"""


class UltraMaxMethodology:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def solve(self, problem: str, methodology: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": f"Apply this methodology:\n\n{methodology}\n\n---\n\nPROBLEM:\n{problem}"}]
        )
        return response.content[0].text

    def refine(self, problem: str, solution: str) -> str:
        prompt = f"""PROBLEM:
{problem}

CURRENT SOLUTION:
{solution}

---

{TARGETED_REFINEMENT}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def evaluate(self, problem: str, solution: str) -> Optional[Dict]:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": f"{EVAL_RUBRIC}\n\nPROBLEM:\n{problem}\n\nSOLUTION:\n{solution}"}]
        )
        try:
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            return json.loads(text[json_start:json_end])
        except:
            return None

    def solve_with_iterations(self, problem: str, n_iterations: int = 3) -> tuple:
        """Solve with N refinement iterations, tracking improvement."""
        # Initial solution
        solution = self.solve(problem, METHODOLOGY_V52)
        scores = []

        # Evaluate initial
        eval_result = self.evaluate(problem, solution)
        if eval_result:
            scores.append(eval_result.get('total', 0))

        # Iterative refinement
        for i in range(n_iterations):
            solution = self.refine(problem, solution)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                scores.append(eval_result.get('total', 0))

        final_eval = self.evaluate(problem, solution)
        return solution, final_eval, scores

    def best_of_n(self, problem: str, n: int = 3) -> tuple:
        """Generate N solutions and return the best one."""
        solutions = []
        for _ in range(n):
            solution = self.solve(problem, METHODOLOGY_V52)
            # Apply one refinement pass
            solution = self.refine(problem, solution)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                solutions.append((solution, eval_result, eval_result.get('total', 0)))
            time.sleep(0.5)

        if not solutions:
            return None, None, []

        # Return best
        best = max(solutions, key=lambda x: x[2])
        all_scores = [s[2] for s in solutions]
        return best[0], best[1], all_scores

    def run_ultra_test(self, n_problems: int = 5):
        """Run ultra-max test with multiple strategies."""
        print("="*60)
        print("🔥 ULTRA-MAX METHODOLOGY TEST")
        print("="*60)
        print(f"Testing on {n_problems} problems")
        print("Strategies: Multi-iteration refinement + Best-of-N selection")

        problems = random.sample(PROBLEMS, min(n_problems, len(PROBLEMS)))

        # Test 1: Baseline
        print(f"\n{'='*60}")
        print("TEST 1: Baseline v5.2")
        print("="*60)
        baseline_scores = []
        for i, problem in enumerate(problems):
            print(f"  Problem {i+1}...", end=" ")
            solution = self.solve(problem, METHODOLOGY_V52)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                score = eval_result.get('total', 0)
                baseline_scores.append(score)
                print(f"{score}/50")
            time.sleep(0.5)
        baseline_avg = sum(baseline_scores) / len(baseline_scores)
        print(f"  Average: {baseline_avg:.1f}/50")

        # Test 2: 3-iteration refinement
        print(f"\n{'='*60}")
        print("TEST 2: v5.2 + 3 Targeted Refinement Iterations")
        print("="*60)
        iter3_scores = []
        iter3_progressions = []
        for i, problem in enumerate(problems):
            print(f"  Problem {i+1}...", end=" ")
            _, eval_result, progression = self.solve_with_iterations(problem, n_iterations=3)
            if eval_result:
                score = eval_result.get('total', 0)
                iter3_scores.append(score)
                iter3_progressions.append(progression)
                print(f"{score}/50 (progression: {' → '.join(str(p) for p in progression)})")
            time.sleep(0.5)
        iter3_avg = sum(iter3_scores) / len(iter3_scores)
        print(f"  Average: {iter3_avg:.1f}/50")

        # Test 3: Best-of-3
        print(f"\n{'='*60}")
        print("TEST 3: Best-of-3 Selection (each with 1 refinement)")
        print("="*60)
        best3_scores = []
        all_candidate_scores = []
        for i, problem in enumerate(problems):
            print(f"  Problem {i+1}...", end=" ")
            _, eval_result, candidates = self.best_of_n(problem, n=3)
            if eval_result:
                score = eval_result.get('total', 0)
                best3_scores.append(score)
                all_candidate_scores.append(candidates)
                print(f"{score}/50 (candidates: {candidates})")
            time.sleep(0.5)
        best3_avg = sum(best3_scores) / len(best3_scores)
        print(f"  Average: {best3_avg:.1f}/50")

        # Test 4: Best-of-3 + 2 more iterations
        print(f"\n{'='*60}")
        print("TEST 4: Best-of-3 + 2 Additional Refinement Iterations")
        print("="*60)
        combo_scores = []
        for i, problem in enumerate(problems):
            print(f"  Problem {i+1}...", end=" ")
            # Get best of 3
            best_solution, _, _ = self.best_of_n(problem, n=3)
            if best_solution:
                # Apply 2 more refinements
                for _ in range(2):
                    best_solution = self.refine(problem, best_solution)
                eval_result = self.evaluate(problem, best_solution)
                if eval_result:
                    score = eval_result.get('total', 0)
                    combo_scores.append(score)
                    print(f"{score}/50")
            time.sleep(0.5)
        combo_avg = sum(combo_scores) / len(combo_scores) if combo_scores else 0
        print(f"  Average: {combo_avg:.1f}/50")

        # Final Summary
        print("\n" + "="*60)
        print("🏆 FINAL RANKINGS")
        print("="*60)

        results = [
            ("Baseline v5.2", baseline_avg, baseline_scores),
            ("3-Iteration Refinement", iter3_avg, iter3_scores),
            ("Best-of-3", best3_avg, best3_scores),
            ("Best-of-3 + 2 Iterations", combo_avg, combo_scores),
        ]

        results.sort(key=lambda x: x[1], reverse=True)

        for i, (name, avg, scores) in enumerate(results):
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
            print(f"{medal} {name}: {avg:.1f}/50 (max: {max(scores)}/50)")

        best = results[0]
        print(f"\n🎯 BEST: {best[0]} at {best[1]:.1f}/50")
        print(f"   Peak score: {max(best[2])}/50")

        # Save results
        output = {
            "results": {name: {"avg": avg, "scores": scores} for name, avg, scores in results},
            "best": best[0],
            "best_avg": best[1],
            "best_max": max(best[2]),
            "timestamp": datetime.now().isoformat()
        }

        with open("/home/user/claude/Meta/ultra_max_results.json", "w") as f:
            json.dump(output, f, indent=2)

        return results


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ultra_max_methodology.py <API_KEY> [n_problems]")
        sys.exit(1)

    api_key = sys.argv[1]
    n_problems = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    test = UltraMaxMethodology(api_key)
    test.run_ultra_test(n_problems)


if __name__ == "__main__":
    main()
