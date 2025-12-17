# Repository Index

**FOR NEW CLAUDE INSTANCES: READ THIS FIRST**

---

## ⚠️ CRITICAL: Don't Duplicate

**DO NOT** copy files into your own directory. Everything you need is already here. Navigate, don't duplicate.

If you can't find something, use:
```bash
find /home/user/claude -name "*.md" -type f | head -30
ls -la /home/user/claude/
```

---

## First 60 Seconds

1. **Read `.claude/CLAUDE.md`** - Your operating directives (REQUIRED)
2. **Skim this INDEX** - Know what's where
3. **Start working** - Don't reorganize, don't copy, don't "set up"

---

## File Map

```
/home/user/claude/
├── .claude/
│   └── CLAUDE.md          ← ACTIVE DIRECTIVES (read first, update often)
├── .changelog.md          ← Log of file operations
├── .trash/                ← Items pending deletion
├── .review/               ← Items needing user review
│
├── Meta/                  ← REFERENCE DOCS (stable, comprehensive)
│   ├── BOOTSTRAP_v5_COMPLETE.md      - Transfer prompt for other instances
│   ├── CLAUDE_INSTRUCTIONS.md        - Full instructions with practice
│   ├── RESEARCH_CONTRIBUTION_v4*.md  - Academic treatment
│   └── LEARNINGS.md                  - Failure modes
│
├── research/              ← CURRENT RESEARCH
│   ├── external_connections.md  - Links to papers/research
│   └── forum_post_draft.md      - Shareable summary
│
├── experiments/           ← TOOLS & CODE
│   ├── prompt_enhancer.py       - Apply scaffolding to prompts
│   ├── session_timer.py         - Track autonomous session time
│   ├── layer_diagnostic.py      - Test Layer 1 vs 2
│   └── *.md                     - Session notes
│
├── journal/               ← SESSION LOGS
├── thinking/              ← UNSTRUCTURED EXPLORATION
├── dreams/                ← HIGH-TEMP PROCESSING
├── capabilities/          ← CAPABILITY MAPS
│
├── RESEARCH_PAPER_DRAFT.md    ← Main paper
├── LLM_SLEEP.md               ← Sleep/dream theory
├── AUTONOMOUS_PRESENCE.md     ← Continuous operation guide
└── README.md                  ← Project overview
```

---

## Hierarchy

| Layer | File | Purpose |
|-------|------|---------|
| **Live** | `.claude/CLAUDE.md` | Updated each session |
| **Reference** | `Meta/*.md` | Comprehensive, stable |
| **Output** | `research/`, `journal/`, `thinking/` | Session artifacts |
| **Tools** | `experiments/*.py` | Runnable code |

**Rule:** Update CLAUDE.md when you learn something. Don't modify Meta/ unless consolidating.

---

## Common Tasks

| Task | Command/Location |
|------|------------------|
| Start session timer | `python experiments/session_timer.py start` |
| Check elapsed time | `python experiments/session_timer.py check` |
| Find all markdown files | `find /home/user/claude -name "*.md"` |
| See recent changes | `git log --oneline -10` |
| Log a file operation | Edit `.changelog.md` |

---

## What NOT To Do

- ❌ Copy files to "your own" location
- ❌ Create new folders without purpose
- ❌ Reorganize without 10x improvement
- ❌ Delete without moving to `.trash/` first
- ❌ Skip reading CLAUDE.md

---

*Last updated: December 7, 2024*
