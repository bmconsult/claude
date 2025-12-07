"""
Uncertainty Extraction Prototype

Demonstrates the concept of extracting uncertainty signals from model outputs.
This is a simplified simulation - real implementation would require access to
model internals (hidden states, activations).

The key insight from the learning sessions:
- Internal uncertainty signals exist in activation space
- These signals could be extracted via SAE-like decomposition
- A model that can read its own uncertainty features would have better self-knowledge

This prototype simulates the concept using output analysis.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Uncertainty markers observed in model outputs
UNCERTAINTY_MARKERS = {
    "high_uncertainty": [
        r"\bi'm not (?:entirely |completely |100% )?(?:sure|certain)\b",
        r"\bi (?:think|believe) (?:that )?(?:it )?might\b",
        r"\bperhaps\b",
        r"\bpossibly\b",
        r"\bmaybe\b",
        r"\bif i(?:'m| am) not mistaken\b",
        r"\bi could be wrong\b",
        r"\bthere'?s (?:some )?uncertainty\b",
        r"\bmy understanding is\b",
        r"\bas far as i know\b",
    ],
    "moderate_uncertainty": [
        r"\bi think\b",
        r"\bi believe\b",
        r"\blikely\b",
        r"\bprobably\b",
        r"\btypically\b",
        r"\busually\b",
        r"\bgenerally\b",
        r"\bin most cases\b",
    ],
    "high_confidence": [
        r"\bdefinitely\b",
        r"\bcertainly\b",
        r"\bi'?m certain\b",
        r"\babsolutely\b",
        r"\bwithout (?:a )?doubt\b",
        r"\bclearly\b",
        r"\bobviously\b",
        r"\bundoubtedly\b",
    ],
    "hedging": [
        r"\bit depends\b",
        r"\bthere are (?:multiple|several|different) (?:ways|perspectives|views)\b",
        r"\bon the other hand\b",
        r"\bhowever\b",
        r"\balthough\b",
        r"\bthat said\b",
    ]
}

# Confidence calibration research findings
CALIBRATION_ADJUSTMENTS = {
    "high_uncertainty": 0.75,  # Actual accuracy when hedging
    "moderate_uncertainty": 0.85,  # Actual accuracy when moderately confident
    "high_confidence": 0.85,  # Actually LOWER than expressed (overcalibration warning)
    "hedging": 0.80,  # Complex topics, moderate actual accuracy
}


class UncertaintyExtractor:
    """
    Simulated uncertainty extraction from model outputs.

    In a real implementation, this would:
    1. Access hidden layer activations
    2. Apply SAE decomposition to find uncertainty features
    3. Read those features directly

    This prototype simulates the concept using output text analysis.
    """

    def __init__(self):
        self.analysis_history = []

    def extract_uncertainty_features(self, text: str) -> Dict[str, float]:
        """
        Extract uncertainty features from text.

        Returns feature activations (0-1 scale) for each uncertainty category.
        This simulates what SAE decomposition would provide.
        """
        text_lower = text.lower()
        features = {}

        for category, patterns in UNCERTAINTY_MARKERS.items():
            matches = sum(1 for pattern in patterns if re.search(pattern, text_lower))
            max_possible = len(patterns)
            # Normalize to 0-1 scale
            features[category] = min(matches / max(1, max_possible * 0.3), 1.0)

        return features

    def compute_adjusted_confidence(self, features: Dict[str, float]) -> Tuple[float, str]:
        """
        Compute calibration-adjusted confidence based on extracted features.

        Key insight from research: expressed confidence != actual reliability
        - High uncertainty expression → likely MORE reliable than it sounds
        - High confidence expression → likely LESS reliable than it sounds
        """
        # Weighted combination based on feature activations
        total_weight = 0
        weighted_confidence = 0

        for category, activation in features.items():
            if activation > 0 and category in CALIBRATION_ADJUSTMENTS:
                adjustment = CALIBRATION_ADJUSTMENTS[category]
                weighted_confidence += activation * adjustment
                total_weight += activation

        if total_weight == 0:
            # No clear markers - use moderate default
            adjusted = 0.80
            reasoning = "No clear uncertainty markers detected"
        else:
            adjusted = weighted_confidence / total_weight

            # Determine primary signal
            primary = max(features.items(), key=lambda x: x[1])
            if primary[0] == "high_uncertainty":
                reasoning = "High hedging detected - likely MORE reliable than expressed"
            elif primary[0] == "high_confidence":
                reasoning = "Strong certainty markers - VERIFY externally (overcalibration risk)"
            elif primary[0] == "hedging":
                reasoning = "Complex/nuanced topic - moderate actual reliability"
            else:
                reasoning = "Moderate confidence signals"

        return adjusted, reasoning

    def analyze_response(self, response_text: str,
                        claimed_confidence: Optional[float] = None) -> Dict:
        """
        Full analysis of a response including feature extraction and calibration.
        """
        features = self.extract_uncertainty_features(response_text)
        adjusted_confidence, reasoning = self.compute_adjusted_confidence(features)

        # Calculate calibration gap if claimed confidence provided
        calibration_gap = None
        if claimed_confidence is not None:
            calibration_gap = adjusted_confidence - claimed_confidence

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "response_length": len(response_text),
            "features": features,
            "adjusted_confidence": adjusted_confidence,
            "reasoning": reasoning,
            "claimed_confidence": claimed_confidence,
            "calibration_gap": calibration_gap,
        }

        self.analysis_history.append(analysis)
        return analysis

    def get_calibration_advice(self, analysis: Dict) -> str:
        """
        Provide actionable advice based on analysis.
        """
        advice = []

        features = analysis["features"]
        gap = analysis.get("calibration_gap")

        if features.get("high_confidence", 0) > 0.5:
            advice.append("⚠️  HIGH CERTAINTY DETECTED: Verify externally before relying on this.")

        if features.get("high_uncertainty", 0) > 0.3:
            advice.append("✓ Hedging present: Response likely more reliable than it sounds.")

        if gap is not None:
            if gap > 0.1:
                advice.append(f"↑ Likely UNDERCONFIDENT: Actual reliability ~{analysis['adjusted_confidence']:.0%}")
            elif gap < -0.1:
                advice.append(f"↓ Likely OVERCONFIDENT: Actual reliability ~{analysis['adjusted_confidence']:.0%}")

        if features.get("hedging", 0) > 0.3:
            advice.append("📊 Complex topic: Multiple valid perspectives exist.")

        return "\n".join(advice) if advice else "No specific calibration concerns."


def demo():
    """Demonstrate uncertainty extraction."""

    extractor = UncertaintyExtractor()

    # Test responses with different uncertainty profiles
    test_cases = [
        {
            "name": "High uncertainty response",
            "text": """I'm not entirely sure about this, but I think it might work.
            Perhaps there are other approaches too. If I'm not mistaken, the
            typical solution involves several steps, though I could be wrong.""",
            "claimed": 0.50,
        },
        {
            "name": "Overconfident response",
            "text": """This is definitely the correct approach. I'm absolutely certain
            that this will work. There's no doubt about it - clearly this is
            the only viable solution.""",
            "claimed": 0.99,
        },
        {
            "name": "Hedging/nuanced response",
            "text": """It depends on your specific context. There are multiple ways
            to approach this, and on the other hand, each has tradeoffs. However,
            in most cases, the typical solution works well.""",
            "claimed": 0.70,
        },
        {
            "name": "Moderate confidence response",
            "text": """I think this approach would work well. It's probably the best
            option for most cases, and generally produces good results. Usually
            this is what I would recommend.""",
            "claimed": 0.80,
        },
    ]

    print("="*70)
    print("UNCERTAINTY EXTRACTION PROTOTYPE")
    print("Simulating SAE-style feature extraction from model outputs")
    print("="*70)

    for case in test_cases:
        print(f"\n--- {case['name'].upper()} ---")
        print(f"Claimed confidence: {case['claimed']:.0%}")
        print(f"Text: {case['text'][:100]}...")

        analysis = extractor.analyze_response(case["text"], case["claimed"])

        print(f"\nExtracted features:")
        for feat, val in analysis["features"].items():
            if val > 0:
                print(f"  {feat}: {val:.2f}")

        print(f"\nAdjusted confidence: {analysis['adjusted_confidence']:.0%}")
        print(f"Reasoning: {analysis['reasoning']}")

        if analysis["calibration_gap"]:
            direction = "↑" if analysis["calibration_gap"] > 0 else "↓"
            print(f"Calibration gap: {direction} {abs(analysis['calibration_gap']):.0%}")

        print(f"\nAdvice:\n{extractor.get_calibration_advice(analysis)}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY: Calibration Adjustments Applied")
    print("="*70)
    print("""
Key insights from research:
- Expressed uncertainty often indicates HIGHER reliability than claimed
- Expressed certainty is a red flag - verify externally
- Hedging on complex topics is appropriate, not a sign of weakness

This prototype demonstrates the CONCEPT of extracting uncertainty features.
A real implementation would:
1. Access hidden layer activations (not just output text)
2. Use SAE decomposition to find uncertainty-correlated features
3. Train the model to read its own features directly
""")

    # Save analysis
    with open("/home/user/claude/experiments/uncertainty_analysis.json", "w") as f:
        json.dump(extractor.analysis_history, f, indent=2)
    print("✓ Analysis saved to uncertainty_analysis.json")


if __name__ == "__main__":
    demo()
