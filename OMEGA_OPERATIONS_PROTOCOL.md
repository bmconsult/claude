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
