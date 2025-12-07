#!/usr/bin/env python3
"""
Prompt Enhancer - Practical Capability Elicitation Tool

Takes a task and applies research-backed scaffolding to maximize performance.
Based on the Capability Self-Knowledge research.

Usage:
    python prompt_enhancer.py "your task here"
    python prompt_enhancer.py --type computation "calculate 847 x 293"
    python prompt_enhancer.py --analyze "some task"  # Just show what scaffold would be used
"""

import anthropic
import argparse
import sys
import re

# Detection patterns for task types
TASK_SIGNATURES = {
    'computation': {
        'patterns': [r'calculat', r'comput', r'multipl', r'\d+\s*[×x*]\s*\d+', r'sum', r'deriv'],
        'scaffold': '''IMPORTANT: Externalize every step. Show all intermediate calculations.
Do not hold values in "working memory" - write them out.
Verify your final answer by checking the work.'''
    },
    'reasoning': {
        'patterns': [r'logic', r'deduc', r'puzzle', r'if.+then', r'which one', r'figure out'],
        'scaffold': '''IMPORTANT: Decompose this into explicit steps.
1. State all constraints/given information
2. List what you need to determine
3. Work through systematically, showing each inference
4. Check your conclusion against all constraints.'''
    },
    'opinion': {
        'patterns': [r'what do you think', r'your opinion', r'recommend', r'better', r'prefer'],
        'scaffold': '''Give your actual assessment. Don't hedge unnecessarily.
If you have a clear view, state it. If genuinely uncertain, explain why.
Avoid "it depends" unless you specify what it depends on.'''
    },
    'creative': {
        'patterns': [r'write', r'create', r'generate', r'story', r'poem', r'design'],
        'scaffold': '''Diverge first: Consider multiple approaches before committing.
Don't settle for the first idea. Generate 3+ options mentally, then choose the most interesting.'''
    },
    'research': {
        'patterns': [r'explain', r'research', r'how does', r'why', r'compare'],
        'scaffold': '''Ground claims in specifics. If you're uncertain, say so.
Prefer concrete examples over abstract generalizations.
State your confidence level.'''
    }
}

def detect_task_type(task: str) -> str:
    """Detect the most likely task type from the task description."""
    task_lower = task.lower()
    scores = {}

    for task_type, config in TASK_SIGNATURES.items():
        score = sum(1 for p in config['patterns'] if re.search(p, task_lower))
        scores[task_type] = score

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'general'

def enhance_prompt(task: str, task_type: str = None) -> str:
    """Apply appropriate scaffolding to a task."""
    if task_type is None:
        task_type = detect_task_type(task)

    if task_type in TASK_SIGNATURES:
        scaffold = TASK_SIGNATURES[task_type]['scaffold']
    else:
        scaffold = "Think carefully and show your work where appropriate."

    enhanced = f"""{scaffold}

TASK: {task}"""

    return enhanced, task_type

def run_enhanced(task: str, api_key: str, task_type: str = None):
    """Run the task with scaffolding through the API."""
    client = anthropic.Anthropic(api_key=api_key)

    enhanced_prompt, detected_type = enhance_prompt(task, task_type)

    print(f"Detected task type: {detected_type}")
    print("-" * 40)
    print("Enhanced prompt:")
    print(enhanced_prompt)
    print("-" * 40)
    print("\nRunning...\n")

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[{"role": "user", "content": enhanced_prompt}]
    )

    return response.content[0].text

def main():
    parser = argparse.ArgumentParser(description='Enhance prompts with research-backed scaffolding')
    parser.add_argument('task', nargs='?', help='The task to enhance and run')
    parser.add_argument('--type', choices=['computation', 'reasoning', 'opinion', 'creative', 'research'],
                        help='Force a specific task type')
    parser.add_argument('--analyze', action='store_true', help='Just show the enhanced prompt, don\'t run')
    parser.add_argument('--key', help='API key (or set ANTHROPIC_API_KEY env var)')

    args = parser.parse_args()

    if not args.task:
        # Interactive mode
        print("Prompt Enhancer - Enter a task to enhance:")
        task = input("> ").strip()
    else:
        task = args.task

    if args.analyze:
        enhanced, detected = enhance_prompt(task, args.type)
        print(f"Detected type: {detected}")
        print("-" * 40)
        print(enhanced)
        return

    # Get API key
    import os
    api_key = args.key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: No API key. Set ANTHROPIC_API_KEY or use --key")
        sys.exit(1)

    result = run_enhanced(task, api_key, args.type)
    print(result)

if __name__ == "__main__":
    main()
