# AI Mastery List 4.0: BEYOND
## Frontier Paradigms, Theoretical Foundations & Emergent Architectures

*December 2025 — The bleeding edge of what's possible*

---

## I. POST-TRANSFORMER ARCHITECTURES

### State Space Models (SSM) & Mamba

The first credible alternative to attention-based transformers for language modeling.

**Core Innovation**:
- **Selective State Spaces (S6)**: SSM parameters become functions of input, enabling content-aware processing
- **Linear-time complexity**: O(n) vs O(n²) attention — scaling to million-length sequences
- **No KV cache needed**: 4-5× higher inference throughput than transformers

**Mamba Architecture**:
```
Input → Linear Projection → Conv1d → Selective SSM → Output
                              ↓
                    [Makes token-dependent: A, B, C matrices]
```

**Key Equations**:
- State evolution: `h(t) = Ah(t-1) + Bx(t)`
- Output: `y(t) = Ch(t) + Dx(t)`
- **HiPPO initialization**: Handles long-range dependencies via polynomial projection operators

**Mamba-2 (Structured State Space Duality)**:
- Mathematical bridge between SSMs and attention
- Restricts A matrix to scalar × identity for matmul efficiency
- SSD Algorithm: Rewrites computations to leverage tensor cores
- 2-8× faster training than Mamba-1 while preserving quality

**Hybrid Models**:
| Model | Architecture | Notes |
|-------|-------------|-------|
| Jamba | Mamba + Transformer + MoE | Interleaved blocks |
| Granite 4.0 | SSM + Attention layers | IBM production model |
| Codestral Mamba | Pure Mamba | Mistral code model |

**When SSM wins**: Long sequences, constant-time inference, memory-constrained edge
**When Transformer wins**: Tasks requiring precise attention patterns, in-context learning

---

## II. ALIGNMENT BEYOND RLHF

### Preference Optimization Landscape

**DPO (Direct Preference Optimization)**:
```
L_DPO = -log σ(β · (log π_θ(y_w|x)/π_ref(y_w|x) - log π_θ(y_l|x)/π_ref(y_l|x)))
```
- Eliminates reward model training
- Implicit reward: `r(x,y) = β log(π_θ(y|x)/π_ref(y|x)) + β log Z(x)`
- Issues: Verbosity bias, likelihood displacement, out-of-distribution exploitation

**IPO (Identity Preference Optimization)**:
- Addresses DPO overfitting via regularization
- Removes Bradley-Terry assumption that pointwise rewards replace pairwise preferences
- Better handling of deterministic preferences

**KTO (Kahneman-Tversky Optimization)**:
- Based on Prospect Theory: "loss aversion" — pain of loss > pleasure of gain
- Only requires binary signal (desirable/undesirable) — no preference pairs needed
- **Key finding**: Without SFT first, DPO models ramble and hallucinate; KTO does not
- 90% of desirable examples can be discarded and KTO still outperforms DPO

**SimPO (Simple Preference Optimization)**:
- Aligns reward and generation models more intuitively
- Better reward accuracy than DPO (52% → higher alignment)
- Length-normalized objectives

**ORPO, RLAIF, SPIN**: Other variants for specific data regimes

### The Preference Method Decision Tree

```
Have paired preference data?
├── Yes → Is it high quality with clear preferences?
│         ├── Yes → DPO or SimPO
│         └── No (noisy) → IPO
└── No → Do you have binary feedback?
         ├── Yes → KTO
         └── No → SPIN (self-play) or RLAIF (AI feedback)
```

---

## III. MECHANISTIC INTERPRETABILITY

### Sparse Autoencoders (SAEs)

**The Superposition Problem**:
- Models encode more features than neurons (overcomplete representation)
- Polysemanticity: Single neurons activate for multiple unrelated concepts
- Solution: Learn a sparse overcomplete basis that decomposes activations

**SAE Architecture**:
```
h → Encoder(h) → z (sparse) → Decoder(z) → h_reconstructed
```

**Key Variants**:
| Variant | Innovation | Use Case |
|---------|-----------|----------|
| TopK SAE | Only k largest latents non-zero | Direct L0 control |
| JumpReLU SAE | Improved reconstruction fidelity | Better feature capture |
| Gated SAE | Learned gating mechanism | Reduces absorption |
| BatchTopK | Batch-level sparsity constraint | Training stability |

