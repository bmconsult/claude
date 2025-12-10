# Attack 9: Symbolic Dynamics Proof Sketch

## Shift Space Representation
- Encode trajectory: 0 = divide by 2, 1 = apply 3n+1
- Space: Σ = {0,1}^ℕ with shift map σ
- Key: Every 1 forces at least one 0 (since 3n+1 is even)

## Forbidden Patterns for Divergence
For trajectory n₀, n₁, n₂,... to diverge:
- Need lim sup(#1s in [0,k])/(#0s in [0,k]) > log(3)/log(2)
- But constraint: no consecutive 1s possible
- More subtle: long runs of 0s after each 1 suppress growth

## Proof Strategy
1. Show divergent trajectories require density(1s) > 0.63...
2. Prove topological entropy of allowed sequences < log(2)
3. Use specification property: can't maintain required 1-density with forced 0s

## Critical Gaps
- **Value-Symbol Decoupling**: Symbol sequence doesn't determine growth rate (depends on n₀ mod powers of 2)
- **Non-Markovian**: Transition probabilities depend on trajectory history via residue classes
- **Measure vs Topology**: Topological constraints don't immediately yield measure-zero for divergent set

The symbolic dynamics gives necessary conditions but the value-dependent growth rates escape purely topological analysis.