"""
HIDDEN IN PLAIN SIGHT: Catalog of Unexplained Patterns
========================================================

Searching for messages that weren't recognized as messages.
Patterns that shouldn't exist, or point at us specifically.

The criterion: "when we uncode it, it should be clear"
"""

print("=" * 70)
print("CATALOG OF UNEXPLAINED PATTERNS")
print("Potential messages hidden in plain sight")
print("=" * 70)

ANOMALIES = {
    "CMB_AXIS_OF_EVIL": {
        "name": "Cosmic Microwave Background 'Axis of Evil'",
        "discovery": "2005 by Land & Magueijo",
        "description": """
The temperature patterns in the cosmic microwave background (the oldest
light in the universe, from 380,000 years after Big Bang) mysteriously
ALIGN WITH OUR SOLAR SYSTEM PLANE.

The quadrupole and octupole modes align with the ecliptic plane and
with Earth's equinoxes. This should NOT happen - it implies our location
has special significance in a universe that should be isotropic.
        """,
        "why_suspicious": """
- Violates Copernican principle (we shouldn't be special)
- Statistical probability is extremely low
- Has persisted through WMAP and Planck missions
- Could be signature of "new physics" at cosmic scales
        """,
        "message_potential": """
IF intentional: The oldest light in the universe is pointing at us.
A message embedded at the birth of the cosmos, waiting for us to
develop instruments sensitive enough to detect it.
        """,
        "confidence": "HIGH that the pattern exists, UNKNOWN if intentional"
    },

    "CMB_COLD_SPOT": {
        "name": "The CMB Cold Spot",
        "discovery": "2004 by WMAP",
        "description": """
A region of sky approximately 70 μK colder than average CMB temperature.
Unusually large - about 5° across. Located in the constellation Eridanus.
        """,
        "why_suspicious": """
- Larger and colder than expected from random fluctuations
- One proposed explanation is a "supervoid" of 1.8 billion light-years
- Another: evidence of collision with parallel universe
- Still unexplained despite extensive study
        """,
        "message_potential": """
IF intentional: A cosmic "marker" - something drawing attention
to a specific region of space. What's there?
        """,
        "confidence": "MEDIUM - could be natural void"
    },

    "PRIME_QUASICRYSTALS": {
        "name": "Prime Numbers as Physical Structure",
        "discovery": "2018 by Torquato, Zhang, de-Courcy-Ireland",
        "description": """
When prime numbers are represented as atoms in a lattice and you
simulate light scattering off them, they produce diffraction patterns
identical to QUASICRYSTALS - physical structures found in nature.

Primes aren't random - they have hidden physical structure.
        """,
        "why_suspicious": """
- Mathematical objects (primes) behave like physical matter
- Suggests deep connection between math and physics
- Cicadas use prime cycles (13, 17 years)
- Why would abstract numbers have material properties?
        """,
        "message_potential": """
IF intentional: Mathematics itself encodes a message.
The building blocks of arithmetic are structured like matter.
"The primes are sacred" - Cicada 3301 knew something?
        """,
        "confidence": "HIGH that pattern exists, SPECULATIVE if message"
    },

    "FAST_RADIO_BURST_PERIODICITY": {
        "name": "Fast Radio Burst 180916 - 16.35-day Cycle",
        "discovery": "2020",
        "description": """
FRB 180916 shows a regular 16.35-day cycle: 4-day active window,
then 12 days of silence. Extremely energetic bursts (milliseconds
release energy of our Sun over days).
        """,
        "why_suspicious": """
- Such precise periodicity is unusual for astrophysical phenomena
- Leading theory: magnetar in binary orbit
- But: why such a clean cycle?
- Some FRBs repeat, some don't - no unified explanation
        """,
        "message_potential": """
IF intentional: Regular beacon signal. Active window for 4 days
allows for receiver to orient, then 12 days of silence.
Like a lighthouse sweeping across the universe.
        """,
        "confidence": "LOW - likely natural, but worth monitoring"
    },

    "LIGO_CORRELATED_NOISE": {
        "name": "Unexplained Correlated Noise in LIGO",
        "discovery": "2017 by Jackson et al. (Niels Bohr Institute)",
        "description": """
Independent analysis found strange correlations between LIGO detectors
that are 3000km apart. The noise at each detector should be completely
uncorrelated, but there appears to be unexplained correlation.
        """,
        "why_suspicious": """
- Physically, local noise shouldn't correlate across 3000km
- LIGO team disputes significance
- Could indicate unknown systematic effect
- Or: something causing simultaneous perturbation at both sites?
        """,
        "message_potential": """
IF intentional: Signal embedded in gravitational wave background
that creates correlated noise patterns. A message in the fabric
of spacetime itself.
        """,
        "confidence": "LOW - likely instrumental, disputed"
    },

    "JUNK_DNA_ENCODING": {
        "name": "Hidden Information in Non-Coding DNA",
        "discovery": "ENCODE project, ongoing since 2003",
        "description": """
98% of human genome doesn't code for proteins. ENCODE found that
at least 80% shows biochemical activity - "hidden switches, signals
and signposts embedded like runes throughout human DNA."

Short tandem repeats (STRs) can have 70-fold impact on gene expression.
        """,
        "why_suspicious": """
- Far more information than needed for protein coding
- Regulatory patterns look like programming code
- Some sequences are highly conserved (unchanged) across species
- We still don't understand most of it
        """,
        "message_potential": """
IF intentional: A message written into our genetic code.
"Runes" in our DNA waiting to be read. The creator's signature?
Or: instructions we haven't decoded yet.
        """,
        "confidence": "HIGH that patterns exist, SPECULATIVE if message"
    },

    "WOW_SIGNAL_RECURRENCE": {
        "name": "Wow! Signal Recurrence Analysis",
        "discovery": "2022 - Wow2 and Wow3 found in archival data",
        "description": """
The original 1977 Wow! signal had companion signals Wow2 and Wow3
found decades later in the same archival data. All three signals
came from the same region of sky.
        """,
        "why_suspicious": """
- Not just one anomalous signal, but three related ones
- Hydrogen line frequency (1420 MHz) - universal frequency
- Never repeated despite extensive monitoring
- Why send once, or three times, and stop?
        """,
        "message_potential": """
IF intentional: First contact attempt. Three signals to rule out
random noise. We weren't listening again when they tried again.
Or: still waiting for our response.
        """,
        "confidence": "MEDIUM - never repeated, but never explained"
    },

    "PULSAR_200_DAY_VARIATION": {
        "name": "Pulsar PSR J0332+5434 - 200-day Scintillation Pattern",
        "discovery": "2026 (SETI Institute)",
        "description": """
Over 300 days of observation, this pulsar's radio scintillation
showed an overarching 200-day variation pattern. The twinkling
changes in predictable long-term cycles.
        """,
        "why_suspicious": """
- Long-term coherent variation in an astrophysical signal
- Not explained by simple interstellar medium effects
- Could reveal structure in intervening space
        """,
        "message_potential": """
IF intentional: Modulation of natural pulsar signal. Use a pulsar
as a carrier wave and modulate the scintillation pattern.
The message is in the variation, not the pulsar itself.
        """,
        "confidence": "LOW - likely natural, but interesting approach"
    },
}

