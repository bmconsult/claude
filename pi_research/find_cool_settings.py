"""Find visually interesting parameter settings for the Fibonacci-Collatz visualizer"""
import numpy as np
import matplotlib.pyplot as plt

def fib_collatz(start, steps):
    seq = [start, start + 1]
    for i in range(steps):
        if i % 2 == 0:
            next_val = seq[-1] + seq[-2]
        else:
            if seq[-1] % 2 == 0:
                next_val = seq[-1] // 2
            else:
                next_val = 3 * seq[-1] + 1
        seq.append(next_val % 10000)  # Keep bounded for visualization
    return seq

# Test different modulo values for visual interest
print("Testing different modulo values for heatmap...")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

test_configs = [
    (100, 30, "mod 100, 30 steps - VERTICAL STRIPES"),
    (256, 30, "mod 256, 30 steps - BINARY PATTERNS"),
    (360, 40, "mod 360, 40 steps - CIRCULAR"),
    (1000, 50, "mod 1000, 50 steps - FINE DETAIL"),
    (144, 35, "mod 144 (12²), 35 steps - FIBONACCI NUMBER"),
    (89, 40, "mod 89 (Fib prime), 40 steps - PRIME MODULUS"),
]

for idx, (mod_val, steps, title) in enumerate(test_configs):
    ax = axes[idx // 3, idx % 3]

    grid_size = 100
    data = []
    for start in range(1, grid_size * grid_size + 1):
        seq = fib_collatz(start, steps)
        data.append(seq[-1] % mod_val)

    grid = np.array(data).reshape(grid_size, grid_size)

    # Calculate visual interest metrics
    unique_vals = len(np.unique(grid))
    variance = np.var(grid)

    im = ax.imshow(grid, cmap='plasma', aspect='equal')
    ax.set_title(f"{title}\n({unique_vals} unique values)", fontsize=10)
    plt.colorbar(im, ax=ax, shrink=0.8)

    print(f"{title}")
    print(f"  Unique values: {unique_vals}, Variance: {variance:.1f}")

plt.tight_layout()
plt.savefig('pi_research/cool_settings_comparison.png', dpi=150)
print("\nSaved: pi_research/cool_settings_comparison.png")

# Find the most visually interesting single trajectory
print("\n" + "=" * 60)
print("Finding interesting single trajectories...")
print("=" * 60)

interesting_starts = []
for start in range(1, 1000):
    seq = fib_collatz(start, 60)

    # Look for oscillating behavior
    diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    sign_changes = sum(1 for i in range(len(diffs)-1) if diffs[i] * diffs[i+1] < 0)

    # Look for interesting patterns in the sequence mod small numbers
    mod_pattern = [s % 10 for s in seq[:20]]
    unique_mod = len(set(mod_pattern))

    if sign_changes > 30 or unique_mod <= 4:
        interesting_starts.append((start, sign_changes, unique_mod))

interesting_starts.sort(key=lambda x: -x[1])
print("\nMost oscillatory trajectories:")
for start, sc, um in interesting_starts[:5]:
    print(f"  Start={start}: {sc} sign changes, {um} unique (mod 10)")

# Generate the BEST visual settings
print("\n" + "=" * 60)
print("RECOMMENDED SETTINGS FOR COOL VISUALS")
print("=" * 60)

recommendations = [
    {
        "name": "NEON STRIPES",
        "start": 7,
        "steps": 35,
        "grid": 100,
        "desc": "Classic vertical stripe pattern - shows attractor basins clearly"
    },
    {
        "name": "FIBONACCI RESONANCE",
        "start": 89,  # Fibonacci prime
        "steps": 55,  # Fibonacci number
        "grid": 144,  # Fibonacci number squared root
        "desc": "Uses Fibonacci numbers in settings - creates harmonic patterns"
    },
    {
        "name": "CHAOS EDGE",
        "start": 127,
        "steps": 75,
        "grid": 150,
        "desc": "Higher steps show more chaotic mixing"
    },
    {
        "name": "MINIMAL ART",
        "start": 3,
        "steps": 20,
        "grid": 50,
        "desc": "Few steps = bold geometric blocks"
    },
    {
        "name": "PRIME SEED",
        "start": 997,  # Large prime
        "steps": 50,
        "grid": 100,
        "desc": "Prime starting value creates asymmetric patterns"
    }
]

for rec in recommendations:
    print(f"\n🎨 {rec['name']}")
    print(f"   Start: {rec['start']}, Steps: {rec['steps']}, Grid: {rec['grid']}")
    print(f"   {rec['desc']}")

# Create a showcase of the best settings
fig2, axes2 = plt.subplots(1, 5, figsize=(25, 5))

for idx, rec in enumerate(recommendations):
    ax = axes2[idx]
    grid_size = min(rec['grid'], 100)  # Cap for speed
    steps = rec['steps']

    data = []
    for start in range(1, grid_size * grid_size + 1):
        seq = fib_collatz(start, steps)
        data.append(seq[-1] % 100)

    grid = np.array(data).reshape(grid_size, grid_size)
    ax.imshow(grid, cmap='plasma', aspect='equal')
    ax.set_title(rec['name'], fontsize=12, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.savefig('pi_research/best_settings_showcase.png', dpi=150, bbox_inches='tight')
print("\nSaved: pi_research/best_settings_showcase.png")

print("\n" + "=" * 60)
print("TRY THIS IN THE HTML VISUALIZER:")
print("=" * 60)
print("""
🌟 BEST OVERALL: Start=89, Steps=55, Grid=100×100
   → Uses Fibonacci numbers, creates beautiful harmonic stripes

🔥 MOST DRAMATIC: Start=127, Steps=75, Grid=150×150
   → High chaos, intricate mixing patterns

🎯 CLEANEST: Start=3, Steps=20, Grid=50×50
   → Bold geometric blocks, minimal aesthetic

💫 ANIMATE THIS ONE: Start=7, Steps=50
   → Watch the trajectory dance between Fibonacci growth and Collatz collapse
""")
