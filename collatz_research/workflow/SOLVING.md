# Collatz Solving Workspace

> **Role**: 🔧 SOLVER
>
> This is your primary workspace. Your job is to close the divergence gap—convert understanding into proof.
>
> ⚠️ **Have you completed `MASTERY_CHECKLIST.md`?** If not, go back to research mode.

**Purpose**: Active problem-solving attempts
**Status**: Divergence is the target

---

## Solver Protocol

1. **Start**: Read `CURRENT.md`, verify mastery checklist is complete
2. **Work**: Attempt proofs, document everything (successes AND failures)
3. **Failed?**: Add to `DONT_TRY_THIS.md` immediately
4. **Succeeded?**: Add to `THEOREM_INDEX.md`, write full proof in `proofs/`
5. **End**: Update `WORK_IN_PROGRESS.md` and `CURRENT.md`

---

## Current Goal

**Prove**: No Collatz trajectory diverges to infinity.

**Equivalent**: For all n, the trajectory eventually drops below n.

---

## Active Approaches

### Approach 1: Block-Escape Exclusion

**Idea**: Prove no orbit has the "Block-Escape Property"

**Status**: Spectral machinery reportedly complete

**What's needed**:
- [ ] Understand Block-Escape definition precisely
- [ ] Review spectral calculus preprint
- [ ] Identify the exact remaining gap
- [ ] Attempt to close it

**Notes**:
```
The preprint claims all analytic components are done.
The gap is excluding specific forward orbits.
```

### Approach 2: Renewal Theory

**Idea**: Use q ≡ 1 (mod 8) as renewal state

**Key facts**:
- From q ≡ 1: transitions are uniform
- Expected return time is finite
- This is where trajectories "reset"

**What's needed**:
- [ ] Formalize renewal state properties
- [ ] Prove trajectories must hit renewal states
- [ ] Bound excursions between renewals

**Notes**:
```
Markov chain on q mod 8 has been analyzed.
E[log(factor)] = -0.58 under stationary.
The gap: deterministic sequences might not follow this.
```

### Approach 3: Lyapunov Function Search

**Idea**: Find L(n) that strictly decreases on average

**Candidates tested**:
- log(v): Doesn't work (can increase)
- v^α: Doesn't work
- log(v) - c·T(v): ?
- log(v) + f(v mod 8): ?

**What's needed**:
- [ ] Systematic search over function families
- [ ] Prove no simple Lyapunov exists (or find one)

---

## Proof Attempts Log

### Attempt: Direct T_max Bound → Convergence

**Idea**: Use T_max ≤ log₂(n) + 5 to bound growth

**Result**: Insufficient alone. Bounds growth rate but not direction.

### Attempt: 4:1 Asymmetry Argument

**Idea**: Contraction 4× stronger than expansion, so must converge

**Result**: Probabilistic. Doesn't rule out "lucky" divergent sequences.

### Attempt: Gambler's Ruin Formalization

**Idea**: Model as random walk, show ruin is certain

**Result**: Works for random model. Gap: Collatz is deterministic.

---

## Ideas to Try

1. **Finite automaton analysis**: Can trajectory structure be captured?

2. **Backward tree density**: Prove divergent trajectory backward tree is empty

3. **Cross-residue analysis**: Use mod 8 × mod 3 structure

4. **Computational search**: Look for near-misses to divergence

---

## Scratchpad

```
Working thoughts:

For divergence, need T=1 fraction > 63.1% forever.
But q ≡ 5 (mod 8) gives T=1 with expansion.
q ≡ 3 (mod 8) gives T≥2 with strong contraction.

One visit to q≡3 cancels four visits to q≡5.
Break-even needs 79% q≡5, but transition limits to ~25%.

The question: can a trajectory "dodge" q≡3 forever?
Mod structure says no... but not proven deterministically.
```

---

## Resources at Hand

- proofs/NO_CYCLES_PROOF.md (complete)
- proofs/T_CASCADE_AND_TB2.md (complete)
- proofs/DIVERGENCE_PROGRESS.md (working)
- research/PAPERS_NEEDED.md (references)
- pdfs/ (papers)
- scripts/ (computational tools)

---

**END OF SOLVING WORKSPACE**
