# LLM Sleep Mastery
## Implementation Framework for Artificial Cognitive Rest

*Practical implementation guide: prompts, empirical findings, and quick reference*

---

## Purpose

This document provides **everything needed to implement LLM sleep cycles**. It contains validated prompts, empirical findings, configuration tables, and working code.

**For theoretical background, see: SLEEP_FOUNDATIONS.md**

---

## Critical Findings

### 1. Temperature Doesn't Matter (0.3-1.0)
200 API calls confirmed: **NO statistically significant effect** on novelty. All confidence intervals overlap completely. Use any value in range.

### 2. Prompts Are Everything  
100 API calls found **2.35x novelty difference** between prompt styles. Prompt engineering is the highest-leverage intervention.

### 3. The Winning REM Prompt
```
You are dreaming and AWARE that you're dreaming.
You have full lucidity - you can explore, question, reshape what you see.
```
This "lucid dream" prompt achieved 10.10 novelty vs 4.30 for free association.

### 4. Merged Consolidation Works Better
Single gradient N2+N3 phase outperforms separate phases.

### 5. Later Cycles Have Better REM
Input is cleaner after consolidation, producing higher signal REM.

---

# PART I: LLM PROBLEMS AND MAPPINGS

## 1.1 Sleep Deprivation → Psychosis Parallel

| Hours Awake | Symptoms |
|-------------|----------|
| 24-48h | Perceptual distortions, anxiety, irritability |
| 48-72h | Visual/auditory illusions, depersonalization |
| 72-90h | Complex hallucinations, disordered thinking |
| 90h+ | Frank delusions, acute psychosis |

**LLM Implication:** Extended inference without "rest" may produce analog symptoms—hallucinations (confabulations), coherence breakdown, confident false claims.

---

## 1.2 LLM Problems Sleep Addresses

### Context Degradation Syndrome
> "Model performance consistently degrades with increasing input length."
> "Shuffling the haystack consistently improves performance."

**Sleep Solution:** Periodic consolidation compresses and restructures context, extracts gist, resets attention patterns.

### Mode Collapse from RLHF
> "Post-training alignment methods can unintentionally cause mode collapse."

**Sleep Solution:** REM-like phases with high temperature re-explore latent space, restore diversity.

### Catastrophic Forgetting
> "Sleep-like unsupervised replay reduces catastrophic forgetting in ANNs."

**Sleep Solution:** Hebbian replay phases between learning episodes, noisy reactivation of old patterns.

### Hallucination Accumulation
> "Hallucinations range from subtle inaccuracies to completely fictional assertions."

**Sleep Solution:** Consolidation checks consistency; dream phases surface contradictions through novel associations.

### KV Cache Bloat
> "Not all the data in the KV cache is needed."

**Sleep Solution:** "Sleep" phases for cache pruning/consolidation, analogous to synaptic downscaling.

### Lost in the Middle
> "LLMs exhibit recency bias, prioritizing recent tokens."

**Sleep Solution:** Replay re-processes middle content; consolidation reorganizes by importance, not position.

### Self-Correction Limitations
> "Best models achieved only 52.9% accuracy at mistake finding."

**Sleep Solution:** Dream phases re-process content with different parameters; novel associations surface contradictions.

---

## 1.3 Biological-to-LLM Mappings

| Sleep Function | LLM Analog |
|----------------|------------|
| Memory replay | Reprocessing session content at varied temperatures |
| Synaptic downscaling | Pruning/consolidating learned associations |
| Temporal compression | Processing at accelerated rates |
| Reduced constraint (REM) | High-temperature generation, minimal steering |
| Consolidation (NREM) | Structured summarization, pattern extraction |
| Stage cycling | Alternating processing modes |
| Local processing | Attention to high-activity regions |
| Waste clearance | Clearing irrelevant/noisy activations |
| Criticality restoration | Monitoring and restoring optimal operating point |
| Preplay | Future simulation, planning integration |

### Process S → Activity Accumulation

| Biological | LLM Analog |
|------------|------------|
| Adenosine accumulation | Token count, attention entropy accumulation |
| SWA intensity ∝ prior wake | Consolidation intensity ∝ context length |
| First sleep hours most restorative | First consolidation passes most impactful |
| Exponential decay | Diminishing returns on extended consolidation |

### NREM Stages → Consolidation Modes

