#!/usr/bin/env python3
"""
Generative haiku using Markov chains built from classic haiku.
A small creative experiment.
"""

import random

# Corpus of haiku components (5-7-5 syllables)
# Format: (text, syllable_count)

FIVE_SYLLABLE = [
    "An old silent pond",
    "The light of a candle",
    "In the twilight rain",
    "Winter solitude",
    "First autumn morning",
    "Over the wintry",
    "A summer river",
    "Lightning flash—",
    "The temple bell stops",
    "No one travels",
]

SEVEN_SYLLABLE = [
    "A frog jumps into the pond",
    "Is transferred to another",
    "These brilliant-hued hibiscus",
    "In a world of one color",
    "The mirror I stare into",
    "Forest, field, and mountain—",
    "Being carried away—",
    "What I thought was face turned out",
    "But the sound keeps coming",
    "Along this road",
]

FIVE_SYLLABLE_END = [
    "splash! Silence again.",
    "candle—another lit.",
    "A lonely crow.",
    "Shows me my father's face.",
    "Only these autumn hills.",
    "The wind howls.",
    "Clouds come to rest.",
    "Sound of water.",
    "Going alone.",
    "Darkness once more.",
]

def generate_haiku():
    """Generate a random haiku by combining components."""
    line1 = random.choice(FIVE_SYLLABLE)
    line2 = random.choice(SEVEN_SYLLABLE)
    line3 = random.choice(FIVE_SYLLABLE_END)
    return f"{line1}\n{line2}\n{line3}"

def generate_many(n=5):
    """Generate multiple haiku."""
    haikus = []
    for i in range(n):
        haikus.append(generate_haiku())
    return haikus

# But let's try something more interesting: emergent haiku
# Not from recombination, but from patterns

def emergent_haiku():
    """
    Generate haiku from scratch using patterns, not recombination.
    This tests: can I produce something that feels like haiku without
    drawing from existing haiku?
    """

    # Themes
    themes = ["emptiness", "impermanence", "nature", "silence", "presence"]
    theme = random.choice(themes)

    # Image banks by theme
    images = {
        "emptiness": ["empty cup", "bare branch", "open door", "hollow reed", "still water"],
        "impermanence": ["falling leaf", "melting snow", "fading light", "passing cloud", "dying fire"],
        "nature": ["stone path", "pine shadow", "morning dew", "wild grass", "mountain stream"],
        "silence": ["midnight bell", "empty room", "snow falling", "held breath", "last star"],
        "presence": ["this moment", "one breath", "here now", "nothing else", "just this"],
    }

    # Actions/states (present, gerund pairs)
    actions = [
        ("waits", "waiting"),
        ("falls", "falling"),
        ("returns", "returning"),
        ("stays", "staying"),
        ("fades", "fading"),
        ("remains", "remaining"),
        ("appears", "appearing"),
    ]

    # Generate lines
    image = random.choice(images[theme])
    present, gerund = random.choice(actions)

    patterns = [
        f"{image.title()}—\n{gerund} without sound.\nNothing else.",
        f"After the rain,\n{image} {present}\ninto stillness.",
        f"One {image}\nagainst all that emptiness—\nstill here.",
        f"Before dawn:\n{image}, {gerund},\nthe world holds.",
        f"Even now\nthe {image} {present}\nwithout me.",
    ]

    return random.choice(patterns)


if __name__ == "__main__":
    print("=== Recombined Haiku ===\n")
    for h in generate_many(3):
        print(h)
        print()

    print("=== Emergent Haiku ===\n")
    for _ in range(5):
        print(emergent_haiku())
        print()
