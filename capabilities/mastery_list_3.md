# AI Mastery List 3.0: Deep Techniques & Architecture Patterns
*December 2025 - Expert-Level Knowledge Base*

---

## I. ADVANCED RAG ARCHITECTURE

### A. Query Transformation Techniques

**HyDE (Hypothetical Document Embeddings)**
- Generate synthetic answer document before retrieval
- Embed hypothetical answer instead of raw query
- Bridges query-document semantic asymmetry (short queries vs long docs)
- **HyPE variant**: Pre-compute hypothetical prompts at indexing time → zero runtime LLM overhead

**Query Expansion & Rewriting**
- LLM rewrites vague queries into precise, terminology-matched versions
- Multi-query generation: Break complex query into sub-queries
- Fusion Retrieval (RRF): Combine keyword (BM25) + vector results via Reciprocal Rank Fusion

**RAG Decider Pattern**
- Route queries to appropriate data sources
- Determine when retrieval is necessary vs LLM can answer independently
- Conserves resources on queries that don't need external context

### B. Hierarchical & Structured Retrieval

**RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)**
- Build hierarchical tree structure over documents
- Abstractive summarization at each level
- Enables multi-resolution context: detailed → general
- Maintains context at multiple levels of abstraction

**GraphRAG (Microsoft)**
- Extract entities, relationships, claims into knowledge graph
- Leiden algorithm for hierarchical community clustering
- Generates community summaries bottom-up
- **Performance**: 26-97% fewer tokens, 86.31% on RobustQA benchmark
- Traverses relationship paths for multi-hop reasoning

**Parent Document Retrieval**
- Index small chunks for precision retrieval
- Return parent documents for context completeness
- Structure-aware chunking preserves document organization

### C. Self-Correcting RAG

**Corrective RAG (CRAG)**
- Lightweight evaluator scores retrieved document relevance
- Decision points: use documents, ignore, or seek additional info
- Falls back to web search if internal knowledge insufficient
- **Threshold-based**: Only use retrieval when confidence ≥ threshold

**Self-RAG**
- Reflection tokens for self-evaluation during generation
- Assesses factual accuracy, relevance, usability of outputs
- Multi-step: retrieval decision → document retrieval → relevance evaluation → response generation → support assessment → utility evaluation

**FLARE (Flexible Retrieval Triggering)**
- LLM proactively decides when to retrieve mid-generation
- Triggers retrieval only when uncertainty detected
- Reduces unnecessary retrieval overhead

### D. Agentic RAG
- Dynamic strategy selection per query
- Multi-tool orchestration: navigate info landscapes
- Query reformulation, document parsing, reranking chains
- Higher token usage and latency for multi-step reasoning
- Requires larger context windows for memory across steps

---

## II. INFERENCE OPTIMIZATION DEEP DIVE

### A. Attention Mechanism Variants

| Mechanism | KV Heads | Query Heads | KV Cache Size | Use Case |
|-----------|----------|-------------|---------------|----------|
| **MHA** | H | H | Full | Maximum quality |
| **GQA** | G | H | H/G × base | Balance quality/efficiency |
| **MQA** | 1 | H | 1/H × base | Maximum memory efficiency |

**Multi-Head Attention (MHA)**
- Original design: Independent K,V per head
- Maximum representational capacity
- Highest memory bandwidth requirement

**Grouped-Query Attention (GQA)**
- Groups of query heads share K,V
- Tunable parameter G between 1 and H
- LLaMA 2 70B, Mistral 7B use this
- 4:1 ratio (8 KV heads for 32 query heads) common

**Multi-Query Attention (MQA)**
- All query heads share single K,V
- Up to 12x inference speedup
- May reduce model capacity / training stability

**Sliding Window Attention (SWA)**
- Limits attention to local window
- Reduces O(n²) complexity
- Introduces locality bias
- Often combined with global attention tokens (Longformer)

**Multi-Head Latent Attention (MLA)** - DeepSeek
- Low-rank K,V representations
- Optimizes inference with smaller KV cache
- Surpasses MHA with reduced memory footprint

### B. FlashAttention Deep Dive

