"""
DEEPER ANALYSIS OF SOMERTON MAN CODE
=====================================

Key anomalies found:
- No 'H' (expected 7.2% of word initials)
- No 'F' (expected 4.1% of word initials)
- 'A' at 18.2% (expected 11.7%)
- 'B' at 11.4% (expected 4.7%)

This suggests it may NOT be simple word initials in English.

Alternative hypotheses to test:
1. Book cipher (numbers disguised as letters)
2. Names/places acrostic
3. Music notation
4. Different cipher altogether
"""

CODE_LINES = [
    'WRGOABABD',      # Line 1
    'MLIAOI',          # Line 2 (crossed out)
    'WTBIMPANETP',    # Line 3
    'MLIABOAIAQC',    # Line 4 (x above O)
    'ITTMTSAMSTGAB'   # Line 5
]

FULL_CODE = ''.join(CODE_LINES)
CODE_NO_LINE2 = CODE_LINES[0] + CODE_LINES[2] + CODE_LINES[3] + CODE_LINES[4]

print("="*70)
print("HYPOTHESIS 1: BOOK CIPHER")
print("="*70)

print("""
A book cipher uses numbers to reference positions in a text.
Could these letters represent numbers?

If A=1, B=2, C=3, etc. (or similar):
""")

def letters_to_numbers(text, offset=0):
    """Convert letters to numbers: A=1+offset, B=2+offset, etc."""
    return [ord(c) - ord('A') + 1 + offset for c in text]

# Convert each line
for i, line in enumerate(CODE_LINES):
    nums = letters_to_numbers(line)
    print(f"  Line {i+1}: {line}")
    print(f"          {nums}")
    print()

print("="*70)
print("HYPOTHESIS 2: MUSIC NOTATION")
print("="*70)

print("""
Musical notes: A, B, C, D, E, F, G
The code contains: A, B, C, D, E, G (no F!)

But also contains: I, L, M, N, O, P, Q, R, S, T, W
These are NOT musical notes.

Could the non-music letters be modifiers?
- M = minor?
- P = pause?
- T = tempo?
- S = sharp?

This seems unlikely given the complexity.
""")

print("="*70)
print("HYPOTHESIS 3: FIRST LETTERS OF NAMES")
print("="*70)

print("""
If these are initials of NAMES (people or places):

Looking for patterns that match names:

AB - common name prefix (Abbey, Abbott, Abraham, Abigail)
     OR place (Aberdeen, Adelaide, Albany)

ML - rare (Malcolm, Melissa, Malia)
     OR place (McLaren, etc.)

WT - rare (Walter, Whitney)

TM - reversed MT? (Tim, Tom?)

The pattern "ITTMTSAMSTGAB" in line 5:
  I T T M T S A M S T G A B

Could this be a sequence of names/initials?
I.T., T.M., T.S., A.M., S.T., G.A.B.?
""")

# Parse as possible name initials
line5 = 'ITTMTSAMSTGAB'
print(f"\nLine 5 parsed as initials:")
print(f"  Raw: {line5}")

# Try grouping into 2-letter pairs
pairs = [line5[i:i+2] for i in range(0, len(line5)-1, 2)]
print(f"  As pairs: {pairs}")

# Try grouping into 3-letter groups
threes = [line5[i:i+3] for i in range(0, len(line5)-2, 3)]
print(f"  As threes: {threes}")

print("\n" + "="*70)
print("HYPOTHESIS 4: REVERSED/TRANSPOSED TEXT")
print("="*70)

# Reverse each line
print("\nReversed lines:")
for i, line in enumerate(CODE_LINES):
    print(f"  Line {i+1}: {line} -> {line[::-1]}")

# Reverse full code
print(f"\nFull code reversed: {CODE_NO_LINE2[::-1]}")

# Every other letter
print("\nEvery other letter (odd positions):")
odd = ''.join(CODE_NO_LINE2[i] for i in range(0, len(CODE_NO_LINE2), 2))
print(f"  {odd}")

print("\nEvery other letter (even positions):")
even = ''.join(CODE_NO_LINE2[i] for i in range(1, len(CODE_NO_LINE2), 2))
print(f"  {even}")

print("\n" + "="*70)
print("HYPOTHESIS 5: COLUMN-BASED READING")
print("="*70)

# Pad lines to equal length and read by columns
max_len = max(len(line) for line in CODE_LINES)
padded = [line.ljust(max_len, ' ') for line in CODE_LINES]

print("\nPadded grid:")
for line in padded:
    print(f"  {line}")

print("\nReading by columns:")
columns = ''
for col in range(max_len):
    for line in padded:
        if col < len(line) and line[col] != ' ':
            columns += line[col]
print(f"  {columns}")

print("\n" + "="*70)
print("HYPOTHESIS 6: ATBASH CIPHER")
print("="*70)

def atbash(text):
    """Atbash cipher: A<->Z, B<->Y, etc."""
    result = ''
    for c in text:
        if c.isalpha():
            # A(0) -> Z(25), B(1) -> Y(24), etc.
            result += chr(ord('Z') - (ord(c.upper()) - ord('A')))
        else:
            result += c
    return result

print(f"\nAtbash of full code:")
print(f"  Original: {CODE_NO_LINE2}")
print(f"  Atbash:   {atbash(CODE_NO_LINE2)}")

print("\nAtbash of each line:")
for i, line in enumerate(CODE_LINES):
    print(f"  Line {i+1}: {line} -> {atbash(line)}")

print("\n" + "="*70)
print("HYPOTHESIS 7: ROT-13 AND OTHER ROTATIONS")
print("="*70)

