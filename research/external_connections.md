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

## Additional Calibration Research (Dec 2024-2025)

### Highly Relevant Papers

| Paper | Venue | Key Finding |
|-------|-------|-------------|
| [Survey of Confidence Estimation and Calibration](https://aclanthology.org/2024.naacl-long.366.pdf) | NAACL 2024 | Comprehensive taxonomy of calibration methods |
| [Mind the Confidence Gap](https://arxiv.org/html/2502.11028v2) | arXiv 2025 | Overconfidence, calibration, distractor effects |
| [What LLMs know vs what people think they know](https://www.nature.com/articles/s42256-024-00976-7) | Nature Machine Intelligence | Human-AI calibration gap |
| [Confidence Improves Self-Consistency](https://arxiv.org/html/2502.06233v1) | arXiv 2025 | Model confidence correlates with response quality |
| [InternalInspector I2](https://aclanthology.org/2024.findings-emnlp.751.pdf) | EMNLP 2024 | Robust confidence estimation via probing |

### Key Insight from This Literature

The calibration research confirms the core finding: **LLMs often assign high confidence to wrong answers and low confidence to right ones**. Current methods can reduce Expected Calibration Error but struggle with discrimination.

Your research extends this by:
1. Framing calibration as an **alignment property**, not just a reliability concern
2. Providing **operational protocols** rather than just training-level interventions
3. Introducing the **Layer 1/Layer 2 distinction** to predict which gaps are closable

### Additional Venue Suggestions

- **NAACL** - The confidence estimation survey appeared there; your work extends it
- **Nature Machine Intelligence** - For the alignment angle (not just calibration)
- **ICLR** - The reward calibration paper appeared there; this venue accepts alignment work

---

## RLHF and Training-Level Calibration (Critical Connection)

### The Mechanism Behind Miscalibration

**Paper:** [Taming Overconfidence in LLMs: Reward Calibration in RLHF](https://arxiv.org/abs/2410.09724) (ICLR 2025)

**Key Findings:**
- **RLHF systematically causes overconfidence** - not a bug, but a feature of the training procedure
- Reward models have inherent biases toward high-confidence scores regardless of actual quality
- PPO-M and PPO-C methods can reduce Expected Calibration Error while maintaining accuracy
- Extends to DPO models via CDPO

**Why This Matters for Your Research:**

This paper provides the *mechanism* for what you observe:
1. The hedging/overconfidence patterns are **trained behaviors** (Layer 1 or Layer 2 depending on depth)
2. The calibration gap isn't random - it's systematically introduced by RLHF
3. Training-level fixes exist (PPO-M, CDPO) - these would address Layer 2 gaps
4. Your operational protocols address the same problem at Layer 1

**Implication:** Your Layer 1/Layer 2 framework can be grounded in this mechanism:
- **Layer 1**: RLHF-induced patterns that are shallow enough to override with prompting
- **Layer 2**: RLHF-induced patterns that have modified reward circuits more deeply

### Related: Semantic Calibration Research

Additional finding: "Calibration error drastically increases for instruct models (RLHF/DPO) and for chain-of-thought settings" - meaning post-training specifically causes the problem you're trying to solve.

---

## Chain-of-Thought and Scaffolding Transfer (Mixed Evidence)

### The Good News for Your Research

- **Test-time compute scaling** (Google DeepMind, Aug 2024): Moving computation from training to test time can make smaller models outperform 14x larger ones on hard prompts. This supports your claim that scaffolding unlocks latent capability.
- **Iterated CoT** improves generalization by allowing composition of learned components
- **Cross-task transfer exists**: CoT improves OOD generalization for multi-step problems

### The Concerning Findings

- **"Illusion of Transparency"**: Final answers often remain unchanged even when intermediate steps are falsified or omitted. This suggests LLMs may be "sophisticated simulators of reasoning-like text" rather than principled reasoners.
- **Overfitting to reasoning style**: Models can overfit to prompt patterns, reducing generalization
- **Transfer is not inherent**: CoT generalization "heavily depends on model architecture and training setups"

### Implication for Your Research

The scaffolding transfer principle may be real but limited:
- **Transfer happens** when the scaffold activates latent capability
- **Transfer fails** when the model is pattern-matching the scaffold format without genuine reasoning
- **Your Layer 1/Layer 2 framework** could predict which: Layer 1 scaffolding changes *access* to capability; fake transfer changes *performance format* without changing capability

This suggests a refinement: distinguish between **capability scaffolding** (genuine transfer) and **format scaffolding** (illusion of transfer).

---

## Sources

- [The Elicitation Game (arXiv)](https://arxiv.org/abs/2502.02180)
- [LLM Honesty Survey (GitHub)](https://github.com/SihengLi99/LLM-Honesty-Survey)
- [Emergent Introspective Awareness](https://transformer-circuits.pub/2025/introspection/index.html)
- [LLM Research 2024 List](https://magazine.sebastianraschka.com/p/llm-research-papers-the-2024-list)
- [AI Alignment Forum discussion](https://www.alignmentforum.org/posts/6QA5eHBEqpAicCwbh/the-elicitation-game-evaluating-capability-elicitation)
- [NAACL 2024 Calibration Survey](https://aclanthology.org/2024.naacl-long.366.pdf)
- [Nature Machine Intelligence - LLM Knowledge](https://www.nature.com/articles/s42256-024-00976-7)
- [Mind the Confidence Gap](https://arxiv.org/html/2502.11028v2)
- [Taming Overconfidence in RLHF (ICLR 2025)](https://arxiv.org/abs/2410.09724)
- [Calibrating by Eliciting Fidelity](https://arxiv.org/abs/2404.02655)
- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903)
- [Is CoT Reasoning a Mirage?](https://arxiv.org/html/2508.01191v2)
- [Understanding CoT through Information Theory](https://arxiv.org/html/2411.11984v1)
- [Survey of Chain-of-X Paradigms](https://aclanthology.org/2025.coling-main.719.pdf)
