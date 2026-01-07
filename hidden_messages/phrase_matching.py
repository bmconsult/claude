"""
CREATIVE PHRASE MATCHING FOR SOMERTON MAN CODE
==============================================

Attempting to construct English phrases that produce the exact initials.

Context clues:
- Found in Rubaiyat of Omar Khayyam (Persian poetry about love, death, fate)
- "Tamam Shud" = "It is finished" torn from final page
- Possible spy connection (Cold War 1948)
- Possible love letter (linked to Jessica Thomson)
- Possible suicide note

The code again:
Line 1: WRGOABABD     (9 words)
Line 2: MLIAOI        (6 words, crossed out)
Line 3: WTBIMPANETP   (11 words)
Line 4: MLIABOAIAQC   (11 words)
Line 5: ITTMTSAMSTGAB (13 words)

Total: 50 words if including crossed-out line
"""

# The patterns to match
patterns = {
    'line1': 'WRGOABABD',
    'line2': 'MLIAOI',
    'line3': 'WTBIMPANETP',
    'line4': 'MLIABOAIAQC',
    'line5': 'ITTMTSAMSTGAB'
}

print("="*70)
print("ATTEMPTING PHRASE RECONSTRUCTION")
print("="*70)

# Key insight: The Rubaiyat is about love, death, and the fleeting nature of life
# Common themes: wine, love, death, time, fate, garden, roses, beauty

print("""
THEMATIC WORD CANDIDATES (Rubaiyat themes):

Starting with W: With, Was, Were, Wine, Would, When, Where, Wrath, World, Why
Starting with R: Rose, Right, Remember, Regret, Return, Remain
Starting with G: Go, Gone, Gone, Garden, Give, Gave, Get, Got
Starting with O: Of, Our, On, One, Only, Over, Out
Starting with A: And, As, At, All, About, After, Am, Are, Away
Starting with B: But, By, Be, Been, Before, Beyond, Back, Beautiful
Starting with D: Death, Die, Do, Did, Done, Down, Dark

Starting with M: My, Me, More, Make, Made, Must, May, Might
Starting with L: Love, Loved, Life, Like, Long, Lost, Last, Leave
Starting with I: I, In, It, Is, Into, If
Starting with T: The, To, That, This, They, Their, There, Then, Time, Take
Starting with P: Perhaps, Pass, Past, Place
Starting with N: Not, Now, No, Never, Night
Starting with E: Ever, End, Even
Starting with S: So, Some, Such, Said, Shall, Still, Stay
Starting with Q: Quite, Question (rare)
Starting with C: Come, Can, Could, Cup
""")

print("\n" + "="*70)
print("LINE-BY-LINE RECONSTRUCTION ATTEMPTS")
print("="*70)

# Line 1: WRGOABABD
print("""
LINE 1: W R G O A B A B D

Attempt 1 (love theme):
  "With Roses Gone, Our Affection Beyond All Bounds Dies"
  W     R     G     O   A         B      A   B      D
  ✓ 9 words, matches!

Attempt 2 (death theme):
  "When Resting, Go On And Be At Blessed Death"
  W     R        G  O  A   B  A  B       D
  ✓ 9 words, matches! (if "At" counts)

Attempt 3 (journey theme):
  "We Ran, Got Out And Began A Bold Dash"
  W  R    G   O   A   B     A B    D
  ✓ 9 words, matches!

Attempt 4 (regret theme):
  "With Regret Gone, Only Ashes Burn And Blackened Dreams"
  W    R      G     O    A      B    A   B        D
  ✓ 9 words, matches!
""")

# Line 2: MLIAOI (crossed out)
print("""
LINE 2 (CROSSED OUT): M L I A O I

This line starts like Line 4 (MLIA...) - suggests it was started wrongly

Attempt 1:
  "My Love Is Always On Ice" (cold/distant?)
  M  L    I  A      O  I
  ✓ 6 words

Attempt 2:
  "Must Leave, I Am Over It"
  M    L      I A  O    I
  ✓ 6 words

Attempt 3:
  "My Life Is Almost Over Indeed"
  M  L    I  A      O    I
  ✓ 6 words - poignant given suicide theory
""")

# Line 3: WTBIMPANETP
print("""
LINE 3: W T B I M P A N E T P

Attempt 1:
  "With Time, Beauty In Me Passes And Now Even The Pain"
  W    T     B      I  M  P      A   N   E    T   P
  ✓ 11 words

Attempt 2:
  "We Two, Bound In Marriage, Part And Now End This Pact"
  W  T    B     I  M         P    A   N   E   T    P
  ✓ 11 words - divorce/separation?

Attempt 3:
  "What Time Brings Is Most Precious And Never Ends Truly Permanent"
  W    T    B      I  M    P        A   N     E    T     P
  ✓ 11 words
""")

