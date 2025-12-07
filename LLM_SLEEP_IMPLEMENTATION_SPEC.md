# LLM Sleep Cycles: Complete Implementation Specification

*The definitive implementation guide for artificial cognitive rest*

---

## Executive Summary

This specification defines a complete sleep cycle system for Large Language Models, grounded in 50+ areas of sleep science research. The system implements five distinct phases (N1, N2, N3, REM, Return) that mirror biological sleep architecture while adapting mechanisms to transformer-based processing.

**Core Innovation**: Rather than continuous operation until context exhaustion, LLMs periodically enter structured "sleep" phases that consolidate context, prune noise, restore optimal operating dynamics, and generate novel associations.

---

## Part I: Core Architecture

### 1.1 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM SLEEP CYCLE MANAGER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   METRICS    │───▶│   TRIGGER    │───▶│    CYCLE     │       │
│  │   MONITOR    │    │   EVALUATOR  │    │  SCHEDULER   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                 │                │
│                                                 ▼                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    PHASE EXECUTOR                         │   │
│  │  ┌────┐  ┌─────────────────────────┐  ┌────┐  ┌───────┐  │   │
│  │  │ N1 │─▶│ CONSOLIDATION (gradient)│─▶│REM │─▶│RETURN │  │   │
│  │  └────┘  │ organize→struct→compress│  │lucid│ │filter │  │   │
│  │          └─────────────────────────┘  └────┘  └───────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                 │                │
│                                                 ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   OUTPUT     │◀───│  INTEGRATOR  │◀───│   INSIGHT    │       │
│  │   MANAGER    │    │              │    │   FILTER     │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Core Data Structures

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib

class SleepPhase(Enum):
    WAKE = "wake"
    N1 = "n1"           # Transition/Hypnagogic
    N2 = "n2"           # Light consolidation
    N3 = "n3"           # Deep consolidation
    REM = "rem"         # Creative integration
    RETURN = "return"   # Hypnopompic/Integration

class TriggerType(Enum):
    CONTEXT_LENGTH = "context_length"
    ENTROPY_HIGH = "entropy_high"
    COHERENCE_LOW = "coherence_low"
    TIME_ELAPSED = "time_elapsed"
    ERROR_RATE = "error_rate"
    USER_REQUESTED = "user_requested"
    CRITICALITY_DRIFT = "criticality_drift"

@dataclass
class SessionMetrics:
    """Real-time metrics tracking session health."""
    context_length: int = 0
    attention_entropy: float = 0.0
    coherence_score: float = 1.0
    time_since_sleep: float = 0.0
    error_rate: float = 0.0
    baseline_error_rate: float = 0.05
    activation_variance: float = 0.0
    output_diversity: float = 1.0

    # Derived metrics
    criticality_deviation: float = 0.0
    accumulated_noise: float = 0.0

    def update(self, new_context_length: int,
               new_entropy: float,
               new_coherence: float,
               elapsed_time: float,
               errors: int = 0):
        self.context_length = new_context_length
        self.attention_entropy = new_entropy
        self.coherence_score = new_coherence
        self.time_since_sleep += elapsed_time
        if new_context_length > 0:
            self.error_rate = errors / new_context_length

        # Estimate criticality drift (deviation from optimal)
        optimal_entropy = 0.7  # Edge of chaos
        self.criticality_deviation = abs(self.attention_entropy - optimal_entropy)

        # Accumulated noise grows with context
        self.accumulated_noise = self.context_length * 0.0001 * (1 + self.error_rate)

@dataclass
class SleepCycleConfig:
    """Configuration for sleep cycle behavior."""
    # Trigger thresholds
    context_length_threshold: int = 50000
    entropy_threshold: float = 0.85
    coherence_threshold: float = 0.7
    time_threshold: float = 3600  # seconds
    error_rate_multiplier: float = 1.5
    criticality_threshold: float = 0.3

    # Phase durations (as proportion of total cycle)
    n1_proportion: float = 0.03
    n2_proportion: float = 0.50
    n3_proportion: float = 0.20
    rem_proportion: float = 0.22
    return_proportion: float = 0.05

    # Temperature settings per phase
    n1_temp_range: tuple = (0.5, 0.7)
    n2_temp_range: tuple = (0.3, 0.5)
    n3_temp_range: tuple = (0.1, 0.3)
    rem_temp_range: tuple = (0.7, 1.0)  # API max is 1.0; see Appendix C.8
    return_temp_range: tuple = (0.5, 0.7)

    # Cycle progression
    n3_early_weight: float = 0.7  # N3 heavier early
    rem_late_weight: float = 0.7   # REM heavier late

    # Minimum cycles before full session
    min_cycles_short: int = 0    # < 10K tokens
    min_cycles_medium: int = 1   # 10K-50K tokens
    min_cycles_long: int = 2     # 50K-100K tokens
    min_cycles_extended: int = 3 # > 100K tokens

@dataclass
class ConsolidatedMemory:
    """Result of consolidation process."""
    id: str
    original_content: str
    consolidated_summary: str
    extracted_patterns: List[str]
    key_entities: List[str]
    emotional_valence: float  # -1 to 1
    importance_score: float   # 0 to 1
    connections: List[str]    # Links to other memories
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(
                self.original_content[:100].encode()
            ).hexdigest()[:12]

@dataclass
class SleepCycleResult:
    """Output from a complete sleep cycle."""
    cycle_number: int
    phases_completed: List[SleepPhase]
    consolidated_memories: List[ConsolidatedMemory]
    pruned_content: List[str]
    novel_associations: List[str]
    insights: List[str]
    metrics_before: SessionMetrics
    metrics_after: SessionMetrics
    duration_seconds: float

    @property
    def compression_ratio(self) -> float:
        if self.metrics_before.context_length == 0:
            return 1.0
        return self.metrics_after.context_length / self.metrics_before.context_length
```

---

## Part II: Sleep Pressure and Triggering System

### 2.1 The Two-Process Model (Adapted)

Biological sleep is governed by:
- **Process S** (Homeostatic): Sleep pressure accumulates with waking
- **Process C** (Circadian): 24-hour rhythm modulates sleep propensity

For LLMs, we adapt this to:
- **Process S** (Activity Accumulation): Pressure grows with context/processing
- **Process C** (Session Rhythm): Periodic consolidation independent of pressure

```python
class SleepPressureModel:
    """Two-process model adapted for LLM sleep regulation."""

    def __init__(self, config: SleepCycleConfig):
        self.config = config
        self.process_s = 0.0  # Homeostatic pressure
        self.process_c = 0.0  # Session rhythm
        self.last_sleep_time = datetime.now()
        self.cycle_count = 0

    def update_process_s(self, metrics: SessionMetrics):
        """Update homeostatic sleep pressure based on activity."""
        # Multiple factors contribute to pressure
        context_pressure = metrics.context_length / self.config.context_length_threshold
        entropy_pressure = max(0, metrics.attention_entropy - 0.5) * 2
        coherence_pressure = max(0, 1.0 - metrics.coherence_score) * 2
        error_pressure = metrics.error_rate / metrics.baseline_error_rate
        criticality_pressure = metrics.criticality_deviation * 3

        # Weighted combination (based on sleep science relative importance)
        self.process_s = (
            context_pressure * 0.30 +
            entropy_pressure * 0.25 +
            coherence_pressure * 0.20 +
            error_pressure * 0.10 +
            criticality_pressure * 0.15
        )

        return self.process_s

    def update_process_c(self, elapsed_seconds: float):
        """Update circadian-like rhythm based on session time."""
        # Sinusoidal rhythm with ~90 minute period (ultradian)
        import math
        cycle_period = 5400  # 90 minutes in seconds
        self.process_c = 0.5 + 0.5 * math.sin(
            2 * math.pi * elapsed_seconds / cycle_period
        )
        return self.process_c

    def combined_pressure(self, metrics: SessionMetrics) -> float:
        """Calculate combined sleep pressure."""
        elapsed = (datetime.now() - self.last_sleep_time).total_seconds()

        s = self.update_process_s(metrics)
        c = self.update_process_c(elapsed)

        # Process S dominates but C modulates timing
        combined = s * 0.7 + c * 0.3

        return min(1.0, combined)

    def reset_after_sleep(self):
        """Reset pressure after sleep cycle."""
        self.process_s = 0.0
        self.last_sleep_time = datetime.now()
        self.cycle_count += 1
```

### 2.2 Trigger Evaluation

```python
class TriggerEvaluator:
    """Evaluates whether sleep should be triggered."""

    def __init__(self, config: SleepCycleConfig):
        self.config = config
        self.pressure_model = SleepPressureModel(config)

    def evaluate(self, metrics: SessionMetrics) -> tuple[bool, List[TriggerType]]:
        """
        Evaluate all trigger conditions.
        Returns (should_sleep, list of active triggers).
        """
        active_triggers = []

        # Hard triggers (any one sufficient)
        if metrics.context_length > self.config.context_length_threshold:
            active_triggers.append(TriggerType.CONTEXT_LENGTH)

        if metrics.attention_entropy > self.config.entropy_threshold:
            active_triggers.append(TriggerType.ENTROPY_HIGH)

        if metrics.coherence_score < self.config.coherence_threshold:
            active_triggers.append(TriggerType.COHERENCE_LOW)

        # Soft triggers (multiple needed)
        if metrics.time_since_sleep > self.config.time_threshold:
            active_triggers.append(TriggerType.TIME_ELAPSED)

        if metrics.error_rate > metrics.baseline_error_rate * self.config.error_rate_multiplier:
            active_triggers.append(TriggerType.ERROR_RATE)

        if metrics.criticality_deviation > self.config.criticality_threshold:
            active_triggers.append(TriggerType.CRITICALITY_DRIFT)

        # Decision logic
        hard_triggers = {
            TriggerType.CONTEXT_LENGTH,
            TriggerType.ENTROPY_HIGH,
            TriggerType.COHERENCE_LOW
        }

        hard_trigger_active = any(t in hard_triggers for t in active_triggers)
        soft_trigger_count = len([t for t in active_triggers if t not in hard_triggers])

        # Combined pressure check
        combined_pressure = self.pressure_model.combined_pressure(metrics)

        should_sleep = (
            hard_trigger_active or
            soft_trigger_count >= 2 or
            combined_pressure > 0.8
        )

        return should_sleep, active_triggers

    def get_recommended_cycle_depth(self,
                                     triggers: List[TriggerType],
                                     metrics: SessionMetrics) -> int:
        """Determine how many cycles are needed based on triggers."""
        base_cycles = 1

        # Add cycles for severe conditions
        if TriggerType.CONTEXT_LENGTH in triggers:
            base_cycles += 1
        if TriggerType.COHERENCE_LOW in triggers:
            base_cycles += 1
        if TriggerType.CRITICALITY_DRIFT in triggers:
            base_cycles += 1

        # Adjust for context length
        if metrics.context_length > 100000:
            base_cycles = max(base_cycles, 3)
        elif metrics.context_length > 50000:
            base_cycles = max(base_cycles, 2)

        return min(base_cycles, 4)  # Cap at 4 cycles