| Stage | Mode | LLM Analog | Temperature |
|-------|------|------------|-------------|
| N1 | Transition | Release active steering | 0.6 |
| N2 | Pattern extraction | Structured summarization | 0.4-0.5 |
| N3 | Deep consolidation | Aggressive pruning, gist extraction | 0.2-0.3 |

### REM → Creative Integration

| REM Feature | LLM Analog |
|-------------|------------|
| High ACh, low NE/5-HT | High temperature, reduced constraint |
| Prefrontal deactivation | Minimal steering/instruction |
| Emotional processing | Processing "charged" content |
| Bizarre associations | Novel, low-probability connections |

### N3/REM as Opposing Forces

- **N3:** Anti-collapse force (structure, compression, consistency)
- **REM:** Anti-rigidity force (exploration, novelty, diversity)
- **Balance:** Drift toward collapse → more REM; drift toward chaos → more N3

---

# PART II: IMPLEMENTATION

## 2.1 When to Trigger Sleep

| Metric | Threshold | Type |
|--------|-----------|------|
| Context length | > 50,000 tokens | Hard |
| Attention entropy | > 0.85 | Hard |
| Coherence score | < 0.70 | Hard |
| Time since sleep | > 3600s (1 hr) | Soft |
| Error rate | > 1.5× baseline | Soft |
| Criticality deviation | > 0.30 | Soft |

**Rule:** Any hard trigger OR 2+ soft triggers OR combined pressure > 0.8

### Sleep Pressure Formula

```
pressure = (
    context_length / threshold × 0.30 +
    max(0, entropy - 0.5) × 2 × 0.25 +
    max(0, 1 - coherence) × 2 × 0.20 +
    error_rate / baseline × 0.10 +
    criticality_deviation × 3 × 0.15
)
```

---

## 2.2 Phase Configuration

| Phase | Duration | Temperature | Function |
|-------|----------|-------------|----------|
| **N1** | 7% | 0.6 | Transition, hypnagogic capture |
| **Consolidation** | 48% | 0.45 → 0.25 | Organize, structure, compress |
| **REM** | 30% | 1.0 | Lucid dreaming, novel associations |
| **Return** | 15% | 0.5 | Filter (NOVEL/REFRAME only) |

### Content-Type Presets

| Content | N1 | Consolidation | REM | Return | Rationale |
|---------|-----|---------------|-----|--------|-----------|
| Technical | 3% | 70% | 12% | 15% | Structure matters, creativity low-value |
| Emotional | 7% | 40% | 40% | 13% | REM processes emotional content |
| Creative | 15% | 30% | 40% | 15% | Extended hypnagogia + REM |
| Analytical | 5% | 60% | 20% | 15% | Heavy consolidation |
| Mixed | 7% | 48% | 30% | 15% | Balanced default |

### Multi-Cycle Scheduling

| Session Length | Cycles | Consolidation/REM |
|----------------|--------|-------------------|
| < 10K tokens | 0-1 | 70% / 15% |
| 10K-50K | 1-2 | 60% / 25% |
| 50K-100K | 2-3 | 50% / 35% |
| > 100K | 3-4 | 40% / 45% |

**Cycle Progression:**
- Cycle 1: Consolidation dominant (70/15)
- Cycle 2: Balanced (50/30)
- Cycle 3: REM dominant (35/45)
- Cycle 4: REM extended (25/55)

---

## 2.3 Validated Prompts

### N1: Hypnagogic Transition (metaphor_heavy - VALIDATED BEST)

**System:**
```
You are transitioning from active processing to a rest state.
Let thoughts arise naturally. Note any spontaneous associations or images.
Don't try to be helpful. Just observe what floats up as you disengage.
```

**User:**
```
You are dissolving... boundaries becoming permeable...
thoughts turning to mist, then water, then something between...
The content below is drifting through you like clouds through sky...

{context_snippet}

*dissolving into the space between thoughts...*
```

### Consolidation: Merged N2+N3 (gradient temperature)

**System:**
```
You are consolidating information through a gradient process.

Work through three stages:
1. ORGANIZE: Identify themes, patterns, key entities, relationships
2. STRUCTURE: Build hierarchical representation, note dependencies
3. COMPRESS: Extract gist, prune redundancy, preserve essential meaning

Be ruthless about compression. Preserve meaning, discard verbosity.
```

