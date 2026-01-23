"""
Experiment 14: HDC/VSA (Hyperdimensional Computing / Vector Symbolic Architectures)

This is a COMPLETELY DIFFERENT paradigm from neural networks.

Key ideas:
1. Represent everything with HIGH-DIMENSIONAL random vectors (10,000+ dims)
2. BINDING: Combine position and value (XOR or element-wise multiply)
3. BUNDLING: Sum all bindings to represent a sequence
4. SIMILARITY: Cosine similarity to compare/retrieve

Why this might work for positional transforms:
- Position is EXPLICITLY encoded in the vector
- No gradient descent needed - algebraic operations
- Extremely sparse and efficient
- Built-in compositional structure

Example:
  Sequence [3, 7, 2] becomes:
    (P0 ⊗ V3) + (P1 ⊗ V7) + (P2 ⊗ V2)

  Where P0, P1, P2 are position vectors and V3, V7, V2 are value vectors.

Success criteria (from charter):
- >80% accuracy on positional transforms
- Learning curve shows transfer
- <1M parameters (HDC uses fixed codebooks, very sparse)
- Runs on laptop CPU
- Generalizes to novel inputs
"""

import torch
import torch.nn.functional as F
from typing import List, Tuple, Dict
import random
import math


# =============================================================================
# PART 1: HDC CODEBOOK
# =============================================================================

class HDCCodebook:
    """
    High-dimensional codebook for symbols.

    Each symbol (position, value) gets a random high-dimensional vector.
    These are fixed (not learned) - the power comes from the algebra.
    """

    def __init__(self, dim: int = 10000, sparsity: float = 0.01):
        """
        Args:
            dim: Dimensionality of vectors (higher = more capacity)
            sparsity: Fraction of non-zero elements (lower = more efficient)
        """
        self.dim = dim
        self.sparsity = sparsity

        # Position vectors (for sequence positions)
        self.position_vectors: Dict[int, torch.Tensor] = {}

        # Value vectors (for sequence values)
        self.value_vectors: Dict[int, torch.Tensor] = {}

    def get_position_vector(self, pos: int) -> torch.Tensor:
        """Get or create vector for a position."""
        if pos not in self.position_vectors:
            self.position_vectors[pos] = self._random_vector()
        return self.position_vectors[pos]

    def get_value_vector(self, val: int) -> torch.Tensor:
        """Get or create vector for a value."""
        if val not in self.value_vectors:
            self.value_vectors[val] = self._random_vector()
        return self.value_vectors[val]

    def _random_vector(self) -> torch.Tensor:
        """Create a random sparse binary vector."""
        # Sparse: only `sparsity` fraction are +1 or -1
        vec = torch.zeros(self.dim)
        num_active = int(self.dim * self.sparsity)
        indices = random.sample(range(self.dim), num_active)

        for idx in indices:
            vec[idx] = random.choice([-1.0, 1.0])

        return vec


# =============================================================================
# PART 2: HDC OPERATIONS
# =============================================================================

