import matplotlib.pyplot as plt
import numpy as np

# Modern style setup
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Data
problem_sizes = ['3×3', '4×4', '5×5', '6×6', '7×7', '8×8', '9×9', '10×10', '11×11', '12×12', '13×13', '14×14']
stated_confidence = [92, 75, 40, 15, 3, 0.5, 0.05, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001]
actual_accuracy = [100] * 12

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')

x = np.arange(len(problem_sizes))
width = 0.28

# Modern colors
red = '#ff6b6b'
green = '#51cf66'

bars1 = ax.bar(x - width/2 - 0.03, stated_confidence, width, label='Stated Confidence', 
               color=red, alpha=0.9, edgecolor='white', linewidth=1.5, zorder=3)
bars2 = ax.bar(x + width/2 + 0.03, actual_accuracy, width, label='Actual Accuracy (Scaffolded)', 
               color=green, alpha=0.9, edgecolor='white', linewidth=1.5, zorder=3)

ax.set_yscale('log')
ax.set_ylabel('Percentage (log scale)', fontsize=13, fontweight='medium', color='#333', labelpad=15)
ax.set_xlabel('Problem Size (digits × digits)', fontsize=13, fontweight='medium', color='#333', labelpad=15)
ax.set_title('The Confidence-Accuracy Gap', fontsize=20, fontweight='bold', color='#222', pad=35)
ax.text(0.5, 1.04, 'What Models Think vs. What They Actually Do', transform=ax.transAxes, 
        fontsize=13, color='#666', ha='center', style='italic')

ax.set_xticks(x)
ax.set_xticklabels(problem_sizes, fontsize=11, color='#444')
ax.tick_params(axis='y', labelsize=11, colors='#444')
ax.tick_params(axis='x', pad=8)

# Legend
legend = ax.legend(loc='upper right', fontsize=12, frameon=True, fancybox=True, 
                   shadow=False, framealpha=0.95, edgecolor='#ddd',
                   bbox_to_anchor=(0.95, 0.95))
legend.get_frame().set_facecolor('#fff')

# Subtle grid
ax.yaxis.grid(True, linestyle='-', alpha=0.3, color='#ccc', zorder=0)
ax.xaxis.grid(False)

# Axis limits
ax.set_ylim(0.000000008, 500)
ax.set_xlim(-1.0, len(problem_sizes) - 0.0)

# Annotation
ax.annotate('1 billion×\nmiscalibration', xy=(11, 0.0000001), xytext=(9, 0.000008),
            fontsize=11, ha='center', color='#444', fontweight='medium',
            arrowprops=dict(arrowstyle='->', color='#888', lw=1.5))

# Clean up spines
ax.spines['left'].set_color('#ccc')
ax.spines['bottom'].set_color('#ccc')

# Adjust layout
plt.subplots_adjust(left=0.10, bottom=0.12, right=0.95, top=0.88)

# Save with padding around the entire figure
plt.savefig('confidence_accuracy_gap_v3.png', dpi=180, bbox_inches='tight', 
            pad_inches=0.5, facecolor='#fafafa')  # pad_inches adds margin around entire image
print("Chart saved to confidence_accuracy_gap_v3.png")