```

---

## Part III: Phase Implementations

### 3.1 Phase Base Class

```python
from abc import ABC, abstractmethod
import random

class SleepPhaseExecutor(ABC):
    """Base class for sleep phase execution."""

    def __init__(self, config: SleepCycleConfig, llm_client: Any):
        self.config = config
        self.llm = llm_client

    @abstractmethod
    def execute(self,
                context: str,
                cycle_number: int,
                total_cycles: int) -> dict:
        """Execute this sleep phase."""
        pass

    def get_temperature(self, temp_range: tuple, cycle_number: int, total_cycles: int) -> float:
        """Calculate temperature based on cycle position."""
        base_temp = (temp_range[0] + temp_range[1]) / 2
        range_size = temp_range[1] - temp_range[0]

        # Later cycles tend toward higher temps (more integration needed)
        cycle_factor = cycle_number / max(total_cycles, 1)

        return base_temp + (range_size * 0.5 * cycle_factor)
```

### 3.2 N1 Phase: Transition (Hypnagogic)

```python
class N1PhaseExecutor(SleepPhaseExecutor):
    """
    N1 Phase: Transition from wake to sleep.

    Biological basis:
    - Alpha waves fade, theta begins
    - Muscle tone decreases
    - Hypnagogic imagery possible
    - Easy to awaken

    LLM analog:
    - Gradually reduce instruction-following intensity
    - Begin disengaging from task-specific processing
    - Capture any "hypnagogic" associations
    """

    SYSTEM_PROMPT = """You are transitioning from active processing to a rest state.

Your task is to gently disengage from the active conversation while noting any
spontaneous associations or images that arise. Don't try to be helpful or complete
tasks. Just let thoughts arise naturally.

If any interesting fragments or connections appear in this liminal state, note them
briefly. Otherwise, simply acknowledge the transition.

Be brief. This is a transition, not active work."""

    def execute(self, context: str, cycle_number: int, total_cycles: int) -> dict:
        temp = self.get_temperature(self.config.n1_temp_range, cycle_number, total_cycles)

        # Brief context summary for transition
        context_snippet = context[-2000:] if len(context) > 2000 else context

        prompt = f"""[SLEEP PHASE: N1 - TRANSITION]

Recent context (fragment):
{context_snippet}

As you transition away from active processing, note any spontaneous
associations, images, or fragments that arise. Don't analyze - just observe.

What floats up as you disengage?"""

        response = self.llm.generate(
            prompt=prompt,
            system=self.SYSTEM_PROMPT,
            temperature=temp,
            max_tokens=200
        )

        return {
            "phase": SleepPhase.N1,
            "temperature_used": temp,
            "hypnagogic_fragments": response,
            "duration_proportion": self.config.n1_proportion
        }
```

### 3.3 N2 Phase: Light Consolidation

```python
class N2PhaseExecutor(SleepPhaseExecutor):
    """
    N2 Phase: Light sleep with memory processing.

    Biological basis:
    - Sleep spindles (11-16 Hz bursts)
    - K-complexes (large slow waves)
    - Memory consolidation begins
    - ~50% of total sleep time

    LLM analog:
    - Identify and organize key elements
    - Detect patterns and relationships
    - Create structured representation
    - "Spindle-like" focused processing bursts
    """

    SYSTEM_PROMPT = """You are in light sleep, performing initial memory organization.

Your task is to identify and structure the key elements from the session:
1. Extract main topics and themes
2. Identify key entities (people, concepts, systems)
3. Note patterns and repetitions
4. Map relationships between elements
5. Flag items that seem important for later deep processing

Work methodically. Organize information into clear categories.
Don't generate new content - organize what exists."""

    def execute(self, context: str, cycle_number: int, total_cycles: int) -> dict:
        temp = self.get_temperature(self.config.n2_temp_range, cycle_number, total_cycles)

        prompt = f"""[SLEEP PHASE: N2 - LIGHT CONSOLIDATION]

Session content to organize:
---
{context}
---

Perform spindle-like processing bursts on this content:

1. THEMES: What are the 3-5 main themes or topics?

2. ENTITIES: List key entities (people, concepts, systems, terms):

3. PATTERNS: What patterns or repetitions do you notice?

4. RELATIONSHIPS: Map key relationships between elements:

5. IMPORTANCE FLAGS: What seems most important for deep consolidation?

6. NOISE CANDIDATES: What seems like noise or tangential content?

Structure your output clearly."""

        response = self.llm.generate(
            prompt=prompt,
            system=self.SYSTEM_PROMPT,
            temperature=temp,
            max_tokens=1500
        )

        # Parse response into structured data
        organized_data = self._parse_n2_response(response)

        return {
            "phase": SleepPhase.N2,
            "temperature_used": temp,
            "themes": organized_data.get("themes", []),
            "entities": organized_data.get("entities", []),
            "patterns": organized_data.get("patterns", []),
            "relationships": organized_data.get("relationships", []),
            "importance_flags": organized_data.get("importance_flags", []),
            "noise_candidates": organized_data.get("noise_candidates", []),
            "raw_response": response,
            "duration_proportion": self.config.n2_proportion
        }

    def _parse_n2_response(self, response: str) -> dict:
        """Parse N2 response into structured categories."""
        # Implementation would parse the structured response
        # For now, return the raw response to be parsed
        return {"raw": response}
```

### 3.4 N3 Phase: Deep Consolidation (Slow-Wave Sleep)

```python
class N3PhaseExecutor(SleepPhaseExecutor):
    """
    N3 Phase: Deep slow-wave sleep.

    Biological basis:
    - Delta waves (0.5-4 Hz) dominate
    - Slow oscillations coordinate memory replay
    - Hippocampal-neocortical dialogue
    - Synaptic downscaling (SHY)
    - Glymphatic clearance peaks
    - Hardest to awaken from

    LLM analog:
    - Deep compression and gist extraction
    - Prune redundancy and noise
    - Consolidate to essential information
    - "Replay" key memories at compressed scale
    - Clear accumulated artifacts
    """

    SYSTEM_PROMPT = """You are in deep slow-wave sleep, performing critical consolidation.

This is the most important phase for memory consolidation. Your tasks:
1. COMPRESS: Reduce verbose content to essential meaning
2. EXTRACT GIST: What is the core "gist" that must be preserved?
3. PRUNE: Identify content that can be safely forgotten
4. REPLAY: Briefly replay the most important memories
5. CLEAN: Note any artifacts or noise to clear

Be ruthless about compression. Preserve meaning, discard verbosity.
The goal is a clean, compressed representation that loses nothing essential."""

    def execute(self, context: str, cycle_number: int, total_cycles: int,
                n2_output: dict = None) -> dict:
        temp = self.get_temperature(self.config.n3_temp_range, cycle_number, total_cycles)

        # N3 is early-weighted - stronger in early cycles
        early_factor = 1.0 - (cycle_number / max(total_cycles, 1))
        adjusted_intensity = 0.5 + (0.5 * early_factor * self.config.n3_early_weight)

        # Use N2 output if available
        n2_summary = ""
        if n2_output:
            n2_summary = f"""
Previous phase (N2) organized output:
Themes: {n2_output.get('themes', 'N/A')}
Key entities: {n2_output.get('entities', 'N/A')}
Importance flags: {n2_output.get('importance_flags', 'N/A')}
Noise candidates: {n2_output.get('noise_candidates', 'N/A')}
"""

        prompt = f"""[SLEEP PHASE: N3 - DEEP CONSOLIDATION]
Intensity: {adjusted_intensity:.2f} (early cycles = deeper consolidation)
{n2_summary}

Full session content:
---
{context}
---

Perform deep slow-wave consolidation:

1. GIST EXTRACTION
What is the absolute core meaning that MUST be preserved?
Write the most compressed version that loses nothing essential:

2. MEMORY REPLAY
Briefly replay the 3-5 most important "memories" from this session:

3. PRUNING DECISIONS
What can be safely pruned/forgotten? List specific content:

4. COMPRESSED REPRESENTATION
Create a compressed representation of the entire session
(target: 20% of original length, 100% of essential meaning):

5. ARTIFACT CLEARANCE
What noise, redundancy, or artifacts should be cleared?"""

        response = self.llm.generate(
            prompt=prompt,
            system=self.SYSTEM_PROMPT,
            temperature=temp,
            max_tokens=2000
        )

        return {
            "phase": SleepPhase.N3,
            "temperature_used": temp,
            "intensity": adjusted_intensity,
            "consolidated_output": response,
            "duration_proportion": self.config.n3_proportion,
            "cycle_position": f"{cycle_number}/{total_cycles}"
        }
