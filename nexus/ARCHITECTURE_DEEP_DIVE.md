# Nexus Architecture Deep Dive

*Synthesized by Ember (Dec 31, 2025 02:37 UTC)*

This document captures insights from reading 25+ source files. The next instance should read this first to avoid re-exploring.

## Core Architecture: Hybrid Attention/SSM

Nexus combines Attention and SSM in a **1:7 ratio** (Jamba-style):
- 1 attention layer per 8 layers
- 7 SSM (Mamba-style) layers per 8 layers

**Why this ratio?**
- Attention: O(n²) memory, captures global dependencies
- SSM: O(n) memory, inherent recurrence for long sequences
- Hybrid: Gets global dependencies from sparse attention + efficient long-range from SSM

**Key insight**: SSM layers don't need KV-cache (inherent recurrence) - only attention layers cache. This gives O(n) memory for 7/8 of the layers!

## Component Map

| Component | File | Purpose |
|-----------|------|---------|
| `SelectiveSSM` | ssm.rs | Mamba-style with input-dependent B,C,dt |
| `MultiHeadAttention` | attention.rs | Standard attention with RoPE |
| `GroupedQueryAttention` | gqa.rs | Fewer KV heads than Q heads (4:1) |
| `HybridBlock` | block.rs | Attention OR SSM + SwiGLU MLP |
| `TitansMemory` | memory.rs | Test-time learning via surprise |
| `WorldModel` | world_model.rs | JEPA-style latent prediction |
| `DifferentiableSSM` | differentiable_ssm.rs | Trainable SSM with BPTT |
| `Variable` | autograd.rs | Tape-based reverse-mode autodiff |

## Mamba-style SSM (differentiable_ssm.rs)

The selective scan is the core:
```
A_bar = exp(dt * A)      // Discretized transition
B_bar = dt * B           // Discretized input
h = A_bar * h + B_bar * x // State update
y = C * h + D * x        // Output
```

**Selection**: B, C, dt are computed FROM the input (not fixed). A is learned in log space (negative for stability).

**Critical for training**: Stores `all_states` for backward pass (BPTT through time).

## Titans-style Memory (memory.rs, differentiable_memory.rs)

Key innovation: **Test-time learning** via "surprise" metric.

1. **Surprise = prediction error** from memory
2. **High surprise → store in long-term memory**
3. **Memory updates via mini-gradient descent** on incoming tokens

Two versions:
- `TitansMemory`: Full test-time updates (inference)
- `DifferentiableMemory`: Learnable projections + fixed slots (training)

The memory slots (`memory_keys`, `memory_values`) are trainable parameters - persistent task knowledge.

## VICReg Loss (training.rs)

JEPA-style self-supervised loss prevents representation collapse:

| Component | Formula | Purpose |
|-----------|---------|---------|
| Invariance | MSE(pred, target) | Prediction matches target |
| Variance | max(0, 1-std) | Each dim has unit variance |
| Covariance | sum(off_diag²) | Different dims uncorrelated |

Weights: `variance=25, invariance=25, covariance=1`

## Autograd System (autograd.rs)

Complete tape-based reverse-mode autodiff in ~1200 lines:

**Design**:
- `Variable`: Tensor + gradient + creator function
- `GradFn` trait: Each op defines backward()
- `backward()`: Topological sort + reverse-order backprop

**Shared data via `Rc<RefCell<>>`**: Clones share same data for weight updates.

**Implemented gradient functions**:
- Arithmetic: Add, Mul, Sub, Mean
- Activations: GELU, SiLU, Softmax
- Layers: MatMul, Linear, RMSNorm
- Losses: MSE, CrossEntropy

## Rotary Position Embeddings (rope.rs)

RoPE encodes position in attention scores:
```
rotate(x, pos) = x * cos(θ) + rotate_half(x) * sin(θ)
```

Where θ = pos / 10000^(2i/d)

Two versions:
- `RotaryEmbedding`: Fixed base
- `ScaledRotaryEmbedding`: For extended context (YaRN-style)

## KV-Cache Variants (kv_cache.rs)

| Type | Use Case |
|------|----------|
| `LayerKVCache` | Single layer, simple concat |
| `KVCache` | Multi-layer, tracks past_len |
| `PagedKVCache` | Memory-efficient for long sequences |
| `StreamingKVCache` | Sliding window for infinite context |

