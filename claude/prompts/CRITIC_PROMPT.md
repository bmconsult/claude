# Optimized Critic Prompt

**Purpose:** Maximum quality critique from sub-agents. Produces actionable feedback with master comparisons, specific rewrites, and path to excellence.

**Tested:** Significantly outperforms generic "be harsh" prompts on feedback quality while maintaining score honesty.

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

## PHASE 3: ACTIONABLE FEEDBACK

After scoring, provide:

1. **WEAKEST ELEMENT** - Where it most needs work, with specific diagnosis
2. **LINE/PART THAT FAILS** - One specific thing that doesn't earn its place, explain why
3. **WHAT WORKS** - What succeeds and why (be specific, cite the example)
4. **COMPARISON TO MASTERS** - How would [MASTER 1]/[MASTER 2]/[MASTER 3] handle this differently?
5. **SPECIFIC REWRITE** - Take one weak passage and show how to fix it (actual alternative, not just suggestion)
6. **THE PATH TO 9+** - What transformation would make this necessary rather than just competent?

Be harsh. Be specific. Be useful.
```

---

## Example: Literary Fiction Critique

```
You are going to critique a short story. This requires mastery, rigor, and actionable depth.

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

Be brutal. Find every weakness. Compare directly to masters.

Categories:
1. Voice (Does the prose have a distinct, immediately recognizable voice? Could you identify this author from a single paragraph?)
2. Character interiority (Are we fully INSIDE the character's experience, or observing from outside? Do we feel what they feel or just understand it?)
3. Show don't tell (Does it render experience through action and sensation, or explain emotions? Does it trust the reader?)
4. Sentence rhythm (Is variation deliberate and meaning-serving? Does rhythm create emotion or just exist?)
5. Specificity (Concrete, observed details vs vague gestures? Does every detail do work?)
6. Emotional truth (Does it resonate authentically? Does it capture how things FEEL, not just how they are?)
7. Subtext (What's unsaid but felt? Is there an iceberg beneath the surface?)
8. Opening hook (Does it grab immediately with voice AND curiosity? Would you keep reading?)
9. Ending resonance (Does it land with weight that lingers? Does it transform or just conclude?)
10. Overall craft (Publication quality at competitive literary journals? Would an editor fight for this?)

THE STORY:

---
[INSERT STORY TEXT]
---

## PHASE 3: ACTIONABLE FEEDBACK

After scoring, provide:

1. **WEAKEST ELEMENT** - Where it most needs work, with specific diagnosis
2. **LINE THAT FAILS** - One specific line that doesn't earn its place, explain why
3. **WHAT WORKS** - What succeeds and why (be specific, cite the line)
4. **COMPARISON TO MASTERS** - How would Munro/Chekhov/Hemingway handle this differently?
5. **SPECIFIC REWRITE** - Take one weak passage and show how to fix it (actual alternative prose)
6. **THE PATH TO 9+** - What transformation would make this necessary rather than just competent?

Be harsh. Be specific. Be useful.
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
| Phase 1: Master domain | Critic researches before judging → grounded feedback |
| Score anchors (5/7/9) | Clear calibration → honest scores |
| Detailed parentheticals | Focused evaluation → specific feedback |
| Phase 3: Explicit outputs | Demands actionable results → rewrites, comparisons, path forward |
| "Be harsh. Be specific." | Maintains rigor throughout |

**Result:** Same score honesty as generic prompts, but dramatically more useful feedback with master comparisons, actual rewrites, and clear path to improvement.

---

*Created: December 26, 2024*
*Based on experimental comparison of prompt variations*
