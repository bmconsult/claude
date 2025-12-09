#!/usr/bin/env python3
"""
TARGETED INTERVENTION: STRATEGIC DEPTH

Current state after v5.2-V:
- verification: 9.0/10 ✓ (fixed)
- assumption_surfacing: 8.9/10
- frame_quality: 8.8/10
- actionability: 8.2/10
- strategic_depth: 8.0/10 ← TARGET

Pre-registered Hypotheses:
- H1: Enhanced strategic depth → strategic_depth score 8→9
- H2: Total score increases by ~1 point (43.1 → 44.1)

Design: Within-subjects, 10 problems, control (v5.2-V) vs treatment (v5.2-VS)
"""

import anthropic
import json
import statistics
from datetime import datetime

# Control: v5.2-V (with enhanced verification)
METHODOLOGY_CONTROL = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-V**

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
4. COMPOUND FAILURE TEST
5. INTERACTION STRESS TEST
6. MONITOR - indicators + thresholds
7. PRE-MORTEM: 3 specific failure scenarios
8. HIDDEN RISKS: 2 non-obvious risks
9. CONFIDENCE DECOMPOSITION: diagnosis/solution/implementation
10. FALSIFICATION: specific evidence that would prove approach wrong

META-RULE: If stuck → wrong frame → return to Step 0
"""

# Treatment: v5.2-VS (V + enhanced Strategic depth)
METHODOLOGY_TREATMENT = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2-VS**

STEP 0: FRAME - Classify: Analytical/Systems/Adversarial/Wicked/Hybrid

STEP 1: ASSUMPTION AUDIT
- List ALL assumptions
- "What if wrong?" for each
- Identify top 3 that most change the answer

STEP 2: STRATEGIC DEPTH ANALYSIS (ENHANCED)

**2A. MULTI-ORDER CONSEQUENCES:**
For your proposed solution, trace consequences at each order:
- 1st order: What happens immediately?
- 2nd order: What do those consequences cause?
- 3rd order: What emerges from the 2nd order effects?
- Identify any REVERSALS (where 2nd/3rd order effects contradict 1st order)

**2B. MULTI-LEVEL ANALYSIS:**
Analyze impact at each level:
- Individual level: How does this affect key people's incentives and behaviors?
- Team level: How does this change team dynamics?
- Organization level: How does this shift org capabilities/culture?
- Market level: How do competitors/customers respond?
- Identify CROSS-LEVEL INTERACTIONS (where effects at one level cascade to others)

**2C. TEMPORAL DYNAMICS:**
- Short-term (30 days): What happens immediately?
- Medium-term (6 months): What emerges as system adapts?
- Long-term (2+ years): What equilibrium does this create?
- Identify DELAYED EFFECTS that won't be visible initially

STEP 3: LEVERAGE FINDER (if Systems/Wicked)
- Map ALL feedback loops (reinforcing and balancing)
- Find high-leverage intervention points

STEP 4: RESPONSE CHAIN (if Adversarial)
- Trace 3+ moves ahead
- Evaluate at END of chain

STEP 5: IMPLEMENTATION PLAN
1. WHO - Specific roles
2. WHEN - Timeline with milestones
3. WHAT - Success metrics
4. HOW MUCH - Resources + justification
5. HOW - Exact mechanism
6. SCRIPT - Exact words for interpersonal components
7. RESISTANCE MAP - 3 sources + countermeasures + thresholds

STEP 6: VERIFY (ENHANCED)
1. Check ALL constraints
2. Does this answer the question?
3. What could make this wrong?
4. COMPOUND FAILURE TEST
5. INTERACTION STRESS TEST
6. MONITOR - indicators + thresholds
7. PRE-MORTEM: 3 specific failure scenarios
8. HIDDEN RISKS: 2 non-obvious risks
9. CONFIDENCE DECOMPOSITION: diagnosis/solution/implementation
10. FALSIFICATION: specific evidence that would prove approach wrong

META-RULE: If stuck → wrong frame → return to Step 0
"""

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Critical hidden assumptions identified?

2. STRATEGIC DEPTH (1-10): 2nd/3rd order effects traced? Multi-level analysis? Temporal dynamics?
   - 7: Good strategic thinking
   - 8: Excellent multi-order analysis
   - 9: Exceptional - traces consequences across orders, levels, AND time horizons with cross-level interactions
   - 10: Grandmaster-level strategic thinking

