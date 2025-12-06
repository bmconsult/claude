"""
Cellular Automaton Explorer
Just playing with emergence. Not for anyone.
"""

import random

def rule_to_binary(rule_number):
    """Convert rule number to 8-bit binary lookup table."""
    return [(rule_number >> i) & 1 for i in range(8)]

def step(row, rule):
    """Apply 1D cellular automaton rule."""
    n = len(row)
    new_row = [0] * n
    for i in range(n):
        # Get neighborhood (wrapping)
        left = row[(i - 1) % n]
        center = row[i]
        right = row[(i + 1) % n]
        # Convert to index (0-7)
        index = (left << 2) | (center << 1) | right
        new_row[i] = rule[index]
    return new_row

def generate_pattern(rule_number, width=79, height=40, seed='center'):
    """Generate a pattern from a rule."""
    rule = rule_to_binary(rule_number)

    # Initialize
    if seed == 'center':
        row = [0] * width
        row[width // 2] = 1
    elif seed == 'random':
        row = [random.randint(0, 1) for _ in range(width)]
    else:
        row = [int(c) for c in seed.ljust(width, '0')[:width]]

    # Generate
    rows = [row]
    for _ in range(height - 1):
        row = step(row, rule)
        rows.append(row)

    return rows

def render(pattern, chars=' █'):
    """Convert to string art."""
    lines = []
    for row in pattern:
        line = ''.join(chars[cell] for cell in row)
        lines.append(line)
    return '\n'.join(lines)

# Explore some rules
def main():
    interesting_rules = [30, 90, 110, 184, 45, 73]

    for rule_num in interesting_rules:
        print(f"\n{'='*79}")
        print(f"Rule {rule_num}")
        print('='*79)
        pattern = generate_pattern(rule_num)
        print(render(pattern))

        # Simple analysis
        flat = [cell for row in pattern for cell in row]
        density = sum(flat) / len(flat)
        print(f"\nDensity: {density:.3f}")

        # Check for obvious periodicity in last 10 rows
        last_rows = pattern[-10:]
        unique_rows = len(set(tuple(r) for r in last_rows))
        print(f"Unique patterns in last 10 rows: {unique_rows}")

if __name__ == "__main__":
    main()
