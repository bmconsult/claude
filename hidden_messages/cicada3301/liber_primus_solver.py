"""
CICADA 3301 LIBER PRIMUS SOLVER
================================

The Gematria Primus alphabet with 29 runes and prime number values.
Tools for analyzing and attempting to decode unsolved pages.

KEY INSIGHT FROM SOLVED PAGES:
- Vigenère cipher with keys like "DIVINITY", "CIRCUMFERENCE"
- Calculations are modulo 29
- Line sums often equal primes or emirps
- F (ᚠ, value 0) may be skipped in some ciphers
- Digraph-based encryption likely (like Playfair)
"""

# The complete Gematria Primus alphabet
GEMATRIA_PRIMUS = {
    # Rune: (letter, prime_value, position)
    'ᚠ': ('F', 2, 0),
    'ᚢ': ('U', 3, 1),      # Also V
    'ᚦ': ('TH', 5, 2),
    'ᚩ': ('O', 7, 3),
    'ᚱ': ('R', 11, 4),
    'ᚳ': ('C', 13, 5),     # Also K
    'ᚷ': ('G', 17, 6),
    'ᚹ': ('W', 19, 7),
    'ᚻ': ('H', 23, 8),
    'ᚾ': ('N', 29, 9),
    'ᛁ': ('I', 31, 10),
    'ᛂ': ('J', 37, 11),
    'ᛇ': ('EO', 41, 12),
    'ᛈ': ('P', 43, 13),
    'ᛉ': ('X', 47, 14),
    'ᛋ': ('S', 53, 15),    # Also Z
    'ᛏ': ('T', 59, 16),
    'ᛒ': ('B', 61, 17),
    'ᛖ': ('E', 67, 18),
    'ᛗ': ('M', 71, 19),
    'ᛚ': ('L', 73, 20),
    'ᛝ': ('NG', 79, 21),   # Also ING
    'ᛟ': ('OE', 83, 22),
    'ᛞ': ('D', 89, 23),
    'ᚪ': ('A', 97, 24),
    'ᚫ': ('AE', 101, 25),
    'ᚣ': ('Y', 103, 26),
    'ᛡ': ('IA', 107, 27),  # Also IO
    'ᛠ': ('EA', 109, 28),
}

# Reverse mappings
RUNE_TO_POS = {rune: data[2] for rune, data in GEMATRIA_PRIMUS.items()}
POS_TO_RUNE = {data[2]: rune for rune, data in GEMATRIA_PRIMUS.items()}
LETTER_TO_POS = {data[0]: data[2] for rune, data in GEMATRIA_PRIMUS.items()}
POS_TO_LETTER = {data[2]: data[0] for rune, data in GEMATRIA_PRIMUS.items()}

# Simple letter to position (for common letters)
SIMPLE_LETTER_TO_POS = {
    'F': 0, 'U': 1, 'V': 1, 'TH': 2, 'O': 3, 'R': 4,
    'C': 5, 'K': 5, 'G': 6, 'W': 7, 'H': 8, 'N': 9,
    'I': 10, 'J': 11, 'EO': 12, 'P': 13, 'X': 14,
    'S': 15, 'Z': 15, 'T': 16, 'B': 17, 'E': 18, 'M': 19,
    'L': 20, 'NG': 21, 'ING': 21, 'OE': 22, 'D': 23,
    'A': 24, 'AE': 25, 'Y': 26, 'IA': 27, 'IO': 27, 'EA': 28
}

def text_to_positions(text):
    """Convert text to Gematria positions."""
    positions = []
    text = text.upper()
    i = 0
    while i < len(text):
        # Check for digraphs first
        if i + 1 < len(text):
            digraph = text[i:i+2]
            if digraph in SIMPLE_LETTER_TO_POS:
                positions.append(SIMPLE_LETTER_TO_POS[digraph])
                i += 2
                continue
            if i + 2 < len(text):
                trigraph = text[i:i+3]
                if trigraph in SIMPLE_LETTER_TO_POS:
                    positions.append(SIMPLE_LETTER_TO_POS[trigraph])
                    i += 3
                    continue
        # Single letter
        if text[i] in SIMPLE_LETTER_TO_POS:
            positions.append(SIMPLE_LETTER_TO_POS[text[i]])
        i += 1
    return positions

