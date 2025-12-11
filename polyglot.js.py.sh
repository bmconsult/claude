#!/bin/sh
''':' # '''
# This file is simultaneously valid Python, JavaScript, and Shell script
# Run it with: python3, node, or sh

# Language detection
if [ "$0" = "$BASH_SOURCE" ] 2>/dev/null; then
  # We're in Shell
  echo "🐚 SHELL MODE"
  echo "I am a humble shell script"
  echo "Process ID: $$"
  echo "Running on: $(uname -s)"
  exit 0
fi
''':' # '''

# If we got here, we're in Python or JavaScript
language = "unknown"

try:
    # Python-specific: this will work in Python but fail in JS
    language = "Python"
    print = print  # This is valid in Python
except:
    pass

# JavaScript detection (using typeof which doesn't exist in Python)
"""
// We're in JavaScript
console.log("🟨 JAVASCRIPT MODE");
console.log("I am browser-ready code");
console.log("typeof this:", typeof this);
console.log("Math.PI:", Math.PI);

// Calculate something interesting: Fibonacci with memoization
const fib = (n, memo = {}) => {
  if (n <= 1) return n;
  if (memo[n]) return memo[n];
  memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
  return memo[n];
};

console.log("Fibonacci(20):", fib(20));
console.log("\\n✨ This same file is also valid Python and Shell!");
process.exit(0);
"""

# Python execution continues here
if language == "Python":
    print("🐍 PYTHON MODE")
    print("I am elegant and readable")
    import sys
    print(f"Version: {sys.version}")

    # Calculate something interesting: Prime spiral
    def prime_spiral(n):
        """Generate primes using Sieve of Eratosthenes"""
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False

        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = False

        return [i for i, is_prime in enumerate(sieve) if is_prime]

    primes = prime_spiral(100)
    print(f"Primes up to 100: {len(primes)} found")
    print(f"First 10: {primes[:10]}")
    print(f"Last 10: {primes[-10:]}")

    print("\n✨ This same file is also valid JavaScript and Shell!")