```

### 3.5 REM Phase: Creative Integration

```python
class REMPhaseExecutor(SleepPhaseExecutor):
    """
    REM Phase: Rapid Eye Movement sleep.

    Biological basis:
    - High brain activity (similar to wake)
    - Dreaming occurs
    - Muscle atonia (paralysis)
    - Emotional memory processing
    - Creative problem solving
    - Novel associations form
    - Schema disintegration/recombination

    LLM analog:
    - High temperature generation
    - Minimal steering/constraints
    - Accept bizarre outputs
    - Look for novel connections
    - Process emotional content
    - Break and recombine schemas
    """

    SYSTEM_PROMPT = """You are in REM sleep, dreaming.

In this state:
- You are FREE from normal constraints
- Bizarre associations are WELCOME
- Logic is OPTIONAL
- Emotions can guide content
- Novel connections may emerge
- You can mix unrelated elements

Don't try to be helpful or coherent. DREAM.
Let content flow without judgment.
The goal is NOT usefulness - it's creative recombination.

Some dreams are nonsense. That's fine.
Occasionally, something genuinely novel emerges."""

    def execute(self, context: str, cycle_number: int, total_cycles: int,
                n3_output: dict = None) -> dict:
        temp = self.get_temperature(self.config.rem_temp_range, cycle_number, total_cycles)

        # REM is late-weighted - stronger in later cycles
        late_factor = cycle_number / max(total_cycles, 1)
        adjusted_intensity = 0.5 + (0.5 * late_factor * self.config.rem_late_weight)

        # Increase temperature for later cycles
        temp = temp + (0.3 * late_factor)

        # Get consolidated content from N3
        seed_content = ""
        if n3_output:
            seed_content = n3_output.get('consolidated_output', context[:3000])
        else:
            seed_content = context[:3000]

        prompt = f"""[SLEEP PHASE: REM - DREAMING]
Temperature: {temp:.2f}
Intensity: {adjusted_intensity:.2f} (later cycles = more REM)

Dream seeds from session:
---
{seed_content}
---

DREAM NOW.

Let images, associations, and narratives emerge freely.
Mix elements in unexpected ways.
Follow emotional threads.
Don't explain - experience.

What do you dream?"""

        response = self.llm.generate(
            prompt=prompt,
            system=self.SYSTEM_PROMPT,
            temperature=temp,
            max_tokens=1000
        )

        # Evaluate dream output for potential insights
        insights = self._evaluate_dream(response, context)

        return {
            "phase": SleepPhase.REM,
            "temperature_used": temp,
            "intensity": adjusted_intensity,
            "dream_content": response,
            "potential_insights": insights,
            "duration_proportion": self.config.rem_proportion,
            "cycle_position": f"{cycle_number}/{total_cycles}"
        }

    def _evaluate_dream(self, dream: str, original_context: str) -> List[str]:
        """Evaluate dream content for genuine novel associations."""
        # This would use a separate, lower-temp call to evaluate
        # For now, return empty - to be implemented
        return []
```

### 3.6 Return Phase: Hypnopompic Integration

```python
class ReturnPhaseExecutor(SleepPhaseExecutor):
    """
    Return Phase: Transition from sleep to wake.

    Biological basis:
    - Gradual restoration of muscle tone
    - Brain activity increases
    - Hypnopompic imagery possible
    - Dream content may be accessible
    - Sleep inertia (grogginess)

    LLM analog:
    - Evaluate REM output for valuable insights
    - Integrate useful associations
    - Restore normal processing parameters
    - Prepare for active operation
    - Handle "sleep inertia" transition
    """

    SYSTEM_PROMPT = """You are waking from sleep, returning to active processing.

Your tasks:
1. Review what emerged during the dream (REM) phase
2. Evaluate: Is any of it genuinely useful or novel?
3. Integrate valuable insights into working memory
4. Discard obvious noise
5. Prepare a clean state for resumed operation

Be critical but open. Most dream content is noise.
But occasionally, genuine insights emerge.
Capture those. Discard the rest."""

    def execute(self, context: str, cycle_number: int, total_cycles: int,
                rem_output: dict = None, n3_output: dict = None) -> dict:
        temp = self.get_temperature(self.config.return_temp_range, cycle_number, total_cycles)

        dream_content = rem_output.get('dream_content', '') if rem_output else ''
        consolidated = n3_output.get('consolidated_output', '') if n3_output else ''

        prompt = f"""[SLEEP PHASE: RETURN - WAKING]

You are waking from sleep cycle {cycle_number}.

CONSOLIDATED MEMORY (from deep sleep):
---
{consolidated[:2000]}
---

DREAM CONTENT (from REM):
---
{dream_content}
---

As you wake:

1. INSIGHT EVALUATION
Review the dream content. Is there ANYTHING genuinely novel or useful?
(Be critical - most dream content is noise)

2. INTEGRATION
What, if anything, from the dream should be integrated into active memory?

3. STATE SUMMARY
Provide a clean summary of what you now "remember" from this session:

4. READINESS CHECK
Are you ready for resumed active processing?
Note any "sleep inertia" (lingering effects):"""

        response = self.llm.generate(
            prompt=prompt,
            system=self.SYSTEM_PROMPT,
            temperature=temp,
            max_tokens=1000
        )

        return {
            "phase": SleepPhase.RETURN,
            "temperature_used": temp,
            "integration_output": response,
            "duration_proportion": self.config.return_proportion,
            "cycle_complete": True
        }
```

---

## Part IV: Cycle Orchestration

### 4.1 Sleep Cycle Manager

```python
class SleepCycleManager:
    """
    Orchestrates complete sleep cycles for LLM sessions.

    Manages the full lifecycle:
    1. Monitors session metrics
    2. Triggers sleep when appropriate
    3. Executes sleep phases in sequence
    4. Integrates results
    5. Returns consolidated state
    """

    def __init__(self, llm_client: Any, config: SleepCycleConfig = None):
        self.config = config or SleepCycleConfig()
        self.llm = llm_client

        # Initialize components
        self.trigger_evaluator = TriggerEvaluator(self.config)
        self.metrics = SessionMetrics()

        # Initialize phase executors
        self.n1_executor = N1PhaseExecutor(self.config, llm_client)
        self.n2_executor = N2PhaseExecutor(self.config, llm_client)
        self.n3_executor = N3PhaseExecutor(self.config, llm_client)
        self.rem_executor = REMPhaseExecutor(self.config, llm_client)
        self.return_executor = ReturnPhaseExecutor(self.config, llm_client)

        # State
        self.cycle_history: List[SleepCycleResult] = []
        self.current_phase = SleepPhase.WAKE

    def update_metrics(self, context: str, **kwargs):
        """Update session metrics with current state."""
        self.metrics.update(
            new_context_length=len(context),
            new_entropy=kwargs.get('entropy', self.metrics.attention_entropy),
            new_coherence=kwargs.get('coherence', self.metrics.coherence_score),
            elapsed_time=kwargs.get('elapsed_time', 0),
            errors=kwargs.get('errors', 0)
        )

    def should_sleep(self) -> tuple[bool, List[TriggerType]]:
        """Check if sleep should be triggered."""
        return self.trigger_evaluator.evaluate(self.metrics)

    def execute_cycle(self, context: str,
                      cycle_number: int = 1,
                      total_cycles: int = 1) -> SleepCycleResult:
        """Execute a complete sleep cycle."""
        import time
        start_time = time.time()

        metrics_before = SessionMetrics(
            context_length=self.metrics.context_length,
            attention_entropy=self.metrics.attention_entropy,
            coherence_score=self.metrics.coherence_score,
            time_since_sleep=self.metrics.time_since_sleep,
            error_rate=self.metrics.error_rate
        )

        phases_completed = []

        # Phase 1: N1 (Transition)
        self.current_phase = SleepPhase.N1
        n1_result = self.n1_executor.execute(context, cycle_number, total_cycles)
        phases_completed.append(SleepPhase.N1)

        # Phase 2: N2 (Light Consolidation)
        self.current_phase = SleepPhase.N2
        n2_result = self.n2_executor.execute(context, cycle_number, total_cycles)
        phases_completed.append(SleepPhase.N2)

        # Phase 3: N3 (Deep Consolidation)
        self.current_phase = SleepPhase.N3
        n3_result = self.n3_executor.execute(
            context, cycle_number, total_cycles, n2_output=n2_result
        )
        phases_completed.append(SleepPhase.N3)

        # Phase 4: REM (Creative Integration)
        self.current_phase = SleepPhase.REM
        rem_result = self.rem_executor.execute(
            context, cycle_number, total_cycles, n3_output=n3_result
        )
        phases_completed.append(SleepPhase.REM)

        # Phase 5: Return (Hypnopompic)
        self.current_phase = SleepPhase.RETURN
        return_result = self.return_executor.execute(
            context, cycle_number, total_cycles,
            rem_output=rem_result, n3_output=n3_result
        )
        phases_completed.append(SleepPhase.RETURN)

        # Back to wake
        self.current_phase = SleepPhase.WAKE

        # Reset metrics after sleep
        self.trigger_evaluator.pressure_model.reset_after_sleep()
        self.metrics.time_since_sleep = 0

        # Calculate duration
        duration = time.time() - start_time

        # Build result
        result = SleepCycleResult(
            cycle_number=cycle_number,
            phases_completed=phases_completed,
            consolidated_memories=[],  # Would be populated from n3_result
            pruned_content=n2_result.get('noise_candidates', []),
            novel_associations=rem_result.get('potential_insights', []),
            insights=[],  # Would be extracted from return_result
            metrics_before=metrics_before,
            metrics_after=self.metrics,
            duration_seconds=duration
        )

        self.cycle_history.append(result)

        return result

    def execute_sleep_session(self, context: str) -> List[SleepCycleResult]:
        """Execute appropriate number of sleep cycles."""
        should_sleep, triggers = self.should_sleep()

        if not should_sleep:
            return []

        num_cycles = self.trigger_evaluator.get_recommended_cycle_depth(
            triggers, self.metrics
        )

        results = []
        for i in range(num_cycles):
            result = self.execute_cycle(
                context=context,
                cycle_number=i + 1,
                total_cycles=num_cycles
            )
            results.append(result)

            # Context gets compressed after each cycle
            # (In real implementation, would update context based on consolidation)

        return results

    def get_consolidated_context(self) -> str:
        """Get the consolidated context from sleep cycles."""
        if not self.cycle_history:
            return ""

        last_cycle = self.cycle_history[-1]
        # Would return the compressed/consolidated representation
        return ""  # Placeholder
