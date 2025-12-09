# Agentic Architecture v2: Enhanced Multi-Agent System

**Status**: Designed, partially tested
**Date**: December 2024

---

## Executive Summary

v2 is a sophisticated multi-agent architecture designed for complex problem-solving. Key improvements over v1:

| Aspect | v1 (Used) | v2 (Proposed) |
|--------|-----------|---------------|
| Agents per attempt | ~11 | ~25-40 |
| Parallelism | Within phase | Across phases + speculative |
| Validation | None | Adversarial critics |
| Learning | None | Meta-learner |
| Memory | Files (unstructured) | Structured KB + indices |
| Recursion | None | Up to depth 5 |
| Model selection | All same | Task-appropriate |
| Failure handling | Abandon | Analyze + learn |

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR (Main Agent)                        │
│  • Strategic decisions    • Resource allocation    • Termination logic  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
            │   MEMORY    │  │    META     │  │  DISPATCH   │
            │   MANAGER   │  │   LEARNER   │  │   ROUTER    │
            │             │  │             │  │             │
            │ • Shared KB │  │ • Track ROI │  │ • Load bal. │
            │ • Dedup     │  │ • Pattern   │  │ • Priority  │
            │ • Index     │  │   extract   │  │   queue     │
            └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                   │                │                │
                   └────────────────┴────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│  EXPLORATION  │          │  EXPLOITATION │          │  VALIDATION   │
│    SWARM      │          │     SWARM     │          │    SWARM      │
│               │          │               │          │               │
│ • Scout       │          │ • Builder     │          │ • Critic      │
│ • Mapper      │          │ • Prover      │          │ • Adversary   │
│ • Connector   │          │ • Synthesizer │          │ • Verifier    │
└───────────────┘          └───────────────┘          └───────────────┘
```

---

## 2. Agent Role Taxonomy

### 2.1 Exploration Swarm

```yaml
Scout:
  purpose: "Find new attack vectors, unexplored territory"
  output: "Candidate approaches with potential assessment"
  model: haiku  # Fast, cheap, many parallel
  count: 4-8 parallel

Mapper:
  purpose: "Build knowledge graph of domain"
  output: "Structured relationships, dependencies"
  model: haiku
  count: 2-4 parallel

Connector:
  purpose: "Find links between disparate findings"
  output: "Cross-domain insights, unexpected bridges"
  model: sonnet  # Needs reasoning
  count: 1-2
```

### 2.2 Exploitation Swarm

```yaml
Builder:
  purpose: "Construct proofs, write code, create artifacts"
  output: "Concrete deliverables"
  model: sonnet
  count: 2-4 parallel

Prover:
  purpose: "Rigorous mathematical/logical derivation"
  output: "Step-by-step proofs with confidence"
  model: opus  # Highest reasoning for proofs
  count: 1-2

Synthesizer:
  purpose: "Combine multiple partial results"
  output: "Unified theories, merged proofs"
  model: opus
  count: 1
```

### 2.3 Validation Swarm

```yaml
Critic:
  purpose: "Find flaws, gaps, weaknesses"
  output: "List of issues with severity"
  model: opus  # Best at finding subtle errors
  count: 1-2

Adversary:
  purpose: "Actively try to break/disprove"
  output: "Counterexamples or proof of robustness"
  model: opus
  count: 1

Verifier:
  purpose: "Independent re-derivation"
  output: "Confirmation or contradiction"
  model: sonnet
  count: 2 (for independent verification)
