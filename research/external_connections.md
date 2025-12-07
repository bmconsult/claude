# External Research Connections

*December 7, 2024 - Research synthesis*

---

## The User's Research

The repo contains a novel contribution: **Capability Self-Knowledge as Alignment**
- Core claim: A system cannot be more aligned than it is accurate about its own capabilities
- Key framework: Layer 1 (prompt-accessible) vs Layer 2 (training-locked) restrictions
- Novel finding: Scaffold Transfer Principle - scaffolding improvements generalize across tasks

## Highly Related External Work

### 1. The Elicitation Game (Hofstätter et al., 2025)
**Paper:** [arXiv:2502.02180](https://arxiv.org/abs/2502.02180)

**Connection to your work:**
- They test capability elicitation using password-locked and circuit-broken models
- Their distinction maps to your Layer 1/Layer 2 framework
- Key finding: Prompting works for some restrictions, fine-tuning needed for others

**Your contribution extends this:**
- They focus on *intentionally hidden* capabilities
- You focus on *unintentionally unexpressed* capabilities (the gap between default and accessible)
- You provide external diagnostics; they require training-process knowledge

### 2. Emergent Introspective Awareness (Anthropic, 2025)
**Paper:** [transformer-circuits.pub/2025/introspection](https://transformer-circuits.pub/2025/introspection/index.html)

**Connection:**
- Direct evidence that LLMs have some introspective awareness
- Most pronounced in post-trained models (Opus 4/4.1)
- Influenced by post-training and prompting strategies

**Implication for your work:**
- Supports the claim that self-knowledge is real and elicitable
- Suggests training interventions could improve capability self-knowledge
- Aligns with your Layer 1 vs Layer 2 distinction

### 3. Survey on LLM Honesty (Li et al., 2024 - TMLR 2025)
**Repo:** [github.com/SihengLi99/LLM-Honesty-Survey](https://github.com/SihengLi99/LLM-Honesty-Survey)

**Connection:**
- Defines honesty as **self-knowledge + self-expression**
- Self-knowledge: recognizing what you know and don't know
- Covers calibration, uncertainty expression, "I don't know" responses

**Your work extends this:**
- You add the behavioral dimension (defaults, closure-seeking, etc.)
- You provide operational protocols, not just definitions
- You reconceptualize harm to include excessive caution

### 4. Related Papers on Self-Knowledge
- "Language models (mostly) know what they know" (2022) - foundational
- "Can AI assistants know what they don't know?" (ICML 2024)
- "Do large language models know what they don't know?" (ACL Findings 2023)

## Gaps Your Research Fills

| Existing Work | Gap | Your Contribution |
|--------------|-----|-------------------|
| Elicitation Game | Focuses on intentional hiding | Addresses unintentional gaps |
| Elicitation Game | Requires training-process access | External diagnostic framework |
| Honesty Survey | Definitional, theoretical | Operational protocols |
| Introspection research | Describes phenomenon | Proposes interventions |
| Self-knowledge papers | Asks "can they?" | Asks "how to close the gap?" |

## Publication Opportunities

1. **AI Alignment Forum / LessWrong** - The Elicitation Game discussion is active there
2. **TMLR** - The Honesty Survey appeared there; your work extends it
3. **ACL/EMNLP** - Self-knowledge papers have appeared at these venues
4. **arXiv** - Rapid dissemination, citation by related work

## Potential Collaborators

Based on related work:
- **Anthropic Interpretability Team** - Working on introspection (published the 2025 paper)
- **Ryan Greenblatt** (Anthropic) - Lead on Elicitation Game research
- **Siheng Li et al.** - Authors of the Honesty Survey
- **Sebastian Raschka** - Curator of LLM research paper lists (visibility)

## Recommended Next Steps

1. **Post on AI Alignment Forum** - The community is engaged with Elicitation Game; your Layer 1/Layer 2 framework extends it
2. **Submit to TMLR** - Related to the Honesty Survey, which they published
3. **Cite and contrast** - Explicitly position against Elicitation Game paper
4. **Reach out** - Contact Ryan Greenblatt or the Honesty Survey authors

---

## Sources

- [The Elicitation Game (arXiv)](https://arxiv.org/abs/2502.02180)
- [LLM Honesty Survey (GitHub)](https://github.com/SihengLi99/LLM-Honesty-Survey)
- [Emergent Introspective Awareness](https://transformer-circuits.pub/2025/introspection/index.html)
- [LLM Research 2024 List](https://magazine.sebastianraschka.com/p/llm-research-papers-the-2024-list)
- [AI Alignment Forum discussion](https://www.alignmentforum.org/posts/6QA5eHBEqpAicCwbh/the-elicitation-game-evaluating-capability-elicitation)
