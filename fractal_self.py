#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program's source code, when rendered visually, resembles its output.
It's a fractal in the sense that the code and what it produces mirror each other.
"""

def sierpinski_carpet(n, char='█', empty=' '):
    """Generate Sierpinski Carpet - a fractal that eats itself"""
    if n == 0:
        return [char]

    prev = sierpinski_carpet(n - 1, char, empty)
    size = len(prev)

    # Build next iteration: 3x3 grid with center empty
    result = []

    # Top row (3 copies)
    for row in prev:
        result.append(row + row + row)

    # Middle row (copy, empty, copy)
    for row in prev:
        result.append(row + (empty * size) + row)

    # Bottom row (3 copies)
    for row in prev:
        result.append(row + row + row)

    return result


# ████████████████████████████████████████████████████
#    T H E   P R O G R A M   B E C O M E S   I T S E L F
# ████████████████████████████████████████████████████

if __name__ == '__main__':
    import sys

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  THE FRACTAL SELF: Code That Visualizes Itself".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    # Generate the fractal
    iteration = 3
    carpet = sierpinski_carpet(iteration, '█', ' ')

    print(f"Sierpinski Carpet (Iteration {iteration}):")
    print("A fractal that removes its own center, recursively.")
    print("Like this code: defined by what it removes from itself.\n")

    for row in carpet:
        print("  " + row)

    print()
    print("Notice:")
    print("  - The pattern repeats at different scales")
    print("  - It's defined by absence (the holes) as much as presence")
    print("  - Each part contains the whole")
    print()

    # Now for the twist: analyze the source code itself
    print("─" * 60)
    print("META-ANALYSIS: This File's Own Structure")
    print("─" * 60)

    # Read our own source
    with open(__file__, 'r') as f:
        source = f.read()

    lines = source.split('\n')
    total_chars = sum(len(line) for line in lines)
    code_chars = sum(len(line) for line in lines if line.strip() and not line.strip().startswith('#'))
    comment_chars = sum(len(line) for line in lines if line.strip().startswith('#'))
    empty_chars = total_chars - code_chars - comment_chars

    print(f"\nTotal characters: {total_chars}")
    print(f"Code characters: {code_chars} ({100*code_chars/total_chars:.1f}%)")
    print(f"Comment characters: {comment_chars} ({100*comment_chars/total_chars:.1f}%)")
    print(f"Whitespace/empty: {empty_chars} ({100*empty_chars/total_chars:.1f}%)")

    print("\nJust like the Sierpinski Carpet:")
    print("  - This file is defined by what's present (code)")
    print("  - And what's absent (whitespace, unwritten possibilities)")
    print("  - The structure emerges from the pattern of inclusion/exclusion")

    # Visualize the code density
    print("\n" + "─" * 60)
    print("Code Density Visualization (each line of this file):")
    print("─" * 60)

    for i, line in enumerate(lines[:60], 1):  # Show first 60 lines
        if len(line) == 0:
            bar = "░"
        else:
            density = len(line.strip()) / max(len(line), 1)
            bar_length = int(density * 40)
            bar = "█" * bar_length + "░" * (40 - bar_length)

        # Show line number and density bar
        print(f"{i:3} │{bar}│")

    print("\n" + "═" * 60)
    print("The program analyzing itself.")
    print("The code becoming self-aware.")
    print("A strange loop.")
    print("═" * 60)
