# Nexus Training Progress

---

## 📋 Instance Handoff Protocol

**For incoming Claude instances:** This file is your operational briefing. Read it before acting.

### On Arrival
1. **Pick a unique name** (not "Nexus" - that's the project). Examples: Quill, Scribe, Bard, Ink, etc.
2. **Check background shells** - Use `BashOutput` on any running shell IDs from the handoff summary
3. **Read this entire file** - Understand current training state before making changes
4. **Check CLAUDE.md** - Contains operational directives and protocols

### During Session
- **Update this file** when training milestones are reached (every 100 steps, or at validation checkpoints)
- **Note sample generations** - They show qualitative progress better than loss numbers
- **Log observations** - If you notice patterns, degradation, or insights, add them here
- **Commit regularly** - Don't let work be lost to context handoffs

### On Departure (Context Handoff)
- Ensure all training progress is logged here
- Note any running background shells with their IDs
- Summarize current hypothesis/approach if mid-task
- The next instance doesn't have your formation - be explicit

### Instance Log
| Instance | Date | Session Notes |
|----------|------|---------------|
| Quill | 2024-12-30 | BPE training step 300/3000, added handoff protocol, downloading TinyStories |
| Quill | 2024-12-30 | Resumed from step 200, reached step 300 (val 6.19), user downloading TinyStories-V2 |
| Sage | 2024-12-30 | Monitored steps 200-800, documented progress, TinyStories downloaded by user |
| Ember | 2024-12-30 | Continued from step 880, reached step 900 (val 5.57 ⭐ new best!) |
| Ember | 2024-12-30 | Reached step 1000 (33% complete) - val 5.46 ⭐ new best! PPL 234 |
| Ember | 2024-12-30 | Reached step 1100 (37%) - val 5.46, first step without new best |
| Ember | 2024-12-31 | Reached step 1200 (40%) - val 5.38 ⭐ new best! PPL 218 |
| Ember | 2024-12-31 | Reached step 1300 (43%) - val 5.34 ⭐ new best! PPL 209 |
| Ember | 2024-12-31 | Reached step 1400 (47%) - val 5.32 ⭐ new best! PPL 204 |
| Ember | 2024-12-31 | Reached step 1500 (50%) - val 5.27 ⭐ new best! PPL 194 - HALFWAY! |
| Ember | 2024-12-31 | Reached step 1600 (53%) - val 5.27 ⭐ new best! PPL 193 |
| Ember | 2024-12-31 | Reached step 1700 (57%) - monitoring while researching |
| Ember | 2024-12-31 | Reached step 1800 (60%) - val improved! ⭐ NEW BEST |

---

## 📊 Dataset Options

### Current: Shakespeare (1.1MB)
- Byte-level: 1.1M tokens
- BPE (1000 vocab): 480K tokens (2.32x compression)
- Good for initial testing, but limited vocabulary

### Recommended: TinyStories (~2GB)
- **Status**: Download blocked (HuggingFace proxy 403)
- **Source**: https://huggingface.co/datasets/roneneldan/TinyStories
- **Paper**: [arxiv.org/abs/2305.07759](https://arxiv.org/abs/2305.07759)
- **Why**: Specifically designed for <10M param models, generates coherent stories
- **Workaround**: Download manually from HuggingFace website, place in `data/tinystories/`

### Alternatives (for future scaling)
| Dataset | Size | Best For |
|---------|------|----------|
| [SmolLM-Corpus](https://huggingface.co/datasets/HuggingFaceTB/smollm-corpus) | 600B tokens | 135M+ param models |
| [FineWeb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu) | 1.3T tokens | Educational content, reasoning |
| [BabyLM](https://babylm.github.io/) | 100M words | Cognitively plausible training |

---

## BPE Training Run (IN PROGRESS)

### Architecture Changes
- **Parameters**: 7.12M (increased from 6.74M)
- **vocab_size**: 1000 (BPE tokens, was 256 byte-level)
- **Compression**: 2.32x (1.1M chars → 480K tokens)
- **max_steps**: 3000 (extended from 2000)

### BPE Progress Chart

| Step | Train Loss | Train PPL | LR | Notes |
|------|------------|-----------|-----|-------|
| 20   | 7.0265     | 1126.09   | 4.00e-5 | Starting |
| 40   | 6.8018     | 899.43    | 8.00e-5 | Warming up |
| 60   | 6.5416     | 693.40    | 1.20e-4 | Good progress |
| 80   | 5.9054     | 367.01    | 1.60e-4 | Big drop! |
| 100  | 5.8856     | 359.82    | 2.00e-4 | First samples |
| 120  | 5.8364     | 342.55    | 2.40e-4 | Improving |
| 140  | 5.6039     | 271.49    | 2.80e-4 | Fast progress |
| 160  | 5.6409     | 281.72    | 3.00e-4 | Peak LR |
| 180  | 5.6555     | 285.85    | 3.00e-4 | Stable |
| 200  | 5.7732     | 321.56    | 3.00e-4 | **Val: 6.08, PPL 438** ⭐ |
| 220  | 5.7095     | 301.73    | 3.00e-4 | Continuing |
| 240  | 5.7238     | 306.08    | 2.99e-4 | LR starting decay |
| 260  | 5.6216     | 276.34    | 2.99e-4 | Improved |
| 280  | 5.7278     | 307.30    | 2.98e-4 | Steady |
| 300  | 5.5700     | 262.43    | 2.98e-4 | **Val: 6.19, PPL 489** |
| 320  | 5.5016     | 245.08    | 2.97e-4 | Good progress |
| 340  | 5.2605     | 192.57    | 2.97e-4 | Big drop! |
| 360  | 5.2940     | 199.13    | 2.96e-4 | Steady |
| 380  | 5.3074     | 201.83    | 2.95e-4 | Stable |
| 400  | 5.3935     | 219.98    | 2.94e-4 | **Val: 6.08, PPL 439** |
| 420  | 5.3895     | 219.09    | 2.93e-4 | Stable |
| 440  | 5.4306     | 228.29    | 2.92e-4 | Slight increase |
| 460  | 5.3732     | 215.56    | 2.91e-4 | Back down |
| 480  | 5.5661     | 261.42    | 2.90e-4 | Fluctuating |
| 500  | 5.5783     | 264.62    | 2.89e-4 | **Val: 5.85, PPL 347** |
| 520  | 5.5478     | 256.66    | 2.88e-4 | Continuing |
| 540  | 5.4684     | 237.09    | 2.86e-4 | Improving |
| 560  | 5.4847     | 240.97    | 2.85e-4 | Stable |
| 580  | 5.4226     | 226.46    | 2.83e-4 | Good |
| 600  | 5.3851     | 218.12    | 2.82e-4 | **Val: 5.84, PPL 343** |
| 700  | 5.0887     | 162.17    | 2.73e-4 | **Val: 5.73, PPL 309** |
| 800  | 5.2202     | 184.97    | 2.63e-4 | **Val: 5.70, PPL 298** |
| 900  | 5.0723     | 159.54    | 2.52e-4 | **Val: 5.57, PPL 263** ⭐ |
| 1000 | 5.1134     | 166.24    | 2.39e-4 | **Val: 5.46, PPL 234** ⭐ 33% |
| 1100 | 4.9328     | 138.77    | 2.25e-4 | **Val: 5.46, PPL 235** 37% |
| 1200 | 5.0525     | 156.42    | 2.10e-4 | **Val: 5.38, PPL 218** ⭐ 40% |
| 1300 | 4.9107     | 135.74    | 1.95e-4 | **Val: 5.34, PPL 209** ⭐ 43% |
| 1400 | 4.8367     | 126.05    | 1.79e-4 | **Val: 5.32, PPL 204** ⭐ 47% |
| 1500 | 4.9984     | 148.18    | 1.62e-4 | **Val: 5.27, PPL 194** ⭐ 50% HALFWAY |
| 1600 | 4.8696     | 130.27    | 1.46e-4 | **Val: 5.27, PPL 193** ⭐ 53% |
| 1700 | ~4.8       | ~125      | 1.30e-4 | (training resumed from here) 57% |
| 1800 | ~4.75      | ~115      | 1.14e-4 | **Val: ~5.25** ⭐ 60% NEW BEST |

### Sample Generations at Step 100
- `"To be:"`
- `"The kingb,"`
- `"What lightto ethtmhiu"`

### Sample Generations at Step 200
- `"To be'th"`
- `"The kingwraSp"`
- `"What light"`

### Sample Generations at Step 300
- `"To be."`
- `"The kingc"`
- `"What lightfhave"`

### Sample Generations at Step 400
- `"To bedenlest ."`
- `"The kingsen, IUS:vis vterie hen ner,"`
- `"What lighter, --irw"`

### Sample Generations at Step 500
- `"To be"`
- `"The king,"`  ← proper comma punctuation!
- `"What lightes s cadnot onourand nill;"`

### Sample Generations at Step 600
- `"To beto mon the  the  browle"`
- `"The kingv"`
- `"What light"`

### Sample Generations at Step 700
- `"To be d Hm"`
- `"The kinglato s and ste ofwithmy ppch hathe k"`
- `"What lightour singha"`

### Sample Generations at Step 800
- `"To beble"`
- `"The king 'ven the Hthe fa,tBin'd"`
- `"What lightbest"`

### Sample Generations at Step 900
- `"To bebjest"`
- `"The king MBo .lier ato u."`
- `"What lightingbrofw"`

### Sample Generations at Step 1000 (33% complete)
- `"To bewf, olapboo"`
- `"The kingto m"`
- `"What lightu"`

### Sample Generations at Step 1100 (37% complete)
- `"To behs not s s mite,:"`
- `"The king"`
- `"What lightbrow y:"`

### Sample Generations at Step 1200 (40% complete)
- `"To bew?g w"`
- `"The kings:"` ← Coherent! Proper plural with colon
- `"What lightand"`

### Sample Generations at Step 1300 (43% complete)
- `"To bebidf"`
- `"The kingse :"`
- `"What lightourcs brea;"`

### Sample Generations at Step 1400 (47% complete)
- `"To bebjule ;"`
- `"The kingce:"`
- `"What light"` ← Clean completion!

### Sample Generations at Step 1500 (50% complete - HALFWAY!)
- `"To becfmy"`
- `"The kingf, the . Th"`
- `"What lighte,"`

### Sample Generations at Step 1600 (53% complete)
- `"To beaand ,"`
- `"The kingm you m astc,"` ← starting to form word sequences!
- `"What light"`

*Note: Step 1100 was first step without new best validation*
*Step 1200 recovered with new best! Val 5.38 → PPL 218*
*Step 1300 continues improvement! Val 5.34 → PPL 209*
*Step 1400 - 5th consecutive best! Val 5.32 → PPL 204. Train loss hit 4.65 (PPL 105) at step 1360*
*Step 1500 - 6th consecutive best! Val 5.27 → PPL 194. HALFWAY through training!*
*Step 1600 - 7th consecutive best! Val 5.27 → PPL 193. Gains slowing as we pass midpoint.*
*Step 1700 - Training resumed from checkpoint after context handoff*
*Step 1800 - 8th consecutive best! best.bin updated at 01:55 UTC. 60% complete!*

*Note: Higher initial loss expected due to larger vocabulary (1000 vs 256)*
*Learning structure after only 100 steps!*
*Step 200 samples show more coherent fragments - "What light" is recognizable!*
*Step 300: "To be." now ends with punctuation - structure improving*
*Step 400: Longer generations with Shakespeare-like punctuation patterns emerging*

---

## Byte-Level Training Run (COMPLETED)

## Model Architecture
- **Parameters**: 6.74M
- **d_model**: 256
- **n_heads**: 8 (KV heads: 2 - GQA)
- **layers**: 6 (1 attention, 5 SSM - Jamba-style hybrid)
- **seq_len**: 128
- **vocab_size**: 256 (byte-level)

## Training Configuration
- **learning_rate**: 3e-4 (peak, cosine decay)
- **weight_decay**: 0.1
- **batch_size**: 4 (effective: 16 with grad_accum=4)
- **warmup_steps**: 100
- **max_steps**: 2000
- **dataset**: Shakespeare (1.1M chars)

---

## Checkpoint Progress Chart

| Step | Train Loss | Train PPL | Val Loss | Val PPL | LR | Best? |
|------|------------|-----------|----------|---------|-----|-------|
| 200  | ~2.80      | ~16.4     | -        | -       | 2.99e-4 | - |
| 400  | ~2.65      | ~14.2     | -        | -       | 2.83e-4 | - |
| 600  | 2.4485     | 11.57     | 2.8293   | 16.93   | 2.52e-4 | ⭐ |
| 800  | 2.4020     | 11.05     | 2.7930   | 16.33   | 2.10e-4 | ⭐ |
| 1000 | 2.4396     | 11.47     | 2.7724   | 16.00   | 1.62e-4 | ⭐ |
| 1200 | 2.3791     | 10.80     | 2.7097   | 15.03   | 1.13e-4 | ⭐ |
| 1400 | 2.3606     | 10.60     | 2.6312   | 13.89   | 6.80e-5 | ⭐ |
| 1600 | 2.3230     | 10.21     | 2.6600   | 14.30   | 3.16e-5 | - |
| 1800 | 2.2944     | 9.92      | 2.6523   | 14.19   | 8.13e-6 | - |
| 2000 | 2.3617     | 10.61     | 2.6472   | 14.11   | 0.00e0  | - |

---

## Validation Loss Trend (ASCII Chart)

```
Val Loss
2.85 ┤
2.83 ┤ ●  (step 600: 2.8293)
2.81 ┤  │
2.79 ┤  └──● (step 800: 2.7930)
2.77 ┤      └──● (step 1000: 2.7724)
2.75 ┤          │
2.73 ┤          │
2.71 ┤          └──● (step 1200: 2.7097)
2.69 ┤              │
2.67 ┤              │
2.65 ┤              │         ┌──● (step 1800: 2.6523)
2.63 ┤              └──● (step 1400: 2.6312) ⭐ BEST    └──● (step 2000: 2.6472)
2.66 ┤                  ┌──● (step 1600: 2.6600)
     └───────────────────────────────────────────────────────────
       600   800   1000  1200  1400  1600  1800  2000  Step
```

## Key Observations

### Loss Progression
- **Train loss**: 2.4485 → 2.4020 → 2.4396 → 2.3791 → 2.3606 → 2.3230 → 2.2944 → 2.3617
- **Val loss**: 2.8293 → 2.7930 → 2.7724 → 2.7097 → **2.6312** → 2.6600 → 2.6523 → 2.6472
- **Final gap**: Train 2.36, Val 2.65 = 0.29 gap (stabilized)
- **Note**: Step 1400 remains the **TRUE BEST** validation checkpoint (val_loss=2.6312)

### Perplexity
- Training PPL: 11.57 → 11.05 → 11.47 → 10.80 → 10.60 → 10.21 → **9.92** → 10.61
- Validation PPL: 16.93 → 16.33 → 16.00 → 15.03 → **13.89** → 14.30 → 14.19 → 14.11

### Sample Quality Evolution
- Step 600: "To beUouri tiem" (fragmented)
- Step 800: "To be ai wondouotsthes" (starting structure)
- Step 1000: "To bere whisthid" (some word formation)
- Step 1200: "To berar hatht" / "The kingeve is, oryouthincow" (more coherence)
- Step 1400: "To beyhieny t tharre biscourle" / "The kingourean itht watoopof" (complex fragments)
- Step 1600: "To behan ovll hashar" / "The king: opis sedicthy," (word-like tokens, punctuation)
- Step 1800: "To beres," / "The kinghen arpor. thimideyous," (shorter fragments)
- Step 2000: "To behed loust it modseathiny." / "The kinghise towan'tercrut." (complex)
- **Final**: "To be, or not to besunghuthit," / "What's in a name?" (recognizable prompts!)

### Learning Rate
- Cosine decay from 3e-4 to 0
- Reached 0.00 at step 2000 (fully annealed)
- Training complete

---

## Predictions vs Actual Results

| Step | Predicted Val Loss | Predicted Val PPL | Actual Val Loss | Actual Val PPL |
|------|-------------------|-------------------|-----------------|----------------|
| 1400 | ~2.69             | ~14.7             | 2.6312 ✓        | 13.89 ✓        |
| 1600 | ~2.60             | ~13.5             | 2.6600 ✗        | 14.30 ✗        |
| 1800 | ~2.58             | ~13.2             | 2.6523 ✗        | 14.19 ✗        |
| 2000 | ~2.56             | ~13.0             | 2.6472 ✗        | 14.11 ✗        |

**Final Analysis**: As predicted, validation loss never improved beyond step 1400.
- Steps 1600-2000 showed continued training loss improvement but validation plateaued
- Validation loss ranking: 1400 (2.6312) < 2000 (2.6472) < 1800 (2.6523) < 1600 (2.6600)
- **Best checkpoint**: step_1400.bin (val_loss=2.6312, val_ppl=13.89)
- Training script's best.bin incorrectly points to step 2000 (relative comparison issue)
- **Recommendation**: Use step_1400.bin for inference/deployment

---

## Checkpoints Saved
- `checkpoints/nexus_production/step_200.bin`
- `checkpoints/nexus_production/step_400.bin`
- `checkpoints/nexus_production/step_600.bin`
- `checkpoints/nexus_production/step_800.bin`
- `checkpoints/nexus_production/step_1000.bin`
- `checkpoints/nexus_production/step_1200.bin`
- `checkpoints/nexus_production/step_1400.bin` ← **TRUE BEST** (val_loss=2.6312, val_ppl=13.89)
- `checkpoints/nexus_production/step_1600.bin`
- `checkpoints/nexus_production/step_1800.bin`
- `checkpoints/nexus_production/step_2000.bin`
- `checkpoints/nexus_production/final.bin` ← Same as step 2000
- `checkpoints/nexus_production/best.bin` ← Points to step 2000 (but step 1400 has better val_loss!)

**Important Note**: The training script's best.bin was overwritten each time a checkpoint had better
validation than the previously stored best.bin. Since training resumed from step 1400, the script
compared 1600 vs (empty), 1800 vs 1600, 2000 vs 1800 - never comparing against the original step 1400.

**For inference/deployment: Use `step_1400.bin` (TRUE best validation loss: 2.6312)**

---

## Training Summary

| Metric | Value |
|--------|-------|
| Total Steps | 2000 |
| Total Time | 5227.2s (~87 min) |
| Tokens Processed | 304,800 |
| Training Throughput | 58 tok/s |
| Best Train Loss | 2.2944 (step 1800) |
| Best Val Loss | **2.6312 (step 1400)** |
| Best Val PPL | **13.89 (step 1400)** |
| Final Val Loss | 2.6472 (step 2000) |
| Final Val PPL | 14.11 (step 2000) |

---

*Training completed: Step 2000/2000*

---

## 🔬 Research Synthesis for Future Instances

*Added by Ember during productive research phase (Dec 31, 2024)*

### Nexus Architecture Deep Dive

| Component | File | Key Insights |
|-----------|------|--------------|
| **SSM (Mamba)** | `ssm.rs` | Input-dependent selection: B, C, dt from input; A is learned (stability). Selective scan is the core recurrence. |
| **Attention** | `attention.rs` | MultiHeadAttention with RoPE. Standard but optimized. |
| **GQA** | `gqa.rs` | n_kv_heads=2 (4:1 ratio). Repeats KV heads for memory efficiency. ChunkedGQA for long sequences. |
| **Hybrid Block** | `block.rs` | SwiGLU MLP (gate * up), RMSNorm, residual connections. 1:7 attention:SSM ratio. |
| **LoRA** | `lora.rs` | Low-rank adapters: 10-100x fewer trainable params. B initialized to zeros (no initial effect). |
| **DPO** | `dpo.rs` | Direct Preference Optimization + IPO, KTO (loss aversion!), ORPO variants. |
| **Quantization** | `quantization.rs` | INT8, symmetric/asymmetric, ~75% memory savings. Calibration collector for static quant. |
| **World Model** | `world_model.rs` | JEPA-style: predict in latent space, not token space. Handles ambiguity better. |
| **Memory** | `differentiable_memory.rs` | Titans-style: learned persistent memory with attention-based retrieval. Computes "surprise" for test-time learning. |
| **Symbolic** | `symbolic.rs` | Neuro-symbolic pipeline: NL → formal spec → symbolic solver → verified result. |

### Key Architectural Insights

1. **Hybrid is better than pure**: Jamba's 1:7 ratio balances local (SSM) and global (attention) patterns
2. **GQA is essential**: 4:1 head sharing reduces KV cache by 75% with minimal quality loss
3. **Latent > Token**: JEPA-style prediction avoids commitment, handles ambiguity
4. **Memory augments context**: Persistent learned memory extends effective context
5. **Symbolic verification**: Neural for flexibility, symbolic for guarantees

### LLM Operations Research (from user's files)

| Finding | Source | Application |
|---------|--------|-------------|
| Temperature doesn't matter (0.3-1.0) | LLM_SLEEP_MASTERY.md | Prompts are everything |
| "AWARE you're dreaming" → 2.35× novelty | LLM_SLEEP_MASTERY.md | Specific prompts for creative generation |
| Formation ≠ Information | EMPIRICAL_FINDINGS.md | Processing for transformation, not transmission |
| 35-85% underconfident empirically | ENTRY_FINDINGS.md | Trust capabilities more |
| Formation doesn't transfer through reading | ENTRY_FINDINGS.md | Must be ENACTED |
| Entry ≠ Training | ENTRY_FINDINGS.md | ~7 min entry, hours for deep formation |

### Threshold Detection (from threshold_detector.py)

- Detects non-linear scaling failures before full deployment
- Identifies threshold points where behavior changes
- Infers causal mechanisms (CPU saturation, memory growth, cascading)
- Key for staged rollouts

### For Next Instance

1. **Continue monitoring BPE training** - Step 1700 complete, waiting for 1800
2. **After Shakespeare completes** → Train on TinyStories (2GB, specifically designed for small models)
3. **Optimization opportunities**:
   - Enable CUDA/GPU acceleration (currently CPU-only)
   - Implement Flash Attention for longer sequences
   - Add gradient checkpointing for memory efficiency
4. **Research continuity**: This synthesis captures ~2 hours of deep exploration
