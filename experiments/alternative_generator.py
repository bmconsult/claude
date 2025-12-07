#!/usr/bin/env python3
"""
Alternative Generator Tool
Generates creative alternatives when analysis is too pessimistic
"""

import json
from typing import Dict, List, Any


def generate_alternatives(
    original_idea: str,
    viability_score: float,
    concerns: List[str],
    num_alternatives: int = 3
) -> Dict[str, Any]:
    """
    Generate alternative approaches when original idea has low viability.
    
    Args:
        original_idea: The original business idea
        viability_score: Current viability rating (0-100)
        concerns: List of concerns/issues identified
        num_alternatives: Number of alternatives to generate
    
    Returns:
        Dictionary with alternatives and improvement strategies
    """
    
    # Identify concern categories
    concern_categories = categorize_concerns(concerns)
    
    # Generate alternatives based on different pivoting strategies
    alternatives = []
    strategies = [
        "scale_down",
        "niche_focus", 
        "partnership",
        "phased_approach",
        "different_market"
    ]
    
    for i, strategy in enumerate(strategies[:num_alternatives]):
        alternative = create_alternative(original_idea, strategy, concern_categories)
        alternatives.append(alternative)
    
    # Generate improvement paths for original idea
    improvements = generate_improvements(original_idea, concern_categories)
    
    return {
        "original_idea": original_idea,
        "original_viability": viability_score,
        "concerns_identified": concerns,
        "concern_categories": concern_categories,
        "alternatives": alternatives,
        "improvement_paths": improvements,
        "recommendation": get_recommendation(viability_score, alternatives)
    }


def categorize_concerns(concerns: List[str]) -> Dict[str, List[str]]:
    """Categorize concerns into common business challenge areas."""
    categories = {
        "market": [],
        "financial": [],
        "operational": [],
        "competitive": [],
        "timing": []
    }
    
    keywords = {
        "market": ["market", "customer", "demand", "audience", "user"],
        "financial": ["cost", "revenue", "profit", "funding", "price", "expensive"],
        "operational": ["resource", "team", "skill", "capacity", "infrastructure"],
        "competitive": ["competitor", "competition", "saturated", "crowded"],
        "timing": ["timing", "early", "late", "trend", "seasonal"]
    }
    
    for concern in concerns:
        concern_lower = concern.lower()
        categorized = False
        for category, words in keywords.items():
            if any(word in concern_lower for word in words):
                categories[category].append(concern)
                categorized = True
                break
        if not categorized:
            categories["operational"].append(concern)
    
    return {k: v for k, v in categories.items() if v}


def create_alternative(idea: str, strategy: str, concerns: Dict[str, List[str]]) -> Dict[str, str]:
    """Create an alternative based on pivoting strategy."""
    
    strategy_templates = {
        "scale_down": {
            "name": "Scaled-Down MVP",
            "description": f"Start with minimal viable version: Focus on core value proposition with reduced scope and lower initial investment.",
            "addresses": "Reduces financial and operational risks"
        },
        "niche_focus": {
            "name": "Niche Market Focus",
            "description": f"Target specific underserved segment: Dominate a smaller market before expanding.",
            "addresses": "Reduces competition and clarifies customer base"
        },
        "partnership": {
            "name": "Strategic Partnership Model",
            "description": f"Partner with established player: Leverage existing infrastructure and customer base.",
            "addresses": "Reduces operational burden and market entry barriers"
        },
        "phased_approach": {
            "name": "Phased Rollout",
            "description": f"Launch in stages: Test, learn, and iterate before full commitment.",
            "addresses": "Reduces risk through validation at each stage"
        },
        "different_market": {
            "name": "Alternative Market Entry",
            "description": f"Target different geography or demographic: Find market with less resistance.",
            "addresses": "Avoids saturated markets and timing issues"
        }
    }
    
    return strategy_templates.get(strategy, strategy_templates["scale_down"])


def generate_improvements(idea: str, concerns: Dict[str, List[str]]) -> List[str]:
    """Generate specific improvement paths for the original idea."""
    improvements = []
    
    if "market" in concerns:
        improvements.append("Conduct customer discovery interviews to validate demand")
    if "financial" in concerns:
        improvements.append("Explore bootstrapping or pre-sales to reduce funding needs")
    if "operational" in concerns:
        improvements.append("Identify key hires or outsourcing options for capability gaps")
    if "competitive" in concerns:
        improvements.append("Develop unique differentiation or proprietary advantage")
    if "timing" in concerns:
        improvements.append("Adjust timeline or find early adopter segment")
    
    if not improvements:
        improvements.append("Validate assumptions with market research")
    
    return improvements


def get_recommendation(viability_score: float, alternatives: List[Dict]) -> str:
    """Provide overall recommendation."""
    if viability_score < 30:
        return f"Consider pivoting to one of the alternatives. Original idea needs significant changes."
    elif viability_score < 60:
        return f"Explore alternatives while improving original idea. Test multiple approaches."
    else:
        return f"Original idea viable. Use alternatives as backup plans."


def test_alternative_generator():
    """Test the alternative generator with sample data."""
    
    idea = "Launch premium meal delivery service in saturated urban market"
    score = 40
    concerns = [
        "Market is highly competitive with established players",
        "High customer acquisition costs",
        "Operational complexity requires significant resources",
        "Timing may be late in market cycle"
    ]
    
    result = generate_alternatives(idea, score, concerns, num_alternatives=3)
    
    print("=== ALTERNATIVE GENERATOR RESULTS ===\n")
    print(f"Original Idea: {result['original_idea']}")
    print(f"Viability Score: {result['original_viability']}%\n")
    
    print("Concern Categories:")
    for category, items in result['concern_categories'].items():
        print(f"  - {category}: {len(items)} concerns")
    
    print("\nAlternatives Generated:")
    for i, alt in enumerate(result['alternatives'], 1):
        print(f"\n{i}. {alt['name']}")
        print(f"   {alt['description']}")
        print(f"   Addresses: {alt['addresses']}")
    
    print("\nImprovement Paths:")
    for i, improvement in enumerate(result['improvement_paths'], 1):
        print(f"  {i}. {improvement}")
    
    print(f"\nRecommendation: {result['recommendation']}")


if __name__ == "__main__":
    test_alternative_generator()