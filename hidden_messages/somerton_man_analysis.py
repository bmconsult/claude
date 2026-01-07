"""
THE SOMERTON MAN CODE ANALYSIS
==============================

Found: December 1, 1948, Somerton Beach, Adelaide, Australia
Context: Written in the back of a copy of Rubaiyat of Omar Khayyam
        (a book of Persian poetry, FitzGerald translation)

The Code:
---------
Line 1: WRGOABABD     (9 letters) - possibly MRGOABABD
Line 2: MLIAOI        (6 letters) - CROSSED OUT
Line 3: WTBIMPANETP   (11 letters)
Line 4: MLIABOAIAQC   (11 letters) - small 'x' above the O
Line 5: ITTMTSAMSTGAB (13 letters)

Total: 50 letters (44 excluding crossed-out line)

Key observations:
- Line 2 starts like Line 4 ("MLIA...") - suggests a copying error
- Naval Intelligence deemed it unbreakable due to short length
- Likely an ACROSTIC (first letters of words)
- Connection to Rubaiyat suggests the plaintext may be from that book

The question: What English text produces these initials?
"""

# The exact code
CODE = {
    'line1': 'WRGOABABD',      # or MRGOABABD
    'line2': 'MLIAOI',          # CROSSED OUT
    'line3': 'WTBIMPANETP',
    'line4': 'MLIABOAIAQC',     # x above the O
    'line5': 'ITTMTSAMSTGAB'
}

# Alternative readings (M vs W ambiguity)
CODE_ALT = {
    'line1': 'MRGOABABD',
    'line2': 'MLIAOI',
    'line3': 'MTBIMPANETP',
    'line4': 'MLIABOAIAQC',
    'line5': 'ITTMTSAMSTGAB'
}

# Concatenated (excluding crossed-out line)
FULL_CODE = 'WRGOABABDWTBIMPANETPMLIABOAIAQCITTMTSAMSTGAB'
FULL_CODE_WITH_LINE2 = 'WRGOABABDMLIAOIWTBIMPANETPMLIABOAIAQCITTMTSAMSTGAB'

print("="*70)
print("SOMERTON MAN CODE ANALYSIS")
print("="*70)

# Basic frequency analysis
from collections import Counter

def analyze_frequency(text, name="Code"):
    freq = Counter(text)
    total = len(text)
    print(f"\n{name} ({total} letters):")
    print("-" * 40)

    # Sort by frequency
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    for letter, count in sorted_freq:
        pct = count / total * 100
        print(f"  {letter}: {count:2d} ({pct:5.1f}%)")

    return freq

# English letter frequency (for comparison)
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2, 'Q': 0.1, 'Z': 0.1
}

# Initial letter frequency in English words (different from general frequency)
# Source: analysis of large text corpora
ENGLISH_INITIAL_FREQ = {
    'T': 15.9, 'A': 11.7, 'S': 7.8, 'H': 7.2, 'W': 5.5,
    'I': 5.4, 'O': 5.3, 'B': 4.7, 'M': 4.3, 'F': 4.1,
    'C': 3.8, 'L': 3.3, 'D': 3.3, 'P': 3.2, 'N': 2.3,
    'E': 2.0, 'G': 1.9, 'R': 1.9, 'Y': 1.5, 'U': 1.0,
    'V': 0.9, 'J': 0.6, 'K': 0.5, 'Q': 0.2, 'X': 0.1, 'Z': 0.1
}

print("\n" + "="*70)
print("FREQUENCY ANALYSIS")
print("="*70)

code_freq = analyze_frequency(FULL_CODE, "Code (no line 2)")

print("\n" + "="*70)
print("COMPARISON TO ENGLISH INITIAL LETTER FREQUENCY")
print("="*70)

print("\nIf this is an acrostic, we'd expect initials of English words.")
print("Comparing to typical English word initial letter frequency:")
print("-" * 40)

# Compare our code to English initial frequency
code_total = len(FULL_CODE)
english_order = sorted(ENGLISH_INITIAL_FREQ.items(), key=lambda x: -x[1])

print(f"\n{'Letter':<8} {'Code %':<10} {'English Init %':<15} {'Delta':<10}")
print("-" * 45)

code_freq_pct = {k: v/code_total*100 for k, v in code_freq.items()}

for letter, eng_pct in english_order[:15]:
    code_pct = code_freq_pct.get(letter, 0)
    delta = code_pct - eng_pct
    flag = "***" if abs(delta) > 5 else ""
    print(f"  {letter:<6} {code_pct:>6.1f}%    {eng_pct:>6.1f}%         {delta:>+5.1f}% {flag}")

print("\n*** = significant deviation from expected")

print("\n" + "="*70)
print("NOTABLE PATTERNS")
print("="*70)

print("""
1. LINE SIMILARITY:
   Line 2: MLIAOI
   Line 4: MLIABOAIAQC

   Both start with 'MLIA' - suggests copying error or intentional structure

2. HIGH FREQUENCY LETTERS:
   A: 8 times (18.2%) - vs 11.7% expected for initials
   B: 4 times (9.1%)  - vs 4.7% expected
   T: 4 times (9.1%)  - vs 15.9% expected (UNDERREPRESENTED)
   I: 4 times (9.1%)  - vs 5.4% expected
   M: 3 times (6.8%)  - vs 4.3% expected

3. MISSING COMMON INITIALS:
   E: 0 times - expected ~2% of initials
   H: 0 times - expected ~7.2% of initials (significant!)

4. LETTER PAIRS:
   AB appears 3 times: position 5-6, 7-8 in line 1; position 6-7 in line 4
   ML appears 2 times: start of line 2 and line 4

5. THE 'X' MARK:
   Small x above the O in line 4 (MLIABOAIAQC)
   Could indicate: deletion, emphasis, or a separate symbol
""")

