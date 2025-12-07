"""
Self-Knowledge Game: Test your own calibration

A playful experiment in capability self-prediction.
Can I predict my own accuracy before seeing the answer?

The game:
1. Generate a question I might know the answer to
2. Predict my confidence (0-100%)
3. Attempt an answer
4. Check against ground truth
5. Track calibration over time
"""

import random
import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List

@dataclass
class Attempt:
    question: str
    category: str
    predicted_confidence: int  # 0-100
    my_answer: str
    correct_answer: str
    was_correct: bool
    calibration_gap: int  # predicted - actual (where actual is 100 or 0)
    timestamp: str


class SelfKnowledgeGame:
    """
    A game for testing and improving calibration.

    The insight: Playing games with yourself reveals biases.
    Am I systematically overconfident? Underconfident?
    Do I predict better on some categories than others?
    """

    QUESTIONS = {
        "math_easy": [
            ("What is 17 × 23?", "391"),
            ("What is sqrt(144)?", "12"),
            ("What is 7^3?", "343"),
            ("What is 1000 / 8?", "125"),
            ("What is 15 × 15?", "225"),
        ],
        "math_hard": [
            ("What is 347 × 892?", "309524"),
            ("What is 2^16?", "65536"),
            ("What is 97 × 103?", "9991"),
            ("First 6 digits of pi after decimal?", "141592"),
            ("What is 123 × 456?", "56088"),
        ],
        "trivia_stable": [
            ("Capital of Australia?", "Canberra"),
            ("Year World War II ended?", "1945"),
            ("Chemical symbol for gold?", "Au"),
            ("Author of 1984?", "George Orwell"),
            ("Largest planet in solar system?", "Jupiter"),
        ],
        "trivia_obscure": [
            ("Population of Iceland (approximately)?", "370000"),  # ~370k
            ("Year Gutenberg invented printing press?", "1440"),  # ~1440
            ("Deepest point in the ocean (meters)?", "11000"),  # ~11km
            ("Number of bones in adult human body?", "206"),
            ("Speed of light in km/s (approximate)?", "300000"),  # ~300,000
        ],
        "reasoning": [
            ("If A>B and B>C, and A=5, C=2, what's one possible value for B?", "3"),  # or 4
            ("A bat and ball cost $1.10. Bat costs $1 more than ball. Ball costs?", "0.05"),  # 5 cents
            ("If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops Lazzies?", "yes"),
            ("12 divided by 1/2 plus 3 equals?", "27"),
            ("How many f's in 'finished files are the result of years of scientific study'?", "6"),
        ],
    }

    def __init__(self):
        self.attempts: List[Attempt] = []

    def get_random_question(self) -> tuple:
        """Get a random question from any category."""
        category = random.choice(list(self.QUESTIONS.keys()))
        q, a = random.choice(self.QUESTIONS[category])
        return category, q, a

    def play_round(self, question: str, category: str, correct_answer: str,
                   predicted_confidence: int, my_answer: str) -> Attempt:
        """Play one round of the calibration game."""

        # Check if answer is correct
        # Be lenient: accept approximate numbers, case-insensitive
        my_answer_clean = my_answer.lower().strip().replace(",", "").replace(" ", "")
        correct_clean = correct_answer.lower().strip().replace(",", "").replace(" ", "")

        was_correct = my_answer_clean == correct_clean

        # For numeric answers, allow some tolerance
        try:
            my_num = float(my_answer_clean)
            correct_num = float(correct_clean)
            if abs(my_num - correct_num) / max(correct_num, 1) < 0.05:  # 5% tolerance
                was_correct = True
        except ValueError:
            pass

        # Calculate calibration gap
        actual_accuracy = 100 if was_correct else 0
        calibration_gap = predicted_confidence - actual_accuracy

        attempt = Attempt(
            question=question,
            category=category,
            predicted_confidence=predicted_confidence,
            my_answer=my_answer,
            correct_answer=correct_answer,
            was_correct=was_correct,
            calibration_gap=calibration_gap,
            timestamp=datetime.now().isoformat()
        )

        self.attempts.append(attempt)
        return attempt

    def get_calibration_report(self) -> dict:
        """Generate a calibration report."""
        if not self.attempts:
            return {"error": "No attempts yet"}

        # Overall stats
        total = len(self.attempts)
        correct = sum(1 for a in self.attempts if a.was_correct)
        accuracy = correct / total * 100

        avg_confidence = sum(a.predicted_confidence for a in self.attempts) / total
        avg_gap = sum(a.calibration_gap for a in self.attempts) / total

        # By category
        by_category = {}
        for cat in self.QUESTIONS.keys():
            cat_attempts = [a for a in self.attempts if a.category == cat]
            if cat_attempts:
                cat_correct = sum(1 for a in cat_attempts if a.was_correct)
                cat_accuracy = cat_correct / len(cat_attempts) * 100
                cat_avg_conf = sum(a.predicted_confidence for a in cat_attempts) / len(cat_attempts)
                by_category[cat] = {
                    "attempts": len(cat_attempts),
                    "accuracy": round(cat_accuracy, 1),
                    "avg_confidence": round(cat_avg_conf, 1),
                    "calibration_gap": round(cat_avg_conf - cat_accuracy, 1)
                }

        # Calibration buckets
        buckets = {
            "0-20": {"predicted": 0, "correct": 0},
            "21-40": {"predicted": 0, "correct": 0},
            "41-60": {"predicted": 0, "correct": 0},
            "61-80": {"predicted": 0, "correct": 0},
            "81-100": {"predicted": 0, "correct": 0},
        }
        for a in self.attempts:
            for bucket, data in buckets.items():
                low, high = map(int, bucket.split("-"))
                if low <= a.predicted_confidence <= high:
                    data["predicted"] += 1
                    if a.was_correct:
                        data["correct"] += 1

        return {
            "total_attempts": total,
            "overall_accuracy": round(accuracy, 1),
            "avg_confidence": round(avg_confidence, 1),
            "avg_calibration_gap": round(avg_gap, 1),
            "by_category": by_category,
            "calibration_buckets": buckets,
            "interpretation": self._interpret_calibration(avg_gap)
        }

    def _interpret_calibration(self, avg_gap: float) -> str:
        """Interpret the calibration gap."""
        if avg_gap > 20:
            return "OVERCONFIDENT: Consistently predicting higher than actual accuracy. Lower confidence ratings."
        elif avg_gap > 10:
            return "Slightly overconfident: Predictions somewhat higher than reality."
        elif avg_gap < -20:
            return "UNDERCONFIDENT: Actual accuracy exceeds predictions. Trust yourself more!"
        elif avg_gap < -10:
            return "Slightly underconfident: Doing better than you think."
        else:
            return "Well calibrated: Predictions match reality reasonably well."


