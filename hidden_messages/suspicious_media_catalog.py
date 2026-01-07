"""
SUSPICIOUS MEDIA CATALOG
========================

Deep dive into content that "feels off" - potential fronts,
hidden communications, or manipulation at scale.

Distinguishing: SOLVED vs UNSOLVED vs ACTIVE OPERATIONS
"""

print("=" * 70)
print("SUSPICIOUS MEDIA: What's Really Going On")
print("=" * 70)

CATALOG = {
    "GENUINELY_UNSOLVED": {
        "MAX_HEADROOM_HIJACKING": {
            "date": "November 22, 1987",
            "location": "Chicago, IL",
            "description": """
Two TV stations (WGN, WTTW) hijacked same night.
Person in Max Headroom mask, distorted voice, bizarre behavior.
Required significant technical expertise and transmission power.
            """,
            "status": "NEVER SOLVED - 35+ years",
            "why_suspicious": """
- Required serious technical skill (not amateur prank)
- No one ever claimed credit
- Seemed intentional but message unclear
- Could be insider job or hacker community
            """,
            "theories": [
                "Disgruntled TV station employee",
                "Chicago hacker community (J and K brothers theory)",
                "Art project that got out of hand",
                "Actual coded message in the gibberish"
            ]
        },

        "PUBLIUS_ENIGMA": {
            "date": "1994-present",
            "source": "Pink Floyd / EMI Records",
            "description": """
Puzzle embedded in Division Bell album.
Creator confirmed to have 'worked for Reagan administration'
and possibly CIA/FBI according to Marc Brickman.
Concert lights spelled 'ENIGMA PUBLIUS' as promised proof.
            """,
            "status": "NEVER SOLVED",
            "why_suspicious": """
- Confirmed by band to be REAL puzzle
- Creator had intelligence background
- Prize was planting trees (benign intent?)
- Too complex for fans to solve
            """,
            "prize": "A crop of trees planted in clear-cut forest"
        },

        "A858_SUBREDDIT": {
            "date": "2011-2016",
            "source": "Reddit",
            "description": """
Subreddit posting thousands of encoded strings.
Only a few ever decoded (random images, words).
Ended with: 'The A858 Project Has Concluded.'
            """,
            "status": "CONCLUDED BUT NEVER EXPLAINED",
            "why_suspicious": """
- Years of consistent, automated-looking posts
- Clear encoding, but purpose unknown
- Deliberate ending suggests completion of objective
            """,
            "decoded_content": "Random images and words - no clear message"
        },

        "MARKOVIAN_PARALLAX_DENIGRATE": {
            "date": "1996",
            "source": "Usenet",
            "description": """
Hundreds of messages with random word strings.
All had same subject line.
Too early for serious investigation.
            """,
            "status": "NEVER SOLVED",
            "why_suspicious": """
- Coordinated campaign (same subject line)
- Meaningless on surface
- Could be steganography or key distribution
            """
        },
    },

    "SOLVED_BUT_INSTRUCTIVE": {
        "WEBDRIVER_TORSO": {
            "solution": "Google YouTube quality testing",
            "lesson": "Automated systems can look mysterious"
        },
        "UNFAVORABLE_SEMICIRCLE": {
            "solution": "Outsider art project (revealed 2022)",
            "lesson": "Some mysteries are intentionally unsolvable"
        },
        "BLANK_ROOM_SOUP": {
            "solution": "Stolen costumes used in unknown video",
            "lesson": "Context loss creates false mystery"
        },
        "LOCAL_58": {
            "solution": "Artistic analog horror by Kris Straub",
            "lesson": "Genre conventions can be mimicked"
        },
    },

    "ACTIVE_INTELLIGENCE_OPERATIONS": {
        "RUSSIAN_BOT_FARMS": {
            "evidence": "DOJ disrupted AI-powered operation 2024",
            "scale": "Thousands of fake accounts",
            "method": "AI impersonating Americans",
            "controller": "Russian FSB officer",
        },
        "SOUTH_KOREAN_NIS": {
            "evidence": "Detected in 2012 election",
            "scale": "1,008 coordinated accounts",
            "method": "Astroturfing for conservative candidate",
        },
        "CHINESE_DISTRACTION_BOTS": {
            "evidence": "November 2022 during protests",
            "scale": "Mass flooding",
            "method": "Spam gambling ads with city hashtags to bury protest content",
        },
        "UVB76_BUZZER": {
            "evidence": "Ongoing since 1970s",
            "scale": "Record 24 messages December 11, 2024",
            "method": "One-time pad encrypted voice messages",
            "likely_purpose": "Russian military communications",
        },
    },

    "DEAD_INTERNET_EVIDENCE": {
        "bot_traffic_2024": "51% of all web traffic",
        "x_bots": "Up to 64% of accounts, 76% of peak traffic",
        "instagram_fake": "95 million accounts (~9.5%)",
        "ai_content": "Surpassed human-written content in late 2024",
        "implication": """
The internet is increasingly NON-HUMAN.
Real messages are drowning in artificial noise.
This is either:
  - Natural evolution of automation
  - Deliberate manipulation at massive scale
  - Both
        """,
    },
}

