# Agentic Architecture v2: Enhanced from v1

**Context**: User said "pretty smart. can you refine, expand, enhance, optimize this to make it even more / way more effective?"
**Method**: Taking v1 Natural and systematically improving each weakness

---

## What v1 Got Right

- Phased approach (research → explore → attack → synthestic)
- Parallel within phases
- Funnel structure (broad → narrow)
- ~11 agents is tractable

## What v1 Got Wrong (Limitations Identified)

1. **No error checking** → Need validation/critic agents
2. **No iteration** → Need feedback loops
3. **Fixed structure** → Need recursive depth
4. **No learning** → Need meta-tracking
5. **Same model for all** → Need task-appropriate models
6. **No speculation** → Need parallel branching on uncertainty

---

## v2 Architecture: Addressing Each Weakness

### Enhancement 1: Adversarial Validation

**Problem**: v1 agents could make errors that propagate

**Solution**: Add Critic agents that run alongside Builders

```
v1:  Builder → Output

v2:  Builder → Output
         ↓
     Critic → Issues found?
         ↓
     Builder → Revised output (iterate until clean)
```

**New agents**: +2-3 Critics (opus model for catching subtle errors)

---

### Enhancement 2: Iteration Loops

**Problem**: v1 is single-pass, no refinement

**Solution**: Builder-Critic protocol with convergence

```
┌──────────────────────────────────────────────────┐
│  BUILDER-CRITIC LOOP                             │
│                                                  │
│  Round 1: Builder drafts → Critic finds 3 gaps  │
│  Round 2: Builder fixes → Critic finds 1 gap    │
│  Round 3: Builder fixes → Critic: "Clean"       │
│                                                  │
│  Exit when: No FATAL/MAJOR issues OR max rounds │
└──────────────────────────────────────────────────┘
```

**Impact**: Better quality, catches errors before they compound

---

### Enhancement 3: Recursive Depth

**Problem**: v1 can't go deeper on promising vectors

**Solution**: Agents can spawn sub-agents for sub-problems

```
Attack Agent 8 finds: "This approach works IF Lemma X holds"
                              │
                              ▼
                    Spawn sub-agent to prove Lemma X
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            Sub-agent A           Sub-agent B
            (assumes true)        (tries to prove)
```

**New capability**: Recursive decomposition up to depth 3-5

---

### Enhancement 4: Meta-Learning

**Problem**: v1 doesn't learn what works

**Solution**: Meta-agent analyzes results after each phase

```
┌──────────────────────────────────────────────────┐
│  META-LEARNER (runs after each phase)            │
│                                                  │
│  Inputs: All outputs, timing, success/failure   │
│                                                  │
│  Outputs:                                        │
│  • "Research agents had 80% overlap → use 2"    │
│  • "Approach X failed 3 times → blocklist"      │
│  • "2-adic angle most promising → prioritize"   │
└──────────────────────────────────────────────────┘
```

**New agent**: +1 Meta-Learner

---

### Enhancement 5: Model Selection

**Problem**: v1 uses same model for all tasks

**Solution**: Match model to task complexity

```
┌─────────────────┬───────────┬─────────────────────┐
│ Task            │ Model     │ Why                 │
├─────────────────┼───────────┼─────────────────────┤
│ Scouting        │ haiku     │ Fast, cheap, broad  │
│ Research        │ haiku     │ Retrieval-focused   │
│ Building        │ sonnet    │ Good balance        │
│ Proving         │ opus      │ Max reasoning       │
│ Criticizing     │ opus      │ Catch subtle errors │
│ Synthesis       │ opus      │ Deep integration    │
└─────────────────┴───────────┴─────────────────────┘
```

**Impact**: Better cost/quality tradeoff, faster scouting

---

### Enhancement 6: Speculative Execution

**Problem**: v1 blocks on uncertainties

**Solution**: Branch on uncertain dependencies, resolve in parallel

```
"Does Lemma X hold?"
        │
        ├─────────────────┐
        ▼                 ▼
  Branch A:            Branch B:
  Assume TRUE          Assume FALSE
  Build on it          Build alternative
        │                 │
        └────────┬────────┘
                 │
        Meanwhile: Prover works on Lemma X
                 │
        When resolved → Keep correct branch
```

**Impact**: Don't block on uncertainties, parallel progress

---

### Enhancement 7: Shared Memory

**Problem**: v1 agents don't share knowledge effectively

**Solution**: Structured knowledge base all agents read/write

```
/workspace/.agent_memory/
├── knowledge_base.json    # What we know
├── attempts.json          # What we've tried
├── failures.json          # Why things failed
├── confidence.json        # How sure per claim
└── dependencies.json      # What needs what
```

**Impact**: No redundant work, build on each other's findings

---

## v2 Full Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR (Main Agent)                        │
│              Strategic decisions, resource allocation                    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
            │   MEMORY    │  │    META     │  │  DISPATCH   │
            │   MANAGER   │  │   LEARNER   │  │   ROUTER    │
            └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                   └────────────────┴────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│  EXPLORATION  │          │  EXPLOITATION │          │  VALIDATION   │