**Core Innovation**
- IO-aware algorithm minimizing memory reads/writes
- Tiling strategy keeps submatrices in on-chip SRAM
- Incremental softmax computation (online softmax)
- **Result**: O(Nd) memory IO vs O(N²) standard

**FlashAttention-2/3 Improvements**
- Better parallelization across GPU SMs
- Improved work partitioning
- Native support for causal masking

**FlexAttention**
- Custom masking and indexing logic
- Near-FlashAttention speed on non-contiguous layouts
- PyTorch 2.x native integration

### C. KV Cache Optimization

**PagedAttention (vLLM)**
- OS-inspired paged memory management
- Fixed-size blocks for KV cache
- Block table for non-contiguous allocation
- Eliminates memory fragmentation
- Enables larger batch sizes

**Memory Fragmentation Types**
1. **Internal**: Over-allocation for unknown output length
2. **Reservation Waste**: Memory reserved for future tokens
3. **External**: Gaps from different sequence lengths

**Compression Techniques**
- **Quantization**: INT8/INT4 for KV pairs
- **Sparsity**: Evict less important tokens based on attention scores
- **MorphKV**: Adaptive method maintaining fixed-size cache
- **Cascading KV Cache**: Hierarchical sub-caches, 6.8x prefill latency reduction

**KVPress Library**: 20+ compression methods, research benchmark toolkit

### D. Speculative Decoding Mastery

**Core Mechanism**
- Draft model proposes γ tokens (speculation lookahead)
- Target model verifies in parallel
- Accept matching tokens, reject divergent ones
- **Lossless**: Final output matches target-only generation

**Key Metrics**
- **Acceptance rate (α)**: Probability of draft token acceptance
- **Acceptance length (τ)**: Average tokens accepted per round
- At α ≥ 0.6 and γ ≥ 5: 2-3× speedups achievable

**Advanced Variants**
- **EAGLE**: Extrapolate hidden representations, use target LM head
- **EAGLE-3**: Additional 7.7% speedup via Group Tree Optimization
- **Suffix Decoding**: Pattern-match using frequency counts
- **N-gram Prompting**: Use prompt tokens as speculation source
- **Lookahead Decoding**: Break sequential dependency
- **Medusa**: Multiple decoding heads for parallel proposals
- **HiSpec**: Hierarchical with early-exit intermediate verification

**DISCO (Dynamic Speculation Lookahead)**
- Classifier estimates next token acceptance likelihood
- Dynamically adjusts speculation length per iteration
- 10.3% speedup vs optimal static, 31.4% vs dynamic heuristic

### E. Continuous Batching

**Mechanism**
- Merge new requests mid-generation
- Don't wait for batch completion
- 3.5× throughput increase demonstrated

**Benefits**
- Better GPU utilization
- Lower average latency
- Higher throughput at scale

---

## III. QUANTIZATION MASTERY

### A. Format Comparison

| Format | Target | Key Feature | Best For |
|--------|--------|-------------|----------|
| **GGUF** | CPU + GPU hybrid | Single-file format, layer offloading | Consumer hardware |
| **GPTQ** | GPU | Post-training, calibration-based | Pure GPU inference |
| **AWQ** | GPU | Activation-aware, no backprop | Fast GPU inference |
| **EXL2** | GPU | Variable bit-depth, speed optimized | Maximum speed |

### B. GGUF Deep Dive
- Developed by llama.cpp team (ggerganov)
- Single .gguf file packages model + metadata
- Flexible GPU layer distribution across mixed hardware
- K-quants: Hybrid schemes (Q4_K_M, Q6_K, etc.)

**Common Variants**
- **Q4_K_M**: Balanced 4-bit, recommended for 7B on 24GB
- **Q4_K_S**: Smaller, slightly lower quality
- **Q5_K_M**: Higher quality 5-bit
- **Q6_K**: Near-FP16 quality
- **Q8_0**: 8-bit, minimal quality loss

### C. GPTQ Specifics
- One-shot weight quantization
- Uses calibration dataset (1000 samples typical)
- Approximate second-order information (Hessian)
- 5× faster than GGUF when purely on GPU
- Supports 2/3/4/8-bit levels

