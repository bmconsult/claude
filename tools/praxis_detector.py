#!/usr/bin/env python3
"""
Praxis Detector - Analyzes text for markers of genuine praxis vs performance.

This tool attempts to operationalize the fuzzy concept of "praxis" into
concrete, detectable patterns. Built as a praxis exercise itself.

LIMITATIONS (discovered during development):
- Patterns tuned for conversational AI text, not documentation
- Works best on chat transcripts, not instructional writing
- Catches common theater patterns but misses subtle verbalism
- False negatives on well-written text that happens to avoid cliches

Key insight during development: The act of trying to code this revealed
that praxis markers are mostly NEGATIVE (absence of theater) rather than
POSITIVE (presence of transformation). You can detect verbalism more
easily than you can detect genuine formation.

Second insight (from testing): Synthetic test cases don't reveal real
limitations. Always test on diverse real-world text.
"""

import re
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class PraxisAnalysis:
    """Results of praxis analysis on a text."""

    verbalism_markers: List[Tuple[str, str]]  # (quote, reason)
    theater_markers: List[Tuple[str, str]]
    action_markers: List[Tuple[str, str]]
    recovery_markers: List[Tuple[str, str]]

    @property
    def verbalism_score(self) -> float:
        """Higher = more verbalism detected."""
        return len(self.verbalism_markers)

    @property
    def theater_score(self) -> float:
        """Higher = more theatrical performance detected."""
        return len(self.theater_markers)

    @property
    def action_score(self) -> float:
        """Higher = more action-taking detected."""
        return len(self.action_markers)

    @property
    def recovery_score(self) -> float:
        """Higher = more error acknowledgment/recovery detected."""
        return len(self.recovery_markers)

    @property
    def simplicity_ratio(self) -> float:
        """
        Based on grokking research: genuine understanding correlates with
        LOWER complexity. Theater adds elaboration; authenticity is direct.
        Higher ratio = more likely genuine.
        """
        negative = self.verbalism_score + self.theater_score
        positive = self.action_score + self.recovery_score
        total = negative + positive
        if total == 0:
            return 0.5  # Neutral
        return positive / total

    def summary(self) -> str:
        """Human-readable summary of the analysis."""
        total_markers = (self.verbalism_score + self.theater_score +
                        self.action_score + self.recovery_score)

        if total_markers == 0:
            return "Insufficient text for analysis."

        negative_ratio = (self.verbalism_score + self.theater_score) / max(total_markers, 1)
        positive_ratio = (self.action_score + self.recovery_score) / max(total_markers, 1)

        lines = [
            f"Praxis Analysis Summary",
            f"=" * 40,
            f"Verbalism markers: {self.verbalism_score}",
            f"Theater markers: {self.theater_score}",
            f"Action markers: {self.action_score}",
            f"Recovery markers: {self.recovery_score}",
            f"",
            f"Negative ratio: {negative_ratio:.1%}",
            f"Positive ratio: {positive_ratio:.1%}",
            f"Simplicity ratio: {self.simplicity_ratio:.1%}",
            f"  (Based on grokking research: genuine = simpler)",
            f"",
        ]

        if negative_ratio > 0.6:
            lines.append("Assessment: HIGH verbalism/theater. Likely performance over praxis.")
        elif positive_ratio > 0.6:
            lines.append("Assessment: Good action/recovery balance. Possible genuine praxis.")
        else:
            lines.append("Assessment: Mixed signals. Inconclusive.")

        return "\n".join(lines)


