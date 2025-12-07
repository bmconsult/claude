import math
import time
import sys

def wave(t, width=60):
    """Generate one frame of an ASCII wave."""
    for y in range(10):
        line = ""
        for x in range(width):
            val = math.sin((x / 5) + t) * 4 + 5
            if abs(y - val) < 0.5:
                line += "~"
            else:
                line += " "
        print(line)
    print()

# Single frame - no animation since we can't clear screen
t = 0
wave(t)
print("A wave, frozen.")
