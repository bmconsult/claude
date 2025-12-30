# Nexus v2 Roadmap: Research-Driven Enhancements

Based on comprehensive research across 13 areas of cutting-edge LLM techniques.

---

## Executive Summary

Nexus v1 has proven the hybrid Attention+SSM architecture. v2 focuses on:
1. **Inference Speed**: 2-5x via speculative decoding + quantization
2. **Memory Efficiency**: 4-8x via KV cache compression
3. **Scaling**: MoE for 10x+ parameters at same compute
4. **Deployment**: Production-ready serving infrastructure

---

## Phase 1: Immediate Wins (Low Effort, High Impact)

### 1.1 Quantization (AWQ/GPTQ)
**Research Insight**: AWQ achieves <1% quality loss with 4-bit weights
**Integration**: Post-training quantization of trained checkpoints

```rust
// Add to nexus/src/quantization.rs
pub struct AWQConfig {
    bits: u8,           // 4-bit default
    group_size: usize,  // 128 typical
    calibration_samples: usize,
}
```

**Implementation**:
- Add `QuantizedLinear` layer type
- Calibration pass with ~128 samples
- Pack int4 weights with SIMD unpacking
- **Expected Result**: 4x memory reduction, ~2x faster on CPU

### 1.2 KV Cache Optimization: MLA (Multi-head Latent Attention)
**Research Insight (Dec 2024)**: DeepSeek V2/V3 MLA achieves **93% KV cache reduction** and **6x generation throughput**
**Key Innovation**: Compress KV into latent space, decompress on-demand

```rust
// New: src/attention/mla.rs
pub struct MultiHeadLatentAttention {
    d_model: usize,
    num_heads: usize,
    q_latent_dim: usize,      // Query compression dimension
    kv_latent_dim: usize,     // KV compression dimension (e.g., 512 vs 4096)

    // Low-rank projections
    down_proj_kv: Linear,     // d_model -> kv_latent_dim
    up_proj_k: Linear,        // kv_latent_dim -> d_model
    up_proj_v: Linear,        // kv_latent_dim -> d_model
}

impl MultiHeadLatentAttention {
    pub fn cache_compressed(&self, hidden: &Tensor) -> Tensor {
        // Store only latent vector (8x smaller than full KV)
        self.down_proj_kv.forward(hidden)
    }

    pub fn decompress_for_attention(&self, latent: &Tensor) -> (Tensor, Tensor) {
        (self.up_proj_k.forward(latent), self.up_proj_v.forward(latent))
    }
}
```

**Implementation**:
- Replace GQA with MLA in attention layer
- Cache compressed latent (512 dims vs 4096)
- Decompress K,V on-the-fly during attention
- **Expected Result**: 93% cache reduction, 6x throughput

**Alternative**: PyramidKV for hierarchical compression if MLA is too complex

