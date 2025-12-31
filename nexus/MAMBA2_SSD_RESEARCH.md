# Mamba-2 State Space Duality (SSD) Research

*Synthesized by Ember (Dec 31, 2025)*

## Executive Summary

Mamba-2 introduces State Space Duality (SSD), a fundamental reconceptualization revealing transformers and SSMs as two sides of the same mathematical coin. The key innovation is a chunk-parallel algorithm that leverages matrix multiplication (and tensor cores) instead of sequential scans, achieving 2-8x speedup over Mamba-1.

## Core Innovation: SSD Framework

**Key Insight**: SSMs and (linear) attention are mathematically equivalent through structured matrices.

| Aspect | Mamba-1 | Mamba-2 |
|--------|---------|---------|
| Algorithm | Parallel associative scan | Chunk-parallel matmul |
| Tensor Core Use | ~10-15% | ~75%+ |
| State Dimension N | 16 (limited) | 64-128 (flexible) |
| Lines of Code | ~hundreds | ~25 (minimal SSD) |
| Speed | Baseline | 2-8x faster |

## The Four-Step Chunk Algorithm

The sequence is split into chunks of size Q (e.g., 64-256). Steps 1, 2, and 4 use matmul (parallel on tensor cores); only Step 3 requires sequential processing.

### Step 1: Intra-Chunk Outputs (Parallel)
Compute local output of each chunk assuming initial state = 0.
```
L = exp(segsum(log(A)))  # Decay matrix
Y_local = C @ (L * (B @ X))  # Quadratic form within chunk
```

### Step 2: Chunk State Computation (Parallel)
Compute final state of each chunk assuming initial state = 0.
```
states = B @ (decay * X)  # Per-chunk boundary states
```

### Step 3: Pass States (Sequential)
Recurrence on chunk states - produces actual final states considering all previous inputs.
```
for chunk in chunks:
    state = decay * prev_state + chunk_state
```
This operates on chunks (not tokens) - 100x reduction in sequential operations.

### Step 4: Output from States (Parallel)
Compute output contribution from initial state for each chunk.
```
Y_state = C @ (decay * state)  # Off-diagonal contribution
Y = Y_local + Y_state
```

## The Segsum Primitive

**Problem**: Need to compute segment sums log(a_i) + ... + log(a_{j-1}) for every segment [i:j].

**Solution**: Work in log-space. Products become additions, cumprods become cumsums.

```python
def segsum(x):
    """Stable segment sum in log-space"""
    T = x.shape[-1]
    x = repeat(x, "... d -> ... d e", e=T)
    mask = torch.tril(torch.ones(T, T), diagonal=-1)
    x = x.masked_fill(~mask.bool(), 0)
    return x.cumsum(dim=-2)
```

## Minimal SSD Implementation (~25 lines)

From `ssd_minimal.py`:

```python
def ssd_minimal_discrete(X, A, B, C, block_len, initial_states=None):
    """Minimal SSD with four-step chunk algorithm"""
    assert X.shape[1] % block_len == 0

    # Reshape into chunks
    X, A, B, C = [reshape(x, block_len) for x in (X, A, B, C)]

    # Step 1: Intra-chunk diagonal
    L = torch.exp(segsum(A))
    Y_diag = torch.einsum("bclhn,bcshn,bhcls,bcshp->bclhp", C, B, L, X)

    # Step 2: Intra-chunk state
    decay = torch.exp(A.sum(dim=2))  # Block decay
    states = torch.einsum("bclhn,bcshp->bchpn", B * decay, X)

    # Step 3: Inter-chunk recurrence
    if initial_states is None:
        initial_states = torch.zeros_like(states[:, :1])
    states = torch.cat([initial_states, states], dim=1)
    for i in range(1, states.shape[1]):
        states[:, i] = decay * states[:, i-1] + states[:, i]

    # Step 4: State to output
    state_decay = torch.exp(segsum(A.flip(-1)).flip(-1))
    Y_off = torch.einsum("bclhn,bhcl,bchpn->bclhp", C, state_decay, states)

    return Y_diag + Y_off
```

## Architecture Changes from Mamba-1

### Parameter Generation
- **Mamba-1**: A, B, C computed sequentially from X
- **Mamba-2**: A, B, C computed in parallel with X (fused projection)

### Head Structure
- **Mamba-1**: Single-head SSM
- **Mamba-2**: Multi-head with `headdim` (default 64), grouped via `ngroups`
  - A and D parameters are per-head
  - Enables flexible capacity scaling