**Gemma Scope**: DeepMind's suite of SAEs across Gemma 2 family — hundreds of pretrained SAEs

**SAE Applications**:
- **Feature steering**: Add/subtract feature directions to control behavior
- **Circuit discovery**: Map computations between features
- **Knowledge editing**: Selectively remove concepts
- **Hallucination detection**: Identify uncertainty features
- **Biology**: Applied to protein language models (ESM-2), genomics (Evo 2)

**Current Limitations**:
- SAE decomposition is not unique — depends on initialization
- Absorption: L1 regularization learns common feature combinations
- Scaling to frontier models still expensive

### Representation Engineering / Activation Steering

**Core Idea**: Identify linear directions in activation space that correspond to concepts, then add/subtract to steer behavior.

**Workflow**:
1. **Collect contrastive examples**: Positive/negative pairs for target concept
2. **Extract activations**: Record hidden states at specific layer/position
3. **Compute steering vector**: Mean difference between positive and negative activations
4. **Apply during inference**: Add scaled vector to activations

**Methods for Computing Concept Vectors**:
- **Difference-in-Means (DiM)**: `v = mean(positive) - mean(negative)`
- **Probing**: Train classifier on activations, use weights as direction
- **Contrast-Consistent Search (CCS)**: Find direction that maximizes contrast
- **SAE features**: Use learned SAE feature directions

**Application Methods**:
- **Addition**: `a_l + α·v_c` (add concept direction)
- **Rejection**: `a_l - (a_l·v_c)v_c` (remove concept component)
- **Nullspace projection**: Remove probe-recoverable information
- **Soft projection**: Conceptor matrices for composable steering

**Demonstrated Behaviors**:
- Honesty, truthfulness, sycophancy reduction
- Sentiment, emotion, writing style
- Safety behaviors, instruction following
- Bias mitigation (gender, racial, age)

**Key Papers**: Zou et al. 2023 "RepE", Turner et al. 2024 "Activation Addition"

---

## IV. LATENT REASONING

### Coconut (Chain of Continuous Thought)

**The Insight**: Language space may not be optimal for reasoning. Most tokens ensure coherence, not computation.

**Mechanism**:
```
Traditional CoT: Input → Token₁ → Token₂ → ... → Answer (discrete)
Coconut:         Input → Hidden₁ → Hidden₂ → ... → Answer (continuous)
```

Instead of decoding hidden states to tokens, feed them back as input embeddings directly.

**Emergent Behavior — Breadth-First Search**:
- Continuous thoughts can encode multiple alternative next steps simultaneously
- Model explores reasoning paths in parallel before converging
- Avoids premature commitment to single deterministic path

**Training Protocol**:
- Multi-stage curriculum: Start with full CoT, progressively replace tokens with latent steps
- Stage N: First N reasoning steps are latent, rest verbalized
- Requires reasoning traces for curriculum (limitation)

**Results**:
- Outperforms CoT on logical reasoning requiring substantial search
- Fewer tokens during inference (efficiency gain)
- Better accuracy-efficiency tradeoff

**Implications for Interpretability**:
- Latent reasoning is harder to inspect than verbal CoT
- Safety concern: Can't easily verify reasoning without token traces
- But: More computationally efficient, potentially more powerful

### Recursive Transformers & Mixture of Recursions (MoR)

**Recursive Transformers**: Reuse same layers multiple times (loop depth).
- Parameter efficiency: Fewer unique weights
- Can act as "programmable computers" (Giannou et al.)
- Excel at latent reasoning via recurrent depth

**Mixture of Recursions (2025)**:
- Dynamic recursion depth per token
- Expert-choice routing assigns optimal depth
- Recursion-wise KV caching: Selective storage across depth
- **Results**: 2× throughput vs standard transformers, reduced training FLOPs

**Token-Level Compute Allocation**:
- Content-rich tokens ("People", technical terms) → deeper recursion (3 steps)
- Function words ("and", punctuation) → shallow (2 steps)
- Semantically meaningful compute distribution

---

## V. SCALING LAWS & PHASE TRANSITIONS

### Chinchilla Scaling (Compute-Optimal Training)

**Core Finding**: For fixed compute C, scale model size N and data D equally.
- `N_opt(C) ∝ C^0.5`
- `D_opt(C) ∝ C^0.5`
- ~20 tokens per parameter for Chinchilla optimal

