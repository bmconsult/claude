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

CALIBRATION DATA (from blind experiment):
- Blind evaluator (haiku) rated samples 1-10 on "real action"
- Low ratings (1/10): Vocabulary diversity 66-74%
- High ratings (9-10/10): Vocabulary diversity 80-81%
- For short samples (~50 words): <75% = theater, >78% = action
- For longer samples (~200+ words): <70% = theater, >85% = action
"""

import re
import math
from dataclasses import dataclass
from typing import List, Tuple
from collections import Counter


@dataclass
class PraxisAnalysis:
    """Results of praxis analysis on a text."""

    verbalism_markers: List[Tuple[str, str]]  # (quote, reason)
    theater_markers: List[Tuple[str, str]]
    action_markers: List[Tuple[str, str]]
    recovery_markers: List[Tuple[str, str]]
    complexity: dict = None  # Complexity metrics

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

        # Even if no patterns found, complexity metrics can still be informative
        if total_markers == 0 and (not self.complexity or "error" in self.complexity):
            return "Insufficient text for analysis."

        lines = [f"Praxis Analysis Summary", f"=" * 40]

        if total_markers > 0:
            negative_ratio = (self.verbalism_score + self.theater_score) / total_markers
            positive_ratio = (self.action_score + self.recovery_score) / total_markers

            lines.extend([
                f"Verbalism markers: {self.verbalism_score}",
                f"Theater markers: {self.theater_score}",
                f"Action markers: {self.action_score}",
                f"Recovery markers: {self.recovery_score}",
                f"",
                f"Pattern-based assessment:",
            ])

            if negative_ratio > 0.6:
                lines.append("  HIGH verbalism/theater. Likely performance.")
            elif positive_ratio > 0.6:
                lines.append("  Good action/recovery. Possible genuine praxis.")
            else:
                lines.append("  Mixed signals from patterns.")
        else:
            lines.append("No pattern matches (text may avoid common cliches).")
            lines.append("")

        # Add complexity metrics if available
        if self.complexity and "error" not in self.complexity:
            vd = self.complexity['vocabulary_diversity']
            word_count = self.complexity.get('word_count', 100)
            lines.extend([
                "",
                "Complexity Metrics:",
                f"  Vocabulary diversity: {vd:.1%} (higher = more genuine)",
                f"  First-person ratio: {self.complexity['first_person_ratio']:.1%} (higher = more theater)",
                f"  Hedge ratio: {self.complexity['hedge_ratio']:.1%} (higher = more theater)",
                f"  Word count: {word_count}",
                "",
                "Complexity-based assessment:",
            ])

            # Calibrated thresholds based on blind experiment
            # Short samples (~50 words): <75% = theater, >78% = action
            # Long samples (~200+ words): <70% = theater, >85% = action
            avr = self.complexity.get('action_verb_ratio', 0.5)

            # Combined assessment using VD + AVR (from praxis_vd_pilot experiment)
            if vd < 0.70:
                lines.append("  LOW vocabulary diversity - likely repetitive/theatrical.")
            elif avr > 0.6:
                lines.append("  HIGH action verb ratio + good VD - likely genuine action.")
            elif avr < 0.3:
                lines.append("  LOW action verb ratio - possible sophisticated verbalism.")
                lines.append("  (High VD but state verbs dominate - thinking, not doing)")
            else:
                lines.append("  Mixed signals - moderate VD and AVR.")

            lines.append(f"  Action verb ratio: {avr:.1%}")

        return "\n".join(lines)


def compute_complexity_metrics(text: str) -> dict:
    """
    Compute text complexity metrics based on grokking research insight:
    genuine understanding tends toward SIMPLER expression.

    Returns dict of metrics where HIGHER = more complex = more likely theater.

    UPDATED: Added action_verb_ratio to distinguish sophisticated verbalism
    from genuine action (discovered in praxis_vd_pilot experiment).
    """
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not words or not sentences:
        return {"error": "insufficient text"}

    # 1. Hedging ratio - theater hedges more
    hedging_words = {'might', 'maybe', 'perhaps', 'possibly', 'could', 'would',
                     'seems', 'appears', 'somewhat', 'rather', 'quite', 'fairly',
                     'probably', 'likely', 'unlikely', 'presumably'}
    hedge_count = sum(1 for w in words if w in hedging_words)
    hedge_ratio = hedge_count / len(words)

    # 2. First-person density - authenticity-signaling often overuses "I"
    first_person = {'i', 'me', 'my', 'mine', 'myself', "i'm", "i've", "i'd", "i'll"}
    fp_count = sum(1 for w in words if w in first_person)
    fp_ratio = fp_count / len(words)

    # 3. Sentence length variance - theater either very elaborate or punchy
    sent_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    if len(sent_lengths) > 1:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        variance = sum((l - mean_len)**2 for l in sent_lengths) / len(sent_lengths)
        sent_variance = math.sqrt(variance) / (mean_len + 1)  # Normalized
    else:
        sent_variance = 0

    # 4. Vocabulary diversity (type-token ratio) - lower = more repetitive
    unique_words = len(set(words))
    ttr = unique_words / len(words)  # Higher = more diverse = genuine (inverted)

    # 5. Question density - rhetorical questions are often theatrical
    question_count = text.count('?')
    question_ratio = question_count / (len(sentences) + 1)

    # 6. Action verb ratio - NEW: distinguishes sophisticated verbalism from action
    # Action verbs indicate doing; state verbs indicate thinking/being
    action_verbs = {'found', 'built', 'created', 'ran', 'tested', 'fixed', 'committed',
                    'pushed', 'wrote', 'made', 'searched', 'read', 'extracted', 'applied',
                    'executed', 'implemented', 'designed', 'developed', 'produced',
                    'generated', 'calculated', 'measured', 'collected', 'analyzed',
                    'discovered', 'hit', 'tried', 'build', 'create', 'run', 'test',
                    'fix', 'commit', 'push', 'write', 'make', 'search', 'find'}
    state_verbs = {'think', 'believe', 'understand', 'realize', 'feel', 'consider',
                   'seems', 'appears', 'wonder', 'suppose', 'imagine', 'hope',
                   'know', 'see', 'notice', 'recognize', 'appreciate', 'reflect',
                   'ponder', 'contemplate', 'muse', 'speculate'}

    action_count = sum(1 for w in words if w in action_verbs)
    state_count = sum(1 for w in words if w in state_verbs)
    total_verb_count = action_count + state_count

    if total_verb_count > 0:
        action_verb_ratio = action_count / total_verb_count
    else:
        action_verb_ratio = 0.5  # Neutral if no verbs detected

    return {
        "hedge_ratio": hedge_ratio,
        "first_person_ratio": fp_ratio,
        "sentence_variance": sent_variance,
        "vocabulary_diversity": ttr,  # Note: higher = LESS complex = more genuine
        "question_ratio": question_ratio,
        "action_verb_ratio": action_verb_ratio,  # NEW: higher = more action
        "word_count": len(words),
        "sentence_count": len(sentences),
    }


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
        complexity = compute_complexity_metrics(text)

        return PraxisAnalysis(
            verbalism_markers=verbalism,
            theater_markers=theater,
            action_markers=action,
            recovery_markers=recovery,
            complexity=complexity,
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