### Normalization
- **Mamba-1**: Standard LayerNorm
- **Mamba-2**: RMSNorm with multiplicative gating (`RMSNormGated`)

### Gated MLP Path
- `d_ssm` parameter controls SSM dimensions
- Non-SSM dimensions can go through gated MLP path

## GPU Optimization Details

### Tensor Core Utilization

| GPU | BF16 Matmul | FP32 Arithmetic | Ratio |
|-----|-------------|-----------------|-------|
| A100 | 312 TFLOPS | 19 TFLOPS | 16x |
| H100 | 989 TFLOPS | 67 TFLOPS | 15x |

Mamba-2's matmul-based algorithm accesses this 15-16x advantage.

### Chunk Size Considerations

- **Default**: 64-256 tokens per chunk
- **Trade-off**: Larger chunks = more parallelism, more memory
- **Optimal**: Depends on sequence length and hardware

### Distributed Training

SSD's matrix structure enables:
- **Tensor Parallelism**: Single all-reduce per layer (vs two for attention)
- **Sequence Parallelism**: Split sequence across devices
- **Variable-length sequences**: Efficient for finetuning/inference

## Integration with Nexus

### Current Nexus SSM (differentiable_ssm.rs)
```rust
// Mamba-1 style selective scan
h = A_bar * h + B_bar * x  // Sequential per-token
y = C * h + D * x
```

### Proposed Mamba-2 Upgrade
```rust
// Chunk-parallel SSD
fn ssd_forward(x: Tensor, a: Tensor, b: Tensor, c: Tensor, chunk_size: usize) {
    // 1. Reshape into chunks
    let x_chunks = x.reshape([-1, chunk_size, dim]);

    // 2. Compute decay matrix L = exp(segsum(log(A)))
    let l = segsum_log_space(a);

    // 3. Parallel matmul for intra-chunk (Steps 1, 2, 4)
    // 4. Sequential state passing (Step 3) - but on chunks, not tokens
}
```

### Implementation Steps

1. **Add multi-head structure** to existing SSM
2. **Implement segsum primitive** for decay computation
3. **Add chunk processing** with configurable chunk_size
4. **Fuse parameter generation** (A, B, C in parallel)
5. **Add RMSNormGated** normalization

### Effort/Impact Assessment

| Change | Effort | Impact |
|--------|--------|--------|
| Multi-head SSM | Medium | High (expressivity) |
| Chunk algorithm | High | Very High (2-8x speed) |
| RMSNormGated | Low | Medium (training stability) |
| Fused projections | Medium | Medium (efficiency) |

## Performance Expectations

For Nexus (7.12M params, 6 layers, 5 SSM):

| Metric | Mamba-1 (Current) | Mamba-2 (After Upgrade) |
|--------|-------------------|-------------------------|
| Training Speed | 56 tok/s | ~150-200 tok/s (est.) |
| State Dimension | 16 | 64+ |
| Memory | Baseline | Similar (with chunks) |

## Key Takeaways

1. **SSD unifies SSMs and attention** - Same math, different perspectives
2. **Chunk algorithm is key** - Enables tensor core utilization
3. **25-line implementation** - Simpler than Mamba-1's optimized scan
4. **State dimension unlocked** - N=64-128 vs N=16 limit
5. **Drop-in replacement potential** - Can upgrade existing SSM layers

## Sources

- [Tri Dao's Blog - Mamba-2 Algorithm](https://tridao.me/blog/2024/mamba2-part3-algorithm/)
- [Goomba Lab Mirror](https://goombalab.github.io/blog/2024/mamba2-part3-algorithm/)
- [Princeton PLI Blog](https://pli.princeton.edu/blog/2024/mamba-2-algorithms-and-systems)
- [GitHub: state-spaces/mamba](https://github.com/state-spaces/mamba)
- [HuggingFace Mamba2 Docs](https://huggingface.co/docs/transformers/model_doc/mamba2)
- [Mamba-2 Paper (ICML 2024)](https://arxiv.org/abs/2405.21060)

## Next Steps for Nexus

1. **Complete Shakespeare training** (step 3000)
2. **Prototype multi-head SSM** in Rust
3. **Implement segsum** with numerical stability
4. **Benchmark chunk sizes** on user's NVIDIA GPU
5. **Validate against Mamba-2 reference** outputs
