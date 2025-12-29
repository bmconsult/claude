# Nexus: Hybrid Intelligence Architecture

## Vision

Combine the breakthroughs of 2024-2025 into a unified architecture:
- Hybrid Attention/SSM for efficient long context
- Test-time learning memory (Titans-style)
- Latent world model (JEPA-inspired)
- Neuro-symbolic reasoning pipeline

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           NEXUS CORE                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │  ATTENTION  │    │     SSM     │    │   MEMORY    │              │
│  │   (1:7)     │◄──►│   (Mamba)   │◄──►│  (Titans)   │              │
│  └─────────────┘    └─────────────┘    └─────────────┘              │
│         │                  │                  │                     │
│         └──────────────────┼──────────────────┘                     │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │  WORLD MODEL    │                               │
│                   │  (JEPA-style)   │                               │
│                   │  Latent Space   │                               │
│                   └────────┬────────┘                               │
│                            │                                        │
│         ┌──────────────────┼──────────────────┐                     │
│         ▼                  ▼                  ▼                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐              │
│  │   REASON    │    │   VERIFY    │    │   OUTPUT    │              │
│  │  (Symbolic) │───►│  (Prover)   │───►│ (Generate)  │              │
│  └─────────────┘    └─────────────┘    └─────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Hybrid Core (Rust)

**Attention Block:**
- Standard multi-head attention with RoPE
- Used sparingly (1 in 8 layers)
- Handles retrieval and copying tasks

**SSM Block (Mamba-style):**
- Selective state space model
- Linear scaling with sequence length
- Handles most sequence modeling

**Ratio:** 1:7 (attention:SSM) based on Jamba findings

### 2. Test-Time Memory (Titans-style)

**Key Innovation:** Memory that learns DURING inference

**Surprise Metric:**
```
surprise(x) = -log P(x | context)
```
High surprise → store in long-term memory

**Three Memory Types:**
- **Short-term:** Attention window (current context)
- **Long-term:** Learned representations (test-time updated)
- **Persistent:** Task knowledge (fixed after training)

**Memory Update Rule:**
```
M' = M + η * surprise(x) * gradient(loss)
```

### 3. World Model (JEPA-inspired)

**Core Idea:** Predict in latent space, not token space

```
encoder(x) → z
predictor(z, context) → z'
compare(z', encoder(x')) → loss
```

**Benefits:**
- No need to predict exact tokens
- Can handle ambiguity
- More efficient than generative models

### 4. Neuro-Symbolic Reasoning

**Pipeline:**
```
Natural Language → LLM Parser → Formal Logic (PDDL/Prolog)
                                      ↓
                              Symbolic Solver
                                      ↓
                              Verified Result
```

**Components:**
- Parser: Convert NL to formal representation
- Solver: Execute formal reasoning (deterministic)
- Verifier: Check solution satisfies constraints

## Implementation Plan

### Phase 1: Core Types and Interfaces (Rust)
- [ ] Tensor type with basic ops
- [ ] Attention mechanism
- [ ] SSM (simplified Mamba)
- [ ] Memory module interface

### Phase 2: Hybrid Block
- [ ] Combine attention + SSM in configurable ratio
- [ ] RMSNorm for stability
- [ ] Residual connections

### Phase 3: Titans Memory
- [ ] Surprise computation
- [ ] Test-time gradient update
- [ ] Memory read/write operations

### Phase 4: Integration
- [ ] Stack blocks into full model
- [ ] World model predictor
- [ ] Neuro-symbolic pipeline

### Phase 5: Python Bindings
- [ ] PyO3 bindings for Rust core
- [ ] Training loop in Python
- [ ] Evaluation scripts

## File Structure

```
nexus/
├── Cargo.toml
├── src/
│   ├── lib.rs           # Main library
│   ├── tensor.rs        # Tensor operations
│   ├── attention.rs     # Multi-head attention
│   ├── ssm.rs           # State space model
│   ├── memory.rs        # Titans-style memory
│   ├── block.rs         # Hybrid block
│   ├── world_model.rs   # JEPA-style predictor
│   └── symbolic.rs      # Neuro-symbolic interface
├── python/
│   ├── nexus.py         # Python bindings
│   └── train.py         # Training script
├── tests/
│   └── integration.rs
└── docs/
    └── ARCHITECTURE.md
```

## Key Design Decisions

1. **Rust for core:** Performance-critical, memory-safe, good for low-level tensor ops
2. **1:7 ratio:** Proven effective in Jamba, balances efficiency and capability
3. **Surprise metric:** Simple, effective, well-researched (from Titans)
4. **Latent prediction:** JEPA approach avoids token-space complexity
5. **Symbolic verification:** Guarantees correctness where it matters

## References

- [Jamba: Hybrid Transformer-Mamba](https://arxiv.org/abs/2403.19887)
- [Titans: Learning to Memorize at Test Time](https://arxiv.org/abs/2501.00663)
- [JEPA: Joint Embedding Predictive Architecture](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)
- [Neuro-Symbolic AI Survey](https://arxiv.org/html/2501.05435v1)
