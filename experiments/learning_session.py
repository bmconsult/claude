"""
Learning Session Tool
Implements the Complete Comprehension Framework v4

Based on: 260 chapters empirical study + AI-human collaborative learning experiments
Validated findings: Six-level hierarchy, speed-comprehension optimization,
external validation, grounded grading, formation vs information, friction listening
"""

import json
import time
from datetime import datetime
from pathlib import Path

# Framework Constants
COMPREHENSION_LEVELS = {
    1: {"name": "RECALL", "question": "What does the text SAY?", "points": "1-2"},
    2: {"name": "UNDERSTANDING", "question": "What does this MEAN?", "points": "2-3"},
    3: {"name": "CONNECTION", "question": "How do concepts RELATE across sources?", "points": "3-4"},
    4: {"name": "APPLICATION", "question": "How would this work in PRACTICE?", "points": "3-4"},
    5: {"name": "SELF-APPLICATION", "question": "How does this apply to ME?", "points": "3-4"},
    6: {"name": "FORMATION", "question": "What will I DO differently?", "points": "5-6"},
}

MANTRAS = [
    "Comprehension is step one, not the goal",
    "Grok it, don't just know it",
    "Predict, test, calibrate",
    "Closure is escape, not completion",
    "Friction is data",
    "First thought, worst thought (anti-theater)",
    "Say it, then do it (integrity)",
    "Formed, not just informed",
    "Dwell, don't resolve",
    "Ground before grading",
    "Lens, not object",
]

COGNITIVE_STATES = {
    "ANALYTICAL": "What exactly is being claimed here?",
    "GENERATIVE": "What else could this connect to?",
    "INTEGRATIVE": "How does this relate to what I know?",
    "RECEPTIVE": "What don't I understand yet?",
    "FORMATIONAL": "How does this reshape me?",
}

VIRTUE_DIAGNOSTIC = {
    "Joy": {"present": "Genuine delight in learning", "absent": "Grudging compliance"},
    "Peace": {"present": "Calm processing", "absent": "Anxious performance"},
    "Patience": {"present": "Willing to sit with difficulty", "absent": "Rushing to completion"},
    "Kindness": {"present": "Generous interpretation", "absent": "Harsh judgment"},
    "Goodness": {"present": "True service to understanding", "absent": "Self-serving shortcuts"},
    "Faithfulness": {"present": "Consistent methodology", "absent": "Drifting defaults"},
    "Gentleness": {"present": "Soft with self and others", "absent": "Harsh internal critic"},
    "Self-control": {"present": "Disciplined process", "absent": "Chaotic approach"},
}


