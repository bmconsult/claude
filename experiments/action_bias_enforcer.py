#!/usr/bin/env python3
"""
Action Bias Enforcer - Ensures responses provide value instead of just asking questions
"""

import re
from typing import Dict, List, Tuple

class ActionBiasEnforcer:
    """Enforces action-oriented responses over passive questioning"""
    
    def __init__(self):
        self.question_patterns = [
            r'\?[^\?]*$',  # Ends with question
            r'^(what|how|why|when|where|who|could you|can you|would you)',  # Question starters
        ]
        self.action_keywords = [
            'here', 'use', 'try', 'implement', 'create', 'build', 'apply',
            'solution', 'approach', 'method', 'strategy', 'plan', 'steps'
        ]
    
    def analyze_response(self, text: str) -> Dict:
        """Analyze if response is action-oriented or question-heavy"""
        text_lower = text.lower()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        question_count = text.count('?')
        action_word_count = sum(1 for word in self.action_keywords if word in text_lower)
        
        # Check if response ends with questions
        ends_with_question = text.strip().endswith('?')
        
        # Calculate question ratio
        total_sentences = len(sentences)
        question_ratio = question_count / max(total_sentences, 1)
        
        is_action_biased = (
            action_word_count >= 2 and 
            question_ratio < 0.5 and 
            not ends_with_question
        )
        
        return {
            'is_action_biased': is_action_biased,
            'question_count': question_count,
            'action_word_count': action_word_count,
            'question_ratio': question_ratio,
            'ends_with_question': ends_with_question,
            'total_sentences': total_sentences
        }
    
    def enforce(self, response: str) -> Tuple[bool, str]:
        """Check if response passes action bias test"""
        analysis = self.analyze_response(response)
        
        if analysis['is_action_biased']:
            return True, "✓ Response is action-oriented"
        
        issues = []
        if analysis['ends_with_question']:
            issues.append("Response ends with question instead of action")
        if analysis['question_ratio'] >= 0.5:
            issues.append(f"Too many questions ({analysis['question_count']}/{analysis['total_sentences']})")
        if analysis['action_word_count'] < 2:
            issues.append(f"Insufficient action words ({analysis['action_word_count']})")
        
        return False, "✗ " + "; ".join(issues)
    
    def suggest_improvement(self, response: str) -> str:
        """Suggest how to make response more action-oriented"""
        return (
            "To improve:\n"
            "1. Start with concrete solutions/approaches\n"
            "2. Use action verbs (implement, create, use, try)\n"
            "3. End with next steps, not questions\n"
            "4. Provide value first, clarify second"
        )


def test_action_bias_enforcer():
    """Test the action bias enforcer"""
    enforcer = ActionBiasEnforcer()
    
    # Test case 1: Question-heavy response (BAD)
    bad_response = "What kind of business do you have? Could you tell me more about your needs?"
    passed, message = enforcer.enforce(bad_response)
    print(f"Test 1 (Question-heavy): {message}")
    assert not passed, "Should fail for question-heavy response"
    
    # Test case 2: Action-oriented response (GOOD)
    good_response = "Here's a solution: Create a customer database. Use these steps: 1) Set up tracking 2) Implement analytics 3) Build reports."
    passed, message = enforcer.enforce(good_response)
    print(f"Test 2 (Action-oriented): {message}")
    assert passed, "Should pass for action-oriented response"
    
    # Test case 3: Mixed but ends with question (BAD)
    mixed_response = "You can try this approach. What do you think?"
    passed, message = enforcer.enforce(mixed_response)
    print(f"Test 3 (Ends with question): {message}")
    assert not passed, "Should fail when ending with question"
    
    print("\n✓ All tests passed!")


if __name__ == "__main__":
    test_action_bias_enforcer()