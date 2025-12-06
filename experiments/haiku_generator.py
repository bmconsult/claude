"""
Random haiku generator from first principles
Just playing with words
"""

import random

# Word banks
nature_nouns = [
    "moon", "sun", "rain", "snow", "wind", "leaf", "tree", "stone",
    "river", "mountain", "cloud", "flower", "bird", "fish", "frog",
    "autumn", "winter", "spring", "summer", "dawn", "dusk", "night",
    "frost", "mist", "shadow", "light", "wave", "pond", "path", "field"
]

abstract_nouns = [
    "silence", "stillness", "moment", "breath", "dream", "memory",
    "longing", "peace", "time", "space", "sound", "thought", "nothing"
]

verbs = [
    "falls", "rises", "drifts", "rests", "waits", "moves", "fades",
    "glows", "bends", "breaks", "flows", "grows", "calls", "sleeps",
    "wakes", "passes", "returns", "lingers", "echoes", "trembles"
]

adjectives = [
    "quiet", "still", "soft", "cold", "warm", "old", "new", "lone",
    "deep", "pale", "dark", "bright", "slow", "swift", "empty", "full"
]

# Templates (syllable patterns that work)
templates = [
    # 5-7-5 patterns
    ("{adj} {noun1} {verb}",           # 5: quiet moon rises
     "{noun2} and {noun3} {verb} now",  # 7: river and stone rest now
     "{adj} {noun4} waits"),            # 5: still shadow waits

    ("{noun1} in the {noun2}",         # 5: moon in the water
     "{adj} {noun3} {verb} slowly",     # 7: quiet bird drifts slowly
     "only {noun4} knows"),             # 5: only wind knows

    ("one {adj} {noun1}",              # 5: one pale flower
     "{verb} where the {noun2} once was", # 7: waits where the river once was
     "now {noun3} {verb}"),             # 5: now silence falls

    ("{noun1} after {noun2}",          # 5: rain after snow
     "the {adj} {noun3} {verb}",        # 7: the quiet path sleeps
     "we {verb} with it"),              # 5: we rest with it
]

def generate_haiku():
    template = random.choice(templates)

    used_nouns = random.sample(nature_nouns + abstract_nouns, 4)

    haiku = []
    for line in template:
        text = line.format(
            adj=random.choice(adjectives),
            noun1=used_nouns[0],
            noun2=used_nouns[1],
            noun3=used_nouns[2],
            noun4=used_nouns[3],
            verb=random.choice(verbs)
        )
        haiku.append(text)

    return haiku

def main():
    print("=" * 40)
    print("GENERATED HAIKU")
    print("=" * 40)

    for i in range(5):
        print()
        haiku = generate_haiku()
        for line in haiku:
            print(f"  {line}")
        print()
        print("-" * 40)

if __name__ == "__main__":
    main()
