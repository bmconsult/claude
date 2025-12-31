# Inference Serving & Quantization for LLM Deployment

*Synthesized by Ember (Dec 31, 2025 ~03:45 UTC)*

Research on inference engines (vLLM, TensorRT-LLM, SGLang) and quantization methods (GPTQ, AWQ, GGUF).

## Executive Summary

| Engine | Best For | Throughput | Ease of Use |
|--------|----------|------------|-------------|
| **vLLM** | General serving, flexibility | 600-650 tok/s | Excellent |
| **TensorRT-LLM** | NVIDIA-specific, low latency | 700 tok/s | Challenging |
| **SGLang** | Structured output, prefix caching | 6.4× vLLM | Good |

| Quantization | Target | Quality | Speed |
|--------------|--------|---------|-------|
| **GPTQ** | GPU inference | Good | 5× faster |
| **AWQ** | Edge/latency-sensitive | Better | 1.3× GPTQ |
| **GGUF** | CPU/Apple Silicon | Good | CPU-optimized |

## Inference Engines Comparison

### vLLM (UC Berkeley)

**Key innovations:**
- **PagedAttention**: KV cache memory efficiency
- **Continuous Batching**: Dynamic request handling

**Performance:**
- 600-650 tok/s on Llama-3-70B-Q4 (A100 80GB)
- Low TTFT even under high load
- OpenAI-compatible API

**Best for:**
- Fast time-to-serve
- Elastic batching
- Prefix caching
- Dynamic workloads

### TensorRT-LLM (NVIDIA)

**Key innovations:**
- CUDA graph optimizations
- Fused custom kernels
- Tensor Core acceleration
- Inflight batching

**Performance:**
- 700 tok/s on Llama-3-70B-Q4 (A100 80GB)
- Best on latest NVIDIA hardware (B200)
- TTFT can increase significantly under load

**Best for:**
- Ultra-low latency
- Short prompts/outputs
- Stable, high-performance demands
- When hardware is well-supported

**Challenges:**
- Complex setup (convert checkpoints, build TRT engine)
- Requires reading through multiple docs
- Less flexible than vLLM

### SGLang (LMSYS)

**Key innovations:**
- **RadixAttention**: Automatic KV cache reuse across calls
  - 85-95% hit rate vs 15-25% for PagedAttention (few-shot)
  - 75-90% hit rate vs 10-20% (multi-turn chat)
- **Compressed FSM**: 3× faster structured JSON output
- Zero-overhead CPU scheduler

**Performance:**
- Up to 6.4× higher throughput than vLLM/TensorRT-LLM
- Day-0 support for DeepSeek V3/R1
- Trillions of tokens daily in production

**Best for:**
- Structured generation (JSON, code)
- Multi-turn conversations
- Few-shot learning with shared examples
- Prefix-heavy workloads

**Industry adoption:**
- 400,000+ GPUs worldwide
- Used by xAI, AMD, NVIDIA, Intel, LinkedIn, Cursor

### Decision Matrix

```
Need structured output?     → SGLang
Need NVIDIA-specific perf?  → TensorRT-LLM (if complexity acceptable)
Need flexibility/easy API?  → vLLM
Need prefix caching?        → SGLang > vLLM
Need lowest latency?        → TensorRT-LLM
Need easiest setup?         → vLLM > SGLang > TensorRT-LLM
```

## Quantization Methods

### GPTQ (GPU Post-Training Quantization)

**How it works:**
- One-shot weight quantization using second-order information
- Calibration dataset required
- Supports 2/3/4/8-bit quantization

**Key characteristics:**
```
Pros:
  - First method to achieve 4-bit with good quality
  - 5× faster than GGUF on GPU
  - Optimized kernels (Marlin)

Cons:
  - Calibration-sensitive (dataset choice matters)
  - GPU-focused only
```

**Performance:**
- GPTQ-INT8: ~95%+ baseline accuracy
- GPTQ-INT4: ~85-90% baseline (task-dependent)

### AWQ (Activation-Aware Weight Quantization)

**How it works:**
- Identifies salient weights (<1% of total)
- Keeps salient weights in FP16
- Quantizes rest to INT3/INT4
- No backpropagation required