# Line 4: MLIABOAIAQC
print("""
LINE 4: M L I A B O A I A Q C

The 'x' above the O might indicate:
- A correction (O should be something else)
- Multiplication (as in "times")
- A cross/kiss symbol

Attempt 1:
  "My Love Is Abandoned Because Of An Irrevocable And Quiet Conclusion"
  M  L    I  A         B       O  A  I           A   Q     C
  ✓ 11 words

Attempt 2:
  "Must Leave, I Accept Being Over And In Anguish, Quietly Cry"
  M    L      I A      B     O    A   I  A        Q       C
  ✓ 11 words

Attempt 3:
  "My Life, I Acknowledge, Became Only A Illusion And Quickly Crumbled"
  M  L     I A            B      O    A I        A   Q       C
  ✓ 11 words
""")

# Line 5: ITTMTSAMSTGAB
print("""
LINE 5: I T T M T S A M S T G A B

Attempt 1:
  "I Took The Moment To Say A Message, So That God Accepts Both"
  I T    T   M      T  S   A M        S  T    G   A       B
  ✓ 13 words

Attempt 2:
  "It Took Too Much To Say A Meaningful Sentiment To Get A Breakthrough"
  I  T    T   M    T  S   A M          S         T  G   A B
  ✓ 13 words

Attempt 3:
  "I Trust That My Time Shall Arrive, Most Surely Then God Answers Beautifully"
  I T     T    M  T    S     A       M    S      T    G   A       B
  ✓ 13 words
""")

print("\n" + "="*70)
print("COMPLETE MESSAGE RECONSTRUCTION (Best Attempt)")
print("="*70)

print("""
THEME: A love letter/farewell from someone facing death

Line 1: "With Roses Gone, Our Affection Beyond All Bounds Dies"
         (The relationship has ended, love has died)

Line 2: "My Life Is Almost Over Indeed" [CROSSED OUT]
         (He started to write about his death, then crossed it out)

Line 3: "With Time, Beauty In Me Passes And Now Even The Pain"
         (Reflecting on aging and loss)

Line 4: "My Love Is Abandoned Because Of An Irrevocable And Quiet Conclusion"
         (His love is abandoned because of a final, quiet decision - suicide?)
         [The 'x' above O might be a kiss symbol]

Line 5: "I Took The Moment To Say A Message, So That God Accepts Both"
         (He's leaving a final message hoping for forgiveness for both of them)

COMBINED MEANING:
A man writing a farewell to a lost love (Jessica Thomson?), acknowledging
that their relationship ended, he's facing the end, and hoping for peace.

This fits:
✓ The Rubaiyat themes (love, death, transience)
✓ "Tamam Shud" = "It is finished"
✓ The crossed-out line (changed his mind about being too explicit)
✓ The 'x' mark (a kiss to his love)
✓ The mystery of his unidentified body
✓ Jessica Thomson's denial and apparent distress
""")

print("\n" + "="*70)
print("ALTERNATIVE: SPY COMMUNICATION")
print("="*70)

print("""
If this is spy code, the letters might mean:

Line 1: WRGOABABD
  "Wire Report Gained, Operation Alpha Bravo Alpha Bravo Delta"
  (Military/spy phonetic alphabet mixed with instructions)

Line 4: MLIABOAIAQC
  "Message Location Is At Base Of Angel, Item At Quebec Charlie"
  (Location and item codes)

However, this seems LESS likely because:
- The crossed-out line suggests personal writing, not coded transmission
- The Rubaiyat connection is too specific for random spy communication
- The emotional resonance of the Tamam Shud phrase
""")

print("\n" + "="*70)
print("CONFIDENCE ASSESSMENT")
print("="*70)

print("""
MOST LIKELY INTERPRETATION: Personal acrostic (love letter/farewell)

Confidence: ~40%

Why not higher:
- We can't VERIFY any reconstruction
- Multiple valid phrase combinations exist
- The true meaning died with the Somerton Man

What would confirm it:
- Finding a similar message in the Rubaiyat
- Historical evidence linking phrases to the era/location
- Decryption of related codes (phone number, etc.)

This remains UNSOLVED but our analysis suggests it's likely a
personal, emotional message rather than spy communication.
""")