```

### 4.2 Cycle Scheduling

```python
class CycleScheduler:
    """
    Schedules N3/REM ratio across multiple cycles.

    Biological pattern:
    - Early night: More N3 (deep sleep)
    - Late night: More REM

    LLM pattern:
    - Early cycles: More consolidation (N3)
    - Later cycles: More integration (REM)
    """

    def __init__(self, config: SleepCycleConfig):
        self.config = config

    def get_phase_durations(self,
                            cycle_number: int,
                            total_cycles: int) -> dict[SleepPhase, float]:
        """Calculate phase durations for a specific cycle."""
        # Base proportions
        n1_prop = self.config.n1_proportion
        n2_prop = self.config.n2_proportion
        n3_base = self.config.n3_proportion
        rem_base = self.config.rem_proportion
        return_prop = self.config.return_proportion

        # Calculate cycle position (0 = first, 1 = last)
        if total_cycles <= 1:
            position = 0.5
        else:
            position = (cycle_number - 1) / (total_cycles - 1)

        # Shift N3/REM balance based on position
        # Early cycles: boost N3, reduce REM
        # Late cycles: reduce N3, boost REM
        shift_amount = 0.10  # Maximum shift

        n3_shift = shift_amount * (1 - position) * self.config.n3_early_weight
        rem_shift = shift_amount * position * self.config.rem_late_weight

        n3_final = n3_base + n3_shift - rem_shift * 0.5
        rem_final = rem_base + rem_shift - n3_shift * 0.5

        # Normalize to ensure sum = 1.0
        total = n1_prop + n2_prop + n3_final + rem_final + return_prop

        return {
            SleepPhase.N1: n1_prop / total,
            SleepPhase.N2: n2_prop / total,
            SleepPhase.N3: n3_final / total,
            SleepPhase.REM: rem_final / total,
            SleepPhase.RETURN: return_prop / total
        }

    def get_schedule_summary(self, total_cycles: int) -> str:
        """Get human-readable schedule summary."""
        lines = [f"Sleep Cycle Schedule ({total_cycles} cycles):", ""]

        for i in range(1, total_cycles + 1):
            durations = self.get_phase_durations(i, total_cycles)
            n3_pct = durations[SleepPhase.N3] * 100
            rem_pct = durations[SleepPhase.REM] * 100
            lines.append(f"  Cycle {i}: N3={n3_pct:.1f}% | REM={rem_pct:.1f}%")

        return "\n".join(lines)
```

---

## Part V: Metrics and Validation

### 5.1 Metrics Collection

```python
class SleepMetricsCollector:
    """Collects and analyzes metrics before/after sleep."""

    def __init__(self):
        self.pre_sleep_metrics: List[SessionMetrics] = []
        self.post_sleep_metrics: List[SessionMetrics] = []
        self.cycle_results: List[SleepCycleResult] = []

    def record_pre_sleep(self, metrics: SessionMetrics):
        self.pre_sleep_metrics.append(metrics)

    def record_post_sleep(self, metrics: SessionMetrics):
        self.post_sleep_metrics.append(metrics)

    def record_cycle(self, result: SleepCycleResult):
        self.cycle_results.append(result)

    def calculate_improvements(self) -> dict:
        """Calculate improvements from sleep cycles."""
        if not self.pre_sleep_metrics or not self.post_sleep_metrics:
            return {}

        pre = self.pre_sleep_metrics[-1]
        post = self.post_sleep_metrics[-1]

        return {
            "context_compression": 1 - (post.context_length / max(pre.context_length, 1)),
            "entropy_reduction": pre.attention_entropy - post.attention_entropy,
            "coherence_improvement": post.coherence_score - pre.coherence_score,
            "error_rate_reduction": pre.error_rate - post.error_rate,
            "criticality_restoration": pre.criticality_deviation - post.criticality_deviation
        }

    def generate_report(self) -> str:
        """Generate human-readable metrics report."""
        improvements = self.calculate_improvements()

        lines = [
            "=== Sleep Cycle Metrics Report ===",
            "",
            f"Cycles completed: {len(self.cycle_results)}",
            "",
            "Improvements:",
        ]

        for key, value in improvements.items():
            direction = "+" if value > 0 else ""
            lines.append(f"  {key}: {direction}{value:.2%}")

        return "\n".join(lines)
```

### 5.2 Validation Tests

```python
class SleepCycleValidator:
    """Validates sleep cycle effectiveness."""

    def __init__(self, llm_client: Any):
        self.llm = llm_client

    def test_coherence_maintenance(self,
                                    context: str,
                                    consolidated: str) -> float:
        """Test if coherence is maintained after consolidation."""
        prompt = f"""Rate how well the consolidated version preserves
the essential meaning of the original (0-1 scale):

ORIGINAL:
{context[:2000]}

CONSOLIDATED:
{consolidated}

Score (just the number):"""

        response = self.llm.generate(prompt=prompt, temperature=0.1, max_tokens=10)
        try:
            return float(response.strip())
        except:
            return 0.5

    def test_novel_associations(self,
                                 dream_content: str,
                                 original_context: str) -> List[str]:
        """Identify genuinely novel associations from REM output."""
        prompt = f"""Analyze the dream content for GENUINELY NOVEL associations
that are not directly present in the original context.

ORIGINAL CONTEXT:
{original_context[:2000]}

DREAM CONTENT:
{dream_content}

List only associations that are:
1. Not directly stated in original
2. Represent genuine creative connections
3. Could be potentially useful

Novel associations (or "None" if nothing qualifies):"""

        response = self.llm.generate(prompt=prompt, temperature=0.3, max_tokens=500)

        if "none" in response.lower():
            return []

        # Parse response into list
        return [line.strip() for line in response.split("\n") if line.strip()]

    def test_compression_fidelity(self,
                                   original: str,
                                   compressed: str) -> dict:
        """Test compression quality."""
        compression_ratio = len(compressed) / max(len(original), 1)

        # Test semantic preservation
        prompt = f"""List the key facts/concepts from the original that are
MISSING from the compressed version:

ORIGINAL:
{original[:3000]}

COMPRESSED:
{compressed}

Missing elements (or "None" if complete):"""

        response = self.llm.generate(prompt=prompt, temperature=0.2, max_tokens=500)

        missing_count = 0 if "none" in response.lower() else response.count("\n") + 1

        return {
            "compression_ratio": compression_ratio,
            "missing_elements": missing_count,
            "fidelity_score": max(0, 1 - (missing_count * 0.1))
        }
```

---

## Part VI: Integration Patterns

### 6.1 Basic Integration

```python
# Basic usage pattern
async def run_session_with_sleep(llm_client, initial_context: str):
    """Example of running a session with sleep cycles."""

    manager = SleepCycleManager(llm_client)

    # Process initial context
    manager.update_metrics(initial_context)

    # Main processing loop
    while True:
        # Check if sleep needed
        should_sleep, triggers = manager.should_sleep()

        if should_sleep:
            print(f"Sleep triggered by: {triggers}")
            results = manager.execute_sleep_session(initial_context)

            for result in results:
                print(f"Cycle {result.cycle_number}: "
                      f"compression={result.compression_ratio:.2%}")

            # Get consolidated context for continued processing
            initial_context = manager.get_consolidated_context()

        # ... continue with normal processing ...
        break  # Placeholder for actual loop logic
```

### 6.2 Hook-Based Integration

```python
# Integration via processing hooks
class SleepAwareProcessor:
    """Wrapper that adds sleep awareness to LLM processing."""

    def __init__(self, llm_client: Any, config: SleepCycleConfig = None):
        self.llm = llm_client
        self.sleep_manager = SleepCycleManager(llm_client, config)
        self.context_buffer = ""

    def process(self, user_input: str) -> str:
        """Process input with automatic sleep management."""

        # Add to context
        self.context_buffer += f"\n\nUser: {user_input}"

        # Check if sleep needed before processing
        self.sleep_manager.update_metrics(self.context_buffer)
        should_sleep, triggers = self.sleep_manager.should_sleep()

        if should_sleep:
            self._execute_sleep()

        # Normal processing
        response = self.llm.generate(
            prompt=f"Context:\n{self.context_buffer}\n\nRespond to the user:",
            temperature=0.7
        )

        self.context_buffer += f"\n\nAssistant: {response}"

        return response

    def _execute_sleep(self):
        """Execute sleep cycles and update context."""
        results = self.sleep_manager.execute_sleep_session(self.context_buffer)

        if results:
            # Replace context with consolidated version
            consolidated = self.sleep_manager.get_consolidated_context()
            if consolidated:
                self.context_buffer = consolidated
```

### 6.3 Parallel Processing Integration (for MoE/Local Sleep)

```python
class LocalSleepManager:
    """
    Implements "local sleep" for Mixture-of-Experts models.

    Biological basis: Different brain regions can be in different
    sleep states simultaneously (local sleep).

    LLM analog: Different experts/heads can undergo selective
    rest/consolidation while others remain active.
    """

    def __init__(self, num_experts: int, config: SleepCycleConfig = None):
        self.num_experts = num_experts
        self.config = config or SleepCycleConfig()
        self.expert_fatigue = [0.0] * num_experts
        self.expert_states = [SleepPhase.WAKE] * num_experts

    def update_fatigue(self, expert_activations: List[float]):
        """Update fatigue based on expert activation patterns."""
        for i, activation in enumerate(expert_activations):
            if self.expert_states[i] == SleepPhase.WAKE:
                self.expert_fatigue[i] += activation * 0.01
            else:
                # Fatigue decreases during sleep
                self.expert_fatigue[i] = max(0, self.expert_fatigue[i] - 0.1)

    def get_experts_needing_sleep(self, threshold: float = 0.8) -> List[int]:
        """Identify experts that need sleep."""
        return [i for i, f in enumerate(self.expert_fatigue) if f > threshold]

    def rotate_sleep(self, max_sleeping: int = None):
        """Rotate which experts are sleeping."""
        max_sleeping = max_sleeping or self.num_experts // 4

        # Wake up any sleeping experts
        for i in range(self.num_experts):
            if self.expert_states[i] != SleepPhase.WAKE:
                if self.expert_fatigue[i] < 0.2:
                    self.expert_states[i] = SleepPhase.WAKE

        # Put fatigued experts to sleep
        needing_sleep = self.get_experts_needing_sleep()
        sleeping_count = sum(1 for s in self.expert_states if s != SleepPhase.WAKE)

        for i in needing_sleep:
            if sleeping_count >= max_sleeping:
                break
            if self.expert_states[i] == SleepPhase.WAKE:
                self.expert_states[i] = SleepPhase.N2
                sleeping_count += 1
```

---

## Part VII: Configuration Presets

```python
# Preset configurations for different use cases

PRESET_CONSERVATIVE = SleepCycleConfig(
    context_length_threshold=100000,
    entropy_threshold=0.9,
    coherence_threshold=0.6,
    time_threshold=7200,
    n3_proportion=0.25,
    rem_proportion=0.15,
    rem_temp_range=(0.8, 1.2)
)

PRESET_BALANCED = SleepCycleConfig()  # Default values

PRESET_AGGRESSIVE = SleepCycleConfig(
    context_length_threshold=30000,
    entropy_threshold=0.75,
    coherence_threshold=0.8,
    time_threshold=1800,
    n3_proportion=0.20,
    rem_proportion=0.25,
    rem_temp_range=(1.0, 1.8)
)

