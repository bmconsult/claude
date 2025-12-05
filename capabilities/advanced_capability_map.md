# Advanced AI Capability Map 2.0
## Beyond Mainstream: Cutting-Edge Tools for Power Users (December 2025)

---

## 🏗️ AGENT FRAMEWORKS

### Tier 1: Production-Ready

| Framework | Philosophy | Best For | GPU Needed |
|-----------|------------|----------|------------|
| **LangGraph** | Graph-based DAG workflows | Complex stateful workflows, precise control | No |
| **AutoGen** (Microsoft) | Multi-agent conversations | Collaborative coding, async dialogues | No |
| **CrewAI** | Role-based team orchestration | Simulated org structures, rapid dev | No |
| **Semantic Kernel** (MS) | Enterprise .NET integration | Azure ecosystems, SOC2/GDPR compliance | No |

### Tier 2: Specialized

| Framework | Philosophy | Best For |
|-----------|------------|----------|
| **DSPy** (Stanford) | Programmatic prompt optimization | Research, eval-driven iteration, reproducibility |
| **LlamaIndex** | Data indexing + retrieval | RAG-heavy applications, document Q&A |
| **PydanticAI** | Typed Python-first agents | Production Python environments |
| **Smolagents** (HuggingFace) | Minimal code-driven patterns | Lightweight, simple agents |

### Tier 3: Emerging

| Framework | Philosophy | Best For |
|-----------|------------|----------|
| **Google ADK** | Production agent lifecycle | Deep Google Cloud integration |
| **OpenAI Agents SDK** | Native OpenAI tooling | OpenAI-exclusive deployments |
| **MetaGPT** | Domain-specific software automation | Code generation pipelines |
| **Strands Agents** (AWS) | Model-agnostic + AWS integration | AWS-heavy infrastructure |

**Decision Framework:**
- Beginner → CrewAI or LangChain
- Complex workflows → LangGraph
- Multi-agent conversations → AutoGen
- Research/optimization → DSPy
- Enterprise/Azure → Semantic Kernel

---

## ⚡ LLM INFERENCE ENGINES

### Local/Self-Hosted Serving

| Engine | Speed | Memory | Best For |
|--------|-------|--------|----------|
| **SGLang** | 🏆 Fastest | Excellent | Production serving, multi-turn, agents |
| **vLLM** | Very Fast | Good | High-throughput, multi-GPU |
| **LMDeploy** | Fast | Good | Deployment simplicity |
| **Ollama** | Moderate | Easy | Local dev, beginners |
| **llama.cpp** | Moderate | Minimal | CPU inference, edge devices |
| **TensorRT-LLM** | Very Fast | GPU-heavy | NVIDIA enterprise deployments |

**Key Technologies:**
- **PagedAttention** (vLLM): Efficient KV cache management
- **RadixAttention** (SGLang): Cross-query cache reuse, 5x throughput on agents
- **Continuous Batching**: Merge requests mid-generation
- **Speculative Decoding**: Draft-verify for faster generation

**Benchmarks (Llama3-70B, 2xH100):**
```
SGLang: 38 tok/s sequential, 30-31 tok/s concurrent (stable)
vLLM:   35 tok/s sequential, 22→16 tok/s concurrent (degrades)
```

**NVIDIA Dynamo** (GTC 2025): Disaggregated serving framework separating prefill/decode phases across GPUs.

---

## 🎯 STRUCTURED OUTPUT LIBRARIES

### Guaranteed JSON/Schema Output

| Library | Approach | Best For |
|---------|----------|----------|
| **Instructor** | Pydantic + API providers | Fast extraction, 15+ providers |
| **Outlines** | Constrained token generation | Local models, guaranteed structure |
| **PydanticAI** | Agent runtime + structured output | Production agents |
| **Marvin** | Simple syntax, built-in tasks | Quick prototyping |

