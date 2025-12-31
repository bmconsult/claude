# SSM Architectures Research

*Synthesized by Ember (Dec 31, 2025 ~04:20 UTC)*

Deep dive into Mamba-2, Linear Attention, and SSM architectural innovations.

## Executive Summary

| Architecture | Speed | Memory | Key Innovation |
|--------------|-------|--------|----------------|
| **Mamba-1** | 5x vs Transformer | O(1) per token | Selective State Space |
| **Mamba-2** | 2-8x faster than Mamba-1 | Same | State Space Duality (SSD) |
| **Linear Attention** | 3.3x faster | 3.6x less | Linear kernel approximation |
| **Hybrid 1:7** | Balanced | Mixed O(n²)/O(n) | Best of both worlds |

## Mamba-2: State Space Duality

### Core Innovation

Mamba-2 introduces **State Space Duality (SSD)** - a mathematical framework unifying SSMs with structured attention.

```
Key Insight: Certain SSMs are equivalent to a form of
structured masked attention (specifically semiseparable matrices).

This means:
- SSM operations can be computed with attention-like algorithms
- Enables use of tensor core hardware (like FlashAttention)
- 2-8x faster than original Mamba scan
```

### Architectural Changes from Mamba-1

| Component | Mamba-1 | Mamba-2 |
|-----------|---------|---------|
| **State dimension** | N=16 | N=64-128+ |
| **A matrix** | Diagonal | Scalar times identity |
| **Computation** | Sequential scan | Matrix multiply blocks |
| **Hardware** | Generic | Tensor cores optimized |
| **Multi-head** | Not used | 8+ heads typical |

### SSD Block Structure

```
Input: x ∈ R^(B×L×D)

1. Linear projections:
   A = linear_A(x)        # State transition (scalar per head)
   B = linear_B(x)        # Input projection
   C = linear_C(x)        # Output projection
   D = linear_D(x)        # Skip connection

2. SSD core (structured attention view):
   - Create semiseparable matrix M from A, B, C
   - Compute y = M @ x using block-diagonal algorithm
   - Hardware-friendly: uses matmul, not sequential scan

3. Output:
   y = y + D * x          # Skip connection
   output = linear_out(y)
```

### Performance Results (Official)

From Mamba-2 paper (Tri Dao, Albert Gu, 2024):

| Model Size | Mamba-1 (tok/s) | Mamba-2 (tok/s) | Speedup |
|------------|-----------------|-----------------|---------|
| 130M | 1,200 | 4,800 | 4.0x |
| 370M | 800 | 4,200 | 5.3x |
| 1.3B | 350 | 2,100 | 6.0x |
| 2.7B | 180 | 1,400 | 7.8x |

### State Expansion Benefits

Larger state dimension N allows more expressive modeling:

```
Mamba-1: N=16 (limited memory per position)
Mamba-2: N=64-128 (8x more state capacity)

More state = better long-range dependencies
Without the O(N²) cost of attention
```

### Algorithm: Chunk-wise Parallel Scan

```python
# Pseudocode for Mamba-2 SSD computation
def ssd_forward(x, A, B, C, D, chunk_size=64):
    B, L, D = x.shape
    num_chunks = L // chunk_size

    # Process chunks in parallel
    chunks = x.reshape(B, num_chunks, chunk_size, D)

    # Within-chunk: dense matmul (on tensor cores)
    # Between-chunk: recurrence (small state)

    for chunk_idx in range(num_chunks):
        # Build semiseparable matrix for this chunk
        M = build_semiseparable(A, B, C, chunk_idx)
        # Matmul on tensor cores
        y_chunk = M @ x_chunk
        # Update inter-chunk state
        state = update_state(state, chunk)

    return y + D * x  # Skip connection
```

## Linear Attention

### Theory

Standard attention has quadratic complexity from softmax:
```
Attention(Q, K, V) = softmax(QK^T / √d) V    # O(L²)
```

Linear attention replaces softmax with feature maps:
```
Linear(Q, K, V) = φ(Q) (φ(K)^T V)            # O(L)
```

Where φ is a kernel feature map (e.g., ELU + 1, ReLU, random features).

### Flash Linear Attention (FLA)

State-of-the-art library for linear attention variants:

| Variant | Description | Speed vs FlashAttention-2 |
|---------|-------------|---------------------------|
| **GLA** | Gated Linear Attention | 2.1x |
| **RetNet** | Retention Networks | 2.8x |
| **HGRN** | Hierarchical Gated RNN | 3.1x |
| **Mamba** | Selective SSM | 2.5x |
| **RWKV** | Receptance Weighted KV | 3.3x |

### FLA Performance (from triton-lang/flash-linear-attention)

```
Benchmarks on A100 (seq_len=2048, batch=16):

Model         | Time (ms) | Memory (GB) | vs FA-2
--------------|-----------|-------------|--------
FlashAttn-2   | 12.4      | 18.2        | 1.0x
GLA           | 5.9       | 5.1         | 2.1x
RetNet        | 4.4       | 4.8         | 2.8x
RWKV-6        | 3.8       | 5.0         | 3.3x

Memory improvement: 3.6x less than FlashAttention-2
```

### Linear Attention Variants

**1. Gated Linear Attention (GLA)**
```
GLA adds gating to control information flow:
y_t = g_t * (φ(q_t)^T S_t) + (1 - g_t) * x_t
S_t = S_{t-1} + φ(k_t) v_t^T   # Cumulative sum
```

**2. RetNet (Retention Networks)**
```
Combines recurrence with parallel training:
- Training: Parallel chunk-wise computation
- Inference: O(1) recurrent state
- Uses exponential decay for "forgetting"
```

