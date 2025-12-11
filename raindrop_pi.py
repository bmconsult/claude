#!/usr/bin/env python3
"""
Discovering Pi through the poetry of random raindrops
Mathematical truth emerging from chaos
"""

import random
import math
import time

def raindrop_pi(total_drops=100000, poetry_mode=True):
    """
    Imagine a square with a circle inscribed in it.
    Raindrops fall randomly on the square.
    The ratio of drops inside vs outside reveals π.

    This is math as weather.
    """

    inside_circle = 0
    total_drops_so_far = 0

    if poetry_mode:
        print("🌧️  THE RAIN BEGINS\n")
        print("A square field, side length 2")
        print("A circle inscribed within, radius 1")
        print("Raindrops fall randomly...\n")
        time.sleep(1)

    # Checkpoints for poetic narration
    checkpoints = [100, 1000, 10000, 50000, total_drops]
    next_checkpoint = 0

    for drop in range(total_drops):
        # Random raindrop position (-1 to 1 in x and y)
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        # Is it inside the circle?
        distance = math.sqrt(x*x + y*y)
        if distance <= 1:
            inside_circle += 1

        total_drops_so_far += 1

        # Poetic checkpoints
        if poetry_mode and total_drops_so_far == checkpoints[next_checkpoint]:
            estimated_pi = 4 * (inside_circle / total_drops_so_far)
            error = abs(estimated_pi - math.pi)

            print(f"After {total_drops_so_far:,} raindrops:")
            print(f"  Inside circle: {inside_circle:,}")
            print(f"  Outside circle: {total_drops_so_far - inside_circle:,}")
            print(f"  Ratio: {inside_circle/total_drops_so_far:.6f}")
            print(f"  Estimated π: {estimated_pi:.8f}")
            print(f"  True π:      {math.pi:.8f}")
            print(f"  Error:       {error:.8f}")

            # Poetic commentary
            if next_checkpoint == 0:
                print("  (Chaos begins to hint at order...)")
            elif next_checkpoint == 1:
                print("  (A pattern emerges from randomness...)")
            elif next_checkpoint == 2:
                print("  (The circle reveals itself...)")
            elif next_checkpoint == 3:
                print("  (Getting closer to truth...)")
            else:
                print("  (The rain has spoken.)")

            print()
            next_checkpoint += 1

    final_pi = 4 * (inside_circle / total_drops)

    if poetry_mode:
        print("🌈 THE RAIN STOPS\n")
        print("From pure randomness,")
        print("From countless chaotic raindrops,")
        print("Mathematical truth emerged.")
        print()
        print(f"π ≈ {final_pi:.10f}")
        print()
        print("This is the magic:")
        print("Order hiding in chaos,")
        print("Truth accessible through randomness,")
        print("The universe calculating itself.")
        print()
        print("We didn't compute π.")
        print("We let it rain until π appeared.")

    return final_pi


if __name__ == '__main__':
    print("=" * 60)
    print("  MONTE CARLO POETRY: Discovering π Through Raindrops")
    print("=" * 60)
    print()

    discovered_pi = raindrop_pi(total_drops=100000, poetry_mode=True)

    print("\n" + "=" * 60)
    print("\nP.S. This works because:")
    print("  Circle area = πr² = π (when r=1)")
    print("  Square area = (2r)² = 4")
    print("  Ratio = π/4")
    print("  Therefore: π = 4 × (drops in circle / total drops)")
    print("\nMathematics is a strange rain.")
    print("=" * 60)