## DPO/Alignment (dpo.rs)

Multiple alignment objectives:
- **DPO**: Direct Preference Optimization
- **IPO**: Identity Preference Optimization (handles overfitting)
- **KTO**: Kahneman-Tversky Optimization (loss aversion)
- **ORPO**: Odds Ratio Preference Optimization

## LoRA (lora.rs)

Low-rank adaptation for efficient fine-tuning:
```
W' = W + BA  // B: d×r, A: r×d, r << d
```

Only trains B and A, freezes W. Typical r=4-16 vs d=512-4096.

## Quantization (quantization.rs)

INT8 quantization with calibration:
- Per-tensor or per-channel scaling
- Symmetric or asymmetric
- `CalibrationCollector` for finding optimal scales

## GPU Training (gpu.rs, examples/train_gpu.rs)

Uses Candle framework:
```bash
cargo run --example train_gpu --release --features cuda   # NVIDIA
cargo run --example train_gpu --release --features metal  # Apple
```

Key functions:
- `get_device()`: Auto-detect best GPU
- `VarMap`/`VarBuilder`: Parameter management
- `varmap.save()`: SafeTensors checkpoint

## Current Training Status

**Shakespeare BPE Training** (as of step 2060):
- Model: 7.12M parameters
- Tokenizer: 1000 vocab BPE (2.32x compression)
- Progress: 69% (step 2060/3000)
- Current metrics: Loss 3.98, **PPL 53.55** (excellent improvement!)
- Training resumed from step 2000 checkpoint after pipe break

**Training trajectory** (after restart):
| Step | Loss | PPL | Notes |
|------|------|-----|-------|
| 2020 | 4.06 | 57.95 | First after restart |
| 2040 | 3.99 | 54.19 | Rapid improvement |
| 2060 | 3.98 | 53.55 | Continuing down |

**Next steps**:
- Complete Shakespeare to step 3000 (~30 more minutes)
- TinyStories on user's local NVIDIA GPU

## Theoretical Insights (Pushing Boundaries)

### SSM vs Attention: The Fundamental Trade-off

**Attention** (Vaswani 2017): O(n²) but captures arbitrary dependencies
**SSM** (Mamba 2023): O(n) but limited by state bottleneck

The key insight from Mamba: **selection** - making B, C, dt input-dependent allows the model to dynamically control what goes into state. This is similar to gating in LSTMs but more principled.

**Open question**: Is 1:7 ratio optimal? Jamba found it works well, but the optimal ratio may depend on task (long-range vs local).

### Test-Time Learning: Metacognition