**Key characteristics:**
```
Pros:
  - Better quality than GPTQ at same bit-width
  - Less calibration-sensitive
  - 1.3× faster than GPTQ
  - Better generalization

Cons:
  - Slightly more complex implementation
  - Less mature ecosystem
```

**Performance:**
- Often outperforms GPTQ in benchmarks
- Less prone to overfitting calibration set

### GGUF (GGML Unified Format)

**How it works:**
- File format for quantized models
- Multiple quantization levels (Q2-Q8, K variants)
- CPU-optimized with GPU offload support

**Key characteristics:**
```
Pros:
  - CPU inference (no GPU required)
  - Apple Silicon optimized
  - Flexible GPU offloading
  - Used by llama.cpp

Cons:
  - Slower than pure GPU methods
  - Quality varies by quant level
```

**Quantization levels:**
| Level | Size | Quality | Use Case |
|-------|------|---------|----------|
| Q8_0 | 100% | Best | Development |
| Q5_K_M | 63% | Excellent | Production |
| Q4_K_M | 50% | Good | Balanced |
| Q4_K_S | 47% | Acceptable | Memory-constrained |
| Q2_K | 25% | Poor | Extreme compression |

### Quality by Task Type

| Task | GPTQ-INT8 | GPTQ-INT4 | AWQ | GGUF Q4_K_M |
|------|-----------|-----------|-----|-------------|
| IFEval (instruction) | Good | Poor (>10% loss) | Worse than GPTQ | Poor |
| GSM8K (math) | Excellent | Good (84-87%) | Good | Good |
| General reasoning | Good | Acceptable | Good | Acceptable |
| Text generation | Excellent | Good | Good | Good |

**Key finding:** Math reasoning is structurally resilient to quantization, while instruction-following is highly sensitive.

### Recommendations

| Deployment Target | Method | Why |
|-------------------|--------|-----|
| NVIDIA GPU, production | AWQ or GPTQ-INT4 | Best speed + quality |
| NVIDIA GPU, quality-critical | GPTQ-INT8 | Near-baseline quality |
| CPU only | GGUF Q4_K_M or Q5_K_M | Only option |
| Apple Silicon | GGUF with Metal | Optimized |
| Edge/mobile | AWQ | Best quality at low bits |

## For Nexus Deployment

### Current State
- 7M parameters (small model)
- Hybrid attention/SSM architecture
- Already has quantization.rs (INT8)

### Recommended Path

**Phase 1: CPU/Local Inference**
```
Export to GGUF format
Use Q4_K_M or Q5_K_M
Target: llama.cpp compatible

Why: Broadest deployment reach
```

**Phase 2: GPU Serving (if scaled)**
```
Option A: vLLM + AWQ
  - Easiest setup
  - Good quality

Option B: SGLang + GPTQ
  - If structured output needed
  - Better prefix caching
```

**Quantization for 7M Model:**
At 7M parameters, quantization savings are minimal:
- FP32: 28MB → INT4: 7MB (only 21MB saved)
- Focus on speed rather than memory

Consider: **Mixed precision** (FP16 for attention, INT8 for SSM) given hybrid architecture.

### SSM-Specific Considerations

Mamba/SSM layers may have different quantization sensitivity than attention:
- State matrices (A, B, C) may be more sensitive
- Discretization (dt) requires precision
- Gating mechanisms need testing

**Recommendation:** Benchmark SSM vs attention layer sensitivity before deploying quantized Nexus.

## Key Formulas

### Throughput Calculation
```
Throughput = tokens_generated / (prefill_time + decode_time)

Where:
  prefill_time = O(seq_len² · d_model)  # for attention
  decode_time = O(seq_len · d_model)    # per token
```

### Quantization Memory Savings
```
Memory_ratio = bits_quantized / bits_original
INT4/FP16 = 4/16 = 25%
INT4/FP32 = 4/32 = 12.5%
```

### Cache Hit Rate (RadixAttention)
```
Hit_rate = reused_tokens / total_tokens
SGLang: 75-95% for multi-turn
vLLM:   10-25% for multi-turn
```

## References

- vLLM Paper: UC Berkeley (2023)
- SGLang Paper: NeurIPS 2024, arxiv.org/abs/2312.07104
- GPTQ Paper: arxiv.org/abs/2210.17323
- AWQ Paper: MIT (2024)
- BentoML Benchmarks (2025)
- Rafay Documentation on vLLM vs TensorRT-LLM
