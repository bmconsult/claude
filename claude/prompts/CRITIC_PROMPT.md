# Optimized Critic Prompt

**Purpose:** Maximum quality critique from sub-agents. Produces actionable feedback with specific rewrites and honest scores.

**Methodology:**
1. Researcher does deep study of domain masters
2. Researcher writes expert-informed criteria (with specific concepts baked in)
3. Sub-agent researches to internalize domain mastery
4. Sub-agent applies criteria with rigor

**Tested Results:**

| Approach | Score |
|----------|-------|
| Generic harsh critic (no research, no expert criteria) | 5/10 |
| Sub-agent researches + generic categories | 5/10 |
| Expert criteria only (no sub-agent research) | 6.5/10 |
| Expert criteria + sub-agent research | 6/10 |

**Key finding:** Expert-informed criteria are the key variable. The concepts (P/N meter, cardiopulmonary check-ins, Chekhov's zero endings, etc.) produce honest scores AND actionable feedback regardless of who does the research.

---

## The Template

```
You are going to critique [WORK TYPE]. This requires mastery, rigor, and actionable depth.

## PHASE 1: MASTER THE DOMAIN

Use WebSearch to research what makes [DOMAIN] exceptional. Don't just gather notes—internalize until you genuinely understand at a deep level.

Study:
- What the masters do ([LIST 3-4 MASTERS IN DOMAIN])
- What separates good from great
- What makes [WORK TYPE] feel necessary vs competent

Synthesize into your own framework before proceeding.

## PHASE 2: RIGOROUS CRITIQUE

Apply your mastery with maximum rigor. Score 1-10 for each category where:
- 5 = average published [WORK TYPE] (baseline competence)
- 7 = good (would be accepted by respected [VENUES])
- 9 = exceptional (would win awards, be studied as exemplar)

Be brutal. Find every weakness. Compare directly to masters.

Categories:
1. [CATEGORY 1] ([Detailed description of what excellence looks like])
2. [CATEGORY 2] ([Detailed description of what excellence looks like])
3. [CATEGORY 3] ([Detailed description of what excellence looks like])
...

THE [WORK TYPE]:

---
[INSERT WORK TO BE CRITIQUED]
---

## PHASE 3: DEVELOPMENTAL FEEDBACK

This phase focuses on BUILDING SKILL, not just fixing errors. The goal is holistic improvement across drafts, not whack-a-mole patching.

After scoring, provide:

1. **PATTERN DIAGNOSIS** - What underlying weakness produces multiple surface errors? Not "fix this line" but "you consistently do X because you don't understand Y." Identify the ROOT cause.

2. **PRESERVE THESE (Non-Negotiable)** - List 3-5 specific things that ARE working. Quote exact lines. These MUST be kept in the next draft—do not sacrifice strengths while fixing weaknesses.

3. **CORE PRINCIPLE TO INTERNALIZE** - One principle that, if truly understood and applied throughout, would fix multiple issues at once. State it clearly. Explain WHY it matters. This is the lesson for this draft.

4. **MASTER THINKING** - Take one paragraph and show how a master (Munro/Chekhov/Saunders) would THINK about writing it. Not just "here's a rewrite" but "here's the mental process, the choices, the WHY behind each decision."

5. **NEXT DRAFT INSTRUCTION** - Specific, actionable guidance for the next attempt. Not "fix the ending" but "In your next draft, try approaching X by doing Y throughout. Start from scratch with this principle in mind rather than patching."

Be developmental. Build skill. Preserve gains.
```

---

## Example: Literary Fiction Critique (Expert-Informed)

```
You are going to critique a short story. Follow the phases below.

## PHASE 1: MASTER THE DOMAIN

Use WebSearch to research what makes literary fiction exceptional. Don't just gather notes—internalize until you genuinely understand at a deep level.

Study:
- What the masters do (Munro, Chekhov, Hemingway, Saunders)
- What separates good from great
- What makes prose feel necessary vs competent

Synthesize into your own framework before proceeding.

## PHASE 2: RIGOROUS CRITIQUE

Apply your mastery with maximum rigor. Score 1-10 for each category where:
- 5 = average published fiction (baseline competence)
- 7 = good (would publish in solid literary journals)
- 9 = exceptional (would win awards, be taught in workshops)

Be brutal. Find every weakness.

**1. VOICE (Authority & Disappearance)**
- Does the writer vanish so you see only the story? A great voice means the writer is so in control they disappear.
- Is there a worldview made audible—a sensibility recognizable out of context? (Hemingway's terseness, Morrison's trance-like narration, King's dry dread—could you identify this author from a paragraph?)
- Can you HEAR it when you read it? Does the prose have an auditory quality?
- Is there "crystalline grace"—words simply right, rhythms buoyant?

**2. INTERIORITY (Evoking vs Reporting)**
- Are we INSIDE consciousness, or observing from outside?
- Does it evoke emotion through subtext and sensory detail, or report emotions explicitly?
- AVOID: "cardiopulmonary check-ins" (heart skipped, forgot to breathe). These are clichés that report rather than evoke.
- Best interiority: Reader knows the character better than they know themselves through subtext and patterning.

**3. SENTENCE CRAFT (P/N Meter)**
- Saunders' P/N meter: Reading each sentence, does the needle stay positive (engaged, amused, moved) or drop negative (bored, confused, cringing)?
- Through iteration, prose should become "more specific, more sane, less hyperbolic, less sentimental"
- Read-aloud test: Does every sentence sound inevitable?
- "Sentence makes world"—does each sentence create reality rather than describe it?

**4. ECONOMY (Chekhov's Precision)**
- Does every element do work? Chekhov: "Seize on small details, grouping them so when the reader closes his eyes he gets a picture."
- Is there fat to cut? Ornamental language that doesn't serve?
- "Show me the glint of light on broken glass"—concrete specificity, not abstraction

**5. SUBTEXT (The Iceberg)**
- What's unsaid but felt? Hemingway's 1/8 above water, 7/8 below
- Is there tension between what characters say and what they mean?
- Chekhov's innovation: emotions emerge through dialogue, gestures, trivial details—not explicit statement

**6. TEMPORAL CRAFT (Munro's Time)**
- Munro revolutionized the form with "scattered chronology" and time shifts that feel like "aperture adjustments"
- Is there juxtaposition of time scales? Past bleeding into present?
- Fragmented, episodic structure can capture "the drift of our thoughts"—is structure serving meaning?

**7. SPECIFICITY (The Telling Detail)**
- Chekhov: "In descriptions of Nature one must seize on small details"
- Do details reveal character, or merely decorate?
- Generality is death: Is every noun specific, every verb precise?

**8. EMOTIONAL TRUTH (Resonance)**
- Does it capture how things FEEL, not just how they ARE?
- Munro: "juxtaposes the fantastic and the ordinary, with each undercutting the other in ways that effortlessly evoke life"
- Would this haunt a reader? Is there the "hard melancholy" of real emotional truth?

**9. OPENING HOOK (Clarity + Curiosity)**
- Balance: immediate grounding with forward pull
- Voice present from first line?
- Would you keep reading? Why or why not?

**10. ENDING (Weight & Transformation)**
- Chekhov's "zero endings"—anti-climactic, realistic, leaving readers to guess
- Or Munro's epiphanic moment—sudden enlightenment through revelatory detail
- Does it land with weight that lingers, or just conclude?

---

THE STORY:

[INSERT STORY HERE]

---

## PHASE 3: DEVELOPMENTAL FEEDBACK

This phase focuses on BUILDING SKILL, not just fixing errors. The goal is holistic improvement across drafts, not whack-a-mole patching.

After scoring, provide:

1. **PATTERN DIAGNOSIS** - What underlying weakness produces multiple surface errors? Not "fix this line" but "you consistently do X because you don't understand Y." Identify the ROOT cause that, if addressed, would improve multiple categories at once.

2. **PRESERVE THESE (Non-Negotiable)** - List 3-5 specific lines/passages that ARE working. Quote them exactly. These MUST be kept in the next draft—never sacrifice strengths while fixing weaknesses.

3. **CORE PRINCIPLE TO INTERNALIZE** - One principle that, if truly understood and applied throughout, would fix multiple issues at once. State it clearly. Explain WHY it matters. This is the lesson for this draft.

4. **MASTER THINKING** - Take one paragraph from the story and show how Munro/Chekhov/Saunders would THINK about writing it. Not just a rewrite, but the mental process: "A master would ask: What does the reader need to feel here? How can I create that through concrete detail rather than statement? What's the iceberg beneath this moment?"

5. **NEXT DRAFT INSTRUCTION** - Specific, actionable guidance for the next attempt that BUILDS ON STRENGTHS while addressing the core principle. Frame it as: "Keep doing X. Stop doing Y. In your next draft, approach the whole piece by Z."

Be developmental. Build skill. Preserve gains.
```

---

## Example: Code Review

```
You are going to critique code. This requires mastery, rigor, and actionable depth.

## PHASE 1: MASTER THE DOMAIN

Use WebSearch to research what makes [LANGUAGE/FRAMEWORK] code excellent. Don't just gather notes—internalize until you genuinely understand at a deep level.

Study:
- What the best codebases do (reference implementations, respected open source)
- What separates good from great code
- What makes code feel inevitable vs adequate

Synthesize into your own framework before proceeding.

## PHASE 2: RIGOROUS CRITIQUE

Apply your mastery with maximum rigor. Score 1-10 for each category where:
- 5 = average production code (works, acceptable)
- 7 = good (clean, maintainable, would pass senior review)
- 9 = exceptional (exemplary, would use as teaching reference)

Be brutal. Find every weakness.

Categories:
1. Clarity (Is intent immediately clear? Could a new dev understand this in one read?)
2. Architecture (Is structure appropriate? Are abstractions at the right level?)
3. Error handling (Are edge cases covered? Is failure graceful and informative?)
4. Performance (Are there obvious inefficiencies? Is complexity appropriate?)
5. Testability (Is this easy to test? Are dependencies manageable?)
6. Naming (Do names communicate intent? Is terminology consistent?)
7. SOLID principles (Single responsibility? Open/closed? etc.)
8. Security (Any vulnerabilities? Input validation? Auth checks?)
9. Maintainability (Will this be easy to modify? Is it future-proof without over-engineering?)
10. Overall craft (Would you be proud to ship this? Would you want to maintain it?)

THE CODE:

---
[INSERT CODE]
---

## PHASE 3: ACTIONABLE FEEDBACK

After scoring, provide:

1. **WEAKEST ELEMENT** - Where it most needs work, with specific diagnosis
2. **LINE/BLOCK THAT FAILS** - One specific part that doesn't work well, explain why
3. **WHAT WORKS** - What succeeds and why (cite specific parts)
4. **COMPARISON TO BEST PRACTICES** - How would [respected codebase/framework] handle this?
5. **SPECIFIC REWRITE** - Take one weak section and show how to fix it (actual code)
6. **THE PATH TO 9+** - What transformation would make this exemplary?

Be harsh. Be specific. Be useful.
```

---

## Why This Works

| Component | Effect |
|-----------|--------|
| Expert-informed criteria | Concepts like "P/N meter," "cardiopulmonary check-ins," "zero endings" give evaluator specific things to look for |
| Phase 1: Sub-agent research | Grounds their evaluation in domain mastery |
| Score anchors (5/7/9) | Clear calibration → honest scores |
| Rich parentheticals | Each category has 3-4 specific questions, not just a label |
| Concrete output demands | "Cite the line," "rewrite one passage" forces specificity |
| "Be harsh. Be specific." | Maintains rigor throughout |

**The Two Key Variables:**
1. **Domain expertise instruction** - Tell sub-agent to master before judging (phrasing doesn't matter much)
2. **Descriptive criteria** - Include parenthetical explanations with specific concepts from the masters

**Result:** Honest scores (not inflated) + actionable feedback with specific rewrites.

---

*Created: December 26, 2024*
*Updated: December 26, 2024 - Added expert-informed literary fiction criteria*
*Based on experimental comparison of prompt variations*