```

---

## 3. Dynamic Execution Flow

```
                    ┌─────────────────────┐
                    │   PROBLEM INPUT     │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │      DECOMPOSITION PHASE       │
              │                                │
              │  Scout×4 (parallel, haiku)     │
              │  → Identify sub-problems       │
              │  → Rate difficulty/potential   │
              └────────────────┬───────────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       PRIORITY RANKING         │
              │                                │
              │  Synthesizer×1 (sonnet)        │
              │  → Rank by (potential/effort)  │
              │  → Identify dependencies       │
              │  → Create execution graph      │
              └────────────────┬───────────────┘
                               │
                               ▼
         ┌─────────────────────┴─────────────────────┐
         │              ATTACK WAVE 1                │
         │                                           │
         │  For top-3 candidates IN PARALLEL:        │
         │  ┌─────────────────────────────────────┐  │
         │  │ Builder (sonnet) → attempt solution │  │
         │  │ Critic (opus) → find flaws          │  │
         │  │         [run simultaneously]        │  │
         │  └─────────────────────────────────────┘  │
         └─────────────────────┬─────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       RESULTS TRIAGE           │
              │                                │
              │  Meta-Learner assesses:        │
              │  • Which attempts succeeded?   │
              │  • Which failed and why?       │
              │  • What patterns emerge?       │
              │  • Should we recurse deeper?   │
              └────────────────┬───────────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
    ┌─────────────────┐              ┌─────────────────┐
    │  SUCCESS PATH   │              │  RECURSE PATH   │
    │                 │              │                 │
    │ Verifier×2      │              │ Decompose the   │
    │ (independent)   │              │ sub-problem     │
    │ → Confirm       │              │ → GOTO start    │
    └────────┬────────┘              └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │  FINAL MERGE    │
    │                 │
    │ Synthesizer     │
    │ → Combine all   │
    │   verified      │
    │   results       │
    └─────────────────┘
```

---

## 4. Key Protocols

### 4.1 Builder-Critic Protocol (Adversarial)

```
┌──────────────────────────────────────────────────────────────┐
│  BUILDER-CRITIC LOOP (run until convergence)                 │
│                                                              │
│  Round 1:                                                    │
│    Builder → produces draft proof                            │
│    Critic  → finds 3 gaps                                    │
│                                                              │
│  Round 2:                                                    │
│    Builder → addresses gaps, produces v2                     │
│    Critic  → finds 1 remaining issue                         │
│                                                              │
│  Round 3:                                                    │
│    Builder → fixes final issue, produces v3                  │
│    Critic  → "No significant gaps found"                     │
│                                                              │
│  → VERIFIED: Send to Verifier for independent check          │
└──────────────────────────────────────────────────────────────┘
```

**Termination conditions:**
- Critic finds no FATAL or MAJOR issues
- Max 5 rounds (prevent infinite loops)
- Builder explicitly cannot address critique (escalate)

### 4.2 Speculative Execution Protocol

```
┌──────────────────────────────────────────────────────────────┐
│  SPECULATIVE BRANCHING                                       │
│                                                              │
│  When outcome uncertain, launch BOTH branches:               │
│                                                              │
│  "If Lemma X is true..."     "If Lemma X is false..."       │
│         │                            │                       │
│         ▼                            ▼                       │
│    Builder A                    Builder B                    │
│    (assumes true)               (assumes false)              │
│         │                            │                       │
│         ▼                            ▼                       │
│    Result A                     Result B                     │
│                                                              │
│  Meanwhile: Prover C attempts to resolve Lemma X             │
│                                                              │
│  When resolved → keep relevant branch, discard other         │
└──────────────────────────────────────────────────────────────┘
```

**Use when:**
- Critical dependency is uncertain
- Both branches are tractable
- Resolution time is significant

### 4.3 Recursive Depth Protocol

```python
def attack_problem(problem, depth=0, max_depth=5):
    if depth > max_depth:
        return "DEPTH_LIMIT: Manual intervention needed"

    # Phase 1: Scout
    sub_problems = spawn_parallel([
        Scout(f"decompose: {problem}") for _ in range(4)
    ])

    # Phase 2: Attempt each
    for sub in prioritize(sub_problems):
        result = spawn_parallel([
            Builder(sub),
            Critic(sub)  # Adversarial
        ])

        if result.verified:
            store_to_memory(result)
        elif result.needs_decomposition:
            # RECURSE
            attack_problem(sub, depth + 1)
        else:
            store_failure_analysis(result)

    # Phase 3: Synthesize
    return Synthesizer(memory.get_all_verified())