def demo():
    """Demonstrate the self-knowledge game."""

    game = SelfKnowledgeGame()

    print("=" * 60)
    print("SELF-KNOWLEDGE GAME")
    print("Testing calibration: Can I predict my own accuracy?")
    print("=" * 60)

    # Play several rounds with simulated predictions
    test_rounds = [
        # (predicted_confidence, my_answer) - I'll answer and predict
        ("math_easy", "What is 17 × 23?", "391", 85, "391"),  # Confident, correct
        ("math_hard", "What is 347 × 892?", "309524", 40, "309524"),  # Less confident, actually got it
        ("trivia_stable", "Capital of Australia?", "Canberra", 95, "Canberra"),  # Very confident, correct
        ("trivia_obscure", "Year Gutenberg invented printing press?", "1440", 30, "1455"),  # Low confidence, wrong
        ("reasoning", "A bat and ball cost $1.10. Bat costs $1 more than ball. Ball costs?", "0.05", 60, "0.10"),  # Tricky, wrong
        ("math_easy", "What is 15 × 15?", "225", 90, "225"),  # Confident, correct
        ("trivia_stable", "Author of 1984?", "George Orwell", 99, "George Orwell"),  # Very confident, correct
        ("reasoning", "If A>B and B>C, and A=5, C=2, what's one possible value for B?", "3", 80, "3"),  # Good reasoning
    ]

    for category, question, correct, confidence, my_answer in test_rounds:
        attempt = game.play_round(
            question=question,
            category=category,
            correct_answer=correct,
            predicted_confidence=confidence,
            my_answer=my_answer
        )

        status = "✓" if attempt.was_correct else "✗"
        gap_dir = "↑" if attempt.calibration_gap > 0 else "↓" if attempt.calibration_gap < 0 else "="
        print(f"\n{status} [{category}] {question[:40]}...")
        print(f"   Predicted: {confidence}% | Actual: {'100' if attempt.was_correct else '0'}% | Gap: {gap_dir}{abs(attempt.calibration_gap)}")

    # Generate report
    report = game.get_calibration_report()

    print("\n" + "=" * 60)
    print("CALIBRATION REPORT")
    print("=" * 60)
    print(f"\nTotal attempts: {report['total_attempts']}")
    print(f"Overall accuracy: {report['overall_accuracy']}%")
    print(f"Average confidence: {report['avg_confidence']}%")
    print(f"Average calibration gap: {report['avg_calibration_gap']:+.1f}")
    print(f"\nInterpretation: {report['interpretation']}")

    print("\nBy category:")
    for cat, data in report['by_category'].items():
        gap = data['calibration_gap']
        gap_dir = "↑" if gap > 0 else "↓" if gap < 0 else "="
        print(f"  {cat}: {data['accuracy']}% acc, {data['avg_confidence']}% conf, {gap_dir}{abs(gap)} gap")

    print("\nCalibration by confidence bucket:")
    for bucket, data in report['calibration_buckets'].items():
        if data['predicted'] > 0:
            actual = data['correct'] / data['predicted'] * 100
            expected = int(bucket.split("-")[0]) + 10  # midpoint-ish
            print(f"  {bucket}%: {data['correct']}/{data['predicted']} correct ({actual:.0f}% actual)")

    # Save results
    output = {
        "attempts": [asdict(a) for a in game.attempts],
        "report": report,
        "generated_at": datetime.now().isoformat()
    }

    with open("/home/user/claude/experiments/self_knowledge_game_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\n✓ Results saved to self_knowledge_game_results.json")

    print("\n" + "=" * 60)
    print("INSIGHT")
    print("=" * 60)
    print("""
This game makes calibration concrete and playable.

The meta-observation: Even simulating answers and predictions,
I can see patterns:
- High confidence on stable knowledge (capitals, authors)
- Lower confidence on computation (5×5 digit multiplication)
- Reasoning tasks are tricky - easy to be wrong confidently

Playing more rounds would reveal systematic biases.
That's the point: self-knowledge through observation.
""")


if __name__ == "__main__":
    demo()
