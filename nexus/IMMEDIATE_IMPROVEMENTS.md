# Immediate Improvements for Nexus v1.x

Low-effort, high-value changes to apply NOW or soon after training completes.

---

## 1. Quick Wins (Can Apply Today)

### 1.1 Better Tokenization
**Current**: Byte-level (vocab_size=256) - inefficient for text
**Problem**: ~4 bytes per token average, 4x more tokens than necessary

**Fix**: Use trained BPE tokenizer (already exists!)
```
nexus/tokenizers/
└── shakespeare_bpe.json  ← Already trained, 2000 tokens
```

**Impact**: 3-4x fewer tokens = 3-4x faster inference + better learning

### 1.2 Sampler Improvements ✅ DONE
**COMPLETED in streaming.rs** (Dec 2024)

Added to SamplingConfig:
```rust
pub struct SamplingConfig {
    temperature: f32,
    top_k: usize,
    top_p: f32,
    min_p: f32,                    // ✅ Added - min probability threshold
    repetition_penalty: f32,
    repetition_window: usize,      // ✅ Added - how far back to look
    frequency_penalty: f32,        // ✅ Added - penalize by count
    presence_penalty: f32,         // ✅ Added - penalize present tokens
    greedy: bool,
    seed: Option<u64>,
}
```

**Location**: `nexus/src/streaming.rs` lines 16-37

### 1.3 Batch Inference
**Current**: Single sequence at a time
**Fix**: Batch multiple prompts together

```rust
// In inference.rs generate function
fn generate_batch(
    model: &DifferentiableHybridNexusLM,
    prompts: &[String],  // Multiple prompts
    max_tokens: usize,
    sampler: &mut Sampler,
) -> Vec<String>
```

**Impact**: 2-4x throughput on same hardware

---

## 2. Memory Optimization (Apply This Week)

### 2.1 Gradient Checkpointing
**Problem**: Memory grows with sequence length
**Already in code**: Checkpointing infrastructure exists

**Verify enabled**:
```rust
// In training loop - check these are using checkpointing
let logits = model.forward_with_checkpointing(&tokens);
```

### 2.2 Mixed Precision Training
**Problem**: f32 uses 4 bytes per param
**Fix**: Use bf16/fp16 for forward pass, f32 for accumulation

**Impact**: 2x memory reduction, often faster

### 2.3 KV Cache Reuse
**Current**: Regenerates KV for entire sequence each step
**Fix**: Cache and only compute new positions

```rust
pub struct InferenceCache {
    kv_cache: Vec<(Tensor, Tensor)>,  // Per layer
    past_length: usize,
}
```

**Impact**: O(1) per new token instead of O(n)

---

## 3. Training Improvements (Next Run)

### 3.1 Learning Rate Warmup Adjustment
**Current**: 100 warmup steps, cosine to 2000
**Observation**: Loss still improving at step 1000

**Recommendation**:
- Extend to 3000-4000 steps
- Or use inverse sqrt decay instead of cosine

### 3.2 Larger Batch Size
**Current**: effective batch = 16 (4 * 4 accum)
**Problem**: Small batch can cause noisy gradients

**Recommendation**:
- Increase grad_accum to 8 (effective 32)
- Or increase batch_size if memory allows

### 3.3 Data Augmentation
**Current**: Raw Shakespeare text
**Add**:
- Random chunking at different offsets
- Character-level noise (typos for robustness)
- Mix in more diverse text

---

## 4. Inference Speed (Post-Training)

### 4.1 Torch-style JIT Compilation
**For Rust**: Use `#[inline(always)]` on hot paths
**Key functions**:
- `forward` in all layers
- `softmax`
- Matrix multiplications

### 4.2 SIMD Vectorization
**Check**: Is SIMD being used in ndarray ops?
```rust
// Cargo.toml - verify these features
ndarray = { version = "0.16", features = ["rayon"] }
```

**Add**: `blas` feature for SIMD matrix ops
```rust
ndarray = { version = "0.16", features = ["rayon", "blas"] }
```

### 4.3 Parallel Attention Heads
**Current**: Likely sequential head computation
**Fix**: Use rayon to parallelize across heads

```rust
use rayon::prelude::*;

let head_outputs: Vec<_> = (0..n_heads)
    .into_par_iter()
    .map(|h| self.compute_head(h, q, k, v))
    .collect();
```

---

## 5. Serving Improvements

### 5.1 Streaming Response
**Current server**: Returns full response
**Fix**: Stream tokens as generated

```rust
// In serve.rs
async fn generate_stream(
    prompt: String,
) -> impl Stream<Item = String> {
    // Yield each token as generated
}
```

### 5.2 Request Queuing
**Add**: Priority queue for incoming requests
**Benefit**: Handle burst traffic gracefully

### 5.3 Health Endpoint
**Add**: `/health` endpoint for load balancers
```rust
app.route("/health", get(|| async { "OK" }))
```

---

## 6. Evaluation Additions

### 6.1 Perplexity Benchmark
**Add**: Standardized eval on held-out text
```rust
fn evaluate_perplexity(model: &Model, text: &str) -> f32 {
    // Cross-entropy on held-out text
}
```

### 6.2 Generation Quality Metrics
**Add**:
- Distinct-n (diversity)
- Repetition rate
- Average token probability

### 6.3 Speed Benchmarks
**Add**: Tokens/second at various batch sizes
```rust
fn benchmark_throughput(model: &Model, batch_sizes: &[usize]) {
    for bs in batch_sizes {
        let tokens_per_sec = measure_speed(model, *bs);
        println!("Batch {}: {} tok/s", bs, tokens_per_sec);
    }
}
```

---

## Priority Ranking

| Improvement | Effort | Impact | Status |
|-------------|--------|--------|--------|
| ✅ Min-p sampling | Low | Medium | **DONE** (streaming.rs) |
| Use BPE tokenizer | Low | High | After training |
| KV cache reuse | Medium | High | After training |
| Batch inference | Medium | High | After training |
| Streaming server | Low | Medium | After training |
| SIMD/BLAS | Low | Medium | After training |
| Parallel heads | Medium | Medium | After training |
| Gradient checkpointing | Low | Medium | Next training run |
| Mixed precision | Medium | High | Next training run |
| Extended training | Low | Medium | Next run (3000+ steps) |

---

## Files to Modify

```
nexus/
├── src/
│   ├── sampling.rs      # Add min-p, frequency penalty
│   ├── hybrid.rs        # KV cache, parallel heads
│   └── bin/
│       ├── serve.rs     # Streaming, health endpoint
│       └── infer.rs     # Batch inference
├── examples/
│   └── inference.rs     # Use BPE tokenizer
└── Cargo.toml           # Add BLAS feature
```

---

*Apply these before starting v2 development for immediate wins.*
