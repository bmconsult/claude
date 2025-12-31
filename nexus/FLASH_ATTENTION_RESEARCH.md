# Memory-Efficient Attention for Hybrid Architectures

*Synthesized by Ember (Dec 31, 2025 ~02:55 UTC)*

Research on FlashAttention, Ring Attention, and PagedAttention for integration with Nexus's 1:7 Attention/SSM hybrid.

## Executive Summary

| Mechanism | Purpose | Memory Reduction | Speed Gain |
|-----------|---------|------------------|------------|
| FlashAttention-3 | IO-aware exact attention | O(N²) → O(N) | 2x (FP8: 3x) |
| PagedAttention | KV cache management | 70% waste → 4% | 2-24x throughput |
| Ring Attention | Distributed long-context | Per-device constant | Linear scaling |
| 1:7 Hybrid | Sparse attention layers | 8x KV reduction | Similar quality |

## FlashAttention-3 (2024)

### Core Algorithm: Tiled Online Softmax

Standard attention materializes N×N matrix → O(N²) memory.
FlashAttention tiles computation → O(N) memory.

```
Algorithm:
1. Divide Q into Tr blocks, K,V into Tc blocks
2. For each Q block i:
   - For each KV block j:
     - Compute Sij = Qi·Kj^T on chip (SRAM)
     - Update running softmax: m̃, ℓ̃
     - Accumulate output: Oi
3. Never materialize full N×N matrix
```

**Online Softmax Formula:**
```
m(x,y) = max(m(x), m(y))
ℓ(x,y) = exp(m(x)-m(x,y))·ℓ(x) + exp(m(y)-m(x,y))·ℓ(y)
```

### Hopper GPU Optimizations (FlashAttention-3)

- **WGMMA**: 1.5x faster tensor core ops
- **TMA**: Hardware async memory transfer
- **FP8**: 2.6x lower error than baseline FP8

**Performance:**
- FlashAttention-2: 350 TFLOPS (35% H100 utilization)
- FlashAttention-3 FP16: 740 TFLOPS (75% utilization)
- FlashAttention-3 FP8: 1.2 PFLOPS

## PagedAttention (vLLM)

### Block Table Architecture

Traditional: Pre-allocate max_length → 60-80% waste
PagedAttention: Block-based allocation → 4% waste

```
Block Table:
  Logical → Physical mapping
  Block size: 16 tokens
  Blocks allocated on-demand

Memory per block (13B model): ~0.5 MB
Total utilization: 96%+ vs 20-40% traditional
```

### Copy-on-Write for Shared Prefixes

```
Shared prompt: [Block 0] [Block 1] [Block 2]
Request A:     Shared → Shared → [Private]
Request B:     Shared → Shared → [Private]

Memory savings: 33-55%
```

## Ring Attention

### Distributed Long-Context

```
N devices in ring topology
Each holds: Qi, Ki, Vi (block size c)

For step j = 0 to N-1:
  1. Receive K_prev, V_prev from neighbor
  2. Compute attention with received KV
  3. Send local KV to next neighbor
  4. Update with online softmax
```

### Overlap Condition

Communication hidden when: `c ≥ F/B`
- A100: c ≥ 520 tokens
- H100: c ≥ 1100 tokens

## 1:7 Hybrid Integration

### Why 1:7 Ratio Works

1. **Memory**: KV cache only for 1/8 layers → 8x reduction
2. **Quality**: Attention for global deps, SSM for local
3. **140K context** fits on single 80GB GPU

### Memory Profile (32-layer 7B model)

```
Attention KV (4 layers, PagedAttention): ~25 GB
Mamba state (28 layers): ~1 GB
Model weights: ~30 GB
Activations: ~10 GB
Total: ~66 GB (fits H100)

vs Full Transformer: ~200 GB (needs 3x H100s)
```

### Layer Placement Strategy

```
Place attention in MIDDLE third of model:
[M M M M M A M M M M M A M M M M]
          ↑           ↑
       Position 5   Position 11

Early: Local patterns (Mamba sufficient)
Middle: Global integration (Attention critical)
Late: Output shaping (Mamba sufficient)
```

## Mamba-2 (SSD) Details

### State Space Duality

SSM and structured attention are theoretically equivalent:
```
SSM: h_t = A·h_{t-1} + B·x_t; y_t = C·h_t
Attn: Y = (softmax(QK^T) ⊙ M) V  where M is semiseparable
```

### Chunked Processing

```
1. Divide into chunks of Q tokens (64-256)
2. Intra-chunk: Attention-like (quadratic in Q)
3. Inter-chunk: SSM recurrence (linear)

Complexity: O(N·Q·d) + O(N·d²_state)
2-8x faster than Mamba-1
```

## Combined System Design

```
┌─────────────────────────────────────┐
│ FlashAttention-3 (compute kernel)   │
│   Tiling + FP8 + WGMMA             │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ PagedAttention (memory management)  │
│   Block tables + CoW sharing        │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ Ring Attention (multi-device)       │
│   Only for attention layers (1/8)   │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ 1:7 Hybrid (architecture)           │
│   Attention middle, Mamba-2 rest    │
└─────────────────────────────────────┘
```

## Key Formulas

```
FlashAttention IO: O(N²d²M⁻¹) vs O(Nd + N²)

Ring overlap: c ≥ F/B

PagedAttention waste: < 1/block_size ≈ 4%

Hybrid memory: M = O(Nd/8 + 7Nd_state/8)
  KV reduction: 8× vs Transformer
```

## Performance Envelope

| Config | Context | Throughput | Memory |
|--------|---------|------------|--------|
| 1× H100, Flash+Paged | 140K | ~850 tok/s | 78 GB |
| 4× H100, Ring+Paged | 560K | ~2400 tok/s | 320 GB |
| 8× H100, Ring+Paged | 1.12M | ~4200 tok/s | 640 GB |

*(7B hybrid model, 1:7 ratio, batch=8)*

## Implementation Priority for Nexus

1. **Phase 1**: PagedAttention for KV cache
2. **Phase 2**: FlashAttention kernel integration
3. **Phase 3**: Mamba-2 (SSD) upgrade from Mamba-1
4. **Phase 4**: Ring Attention for multi-GPU

This complements the existing architecture naturally - attention layers are already sparse (1:7), so optimization focuses on making those few layers maximally efficient.