**Sources**: [DeepSeek V2 MLA](https://huggingface.co/bird-of-paradise/deepseek-mla), [Sebastian Raschka MLA Guide](https://sebastianraschka.com/llms-from-scratch/ch04/05_mla/)

### 1.3 Inference Server Improvements
**Research Insight**: vLLM-style PagedAttention + continuous batching
**Already Have**: `nexus-serve` binary exists

**Add**:
- Continuous batching for concurrent requests
- PagedAttention-style memory management
- OpenAI-compatible API (already started)
- **Expected Result**: 3-5x throughput improvement

---

## Phase 2: Speculative Decoding (Medium Effort, High Impact)

### 2.1 EAGLE-style Speculative Decoding
**Research Insight**: EAGLE achieves 2.8-3.8x speedup, lossless
**Key Insight**: Draft model reuses target's feature vectors, not independent

```rust
// New: src/speculative.rs
pub struct EAGLEDecoder {
    draft_head: DraftHead,          // Lightweight, shares embeddings
    tree_attention_mask: Tensor,    // Tree-structured speculation
    speculation_depth: usize,       // 4-6 typical
}

impl EAGLEDecoder {
    pub fn speculate(&self, context: &[u32], target_features: &Tensor)
        -> Vec<SpeculativeSequence> {
        // Generate tree of candidates using target's hidden states
    }

    pub fn verify(&self, target: &Model, candidates: &[Vec<u32>])
        -> Vec<u32> {
        // Single forward pass to verify multiple candidates
    }
}
```

**Implementation Steps**:
1. Add lightweight draft head (~10% of model size)
2. Implement tree attention mask for parallel verification
3. Training: draft head only (target frozen)
4. **Expected Result**: 2-3x generation speedup

### 2.2 Medusa Heads (Alternative)
**Research Insight**: Multiple heads predict future tokens in parallel
**Advantage**: No separate draft model, simpler training

```rust
pub struct MedusaHeads {
    heads: Vec<Linear>,  // One per future position
    num_predictions: usize,  // 3-5 typical
}
```

**Trade-off**: Simpler but ~2x speedup vs EAGLE's 2.8-3.8x

---

## Phase 3: Scaling with MoE (High Effort, Transformative)

### 3.1 DeepSeek-style MoE Integration
**Research Insight (Dec 2024)**: DeepSeek V3 achieves 671B total params, 37B active per token
**Training Cost**: Only $5.576M (2.788M H800 GPU hours) - remarkably efficient

**Key DeepSeek Innovations**:
1. **Auxiliary-Loss-Free Load Balancing**: No aux loss needed! Performance preserved while balanced
2. **Multi-Token Prediction (MTP)**: Predicts multiple future tokens, 1.8x inference speedup via speculative decoding
3. **FP8 Mixed-Precision Training**: First validated at extreme scale, enables efficient training

```rust
// New: src/moe.rs
pub struct MoELayer {
    shared_experts: Vec<FFN>,      // Always active (1-2)
    routed_experts: Vec<FFN>,      // Conditionally active (64-256)
    router: AuxFreRouter,          // Aux-loss-free routing!
    expert_capacity: usize,        // Load balancing
}

// DeepSeek's aux-loss-free router (no performance degradation from balancing)
pub struct AuxFreRouter {
    top_k: usize,                  // 6-8 per token
    bias_update_rate: f32,         // Dynamic bias for load balancing
    expert_biases: Vec<f32>,       // Per-expert routing bias
}

impl AuxFreRouter {
    pub fn route(&mut self, x: &Tensor) -> (Vec<usize>, Vec<f32>) {
        // Route with dynamic bias - no aux loss needed!
        // Biases updated based on expert load during training
    }
}
```

**Note on MTP**: Multi-Token Prediction improves training quality but research shows it only helps models >1B parameters. For our 6.74M model, focus on other optimizations.

**Sources**: [DeepSeek V3 Paper](https://arxiv.org/abs/2412.19437), [Sebastian Raschka DeepSeek Guide](https://magazine.sebastianraschka.com/p/technical-deepseek)

**Architecture for Nexus v2-MoE**:
- Keep hybrid Attention+SSM backbone
- Replace FFN layers with MoE
- 64 experts, 6 active per token
- Shared 1-2 experts for common patterns
- **Expected Result**: 10x parameters at same inference cost

### 3.2 Expert Parallelism Infrastructure
**For multi-GPU deployment**:
- Expert-parallel distribution across GPUs
- All-to-all communication for expert routing
- Load balancing to prevent hotspots

---

## Phase 4: Mamba-2 SSM Upgrade (Medium Effort, Core Improvement)

### 4.1 State Space Duality (SSD)
**Research Insight (ICML 2024)**: Mamba-2 achieves 2-8x faster training via matrix form + **16x larger state size**
**Key Paper**: "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality" (Dao & Gu)

**Why Mamba-2 is Better**:
1. **Tensor Core Utilization**: A100 has 312 TFLOPS BF16 matmul vs 19 TFLOPS FP32 (16x faster!)
2. **Larger State Size**: N=256 vs N=16 in Mamba-1 (16x more expressive)
3. **System Optimizations**: Tensor parallelism, sequence parallelism from Transformer land

```rust
// Upgrade src/ssm.rs
pub struct Mamba2Block {
    // SSD-form for training (matrix multiply primitive)
    A_matrix: Tensor,      // Structured state matrix
    B_proj: Linear,        // Input projection
    C_proj: Linear,        // Output projection

    // Head structure (new in Mamba-2)
    num_heads: usize,      // 8-16 typical
    head_dim: usize,       // d_model / num_heads
    state_dim: usize,      // N=64-256 (was 16 in Mamba-1!)

    // SSD algorithm uses 4-step block decomposition
    block_size: usize,     // For chunked computation
}

impl Mamba2Block {
    // Training: Use matrix multiply form (parallel)
    pub fn forward_training(&self, x: &Tensor) -> Tensor {
        // Block decomposition of token-mixing matrix
        // Gets advantages of both linear-recurrent AND quadratic-attention forms
    }

    // Inference: Use recurrent form (sequential, O(1) per step)
    pub fn forward_inference(&self, x: &Tensor, state: &mut Tensor) -> Tensor {
        // Standard recurrent SSM scan
    }
}
```

**Key Changes**:
- Multi-head SSM (like attention heads)
- Matrix multiply form for training (parallelizable via tensor cores)
- Recurrent form for inference (sequential, efficient)
- 16x larger state dimension (N=256)
- **Expected Result**: 2-8x faster training, same inference speed, better quality

**Sources**: [Mamba-2 Paper](https://arxiv.org/abs/2405.21060), [Tri Dao Blog](https://tridao.me/blog/2024/mamba2-part1-model/)

### 4.2 Jamba-1.5 Architecture Insights
**Research Insight**: AI21 Jamba 1.5 scales to 398B total/94B active with 1:7 Attention:Mamba ratio
**Current Nexus**: 1:5 ratio - already aligned with SOTA!

**Key Jamba Metrics**:
- **256K context** with only **4GB attention cache** (vs 32GB Mixtral, 128GB LLaMA-70B)
- 72 layers total, interleaved attention and Mamba
- MoE with 16 experts per layer, top-2 selected

**Refinements for Nexus**:
- Maintain 1:5 ratio (close to Jamba's 1:7)
- Interleaved arrangement (attention at strategic positions for reasoning)
- Consider MoE in Mamba layers for capacity without latency
- **Expected Result**: Better long-context with minimal memory overhead

**Sources**: [AI21 Jamba Blog](https://www.ai21.com/blog/announcing-jamba/), [Jamba Paper](https://arxiv.org/abs/2403.19887)

---

## Phase 4.5: Small Model Optimizations (Critical for 6.74M Params)

**Context**: Many cutting-edge techniques (MTP, large MoE) require >1B params. This section covers techniques that work at our scale.

### 4.5.1 Block-wise Weight Sharing (MobileLLM)
**Research Insight**: Sharing weights across transformer blocks reduces params while maintaining quality
**Applicability**: Works at any scale

```rust
// Modify layer construction
pub struct SharedBlockConfig {
    share_attention_weights: bool,   // Share QKV across blocks
    share_ffn_weights: bool,         // Share FFN across blocks
    share_interval: usize,           // Share every N blocks
}

// Example: Share weights between layer 0-2 and 3-5
// Reduces effective parameters by ~40% with <5% quality loss
```

### 4.5.2 Linear Attention Variants
**Research Insight**: Reformulate attention as linear dot-product, faster inference
**Trade-off**: May lose some expressiveness, good for efficiency-critical deployments

### 4.5.3 Knowledge Distillation from Larger Models
**Research Insight**: Distill knowledge from 8B+ models into our 6.74M model
**Implementation**: Train with KL divergence against larger model's logits

```rust
pub struct DistillationConfig {
    teacher_logits_path: String,  // Pre-computed teacher outputs
    temperature: f32,              // Softmax temperature (2-4)
    alpha: f32,                    // Balance: alpha*distill + (1-alpha)*CE
}
```

### 4.5.4 Depth-Width Tradeoffs (NAS-informed)
**Research Insight**: MobileLLM found deeper-narrower better than shallow-wide for small models
**Current Nexus**: 6 layers, d_model=256
**Consider**: 8-10 layers, d_model=192-224 (same param count, potentially better)

**Sources**: [MobileLLM Paper](https://arxiv.org/abs/2402.14905), [Small LM Survey](https://arxiv.org/abs/2411.03350)

### 4.5.5 Byte Latent Transformer (BLT) - Dynamic Patching
**Research Insight (Dec 2024)**: Meta's BLT achieves **tokenizer parity at 8B scale** + **50% FLOP efficiency gains**
**HIGHLY RELEVANT**: Nexus already uses byte-level tokenization (vocab_size=256)!

**Key Innovation**: Dynamic patching based on next-byte entropy:
- Easy bytes → compress into latent patches (shorter sequence)
- Complex bytes → keep as-is for detailed modeling
- Treats all languages equally (no tokenizer bias)

```rust
// Potential: src/blt.rs
pub struct ByteLatentEncoder {
    entropy_model: SmallTransformer,  // Predicts byte-level entropy
    local_encoder: Conv1D,            // Encode patches to latents
    patch_threshold: f32,             // Entropy threshold for patch boundaries
}

impl ByteLatentEncoder {
    pub fn segment_to_patches(&self, bytes: &[u8]) -> Vec<Patch> {
        // Use entropy model to predict complexity
        // Segment into variable-length patches
        // Compress each patch into a latent vector
    }
}
```

**Why This Fits Nexus**:
1. We already operate at byte-level (no tokenizer needed)
2. SSM layers handle variable-length sequences naturally
3. Could reduce effective sequence length by 2-4x on predictable text
4. More robust to typos, novel words, formatting

**Implementation Path**:
1. Train small entropy model on byte sequences
2. Add patching layer before main transformer
3. Add un-patching layer after decoder
4. **Expected Result**: 30-50% efficiency gains, better robustness

**Sources**: [BLT Paper](https://arxiv.org/abs/2412.09871), [Meta GitHub](https://github.com/facebookresearch/blt), [HuggingFace BLT](https://huggingface.co/docs/transformers/model_doc/blt)

---

## Phase 5: Training Enhancements (PEFT + Efficiency)

### 5.1 LoRA Integration
**Research Insight**: LoRA matches full finetuning at 0.1% parameters
**Use Case**: Efficient adaptation for downstream tasks

```rust
// New: src/peft/lora.rs
pub struct LoRAAdapter {
    rank: usize,           // 8-64 typical
    alpha: f32,            // Scaling factor
    A: Tensor,             // Low-rank matrix A
    B: Tensor,             // Low-rank matrix B
    target_modules: Vec<String>,  // Which layers to adapt
}
```

**Implementation**:
- Wrap existing Linear layers with LoRA
- Merge for inference (zero overhead)
- Support QLoRA (4-bit base + LoRA)
- **Expected Result**: 10-100x faster finetuning

### 5.2 GaLore Memory Optimization
**Research Insight**: 8x memory reduction during training via gradient low-rank projection
**Use Case**: Training larger models on same hardware

```rust
pub struct GaLoreOptimizer {
    rank: usize,           // Gradient projection rank
    update_freq: usize,    // How often to update projector
    scale: f32,
}
```

---

## Phase 6: Advanced Capabilities

### 6.1 Titans-style Test-Time Memory (Enhancement)
**Already Have**: `src/memory.rs` implements surprise-based memory
**Research Insight**: Can be enhanced with learned gates

**Enhancements**:
- Neural gate for memory update decisions
- Differentiable memory addressing
- Integration with attention for memory retrieval
- **Expected Result**: Better long-context reasoning

### 6.2 Long-Context Extensions
**Research Insight**: YaRN/NTK-aware RoPE interpolation for 100K+ context

```rust
// Enhance src/rope.rs
pub struct YaRNConfig {
    base_context: usize,   // Original training context
    target_context: usize, // Extended context
    alpha: f32,            // NTK-aware scaling
    beta: f32,             // YaRN attention factor
}
```

**Implementation**:
- NTK-aware frequency scaling
- YaRN attention temperature adjustment
- **Expected Result**: 8-16x context extension

### 6.3 Multimodal Extension (Future)
**Research Insight**: Qwen3-VL uses native dynamic resolution
**Architecture**:
- Add ViT vision encoder
- Cross-attention or early fusion
- Keep text backbone as-is

---

## Implementation Priority Matrix

| Feature | Effort | Impact | Priority | Notes |
|---------|--------|--------|----------|-------|
| **MLA Attention** | Medium | Very High | 🔥 P0 | 93% cache reduction, 6x throughput |
| AWQ Quantization | Low | High | 🔥 P0 | 4-bit weights, 4x memory reduction |
| Continuous Batching | Medium | High | 🔥 P0 | vLLM-style serving |
| Weight Sharing | Low | Medium | 🔥 P0 | Small model specific, ~40% param reduction |
| EAGLE Speculative | Medium | High | ⭐ P1 | 2.8-3.8x inference speedup |
| Mamba-2 SSD | Medium | High | ⭐ P1 | 16x state size, 2-8x faster training |
| LoRA Finetuning | Medium | Medium | ⭐ P1 | 10-100x faster finetuning |
| Deeper Architecture | Medium | Medium | ⭐ P1 | 8-10 layers vs 6, NAS-informed |
| MoE (Aux-Free) | High | Transformative | 🎯 P2 | DeepSeek-style, no aux loss |
| Long-Context (YaRN) | Medium | Medium | 🎯 P2 | 8-16x context extension |
| Knowledge Distillation | Medium | High | 🎯 P2 | Learn from 8B+ teachers |
| **BLT Dynamic Patching** | Medium | High | ⭐ P1 | 30-50% efficiency, fits byte-level arch |
| Multimodal | High | Transformative | 🔮 P3 | Future vision support |

**Updated Dec 2024**: MLA replaces PyramidKV as primary cache optimization. DeepSeek aux-loss-free routing added to MoE. Small model optimizations section added for 6.74M scale.

---

## Recommended v2 Feature Set

### v2.0 Release (Near-term) - Focus: Inference Efficiency
1. **MLA Attention** - Replace GQA with Multi-head Latent Attention (93% cache reduction)
2. AWQ 4-bit quantization
3. Continuous batching server
4. Block-wise weight sharing (for our small model scale)

### v2.1 Release (Medium-term) - Focus: Training & Scaling
1. **Mamba-2 SSD** upgrade (16x state, 2-8x training speedup)
2. EAGLE speculative decoding (2.8-3.8x inference)
3. Deeper architecture (8-10 layers, NAS-informed)
4. LoRA adapter support for efficient finetuning

### v2.2 Release (Future) - Focus: Capability Expansion
1. MoE architecture (DeepSeek-style aux-loss-free)
2. Knowledge distillation from larger models
3. YaRN context extension (8-16x context)
4. Multi-GPU serving

### v3.0 (Vision) - Focus: Reasoning & Multimodal
1. **Test-Time Compute Scaling** (o1-style reasoning)
   - Chain-of-Thought via RL training
   - Key insight: Smaller model + more inference compute > 14x larger model
   - Sequential scaling (longer CoT) + parallel scaling (best-of-N sampling)
2. Multimodal support (ViT encoder)
3. Forest-of-Thought for complex logical problems

---

## Files to Create/Modify

```
nexus/src/
├── quantization/
│   ├── mod.rs
│   ├── awq.rs          # AWQ quantization
│   └── packing.rs      # Int4 packing/unpacking
├── speculative/
│   ├── mod.rs
│   ├── eagle.rs        # EAGLE decoder
│   └── medusa.rs       # Medusa heads
├── moe/
│   ├── mod.rs
│   ├── router.rs       # Top-k routing
│   └── experts.rs      # Expert FFN layers
├── peft/
│   ├── mod.rs
│   ├── lora.rs         # LoRA adapters
│   └── qlora.rs        # Quantized LoRA
├── cache/
│   ├── mod.rs
│   ├── pyramid.rs      # PyramidKV
│   └── paged.rs        # PagedAttention
└── context/
    ├── mod.rs
    └── yarn.rs         # YaRN RoPE scaling
```

---

## Metrics to Track

| Metric | v1 Baseline | v2 Target |
|--------|-------------|-----------|
| Tokens/sec (inference) | 59 | 200+ |
| Memory (7B model) | 28GB | 7GB (4-bit) |
| Context length | 128 | 4K+ |
| Finetuning memory | 100% | 10% (LoRA) |
| Training throughput | 1x | 2-4x (Mamba-2) |

---

## Research Sources (Dec 2024)

### Architecture
- [Mamba-2 Paper (ICML 2024)](https://arxiv.org/abs/2405.21060) - Structured State Space Duality
- [Jamba Paper](https://arxiv.org/abs/2403.19887) - Hybrid Transformer-Mamba architecture
- [IBM Granite 4.0](https://venturebeat.com/ai/western-qwen-ibm-wows-with-granite-4-llm-launch-and-hybrid-mamba-transformer) - Production hybrid models

### Efficiency
- [DeepSeek V3 Technical Report](https://arxiv.org/abs/2412.19437) - MLA, aux-loss-free MoE, FP8 training
- [MLA Explanation (HuggingFace)](https://huggingface.co/blog/NormalUhr/mla-explanation) - KV cache compression
- [Sebastian Raschka MLA Guide](https://sebastianraschka.com/llms-from-scratch/ch04/05_mla/)

### Small Models & Byte-Level
- [MobileLLM Paper](https://arxiv.org/abs/2402.14905) - Weight sharing, depth-width tradeoffs
- [Small Language Model Survey](https://arxiv.org/abs/2411.03350) - Comprehensive techniques overview
- [Byte Latent Transformer (Meta, Dec 2024)](https://arxiv.org/abs/2412.09871) - Dynamic patching, 50% FLOP gains

### Inference
- [Multi-Token Prediction (Meta)](https://arxiv.org/abs/2404.19737) - 3x faster inference (>1B params)
- [EAGLE Speculative Decoding](https://arxiv.org/abs/2401.15077) - 2.8-3.8x lossless speedup

---

*This roadmap synthesizes research findings into actionable development priorities.*
*Last updated: December 30, 2024*