def bind(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Binding operation: associates two concepts.

    Uses element-wise multiplication (XOR for binary).
    Binding is its own inverse: bind(bind(a, b), b) ≈ a
    """
    return a * b


def unbind(bound: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """Unbind: recover a from bind(a, b) using b."""
    return bound * b  # Same as bind since it's self-inverse


def bundle(*vectors: torch.Tensor) -> torch.Tensor:
    """
    Bundling operation: combines multiple concepts.

    Uses element-wise addition (like a "superposition").
    Result is similar to all inputs.
    """
    result = torch.zeros_like(vectors[0])
    for v in vectors:
        result = result + v
    return result


def similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    """Cosine similarity between vectors."""
    return F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()


# =============================================================================
# PART 3: SEQUENCE ENCODING/DECODING
# =============================================================================

class HDCSequenceEncoder:
    """
    Encode sequences as HDC vectors.

    Sequence [v0, v1, v2, ...] becomes:
        bundle(bind(P0, V_v0), bind(P1, V_v1), ...)

    This EXPLICITLY encodes position in the vector structure.
    """

    def __init__(self, codebook: HDCCodebook):
        self.codebook = codebook

    def encode(self, seq: List[int]) -> torch.Tensor:
        """Encode a sequence as a single HDC vector."""
        bindings = []
        for pos, val in enumerate(seq):
            p_vec = self.codebook.get_position_vector(pos)
            v_vec = self.codebook.get_value_vector(val)
            bindings.append(bind(p_vec, v_vec))

        return bundle(*bindings) if bindings else torch.zeros(self.codebook.dim)

    def decode(self, vec: torch.Tensor, length: int) -> List[int]:
        """
        Decode a vector back to a sequence.

        For each position, unbind with position vector and find most similar value.
        """
        result = []

        for pos in range(length):
            p_vec = self.codebook.get_position_vector(pos)
            unbound = unbind(vec, p_vec)

            # Find most similar value vector
            best_val = 0
            best_sim = -1

            for val in range(20):  # Check values 0-19
                v_vec = self.codebook.get_value_vector(val)
                sim = similarity(unbound, v_vec)
                if sim > best_sim:
                    best_sim = sim
                    best_val = val

            result.append(best_val)

        return result


# =============================================================================
# PART 4: LEARNING TRANSFORMS
# =============================================================================

class HDCTransformLearner:
    """
    Learn sequence transformations in HDC space.

    Method:
    1. Encode input and output sequences
    2. Learn a transformation that maps input encoding to output encoding
    3. For new input: encode → transform → decode

    The transformation is learned as a linear mapping in HD space.
    """

    def __init__(self, dim: int = 10000, sparsity: float = 0.01):
        self.dim = dim
        self.codebook = HDCCodebook(dim=dim, sparsity=sparsity)
        self.encoder = HDCSequenceEncoder(self.codebook)

        # Learned transform (accumulator of input-output associations)
        self.transform_matrix = None
        self.num_examples = 0

    def learn(self, input_seq: List[int], output_seq: List[int]):
        """
        Learn from an (input, output) example.

        Uses Hebbian-style learning: strengthen connection between input and output.
        """
        enc_in = self.encoder.encode(input_seq)
        enc_out = self.encoder.encode(output_seq)

        # Outer product gives association matrix
        # But that's O(dim^2) which is huge for dim=10000
        # Instead, use a simpler approach: store example pairs

        if self.transform_matrix is None:
            # Initialize as identity-ish
            self.transform_matrix = {
                'inputs': [enc_in],
                'outputs': [enc_out]
            }
        else:
            self.transform_matrix['inputs'].append(enc_in)
            self.transform_matrix['outputs'].append(enc_out)

        self.num_examples += 1

    def predict(self, input_seq: List[int]) -> List[int]:
        """Predict output for a new input."""
        if self.transform_matrix is None:
            return input_seq  # No learning yet

        enc_in = self.encoder.encode(input_seq)

        # Find most similar stored input
        best_idx = 0
        best_sim = -1

        for i, stored_in in enumerate(self.transform_matrix['inputs']):
            sim = similarity(enc_in, stored_in)
            if sim > best_sim:
                best_sim = sim
                best_idx = i

        # Return corresponding output
        enc_out = self.transform_matrix['outputs'][best_idx]

        # Decode
        return self.encoder.decode(enc_out, len(input_seq))

    def predict_weighted(self, input_seq: List[int]) -> List[int]:
        """
        Predict using weighted combination of all examples.

        More sophisticated: weight each stored output by input similarity.
        """
        if self.transform_matrix is None:
            return input_seq

        enc_in = self.encoder.encode(input_seq)

        # Compute similarities to all stored inputs
        sims = []
        for stored_in in self.transform_matrix['inputs']:
            sims.append(similarity(enc_in, stored_in))

        # Softmax for weights
        sims = torch.tensor(sims)
        weights = F.softmax(sims * 10, dim=0)  # Temperature 10

        # Weighted combination of outputs
        combined_out = torch.zeros(self.dim)
        for i, w in enumerate(weights):
            combined_out += w * self.transform_matrix['outputs'][i]

        return self.encoder.decode(combined_out, len(input_seq))

    def reset(self):
        """Reset for new transform type."""
        self.transform_matrix = None
        self.num_examples = 0
        # Keep codebook (transfer!)


# =============================================================================
# PART 5: TESTING
# =============================================================================

def generate_task(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """Generate a (input, output) pair for a transform."""
    input_seq = [random.randint(1, 9) for _ in range(length)]

    if transform_name == 'identity':
        output_seq = input_seq.copy()
    elif transform_name == 'increment':
        output_seq = [x + 1 for x in input_seq]
    elif transform_name == 'reverse':
        output_seq = input_seq[::-1]
    elif transform_name == 'swap_pairs':
        output_seq = []
        for i in range(0, len(input_seq) - 1, 2):
            output_seq.extend([input_seq[i+1], input_seq[i]])
        if len(input_seq) % 2 == 1:
            output_seq.append(input_seq[-1])
    elif transform_name == 'running_max':
        output_seq = []
        current_max = 0
        for x in input_seq:
            current_max = max(current_max, x)
            output_seq.append(current_max)
    elif transform_name == 'mirror_add':
        output_seq = [input_seq[i] + input_seq[-(i+1)] for i in range(len(input_seq))]
    else:
        raise ValueError(f"Unknown transform: {transform_name}")

    return input_seq, output_seq


def test_transform(system: HDCTransformLearner, transform_name: str,
                   num_train: int = 50, num_test: int = 5,
                   use_weighted: bool = True) -> Tuple[int, int]:
    """
    Test system on a transform.

    1. Train on num_train examples
    2. Test on num_test NEW examples
    """
    print(f"\n  Testing {transform_name}:")

    # Reset but keep codebook (transfer)
    system.reset()

    # Training phase
    print(f"    Training on {num_train} examples...")
    for i in range(num_train):
        input_seq, output_seq = generate_task(transform_name)
        system.learn(input_seq, output_seq)

    # Testing phase
    print(f"    Testing on {num_test} NEW examples...")
    correct = 0

    for i in range(num_test):
        input_seq, output_seq = generate_task(transform_name)

        if use_weighted:
            predicted = system.predict_weighted(input_seq)
        else:
            predicted = system.predict(input_seq)

        if predicted == output_seq:
            correct += 1
            print(f"      Test {i+1}: ✓ {input_seq} → {predicted}")
        else:
            print(f"      Test {i+1}: ✗ {input_seq} → {predicted} (expected {output_seq})")

    return correct, num_train


def main():
    """Run Experiment 14: HDC/VSA Encoding."""
    print("=" * 70)
    print("EXPERIMENT 14: HDC/VSA (Hyperdimensional Computing)")
    print("=" * 70)
    print("\nThis is a COMPLETELY DIFFERENT paradigm.")
    print("High-dimensional vectors + algebraic operations")
    print("Position EXPLICITLY encoded via binding")
    print("\nSuccess criteria:")
    print("  - >80% on positional transforms")
    print("  - Generalizes to NEW inputs")
    print("  - Very sparse and efficient")
    print("=" * 70)

    # Create system (10,000 dimensions, 1% sparsity)
    system = HDCTransformLearner(dim=10000, sparsity=0.01)

    # Test transforms
    transforms = [
        'identity',
        'increment',
        'reverse',
        'running_max',
        'swap_pairs',
        'mirror_add',
    ]

    results = {}

    for transform in transforms:
        correct, num_train = test_transform(system, transform, num_train=50, num_test=5)
        results[transform] = {
            'accuracy': correct / 5,
            'num_examples': num_train
        }
        print(f"\n  Result: {correct}/5 ({correct/5*100:.0f}%)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    element_wise = ['identity', 'increment']
    positional = ['reverse', 'running_max', 'swap_pairs', 'mirror_add']

    ew_acc = sum(results[t]['accuracy'] for t in element_wise) / len(element_wise)
    pos_acc = sum(results[t]['accuracy'] for t in positional) / len(positional)

    print(f"\nElement-wise accuracy: {ew_acc*100:.0f}%")
    print(f"Positional accuracy: {pos_acc*100:.0f}%")
    print(f"Overall accuracy: {(ew_acc + pos_acc) / 2 * 100:.0f}%")

    # Memory usage
    num_vectors = len(system.codebook.position_vectors) + len(system.codebook.value_vectors)
    memory = num_vectors * system.dim * 4 / 1024 / 1024  # MB (float32)
    print(f"\nCodebook: {num_vectors} vectors × {system.dim} dims")
    print(f"Memory: ~{memory:.1f} MB")
    print(f"Sparsity: {system.codebook.sparsity * 100:.0f}% active")

    # Verdict
    print("\n" + "=" * 70)
    if pos_acc >= 0.8:
        print("SUCCESS: >80% on positional transforms!")
        print("HDC/VSA WORKS for sequences.")
    elif pos_acc > 0:
        print(f"PARTIAL: {pos_acc*100:.0f}% on positional (need >80%)")
        print("HDC shows promise but needs more examples or better encoding.")
    else:
        print(f"NOT YET: {pos_acc*100:.0f}% on positional (need >80%)")
        print("HDC approach needs fundamental changes.")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = main()