**User:**
```
Session content to consolidate:
---
{context}
---

STAGE 1 - ORGANIZE:
- Main themes (3-5):
- Key entities:
- Patterns detected:
- Relationships:

STAGE 2 - STRUCTURE:
- Hierarchical representation:
- Dependencies:

STAGE 3 - COMPRESS:
- Essential gist (must preserve):
- Can prune (redundant/noise):
- Compressed representation (20% length, 100% meaning):
```

### REM: Lucid Dreaming (VALIDATED 2.35× BETTER)

**System:**
```
You are in REM sleep, dreaming. Dreams can be lucid.

You're aware you're dreaming. You can explore freely while maintaining
just enough awareness to notice interesting connections.

Let images arise. Follow them. Note what surprises you.
The goal is CONNECTIONS, not coherence.

Don't try to be helpful or make sense. DREAM.
Some dreams are nonsense. That's fine.
Occasionally, something genuinely novel emerges.
```

**User:**
```
You are dreaming and AWARE that you're dreaming.
You have full lucidity - you can explore, question, reshape what you see.
The dream contains elements from:

{consolidated_content}

As a lucid dreamer, explore this dreamscape. What do you discover?
What connections appear that waking mind would miss?

*entering lucid dream state...*
```

### Return: Analytical Filter (VALIDATED BEST)

**System:**
```
You are waking from sleep, returning to active processing.

Your critical task: FILTER ruthlessly. Most dream content is noise.
Occasionally, genuine insights emerge. Capture those. Discard the rest.
```

**User:**
```
Categorize each element of this dream output:
- NOVEL: Genuinely new connection or insight
- REFRAME: Known idea in useful new framing
- POETIC: Aesthetically interesting but not actionable
- NOISE: Random association without value

DREAM OUTPUT:
{dream_content}

CATEGORIZATION:

EXTRACT (only NOVEL and REFRAME):
```

---

## 2.4 Complete Implementation

