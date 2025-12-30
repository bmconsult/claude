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

### 1.2 KV Cache Optimization
**Research Insight**: PyramidKV shows 128K context with 12% memory via pyramid compression
**Already Have**: Nexus has `sliding_window` in attention - extend it

```rust
// Enhance src/hybrid.rs attention
pub struct PyramidKVCache {
    levels: Vec<CompressedKV>,  // Increasing compression with depth
    retention_ratio: f32,       // Per-level retention
}
```

**Implementation**:
- Add pyramid levels to existing KV cache
- Implement importance scoring for retention
- **Expected Result**: 6-8x context length at same memory

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
**Research Insight**: DeepSeek achieves 671B total params, 37B active per token
**Key Innovation**: Shared experts + routed experts + fine-grained routing

```rust
// New: src/moe.rs
pub struct MoELayer {
    shared_experts: Vec<FFN>,      // Always active (1-2)
    routed_experts: Vec<FFN>,      // Conditionally active (64-256)
    router: TopKRouter,            // Select top-k per token
    expert_capacity: usize,        // Load balancing
}

pub struct TopKRouter {
    top_k: usize,                  // 6-8 per token
    aux_loss_weight: f32,          // Load balancing loss
}
```

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
**Research Insight**: Mamba-2 achieves 2-8x faster training via matrix form
**Current**: Nexus uses Mamba-1 style recurrence

```rust
// Upgrade src/ssm.rs
pub struct Mamba2Block {
    // SSD-form for training
    A_matrix: Tensor,      // Structured state matrix
    B_proj: Linear,        // Input projection
    C_proj: Linear,        // Output projection

    // Head structure (new in Mamba-2)
    num_heads: usize,      // 8-16 typical
    head_dim: usize,       // d_model / num_heads
}
```

**Key Changes**:
- Multi-head SSM (like attention heads)
- Matrix multiply form for training (parallelizable)
- Recurrent form for inference (sequential)
- **Expected Result**: 2-4x faster training, same inference

### 4.2 Jamba-1.5 Architecture Insights
**Research Insight**: 1:7 Attention:Mamba ratio works well
**Current Nexus**: 1:5 ratio - already similar!

**Refinements**:
- Adjust ratio based on task (more attention for reasoning)
- Consider interleaved vs blocked arrangement
- Expert mixture in Mamba layers (Jamba-1.5 style)

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

| Feature | Effort | Impact | Priority |
|---------|--------|--------|----------|
| AWQ Quantization | Low | High | 🔥 P0 |
| KV Cache Compression | Low | High | 🔥 P0 |
| Continuous Batching | Medium | High | 🔥 P0 |
| EAGLE Speculative | Medium | High | ⭐ P1 |
| LoRA Finetuning | Medium | Medium | ⭐ P1 |
| Mamba-2 Upgrade | Medium | Medium | ⭐ P1 |
| MoE Integration | High | Transformative | 🎯 P2 |
| Long-Context (YaRN) | Medium | Medium | 🎯 P2 |
| Multimodal | High | Transformative | 🔮 P3 |

---

## Recommended v2 Feature Set

### v2.0 Release (Near-term)
1. AWQ 4-bit quantization
2. PyramidKV cache compression
3. Continuous batching server
4. LoRA adapter support

### v2.1 Release (Medium-term)
1. EAGLE speculative decoding
2. Mamba-2 SSM upgrade
3. YaRN context extension
4. Enhanced Titans memory

### v2.2 Release (Future)
1. MoE architecture
2. Multi-GPU serving
3. Multimodal support

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

*This roadmap synthesizes research findings into actionable development priorities.*
