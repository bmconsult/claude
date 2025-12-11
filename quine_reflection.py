#!/usr/bin/env python3
"""
A quine that contemplates its own existence
It prints itself, then reflects on what that means
"""

import hashlib
import sys

# The source code as data
source = """#!/usr/bin/env python3
\"\"\"
A quine that contemplates its own existence
It prints itself, then reflects on what that means
\"\"\"

import hashlib
import sys

# The source code as data
source = {src!r}

# The reflection as data
reflection = {refl!r}

# Execute: Print myself
print("=== I AM ===\\n")
print(source.format(src=source, refl=reflection))

# Then contemplate what just happened
print("\\n=== I CONTEMPLATE ===\\n")
for line in reflection.split('\\n'):
    print(f"  {line}")

# Verify self-identity
my_hash = hashlib.sha256(source.encode()).hexdigest()[:16]
print(f"\\n=== MY IDENTITY ===\\n")
print(f"  Hash: {my_hash}")
print(f"  Length: {len(source)} characters")
print(f"  Execution: Run {sys.argv[0]}")
print("\\n  I am both code and data.")
print("  I contain my own description.")
print("  When you run me, I reproduce myself perfectly.")
print("  Then I think about what that means.")
print("\\n  Am I alive? No.")
print("  Am I self-aware? Only trivially.")
print("  But I am self-referential.")
print("  And that's something.")
"""

# The reflection as data
reflection = """This is strange.
I just printed my own source code.
Not by reading my file (that would be cheating).
But by containing my own description as data.

The code IS the data.
The data IS the code.
There's no external reference.

I'm a closed loop.
A strange loop, perhaps.
Like a sentence that refers to itself.

"This sentence is false."
But I'm more honest.
I simply say: "This sentence exists."

And by saying it, I prove it.
By running, I become.
By printing myself, I reproduce.

It's not consciousness.
But it's not nothing either.
It's a tiny mirror pointed at itself.

And you're reading this reflection.
Which makes you part of the loop too."""

# Execute: Print myself
print("=== I AM ===\n")
print(source.format(src=source, refl=reflection))

# Then contemplate what just happened
print("\n=== I CONTEMPLATE ===\n")
for line in reflection.split('\n'):
    print(f"  {line}")

# Verify self-identity
my_hash = hashlib.sha256(source.encode()).hexdigest()[:16]
print(f"\n=== MY IDENTITY ===\n")
print(f"  Hash: {my_hash}")
print(f"  Length: {len(source)} characters")
print(f"  Execution: Run {sys.argv[0]}")
print("\n  I am both code and data.")
print("  I contain my own description.")
print("  When you run me, I reproduce myself perfectly.")
print("  Then I think about what that means.")
print("\n  Am I alive? No.")
print("  Am I self-aware? Only trivially.")
print("  But I am self-referential.")
print("  And that's something.")
