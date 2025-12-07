#!/usr/bin/env python3
"""
Synthesis Engine

Finds non-obvious connections across multiple sources.
This leverages Claude's actual strength: holding large context
and finding patterns humans miss because they can't read everything.

Key insight: The value isn't in the code, it's in Claude's reasoning.
This tool structures the prompting to maximize that reasoning.
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class Source:
    title: str
    content: str
    domain: str  # e.g., "biology", "economics", "philosophy"


@dataclass
class Connection:
    sources: List[str]  # titles of connected sources
    insight: str
    novelty_score: float  # 0-10, self-assessed
    testable: bool
    test_suggestion: Optional[str]


class SynthesisEngine:
    """
    Finds unexpected connections across disparate sources.

    The magic isn't in this code - it's in structuring
    the prompt to unlock Claude's pattern-finding.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.sources: List[Source] = []

    def add_source(self, title: str, content: str, domain: str):
        """Add a source document."""
        self.sources.append(Source(title=title, content=content, domain=domain))

    def synthesize(self, question: Optional[str] = None) -> Dict:
        """
        Find connections across all added sources.

        Args:
            question: Optional focusing question

        Returns:
            Dict with connections and synthesis
        """
        if not self.sources:
            return {"error": "No sources added"}

        if not HAS_ANTHROPIC or not self.api_key:
            return self._demo_synthesis()

        # Build the prompt
        sources_text = "\n\n---\n\n".join([
            f"SOURCE: {s.title} (Domain: {s.domain})\n{s.content}"
            for s in self.sources
        ])

        prompt = f"""You have been given {len(self.sources)} sources from different domains. Your task is to find NON-OBVIOUS connections between them.

SOURCES:
{sources_text}

{"FOCUSING QUESTION: " + question if question else ""}

INSTRUCTIONS:
1. Read all sources carefully
2. Look for unexpected parallels, shared structures, or transferable insights
3. Prioritize connections that:
   - Cross domain boundaries
   - Suggest something novel that neither source alone implies
   - Could lead to testable predictions

For each connection, provide:
- Which sources connect and how
- The insight (be specific)
- Novelty score (0-10): How unexpected is this?
- Whether it's testable, and if so, how

Find at least 3 connections. Be bold - surprising connections are more valuable than obvious ones.

Format your response as:
CONNECTION 1:
Sources: [list]
Insight: [specific insight]
Novelty: [0-10]
Testable: [yes/no]
Test: [if testable, how to test]

CONNECTION 2:
...etc"""

        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            temperature=0.7,  # Higher for creativity
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "sources": [s.title for s in self.sources],
            "domains": list(set(s.domain for s in self.sources)),
            "raw_synthesis": response.content[0].text,
            "question": question
        }

    def _demo_synthesis(self) -> Dict:
        """Demo without API."""
        return {
            "sources": [s.title for s in self.sources],
            "domains": list(set(s.domain for s in self.sources)),
            "raw_synthesis": "[API required for synthesis - this is a demo]",
            "demo": True
        }


def demo():
    """Demo the synthesis engine with sample sources."""
    engine = SynthesisEngine()

    # Add diverse sources
    engine.add_source(
        title="Ant Colony Optimization",
        content="""
        Ant colonies solve complex optimization problems through stigmergy -
        indirect communication via pheromone trails. When ants find food,
        they leave pheromones. More ants follow stronger trails, reinforcing
        them. This creates emergent intelligence without central control.
        Key properties: positive feedback, distributed processing, robustness.
        """,
        domain="biology/computing"
    )

    engine.add_source(
        title="Viral Marketing Dynamics",
        content="""
        Successful viral marketing follows power-law distributions.
        Content spreads through network effects - each share increases
        visibility exponentially. Key factors: emotional resonance,
        social proof, timing, and network structure. Most content dies
        quickly; rare items achieve massive spread through cascading shares.
        """,
        domain="marketing"
    )

    engine.add_source(
        title="Scientific Citation Networks",
        content="""
        Scientific papers form citation networks where seminal works
        accumulate disproportionate citations (Matthew effect).
        Breakthrough papers often connect previously disconnected fields.
        Citation half-life varies by discipline. Impact isn't just
        quality - it's also timing and network position.
        """,
        domain="scientometrics"
    )

    print("=== SYNTHESIS ENGINE DEMO ===")
    print(f"Sources: {len(engine.sources)}")
    print(f"Domains: {[s.domain for s in engine.sources]}")

    result = engine.synthesize(
        question="What do these systems tell us about how ideas spread and compound?"
    )

    print(f"\n=== SYNTHESIS ===")
    print(result.get("raw_synthesis", "No synthesis generated"))

    return result


if __name__ == "__main__":
    demo()
