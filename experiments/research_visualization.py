"""
Visualizing the Capability Self-Knowledge Research Program

Six paths converging on one question:
How can a model know what it can do?
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patheffects as pe

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(-10, 10)
ax.set_ylim(-8, 8)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('#f8f9fa')

# Title
ax.text(0, 7.5, "Capability Self-Knowledge", fontsize=24, fontweight='bold',
        ha='center', va='center', color='#2c3e50')
ax.text(0, 6.5, "Six Paths to Closing the Gap", fontsize=14,
        ha='center', va='center', color='#7f8c8d')

# Central node - the gap
center_circle = Circle((0, 0), 1.5, facecolor='#e74c3c', edgecolor='#c0392b',
                       linewidth=3, alpha=0.9)
ax.add_patch(center_circle)
ax.text(0, 0.2, "The Gap", fontsize=12, fontweight='bold', ha='center', va='center', color='white')
ax.text(0, -0.3, "What I can do vs", fontsize=9, ha='center', va='center', color='white')
ax.text(0, -0.7, "What I know I can do", fontsize=9, ha='center', va='center', color='white')

# Six paths arranged in a circle
paths = [
    {"name": "Architectural", "sub": "Latent Reasoning", "color": "#3498db", "angle": 90},
    {"name": "Interpretability", "sub": "SAE Features", "color": "#9b59b6", "angle": 30},
    {"name": "Training", "sub": "KTO Calibration", "color": "#1abc9c", "angle": -30},
    {"name": "Simulation", "sub": "Self-World-Models", "color": "#f39c12", "angle": -90},
    {"name": "Post-Training", "sub": "Task Vectors", "color": "#e67e22", "angle": -150},
    {"name": "Routing", "sub": "Depth Signals", "color": "#27ae60", "angle": 150},
]

radius = 5.5
node_radius = 1.2

for path in paths:
    angle_rad = np.radians(path["angle"])
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)

    # Draw connection to center
    ax.plot([x * 0.35, 0], [y * 0.35, 0], color=path["color"],
            linewidth=3, alpha=0.5, zorder=1)

    # Draw node
    node = Circle((x, y), node_radius, facecolor=path["color"],
                 edgecolor='white', linewidth=2, alpha=0.9)
    ax.add_patch(node)

    # Path name
    ax.text(x, y + 0.25, path["name"], fontsize=11, fontweight='bold',
            ha='center', va='center', color='white')
    # Sub-description
    ax.text(x, y - 0.25, path["sub"], fontsize=8,
            ha='center', va='center', color='white', alpha=0.9)

# Key insights around the edge
insights = [
    ("Token space forces\ncommitment", -8, 5, "#3498db"),
    ("Uncertainty as\nextractable direction", 8, 4, "#9b59b6"),
    ("Loss aversion for\nrobust calibration", 8, -3, "#1abc9c"),
    ("Predict before\ncommitting", 0, -6.5, "#f39c12"),
    ("Calibration as\nportable patch", -8, -3, "#e67e22"),
    ("Processing depth\n→ uncertainty", -8, 1, "#27ae60"),
]

for text, x, y, color in insights:
    ax.text(x, y, text, fontsize=8, ha='center', va='center',
            color=color, alpha=0.8, style='italic')

# Bottom note
ax.text(0, -7.5, "Each path addresses the gap at a different level.\nA comprehensive solution combines multiple approaches.",
        fontsize=10, ha='center', va='center', color='#7f8c8d')

plt.tight_layout()
plt.savefig('/home/user/claude/experiments/research_visualization.png', dpi=150,
            bbox_inches='tight', facecolor='#f8f9fa')
print("Visualization saved to research_visualization.png")

# Also save a simpler text diagram
text_diagram = """
                    ┌─────────────────┐
                    │  ARCHITECTURAL  │
                    │ Latent Reasoning │
                    └────────┬────────┘
                             │
    ┌───────────────┐        │        ┌────────────────┐
    │    ROUTING    │────────┼────────│ INTERPRETABILITY│
    │ Depth Signals │        │        │  SAE Features   │
    └───────────────┘        │        └────────────────┘
                             │
                     ┌───────┴───────┐
                     │   THE GAP     │
                     │ What I can do │
                     │      vs       │
                     │ What I know   │
                     └───────┬───────┘
                             │
    ┌───────────────┐        │        ┌────────────────┐
    │ POST-TRAINING │────────┼────────│    TRAINING    │
    │ Task Vectors  │        │        │ KTO Calibration │
    └───────────────┘        │        └────────────────┘
                             │
                    ┌────────┴────────┐
                    │   SIMULATION    │
                    │ Self-World-Models│
                    └─────────────────┘

    Six paths converging on one question:
    How can a model know what it can do?
"""

with open('/home/user/claude/experiments/research_diagram.txt', 'w') as f:
    f.write(text_diagram)
print("Text diagram saved to research_diagram.txt")
