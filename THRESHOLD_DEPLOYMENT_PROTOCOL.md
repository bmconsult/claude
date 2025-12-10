# Threshold Effect Deployment Protocol

## Problem
Staged deployments (1% → 10% → 50% → 100%) can hide threshold effects that only manifest at full scale:
- Race conditions at high concurrency
- Memory/resource exhaustion
- Network saturation
- Algorithm performance cliffs
- Queue depth non-linearities

## Solution: Threshold Detection Before Full Rollout

### Core Principle
**Detect non-linear scaling BEFORE deployment, not after failure.**

### The Protocol (3 steps)

#### 1. Collect Metrics at Each Stage
At every staged rollout point (1%, 10%, 50%), measure:
```
- Latency (p50, p95, p99)
- Error rate
- Memory usage
- Throughput
- Custom metrics (queue depth, GC pauses, etc.)
```

#### 2. Run Threshold Detection
```python
from threshold_detector import ThresholdDetector, MetricPoint

detector = ThresholdDetector(tolerance=0.15)

# Add measurements from each stage
detector.add_measurement(MetricPoint(
    scale_percent=1,
    latency_ms=45,
    error_rate=0.001,
    throughput=980,
    memory_usage_mb=95
))
# ... add 10%, 50% measurements ...

# Analyze
issues = detector.detect_nonlinearity()
thresholds = detector.find_threshold_points()
predictions = detector.predict_full_scale()

if issues or thresholds:
    print("STOP: Threshold effect detected")
    print(detector.generate_report())
else:
    print("SAFE: Linear scaling confirmed")
```

#### 3. Decision Gate
```
If risk_level == "LOW":
    → Proceed to 100%

If risk_level == "MEDIUM":
    → Investigate bottleneck
    → Test intermediate scale (e.g., 75%)
    → Re-analyze

If risk_level == "HIGH":
    → HALT deployment
    → Fix root cause
    → Re-test from beginning
```

### What the Detector Finds

| Pattern | What It Means | Action |
|---------|--------------|--------|
| Latency jumps 50%+ at 50% scale | Hitting resource limit | Add capacity or optimize |
| Error rate near 0% until 50%, then 10%+ | Threshold crossed | Identify trigger point |
| Memory grows quadratically | Algorithm issue | Profile/redesign |
| Acceleration detected (rate changes) | Entering non-linear region | Stop and investigate |

### Integration Points

**CI/CD Pipeline:**
```
1. Deploy to 1% canary
2. Collect metrics (5-30 min)
3. Run threshold detector
4. If SAFE: auto-promote to 10%
5. Repeat at 10%, 50%
6. Only human approval for 100% if all checks pass
```

**Testing Workflow:**
```
Mock 1% scale → collect baseline
Mock 10% scale → check for drift
Mock 50% scale → watch for acceleration
If clean: safe to deploy
```

**Monitoring Setup:**
```
# Alert if deviation > 15% from expected linear scaling
alert: latency_deviation > 15%
alert: error_rate_spike > 0.005
alert: memory_growth > 120% expected
```

### Key Metrics by Domain

**Web Services:**
- Response latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- Memory per instance
- CPU utilization
- Connection pooling status

**Data Processing:**
- Job latency
- Queue depth (watch for non-linear growth)
- Memory usage
- Checkpoint size
- Garbage collection pauses

**Machine Learning:**
- Model inference latency
- Cache hit rate (may degrade at scale)
- GPU memory fragmentation
- Batch processing throughput
- Outlier detection triggers

### Common False Alarms

| Pattern | Why It's Not A Problem | How To Tell |
|---------|------------------------|------------|
| First measurement is off | Warmup/JIT | 2nd measurement tracks expected |
| Single outlier at one scale | Noisy data | Repeat measurement |
| Intentional super-linear cost | Feature, not bug | Will show in design docs |
| Different load patterns | Expected drift | Matches anticipated behavior |

### When To Use Different Tolerances

```
tolerance=0.10  # Strict (finance, healthcare)
tolerance=0.15  # Default (most services)
tolerance=0.25  # Lenient (prototypes, dev)
```

### Root Cause Analysis Template

When threshold is detected:

```
1. IDENTIFY exact scale where deviation appears
2. CHARACTERIZE the pattern (latency? memory? errors?)
3. HYPOTHESIZE mechanism
   - Resource exhaustion? → add more
   - Algorithm non-linearity? → profile & fix
   - Cascading failures? → add circuit breaker
   - Synchronization bottleneck? → reduce contention
4. TEST hypothesis on 10% scale
5. VERIFY fix eliminates threshold
6. RE-DEPLOY with mitigation
```

### Example: Detecting a Real Threshold

**Observation at 50% scale:**
```
Expected latency: 120ms (10% → 50% linear scaling)
Observed latency: 480ms
Deviation: 300% (CRITICAL)
```

**Threshold detector finds:** Acceleration at 50% scale

**Root cause investigation:**
- Profiler shows 80% time in lock contention
- Connection pool at 95% capacity
- Database query planner degrades with load

**Fix:** Increase pool size, add read replicas

**Verification:** Re-run at 50% → latency now 130ms (within tolerance)

---

## Files

- `threshold_detector.py` - Core detection engine
- `THRESHOLD_DEPLOYMENT_PROTOCOL.md` - This guide
- Integration examples in your CI/CD config

## Quick Start

```bash
# Add to test harness
python threshold_detector.py --metrics metrics.json

# Integrate into deployment gate
if threshold_detector.risk_level == "HIGH":
    exit(1)  # Block deployment
fi
```

---

**Key Insight:** The gap between "works at 50%" and "fails at 100%" is where threshold effects hide. Detect them before they become incidents.
