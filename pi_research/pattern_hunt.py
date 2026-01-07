"""
HUNT FOR GEOMETRIC PATTERNS IN NUMBER SEQUENCES
Testing various mathematical sequences for visual structure
"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from collections import Counter
import math

# Create massive figure with many candidates
fig = plt.figure(figsize=(24, 32))

def digits_to_grid(digits, size=100):
    """Convert digit string to square grid"""
    n = size * size
    if len(digits) < n:
        digits = digits + '0' * (n - len(digits))
    return np.array([int(d) for d in digits[:n]]).reshape(size, size)

def sequence_to_digits(seq, base=10):
    """Convert sequence of integers to digit string"""
    return ''.join(str(x % base) for x in seq)

# ===== 1. CHAMPERNOWNE'S CONSTANT (0.123456789101112...) =====
champernowne = ''.join(str(i) for i in range(1, 10001))

# ===== 2. COPELAND-ERDŐS (Primes concatenated) =====
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

primes = sieve(100000)
copeland_erdos = ''.join(str(p) for p in primes)

# ===== 3. THUE-MORSE SEQUENCE (Fractal structure!) =====
def thue_morse(n):
    """Generate Thue-Morse sequence: count 1-bits in binary representation"""
    return [bin(i).count('1') % 2 for i in range(n)]

tm = thue_morse(10000)

# ===== 4. FIBONACCI MOD 10 =====
def fib_mod(n, mod=10):
    seq = [0, 1]
    for _ in range(n - 2):
        seq.append((seq[-1] + seq[-2]) % mod)
    return seq

fib_digits = fib_mod(10000)

# ===== 5. COLLATZ SEQUENCE LENGTHS =====
def collatz_length(n):
    count = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3*n + 1
        count += 1
    return count

collatz_lengths = [collatz_length(i) % 10 for i in range(1, 10001)]

# ===== 6. PRIME GAPS MOD 10 =====
prime_gaps = [(primes[i+1] - primes[i]) % 10 for i in range(len(primes)-1)]

# ===== 7. RULER SEQUENCE (Binary: trailing zeros + 1) =====
def ruler_sequence(n):
    """a(n) = largest power of 2 dividing n"""
    seq = []
    for i in range(1, n + 1):
        k = 0
        while i % (2 ** (k + 1)) == 0:
            k += 1
        seq.append(k % 10)
    return seq

ruler = ruler_sequence(10000)

# ===== 8. PASCAL'S TRIANGLE MOD 2 (Sierpinski!) =====
def pascal_mod(rows, mod=2):
    """Generate Pascal's triangle mod n as flat sequence"""
    triangle = [[1]]
    for i in range(1, rows):
        row = [1]
        for j in range(1, i):
            row.append((triangle[i-1][j-1] + triangle[i-1][j]) % mod)
        row.append(1)
        triangle.append(row)
    return triangle

pascal = pascal_mod(200, 2)

# ===== 9. ULAM SPIRAL (Primes on spiral) =====
def ulam_spiral(size):
    """Generate Ulam spiral - 1 if prime, 0 otherwise"""
    grid = np.zeros((size, size), dtype=int)
    x, y = size // 2, size // 2
    dx, dy = 1, 0
    steps = 1
    n = 1

    prime_set = set(sieve(size * size + 1))

    while 0 <= x < size and 0 <= y < size:
        for _ in range(2):  # Two legs per step size
            for _ in range(steps):
                if 0 <= x < size and 0 <= y < size:
                    grid[y, x] = 1 if n in prime_set else 0
                    n += 1
                x, y = x + dx, y + dy
            dx, dy = -dy, dx  # Turn left
        steps += 1

    return grid

# ===== 10. RECAMÁN'S SEQUENCE =====
def recaman(n):
    seq = [0]
    seen = {0}
    for i in range(1, n):
        prev = seq[-1]
        candidate = prev - i
        if candidate > 0 and candidate not in seen:
            seq.append(candidate)
        else:
            seq.append(prev + i)
        seen.add(seq[-1])
    return [x % 10 for x in seq]

recaman_seq = recaman(10000)

