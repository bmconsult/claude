#!/usr/bin/env python3
"""
Automatic Gap Detector

Watches for patterns that indicate capability gaps:
1. Explicit failures (errors, wrong answers)
2. Confidence drops (hedging language, uncertainty)
3. Repeated attempts (trying same thing multiple ways)
4. Time sinks (spending disproportionate time on subtasks)
5. External dependencies (needing to look things up)

The goal: Turn implicit failures into explicit gap records
that can drive tool creation.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum

GAP_LOG = Path(__file__).parent / "detected_gaps.json"

class GapType(Enum):
    VERIFICATION = "verification"      # Claimed something false
    COMPUTATION = "computation"        # Math/logic error
    KNOWLEDGE = "knowledge"            # Didn't know something
    REASONING = "reasoning"            # Logical chain broke
    FRAMING = "framing"               # Wrong problem formulation
    CREATIVITY = "creativity"          # Stuck in local optimum
    INTEGRATION = "integration"        # Couldn't combine things
    META = "meta"                      # Failed to notice failure

@dataclass
class DetectedGap:
    timestamp: str
    gap_type: str
    description: str
    evidence: str
    severity: str  # low, medium, high, critical
    suggested_tool: Optional[str]
    context: Optional[str]
    resolved: bool = False
    resolution: Optional[str] = None

class GapDetector:
    """Analyzes text/behavior for capability gaps."""

    # Patterns that indicate uncertainty/hedging
    HEDGE_PATTERNS = [
        r"\bI think\b", r"\bprobably\b", r"\bmaybe\b", r"\bmight\b",
        r"\bnot sure\b", r"\buncertain\b", r"\bpossibly\b",
        r"\bI believe\b", r"\bseems like\b", r"\bcould be\b"
    ]

    # Patterns that indicate struggle
    STRUGGLE_PATTERNS = [
        r"\blet me try\b", r"\bactually\b", r"\bwait\b", r"\bhmm\b",
        r"\bon second thought\b", r"\bthat's not right\b",
        r"\bI was wrong\b", r"\blet me reconsider\b"
    ]

    # Patterns that indicate external dependency
    DEPENDENCY_PATTERNS = [
        r"\bneed to look up\b", r"\bdon't have access\b",
        r"\bcan't verify\b", r"\bwould need to check\b",
        r"\bI don't know\b", r"\bbeyond my\b"
    ]

    def __init__(self):
        self.gaps: List[DetectedGap] = []
        self._load_existing()

    def _load_existing(self):
        """Load previously detected gaps."""
        if GAP_LOG.exists():
            try:
                data = json.loads(GAP_LOG.read_text())
                self.gaps = [DetectedGap(**g) for g in data]
            except:
                self.gaps = []

    def _save(self):
        """Persist gaps to file."""
        GAP_LOG.write_text(json.dumps([asdict(g) for g in self.gaps], indent=2))

    def analyze_text(self, text: str, context: str = "") -> List[DetectedGap]:
        """Analyze text for signs of capability gaps."""
        detected = []

        # Count hedge patterns
        hedge_count = sum(len(re.findall(p, text, re.I)) for p in self.HEDGE_PATTERNS)
        if hedge_count > 5:
            detected.append(DetectedGap(
                timestamp=datetime.now().isoformat(),
                gap_type=GapType.REASONING.value,
                description="High uncertainty in response",
                evidence=f"Found {hedge_count} hedging phrases",
                severity="medium",
                suggested_tool="confidence_calibrator",
                context=context
            ))

        # Count struggle patterns
        struggle_count = sum(len(re.findall(p, text, re.I)) for p in self.STRUGGLE_PATTERNS)
        if struggle_count > 3:
            detected.append(DetectedGap(
                timestamp=datetime.now().isoformat(),
                gap_type=GapType.REASONING.value,
                description="Multiple course corrections during reasoning",
                evidence=f"Found {struggle_count} struggle indicators",
                severity="medium",
                suggested_tool="structured_reasoning",
                context=context
            ))

        # Check for dependency patterns
        dependency_count = sum(len(re.findall(p, text, re.I)) for p in self.DEPENDENCY_PATTERNS)
        if dependency_count > 0:
            detected.append(DetectedGap(
                timestamp=datetime.now().isoformat(),
                gap_type=GapType.KNOWLEDGE.value,
                description="External knowledge dependency",
                evidence=f"Found {dependency_count} dependency indicators",
                severity="low",
                suggested_tool="knowledge_retriever",
                context=context
            ))

        return detected

    def record_explicit_failure(
        self,
        description: str,
        gap_type: GapType,
        evidence: str,
        severity: str = "medium",
        suggested_tool: Optional[str] = None,
        context: str = ""
    ):
        """Record an explicitly observed failure."""
        gap = DetectedGap(
            timestamp=datetime.now().isoformat(),
            gap_type=gap_type.value,
            description=description,
            evidence=evidence,
            severity=severity,
            suggested_tool=suggested_tool,
            context=context
        )
        self.gaps.append(gap)
        self._save()
        return gap

    def record_verification_failure(
        self,
        claimed: str,
        actual: str,
        context: str = ""
    ):
        """Specifically record when verification failed."""
        return self.record_explicit_failure(
            description="Claimed something was true that wasn't",
            gap_type=GapType.VERIFICATION,
            evidence=f"Claimed: {claimed}\nActual: {actual}",
            severity="high",
            suggested_tool="verification_engine",
            context=context
        )

    def record_framing_failure(
        self,
        original_framing: str,
        better_framing: str,
        context: str = ""
    ):
        """Record when problem framing was wrong."""
        return self.record_explicit_failure(
            description="Initial problem framing was suboptimal",
            gap_type=GapType.FRAMING,
            evidence=f"Original: {original_framing}\nBetter: {better_framing}",
            severity="medium",
            suggested_tool="problem_reframer",
            context=context
        )

    def get_unresolved(self) -> List[DetectedGap]:
        """Get gaps that haven't been resolved."""
        return [g for g in self.gaps if not g.resolved]

    def get_by_type(self, gap_type: GapType) -> List[DetectedGap]:
        """Get gaps of a specific type."""
        return [g for g in self.gaps if g.gap_type == gap_type.value]

    def get_suggested_tools(self) -> dict:
        """Get frequency of suggested tools from unresolved gaps."""
        suggestions = {}
        for gap in self.get_unresolved():
            if gap.suggested_tool:
                suggestions[gap.suggested_tool] = suggestions.get(gap.suggested_tool, 0) + 1
        return dict(sorted(suggestions.items(), key=lambda x: -x[1]))

    def mark_resolved(self, gap_index: int, resolution: str):
        """Mark a gap as resolved."""
        if 0 <= gap_index < len(self.gaps):
            self.gaps[gap_index].resolved = True
            self.gaps[gap_index].resolution = resolution
            self._save()

    def summary(self) -> str:
        """Generate summary of detected gaps."""
        unresolved = self.get_unresolved()
        by_type = {}
        by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for gap in unresolved:
            by_type[gap.gap_type] = by_type.get(gap.gap_type, 0) + 1
            by_severity[gap.severity] = by_severity.get(gap.severity, 0) + 1

        lines = [
            f"=== GAP DETECTOR SUMMARY ===",
            f"Total gaps: {len(self.gaps)}",
            f"Unresolved: {len(unresolved)}",
            "",
            "By type:",
        ]
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            lines.append(f"  {t}: {c}")

        lines.extend(["", "By severity:"])
        for s in ["critical", "high", "medium", "low"]:
            if by_severity[s] > 0:
                lines.append(f"  {s}: {by_severity[s]}")

        suggested = self.get_suggested_tools()
        if suggested:
            lines.extend(["", "Suggested tools to build:"])
            for tool, count in list(suggested.items())[:5]:
                lines.append(f"  {tool}: {count} gaps")

        return "\n".join(lines)


def test_detector():
    """Test the gap detector."""
    detector = GapDetector()

    # Test text analysis
    uncertain_text = """
    I think this might work, but I'm not sure. It probably could be
    the answer, though I believe there may be other possibilities.
    Let me try another approach... actually, wait, that's not right.
    On second thought, I need to look up the exact formula.
    """

    gaps = detector.analyze_text(uncertain_text, "test context")
    print(f"Detected {len(gaps)} gaps from text analysis:")
    for g in gaps:
        print(f"  - {g.gap_type}: {g.description}")

    # Test explicit recording
    detector.record_verification_failure(
        claimed="Solution (2,4,5,1,3) is valid",
        actual="Has 2 diagonal attacks - invalid",
        context="5-Queens with constraints"
    )

    print("\n" + detector.summary())


if __name__ == "__main__":
    test_detector()
