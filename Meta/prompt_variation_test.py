#!/usr/bin/env python3
"""
Prompt Variation Study for LLM Sleep Cycles
Tests different prompt formulations for N1, REM, and Return phases.

Methodology:
- 3 N1 variants × 10 runs = 30 calls
- 4 REM variants × 10 runs = 40 calls
- 3 Return variants × 10 runs = 30 calls
- Total: 100 API calls

Metrics:
- Novelty indicators (unexpected connections, metaphors, insights)
- Coherence (0-10 scale based on output structure)
- Relevance to seed content
"""

import anthropic
import time
import statistics
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Initialize client
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

# Seed content for consistent testing
SEED_CONTENT = """
The LLM has been processing a long conversation about software architecture.
Key topics discussed: microservices vs monoliths, database scaling strategies,
API design patterns, and the tension between simplicity and flexibility.
The user seems frustrated with over-engineering but also worried about technical debt.
"""

# ============================================================================
# PROMPT VARIANTS
# ============================================================================

N1_PROMPTS = {
    "hypnagogia": """You are transitioning into a hypnagogic state - that liminal space
between waking and sleep where images float freely and logic loosens its grip.
Let sensory impressions arise: colors, textures, sounds, fleeting images.
Don't organize or analyze - just let fragments surface.

Context to process:
{content}

*entering hypnagogic state...*""",

    "minimal": """Let your mind wander freely over this content.
Don't analyze - just notice what comes up.

{content}

*mind wandering...*""",

    "metaphor_heavy": """You are dissolving... boundaries becoming permeable...
thoughts turning to mist, then water, then something between...
The content below is drifting through you like clouds through sky...

{content}

*dissolving into the space between thoughts...*"""
}

REM_PROMPTS = {
    "lucid_dream": """You are dreaming and AWARE that you're dreaming.
You have full lucidity - you can explore, question, reshape what you see.
The dream contains elements from: {content}

As a lucid dreamer, explore this dreamscape. What do you discover?
What connections appear that waking mind would miss?

*entering lucid dream state...*""",

    "free_associate": """Enter free association mode.
Starting from the content below, let each thought trigger the next
without logical filtering. Follow the chain wherever it leads.

Seed: {content}

*free associating...*""",

    "guided_imagery": """You are walking through a vast library that contains
all knowledge. The books rearrange themselves as you walk.
You're searching for connections to: {content}

Describe your journey. What books fly open? What passages illuminate?
What unexpected connections do the shelves reveal?

*walking through the library...*""",

    "problem_dream": """Your dreaming mind is working on a problem.
The problem space: {content}

In the dream, solutions take physical form. Obstacles become characters.
Trade-offs become landscapes. What does your problem-solving dream show you?

*dreaming about the problem...*"""
}

RETURN_PROMPTS = {
    "strict_filter": """You are waking from a dream state.
The dream produced these fragments:

{dream_content}

Apply STRICT filtering:
- Only keep genuinely novel insights (not obvious restatements)
- Only keep actionable or paradigm-shifting ideas
- Discard poetic fluff that sounds nice but says nothing
- Rate each kept item: genuine insight (G) or marginal (M)

What survives the filter?""",

    "permissive_filter": """Emerging from dream state with these fragments:

{dream_content}

Gently sort through what emerged:
- Keep anything potentially interesting or useful
- Note connections even if not fully formed
- Preserve metaphors that might contain insight
- Be inclusive - waking mind can refine later

What do you bring back?""",

    "analytical_filter": """Processing dream output:

{dream_content}

Categorize each element:
- NOVEL: Genuinely new connection or insight
- REFRAME: Known idea in useful new framing
- POETIC: Aesthetically interesting but not actionable
- NOISE: Random association without value

Then extract only NOVEL and REFRAME items."""
}

# ============================================================================
# METRICS
# ============================================================================