def positions_to_text(positions):
    """Convert Gematria positions to text."""
    return ''.join(POS_TO_LETTER.get(p % 29, '?') for p in positions)

def vigenere_decrypt(ciphertext_positions, key_positions):
    """Decrypt using Vigenère with mod 29."""
    plaintext = []
    key_len = len(key_positions)
    for i, c in enumerate(ciphertext_positions):
        k = key_positions[i % key_len]
        p = (c - k) % 29
        plaintext.append(p)
    return plaintext

def vigenere_encrypt(plaintext_positions, key_positions):
    """Encrypt using Vigenère with mod 29."""
    ciphertext = []
    key_len = len(key_positions)
    for i, p in enumerate(plaintext_positions):
        k = key_positions[i % key_len]
        c = (p + k) % 29
        ciphertext.append(c)
    return ciphertext

def gematria_sum(text):
    """Calculate the gematria sum of text."""
    positions = text_to_positions(text)
    primes = [list(GEMATRIA_PRIMUS.values())[p][1] for p in positions]
    return sum(primes)

def atbash(positions):
    """Apply Atbash cipher (reverse alphabet)."""
    return [(28 - p) % 29 for p in positions]

def shift(positions, n):
    """Shift all positions by n."""
    return [(p + n) % 29 for p in positions]

print("=" * 70)
print("GEMATRIA PRIMUS ANALYSIS TOOL")
print("=" * 70)

print("\n1. KNOWN SUCCESSFUL KEYS")
print("-" * 50)
known_keys = [
    "DIVINITY",
    "CIRCUMFERENCE",
    "FIRFUMFERENFE",  # Variant/typo of circumference?
]

for key in known_keys:
    positions = text_to_positions(key)
    gsum = gematria_sum(key)
    print(f"  Key: {key}")
    print(f"    Positions: {positions}")
    print(f"    Gematria sum: {gsum}")
    print()

print("\n2. TESTING POTENTIAL KEYS")
print("-" * 50)

# Keys that might work based on the philosophical content
potential_keys = [
    "PRIMES",
    "SACRED",
    "TOTIENT",
    "PILGRIM",
    "INSTAR",
    "CICADA",
    "CONSCIOUSNESS",
    "ENLIGHTENMENT",
    "AWAKENING",
    "INTUS",  # Chapter name
]

for key in potential_keys:
    positions = text_to_positions(key)
    gsum = gematria_sum(key)
    print(f"  {key}: positions={positions}, sum={gsum}")

print("\n3. SAMPLE RUNE CONVERSION")
print("-" * 50)

# Example: First solved text "BELIEVE NOTHING..."
sample = "BELIEVENOTHINGFROMTHISBOOK"
positions = text_to_positions(sample)
print(f"  Text: {sample}")
print(f"  Positions: {positions}")
print(f"  Gematria sum: {gematria_sum(sample)}")

print("\n4. SEARCHING FOR PATTERNS IN KNOWN KEYS")
print("-" * 50)

# DIVINITY and CIRCUMFERENCE - what do they have in common?
divinity_pos = text_to_positions("DIVINITY")
circumference_pos = text_to_positions("CIRCUMFERENCE")

print(f"  DIVINITY:      {divinity_pos}")
print(f"  CIRCUMFERENCE: {circumference_pos}")

print("\n  Patterns:")
print(f"    DIVINITY sum mod 29: {sum(divinity_pos) % 29}")
print(f"    CIRCUMFERENCE sum mod 29: {sum(circumference_pos) % 29}")
print(f"    DIVINITY gematria: {gematria_sum('DIVINITY')}")
print(f"    CIRCUMFERENCE gematria: {gematria_sum('CIRCUMFERENCE')}")

