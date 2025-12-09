#!/usr/bin/env python3
"""
TARGETED INTERVENTION EXPERIMENT

Finding: Verification dimension is always 8/10 (no variance)
Hypothesis: Enhanced verification instructions will push it to 9/10

Pre-registered:
- H1: Enhanced verification increases verification score (8 → 9)
- H2: This increases total score by ~1 point (42.4 → 43.4)

Design:
- Within-subjects: Same 10 problems, both conditions
- Control: v5.2 baseline
- Treatment: v5.2 + enhanced verification
- Primary outcome: Verification dimension score
- Secondary outcome: Total score
"""

import anthropic
import json
import statistics
from datetime import datetime

# Control: Standard v5.2
METHODOLOGY_CONTROL = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

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

# Treatment: Enhanced verification (targeting the 8→9 gap)
METHODOLOGY_TREATMENT = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-V**

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

STEP 5: VERIFY (ENHANCED)
1. Check ALL constraints
2. Does this answer the question?
3. What could make this wrong?
4. COMPOUND FAILURE TEST - all top 3 assumptions wrong simultaneously
5. INTERACTION STRESS TEST - how failures compound each other
6. MONITOR - indicators + thresholds for each assumption

**EXCEPTIONAL FAILURE MODE ANALYSIS (NEW):**
7. PRE-MORTEM: "It's 12 months later and this strategy failed catastrophically. Write 3 specific scenarios explaining exactly what went wrong."
8. HIDDEN RISKS: Identify 2 risks that are NOT obvious from the problem statement but could derail execution
9. CONFIDENCE DECOMPOSITION: State confidence separately for (a) diagnosis correctness, (b) solution effectiveness, (c) implementation feasibility
10. FALSIFICATION: "What specific evidence in the next 30 days would prove this approach is wrong?"

META-RULE: If stuck → wrong frame → return to Step 0
"""

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Critical hidden assumptions identified?
2. STRATEGIC DEPTH (1-10): 2nd/3rd order effects traced?
3. FRAME QUALITY (1-10): Right way to think about problem?
4. ACTIONABILITY (1-10): Specific and executable tomorrow?
5. VERIFICATION (1-10): Stress-tested? Failure modes identified? Pre-mortem done?

Scoring guide for VERIFICATION:
- 7: Good verification, checks basic constraints
- 8: Excellent stress-testing, compound failure considered
- 9: Exceptional failure mode analysis, pre-mortem, hidden risks, falsification criteria
- 10: Bulletproof verification that anticipates every reasonable failure mode

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


class TargetedExperiment:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def solve(self, problem: str, methodology: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3500,
            messages=[{"role": "user", "content": f"Apply this methodology:\n\n{methodology}\n\n---\n\nPROBLEM:\n{problem}"}]
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

    def run_experiment(self):
        """Within-subjects design: same problems, both conditions."""
        print("="*60)
        print("TARGETED INTERVENTION EXPERIMENT")
        print("="*60)
        print("\nPRE-REGISTERED HYPOTHESES:")
        print("  H1: Enhanced verification → verification score 8→9")
        print("  H2: Total score increases by ~1 point")
        print("\nDESIGN: Within-subjects, 10 problems, both conditions")
        print("="*60)

        control_results = []
        treatment_results = []

        for i, problem in enumerate(PROBLEMS):
            print(f"\nProblem {i+1}/10:")

            # Control condition
            print("  Control (v5.2)...", end=" ")
            solution_c = self.solve(problem, METHODOLOGY_CONTROL)
            eval_c = self.evaluate(problem, solution_c)
            if eval_c:
                control_results.append(eval_c)
                print(f"total={eval_c['total']}, verif={eval_c['verification']}")

            # Treatment condition
            print("  Treatment (v5.2-V)...", end=" ")
            solution_t = self.solve(problem, METHODOLOGY_TREATMENT)
            eval_t = self.evaluate(problem, solution_t)
            if eval_t:
                treatment_results.append(eval_t)
                print(f"total={eval_t['total']}, verif={eval_t['verification']}")

        # Analysis
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)

        # Verification scores
        control_verif = [r['verification'] for r in control_results]
        treatment_verif = [r['verification'] for r in treatment_results]

        print(f"\nVERIFICATION SCORES (Primary Outcome):")
        print(f"  Control:   mean={statistics.mean(control_verif):.2f}, scores={control_verif}")
        print(f"  Treatment: mean={statistics.mean(treatment_verif):.2f}, scores={treatment_verif}")

        verif_diff = statistics.mean(treatment_verif) - statistics.mean(control_verif)
        print(f"  Difference: {verif_diff:+.2f}")

        # Total scores
        control_total = [r['total'] for r in control_results]
        treatment_total = [r['total'] for r in treatment_results]

        print(f"\nTOTAL SCORES (Secondary Outcome):")
        print(f"  Control:   mean={statistics.mean(control_total):.1f}, scores={control_total}")
        print(f"  Treatment: mean={statistics.mean(treatment_total):.1f}, scores={treatment_total}")

        total_diff = statistics.mean(treatment_total) - statistics.mean(control_total)
        print(f"  Difference: {total_diff:+.1f}")

        # All dimensions
        print(f"\nDIMENSION BREAKDOWN:")
        for dim in ['assumption_surfacing', 'strategic_depth', 'frame_quality', 'actionability', 'verification']:
            c_mean = statistics.mean([r[dim] for r in control_results])
            t_mean = statistics.mean([r[dim] for r in treatment_results])
            diff = t_mean - c_mean
            print(f"  {dim}: control={c_mean:.1f}, treatment={t_mean:.1f}, diff={diff:+.1f}")

        # Hypothesis evaluation
        print(f"\n{'='*60}")
        print("HYPOTHESIS EVALUATION")
        print("="*60)

        h1_supported = verif_diff >= 0.5
        h2_supported = total_diff >= 0.5

        print(f"\nH1 (verification 8→9): {'SUPPORTED' if h1_supported else 'NOT SUPPORTED'}")
        print(f"  Effect: {verif_diff:+.2f} points")

        print(f"\nH2 (total +1 point): {'SUPPORTED' if h2_supported else 'NOT SUPPORTED'}")
        print(f"  Effect: {total_diff:+.1f} points")

        # Effect size
        if len(control_total) > 1 and len(treatment_total) > 1:
            pooled_std = ((statistics.stdev(control_total)**2 + statistics.stdev(treatment_total)**2) / 2) ** 0.5
            if pooled_std > 0:
                cohens_d = total_diff / pooled_std
                print(f"\nCohen's d: {cohens_d:.2f}")

        # Save results
        results = {
            "design": "within-subjects, targeted verification enhancement",
            "n_problems": len(PROBLEMS),
            "control": {
                "verification_mean": statistics.mean(control_verif),
                "verification_scores": control_verif,
                "total_mean": statistics.mean(control_total),
                "total_scores": control_total
            },
            "treatment": {
                "verification_mean": statistics.mean(treatment_verif),
                "verification_scores": treatment_verif,
                "total_mean": statistics.mean(treatment_total),
                "total_scores": treatment_total
            },
            "effects": {
                "verification_diff": verif_diff,
                "total_diff": total_diff,
                "h1_supported": h1_supported,
                "h2_supported": h2_supported
            },
            "timestamp": datetime.now().isoformat()
        }

        with open("/home/user/claude/Meta/targeted_experiment_results.json", "w") as f:
            json.dump(results, f, indent=2)

        return results


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python targeted_experiment.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    exp = TargetedExperiment(api_key)
    exp.run_experiment()


if __name__ == "__main__":
    main()