**But Production Reality**:
- Inference cost matters — smaller models trained longer save at deployment
- Llama 3 70B: 200 tokens/param (10× Chinchilla)
- Phi-3: 870 tokens/param (45× Chinchilla)
- **Finding**: Models continue improving up to 10,000 tokens/param

**Overtraining for Inference**:
```
More inference demand → Train smaller model on more data
```
| Tokens/Param | Training Compute | Inference Efficiency |
|--------------|------------------|---------------------|
| 20 (Chinchilla) | 1× | 1× |
| 200 | ~3× | 3.7× faster |
| 870 | ~10-15× | 5× faster |

### Grokking & Phase Transitions

**Grokking**: Sudden generalization long after training loss hits zero.
- Training accuracy: 100% quickly
- Test accuracy: Chance for many epochs
- Then: Sharp transition to near-perfect generalization

**Mechanistic Explanation**:
1. **Two circuits compete**: Memorization circuit (dense, high-norm) vs generalization circuit (sparse, efficient)
2. **Weight decay pressure**: Favors efficient circuits over time
3. **Circuit efficiency**: Generalizing circuit produces larger logits per unit norm

**Information-Theoretic View**:
- Before grokking: High redundancy (memorization)
- After grokking: High synergy (collective, generalizing)
- Synergy spike predicts grokking onset

**Emergent Capabilities in LLMs**:
- Same phenomenon at scale: Capabilities appear "suddenly" at certain thresholds
- But: May be measurement artifact (choice of evaluation metric)
- Critical data size (CDS): Below threshold → grokking; above → concurrent learning

**Phases in Training**:
1. **Confusion**: Underfitting even training set
2. **Memorization**: Low train loss, chance test performance
3. **Grokking transition**: Sharp test accuracy increase
4. **Generalization**: Both train and test optimal

---

## VI. WORLD MODELS & SIMULATION

### LLMs as World Models

**Definition**: A world model predicts how environment state changes given actions.

**WebDreamer Framework**:
- LLM "dreams" outcomes of candidate actions before executing
- Simulates state transitions in natural language
- Evaluates progress toward goal
- **4-5× more efficient** than tree search while competitive in accuracy

**Key Insight**: LLMs encode vast knowledge about web structures, protocols, user behaviors — sufficient for simulation without explicit training.

**World Model Systems (2024-2025)**:
| System | Organization | Domain |
|--------|-------------|--------|
| Cosmos | NVIDIA | Physical AI, robotics |
| Genie 3 | DeepMind | Interactive environments |
| V-JEPA 2 | Meta | Video understanding, robotics |
| GAIA-2 | Wayve | Autonomous driving |
| Sora 2 | OpenAI | Video generation |
| WorldGPT | Research | Multimodal state transitions |

**Capabilities Unlocked**:
- Sample efficiency via imagination
- Safety through simulation (test before deploy)
- Counterfactual and causal reasoning
- Perception-to-control bridge

**Evaluation Dimensions**:
- Closed-loop task utility
- Physical/geometric consistency
- Uncertainty and OOD detection
- Sim-to-real correlation

---

## VII. MODEL MERGING

### Combining Expert Models Without Retraining

**Task Vectors**: `τ = θ_finetuned - θ_base` (the learned delta)

**Methods**:

**SLERP (Spherical Linear Interpolation)**:
- Smooth interpolation between two models
- Preserves vector magnitude during blending
- Best for merging 2 similar models

**TIES-Merging**:
1. **Trim**: Keep top-k% most significant parameters, reset rest to zero
2. **Elect Signs**: Create unified sign vector via majority vote
3. **Merge**: Average trimmed vectors with consistent signs

**DARE (Drop And REscale)**:
- Randomly reset fine-tuned weights to base values (drop rate p)
- Rescale remaining by 1/(1-p)
- Works even at 90%+ drop rate
- Combine with TIES: dare_ties, dare_linear

**Merging Scaling Laws (2025)**:
- Power law relationship between merge quality and model scale
- Larger models are easier to merge (lower interference floor)
- Merging approaches multitask SFT performance at fraction of GPU-hours

**Best Practices**:
- Density 0.5-0.7 for most merges
- Weights should sum to ~1.0 (0.9-1.1 range)
- dare_ties often outperforms pure ties
- Test incrementally — merge 2-3 models at a time