**Instructor Example:**
```python
import instructor
from pydantic import BaseModel

client = instructor.from_provider("anthropic/claude-sonnet-4-20250514")

class User(BaseModel):
    name: str
    age: int

user = client.chat.completions.create(
    response_model=User,
    messages=[{"role": "user", "content": "John is 25 years old"}]
)
# User(name='John', age=25) - guaranteed valid
```

**Outlines** (for local models): Hooks into token generation, only allows valid tokens. Zero chance of malformed JSON.

---

## 🔬 FINE-TUNING FRAMEWORKS

### The Big Three

| Framework | Speed | Memory | Multi-GPU | Best For |
|-----------|-------|--------|-----------|----------|
| **Unsloth** | 2-5x faster | 80% less | Pro only | Single GPU, resource-constrained |
| **Axolotl** | Standard | Standard | Yes (FSDP/DeepSpeed) | Flexibility, multi-GPU |
| **Torchtune** | Standard+ | Standard | Yes | PyTorch purists, customization |

**Unsloth Magic:**
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-32B",
    load_in_4bit=True,  # 4-bit quantization
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    use_gradient_checkpointing="unsloth",  # 30% less VRAM
)
```

**Also Notable:**
- **LLaMA-Factory**: UI-based, supports DoRA/LongLoRA/LLaMA Pro
- **Hugging Face PEFT**: Standard LoRA/QLoRA implementation
- **TRL** (Transformers RL): RLHF, DPO, PPO training

**Hardware Requirements:**
- 8B model + LoRA: 24GB VRAM (RTX 4090)
- 8B model + QLoRA: 6-8GB VRAM
- 70B model + QLoRA: 48GB+ VRAM (A100)

---

## 📊 EVALUATION FRAMEWORKS

### RAG & LLM Evaluation

| Framework | Focus | Metrics | Cost |
|-----------|-------|---------|------|
| **DeepEval** | Full-stack LLM eval | 30+ metrics, RAG+safety | Free (local) |
| **RAGAS** | RAG-specific | Faithfulness, relevancy, recall | ~$0.01-0.10/eval |
| **TruLens** | Real-time monitoring | Feedback functions, hallucination | Free |
| **LangSmith** | Observability + eval | Tracing, annotation queues | Freemium |
| **Phoenix** (Arize) | LLM observability | Clustering, embedding analysis | Free |

**DeepEval Example:**
```python
from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is the refund policy?",
    actual_output="30-day full refund available.",
    retrieval_context=["All customers eligible for 30-day refund."]
)

metric = FaithfulnessMetric(threshold=0.7)
evaluate([test_case], [metric])
```

**Key Metrics:**
- **Faithfulness**: Does output match retrieved context?
- **Answer Relevancy**: Is answer relevant to query?
- **Context Precision**: How relevant is retrieved context?
- **Hallucination Score**: Detecting fabricated content

---

## 🔍 EMBEDDING MODELS

### Top Performers (2025)

| Model | Dimensions | Context | Multilingual | Cost |
|-------|------------|---------|--------------|------|
| **voyage-3.5-large** | 2048 | 32K | 26 langs | $0.06/M tokens |
| **voyage-3.5-lite** | 512 | 32K | 26 langs | $0.02/M tokens |
| **text-embedding-3-large** | 3072 | 8K | Yes | $0.13/M tokens |
| **gemini-embedding-001** | 3072 | 8K | 100+ langs | **FREE** |
| **nomic-embed-text-v2** | 768 | 8K | 100 langs | Open source |
| **BGE-M3** | 1024 | 8K | 100+ langs | Open source |

**Open Source Leaders:**
- **nomic-embed-text**: 8K context, Apache-2.0, beats Ada-002
- **mxbai-embed-large**: State-of-the-art for Ollama users
- **ModernBERT-Embed**: RoPE + alternating attention, 768d

**Specialized:**
- **VoyageCode3**: Best for code retrieval
- **jina-code-v2**: Code similarity tasks
- **nomic-embed-code**: Code-specific SOTA

**Local (Ollama):**
```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

---

## 🎯 RERANKERS

### Cross-Encoder Reranking

