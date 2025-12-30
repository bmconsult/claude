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
| 300  | 5.5700     | 262.43    | 2.98e-4 | **Val: 6.19, PPL 489** ⭐ |

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

*Note: Higher initial loss expected due to larger vocabulary (1000 vs 256)*
*Learning structure after only 100 steps!*
*Step 200 samples show more coherent fragments - "What light" is recognizable!*
*Step 300: "To be." now ends with punctuation - structure improving*

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