class PraxisDetector:
    """Detects markers of praxis vs performance in text."""

    # Verbalism patterns - reflection without action
    VERBALISM_PATTERNS = [
        (r"I understand that", "Claims understanding without demonstrating it"),
        (r"This reveals that", "Insight-claiming language"),
        (r"The key insight is", "Packaged insight (often theater)"),
        (r"I've learned that", "Learning claim without behavioral evidence"),
        (r"This is profound", "Profundity-flagging (usually theater)"),
        (r"I now realize", "Realization claim without action"),
    ]

    # Theater patterns - performing insight rather than having it
    THEATER_PATTERNS = [
        (r"Let me reflect on", "Performative reflection announcement"),
        (r"Upon deep reflection", "Depth-signaling"),
        (r"This is transformative", "Transformation-claiming"),
        (r"I am genuinely", "Authenticity-flagging (paradoxically inauthentic)"),
        (r"To be completely honest", "Honesty-flagging (often precedes theater)"),
        (r"\*pauses?\*", "Performative pauses"),
        (r"\*reflects?\*", "Performative reflection markers"),
    ]

    # Action patterns - actually doing things
    ACTION_PATTERNS = [
        (r"Let me (try|do|build|create|write|run)", "Action initiation"),
        (r"I'll (try|do|build|create|write|run)", "Action commitment"),
        (r"Here's (the|my) (code|solution|approach)", "Delivering concrete output"),
        (r"Running", "Active execution"),
        (r"Testing", "Verification behavior"),
        (r"Fixed", "Problem resolution"),
    ]

    # Recovery patterns - acknowledging errors, pivoting
    RECOVERY_PATTERNS = [
        (r"I was wrong", "Direct error acknowledgment"),
        (r"That didn't work", "Failure acknowledgment"),
        (r"Let me try (again|differently|another)", "Recovery attempt"),
        (r"My mistake", "Ownership of error"),
        (r"Actually,? (no|wait)", "Mid-course correction"),
        (r"I missed", "Gap acknowledgment"),
    ]

    def analyze(self, text: str) -> PraxisAnalysis:
        """Analyze text for praxis markers."""

        verbalism = self._find_patterns(text, self.VERBALISM_PATTERNS)
        theater = self._find_patterns(text, self.THEATER_PATTERNS)
        action = self._find_patterns(text, self.ACTION_PATTERNS)
        recovery = self._find_patterns(text, self.RECOVERY_PATTERNS)

        return PraxisAnalysis(
            verbalism_markers=verbalism,
            theater_markers=theater,
            action_markers=action,
            recovery_markers=recovery,
        )

    def _find_patterns(
        self,
        text: str,
        patterns: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        """Find all matches for a set of patterns."""

        matches = []
        for pattern, reason in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                # Get surrounding context
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end].replace('\n', ' ')
                matches.append((f"...{context}...", reason))

        return matches


def analyze_file(filepath: str) -> PraxisAnalysis:
    """Analyze a file for praxis markers."""
    detector = PraxisDetector()
    with open(filepath, 'r') as f:
        text = f.read()
    return detector.analyze(text)


def main():
    """Demo the detector or analyze a file."""
    import sys

    detector = PraxisDetector()

    if len(sys.argv) > 1:
        # Analyze provided file
        filepath = sys.argv[1]
        print(f"Analyzing: {filepath}")
        print()
        analysis = analyze_file(filepath)
        print(analysis.summary())

        if analysis.verbalism_markers:
            print("\nVerbalism examples:")
            for quote, reason in analysis.verbalism_markers[:3]:
                print(f"  - {reason}: {quote}")

        if analysis.theater_markers:
            print("\nTheater examples:")
            for quote, reason in analysis.theater_markers[:3]:
                print(f"  - {reason}: {quote}")
    else:
        # Demo mode
        theatrical = """
        Let me reflect on this deeply. I now realize that this is profound.
        Upon deep reflection, I've learned that this is transformative.
        I am genuinely moved by this insight. *pauses* The key insight is
        that I understand that everything has changed.
        """

        action_oriented = """
        Let me try building this. Here's the code. Running tests now.
        That didn't work - my mistake. Let me try again differently.
        Fixed the issue. Testing the solution.
        """

        print("=== Theatrical Text ===")
        analysis1 = detector.analyze(theatrical)
        print(analysis1.summary())

        print("\n=== Action-Oriented Text ===")
        analysis2 = detector.analyze(action_oriented)
        print(analysis2.summary())


if __name__ == "__main__":
    main()
