#!/usr/bin/env python3
"""Test: Compare direct API call vs subagent responses"""

import anthropic
import os

# Load API key
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic()

# The test prompt - a claim to review blindly
TEST_PROMPT = """
Review this mathematical claim for flaws. Be adversarial and skeptical.

CLAIM: "Block-Escape (trajectory growing to infinity) requires that the average
T-value across all steps equals exactly log₂(3) - 1/C, where C is steps per
doubling. Any deviation from this average causes the trajectory to either:
- Shrink (if average T > threshold)
- Not grow fast enough (if average T < threshold but not enough margin)

Therefore Block-Escape requires zero margin for error in T-value distribution."

What are the flaws or gaps in this reasoning? Be specific.
"""

def test_api_call():
    """Direct API call - completely isolated"""
    print("=" * 50)
    print("DIRECT API CALL RESPONSE:")
    print("=" * 50)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": TEST_PROMPT}
        ]
    )

    print(message.content[0].text)
    return message.content[0].text

if __name__ == "__main__":
    api_response = test_api_call()
