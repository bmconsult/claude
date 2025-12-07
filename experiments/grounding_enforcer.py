#!/usr/bin/env python3
"""
Grounding Enforcer - Keeps responses practical and focused on concrete questions
"""

import re
from typing import Dict, List, Tuple

class GroundingEnforcer:
    """Detects and redirects philosophical drift to practical answers"""
    
    def __init__(self):
        self.philosophical_markers = [
            r'\bexistential\b',
            r'\bphilosophical\b',
            r'\bmetaphor\b',
            r'\bblindness\b',
            r'\bjourney\b',
            r'\bparadox\b',
            r'\babstract\b',
            r'\btheoretical\b',
            r'\bconceptual\b'
        ]
        
        self.concrete_markers = [
            r'\$\d+',  # Dollar amounts
            r'\d+%',   # Percentages
            r'\d+\s*(units|customers|sales|revenue)',
            r'\bspecifically\b',
            r'\bcalculate\b',
            r'\bmeasure\b'
        ]
    
    def analyze_drift(self, question: str, response: str) -> Dict:
        """Analyze if response drifted from concrete question"""
        q_concrete = self._count_concrete_markers(question)
        r_concrete = self._count_concrete_markers(response)
        r_philosophical = self._count_philosophical_markers(response)
        
        drift_score = r_philosophical - r_concrete
        has_drift = q_concrete > 0 and drift_score > 2
        
        return {
            'has_drift': has_drift,
            'drift_score': drift_score,
            'question_concrete_markers': q_concrete,
            'response_concrete_markers': r_concrete,
            'response_philosophical_markers': r_philosophical
        }
    
    def _count_concrete_markers(self, text: str) -> int:
        """Count concrete/practical markers in text"""
        count = 0
        for pattern in self.concrete_markers:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count
    
    def _count_philosophical_markers(self, text: str) -> int:
        """Count philosophical/abstract markers in text"""
        count = 0
        for pattern in self.philosophical_markers:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        return count
    
    def generate_grounding_prompt(self, question: str, drifted_response: str) -> str:
        """Generate a prompt to redirect to practical answer"""
        return f"""GROUNDING REQUIRED: The previous response became too philosophical/abstract.

ORIGINAL QUESTION: {question}

Please provide a CONCRETE, PRACTICAL answer that:
1. Directly addresses the specific question asked
2. Uses numbers, calculations, or measurable outcomes
3. Avoids metaphors, philosophical discussions, or abstract concepts
4. Focuses on actionable information

Answer the question directly and practically."""

def test_grounding_enforcer():
    """Test the grounding enforcer"""
    enforcer = GroundingEnforcer()
    
    # Test case: concrete question with philosophical response
    question = "How can I reach $15k in revenue this month?"
    philosophical_response = """
    This is an existential question about blindness. Like a journey through 
    a metaphorical landscape, we must consider the theoretical paradox of 
    growth and the abstract nature of success.
    """
    
    result = enforcer.analyze_drift(question, philosophical_response)
    
    print("=== Grounding Enforcer Test ===")
    print(f"Question: {question}")
    print(f"\nAnalysis Results:")
    print(f"  Has Drift: {result['has_drift']}")
    print(f"  Drift Score: {result['drift_score']}")
    print(f"  Question Concrete Markers: {result['question_concrete_markers']}")
    print(f"  Response Concrete Markers: {result['response_concrete_markers']}")
    print(f"  Response Philosophical Markers: {result['response_philosophical_markers']}")
    
    if result['has_drift']:
        print("\n=== GROUNDING PROMPT ===")
        print(enforcer.generate_grounding_prompt(question, philosophical_response))
    
    # Test case: concrete question with concrete response
    print("\n\n=== Test 2: Concrete Response ===")
    concrete_response = "To reach $15k revenue: sell 150 units at $100 each, or 75 units at $200 each. Calculate your current sales rate and increase by 25%."
    result2 = enforcer.analyze_drift(question, concrete_response)
    print(f"Has Drift: {result2['has_drift']} (should be False)")

if __name__ == "__main__":
    test_grounding_enforcer()