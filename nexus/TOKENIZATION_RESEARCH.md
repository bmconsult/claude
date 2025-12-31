# Tokenization Research: Beyond BPE

*Synthesized by Ember (Dec 31, 2025)*

## Executive Summary

Tokenization is increasingly being questioned as necessary for LLMs. Recent research shows byte-level models can match tokenized transformer performance while eliminating tokenization's limitations.

## Current Approaches

### BPE (Byte Pair Encoding)
**Status**: Industry standard, used in most production LLMs.

**Nexus current**: 1000 vocab BPE, 2.32x compression on Shakespeare.

**Limitations**:
- Domain/modality sensitivity
- Sensitivity to input noise
- Lack of orthographic knowledge
- Multilingual inequity (under-representation of non-English)
- Morphologically unaware token boundaries

### Unigram
- Probabilistic subword segmentation
- Starts from large vocabulary, prunes down
- More flexible than BPE's greedy merging
- Used in SentencePiece alongside BPE

### SentencePiece
- Language-neutral (handles Chinese without spaces)
- Treats input as raw Unicode stream
- Combines BPE and Unigram under one framework
- Widely used in multilingual models

## Tokenizer-Free Architectures

### Byte Latent Transformer (BLT) - Meta, Dec 2024

**Key Innovation**: Entropy-based dynamic patching

**Architecture**:
```
Bytes → Local Encoder → Latent Transformer → Local Decoder → Bytes
         (patches)        (main model)        (unpatch)
```

**Patching Mechanism**:
1. Train small character-level LLM for entropy estimation
2. Set patch boundaries where next-byte entropy jumps
3. Patches are ~4 bytes on average (dynamic)
4. More compute allocated to complex regions

**Results**:
- First FLOP-controlled scaling to 8B parameters
- Matches tokenized LLM performance
- Improved inference efficiency
- Better robustness to input noise
- Released 1B and 7B models on HuggingFace

**Relevance to Nexus**: Our hybrid SSM architecture could benefit from dynamic patching - SSM layers already have O(n) memory, BLT-style patching could further reduce sequence length.

### MegaByte - Meta, May 2023

**Key Innovation**: Hierarchical fixed-size patching

**Architecture**:
```
Bytes → Patch Embedder → Global Transformer → Local Transformer → Bytes
         (concat bytes)    (between patches)   (within patches)
```

**Components**:
1. Patch embedder: concatenates byte embeddings
2. Global transformer: contextualizes patches via self-attention
3. Local transformer: autoregressively predicts bytes within patch

**Benefits**:
- Sub-quadratic self-attention (O(n) instead of O(n²))
- Larger feedforward layers for same compute
- Parallel generation during decoding
- Scales to 1M+ byte sequences

**Typical Configuration**: P=8 (8 bytes per patch)

### SpaceByte - NeurIPS 2024

**Key Innovation**: Whitespace-based dynamic patching

**Architecture**:
- Standard byte-level transformer with extra global blocks
- Global blocks applied only after space/boundary characters
- Intuition: First character of word is hardest to predict

**Key Finding**: Fixed patch sizes significantly degrade performance vs dynamic.

**Results**:
- Matches tokenized transformer performance for fixed compute
- Byte-level transformers need ~10x more FLOPs to match subword without this

**Evolution**: SpaceByte → BLT (entropy replaces whitespace rule)

### Multiscale Byte Language Model (MBLM) - IBM, Feb 2025

**Key Innovation**: Hybrid Transformer+Mamba for extreme context

**Capabilities**:
- 5M byte context on single GPU in full precision
- Multimodal: same pipeline for text, images, audio
- First BLM evaluation on visual Q&A

**Architecture**:
- Hierarchical with multiple abstraction levels
- Hybrid architectures (Transformer + Mamba)
- Near-linear generational efficiency

**Multimodal Processing**:
- UTF-8 text: raw bytes
- Images: raw pixels OR JPEG bytes
- Audio: raw stream bytes
- No modality-specific preprocessing!

## Comparison Table