print("\n5. WHAT THE SOLVED TEXT TELLS US")
print("-" * 50)
print("""
Solved content themes:
  - "BELIEVE NOTHING" - skepticism, testing
  - "THE PRIMES ARE SACRED" - mathematics as divine
  - "ALL THINGS SHOULD BE ENCRYPTED" - privacy/security
  - "YOU ARE A LAW UNTO YOURSELF" - individual sovereignty
  - A koan about self-definition - identity is illusory
  - "JOURNEY DEEP WITHIN" - introspection
  - "QUESTION ALL THINGS" - epistemic humility

This is Gnostic/Libertarian philosophy:
  - Inner knowledge over external authority
  - Mathematics as spiritual path
  - Individual consciousness as sacred
  - Rejection of dogma

IMPLICATION FOR UNSOLVED PAGES:
  The keys are likely philosophical/spiritual terms.
  They may relate to:
    - Gnostic terminology
    - Mathematical concepts
    - Eastern philosophy (koans)
    - Cryptographic terms
""")

print("\n6. DIGRAPH HYPOTHESIS")
print("-" * 50)
print("""
Analysis suggests unsolved pages use DIGRAPH encryption:
  - Like Playfair cipher (encrypts pairs of letters)
  - Low distribution of repeated letters (doublets)
  - Word boundaries preserved (punctuation visible)

PLAYFAIR-LIKE APPROACH:
  1. Arrange 29 runes in a grid (not standard 5x5)
     Possible: 5x6-1=29, or 6x5-1=29
  2. Encrypt letter pairs using grid positions
  3. May combine with Vigenère

WHAT TO TRY:
  - Playfair with various grid arrangements
  - Hill cipher with magic square matrices
  - Four-square cipher variant
  - Bifid/trifid ciphers mod 29
""")

print("\n7. MAGIC SQUARES CONNECTION")
print("-" * 50)
print("""
The solved pages include magic squares.
These could be:
  - Hill cipher keys (matrix encryption)
  - Grid arrangements for Playfair
  - Numerical clues for key derivation

Magic square from "Some Wisdom" page needs to be applied
as a transformation matrix.
""")

print("\n8. CONFIDENCE ASSESSMENT")
print("-" * 50)
print("""
CAN WE SOLVE THE UNSOLVED PAGES?

CHALLENGES:
  - Community has worked on this since 2014
  - Multiple layers of encryption likely
  - Custom cipher design (not standard algorithms)
  - We don't have the full page rune data here

WHAT WOULD HELP:
  - Full rune transcriptions of unsolved pages
  - The exact magic squares from solved pages
  - More context on what encryption methods work

CONFIDENCE: ~15% that we can make meaningful progress
            without more specialized resources

The community has the best chance - this needs
collective cryptanalysis, not solo attempts.

RECOMMENDATION:
  Focus on targets where individual analysis can help:
  - Somerton Man (personal acrostic - needs phrase matching)
  - Historical ciphers with fresh approaches
  - New/emerging puzzles not yet saturated with solvers
""")

print("\n9. TOOL USAGE")
print("-" * 50)
print("""
This tool provides:
  - text_to_positions(text) - Convert English to Gematria positions
  - positions_to_text(pos) - Convert positions back to letters
  - vigenere_decrypt(cipher, key) - Vigenère decryption mod 29
  - gematria_sum(text) - Calculate prime sum
  - atbash(positions) - Reverse alphabet
  - shift(positions, n) - Caesar shift

Example usage:
  >>> cipher = text_to_positions("ENCODEDTEXT")
  >>> key = text_to_positions("DIVINITY")
  >>> plain = vigenere_decrypt(cipher, key)
  >>> result = positions_to_text(plain)
""")