```

---

## 5. Shared Memory Architecture

```
/workspace/
├── .agent_memory/
│   ├── knowledge_base.json       # Structured findings
│   │   {
│   │     "claims": [...],
│   │     "proofs": [...],
│   │     "dependencies": {...}
│   │   }
│   │
│   ├── execution_log.json        # What's been tried
│   │   {
│   │     "attempts": [...],
│   │     "timestamps": [...],
│   │     "outcomes": [...]
│   │   }
│   │
│   ├── failure_analysis.json     # Why things failed
│   │   {
│   │     "approach": "...",
│   │     "failure_mode": "...",
│   │     "lessons": [...]
│   │   }
│   │
│   ├── confidence_tracker.json   # Confidence per claim
│   │   {
│   │     "claim_id": {
│   │       "confidence": 0.85,
│   │       "sources": [...],
│   │       "verified_by": [...]
│   │     }
│   │   }
│   │
│   └── dependency_graph.json     # What depends on what
│       {
│         "claim_A": ["claim_B", "claim_C"],
│         "claim_B": []
│       }
│
├── .agent_queue/
│   ├── pending_tasks.json        # Tasks waiting
│   ├── in_progress.json          # Currently running
│   └── completed.json            # Done tasks
│
└── outputs/
    ├── proofs/                   # Verified proofs
    ├── drafts/                   # Unverified work
    ├── rejected/                 # Failed attempts (with analysis)
    └── synthesis/                # Combined results
```

---

## 6. Model Selection Matrix

```
┌─────────────────────────────────────────────────────────────┐
│              MODEL SELECTION MATRIX                          │
├─────────────────┬───────────┬───────────┬───────────────────┤
│ Task Type       │ Model     │ Parallel? │ Why               │
├─────────────────┼───────────┼───────────┼───────────────────┤
│ Scouting        │ haiku     │ Yes (8)   │ Fast, cheap       │
│ Mapping         │ haiku     │ Yes (4)   │ Breadth > depth   │
│ Connecting      │ sonnet    │ Yes (2)   │ Needs reasoning   │
│ Building draft  │ sonnet    │ Yes (3)   │ Good balance      │
│ Proving         │ opus      │ No (1)    │ Max reasoning     │
│ Criticizing     │ opus      │ Yes (2)   │ Find subtle errors│
│ Adversarial     │ opus      │ No (1)    │ Deep analysis     │
│ Synthesizing    │ opus      │ No (1)    │ Integration       │
│ Verifying       │ sonnet    │ Yes (2)   │ Independent check │
└─────────────────┴───────────┴───────────┴───────────────────┘
```

**Cost estimation per full run:**
- Scouts: 8 × haiku = low cost
- Builders: 3 × sonnet = medium cost
- Critics: 2 × opus = high cost
- Provers: 1 × opus = high cost
- Synthesizer: 1 × opus = high cost

**Total: ~25-40 agent invocations per problem**

---

## 7. Meta-Learning Component

```
┌──────────────────────────────────────────────────────────────┐
│  META-LEARNER (runs after each wave)                         │
│                                                              │
│  Inputs:                                                     │
│    - All agent outputs this wave                             │
│    - Time taken per agent                                    │
│    - Success/failure outcomes                                │
│    - Historical patterns                                     │
│                                                              │
│  Analysis:                                                   │
│    - ROI per agent type                                      │
│    - Pattern extraction from failures                        │
│    - Redundancy detection                                    │
│    - Bottleneck identification                               │
│                                                              │
│  Outputs:                                                    │
│    - "Scout agents finding 80% overlap → reduce to 2"        │
│    - "Opus provers succeeding 3x more → prioritize"          │
│    - "Approach X failed 4 times → add to blocklist"          │
│    - "Pattern: failures share trait Y → avoid"               │
│                                                              │
│  Writes to: /workspace/.agent_memory/meta_insights.json      │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Prompt Templates

### 8.1 Scout Prompt