**3. RWKV-6**
```
Latest RWKV with:
- Time-mixing: Linear attention with decay
- Channel-mixing: FFN-like operation
- State-of-the-art linear RNN performance
```

## Hybrid Architectures

### Optimal Mixing Ratios

Research consensus on attention/SSM mixing:

| Ratio | Use Case | Examples |
|-------|----------|----------|
| **1:1** | Balanced | Early hybrids |
| **1:3** | More SSM | Jamba small |
| **1:7** | SSM-heavy | Jamba, Nexus |
| **Pure SSM** | Long context | Mamba, RWKV |

### Why 1:7 Works

```
Attention layers:
- Capture arbitrary dependencies (in-context learning)
- O(n²) cost but only 1/8 of layers
- Handle "lookup" operations

SSM layers:
- Efficient long-range (O(n) per layer)
- Recurrent state for compression
- Handle sequential patterns

Together: Best of both with O(n) dominated
```

### Jamba Architecture

Jamba (AI21 Labs) validated the 1:7 hybrid:

| Component | Details |
|-----------|---------|
| **Attention** | Every 8th layer (with MoE) |
| **SSM** | 7 of 8 layers (Mamba-style) |
| **MoE** | 16 experts, top-2 routing |
| **Context** | 256K tokens |
| **Parameters** | 52B total, 12B active |

Results: 3x throughput vs Mixtral at same quality.

## For Nexus: Integration Roadmap

### Phase 1: Mamba-2 Core (Recommended First)

Current Nexus uses Mamba-1 style scan. Upgrade path:

```rust
// Current: differentiable_ssm.rs uses sequential scan
// New: Add SSD block with chunk-parallel computation

struct SSDBlock {
    // Larger state dimension
    state_dim: usize,  // 64-128 vs current 16

    // Scalar A (simpler than diagonal)
    a_log: f32,  // Single learned parameter

    // Multi-head structure
    num_heads: usize,  // 8 typical

    // Chunk size for parallel computation
    chunk_size: usize,  // 64 typical
}

impl SSDBlock {
    fn forward(&self, x: &Tensor) -> Tensor {
        // 1. Project to heads
        let (b, c, d) = self.compute_bcd(x);

        // 2. Chunk-parallel SSD computation
        let y = self.ssd_parallel(x, b, c, d);

        // 3. Apply skip connection
        y + self.d_proj * x
    }
}
```

### Phase 2: Linear Attention Layer

Add GLA as alternative to standard attention:

```rust
struct GatedLinearAttention {
    d_model: usize,
    num_heads: usize,
    feature_map: FeatureMap,  // ELU+1, ReLU, etc.
}

impl GatedLinearAttention {
    fn forward(&self, x: &Tensor, state: Option<&Tensor>) -> Tensor {
        let (q, k, v, g) = self.qkvg_proj(x);

        // Apply feature map
        let q = self.feature_map.apply(q);
        let k = self.feature_map.apply(k);

        // Linear attention with gating
        let s = cumsum(outer(k, v));  // Running sum
        let y = einsum("bhd,bhde->bhe", q, s);

        // Gated output
        g * y + (1 - g) * x
    }
}
```

### Phase 3: Hybrid Controller

Dynamic selection between mechanisms:

```rust
enum MechanismType {
    SSD,      // Mamba-2 style
    GLA,      // Gated Linear Attention
    Attention,// Standard (sparse)
}

struct AdaptiveHybridBlock {
    mechanisms: Vec<Box<dyn Mechanism>>,
    router: Router,  // Learned or rule-based
}

impl AdaptiveHybridBlock {
    fn forward(&self, x: &Tensor) -> Tensor {
        // Rule-based: attention every 8th layer
        // Or learned: router selects based on input
        let mechanism = self.router.select(x);
        mechanism.forward(x)
    }
}
```

## Performance Formulas

### Mamba-2 SSD Complexity

```
Traditional scan: O(L * N * D) sequential
SSD parallel:     O(L * N * D / chunk_size) parallel + O(chunks) sequential

With chunk_size = 64, L = 2048:
- 32x more parallelism
- Enables tensor core usage
```

### Linear Attention Complexity

```
Standard Attention: O(L² * d) compute, O(L²) memory
Linear Attention:   O(L * d * d) compute, O(L * d) memory

For d << L (typical):
- Compute: L/d speedup (e.g., 32x for L=2048, d=64)
- Memory: L/d reduction
```

### State Capacity

```
SSM state: N dimensions per position
- Mamba-1: N=16 → 16 numbers to remember
- Mamba-2: N=128 → 128 numbers to remember

Effective "context": O(N * D) parameters in state
- Higher N = more expressive memory
- But still O(1) inference per token
```

## Key Insights

1. **SSD unifies SSM and attention** - Same math, different views
2. **Larger state is affordable** - Mamba-2 proves N=128 works well
3. **Chunk parallelism is key** - Enables tensor core utilization
4. **Linear attention is mature** - FLA library production-ready
5. **1:7 ratio validated** - Jamba proves hybrid works at scale

## References

- [Mamba-2 Paper](https://arxiv.org/abs/2405.21060) - Tri Dao, Albert Gu, May 2024
- [Flash Linear Attention](https://github.com/triton-lang/flash-linear-attention) - Triton implementation
- [Jamba Architecture](https://arxiv.org/abs/2403.19887) - AI21 Labs, March 2024
- [GLA Paper](https://arxiv.org/abs/2312.06635) - Gated Linear Attention
- [RetNet Paper](https://arxiv.org/abs/2307.08621) - Retention Networks
- [RWKV-6 Release](https://github.com/BlinkDL/RWKV-LM)