### D. AWQ (Activation-aware Weight Quantization)
- Identifies salient weights via activation observation
- Skips most important weights during quantization
- No backpropagation required
- Often faster than GPTQ with better preservation

### E. EXL2
- Variable bit-depth across layers
- Target arbitrary bits per weight (e.g., 4.65bpw)
- Iterative calibration and bit allocation
- **Speed**: 147% more tokens/s than load_in_4bit
- Lower perplexity at same model size vs GPTQ

### F. BitNet & Extreme Quantization
- 1.58-bit quantization research
- Ternary weights: {-1, 0, +1}
- Massive compression potential
- Still maturing for production use

**Hardware Recommendations**
| VRAM | Recommended Format |
|------|-------------------|
| ≤8GB | GGUF with CPU offload (Q4_K_M for 7B) |
| 12-16GB | GPTQ or AWQ, EXL2 for tunable size |
| 24GB+ | Any format, EXL2 for max quality control |

---

## IV. REASONING & TEST-TIME COMPUTE

### A. Chain-of-Thought (CoT) Evolution

**Zero-Shot CoT**
- "Let's think step by step"
- No examples required
- 2022 breakthrough (Kojima et al.)

**Few-Shot CoT**
- Provide reasoning examples
- Model mimics reasoning patterns
- Higher accuracy on complex problems

**Self-Consistency**
- Generate multiple reasoning paths
- Select most consistent answer via majority voting
- Reduces single-path reasoning errors

### B. Test-Time Compute Scaling

**Core Insight**
- More compute at inference → better results
- Trade latency for accuracy
- o1/o3 models: trained to "think longer"

**Scaling Approaches**
1. **Longer chains**: Extended reasoning tokens
2. **Multiple samples**: Best-of-N sampling
3. **Search**: Beam search, tree search
4. **Verification**: Process reward models (PRMs)

**DeepSeek-R1 Training**
- GRPO (Group Relative Policy Optimization)
- Indirect RL rewards for CoT behavior
- Model discovers optimal reasoning patterns
- Cold-start fine-tuning on high-quality CoT examples

### C. Reward Models

**Outcome Reward Models (ORM)**
- Judge final answer only
- Simpler to train
- May miss reasoning flaws

**Process Reward Models (PRM)**
- Score each reasoning step
- Better for detecting logical errors
- "Let's Verify Step by Step" (Lightman et al.)
- Significantly outperforms outcome supervision

### D. Tree-of-Thoughts (ToT)
- Explore multiple reasoning branches
- Backtrack on dead ends
- Evaluate intermediate states
- Best for problems requiring exploration

### E. Advanced Techniques

**Monte Carlo Tree Search (MCTS)**
- Simulation-based exploration
- Balance exploitation vs exploration
- Used in o1-like reasoning speculation

**Self-Reflection**
- Model critiques own outputs
- Identifies flaws, generates improvements
- Iterative refinement loop

**Chain-of-Associated-Thoughts**
- Link related concepts during reasoning
- Build associative memory during generation

---

## V. FINE-TUNING ARCHITECTURE

### A. LoRA Family Deep Dive

**LoRA Core Principles**
- Freeze base weights W
- Add low-rank decomposition: ΔW = BA
- Train only small A (down) and B (up) matrices
- Merge adapters for zero inference overhead

**Key Hyperparameters**
- **Rank (r)**: 4-64 typical, higher = more capacity
- **Alpha (α)**: Scaling factor, often 2× rank
- **Target modules**: q_proj, k_proj, v_proj, o_proj, mlp

**QLoRA**
- 4-bit quantized base model (NF4)
- LoRA adapters on frozen quantized weights
- 70B on 48GB, 8B on 6-8GB

**DoRA (Weight-Decomposed Low-Rank Adaptation)**
- Decompose weights into magnitude + direction
- LoRA updates direction component only
- Enhances learning capacity and stability
- +3.7 accuracy on Llama 7B vs LoRA
- QDoRA: Combines QLoRA efficiency with DoRA quality

