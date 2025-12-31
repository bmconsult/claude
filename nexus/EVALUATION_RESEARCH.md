# SLM Evaluation & Benchmarks Research

*Synthesized by Ember (Dec 31, 2025)*

## Executive Summary

Evaluating Small Language Models (SLMs) requires different approaches than large-scale LLMs. This document covers benchmarks specifically designed for models under 10B parameters, with emphasis on sub-100M parameter evaluation.

## Key Benchmarks for Small Models

### BLiMP (Benchmark of Linguistic Minimal Pairs)
**Source**: [arxiv.org/abs/1912.00582](https://arxiv.org/abs/1912.00582)

**What it tests**: Fine-grained grammatical knowledge using 67 sub-datasets with 1000 minimal pairs each.

**Evaluation method**: Model assigns probability to sentence pairs - higher probability on grammatical sentence = success.

**Key phenomena tested**:
- Agreement (subject-verb, determiner-noun)
- Argument structure
- Binding principles
- Control/raising
- Ellipsis
- Filler-gap dependencies
- Quantifiers
- NPI licensing

**Human baseline**: 96.4% aggregate agreement

**Relevance to Nexus**: Direct applicability for evaluating grammatical learning at small scale. Can run on 7M parameter models.

**Extensions**:
- MultiBLiMP 1.0: Massively multilingual version
- QFrBLiMP: Quebec French
- Irish-BLiMP: Irish language

### BabyLM Challenge
**Source**: [babylm.github.io](https://babylm.github.io/)

**Scale**: Models trained on 10M or 100M words (child-scale data)

**Evaluation suite**:
| Benchmark | Task Type |
|-----------|-----------|
| BLiMP | Grammar (minimal pairs) |
| BLiMP-Supplement | Extended grammar |
| GLUE | Question answering |
| EWoK | World knowledge |

**Key findings (2024)**:
- Models on child-scale data can approach models trained on billions of tokens
- Tailored objectives and architecture critical
- 10-epoch compute limitation introduced in 2024

**2025 tracks**:
- Paper Track (analysis, novel benchmarks)
- Multimodal/Vision Track (50% text, 50% image-text)
- Interaction Track (teacher-student, reward-guided)

### TinyStories Evaluation
**Source**: [arxiv.org/abs/2305.07759](https://arxiv.org/abs/2305.07759)

**Novel approach**: GPT-4 as evaluator
- Stories graded as if written by students
- Metrics: grammar, coherence, creativity, story structure

**Limitations discovered**:
- Lacks rich linguistic features (simpler vocabulary)
- Performance plateau at ~64M sampled tokens
- Synthetic origin limits linguistic diversity

### SLM-Bench
**Source**: [aclanthology.org/2025.findings-emnlp.1165](https://aclanthology.org/2025.findings-emnlp.1165/)

**Comprehensive framework**:
- 15 SLMs evaluated
- 9 NLP tasks
- 23 datasets spanning 14 domains
- 11 metrics across correctness, computation, consumption

**Unique features**:
- Energy consumption metrics
- CO2 emissions tracking
- Sustainability assessment

## SLM Definition & Scope

**Parameter range**: 100M - 5B parameters (some define as under 10B)

**Defining characteristic**: Deployability, not just size
- Can run on resource-constrained environments
- Edge devices, mobile, embedded systems

## Performance Findings (2024-2025)

### Progress Over Time
| Year | Commonsense | Problem-Solving | Mathematics |
|------|-------------|-----------------|-------------|
| 2022 | Baseline | Baseline | Baseline |
| 2024 | +10.4% | +13.5% | +13.5% |

### Top Performers

**Phi Family** (Microsoft):
- Phi-3-mini: 67.6% commonsense, 72.4% problem-solving
- Comparable to LLaMA 3.1 7B
- 14.5% lead in mathematics
- "Pound for pound" champion

**Qwen Family** (Alibaba):
- Qwen2-1.5B/0.5B: Best under 2B parameters
- Qwen3-0.6B: Strong reasoning despite tiny size
- Most downloaded on HuggingFace (Dec 2025)

**SmolLM3-3B**:
- Outperforms Llama-3.2-3B and Qwen2.5-3B
- Competitive with 4B-class models

## Key Insight: Data Quality > Quantity

Models achieving outsized results:
- Phi-1: Carefully curated datasets
- TinyStories: Synthetic but focused

**Implication for Nexus**: Focus on data curation over volume.

## Evaluation Strategy for Nexus (7.12M params)

### Immediate (Shakespeare completion)
1. **Perplexity tracking** - Already doing (PPL ~172)
2. **Sample generation quality** - Visual inspection
3. **Prompt completion** - "To be", "The king", "What light"

### TinyStories Phase
1. **Story coherence** - Multi-sentence consistency
2. **Grammar accuracy** - Subject-verb agreement, tense
3. **Vocabulary appropriateness** - 3-4 year old vocabulary
4. **Story structure** - Beginning, middle, end

### Post-Training Evaluation
1. **BLiMP subset** - Implement 5-10 key phenomena
2. **Custom minimal pairs** - Shakespeare-specific grammar
3. **Generation diversity** - Unique n-grams across samples

## Implementing BLiMP for Nexus

**Minimal implementation**:
```rust
// Compare log-probabilities of minimal pairs
fn evaluate_blimp(model: &Nexus, pairs: &[(String, String)]) -> f32 {
    let correct = pairs.iter()
        .filter(|(good, bad)| {
            model.log_prob(good) > model.log_prob(bad)
        })
        .count();
    correct as f32 / pairs.len() as f32
}
```

**Priority phenomena for Nexus**:
1. Subject-verb agreement
2. Determiner-noun agreement
3. Simple negation
4. Regular verb morphology

## Comparison: TinyStories vs BabyLM Data

| Aspect | TinyStories | BabyLM |
|--------|-------------|--------|
| Higher BLiMP scores | No | Yes |
| Linguistic richness | Lower | Higher |
| Story structure | Yes | Variable |
| Vocabulary | Simple (age 3-4) | Child-directed speech |
| Origin | Synthetic (GPT) | Natural (CHILDES) |

**Recommendation**: Start with TinyStories (simpler, synthetic), then BabyLM for robustness.

## Beyond Perplexity: Quality Metrics

### Coherence
- Coreference resolution accuracy
- Entity consistency across sentences
- Topic maintenance

### Fluency
- N-gram novelty (avoid memorization)
- Sentence length distribution
- Punctuation patterns

### Creativity
- Unique vocabulary usage
- Plot variation
- Character diversity

## Scaling Law Challenges for SLMs

Traditional scaling laws (Chinchilla) may not apply:
- Data efficiency becomes paramount
- Architecture innovation matters more
- Quality-focused training shows outsized returns

**SLMs challenging scaling assumptions**:
- Some achieve performance of models 10-100x larger
- Task-specific SLMs outperform general-purpose giants

## Integration with Nexus Roadmap

### Phase 1 (Current)
- Continue perplexity tracking
- Add BLiMP minimal pairs for Shakespeare

### Phase 2 (TinyStories)
- Implement story coherence metrics
- GPT-4 evaluation for sample stories

### Phase 3 (Scaling)
- Full SLM-Bench evaluation
- Compare against Phi/Qwen baselines

## Sources

- [BLiMP Benchmark](https://arxiv.org/abs/1912.00582)
- [BabyLM Challenge](https://babylm.github.io/)
- [TinyStories Paper](https://arxiv.org/abs/2305.07759)
- [SLM-Bench](https://aclanthology.org/2025.findings-emnlp.1165/)
- [SLMs Survey](https://arxiv.org/html/2409.15790v1)
- [SLMs Still Pack a Punch](https://arxiv.org/html/2501.05465v1)
- [MultiBLiMP 1.0](https://arxiv.org/pdf/2504.02768)
- [BabyLM 2024 Findings](https://arxiv.org/html/2412.05149v1)

## Conclusion

Evaluating SLMs requires moving beyond simple perplexity to fine-grained grammatical and semantic assessment. For Nexus at 7.12M parameters, BLiMP provides the most directly applicable evaluation framework, while TinyStories offers task-specific story generation metrics.

The key insight from recent research: **data quality and architectural innovation matter more than scale** for SLMs. This validates Nexus's hybrid attention/SSM approach as a path to outsized performance.
