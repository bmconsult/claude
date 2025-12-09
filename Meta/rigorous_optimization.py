#!/usr/bin/env python3
"""
RIGOROUS METHODOLOGY OPTIMIZATION

Applying Virtuoso Experiment Design:
1. First diagnose the measurement system
2. Then design properly powered experiments
3. Pre-register hypotheses
4. Run with appropriate controls
"""

import anthropic
import json
import statistics
from datetime import datetime

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Did they identify critical hidden assumptions?
2. STRATEGIC DEPTH (1-10): Did they trace 2nd/3rd order consequences?
3. FRAME QUALITY (1-10): Did they find the RIGHT way to think about the problem?
4. ACTIONABILITY (1-10): Is this specific and executable tomorrow?
5. VERIFICATION (1-10): Did they stress-test and identify failure modes?

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X}
"""

# Fixed problem and solution for calibration
CALIBRATION_PROBLEM = """You're CEO of a 200-person SaaS company. Your biggest competitor just got acquired by Microsoft. Your top 3 engineers are being recruited heavily. Revenue growth has slowed from 40% to 15% YoY. What's your strategy?"""

CALIBRATION_SOLUTION = """**Problem Classification**: Hybrid (Adversarial + Systems + Wicked)

**ASSUMPTION AUDIT**
Top 3 assumptions that most change the answer:
1. Microsoft acquisition means aggressive competition (what if they neglect the product?)
2. Engineers leaving would hurt us (what if we're over-reliant on specific people?)
3. Growth slowdown is a problem to fix (what if it's natural market maturation?)

**STRATEGY: Focused Differentiation + Talent Fortress**

Rather than compete head-on with Microsoft, we pivot to own a specific niche they'll ignore.

**LEVERAGE POINTS**
- Microsoft's acquisition creates 6-12 months of integration chaos - our window
- Our engineers know things Microsoft doesn't - this is leverage in retention
- Slowdown might mean we've saturated easy customers - time to go upmarket

**RESPONSE CHAIN**
1. We announce vertical focus → Microsoft ignores (too small)
2. We win 3 flagship enterprise deals → Microsoft notices but too late
3. We become "the X for Y industry" → Microsoft can't compete without acquisition

**IMPLEMENTATION**
WHO:
- CEO (me): Lead customer conversations, set vision
- VP Eng: Retention program owner
- VP Sales: Enterprise pivot lead

WHEN:
- Week 1-2: Engineer retention conversations (equity refresh, project ownership)
- Week 3-4: Identify target vertical (analyze where we over-index)
- Month 2-3: Land 2 flagship enterprise logos
- Month 4-6: Product roadmap for vertical-specific features

WHAT (Success Metrics):
- Engineer retention: 0 departures in 90 days
- Enterprise pipeline: 5 qualified opps >$100K ACV by month 3
- Win rate: 40%+ on enterprise deals

HOW MUCH:
- Retention equity pool: $2M (10% of typical Series B, justified by replacement cost of 3 senior engineers at $500K each)
- Enterprise sales investment: $300K (1 enterprise AE + SC)

SCRIPT for engineer retention:
"I want to be direct. I know you're being recruited. I can't match Microsoft's cash. But I can offer you something they can't: ownership of [specific project], equity upside if we win, and the chance to build something that matters. What would it take for you to commit to 18 months?"

RESISTANCE MAP:
1. Board wants to "stay the course" → Counter: Show burn rate vs runway math, request 90-day pilot
2. Engineers skeptical of equity → Counter: Bring term sheet showing 3x liquidation preference, they're ahead of VCs
3. Sales team comfortable with SMB → Counter: Tie 30% of comp to enterprise pipeline

**VERIFICATION**

COMPOUND FAILURE: If Microsoft executes well AND engineers leave AND enterprise fails?
→ Backup: Acqui-hire to vertical competitor (we'd still have customer relationships and domain expertise)

INTERACTION STRESS: Engineers leaving + enterprise focus = can't ship features
→ Mitigation: Retention must succeed first. Pause enterprise push if retention fails.

MONITOR:
- Engineer sentiment: Weekly 1:1s, score 1-5. If <3 avg, escalate.
- Pipeline: Weekly review. If <$500K qualified by week 6, pivot approach.
- Microsoft moves: Track their pricing/features. If aggressive move, accelerate timeline.

CONFIDENCE: 65%. Highest risk is engineer retention - this must work or strategy collapses."""


class RigorousOptimization:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def evaluate(self, problem: str, solution: str) -> dict:
        """Single evaluation."""
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

    def calibration_test(self, n_evals: int = 10):
        """
        DIAGNOSTIC: Evaluate the SAME solution N times.
        This reveals evaluation variance independent of solution quality.
        """
        print("="*60)
        print("PHASE 1: EVALUATION CALIBRATION")
        print("="*60)
        print(f"Evaluating IDENTICAL solution {n_evals} times")
        print("This measures evaluator variance, not methodology quality\n")

        scores = []
        dimension_scores = {
            'assumption_surfacing': [],
            'strategic_depth': [],
            'frame_quality': [],
            'actionability': [],
            'verification': []
        }

        for i in range(n_evals):
            print(f"  Evaluation {i+1}/{n_evals}...", end=" ")
            result = self.evaluate(CALIBRATION_PROBLEM, CALIBRATION_SOLUTION)
            if result:
                total = result.get('total', 0)
                scores.append(total)
                for dim in dimension_scores:
                    if dim in result:
                        dimension_scores[dim].append(result[dim])
                print(f"{total}/50")

        # Statistics
        print(f"\n{'='*60}")
        print("CALIBRATION RESULTS")
        print("="*60)

        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores) if len(scores) > 1 else 0
        min_s, max_s = min(scores), max(scores)
        range_s = max_s - min_s

        print(f"\nTOTAL SCORE:")
        print(f"  Mean: {mean:.1f}/50")
        print(f"  StdDev: {stdev:.2f}")
        print(f"  Range: {min_s}-{max_s} ({range_s} points)")
        print(f"  All scores: {scores}")

        print(f"\nDIMENSION VARIANCE:")
        for dim, vals in dimension_scores.items():
            if len(vals) > 1:
                d_mean = statistics.mean(vals)
                d_std = statistics.stdev(vals)
                d_range = max(vals) - min(vals)
                print(f"  {dim}: mean={d_mean:.1f}, std={d_std:.2f}, range={d_range}")

        # Implications
        print(f"\n{'='*60}")
        print("IMPLICATIONS FOR EXPERIMENT DESIGN")
        print("="*60)

        # Calculate required N for detecting various effect sizes
        if stdev > 0:
            for effect in [2, 3, 5]:
                # Cohen's d
                d = effect / stdev
                # Approximate N for 80% power, alpha=0.05, two-tailed
                n_required = int((2 * (1.96 + 0.84)**2) / (d**2)) + 1
                print(f"  To detect {effect}-point difference: need n≈{n_required} per condition")

        print(f"\n  Evaluation variance: {stdev:.2f} points")
        if stdev > 3:
            print("  ⚠️  HIGH VARIANCE - improvements <3 points are likely noise")
        elif stdev > 1.5:
            print("  ⚠️  MODERATE VARIANCE - need n≥20 for reliable detection")
        else:
            print("  ✓ LOW VARIANCE - can detect small improvements")

        return {
            "mean": mean,
            "stdev": stdev,
            "range": range_s,
            "scores": scores,
            "dimension_scores": dimension_scores
        }


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python rigorous_optimization.py <API_KEY>")
        sys.exit(1)

    api_key = sys.argv[1]
    opt = RigorousOptimization(api_key)

    # Phase 1: Calibration
    results = opt.calibration_test(n_evals=10)

    # Save results
    with open("/home/user/claude/Meta/calibration_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to calibration_results.json")


if __name__ == "__main__":
    main()