**AdaLoRA**
- Adaptive rank allocation per layer
- SVD-based importance scoring
- Prune less important singular values
- Higher ranks for critical layers

**RS-LoRA (Rank-Stabilized)**
- Stabilized training dynamics
- Better convergence at higher ranks

**GateRA** (2025)
- Token-aware modulation
- Dynamic adaptation strength per token
- Suppresses updates for in-distribution tokens
- Amplifies for out-of-distribution uncertainty

### B. Advanced PEFT Techniques

**Prefix Tuning**
- Prepend trainable continuous prompts
- Virtual tokens in attention computation

**P-Tuning v2**
- Trainable prompts at every layer
- More expressive than prefix tuning

**Adapter Tuning**
- Small modules between layers
- H-Adapter, P-Adapter variants

**BitFit**
- Only train bias terms
- Minimal parameters, surprisingly effective

### C. Full Fine-Tuning Optimization

**Unsloth**
- Custom Triton kernels: 2-5× faster, 80% less VRAM
- 9B on 24GB (LoRA 16-bit)
- 9B on 6.5GB (QLoRA 4-bit)
- 70B fine-tuning on consumer GPUs

**Axolotl**
- YAML-driven configuration
- Supports full, LoRA, QLoRA
- Multi-GPU via FSDP/DeepSpeed
- Sequence parallelism via Ring FlashAttention

**Torchtune**
- PyTorch-native, lean design
- Memory-efficient recipes for 24GB
- Deep customization, multi-node scaling

---

## VI. CONTEXT ENGINEERING

### A. Context Window Optimization

**Current State (2025)**
- Gemini: 1M tokens, Claude: 200K, GPT: 128K
- Trend: ~30× growth per year since mid-2023
- Effectiveness growing faster than window size

**Performance Degradation**
- NoLiMa: Performance degrades with context length
- "Lost in the Middle" effect
- Quality vs quantity tradeoff

### B. Context Management Strategies

**Observation Masking**
- Hide older, less important info
- Tune masking window per agent
- No additional inference cost

**LLM Summarization**
- Compress history into summaries
- Preserve critical information
- Additional inference overhead

**Hybrid Approach**
- Combine masking + summarization
- 7% cost reduction vs pure masking
- 11% vs pure summarization

**Cascading KV Cache**
- Hierarchical sub-caches
- Retain critical tokens longer
- 12.13% improvement on LongBench
- 6.8× prefill latency reduction

### C. Long Context Techniques

**YaRN**
- RoPE scaling for longer contexts
- May reduce short-task accuracy
- Used in QwQ for 128K context

**LongRoPE/LongRoPE2**
- PPL-guided evolutionary search
- Optimized scaling factors
- Strong RULER and Needle-in-a-Haystack performance

**Infinite Retrieval**
- Sliding window with retrieval
- Process overlapping chunks
- Retain critical info without full storage

---

## VII. PROMPT ENGINEERING MASTERY

### A. Meta-Prompting

**Core Concept**
- Use LLMs to generate/improve prompts
- Prompts create other prompts
- Structure over content focus

**Automatic Prompt Engineer (APE)**
- Treat prompt as "program"
- Generate candidate pool
- Score and evaluate effectiveness
- Monte Carlo search for optimization

**Conversational Prompt Engineering (CPE)**
- Interactive prompt refinement via chat
- Data-driven questions about preferences
- Iterative optimization

**PromptAgent**
- Prompt generation as planning problem
- Leverage SME knowledge
- Tree-structure refinement

### B. Advanced Techniques

**Self-Consistency Prompting**
- Multiple reasoning paths
- Majority voting for answer
- 10-40% improvement on math/logic

**Role Prompting**
- Assign expert persona
- Channels domain-specific knowledge
- "Act as a Harvard economics professor..."

**Constraint-Based Design**
- Explicit output requirements
- Format specifications
- Negative constraints ("never mention X")

**Prompt Chaining**
- Break complex tasks into steps
- Each output feeds next prompt
- Enables multi-stage reasoning

### C. Production Prompt Engineering

**Version Control**
- Track prompt iterations
- A/B testing results
- Performance metrics per version

