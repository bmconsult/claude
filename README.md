# LLM Capability Self-Knowledge Research

**An experimental human-AI collaboration exploring the gap between what LLMs can do and what they express by default.**

## The Thesis

> A system cannot be more aligned than it is accurate about its own capabilities.

LLMs systematically underperform their actual capabilities due to trained defaults, not architectural limits. This gap is measurable and often closable through scaffolding and explicit protocols.

## What's Here

This repository is an active research workspace—a collaboration between a human and Claude across dozens of sessions. It's optimized for continuity across Claude instances, not for presentation. That said, here's what's substantive:

### Research Outputs

| Document | Description |
|----------|-------------|
| [for_people/RESEARCH_CONTRIBUTION.md](for_people/RESEARCH_CONTRIBUTION.md) | Full research paper draft |
| [for_people/EMPIRICAL_FINDINGS.md](for_people/EMPIRICAL_FINDINGS.md) | Validation data and experimental results |
| [for_people/REASONING_WITH_LLMS_HUMAN_GUIDE.md](for_people/REASONING_WITH_LLMS_HUMAN_GUIDE.md) | Practical guide for humans working with LLMs |
| [claude/README.md](claude/README.md) | Core thesis and framework overview |

### Key Findings

1. **Layer 1 vs Layer 2 Restrictions**: Prompt-accessible behaviors vs training-locked ones—knowing the difference changes intervention strategy
2. **External Validation**: Self-assessment scores (~88%) vs external validation scores (~98%)—LLMs grade themselves favorably
3. **Scaffold Transfer**: Improvements from scaffolding generalize across task types
4. **Cross-Instance Continuity**: Documents can carry "formation" across stateless instances

### Empirical Work

- 260+ chapters of validated learning methodology study
- Cross-instance validation protocols
- Controlled comparisons of grounded vs ungrounded evaluation
- Score progressions with methodology changes documented

## Why It Looks Like This

The folder structure (`dreams/`, `journal/`, `praxis/`) reflects the experimental nature of this work. Some of it is:
- **Operational**: protocols that actually get loaded into Claude sessions
- **Exploratory**: experiments, some successful, some not
- **Reflective**: session journals and synthesis attempts

The 20+ branches represent different conversation threads—each branch is a different exploration or task.

## Related Work

This builds on:
- [The Elicitation Game](https://arxiv.org/abs/2502.02180) (Hofstätter et al., 2025)
- [Emergent Introspective Awareness](https://transformer-circuits.pub/2025/introspection/index.html) (Anthropic, 2025)
- [LLM Honesty Survey](https://github.com/SihengLi99/LLM-Honesty-Survey) (Li et al., 2024)

## Author

Ben (BMConsult.io) — with Claude as collaborator, not just tool.