| Model | Patching | Scale | Context | Modality |
|-------|----------|-------|---------|----------|
| BLT | Entropy-based | 8B | Standard | Text |
| MegaByte | Fixed (P=8) | - | 1M+ bytes | Text/Image/Audio |
| SpaceByte | Whitespace | - | Standard | Text |
| MBLM | Hierarchical | - | 5M bytes | Multimodal |

## Key Insights

### The Bitter Lesson for Tokenization
"The history of AI has taught us that general methods that leverage computation are ultimately the most effective. Tokenization is a form of human-designed feature engineering that may be replaced by learned representations."

### Why Tokenization Persists
1. Training efficiency (shorter sequences)
2. Existing infrastructure (vocab management)
3. Benchmark performance on standard evals
4. Engineering inertia

### Why Tokenization May Die
1. Robustness to noise/typos (bytes don't care)
2. True multilinguality (no vocab bias)
3. Multimodal unification (everything is bytes)
4. Morphological awareness (learns subword patterns)
5. No preprocessing pipeline complexity

## Integration Roadmap for Nexus

### Short-term: Keep BPE
- Current 1000-vocab BPE working well
- 2.32x compression suitable for Shakespeare
- Expand vocab for TinyStories (8000+)

### Medium-term: Explore SpaceByte-style
- Add "global" attention blocks after boundary bytes
- Leverage existing hybrid architecture
- Could combine with SSM for local processing:
  ```
  Bytes → SSM (local) → Attention (at boundaries) → SSM (local) → Output
  ```

### Long-term: Full BLT Integration
- Train entropy model for patching decisions
- Dynamic patching with our 1:7 SSM/Attention ratio
- Potential architecture:
  ```
  Bytes → Entropy-based Patching → Hybrid SSM/Attention → Unpatch
  ```

### Nexus-Specific Advantages
1. **SSM + Dynamic Patching**: SSM's O(n) already efficient; patches further reduce n
2. **Titans Memory**: Could store entropy patterns for patching decisions
3. **Hybrid 1:7 Ratio**: Natural fit for patch/byte levels

## Implementation Notes

### BLT Code (Meta)
```python
from bytelatent.transformer import LMTransformer
from bytelatent.model.blt import ByteLatentTransformer

entropy_model = LMTransformer.from_pretrained("facebook/blt-entropy")
blt_model = ByteLatentTransformer.from_pretrained("facebook/blt-1b")
```

### SpaceByte (GitHub: kjslag/spacebyte)
- PyTorch implementation
- Multiscale modeling at byte and word levels

### Key Hyperparameters
- Average patch size: 4-8 bytes
- Entropy threshold: task-dependent
- Global block frequency: every patch (BLT) or whitespace (SpaceByte)

## Research Questions

1. **SSM for byte modeling**: Can Mamba's selection mechanism learn optimal patching?
2. **Entropy from SSM state**: Could SSM hidden state indicate prediction difficulty?
3. **Hybrid patching**: Combine whitespace + entropy signals?
4. **Cross-modal patching**: Different patch sizes for text vs code vs data?

## Sources

- [Byte Latent Transformer (BLT)](https://github.com/facebookresearch/blt) - Meta Research
- [MegaByte](https://arxiv.org/abs/2305.07185) - Meta AI
- [SpaceByte](https://arxiv.org/abs/2404.14408) - NeurIPS 2024
- [MBLM](https://arxiv.org/abs/2502.14553) - IBM Research
- [Tokenizer Adaptation](https://arxiv.org/html/2512.03989v1) - Continued BPE training
- [HuggingFace Tokenizers](https://huggingface.co/docs/transformers/en/tokenizer_summary)

## Conclusion

Tokenization is no longer a hard requirement for competitive LLM performance. The field is moving toward:
1. **Dynamic patching** over fixed vocabulary
2. **Entropy-based** decisions over rule-based
3. **Hierarchical** architectures for efficiency
4. **Multimodal unification** through bytes

For Nexus, the hybrid SSM/Attention architecture is well-positioned to adopt byte-level modeling with dynamic patching, leveraging SSM for efficient local processing and sparse attention for patch-level global context.