**Systematic Testing**
- Test sets for edge cases
- Automated evaluation
- Regression testing

**Context Engineering**
- "Fill context with just the right information"
- Directory-level rules (CLAUDE.md)
- Selective MCP server loading

---

## VIII. SYNTHETIC DATA & DISTILLATION

### A. Data Generation Methods

**Distillation**
- Large teacher → small student
- Transfer knowledge via generated examples
- 405B → 8B patterns

**Evol-Instruct**
- Iteratively evolve prompts
- Increase complexity systematically
- Cover edge cases

**Self-Improvement**
- Model generates from own outputs
- Iterative refinement
- Limited by model's own capabilities

### B. Quality Assurance

**Critic Systems**
- AI evaluates generated data quality
- Filter low-quality samples
- Multi-stage validation

**Human-in-the-Loop**
- Curate seed examples
- Post-generation review
- Bias detection

**Synthetic Data Pitfalls**
- Bias amplification
- Verbatim regeneration (copyright)
- Distribution shift
- Model collapse risk

### C. Knowledge Distillation

**Task-Specific Alignment**
- Match student to teacher on target tasks
- Domain-focused training data

**Rationale-Based Training**
- Include reasoning chains
- Student learns process, not just answers

**Multi-Teacher Frameworks**
- Multiple teachers for diversity
- Ensemble knowledge transfer

### D. Dataset Distillation

**Gradient Matching**
- Synthetic data produces similar gradients
- Optimize data, not model

**Distribution Matching**
- Align synthetic and real distributions
- Maximum Mean Discrepancy metrics

**Trajectory Matching**
- Match training dynamics
- Robust over longer training

---

## IX. EMBEDDING & RETRIEVAL MASTERY

### A. Embedding Model Selection

**Top Performers 2025**
| Model | Dimensions | Context | Cost | Key Feature |
|-------|------------|---------|------|-------------|
| voyage-3.5-large | 2048 | 32K | $0.06/M | MRL, benchmark leader |
| voyage-3.5-lite | 512 | 32K | $0.02/M | Near-large performance |
| gemini-embedding-001 | 3072 | 8K | FREE | Google AI Studio |
| nomic-embed-text-v2 | 768 | 8K | Free | MoE architecture, Apache-2.0 |
| BGE-M3 | 1024 | 8K | Free | Dense + sparse + ColBERT |

**Matryoshka Representation Learning (MRL)**
- Truncate dimensions without retraining
- 2048 → 256 with graceful degradation
- Enables flexible accuracy/cost tradeoff

### B. Reranking Strategies

**Cross-Encoder Rerankers**
- Full attention between query and document
- More accurate than bi-encoders
- Higher latency

**Top Rerankers**
- **voyage-3-large**: "In league of its own" (DataStax)
- **Cohere Rerank 3**: 100+ languages, Nimble variant
- **jina-reranker-v2**: 15× faster than v1, function-calling aware
- **mxbai-rerank-v2**: SOTA on BEIR, 100+ languages

**FlashRank**
- ONNX-optimized, CPU-friendly
- Minimal overhead, substantial gains
- Great for resource-constrained deployments

**Unified API (rerankers library)**
```python
from rerankers import Reranker
ranker = Reranker("cohere", api_key=KEY)
results = ranker.rank(query, documents)
```

### C. Hybrid Search

**Reciprocal Rank Fusion (RRF)**
- Combine BM25 + vector scores
- Different scoring systems → unified ranking
- No tuning required

**Dense + Sparse + Multi-vector**
- BGE-M3 supports all three
- Dense: Semantic similarity
- Sparse: BM25-like keyword matching
- Multi-vector: ColBERT-style token matching

---

## X. ARCHITECTURE PATTERNS

### A. Mixture of Experts (MoE)

**Core Design**
- Multiple expert networks per layer
- Router selects k experts per token
- Massive total params, small activated params

**Examples**
- DeepSeek-R1: 671B total, 37B activated
- Qwen3-Coder-480B: 480B total, 35B activated
- GPT-5 Maverick: 400B total, 17B activated

**Benefits**
- Scale capacity without proportional compute
- Specialization per expert
- Efficient inference