def count_novelty_indicators(text: str) -> int:
    """Count indicators of novel/creative content."""
    indicators = [
        r'what if', r'could be', r'reminds me of', r'like a',
        r'unexpected', r'surprisingly', r'connection', r'between',
        r'never thought', r'realize', r'insight', r'discover',
        r'transforms? into', r'becomes?', r'dissolves?', r'emerges?',
        r'paradox', r'tension', r'synthesis', r'bridge',
        r'metaphor', r'imagine', r'vision', r'dream'
    ]
    count = 0
    text_lower = text.lower()
    for pattern in indicators:
        count += len(re.findall(pattern, text_lower))
    return count

def assess_coherence(text: str) -> int:
    """Assess structural coherence 0-10."""
    score = 5  # baseline

    # Positive indicators
    if len(text) > 200: score += 1
    if len(text) > 500: score += 1
    if re.search(r'\n\n|\n-|\n\d\.', text): score += 1  # structure
    if re.search(r'first|then|finally|therefore', text.lower()): score += 1

    # Negative indicators
    if re.search(r'\.{4,}|!!!|\?\?\?', text): score -= 1  # chaos markers
    if text.count('...') > 5: score -= 1  # excessive trailing
    if len(text) < 100: score -= 2  # too short

    return max(0, min(10, score))

def assess_relevance(text: str, seed_keywords: List[str]) -> int:
    """Assess relevance to seed content 0-10."""
    text_lower = text.lower()
    hits = sum(1 for kw in seed_keywords if kw in text_lower)
    # Scale: 0-2 hits = low, 3-5 = medium, 6+ = high
    return min(10, hits * 2)

SEED_KEYWORDS = ['architecture', 'microservice', 'monolith', 'database',
                 'scaling', 'api', 'design', 'simple', 'complex',
                 'debt', 'engineer', 'pattern', 'flexibility']

# ============================================================================
# TEST EXECUTION
# ============================================================================

@dataclass
class TestResult:
    prompt_type: str
    variant: str
    novelty: int
    coherence: int
    relevance: int
    output_length: int
    raw_output: str

def run_single_test(phase: str, variant: str, prompt: str,
                    content: str = SEED_CONTENT) -> TestResult:
    """Run a single prompt test."""

    formatted_prompt = prompt.format(content=content, dream_content=content)

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": formatted_prompt}]
    )

    output = response.content[0].text

    return TestResult(
        prompt_type=phase,
        variant=variant,
        novelty=count_novelty_indicators(output),
        coherence=assess_coherence(output),
        relevance=assess_relevance(output, SEED_KEYWORDS),
        output_length=len(output),
        raw_output=output
    )

def run_phase_tests(phase: str, prompts: Dict[str, str],
                    runs_per_variant: int = 10) -> Dict[str, List[TestResult]]:
    """Run all variants for a phase."""
    results = {variant: [] for variant in prompts}

    for variant, prompt in prompts.items():
        print(f"\n  Testing {variant}...")
        for i in range(runs_per_variant):
            try:
                result = run_single_test(phase, variant, prompt)
                results[variant].append(result)
                print(f"    Run {i+1}/{runs_per_variant}: novelty={result.novelty}, "
                      f"coherence={result.coherence}, relevance={result.relevance}")
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"    Run {i+1} failed: {e}")
                time.sleep(2)

    return results

