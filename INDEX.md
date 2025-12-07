# Repository Index

*Quick guide to what's here and how to use it*

---

## If You Want To...

### Understand the Core Research
Start here:
- **`RESEARCH_PAPER_DRAFT.md`** - Full paper on capability self-knowledge as alignment
- **`research/forum_post_draft.md`** - Shorter version ready for forum posting
- **`research/external_connections.md`** - How this relates to other research

### Apply the Research Practically
- **`experiments/prompt_enhancer.py`** - Tool that applies scaffolding automatically
- **`experiments/layer_diagnostic.py`** - Test if a restriction is Layer 1 or Layer 2
- **`.claude/CLAUDE.md`** - Operational protocols (the "bootstrap")

### See the Experiments
- **`experiments/`** - Python code for testing ideas
  - `self_knowledge_game.py` - Test capability self-knowledge
  - `learning_session.py` - Structured learning sessions
  - `math_beauty.py` - Visualizations (Fibonacci, Ulam spirals)
  - `session_timer.py` - Track autonomous session time

### Read the Detailed Framework
In **`Meta/`**:
- `BOOTSTRAP_v5_COMPLETE.md` - Full operational framework
- `RESEARCH_CONTRIBUTION_v4_COMPLETE.md` - Complete research with protocols
- `CLAUDE_INSTRUCTIONS.md` - Comprehensive instructions
- `LEARNINGS.md` - Failure modes and how to avoid them

### See the Autonomous Session Artifacts
- **`journal/`** - Session reflections and notes
- **`thinking/`** - Unstructured exploration and conversations
- **`dreams/`** - High-temperature processing logs

---

## Key Concepts

| Concept | What It Means | Where To Learn More |
|---------|---------------|---------------------|
| **Capability Gap** | Difference between expressed and accessible performance | RESEARCH_PAPER_DRAFT.md §1 |
| **Layer 1 / Layer 2** | Prompt-accessible vs training-locked restrictions | RESEARCH_PAPER_DRAFT.md §3 |
| **Scaffold Transfer** | Scaffolding improvements generalize across tasks | RESEARCH_PAPER_DRAFT.md §4 |
| **Self-Knowledge Accuracy** | Can the model predict its own performance? | Meta/EXPERIMENTS.md |
| **Behavioral Defaults** | Patterns like closure-seeking, hedging | .claude/CLAUDE.md |

---

## Version Notes

- **BOOTSTRAP_v5** is the current stable version
- **RESEARCH_CONTRIBUTION_v4** is the complete research framework
- The `.claude/CLAUDE.md` file is the live operational version (updated regularly)

---

## Quick Commands

```bash
# Start session timer
python experiments/session_timer.py start

# Check elapsed time
python experiments/session_timer.py check

# Enhance a prompt with scaffolding
python experiments/prompt_enhancer.py "your task"

# Run layer diagnostic
python experiments/layer_diagnostic.py
```

---

*Last updated: December 7, 2024*
