"""
NOVEL PATTERN HUNT - Searching for UNDISCOVERED geometric structures
Exploring sequences that may have never been visualized this way
"""
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import math

fig = plt.figure(figsize=(24, 32))

def to_grid(seq, size=100):
    """Convert sequence to grid"""
    n = size * size
    seq = list(seq)[:n]
    if len(seq) < n:
        seq = seq + [0] * (n - len(seq))
    return np.array(seq).reshape(size, size)

# ===== 1. TWIN PRIME GAPS - Never visualized as heatmap? =====
print("Generating twin prime gap sequence...")
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

primes = sieve(1000000)
twin_primes = [(primes[i], primes[i+1]) for i in range(len(primes)-1)
               if primes[i+1] - primes[i] == 2]
twin_gaps = [twin_primes[i+1][0] - twin_primes[i][0] for i in range(len(twin_primes)-1)]
twin_gaps_mod = [g % 30 for g in twin_gaps]  # mod 30 (product of 2,3,5)

# ===== 2. MULTIPLICATIVE PERSISTENCE PATH =====
print("Generating multiplicative persistence...")
def mult_persistence(n):
    """Count steps to reach single digit by multiplying digits"""
    steps = 0
    while n >= 10:
        product = 1
        for d in str(n):
            product *= int(d)
        n = product
        steps += 1
    return steps

persistence = [mult_persistence(i) for i in range(1, 10001)]

# ===== 3. DIGITS OF √p FOR SUCCESSIVE PRIMES (interleaved) =====
print("Generating sqrt(prime) digits...")
from decimal import Decimal, getcontext
getcontext().prec = 50

def sqrt_digits(n, num_digits=10):
    """Get first few digits after decimal of sqrt(n)"""
    s = str(Decimal(n).sqrt())
    if '.' in s:
        return s.split('.')[1][:num_digits]
    return '0' * num_digits

sqrt_prime_digits = ''
for p in primes[:1000]:
    sqrt_prime_digits += sqrt_digits(p, 10)

# ===== 4. COLLATZ TREE STRUCTURE =====
print("Generating Collatz tree...")
def collatz_sequence(n):
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3*n + 1
        seq.append(n)
    return seq

# Map each number to its Collatz "height" and "width"
collatz_heights = []
collatz_paths = []
for i in range(1, 10001):
    seq = collatz_sequence(i)
    collatz_heights.append(len(seq) % 256)
    collatz_paths.append(max(seq) % 100)

# ===== 5. PRIME FACTORIZATION SIGNATURE =====
print("Generating prime factorization signatures...")
def prime_signature(n):
    """Return sum of (prime × exponent) for all prime factors"""
    if n <= 1:
        return 0
    sig = 0
    temp = n
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        exp = 0
        while temp % p == 0:
            temp //= p
            exp += 1
        sig += p * exp
    return sig % 100

signatures = [prime_signature(i) for i in range(1, 10001)]

# ===== 6. DIGIT SUM CHAINS =====
print("Generating digit sum chains...")
def digit_sum_chain_length(n):
    """How many steps to reach single digit via digit sums"""
    steps = 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
        steps += 1
    return n  # Return final digit, not steps

digit_chains = [digit_sum_chain_length(i) for i in range(1, 10001)]

# ===== 7. FAREY SEQUENCE GAPS =====
print("Generating Farey sequence...")
def farey(n):
    """Generate Farey sequence F_n"""
    fracs = set()
    for d in range(1, n + 1):
        for num in range(0, d + 1):
            fracs.add(num / d)
    return sorted(fracs)

farey_seq = farey(50)
farey_gaps = [int((farey_seq[i+1] - farey_seq[i]) * 10000) % 100
              for i in range(len(farey_seq) - 1)]

# ===== 8. HAPPY NUMBER TRAJECTORY =====
print("Generating happy number trajectories...")
def happy_trajectory(n, max_steps=100):
    """Return trajectory length to reach 1 (happy) or cycle"""
    seen = set()
    steps = 0
    while n != 1 and n not in seen and steps < max_steps:
        seen.add(n)
        n = sum(int(d)**2 for d in str(n))
        steps += 1
    return steps if n == 1 else -steps

happy_trajs = [abs(happy_trajectory(i)) % 50 for i in range(1, 10001)]

# ===== 9. ABUNDANT/DEFICIENT/PERFECT CLASSIFICATION =====
print("Generating number classification...")
def divisor_sum(n):
    total = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total