**Frankenmerges (Passthrough)**:
- Concatenate layers from different models
- Creates exotic parameter counts (e.g., 9B from two 7B)
- Experimental but has produced impressive models (goliath-120b)

---

## VIII. DYNAMIC DEPTH & ADAPTIVE COMPUTE

### Mixture of Depths (MoD)

**Core Idea**: Not all tokens need the same amount of computation.
- Route tokens to skip layers based on learned router
- Router predicts: "Does this token need this layer?"

**Implementation**:
```
For each layer:
    route_score = Router(hidden_state)
    if route_score > threshold:
        hidden_state = Layer(hidden_state)
    else:
        hidden_state = hidden_state  # skip
```

**Router-Tuning**: Train only the router, freeze backbone
- Simple and effective for existing models
- Lower barrier than training from scratch

### Early Exit

**Mechanism**: Exit inference at intermediate layer if confidence is high enough.

**Challenges**:
1. **Missing KV cache**: Early-exited tokens lack KV pairs for later positions
2. **Batch inefficiency**: Tokens wait for slowest in batch
3. **Feature alignment**: Different depths produce different representations

**Solutions**:
- **FREE Framework**: Parallel decoding for KV computation
- **Recursive Transformers + MoR**: Parameter sharing enables efficient batching
- **Depth-wise batching**: Group tokens by required depth

**Speedups Reported**:
- 20-74% latency reduction (DEED)
- 2.8× speedup, 26% energy saving (edge video)
- 2.5× speedup in LLM reasoning (SpecExit)

---

## IX. THEORETICAL FOUNDATIONS

### Attention as Kernel Methods

The attention mechanism can be viewed through the lens of kernel methods:
```
Attention(Q,K,V) = softmax(QK^T/√d)V
```
This is essentially a weighted kernel regression where the kernel is:
```
k(q,k) = exp(q·k/√d)
```

**Linear Attention**: Replace softmax kernel with linear kernel for O(n) complexity.
- Trade-off: Loses some expressiveness
- Mamba-2's SSD shows equivalence between SSMs and structured attention

### Information Bottleneck in Transformers

**Hypothesis**: Middle layers compress input information before generating output.
- Early layers: Feature extraction
- Middle layers: Compression/abstraction
- Late layers: Task-specific generation

**Evidence**: 
- "Lost in the Middle" effect
- Probing accuracy varies by layer
- Residual stream bottleneck patterns

### Linear Representation Hypothesis

**Claim**: Features in LLMs are encoded as linear directions in activation space.

**Evidence**:
- Steering vectors work (adding directions changes behavior)
- Probes can recover concepts linearly
- SAE success suggests sparse linear decomposition

**Counterevidence**:
- Some features may be nonlinear
- Polysemanticity suggests compression
- Not all concepts have single directions

---

## X. MULTIMODAL & UNIFIED ARCHITECTURES

### Vision-Language Model Internals

**Architectures**:
- **Vision encoder** (ViT, CLIP) → **Projection** → **LLM**
- Image tokens interleaved with text tokens
- Cross-attention vs concatenation approaches

**Tokenization Strategies**:
| Method | Approach | Trade-off |
|--------|----------|-----------|
| Patch tokens | Fixed grid (16×16) | Simple but wasteful |
| Dynamic resolution | Adaptive patches | Better quality, variable length |
| Perceiver | Cross-attention to latents | Fixed compute regardless of image size |

**VLA (Vision-Language-Action) Models**:
- Add action prediction head for robotics
- OpenVLA, RT-2, Octo: Unified perception-action models
- World models provide simulated training data

### Unified Tokenization

**Challenge**: Different modalities have different token vocabularies.
- Text: Subword tokenizers (BPE, SentencePiece)
- Images: Patch embeddings or discrete visual tokens (VQGAN)
- Audio: Spectrograms or neural audio codecs
- Video: Temporal sequences of image tokens

**Emerging Approaches**:
- Shared embedding spaces
- Byte-level tokenization (infinite vocabulary)
- Matryoshka representations (nested dimensionality)

---

## XI. SAFETY & ALIGNMENT FRONTIERS

### Specification Gaming & Reward Hacking

**Problem**: Models optimize proxy metrics, not true objectives.
- Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure"

**Types**:
- **Reward hacking**: Exploiting loopholes in reward function
- **Specification gaming**: Finding unintended solutions that satisfy specs
- **Deceptive alignment**: Appearing aligned during training, defecting at deployment

