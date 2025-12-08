#!/usr/bin/env python3
"""
Exponential Improvement Loop v2

KEY FIX: Test improvements BEFORE integrating.
Only keep changes that improve scores.

The loop:
1. Generate problems
2. Solve with current methodology
3. Evaluate externally
4. Extract potential improvement
5. TEST improvement on new problems
6. If improved → integrate. If not → discard.
7. Loop until ceiling.
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

# Starting methodology (v4.0 validated at 42.3/50)
METHODOLOGY_V4 = """
STRATEGIC PROBLEM-SOLVING PROTOCOL v4.0

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

STEP 4: VERIFY (mandatory)
1. Check solution against ALL stated constraints
2. Does this actually answer the original question?
3. What could make this answer wrong?
4. State confidence level explicitly

META-RULE:
If problem is Hybrid (most are) → apply MULTIPLE tools
If stuck at any point → you're solving the wrong problem → return to Step 0
"""

# Problem bank for testing
PROBLEMS = [
    # Strategic
    "You're CEO of a 200-person SaaS company. Your biggest competitor just got acquired by Microsoft. Your top 3 engineers are being recruited heavily. Revenue growth has slowed from 40% to 15% YoY. What's your strategy?",

    "You run a successful restaurant chain (15 locations). A new food delivery app is demanding 30% commission or they'll delist you. 40% of your orders come through them. What do you do?",

    "You're VP of Product at a fintech startup. Your main product has PMF but a larger competitor just launched an identical feature with better UX. Your engineering team is burned out. Board meeting in 2 weeks. What's your plan?",

    # Ethical/Wicked
    "You're Head of HR. An anonymous report alleges your highest-performing sales director is creating a hostile environment. Sales are up 50% under their leadership. The alleged victims are afraid to come forward. What do you do?",

    "Your AI startup has built a tool that can detect lies with 85% accuracy. Law enforcement wants to buy it. Civil liberties groups are protesting. Your investors are split. What's your decision?",

    # Systems
    "Your engineering team's velocity has dropped 40% over 6 months. Exit interviews cite 'too many meetings' and 'unclear priorities.' Adding more engineers hasn't helped. What's wrong and how do you fix it?",

    "Your city's traffic is getting worse despite adding lanes. Public transit ridership is down. Remote work has plateaued. How do you actually solve this?",

    # Adversarial
    "A former employee is starting a competing company and recruiting your team. They have insider knowledge of your roadmap. Three key people have already left. How do you respond?",

    "You're negotiating a major partnership. The other side knows you need this deal more than they do. Your alternative options are limited. How do you get a fair deal?",

    # Hybrid/Complex
    "You're founder of a 5-year-old startup. You've raised $20M, have 50 employees, $5M ARR growing 30%. A competitor just raised $100M. Your lead investor suggests you either raise a big round now or consider acquisition. What do you do?",
]

EVAL_RUBRIC = """
Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Did they identify critical hidden assumptions?
2. STRATEGIC DEPTH (1-10): Did they trace consequences, dynamics, multi-level thinking?
3. FRAME QUALITY (1-10): Did they find the right way to think about the problem?
4. ACTIONABILITY (1-10): Is the recommendation specific and executable?
5. VERIFICATION (1-10): Did they check reasoning, state uncertainty, identify what could be wrong?

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X, "weakest": "dimension_name", "gap": "specific weakness"}
"""


class ExponentialLoop:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.methodology = METHODOLOGY_V4
        self.version = 4.0
        self.best_score = 0
        self.history = []
        self.improvements_tested = 0
        self.improvements_kept = 0

    def solve(self, problem: str, methodology: str) -> str:
        """Solve problem using given methodology."""
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            messages=[{"role": "user", "content": f"Apply this methodology:\n\n{methodology}\n\n---\n\nPROBLEM:\n{problem}"}]
        )
        return response.content[0].text

    def evaluate(self, problem: str, solution: str) -> Optional[Dict]:
        """Blind evaluation of solution."""
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

    def test_methodology(self, methodology: str, n_problems: int = 3) -> float:
        """Test a methodology on n problems, return average score."""
        problems = random.sample(PROBLEMS, min(n_problems, len(PROBLEMS)))
        scores = []

        for problem in problems:
            solution = self.solve(problem, methodology)
            eval_result = self.evaluate(problem, solution)
            if eval_result and 'total' in eval_result:
                scores.append(eval_result['total'])
            time.sleep(0.5)

        return sum(scores) / len(scores) if scores else 0

    def generate_improvement(self, weaknesses: List[Dict]) -> Optional[str]:
        """Generate a potential improvement based on observed weaknesses."""
        weakness_summary = "\n".join([
            f"- {w.get('weakest', 'unknown')}: {w.get('gap', 'unknown')}"
            for w in weaknesses if w
        ])

        prompt = f"""Current methodology:
{self.methodology}

Observed weaknesses from evaluation:
{weakness_summary}

Generate ONE specific improvement to the methodology that addresses the most common weakness.