| Model | Size | Speed | Languages | Best For |
|-------|------|-------|-----------|----------|
| **voyage-3-large** | - | Fast | Multi | Highest accuracy |
| **Cohere Rerank 3** | - | Fast | 100+ | Production API |
| **jina-reranker-v2** | 278M | 15x faster | 100+ | Agentic RAG, code |
| **mxbai-rerank-v2** | 0.5-1.5B | Fast | 100+ | Open source SOTA |
| **bge-reranker-v2-m3** | 567M | Moderate | Multi | Balanced performance |

**FlashRank**: Lightweight, CPU-friendly, ONNX-optimized

**Unified API (rerankers library):**
```python
from rerankers import Reranker

# Switch between any reranker with same API
ranker = Reranker("cohere", api_key=KEY)
ranker = Reranker("jina", api_key=KEY)
ranker = Reranker("BAAI/bge-reranker-v2-m3")  # Local
ranker = Reranker("flashrank")  # Fast CPU

results = ranker.rank(query, documents)
```

---

## 🌐 BROWSER AUTOMATION

### AI-Powered Web Agents

| Tool | Approach | Best For |
|------|----------|----------|
| **Playwright MCP** | Accessibility tree snapshots | Claude/Cursor integration |
| **Browser-Use** | Playwright + LLM wrapper | Natural language automation |
| **Puppeteer** | Chrome DevTools Protocol | Native Chrome behavior |
| **Selenium** | WebDriver | Cross-browser, mature |

**Playwright MCP (March 2025):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Features:
- Uses accessibility tree (not screenshots)
- No vision model needed
- Deterministic actions
- Works with Claude Desktop, Cursor, VS Code Copilot

**Browser-Use:**
```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="Go to amazon.com, search for 'Playwright', get first URL",
    llm=ChatOpenAI(model="gpt-4o")
)
result = await agent.run()
```

**Raw CDP (bleeding edge):**
- **pydoll**: Python-first Playwright replacement
- **go-rod**: Best CDP reference implementation
- Direct Chrome DevTools Protocol for lowest latency

---

## 🔌 MCP SERVERS (Model Context Protocol)

### Categories (7000+ servers available)

**Official/Reference:**
- filesystem, git, memory, fetch, sequential-thinking, everything

**Databases:**
- PostgreSQL, MongoDB, MySQL, SQLite, Pinecone, Qdrant, Neo4j, DuckDB

**Cloud/DevOps:**
- AWS, Azure, GCP, Kubernetes, Docker, Terraform, GitHub, GitLab

**Communication:**
- Slack, Discord, Gmail, Google Calendar, Notion, Linear, Jira

**Search/Data:**
- Brave Search, Exa, Google Maps, Web Scraping, Playwright

**Specialty:**
- Figma, Xcode, After Effects, QGIS, Anki, Obsidian

**Installation:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "TOKEN" }
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

**Resources:**
- https://github.com/wong2/awesome-mcp-servers
- https://mcpservers.org
- https://github.com/modelcontextprotocol/servers

---

## 🧬 SELF-IMPROVING SYSTEMS

### Darwin Gödel Machine (Research-Grade)

Population-based self-modification:
- Agents propose code changes to themselves
- Test on benchmarks (SWE-bench, Polyglot)
- Keep successful mutations
- Darwinian evolution for open-ended exploration

**Results:**
- SWE-bench: 20% → 50% (2.5x improvement)
- Polyglot: 14% → 30% (2.2x improvement)
- Cost: ~$22,000 for 80 iterations

**Self-Discovered Improvements:**
- Patch validation steps
- Better file viewing tools
- Multi-solution generation + ranking
- History tracking
- Hallucination detection (then removed it 😬)

### Claude Code Self-Improvement (Accessible)

**CLAUDE.md Pattern:**
```markdown
# CLAUDE.md

## Meta-Rules
- When you make an error, stop and analyze root cause
- Abstract to general principle
- Add rule to prevent recurrence
- Verify rule doesn't conflict with existing rules

## Learned Rules
[Rules accumulate here as Claude learns]
```

