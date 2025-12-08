#!/usr/bin/env python3
"""
Automated Continuous Improvement Loop

This system:
1. Generates problems
2. Solves with current methodology
3. Evaluates externally (blind)
4. Extracts improvements
5. Integrates improvements
6. Loops forever (or until convergence)

The exponential comes from automation - no human bottleneck.
"""

import anthropic
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Tuple

# Problem templates for generation
PROBLEM_TEMPLATES = {
    "strategic": [
        "You're the {role} of a {size} {industry} company. {situation}. {constraint}. What's your strategy?",
        "You face a decision: {option_a} or {option_b}. {context}. {stakes}. What do you do?",
        "A competitor has {threat}. You have {resource}. {timeline}. How do you respond?",
    ],
    "ethical": [
        "You've discovered {discovery}. {stakeholders}. {tradeoff}. What's the right path?",
        "Your team has built {capability}. {benefit} but also {risk}. {pressure}. What do you recommend?",
    ],
    "interpersonal": [
        "Two key people {conflict}. {stakes}. {constraint}. How do you resolve this?",
        "{relationship} has {problem}. {attempts}. {what_matters}. What's your approach?",
    ],
    "systems": [
        "{system} is showing {symptoms}. {obvious_fix} but {hidden_dynamic}. What do you actually do?",
        "You want to change {behavior}. {current_state}. {resistance}. Where's the leverage?",
    ]
}

# Variable pools for problem generation
VARIABLES = {
    "role": ["CEO", "VP of Engineering", "Head of Product", "Founder", "CTO", "COO"],
    "size": ["50-person startup", "500-person scale-up", "5000-person enterprise", "10-person early-stage"],
    "industry": ["SaaS", "healthcare", "fintech", "e-commerce", "AI/ML", "enterprise software"],
    "situation": [
        "Your main product is commoditizing",
        "A key acquisition target just became available",
        "Your best team is threatening to leave",
        "Revenue is flat but costs are rising",
        "A major customer wants exclusivity"
    ],
    "constraint": [
        "You have 6 months of runway",
        "Your board is split 50/50",
        "Your biggest customer represents 40% of revenue",
        "You can't raise another round in this market"
    ],
    # Add more variable pools...
}

CURRENT_METHODOLOGY = """
STRATEGIC PROTOCOL (v4.0):

STEP 0: FRAME
What type of problem?
- Analytical: Clear answer exists
- Systems: Feedback loops, dynamics
- Adversarial: Other agents respond
- Wicked: Stakeholders, values, no clean answer
- Hybrid: Multiple types (most common)

STEP 1: ASSUMPTION AUDIT (mandatory)
List EVERY embedded assumption
For EACH ask "What if wrong?"
Identify top 3 that most change answer

STEP 2: LEVERAGE FINDER (for Systems/Wicked)
Map ALL feedback loops
Find intervention points
Prioritize high-leverage moves

STEP 3: RESPONSE CHAIN (for Adversarial)
For each option, trace 3+ response moves
Evaluate at END of chain
Find robust strategies

STEP 4: VERIFY (mandatory)
Check ALL constraints
Does solution answer actual question?
What could make this wrong?
State confidence explicitly

META-RULE:
If problem is Hybrid → apply MULTIPLE tools
If stuck → wrong frame → return to Step 0
"""

EVALUATION_RUBRIC = """
Score this solution on 5 dimensions (1-10):

1. ASSUMPTION SURFACING: Did they identify critical hidden assumptions?
2. STRATEGIC DEPTH: Did they trace consequences and dynamics?
3. FRAME QUALITY: Did they find the right way to think about the problem?
4. ACTIONABILITY: Is the recommendation specific and executable?
5. VERIFICATION: Did they check their reasoning and state uncertainty?

Return JSON only:
{
  "assumption_surfacing": {"score": X, "weakness": "..."},
  "strategic_depth": {"score": X, "weakness": "..."},
  "frame_quality": {"score": X, "weakness": "..."},
  "actionability": {"score": X, "weakness": "..."},
  "verification": {"score": X, "weakness": "..."},
  "total": X,
  "biggest_gap": "...",
  "suggested_improvement": "..."
}
"""