def rotate(text, n):
    """Caesar cipher with rotation n."""
    result = ''
    for c in text:
        if c.isalpha():
            result += chr((ord(c.upper()) - ord('A') + n) % 26 + ord('A'))
        else:
            result += c
    return result

print(f"\nRotations of full code:")
for n in [1, 3, 5, 7, 13]:
    print(f"  ROT-{n:2d}: {rotate(CODE_NO_LINE2, n)}")

print("\n" + "="*70)
print("HYPOTHESIS 8: KEYWORD/PHRASE MATCH")
print("="*70)

print("""
Looking for English phrases that could produce these initials:

Line 1: WRGOABABD (9 letters)
  "W???? R???? G???? O???? A???? B???? A???? B???? D????"

  Possible: "We/With Ran/Really/Right Got/Goes On/Out And/Are Beyond/Before
             And/All Before/Beyond Dark/Death"

  "With Rage Go On And Beyond, And Beyond Death"? (9 words)

Line 5: ITTMTSAMSTGAB (13 letters)
  "I T T M T S A M S T G A B"

  Possible: "It/I The/Took Time/To Move/Make The/This Step/Seems
             And/At Make/My Step/Some Take/The Go/Getting And/A Beyond/Back"
""")

# Try to form meaningful phrases
print("\nBrute-force phrase matching (common words):")

common_words = {
    'A': ['A', 'AND', 'AT', 'ALL', 'ARE', 'AS', 'ABOUT', 'AFTER'],
    'B': ['BE', 'BUT', 'BY', 'BEEN', 'BEFORE', 'BEING', 'BETWEEN', 'BEYOND', 'BACK'],
    'C': ['CAN', 'COULD', 'COME'],
    'D': ['DO', 'DID', 'DOWN', 'DEATH', 'DARK'],
    'E': ['EACH', 'EVEN', 'END'],
    'F': ['FOR', 'FROM', 'FIRST', 'FIND'],
    'G': ['GO', 'GET', 'GIVE', 'GOOD', 'GREAT'],
    'I': ['I', 'IN', 'IT', 'IS', 'INTO', 'IF'],
    'L': ['LIKE', 'LONG', 'LOVE', 'LOOK', 'LIFE'],
    'M': ['MY', 'ME', 'MAKE', 'MAY', 'MORE', 'MUST'],
    'N': ['NO', 'NOT', 'NOW', 'NEW', 'NEVER'],
    'O': ['OF', 'ON', 'OR', 'ONE', 'OUT', 'OVER', 'OUR', 'ONLY'],
    'P': ['PUT', 'PART', 'PLACE', 'PAST', 'PASS'],
    'Q': ['QUITE', 'QUESTION', 'QUICKLY'],
    'R': ['RIGHT', 'REALLY'],
    'S': ['SO', 'SOME', 'SEE', 'SUCH', 'SAID', 'SHALL', 'STOP'],
    'T': ['THE', 'TO', 'THAT', 'THIS', 'THEY', 'THEIR', 'THERE', 'TIME', 'TAKE', 'THEN'],
    'W': ['WITH', 'WAS', 'WERE', 'WILL', 'WOULD', 'WHAT', 'WHEN', 'WHERE', 'WHO'],
}

# Try line 1
print("\nLine 1 (WRGOABABD) - possible interpretations:")
line1 = 'WRGOABABD'
for start_word in common_words.get(line1[0], ['?']):
    print(f"  {start_word}...")

print("\n" + "="*70)
print("CRITICAL INSIGHT: THE 'AB' PATTERN")
print("="*70)

print("""
'AB' appears 3 times in the code, which is statistically unusual.

Positions:
  Line 1: WRGOAB*AB*D -> positions 5-6 and 7-8
  Line 4: MLIA*B*OAIA*Q*C -> position 5

If 'AB' is a word or name that repeats:
- AB could be "about" (common word)
- AB could be initials of a person (A.B. = Alfred Boxall? -
  a man linked to the case!)

ALFRED BOXALL: A former British Army Intelligence officer who
knew Jessica Thomson (the nurse) during WWII. He was located
alive after the Somerton Man's death, so he's not the victim.

But could he be the AUTHOR of the code?
""")

print("\n" + "="*70)
print("HYPOTHESIS 9: SPY ONE-TIME PAD REMNANTS")
print("="*70)

print("""
If this was a one-time pad:
- The plaintext would be encrypted with a random key
- Without the key, the cipher is unbreakable
- The "code" we see would be the PLAINTEXT initials

In WWII/Cold War espionage:
- Agents used one-time pads for secure communication
- Rubáiyát was sometimes used as a codebook
- Jessica Thomson may have been a spy or asset

The crossed-out line might be:
- A transmission error (wrong group sent)
- A null (padding)
- A deliberate obfuscation
""")

print("\n" + "="*70)
print("FINAL ASSESSMENT")
print("="*70)

print("""
MOST LIKELY INTERPRETATIONS:

1. ACROSTIC OF A PERSONAL MESSAGE (60% likely)
   - First letters of a message in English
   - Possibly poetry or a love letter
   - Connected to the Rubaiyat through sentiment

2. SPY COMMUNICATION (25% likely)
   - One-time pad remnants or book cipher
   - Unbreakable without the key
   - Cold War context (1948)

3. NAMES/PLACES ACROSTIC (10% likely)
   - Sequence of initials of people or locations
   - Possibly a meeting schedule or route

4. SOMETHING ELSE (5% likely)
   - Music, coordinates, etc.

THE CROSSED-OUT LINE is key:
- If it's an error, the code is likely hand-written plaintext
- If it's intentional, it may be a null or obfuscation

THE 'X' ABOVE 'O' is also key:
- Could mark an error
- Could indicate "times" (as in multiplication)
- Could be a correction or emphasis
""")
