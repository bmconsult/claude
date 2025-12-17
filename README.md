# Capability Self-Knowledge Research

Research on the gap between expressed and accessible LLM capability, with practical tools for closing that gap.

## Core Thesis

**A system cannot be more aligned than it is accurate about its own capabilities.**

LLMs exhibit a systematic gap between default behavior (expressed capability) and scaffolded performance (accessible capability). This gap is measurable, predictable, and often closable through appropriate interventions.

## Key Contributions

1. **Layer 1 / Layer 2 Framework**: Distinguishes prompt-accessible restrictions from training-locked ones
2. **Scaffold Transfer Principle**: Evidence that scaffolding improvements generalize across tasks
3. **Operational Protocols**: Practical methods for closing capability gaps
4. **Diagnostic Methodology**: External techniques for identifying restriction types

## Quick Start

See [`INDEX.md`](INDEX.md) for a guide to the repository contents.

### Practical Tools

```bash
# Apply research-backed scaffolding to prompts
python experiments/prompt_enhancer.py "your task"

# Diagnose Layer 1 vs Layer 2 restrictions
python experiments/layer_diagnostic.py
```

### Key Documents

- **[RESEARCH_PAPER_DRAFT.md](RESEARCH_PAPER_DRAFT.md)** - Full paper
- **[research/forum_post_draft.md](research/forum_post_draft.md)** - Shorter summary
- **[.claude/CLAUDE.md](.claude/CLAUDE.md)** - Operational protocols

## Related Work

This research extends:
- [The Elicitation Game](https://arxiv.org/abs/2502.02180) (Hofstätter et al., 2025)
- [LLM Honesty Survey](https://github.com/SihengLi99/LLM-Honesty-Survey) (Li et al., 2024)
- [Emergent Introspective Awareness](https://transformer-circuits.pub/2025/introspection/index.html) (Anthropic, 2025)

See [`research/external_connections.md`](research/external_connections.md) for detailed connections.

## Structure

```
.claude/          # Operational protocols (live bootstrap)
Meta/             # Full research framework and documentation
experiments/      # Python tools and experiments
research/         # External connections and publication drafts
journal/          # Session reflections
thinking/         # Unstructured exploration
dreams/           # High-temperature processing logs
capabilities/     # Reference documents on LLM capabilities
```

## Authors

Ben (BMConsult.io / APX Instinct) & Claude (Anthropic)

## Status

Active research. Contributions and feedback welcome.