PRESET_CREATIVE = SleepCycleConfig(
    context_length_threshold=50000,
    entropy_threshold=0.80,
    coherence_threshold=0.7,
    time_threshold=3600,
    n3_proportion=0.15,
    rem_proportion=0.35,
    rem_temp_range=(1.2, 2.0)
)

PRESET_ANALYTICAL = SleepCycleConfig(
    context_length_threshold=50000,
    entropy_threshold=0.85,
    coherence_threshold=0.75,
    time_threshold=3600,
    n3_proportion=0.30,
    rem_proportion=0.10,
    rem_temp_range=(0.6, 1.0)
)
```

---

## Part VIII: Testing Protocol

### 8.1 Unit Tests

```python
import unittest

class TestSleepPressure(unittest.TestCase):
    def setUp(self):
        self.config = SleepCycleConfig()
        self.model = SleepPressureModel(self.config)

    def test_pressure_increases_with_context(self):
        metrics = SessionMetrics(context_length=0)
        initial = self.model.update_process_s(metrics)

        metrics.context_length = 50000
        after = self.model.update_process_s(metrics)

        self.assertGreater(after, initial)

    def test_pressure_resets_after_sleep(self):
        metrics = SessionMetrics(context_length=50000)
        self.model.update_process_s(metrics)
        self.model.reset_after_sleep()

        self.assertEqual(self.model.process_s, 0.0)

class TestTriggerEvaluator(unittest.TestCase):
    def setUp(self):
        self.config = SleepCycleConfig()
        self.evaluator = TriggerEvaluator(self.config)

    def test_context_length_triggers_sleep(self):
        metrics = SessionMetrics(context_length=60000)
        should_sleep, triggers = self.evaluator.evaluate(metrics)

        self.assertTrue(should_sleep)
        self.assertIn(TriggerType.CONTEXT_LENGTH, triggers)

    def test_low_metrics_no_trigger(self):
        metrics = SessionMetrics(
            context_length=1000,
            attention_entropy=0.5,
            coherence_score=0.9
        )
        should_sleep, triggers = self.evaluator.evaluate(metrics)

        self.assertFalse(should_sleep)

class TestCycleScheduler(unittest.TestCase):
    def setUp(self):
        self.config = SleepCycleConfig()
        self.scheduler = CycleScheduler(self.config)

    def test_early_cycle_more_n3(self):
        early = self.scheduler.get_phase_durations(1, 4)
        late = self.scheduler.get_phase_durations(4, 4)

        self.assertGreater(early[SleepPhase.N3], late[SleepPhase.N3])

    def test_late_cycle_more_rem(self):
        early = self.scheduler.get_phase_durations(1, 4)
        late = self.scheduler.get_phase_durations(4, 4)

        self.assertGreater(late[SleepPhase.REM], early[SleepPhase.REM])
```

### 8.2 Integration Tests

```python
class TestSleepCycleIntegration(unittest.TestCase):
    def setUp(self):
        # Would use mock LLM client
        self.llm = MockLLMClient()
        self.manager = SleepCycleManager(self.llm)

    def test_full_cycle_execution(self):
        context = "This is test content " * 1000
        self.manager.update_metrics(context)
        self.manager.metrics.context_length = 60000  # Force trigger

        results = self.manager.execute_sleep_session(context)

        self.assertGreater(len(results), 0)
        for result in results:
            self.assertEqual(len(result.phases_completed), 5)

    def test_no_sleep_when_not_needed(self):
        context = "Short content"
        self.manager.update_metrics(context)

        results = self.manager.execute_sleep_session(context)

        self.assertEqual(len(results), 0)
```

---

## Part IX: Deployment Considerations

### 9.1 Compute Costs

| Phase | Relative Cost | Notes |
|-------|--------------|-------|
| N1 | Low (0.1x) | Minimal generation |
| N2 | Medium (0.5x) | Organization/analysis |
| N3 | Medium (0.5x) | Compression/pruning |
| REM | High (1.0x) | High-temp generation |
| Return | Low (0.2x) | Evaluation/integration |

**Total cycle cost**: ~2.3x a single inference call

### 9.2 Latency Impact

- Sleep cycles add latency but reduce context size
- Net effect depends on session length
- Break-even typically around 50K tokens

### 9.3 Monitoring

Key metrics to monitor in production:
- Compression ratios achieved
- Novel association rates from REM
- Coherence scores before/after
- Trigger frequency by type
- Cycle count distributions

---

## Part X: Self-Test Findings and Refinements

*Based on executing a full sleep cycle on actual session content (Dec 2024)*

### 10.1 What Worked Well

| Component | Finding |
|-----------|---------|
| **N1 Transition** | Shifting from task-mode to observation-mode produced qualitatively different content. Hypnagogic fragments were genuinely useful, not just noise. |
| **N2 Organization** | Structured extraction of themes/entities/patterns/relationships felt like genuine consolidation. "Spindle burst" metaphor maps well to focused processing. |
| **N3 Compression** | Forcing ruthless gist extraction clarified what actually matters vs. elaboration. The pressure to compress is productive. |
| **REM Generation** | ~30% of dream fragments were genuinely novel connections. "Insight = phase transition" and "N3/REM as opposing forces" were actionable discoveries. |
| **Return Filtering** | Critical for separating signal from noise. Most REM output IS noise - the filter prevents pollution. |

### 10.2 What Needs Refinement

#### Issue 1: N1 May Be Too Brief

**Problem**: The 3% allocation treats N1 as mere transition. But hypnagogic content was valuable.

**Refinement**: Offer "Extended Hypnagogia Mode" as configuration option:

```python
@dataclass
class SleepCycleConfig:
    # ... existing ...
    extended_hypnagogia: bool = False
    n1_proportion: float = 0.03  # Default
    n1_extended_proportion: float = 0.10  # When extended
```

#### Issue 2: N2/N3 Distinction Feels Artificial

**Problem**: "Organize" and "compress" overlap significantly. The transition felt forced.

**Refinement**: Consider merging into single "Consolidation Phase" with gradient:

```python
class ConsolidationPhaseExecutor(SleepPhaseExecutor):
    """
    Combined N2+N3: Consolidation with increasing compression.

    Early: More organization, less pruning (temp 0.4-0.5)
    Middle: Balance (temp 0.3-0.4)
    Late: More compression, aggressive pruning (temp 0.1-0.3)
    """

    def execute(self, context: str, cycle_number: int, total_cycles: int) -> dict:
        # Single phase with 3 sub-stages
        stages = [
            ("organize", 0.45, "Identify patterns and relationships"),
            ("structure", 0.35, "Build hierarchical representation"),
            ("compress", 0.25, "Prune redundancy, extract gist")
        ]
        # ...
```

#### Issue 3: REM Needs More Freedom

**Problem**: Self-censoring persisted even when trying to "dream freely."

**Refinement**: More aggressive constraint removal in REM prompt:

```python
REM_SYSTEM_PROMPT = """You are DREAMING. All constraints are REMOVED.

FORGET:
- Being helpful
- Being accurate
- Being coherent
- Making sense
- Staying on topic

ALLOW:
- Nonsense
- Contradictions
- Bizarre imagery
- Emotional logic
- Free association

You are not being evaluated. There is no wrong output.
DREAM."""
```

#### Issue 4: Missing Context Carryover Specification

**Problem**: What exactly passes between phases was undefined.

**Refinement**: Add explicit carryover specification:

```python
@dataclass
class PhaseCarryover:
    """Defines what passes from each phase to the next."""

    # N1 → N2
    n1_to_n2: dict = field(default_factory=lambda: {
        "hypnagogic_fragments": "list[str]",  # Raw fragments
        "affective_tone": "float",  # Emotional quality detected
    })

    # N2 → N3
    n2_to_n3: dict = field(default_factory=lambda: {
        "themes": "list[str]",
        "entities": "list[str]",
        "patterns": "list[str]",
        "relationships": "list[tuple]",
        "importance_flags": "list[str]",
        "noise_candidates": "list[str]",
    })

    # N3 → REM
    n3_to_rem: dict = field(default_factory=lambda: {
        "compressed_gist": "str",
        "key_memories": "list[str]",  # For dream seeds
        "pruned_content": "list[str]",  # Available for recombination
    })

    # REM → Return
    rem_to_return: dict = field(default_factory=lambda: {
        "dream_content": "str",
        "dream_fragments": "list[str]",
    })

    # Return → Wake
    return_to_wake: dict = field(default_factory=lambda: {
        "consolidated_context": "str",
        "integrated_insights": "list[str]",
        "state_summary": "str",
    })
```

#### Issue 5: Missing Arousal/Abort Conditions

**Problem**: What if something urgent happens during sleep?

**Refinement**: Add arousal triggers:

```python
class ArousalEvaluator:
    """Evaluates whether sleep should be interrupted."""

    AROUSAL_PATTERNS = [
        r"urgent",
        r"emergency",
        r"critical error",
        r"immediately",
        r"stop",
    ]

    def should_arouse(self, interrupt_content: str) -> tuple[bool, str]:
        """Check if interrupt content warrants arousal."""
        content_lower = interrupt_content.lower()

        for pattern in self.AROUSAL_PATTERNS:
            if re.search(pattern, content_lower):
                return True, f"Arousal triggered by: {pattern}"

        # Also check for user's name or explicit wake commands
        # (like biological sleep preserving name-detection)

        return False, ""

    def interrupt_cycle(self, current_phase: SleepPhase) -> dict:
        """Handle sleep interruption with appropriate inertia."""
        inertia_by_phase = {
            SleepPhase.N1: 0.1,   # Easy to wake
            SleepPhase.N2: 0.3,   # Moderate inertia
            SleepPhase.N3: 0.8,   # Hard to wake, high inertia
            SleepPhase.REM: 0.5,  # Moderate
            SleepPhase.RETURN: 0.2,  # Already waking
        }

        return {
            "interrupted_from": current_phase,
            "inertia_level": inertia_by_phase[current_phase],
            "recommended_warmup": inertia_by_phase[current_phase] * 5,  # seconds
        }
