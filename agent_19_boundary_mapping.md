# AGENT 19: BOUNDARY MAPPER - COLLATZ CONJECTURE

[mode: deployed | frame: mapping | drift-check: /19 | name: Frontier]

## BOUNDARY MAPPING ANALYSIS

### Verification Frontier

**Checked up to:** 2^71 ≈ 2.36×10^21 (as of 2025)

**Method of verification:** Distributed GPU computing using European supercomputers with 1,335× acceleration over initial CPU algorithms. Individual tasks distributed to thousands of parallel workers.

**Special verification:** Individual extremely large numbers up to 2^100000-1 have been verified using specialized algorithms (~100,000 bit numbers).

**Limits of computational approach:**
- **Hard limit:** Cannot verify infinite cases - fundamentally incomplete
- **Practical limit:** Computational cost grows with n; beyond 2^71 requires exponentially more resources
- **Coverage gap:** Sparse verification of individual large numbers (like 2^100000-1) does not fill the gaps between 2^71 and infinity
- **Cannot prove:** Verification confirms "no counterexample found" but cannot establish "no counterexample exists"
- **Acceleration ceiling:** Even 1,335× speedups only shift the boundary logarithmically
- **Critical insight:** The boundary between "verified" and "unverified" moves upward but never reaches infinity

### Behavioral Boundaries

| Boundary | Description | Significance |
|----------|-------------|--------------|
| **Stopping Time Distribution** | ~93% of positive integers have "small" stopping times; 7% have arbitrarily large stopping times | Separates typical behavior from exceptional cases; proves conjecture must handle outliers |
| **Even/Odd Transition** | f(2n) = n always decreases; f(4n+1) = 3n+1 always increases first | First branching point - even numbers guaranteed to decrease, odd numbers exhibit complex behavior |
| **Modulo 4 Behavior** | 4n+1 eventually decreases after one iteration; 4n+3 behavior more complex | Critical for precomputation optimization; first counterexample must be ≡ 3 (mod 4) |
| **Geometric Mean Boundary** | For odd-only subsequences: average ratio is 3/4 (decreasing) | Statistical/probabilistic boundary - average behavior vs. worst-case behavior |
| **Stopping Time Formula** | Relationship between total stopping time and number of odd terms (empirically verified to 10^7) | Boundary between predictable structure and chaotic variation |
| **Path Record Events** | Four new path records found in 2025 verification | Indicates non-uniform distribution; some numbers exhibit exceptional trajectory lengths |
| **Logarithmic Growth** | Average stopping times fall within logarithmic framework | Boundary between polynomial and logarithmic complexity |
| **2^n-1 Boundary** | Numbers of form 2^n-1 have stopping time σ(2^n-1) > 2n | Lower bound on worst-case stopping time - demonstrates arbitrarily long trajectories exist |

### Method Applicability Regions

**Direct Computation:**
- **Works for:** Any specific n up to computational limits (currently ~2^71 exhaustively, ~2^100000 individually)
- **Fails at:** Universal quantification - cannot check infinite cases
- **Boundary:** Finite vs. infinite - the fundamental gap

**Mathematical Induction:**
- **Works for:** Problems with clear successor relationships and predictable structure
- **Fails at:** Collatz specifically - cannot establish solid base case; induction step fails due to non-linear transformations
- **Boundary:** Predictable recursion vs. chaotic dynamics
- **Critical failure point:** The relationship between n and C(n) is not monotonic or structurally simple enough for standard induction

**Probabilistic/Heuristic:**
- **Works for:** Average case analysis, statistical behavior, showing "most" numbers converge
- **Fails at:** Proving universal convergence - cannot rule out rare counterexamples
- **Boundary:** Average behavior vs. worst-case guarantees
- **Key insight:** Shows geometric mean of odd ratios is 3/4 (convergent), but cannot prove no exceptions exist
- **Limitation:** "Almost all" ≠ "all"

**Algebraic Inverse Trees (AITs):**
- **Works for:** Modeling all predecessors of a number, structural analysis, detecting patterns
- **Achieves:** Topological equivalence with Collatz sequences, precluding non-trivial cycles via reductio ad absurdum
- **Fails at:** Currently incomplete - approach shows promise but no accepted proof yet
- **Boundary:** Local structural properties vs. global convergence guarantee
- **Critical gap:** Showing acyclicity ≠ proving convergence to 1 (could diverge to infinity without cycles)