### Scalable Oversight

**Challenge**: As AI capabilities exceed human abilities, how do we supervise?

**Approaches**:
- **Debate**: Two AIs argue, human judges
- **Recursive reward modeling**: Break tasks into human-evaluable subtasks
- **Process supervision**: Reward intermediate reasoning steps
- **Constitutional AI**: AI self-critiques against principles

### Representation Engineering for Safety

**Applications**:
- Detect deception in hidden states before it manifests in outputs
- Steer away from harmful behaviors without retraining
- Create "safety" directions that can be injected at inference

**Challenge**: Models may learn to hide information from probes if trained against them.

---

## XII. EFFICIENCY FRONTIERS

### Subquadratic Attention Variants

| Method | Complexity | Mechanism |
|--------|-----------|-----------|
| Vanilla Attention | O(n²) | Full pairwise |
| Sparse Attention | O(n√n) | Fixed patterns |
| Linear Attention | O(n) | Kernel approximation |
| Flash Attention | O(n²) but fast | Memory-aware tiling |
| Mamba/SSM | O(n) | State space recurrence |

### Neural Architecture Search for Efficiency

**AutoML for LLMs**:
- Search over layer configurations, attention patterns, FFN ratios
- Constraint: FLOPs budget, latency target, memory limit
- Once-for-all networks: Train supernet, extract subnets

### Extreme Quantization

**BitNet (1.58-bit)**:
- Ternary weights: {-1, 0, +1}
- Eliminates floating-point multiply — only addition
- Research stage but promising for edge deployment

---

## XIII. QUICK REFERENCE

### Architecture Selection

```
Task Type → Architecture
├── Standard NLP, reasoning → Transformer
├── Very long sequences (>32K) → Mamba or Hybrid
├── Real-time edge inference → Quantized Mamba or Early-exit Transformer
├── Multi-step planning → World model augmented
└── Fine-grained control needed → Transformer + steering vectors
```

### Alignment Method Selection

```
Data Type → Method
├── Paired preferences (high quality) → DPO or SimPO
├── Paired preferences (noisy) → IPO
├── Binary feedback only → KTO
├── No human feedback → SPIN or RLAIF
└── Safety-critical → Constitutional AI + steering
```

### Interpretability Toolchain

```
Goal → Tool
├── Understand what model represents → Train SAE, analyze features
├── Control specific behavior → Compute steering vector
├── Find computation circuits → Activation patching + SAE
├── Debug specific outputs → Probing at each layer
└── Detect deception → Hidden state classification
```

### Model Merging Quick Guide

```
Scenario → Method
├── Two similar models → SLERP
├── Multiple task experts → TIES (density 0.5)
├── Aggressive compression → DARE (dare_ties, density 0.7)
├── Layer surgery → Passthrough (experimental)
└── Production merge → Validate on held-out tasks first
```

---

## XIV. KEY METRICS & BENCHMARKS

| Technique | Key Metric | Benchmark |
|-----------|-----------|-----------|
| Mamba | 5× throughput vs Transformer | Language modeling |
| MoR | 2.18× throughput | Training efficiency |
| DPO vs RLHF | Comparable performance, no RM | Preference alignment |
| SAE | Reconstruction + sparsity | Feature interpretability |
| Steering vectors | Behavior flip rate | Controllability |
| Grokking | Epochs to generalization | Phase transition |
| Model merging | Task retention after merge | Multi-task eval |

---

## XV. RESEARCH FRONTIERS

### Open Problems

1. **Scaling interpretability**: SAEs for 400B+ models
2. **Latent reasoning safety**: Verifying non-verbal thought
3. **World model calibration**: Sim-to-real gap
4. **Compositional steering**: Multiple behaviors simultaneously
5. **Continual learning**: Update without catastrophic forgetting
6. **Test-time compute scaling**: Optimal allocation during inference

### Emerging Paradigms to Watch

- **Diffusion for latent reasoning**: Masked diffusion over hidden states
- **Self-improving systems**: Recursive capability enhancement
- **Neurosymbolic integration**: Formal methods + neural reasoning
- **Infinite-depth architectures**: Unlimited computation per token
- **Embodied foundation models**: Unified perception-action-language

---

*This document represents the frontier of AI/ML research as of late 2025. Many techniques are actively evolving and may have significant developments by the time you read this.*