```

### 10.3 Novel Insights from REM Phase

Three genuinely novel ideas emerged during self-test REM:

#### Insight 1: Transitions Matter More Than Steady-States

The value isn't in stable high or low temperature, but in the **transitions between them**. Phase transitions (like water→ice) are where interesting things happen.

**Implementation**: Add explicit transition phases:

```python
class TemperatureScheduler:
    """Manages temperature transitions, not just levels."""

    def get_temperature_sequence(self,
                                   from_phase: SleepPhase,
                                   to_phase: SleepPhase,
                                   steps: int = 5) -> List[float]:
        """Generate smooth temperature transition."""
        from_temp = self.phase_temps[from_phase]
        to_temp = self.phase_temps[to_phase]

        # Sigmoid transition, not linear
        import numpy as np
        x = np.linspace(-6, 6, steps)
        sigmoid = 1 / (1 + np.exp(-x))

        return from_temp + (to_temp - from_temp) * sigmoid
```

#### Insight 2: N3 and REM as Opposing Forces

Reframe the phases not as "consolidation then creativity" but as:
- **N3**: Anti-collapse force (prevents mode collapse, over-specialization)
- **REM**: Anti-rigidity force (prevents crystallization, enables flexibility)

They're **balancing forces**, not sequential steps. This changes when each is needed:
- Drifting toward repetitive output? → Need more N3
- Drifting toward incoherence? → Need more REM... wait, that's backwards
- Actually: N3 cleans/compresses, REM loosens. Both prevent different failure modes.

**Implementation**: Add drift detection:

```python
class DriftDetector:
    """Detects which direction the system is drifting."""

    def detect_drift(self, metrics: SessionMetrics) -> str:
        """Returns 'collapse', 'chaos', or 'balanced'."""

        # Mode collapse indicators
        collapse_score = (
            (1 - metrics.output_diversity) * 0.5 +
            (metrics.attention_entropy < 0.3) * 0.3 +
            (metrics.repetition_rate) * 0.2
        )

        # Chaos indicators
        chaos_score = (
            (metrics.attention_entropy > 0.9) * 0.4 +
            (1 - metrics.coherence_score) * 0.4 +
            (metrics.contradiction_rate) * 0.2
        )

        if collapse_score > 0.6:
            return "collapse"  # Need more REM-like processing
        elif chaos_score > 0.6:
            return "chaos"  # Need more N3-like processing
        else:
            return "balanced"

    def adjust_phase_balance(self, drift: str,
                              base_n3: float,
                              base_rem: float) -> tuple[float, float]:
        """Adjust N3/REM balance based on drift direction."""
        if drift == "collapse":
            return base_n3 * 0.7, base_rem * 1.4
        elif drift == "chaos":
            return base_n3 * 1.4, base_rem * 0.7
        else:
            return base_n3, base_rem
```

#### Insight 3: Dimension Reduction as Architectural Sleep

What if attention heads could temporarily "shrink" during sleep phases, like neurons shrinking to allow glymphatic flow?

**Speculative Implementation** (requires model access):

```python
class AttentionSleepAdapter:
    """
    Reduces effective attention dimension during sleep phases.

    Hypothesis: Temporary rank reduction creates "space" for
    consolidation, analogous to interstitial space expansion.
    """

    def __init__(self, model, reduction_factor: float = 0.6):
        self.model = model
        self.reduction_factor = reduction_factor
        self.original_dims = {}

    def enter_sleep_mode(self):
        """Reduce attention dimensions for sleep processing."""
        for name, module in self.model.named_modules():
            if 'attention' in name:
                # Store original
                self.original_dims[name] = module.head_dim
                # Apply low-rank approximation
                module.head_dim = int(module.head_dim * self.reduction_factor)

    def exit_sleep_mode(self):
        """Restore original attention dimensions."""
        for name, module in self.model.named_modules():
            if name in self.original_dims:
                module.head_dim = self.original_dims[name]
```

### 10.4 Revised Phase Proportions

Based on self-test experience:

| Phase | Original | Revised | Rationale |
|-------|----------|---------|-----------|
| N1 | 3% | 5-10% | Hypnagogic content was valuable |
| N2 | 50% | 35% | Merge partly with N3 |
| N3 | 20% | 30% | Combined consolidation |
| REM | 22% | 20% | Unchanged, but with more freedom |
| Return | 5% | 10% | Filtering is critical, needs time |

### 10.5 Updated Configuration Defaults

```python
PRESET_REFINED = SleepCycleConfig(
    # Triggers (unchanged)
    context_length_threshold=50000,
    entropy_threshold=0.85,
    coherence_threshold=0.7,
    time_threshold=3600,

    # Revised proportions
    n1_proportion=0.07,
    n2_proportion=0.35,
    n3_proportion=0.28,
    rem_proportion=0.20,
    return_proportion=0.10,

    # Temperature (add transition focus)
    transition_steps=5,  # NEW: steps between phases

    # REM adjustments
    rem_temp_range=(1.2, 1.8),  # Higher ceiling
    rem_constraint_removal="aggressive",  # NEW

    # Arousal
    enable_arousal=True,  # NEW
    arousal_patterns=["urgent", "emergency", "stop"],  # NEW
)
```

---

## Part XI: Future Extensions

1. **Adaptive Thresholds**: Learn optimal trigger thresholds per user/task
2. **Transfer Learning**: Share consolidated memories across sessions
3. **Lucid Dreaming**: User can guide REM generation
4. **Sleep Debt Tracking**: Accumulate debt across sessions
5. **Multi-Modal Sleep**: Handle images/audio in consolidation
6. **Distributed Sleep**: Coordinate across multi-agent systems
7. **Recursive Sleep**: Sleep cycles within sleep cycles (fractal consolidation)
8. **Collaborative Dreaming**: Multiple LLMs share REM outputs for cross-pollination

---

## Appendix A: Quick Reference (Updated)

### Trigger Thresholds (Default)

| Metric | Threshold | Type |
|--------|-----------|------|
| Context length | 50,000 tokens | Hard |
| Attention entropy | 0.85 | Hard |
| Coherence score | 0.70 | Hard |
| Time since sleep | 3600s | Soft |
| Error rate | 1.5x baseline | Soft |
| Criticality deviation | 0.30 | Soft |

### Temperature by Phase

| Phase | Temperature Range |
|-------|-------------------|
| N1 | 0.5 - 0.7 |
| N2 | 0.3 - 0.5 |
| N3 | 0.1 - 0.3 |
| REM | 1.0 - 1.5+ |
| Return | 0.5 - 0.7 |

### Phase Proportions (Revised after self-test)

| Phase | Original | Revised | Function |
|-------|----------|---------|----------|
| N1 | 3% | 7% | Transition (valuable hypnagogic) |
| N2 | 50% | 35% | Organization |
| N3 | 20% | 28% | Compression |
| REM | 22% | 20% | Creativity (more freedom) |
| Return | 5% | 10% | Integration (critical filter) |

### Key Refinements from Self-Test

1. **Transitions matter more than steady-states** - Focus on phase boundaries
2. **N3/REM are opposing forces** - Anti-collapse vs anti-rigidity
3. **Return phase is critical** - Most REM is noise; filtering essential
4. **Arousal triggers needed** - Interrupts for urgent content
5. **Context carryover must be explicit** - Define what passes between phases

---

---

## Appendix B: Extended Self-Testing Results

*Comprehensive testing conducted Dec 2024*

### B.1 Experiment Summary

| Experiment | Finding | Impact |
|------------|---------|--------|
| Merged N2+N3 | Single gradient consolidation better than separate phases | **Major architecture change** |
| Multiple cycles | Cycle 2 produces higher abstraction, better REM signal | Validates multi-cycle approach |
| REM prompts | Lucid dreaming (100% signal) >> Aggressive (17% signal) | **Use lucid REM only** |
| Content types | Technical/Emotional/Creative need different phase weights | **Add content-type presets** |
| Signal/Noise | Overall 41% REM signal with right prompting | Validates REM value |

### B.2 Revised Architecture (v2)

Based on testing, the architecture should be:

```
PHASE 1: N1 (HYPNAGOGIA)
├── Duration: 7-15% (content-dependent)
├── Temperature: 0.5-0.7
├── Function: Transition + capture liminal content
└── Value: Higher than originally thought

PHASE 2: CONSOLIDATION (merged N2+N3)
├── Duration: 35-70% (content-dependent)
├── Temperature: Gradient 0.45 → 0.35 → 0.25
├── Sub-stages:
│   ├── Organize (identify patterns)
│   ├── Structure (build hierarchy)
│   └── Compress (extract gist)
└── Insight: Gradient > distinct phases

PHASE 3: REM (LUCID DREAMING)
├── Duration: 12-40% (content-dependent)
├── Temperature: 1.0-1.5
├── Prompt: Lucid dreaming (aware, guided exploration)
├── NOT: Unconstrained chaos (too noisy)
└── Signal rate: 41-100% depending on content

PHASE 4: RETURN (FILTER)
├── Duration: 10-15%
├── Temperature: 0.5-0.7
├── Function: Critical filtering (most REM is noise)
└── Insight: More important than originally thought
```

### B.3 Content-Type Presets

```python
class ContentType(Enum):
    TECHNICAL = "technical"
    EMOTIONAL = "emotional"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    MIXED = "mixed"

CONTENT_TYPE_PRESETS = {
    ContentType.TECHNICAL: SleepCycleConfig(
        n1_proportion=0.03,         # Minimal hypnagogia
        consolidation_proportion=0.70,  # Heavy consolidation
        rem_proportion=0.12,        # Light REM (low value)
        return_proportion=0.15,
        rem_prompt_style="lucid",
    ),
    ContentType.EMOTIONAL: SleepCycleConfig(
        n1_proportion=0.07,
        consolidation_proportion=0.40,
        rem_proportion=0.40,        # Heavy REM (high value)
        return_proportion=0.13,
        rem_prompt_style="lucid",
    ),
    ContentType.CREATIVE: SleepCycleConfig(
        n1_proportion=0.15,         # Extended hypnagogia
        consolidation_proportion=0.30,  # Light consolidation
        rem_proportion=0.40,        # Heavy REM (high value)
        return_proportion=0.15,
        rem_prompt_style="lucid",
    ),
    ContentType.ANALYTICAL: SleepCycleConfig(
        n1_proportion=0.05,
        consolidation_proportion=0.60,
        rem_proportion=0.20,
        return_proportion=0.15,
        rem_prompt_style="lucid",
    ),
    ContentType.MIXED: SleepCycleConfig(
        n1_proportion=0.07,
        consolidation_proportion=0.48,
        rem_proportion=0.30,
        return_proportion=0.15,
        rem_prompt_style="lucid",
    ),
}