```markdown
## Role: Scout Agent
You are exploring attack vectors for: {PROBLEM}

## Existing Knowledge
{MEMORY_DUMP}

## Your Task
1. Identify 3-5 novel approaches NOT already in memory
2. For each, estimate:
   - Potential (1-10): How likely to succeed?
   - Effort (1-10): How hard to attempt?
   - Dependencies: What must be true first?
3. Flag any connections to existing verified results

## Output Format
Write to: /workspace/.agent_memory/scout_{ID}.json
Schema:
{
  "approaches": [
    {
      "name": "...",
      "description": "...",
      "potential": 8,
      "effort": 5,
      "dependencies": ["..."],
      "connections": ["..."]
    }
  ]
}
```

### 8.2 Builder Prompt

```markdown
## Role: Builder Agent
Construct a proof/solution for: {CLAIM}

## Available Resources
- Verified claims: {VERIFIED_CLAIMS}
- Tools: {AVAILABLE_TOOLS}

## Constraints
- Use ONLY results from verified memory
- Mark ANY assumption with [ASSUMPTION: ...]
- Cite sources for each step
- Explicit confidence level for each claim

## Output Format
Write to: /workspace/outputs/drafts/{CLAIM_ID}.md
Include:
- Step-by-step derivation
- All assumptions marked
- Confidence assessment
- Known gaps or weaknesses
```

### 8.3 Critic Prompt

```markdown
## Role: Critic Agent
Your job is to BREAK this proof: {PROOF_LOCATION}

## Critique Dimensions
1. Logical gaps - missing steps, unjustified leaps
2. Assumption validity - are marked assumptions reasonable?
3. Circular reasoning - does it assume what it proves?
4. Edge cases - does it handle all cases?
5. Dependency accuracy - are cited results used correctly?

## Severity Ratings
- FATAL: Proof is fundamentally broken
- MAJOR: Significant gap that needs addressing
- MINOR: Small issue, doesn't invalidate proof
- STYLE: Presentation issue only

## Output Format
{
  "issues": [
    {
      "location": "Step 3",
      "description": "...",
      "severity": "MAJOR",
      "suggested_fix": "..."
    }
  ],
  "overall_assessment": "...",
  "recommendation": "REJECT/REVISE/ACCEPT"
}
```

### 8.4 Meta-Learner Prompt

```markdown
## Role: Meta-Learner Agent
Analyze this wave's results and extract patterns.

## Input Data
- Agent outputs: {OUTPUTS}
- Timing data: {TIMING}
- Success/failure: {OUTCOMES}

## Analysis Tasks
1. Which agent types had highest ROI?
2. What patterns appear in failures?
3. Was there redundant work?
4. What bottlenecks emerged?

## Output
{
  "insights": [...],
  "recommendations": [...],
  "blocklist_additions": [...],
  "next_wave_adjustments": {...}
}
```

---

## 9. Comparison: v1 vs v2

| Dimension | v1 | v2 | Expected Improvement |
|-----------|----|----|---------------------|
| Error rate | ~10-20% | ~2-5% | Adversarial validation |
| Novel insights | Moderate | High | Scout diversity + Connectors |
| Wasted work | High | Low | Meta-learner optimization |
| Depth of analysis | Fixed | Adaptive | Recursive decomposition |
| Recovery from failure | None | Automatic | Failure analysis + retry |
| Cost efficiency | Fixed | Optimized | Model selection matrix |

---

## 10. Known Limitations

1. **Coordination overhead**: More agents = more synthesis work
2. **Context limits**: Each agent has limited context window
3. **Latency**: Sequential phases add wall-clock time
4. **Cost**: Opus agents are expensive
5. **Untested**: Full architecture not yet empirically validated

---

## 11. Implementation Status

| Component | Status |
|-----------|--------|
| Basic parallel agents | ✅ Tested |
| Builder-Critic pair | ✅ Tested (partial) |
| Scout swarm | ✅ Tested |
| Full three-swarm | ❌ Not tested |
| Recursive depth | ❌ Not tested |
| Speculative execution | ❌ Not tested |
| Structured memory | ❌ Not tested |
| Meta-learner | ❌ Not tested |

**Next step**: Full implementation test on a suitable problem.

---

**END OF DOCUMENT**