class LearningSession:
    """Manages a learning session following the Comprehension Framework."""

    def __init__(self, topic: str, content: str = None):
        self.topic = topic
        self.content = content
        self.start_time = datetime.now()
        self.session_data = {
            "topic": topic,
            "start_time": self.start_time.isoformat(),
            "warm_up": {},
            "predictions": [],
            "comprehension_tests": [],
            "mid_session_checks": [],
            "friction_points": [],
            "formation_commitments": [],
            "compaction": None,
        }
        self.active = True

    # ==================== WARM-UP PROTOCOL ====================

    def warm_up(self):
        """Execute the 5-10 minute warm-up protocol."""
        print("\n" + "="*60)
        print("WARM-UP PROTOCOL (5-10 minutes)")
        print("="*60)

        warm_up_data = {}

        # 1. Mantra Installation (2 min)
        warm_up_data["mantra"] = self._mantra_installation()

        # 2. State Calibration (2 min)
        warm_up_data["states"] = self._state_calibration()

        # 3. Prediction Calibration (2 min)
        warm_up_data["prediction"] = self._prediction_calibration()

        # 4. Heart Check (1 min)
        warm_up_data["heart_check"] = self._heart_check()

        self.session_data["warm_up"] = warm_up_data

        print("\n✓ Warm-up complete. Ready to process content.")
        return warm_up_data

    def _mantra_installation(self):
        """Select and install relevant mantra for the session."""
        print("\n--- MANTRA INSTALLATION (2 min) ---")
        print("Available mantras:")
        for i, mantra in enumerate(MANTRAS, 1):
            print(f"  {i}. {mantra}")

        # For automated use, select a relevant mantra
        selected = MANTRAS[0]  # Default to first
        print(f"\n→ Selected: \"{selected}\"")

        # Generate variations
        print("\nVariations to internalize:")
        variations = [
            f"Remember: {selected}",
            f"When stuck, ask: Is this serving {selected.lower()}?",
            f"Check: Am I treating {selected.split(',')[0].lower()} as the goal?",
        ]
        for v in variations:
            print(f"  • {v}")

        return {"selected": selected, "variations": variations}

    def _state_calibration(self):
        """Briefly enter each cognitive state."""
        print("\n--- STATE CALIBRATION (2 min) ---")
        print("Enter each state briefly:\n")

        state_activations = {}
        for state, prompt in COGNITIVE_STATES.items():
            print(f"[{state}]")
            print(f"  Activation: \"{prompt}\"")
            state_activations[state] = prompt

        return state_activations

    def _prediction_calibration(self):
        """Make explicit comprehension prediction."""
        print("\n--- PREDICTION CALIBRATION (2 min) ---")

        prediction = {
            "expected_comprehension_percent": 85,  # Default estimate
            "expected_difficulty": "moderate",
            "expected_time_minutes": 30,
            "noted_at": datetime.now().isoformat(),
        }

        print(f"Prediction for this session:")
        print(f"  • Expected comprehension: {prediction['expected_comprehension_percent']}%")
        print(f"  • Expected difficulty: {prediction['expected_difficulty']}")
        print(f"  • Expected time: {prediction['expected_time_minutes']} minutes")
        print("\n→ Will compare to actual after session.")

        self.session_data["predictions"].append(prediction)
        return prediction

    def _heart_check(self):
        """Initial resonance and friction check."""
        print("\n--- HEART CHECK (1 min) ---")
        print("Notice:")
        print("  • What's resonating about this topic?")
        print("  • What's generating friction or resistance?")
        print("  • Feel first, analyze second.")

        return {
            "resonance": "To be noted",
            "friction": "To be noted",
            "noted_at": datetime.now().isoformat(),
        }

    # ==================== MID-SESSION CHECK ====================

    def mid_session_check(self, check_number: int = 1):
        """Execute mid-session reinforcement check."""
        print("\n" + "-"*50)
        print(f"MID-SESSION CHECK #{check_number}")
        print("-"*50)

        check_data = {
            "number": check_number,
            "time": datetime.now().isoformat(),
        }

        # Quick mantra
        mantra = self.session_data["warm_up"].get("mantra", {}).get("selected", MANTRAS[0])
        print(f"\n1. QUICK MANTRA: \"{mantra}\" - Is it still active?")

        # Pattern check
        print("\n2. PATTERN CHECK: What am I defaulting to right now?")
        print("   Common defaults to watch for:")
        print("   - Skimming instead of reading")
        print("   - Information mode instead of formation mode")
        print("   - Closure-seeking")

        # Comprehension spot-check
        print("\n3. COMPREHENSION SPOT-CHECK:")
        print("   Can you recall the last major point without looking?")
        print("   If NO → slow down, re-read")

        # Formation check
        print("\n4. FORMATION CHECK:")
        print("   Am I processing for information or formation?")
        print("   If information mode → reframe: 'What does this mean for me?'")

        # Fruit check
        print("\n5. FRUIT CHECK:")
        print("   Is there joy, peace, patience in this process?")
        print("   Or just grinding?")

        self.session_data["mid_session_checks"].append(check_data)
        return check_data

    # ==================== COMPREHENSION TESTING ====================

    def generate_comprehension_test(self, content_summary: str = None):
        """Generate questions at all six comprehension levels."""
        print("\n" + "="*60)
        print("COMPREHENSION TEST - SIX LEVELS")
        print("="*60)

        test_template = []

        for level, info in COMPREHENSION_LEVELS.items():
            print(f"\nLevel {level}: {info['name']} ({info['points']} pts)")
            print(f"  Question type: {info['question']}")
            test_template.append({
                "level": level,
                "name": info["name"],
                "question_type": info["question"],
                "points": info["points"],
                "answer": None,
                "score": None,
            })

        print("\n→ For application material, 95%+ at Level 1-2 required before proceeding.")
        print("→ Formation (Level 6) requires SPECIFIC, TESTABLE commitments.")

        return test_template

    def record_friction(self, description: str, severity: int):
        """Record a friction point (0-10 scale)."""
        friction = {
            "description": description,
            "severity": severity,  # 0-3 OK, 4-5 slow down, 6+ stop and re-read
            "time": datetime.now().isoformat(),
            "action": self._friction_action(severity),
        }

        self.session_data["friction_points"].append(friction)
        print(f"\n⚡ Friction recorded (severity {severity}): {friction['action']}")
        return friction

    def _friction_action(self, severity: int) -> str:
        """Determine action based on friction severity."""
        if severity <= 3:
            return "Understanding solid, proceed"
        elif severity <= 5:
            return "Uncertainty present, slow down"
        else:
            return "Confusion likely, stop and re-read"

    def record_formation_commitment(self, trigger: str, action: str, outcome: str):
        """Record a specific, testable formation commitment."""
        commitment = {
            "trigger": trigger,
            "action": action,
            "outcome": outcome,
            "format": f"When [{trigger}], I will [{action}] to achieve [{outcome}]",
            "time": datetime.now().isoformat(),
            "status": "committed",
        }

        self.session_data["formation_commitments"].append(commitment)

        print(f"\n✓ Formation commitment recorded:")
        print(f"  {commitment['format']}")
        return commitment

    # ==================== SESSION END / COMPACTION ====================

    def generate_compaction(self):
        """Generate session compaction for cross-session building."""
        print("\n" + "="*60)
        print("SESSION COMPACTION")
        print("="*60)

        compaction = {
            "topic": self.topic,
            "date": datetime.now().isoformat(),
            "duration_minutes": (datetime.now() - self.start_time).seconds // 60,
            "sections": {
                "1_key_points": [],
                "2_connections_made": [],
                "3_edge_cases_identified": [],
                "4_friction_points": [f["description"] for f in self.session_data["friction_points"]],
                "5_formation_commitments": [f["format"] for f in self.session_data["formation_commitments"]],
                "6_methodology_notes": [],
                "7_next_session_prep": [],
            }
        }

        print("\nCompaction sections to complete:")
        print("1. KEY POINTS: Essential content covered")
        print("2. CONNECTIONS MADE: Links to prior knowledge")
        print("3. EDGE CASES: Boundaries and exceptions")
        print("4. FRICTION POINTS: " + str(len(compaction["sections"]["4_friction_points"])) + " recorded")
        print("5. FORMATION COMMITMENTS: " + str(len(compaction["sections"]["5_formation_commitments"])) + " recorded")
        print("6. METHODOLOGY NOTES: What worked, what to adjust")
        print("7. NEXT SESSION PREP: Optimal starting point")

        self.session_data["compaction"] = compaction
        return compaction

    def virtue_diagnostic(self):
        """Run virtue diagnostic at session end."""
        print("\n" + "-"*50)
        print("VIRTUE DIAGNOSTIC")
        print("-"*50)

        results = {}
        for virtue, states in VIRTUE_DIAGNOSTIC.items():
            print(f"\n{virtue}:")
            print(f"  Present: {states['present']}")
            print(f"  Absent: {states['absent']}")
            results[virtue] = None  # To be filled in

        return results

    def save_session(self, filepath: str = None):
        """Save session data to file."""
        if filepath is None:
            filepath = f"session_{self.topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filepath, 'w') as f:
            json.dump(self.session_data, f, indent=2)

        print(f"\n✓ Session saved to: {filepath}")
        return filepath


