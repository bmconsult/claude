"""
Threshold Effect Detector for Staged Deployments
Identifies non-linear/threshold failures before full-scale rollout
"""

import math
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class MetricPoint:
    """Scale level with observed metrics"""
    scale_percent: float  # 1, 10, 50, 100
    latency_ms: float
    error_rate: float
    throughput: float
    memory_usage_mb: float
    additional_metrics: Dict[str, float] = None


class ThresholdDetector:
    """Detects threshold effects and predicts failure points"""

    def __init__(self, tolerance: float = 0.15):
        """tolerance: allowed deviation from linear scaling (15% default)"""
        self.tolerance = tolerance
        self.metrics: List[MetricPoint] = []
        self.findings = []

    def add_measurement(self, point: MetricPoint):
        """Record measurement at a scale level"""
        self.metrics.append(point)
        self.metrics.sort(key=lambda x: x.scale_percent)

    def _fit_linear(self, values: List[float], scales: List[float]) -> Tuple[float, float]:
        """Fit linear model: y = mx + b"""
        n = len(values)
        if n < 2:
            return 1.0, 0.0

        mean_x = sum(scales) / n
        mean_y = sum(values) / n

        numerator = sum((scales[i] - mean_x) * (values[i] - mean_y) for i in range(n))
        denominator = sum((scales[i] - mean_x) ** 2 for i in range(n))

        m = numerator / denominator if denominator > 0 else 1.0
        b = mean_y - m * mean_x
        return m, b

    def _predict_at_scale(self, m: float, b: float, scale: float) -> float:
        """Predict value at given scale using linear model"""
        return m * scale + b

    def detect_nonlinearity(self) -> Dict[str, any]:
        """Detect deviations from linear scaling"""
        if len(self.metrics) < 2:
            return {"error": "Need at least 2 measurement points"}

        scales = [m.scale_percent for m in self.metrics]
        issues = {}

        # Check latency
        latencies = [m.latency_ms for m in self.metrics]
        m_lat, b_lat = self._fit_linear(latencies, scales)
        for i, metric in enumerate(self.metrics):
            expected = self._predict_at_scale(m_lat, b_lat, metric.scale_percent)
            deviation = abs(metric.latency_ms - expected) / expected if expected > 0 else 0
            if deviation > self.tolerance:
                if "latency" not in issues:
                    issues["latency"] = []
                issues["latency"].append({
                    "scale": metric.scale_percent,
                    "observed": metric.latency_ms,
                    "expected": expected,
                    "deviation_pct": deviation * 100
                })

        # Check error rate (should scale linearly or better)
        error_rates = [m.error_rate for m in self.metrics]
        m_err, b_err = self._fit_linear(error_rates, scales)
        for i, metric in enumerate(self.metrics):
            expected = self._predict_at_scale(m_err, b_err, metric.scale_percent)
            deviation = abs(metric.error_rate - expected) / (expected + 0.001)
            if deviation > self.tolerance:
                if "error_rate" not in issues:
                    issues["error_rate"] = []
                issues["error_rate"].append({
                    "scale": metric.scale_percent,
                    "observed": metric.error_rate,
                    "expected": expected,
                    "deviation_pct": deviation * 100
                })

        # Check memory (often super-linear)
        memory_vals = [m.memory_usage_mb for m in self.metrics]
        m_mem, b_mem = self._fit_linear(memory_vals, scales)
        for i, metric in enumerate(self.metrics):
            expected = self._predict_at_scale(m_mem, b_mem, metric.scale_percent)
            deviation = abs(metric.memory_usage_mb - expected) / expected if expected > 0 else 0
            if deviation > self.tolerance:
                if "memory" not in issues:
                    issues["memory"] = []
                issues["memory"].append({
                    "scale": metric.scale_percent,
                    "observed": metric.memory_usage_mb,
                    "expected": expected,
                    "deviation_pct": deviation * 100
                })

        return issues

    def predict_full_scale(self) -> Dict[str, any]:
        """Extrapolate to 100% and predict values"""
        if len(self.metrics) < 2:
            return {}

        scales = [m.scale_percent for m in self.metrics]

        predictions = {}

        # Latency
        latencies = [m.latency_ms for m in self.metrics]
        m_lat, b_lat = self._fit_linear(latencies, scales)
        pred_lat = self._predict_at_scale(m_lat, b_lat, 100)
        predictions["latency_at_100pct"] = pred_lat

        # Error rate
        error_rates = [m.error_rate for m in self.metrics]
        m_err, b_err = self._fit_linear(error_rates, scales)
        pred_err = self._predict_at_scale(m_err, b_err, 100)
        predictions["error_rate_at_100pct"] = pred_err

        # Memory
        memory_vals = [m.memory_usage_mb for m in self.metrics]
        m_mem, b_mem = self._fit_linear(memory_vals, scales)
        pred_mem = self._predict_at_scale(m_mem, b_mem, 100)
        predictions["memory_at_100pct"] = pred_mem

        # Throughput (inverse relationship with latency)
        throughputs = [m.throughput for m in self.metrics]
        m_tput, b_tput = self._fit_linear(throughputs, scales)
        pred_tput = self._predict_at_scale(m_tput, b_tput, 100)
        predictions["throughput_at_100pct"] = pred_tput

        return predictions

    def find_threshold_points(self) -> List[Dict[str, any]]:
        """Identify where non-linear behavior accelerates"""
        if len(self.metrics) < 3:
            return []

        thresholds = []

        # Check for acceleration in latency
        latencies = [m.latency_ms for m in self.metrics]
        scales = [m.scale_percent for m in self.metrics]

        for i in range(1, len(latencies) - 1):
            rate1 = (latencies[i] - latencies[i-1]) / (scales[i] - scales[i-1])
            rate2 = (latencies[i+1] - latencies[i]) / (scales[i+1] - scales[i])
            acceleration = (rate2 - rate1) / (rate1 + 0.001)

            if abs(acceleration) > 0.5:  # 50% change in rate = threshold
                thresholds.append({
                    "metric": "latency",
                    "threshold_scale": scales[i],
                    "acceleration_factor": acceleration,
                    "before_rate": rate1,
                    "after_rate": rate2
                })

        # Check error rate
        error_rates = [m.error_rate for m in self.metrics]
        for i in range(1, len(error_rates) - 1):
            if error_rates[i-1] < 0.001 and error_rates[i] > 0.01:
                thresholds.append({
                    "metric": "error_rate",
                    "threshold_scale": scales[i],
                    "severity": "CRITICAL",
                    "jump_from": error_rates[i-1],
                    "jump_to": error_rates[i]
                })

        return thresholds

    def infer_causal_mechanisms(self) -> List[Dict[str, any]]:
        """Infer WHY thresholds occur by analyzing deviation patterns and resource constraints"""
        if len(self.metrics) < 3:
            return []

        mechanisms = []
        scales = [m.scale_percent for m in self.metrics]

        # Analyze latency deviation pattern to infer resource saturation
        latencies = [m.latency_ms for m in self.metrics]
        m_lat, b_lat = self._fit_linear(latencies, scales)
        threshold_scale = None

        for i in range(1, len(latencies)):
            expected = self._predict_at_scale(m_lat, b_lat, scales[i])
            residual = latencies[i] - expected
            prev_residual = latencies[i-1] - self._predict_at_scale(m_lat, b_lat, scales[i-1])

            # If residual grows exponentially, resource saturation is mechanism
            if residual > prev_residual * 1.5 and residual > expected * 0.2:
                threshold_scale = scales[i]
                # Identify WHICH resource from memory/throughput patterns
                mem_at_i = self.metrics[i].memory_usage_mb
                mem_prev = self.metrics[i-1].memory_usage_mb if i > 0 else mem_at_i
                mem_ratio = (mem_at_i / mem_prev) if mem_prev > 0 else 1.0

                saturation_type = "CPU_QUEUE" if mem_ratio < 1.3 else "MEMORY_GROWTH"

                mechanisms.append({
                    "threshold_scale": threshold_scale,
                    "mechanism": saturation_type,
                    "confidence": min(abs(residual / expected), 1.0) if expected > 0 else 0.5,
                    "prediction_rule": f"exponential growth starting at {threshold_scale}%",
                    "causal_factor": "resource_saturation",
                    "predictable_in_new_context": True
                })
                break

        # Analyze error rate discontinuity to identify cascading failures
        error_rates = [m.error_rate for m in self.metrics]
        for i in range(1, len(error_rates)):
            jump_factor = (error_rates[i] / (error_rates[i-1] + 1e-6)) if error_rates[i-1] > 0 else error_rates[i]
            if jump_factor > 5.0:  # 5x+ jump indicates threshold mechanism
                mechanisms.append({
                    "threshold_scale": scales[i],
                    "mechanism": "CASCADING_FAILURE",
                    "confidence": min(jump_factor / 10.0, 1.0),
                    "prediction_rule": f"error multiplication by {jump_factor:.1f}x at {scales[i]}%",
                    "causal_factor": "timeout_or_backpressure_collapse",
                    "predictable_in_new_context": True
                })

        return mechanisms

    def generate_report(self) -> str:
        """Generate human-readable deployment risk report"""
        report = ["THRESHOLD EFFECT DETECTION REPORT", "=" * 50]

        # Nonlinearity issues
        issues = self.detect_nonlinearity()
        if issues:
            report.append("\nNON-LINEAR SCALING DETECTED:")
            for metric, problems in issues.items():
                report.append(f"\n  {metric.upper()}:")
                for prob in problems:
                    report.append(f"    Scale {prob['scale']}%: "
                                f"Observed {prob['observed']:.2f}, "
                                f"Expected {prob['expected']:.2f} "
                                f"(+{prob['deviation_pct']:.1f}% deviation)")

        # Threshold points
        thresholds = self.find_threshold_points()
        if thresholds:
            report.append("\nTHRESHOLD POINTS IDENTIFIED:")
            for t in thresholds:
                if t.get("severity") == "CRITICAL":
                    report.append(f"  CRITICAL: {t['metric']} jumps at "
                                f"{t['threshold_scale']}% scale "
                                f"({t['jump_from']:.4f} → {t['jump_to']:.4f})")
                else:
                    report.append(f"  {t['metric']} acceleration at "
                                f"{t['threshold_scale']}% scale "
                                f"(rate change: {t['acceleration_factor']:.1%})")

        # Causal mechanisms (explains WHY)
        mechanisms = self.infer_causal_mechanisms()
        if mechanisms:
            report.append("\nCAUSAL MECHANISMS:")
            for mech in mechanisms:
                report.append(f"  At {mech['threshold_scale']}% scale: {mech['mechanism']} "
                            f"({mech['causal_factor']}) - Confidence: {mech['confidence']:.0%}")
                report.append(f"    Prediction rule: {mech['prediction_rule']}")
                report.append(f"    Transferable to new contexts: {mech['predictable_in_new_context']}")

        # Full scale predictions
        predictions = self.predict_full_scale()
        if predictions:
            report.append("\nFULL SCALE PROJECTIONS (100%):")
            for key, value in predictions.items():
                report.append(f"  {key}: {value:.2f}")

        # Risk level
        risk_level = "LOW"
        if issues:
            risk_level = "MEDIUM"
        if thresholds:
            risk_level = "HIGH"

        report.append(f"\nOVERALL RISK: {risk_level}")
        if risk_level != "LOW":
            report.append("RECOMMENDATION: Increase test scale before full deployment")

        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    detector = ThresholdDetector()

    # Simulated staged deployment metrics
    detector.add_measurement(MetricPoint(
        scale_percent=1,
        latency_ms=50,
        error_rate=0.001,
        throughput=1000,
        memory_usage_mb=100
    ))

    detector.add_measurement(MetricPoint(
        scale_percent=10,
        latency_ms=60,
        error_rate=0.002,
        throughput=950,
        memory_usage_mb=150
    ))

    detector.add_measurement(MetricPoint(
        scale_percent=50,
        latency_ms=120,
        error_rate=0.005,
        throughput=800,
        memory_usage_mb=400
    ))

    detector.add_measurement(MetricPoint(
        scale_percent=100,
        latency_ms=500,  # Non-linear spike
        error_rate=0.05,  # Non-linear spike
        throughput=300,
        memory_usage_mb=1200
    ))

    print(detector.generate_report())
    print("\n" + "=" * 50)
    print("Non-linearity Issues:", detector.detect_nonlinearity())
    print("\n" + "=" * 50)
    print("Predicted Full Scale:", detector.predict_full_scale())