# ===== 11. STERN-BROCOT SEQUENCE =====
def stern_brocot(n):
    """Stern's diatomic sequence"""
    seq = [0, 1]
    for i in range(2, n):
        if i % 2 == 0:
            seq.append(seq[i // 2])
        else:
            seq.append(seq[i // 2] + seq[i // 2 + 1])
    return [x % 10 for x in seq]

stern = stern_brocot(10000)

# ===== 12. LOGISTIC MAP (Chaos!) =====
def logistic_map(r, x0, n):
    """x_{n+1} = r * x_n * (1 - x_n)"""
    seq = [x0]
    for _ in range(n - 1):
        seq.append(r * seq[-1] * (1 - seq[-1]))
    # Convert to digits
    return [int(x * 10) % 10 for x in seq]

logistic = logistic_map(3.99, 0.1, 10000)  # Chaotic regime

# ===== PLOTTING =====
sequences = [
    ("Champernowne (1,2,3...)", champernowne, 'sequential'),
    ("Copeland-Erdős (primes)", copeland_erdos, 'viridis'),
    ("Thue-Morse", ''.join(str(x) for x in tm), 'binary'),
    ("Fibonacci mod 10", ''.join(str(x) for x in fib_digits), 'hsv'),
    ("Collatz lengths mod 10", ''.join(str(x) for x in collatz_lengths), 'plasma'),
    ("Prime gaps mod 10", ''.join(str(x) for x in prime_gaps), 'magma'),
    ("Ruler sequence", ''.join(str(x) for x in ruler), 'coolwarm'),
    ("Recamán mod 10", ''.join(str(x) for x in recaman_seq), 'Spectral'),
    ("Stern-Brocot mod 10", ''.join(str(x) for x in stern), 'twilight'),
    ("Logistic map (chaotic)", ''.join(str(x) for x in logistic), 'inferno'),
]

# Plot the first 10 as grids
for idx, (name, digits, cmap) in enumerate(sequences):
    ax = fig.add_subplot(4, 3, idx + 1)
    grid = digits_to_grid(digits, 100)
    if cmap == 'binary':
        im = ax.imshow(grid, cmap='gray', aspect='equal')
    else:
        im = ax.imshow(grid, cmap=cmap if cmap != 'sequential' else 'viridis', aspect='equal')
    ax.set_title(name, fontsize=12)
    ax.axis('off')

# Special: Pascal's Triangle (Sierpinski)
ax11 = fig.add_subplot(4, 3, 11)
# Create image from Pascal triangle
max_row = len(pascal)
pascal_img = np.zeros((max_row, max_row))
for i, row in enumerate(pascal):
    offset = (max_row - len(row)) // 2
    for j, val in enumerate(row):
        pascal_img[i, offset + j] = val
ax11.imshow(pascal_img, cmap='binary', aspect='equal')
ax11.set_title("Pascal's Triangle mod 2 (SIERPINSKI!)", fontsize=12)
ax11.axis('off')

# Special: Ulam Spiral
ax12 = fig.add_subplot(4, 3, 12)
ulam = ulam_spiral(200)
ax12.imshow(ulam, cmap='binary', aspect='equal')
ax12.set_title("Ulam Spiral (primes show DIAGONALS!)", fontsize=12)
ax12.axis('off')

plt.tight_layout()
plt.savefig('pi_research/sequence_patterns.png', dpi=150, bbox_inches='tight')
print("Saved: pi_research/sequence_patterns.png")

# ===== ADDITIONAL: High-detail views of the most interesting ones =====
fig2, axes = plt.subplots(2, 2, figsize=(16, 16))

# Thue-Morse larger
ax = axes[0, 0]
tm_large = thue_morse(40000)
tm_grid = np.array(tm_large).reshape(200, 200)
ax.imshow(tm_grid, cmap='binary', aspect='equal')
ax.set_title('Thue-Morse 200×200 (FRACTAL STRUCTURE!)', fontsize=14)
ax.axis('off')

# Ruler sequence larger
ax = axes[0, 1]
ruler_large = ruler_sequence(40000)
ruler_grid = np.array(ruler_large).reshape(200, 200)
ax.imshow(ruler_grid, cmap='hot', aspect='equal')
ax.set_title('Ruler Sequence 200×200 (BINARY TREE!)', fontsize=14)
ax.axis('off')

# Fibonacci mod with different mod values
ax = axes[1, 0]
fib_mod_large = fib_mod(40000, mod=10)
fib_grid = np.array(fib_mod_large).reshape(200, 200)
ax.imshow(fib_grid, cmap='hsv', aspect='equal')
ax.set_title('Fibonacci mod 10 (PERIODIC!)', fontsize=14)
ax.axis('off')

# Pascal mod 3
ax = axes[1, 1]
pascal3 = pascal_mod(300, 3)
max_row = len(pascal3)
pascal3_img = np.zeros((max_row, max_row))
for i, row in enumerate(pascal3):
    offset = (max_row - len(row)) // 2
    for j, val in enumerate(row):
        pascal3_img[i, offset + j] = val
ax.imshow(pascal3_img, cmap='viridis', aspect='equal')
ax.set_title("Pascal mod 3 (SIERPINSKI VARIANT!)", fontsize=14)
ax.axis('off')

plt.tight_layout()
plt.savefig('pi_research/geometric_patterns_detail.png', dpi=150, bbox_inches='tight')
print("Saved: pi_research/geometric_patterns_detail.png")

print("\n" + "=" * 60)
print("SEQUENCES THAT PRODUCE GEOMETRIC PATTERNS:")
print("=" * 60)
print("""
✓ THUE-MORSE: Perfect fractal self-similarity!
✓ RULER SEQUENCE: Binary tree structure
✓ PASCAL MOD 2: Sierpinski triangle (famous!)
✓ PASCAL MOD 3: Sierpinski variant with 3 colors
✓ ULAM SPIRAL: Diagonal lines emerge from primes
✓ FIBONACCI MOD N: Periodic with clear bands

These are NOT random - they have structure that
shows up visually. Compare to π which is pure noise!
""")
