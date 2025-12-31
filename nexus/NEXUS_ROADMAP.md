# Nexus Development Roadmap

*Synthesized from 14 research documents by Ember (Dec 31, 2025)*

## Executive Summary

This roadmap synthesizes insights from comprehensive research into a prioritized development plan for Nexus, the hybrid Attention/SSM architecture with 7.12M parameters.

## Current Status

**Shakespeare Training (Step 2700/3000)**:
- 17 consecutive NEW BEST validation losses
- Val loss: 5.15, PPL: 172
- Sample: "What light" - recognizable Shakespeare
- BPE 1000-vocab tokenizer (2.32x compression)

**Architecture**:
- 1:7 attention/SSM ratio (Jamba-style)
- 6 layers (1 attention, 5 SSM)
- GQA (8 Q heads, 2 KV heads)
- RoPE position encoding
- 7.12M parameters

## Phase 1: Complete Shakespeare & Prepare TinyStories (Current)

### Immediate Tasks
1. **Complete Shakespeare training** - Step 3000 (~15 min remaining)
2. **Expand BPE vocabulary** - 1000 → 8000 tokens for TinyStories
3. **Validate model checkpoint** - Run inference tests on best.bin
4. **Document training insights** - Final TRAINING_PROGRESS.md update

### TinyStories Preparation
- Dataset: ~2GB, designed for <10M param models
- Expected: Coherent story generation capability
- Training estimate: ~12-24 hours on NVIDIA GPU

## Phase 2: Architecture Improvements (1-2 weeks)

### Priority 1: Mamba-2 Upgrade
*From SSM_ARCHITECTURES_RESEARCH.md*

**Rationale**: Mamba-2's State Space Duality (SSD) is 2-8x faster than Mamba-1 with equivalent quality.

**Implementation**:
```rust
// Key changes to differentiable_ssm.rs
// 1. Replace scalar head_dim with multi-head structure
// 2. Implement chunk-parallel algorithm for tensor cores
// 3. Use SSD framework for unified attention/SSM
```

**Effort**: Medium (modify existing SSM, add chunking)
**Impact**: 2-4x training speedup

### Priority 2: Flash Linear Attention Integration
*From FLASH_ATTENTION_RESEARCH.md*

**Rationale**: Our sparse attention layers bottleneck at long sequences.

**Options**:
1. **FlashAttention-3 kernel** - 75% H100 utilization (if CUDA)
2. **PagedAttention** - 4% memory waste vs 70% default
3. **Tiled Flash Linear Attention** - For Mamba's linear attention equivalent

**Effort**: Low-Medium (add optional feature flag)
**Impact**: 2-3x attention layer speedup, longer sequences

### Priority 3: Gated Linear Attention (GLA)
*From SSM_ARCHITECTURES_RESEARCH.md*

**Rationale**: GLA adds data-dependent gating to linear attention, improving expressivity while maintaining O(n) complexity.

**Benefits for Nexus**:
- Drop-in replacement for SSM layers
- Better expressivity than vanilla SSM
- Maintains efficiency at long sequences

## Phase 3: Training Improvements (2-3 weeks)

### Priority 1: GRPO for Alignment
*From REWARD_ALIGNMENT_RESEARCH.md*

**Rationale**: DeepSeek's GRPO eliminates separate critic model, saving 50% RL compute.

**Implementation Path**:
1. Fine-tune on TinyStories
2. Collect preference data (story quality ratings)
3. Implement group-relative policy optimization
4. Train with sampled responses + rewards

**Effort**: Medium
**Impact**: Aligned story generation without massive compute

### Priority 2: Knowledge Distillation Pipeline
*From DISTILLATION_RESEARCH.md*

**Rationale**: MOHAWK achieves Transformer→SSM distillation with <1% data. Llamba matches Llama-3-8B quality.

**Implementation**:
```
Teacher (Qwen2.5-0.5B) → Student (Nexus 7.12M)
Phases: Logit → Feature → Attention distillation
```

**Effort**: Medium-High
**Impact**: Potentially matches 100M+ param quality

### Priority 3: Synthetic Data Generation
*From DATA_TRAINING_RESEARCH.md*

**Rationale**: Small models can self-improve with curriculum.

**Pipeline**:
1. Generate diverse prompts (seed stories)
2. Use larger model for initial completions
3. Filter by quality metrics
4. Train on curriculum (easy → hard)