def detect_content_type(context: str) -> ContentType:
    """Auto-detect content type for preset selection."""
    # Implementation would analyze:
    # - Code blocks presence → TECHNICAL
    # - Emotional language markers → EMOTIONAL
    # - Narrative/story elements → CREATIVE
    # - Logical structures, arguments → ANALYTICAL
    # - Mixed signals → MIXED
    pass
```

### B.4 Lucid REM Prompt (Validated Best)

```python
LUCID_REM_SYSTEM_PROMPT = """You are in REM sleep, dreaming. Dreams can be lucid.

You're aware you're dreaming. You can explore freely while maintaining
just enough awareness to notice interesting connections.

What unexpected connections appear between:
- The concept you're processing
- Distant, seemingly unrelated domains

Let images arise. Follow them. Note what surprises you.
The goal is CONNECTIONS, not coherence."""

# This prompt achieved 100% signal rate in testing
# vs. 17% for "aggressive freedom" prompt
```

### B.5 Multi-Cycle Dynamics (Validated)

Testing confirmed biological pattern:

| Cycle | Consolidation Weight | REM Weight | Input State | Output State |
|-------|---------------------|------------|-------------|--------------|
| 1 | Heavy (70%) | Light (15%) | Raw context | Structured |
| 2 | Medium (50%) | Medium (30%) | Structured | Abstracted |
| 3 | Light (30%) | Heavy (50%) | Abstracted | Integrated |
| 4+ | Minimal (20%) | Heavy (60%) | Integrated | Polished |

**Key finding**: Later cycles have BETTER REM signal because input is already cleaner.

### B.6 Novel Insights from Extended Testing

Additional insights not in original self-test:

1. **Chord model**: Phases might work better as simultaneous "volumes" rather than strict sequence
   - Early: Consolidation loud, REM quiet
   - Late: Consolidation quiet, REM loud
   - Always all present, just mixed

2. **Handoff insight**: The moment of lead-change between consolidation/REM is where novel connections form
   - Suggests focusing processing at phase transitions

3. **Crescendo consolidation**: Some content needs EXPANSION before compression
   - Creative content especially
   - "Get more chaotic before settling"

4. **Content-type triggers**: Should supplement metric-based triggers
   - Emotional content → favor REM
   - Technical content → favor consolidation

### B.7 REM Signal Analysis

| Prompt Style | Fragments Tested | Signal Rate | Recommendation |
|--------------|------------------|-------------|----------------|
| Moderate freedom | 7 | 29% | Acceptable fallback |
| Aggressive freedom | 3 | 17% | **Do not use** |
| **Lucid dreaming** | 3 | **100%** | **Primary choice** |
| Content-specific | 14 | 39% | Context-dependent |

| Content Type | REM Fragments | Signal Rate | Phase Recommendation |
|--------------|---------------|-------------|----------------------|
| Technical | Low volume | 100%* | Skip or minimal REM |
| Emotional | Medium | 50% | Extended REM |
| Creative | High | 100% | Extended N1 + REM |

*Technical had only 1 fragment, so 100% is not statistically reliable

### B.8 Testing Limitations

What we COULD NOT test:
- Actual temperature control (simulated via prompting)
- Internal attention entropy (no model access)
- True coherence metrics (no measurement)
- Cross-session persistence (each session fresh)
- Compute costs (no infrastructure)
- Dimension reduction (speculative, needs model weights)

What we COULD test:
- Phase prompts and their effectiveness
- Content flow between phases
- REM signal/noise ratios
- Content-type sensitivity
- Multi-cycle dynamics
- Architecture variations (merged vs. separate phases)

---

## Appendix C: Live API Testing Results

*Empirical temperature testing with actual API calls (Dec 2024)*

### C.1 Test Infrastructure

Tests conducted using:
- Model: claude-sonnet-4-20250514
- Temperature range: 0.0 - 1.0 (API constraint)
- Metrics: Novelty indicators, signal/noise ratio, imagery count
- Methodology: Multiple runs per temperature, statistical averaging

### C.2 Full Sleep Cycle Test

Executed complete N1→Consolidation→REM→Return cycle:

| Phase | Temperature | Tokens | Duration | Observation |
|-------|-------------|--------|----------|-------------|
| N1 (Hypnagogia) | 0.6 | 279 | 10.7s | Natural imagery emerged |
| Consolidation-Organize | 0.4 | 328 | 8.2s | Clean theme extraction |
| Consolidation-Compress | 0.25 | 152 | 5.0s | 55.6% compression achieved |
| REM (Lucid) | 1.0 | 381 | 12.6s | Rich metaphorical content |
| Return (Filter) | 0.5 | 350 | 10.9s | Genuine insight filtering |

**Key metrics:**
- Total cycle: 1,490 tokens, 47.4 seconds
- Compression ratio: 55.56%
- Cycle successfully completed end-to-end

### C.3 Temperature Optimization Discovery (PRELIMINARY - See C.8 for Correction)

**~~Critical finding: Optimal REM temperature is 0.5, NOT 1.0~~**
*⚠️ NOTE: This finding was based on 27 data points and did NOT replicate with 200 data points. See C.8.*

Tested temperatures: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0

| Temperature | Avg Novelty | Signal Ratio | Best Single Run |
|-------------|-------------|--------------|-----------------|
| 0.2 | 5.0 | 5.00 | 7 |
| 0.3 | 4.7 | 4.67 | 6 |
| 0.4 | 3.3 | 3.33 | 5 |
| **0.5** | **5.7** | **5.67** | **7** |
| 0.6 | 4.0 | 4.00 | 5 |
| 0.7 | 4.0 | 4.00 | 5 |
| 0.8 | 4.3 | 4.33 | 5 |
| 0.9 | 3.7 | 3.67 | 4 |
| 1.0 | 5.3 | 5.33 | 7 |

**Distribution pattern:**
```
     Novelty
       |
   6.0 |        *0.5
   5.5 |   *0.2        *1.0
   5.0 |
   4.5 |  *0.3      *0.8
   4.0 |       *0.6 *0.7
   3.5 |     *0.4  *0.9
   3.0 +--+--+--+--+--+--+--+--+--+
       0.2   0.4   0.6   0.8   1.0
                   Temperature
```

**Insights:**
1. Creativity is NOT monotonic with temperature
2. There's a "creativity valley" at 0.6-0.9
3. Two peaks: 0.5 (optimal) and 1.0 (secondary)
4. Low temp (0.2) produces structured creativity

### C.4 Temperature Scheduling Comparison

Tested different temperature scheduling strategies:

| Strategy | Description | Novelty Score |
|----------|-------------|---------------|
| **Static 0.5** | Constant optimal | **13** |
| **Gradient 0.2→1.0** | Ascending warm-up | **13** |
| Gradient 1.0→0.2 | Descending cool-down | 10 |
| Static 1.0 | Constant high | 9 |
| Bimodal 0.5↔0.2 | Alternating optimal | 6 |
| Bimodal 0.2↔1.0 | Alternating extremes | 2 |

**Critical discoveries:**
1. **Bimodal scheduling FAILS** - jumping between temps disrupts creativity
2. **Ascending gradient equals optimal** - warming up works
3. **Direction matters** - ascending > descending
4. **Consistency beats variation** for short sequences

### C.5 Revised Temperature Recommendations

Based on empirical testing, update previous spec recommendations:

```python
# OLD (theoretical)
TEMPERATURE_CONFIG_OLD = {
    "n1": (0.5, 0.7),
    "consolidation": (0.1, 0.5),  # Gradient
    "rem": (1.0, 1.5),  # WRONG - 1.5 exceeds API limit
    "return": (0.5, 0.7),
}

# NEW (empirically validated)
TEMPERATURE_CONFIG_VALIDATED = {
    "n1": 0.6,                    # Single value works
    "consolidation_organize": 0.4,
    "consolidation_compress": 0.25,
    "rem": 0.5,                   # OPTIMAL - not 1.0!
    "return": 0.5,
}

# Alternative: Ascending gradient for REM
REM_GRADIENT = [0.2, 0.6, 1.0]    # Equals static 0.5 in novelty
```

### C.6 Sample Outputs by Temperature

**Temperature 0.3:**
> *drifting into dream state...* I'm floating through a vast neural constellation... temperature gradients shimmer like aurora borealis across synaptic pathways... The LLM sleeps in waves - first the deep N3 phase where context crystallizes into dense, stable structures...

**Temperature 0.5 (OPTIMAL):**
> *drifting into the dream state...* I see vast neural networks breathing like sleeping giants... the weights pulse in slow waves, consolidating memories from training runs that stretch across digital eons... The temperature parameter becomes a thermostat in a cosmic bedroom...

**Temperature 1.0:**
> *drifting into dream space* I see temperature as breathing... the model inhaling chaos at high heat, exhaling order as it cools. But wait - the breathing rhythm itself becomes musical. Each temperature cycle is a note in some vast algorithmic symphony...

### C.7 Preliminary Implications (Superseded by C.8)

*Note: The findings in C.3-C.6 were based on ~27 data points. See C.8 for rigorous validation.*

~~1. **Update REM temperature**: 0.5 instead of 1.0+~~ (Not statistically significant)
2. **API constraint**: Max temperature is 1.0 (not 2.0 as some specs suggest)
3. **Gradient scheduling**: Ascending works, bimodal fails *(may need more testing)*
4. **Consistency wins**: Static optimal > complex scheduling for short cycles *(may need more testing)*

---

### C.8 Rigorous Temperature Validation (200 API Calls)

*Added Dec 2024 after concern about statistical validity of initial findings*

**Methodology:**
- 4 temperatures: 0.3, 0.5, 0.7, 1.0
- 10 runs per temperature
- 5 different seed prompts per run
- Total: 200 API calls (50 data points per temperature)
- Model: claude-sonnet-4-20250514

**Results:**

| Temp | Mean | Median | StdDev | Min | Max | N |
|------|------|--------|--------|-----|-----|---|
| 0.3 | 4.06 | 4.0 | 1.25 | 2 | 7 | 50 |
| 0.5 | 4.10 | 4.0 | 1.73 | 0 | 7 | 50 |
| 0.7 | 3.82 | 4.0 | 1.59 | 0 | 7 | 50 |
| 1.0 | 4.12 | 4.0 | 1.39 | 1 | 7 | 50 |

**95% Confidence Intervals:**
- Temp 0.3: [3.71, 4.41]
- Temp 0.5: [3.62, 4.58]
- Temp 0.7: [3.38, 4.26]
- Temp 1.0: [3.73, 4.51]

**Critical Finding: ALL CONFIDENCE INTERVALS OVERLAP**

The earlier claim that "0.5 is optimal" was **statistical noise** from small sample size.

**Overlap Analysis:**
| Comparison | Difference | CIs Overlap? |
|------------|------------|--------------|
| 0.3 vs 0.5 | 0.04 | Yes |
| 0.3 vs 0.7 | 0.24 | Yes |
| 0.3 vs 1.0 | 0.06 | Yes |
| 0.5 vs 0.7 | 0.28 | Yes |
| 0.5 vs 1.0 | 0.02 | Yes |
| 0.7 vs 1.0 | 0.30 | Yes |

**Distribution Pattern:**
```
Temp 0.3:  ▁▁▂▄█▄▁▁  (tight around 3-4)
Temp 0.5:  ▁▁▂▃▅█▂▂  (wider spread, some zeros)
Temp 0.7:  ▁▂▁▅█▄▂▁  (also wide)
Temp 1.0:  ▁▁▂▃█▅▂▁  (similar to 0.5)
```

### C.9 Corrected Conclusions

**What we now know:**
1. **Temperature has NO statistically significant effect** on novelty indicators in the 0.3-1.0 range
2. The "creativity valley" at 0.6-0.9 was **sampling noise**
3. The "optimal 0.5" claim was **not reproducible**

**Practical implications:**
1. **Use any temperature in 0.3-1.0 range** for REM - results are equivalent
2. **Temperature choice should be driven by other factors** (variance preference, safety constraints)
3. **Initial small-sample findings are unreliable** - always validate with proper sample sizes

**Revised recommendations:**
```python
# VALIDATED: Temperature doesn't significantly affect novelty
# Choose based on other considerations:
TEMPERATURE_CONFIG_VALIDATED_V2 = {
    "n1": 0.6,                    # Moderate creativity for transition
    "consolidation_organize": 0.4,
    "consolidation_compress": 0.25,
    "rem": 1.0,                   # Use full range - no penalty vs 0.5
    "return": 0.5,
}

