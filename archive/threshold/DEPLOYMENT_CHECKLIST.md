# Threshold Effect Deployment Checklist

## Pre-Deployment Preparation

- [ ] Define acceptable thresholds for each metric
  - Max latency: ___ ms
  - Max error rate: ___ %
  - Max memory: ___ MB
  - Custom metrics: ___

- [ ] Set tolerance for threshold detector
  - [ ] 0.10 (strict)
  - [ ] 0.15 (standard)
  - [ ] 0.25 (lenient)

- [ ] Prepare monitoring for each stage
  - [ ] Baseline metrics (1% stage)
  - [ ] Measurement frequency (recommend: every 5 min)
  - [ ] Data collection duration (recommend: 30 min per stage)

## At Each Stage (1%, 10%, 50%)

### Stage Entry
- [ ] Load is stable (no spikes, transients)
- [ ] System is warmed up (if applicable)
- [ ] Start collecting metrics

### Stage Monitoring (5-30 min)
- [ ] Latency p50/p95/p99 stable
- [ ] Error rate stable
- [ ] Memory usage stable
- [ ] No cascading failures or alerts

### Stage Analysis
- [ ] Collect full metrics snapshot
- [ ] Save to JSON: `metrics_{STAGE}.json`
- [ ] Run: `python deployment_gate_example.py --gate`

### Stage Decision
```
IF risk_level == "LOW":
   ✅ Proceed to next stage (or 100% if final)

IF risk_level == "MEDIUM":
   ⚠️ Optional: Test intermediate scale (e.g., 75%)
   OR escalate for team review

IF risk_level == "HIGH":
   ❌ STOP deployment
   - Document threshold point
   - Root cause analysis
   - Fix implementation
   - Re-test from 1%
```

## Metrics Template

For each stage, collect:

```json
{
  "scale_percent": 50,
  "timestamp": "2024-12-10T15:30:00Z",
  "latency_p50": 120,
  "latency_p95": 200,
  "latency_p99": 500,
  "error_rate": 0.005,
  "throughput": 800,
  "memory_mb": 400,
  "cpu_percent": 65,
  "connections_active": 250,
  "custom": {
    "cache_hit_rate": 0.85,
    "gc_pause_ms": 15,
    "queue_depth": 100
  }
}
```

## Common Issues & Quick Fixes

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Latency jumps at 50% | Resource pool saturated | Increase pool size |
| Memory grows non-linear | Memory leak or bad algorithm | Profile with pyflame/pprof |
| Error rate spikes at scale | Cascading failures | Add circuit breaker |
| Cache hit rate drops | Cache size insufficient | Increase cache or implement LRU |
| GC pauses appear | Heap pressure | Increase heap or optimize allocation |
| Connection pool exhausted | Not closing connections | Add connection pooling with timeout |

## Red Flags (Stop and Investigate)

- [ ] Error rate > 1% at any scale
- [ ] Latency > 2x expected at any scale
- [ ] Memory growth > 3x expected
- [ ] Any metric with >50% deviation from linear
- [ ] Acceleration detected (rate of change increasing)
- [ ] Multiple metrics failing simultaneously

## Post-Deployment Validation

After reaching 100%:

- [ ] Monitor for 24+ hours
- [ ] Watch for late-appearing issues (cache warmup, etc.)
- [ ] Compare actual 100% metrics vs predicted
- [ ] If actual > predicted + 10%: escalate
- [ ] Document any surprises for next iteration

## Rollback Criteria

Automatic rollback if:
- [ ] Error rate exceeds defined threshold
- [ ] Latency exceeds defined threshold
- [ ] Memory usage exceeds system capacity
- [ ] Critical business metric affected

## Document Template

For each deployment, create record:

```
Deployment: [service name] v[version]
Date: [YYYY-MM-DD]
Requester: [name]

STAGE RESULTS:
1%:  Risk=LOW   | Status=✅ Passed gate
10%: Risk=LOW   | Status=✅ Passed gate
50%: Risk=MEDIUM | Status=⚠️ Reviewed by [name]
100%: Risk=LOW  | Status=✅ Deployed

THRESHOLDS DETECTED: None

PREDICTION ACCURACY:
Predicted 100% latency: 350ms
Actual 100% latency: 370ms
Error: +5.7% (acceptable)

NOTES:
- Cache hit rate dropped slightly at 50% (expected due to load diversity)
- No bottlenecks identified
- Ready for next deployment cycle
```

---

## Success Criteria

Deployment is **successful** when:
- ✅ All stages pass threshold detection
- ✅ Actual metrics match predictions (±10%)
- ✅ No threshold points identified
- ✅ No late failures appear in 24h
- ✅ Business metrics healthy

Deployment is **blocked** when:
- ❌ Any stage triggers HIGH risk
- ❌ Cascading failures observed
- ❌ Critical bottleneck found
- ❌ Multiple metrics non-linear

---

**Reference:** See `THRESHOLD_DEPLOYMENT_PROTOCOL.md` for detailed guidance