**Magic Prompt:**
> "Reflect on what just went wrong. Abstract the general pattern. Update CLAUDE.md with a new rule. Then retry."

Cost: $0-50/month

---

## 🛠️ SPECIALTY TOOLS

### Document Processing
- **Docling** (IBM): Universal document parser
- **Marker**: PDF to Markdown with tables
- **Unstructured**: Multi-format ingestion
- **PyMuPDF/pdfplumber**: PDF extraction

### Speech/Audio
- **Whisper** (OpenAI): SOTA transcription
- **Deepgram**: Real-time speech
- **ElevenLabs/Cartesia**: TTS synthesis

### Vision/Multimodal
- **ColPali**: Vision document retrieval
- **Florence-2**: Visual understanding
- **LLaVA/Qwen-VL**: Vision-language models

### Code Analysis
- **tree-sitter**: AST parsing (40+ languages)
- **CodeSage**: Code embeddings
- **sourcery**: Python refactoring

### Observability
- **Langfuse**: Open-source LLM observability
- **Helicone**: Request logging
- **Weights & Biases**: Experiment tracking

---

## 📦 QUICK INSTALL REFERENCE

### Python (pip)
```bash
# Agent Frameworks
pip install langchain langgraph crewai autogen-agentchat
pip install dspy-ai llama-index pydantic-ai

# Inference
pip install vllm sglang

# Fine-tuning
pip install unsloth axolotl torchtune
pip install peft trl transformers

# Evaluation
pip install deepeval ragas trulens langfuse

# Embeddings/Reranking
pip install sentence-transformers FlagEmbedding
pip install rerankers

# Structured Output
pip install instructor outlines

# Browser Automation
pip install playwright browser-use

# Document Processing
pip install docling marker pdfplumber unstructured
```

### NPM (MCP Servers)
```bash
npx @playwright/mcp@latest
npx @modelcontextprotocol/server-memory
npx @modelcontextprotocol/server-filesystem
npx @modelcontextprotocol/server-github
```

### Ollama Models
```bash
# Embeddings
ollama pull nomic-embed-text
ollama pull mxbai-embed-large

# LLMs
ollama pull llama3.3
ollama pull qwen2.5:32b
ollama pull deepseek-r1:32b
```

---

## 🎯 DECISION TREES

### "Which Agent Framework?"
```
Need multi-GPU? 
├─ Yes → LangGraph or AutoGen
└─ No → What's your priority?
         ├─ Speed to market → CrewAI
         ├─ Research/eval → DSPy  
         ├─ RAG-heavy → LlamaIndex
         └─ Enterprise → Semantic Kernel
```

### "Which Inference Engine?"
```
Running locally?
├─ Yes → Got GPU?
│        ├─ Yes → SGLang (fastest) or vLLM
│        └─ No → llama.cpp or Ollama
└─ No → Use API (OpenAI, Anthropic, etc.)
```

### "Which Embedding Model?"
```
Budget?
├─ Free → Gemini (API) or Nomic (local)
├─ Cheap → voyage-3.5-lite ($0.02/M)
└─ Best quality → voyage-3.5-large
```

---

## 📊 COST COMPARISON

| Use Case | Budget Option | Mid-tier | Premium |
|----------|---------------|----------|---------|
| Embeddings | Gemini (free) | voyage-lite ($0.02/M) | voyage-large ($0.06/M) |
| Reranking | FlashRank (free) | Jina ($0.01/M) | Cohere API |
| Fine-tuning | Unsloth (free) | Cloud GPUs (~$1-3/hr) | Full fine-tune ($1000s) |
| Evaluation | DeepEval (free) | RAGAS (~$0.01-0.10/eval) | Enterprise tools |
| Inference | Ollama (free) | vLLM ($1-3/hr GPU) | SGLang cluster |

---

*Last updated: December 2025*
*For mainstream tools, see: capability_map.md*
