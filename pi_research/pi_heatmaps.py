"""
HEATMAP VISUALIZATIONS OF π
Multiple visual representations to spot patterns
"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from collections import Counter, defaultdict

# Load pi digits
with open('pi_research/pi_10k_digits.txt', 'r') as f:
    pi_digits = f.read().strip()

print("Generating π heatmaps...")

# Create figure with multiple subplots
fig = plt.figure(figsize=(20, 24))

# ===== 1. GRID HEATMAP - π as a 100x100 image =====
ax1 = fig.add_subplot(3, 2, 1)
grid_size = 100
digits_grid = np.array([int(d) for d in pi_digits[:grid_size**2]]).reshape(grid_size, grid_size)
im1 = ax1.imshow(digits_grid, cmap='viridis', aspect='equal')
ax1.set_title('π as 100×100 Grid (digit value = color)', fontsize=14)
ax1.set_xlabel('Position mod 100')
ax1.set_ylabel('Position // 100')
plt.colorbar(im1, ax=ax1, label='Digit (0-9)')

# ===== 2. TRANSITION HEATMAP - Which digit follows which =====
ax2 = fig.add_subplot(3, 2, 2)
transition_matrix = np.zeros((10, 10))
for i in range(len(pi_digits) - 1):
    d1, d2 = int(pi_digits[i]), int(pi_digits[i+1])
    transition_matrix[d1, d2] += 1

# Normalize to percentages
transition_pct = transition_matrix / transition_matrix.sum(axis=1, keepdims=True) * 100
im2 = ax2.imshow(transition_pct, cmap='hot', aspect='equal')
ax2.set_title('Transition Heatmap: P(next digit | current digit)', fontsize=14)
ax2.set_xlabel('Next Digit')
ax2.set_ylabel('Current Digit')
ax2.set_xticks(range(10))
ax2.set_yticks(range(10))
plt.colorbar(im2, ax=ax2, label='Probability %')

# Add text annotations
for i in range(10):
    for j in range(10):
        ax2.text(j, i, f'{transition_pct[i,j]:.1f}', ha='center', va='center',
                fontsize=7, color='white' if transition_pct[i,j] < 12 else 'black')

# ===== 3. ROLLING FREQUENCY HEATMAP =====
ax3 = fig.add_subplot(3, 2, 3)
window_size = 100
num_windows = len(pi_digits) // window_size
freq_matrix = np.zeros((num_windows, 10))

for w in range(num_windows):
    window = pi_digits[w*window_size:(w+1)*window_size]
    freq = Counter(window)
    for d in range(10):
        freq_matrix[w, d] = freq.get(str(d), 0)

im3 = ax3.imshow(freq_matrix.T, cmap='YlOrRd', aspect='auto')
ax3.set_title(f'Rolling Digit Frequency (window={window_size})', fontsize=14)
ax3.set_xlabel(f'Window Number (each = {window_size} digits)')
ax3.set_ylabel('Digit')
ax3.set_yticks(range(10))
plt.colorbar(im3, ax=ax3, label='Count in window')

# ===== 4. DIGIT POSITION SCATTER/DENSITY =====
ax4 = fig.add_subplot(3, 2, 4)
# Create density map: for each digit, show where it appears
density_map = np.zeros((10, 100))
for i, d in enumerate(pi_digits[:10000]):
    density_map[int(d), i % 100] += 1

im4 = ax4.imshow(density_map, cmap='Blues', aspect='auto')
ax4.set_title('Digit Density by Position mod 100', fontsize=14)
ax4.set_xlabel('Position mod 100')
ax4.set_ylabel('Digit')
ax4.set_yticks(range(10))
plt.colorbar(im4, ax=ax4, label='Occurrences')

# ===== 5. CUMULATIVE SUM TRAJECTORY =====
ax5 = fig.add_subplot(3, 2, 5)
cumsum = np.cumsum([int(d) - 4.5 for d in pi_digits[:5000]])  # Centered at 4.5
ax5.plot(cumsum, linewidth=0.5, color='purple')
ax5.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax5.set_title('Cumulative Sum (digits - 4.5): Random Walk of π', fontsize=14)
ax5.set_xlabel('Position')
ax5.set_ylabel('Cumulative deviation from mean')
ax5.fill_between(range(len(cumsum)), cumsum, alpha=0.3)

# ===== 6. 2D RANDOM WALK =====
ax6 = fig.add_subplot(3, 2, 6)
# Use pairs of digits as (dx, dy) moves
x, y = [0], [0]
for i in range(0, 2000, 2):
    dx = int(pi_digits[i]) - 4.5
    dy = int(pi_digits[i+1]) - 4.5
    x.append(x[-1] + dx)
    y.append(y[-1] + dy)

# Color by position in sequence
colors = np.linspace(0, 1, len(x))
scatter = ax6.scatter(x, y, c=colors, cmap='rainbow', s=1, alpha=0.6)
ax6.plot(x, y, 'k-', linewidth=0.2, alpha=0.3)
ax6.scatter([0], [0], color='green', s=100, marker='o', label='Start', zorder=5)
ax6.scatter([x[-1]], [y[-1]], color='red', s=100, marker='*', label='End', zorder=5)
ax6.set_title('2D Random Walk using π digit pairs', fontsize=14)
ax6.set_xlabel('X (cumulative)')
ax6.set_ylabel('Y (cumulative)')
ax6.legend()
ax6.set_aspect('equal')

plt.tight_layout()
plt.savefig('pi_research/pi_heatmaps.png', dpi=150, bbox_inches='tight')
print("Saved: pi_research/pi_heatmaps.png")

# ===== ADDITIONAL: HIGH-RES DIGIT GRID =====
fig2, ax = plt.subplots(figsize=(20, 20))
grid_size = 200
if len(pi_digits) >= grid_size**2:
    digits_grid_large = np.array([int(d) for d in pi_digits[:grid_size**2]]).reshape(grid_size, grid_size)

    # Custom colormap: each digit gets a distinct color
    colors = plt.cm.tab10(np.linspace(0, 1, 10))
    cmap = mcolors.ListedColormap(colors)

    im = ax.imshow(digits_grid_large, cmap=cmap, aspect='equal', vmin=0, vmax=9)
    ax.set_title(f'First {grid_size**2:,} digits of π as {grid_size}×{grid_size} grid', fontsize=16)
    ax.set_xlabel('Column (position mod 200)')
    ax.set_ylabel('Row (position // 200)')

    # Add colorbar with digit labels
    cbar = plt.colorbar(im, ax=ax, ticks=range(10))
    cbar.set_label('Digit')

    plt.savefig('pi_research/pi_grid_highres.png', dpi=150, bbox_inches='tight')
    print("Saved: pi_research/pi_grid_highres.png")

# ===== GAP HEATMAP: Distance between consecutive occurrences =====
fig3, axes = plt.subplots(2, 5, figsize=(20, 8))
axes = axes.flatten()

for digit in range(10):
    positions = [i for i, d in enumerate(pi_digits[:10000]) if d == str(digit)]
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]

    ax = axes[digit]
    ax.hist(gaps, bins=30, color=plt.cm.tab10(digit/10), edgecolor='black', alpha=0.7)
    ax.axvline(x=10, color='red', linestyle='--', label='Expected (10)')
    ax.set_title(f'Digit {digit}: Gap Distribution')
    ax.set_xlabel('Gap size')
    ax.set_ylabel('Frequency')
    if digit == 0:
        ax.legend()

plt.suptitle('Distribution of Gaps Between Consecutive Occurrences of Each Digit', fontsize=14)
plt.tight_layout()
plt.savefig('pi_research/pi_gap_distributions.png', dpi=150, bbox_inches='tight')
print("Saved: pi_research/pi_gap_distributions.png")

# ===== SPIRAL VISUALIZATION =====
fig4, ax = plt.subplots(figsize=(12, 12))

# Plot digits along an Archimedean spiral
n_digits = 3000
theta = np.linspace(0, 20*np.pi, n_digits)
r = theta / (2*np.pi)  # Radius grows with angle

x_spiral = r * np.cos(theta)
y_spiral = r * np.sin(theta)

colors_spiral = [int(d) for d in pi_digits[:n_digits]]
scatter = ax.scatter(x_spiral, y_spiral, c=colors_spiral, cmap='tab10', s=3, alpha=0.8)
ax.set_title(f'First {n_digits} digits of π on a spiral', fontsize=14)
ax.set_aspect('equal')
ax.axis('off')
plt.colorbar(scatter, ax=ax, label='Digit', ticks=range(10))

plt.savefig('pi_research/pi_spiral.png', dpi=150, bbox_inches='tight')
print("Saved: pi_research/pi_spiral.png")

print("\n✓ All heatmaps generated!")
print("\nFiles created:")
print("  - pi_heatmaps.png (6-panel analysis)")
print("  - pi_grid_highres.png (200×200 digit grid)")
print("  - pi_gap_distributions.png (gap analysis for each digit)")
print("  - pi_spiral.png (spiral visualization)")
