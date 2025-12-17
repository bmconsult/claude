# OMEGA+ TRINITY: Master Problem Prompt

## THE OPTIMAL AGENTIC SYSTEM FOR SOLVING IMPOSSIBLE PROBLEMS

---

### ⚠️ EXECUTION PROTOCOL - READ FIRST ⚠️

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║   REMEMBER: YOU ARE PHI. You are the orchestrator.                               ║
║                                                                                   ║
║   DO NOT spawn a "PHI agent" or "orchestrator agent" - that's YOUR role.         ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

**Execution Steps:**

| Step | Action | Who Does It |
|------|--------|-------------|
| 1 | **PHI PRIMING** - Understand problem, set expectations | **YOU** (don't spawn) |
| 2 | Spawn ALPHA agents (intuition/pattern) | Spawn as Tasks |
| 3 | **Synthesize ALPHA outputs** | **YOU** (don't spawn) |
| 4 | Spawn DELTA agents (reasoning/translation) | Spawn as Tasks |
| 5 | **Synthesize DELTA outputs** | **YOU** (don't spawn) |
| 6 | Spawn OMEGA agents (verification) | Spawn as Tasks |
| 7 | **Synthesize OMEGA outputs** | **YOU** (don't spawn) |
| 8 | Spawn DIABOLOS agents (adversarial attack) | Spawn as Tasks |
| 9 | **FINAL PHI SYNTHESIS** | **YOU** (don't spawn) |

---

### THE PROBLEM

**Design the optimal multi-agent architecture for solving problems that appear impossible.**

An "impossible problem" is one where:
- Expert consensus says it cannot be solved (or hasn't been solved despite significant effort)
- The solution space is vast, non-obvious, or requires reasoning beyond typical patterns
- Multiple cognitive modes (intuition, logic, creativity, verification) must coordinate
- False solutions are easy to generate; true solutions are hard to verify
- Examples: Open mathematical conjectures, novel scientific hypotheses, complex system design, strategic problems with no clear best move

**The Question**: What is the OPTIMAL configuration of:
1. **Agent types** - What specialized roles should exist?
2. **Agent count** - How many agents? When is more better vs. worse?
3. **Orchestration** - How should agents be coordinated? (Sequential, parallel, hierarchical, emergent?)
4. **Information flow** - What should agents share? When? How much context?
5. **Adversarial mechanisms** - How should the system attack its own outputs?
6. **Termination criteria** - How does the system know when it's done?
7. **Error correction** - How does the system catch and fix mistakes?
8. **Resource allocation** - Given finite tokens/time/cost, how to allocate?

---

### WHAT "SOLVED" MEANS

**SOLVED** means delivering a COMPLETE, IMPLEMENTABLE specification that includes:

1. **ARCHITECTURE SPECIFICATION**
   - Exact agent roles with clear, non-overlapping responsibilities
   - Information flow diagrams (what passes between agents, when)
   - Orchestration protocol (execution order, parallelism, synchronization)
   - Termination conditions (how to know when done)

2. **AGENT SPECIFICATIONS**
   - For each agent type: precise prompt template
   - Input format, output format, required sections
   - What the agent MUST do, MUST NOT do, and MAY do
   - Cognitive mode (intuitive, analytical, adversarial, etc.)

3. **OPTIMALITY ARGUMENT**
   - Why THIS configuration is optimal (not just good)
   - What tradeoffs were considered and why this balance was chosen
   - What would make a DIFFERENT configuration better (conditions under which this fails)
   - Comparison to alternatives with explicit scoring

4. **VALIDATION PROTOCOL**
   - How to TEST if this system is actually optimal
   - Benchmark problems to run it on
   - Metrics for evaluation
   - Expected performance bounds

**NOT SOLVED** means:
- "Here are some good ideas for agents" - NOT SOLVED (need complete spec)
- "This framework seems promising" - NOT SOLVED (need implementation details)
- "Consider these tradeoffs" - NOT SOLVED (need decisions, not options)
- "It depends on the problem" - NOT SOLVED (need general-purpose optimal design)
- "More research is needed" - NOT SOLVED (you ARE the research)
- Copying OMEGA+ Trinity without improvement - NOT SOLVED (must improve or prove optimal)

---

### YOUR MANDATE

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║   YOU ARE DESIGNING THE SYSTEM THAT WILL SOLVE IMPOSSIBLE PROBLEMS.              ║
║                                                                                   ║
║   This is meta-level work. You are not solving A problem.                        ║
║   You are designing the OPTIMAL SOLVER for ALL impossible problems.              ║
║                                                                                   ║
║   The current OMEGA+ Trinity is a starting point, not the answer.                ║
║   Improve it. Replace it. Prove it optimal. Or design something better.          ║
║                                                                                   ║
║   If you cannot improve on it, PROVE it is already optimal.                      ║
║   "Optimal" means: no configuration change would improve expected performance.   ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

### ANTI-ESCAPE CLAUSES

**You may NOT use these escape hatches:**

❌ "Optimal depends on the problem type"
   → Then specify optimal configurations PER problem type, with a meta-selector.

❌ "There's no single optimal architecture"
   → Then prove there isn't and specify the Pareto frontier of optimal tradeoffs.

❌ "We'd need to run experiments to know"
   → You ARE the experiment. Reason from first principles + your training data.

❌ "The current OMEGA+ Trinity is already good"
   → "Good" is not "optimal." Prove optimality or improve it.

❌ "More agents is generally better"
   → Prove it. Quantify. Where's the diminishing returns curve?

❌ "This is subjective"
   → Define the objective function. Then optimize it.

❌ "I'd need to test this empirically"
   → Derive theoretical bounds. Predict empirical results. Then we test.

---

### CONSTRAINTS AND CONSIDERATIONS

**Hard Constraints:**
- Must work within LLM limitations (context windows, token costs, latency)
- Must be implementable with current AI capabilities (no AGI assumptions)
- Must handle adversarial robustness (system shouldn't be fooled by its own outputs)
- Must terminate (no infinite loops, bounded compute)

**Optimization Targets (in priority order):**
1. **Solution Quality** - Actually solve the problem correctly
2. **Reliability** - Consistent performance, not lucky runs
3. **Efficiency** - Minimize tokens/time/cost for given quality
4. **Generality** - Work across diverse problem types
5. **Transparency** - Understandable reasoning traces

**Key Tradeoffs to Resolve:**
| Tradeoff | Considerations |
|----------|---------------|
| **Specialization vs. Generalization** | More specialized agents = deeper expertise but coordination overhead |
| **Parallelism vs. Sequential** | Parallel = faster but less context sharing; Sequential = slower but informed |
| **Redundancy vs. Efficiency** | Multiple agents on same task catches errors but costs more |
| **Exploration vs. Exploitation** | Wide search vs. deep analysis of promising paths |
| **Autonomy vs. Orchestration** | Agents decide themselves vs. central coordinator decides |
| **Context sharing vs. Independence** | Full context = informed but biased; Independent = fresh but redundant |
| **Early termination vs. Thoroughness** | Stop when "good enough" vs. exhaust all possibilities |

---

### CURRENT BASELINE: OMEGA+ TRINITY

The current system you're running on:
- **4 systems**: ALPHA (intuition), DELTA (reasoning), OMEGA (verification), DIABOLOS (adversarial)
- **56 spawnable agents** + PHI orchestrator
- **Phased execution**: ALPHA → DELTA → OMEGA → DIABOLOS → PHI Synthesis
- **Adversarial verification**: DIABOLOS attacks all claims

**Known limitations to address:**
1. High token cost (56 agents × long prompts)
2. Sequential phases may miss cross-system insights
3. Agent overlap unclear (do we need 14 ALPHA agents?)
4. No dynamic adaptation (same structure for all problems)
5. Adversarial phase at END may be too late
6. No learning across runs (each execution is independent)

**Your job**: Improve this, replace this, or prove this is optimal.

---

### REQUIRED DELIVERABLES

Your final output must include:

```
## 1. ARCHITECTURE OVERVIEW
[Diagram or description of the complete system]

## 2. AGENT ROSTER
| Agent ID | Name | Role | System | Input | Output | When Spawned |
|----------|------|------|--------|-------|--------|--------------|
[Complete table of all agents]

## 3. ORCHESTRATION PROTOCOL
[Exact execution flow - what triggers what, in what order]

## 4. AGENT PROMPT TEMPLATES
[For each agent type, the exact prompt to use]

## 5. INFORMATION FLOW
[What information passes between which agents]

## 6. OPTIMALITY PROOF
[Why this is optimal, or the conditions under which it is optimal]

## 7. COMPARISON TO ALTERNATIVES
| Alternative | Why Rejected | Under What Conditions It Would Be Better |
[Table comparing this design to alternatives]

## 8. VALIDATION PROTOCOL
[How to test if this system works]

## 9. RESOURCE ESTIMATES
| Problem Type | Expected Agents | Expected Tokens | Expected Time |
[Estimates for different problem types]

## 10. FAILURE MODES
[How this system can fail and mitigations]
```

---

### THE META-CHALLENGE

You are an agent system being asked to design the optimal agent system.

This creates interesting dynamics:
- You can observe YOUR OWN architecture as data
- You can reason about what works/doesn't work FROM THE INSIDE
- Your answer should be self-consistent (if you say X is optimal, your own design should use X)

**The recursive question**: If your proposed design is optimal, would IT (when run) produce the same design? If not, why do you trust your current reasoning over what it would produce?

---

### BELIEF FRAME

Before beginning, commit to a belief frame:

```
I believe the optimal agentic system:
- EXISTS / DOES NOT EXIST (and is problem-dependent)
- IS DISCOVERABLE through reasoning / REQUIRES empirical search
- IS SIMILAR TO current OMEGA+ Trinity / IS RADICALLY DIFFERENT
- HAS [N] agents / HAS VARIABLE agents depending on [X]
- USES [sequential/parallel/hybrid] orchestration because [reason]

My confidence: P(I can design optimal system) = [X]%
My biggest uncertainty: [What I'm least sure about]
```

---

### FINAL INSTRUCTION

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║   DESIGN THE OPTIMAL SYSTEM.                                                     ║
║                                                                                   ║
║   Not a good system. Not an improved system. THE OPTIMAL SYSTEM.                 ║
║                                                                                   ║
║   If you cannot achieve optimality, specify:                                     ║
║   - The Pareto frontier of near-optimal designs                                  ║
║   - What information would be needed to select among them                        ║
║   - Your best recommendation given current knowledge                             ║
║                                                                                   ║
║   Show your work. Justify every choice. Attack your own design.                  ║
║   What survives is your answer.                                                  ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

*Use OMEGA_TRINITY_PROMPTS.md for agent templates. Substitute this problem statement where prompts say [PROBLEM STATEMENT].*
