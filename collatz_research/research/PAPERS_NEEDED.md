# Papers and Documents Needed for Collatz Research

**Purpose**: Papers blocked by 403 errors or otherwise inaccessible that could help close the remaining gap.

---

## Priority 1: Core Gap (Probabilistic → Deterministic)

### Tao's 2019 Paper
- **Title**: "Almost all Collatz orbits attain almost bounded values"
- **URL**: https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/
- **Also on arXiv**: https://arxiv.org/abs/1909.03562
- **Why needed**: Exact methodology for "almost all" proof; understand precisely where it fails to prove "all"
- **Status**: BLOCKED (403)

### Terras (1976)
- **Title**: "A Stopping Time Problem on the Positive Integers"
- **URL**: https://www.ams.org/journals/tran/1976-196-00/S0002-9947-1976-0378404-X/
- **Why needed**: Original stopping time analysis; probabilistic gap origin
- **Status**: BLOCKED (403)

### Lagarias (1985)
- **Title**: "The 3x+1 Problem and Its Generalizations"
- **URL**: https://www.ams.org/journals/bull/1985-12-01/S0273-0979-1985-15300-5/
- **Why needed**: Comprehensive survey; may contain approaches we haven't tried
- **Status**: BLOCKED (403)

---

## Priority 2: Renewal Theory & Markov Chains

### Durrett - "Probability: Theory and Examples"
- **Why needed**: Rigorous renewal theory framework; could help prove trajectories must hit renewal states
- **Status**: Not attempted yet

### Papers on Ergodic Theory for Dynamical Systems
- **Why needed**: Our gap is essentially an ergodic theory problem - proving mixing for deterministic trajectories
- **Status**: Need specific paper recommendations

### Kontorovich-Sinai (Transfer Operator Spectral Analysis)
- **Why needed**: Understand why spectral methods fail; might find workaround
- **Status**: BLOCKED

---

## Priority 3: Potential/Growth Analysis

### Papers on 2-adic Valuation in Dynamical Systems
- **Why needed**: Our Lifting the Exponent Lemma (LTE) approach to potential destruction
- **Key result we have**: ν₂(3^n - 1) = 1 for n odd, 2 + ν₂(n) for n even
- **Status**: Need more comprehensive treatment

### Eliahou, Simonetto (Cycle Length Lower Bounds)
- **Why needed**: Their methods for cycle analysis might apply to divergence
- **Status**: BLOCKED

---

## Priority 4: Alternative Approaches

### Conway's Undecidability Paper (1972)
- **Title**: "Unpredictable Iterations"
- **Why needed**: Understand exactly what's decidable vs undecidable about generalized Collatz
- **Status**: BLOCKED

### Wirsching's Book on Collatz
- **Why needed**: Comprehensive treatment, might have approaches we missed
- **Status**: Not attempted

---

## Specific Questions These Papers Could Answer

1. **Tao 2019**: How exactly does he handle the "exceptional set"? What specific structure allows proving "almost all" but not "all"?

2. **Terras 1976**: What was the original stopping time probabilistic model? Does it explicitly identify where determinism breaks the model?

3. **Ergodic Theory**: Are there conditions under which deterministic dynamical systems must follow statistical predictions? (This is exactly our gap)

4. **Transfer Operators**: Is there a way to use spectral methods that doesn't require compactness of Z+?

---

## Priority 5: 2024-2025 Developments (from DYNAMICAL_ALGEBRA_FRAMEWORK.md)

### Non-Archimedean Spectral Theory for Collatz (2024)
- **Title**: "The Collatz Conjecture & Non-Archimedean Spectral Theory"
- **Why needed**: Claims complete reformulation; Spectral Conjecture 5.28 would give full reformulation
- **Key concepts**: (p,q)-adic analysis, functions from p-adics to q-adics
- **Status**: Need to obtain and verify claims

### Geometric Langlands Proof (Gaitsgory-Raskin, July 2024)
- **Why needed**: New categorical tools for connecting dynamical systems to representation theory
- **Note**: 800+ pages, 5 papers - may be too advanced for direct application
- **Status**: Reference material

### Operator-Theoretic Framework Papers (2024)
- **Topics**: Lasota-Yorke inequality, backward transfer operators, spectral gaps
- **Why needed**: Direct attack on independence gap via spectral methods
- **Status**: Need specific paper citations

### Jacobsthal Numbers Connection
- **Why needed**: Structural correspondence between Collatz and signed Jacobsthal numbers
- **Status**: Need source paper

---

## Documents Already Read (For Reference)

- COLLATZ_PROOF_COMPLETE.md - Our current framework
- DIVERGENCE_PROOF_PROGRESS.md - Detailed analysis
- RESEARCHER_ASSIGNMENT_CONTRACTION_GAP.md - Research directions
- GRADER_CONSULTATION_TB2.md - TB2 analysis (VERY detailed)
- COLLATZ_FAILED_APPROACHES_ANALYSIS.md (other branch) - 5 failure modes
- DIVERGENCE_RESEARCH_REPORT.md (other branch) - Growth-Destruction Theorem

---

## Key Findings We Need Papers to Validate/Extend

1. **Potential Destruction**: After growth phase from n = 2^k × m - 1, post-growth potential = 1 (ALWAYS)
   - Proven via LTE for all k > 1
   - Need: Papers on whether this implies bounded total potential budget

2. **Renewal Theory**: q ≡ 1 (mod 8) as renewal state with exact uniform transitions
   - Need: Rigorous renewal theory that applies to deterministic sequences

3. **Spectral Analysis**: ρ(P_BB) ≈ 0.73 < 1 for avoid-renewal matrix
   - Need: Papers on when spectral gaps imply universal behavior (not just "almost all")

4. **4:1 Asymmetry**: Contraction from q ≡ 3 is 4× stronger than expansion from q ≡ 5
   - Need: Papers on asymmetric Markov chains and escape probability

---

## If You Can Upload Any Papers

Please prioritize in this order:
1. Tao 2019 (arxiv or blog post)
2. Terras 1976
3. Any paper on ergodic theory for number-theoretic dynamical systems
4. Lagarias 1985 survey

Even partial papers or summaries would help!
