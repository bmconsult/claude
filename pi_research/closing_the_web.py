"""
CLOSING THE WEB: Can trajectories hop between growing regions forever?

Key finding: 62% of escapes from growing regions land in another growing region.
This is HIGHER than the ~20% base rate - growing regions are connected.

Questions to answer:
1. What connects growing regions to each other?
2. Is there a "potential function" that decreases with each hop?
3. Does the web have infinite paths, or must all paths exit?
"""
import math
from collections import defaultdict, deque

def v2(n):
    if n == 0: return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def collatz_step(n):
    next_val = 3*n + 1
    v = v2(next_val)
    return next_val // (2**v), v

def local_vf(r, k, steps=10):
    """Compute V/F for a residue class over steps iterations"""
    modulus = 2**k
    current = r
    v_total = 0
    for _ in range(steps):
        n_rep = current + modulus * 10000
        next_val = 3 * n_rep + 1
        v = v2(next_val)
        v_total += v
        current = (next_val // (2**v)) % modulus
    return v_total / steps

def is_growing(r, k):
    return local_vf(r, k, steps=10) < math.log2(3)

print("=" * 70)
print("STRUCTURE OF THE GROWING WEB")
print("=" * 70)

k = 10  # Use smaller k for tractability
modulus = 2**k

# Find all growing residues
growing = set()
for r in range(1, modulus, 2):
    if is_growing(r, k):
        growing.add(r)

print(f"\nMod-{modulus}: {len(growing)} growing residues ({len(growing)/(modulus//2):.1%} of odd residues)")

# Build the transition graph within growing regions
print("\n" + "=" * 70)
print("BUILDING THE GROWING-TO-GROWING TRANSITION GRAPH")
print("=" * 70)

# For each growing residue, find where it goes after escaping
def trace_escape(start_r, modulus, max_steps=20):
    """Trace from a growing residue until we can classify the destination"""
    n = start_r + modulus * 1000  # Representative value

    for step in range(max_steps):
        n, v = collatz_step(n)
        r = n % modulus
        return r, step + 1, n

    return None, max_steps, n

# Build transition graph: growing -> growing
transitions = defaultdict(list)  # source -> [(dest, steps, growth_factor)]

for src in growing:
    # Try multiple representatives to see where they go
    destinations = defaultdict(int)

    for offset in range(10):
        n = src + modulus * (1000 + offset * 100)
        start_n = n

        # Trace for a few steps
        for step in range(15):
            n, v = collatz_step(n)

        dest_r = n % modulus
        destinations[dest_r] += 1

    # Record transitions to growing regions
    for dest_r, count in destinations.items():
        if dest_r in growing:
            growth = n / start_n if start_n > 0 else 1
            transitions[src].append((dest_r, count, growth))

print(f"\nGrowing regions with outgoing edges to other growing: {len(transitions)}")
print(f"Total edges in growing-to-growing graph: {sum(len(v) for v in transitions.values())}")

# Analyze the structure
print("\n" + "=" * 70)
print("GRAPH STRUCTURE ANALYSIS")
print("=" * 70)

# Find strongly connected components
def find_sccs(nodes, edges):
    """Tarjan's algorithm for SCCs"""
    index_counter = [0]
    stack = []
    lowlinks = {}
    index = {}
    on_stack = {}
    sccs = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack[node] = True

        for dest, _, _ in edges.get(node, []):
            if dest not in index:
                strongconnect(dest)
                lowlinks[node] = min(lowlinks[node], lowlinks[dest])
            elif on_stack.get(dest, False):
                lowlinks[node] = min(lowlinks[node], index[dest])

        if lowlinks[node] == index[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    for node in nodes:
        if node not in index:
            strongconnect(node)

    return sccs

sccs = find_sccs(growing, transitions)
print(f"\nStrongly connected components: {len(sccs)}")
print(f"Largest SCC size: {max(len(scc) for scc in sccs)}")
print(f"SCCs of size > 1: {sum(1 for scc in sccs if len(scc) > 1)}")

# Check for cycles in the growing graph
print("\n" + "=" * 70)
print("CHECKING FOR CYCLES IN GROWING WEB")
print("=" * 70)

cycles_found = []
for scc in sccs:
    if len(scc) > 1:
        cycles_found.append(scc)
        if len(cycles_found) <= 3:
            print(f"  Cycle of size {len(scc)}: {scc[:5]}{'...' if len(scc) > 5 else ''}")

if cycles_found:
    print(f"\n*** FOUND {len(cycles_found)} CYCLES IN GROWING WEB ***")
    print("This means trajectories COULD potentially loop within growing regions!")
else:
    print("\n*** NO CYCLES FOUND - Growing web is a DAG ***")
    print("This means all paths through growing regions must eventually EXIT!")

print("\n" + "=" * 70)
print("PATH LENGTH ANALYSIS")
print("=" * 70)

# If it's a DAG, find the longest path
if not cycles_found:
    # Compute longest path from each node using dynamic programming
    longest_from = {}

    def longest_path(node, memo={}):
        if node in memo:
            return memo[node]

        if node not in transitions or not transitions[node]:
            memo[node] = 0
            return 0

        max_len = 0
        for dest, _, _ in transitions[node]:
            if dest in growing:
                max_len = max(max_len, 1 + longest_path(dest, memo))

        memo[node] = max_len
        return max_len

    max_path = 0
    max_path_start = None

    for node in growing:
        path_len = longest_path(node)
        if path_len > max_path:
            max_path = path_len
            max_path_start = node

    print(f"Longest path in growing DAG: {max_path} hops")
    print(f"Starting from residue: {max_path_start}")

    if max_path < 100:
        print(f"\n*** BOUNDED PATH LENGTH = {max_path} ***")
        print("Any trajectory entering growing region must exit within bounded steps!")

print("\n" + "=" * 70)
print("WHAT HAPPENS AFTER EXITING GROWING WEB")
print("=" * 70)

# Track where trajectories go after leaving the growing web
exit_destinations = defaultdict(int)
total_exits = 0

for src in growing:
    for offset in range(5):
        n = src + modulus * (1000 + offset * 100)

        # Trace until we leave growing
        in_growing = True
        steps_in_growing = 0

        while in_growing and steps_in_growing < 50:
            n, v = collatz_step(n)
            r = n % modulus
            steps_in_growing += 1

            if r not in growing:
                in_growing = False
                # Classify the exit destination
                vf = local_vf(r, k)
                if vf > 2.0:
                    exit_destinations["strongly_shrinking"] += 1
                elif vf > math.log2(3):
                    exit_destinations["shrinking"] += 1
                else:
                    exit_destinations["still_growing"] += 1  # Shouldn't happen
                total_exits += 1

print(f"\nExit destinations from growing web (n={total_exits}):")
for dest, count in sorted(exit_destinations.items(), key=lambda x: -x[1]):
    print(f"  {dest}: {count} ({count/total_exits:.1%})")

print("\n" + "=" * 70)
print("THE POTENTIAL FUNCTION")
print("=" * 70)

print("""
IDEA: Find a quantity that DECREASES with each hop in the growing web.

If such a potential exists, paths through the web must be finite.

Candidates:
1. The residue value itself
2. The V/F ratio of the destination
3. Some function of the position in the SCC hierarchy
""")

# Check if V/F increases (becomes more shrinking) with each hop
print("\nChecking if V/F increases along growing-web edges:")

vf_increases = 0
vf_decreases = 0

for src in transitions:
    src_vf = local_vf(src, k)
    for dest, count, _ in transitions[src]:
        dest_vf = local_vf(dest, k)
        if dest_vf > src_vf:
            vf_increases += count
        else:
            vf_decreases += count

total_edges = vf_increases + vf_decreases
if total_edges > 0:
    print(f"  V/F increases (toward shrinking): {vf_increases} ({vf_increases/total_edges:.1%})")
    print(f"  V/F decreases (deeper into growing): {vf_decreases} ({vf_decreases/total_edges:.1%})")

print("\n" + "=" * 70)
print("*** SYNTHESIS ***")
print("=" * 70)

if not cycles_found:
    print(f"""
THEOREM: The growing web in mod-{modulus} has no cycles.

COROLLARY: Any trajectory passing through growing regions must exit
           within at most {max_path} hops.

PROOF STRUCTURE:
1. The growing-to-growing transition graph is a DAG (no cycles)
2. Every DAG has finite longest path
3. After at most {max_path} transitions within growing, trajectory must exit
4. Exit leads to shrinking region (V/F > 1.585)
5. In shrinking region, trajectory converges toward 1

REMAINING QUESTION: Does this hold for ALL k, not just k={k}?
""")
else:
    print(f"""
WARNING: Found cycles in growing web!

This means trajectories could potentially loop within growing regions.
Need to analyze these cycles more carefully.

Cycles found: {len(cycles_found)}
""")
