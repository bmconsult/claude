#!/usr/bin/env python3
"""
Mathematical Beauty Visualizations
Visual proofs and patterns that reveal mathematical elegance.
"""

import math

def odd_numbers_sum_to_squares(n=8):
    """
    Visual proof: Sum of first n odd numbers = n²

    1 = 1       = 1²
    1+3 = 4     = 2²
    1+3+5 = 9   = 3²
    ...

    Visualized as a growing square made of L-shaped pieces.
    """
    print("Visual Proof: Sum of Odd Numbers = n²\n")

    chars = ['█', '▓', '▒', '░', '◆', '◇', '●', '○']

    for size in range(1, n + 1):
        # The n-th odd number is 2n-1
        # It forms an L-shape around the previous square

        # Build the square
        for row in range(size):
            line = ""
            for col in range(size):
                # Determine which "layer" this cell belongs to
                layer = max(row, col)  # 0-indexed layer
                char = chars[layer % len(chars)]
                line += char + " "
            print(line)
        print(f"\nSize {size}×{size}: Sum of odds 1+3+...+{2*size-1} = {sum(range(1, 2*size, 2))} = {size}²")
        print("-" * 30)


def spiral_primes(size=20):
    """
    Ulam spiral: arrange integers in a spiral, mark primes.
    Primes tend to fall along diagonal lines - unexpected pattern.
    """
    print(f"Ulam Spiral ({size}×{size}): Primes marked with █\n")

    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    # Generate spiral coordinates
    grid = [[0] * size for _ in range(size)]

    x, y = size // 2, size // 2
    dx, dy = 1, 0
    num = 1
    steps_in_direction = 1
    steps_taken = 0
    direction_changes = 0

    while 0 <= x < size and 0 <= y < size:
        grid[y][x] = num
        num += 1
        x += dx
        y += dy
        steps_taken += 1

        if steps_taken == steps_in_direction:
            steps_taken = 0
            # Turn left
            dx, dy = -dy, dx
            direction_changes += 1
            if direction_changes % 2 == 0:
                steps_in_direction += 1

    # Print grid
    for row in grid:
        line = ""
        for val in row:
            if val == 0:
                line += "  "
            elif is_prime(val):
                line += "██"
            else:
                line += "· "
        print(line)
    print("\nDiagonal patterns emerge from seemingly random primes.")


def fibonacci_spiral():
    """
    Fibonacci spiral approximation using ASCII.
    Shows the golden ratio emerging from simple recursion.
    """
    print("Fibonacci Spiral Pattern\n")

    # Generate Fibonacci boxes
    fibs = [1, 1]
    for _ in range(6):
        fibs.append(fibs[-1] + fibs[-2])

    print("Fibonacci sequence:", fibs[:8])
    print("\nGolden ratio approximation from consecutive terms:")
    for i in range(2, 7):
        ratio = fibs[i] / fibs[i-1]
        phi = (1 + math.sqrt(5)) / 2
        print(f"  {fibs[i]}/{fibs[i-1]} = {ratio:.6f}  (φ = {phi:.6f})")

    print("\nASCII spiral approximation:\n")
    spiral = """
           ╭──────────────────────╮
           │                      │
           │   ╭─────────╮        │
           │   │         │        │
           │   │   ╭──╮  │        │
           │   │   │1 │  │        │
           │   │   │  │1 │   5    │
           │   │   ╰──┴──╯        │
           │   │    2    │        │
           │   │         │        │
           │   ╰─────────╯   8    │
           │        3             │
           │                      │
           ╰──────────────────────╯
                     13
    """
    print(spiral)


def pascals_triangle_patterns(rows=12):
    """
    Pascal's triangle with patterns highlighted.
    Contains: powers of 2, Fibonacci numbers, binomial coefficients.
    """
    print(f"Pascal's Triangle ({rows} rows)\n")

    # Generate triangle
    triangle = []
    for n in range(rows):
        row = []
        for k in range(n + 1):
            if k == 0 or k == n:
                row.append(1)
            else:
                row.append(triangle[n-1][k-1] + triangle[n-1][k])
        triangle.append(row)

    # Find max width for formatting
    max_val = max(max(row) for row in triangle)
    width = len(str(max_val)) + 1

    # Print centered
    for i, row in enumerate(triangle):
        padding = " " * (width * (rows - i - 1) // 2)
        line = padding
        for val in row:
            line += str(val).center(width)
        print(line)

    print("\nPatterns hidden within:")
    print("• Row sums = powers of 2:", [sum(row) for row in triangle[:8]])
    print("• Diagonals contain Fibonacci numbers")
    print("• Entry (n,k) = C(n,k) = n!/(k!(n-k)!)")


def symmetry_groups_tiling():
    """
    Simple demonstration of wallpaper group symmetries.
    """
    print("Symmetry in Tiling: Simple Pattern\n")

    # Simple pattern with translation symmetry
    pattern = """
    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲
    ╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱
    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲
    ╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱
    ╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲
    ╲╱╲╱╲╱╲╱╲╱╲╱╲╱╲╱
    """
    print(pattern)
    print("This simple pattern has:")
    print("• Translation symmetry (repeats horizontally and vertically)")
    print("• Reflection symmetry (horizontal and vertical axes)")
    print("• 180° rotational symmetry")
    print("\nThe Alhambra contains all 17 possible wallpaper symmetry groups.")


if __name__ == "__main__":
    print("="*60)
    print("MATHEMATICAL BEAUTY VISUALIZATIONS")
    print("="*60)
    print()

    odd_numbers_sum_to_squares(5)
    print("\n" + "="*60 + "\n")

    pascals_triangle_patterns(10)
    print("\n" + "="*60 + "\n")

    fibonacci_spiral()
    print("\n" + "="*60 + "\n")

    spiral_primes(15)
    print("\n" + "="*60 + "\n")

    symmetry_groups_tiling()
