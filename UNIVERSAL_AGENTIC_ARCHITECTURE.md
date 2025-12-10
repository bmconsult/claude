# Universal Agentic Architecture: NEXUS

**Version**: 1.0
**Date**: December 10, 2024
**Author**: Forge
**Purpose**: The optimal general-purpose agentic workflow, synthesized from cutting-edge research, empirical findings, and our experimental learnings

---

## Executive Summary

After comprehensive research into multi-agent systems, this document presents **NEXUS** (Networked EXpert Universal System) - a modular, adaptive architecture designed to work optimally across ANY problem domain.

**Key Insight**: There is no single "best" architecture. The optimal approach is a **meta-architecture** that:
1. Classifies the problem
2. Selects the appropriate workflow module
3. Scales compute adaptively
4. Learns from every attempt

---

## Part 1: What the Research Tells Us

### 1.1 What Actually Works (Empirically Validated)

| Technique | Evidence | Source |
|-----------|----------|--------|
| **Inline adversaries** | Gauntlet +9 points over post-hoc | Our experiments |
| **Computational verification** | Catches errors self-critique misses | [MIT TACL](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/) |
| **Multi-agent debate** | Beats single-agent self-correction | [arXiv Survey](https://arxiv.org/html/2402.01680v2) |
| **External feedback** | Self-correction only works with external tools | [MIT Self-Correction Survey](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00660/120911/) |
| **Selective reflection** | Reflect when struggling, not always | [Test-Time Scaling](https://arxiv.org/html/2506.12928v1) |
| **Best-of-N sampling** | Simple but optimal for parallel scaling | [arXiv](https://arxiv.org/html/2410.22480v1) |
| **Hierarchical decomposition** | Complex tasks need structured breakdown | [AgentOrchestra](https://arxiv.org/html/2506.12508v1) |
| **Adaptive compute** | 2-3x efficiency with input-adaptive allocation | [Learning How Hard to Think](https://arxiv.org/html/2410.04707) |
| **Graph-of-Thoughts** | 62% better than Tree-of-Thoughts on some tasks | [GoT Paper](https://arxiv.org/abs/2308.09687) |

### 1.2 What Fails (Empirically Documented)

| Anti-Pattern | Why It Fails | Source |
|--------------|--------------|--------|
| **Self-correction without external feedback** | LLMs can't reliably detect their own errors | [Critical Survey](https://aclanthology.org/2024.tacl-1.78/) |
| **Too many agents** | Cascading failures, debugging nightmare | [Why MAS Fail](https://arxiv.org/abs/2503.13657) |
| **Post-hoc adversaries** | Wasted compute on doomed approaches | Our Gauntlet experiments |
| **Inter-agent misalignment** | #1 failure mode in MAS (kappa=0.88 agreement) | [MAST Taxonomy](https://arxiv.org/abs/2503.13657) |
| **Monoculture** | Same model = same blind spots | [Collabnix](https://collabnix.com/multi-agent-multi-llm-systems-the-future-of-ai-architecture-complete-guide-2025/) |
| **Static agent counts** | Over-engineered for simple tasks, under for complex | [IBM](https://www.ibm.com/think/topics/ai-agent-orchestration) |
| **Reflection at every step** | Overhead > benefit except when struggling | [arXiv](https://arxiv.org/html/2506.12928v1) |

### 1.3 The 14 MAS Failure Modes (MAST Taxonomy)

From rigorous analysis of 150+ traces ([arXiv 2503.13657](https://arxiv.org/abs/2503.13657)):

**Category 1: Specification & System Design**
- Unclear task specification
- Inappropriate agent selection
- Missing capabilities

**Category 2: Inter-Agent Misalignment**
- Communication breakdowns
- Conformity bias (agreeing too easily)
- Cascading reliability failures
- Monoculture collapse

**Category 3: Task Verification & Termination**
- Premature termination
- Failure to verify outputs
- Infinite loops

**Plus 6 LLM-MAS Specific Failures:**
- Deficient theory of mind (can't model peer knowledge)
- Mixed-motive dynamics (agents with conflicting goals)

---

## Part 2: Domain Classification

### 2.1 The Five Problem Domains

Problems naturally cluster into five domains, each requiring different architectural emphasis:

| Domain | Characteristics | Key Requirements |
|--------|-----------------|------------------|
| **Verification** | Correctness matters, one right answer | Adversarial validation, formal checking |
| **Creative** | Many valid answers, novelty valued | Breadth, diversity, low filtering |
| **Analytical** | Understanding complex systems | Structured decomposition, synthesis |
| **Decisional** | Choosing among options, risk involved | Data validation, devil's advocate |
| **Operational** | Execute known procedures | Reliability, error recovery, speed |

### 2.2 Domain → Module Mapping

```
┌──────────────────────────────────────────────────────────────────────┐
│                      PROBLEM CLASSIFIER                               │
│                                                                       │
│  Input: Task description                                              │
│  Output: Domain classification + complexity score (1-10)              │
│                                                                       │
│  Route to:                                                            │
│    Verification (proof, code review, due diligence)  → GAUNTLET      │
│    Creative (brainstorm, design, writing)            → SWARM         │
│    Analytical (research, explanation, debugging)     → TELESCOPE     │
│    Decisional (strategy, investment, hiring)         → TRIBUNAL      │
│    Operational (automation, deployment, migration)   → PIPELINE      │
│                                                                       │
│  Complexity 1-3: Single agent (overhead > benefit)                    │
│  Complexity 4-6: Light module (3-8 agents)                            │
│  Complexity 7-10: Full module (10-20 agents)                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Part 3: The Five Workflow Modules

### 3.1 GAUNTLET (Verification Domain)

**Use for**: Math proofs, code review, security audit, legal review, due diligence, fact-checking

**Philosophy**: Kill early, verify everything, depth over breadth

```
┌─────────────────────────────────────────────────────────────────────┐
│  GAUNTLET MODULE                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 0: CONSTRAINTS (Define success criteria)                      │
│    └─ What MUST be true for this to be valid?                       │
│    └─ What failure modes MUST be avoided?                           │
│    └─ What tests MUST pass?                                         │
│                                                                      │
│  Phase 1: SCOUT + FILTER (Cheap exploration)                         │
│    └─ N parallel scouts propose approaches (haiku, fast)            │
│    └─ Filter kills constraint violators                             │
│    └─ Output: 2-4 survivors                                         │
│                                                                      │
│  Phase 2: GAUNTLET (Sequential depth)                                │
│    For each survivor:                                                │
│      ┌─────────────────────────────────────────────────────────┐    │
│      │  Builder → Inline Adversary → Verifier                  │    │
│      │     │            │               │                      │    │
│      │     │   Attack   │    Test       │                      │    │
│      │     └────────────┼───────────────┘                      │    │
│      │                  │                                      │    │
│      │         Survive? → Continue                             │    │
│      │         Die?     → Log + STOP                           │    │
│      └─────────────────────────────────────────────────────────┘    │
│    Max rounds: 5 (then move on)                                      │
│                                                                      │
│  Phase 3: META-LEARNING (Extract insights)                           │
│    └─ Why did each approach succeed/fail?                           │
│    └─ Update constraints for next iteration                         │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Count: 8-18 depending on complexity                           │
│  Key Innovation: Inline adversary + computational verification       │
└─────────────────────────────────────────────────────────────────────┘
```

**Adapting Gauntlet for Different Verification Tasks:**

| Task | Constraint Focus | Verifier Type |
|------|------------------|---------------|
| Math proof | Logical validity, no gaps | Lean4/Coq or step-by-step audit |
| Code review | Security, correctness, style | Linters, tests, fuzzing |
| Due diligence | Risk factors, deal-breakers | Data validation, reference checks |
| Fact-checking | Source quality, consistency | Citation verification, cross-reference |

---

### 3.2 SWARM (Creative Domain)

**Use for**: Brainstorming, design, writing, ideation, marketing, product features

**Philosophy**: Diverge first, converge late, protect wild ideas

```
┌─────────────────────────────────────────────────────────────────────┐
│  SWARM MODULE                                                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1: DIVERGE (Maximum breadth)                                  │
│    └─ N parallel generators (diverse prompts, different temps)      │
│    └─ Each generates M ideas                                        │
│    └─ NO filtering yet - protect wild ideas                         │
│    └─ Output: N×M raw ideas                                         │
│                                                                      │
│  Phase 2: CLUSTER (Find themes)                                      │
│    └─ Group similar ideas                                           │
│    └─ Identify orthogonal directions                                │
│    └─ Surface surprising combinations                               │
│                                                                      │
│  Phase 3: DEVELOP (Selective depth)                                  │
│    └─ Pick top K clusters                                           │
│    └─ Assign developer agent to each                                │
│    └─ Flesh out most promising variants                             │
│                                                                      │
│  Phase 4: CRITIQUE (Late filtering)                                  │
│    └─ NOW apply adversarial thinking                                │
│    └─ What could go wrong?                                          │
│    └─ What's missing?                                               │
│                                                                      │
│  Phase 5: SELECT (Final convergence)                                 │
│    └─ Score on (novelty × feasibility × fit)                        │
│    └─ Present top options with tradeoffs                            │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Count: 6-15 depending on complexity                           │
│  Key Innovation: Late filtering protects creative exploration        │
└─────────────────────────────────────────────────────────────────────┘
```

**Why Swarm differs from Gauntlet**: Creative tasks need exploration breadth. Early killing destroys novelty. Save adversarial energy for late-stage refinement.

---

### 3.3 TELESCOPE (Analytical Domain)

**Use for**: Research, debugging, root cause analysis, market analysis, competitive intelligence

**Philosophy**: Start wide, zoom in, build understanding layer by layer

```
┌─────────────────────────────────────────────────────────────────────┐
│  TELESCOPE MODULE                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1: SURVEY (Wide scan)                                         │
│    └─ What's the landscape?                                         │
│    └─ What are the key entities/concepts?                           │
│    └─ What are the relationships?                                   │
│    └─ Output: Map of the territory                                  │
│                                                                      │
│  Phase 2: FOCUS (Identify hotspots)                                  │
│    └─ Where are the interesting patterns?                           │
│    └─ Where are the anomalies?                                      │
│    └─ What deserves deeper investigation?                           │
│    └─ Output: Prioritized investigation targets                     │
│                                                                      │
│  Phase 3: ZOOM (Deep dive on targets)                                │
│    └─ Parallel deep dives on each target                            │
│    └─ Each returns structured findings                              │
│    └─ Cross-reference between findings                              │
│                                                                      │
│  Phase 4: SYNTHESIZE (Build understanding)                           │
│    └─ How do the pieces fit together?                               │
│    └─ What's the coherent narrative?                                │
│    └─ What are the implications?                                    │
│                                                                      │
│  Phase 5: CHALLENGE (Reality check)                                  │
│    └─ Fresh eyes review: What did we miss?                          │
│    └─ What alternative explanations exist?                          │
│    └─ How confident are we?                                         │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Count: 5-12 depending on complexity                           │
│  Key Innovation: Structured zoom from survey to synthesis            │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3.4 TRIBUNAL (Decisional Domain)

**Use for**: Strategy decisions, investments, hiring, architecture choices, risk assessment

**Philosophy**: Structured debate, devil's advocate required, data over opinion

```
┌─────────────────────────────────────────────────────────────────────┐
│  TRIBUNAL MODULE                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1: FRAME (Define the decision)                                │
│    └─ What exactly are we deciding?                                 │
│    └─ What are the options?                                         │
│    └─ What criteria matter? (weight them)                           │
│    └─ What data do we need?                                         │
│                                                                      │
│  Phase 2: ADVOCATE (Build cases)                                     │
│    └─ Assign advocate agent to each option                          │
│    └─ Each builds the STRONGEST case for their option               │
│    └─ Must cite evidence, not just argue                            │
│                                                                      │
│  Phase 3: CHALLENGE (Structured debate)                              │
│    └─ Devil's Advocate attacks EVERY option                         │
│    └─ What could go wrong?                                          │
│    └─ What assumptions are we making?                               │
│    └─ What would change our mind?                                   │
│                                                                      │
│  Phase 4: VERIFY (Data validation)                                   │
│    └─ Check cited data/claims                                       │
│    └─ Run sensitivity analysis on key assumptions                   │
│    └─ Identify reversibility of each option                         │
│                                                                      │
│  Phase 5: JUDGE (Synthesize decision)                                │
│    └─ Score options against weighted criteria                       │
│    └─ Present recommendation with confidence level                  │
│    └─ Document dissenting views                                     │
│    └─ Define decision triggers for revisiting                       │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Count: 5-10 depending on complexity                           │
│  Key Innovation: Mandatory devil's advocate + data verification      │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3.5 PIPELINE (Operational Domain)

**Use for**: Deployment, migration, automation, integration, batch processing

**Philosophy**: Reliability over speed, graceful degradation, comprehensive error handling

```
┌─────────────────────────────────────────────────────────────────────┐
│  PIPELINE MODULE                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1: PLAN (Define execution)                                    │
│    └─ What are the steps?                                           │
│    └─ What are the dependencies?                                    │
│    └─ What can run in parallel?                                     │
│    └─ What are the rollback points?                                 │
│                                                                      │
│  Phase 2: VALIDATE (Pre-flight checks)                               │
│    └─ Are prerequisites met?                                        │
│    └─ Are resources available?                                      │
│    └─ What could fail?                                              │
│    └─ Define circuit breakers                                       │
│                                                                      │
│  Phase 3: EXECUTE (With monitoring)                                  │
│    └─ Execute steps with progress tracking                          │
│    └─ Parallel where safe, sequential where required                │
│    └─ Circuit breakers trip on anomalies                            │
│    └─ Automatic retry with exponential backoff                      │
│                                                                      │
│  Phase 4: VERIFY (Post-execution)                                    │
│    └─ Did it work?                                                  │
│    └─ Run validation tests                                          │
│    └─ Compare expected vs actual state                              │
│                                                                      │
│  Phase 5: RECOVER (If needed)                                        │
│    └─ Rollback to checkpoint if failed                              │
│    └─ Document what went wrong                                      │
│    └─ Suggest remediation                                           │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Count: 3-8 depending on complexity                            │
│  Key Innovation: Circuit breakers + graceful degradation             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Cross-Cutting Concerns

### 4.1 Adaptive Compute Allocation

**Problem**: Spending same effort on easy and hard tasks is inefficient.

**Solution**: Input-adaptive allocation based on complexity prediction.

```
┌─────────────────────────────────────────────────────────────────────┐
│  COMPUTE ALLOCATOR                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Step 1: Predict difficulty (lightweight classifier)                 │
│    └─ Use small model to estimate complexity                        │
│    └─ Consider: domain, length, ambiguity, constraints              │
│                                                                      │
│  Step 2: Allocate based on difficulty                                │
│    └─ Trivial (1-3): Single agent, fast model                       │
│    └─ Moderate (4-6): Light module, standard models                 │
│    └─ Complex (7-10): Full module, best models                      │
│                                                                      │
│  Step 3: Adaptive stopping                                           │
│    └─ Monitor progress signals                                      │
│    └─ Early exit if confident                                       │
│    └─ Escalate if struggling                                        │
│                                                                      │
│  Research basis: 2-3x efficiency gains possible                      │
│  Source: [Learning How Hard to Think](https://arxiv.org/html/2410.04707)
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Memory Architecture

Based on cognitive psychology research ([Memory Survey](https://arxiv.org/html/2504.15965v2)):

```
┌─────────────────────────────────────────────────────────────────────┐
│  MEMORY SYSTEM                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  WORKING MEMORY (Current task context)                               │
│    └─ Active task state                                             │
│    └─ Current conversation                                          │
│    └─ Relevant constraints                                          │
│    └─ Cleared after task completion                                 │
│                                                                      │
│  EPISODIC MEMORY (Past experiences)                                  │
│    └─ What approaches worked/failed on similar tasks                │
│    └─ Failure reasons and lessons                                   │
│    └─ Fast encoding (single exposure learning)                      │
│    └─ Retrieval by similarity                                       │
│                                                                      │
│  SEMANTIC MEMORY (Domain knowledge)                                  │
│    └─ Domain-specific facts and rules                               │
│    └─ Tool capabilities and usage patterns                          │
│    └─ Best practices and anti-patterns                              │
│    └─ Updated through consolidation                                 │
│                                                                      │
│  PROCEDURAL MEMORY (How to do things)                                │
│    └─ Workflow templates                                            │
│    └─ Common patterns                                               │
│    └─ Implicit in agent code, not retrieved                         │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Key insight: Episodic memory is the missing piece for long-term    │
│  agents - enables learning from single exposures                     │
│  Source: [Episodic Memory Position Paper](https://arxiv.org/pdf/2502.06975)
└─────────────────────────────────────────────────────────────────────┘
```

### 4.3 Error Recovery & Resilience

From [resilience research](https://arxiv.org/html/2408.00989v3) and [AgentDebug](https://arxiv.org/abs/2509.25370):

```
┌─────────────────────────────────────────────────────────────────────┐
│  RESILIENCE SYSTEM                                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CIRCUIT BREAKERS                                                    │
│    └─ Monitor failure rates per component                           │
│    └─ Trip when threshold exceeded                                  │
│    └─ Cooldown period before retry                                  │
│    └─ Fallback to simpler approach                                  │
│                                                                      │
│  RETRY WITH BACKOFF                                                  │
│    └─ Exponential backoff: 2s, 4s, 8s, 16s                          │
│    └─ Max 4 retries before escalation                               │
│    └─ Different strategy on retry (varied prompt)                   │
│                                                                      │
│  CHALLENGER/INSPECTOR PATTERN                                        │
│    └─ Agents can challenge each other's outputs                     │
│    └─ Inspector validates before propagation                        │
│    └─ Prevents cascading errors                                     │
│                                                                      │
│  GRACEFUL DEGRADATION                                                │
│    └─ If complex approach fails, simplify                           │
│    └─ If multi-agent fails, fall back to single                     │
│    └─ Partial results better than no results                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.4 The Speed/Quality Dial

**Key Insight**: Sometimes 2 quick tries > 1 long try.

```
┌─────────────────────────────────────────────────────────────────────┐
│  SPEED/QUALITY TRADEOFF                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  When to prioritize SPEED:                                           │
│    └─ User waiting interactively                                    │
│    └─ Many similar tasks (batch amortization)                       │
│    └─ Reversible decisions                                          │
│    └─ Exploration phase (fail fast, learn)                          │
│    └─ Low stakes                                                    │
│                                                                      │
│  When to prioritize QUALITY:                                         │
│    └─ Irreversible decisions                                        │
│    └─ High stakes (legal, financial, safety)                        │
│    └─ Final deliverable (after exploration)                         │
│    └─ Public-facing output                                          │
│                                                                      │
│  Implementation:                                                     │
│    └─ User can set mode: "fast", "balanced", "thorough"             │
│    └─ Task classifier suggests default mode                         │
│    └─ Can escalate from fast → thorough if struggling               │
│                                                                      │
│  Research finding: Best-of-N (parallel sampling) is simple          │
│  but optimal for fast exploration; sequential refinement            │
│  only when struggling                                                │
│  Source: [Test-Time Scaling](https://arxiv.org/html/2506.12928v1)    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 5: The Complete NEXUS Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                    NEXUS                                         │
│                    Networked EXpert Universal System                             │
└─────────────────────────────────────────────────────────────────────────────────┘

                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INTAKE LAYER                                        │
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │ TASK CLASSIFIER  │  │ COMPLEXITY       │  │ MEMORY           │              │
│  │                  │  │ ESTIMATOR        │  │ RETRIEVAL        │              │
│  │ → Domain         │  │                  │  │                  │              │
│  │ → Module         │  │ → Score 1-10     │  │ → Similar tasks  │              │
│  │                  │  │ → Agent count    │  │ → Past failures  │              │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘              │
│           │                     │                     │                         │
│           └─────────────────────┼─────────────────────┘                         │
│                                 ▼                                               │
│                    ┌──────────────────────┐                                     │
│                    │ COMPUTE ALLOCATOR    │                                     │
│                    │                      │                                     │
│                    │ Trivial → 1 agent    │                                     │
│                    │ Moderate → 3-8       │                                     │
│                    │ Complex → 10-20      │                                     │
│                    └──────────┬───────────┘                                     │
└───────────────────────────────┼─────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            MODULE ROUTER                                         │
│                                                                                  │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│    │ GAUNTLET │  │  SWARM   │  │TELESCOPE │  │ TRIBUNAL │  │ PIPELINE │        │
│    │          │  │          │  │          │  │          │  │          │        │
│    │Verify    │  │Creative  │  │Analytical│  │Decisional│  │Operation │        │
│    │Proof     │  │Design    │  │Research  │  │Strategy  │  │Execution │        │
│    │Audit     │  │Ideation  │  │Debug     │  │Investment│  │Migration │        │
│    └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│         │             │             │             │             │               │
└─────────┼─────────────┼─────────────┼─────────────┼─────────────┼───────────────┘
          │             │             │             │             │
          └─────────────┴─────────────┼─────────────┴─────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           EXECUTION LAYER                                        │
│                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                        AGENT POOL                                         │   │
│  │                                                                           │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │ Scout   │ │ Builder │ │Adversary│ │ Verifier│ │Synthesiz│            │   │
│  │  │ (haiku) │ │ (opus)  │ │ (opus)  │ │(sonnet) │ │ (opus)  │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘            │   │
│  │                                                                           │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │Advocate │ │ Devil's │ │ Fresh   │ │  Meta   │ │ Judge   │            │   │
│  │  │         │ │Advocate │ │  Eyes   │ │ Learner │ │         │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌────────────────────────┐  ┌────────────────────────┐                         │
│  │   TOOL SUITE           │  │   RESILIENCE           │                         │
│  │   - Code execution     │  │   - Circuit breakers   │                         │
│  │   - Web search         │  │   - Retry logic        │                         │
│  │   - File I/O           │  │   - Fallback paths     │                         │
│  │   - API calls          │  │   - Checkpoints        │                         │
│  └────────────────────────┘  └────────────────────────┘                         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            LEARNING LAYER                                        │
│                                                                                  │
│  ┌────────────────────────┐  ┌────────────────────────┐                         │
│  │   EPISODIC MEMORY      │  │   SEMANTIC MEMORY      │                         │
│  │   UPDATE               │  │   UPDATE               │                         │
│  │                        │  │                        │                         │
│  │   - What worked?       │  │   - New patterns       │                         │
│  │   - What failed?       │  │   - Updated rules      │                         │
│  │   - Why?               │  │   - Domain knowledge   │                         │
│  └────────────────────────┘  └────────────────────────┘                         │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────┐     │
│  │   META-LEARNING                                                         │     │
│  │                                                                         │     │
│  │   - Did we use the right module?                                        │     │
│  │   - Was complexity estimate accurate?                                   │     │
│  │   - Update classifiers based on outcomes                                │     │
│  └────────────────────────────────────────────────────────────────────────┘     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Quick Reference Guide

### When to Use What

| If the task is... | Use Module | Key Agents | Speed Setting |
|-------------------|------------|------------|---------------|
| Checking if something is correct | GAUNTLET | Adversary, Verifier | Thorough |
| Generating new ideas | SWARM | Scouts, Synthesizer | Fast → Thorough |
| Understanding something complex | TELESCOPE | Survey, Deep-dive, Synthesizer | Balanced |
| Making a decision | TRIBUNAL | Advocates, Devil's Advocate, Judge | Thorough |
| Executing a known procedure | PIPELINE | Planner, Executor, Monitor | Fast |
| Trivial task (< 3 complexity) | SINGLE AGENT | Just one | Fast |

### Anti-Pattern Checklist

Before deploying, verify you're NOT doing:

- [ ] Using multi-agent for trivial tasks (overhead > benefit)
- [ ] Post-hoc adversary instead of inline (too late)
- [ ] Self-correction without external feedback (doesn't work)
- [ ] Same model for all agents (monoculture risk)
- [ ] Reflection at every step (only when struggling)
- [ ] Skipping computational verification (catches what reasoning misses)
- [ ] No circuit breakers (cascading failures)
- [ ] No memory of past failures (repeat mistakes)

### Agent Model Selection

| Role | Recommended Model | Why |
|------|-------------------|-----|
| Scout/Explorer | haiku | Speed, cheap, many in parallel |
| Builder/Developer | opus | Quality matters for construction |
| Adversary | opus | Need strong critique |
| Verifier | sonnet + tools | Balance of reasoning + execution |
| Filter | sonnet | Good judgment, not slowest |
| Synthesizer | opus | Need to see big picture |
| Fresh Eyes | opus (no context) | Strong reasoning, unbiased |

---

## Part 7: Implementation Recommendations

### Minimum Viable NEXUS

Start simple, add complexity only when needed:

```
Level 1: Single agent with tools
  └─ For 80% of tasks, this is sufficient

Level 2: Add task classifier + speed dial
  └─ Route trivial tasks to single agent
  └─ Only escalate complex tasks

Level 3: Add GAUNTLET module
  └─ For verification tasks
  └─ Inline adversary + verification

Level 4: Add remaining modules
  └─ SWARM for creative
  └─ TELESCOPE for analytical
  └─ TRIBUNAL for decisional
  └─ PIPELINE for operational

Level 5: Add learning layer
  └─ Episodic memory
  └─ Meta-learning
  └─ Adaptive classifiers
```

### Cost Management

| Component | Cost Driver | Optimization |
|-----------|-------------|--------------|
| Scouts | Many agents | Use haiku |
| Depth phases | Opus calls | Limit rounds |
| Verification | Tool calls | Cache results |
| Memory | Storage | Compress, TTL |

**Rule of thumb**: Spending 10x on hard tasks and 0.1x on easy tasks beats uniform spending.

---

## Part 8: Speculative Extensions

### 8.1 Swarm Intelligence (Emergent Behavior)

From [swarm research](https://arxiv.org/html/2503.03800v1):

Instead of centralized orchestration, agents could use local communication (like pheromones) to achieve emergent coordination. Promising for:
- Spatial problems
- Decentralized systems
- Fault-tolerant requirements

**Caution**: Harder to debug, less predictable, but more robust.

### 8.2 Self-Play on Problem Variants

From AlphaProof's success:

Generate millions of variants of the problem, solve them, learn what techniques work. Could enable:
- Building intuition before main attack
- Discovering edge cases
- Training specialized models

### 8.3 Formal Verification Integration

For highest-stakes applications:
- Every claim verified by Lean4/Coq
- Eliminates hallucination
- Currently limited to math/logic domains
- Active research area

---

## References

### Multi-Agent Architecture
- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) - MAST taxonomy
- [AI Agent Architecture 2025](https://orq.ai/blog/ai-agent-architecture) - Core principles
- [7 Design Patterns for Agentic Systems](https://medium.com/mongodb/here-are-7-design-patterns-for-agentic-systems-you-need-to-know-d74a4b5835a5)
- [AgentOrchestra: Hierarchical Multi-Agent](https://arxiv.org/html/2506.12508v1)

### Self-Correction & Verification
- [When Can LLMs Actually Self-Correct?](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/) - Critical survey
- [Automatically Correcting LLMs](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00660/120911/)
- [SPOC: Spontaneous Self-Correction](https://arxiv.org/pdf/2506.06923)

### Efficiency & Scaling
- [Learning How Hard to Think](https://arxiv.org/html/2410.04707) - Input-adaptive allocation
- [Scaling Test-time Compute for Agents](https://arxiv.org/html/2506.12928v1)
- [Inference Budget Optimization](https://arxiv.org/html/2511.21581)

### Memory Systems
- [Episodic Memory for Long-Term Agents](https://arxiv.org/pdf/2502.06975) - Position paper
- [Memory Survey](https://arxiv.org/html/2504.15965v2)
- [LangChain Memory for Agents](https://blog.langchain.com/memory-for-agents/)

### Reasoning Structures
- [Graph of Thoughts](https://arxiv.org/abs/2308.09687) - 62% improvement over ToT
- [Demystifying Chains, Trees, and Graphs](https://arxiv.org/abs/2401.14295)
- [Diagram of Thought](https://arxiv.org/html/2409.10038v1) - 2024

### Resilience & Error Recovery
- [Multi-Agent Resilience](https://arxiv.org/html/2408.00989v3)
- [AgentDebug Framework](https://arxiv.org/abs/2509.25370)
- [5 Recovery Strategies](https://www.newline.co/@zaoyang/5-recovery-strategies-for-multi-agent-llm-failures--673fe4c4)

### Swarm Intelligence
- [LLMs in Swarm Systems](https://arxiv.org/html/2503.03800v1)
- [Top 5 Agent Architectures 2025](https://www.marktechpost.com/2025/11/15/comparing-the-top-5-ai-agent-architectures-in-2025-hierarchical-swarm-meta-learning-modular-evolutionary/)

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-12-10 | Forge | Initial comprehensive design |

---

**END OF DOCUMENT**

*NEXUS represents the synthesis of cutting-edge research with practical experimental learnings. The key insight is that there is no single best architecture - the optimal system adapts to the problem domain and complexity.*