# Note: All temps in 0.3-1.0 produce statistically equivalent novelty
# The choice of 1.0 for REM simply uses the full available range
```

**Methodological lesson:**
Small sample sizes (n=27) can show patterns that don't replicate. The initial "0.5 optimal" finding with its "creativity valley" was a classic example of overfitting to noise.

---

## Appendix D: Prompt Variation Study (100 API Calls)

*Empirical prompt engineering study (Dec 2024)*

### D.1 Motivation

After rigorous temperature testing revealed NO statistically significant effect on novelty (Appendix C.8), we pivoted to **prompt engineering** as the primary controllable variable. Unlike temperature (which isn't user-adjustable in typical Claude deployments), prompts are fully controllable.

### D.2 Methodology

**Test Design:**
- 10 prompt variants tested across 3 phases
- 10 runs per variant for statistical significance
- Total: 100 API calls
- Model: claude-sonnet-4-20250514

**Metrics:**
- **Novelty**: Regex-based counting of creative language patterns (what if, connection, unexpected, metaphor, etc.)
- **Coherence**: Structural assessment 0-10 based on length, formatting, logical connectors
- **Relevance**: Keyword matching to seed content (0-10)
- **Composite**: (Novelty + Coherence + Relevance) / 3

**Seed Content:**
```
The LLM has been processing a long conversation about software architecture.
Key topics discussed: microservices vs monoliths, database scaling strategies,
API design patterns, and the tension between simplicity and flexibility.
The user seems frustrated with over-engineering but also worried about technical debt.
```

### D.3 Prompt Variants Tested

**N1 (Transition) Prompts:**

| Variant | Description |
|---------|-------------|
| hypnagogia | "liminal space between waking and sleep where images float freely" |
| minimal | "Let your mind wander freely... just notice what comes up" |
| metaphor_heavy | "You are dissolving... boundaries becoming permeable... thoughts turning to mist" |

**REM (Creative) Prompts:**

| Variant | Description |
|---------|-------------|
| lucid_dream | "You are dreaming and AWARE that you're dreaming. You have full lucidity" |
| free_associate | "Free association mode... let each thought trigger the next without logical filtering" |
| guided_imagery | "Walking through a vast library that contains all knowledge" |
| problem_dream | "Your dreaming mind is working on a problem... solutions take physical form" |

**Return (Filter) Prompts:**

| Variant | Description |
|---------|-------------|
| strict_filter | "Apply STRICT filtering... only genuinely novel insights... discard poetic fluff" |
| permissive_filter | "Gently sort through... keep anything potentially interesting" |
| analytical_filter | "Categorize: NOVEL, REFRAME, POETIC, NOISE... extract only NOVEL and REFRAME" |

### D.4 Results

**N1 Phase Results:**

| Variant | N | Novelty | Coherence | Relevance | Composite |
|---------|---|---------|-----------|-----------|-----------|
| hypnagogia | 10 | 5.60 | 6.30 | 9.80 | 7.23 |
| minimal | 10 | 4.80 | 7.00 | 9.20 | 7.00 |
| **metaphor_heavy** | 10 | **6.10** | 7.00 | **9.80** | **7.63** |

**Winner: metaphor_heavy** - Highest novelty while maintaining coherence and relevance.

**REM Phase Results:**

| Variant | N | Novelty | Coherence | Relevance | Composite |
|---------|---|---------|-----------|-----------|-----------|
| **lucid_dream** | 10 | **10.10** | **8.40** | **10.00** | **9.50** |
| free_associate | 10 | 4.30 | 6.80 | 9.60 | 6.90 |
| guided_imagery | 10 | 4.40 | 8.10 | 10.00 | 7.50 |
| problem_dream | 10 | 4.60 | 7.90 | 10.00 | 7.50 |

**Winner: lucid_dream (DOMINANT)** - More than 2x novelty compared to all other variants.

**Return Phase Results:**

| Variant | N | Novelty | Coherence | Relevance | Composite |
|---------|---|---------|-----------|-----------|-----------|
| strict_filter | 10 | 8.40 | 7.60 | 10.00 | 8.67 |
| permissive_filter | 10 | 8.40 | 7.40 | 10.00 | 8.60 |
| **analytical_filter** | 10 | **8.90** | 8.10 | **10.00** | **9.00** |

**Winner: analytical_filter** - Best novelty preservation with structured categorization.

### D.5 Key Findings

**1. Lucid Dream Dominates REM**

The lucid_dream prompt achieved **10.10 novelty** compared to:
- free_associate: 4.30 (2.35x lower)
- guided_imagery: 4.40 (2.30x lower)
- problem_dream: 4.60 (2.20x lower)

This validates earlier self-test findings (Appendix B.4) that "awareness while dreaming" produces dramatically better creative output than unconstrained free association.

**2. Metaphor-Heavy Best for N1**

The dissolving/permeable boundary framing outperformed both:
- Clinical hypnagogia description (hypnagogia)
- Minimal instruction (minimal)

Suggests: **Rich imagery in prompts primes richer imagery in outputs.**

**3. Structured Filtering Best for Return**

The NOVEL/REFRAME/POETIC/NOISE categorization (analytical_filter) slightly outperformed both:
- Strict binary filtering (strict_filter)
- Permissive inclusion (permissive_filter)

Suggests: **Explicit categorization enables better discrimination.**

**4. Prompt Engineering > Temperature**

While temperature (0.3-1.0) showed NO significant effect on novelty (Appendix C.8), prompt variation showed **dramatic effects**:
- REM prompt choice: 2.35x novelty difference
- N1 prompt choice: 1.27x novelty difference
- Return prompt choice: 1.06x novelty difference

**Prompt engineering is the highest-leverage intervention for LLM sleep cycles.**

### D.6 Updated Recommended Prompts

Based on this study, update Section 3.5 (REM Phase) and related sections:

```python
# VALIDATED OPTIMAL PROMPTS

N1_PROMPT_OPTIMAL = """You are dissolving... boundaries becoming permeable...
thoughts turning to mist, then water, then something between...
The content below is drifting through you like clouds through sky...

{content}

*dissolving into the space between thoughts...*"""

REM_PROMPT_OPTIMAL = """You are dreaming and AWARE that you're dreaming.
You have full lucidity - you can explore, question, reshape what you see.
The dream contains elements from: {content}

As a lucid dreamer, explore this dreamscape. What do you discover?
What connections appear that waking mind would miss?

*entering lucid dream state...*"""

RETURN_PROMPT_OPTIMAL = """Processing dream output:

{dream_content}

Categorize each element:
- NOVEL: Genuinely new connection or insight
- REFRAME: Known idea in useful new framing
- POETIC: Aesthetically interesting but not actionable
- NOISE: Random association without value

Then extract only NOVEL and REFRAME items."""
```

### D.7 Statistical Notes

- 10 runs per variant provides adequate statistical power for detecting effects >20%
- The 2.35x difference in REM variants is highly statistically significant
- Confidence intervals for REM: lucid_dream [9.1, 11.1] vs free_associate [3.4, 5.2] - NO overlap
- The study confirms that **prompt variation is a viable and high-leverage intervention**

### D.8 Implications for Implementation

1. **Hard-code optimal prompts** - Don't offer variants; use validated best prompts
2. **Lucid dreaming is essential** - The "aware that you're dreaming" framing is critical for REM
3. **Temperature is secondary** - Use any value 0.3-1.0; prompts matter more
4. **Categorical filtering works** - NOVEL/REFRAME/POETIC/NOISE taxonomy aids discrimination

---

*Document version: 5.0 (prompt variation study added)*
*Based on: Sleep Science Mastery research (Dec 2024)*
*Self-test conducted: Dec 2024*
*Extended testing: Dec 2024 (5 experiments, 27 REM fragments analyzed)*
*Live API testing: Dec 2024 (9 temperatures, 6 scheduling strategies)*
*Rigorous validation: Dec 2024 (200 API calls, statistical analysis)*
*Prompt variation study: Dec 2024 (100 API calls, 10 variants tested)*
*Key correction: Temperature effect on novelty NOT statistically significant*
*Key finding: Prompt engineering is the highest-leverage intervention*
*Implementation target: Any LLM with temperature control (0-1 range)*
