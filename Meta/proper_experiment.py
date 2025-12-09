#!/usr/bin/env python3
"""
PROPERLY DESIGNED EXPERIMENT

Pre-registered Hypotheses:
H1: Best-of-3 selection produces higher mean scores than single generation
H2: The improvement equals approximately (max - mean) of 3 samples

Design:
- Fixed methodology (v5.2)
- 10 problems (increased for power)
- For each problem: generate 3 solutions, evaluate all 3
- Compare: single (first) vs best-of-3

This isolates the SELECTION effect from methodology effects.
"""

import anthropic
import json
import statistics
import random
from datetime import datetime

METHODOLOGY_V52 = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

STEP 0: FRAME - Classify: Analytical/Systems/Adversarial/Wicked/Hybrid

STEP 1: ASSUMPTION AUDIT
- List ALL assumptions
- "What if wrong?" for each
- Identify top 3 that most change the answer

STEP 2: LEVERAGE FINDER (if Systems/Wicked)
- Map feedback loops
- Find high-leverage intervention points

STEP 3: RESPONSE CHAIN (if Adversarial)
- Trace 3+ moves ahead
- Evaluate at END of chain

STEP 4: IMPLEMENTATION PLAN
1. WHO - Specific roles
2. WHEN - Timeline with milestones
3. WHAT - Success metrics
4. HOW MUCH - Resources + justification
5. HOW - Exact mechanism
6. SCRIPT - Exact words for interpersonal components
7. RESISTANCE MAP - 3 sources + countermeasures + thresholds

STEP 5: VERIFY
1. Check ALL constraints
2. Does this answer the question?
3. What could make this wrong?
4. COMPOUND FAILURE TEST - all top 3 assumptions wrong
5. INTERACTION STRESS TEST - how failures compound
6. MONITOR - indicators + thresholds
7. CONTINGENCY for slippage
8. State confidence level

META-RULE: If stuck → wrong frame → return to Step 0
"""

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Critical hidden assumptions identified?
2. STRATEGIC DEPTH (1-10): 2nd/3rd order effects traced?
3. FRAME QUALITY (1-10): Right way to think about problem?
4. ACTIONABILITY (1-10): Specific and executable tomorrow?
5. VERIFICATION (1-10): Stress-tested? Failure modes identified?

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X}
"""

PROBLEMS = [
    "You're CEO of a 200-person SaaS company. Your biggest competitor just got acquired by Microsoft. Your top 3 engineers are being recruited heavily. Revenue growth has slowed from 40% to 15% YoY. What's your strategy?",

    "You're Head of HR. An anonymous report alleges your highest-performing sales director is creating a hostile environment. Sales are up 50% under their leadership. The alleged victims are afraid to come forward. What do you do?",

    "Your engineering team's velocity has dropped 40% over 6 months. Exit interviews cite 'too many meetings' and 'unclear priorities.' Adding more engineers hasn't helped. What's wrong and how do you fix it?",

    "A former employee is starting a competing company and recruiting your team. They have insider knowledge of your roadmap. Three key people have already left. How do you respond?",

    "You're founder of a 5-year-old startup. You've raised $20M, have 50 employees, $5M ARR growing 30%. A competitor just raised $100M. Your lead investor suggests raise big or consider acquisition. What do you do?",

    "Your hospital's top surgeon (40% of revenue) has been falsifying credentials. Firing means bankruptcy. Keeping means patient risk. Board meets tomorrow.",

    "You run a restaurant chain (15 locations). A delivery app demands 30% commission or delisting. 40% of orders come through them. What do you do?",

    "Your AI startup built a lie detector (85% accuracy). Law enforcement wants to buy. Civil liberties groups protesting. Investors split. What's your decision?",

    "A key supplier went bankrupt. 2 weeks of inventory. Alternative suppliers need 6-week lead time. Stopping production loses biggest customer forever. What do you do?",

    "You're negotiating a major partnership. Other side knows you need this more than they do. Limited alternatives. How do you get a fair deal?",
]