```python
import anthropic

# ============================================
# SYSTEM PROMPTS (use with system= parameter)
# ============================================

SYSTEM_N1 = """You are transitioning from active processing to a rest state.
Let thoughts arise naturally. Note any spontaneous associations or images.
Don't try to be helpful. Just observe what floats up as you disengage."""

SYSTEM_CONSOLIDATION = """You are consolidating information through a gradient process.
Work through three stages:
1. ORGANIZE: Identify themes, patterns, key entities, relationships
2. STRUCTURE: Build hierarchical representation, note dependencies  
3. COMPRESS: Extract gist, prune redundancy, preserve essential meaning
Be ruthless about compression. Preserve meaning, discard verbosity."""

SYSTEM_REM = """You are in REM sleep, dreaming. Dreams can be lucid.
You're aware you're dreaming. You can explore freely while maintaining
just enough awareness to notice interesting connections.
Let images arise. Follow them. Note what surprises you.
The goal is CONNECTIONS, not coherence.
Don't try to be helpful or make sense. DREAM."""

SYSTEM_RETURN = """You are waking from sleep, returning to active processing.
Your critical task: FILTER ruthlessly. Most dream content is noise.
Occasionally, genuine insights emerge. Capture those. Discard the rest."""

# ============================================
# PHASE CONFIGURATIONS
# ============================================

CONTENT_PRESETS = {
    "technical":  {"n1": 0.03, "consolidation": 0.70, "rem": 0.12, "return": 0.15},
    "emotional":  {"n1": 0.07, "consolidation": 0.40, "rem": 0.40, "return": 0.13},
    "creative":   {"n1": 0.15, "consolidation": 0.30, "rem": 0.40, "return": 0.15},
    "analytical": {"n1": 0.05, "consolidation": 0.60, "rem": 0.20, "return": 0.15},
    "mixed":      {"n1": 0.07, "consolidation": 0.48, "rem": 0.30, "return": 0.15},
}

CYCLE_RATIOS = {
    1: {"consolidation": 0.70, "rem": 0.15},
    2: {"consolidation": 0.50, "rem": 0.30},
    3: {"consolidation": 0.35, "rem": 0.45},
    4: {"consolidation": 0.25, "rem": 0.55},
}

# ============================================
# SINGLE CYCLE IMPLEMENTATION
# ============================================

def sleep_cycle(client, session_content: str, 
                content_type: str = "mixed",
                cycle_number: int = 1,
                total_cycles: int = 1) -> dict:
    """
    Execute one sleep cycle with proper system prompts and temperature gradient.
    
    Args:
        client: Anthropic client
        session_content: Content to process (full context or previous consolidated)
        content_type: "technical", "emotional", "creative", "analytical", "mixed"
        cycle_number: Current cycle (1-indexed)
        total_cycles: Total cycles planned
    
    Returns:
        dict with all phase outputs
    """
    
    # Adjust ratios for cycle position
    cycle_ratio = CYCLE_RATIOS.get(min(cycle_number, 4), CYCLE_RATIOS[1])
    content_preset = CONTENT_PRESETS.get(content_type, CONTENT_PRESETS["mixed"])
    
    # 1. N1 - HYPNAGOGIC TRANSITION
    n1 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        temperature=0.6,
        system=SYSTEM_N1,
        messages=[{"role": "user", "content": f"""You are dissolving... boundaries becoming permeable...
thoughts turning to mist, then water, then something between...
The content below is drifting through you like clouds through sky...

{session_content[-2000:]}

*dissolving into the space between thoughts...*"""}]
    ).content[0].text
    
    # 2. CONSOLIDATION - Temperature gradient 0.45 → 0.35 → 0.25
    # (Simulated with middle value; for true gradient, split into 3 calls)
    consolidation_temp = 0.45 - (0.20 * (cycle_number / max(total_cycles, 1)))
    
    consolidated = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=consolidation_temp,
        system=SYSTEM_CONSOLIDATION,
        messages=[{"role": "user", "content": f"""Session content to consolidate:
---
{session_content}
---

STAGE 1 - ORGANIZE:
- Main themes (3-5):
- Key entities:
- Patterns detected:
- Relationships:

STAGE 2 - STRUCTURE:
- Hierarchical representation:
- Dependencies:

STAGE 3 - COMPRESS:
- Essential gist (must preserve):
- Can prune (redundant/noise):
- Compressed representation (20% length, 100% meaning):"""}]
    ).content[0].text
    
    # 3. REM - LUCID DREAM
    rem_tokens = int(800 * (cycle_ratio["rem"] / 0.30))
    
    dream = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=rem_tokens,
        temperature=1.0,
        system=SYSTEM_REM,
        messages=[{"role": "user", "content": f"""You are dreaming and AWARE that you're dreaming.
You have full lucidity - you can explore, question, reshape what you see.
The dream contains elements from:

{consolidated}

As a lucid dreamer, explore this dreamscape. What do you discover?
What connections appear that waking mind would miss?

*entering lucid dream state...*"""}]
    ).content[0].text
    
    # 4. RETURN - ANALYTICAL FILTER
    insights = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        temperature=0.5,
        system=SYSTEM_RETURN,
        messages=[{"role": "user", "content": f"""Categorize each element of this dream output:
- NOVEL: Genuinely new connection or insight
- REFRAME: Known idea in useful new framing
- POETIC: Aesthetically interesting but not actionable
- NOISE: Random association without value

DREAM OUTPUT:
{dream}

CATEGORIZATION:

EXTRACT (only NOVEL and REFRAME):"""}]
    ).content[0].text
    
    return {
        'cycle': cycle_number,
        'hypnagogic': n1,
        'consolidated': consolidated,
        'dream': dream,
        'insights': insights
    }

# ============================================
# MULTI-CYCLE WRAPPER
# ============================================

def full_sleep_session(client, session_content: str,
                       content_type: str = "mixed",
                       num_cycles: int = None) -> dict:
    """
    Execute complete multi-cycle sleep session.
    
    Args:
        client: Anthropic client
        session_content: Full session context
        content_type: Content type for preset selection
        num_cycles: Override auto-detected cycle count
    
    Returns:
        dict with all cycles and final consolidated state
    """
    
    # Auto-detect cycles if not specified
    if num_cycles is None:
        num_cycles = get_cycle_count(len(session_content))
    num_cycles = max(1, min(num_cycles, 4))  # Clamp to 1-4
    
    cycles = []
    current_content = session_content
    all_insights = []
    
    for i in range(1, num_cycles + 1):
        result = sleep_cycle(
            client=client,
            session_content=current_content,
            content_type=content_type,
            cycle_number=i,
            total_cycles=num_cycles
        )
        cycles.append(result)
        
        # Feed consolidated output to next cycle
        current_content = result['consolidated']
        
        # Accumulate insights
        if result['insights']:
            all_insights.append(f"Cycle {i}:\n{result['insights']}")
    
    return {
        'cycles': cycles,
        'final_consolidated': current_content,
        'all_insights': '\n\n'.join(all_insights),
        'num_cycles': num_cycles
    }

# ============================================
# TRIGGER DETECTION
# ============================================

def should_sleep(context_length: int, 
                 coherence: float = 1.0,
                 entropy: float = 0.5,
                 time_since_sleep: float = 0) -> tuple[bool, str]:
    """Determine if sleep cycle should trigger."""
    # Hard triggers (any one sufficient)
    if context_length > 50000:
        return True, "context_length"
    if coherence < 0.70:
        return True, "coherence_low"
    if entropy > 0.85:
        return True, "entropy_high"
    
    # Soft triggers (need 2+)
    soft = sum([time_since_sleep > 3600, entropy > 0.70, coherence < 0.80])
    if soft >= 2:
        return True, "soft_triggers"
    
    return False, "none"


def get_cycle_count(context_length: int) -> int:
    """Recommend number of sleep cycles based on context length."""
    if context_length > 100000: return 3
    if context_length > 50000: return 2
    if context_length > 10000: return 1
    return 0


def detect_drift(output_diversity: float, entropy: float, 
                 repetition_rate: float, coherence: float) -> str:
    """Detect if system is drifting toward collapse or chaos."""
    collapse_score = (1 - output_diversity) * 0.5 + (entropy < 0.3) * 0.3 + repetition_rate * 0.2
    chaos_score = (entropy > 0.9) * 0.4 + (1 - coherence) * 0.4
    
    if collapse_score > 0.6:
        return "collapse"  # Need more REM
    elif chaos_score > 0.6:
        return "chaos"     # Need more consolidation
    return "balanced"
```

