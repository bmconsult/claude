# Builder C: Hybrid Symbolic-2adic Proof Attempt

## Round 1: Initial Sketch
**Proof:** Encode trajectories as binary sequences (0=even, 1=odd). In 2-adic metric, repeated division by 2 is expansive (increases |n|₂). Symbolic sequences with high 1-density cause growth; those with high 0-density cause 2-adic expansion. Claim: These opposing forces prevent both divergence and cycles.

**Critic:** FATAL - "opposing forces" doesn't prove anything. No rigorous connection established.

## Round 2: Refined Attempt
**Proof:** Map ℤ→ℤ₂ preserves Collatz dynamics. In ℤ₂, the map T₂(x) = x/2 (even) or (3x+1)/2 (odd) has invariant measure μ. Symbolic coding partitions ℤ₂ by trajectory type. Divergent trajectories require symbol density violating μ-typical behavior.

**Critic:** MAJOR - ℤ₂ is compact, so "divergence" needs redefinition. FATAL - "typical" ≠ "all."

## Round 3: Honest Assessment
**Proof:** The 2-adic and symbolic frameworks illuminate different aspects but don't combine cleanly. 2-adic analysis handles local dynamics; symbolic addresses global behavior. Their interaction remains mysterious.

**Final Gap Assessment:**
The hybrid approach reveals why Collatz is hard: natural frameworks pull in opposite directions. 2-adic structure suggests convergence via ultrametric contraction, while symbolic dynamics allows divergent sequences. No clean synthesis achieved. The proof fails - we've only reformulated the difficulty.