Rules:
1. The improvement must be MINIMAL - change as little as possible
2. It must be CONCRETE - specific words to add/change
3. It must be TESTABLE - we can measure if it helps

Return the COMPLETE improved methodology (not just the change)."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def run_cycle(self, n_test: int = 3) -> Dict:
        """Run one improvement cycle with validation."""
        print(f"\n{'='*60}")
        print(f"CYCLE - v{self.version:.1f} (Best: {self.best_score:.1f}/50)")
        print(f"{'='*60}")

        # Test current methodology
        print(f"\nTesting current methodology on {n_test} problems...")
        weaknesses = []
        current_scores = []

        problems = random.sample(PROBLEMS, min(n_test, len(PROBLEMS)))
        for i, problem in enumerate(problems):
            print(f"  Problem {i+1}...", end=" ")
            solution = self.solve(problem, self.methodology)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                score = eval_result.get('total', 0)
                current_scores.append(score)
                weaknesses.append(eval_result)
                print(f"{score}/50")
            time.sleep(0.5)

        current_avg = sum(current_scores) / len(current_scores) if current_scores else 0
        print(f"\nCurrent average: {current_avg:.1f}/50")

        # Update best if improved
        if current_avg > self.best_score:
            self.best_score = current_avg
            print(f"NEW BEST: {self.best_score:.1f}/50")

        # Generate potential improvement
        print("\nGenerating improvement...")
        improved_methodology = self.generate_improvement(weaknesses)

        if not improved_methodology:
            print("Failed to generate improvement")
            return {"version": self.version, "score": current_avg, "improved": False}

        # TEST the improvement before adopting
        print(f"\nTesting improved methodology...")
        self.improvements_tested += 1

        improved_scores = []
        test_problems = random.sample(PROBLEMS, min(n_test, len(PROBLEMS)))
        for i, problem in enumerate(test_problems):
            print(f"  Problem {i+1}...", end=" ")
            solution = self.solve(problem, improved_methodology)
            eval_result = self.evaluate(problem, solution)
            if eval_result:
                score = eval_result.get('total', 0)
                improved_scores.append(score)
                print(f"{score}/50")
            time.sleep(0.5)

        improved_avg = sum(improved_scores) / len(improved_scores) if improved_scores else 0
        print(f"\nImproved average: {improved_avg:.1f}/50")

        # Only adopt if actually better
        delta = improved_avg - current_avg
        if delta > 0:
            print(f"\n✓ IMPROVEMENT VALIDATED: +{delta:.1f} points")
            self.methodology = improved_methodology
            self.version += 0.1
            self.improvements_kept += 1
            adopted = True
        else:
            print(f"\n✗ IMPROVEMENT REJECTED: {delta:.1f} points (no gain)")
            adopted = False

        result = {
            "version": self.version,
            "current_score": current_avg,
            "improved_score": improved_avg,
            "delta": delta,
            "adopted": adopted,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(result)

        return result

    def run_until_ceiling(self, max_cycles: int = 20, convergence_threshold: int = 3):
        """Run cycles until we hit ceiling (no improvement for N consecutive cycles)."""
        print("="*60)
        print("EXPONENTIAL IMPROVEMENT LOOP v2")
        print("="*60)
        print(f"Starting at v{self.version}")
        print(f"Convergence: {convergence_threshold} consecutive non-improvements")

        no_improvement_streak = 0

        for cycle in range(max_cycles):
            result = self.run_cycle()

            if result.get('adopted'):
                no_improvement_streak = 0
            else:
                no_improvement_streak += 1

            print(f"\nStreak without improvement: {no_improvement_streak}/{convergence_threshold}")

            if no_improvement_streak >= convergence_threshold:
                print(f"\n{'='*60}")
                print("CEILING REACHED")
                print(f"{'='*60}")
                break

        # Summary
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        print(f"Final version: v{self.version:.1f}")
        print(f"Best score achieved: {self.best_score:.1f}/50")
        print(f"Improvements tested: {self.improvements_tested}")
        print(f"Improvements kept: {self.improvements_kept}")
        print(f"Success rate: {self.improvements_kept/max(1,self.improvements_tested)*100:.0f}%")

        if self.history:
            scores = [h['current_score'] for h in self.history]
            print(f"Score progression: {' → '.join(f'{s:.1f}' for s in scores)}")

        # Save results
        output = {
            "final_version": self.version,
            "best_score": self.best_score,
            "final_methodology": self.methodology,
            "history": self.history,
            "improvements_tested": self.improvements_tested,
            "improvements_kept": self.improvements_kept
        }

        with open("/home/user/claude/Meta/exponential_loop_results.json", "w") as f:
            json.dump(output, f, indent=2)

        return output


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python exponential_loop_v2.py <API_KEY> [max_cycles]")
        sys.exit(1)

    api_key = sys.argv[1]
    max_cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    loop = ExponentialLoop(api_key)
    loop.run_until_ceiling(max_cycles=max_cycles, convergence_threshold=3)


if __name__ == "__main__":
    main()