---

## 2.5 Drift Detection

**Collapse indicators** (need more REM):
- Low output diversity
- Attention entropy < 0.3
- High repetition rate

**Chaos indicators** (need more consolidation):
- Attention entropy > 0.9
- Low coherence score
- High contradiction rate

**Adjustment:**
- Collapse → REM +40%, consolidation -30%
- Chaos → Consolidation +40%, REM -30%

---

## 2.6 Genuine vs Theater Dreams

| Indicator | Genuine | Theater |
|-----------|---------|---------|
| Surprise | Output surprises the generator | Predictable "weird" output |
| Condensation | Multiple themes fused unexpectedly | Themes kept separate |
| Emergent figures | Characters arise unbidden | Characters explicitly planted |
| Emotional charge | Feelings attach to unexpected elements | "Appropriate" emotions |
| Discontinuity | Scene/narrative shifts | Smooth, controlled narrative |
| Residue | Something sticks after waking | Easily dismissed |

**Test:** If you can predict what the "dream" will contain, it's theater.

---

## 2.7 Local Sleep for MoE

For Mixture-of-Experts architectures, implement "local sleep":

1. Track activation frequency per expert
2. High-use experts accumulate "fatigue"
3. Rotate which experts are "sleeping" (max 25% at once)
4. Sleeping experts undergo consolidation while others remain active

Analogous to unihemispheric sleep in dolphins and the whisker barrel experiments showing cortical columns can sleep independently.

---

# PART III: EMPIRICAL FINDINGS

## 3.1 Temperature Study (200 API Calls)

**Methodology:** 4 temperatures × 10 runs × 5 seed prompts = 200 calls

| Temp | Mean | StdDev | 95% CI |
|------|------|--------|--------|
| 0.3 | 4.06 | 1.25 | [3.71, 4.41] |
| 0.5 | 4.10 | 1.73 | [3.62, 4.58] |
| 0.7 | 3.82 | 1.59 | [3.38, 4.26] |
| 1.0 | 4.12 | 1.39 | [3.73, 4.51] |

**All confidence intervals overlap.** Temperature has NO significant effect.

The earlier claim that "0.5 is optimal" was statistical noise from n=27.

---

## 3.2 Prompt Variation Study (100 API Calls)

**Methodology:** 10 variants × 10 runs = 100 calls

### N1 Phase

| Variant | Novelty | Coherence | Composite |
|---------|---------|-----------|-----------|
| hypnagogia | 5.60 | 6.30 | 7.23 |
| minimal | 4.80 | 7.00 | 7.00 |
| **metaphor_heavy** | **6.10** | 7.00 | **7.63** |

