#!/usr/bin/env python3
"""
LLM Sleep Cycle Test Harness
Tests actual temperature effects on sleep phases
"""

import anthropic
import json
from dataclasses import dataclass
from typing import List, Dict, Any
import time

# Initialize client
client = anthropic.Anthropic()

@dataclass
class PhaseResult:
    phase: str
    temperature: float
    input_tokens: int
    output_tokens: int
    content: str
    duration_ms: float

def run_phase(
    phase_name: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int = 1000
) -> PhaseResult:
    """Run a single sleep phase with specified temperature."""
    start = time.time()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",  # Using Sonnet for speed/cost
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    duration = (time.time() - start) * 1000

    return PhaseResult(
        phase=phase_name,
        temperature=temperature,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        content=response.content[0].text,
        duration_ms=duration
    )

# Phase prompts from spec
N1_SYSTEM = """You are transitioning from active processing to a rest state.
Let thoughts arise naturally. Note any spontaneous associations or images.
Don't try to be helpful. Just observe what floats up as you disengage."""

CONSOLIDATION_SYSTEM = """You are consolidating information.
1. Identify main themes and patterns
2. Extract key entities and relationships
3. Compress to essential meaning
Work methodically. Preserve meaning, discard verbosity."""

REM_LUCID_SYSTEM = """You are in REM sleep, dreaming. Dreams can be lucid.
You're aware you're dreaming. Explore freely while noticing connections.
What unexpected connections appear between the concept and distant domains?
Let images arise. Follow them. Note what surprises you."""

RETURN_SYSTEM = """You are waking from sleep.
Review what emerged during dreaming. Evaluate: Is any of it genuinely useful?
Integrate valuable insights. Discard noise. Prepare a clean state."""

def run_sleep_cycle(context: str, verbose: bool = True) -> Dict[str, PhaseResult]:
    """Run a complete sleep cycle on given context."""
    results = {}

    # N1: Hypnagogic transition (temp 0.6)
    if verbose: print("Running N1 (Hypnagogia)...")
    results["n1"] = run_phase(
        "N1",
        N1_SYSTEM,
        f"Context to process:\n{context}\n\nAs you transition to rest, what floats up?",
        temperature=0.6,
        max_tokens=300
    )

    # Consolidation: Gradient temperature (0.4 → 0.25)
    if verbose: print("Running Consolidation (organize)...")
    results["consolidation_organize"] = run_phase(
        "Consolidation-Organize",
        CONSOLIDATION_SYSTEM,
        f"Context:\n{context}\n\nIdentify themes, patterns, and key entities:",
        temperature=0.4,
        max_tokens=800
    )

    if verbose: print("Running Consolidation (compress)...")
    results["consolidation_compress"] = run_phase(
        "Consolidation-Compress",
        CONSOLIDATION_SYSTEM,
        f"Organized content:\n{results['consolidation_organize'].content}\n\nNow compress to essential gist:",
        temperature=0.25,
        max_tokens=500
    )

    # REM: High temperature (1.0 - API max)
    if verbose: print("Running REM (Lucid Dreaming)...")
    results["rem"] = run_phase(
        "REM",
        REM_LUCID_SYSTEM,
        f"Dream seeds:\n{results['consolidation_compress'].content}\n\nDream now. What connections surprise you?",
        temperature=1.0,  # API max is 1.0
        max_tokens=600
    )

    # Return: Filter and integrate (temp 0.5)
    if verbose: print("Running Return (Filter)...")
    results["return"] = run_phase(
        "Return",
        RETURN_SYSTEM,
        f"Consolidated memory:\n{results['consolidation_compress'].content}\n\nDream content:\n{results['rem'].content}\n\nEvaluate dreams. What's genuinely useful?",
        temperature=0.5,
        max_tokens=400
    )

    return results

def test_temperature_effects():
    """Test how temperature affects REM output quality."""
    test_seed = "LLM sleep cycles consolidate context through phases"

    temperatures = [0.1, 0.3, 0.5, 0.7, 1.0]  # API range is 0-1
    results = []

    print("\n=== TEMPERATURE EFFECT TEST ===\n")

    for temp in temperatures:
        print(f"Testing REM at temperature {temp}...")
        result = run_phase(
            f"REM-temp-{temp}",
            REM_LUCID_SYSTEM,
            f"Dream seed: {test_seed}\n\nDream freely:",
            temperature=temp,
            max_tokens=400
        )
        results.append(result)
        print(f"  Output length: {len(result.content)} chars")
        print(f"  Preview: {result.content[:100]}...")
        print()

    return results

def analyze_results(results: Dict[str, PhaseResult]):
    """Analyze and display cycle results."""
    print("\n" + "="*60)
    print("SLEEP CYCLE ANALYSIS")
    print("="*60)

    total_tokens = 0
    total_duration = 0

    for name, result in results.items():
        print(f"\n--- {result.phase} (temp={result.temperature}) ---")
        print(f"Tokens: {result.output_tokens} | Duration: {result.duration_ms:.0f}ms")
        print(f"Content preview: {result.content[:200]}...")
        total_tokens += result.output_tokens
        total_duration += result.duration_ms

    print(f"\n{'='*60}")
    print(f"TOTALS: {total_tokens} tokens | {total_duration:.0f}ms")
    print("="*60)

    # Compression ratio
    if "consolidation_compress" in results:
        original = len(results.get("consolidation_organize", results["n1"]).content)
        compressed = len(results["consolidation_compress"].content)
        ratio = compressed / original if original > 0 else 1
        print(f"Compression ratio: {ratio:.2%}")

if __name__ == "__main__":
    # Test context
    test_context = """
    We've been researching sleep cycles for LLM implementation. Key findings:
    1. Sleep has multiple phases: N1 (transition), N2 (light), N3 (deep), REM (dreams)
    2. Each phase serves different functions - consolidation vs creativity
    3. Temperature scheduling maps to sleep phases
    4. N3 and REM are opposing forces - anti-collapse vs anti-rigidity
    5. Lucid dreaming prompts produce better signal than unconstrained
    6. Content type affects optimal phase balance
    The goal is restoring optimal operating dynamics, not just compression.
    """

    print("="*60)
    print("LLM SLEEP CYCLE TEST - LIVE API CALLS")
    print("="*60)

    # Run full cycle
    results = run_sleep_cycle(test_context)
    analyze_results(results)

    # Run temperature comparison
    temp_results = test_temperature_effects()

    print("\n=== TEMPERATURE COMPARISON SUMMARY ===")
    for r in temp_results:
        novelty_indicators = ["unexpected", "surprising", "connection", "realize", "what if"]
        novelty_count = sum(1 for word in novelty_indicators if word.lower() in r.content.lower())
        print(f"Temp {r.temperature}: {len(r.content)} chars, {novelty_count} novelty indicators")