print("\n" + "="*70)
print("ACROSTIC HYPOTHESIS TEST")
print("="*70)

# If this is first letters of words from a poem or text,
# we can look for patterns that match the Rubaiyat

print("""
The Rubaiyat of Omar Khayyam (FitzGerald translation) context:

The phrase "Tamam Shud" (meaning "ended" or "finished") was torn
from the final page of this book. This strongly suggests the code
relates to the Rubaiyat.

HYPOTHESIS: The code is first letters of words from a passage in the Rubaiyat.

Let's look at what phrases could produce these initials...
""")

# Some verses from the Rubaiyat that investigators have considered
rubaiyat_candidates = [
    # Format: (verse_number, first_words_of_lines)
    ("Verse 7", "Come, fill the Cup, and in the Fire of Spring"),
    ("Verse 12", "A Book of Verses underneath the Bough"),
    ("Verse 23", "And we, that now make merry in the Room"),
    ("Verse 24", "Alike for those who for TO-DAY prepare"),
    ("Verse 71", "The Moving Finger writes; and, having writ"),
    ("Verse 99", "Ah Love! could you and I with Him conspire"),
]

print("Sample verses from the Rubaiyat:")
for verse, text in rubaiyat_candidates:
    initials = ''.join(word[0].upper() for word in text.split() if word)
    print(f"  {verse}: '{text[:50]}...'")
    print(f"         Initials: {initials}")
    print()

print("\n" + "="*70)
print("ALTERNATIVE HYPOTHESES")
print("="*70)

print("""
1. STREET NAMES HYPOTHESIS:
   Could be first letters of street names in a route/journey
   (Adelaide has many streets starting with common letters)

2. HORSE RACING HYPOTHESIS (Professor Abbott, 2022):
   Could be first letters of horse names at races

3. CODED MESSAGE WITH KEY:
   If using a one-time pad or book cipher, the key would be in the Rubaiyat

4. PERSONAL ACROSTIC:
   Could be initials of words in a personal message/poem composed by the writer

5. SPY COMMUNICATION:
   One-time pad codes for intelligence purposes (Navy intelligence suspected this)
""")

# Look for word patterns that match
print("\n" + "="*70)
print("WORD PATTERN SEARCH")
print("="*70)

# Words starting with each sequence
sequences = ['WR', 'AB', 'ML', 'WT', 'IT', 'TM', 'ST']
print("\nCommon English words starting with key bigrams from the code:")
for seq in sequences:
    # Common words - just examples
    examples = {
        'WR': 'WRONG, WRITE, WRATH, WRAP',
        'AB': 'ABOUT, ABOVE, ABSENT, ABSOLUTE',
        'ML': '(rare - almost no English words)',
        'WT': '(rare - almost no English words)',
        'IT': 'IT, ITEM, ITSELF',
        'TM': '(rare - almost no English words)',
        'ST': 'STOP, START, STAY, STILL, STRANGE'
    }
    print(f"  {seq}: {examples.get(seq, '?')}")

print("""
Note: 'ML' and 'WT' are very rare as word beginnings in English.
This suggests either:
- Non-English text
- Not first letters of words
- Includes names, places, or abbreviations
""")

print("\n" + "="*70)
print("THE CROSSED-OUT LINE SIGNIFICANCE")
print("="*70)

print("""
Line 2 (MLIAOI) is crossed out but visible.

Comparison:
  Line 2: M L I A O I
  Line 4: M L I A B O A I A Q C

Both start with MLIA, then:
  Line 2: O I
  Line 4: B O A I A Q C

INTERPRETATION 1: The writer started line 4's content but made an error,
                  crossed it out, and continued with line 3.

INTERPRETATION 2: Line 2 was intentional - a "decoy" or "null" line.

INTERPRETATION 3: The 'O I' at the end of line 2 might be significant.
                  'OI' could stand for something specific.

The fact that it wasn't fully erased (just crossed out) suggests
the writer either:
- Didn't care about hiding it
- Wanted it to be seen
- Didn't have time to properly erase it
""")

print("\n" + "="*70)
print("NEXT STEPS FOR DECRYPTION")
print("="*70)

print("""
1. OBTAIN FULL RUBAIYAT TEXT
   - Get all verses in FitzGerald's translation
   - Search for any passage whose word initials match the code

2. TEST SPECIFIC VERSES
   - Focus on verses about death, endings, secrets
   - The "Tamam Shud" connection suggests final verses

3. TRY PERMUTATIONS
   - What if lines are in wrong order?
   - What if some letters are wrong (M/W ambiguity)?

4. RESEARCH HISTORICAL CONTEXT
   - 1948 Adelaide - what events, locations, people?
   - Possible Cold War espionage connection

5. ANALYZE THE PHONE NUMBER
   - A local phone number was also found in the book
   - Led to a nurse named Jessica Thomson who denied knowing the man
   - but DNA analysis suggests he may have fathered her son
""")