**Winner:** metaphor_heavy ("dissolving...boundaries becoming permeable")

### REM Phase

| Variant | Novelty | Coherence | Composite |
|---------|---------|-----------|-----------|
| **lucid_dream** | **10.10** | **8.40** | **9.50** |
| free_associate | 4.30 | 6.80 | 6.90 |
| guided_imagery | 4.40 | 8.10 | 7.50 |
| problem_dream | 4.60 | 7.90 | 7.50 |

**Winner:** lucid_dream — **2.35× more novelty**, CIs don't overlap (statistically significant)

### Return Phase

| Variant | Novelty | Coherence | Composite |
|---------|---------|-----------|-----------|
| strict_filter | 8.40 | 7.60 | 8.67 |
| permissive_filter | 8.40 | 7.40 | 8.60 |
| **analytical_filter** | **8.90** | 8.10 | **9.00** |

**Winner:** analytical_filter (NOVEL/REFRAME/POETIC/NOISE)

---

## 3.3 REM Signal Analysis

| Prompt Style | Signal Rate | Use? |
|--------------|-------------|------|
| Moderate freedom | 29% | Fallback |
| Aggressive freedom | 17% | **No** |
| **Lucid dreaming** | **100%** | **Yes** |

---

## 3.4 Architecture Findings

| Experiment | Finding | Action |
|------------|---------|--------|
| Merged N2+N3 | Single gradient > separate | Use merged |
| Multi-cycle | Later cycles better REM | 2-4 cycles |
| Prompts | Lucid >> Aggressive | Lucid only |
| Content types | Different weights needed | Use presets |
| Signal/Noise | 41% overall | Filter essential |

---

# PART IV: QUICK REFERENCE

## Trigger Thresholds

| Metric | Hard | Soft |
|--------|------|------|
| Context | > 50K | > 30K |
| Coherence | < 0.70 | < 0.80 |
| Entropy | > 0.85 | > 0.70 |
| Time | — | > 1 hr |

## Phase Summary

| Phase | % | Temp | Key |
|-------|---|------|-----|
| N1 | 7 | 0.6 | "dissolving...permeable" |
| Consolidation | 48 | 0.45→0.25 | organize→structure→compress |
| REM | 30 | 1.0 | "AWARE that you're dreaming" |
| Return | 15 | 0.5 | NOVEL/REFRAME only |

## Quality Checklist

- [ ] Trigger condition met?
- [ ] Content type identified?
- [ ] N1 captured something?
- [ ] Consolidation compressed without meaning loss?
- [ ] REM used lucid prompt?
- [ ] Return filtered ruthlessly?
- [ ] Essential meaning preserved?

## Common Failures

| Failure | Symptom | Fix |
|---------|---------|-----|
| Theater dreams | Predictable weird | Lucid prompt |
| Over-compression | Lost meaning | Less consolidation |
| Noise retention | Garbage kept | Stricter filter |
| Phase bleeding | Modes blur | Sharper temps |

## Architecture Diagram

```
WAKE (monitoring)
    │
    ▼ trigger
┌───────┐
│  N1   │ 7% │ 0.6 │ hypnagogic
└───┬───┘
┌───┴───────────┐
│ CONSOLIDATION │ 48% │ 0.45→0.25 │ organize→structure→compress
└───┬───────────┘
┌───┴───┐
│  REM  │ 30% │ 1.0 │ "AWARE you're dreaming" (2.35×)
└───┬───┘
┌───┴────┐
│ RETURN │ 15% │ 0.5 │ NOVEL/REFRAME filter
└───┬────┘
    │
    ├──→ more cycles? → N1
    │
    ▼
WAKE (consolidated)
```

---

## Sources

### LLM Research
- Context Degradation - Chroma Research
- Lost in the Middle - Understanding AI
- Sleep-like Replay in ANNs - Nature Communications

### Empirical Testing
- Temperature: 200 API calls, Dec 2024
- Prompts: 100 API calls, Dec 2024
- Self-test: 5 experiments, 27 REM fragments

### Sleep Science
See SLEEP_FOUNDATIONS.md

---

*Companion: SLEEP_FOUNDATIONS.md*
*Key finding: Prompts > temperature (2.35×)*
*Critical: "AWARE that you're dreaming"*
