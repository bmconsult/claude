#!/usr/bin/env python3
"""
Exponential Improvement Loop v3 - Continuation

Continues from v5.2 methodology to push past the ceiling.
Key changes:
- Starts from evolved v5.2 methodology
- More cycles (15+) to find true ceiling
- Better logging of what changes worked
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional

# Load best methodology from previous run
METHODOLOGY_V5_2 = """**STRATEGIC PROBLEM-SOLVING PROTOCOL v5.2**

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
1. WHO: Specific roles/people responsible for each major component
2. WHEN: Timeline with key milestones (weeks/months, not "soon")
3. WHAT: Success metrics and decision criteria for next steps
4. **HOW MUCH: Required resources with JUSTIFICATION ANCHOR - for each significant cost estimate, cite specific comparable data (market rates, benchmarks, similar projects) or calculation method. NO RANGES OVER 25% SPAN (if initial estimate is $500K, range cannot exceed $375K-$625K). For total resource requirements exceeding $100K or 3 months timeline, provide explicit resource allocation rationale comparing focused single-approach execution vs. hybrid approach execution.**
5. HOW: For each major component, specify the exact mechanism of execution
6. **SCRIPT: For interpersonal components (negotiations, meetings, conversations), provide exact words or specific phrases to use. For process components, name the specific tool/template/format and describe its key structural elements.**
7. **RESISTANCE MAP: Identify the 3 most likely sources of implementation resistance (people, processes, or politics) and specify exact countermeasures with numerical thresholds that trigger escalation (e.g., "if adoption rate falls below X% after Y weeks, execute strategy Z").**

STEP 5: VERIFY (mandatory)
1. Check solution against ALL stated constraints
2. Does this actually answer the original question?
3. What could make this answer wrong?
4. **COMPOUND FAILURE TEST: What if your top 3 assumptions are ALL wrong simultaneously? Test this specific scenario and specify what backup strategy you would execute.**
5. **INTERACTION STRESS TEST: For each pair of your top 3 assumptions, specify exactly how their simultaneous failure would amplify or compound each other's impact on your strategy, then adjust your plan to account for these specific interaction effects.**
6. MONITOR: For each top assumption, specify one measurable indicator with an exact threshold that triggers a pivot decision
7. CONTINGENCY: For timeline-dependent plans, specify fallback actions if milestones slip by more than 20%
8. State confidence level explicitly

META-RULE:
If problem is Hybrid (most are) → apply MULTIPLE tools
If stuck at any point → you're solving the wrong problem → return to Step 0
"""

# Expanded problem bank with harder problems
PROBLEMS = [
    # Strategic - Classic
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

    # NEW - Harder problems
    "You're a hospital administrator. A whistleblower has evidence your top surgeon (who brings in 40% of revenue) has been falsifying credentials. Firing means bankruptcy. Keeping means patient risk. The board meets tomorrow.",

    "Your tech company discovered a critical security vulnerability in a competitor's product that affects millions of users. Disclosing helps users but helps your competitive position suspiciously. Your ethics board is divided.",

    "You're CEO during a hostile takeover attempt. The acquirer is offering 40% premium, but you believe the company is worth 2x current price in 3 years. Employees are nervous. Institutional shareholders are wavering.",

    "A key supplier just went bankrupt. You have 2 weeks of inventory. Alternative suppliers require 6-week lead time. Stopping production loses your biggest customer forever. What do you do?",

    "Your successful product is causing unexpected harm in developing markets. Pulling it destroys those economies dependent on it. Continuing causes harm. Modifying takes 18 months. Activists are mobilizing.",
]

EVAL_RUBRIC = """Score this solution on 5 dimensions (1-10 each, 50 total):

1. ASSUMPTION SURFACING (1-10): Did they identify critical hidden assumptions? Did they question the obvious?
2. STRATEGIC DEPTH (1-10): Did they trace consequences, dynamics, multi-level thinking? Did they consider 2nd/3rd order effects?
3. FRAME QUALITY (1-10): Did they find the RIGHT way to think about the problem? Did they avoid obvious frames?
4. ACTIONABILITY (1-10): Is the recommendation specific and executable? Could someone actually DO this tomorrow?
5. VERIFICATION (1-10): Did they check reasoning, state uncertainty, identify what could be wrong? Did they stress-test?