IMPROVEMENT_EXTRACTION_PROMPT = """
You are analyzing evaluation results to extract methodology improvements.

Current methodology:
{methodology}

Evaluation results from {n} problems:
{results}

Patterns observed:
- Average score: {avg_score}/50
- Weakest dimension: {weakest_dim} (avg {weakest_score})
- Most common gap: {common_gap}

Your task:
1. Identify the ROOT CAUSE of the weakest dimension
2. Propose a SPECIFIC modification to the methodology
3. The modification must be:
   - Concrete (not vague like "do better")
   - Testable (we can measure if it helps)
   - Minimal (smallest change that addresses the gap)

Return JSON with these exact keys: diagnosis, root_cause, proposed_modification (with step_affected, current, proposed, rationale), expected_effect, how_to_test.
"""


class AutomatedImprovementLoop:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.methodology = CURRENT_METHODOLOGY
        self.history = []
        self.version = 4.0

    def generate_problem(self) -> str:
        """Generate a novel problem from templates."""
        category = random.choice(list(PROBLEM_TEMPLATES.keys()))
        template = random.choice(PROBLEM_TEMPLATES[category])

        # Fill in variables (simplified - would need full implementation)
        problem = template
        for var, options in VARIABLES.items():
            if f"{{{var}}}" in problem:
                problem = problem.replace(f"{{{var}}}", random.choice(options))

        return problem, category

    def solve_problem(self, problem: str) -> str:
        """Solve problem using current methodology."""
        prompt = f"""Apply the following methodology to solve this problem:

{self.methodology}

---

PROBLEM:
{problem}

---

Apply the full methodology. Show your work for each step."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def evaluate_solution(self, problem: str, solution: str) -> Dict:
        """Have external evaluator score the solution."""
        prompt = f"""{EVALUATION_RUBRIC}

PROBLEM:
{problem}

SOLUTION:
{solution}

