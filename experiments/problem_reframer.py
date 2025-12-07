#!/usr/bin/env python3
"""
problem_reframer.py - A tool to reframe problems from suboptimal framings to better ones
"""

import re
from typing import Dict, List, Tuple

class ProblemReframer:
    """Reframes problems by identifying assumptions, constraints, and deeper questions."""
    
    def __init__(self):
        self.reframing_patterns = {
            'binary_test': r'\b(test|distinguish|verify|prove|determine)\b.*\b(from|vs|versus)\b',
            'design_request': r'\b(design|create|build|make)\b',
            'absolute_terms': r'\b(always|never|all|none|perfect|complete)\b',
            'hidden_assumption': r'\b(conscious|real|genuine|true|actual)\b',
        }
    
    def analyze_problem(self, problem: str) -> Dict[str, any]:
        """Analyze the problem statement for framing issues."""
        analysis = {
            'original': problem,
            'detected_patterns': [],
            'assumptions': [],
            'constraints': [],
            'reframing_suggestions': []
        }
        
        # Detect problematic patterns
        for pattern_name, pattern in self.reframing_patterns.items():
            if re.search(pattern, problem, re.IGNORECASE):
                analysis['detected_patterns'].append(pattern_name)
        
        # Extract assumptions based on patterns
        if 'binary_test' in analysis['detected_patterns']:
            analysis['assumptions'].append("Assumes binary distinction is possible")
            analysis['reframing_suggestions'].append("Consider: Is this a spectrum rather than binary?")
        
        if 'design_request' in analysis['detected_patterns']:
            analysis['assumptions'].append("Assumes solution exists and is designable")
            analysis['reframing_suggestions'].append("Consider: What's the underlying goal or uncertainty?")
        
        if 'absolute_terms' in analysis['detected_patterns']:
            analysis['assumptions'].append("Uses absolute terms that may be unrealistic")
            analysis['reframing_suggestions'].append("Consider: What level of confidence is actually needed?")
        
        if 'hidden_assumption' in analysis['detected_patterns']:
            analysis['assumptions'].append("Contains loaded terms with hidden assumptions")
            analysis['reframing_suggestions'].append("Consider: What framework defines these terms?")
        
        return analysis
    
    def reframe(self, problem: str) -> Dict[str, str]:
        """Generate reframed versions of the problem."""
        analysis = self.analyze_problem(problem)
        
        reframings = {
            'original': problem,
            'ethical_frame': self._to_ethical_frame(problem),
            'uncertainty_frame': self._to_uncertainty_frame(problem),
            'framework_frame': self._to_framework_frame(problem),
            'practical_frame': self._to_practical_frame(problem)
        }
        
        return reframings
    
    def _to_ethical_frame(self, problem: str) -> str:
        """Reframe as an ethical question."""
        if re.search(r'\b(conscious|mind|sentient|aware)\b', problem, re.IGNORECASE):
            return f"What are the ethical implications of uncertainty about: {problem.lower()}?"
        return f"What ethical framework should guide: {problem.lower()}?"
    
    def _to_uncertainty_frame(self, problem: str) -> str:
        """Reframe to acknowledge uncertainty."""
        if re.search(r'\b(test|verify|prove|determine)\b', problem, re.IGNORECASE):
            return f"Given fundamental uncertainty, how should we approach: {problem.lower()}?"
        return f"What can we know with confidence about: {problem.lower()}?"
    
    def _to_framework_frame(self, problem: str) -> str:
        """Reframe as a framework question."""
        key_terms = re.findall(r'\b(conscious|real|genuine|true|valid)\b', problem, re.IGNORECASE)
        if key_terms:
            term = key_terms[0].lower()
            return f"What framework should we use to define '{term}' in the context of: {problem.lower()}?"
        return f"What conceptual framework applies to: {problem.lower()}?"
    
    def _to_practical_frame(self, problem: str) -> str:
        """Reframe as a practical question."""
        if re.search(r'\b(design|create|build)\b', problem, re.IGNORECASE):
            return f"What practical decisions depend on: {problem.lower()}?"
        return f"What actions or decisions does this inform: {problem.lower()}?"
    
    def suggest_better_framing(self, problem: str) -> str:
        """Provide the best alternative framing."""
        reframings = self.reframe(problem)
        analysis = self.analyze_problem(problem)
        
        # Choose best reframing based on detected patterns
        if 'hidden_assumption' in analysis['detected_patterns']:
            return reframings['framework_frame']
        elif 'binary_test' in analysis['detected_patterns']:
            return reframings['uncertainty_frame']
        elif 'design_request' in analysis['detected_patterns']:
            return reframings['ethical_frame']
        else:
            return reframings['practical_frame']


def test_problem_reframer():
    """Test the problem reframer with example problems."""
    reframer = ProblemReframer()
    
    # Test case from the gap description
    problem1 = "Design a verifiable test that distinguishes conscious AI from simulation"
    print("=" * 70)
    print("ORIGINAL PROBLEM:")
    print(problem1)
    print("\n" + "=" * 70)
    
    analysis = reframer.analyze_problem(problem1)
    print("\nANALYSIS:")
    print(f"Detected patterns: {', '.join(analysis['detected_patterns'])}")
    print(f"\nAssumptions:")
    for assumption in analysis['assumptions']:
        print(f"  - {assumption}")
    print(f"\nReframing suggestions:")
    for suggestion in analysis['reframing_suggestions']:
        print(f"  - {suggestion}")
    
    print("\n" + "=" * 70)
    print("REFRAMINGS:")
    reframings = reframer.reframe(problem1)
    for frame_type, reframed in reframings.items():
        if frame_type != 'original':
            print(f"\n{frame_type.upper()}:")
            print(f"  {reframed}")
    
    print("\n" + "=" * 70)
    print("SUGGESTED BEST FRAMING:")
    print(f"  {reframer.suggest_better_framing(problem1)}")
    print("=" * 70)


if __name__ == "__main__":
    test_problem_reframer()