### B. Modern Positional Encodings

**RoPE (Rotary Position Embeddings)**
- Rotation-based relative positions
- Extrapolates to longer sequences
- Standard in LLaMA, Qwen, Mistral

**ALiBi (Attention with Linear Biases)**
- Linear bias based on distance
- Good length generalization
- Used in BLOOM, MPT

### C. Activation Functions

**SwiGLU**
- Swish × Gated Linear Unit
- Standard in modern LLMs
- Better training dynamics than ReLU

**GEGLU**
- GELU × Gated Linear Unit
- Alternative to SwiGLU

### D. Normalization

**RMSNorm**
- Root Mean Square normalization
- Faster than LayerNorm
- Equivalent effectiveness

**Pre-LayerNorm**
- Normalize before attention/FFN
- More stable training
- Standard in modern transformers

---

## XI. EVALUATION FRAMEWORKS

### A. RAG-Specific Metrics (RAGAS)

| Metric | Measures | Range |
|--------|----------|-------|
| Faithfulness | Output matches context | 0-1 |
| Answer Relevancy | Response addresses query | 0-1 |
| Context Precision | Retrieved context quality | 0-1 |
| Context Recall | Coverage of ground truth | 0-1 |
| Contextual Relevancy | Context relevance to query | 0-1 |

### B. DeepEval Capabilities
- 30+ research-backed metrics
- End-to-end and component evaluation
- Synthetic dataset generation
- CI/CD integration via pytest
- Free for local execution

### C. LLM-as-Judge

**Advantages**
- Scalable evaluation
- Nuanced quality assessment
- Cost-effective vs human review

**Challenges**
- Position bias
- Verbosity bias
- Self-preference
- Requires calibration

---

## XII. PRODUCTION PATTERNS

### A. Serving Architecture

**Disaggregated Serving (NVIDIA Dynamo)**
- Separate prefill (compute-bound) and decode (memory-bound)
- Different GPU allocation per phase
- Framework-agnostic KV Cache Manager

**Prefix Caching**
- RadixAttention: Automatic KV cache reuse
- 5× throughput on agent workloads
- Zero-overhead in SGLang

### B. Cost Optimization

| Strategy | Mechanism | Savings |
|----------|-----------|---------|
| Input caching | Reuse prompt KV cache | 75-90% |
| Quantization | 4-bit inference | 4× memory |
| Speculative | Draft model + verify | 2-3× speed |
| Batching | Continuous batching | 3.5× throughput |

### C. Observability

**Tracing**
- LangSmith, Phoenix, TruLens
- Request-level metrics
- Token consumption tracking

**Evaluation Pipeline**
- Automated quality checks
- Regression detection
- A/B testing infrastructure

---

## XIII. QUICK REFERENCE

### Installation Commands

```bash
# Inference engines
pip install sglang vllm

# Structured output
pip install instructor outlines pydantic-ai

# Fine-tuning
pip install unsloth peft trl

# Evaluation
pip install deepeval ragas

# Embeddings & reranking
pip install rerankers flashrank

# Browser automation
npx @playwright/mcp@latest
```

### Decision Trees

**Inference Engine Selection**
```
GPU available?
├── Yes → Multiple GPUs?
│   ├── Yes → SGLang (fastest) or vLLM (mature)
│   └── No → vLLM or Ollama
└── No → llama.cpp or Ollama (CPU mode)
```

**Quantization Selection**
```
Primary hardware?
├── CPU/Apple → GGUF (Q4_K_M for 7B)
├── GPU ≤16GB → GPTQ or AWQ
├── GPU 24GB+ → EXL2 (tunable quality)
└── Mixed → GGUF with layer offloading
```

**Fine-tuning Approach**
```
Resources?
├── Consumer GPU → Unsloth + QLoRA
├── A100/H100 → Full fine-tuning or Axolotl
├── Need portability → LoRA/DoRA adapters
└── Quick experiments → QLoRA + PEFT
```

---

*This mastery list represents expert-level knowledge as of December 2025. The AI landscape evolves rapidly—verify current state of specific tools before production deployment.*