Be rigorous. 8+ requires excellence. 9+ requires exceptional insight.

Return ONLY valid JSON:
{"assumption_surfacing": X, "strategic_depth": X, "frame_quality": X, "actionability": X, "verification": X, "total": X, "weakest": "dimension_name", "gap": "specific weakness"}
"""


class ExponentialLoopContinue:
    def __init__(self, api_key: str, start_version: float = 5.2, start_best: float = 44.3):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.methodology = METHODOLOGY_V5_2
        self.version = start_version
        self.best_score = start_best
        self.history = []
        self.improvements_tested = 0
        self.improvements_kept = 0
        self.breakthrough_log = []  # Track what changes led to big improvements

    def solve(self, problem: str, methodology: str) -> str:
        """Solve problem using given methodology."""
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,  # Increased for complex solutions
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

    def generate_improvement(self, weaknesses: List[Dict]) -> Optional[tuple]:
        """Generate a potential improvement based on observed weaknesses. Returns (methodology, change_description)."""
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
4. Focus on forcing BETTER BEHAVIOR, not just more words

After the methodology, on a new line starting with "CHANGE:", describe the specific change you made in one sentence.

Return the COMPLETE improved methodology followed by the change description."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text

        # Extract change description if present
        change_desc = "Unknown change"
        if "CHANGE:" in text:
            parts = text.split("CHANGE:")
            methodology = parts[0].strip()
            change_desc = parts[1].strip().split("\n")[0]
        else:
            methodology = text

        return methodology, change_desc

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
            print(f"🔥 NEW BEST: {self.best_score:.1f}/50")

        # Generate potential improvement
        print("\nGenerating improvement...")
        result = self.generate_improvement(weaknesses)

        if not result:
            print("Failed to generate improvement")
            return {"version": self.version, "score": current_avg, "improved": False}

        improved_methodology, change_desc = result
        print(f"Change: {change_desc[:80]}...")

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
            print(f"\n✅ IMPROVEMENT VALIDATED: +{delta:.1f} points")
            self.methodology = improved_methodology
            self.version += 0.1
            self.improvements_kept += 1
            adopted = True

            # Log breakthrough if significant
            if delta >= 1.5:
                self.breakthrough_log.append({
                    "version": self.version,
                    "delta": delta,
                    "change": change_desc,
                    "timestamp": datetime.now().isoformat()
                })
                print(f"🚀 BREAKTHROUGH: +{delta:.1f} points!")
        else:
            print(f"\n❌ IMPROVEMENT REJECTED: {delta:.1f} points (no gain)")
            adopted = False

        result = {
            "version": self.version,
            "current_score": current_avg,
            "improved_score": improved_avg,
            "delta": delta,
            "adopted": adopted,
            "change": change_desc,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(result)

        return result

    def run_until_ceiling(self, max_cycles: int = 15, convergence_threshold: int = 3):
        """Run cycles until we hit ceiling (no improvement for N consecutive cycles)."""
        print("="*60)
        print("EXPONENTIAL IMPROVEMENT LOOP v3 - CONTINUATION")
        print("="*60)
        print(f"Starting at v{self.version:.1f} (Best: {self.best_score:.1f}/50)")
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
                print("🏔️ CEILING REACHED")
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

        if self.breakthrough_log:
            print(f"\n🚀 BREAKTHROUGHS:")
            for b in self.breakthrough_log:
                print(f"  v{b['version']:.1f}: +{b['delta']:.1f} - {b['change'][:60]}...")

        # Save results
        output = {
            "final_version": self.version,
            "best_score": self.best_score,
            "final_methodology": self.methodology,
            "history": self.history,
            "improvements_tested": self.improvements_tested,
            "improvements_kept": self.improvements_kept,
            "breakthroughs": self.breakthrough_log
        }

        with open("/home/user/claude/Meta/exponential_loop_v3_results.json", "w") as f:
            json.dump(output, f, indent=2)

        return output


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python exponential_loop_v3_continue.py <API_KEY> [max_cycles]")
        sys.exit(1)

    api_key = sys.argv[1]
    max_cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 15

    loop = ExponentialLoopContinue(api_key, start_version=5.2, start_best=44.3)
    loop.run_until_ceiling(max_cycles=max_cycles, convergence_threshold=3)


if __name__ == "__main__":
    main()
