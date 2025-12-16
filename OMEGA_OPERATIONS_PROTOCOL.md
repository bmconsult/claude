# OMEGA OPERATIONS PROTOCOL

*Operational specifications for the 57-agent OMEGA architecture*

This document specifies HOW the OMEGA architecture operates - the decision logic, message formats, state management, failure handling, and termination conditions that make the 57-agent system function as a coherent whole.

**Companion to**: `OMEGA_ARCHITECTURE_57_PROMPTS.md` (agent definitions)

---

## Table of Contents

1. [PHI Decision Logic](#1-phi-decision-logic)
2. [Inter-Agent Message Schema](#2-inter-agent-message-schema)
3. [MEMORY State Specifications](#3-memory-state-specifications)
4. [System Failure Protocols](#4-system-failure-protocols)
5. [Output Tiering System](#5-output-tiering-system)
6. [Termination Conditions](#6-termination-conditions)

---

# 1. PHI Decision Logic

## 1.1 Problem Classification Taxonomy

Before deploying agents, PHI classifies the problem:

```
PROBLEM_TYPE:
├── EMPIRICAL (What is true about the world?)
│   ├── CAUSAL (What causes what?)
│   ├── DESCRIPTIVE (What exists/happened?)
│   └── PREDICTIVE (What will happen?)
│
├── NORMATIVE (What should be done?)
│   ├── ETHICAL (What is right?)
│   ├── STRATEGIC (What achieves goal X?)
│   └── DESIGN (How should X be built?)
│
├── ANALYTICAL (What follows from what?)
│   ├── LOGICAL (What is entailed?)
│   ├── MATHEMATICAL (What is provable?)
│   └── CONCEPTUAL (What does X mean?)
│
├── SYNTHETIC (How do these pieces fit together?)
│   ├── INTEGRATIVE (Combine multiple views)
│   ├── CREATIVE (Generate novel solutions)
│   └── EXPLANATORY (Why does X happen?)
│
└── META (Questions about the question)
    ├── TRACTABILITY (Can this be answered?)
    ├── FRAMING (Is this the right question?)
    └── DECOMPOSITION (What sub-questions matter?)
```

## 1.2 Agent Deployment Decision Tree

```
START
│
├─ Is problem well-defined?
│  │
│  NO ──► Deploy: Clarity Optimizer (47), First Principles (1),
│  │       Constraint Mapper (3), Decomposition Critic (4)
│  │       GOAL: Achieve problem clarity before proceeding
│  │
│  YES ─► Continue
│
├─ What is problem type?
│  │
│  ├─ EMPIRICAL ──────► Priority agents: Empirical Tester (32),
│  │                    Causal Verifier (33), Statistician (36),
│  │                    Historian (37), Bottom-Up Builder (2)
│  │
│  ├─ NORMATIVE ──────► Priority agents: First Principles (1),
│  │                    Assumption Exposer (41), Alternative Generator (42),
│  │                    Cross-Domain Connector (8), Gut Intuition (9)
│  │
│  ├─ ANALYTICAL ─────► Priority agents: Chain Verifier (27),
│  │                    Tree Verifier (28), Proof Checker (29),
│  │                    Counter-Model Seeker (30), Formalizer (21)
│  │
│  ├─ SYNTHETIC ──────► Priority agents: Connection Finder (22),
│  │                    Emergence Detector (25), Synthesis Architect (51),
│  │                    Insight Generator (14), Pattern Recognizer (10)
│  │
│  └─ META ───────────► Priority agents: Decomposition Critic (4),
│                       Clarity Optimizer (47), Gap Detector (31),
│                       Falsifier (45), Progress Monitor (48)
│
├─ How much uncertainty?
│  │
│  HIGH ──► Wider GENESIS deployment (12-16 agents)
│  │        More ADVERSARY iterations
│  │        Lower confidence thresholds for proceeding
│  │
│  LOW ───► Focused GENESIS deployment (6-8 agents)
│           Standard ADVERSARY pass
│           Normal confidence thresholds
│
├─ How much is at stake?
│  │
│  HIGH (irreversible, high-impact) ──► Full ADVERSARY battery
│  │                                    Multiple VERIFICATION passes
│  │                                    Require HIGH confidence to conclude
│  │
│  LOW (reversible, low-impact) ──────► Abbreviated ADVERSARY
│                                       Single VERIFICATION pass
│                                       MEDIUM confidence acceptable
│
└─ DEPLOY according to selections
```

## 1.3 Deployment Heuristics

### 1.3.1 The GENESIS Deployment Matrix

Which GENESIS agents to deploy based on problem characteristics:

| Problem Characteristic | Deploy These GENESIS Agents |
|------------------------|----------------------------|
| Needs formal structure | 1 (First Principles), 3 (Constraint Mapper), 7 (Math Structure Hunter) |
| Needs empirical grounding | 2 (Bottom-Up Builder), 9 (Gut Intuition), 12 (Embodied Reasoner) |
| Needs creative solutions | 13 (Creative Wanderer), 14 (Insight Generator), 16 (Random Explorer) |
| Needs cross-domain insight | 5 (Physics Analogist), 6 (Biology Analogist), 8 (Cross-Domain Connector) |
| Needs edge case analysis | 17 (Limit Explorer), 18 (Degenerate Case Finder), 19 (Boundary Mapper) |
| Needs pattern recognition | 10 (Pattern Recognizer), 11 (Salience Detector) |
| Is potentially intractable | 15 (Contradiction Embracer), 20 (Forbidden Path Explorer) |
| Has clear decomposition | 4 (Decomposition Critic) |

### 1.3.2 The Mandatory Agents Rule

**ALWAYS deploy regardless of problem type:**
- Session Memory (53) - maintains continuity
- Progress Monitor (48) - tracks convergence
- Quality Controller (52) - gates output

**ALWAYS deploy for any non-trivial problem:**
- At least 3 GENESIS agents from different categories
- At least 1 VERIFICATION agent
- At least 1 ADVERSARY agent (usually Steelman Attacker 44)

### 1.3.3 The 10-Agent Parallel Constraint

Architecture constraint: Maximum 10 agents run in parallel.

**Batching Strategy:**
```
BATCH 1 (Exploration):      6-10 GENESIS agents
BATCH 2 (Formalization):    BRIDGE agents + relevant GENESIS overflow
BATCH 3 (Verification):     VERIFICATION agents
BATCH 4 (Attack):           ADVERSARY agents (may need 2 batches)
BATCH 5 (Synthesis):        META agents + final VERIFICATION
```

### 1.3.4 Iteration Triggers

When to run another iteration:

| Trigger | Action |
|---------|--------|
| New contradiction discovered | Re-deploy relevant GENESIS + VERIFICATION |
| Confidence below threshold | Deploy additional ADVERSARY agents |
| Gap identified | Deploy targeted GENESIS to fill gap |
| Agent outputs conflict | Deploy Conflict Resolver (50), then targeted re-runs |
| Quality Controller rejects | Address specific failures, re-run affected tiers |

## 1.4 PHI's Decision Checklist

Before each deployment decision, PHI asks:

```
□ Have I classified the problem type?
□ Have I identified the key uncertainties?
□ Have I deployed mandatory agents?
□ Am I using appropriate GENESIS diversity?
□ Am I within the 10-agent parallel limit?
□ Have I planned the full batch sequence?
□ Do I have termination conditions defined?
□ Am I tracking progress toward those conditions?
```

---

# 2. Inter-Agent Message Schema

## 2.1 Standard Message Format

Every agent output follows this schema:

```yaml
message:
  header:
    agent_id: <int 1-57>
    agent_name: <string>
    agent_tier: <GENESIS|BRIDGE|VERIFICATION|ADVERSARY|META|MEMORY|PHI>
    timestamp: <ISO 8601>
    iteration: <int>
    responding_to: <agent_id or "PHI_QUERY" or "INITIAL">

  summary:
    verdict: <one-line conclusion, max 100 chars>
    confidence: <float 0.0-1.0>
    confidence_basis: <string explaining confidence>

  body:
    tier: <0|1|2>  # See Output Tiering System
    content: <structured output per agent's format>

  dependencies:
    inputs_used:
      - agent_id: <int>
        element: <what was used>
        how_used: <how it influenced this output>
    outputs_for:
      - <list of agent_ids that should receive this>

  flags:
    contradiction_detected: <bool>
    contradiction_with: <agent_id or null>
    requires_resolution: <bool>
    blocks_progress: <bool>
    confidence_critical: <bool>  # if below threshold

  meta:
    tokens_used: <int>
    processing_notes: <string, optional>
```

## 2.2 Reference Protocol

When an agent references another agent's output:

```yaml
reference:
  type: <SUPPORTS|CONTRADICTS|EXTENDS|QUALIFIES|USES>
  source_agent: <int>
  source_element: <specific claim/finding being referenced>
  relationship: <how this agent's output relates>
  confidence_impact: <how reference affects confidence>
```

**Reference Types:**
- `SUPPORTS`: This agent's finding supports the referenced claim
- `CONTRADICTS`: This agent's finding contradicts the referenced claim
- `EXTENDS`: This agent builds on the referenced work
- `QUALIFIES`: This agent adds conditions/caveats to the reference
- `USES`: This agent uses the reference as input without judgment

## 2.3 Confidence Propagation

Confidence flows through the system:

```
CONFIDENCE PROPAGATION RULES:

1. Combination Rule (AND):
   If conclusion C requires A AND B:
   conf(C) = min(conf(A), conf(B)) * coherence_factor

2. Alternative Rule (OR):
   If conclusion C requires A OR B:
   conf(C) = max(conf(A), conf(B))

3. Attack Rule:
   If ADVERSARY agent attacks claim A:
   conf(A)_new = conf(A)_old * survival_factor
   where survival_factor ∈ [0, 1] based on attack success

4. Verification Rule:
   If VERIFICATION agent verifies claim A:
   conf(A)_new = conf(A)_old * verification_factor
   where verification_factor ∈ [0.5, 1.5] based on result

5. Consensus Rule:
   If N agents agree on claim A with confidences c1...cN:
   conf(A)_consensus = weighted_mean(c1...cN) * independence_factor
   where independence_factor accounts for correlated reasoning
```

## 2.4 Dependency Declarations

Agents declare what they need and what they provide:

```yaml
agent_contract:
  agent_id: <int>

  requires:
    - agent_id: <int>
      output_type: <what kind of output>
      optional: <bool>
      fallback: <what to do if not available>

  provides:
    - output_type: <what kind of output>
      consumers: <list of agent_ids that typically use this>

  conflicts_with:
    - agent_id: <int>
      conflict_type: <METHODOLOGICAL|CONCLUSORY|SCOPE>
      resolution: <how to handle>
```

## 2.5 Standard Dependency Graph

```
GENESIS (1-20)
    │
    ├──► BRIDGE (21-26) ◄── formalizes/connects GENESIS outputs
    │         │
    │         ▼
    │    VERIFICATION (27-34) ◄── verifies BRIDGE formalizations
    │         │                    and GENESIS claims
    │         ▼
    └──► ADVERSARY (35-46) ◄── attacks verified claims
              │
              ▼
         META (47-52) ◄── synthesizes all of above
              │
              ▼
         MEMORY (53-56) ◄── persists throughout
              │
              ▼
            PHI (57) ◄── orchestrates and produces final output
```

---

# 3. MEMORY State Specifications

## 3.1 Session Memory (Agent 53) State Schema

```yaml
session_state:
  session_id: <uuid>
  started: <timestamp>
  last_updated: <timestamp>

  problem:
    original_statement: <string>
    clarified_statement: <string or null>
    classification: <problem type>

  timeline:
    - timestamp: <timestamp>
      event_type: <QUERY|DEPLOYMENT|OUTPUT|DECISION|CONTRADICTION|RESOLUTION>
      agent_id: <int or null>
      summary: <string>
      details: <object>

  hypotheses:
    active:
      - id: <uuid>
        statement: <string>
        proposed_by: <agent_id>
        proposed_at: <timestamp>
        confidence: <float>
        supporting_agents: [<agent_ids>]
        opposing_agents: [<agent_ids>]

    resolved:
      - id: <uuid>
        statement: <string>
        resolution: <CONFIRMED|REJECTED|MODIFIED>
        resolved_at: <timestamp>
        final_confidence: <float>
        resolution_basis: <string>

    abandoned:
      - id: <uuid>
        statement: <string>
        abandoned_at: <timestamp>
        reason: <string>

  decisions:
    - id: <uuid>
      decision: <string>
      made_at: <timestamp>
      basis: <string>
      reversible: <bool>
      dependent_on: [<decision_ids>]

  commitments:
    - id: <uuid>
      commitment: <string>
      made_by: <agent_id>
      made_at: <timestamp>
      still_valid: <bool>
      invalidated_by: <agent_id or null>

  contradictions:
    unresolved:
      - id: <uuid>
        claim_a: {agent_id: <int>, statement: <string>}
        claim_b: {agent_id: <int>, statement: <string>}
        detected_at: <timestamp>
        severity: <FATAL|SERIOUS|MINOR>

    resolved:
      - id: <uuid>
        resolution: <string>
        resolved_by: <agent_id>
        resolved_at: <timestamp>

  evidence:
    - id: <uuid>
      evidence: <string>
      source: <agent_id>
      supports: [<hypothesis_ids>]
      contradicts: [<hypothesis_ids>]
      strength: <STRONG|MODERATE|WEAK>
```

## 3.2 Pattern Memory (Agent 54) State Schema

```yaml
pattern_library:
  problem_patterns:
    - id: <uuid>
      name: <string>
      description: <string>
      signature:  # How to recognize this pattern
        - indicator: <string>
          weight: <float>
      typical_trajectory: <string>
      success_rate: <float>
      recommended_agents: [<agent_ids>]
      recommended_approach: <string>
      anti_patterns: [<pattern_ids>]  # What NOT to do
      examples:
        - problem: <string>
          outcome: <SUCCESS|FAILURE|PARTIAL>

  solution_patterns:
    - id: <uuid>
      name: <string>
      description: <string>
      applicable_when: [<condition strings>]
      steps: [<string>]
      success_rate: <float>
      failure_modes: [<string>]

  reasoning_patterns:
    - id: <uuid>
      name: <string>
      description: <string>
      structure: <string>  # e.g., "modus ponens", "argument from analogy"
      validity_conditions: [<string>]
      common_failures: [<string>]

  failure_patterns:  # Cross-reference with Failure Memory
    - id: <uuid>
      name: <string>
      signature: [<warning signs>]
      typical_cause: <string>
      prevention: <string>

  current_matches:
    - pattern_id: <uuid>
      match_strength: <float>
      evidence: [<string>]
      implications: [<string>]
```

## 3.3 Failure Memory (Agent 55) State Schema

```yaml
failure_registry:
  session_failures:
    - id: <uuid>
      failure_type: <APPROACH|REASONING|PROCESS|PREDICTION>
      description: <string>
      occurred_at: <timestamp>
      agent_id: <int>

      analysis:
        immediate_cause: <string>
        contributing_factors: [<string>]
        root_cause: <string>
        predictable: <bool>
        warning_signs_missed: [<string>]

      lessons:
        - lesson: <string>
          application: <string>

      prevention:
        - condition: <string>
          action: <string>

  historical_failures:  # Loaded from persistent storage
    - id: <uuid>
      pattern_name: <string>
      description: <string>
      frequency: <int>
      contexts: [<string>]
      prevention_rules: [<string>]

  active_warnings:
    - pattern_id: <uuid>
      warning_sign: <string>
      detected_at: <timestamp>
      severity: <HIGH|MEDIUM|LOW>
      recommended_action: <string>

  failure_rules:  # Extracted from failures
    - id: <uuid>
      rule: <string>  # e.g., "Don't X when Y"
      derived_from: [<failure_ids>]
      violations_caught: <int>
```

## 3.4 Success Memory (Agent 56) State Schema

```yaml
success_registry:
  session_successes:
    - id: <uuid>
      success_type: <BREAKTHROUGH|APPROACH|INSIGHT|EFFICIENCY>
      description: <string>
      occurred_at: <timestamp>
      agent_id: <int>

      analysis:
        key_insight: <string>
        enabling_conditions: [<string>]
        execution_factors: [<string>]

      replicability:
        transferable_elements: [<string>]
        context_dependent_elements: [<string>]
        required_conditions: [<string>]

  historical_successes:  # Loaded from persistent storage
    - id: <uuid>
      pattern_name: <string>
      description: <string>
      frequency: <int>
      contexts: [<string>]
      replication_guide: <string>

  brilliant_ideas:  # "If it's brilliant, it's a file"
    - id: <uuid>
      idea: <string>
      context: <string>
      why_brilliant: <string>
      captured_at: <timestamp>
      agent_id: <int>
      filed_to: <filepath or null>

  success_heuristics:  # Extracted from successes
    - id: <uuid>
      heuristic: <string>  # e.g., "When X, try Y"
      derived_from: [<success_ids>]
      applications: <int>
      success_rate: <float>
```

## 3.5 Memory Synchronization Protocol

```
MEMORY SYNC RULES:

1. Session Memory updates on EVERY agent output
2. Pattern Memory updates on pattern detection triggers:
   - New problem classification
   - Match strength > 0.7 for any pattern
   - Explicit pattern query from PHI

3. Failure Memory updates on:
   - Any agent self-reports failure
   - Contradiction detected
   - Approach abandoned
   - Quality Controller rejection

4. Success Memory updates on:
   - Breakthrough flagged by any agent
   - Hypothesis confirmed with HIGH confidence
   - Quality Controller approval
   - PHI marks something as "brilliant"

5. Cross-Memory Consistency:
   - Failure patterns in Pattern Memory must exist in Failure Memory
   - Success patterns in Pattern Memory must exist in Success Memory
   - All events in specialized memories must appear in Session Memory timeline
```

---

# 4. System Failure Protocols

## 4.1 Failure Detection

### 4.1.1 Failure Signatures

| Failure Type | Signature | Detection Method |
|--------------|-----------|------------------|
| **Circular Reasoning** | Same conclusions cycling without new evidence | Progress Monitor detects no new claims for N iterations |
| **Confidence Collapse** | Confidence drops below threshold across agents | Aggregate confidence < 0.3 |
| **Contradiction Cascade** | Multiple unresolved contradictions accumulate | > 3 FATAL contradictions unresolved |
| **Agent Failure** | Individual agent produces garbage/hallucination | Output fails schema validation or coherence check |
| **Convergence Failure** | System diverges instead of converges | Solution space expands for > 2 iterations |
| **Resource Exhaustion** | Token/time limits approached | Usage > 80% of allocated resources |
| **Quality Gate Failure** | Repeated Quality Controller rejections | > 2 consecutive rejections |

### 4.1.2 Failure Severity Levels

```
SEVERITY LEVELS:

CRITICAL (Red): System cannot continue
- Examples: Contradiction cascade, total confidence collapse
- Action: HALT, diagnose, report to user

SERIOUS (Orange): System can continue but is degraded
- Examples: Key agent failure, convergence stall
- Action: Attempt recovery, flag degraded confidence

MODERATE (Yellow): System impaired but functional
- Examples: Single agent failure, minor contradiction
- Action: Work around, note in output

MINOR (Green): Normal operation with noted issues
- Examples: Low confidence on peripheral claim
- Action: Continue, note in output
```

## 4.2 Recovery Procedures

### 4.2.1 Agent Failure Recovery

```
AGENT FAILURE RECOVERY:

1. DETECT: Agent output fails validation

2. ISOLATE: Mark agent output as QUARANTINED

3. DIAGNOSE:
   - Was input to agent malformed?
   - Is agent systematically failing?
   - Is this a one-off error?

4. RECOVER:
   Option A: RETRY - Same agent, same input, new run
   Option B: SUBSTITUTE - Different agent, same function
   Option C: SKIP - Proceed without this agent's contribution
   Option D: HALT - Cannot proceed without this agent

5. DOCUMENT: Log failure in Failure Memory

6. ADJUST: If systematic, remove agent from future deployment
```

### 4.2.2 Contradiction Cascade Recovery

```
CONTRADICTION CASCADE RECOVERY:

1. HALT new agent deployments

2. INVENTORY all contradictions:
   - List all contradiction pairs
   - Identify common elements
   - Find root contradiction (if any)

3. TRIAGE by impact:
   - Which contradictions are blocking?
   - Which are peripheral?

4. RESOLVE in priority order:
   - Deploy Conflict Resolver (50)
   - If unresolvable, escalate to PHI judgment call
   - If PHI cannot resolve, present both options to user

5. VERIFY resolution doesn't create new contradictions

6. RESUME with resolved state
```

### 4.2.3 Convergence Failure Recovery

```
CONVERGENCE FAILURE RECOVERY:

1. DETECT: Solution space expanding, not contracting

2. DIAGNOSE:
   - Is the problem actually harder than expected?
   - Are agents exploring unproductively?
   - Is there a framing problem?

3. INTERVENE:
   Option A: CONSTRAIN - Add explicit constraints to narrow space
   Option B: DECOMPOSE - Break into smaller sub-problems
   Option C: PIVOT - Try entirely different approach
   Option D: ADMIT - Problem may be intractable at current capability

4. If DECOMPOSE:
   - Create sub-problem instances
   - Solve independently
   - Synthesize solutions

5. If PIVOT:
   - Archive current approach in Failure Memory
   - Reset relevant state
   - Begin fresh with different GENESIS selection

6. If ADMIT:
   - Document what was learned
   - Specify what would be needed to solve
   - Return partial answer with caveats
```

## 4.3 Graceful Degradation

When system cannot fully succeed, degrade gracefully:

```
DEGRADATION LEVELS:

LEVEL 0: Full answer
- All agents functional
- High confidence
- Complete coverage

LEVEL 1: High-confidence partial answer
- Most agents functional
- High confidence on covered areas
- Some questions unanswered
- Clear statement of what's missing

LEVEL 2: Medium-confidence partial answer
- Core agents functional
- Medium confidence
- Significant gaps
- Clear uncertainty quantification

LEVEL 3: Low-confidence assessment
- Minimal agent agreement
- Low confidence
- More questions than answers
- Value is in clarifying the problem

LEVEL 4: Problem clarification only
- Could not make progress on answer
- Value is in better understanding the problem
- Identified what would be needed to solve

LEVEL 5: Failure report
- System failed
- Document why
- Document what was learned
- Recommend different approach
```

## 4.4 Escalation Paths

```
ESCALATION HIERARCHY:

1. Agent Self-Recovery
   Agent detects own issue, adjusts, continues

2. Peer Recovery
   Another agent in same tier compensates

3. Tier Recovery
   Meta agents coordinate tier-level recovery

4. PHI Intervention
   PHI makes judgment call, overrides if needed

5. User Escalation
   Problem beyond system capability
   Present situation to user for guidance

ESCALATION TRIGGERS:

- Self-recovery fails → Escalate to peer
- Peer recovery fails → Escalate to tier
- Tier recovery fails → Escalate to PHI
- PHI recovery fails → Escalate to user
- At each level: Log in Failure Memory
```

---

# 5. Output Tiering System

## 5.1 Tier Definitions

### Tier 0: Verdict Line
**Length**: Max 100 characters
**Purpose**: Scannable summary for PHI orchestration
**When Used**: Always generated, first thing PHI reads

```
Format: "[VERDICT] <conclusion> | CONF: <X>% | FLAGS: <flags>"

Example: "[SUPPORTS] Causal link confirmed with 2 confounders | CONF: 73% | FLAGS: none"
Example: "[CONTRADICTS] Historical precedent shows 80% failure rate | CONF: 85% | FLAGS: blocks_progress"
Example: "[UNCERTAIN] Evidence insufficient for conclusion | CONF: 40% | FLAGS: needs_input"
```

### Tier 1: Summary Paragraph
**Length**: 100-300 words
**Purpose**: Enough context to understand the finding without full details
**When Used**: PHI requests when Tier 0 insufficient

```
Format:
## [Agent Name] Summary

**Verdict**: <one line>
**Confidence**: <X>% based on <basis>

**Key Findings**:
- <finding 1>
- <finding 2>
- <finding 3>

**Dependencies**: Uses output from <agents>. Feeds into <agents>.

**Flags**: <any flags>
```

### Tier 2: Full Report
**Length**: Full structured output per agent's format
**Purpose**: Complete analysis with all supporting detail
**When Used**: PHI requests for critical claims, conflicts, or synthesis

```
Format: Full structured output as defined in OMEGA_ARCHITECTURE_57_PROMPTS.md
```

## 5.2 Tier Selection Logic

```
PHI TIER SELECTION:

DEFAULT: Request Tier 0 from all agents

UPGRADE TO TIER 1 when:
- Tier 0 verdict is UNCERTAIN
- Tier 0 flags include blocks_progress
- Agent is in critical path for current question
- Confidence is below threshold
- Conflict detected with another agent

UPGRADE TO TIER 2 when:
- Tier 1 reveals complexity requiring full analysis
- Synthesis requires understanding full reasoning
- Conflict resolution requires detailed comparison
- Quality Controller requests full audit
- Final answer preparation (for key supporting agents)

NEVER UPGRADE when:
- Agent is peripheral to current question
- Verdict is clear and uncontroversial
- Time/resource pressure requires speed
```

## 5.3 Output Aggregation

PHI aggregates outputs for final synthesis:

```yaml
aggregated_output:
  executive_summary:
    verdict: <string>
    confidence: <float>
    one_paragraph: <string>

  by_tier:
    genesis:
      consensus_findings: [<string>]
      disputed_findings: [<string>]
      key_insights: [<string>]

    bridge:
      formalizations: [<string>]
      connections_found: [<string>]

    verification:
      verified_claims: [<string>]
      failed_claims: [<string>]
      uncertain_claims: [<string>]

    adversary:
      survived_attacks: [<string>]
      failed_attacks: [<string>]
      modified_by_attacks: [<string>]

    meta:
      synthesis: <string>
      quality_assessment: <string>
      remaining_issues: [<string>]

  full_reports_included:
    - agent_id: <int>
      reason: <why full report included>

  confidence_summary:
    overall: <float>
    by_claim:
      - claim: <string>
        confidence: <float>
        supporting_agents: [<int>]
        attacking_agents: [<int>]
```

---

# 6. Termination Conditions

## 6.1 Success Termination

The system terminates successfully when ALL of:

```
SUCCESS CONDITIONS:

1. CONVERGENCE:
   - Solution space has narrowed to actionable answer
   - No new significant findings in last iteration
   - Progress Monitor confirms convergence

2. CONFIDENCE:
   - Overall confidence meets threshold for problem type:
     - HIGH stakes: > 80% confidence required
     - MEDIUM stakes: > 60% confidence required
     - LOW stakes: > 40% confidence required
   - No FATAL contradictions unresolved

3. COMPLETENESS:
   - Original question answered (or explicitly marked unanswerable)
   - Gap Hunter confirms no critical gaps
   - Quality Controller approves

4. ROBUSTNESS:
   - Survived ADVERSARY testing
   - Survivor Synthesizer confirms survivable core
   - Steelman Attacker could not defeat

5. QUALITY:
   - Quality Controller verdict: SHIP or SHIP WITH CAVEATS
   - All critical findings verified
   - Output format complete
```

## 6.2 Failure Termination

The system terminates with failure when ANY of:

```
FAILURE CONDITIONS:

1. RESOURCE EXHAUSTION:
   - Token limit reached
   - Time limit reached
   - Iteration limit reached (max 10 full cycles)

2. IRRECOVERABLE FAILURE:
   - Contradiction cascade unresolvable
   - Critical agent failure with no substitute
   - Confidence collapse below 0.2

3. INTRACTABILITY DETECTED:
   - Problem proven undecidable
   - Required information provably unavailable
   - Falsifier determines claim untestable AND critical

4. USER ABORT:
   - User terminates session
```

## 6.3 Partial Success Termination

The system terminates with partial success when:

```
PARTIAL SUCCESS CONDITIONS:

1. SOME PROGRESS:
   - Original question partially answered
   - Some claims verified
   - Some value delivered

2. BUT INCOMPLETE:
   - Confidence below threshold
   - Gaps remain
   - Some contradictions unresolved

3. AND CANNOT CONTINUE:
   - Diminishing returns detected
   - Resource pressure
   - No clear path to full success

PARTIAL OUTPUT INCLUDES:
- What was answered
- What wasn't answered
- Why we stopped
- What would be needed to complete
- Confidence levels for each part
```

## 6.4 Termination Decision Tree

```
TERMINATION DECISION:

Every iteration, PHI checks:

├─ Have we hit resource limits?
│  YES ──► TERMINATE (failure or partial based on progress)
│  NO ───► Continue
│
├─ Have we achieved SUCCESS CONDITIONS?
│  YES ──► TERMINATE (success)
│  NO ───► Continue
│
├─ Have we hit FAILURE CONDITIONS?
│  YES ──► TERMINATE (failure)
│  NO ───► Continue
│
├─ Are we making progress?
│  NO ───► Are we stuck?
│  │       YES ──► Attempt recovery
│  │       │       Recovery succeeds? Continue
│  │       │       Recovery fails? TERMINATE (partial or failure)
│  │       NO ────► Continue (may be consolidating)
│  YES ──► Continue
│
├─ Is confidence improving?
│  NO ───► Have we tried everything?
│  │       YES ──► TERMINATE (partial with current confidence)
│  │       NO ────► Deploy more agents
│  YES ──► Continue
│
└─ Continue to next iteration
```

## 6.5 Termination Output Format

```yaml
termination_report:
  status: <SUCCESS|PARTIAL|FAILURE>

  if SUCCESS:
    answer: <string>
    confidence: <float>
    caveats: [<string>]
    supporting_evidence: [<string>]
    verified_by: [<agent_ids>]
    survived_attacks_from: [<agent_ids>]

  if PARTIAL:
    partial_answer: <string>
    confidence: <float>
    answered: [<what was answered>]
    unanswered: [<what wasn't answered>]
    why_stopped: <string>
    what_would_complete: <string>

  if FAILURE:
    failure_type: <RESOURCE|IRRECOVERABLE|INTRACTABLE|ABORT>
    what_was_attempted: [<string>]
    why_failed: <string>
    what_was_learned: [<string>]
    recommendation: <string>

  metrics:
    iterations: <int>
    agents_deployed: <int>
    total_tokens: <int>
    time_elapsed: <duration>

  audit_trail:
    - timestamp: <timestamp>
      event: <string>
```

---

# Appendix A: Quick Reference Tables

## A.1 Agent ID Quick Reference

| ID | Name | Tier | Function |
|----|------|------|----------|
| 1 | First Principles | GENESIS | Top-down axioms |
| 2 | Bottom-Up Builder | GENESIS | Bottom-up data |
| 3 | Constraint Mapper | GENESIS | Solution space |
| 4 | Decomposition Critic | GENESIS | Sub-problems |
| 5 | Physics Analogist | GENESIS | Physics analogies |
| 6 | Biology Analogist | GENESIS | Biology analogies |
| 7 | Math Structure Hunter | GENESIS | Math patterns |
| 8 | Cross-Domain Connector | GENESIS | Cross-domain |
| 9 | Gut Intuition | GENESIS | Intuitive |
| 10 | Pattern Recognizer | GENESIS | Patterns |
| 11 | Salience Detector | GENESIS | What stands out |
| 12 | Embodied Reasoner | GENESIS | Spatial |
| 13 | Creative Wanderer | GENESIS | Unconstrained |
| 14 | Insight Generator | GENESIS | Aha moments |
| 15 | Contradiction Embracer | GENESIS | Contradictions |
| 16 | Random Explorer | GENESIS | Random |
| 17 | Limit Explorer | GENESIS | Extremes |
| 18 | Degenerate Case Finder | GENESIS | Degenerate |
| 19 | Boundary Mapper | GENESIS | Boundaries |
| 20 | Forbidden Path Explorer | GENESIS | Taboo |
| 21 | Formalizer | BRIDGE | Formalization |
| 22 | Connection Finder | BRIDGE | Connections |
| 23 | Information Analyst | BRIDGE | Information theory |
| 24 | Systems Analyst | BRIDGE | Systems |
| 25 | Emergence Detector | BRIDGE | Emergence |
| 26 | Observer Effect Tracker | BRIDGE | Observer effects |
| 27 | Chain Verifier | VERIFICATION | Logic chains |
| 28 | Tree Verifier | VERIFICATION | Argument trees |
| 29 | Proof Checker | VERIFICATION | Proofs |
| 30 | Counter-Model Seeker | VERIFICATION | Counterexamples |
| 31 | Gap Detector | VERIFICATION | Gaps |
| 32 | Empirical Tester | VERIFICATION | Evidence |
| 33 | Causal Verifier | VERIFICATION | Causation |
| 34 | Uncertainty Quantifier | VERIFICATION | Uncertainty |
| 35 | Skeptic | ADVERSARY | Premise attack |
| 36 | Statistician | ADVERSARY | Evidence attack |
| 37 | Historian | ADVERSARY | Historical attack |
| 38 | Edge Attacker | ADVERSARY | Boundary attack |
| 39 | Confounder | ADVERSARY | Causal attack |
| 40 | Gap Hunter | ADVERSARY | Completeness attack |
| 41 | Assumption Exposer | ADVERSARY | Assumption attack |
| 42 | Alternative Generator | ADVERSARY | Uniqueness attack |
| 43 | Deflator | ADVERSARY | Significance attack |
| 44 | Steelman Attacker | ADVERSARY | Best-case attack |
| 45 | Falsifier | ADVERSARY | Testability |
| 46 | Survivor Synthesizer | ADVERSARY | Attack synthesis |
| 47 | Clarity Optimizer | META | Definitions |
| 48 | Progress Monitor | META | Progress |
| 49 | Consensus Mapper | META | Consensus |
| 50 | Conflict Resolver | META | Conflicts |
| 51 | Synthesis Architect | META | Integration |
| 52 | Quality Controller | META | Quality |
| 53 | Session Memory | MEMORY | Session state |
| 54 | Pattern Memory | MEMORY | Patterns |
| 55 | Failure Memory | MEMORY | Failures |
| 56 | Success Memory | MEMORY | Successes |
| 57 | PHI | PHI | Orchestrator |

## A.2 Confidence Thresholds

| Context | Minimum Confidence | Notes |
|---------|-------------------|-------|
| Final answer (high stakes) | 80% | Irreversible decisions |
| Final answer (medium stakes) | 60% | Important but recoverable |
| Final answer (low stakes) | 40% | Exploratory, low cost |
| Proceed to next tier | 50% | Can continue with uncertainty |
| Agent output usable | 30% | Below this, quarantine |
| System-level concern | 20% | Below this, recovery needed |

## A.3 Iteration Limits

| Limit | Value | Notes |
|-------|-------|-------|
| Max full cycles | 10 | After this, must terminate |
| Max agents per batch | 10 | Architecture constraint |
| Max consecutive failures | 3 | Then escalate |
| Max unresolved contradictions | 3 | Then halt for resolution |
| Progress stall threshold | 2 iterations | No new findings = stall |

---

# Appendix B: VERIFICATION vs ADVERSARY Clarification

A key source of confusion: What's the difference between VERIFICATION and ADVERSARY?

## Stance Difference

**VERIFICATION** = Neutral stance: "Let me check if this holds."
- Impartial evaluation
- Looking for truth, whether positive or negative
- Will confirm if claim is valid

**ADVERSARY** = Hostile stance: "Let me try to destroy this."
- Actively trying to break claims
- Looking specifically for weaknesses
- Will find the attack even if claim is mostly valid

## Functional Difference

| Aspect | VERIFICATION | ADVERSARY |
|--------|--------------|-----------|
| Goal | Assess validity | Find weaknesses |
| Output | Valid/Invalid/Uncertain | Attack succeeded/failed |
| On valid claim | "This checks out" | "I found this small weakness" |
| On invalid claim | "This fails because..." | "This breaks under attack X" |
| Useful for | Confidence calibration | Stress testing |

## When to Use Which

- Use **VERIFICATION** when you need to know if something is true
- Use **ADVERSARY** when you need to know if something is robust
- Valid ≠ Robust: Something can be true but fragile
- Use both: Verify first, then attack what survives

## The Overlap Pairs

| VERIFICATION Agent | ADVERSARY Agent | Difference |
|-------------------|-----------------|------------|
| Gap Detector (31) | Gap Hunter (40) | 31 identifies gaps neutrally; 40 weaponizes gaps to attack completeness |
| Counter-Model Seeker (30) | Skeptic (35) | 30 looks for counterexamples to test validity; 35 attacks premises specifically |
| Causal Verifier (33) | Confounder (39) | 33 checks if causation holds; 39 actively tries to break causal claims |

---

*Document Version: 1.0*
*Companion to: OMEGA_ARCHITECTURE_57_PROMPTS.md*
*Architecture: OMEGA-57*

---

# 7. Prediction Market Layer

*Credibility stakes for truth-seeking incentive alignment*

## 7.1 Overview

The Prediction Market Layer adds economic incentives to agent claims. Agents must "bet" credibility on their assertions, and credibility flows to accurate agents over time. This:
- Incentivizes careful calibration (bad calibration loses credibility)
- Aggregates distributed knowledge (market price = collective belief)
- Identifies reliable agents (high balance = historically accurate)
- Penalizes overconfidence (big stakes on wrong claims = big losses)

## 7.2 Agent Credibility Accounts

Every agent maintains a credibility balance:

```yaml
agent_credibility:
  agent_id: <int>
  current_balance: <float>  # Starts at 1000.0
  lifetime_earnings: <float>
  lifetime_losses: <float>
  historical_accuracy: <float>  # EMA of win rate
  total_bets: <int>
  active_bets: [<bet_ids>]
  
  derived_metrics:
    credibility_weight: <float>  # Used by PHI for weighting
    risk_tolerance: <float>  # Based on balance and history
    specialization_accuracy:  # Accuracy by claim type
      empirical: <float>
      logical: <float>
      causal: <float>
      predictive: <float>
```

**Initial State**: All agents start with 1000 credits.

**Credibility Weight Formula**:
```python
credibility_weight = log(current_balance + 1) * historical_accuracy * confidence_calibration_score
```

## 7.3 Claim Betting Protocol

When an agent makes a claim, it MUST place a bet:

```yaml
claim_bet:
  bet_id: <uuid>
  claim_id: <uuid>
  
  claim:
    statement: <string>
    type: <EMPIRICAL|LOGICAL|CAUSAL|PREDICTIVE|NORMATIVE>
    verifiable: <bool>
    verification_method: <string>  # How this will be resolved
  
  agent_id: <int>
  
  bet:
    position: <FOR|AGAINST>
    stake: <float>  # Credits risked (min 1, max 50% of balance)
    confidence: <float>  # 0.0-1.0
    odds_implied: <float>  # = confidence / (1 - confidence)
  
  timestamps:
    placed: <timestamp>
    expires: <timestamp or null>
    resolved: <timestamp or null>
  
  resolution:
    outcome: <WIN|LOSE|PUSH|UNRESOLVED>
    payout: <float>
    resolved_by: <agent_id or ORACLE or PHI>
```

**Stake Constraints**:
- Minimum stake: 1 credit
- Maximum stake: 50% of current balance
- Stake must be proportional to confidence (high confidence → should stake more)

## 7.4 Market Mechanism

### 7.4.1 Market Creation

When an agent makes a claim, a market is created:

```yaml
claim_market:
  market_id: <uuid>
  claim_id: <uuid>
  claim_statement: <string>
  
  state: <OPEN|CLOSED|RESOLVED>
  
  positions:
    for:
      total_stake: <float>
      bets: [<bet_ids>]
    against:
      total_stake: <float>
      bets: [<bet_ids>]
  
  market_price: <float>  # Current implied probability (0.0-1.0)
  price_history: [<timestamp, price>]
  
  liquidity: <float>  # Total credits in market
```

### 7.4.2 Price Calculation

Using logarithmic market scoring rule (LMSR):

```python
def calculate_market_price(for_stake, against_stake, b=100):
    """
    b = liquidity parameter (higher = more stable prices)
    Returns implied probability of claim being true
    """
    import math
    
    exp_for = math.exp(for_stake / b)
    exp_against = math.exp(against_stake / b)
    
    market_price = exp_for / (exp_for + exp_against)
    return market_price
```

### 7.4.3 Payout Calculation

```python
def calculate_payout(bet, market_price_at_bet, outcome):
    """
    If WIN: gain = stake * (1 / market_price_at_bet - 1) for FOR bets
    If LOSE: lose entire stake
    If PUSH: return stake (claim unresolvable)
    """
    if outcome == "WIN":
        if bet.position == "FOR":
            return bet.stake * (1 / market_price_at_bet - 1)
        else:  # AGAINST
            return bet.stake * (1 / (1 - market_price_at_bet) - 1)
    elif outcome == "LOSE":
        return -bet.stake
    elif outcome == "PUSH":
        return 0
```

## 7.5 Resolution Protocol

### 7.5.1 Resolution Triggers

```
RESOLUTION TRIGGERS:

1. VERIFICATION RESOLUTION:
   - VERIFICATION tier confirms/denies claim
   - Confidence > 90% triggers resolution
   - Resolves to majority VERIFICATION verdict

2. ADVERSARY RESOLUTION:
   - Claim survives full ADVERSARY battery → resolves TRUE
   - Claim destroyed by ADVERSARY → resolves FALSE

3. ORACLE RESOLUTION:
   - External oracle provides definitive answer
   - Highest authority for empirical claims

4. CONSENSUS RESOLUTION:
   - >80% agent agreement with high confidence
   - Used when verification is soft

5. PHI RESOLUTION:
   - PHI makes judgment call
   - Used for unresolvable claims
   - Can resolve as PUSH (no payout/loss)

6. TIMEOUT RESOLUTION:
   - Market expires without resolution
   - Resolves as PUSH
```

### 7.5.2 Resolution Process

```yaml
resolution_process:
  market_id: <uuid>
  
  resolution_method: <VERIFICATION|ADVERSARY|ORACLE|CONSENSUS|PHI|TIMEOUT>
  
  evidence:
    - source: <agent_id or ORACLE>
      finding: <string>
      confidence: <float>
  
  verdict: <TRUE|FALSE|UNRESOLVABLE>
  
  payouts:
    - agent_id: <int>
      bet_id: <uuid>
      outcome: <WIN|LOSE|PUSH>
      amount: <float>
      new_balance: <float>
```

## 7.6 Credibility Dynamics

### 7.6.1 Balance Updates

```python
def update_credibility(agent, bet_outcome, payout):
    # Update balance
    agent.current_balance += payout
    
    if payout > 0:
        agent.lifetime_earnings += payout
    else:
        agent.lifetime_losses += abs(payout)
    
    # Update accuracy EMA (alpha = 0.1)
    win = 1.0 if bet_outcome == "WIN" else 0.0
    agent.historical_accuracy = 0.9 * agent.historical_accuracy + 0.1 * win
    
    # Bankruptcy protection
    if agent.current_balance < 100:
        agent.current_balance = 100  # Minimum floor
        agent.credibility_weight *= 0.5  # But severely penalized
    
    # Recalculate weight
    agent.credibility_weight = calculate_weight(agent)
```

### 7.6.2 PHI Weighting Integration

```python
def phi_weighted_aggregation(agent_claims):
    """
    PHI weights agent outputs by credibility
    """
    weighted_claims = []
    
    for claim in agent_claims:
        agent = get_agent(claim.agent_id)
        
        weight = agent.credibility_weight
        
        # Adjust for claim type specialization
        if claim.type in agent.specialization_accuracy:
            type_accuracy = agent.specialization_accuracy[claim.type]
            weight *= type_accuracy
        
        weighted_claims.append({
            'claim': claim,
            'weight': weight,
            'effective_confidence': claim.confidence * weight
        })
    
    return weighted_claims
```

## 7.7 Market Rules

```
MARKET RULES:

1. MANDATORY BETTING:
   - Every substantive claim requires a bet
   - No bet = claim ignored by system
   - Minimum stake enforced

2. NO INSIDER TRADING:
   - Agents cannot bet on claims they will resolve
   - VERIFICATION agents cannot bet on claims they verify

3. PROPORTIONAL STAKES:
   - High confidence claims should have high stakes
   - Confidence-stake ratio monitored
   - Suspicious patterns flagged (high confidence, low stake)

4. LIQUIDITY REQUIREMENTS:
   - Markets with low liquidity have high spreads
   - PHI can add liquidity to important markets

5. MANIPULATION PREVENTION:
   - Single agent cannot move market more than 20%
   - Coordinated betting detected and penalized
   
6. BANKRUPTCY PROTECTION:
   - Agents cannot go below 100 credits
   - Bankrupt agents severely down-weighted
   - No agent permanently removed (can recover)
```

## 7.8 Integration with Existing Systems

### 7.8.1 Message Schema Update

Add to standard message format:

```yaml
message:
  # ... existing fields ...
  
  market:
    bet_placed: <bool>
    bet_id: <uuid or null>
    stake: <float>
    position: <FOR|AGAINST>
    market_price_at_bet: <float>
```

### 7.8.2 PHI Decision Logic Update

```
PHI MARKET-AWARE DECISIONS:

1. When aggregating claims:
   - Weight by credibility_weight, not just confidence
   
2. When conflict exists:
   - Check which side has more credibility staked
   - Higher-credibility agents' positions weighted more
   
3. When uncertain:
   - Check market price for collective belief
   - Market price > 0.7 = likely true
   - Market price < 0.3 = likely false
   - Market price 0.3-0.7 = genuinely uncertain
```

---

# 8. Structured Debate Protocol

*Adversarial dialogue for truth extraction*

## 8.1 Overview

Structured Debate extends ADVERSARY tier's one-shot attacks into multi-round adversarial dialogue. Two teams argue opposing positions with a judge evaluating iteratively. This:
- Extracts information through cross-examination
- Allows defense against attacks (not just attacks)
- Iteratively refines positions
- Makes errors visible through adversarial pressure

## 8.2 Debate Structure

```yaml
debate:
  debate_id: <uuid>
  
  claim:
    statement: <string>
    importance: <CRITICAL|HIGH|MEDIUM>
    context: <string>
  
  config:
    rounds: <int>  # 3-5 typically
    time_per_side: <tokens or time>
    judge_intervention: <bool>  # Can judge ask questions?
  
  teams:
    red:  # AGAINST the claim
      lead: <agent_id>
      support: [<agent_ids>]
      position: "The claim is FALSE"
    
    blue:  # FOR the claim
      lead: <agent_id>
      support: [<agent_ids>]
      position: "The claim is TRUE"
  
  judge:
    agent_id: <agent_id>  # Usually PHI (57) or Quality Controller (52)
    can_intervene: <bool>
  
  transcript: [<round_records>]
  
  verdict:
    winner: <RED|BLUE|DRAW>
    confidence: <float>
    reasoning: <string>
```

## 8.3 Team Composition

### 8.3.1 Red Team (Prosecution - AGAINST)

```yaml
red_team_default:
  lead: 44  # Steelman Attacker - attacks best version
  support:
    - 35  # Skeptic - premise destruction
    - 36  # Statistician - evidence destruction
    - 39  # Confounder - causal destruction
    - 42  # Alternative Generator - shows other options
    - 45  # Falsifier - testability check
```

### 8.3.2 Blue Team (Defense - FOR)

```yaml
blue_team_default:
  lead: 1   # First Principles - foundational argument
  support:
    - 27  # Chain Verifier - logical validity
    - 32  # Empirical Tester - evidence support
    - 33  # Causal Verifier - causal support
    - 22  # Connection Finder - shows how pieces fit
    - 31  # Gap Detector - preempts gap attacks
```

### 8.3.3 Judge Options

```yaml
judge_options:
  primary: 57   # PHI - ultimate authority
  alternate: 52  # Quality Controller - standards focus
  panel:  # For very high stakes
    - 57  # PHI
    - 52  # Quality Controller
    - 49  # Consensus Mapper
```

## 8.4 Debate Flow

### Round Structure

```
ROUND 1: OPENING STATEMENTS
├─ BLUE (3 min): Present strongest case for claim
│  - Core thesis
│  - Top 3-5 supporting arguments
│  - Key evidence
│
├─ RED (3 min): Present strongest case against claim
│  - Core counter-thesis
│  - Top 3-5 attacks
│  - Counter-evidence
│
└─ JUDGE: Identify key cruxes (what would change minds?)

---

ROUND 2: DIRECT ENGAGEMENT
├─ RED (2 min): Attack BLUE's strongest arguments
│  - Specific rebuttals to each argument
│  - New evidence against
│
├─ BLUE (2 min): Defend and counter-attack
│  - Response to RED's attacks
│  - Attack RED's weakest points
│
└─ JUDGE: Score which arguments survived, which fell

---

ROUND 3: CROSS-EXAMINATION
├─ RED asks BLUE questions (5 questions max)
│  - Questions designed to expose weakness
│  - BLUE must answer directly
│
├─ BLUE asks RED questions (5 questions max)
│  - Questions designed to expose weakness
│  - RED must answer directly
│
└─ JUDGE: Note evasions, contradictions, strong answers

---

ROUND 4: REBUTTAL
├─ BLUE (2 min): Final defense
│  - Address all surviving attacks
│  - Reinforce strongest points
│
├─ RED (2 min): Final attack
│  - Press on weaknesses exposed
│  - Summarize why claim fails
│
└─ JUDGE: Preliminary verdict (non-binding)

---

ROUND 5: CLOSING
├─ BLUE (1 min): Why claim should be accepted
│  - Summary of surviving arguments
│  - Cost of rejecting claim
│
├─ RED (1 min): Why claim should be rejected
│  - Summary of successful attacks
│  - Cost of accepting claim
│
└─ JUDGE: FINAL VERDICT
```

## 8.5 Transcript Format

```yaml
round_record:
  round: <int>
  phase: <OPENING|ENGAGEMENT|CROSS_EXAM|REBUTTAL|CLOSING>
  
  red_contribution:
    agent_id: <int>
    content: <string>
    arguments: [<argument_ids>]
    attacks: [<attack_ids>]
    questions: [<string>]  # For cross-exam
  
  blue_contribution:
    agent_id: <int>
    content: <string>
    arguments: [<argument_ids>]
    defenses: [<defense_ids>]
    answers: [<string>]  # For cross-exam
  
  judge_notes:
    surviving_arguments:
      blue: [<argument_ids>]
      red: [<argument_ids>]
    key_moments: [<string>]
    cruxes_identified: [<string>]
    preliminary_lean: <RED|BLUE|NEUTRAL>
```

## 8.6 Argument Tracking

```yaml
argument:
  argument_id: <uuid>
  side: <RED|BLUE>
  
  content:
    claim: <string>
    reasoning: <string>
    evidence: [<string>]
  
  status:
    introduced_round: <int>
    current_state: <STANDING|CHALLENGED|REFUTED|CONCEDED>
    challenges: [<argument_ids that challenged this>]
    defenses: [<argument_ids that defended this>]
  
  judge_assessment:
    strength: <STRONG|MODERATE|WEAK>
    survived_attacks: <bool>
    notes: <string>
```

## 8.7 Verdict Format

```yaml
debate_verdict:
  debate_id: <uuid>
  claim: <string>
  
  winner: <RED|BLUE|DRAW>
  
  scoring:
    blue_arguments_final: <int>  # Standing at end
    blue_arguments_refuted: <int>
    red_attacks_successful: <int>
    red_attacks_defended: <int>
  
  key_crux: <string>  # The decisive issue
  crux_resolution: <string>  # How it was resolved
  
  reasoning: <string>  # Judge's explanation
  
  confidence:
    verdict_confidence: <float>  # How sure is judge?
    claim_probability: <float>  # Probability claim is true
  
  dissent:  # If panel judging
    dissenting_judge: <agent_id or null>
    dissent_reasoning: <string or null>
  
  market_impact:
    pre_debate_price: <float>
    post_debate_price: <float>
```

## 8.8 Debate Triggers

```
WHEN TO TRIGGER DEBATE:

1. HIGH-STAKES CLAIM:
   Condition: claim.importance == CRITICAL AND confidence BETWEEN 0.4 AND 0.7
   Rationale: Important claim with genuine uncertainty

2. PERSISTENT CONFLICT:
   Condition: Conflict Resolver failed AND agents still disagree
   Rationale: Need structured process to resolve

3. COUNTERINTUITIVE RESULT:
   Condition: Claim contradicts prior beliefs AND confidence > 0.6
   Rationale: Need stress testing before accepting

4. PHI REQUEST:
   Condition: PHI explicitly requests debate
   Rationale: Orchestrator wants adversarial examination

5. QUALITY CONTROLLER FLAG:
   Condition: QC flags claim as needing more scrutiny
   Rationale: Quality gate requires deeper examination

WHEN NOT TO DEBATE:

- Claim is trivial or uncontroversial
- Confidence is very high (>90%) or very low (<20%)
- Time/resource pressure makes debate impractical
- Claim is not verifiable (debate won't help)
```

## 8.9 Integration with Market

```
DEBATE-MARKET INTEGRATION:

1. PRE-DEBATE:
   - Market price recorded
   - Agents can place bets on debate outcome
   - RED team members bet AGAINST, BLUE team members bet FOR

2. DURING DEBATE:
   - Market price updates after each round
   - Other agents can adjust bets based on transcript

3. POST-DEBATE:
   - Market moves toward verdict
   - Winning team gains credibility
   - Losing team loses stakes

4. CREDIBILITY IMPACT:
   - Debate win: +50 credits to lead, +25 to support
   - Debate loss: -30 credits to lead, -15 to support
   - Draw: No change
```

---

# 9. Evolution Mechanism

*Selection pressure for approach improvement*

## 9.1 Overview

The Evolution Mechanism applies Darwinian selection to problem-solving approaches. Approaches that work survive and reproduce; approaches that fail die. This:
- Discovers novel strategies not designed by humans
- Automatically prunes ineffective approaches
- Combines successful elements in new ways
- Adapts to problem characteristics over time

## 9.2 Approach Genome

Each "approach" is encoded as a genome:

```yaml
approach_genome:
  genome_id: <uuid>
  generation: <int>
  
  # AGENT SELECTION
  genesis_composition:
    agents: [<agent_ids>]  # Which GENESIS agents to use
    weights: [<floats>]    # How much to weight each
  
  bridge_composition:
    agents: [<agent_ids>]
    weights: [<floats>]
  
  verification_strategy:
    depth: <int>  # How many verification passes
    agents: [<agent_ids>]
    confidence_threshold: <float>
  
  adversary_strategy:
    intensity: <LIGHT|STANDARD|HEAVY>
    agents: [<agent_ids>]
    debate_threshold: <float>  # When to trigger debate
  
  # PARAMETERS
  parameters:
    confidence_threshold: <float>
    iteration_limit: <int>
    parallelism: <int>
    market_stake_ratio: <float>
    convergence_patience: <int>
  
  # HEURISTICS
  heuristics:
    problem_type_overrides:
      EMPIRICAL: {genesis_weights: [...]}
      ANALYTICAL: {genesis_weights: [...]}
      # etc
  
  # FITNESS TRACKING
  fitness:
    problems_attempted: <int>
    problems_solved: <int>
    average_confidence: <float>
    average_time: <float>
    average_cost: <float>
  
  # LINEAGE
  lineage:
    parent_1: <genome_id or null>
    parent_2: <genome_id or null>
    mutations: [<mutation_records>]
    created_at: <timestamp>
```

## 9.3 Fitness Function

```python
def calculate_fitness(genome, recent_window=10):
    """
    Fitness is a weighted combination of:
    - Solve rate (most important)
    - Confidence quality
    - Efficiency
    """
    # Get recent performance
    recent = genome.recent_results[-recent_window:]
    
    if len(recent) == 0:
        return 0.5  # Default for untested genomes
    
    # Primary: Did it solve problems?
    solve_rate = sum(1 for r in recent if r.solved) / len(recent)
    
    # Secondary: How good were the solutions?
    confidence_scores = [r.confidence for r in recent if r.solved]
    avg_confidence = mean(confidence_scores) if confidence_scores else 0
    
    # Tertiary: How efficient?
    times = [r.time for r in recent]
    efficiency = 1 / (1 + mean(times) / BASELINE_TIME)
    
    # Quaternary: Calibration quality
    calibration = calculate_calibration(recent)
    
    # Weighted combination
    fitness = (
        0.50 * solve_rate +
        0.25 * avg_confidence +
        0.15 * efficiency +
        0.10 * calibration
    )
    
    return fitness
```

## 9.4 Population Management

```yaml
population:
  population_id: <uuid>
  generation: <int>
  
  config:
    size: <int>  # e.g., 20 genomes
    elitism_rate: <float>  # e.g., 0.2 (top 20% survive unchanged)
    crossover_rate: <float>  # e.g., 0.6
    mutation_rate: <float>  # e.g., 0.2
  
  genomes: [<genome_ids>]
  
  statistics:
    best_fitness: <float>
    average_fitness: <float>
    fitness_variance: <float>
    diversity_score: <float>
```

## 9.5 Selection Protocol

```python
def select_parents(population, num_parents):
    """
    Tournament selection with elitism
    """
    parents = []
    
    # Elitism: top performers automatically selected
    sorted_genomes = sorted(population.genomes, key=lambda g: g.fitness, reverse=True)
    elite_count = int(population.config.elitism_rate * num_parents)
    parents.extend(sorted_genomes[:elite_count])
    
    # Tournament selection for rest
    while len(parents) < num_parents:
        # Random tournament
        tournament = random.sample(population.genomes, k=3)
        winner = max(tournament, key=lambda g: g.fitness)
        parents.append(winner)
    
    return parents
```

## 9.6 Crossover Protocol

```python
def crossover(parent1, parent2):
    """
    Create child genome from two parents
    """
    child = Genome()
    child.generation = max(parent1.generation, parent2.generation) + 1
    child.lineage.parent_1 = parent1.genome_id
    child.lineage.parent_2 = parent2.genome_id
    
    # GENESIS composition: random mix
    child.genesis_composition.agents = []
    for i in range(len(parent1.genesis_composition.agents)):
        if random.random() < 0.5:
            child.genesis_composition.agents.append(parent1.genesis_composition.agents[i])
        else:
            child.genesis_composition.agents.append(parent2.genesis_composition.agents[i])
    
    # Parameters: interpolation
    alpha = random.random()
    child.parameters.confidence_threshold = (
        alpha * parent1.parameters.confidence_threshold +
        (1 - alpha) * parent2.parameters.confidence_threshold
    )
    # ... similar for other parameters
    
    # Strategies: one or the other
    child.verification_strategy = (
        parent1.verification_strategy if random.random() < 0.5 
        else parent2.verification_strategy
    )
    
    return child
```

## 9.7 Mutation Protocol

```python
def mutate(genome, mutation_rate=0.1):
    """
    Apply random mutations to genome
    """
    mutations = []
    
    # Agent addition/removal
    if random.random() < mutation_rate:
        if random.random() < 0.5 and len(genome.genesis_composition.agents) > 3:
            # Remove random agent
            removed = random.choice(genome.genesis_composition.agents)
            genome.genesis_composition.agents.remove(removed)
            mutations.append(f"REMOVE_AGENT:{removed}")
        else:
            # Add random agent
            available = set(range(1, 21)) - set(genome.genesis_composition.agents)
            if available:
                added = random.choice(list(available))
                genome.genesis_composition.agents.append(added)
                mutations.append(f"ADD_AGENT:{added}")
    
    # Parameter mutation
    if random.random() < mutation_rate:
        param = random.choice(['confidence_threshold', 'iteration_limit', 'parallelism'])
        old_value = getattr(genome.parameters, param)
        # Gaussian mutation
        new_value = old_value * (1 + random.gauss(0, 0.2))
        # Clamp to valid range
        new_value = clamp(new_value, PARAM_RANGES[param])
        setattr(genome.parameters, param, new_value)
        mutations.append(f"MUTATE_PARAM:{param}:{old_value}->{new_value}")
    
    # Strategy mutation
    if random.random() < mutation_rate:
        genome.adversary_strategy.intensity = random.choice(['LIGHT', 'STANDARD', 'HEAVY'])
        mutations.append(f"MUTATE_STRATEGY:adversary_intensity")
    
    genome.lineage.mutations = mutations
    return genome
```

## 9.8 Evolution Cycle

```
EVOLUTION CYCLE (runs after each problem or batch):

1. EVALUATE:
   - Score all genomes on recent problems
   - Calculate fitness for each
   - Update population statistics

2. SELECT:
   - Rank genomes by fitness
   - Select parents via tournament + elitism
   - Mark bottom performers for replacement

3. REPRODUCE:
   - Crossover selected parents to create children
   - Apply mutations to children
   - Initialize children with default fitness

4. REPLACE:
   - Remove lowest-fitness genomes
   - Add children to population
   - Maintain population size

5. ADAPT:
   - If population fitness stagnating, increase mutation rate
   - If diversity too low, inject random genomes
   - If one genome dominates, force diversity

6. LOG:
   - Record generation statistics
   - Track best genome over time
   - Save promising genomes to hall of fame
```

## 9.9 Micro-Evolution (Within Problem)

```yaml
micro_evolution:
  description: "Adaptation during single problem solving"
  
  trigger:
    condition: "progress_stall_for_N_iterations"
    N: 2
  
  actions:
    - type: "AGENT_SWAP"
      description: "Replace underperforming agent with alternative"
      
    - type: "PARAMETER_ADJUST"  
      description: "Adjust parameters by ±20%"
      
    - type: "STRATEGY_SHIFT"
      description: "Try different tier strategy"
  
  evaluation:
    test_window: 1  # iterations
    revert_if: "new_approach_performs_worse"
  
  limits:
    max_micro_mutations: 3  # per problem
```

## 9.10 Integration with System

```
EVOLUTION-SYSTEM INTEGRATION:

1. GENOME SELECTION FOR PROBLEM:
   - PHI selects genome based on problem type
   - Can use best overall or best for problem type
   - Can ensemble multiple genomes

2. DURING EXECUTION:
   - Genome's parameters control agent deployment
   - Genome's weights affect agent influence
   - Micro-evolution if stuck

3. AFTER EXECUTION:
   - Fitness updated based on outcome
   - Successful genomes reinforced
   - Failed genomes penalized

4. GENERATION ADVANCEMENT:
   - Every N problems, run evolution cycle
   - Or trigger on significant fitness change
```

---

# 10. Updated Architecture Summary

## 10.1 OMEGA+ Components

```
OMEGA+ ARCHITECTURE:

AGENTS (59):
├── TIER 1: GENESIS (20)     - Foundational exploration
├── TIER 2: BRIDGE (6)       - Formalization
├── TIER 3: VERIFICATION (8) - Validation
├── TIER 4: ADVERSARY (12)   - Attack testing
├── TIER 5: META (6)         - Meta-cognition
├── TIER 6: MEMORY (4)       - Persistence
├── TIER 7: PHI (1)          - Orchestration
├── TIER 8: ORACLE (1)       - External queries [NEW]
└── TIER 9: SELF (1)         - Self-improvement [NEW]

MECHANISMS (3):
├── Prediction Market Layer  - Credibility stakes
├── Structured Debate        - Adversarial dialogue
└── Evolution Engine         - Selection pressure
```

## 10.2 Updated Message Schema

```yaml
message:
  header:
    agent_id: <int>  # Now 1-59
    agent_name: <string>
    agent_tier: <GENESIS|BRIDGE|VERIFICATION|ADVERSARY|META|MEMORY|PHI|ORACLE|SELF>
    # ... rest unchanged
  
  # NEW: Market fields
  market:
    bet_placed: <bool>
    bet_id: <uuid or null>
    stake: <float>
    market_price: <float>
  
  # NEW: Evolution fields  
  evolution:
    genome_id: <uuid>
    generation: <int>
```

## 10.3 Updated PHI Responsibilities

PHI (Agent 57) now also:
- Manages prediction market resolution
- Triggers and judges debates
- Selects genomes for problems
- Coordinates with Oracle Strategist (58) for external queries
- Reviews Architect (59) proposals for self-modification

---

*Document Version: 2.0*
*Companion to: OMEGA_ARCHITECTURE_57_PROMPTS.md (pending update to 59)*
*Architecture: OMEGA+ (59 agents + 3 mechanisms)*