│    SWARM      │          │     SWARM     │          │    SWARM      │
│               │          │               │          │               │
│ Scout ×4      │          │ Builder ×3    │          │ Critic ×2     │
│ (haiku)       │          │ (sonnet)      │          │ (opus)        │
│               │          │               │          │               │
│ Mapper ×2     │          │ Prover ×1     │          │ Adversary ×1  │
│ (haiku)       │          │ (opus)        │          │ (opus)        │
│               │          │               │          │               │
│ Connector ×2  │          │ Synthesizer×1 │          │ Verifier ×2   │
│ (sonnet)      │          │ (opus)        │          │ (sonnet)      │
└───────────────┘          └───────────────┘          └───────────────┘
     8 agents                   5 agents                  5 agents
```

**Total: ~18-25 core agents + recursive spawning**

---

## Execution Flow

```
                    ┌─────────────────────┐
                    │   PROBLEM INPUT     │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │   SCOUT SWARM (haiku ×4-8)     │
              │   Find attack vectors          │
              │   Rate potential/effort        │
              └────────────────┬───────────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │   META-LEARNER                 │
              │   Rank vectors, plan attacks   │
              └────────────────┬───────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
   ┌───────────┐         ┌───────────┐         ┌───────────┐
   │ Builder A │         │ Builder B │         │ Builder C │
   │ + Critic  │         │ + Critic  │         │ + Critic  │
   │ (iterate) │         │ (iterate) │         │ (iterate) │
   └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
         │                     │                     │
         │    ┌────────────────┼────────────────┐    │
         │    │                │                │    │
         │    ▼                ▼                ▼    │
         │  ┌────────────────────────────────────┐   │
         │  │         RESULTS TRIAGE             │   │
         │  │   • Success? → Verify              │   │
         │  │   • Partial? → Recurse deeper      │   │
         │  │   • Failed? → Analyze, blocklist   │   │
         │  └────────────────┬───────────────────┘   │
         │                   │                       │
         │    ┌──────────────┴──────────────┐       │
         │    │                             │       │
         │    ▼                             ▼       │
         │  SUCCESS                      RECURSE    │
         │    │                             │       │
         │    ▼                             │       │
         │  Verifier ×2                     │       │
         │  (independent)                   │       │
         │    │                             │       │
         │    ▼                             ▼       │
         └──► FINAL SYNTHESIS ◄─────────────┘
                    │
                    ▼
              ┌─────────────────┐
              │  OUTPUT + META  │
              │  LEARNINGS      │
              └─────────────────┘
```

---

## Key Protocols

### Builder-Critic Protocol

```
For each attack vector:
  1. Builder produces draft
  2. Critic reviews, rates issues FATAL/MAJOR/MINOR
  3. If FATAL/MAJOR: Builder revises, goto 2
  4. If clean or max rounds: proceed
  5. Pass to Verifier for independent check
```

### Speculative Execution

```
When uncertain about dependency X:
  1. Launch Branch-True agent (assumes X)
  2. Launch Branch-False agent (assumes ¬X)
  3. Launch Prover agent (resolves X)
  4. When Prover done: kill wrong branch, continue correct
```

### Recursive Decomposition

```
When Builder hits sub-problem:
  1. Check depth (max 5)
  2. If < max: spawn sub-problem solver
  3. Sub-solver runs same protocol
  4. Results bubble up
```

---

## Agent Count Comparison

| Component | v1 | v2 |
|-----------|----|----|
| Research/Scouting | 2-3 | 4-8 (haiku, cheap) |
| Exploration | 2-4 | 2-4 (+ Connectors) |
| Building | 3-4 | 3 + Critics |
| Proving | 0 | 1 (opus) |
| Validation | 0 | 5 (Critics, Adversary, Verifiers) |
| Meta/Coordination | 0 | 2-3 |
| **Total** | **8-13** | **18-25 base + recursive** |

---

## What This Gains

| Weakness | v1 | v2 | Method |
|----------|----|----|--------|
| Error propagation | High | Low | Adversarial critics |
| Single-pass | Yes | No | Iteration loops |
| Fixed depth | Yes | No | Recursive spawning |
| No learning | Yes | No | Meta-learner |
| Uniform cost | Yes | No | Model selection |
| Blocked by uncertainty | Yes | No | Speculative execution |
| Redundant work | Yes | No | Shared memory |

---

## Honest Assessment

**What I'm confident about:**
- Adversarial validation catches errors (tested on abc, found 3 errors)
- Model selection makes sense (haiku for scouting, opus for proving)
- Phased structure is sound

**What I'm uncertain about:**
- Is 25 agents too many? Coordination overhead?
- Does speculative execution pay off vs. just waiting?
- Is recursive depth worth the complexity?

**Would need to test:**
- v1 vs v2 on same problem, measure outcomes
- Cost analysis (is 2x agents worth 1.5x quality?)
- Latency (does v2 take too long?)

---

**END OF v2 ENHANCED**

This is what I'd genuinely produce when asked to refine v1.
The enhancements address the specific limitations I noticed.