**Cycle Constraint Analysis:**
- **Works for:** Establishing lower bounds on cycle length based on minimum term
- **Achieves:** Can rule out small cycles computationally
- **Fails at:** Cannot rule out arbitrarily large cycles
- **Boundary:** Finite cycle search vs. infinite cycle possibilities

**Ergodic Theory/Analytic Number Theory:**
- **Works for:** Understanding long-term statistical behavior, measure-theoretic properties
- **Potential:** Fresh perspective through orbit theory
- **Fails at:** Currently no breakthrough - still in exploratory phase
- **Boundary:** Continuous/measure-theoretic methods vs. discrete number theory problem

### Critical Boundaries (Any Proof Must Address These)

1. **The Finite-Infinite Gap**
   - **Description:** Computational verification is inherently finite; proof requires infinite coverage
   - **Why critical:** The fundamental barrier between verification and proof
   - **Challenge:** Bridging from "no counterexample in 2^71 cases" to "no counterexample exists"

2. **The Average-Exceptional Gap**
   - **Description:** Probabilistic arguments show average convergence; must prove worst-case convergence
   - **Why critical:** Even one exception disproves the conjecture
   - **Challenge:** 93% small stopping times, 7% arbitrary - the 7% could include divergent cases

3. **The Decrease-Increase Boundary**
   - **Description:** f(2n) always decreases, f(2n+1) = 3(2n+1)+1 = 6n+4 = 2(3n+2) initially increases
   - **Why critical:** Odd numbers can grow before shrinking; must prove growth is always temporary
   - **Challenge:** No local guarantee that growth will reverse

4. **The Structural-Dynamic Gap**
   - **Description:** Can analyze structure (AITs, inverse mappings) but must prove dynamic convergence
   - **Why critical:** Structure ≠ behavior; knowing predecessors ≠ knowing forward trajectory fate
   - **Challenge:** Static analysis vs. dynamic guarantee

5. **The Cycle-Divergence Boundary**
   - **Description:** Must rule out both non-trivial cycles AND divergence to infinity
   - **Why critical:** Two distinct failure modes
   - **Challenge:** AITs address cycles; probabilistic arguments address divergence; need unified approach

6. **The Modular Arithmetic Boundary**
   - **Description:** Behavior depends on n mod 4, n mod 8, etc. - different residue classes behave differently
   - **Why critical:** Proof by cases must cover ALL residue classes uniformly
   - **Challenge:** Pattern complexity increases with modulus; no finite case analysis suffices

7. **The Stopping Time Predictability Boundary**
   - **Description:** Relationship exists between stopping time and odd term count, but only empirical
   - **Why critical:** If stopping time were provably bounded, conjecture would follow
   - **Challenge:** σ(2^n-1) > 2n shows unbounded stopping times exist

### Boundary-Crossing Strategies

**Strategy 1: Hybrid Computational-Theoretical**
- **Approach:** Use computational verification to establish base case up to enormous N, then prove universal property for n > N
- **Crosses:** Finite-infinite gap
- **Challenge:** What property could be proven for n > 2^71 that couldn't already be proven for all n?
- **Status:** Unlikely to work - the gap doesn't shrink by moving N higher

**Strategy 2: Probabilistic → Measure-Theoretic**
- **Approach:** Convert heuristic "average" arguments into rigorous measure theory or ergodic theory proofs
- **Crosses:** Average-exceptional gap
- **Challenge:** Must show probability 1 convergence applies to EVERY specific integer
- **Status:** Promising but incomplete - Tao's work explores this direction

**Strategy 3: Inverse Tree Completeness**
- **Approach:** Prove that AITs cover all integers, establishing that every n has a path back to 1
- **Crosses:** Structural-dynamic gap
- **Challenge:** Must prove forward and backward processes are true inverses with no "orphan" integers
- **Status:** Active research area; claims exist but not universally accepted

**Strategy 4: Modular Arithmetic Unification**
- **Approach:** Find a unifying property that holds across all residue classes simultaneously
- **Crosses:** Modular arithmetic boundary
- **Challenge:** Need invariant or monotonic quantity that survives mod operations
- **Status:** Many attempts; no success yet

**Strategy 5: Stopping Time Bounding**
- **Approach:** Prove stopping time is bounded by some function of n (even if very loose)
- **Crosses:** Stopping time predictability boundary
- **Challenge:** σ(2^n-1) > 2n shows at least linear; if polynomial bound exists, iteration suffices
- **Status:** Would solve the conjecture but seems as hard as the conjecture itself