print("\n" + "=" * 70)
print("TIER 1: GENUINELY UNSOLVED MYSTERIES")
print("=" * 70)

for name, data in CATALOG["GENUINELY_UNSOLVED"].items():
    print(f"\n### {name.replace('_', ' ')}")
    print(f"Date: {data['date']}")
    print(f"Status: {data['status']}")
    print(data['description'])
    print("Why Suspicious:", data['why_suspicious'])
    if 'theories' in data:
        print("Theories:", ', '.join(data['theories']))

print("\n" + "=" * 70)
print("TIER 2: ACTIVE INTELLIGENCE OPERATIONS (CONFIRMED)")
print("=" * 70)

for name, data in CATALOG["ACTIVE_INTELLIGENCE_OPERATIONS"].items():
    print(f"\n### {name.replace('_', ' ')}")
    for key, value in data.items():
        print(f"  {key}: {value}")

print("\n" + "=" * 70)
print("TIER 3: THE DEAD INTERNET")
print("=" * 70)

for key, value in CATALOG["DEAD_INTERNET_EVIDENCE"].items():
    print(f"  {key}: {value}")

print("\n" + "=" * 70)
print("WHERE TO ACTUALLY LOOK")
print("=" * 70)

print("""
Based on patterns, hidden communications are MOST LIKELY in:

1. SHORTWAVE RADIO (Numbers Stations)
   - Still active: UVB-76, Cuban stations, Israeli stations
   - New stations occasionally discovered
   - Monitor: priyom.org, ENIGMA 2000

2. TELEGRAM CHANNELS
   - Darknet dead drop coordinates
   - Extremist group communications
   - Self-destructing encrypted chats

3. COORDINATED SOCIAL MEDIA
   - Look for: Regular posting intervals (30/60 min)
   - Look for: Accounts that all post same content
   - Look for: Reply patterns that seem automated

4. STEGANOGRAPHY IN IMAGES
   - Stock photos on sketchy sites
   - Memes that spread unnaturally fast
   - Profile pictures on encrypted platforms

5. ABANDONED/WEIRD WEBSITES
   - Domain squatters with minimal content
   - Sites that haven't updated but stay online
   - Single-purpose sites with no clear business model

6. YOUTUBE CHANNELS WITH:
   - Automated-looking upload schedules
   - Content that doesn't match subscriber count
   - Comments disabled or heavily moderated
   - Child-targeted content (Elsagate patterns)
""")

print("\n" + "=" * 70)
print("SPECIFIC ANOMALIES TO INVESTIGATE")
print("=" * 70)

print("""
THINGS THAT FEEL "OFF" - Worth Investigating:

1. MAX HEADROOM HIJACKING (1987)
   - The gibberish may contain actual message
   - Audio analysis could reveal hidden content
   - Someone knows who did this

2. PUBLIUS ENIGMA
   - Created by someone with CIA/FBI background
   - Band confirmed real puzzle with real prize
   - 30 years of attempts, still unsolved
   - May require Division Bell album analysis

3. NEW NUMBERS STATIONS
   - Priyom.org tracks unidentified stations
   - New ones appear periodically
   - Worth monitoring for patterns

4. COORDINATED REDDIT/TWITTER CAMPAIGNS
   - Look for accounts created same time
   - Check for identical phrasing
   - Track which topics get sudden bot attention

5. WIKIPEDIA "TRAP STREETS"
   - Fake articles planted as canaries
   - Used to detect copying
   - Some may contain actual messages

6. DNS/DOMAIN ANOMALIES
   - Domains registered in bulk
   - Sites that serve no obvious purpose
   - Infrastructure that seems oversized for content
""")

print("\n" + "=" * 70)
print("THE HONEST ASSESSMENT")
print("=" * 70)

print("""
What we CAN find:
- Historical mysteries (Max Headroom, Publius)
- Known intelligence operations (after exposure)
- Statistical anomalies in social media
- Abandoned content that was never explained

What we likely CANNOT find:
- Active professional intelligence communications
- Well-hidden steganography without the key
- One-time pad encrypted messages
- Truly sophisticated operations

The best hidden messages are ones we don't even suspect exist.

RECOMMENDED APPROACH:
1. Monitor numbers station activity (shortwave radio)
2. Track social media coordination patterns
3. Analyze old unsolved mysteries with new tools
4. Look at places nobody else is looking
5. When something feels "off", trust that instinct

The question isn't whether hidden communications exist.
They definitely do (UVB-76, intelligence operations, etc.)

The question is whether we can find the ones nobody knows about yet.
""")