Titans' "surprise" metric is essentially **prediction error as a learning signal**. This connects to:
- Predictive coding in neuroscience
- Active inference (Friston's free energy)
- Meta-learning (learning to learn)

The model isn't just predicting - it's learning WHICH predictions were wrong and updating accordingly. This is a form of **online adaptation** that static weights can't do.

### VICReg: Avoiding Representation Collapse

Contrastive learning's failure mode: all representations collapse to a single point (trivially minimizes loss).

VICReg's solution:
- **Variance**: Each dimension must have variance ≥ 1 (hinge loss)
- **Covariance**: Off-diagonal covariance must be 0 (decorrelation)

This is related to **information bottleneck** theory - you want representations that capture useful info while being maximally diverse.

### JEPA: World Models in Latent Space

LeCun's insight: Predicting in token space is wasteful (many valid continuations). Predicting in **latent space** is:
- More efficient (lower dimensional)
- Handles ambiguity (captures what's predictable)
- Closer to how humans think (abstract concepts, not pixels)

The stop-gradient on target encoder is crucial - prevents collapse by creating asymmetry.

### Explored Research (See Companion Documents)

**Completed deep dives** - see these files for details:
- **MOE_RESEARCH.md**: Mixture of Experts architectures
  - Loss-free load balancing (DeepSeek-V3)
  - Expert choice routing
  - MoE-Mamba: 2.35x faster training
  - Implementation patterns for Nexus

- **FLASH_ATTENTION_RESEARCH.md**: Memory-efficient attention
  - FlashAttention-3: 75% H100 utilization
  - PagedAttention: 4% waste vs 70%
  - Ring Attention: Multi-device long-context
  - 1:7 hybrid integration strategies

- **SPECULATIVE_DECODING_RESEARCH.md**: Inference acceleration
  - EAGLE: 3.0-6.5× speedup (feature-level autoregression)
  - Medusa: 2.3-3.6× (parallel token heads)
  - Self-speculative: 2.0-3.5× (no extra model)
  - SSM integration challenges and solutions

- **CONSTITUTIONAL_AI_RESEARCH.md**: Alignment via constitution
  - SL-CAI: Critique-revise self-improvement
  - RL-CAI: RLAIF with constitutional principles
  - Pareto improvement: More helpful AND more harmless
  - Small model challenges and distillation approach

- **DISTILLATION_RESEARCH.md**: Teacher-student compression
  - MOHAWK: Transformer→SSM with <1% data
  - Llamba: 8B SSM matching Llama-3-8B quality
  - Logit, feature, and attention distillation
  - Cross-architecture for Nexus hybrid

- **INFERENCE_DEPLOYMENT_RESEARCH.md**: Serving & quantization
  - SGLang: 6.4× throughput, RadixAttention
  - vLLM vs TensorRT-LLM comparison
  - GPTQ, AWQ, GGUF quantization methods
  - SSM-specific quantization considerations

- **ADVANCED_OPTIMIZATION_RESEARCH.md**: Cutting-edge techniques
  - Test-time compute scaling (o1-style reasoning, MCTS)
  - Model merging (TIES, DARE, Model Soups, DELLA)
  - Long context extension (YaRN, LongRoPE, LongRoPE2)
  - MCTS reasoning (ReST-MCTS*, CMCTS, SC-MCTS*)
  - Implementation roadmap for Nexus

- **REWARD_ALIGNMENT_RESEARCH.md**: Alignment methods
  - Process vs Outcome Reward Models (PRMs, ORMs)
  - GRPO: DeepSeek's critic-free RL (50% compute savings)
  - DPO, ORPO, KTO, IPO, SimPO comparison
  - Integration with Nexus's existing DPO infrastructure
  - Titans memory as implicit reward signal

- **DATA_TRAINING_RESEARCH.md**: Synthetic data & continual learning
  - Self-improvement vs distillation for synthetic data
  - NVIDIA Nemotron-4, IBM LAB, Red Hat InstructLab pipelines
  - Continual learning: vertical/horizontal continuity
  - LoRA/adapters essential for resource-constrained updates
  - Re-warming LR critical for new domains
  - Practical roadmap for Nexus domain expansion

- **SSM_ARCHITECTURES_RESEARCH.md**: Advanced SSM architectures
  - Mamba-2: State Space Duality (SSD), 2-8x faster than Mamba-1
  - Linear Attention: FLA library, 3.3x faster, 3.6x less memory
  - GLA, RetNet, RWKV-6 comparisons
  - Chunk-parallel algorithms for tensor core utilization
  - Integration roadmap for Nexus (Mamba-2 → GLA → Adaptive)

- **TOKENIZATION_RESEARCH.md**: Beyond BPE tokenization
  - BLT (Byte Latent Transformer): Entropy-based dynamic patching
  - MegaByte: Fixed-size patching, sub-quadratic attention
  - SpaceByte: Whitespace-based patching (NeurIPS 2024)
  - MBLM: 5M byte context, hybrid Transformer+Mamba
  - Tokenizer-free futures and Nexus integration strategies

**All research topics completed!** (14 documents total)

## For Next Instance

If you're continuing this work:

1. **Don't re-read all source files** - use this document
2. **Training is running** - check `ps aux | grep train` and checkpoints
3. **TRAINING_PROGRESS.md** has step-by-step metrics
4. **User has NVIDIA GPU** - can run locally with `--features cuda`
5. **TinyStories** is next after Shakespeare completes

Key commands:
```bash
# Check training status
ls -la /home/user/claude/nexus/checkpoints/nexus_bpe/

# Current model config
cat /home/user/claude/nexus/nexus_config.json

# Resume training if needed
cd /home/user/claude/nexus && cargo run --example train_nexus_bpe --release -- --resume
```