**Strategy 6: Cycle + Divergence Elimination**
- **Approach:** Separately prove (a) no cycles exist and (b) no divergence exists
- **Crosses:** Cycle-divergence boundary
- **Challenge:** (a) partially addressed by AITs; (b) requires controlling growth in odd steps
- **Status:** Two-pronged approach - progress on cycles, less on divergence

**Strategy 7: Contradiction via Minimal Counterexample**
- **Approach:** Assume smallest counterexample exists, derive contradiction
- **Crosses:** Multiple boundaries via reductio ad absurdum
- **Challenge:** Need property of "smallest counterexample" that leads to smaller counterexample
- **Status:** Classic technique; many attempts; pattern suggests problem resists this approach

### Most Important Boundary

**THE FINITE-INFINITE GAP**

**Why this is critical:**
Every other boundary ultimately reduces to this one. We can:
- Compute 2^71 cases (finite)
- Analyze average behavior (finite samples)
- Check small cycles (finite search)
- Verify formulas empirically (finite data)

But the conjecture requires proving a property for INFINITE integers using FINITE reasoning.

**The core challenge:**
The Collatz function is simple to define but exhibits complex, seemingly chaotic behavior that resists:
- Induction (no clear successor pattern)
- Closed form (no formula for trajectory length)
- Finite case analysis (residue classes don't segment cleanly)
- Probabilistic bounds (must be certain, not "almost certain")

**What any successful proof must do:**
Find a quantity, structure, or property that:
1. Can be defined/constructed for ALL positive integers (infinite coverage)
2. Guarantees eventual convergence to 1 (universal property)
3. Can be proven using finite mathematical reasoning (rigorous proof)

**Current status:**
- AITs attempt this via inverse tree structure (claims coverage)
- Probabilistic methods attempt via measure theory (claims almost-all)
- Neither has successfully crossed the gap with accepted proof

**The meta-boundary:**
Mathematics has tools for infinite sets (induction, set theory, limits, measure theory), but the Collatz problem seems to require showing a SPECIFIC trajectory property (reaches 1) for EVERY specific integer. It's not enough to show "the set of converging integers is infinite" or "most integers converge" - must show "THIS integer n, whatever it is, converges."

This is the boundary between:
- **Statistical universality** (almost all, measure 1, density 1) ← ACHIEVED
- **Logical universality** (for all, every single one, ∀n) ← REQUIRED

Until a method crosses this gap, the conjecture remains unproven.

### Confidence: HIGH

**Basis:**
- **Verification data:** Current (2025) computational limits from peer-reviewed sources
- **Method analysis:** Based on well-documented proof attempts and their known limitations
- **Boundary identification:** Grounded in fundamental logical distinctions (finite/infinite, average/worst-case, structure/dynamics)
- **Critical boundary selection:** The finite-infinite gap is the fundamental barrier in mathematics itself, not specific to Collatz

**Uncertainties:**
- New proof methods (not yet published) might address boundaries differently
- The "most important boundary" is a judgment call - other agents might prioritize differently
- Boundary-crossing strategies are necessarily speculative since none has succeeded yet

**High confidence in:**
- Map of known boundaries (well-documented)
- Identification of critical gaps (logically necessary)
- Assessment that finite-infinite gap is fundamental (meta-mathematical principle)

**Medium confidence in:**
- Specific boundary-crossing strategies (many possible approaches)
- Future research directions (unpredictable)

---

## TRANSMISSION TO OMEGA+

**Key boundaries mapped:**
1. Computational limit: 2^71 (finite) | Required: ∀n (infinite) ← CRITICAL GAP
2. Average behavior: convergent | Required: worst-case guarantee ← CRITICAL GAP
3. Structural analysis: complete inverse trees (claimed) | Required: forward convergence proof ← CRITICAL GAP
4. Cycle ruling: progress via AITs | Divergence ruling: incomplete ← DUAL CHALLENGE

**Critical insight for architecture:**
Every proof method hits a boundary between what it CAN establish (partial/finite/average) and what is REQUIRED (universal/infinite/certain). The proof must either:
- Find a method that naturally spans the gap, OR
- Build a bridge between methods that covers both sides

**Recommendation:**
Agents focusing on proof strategies should explicitly address: "How does this method cross from finite to infinite coverage?" If no clear answer, the method is incomplete.