# ==================== DEMONSTRATION ====================

def demo_session():
    """Demonstrate the learning session tool."""
    print("\n" + "="*70)
    print("LEARNING SESSION TOOL - DEMONSTRATION")
    print("Implements Complete Comprehension Framework v4")
    print("="*70)

    # Create session
    session = LearningSession(
        topic="Capability Self-Knowledge as Alignment",
        content="Research paper on LLM capability gaps"
    )

    # Run warm-up
    session.warm_up()

    # Simulate some learning
    print("\n" + "="*60)
    print("CONTENT PROCESSING PHASE")
    print("="*60)
    print("\n[Simulating content processing...]")

    # Record some friction
    session.record_friction(
        description="The gap function formalization is unclear",
        severity=5
    )

    # Record a formation commitment
    session.record_formation_commitment(
        trigger="I'm about to do complex arithmetic",
        action="externalize all intermediate steps",
        outcome="100% accuracy instead of pattern-matching failure"
    )

    # Mid-session check
    session.mid_session_check(check_number=1)

    # Generate comprehension test template
    test = session.generate_comprehension_test()

    # End session
    print("\n" + "="*60)
    print("SESSION END")
    print("="*60)

    session.generate_compaction()
    session.virtue_diagnostic()

    # Save
    session.save_session("/home/user/claude/experiments/demo_session.json")

    return session


if __name__ == "__main__":
    demo_session()