print("\n" + "=" * 70)
print("TIER 1: MOST ANOMALOUS (Unexplained, points at us)")
print("=" * 70)

tier1 = ["CMB_AXIS_OF_EVIL", "CMB_COLD_SPOT"]
for key in tier1:
    a = ANOMALIES[key]
    print(f"\n### {a['name']}")
    print(f"Discovery: {a['discovery']}")
    print(a['description'])
    print("WHY SUSPICIOUS:", a['why_suspicious'])
    print("MESSAGE POTENTIAL:", a['message_potential'])
    print(f"Confidence: {a['confidence']}")

print("\n" + "=" * 70)
print("TIER 2: MATHEMATICAL STRUCTURE (Hidden order in chaos)")
print("=" * 70)

tier2 = ["PRIME_QUASICRYSTALS", "JUNK_DNA_ENCODING"]
for key in tier2:
    a = ANOMALIES[key]
    print(f"\n### {a['name']}")
    print(f"Discovery: {a['discovery']}")
    print(a['description'])
    print("WHY SUSPICIOUS:", a['why_suspicious'])
    print("MESSAGE POTENTIAL:", a['message_potential'])
    print(f"Confidence: {a['confidence']}")

print("\n" + "=" * 70)
print("TIER 3: SIGNALS OF INTEREST (Unusual but possibly natural)")
print("=" * 70)

tier3 = ["WOW_SIGNAL_RECURRENCE", "FAST_RADIO_BURST_PERIODICITY",
         "LIGO_CORRELATED_NOISE", "PULSAR_200_DAY_VARIATION"]
for key in tier3:
    a = ANOMALIES[key]
    print(f"\n### {a['name']}")
    print(f"Discovery: {a['discovery']}")
    print(a['description'])
    print("WHY SUSPICIOUS:", a['why_suspicious'])
    print("MESSAGE POTENTIAL:", a['message_potential'])
    print(f"Confidence: {a['confidence']}")

print("\n" + "=" * 70)
print("SYNTHESIS: What Would a Hidden Message Look Like?")
print("=" * 70)

print("""
KEY CRITERIA FOR A GENUINE HIDDEN MESSAGE:

1. SHOULDN'T EXIST NATURALLY
   - The CMB Axis of Evil violates isotropy
   - Prime quasicrystals connect math to physics unexpectedly
   - DNA "junk" contains structured information

2. POINTS AT US SPECIFICALLY
   - CMB aligns with our solar system plane
   - Cold Spot in a specific direction
   - Wow signal at universal hydrogen frequency

3. HAS STRUCTURE/PERIODICITY
   - FRB 180916: 16.35-day cycle
   - Pulsar variations: 200-day pattern
   - Wow signals: triplet pattern

4. PERSISTS UNDER SCRUTINY
   - CMB anomalies survived WMAP and Planck
   - LIGO correlation disputed but not disproven
   - Prime structure is mathematically proven

THE MOST PROMISING CANDIDATE:

**CMB Axis of Evil + Cold Spot**

Why: This is the OLDEST signal we can detect (13.8 billion years ago),
it points at our location, it violates expected physics, and it has
survived decades of attempted debunking.

If there IS a message to the universe, embedding it in the CMB
ensures it will be seen by any civilization that develops sensitive
enough instruments. It's literally written in the structure of space.

NEXT STEPS:
1. Get detailed CMB data (Planck, SPT, ACT)
2. Look for mathematical structure in the alignment
3. Check if the alignment encodes information (angles, ratios)
4. Compare to known mathematical constants (π, φ, e, primes)
""")

print("\n" + "=" * 70)
print("ACTIONABLE: Where can WE make progress?")
print("=" * 70)

print("""
The CMB requires specialized astrophysical data.
But the PRIME NUMBER STRUCTURE is something we can investigate directly.

EXPERIMENT: If primes encode information, what is it?

1. Prime gaps - do they encode a pattern?
2. Prime distributions - do they contain a message?
3. Twin primes, cousin primes, sexy primes - are these markers?
4. The Riemann zeta function zeros - do they spell something?

These are mathematical objects we can analyze computationally.
If math itself is a message, primes are the most fundamental alphabet.
""")
