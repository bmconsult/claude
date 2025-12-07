#!/usr/bin/env python3
"""
Improvement Loop - The Core of Exponential Self-Improvement

This is the meta-system that orchestrates:
1. Gap detection → Finding what's missing
2. Tool generation → Creating what's needed
3. Integration → Making tools available
4. Performance tracking → Measuring effectiveness
5. Refinement → Improving based on results

The key insight: Each iteration should be FASTER than the last.
That's what makes it exponential.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from enum import Enum

# Import our components
from gap_detector import GapDetector, GapType, DetectedGap
from tool_generator import ToolGenerator, GeneratedTool

LOOP_LOG = Path(__file__).parent / "improvement_loop_log.json"
METRICS_LOG = Path(__file__).parent / "improvement_metrics.json"


class LoopPhase(Enum):
    DETECT = "detect"
    GENERATE = "generate"
    INTEGRATE = "integrate"
    TEST = "test"
    REFINE = "refine"


@dataclass
class LoopIteration:
    iteration: int
    started_at: str
    completed_at: Optional[str]
    phase: str
    gaps_found: int
    tools_generated: int
    tools_successful: int
    time_seconds: float
    notes: str


@dataclass
class ToolPerformance:
    tool_name: str
    uses: int
    successes: int
    failures: int
    avg_time_ms: float
    last_used: str


class ImprovementLoop:
    """
    The recursive self-improvement engine.

    Core loop:
    1. Attempt something
    2. Detect gaps (automatically or from explicit failure)
    3. Generate tools for high-priority gaps
    4. Integrate tools into the system
    5. Test effectiveness
    6. Refine or iterate

    Key metric: Time per capability improvement should DECREASE.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.gap_detector = GapDetector()
        self.tool_generator = ToolGenerator(api_key)
        self.iterations: List[LoopIteration] = []
        self.tool_performance: Dict[str, ToolPerformance] = {}
        self._load_state()

    def _load_state(self):
        """Load previous state."""
        if LOOP_LOG.exists():
            try:
                data = json.loads(LOOP_LOG.read_text())
                self.iterations = [LoopIteration(**i) for i in data.get("iterations", [])]
            except:
                pass

        if METRICS_LOG.exists():
            try:
                data = json.loads(METRICS_LOG.read_text())
                self.tool_performance = {
                    k: ToolPerformance(**v) for k, v in data.items()
                }
            except:
                pass

    def _save_state(self):
        """Persist state."""
        LOOP_LOG.write_text(json.dumps({
            "iterations": [asdict(i) for i in self.iterations],
            "last_updated": datetime.now().isoformat()
        }, indent=2))

        METRICS_LOG.write_text(json.dumps({
            k: asdict(v) for k, v in self.tool_performance.items()
        }, indent=2))

    def record_tool_use(self, tool_name: str, success: bool, time_ms: float):
        """Record a tool use for performance tracking."""
        if tool_name not in self.tool_performance:
            self.tool_performance[tool_name] = ToolPerformance(
                tool_name=tool_name,
                uses=0,
                successes=0,
                failures=0,
                avg_time_ms=0,
                last_used=""
            )

        perf = self.tool_performance[tool_name]
        perf.uses += 1
        if success:
            perf.successes += 1
        else:
            perf.failures += 1
        # Running average
        perf.avg_time_ms = (perf.avg_time_ms * (perf.uses - 1) + time_ms) / perf.uses
        perf.last_used = datetime.now().isoformat()

        self._save_state()

    def run_iteration(self, context: str = "") -> LoopIteration:
        """
        Run one improvement iteration.

        1. Check for unresolved gaps
        2. Prioritize by severity and frequency
        3. Generate tools for top gaps
        4. Validate and integrate
        """
        start_time = time.time()
        iteration_num = len(self.iterations) + 1

        print(f"\n{'='*60}")
        print(f"IMPROVEMENT LOOP - ITERATION {iteration_num}")
        print(f"{'='*60}\n")

        # Phase 1: Detect
        print("Phase 1: DETECT")
        print("-" * 40)

        # Analyze any provided context for implicit gaps
        if context:
            implicit_gaps = self.gap_detector.analyze_text(context)
            print(f"  Found {len(implicit_gaps)} implicit gaps from context")
            for gap in implicit_gaps:
                self.gap_detector.gaps.append(gap)
            self.gap_detector._save()

        unresolved = self.gap_detector.get_unresolved()
        print(f"  Total unresolved gaps: {len(unresolved)}")

        if not unresolved:
            print("  No gaps to address. System is either perfect or undertested.")
            elapsed = time.time() - start_time
            iteration = LoopIteration(
                iteration=iteration_num,
                started_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat(),
                phase="detect",
                gaps_found=0,
                tools_generated=0,
                tools_successful=0,
                time_seconds=elapsed,
                notes="No unresolved gaps"
            )
            self.iterations.append(iteration)
            self._save_state()
            return iteration

        # Prioritize gaps
        priority_gaps = sorted(
            unresolved,
            key=lambda g: (
                {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(g.severity, 0),
                g.timestamp
            ),
            reverse=True
        )[:3]  # Top 3

        print(f"  Prioritized {len(priority_gaps)} gaps for this iteration:")
        for i, gap in enumerate(priority_gaps, 1):
            print(f"    {i}. [{gap.severity}] {gap.gap_type}: {gap.description}")

        # Phase 2: Generate
        print("\nPhase 2: GENERATE")
        print("-" * 40)

        tools_generated = 0
        tools_successful = 0

        for gap in priority_gaps:
            print(f"\n  Generating tool for: {gap.description}")

            try:
                tool = self.tool_generator.generate_and_save(
                    gap_type=gap.gap_type,
                    description=gap.description,
                    evidence=gap.evidence,
                    suggested_name=gap.suggested_tool
                )

                tools_generated += 1
                if tool.validated:
                    tools_successful += 1
                    print(f"    ✓ Generated and validated: {tool.name}")

                    # Mark gap as resolved
                    gap_idx = self.gap_detector.gaps.index(gap)
                    self.gap_detector.mark_resolved(gap_idx, f"Tool generated: {tool.name}")
                else:
                    print(f"    ✗ Generated but failed validation")

            except Exception as e:
                print(f"    ✗ Generation failed: {e}")

        # Phase 3: Summary
        print("\nPhase 3: SUMMARY")
        print("-" * 40)

        elapsed = time.time() - start_time
        print(f"  Time: {elapsed:.1f}s")
        print(f"  Gaps addressed: {len(priority_gaps)}")
        print(f"  Tools generated: {tools_generated}")
        print(f"  Tools validated: {tools_successful}")

        # Calculate improvement rate
        if self.iterations:
            prev_times = [i.time_seconds for i in self.iterations[-5:]]
            avg_prev = sum(prev_times) / len(prev_times)
            improvement = (avg_prev - elapsed) / avg_prev * 100 if avg_prev > 0 else 0
            print(f"  Speed vs avg of last 5: {improvement:+.1f}%")

        iteration = LoopIteration(
            iteration=iteration_num,
            started_at=datetime.now().isoformat(),
            completed_at=datetime.now().isoformat(),
            phase="complete",
            gaps_found=len(unresolved),
            tools_generated=tools_generated,
            tools_successful=tools_successful,
            time_seconds=elapsed,
            notes=f"Addressed {len(priority_gaps)} priority gaps"
        )

        self.iterations.append(iteration)
        self._save_state()

        return iteration

    def analyze_improvement_rate(self) -> Dict[str, Any]:
        """
        Analyze whether improvement is actually exponential.

        Key metrics:
        - Time per iteration (should decrease)
        - Tools per iteration (should increase or stay stable)
        - Success rate (should increase)
        - Gap discovery rate (should stay healthy - finding new gaps is good)
        """
        if len(self.iterations) < 2:
            return {"status": "insufficient_data", "iterations": len(self.iterations)}

        times = [i.time_seconds for i in self.iterations]
        tools = [i.tools_generated for i in self.iterations]
        successes = [i.tools_successful for i in self.iterations]

        # Calculate trends
        def trend(values):
            if len(values) < 2:
                return 0
            first_half = sum(values[:len(values)//2]) / (len(values)//2)
            second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
            if first_half == 0:
                return 0
            return (second_half - first_half) / first_half * 100

        time_trend = trend(times)
        tools_trend = trend(tools)

        success_rates = [s/t if t > 0 else 0 for s, t in zip(successes, tools)]
        success_trend = trend(success_rates) if success_rates else 0

        is_exponential = time_trend < 0 and tools_trend >= 0

        return {
            "status": "exponential" if is_exponential else "linear_or_worse",
            "iterations": len(self.iterations),
            "time_trend_pct": time_trend,  # Negative is good
            "tools_trend_pct": tools_trend,  # Positive is good
            "success_trend_pct": success_trend,  # Positive is good
            "avg_time_seconds": sum(times) / len(times),
            "total_tools_generated": sum(tools),
            "total_tools_successful": sum(successes),
            "interpretation": (
                "EXPONENTIAL: Getting faster while maintaining output" if is_exponential
                else "LINEAR: Not yet achieving compounding improvement"
            )
        }

    def status(self) -> str:
        """Get current status of the improvement loop."""
        lines = [
            "=== IMPROVEMENT LOOP STATUS ===",
            f"Iterations completed: {len(self.iterations)}",
            f"Unresolved gaps: {len(self.gap_detector.get_unresolved())}",
            f"Tools tracked: {len(self.tool_performance)}",
            ""
        ]

        if self.iterations:
            last = self.iterations[-1]
            lines.extend([
                f"Last iteration:",
                f"  Time: {last.time_seconds:.1f}s",
                f"  Gaps found: {last.gaps_found}",
                f"  Tools generated: {last.tools_generated}",
                f"  Tools successful: {last.tools_successful}",
                ""
            ])

        analysis = self.analyze_improvement_rate()
        lines.extend([
            "Improvement analysis:",
            f"  Status: {analysis.get('status', 'unknown')}",
            f"  Time trend: {analysis.get('time_trend_pct', 0):+.1f}%",
            f"  Tools trend: {analysis.get('tools_trend_pct', 0):+.1f}%",
        ])

        if "interpretation" in analysis:
            lines.append(f"  → {analysis['interpretation']}")

        return "\n".join(lines)


def demo():
    """Demo the improvement loop."""
    loop = ImprovementLoop()

    print("Current status:")
    print(loop.status())

    print("\n" + "="*60)
    print("To run an iteration, call: loop.run_iteration()")
    print("To add a gap manually:")
    print("  loop.gap_detector.record_verification_failure(claimed, actual)")
    print("  loop.gap_detector.record_framing_failure(original, better)")


if __name__ == "__main__":
    demo()
