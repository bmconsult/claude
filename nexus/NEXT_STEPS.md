# Nexus Development: Next Steps

*Prepared by Ember (Dec 31, 2025)*

After Shakespeare training completes, here's the recommended development roadmap.

## Immediate Next Steps

### 1. Complete Shakespeare Training
```bash
# Training should complete at step 3000 (~04:45 UTC)
# Final model will be at: checkpoints/nexus_bpe/best.bin

# Evaluate final model
cargo run --example evaluate_nexus --release -- \
  --checkpoint checkpoints/nexus_bpe/best.bin \
  --data data/shakespeare_test.txt
```

### 2. TinyStories Training (User's NVIDIA GPU)
```bash
# Download TinyStories dataset
mkdir -p data
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-train.txt -O data/tinystories.txt

# Train with CUDA (on user's local machine)
cargo run --example train_nexus_bpe --release --features cuda -- \
  --data data/tinystories.txt \
  --resume  # Optional: continue from Shakespeare weights
```

### 3. Model Evaluation Suite
```bash
# Perplexity on held-out data
cargo run --example perplexity --release -- \
  --model checkpoints/nexus_bpe/best.bin

# Generate samples
cargo run --example generate --release -- \
  --model checkpoints/nexus_bpe/best.bin \
  --prompt "Once upon a time"
```

## Medium-Term Enhancements

### Phase 1: Architecture Improvements

| Enhancement | Research Doc | Priority |
|-------------|--------------|----------|
| Flash Attention | FLASH_ATTENTION_RESEARCH.md | High |
| YaRN context extension | ADVANCED_OPTIMIZATION_RESEARCH.md | High |
| MoE integration | MOE_RESEARCH.md | Medium |
| Speculative decoding | SPECULATIVE_DECODING_RESEARCH.md | Medium |

**Suggested order:**
1. Flash Attention (memory efficiency)
2. YaRN (longer context)
3. MoE (if scaling up)
4. Speculative decoding (inference speed)

### Phase 2: Training Enhancements

| Enhancement | Research Doc | Priority |
|-------------|--------------|----------|
| GRPO alignment | REWARD_ALIGNMENT_RESEARCH.md | High |
| Synthetic data | DATA_TRAINING_RESEARCH.md | High |
| Distillation | DISTILLATION_RESEARCH.md | Medium |
| Constitutional AI | CONSTITUTIONAL_AI_RESEARCH.md | Medium |

### Phase 3: Deployment

| Enhancement | Research Doc | Priority |
|-------------|--------------|----------|
| INT4 quantization | INFERENCE_DEPLOYMENT_RESEARCH.md | High |
| GGUF export | INFERENCE_DEPLOYMENT_RESEARCH.md | High |
| SGLang serving | INFERENCE_DEPLOYMENT_RESEARCH.md | Medium |

## Quick Reference Commands

### Training
```bash
# Resume training
cargo run --example train_nexus_bpe --release -- --resume

# With CUDA (user's GPU)
cargo run --example train_nexus_bpe --release --features cuda

# With Metal (Apple Silicon)
cargo run --example train_nexus_bpe --release --features metal
```

### Checkpoints
```bash
# List checkpoints
ls -la checkpoints/nexus_bpe/

# Best model
cat checkpoints/nexus_bpe/best.bin | head -c 100  # Binary, don't actually run

# Load specific step
cargo run --example load_checkpoint --release -- --step 3000
```

### Monitoring
```bash
# Watch training log
tail -f training_output.log

# Check GPU usage (NVIDIA)
nvidia-smi -l 1

# Memory usage
free -h
```

## Research Summary

| Topic | Document | Key Insight |
|-------|----------|-------------|
| **Architecture** | ARCHITECTURE_DEEP_DIVE.md | Hybrid 1:7 attention/SSM ratio |
| **MoE** | MOE_RESEARCH.md | MoE-Mamba 2.35x faster training |
| **Flash Attention** | FLASH_ATTENTION_RESEARCH.md | 75% H100 utilization |
| **Speculative** | SPECULATIVE_DECODING_RESEARCH.md | EAGLE 3-6.5x speedup |
| **Alignment** | CONSTITUTIONAL_AI_RESEARCH.md | Pareto improvement possible |
| **Distillation** | DISTILLATION_RESEARCH.md | MOHAWK <1% data for SSM |
| **Inference** | INFERENCE_DEPLOYMENT_RESEARCH.md | SGLang 6.4x throughput |
| **Optimization** | ADVANCED_OPTIMIZATION_RESEARCH.md | MCTS +17% vs o1-mini |
| **Reward** | REWARD_ALIGNMENT_RESEARCH.md | GRPO 50% compute savings |
| **Data** | DATA_TRAINING_RESEARCH.md | LoRA essential for continual |

## Current Model Configuration

```json
{
  "d_model": 256,
  "n_heads": 8,
  "kv_heads": 2,
  "n_layers": 6,
  "seq_len": 128,
  "vocab_size": 1000,
  "parameters": "7.12M"
}
```

## Scaling Recommendations

### To 70M Parameters
```json
{
  "d_model": 512,
  "n_heads": 16,
  "kv_heads": 4,
  "n_layers": 12,
  "seq_len": 512,
  "vocab_size": 8000
}
```

### To 700M Parameters
```json
{
  "d_model": 1024,
  "n_heads": 32,
  "kv_heads": 8,
  "n_layers": 24,
  "seq_len": 2048,
  "vocab_size": 32000
}
```

## Key Insights from Training

### What Worked Well
- BPE tokenization (2.32x compression)
- Hybrid attention/SSM architecture
- Gradient accumulation (effective batch 16)
- LR warmup + cosine decay
- Checkpointing every 100 steps

### Metrics Trajectory
| Step | Val PPL | Status |
|------|---------|--------|
| 0 | ~500 | Start |
| 1000 | 234 | 33% |
| 2000 | ~175 | 67% |
| 2500 | 178 | 83% |
| 3000 | ~165 (est) | 100% |

### Training Speed
- ~56 tokens/second on cloud CPU
- Expected ~500+ tok/s on user's NVIDIA GPU

## File Structure
```
nexus/
├── src/                      # Core library
│   ├── attention.rs          # Multi-head attention
│   ├── ssm.rs                # Selective SSM
│   ├── block.rs              # Hybrid blocks
│   ├── autograd.rs           # Autodiff system
│   ├── dpo.rs                # DPO/alignment
│   └── ...
├── examples/
│   ├── train_nexus_bpe.rs    # Main training script
│   └── ...
├── data/
│   ├── shakespeare.txt       # Training data
│   └── tokenizer.bpe         # BPE tokenizer
├── checkpoints/
│   └── nexus_bpe/            # Model checkpoints
├── *.md                      # Research docs
└── Cargo.toml
```

## Questions for User

1. **After Shakespeare**: Proceed to TinyStories or focus on architecture improvements?
2. **Scaling target**: Stay at 7M or scale to 70M/700M?
3. **Alignment priority**: When to integrate DPO/GRPO?
4. **Deployment target**: Local inference or served API?

## Handoff Notes

For future instances continuing this work:

1. **Read ARCHITECTURE_DEEP_DIVE.md first** - contains synthesis of all research
2. **Check TRAINING_PROGRESS.md** - has step-by-step metrics
3. **Training may still be running** - check with `ps aux | grep train`
4. **User has local NVIDIA GPU** - can use `--features cuda`
5. **11 research documents** - don't re-research covered topics