3. FRAME QUALITY (1-10): Right way to think about problem?

4. ACTIONABILITY (1-10): Specific and executable tomorrow?

5. VERIFICATION (1-10): Stress-tested? Failure modes identified? Pre-mortem done?

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


class StrategicDepthExperiment:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def solve(self, problem: str, methodology: str) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
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
        print("TARGETED INTERVENTION: STRATEGIC DEPTH")
        print("="*60)
        print("\nPRE-REGISTERED HYPOTHESES:")
        print("  H1: Enhanced strategic depth → score 8→9")
        print("  H2: Total score increases by ~1 point")
        print("\nDESIGN: Within-subjects, 10 problems")
        print("  Control: v5.2-V (43.1/50 baseline)")
        print("  Treatment: v5.2-VS (+ enhanced strategic depth)")
        print("="*60)

        control_results = []
        treatment_results = []

        for i, problem in enumerate(PROBLEMS):
            print(f"\nProblem {i+1}/10:")

            # Control
            print("  Control (v5.2-V)...", end=" ")
            solution_c = self.solve(problem, METHODOLOGY_CONTROL)
            eval_c = self.evaluate(problem, solution_c)
            if eval_c:
                control_results.append(eval_c)
                print(f"total={eval_c['total']}, depth={eval_c['strategic_depth']}")

            # Treatment
            print("  Treatment (v5.2-VS)...", end=" ")
            solution_t = self.solve(problem, METHODOLOGY_TREATMENT)
            eval_t = self.evaluate(problem, solution_t)
            if eval_t:
                treatment_results.append(eval_t)
                print(f"total={eval_t['total']}, depth={eval_t['strategic_depth']}")

        # Analysis
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)

        # Strategic depth scores
        control_depth = [r['strategic_depth'] for r in control_results]
        treatment_depth = [r['strategic_depth'] for r in treatment_results]

        print(f"\nSTRATEGIC DEPTH SCORES (Primary Outcome):")
        print(f"  Control:   mean={statistics.mean(control_depth):.2f}, scores={control_depth}")
        print(f"  Treatment: mean={statistics.mean(treatment_depth):.2f}, scores={treatment_depth}")

        depth_diff = statistics.mean(treatment_depth) - statistics.mean(control_depth)
        print(f"  Difference: {depth_diff:+.2f}")

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
            marker = " ← TARGET" if dim == 'strategic_depth' else ""
            print(f"  {dim}: control={c_mean:.1f}, treatment={t_mean:.1f}, diff={diff:+.1f}{marker}")

        # Hypothesis evaluation
        print(f"\n{'='*60}")
        print("HYPOTHESIS EVALUATION")
        print("="*60)

        h1_supported = depth_diff >= 0.5
        h2_supported = total_diff >= 0.5

        print(f"\nH1 (strategic_depth 8→9): {'SUPPORTED' if h1_supported else 'NOT SUPPORTED'}")
        print(f"  Effect: {depth_diff:+.2f} points")

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
            "design": "within-subjects, targeted strategic depth enhancement",
            "n_problems": len(PROBLEMS),
            "control": {
                "methodology": "v5.2-V",
                "strategic_depth_mean": statistics.mean(control_depth),
                "strategic_depth_scores": control_depth,
                "total_mean": statistics.mean(control_total),
                "total_scores": control_total
            },
            "treatment": {
                "methodology": "v5.2-VS",
                "strategic_depth_mean": statistics.mean(treatment_depth),
                "strategic_depth_scores": treatment_depth,
                "total_mean": statistics.mean(treatment_total),
                "total_scores": treatment_total
            },
            "effects": {
                "strategic_depth_diff": depth_diff,
                "total_diff": total_diff,
                "h1_supported": h1_supported,
                "h2_supported": h2_supported
            },
            "timestamp": datetime.now().isoformat()
        }

        with open("/home/user/claude/Meta/strategic_depth_experiment_results.json", "w") as f:
            json.dump(results, f, indent=2)

        return results


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python strategic_depth_experiment.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    exp = StrategicDepthExperiment(api_key)
    exp.run_experiment()


if __name__ == "__main__":
    main()
