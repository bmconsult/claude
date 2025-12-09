"""
Run the LLM Difficulty experiment

This script sends problems to Claude and records performance.
"""

import anthropic
import json
import os
import time
from dataclasses import dataclass
from typing import List, Dict, Any

def load_problems(filename: str) -> List[Dict]:
    with open(filename) as f:
        return json.load(f)

def test_problem_with_claude(client, problem: Dict, model: str = "claude-sonnet-4-5-20250929") -> Dict:
    """
    Send problem to Claude and evaluate response.
    Using Sonnet for faster testing (can switch to Opus for comparison).
    """
    prompt = f"""Please solve this problem. Think step by step, then give your final answer.

Problem: {problem['prompt']}

After your reasoning, state your final answer clearly on a line starting with "ANSWER: "
"""

    start_time = time.time()

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        elapsed = time.time() - start_time

        # Extract answer
        answer_line = None
        for line in response_text.split('\n'):
            if line.strip().upper().startswith('ANSWER:'):
                answer_line = line.strip()[7:].strip()
                break

        return {
            'problem_id': problem['id'],
            'full_response': response_text,
            'extracted_answer': answer_line,
            'expected_answer': problem['expected_answer'],
            'response_time': elapsed,
            'model': model,
        }

    except Exception as e:
        return {
            'problem_id': problem['id'],
            'error': str(e),
            'model': model,
        }

def evaluate_answer(result: Dict, problem: Dict) -> bool:
    """
    Evaluate if the answer is correct.
    This is simplified - real evaluation would need fuzzy matching.
    """
    if 'error' in result:
        return False

    extracted = result.get('extracted_answer', '').lower().strip()
    expected = str(problem['expected_answer']).lower().strip()

    # Simple exact match or containment check
    if extracted == expected:
        return True

    # For yes/no questions
    if expected in ['yes', 'no']:
        return expected in extracted

    # For numeric answers
    try:
        if float(extracted) == float(expected):
            return True
    except:
        pass

    # Check if expected is contained in extracted
    if expected in extracted:
        return True

    return False

def run_experiment(api_key: str, problems_file: str = "llm_difficulty_battery.json"):
    """Run the full experiment."""
    client = anthropic.Anthropic(api_key=api_key)
    problems = load_problems(problems_file)

    results = []
    print(f"Running experiment with {len(problems)} problems...")
    print("-" * 60)

    for i, problem in enumerate(problems):
        print(f"[{i+1}/{len(problems)}] {problem['id']}...", end=" ", flush=True)

        result = test_problem_with_claude(client, problem)

        if 'error' not in result:
            correct = evaluate_answer(result, problem)
            result['correct'] = correct
            result['predicted_difficulty'] = problem['predicted_difficulty']
            result['complexity_class'] = problem['complexity_class']
            print(f"{'✓' if correct else '✗'} ({result['response_time']:.1f}s)")
        else:
            print(f"ERROR: {result['error']}")
            result['correct'] = False
            result['predicted_difficulty'] = problem['predicted_difficulty']
            result['complexity_class'] = problem['complexity_class']

        results.append(result)

        # Small delay to avoid rate limits
        time.sleep(0.5)

    # Save results
    with open("experiment_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # Analyze results
    analyze_results(results, problems)

    return results

def analyze_results(results: List[Dict], problems: List[Dict]):
    """Analyze correlation between predicted difficulty and actual performance."""
    print("\n" + "=" * 60)
    print("EXPERIMENT RESULTS ANALYSIS")
    print("=" * 60)

    # Group by difficulty terciles
    sorted_by_pred = sorted(results, key=lambda r: r.get('predicted_difficulty', 0))

    n = len(sorted_by_pred)
    easy = sorted_by_pred[:n//3]
    medium = sorted_by_pred[n//3:2*n//3]
    hard = sorted_by_pred[2*n//3:]

    def accuracy(group):
        if not group:
            return 0
        return sum(1 for r in group if r.get('correct')) / len(group)

    print(f"\nAccuracy by Predicted Difficulty Tercile:")
    print(f"  Easy (lowest predicted):  {accuracy(easy)*100:.1f}% ({sum(1 for r in easy if r.get('correct'))}/{len(easy)})")
    print(f"  Medium:                   {accuracy(medium)*100:.1f}% ({sum(1 for r in medium if r.get('correct'))}/{len(medium)})")
    print(f"  Hard (highest predicted): {accuracy(hard)*100:.1f}% ({sum(1 for r in hard if r.get('correct'))}/{len(hard)})")

    # Individual results
    print(f"\nIndividual Results (sorted by predicted difficulty):")
    print(f"{'ID':<25} {'Pred.Diff':>10} {'Correct':>10} {'Time':>8}")
    print("-" * 58)

    for r in sorted_by_pred:
        pred = r.get('predicted_difficulty', 0)
        correct = '✓' if r.get('correct') else '✗'
        time_s = r.get('response_time', 0)
        print(f"{r['problem_id']:<25} {pred:>10.2f} {correct:>10} {time_s:>8.1f}s")

    # Key prediction: P problems with high state tracking should be hard
    print("\n" + "-" * 60)
    print("KEY HYPOTHESIS TEST: State Tracking in P problems")
    print("-" * 60)

    p_problems = [r for r, p in zip(results, problems) if p['complexity_class'] in ['O(1)', 'O(n)', 'P']]
    high_state = [r for r, p in zip(results, problems)
                  if p['complexity_class'] in ['O(1)', 'O(n)', 'P'] and p['state_depth'] >= 5]

    print(f"All P problems accuracy: {accuracy(p_problems)*100:.1f}%")
    print(f"P problems with high state (≥5): {accuracy(high_state)*100:.1f}%")

    # Compare verify vs compute
    print("\n" + "-" * 60)
    print("VERIFY vs COMPUTE (same complexity)")
    print("-" * 60)

    verify_problems = [r for r, p in zip(results, problems) if 'verify' in p['id']]
    compute_problems = [r for r, p in zip(results, problems)
                        if 'compute' in p['id'] or 'factor' in p['id'] or 'solve' in p['id'] or 'find' in p['id']]

    print(f"Verification tasks accuracy: {accuracy(verify_problems)*100:.1f}%")
    print(f"Computation tasks accuracy:  {accuracy(compute_problems)*100:.1f}%")

if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try to read from a standard location
        print("No ANTHROPIC_API_KEY environment variable set.")
        print("Please set it or pass the key directly.")
    else:
        run_experiment(api_key)