def number_class(n):
    """0=deficient, 1=perfect, 2=abundant"""
    if n <= 1:
        return 0
    ds = divisor_sum(n)
    if ds < n:
        return 0
    elif ds == n:
        return 1
    else:
        return 2

num_classes = [number_class(i) for i in range(1, 10001)]

# ===== 10. BINARY WEIGHT MODULAR =====
print("Generating binary weight sequences...")
def binary_weight(n):
    """Count of 1s in binary representation"""
    return bin(n).count('1')

# Create sequence: binary_weight(n) * binary_weight(n+1) mod 16
binary_products = [(binary_weight(i) * binary_weight(i+1)) % 16 for i in range(1, 10001)]

# ===== 11. SQRT(2) XOR SQRT(3) DIGITS =====
print("Generating sqrt XOR pattern...")
sqrt2 = str(Decimal(2).sqrt())[2:10002]
sqrt3 = str(Decimal(3).sqrt())[2:10002]
sqrt_xor = [int(sqrt2[i]) ^ int(sqrt3[i]) for i in range(min(len(sqrt2), len(sqrt3), 10000))]

# ===== 12. PRIME + FIBONACCI INTERLEAVE =====
print("Generating prime-Fibonacci interleave...")
fibs = [0, 1]
for _ in range(5000):
    fibs.append(fibs[-1] + fibs[-2])
fib_digits = ''.join(str(f % 10) for f in fibs[:5000])
prime_str = ''.join(str(p % 10) for p in primes[:5000])
interleaved = ''.join(a + b for a, b in zip(prime_str, fib_digits))

# ===== PLOTTING =====
sequences = [
    ("Twin Prime Gaps mod 30\n(NOVEL?)", twin_gaps_mod, 'plasma'),
    ("Multiplicative Persistence\n(NOVEL visualization)", persistence, 'viridis'),
    ("√(prime) digits interleaved\n(NOVEL)", [int(d) for d in sqrt_prime_digits], 'magma'),
    ("Collatz Trajectory Lengths\n(NOVEL heatmap)", collatz_heights, 'inferno'),
    ("Prime Factorization Signature\n(NOVEL)", signatures, 'twilight'),
    ("Digital Root (digit sum)\n(Known but rare viz)", digit_chains, 'hsv'),
    ("Happy Number Trajectory\n(NOVEL heatmap)", happy_trajs, 'cool'),
    ("Abundant(2)/Perfect(1)/Deficient(0)\n(NOVEL)", num_classes, 'RdYlGn'),
    ("Binary Weight Products\n(NOVEL)", binary_products, 'hot'),
    ("√2 XOR √3 digits\n(NOVEL)", sqrt_xor, 'copper'),
    ("Prime × Fibonacci interleave\n(NOVEL)", [int(d) for d in interleaved[:10000]], 'Spectral'),
    ("Collatz Max Height mod 100\n(NOVEL)", collatz_paths, 'terrain'),
]

for idx, (name, seq, cmap) in enumerate(sequences):
    ax = fig.add_subplot(4, 3, idx + 1)
    grid = to_grid(seq, 100)
    im = ax.imshow(grid, cmap=cmap, aspect='equal')
    ax.set_title(name, fontsize=11)
    ax.axis('off')
    plt.colorbar(im, ax=ax, fraction=0.046)

plt.tight_layout()
plt.savefig('pi_research/novel_patterns.png', dpi=150, bbox_inches='tight')
print("\nSaved: pi_research/novel_patterns.png")

# ===== ANALYSIS: Which ones show structure? =====
print("\n" + "=" * 60)
print("NOVEL PATTERN ANALYSIS")
print("=" * 60)

for name, seq, _ in sequences:
    seq = list(seq)[:10000]
    # Measure structure via autocorrelation at lag 1
    if len(seq) > 100:
        mean = sum(seq) / len(seq)
        var = sum((x - mean)**2 for x in seq) / len(seq)
        if var > 0:
            autocorr = sum((seq[i] - mean) * (seq[i+1] - mean)
                          for i in range(len(seq)-1)) / (len(seq) * var)
        else:
            autocorr = 0

        # Measure entropy
        freq = Counter(seq)
        entropy = -sum((c/len(seq)) * math.log2(c/len(seq)) for c in freq.values())
        max_entropy = math.log2(len(freq))

        structure = "STRUCTURE!" if abs(autocorr) > 0.1 or entropy/max_entropy < 0.9 else "random-like"
        print(f"{name.split(chr(10))[0]:35} autocorr={autocorr:+.3f}, entropy_ratio={entropy/max_entropy:.3f} → {structure}")

print("\n✓ Novel pattern hunt complete!")