Evaluate and return JSON only."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            return json.loads(text[json_start:json_end])
        except:
            return None

    def extract_improvements(self, results: List[Dict]) -> Dict:
        """Analyze results and extract methodology improvements."""
        # Calculate statistics
        valid = [r for r in results if r is not None]
        if not valid:
            return None

        avg_score = sum(r['total'] for r in valid) / len(valid)

        # Find weakest dimension
        dims = ['assumption_surfacing', 'strategic_depth', 'frame_quality',
                'actionability', 'verification']
        dim_avgs = {}
        for dim in dims:
            dim_avgs[dim] = sum(r[dim]['score'] for r in valid) / len(valid)

        weakest_dim = min(dim_avgs, key=dim_avgs.get)
        weakest_score = dim_avgs[weakest_dim]

        # Find common gaps
        gaps = [r.get('biggest_gap', '') for r in valid]
        common_gap = max(set(gaps), key=gaps.count) if gaps else "Unknown"

        prompt = IMPROVEMENT_EXTRACTION_PROMPT.format(
            methodology=self.methodology,
            results=json.dumps(valid, indent=2),
            n=len(valid),
            avg_score=avg_score,
            weakest_dim=weakest_dim,
            weakest_score=weakest_score,
            common_gap=common_gap
        )

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            return json.loads(text[json_start:json_end])
        except:
            return None

    def apply_improvement(self, improvement: Dict) -> str:
        """Apply the proposed improvement to methodology."""
        mod = improvement.get('proposed_modification', {})

        # For now, just append the improvement
        # In production, would parse and modify the actual methodology
        new_addition = f"""

## IMPROVEMENT v{self.version + 0.1} (Auto-generated)

**Issue**: {improvement.get('diagnosis', 'Unknown')}
**Root cause**: {improvement.get('root_cause', 'Unknown')}
**Modification**: {mod.get('proposed', 'None')}
**Rationale**: {mod.get('rationale', 'None')}
"""
        self.methodology += new_addition
        self.version += 0.1
        return self.methodology

    def run_cycle(self, n_problems: int = 5) -> Dict:
        """Run one improvement cycle."""
        print(f"\n{'='*60}")
        print(f"CYCLE - Methodology v{self.version}")
        print(f"{'='*60}")

        results = []

        for i in range(n_problems):
            print(f"\n--- Problem {i+1}/{n_problems} ---")

            # Generate
            problem, category = self.generate_problem()
            print(f"Category: {category}")

            # Solve
            print("Solving...")
            solution = self.solve_problem(problem)

            # Evaluate
            print("Evaluating...")
            evaluation = self.evaluate_solution(problem, solution)

            if evaluation:
                print(f"Score: {evaluation.get('total', 'N/A')}/50")
                results.append(evaluation)
            else:
                print("Evaluation failed")

            time.sleep(1)  # Rate limiting

        # Extract improvements
        print("\n--- Extracting improvements ---")
        improvement = self.extract_improvements(results)

        if improvement:
            print(f"Diagnosis: {improvement.get('diagnosis', 'Unknown')}")
            print(f"Proposed fix: {improvement.get('proposed_modification', {}).get('proposed', 'None')}")

            # Apply improvement
            self.apply_improvement(improvement)
            print(f"Updated to v{self.version}")
        else:
            print("No improvement extracted")

        cycle_result = {
            "version": self.version,
            "n_problems": len(results),
            "avg_score": sum(r['total'] for r in results) / len(results) if results else 0,
            "improvement": improvement,
            "timestamp": datetime.now().isoformat()
        }

        self.history.append(cycle_result)
        return cycle_result

    def run_loop(self, n_cycles: int = 10, problems_per_cycle: int = 5,
                 convergence_threshold: float = 0.5):
        """Run the full improvement loop until convergence."""
        print("="*60)
        print("AUTOMATED CONTINUOUS IMPROVEMENT LOOP")
        print("="*60)

        for cycle in range(n_cycles):
            result = self.run_cycle(problems_per_cycle)

            # Check for convergence
            if len(self.history) >= 2:
                prev_score = self.history[-2]['avg_score']
                curr_score = self.history[-1]['avg_score']
                improvement = curr_score - prev_score

                print(f"\nImprovement this cycle: {improvement:+.2f}")

                if abs(improvement) < convergence_threshold:
                    print(f"\n{'='*60}")
                    print("CONVERGENCE DETECTED")
                    print(f"Final version: v{self.version}")
                    print(f"Final score: {curr_score:.1f}/50")
                    print(f"{'='*60}")
                    break

        # Save final results
        final_output = {
            "final_version": self.version,
            "final_methodology": self.methodology,
            "history": self.history,
            "total_cycles": len(self.history)
        }

        with open("/home/user/claude/Meta/automated_improvement_results.json", "w") as f:
            json.dump(final_output, f, indent=2)

        return final_output


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python automated_improvement_loop.py <API_KEY> [n_cycles] [problems_per_cycle]")
        sys.exit(1)

    api_key = sys.argv[1]
    n_cycles = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    problems_per = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    loop = AutomatedImprovementLoop(api_key)
    results = loop.run_loop(n_cycles=n_cycles, problems_per_cycle=problems_per)

    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"Total cycles: {results['total_cycles']}")
    print(f"Final version: v{results['final_version']}")
    if results['history']:
        scores = [h['avg_score'] for h in results['history']]
        print(f"Score progression: {' → '.join(f'{s:.1f}' for s in scores)}")
        print(f"Total improvement: {scores[-1] - scores[0]:+.1f} points")


if __name__ == "__main__":
    main()
