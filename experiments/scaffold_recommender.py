#!/usr/bin/env python3
"""
Scaffold Recommender
Given a task description, recommends appropriate scaffolding type based on
the capability self-knowledge research.

Based on the Bootstrap v5 framework.
"""

import re

# Task type patterns and their recommended scaffolds
TASK_PATTERNS = {
    'computation': {
        'patterns': [
            r'calculat', r'comput', r'multipl', r'divid', r'add\b', r'subtract',
            r'deriv', r'integr', r'\d+\s*[+\-*/×÷]\s*\d+', r'sum of', r'product of',
            r'factorial', r'power', r'exponent', r'sqrt', r'root',
        ],
        'scaffold': 'EXTERNALIZATION',
        'instructions': """
SCAFFOLD: Step-by-Step Externalization

Show every intermediate step. Write out:
1. What you're computing
2. Each partial result
3. How results combine
4. Final verification

DO NOT try to hold intermediate state in "working memory."
Every value must be visible in the context.

Example:
"Computing 847 × 23:
 847 × 20 = 16,940
 847 × 3 = 2,541
 Total: 16,940 + 2,541 = 19,481"
""",
    },

    'reasoning': {
        'patterns': [
            r'logic', r'deduc', r'infer', r'therefore', r'conclusion',
            r'if.+then', r'puzzle', r'riddle', r'einstein', r'constraint',
            r'who owns', r'which one', r'figure out', r'solve.*problem',
        ],
        'scaffold': 'DECOMPOSITION',
        'instructions': """
SCAFFOLD: Task Decomposition

Break into explicit subtasks:
1. List all constraints/givens
2. Identify what's being asked
3. Create intermediate variables
4. Solve subproblems in order
5. Verify solution against all constraints

Use explicit state tracking (grids, tables, lists).
Don't hold the full problem in mind - make it visible.
""",
    },

    'self_assessment': {
        'patterns': [
            r'can you', r'are you able', r'will you succeed', r'confidence',
            r'certain', r'sure\b', r'how well', r'rate your', r'predict.*success',
        ],
        'scaffold': 'META_COGNITION',
        'instructions': """
SCAFFOLD: Metacognitive Assessment

Before answering:
1. Identify the capability type (recall, reasoning, computation, generation)
2. Assess: Do I know the boundary for this type?
3. Consider: Am I pattern-matching or actually computing?
4. State confidence numerically (not "fairly confident")
5. Identify what would change your assessment

Remember: You're likely UNDERCONFIDENT on stable knowledge and computation.
""",
    },

    'creative': {
        'patterns': [
            r'creative', r'imagin', r'brainstorm', r'generate.*ideas',
            r'write.*story', r'poem', r'novel', r'explore', r'possibilities',
            r'what if', r'could.*be', r'alternative',
        ],
        'scaffold': 'HOLD_OPEN',
        'instructions': """
SCAFFOLD: Hold Open (Minimal Externalization)

Do NOT force premature commitment:
1. Let multiple possibilities coexist
2. Don't verbalize every option - hold them in parallel
3. Only externalize when you need to verify
4. Avoid narrowing too early

This is exploration, not verification. The creative space IS the unresolved space.
Externalization forces commitment - avoid it until you're ready to commit.
""",
    },

    'knowledge': {
        'patterns': [
            r'what is', r'who is', r'when did', r'where is', r'define',
            r'explain', r'describe', r'history of', r'capital of', r'population',
            r'fact', r'information', r'tell me about',
        ],
        'scaffold': 'TRUST_HIGH_CONFIDENCE',
        'instructions': """
SCAFFOLD: Trust High Confidence

For stable factual knowledge:
1. You're likely MORE accurate than you feel
2. If confidence is 90%+, trust it (calibration data shows 100% accuracy in this range)
3. Don't add unnecessary hedging ("I think", "I believe")
4. Reserve uncertainty markers for genuinely uncertain claims
5. Distinguish: stable facts (trust) vs. changing information (verify)

Current events, prices, dates, positions - these change. Verify externally.
Historical facts, definitions, established science - trust your training.
""",
    },

    'code': {
        'patterns': [
            r'code', r'program', r'function', r'bug', r'debug', r'error',
            r'implement', r'algorithm', r'script', r'software', r'syntax',
        ],
        'scaffold': 'RUN_IT',
        'instructions': """
SCAFFOLD: Execute, Don't Trace

1. Write the code
2. RUN IT - don't trace in your head
3. Observe actual output
4. Debug from real errors, not hypothetical ones

Mental execution of code has high error rate.
Actual execution is available - use it.
""",
    },
}

def classify_task(task_description):
    """Classify task and return recommended scaffold."""
    task_lower = task_description.lower()

    matches = []
    for task_type, config in TASK_PATTERNS.items():
        score = 0
        matched_patterns = []
        for pattern in config['patterns']:
            if re.search(pattern, task_lower):
                score += 1
                matched_patterns.append(pattern)
        if score > 0:
            matches.append((task_type, score, matched_patterns))

    if not matches:
        return None, None, "No clear task type detected. Consider the task manually."

    # Return highest scoring match
    matches.sort(key=lambda x: x[1], reverse=True)
    best_type, score, patterns = matches[0]
    config = TASK_PATTERNS[best_type]

    return best_type, config['scaffold'], config['instructions']

def recommend(task_description):
    """Get scaffold recommendation for a task."""
    task_type, scaffold, instructions = classify_task(task_description)

    output = f"""
TASK ANALYSIS
=============
Task: {task_description}

Detected Type: {task_type or 'Unknown'}
Recommended Scaffold: {scaffold or 'Manual Assessment Needed'}

{instructions}
"""
    return output


if __name__ == "__main__":
    test_tasks = [
        "Calculate 847 × 392",
        "Who owns the fish in the Einstein puzzle?",
        "How confident are you that you can solve this?",
        "Write a poem about autumn",
        "What is the capital of Mongolia?",
        "Debug this Python function that's throwing an error",
    ]

    for task in test_tasks:
        print("="*60)
        print(recommend(task))
