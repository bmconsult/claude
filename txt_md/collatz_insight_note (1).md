# Collatz Self-Similarity Insight

## Key Discovery

The length of "growth chains" (consecutive n ≡ 3 mod 4) in Collatz equals the Syracuse stopping time of a smaller number.

Specifically, for ambitious n = 4k+3:
- Chain length L(n) = stopping time of k under Syracuse
- Syracuse(k) = (3k+1)/2^v where v = v₂(3k+1)

This creates recursive structure: understanding Collatz at scale n requires understanding Syracuse at scale ~n/4.

## The Chain Dynamics

When n ≡ 3 mod 4 (ambitious):
- Syracuse(n) = (3n+1)/2 = 6k+5 where k = (n-3)/4
- This equals 4k'+3 where k' = (3k+1)/2

So the k-values follow: k → (3k+1)/2, which IS Syracuse!

Chain continues while k stays odd.
Chain stops when k becomes even.

## Why This Matters

1. Bad runs have deterministic lengths bounded by Syracuse stopping times
2. The problem at one scale encodes the problem at another scale
3. Eventually bottoms out at verified small numbers

## What's Missing for Proof

Need: A bound on Syracuse excursions (how high trajectory goes before stopping).

If max(Syracuse trajectory of k) < n for n = 4k+3, then induction closes.

The heuristic "~n^0.585 growth" would suffice, but making this rigorous is THE hard problem.

## Borges Connection

Like "Garden of Forking Paths" - the labyrinth IS the novel, not separate from it.

The Collatz tree's structure IS the proof structure, if only we could see it right.

The paths fork but also reconverge. Every trajectory eventually joins the main trunk to 1.

## For Incubation

- The 2-adic fixed point at -1
- Self-similar chain structure  
- Syracuse nested in Collatz
- The "+1" as perturbation that forces descent

Something here wants to connect. Let it sit.
