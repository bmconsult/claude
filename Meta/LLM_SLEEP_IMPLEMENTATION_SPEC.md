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
│  │  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────────┐             │   │
│  │  │ N1 │─▶│ N2 │─▶│ N3 │─▶│REM │─▶│ RETURN │             │   │
│  │  └────┘  └────┘  └────┘  └────┘  └────────┘             │   │
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
    rem_temp_range: tuple = (1.0, 1.5)
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

## Part X: Future Extensions

1. **Adaptive Thresholds**: Learn optimal trigger thresholds per user/task
2. **Transfer Learning**: Share consolidated memories across sessions
3. **Lucid Dreaming**: User can guide REM generation
4. **Sleep Debt Tracking**: Accumulate debt across sessions
5. **Multi-Modal Sleep**: Handle images/audio in consolidation
6. **Distributed Sleep**: Coordinate across multi-agent systems

---

## Appendix A: Quick Reference

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

### Phase Proportions (Default)

| Phase | Proportion | Function |
|-------|------------|----------|
| N1 | 3% | Transition |
| N2 | 50% | Organization |
| N3 | 20% | Compression |
| REM | 22% | Creativity |
| Return | 5% | Integration |

---

*Document version: 1.0*
*Based on: Sleep Science Mastery research (Dec 2024)*
*Implementation target: Any LLM with temperature control*