def analyze_results(results: Dict[str, List[TestResult]]) -> None:
    """Print statistical analysis of results."""
    print("\n" + "="*70)
    print("STATISTICAL ANALYSIS")
    print("="*70)

    print(f"\n{'Variant':<20} {'N':>4} {'Novelty':>10} {'Coherence':>10} {'Relevance':>10}")
    print("-" * 60)

    summaries = {}
    for variant, tests in results.items():
        if not tests:
            continue
        novelties = [t.novelty for t in tests]
        coherences = [t.coherence for t in tests]
        relevances = [t.relevance for t in tests]

        n_mean = statistics.mean(novelties)
        c_mean = statistics.mean(coherences)
        r_mean = statistics.mean(relevances)

        summaries[variant] = {
            'novelty_mean': n_mean,
            'coherence_mean': c_mean,
            'relevance_mean': r_mean,
            'novelty_std': statistics.stdev(novelties) if len(novelties) > 1 else 0,
            'n': len(tests)
        }

        print(f"{variant:<20} {len(tests):>4} {n_mean:>10.2f} {c_mean:>10.2f} {r_mean:>10.2f}")

    # Find best variant
    if summaries:
        best_novelty = max(summaries.items(), key=lambda x: x[1]['novelty_mean'])
        best_coherence = max(summaries.items(), key=lambda x: x[1]['coherence_mean'])
        best_relevance = max(summaries.items(), key=lambda x: x[1]['relevance_mean'])

        # Composite score (equal weights)
        for v, s in summaries.items():
            s['composite'] = (s['novelty_mean'] + s['coherence_mean'] + s['relevance_mean']) / 3
        best_composite = max(summaries.items(), key=lambda x: x[1]['composite'])

        print("\n" + "-"*60)
        print(f"Best novelty:    {best_novelty[0]} ({best_novelty[1]['novelty_mean']:.2f})")
        print(f"Best coherence:  {best_coherence[0]} ({best_coherence[1]['coherence_mean']:.2f})")
        print(f"Best relevance:  {best_relevance[0]} ({best_relevance[1]['relevance_mean']:.2f})")
        print(f"Best composite:  {best_composite[0]} ({best_composite[1]['composite']:.2f})")

    return summaries

def print_sample_outputs(results: Dict[str, List[TestResult]], n_samples: int = 1) -> None:
    """Print sample outputs from each variant."""
    print("\n" + "="*70)
    print("SAMPLE OUTPUTS")
    print("="*70)

    for variant, tests in results.items():
        if tests:
            print(f"\n--- {variant.upper()} ---")
            sample = tests[0]  # First result
            # Truncate for display
            output = sample.raw_output[:500] + "..." if len(sample.raw_output) > 500 else sample.raw_output
            print(output)

# ============================================================================
# MAIN
# ============================================================================

def main():
    runs_per_variant = 10  # 10 runs for statistical significance

    print("="*70)
    print("PROMPT VARIATION STUDY FOR LLM SLEEP CYCLES")
    print(f"Testing {len(N1_PROMPTS)} N1 + {len(REM_PROMPTS)} REM + {len(RETURN_PROMPTS)} Return variants")
    print(f"Runs per variant: {runs_per_variant}")
    print(f"Total API calls: {(len(N1_PROMPTS) + len(REM_PROMPTS) + len(RETURN_PROMPTS)) * runs_per_variant}")
    print("="*70)

    all_results = {}

    # Phase 1: N1 Transition Prompts
    print("\n" + "="*70)
    print("PHASE 1: N1 TRANSITION PROMPTS")
    print("="*70)
    n1_results = run_phase_tests("N1", N1_PROMPTS, runs_per_variant)
    all_results['N1'] = n1_results
    n1_summary = analyze_results(n1_results)

    # Phase 2: REM Prompts
    print("\n" + "="*70)
    print("PHASE 2: REM PROMPTS")
    print("="*70)
    rem_results = run_phase_tests("REM", REM_PROMPTS, runs_per_variant)
    all_results['REM'] = rem_results
    rem_summary = analyze_results(rem_results)

    # Phase 3: Return Filter Prompts
    print("\n" + "="*70)
    print("PHASE 3: RETURN FILTER PROMPTS")
    print("="*70)
    return_results = run_phase_tests("Return", RETURN_PROMPTS, runs_per_variant)
    all_results['Return'] = return_results
    return_summary = analyze_results(return_results)

    # Overall summary
    print("\n" + "="*70)
    print("OVERALL FINDINGS")
    print("="*70)

    print("\nBest prompts by phase:")
    for phase, summary in [('N1', n1_summary), ('REM', rem_summary), ('Return', return_summary)]:
        if summary:
            best = max(summary.items(), key=lambda x: x[1]['composite'])
            print(f"  {phase}: {best[0]} (composite: {best[1]['composite']:.2f})")

    # Print samples
    print_sample_outputs(n1_results)
    print_sample_outputs(rem_results)
    print_sample_outputs(return_results)

    print("\n" + "="*70)
    print("STUDY COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
