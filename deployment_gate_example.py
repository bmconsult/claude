#!/usr/bin/env python3
"""
Deployment gate using threshold detection.
Blocks deployment if threshold effects detected.
"""

import json
import sys
from threshold_detector import ThresholdDetector, MetricPoint


def load_metrics_from_stage(stage_name: str) -> MetricPoint:
    """Load actual metrics from staged deployment monitoring"""
    metrics_file = f"metrics_{stage_name}.json"
    try:
        with open(metrics_file, 'r') as f:
            data = json.load(f)
        return MetricPoint(
            scale_percent=data['scale_percent'],
            latency_ms=data['latency_p50'],
            error_rate=data['error_rate'],
            throughput=data['throughput'],
            memory_usage_mb=data['memory_mb'],
            additional_metrics=data.get('custom', {})
        )
    except FileNotFoundError:
        print(f"ERROR: {metrics_file} not found")
        sys.exit(1)


def deployment_gate():
    """
    Gate decision logic:
    - 1% → 10%: check for obvious issues
    - 10% → 50%: look for acceleration
    - 50% → 100%: predict full scale impact
    """
    detector = ThresholdDetector(tolerance=0.15)

    # Load metrics from all stages that have completed
    stages = []
    for stage_name in ['1pct', '10pct', '50pct']:
        try:
            metric = load_metrics_from_stage(stage_name)
            detector.add_measurement(metric)
            stages.append(stage_name)
            print(f"✓ Loaded metrics from {stage_name} scale")
        except SystemExit:
            break

    if len(detector.metrics) < 2:
        print("Not enough data points yet. Continue staged rollout.")
        return True

    print("\n" + "=" * 60)
    print(detector.generate_report())
    print("=" * 60)

    # Decision logic
    issues = detector.detect_nonlinearity()
    thresholds = detector.find_threshold_points()
    predictions = detector.predict_full_scale()

    # Determine risk level
    risk_level = "LOW"
    block_deployment = False

    if len(issues) >= 2:  # Multiple metrics showing deviation
        risk_level = "HIGH"
        block_deployment = True
    elif len(issues) >= 1:
        risk_level = "MEDIUM"
        # Don't block, but require review

    if thresholds:
        risk_level = "HIGH"
        block_deployment = True

    # Check if predicted values exceed acceptable thresholds
    if predictions.get('latency_at_100pct', 0) > 1000:  # >1s latency
        risk_level = "HIGH"
        block_deployment = True

    if predictions.get('error_rate_at_100pct', 0) > 0.01:  # >1% error
        risk_level = "HIGH"
        block_deployment = True

    # Decision
    print(f"\nRISK LEVEL: {risk_level}")
    print(f"Current stage: {stages[-1]} (can see up to {detector.metrics[-1].scale_percent}% scale)")

    if block_deployment:
        print("\n❌ DEPLOYMENT BLOCKED - Threshold effects detected")
        print("\nRequired actions:")
        if issues:
            print(f"  1. Investigate non-linear scaling in: {', '.join(issues.keys())}")
        if thresholds:
            print(f"  2. Address threshold points detected")
        if predictions.get('latency_at_100pct', 0) > 1000:
            print(f"  3. Latency will exceed 1s at 100% - optimize critical path")
        if predictions.get('error_rate_at_100pct', 0) > 0.01:
            print(f"  4. Error rate will exceed 1% - add error handling/retries")
        return False

    elif risk_level == "MEDIUM":
        print("\n⚠️  DEPLOYMENT PAUSED - Review required")
        print("Recommendation: Test at 75% scale before proceeding to 100%")
        return False

    else:
        print("\n✅ SAFE TO DEPLOY - Linear scaling confirmed")
        return True


def validate_current_stage(stage_name: str) -> bool:
    """Check if current stage metrics are acceptable"""
    metric = load_metrics_from_stage(stage_name)

    # Basic sanity checks for this stage
    max_acceptable_latency = {
        '1pct': 100,    # ms
        '10pct': 150,
        '50pct': 300,
        '100pct': 500
    }

    max_acceptable_error = {
        '1pct': 0.001,
        '10pct': 0.005,
        '50pct': 0.01,
        '100pct': 0.01
    }

    if metric.latency_ms > max_acceptable_latency.get(stage_name, 1000):
        print(f"❌ Latency too high for {stage_name}: {metric.latency_ms}ms")
        return False

    if metric.error_rate > max_acceptable_error.get(stage_name, 0.05):
        print(f"❌ Error rate too high for {stage_name}: {metric.error_rate:.2%}")
        return False

    print(f"✅ {stage_name} metrics within acceptable range")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Deployment gate with threshold detection")
    parser.add_argument("--validate", help="Validate specific stage (1pct, 10pct, 50pct)")
    parser.add_argument("--gate", action="store_true", help="Run full gate decision")

    args = parser.parse_args()

    if args.validate:
        if validate_current_stage(args.validate):
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.gate:
        if deployment_gate():
            sys.exit(0)  # Safe to deploy
        else:
            sys.exit(1)  # Block deployment

    else:
        # Default: run gate
        if deployment_gate():
            sys.exit(0)
        else:
            sys.exit(1)