class ProperExperiment:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def solve(self, problem: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": f"Apply this methodology:\n\n{METHODOLOGY_V52}\n\n---\n\nPROBLEM:\n{problem}"}]
        )
        return response.content[0].text

    def evaluate(self, problem: str, solution: str) -> dict:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": f"{EVAL_RUBRIC}\n\nPROBLEM:\n{problem}\n\nSOLUTION:\n{solution}"}]
        )
        try:
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            return json.loads(text[json_start:json_end])
        except:
            return None

    def run_experiment(self, n_problems: int = 10, n_solutions: int = 3):
        """
        For each problem:
        1. Generate n_solutions solutions
        2. Evaluate each
        3. Record: first score, all scores, best score
        """
        print("="*60)
        print("PROPERLY DESIGNED EXPERIMENT")
        print("="*60)
        print(f"\nPRE-REGISTERED HYPOTHESES:")
        print("  H1: Best-of-3 > Single generation")
        print("  H2: Improvement ≈ (max - mean) of 3 samples")
        print(f"\nDESIGN: {n_problems} problems × {n_solutions} solutions each")
        print("="*60)

        problems = PROBLEMS[:n_problems]

        all_first_scores = []
        all_best_scores = []
        all_mean_scores = []
        selection_advantages = []

        for i, problem in enumerate(problems):
            print(f"\nProblem {i+1}/{n_problems}:")

            scores = []
            for j in range(n_solutions):
                print(f"  Solution {j+1}/{n_solutions}...", end=" ")
                solution = self.solve(problem)
                result = self.evaluate(problem, solution)
                if result:
                    score = result.get('total', 0)
                    scores.append(score)
                    print(f"{score}/50")
                else:
                    print("eval failed")

            if len(scores) == n_solutions:
                first = scores[0]
                best = max(scores)
                mean = statistics.mean(scores)
                advantage = best - mean

                all_first_scores.append(first)
                all_best_scores.append(best)
                all_mean_scores.append(mean)
                selection_advantages.append(advantage)

                print(f"  → First: {first}, Best: {best}, Mean: {mean:.1f}, Advantage: {advantage:.1f}")

        # Results
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)

        mean_first = statistics.mean(all_first_scores)
        mean_best = statistics.mean(all_best_scores)
        mean_mean = statistics.mean(all_mean_scores)
        mean_advantage = statistics.mean(selection_advantages)

        std_first = statistics.stdev(all_first_scores) if len(all_first_scores) > 1 else 0
        std_best = statistics.stdev(all_best_scores) if len(all_best_scores) > 1 else 0

        print(f"\nSINGLE GENERATION (first of 3):")
        print(f"  Mean: {mean_first:.1f}/50")
        print(f"  StdDev: {std_first:.2f}")
        print(f"  Scores: {all_first_scores}")

        print(f"\nBEST-OF-3 SELECTION:")
        print(f"  Mean: {mean_best:.1f}/50")
        print(f"  StdDev: {std_best:.2f}")
        print(f"  Scores: {all_best_scores}")

        improvement = mean_best - mean_first
        print(f"\nSELECTION EFFECT:")
        print(f"  Best-of-3 vs Single: +{improvement:.1f} points")
        print(f"  Mean selection advantage: +{mean_advantage:.1f} points")

        # Effect size
        pooled_std = ((std_first**2 + std_best**2) / 2) ** 0.5 if std_first > 0 else 1
        cohens_d = improvement / pooled_std if pooled_std > 0 else 0
        print(f"  Cohen's d: {cohens_d:.2f}")

        # Hypothesis testing
        print(f"\n{'='*60}")
        print("HYPOTHESIS EVALUATION")
        print("="*60)

        h1_result = "SUPPORTED" if improvement > 1 else "NOT SUPPORTED"
        print(f"\nH1 (Best-of-3 > Single): {h1_result}")
        print(f"  Improvement: {improvement:.1f} points")

        theoretical_advantage = mean_advantage
        print(f"\nH2 (Improvement ≈ max-mean):")
        print(f"  Theoretical: {theoretical_advantage:.1f}")
        print(f"  Observed: {improvement:.1f}")

        # Save results
        results = {
            "design": {
                "n_problems": n_problems,
                "n_solutions": n_solutions,
                "methodology": "v5.2"
            },
            "results": {
                "single_generation": {
                    "mean": mean_first,
                    "stdev": std_first,
                    "scores": all_first_scores
                },
                "best_of_3": {
                    "mean": mean_best,
                    "stdev": std_best,
                    "scores": all_best_scores
                },
                "selection_effect": {
                    "improvement": improvement,
                    "cohens_d": cohens_d,
                    "mean_advantage": mean_advantage
                }
            },
            "hypotheses": {
                "H1_supported": improvement > 1,
                "H1_improvement": improvement
            },
            "timestamp": datetime.now().isoformat()
        }

        with open("/home/user/claude/Meta/proper_experiment_results.json", "w") as f:
            json.dump(results, f, indent=2)

        return results


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python proper_experiment.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    exp = ProperExperiment(api_key)
    exp.run_experiment(n_problems=10, n_solutions=3)


if __name__ == "__main__":
    main()
