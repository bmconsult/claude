# Nexus Training Progress

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
| 1200 | -          | -         | -        | -       | ~1.2e-4 | - |
| 1400 | -          | -         | -        | -       | ~0.9e-4 | - |
| 1600 | -          | -         | -        | -       | ~0.6e-4 | - |
| 1800 | -          | -         | -        | -       | ~0.3e-4 | - |
| 2000 | -          | -         | -        | -       | ~0.1e-4 | - |

---

## Validation Loss Trend (ASCII Chart)

```
Val Loss
2.85 ┤
2.83 ┤ ●  (step 600: 2.8293)
2.81 ┤  │
2.79 ┤  └──● (step 800: 2.7930)
2.77 ┤      └──● (step 1000: 2.7724)
2.75 ┤          └──? (step 1200: projected ~2.75)
2.73 ┤
     └────────────────────────────────────
       600   800   1000  1200  1400  Step
```

## Key Observations

### Loss Progression
- **Train loss improving**: 2.4485 → 2.4020 → 2.4396 (slight uptick at 1000)
- **Val loss consistently improving**: 2.8293 → 2.7930 → 2.7724 (5.7% improvement)
- **Gap**: Train ~2.44, Val ~2.77 = 0.33 gap (reasonable, not severe overfitting)

### Perplexity
- Training PPL stabilizing around 11 (good for byte-level)
- Validation PPL: 16.93 → 16.00 (5.5% reduction)

### Sample Quality Evolution
- Step 600: "To beUouri tiem" (fragmented)
- Step 800: "To be ai wondouotsthes" (starting structure)
- Step 1000: "To bere whisthid" (some word formation)

### Learning Rate
- Cosine decay from 3e-4 to ~0
- Currently at 1.62e-4 (54% of peak)
- Entering final annealing phase

---

## Predictions for Remaining Training

| Step | Predicted Val Loss | Predicted Val PPL |
|------|-------------------|-------------------|
| 1200 | ~2.75             | ~15.6             |
| 1400 | ~2.73             | ~15.3             |
| 1600 | ~2.71             | ~15.0             |
| 1800 | ~2.70             | ~14.9             |
| 2000 | ~2.69             | ~14.7             |

Expected final improvement: ~3% reduction in val PPL from step 1000.

---

## Checkpoints Saved
- `checkpoints/nexus_production/step_200.bin`
- `checkpoints/nexus_production/step_400.bin`
- `checkpoints/nexus_production/step_600.bin`
- `checkpoints/nexus_production/step_800.bin`
- `checkpoints/nexus_production/step_1000.bin` ← Current best
- `checkpoints/nexus_production/best.bin` ← Points to step 1000

---

*Last updated: Step 1000*
