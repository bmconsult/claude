# Nexus

**Hybrid Intelligence Architecture** - A next-generation neural architecture combining the best of transformers, state-space models, and test-time learning.

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Tests](https://img.shields.io/badge/tests-36%20passed-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## Overview

Nexus synthesizes insights from recent AI research breakthroughs:

| Component | Based On | Innovation |
|-----------|----------|------------|
| **Hybrid Core** | Jamba (AI21) | 1:7 Attention:SSM ratio for efficiency |
| **Test-Time Memory** | Titans (Google) | Memory that learns during inference |
| **World Model** | JEPA (Meta) | Predict in latent space, not token space |
| **Reasoning** | Neuro-symbolic | Formal logic + neural representations |

## Architecture

```
Input → [Embed] → [Hybrid Blocks × N] → [Memory] → [World Model] → Output
                         ↓
           ┌─────────────┴─────────────┐
           │                           │
    [Attention Layer]           [SSM Layer × 7]
     (1 per block)             (7 per block)
```

### Key Features

- **O(n) Memory Scaling** - SSM layers process sequences in linear time
- **Test-Time Learning** - Memory updates during inference using "surprise" metric
- **Latent Prediction** - JEPA-style world model predicts representations, not tokens
- **Neuro-Symbolic Reasoning** - Integrates formal logic with neural networks

## Installation

### From Source

```bash
git clone https://github.com/your-org/nexus
cd nexus
cargo build --release
```

### Python Bindings

```bash
pip install maturin
maturin develop --release
```

## Quick Start

### Rust

```rust
use nexus::{Nexus, NexusConfig, Tensor};

// Create model
let config = NexusConfig {
    d_model: 512,
    n_heads: 8,
    layers_per_block: 4,
    n_blocks: 6,
    ..Default::default()
};

let mut model = Nexus::new(config);

// Forward pass with memory updates
let input = Tensor::randn(1, 128, 512);
let output = model.forward(&input, true);

// Check memory statistics
let stats = model.memory.stats();
println!("Memory entries: {}/{}", stats.num_entries, stats.capacity);
```

### Python

```python
from nexus import Nexus, NexusConfig

# Create model
config = NexusConfig(d_model=512, n_heads=8, n_blocks=6)
model = Nexus(config)

# Forward pass
import numpy as np
x = np.random.randn(1, 128, 512).astype(np.float32)
output = model.forward(x, update_memory=True)

print(f"Output shape: {output.shape}")
```

## Training

### Using the Training Binary

```bash
cargo run --release --bin nexus-train -- \
    --config config.json \
    --data training_data/ \
    --output checkpoints/
```

### Using the Python API

```python
from nexus import Nexus, NexusConfig, Trainer, TrainConfig

# Configure
model_config = NexusConfig.base()  # 512d, 8 heads, 6 blocks
train_config = TrainConfig(
    lr=1e-4,
    batch_size=32,
    epochs=100,
    warmup_steps=1000
)

# Train
model = Nexus(model_config)
trainer = Trainer(model_config, train_config, checkpoint_dir="./checkpoints")
trainer.train(model, train_data)
```

## Model Presets

| Preset | d_model | Heads | Blocks | Parameters |
|--------|---------|-------|--------|------------|
| `tiny` | 128 | 4 | 2 | ~2M |
| `small` | 256 | 4 | 4 | ~8M |
| `base` | 512 | 8 | 6 | ~50M |
| `large` | 1024 | 16 | 12 | ~350M |
| `xl` | 2048 | 32 | 24 | ~1.3B |

```python
config = NexusConfig.base()  # or .tiny(), .small(), .large(), .xl()
```

## Inference

```bash
cargo run --release --bin nexus-infer -- \
    --model checkpoint.json \
    --input "Your input text here"
```

## Benchmarks

Run benchmarks with:

```bash
cargo bench
```

## Project Structure

```
nexus/
├── src/
│   ├── lib.rs           # Core library exports
│   ├── tensor.rs        # Tensor operations
│   ├── attention.rs     # Multi-head attention with RoPE
│   ├── ssm.rs           # Selective State Space Model (Mamba)
│   ├── memory.rs        # Titans-style test-time memory
│   ├── block.rs         # Hybrid attention/SSM blocks
│   ├── world_model.rs   # JEPA-style latent predictor
│   ├── symbolic.rs      # Neuro-symbolic reasoning
│   ├── autograd.rs      # Automatic differentiation
│   ├── training.rs      # Training infrastructure
│   ├── python.rs        # Python bindings (PyO3)
│   ├── main.rs          # Demo binary
│   └── bin/
│       ├── train.rs     # Training binary
│       └── infer.rs     # Inference binary
├── python/
│   └── nexus/           # Python package
├── scripts/
│   └── train.py         # Python training script
├── benches/             # Benchmarks
└── tests/               # Integration tests
```

## Technical Details

### Hybrid Attention/SSM Block

Following Jamba's insight, Nexus uses a 1:7 ratio of attention to SSM layers:

- **Attention layers** handle global dependencies (every 8th layer)
- **SSM layers** process local patterns efficiently (7 out of 8 layers)

This provides the best of both worlds: global context when needed, linear complexity otherwise.

### Test-Time Memory

Inspired by Titans, the memory module:

1. Computes "surprise" for each input (how unexpected it is)
2. High-surprise inputs are stored in long-term memory
3. Memory is queried during forward pass for relevant context
4. Mini-gradient descent updates memory weights during inference

### JEPA World Model

Instead of predicting tokens directly:

1. **Encoder** maps inputs to latent representations
2. **Predictor** predicts future latent states
3. **VICReg loss** ensures representations are:
   - Invariant (same content → same representation)
   - Variant (different content → different representation)
   - Covariance-regularized (no redundant dimensions)

### Neuro-Symbolic Integration

The symbolic reasoning module:

1. Extracts logical structure from neural representations
2. Applies formal reasoning rules (modus ponens, etc.)
3. Grounds conclusions back in neural space

## Loss Functions

### VICReg Loss

```
L = λ_inv * invariance + λ_var * variance + λ_cov * covariance
```

- **Invariance**: MSE between context and target representations
- **Variance**: Encourages variance in each dimension
- **Covariance**: Decorrelates representation dimensions

### JEPA Masking

Training uses random masking of input sequences:
- Mask ratio: 15% of positions
- Context sees unmasked positions
- Model predicts representations at masked positions

## GPU Acceleration

The current implementation uses CPU-based ndarray. For production GPU acceleration:

### Option 1: Candle (Recommended)

[Candle](https://github.com/huggingface/candle) provides a Rust ML framework with CUDA support:

```toml
# Cargo.toml
[dependencies]
candle-core = { version = "0.8", features = ["cuda"] }
candle-nn = "0.8"
```

Key changes needed:
- Replace `ndarray::Array3<f32>` with `candle_core::Tensor`
- Use `candle_nn` for layer implementations
- SSM selective scan benefits from custom CUDA kernels (like Mamba's)

### Option 2: Burn

[Burn](https://github.com/tracel-ai/burn) is another Rust ML framework:

```toml
[dependencies]
burn = { version = "0.15", features = ["wgpu"] }  # or "cuda"
```

### Performance Notes

| Backend | Attention | SSM | Notes |
|---------|-----------|-----|-------|
| CPU (ndarray) | O(n²) | O(n) | Current implementation |
| CUDA (cuBLAS) | O(n²) | O(n) | ~10-50x faster |
| CUDA + FlashAttention | O(n) | O(n) | Optimal for long sequences |

The 1:7 attention:SSM ratio shows increasing benefits with:
- Longer sequences (SSM's O(n) vs attention's O(n²))
- GPU acceleration (SSM selective scan kernels)
- Memory-bound workloads (SSM uses O(n) memory vs O(n²))

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Run tests: `cargo test`
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

```bibtex
@software{nexus2024,
  title = {Nexus: Hybrid Intelligence Architecture},
  year = {2024},
  url = {https://github.com/your-org/nexus}
}
```

## References

- [Jamba: AI21's Hybrid Transformer-Mamba](https://arxiv.org/abs/2403.19887)
- [Titans: Learning to Memorize at Test Time](https://arxiv.org/abs/2501.00663)
- [JEPA: A Path Towards Autonomous Machine Intelligence](https://openreview.net/pdf?id=BZ5a1r-kVsf)
- [Mamba: Linear-Time Sequence Modeling](https://arxiv.org/abs/2312.00752)