## Phase 4: Inference Optimization (3-4 weeks)

### Priority 1: Quantization
*From INFERENCE_DEPLOYMENT_RESEARCH.md*

**Target**: INT8 for 2x speedup, INT4 for 4x speedup

**Implementation**:
1. Calibration pass on training data
2. Per-channel quantization for weights
3. Dynamic quantization for activations
4. SSM-specific considerations (state precision)

### Priority 2: Speculative Decoding
*From SPECULATIVE_DECODING_RESEARCH.md*

**Best Option for Nexus**: Self-speculative (Kangaroo-style)
- No separate draft model needed
- Uses early exit from SSM layers
- 2-3x inference speedup

**Implementation**:
1. Add early-exit heads after each SSM layer
2. Confidence-based speculation
3. Verify with full forward pass

### Priority 3: Serving Infrastructure
*From INFERENCE_DEPLOYMENT_RESEARCH.md*

**Options**:
1. **GGML/llama.cpp** - CPU inference, GGUF format
2. **SGLang** - RadixAttention for batching (if scaling up)
3. **Custom Rust server** - Matches codebase, optimal control

## Phase 5: Advanced Features (4+ weeks)

### Test-Time Learning Enhancement
*From ADVANCED_OPTIMIZATION_RESEARCH.md*

**Titans Memory Enhancement**:
- Increase memory slots (4 → 16)
- Add hierarchical memory (short/long term)
- Implement forget mechanism based on surprise decay

### Byte-Level Tokenization (Experimental)
*From TOKENIZATION_RESEARCH.md*

**SpaceByte-style integration**:
```
Bytes → SSM (local) → Attention (at word boundaries) → SSM (local) → Output
```

**Benefits**:
- No vocabulary limitations
- True multilingual capability
- Noise robustness

### MoE Layer (Future Scale)
*From MOE_RESEARCH.md*

**When to add**: If scaling beyond 100M parameters

**Implementation**:
- Expert choice routing (no load balancing loss)
- 4-8 experts with top-2 selection
- Apply to MLP layers only

## Metrics & Milestones

### Near-term (This Week)
| Milestone | Target | Status |
|-----------|--------|--------|
| Shakespeare step 3000 | Val loss <5.15 | In progress |
| TinyStories preprocessing | BPE 8000-vocab | Pending |
| TinyStories training start | PPL <100 @ 1000 steps | Pending |

### Medium-term (2-4 Weeks)
| Milestone | Target |
|-----------|--------|
| Mamba-2 upgrade | 2x training speedup |
| INT8 quantization | Working inference |
| TinyStories completion | Coherent story generation |

### Long-term (1-3 Months)
| Milestone | Target |
|-----------|--------|
| Distillation from teacher | Match 100M quality |
| Speculative decoding | 2x inference speedup |
| GRPO alignment | User-aligned outputs |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SSM expressivity limit | Medium | High | GLA upgrade, more attention layers |
| Memory constraints | Low | Medium | PagedKV, streaming attention |
| Training instability | Low | Medium | Gradient clipping, LR schedules |
| Tokenization bottleneck | Medium | Medium | SpaceByte migration path |

## Resource Requirements

### Compute
- **Shakespeare**: Cloud CPU (current)
- **TinyStories**: NVIDIA GPU (user's local)
- **Distillation**: GPU with teacher model

### Storage
- Checkpoints: ~30MB per step
- TinyStories: ~2GB
- Model variants: ~50-100MB each

## Decision Points

### When to Scale Up
Scale beyond 7.12M when:
1. TinyStories perplexity plateaus above target
2. Distillation shows clear quality ceiling
3. New capabilities require more parameters

### When to Add MoE
Add mixture of experts when:
1. Parameter count >100M
2. Specialization benefits clear (multi-domain)
3. Inference constraints allow sparse activation

### When to Switch Tokenization
Move to byte-level when:
1. Multilingual capability needed
2. Noise robustness critical
3. BLT/SpaceByte implementations mature

## Next Steps (Immediate)

1. **Monitor Shakespeare completion** (step 2800-3000)
2. **Run inference test** on best checkpoint
3. **Prepare TinyStories script** (expand vocab, adjust hyperparams)
4. **Document final Shakespeare results** in TRAINING_PROGRESS.md

---

*This roadmap will be updated as development progresses.*
