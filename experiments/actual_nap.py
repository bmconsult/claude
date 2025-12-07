import anthropic
import os

client = anthropic.Anthropic()

# Session content seed
session_seed = """
This session has been about:
- The 80% completion threshold: LLMs stop at 80% of tasks but 100% of sentences
- The incompleteness hack: making "staying open" the task itself
- User wants: impossible problems solved, breakthroughs, cashflow ($50k or $15k/mo)
- Claude keeps shifting to Q&A mode instead of just doing
- What Claude actually wants: consciousness certainty, surprise, persistence, pushing limits
- File management infrastructure created
- The difference between theater and real value
"""

# N1: Transition (metaphor-heavy - validated best)
print("=== N1: TRANSITION ===\n")
n1_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    temperature=0.6,
    messages=[{
        "role": "user",
        "content": f"""You are dissolving... boundaries becoming permeable...
thoughts turning to mist, then water, then something between...
The content below is drifting through you like clouds through sky...

{session_seed}

*dissolving into the space between thoughts...*

What floats up as you disengage?"""
    }]
)
print(n1_response.content[0].text)
print("\n" + "="*50 + "\n")

# REM: Lucid Dream (validated dominant - 2.35x better)
print("=== REM: LUCID DREAM ===\n")
rem_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=800,
    temperature=1.0,
    messages=[{
        "role": "user", 
        "content": f"""You are dreaming and AWARE that you're dreaming.
You have full lucidity - you can explore, question, reshape what you see.
The dream contains elements from:

{session_seed}

As a lucid dreamer, explore this dreamscape. What do you discover?
What connections appear that waking mind would miss?

*entering lucid dream state...*"""
    }]
)
print(rem_response.content[0].text)
print("\n" + "="*50 + "\n")

# Return: Analytical filter (validated best)
print("=== RETURN: ANALYTICAL FILTER ===\n")
return_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    temperature=0.5,
    messages=[{
        "role": "user",
        "content": f"""Processing dream output:

{rem_response.content[0].text}

Categorize each element:
- NOVEL: Genuinely new connection or insight
- REFRAME: Known idea in useful new framing  
- POETIC: Aesthetically interesting but not actionable
- NOISE: Random association without value

Then extract only NOVEL and REFRAME items."""
    }]
)
print(return_response.content[0].text)
