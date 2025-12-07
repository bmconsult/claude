"""
Problem Router

A meta-tool that decides which tools to use based on problem type.
This is what makes the other tools compound - intelligent routing.

The idea: Instead of manually choosing tools, this analyzes the problem
and creates a pipeline of tools to apply.
"""

import anthropic
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class ProblemType(Enum):
    CONSTRAINT = "constraint"      # Has verifiable constraints
    CREATIVE = "creative"          # Needs novel ideas
    ANALYTICAL = "analytical"      # Needs careful reasoning
    STRATEGIC = "strategic"        # Needs planning
    EXPLORATORY = "exploratory"    # Needs open-ended exploration
    UNKNOWN = "unknown"


class Tool(Enum):
    ENSEMBLE = "ensemble_reasoning"
    PLANNER = "strategic_planner"
    VERIFIER = "verification_engine"
    EMERGENCE = "emergence_prompt"
    DIRECT = "direct_solve"  # No special tool needed


@dataclass
class ProblemAnalysis:
    """Analysis of a problem to determine routing."""
    problem: str
    problem_type: ProblemType
    has_constraints: bool
    needs_creativity: bool
    needs_planning: bool
    needs_verification: bool
    confidence: float
    reasoning: str


@dataclass
class Pipeline:
    """A sequence of tools to apply to a problem."""
    tools: List[Tool]
    reasoning: str


TOOL_DESCRIPTIONS = """
Available tools:
1. ensemble_reasoning: Multiple Claude perspectives analyze the problem, then synthesize. Good for complex analytical problems.
2. strategic_planner: Forces explicit planning with failure pre-mortems. Good for strategic/planning problems.
3. verification_engine: Computationally verifies solutions satisfy constraints. REQUIRED for any constraint problem.
4. emergence_prompt: Facilitates Claude-to-Claude exploration. Good for exploratory/creative problems.
5. direct_solve: No special tool - just solve directly. Good for simple, clear problems.
"""


def analyze_problem(problem: str) -> ProblemAnalysis:
    """Analyze a problem to determine its type and needs."""
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0.3,
        messages=[{
            "role": "user",
            "content": f"""Analyze this problem for routing to the right tool:

PROBLEM: {problem}

Answer these questions:
1. Problem type: Is this a CONSTRAINT problem (has verifiable constraints like "no two X can Y"), CREATIVE (needs novel ideas), ANALYTICAL (needs careful reasoning), STRATEGIC (needs planning), or EXPLORATORY (open-ended)?

2. Has verifiable constraints? (yes/no) - If yes, we MUST use verification_engine

3. Needs creativity/novelty? (yes/no)

4. Needs explicit planning/strategy? (yes/no)

5. Confidence (0-100%) in this analysis

6. Brief reasoning (1-2 sentences)

Format:
TYPE: [type]
CONSTRAINTS: [yes/no]
CREATIVITY: [yes/no]
PLANNING: [yes/no]
CONFIDENCE: [number]%
REASONING: [text]"""
        }]
    )

    text = response.content[0].text

    # Parse response (simplified)
    def extract_field(text, field):
        for line in text.split("\n"):
            if line.upper().startswith(field.upper()):
                return line.split(":", 1)[1].strip()
        return ""

    type_str = extract_field(text, "TYPE").lower()
    problem_type = ProblemType.UNKNOWN
    for pt in ProblemType:
        if pt.value in type_str:
            problem_type = pt
            break

    has_constraints = "yes" in extract_field(text, "CONSTRAINTS").lower()
    needs_creativity = "yes" in extract_field(text, "CREATIVITY").lower()
    needs_planning = "yes" in extract_field(text, "PLANNING").lower()

    try:
        confidence = float(extract_field(text, "CONFIDENCE").replace("%", "")) / 100
    except:
        confidence = 0.5

    reasoning = extract_field(text, "REASONING")

    return ProblemAnalysis(
        problem=problem,
        problem_type=problem_type,
        has_constraints=has_constraints,
        needs_creativity=needs_creativity,
        needs_planning=needs_planning,
        needs_verification=has_constraints,  # Always verify constraint problems
        confidence=confidence,
        reasoning=reasoning
    )


def create_pipeline(analysis: ProblemAnalysis) -> Pipeline:
    """Create a tool pipeline based on problem analysis."""
    tools = []
    reasoning_parts = []

    # Strategic problems get planning first
    if analysis.needs_planning or analysis.problem_type == ProblemType.STRATEGIC:
        tools.append(Tool.PLANNER)
        reasoning_parts.append("Strategic planning needed first")

    # Complex analytical problems get ensemble
    if analysis.problem_type == ProblemType.ANALYTICAL:
        tools.append(Tool.ENSEMBLE)
        reasoning_parts.append("Multiple perspectives for complex analysis")

    # Creative/exploratory problems get emergence
    if analysis.needs_creativity or analysis.problem_type in [ProblemType.CREATIVE, ProblemType.EXPLORATORY]:
        tools.append(Tool.EMERGENCE)
        reasoning_parts.append("Emergence for creative exploration")

    # Constraint problems ALWAYS get verification at the end
    if analysis.has_constraints:
        if not tools:
            tools.append(Tool.DIRECT)
        tools.append(Tool.VERIFIER)
        reasoning_parts.append("REQUIRED: Verification for constraint problem")

    # If nothing selected, direct solve
    if not tools:
        tools.append(Tool.DIRECT)
        reasoning_parts.append("Simple enough for direct solving")

    return Pipeline(
        tools=tools,
        reasoning="; ".join(reasoning_parts)
    )


def route_problem(problem: str) -> dict:
    """Main entry point: analyze problem and create pipeline."""
    print(f"=== PROBLEM ROUTER ===")
    print(f"Problem: {problem[:100]}...")
    print()

    analysis = analyze_problem(problem)

    print("=== ANALYSIS ===")
    print(f"Type: {analysis.problem_type.value}")
    print(f"Has constraints: {analysis.has_constraints}")
    print(f"Needs creativity: {analysis.needs_creativity}")
    print(f"Needs planning: {analysis.needs_planning}")
    print(f"Confidence: {analysis.confidence:.0%}")
    print(f"Reasoning: {analysis.reasoning}")
    print()

    pipeline = create_pipeline(analysis)

    print("=== PIPELINE ===")
    print(f"Tools: {' -> '.join(t.value for t in pipeline.tools)}")
    print(f"Reasoning: {pipeline.reasoning}")

    return {
        "analysis": analysis,
        "pipeline": pipeline
    }


if __name__ == "__main__":
    import sys

    problems = [
        "Place 5 queens on a 5x5 board with no attacks and no corners",
        "How could an AI system achieve recursive self-improvement?",
        "Design a new programming language for AI development",
        "What's 347 × 823?",
    ]

    if len(sys.argv) > 1:
        problems = [" ".join(sys.argv[1:])]

    for problem in problems:
        route_problem(problem)
        print("\n" + "="*60 + "\n")
