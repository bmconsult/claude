#!/usr/bin/env python3
"""
Neural Network Search for 5-Chromatic Unit-Distance Graphs

Idea: Learn vertex coordinates that create a unit-distance graph
that resists 4-coloring.

Key insight: Use differentiable Potts model relaxation to measure
"resistance to k-coloring"

Loss function:
1. Unit distance loss: edges should have length = 1
2. Non-edge loss: non-edges should have length ≠ 1
3. Chromatic loss: graph should resist k-coloring (maximize Potts energy)
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import defaultdict

class GraphCoordinateNet(nn.Module):
    """Neural network that outputs 2D coordinates for n vertices"""

    def __init__(self, n_vertices, hidden_dim=64):
        super().__init__()
        self.n_vertices = n_vertices

        # Simple MLP that maps vertex index embedding to 2D coordinates
        self.embedding = nn.Embedding(n_vertices, hidden_dim)
        self.fc1 = nn.Linear(hidden_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 2)

        # Initialize with random positions
        nn.init.uniform_(self.embedding.weight, -1, 1)

    def forward(self):
        """Return coordinates for all vertices"""
        indices = torch.arange(self.n_vertices)
        x = self.embedding(indices)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        coords = self.fc3(x)
        return coords  # Shape: (n_vertices, 2)


def compute_distances(coords):
    """Compute pairwise distance matrix"""
    # coords: (n, 2)
    n = coords.shape[0]
    # Expand for broadcasting
    diff = coords.unsqueeze(0) - coords.unsqueeze(1)  # (n, n, 2)
    dists = torch.norm(diff, dim=2)  # (n, n)
    return dists


def unit_distance_loss(dists, edge_mask, non_edge_mask, epsilon=0.01):
    """
    Loss for enforcing unit distances.

    edge_mask: 1 where we want unit distance
    non_edge_mask: 1 where we want NON-unit distance
    """
    # Edges should be exactly distance 1
    edge_loss = ((dists - 1.0) ** 2 * edge_mask).sum() / edge_mask.sum()

    # Non-edges should NOT be distance 1
    # Use soft penalty: high when close to 1, low otherwise
    dist_from_one = (dists - 1.0).abs()
    non_edge_penalty = torch.exp(-dist_from_one / epsilon) * non_edge_mask
    non_edge_loss = non_edge_penalty.sum() / non_edge_mask.sum()

    return edge_loss + 0.1 * non_edge_loss


def soft_potts_energy(dists, edge_threshold=0.1, k=4, temperature=0.1):
    """
    Differentiable approximation to "resistance to k-coloring".

    Uses soft assignment vectors (probability distributions over k colors)
    and measures how hard it is to avoid same-color edges.

    Higher energy = harder to color = more "chromatic"
    """
    n = dists.shape[0]

    # Soft adjacency: 1 if distance ≈ 1, 0 otherwise
    adj_soft = torch.exp(-(dists - 1.0) ** 2 / (2 * edge_threshold ** 2))
    adj_soft = adj_soft * (1 - torch.eye(n))  # Remove self-loops

    # Initialize random soft assignments (probability over k colors)
    # In practice, we'd optimize these, but for a quick estimate:
    color_probs = torch.softmax(torch.randn(n, k), dim=1)

    # Potts energy: sum over edges of probability of same color
    # E = Σ_{i,j} A_{ij} * Σ_c p_i(c) * p_j(c)
    same_color_prob = torch.einsum('nc,mc->nm', color_probs, color_probs)
    energy = (adj_soft * same_color_prob).sum() / 2  # Divide by 2 for undirected

    return energy


def optimal_coloring_energy(dists, edge_threshold=0.1, k=4, n_iter=100):
    """
    Find optimal soft coloring and return resulting Potts energy.

    Lower energy = easier to color
    Higher energy = harder to color
    """
    n = dists.shape[0]

    # Soft adjacency
    adj_soft = torch.exp(-(dists - 1.0) ** 2 / (2 * edge_threshold ** 2))
    adj_soft = adj_soft * (1 - torch.eye(n))

    # Learnable color logits
    color_logits = torch.nn.Parameter(torch.randn(n, k))
    optimizer = torch.optim.Adam([color_logits], lr=0.1)

    for _ in range(n_iter):
        color_probs = torch.softmax(color_logits, dim=1)
        same_color_prob = torch.einsum('nc,mc->nm', color_probs, color_probs)
        energy = (adj_soft * same_color_prob).sum() / 2

        optimizer.zero_grad()
        energy.backward()
        optimizer.step()

    # Final energy
    color_probs = torch.softmax(color_logits.detach(), dim=1)
    same_color_prob = torch.einsum('nc,mc->nm', color_probs, color_probs)
    final_energy = (adj_soft * same_color_prob).sum() / 2

    return final_energy.item()


def count_edges(dists, threshold=0.05):
    """Count edges (pairs at distance ~1)"""
    n = dists.shape[0]
    near_one = (dists - 1.0).abs() < threshold
    near_one = near_one * (1 - torch.eye(n).bool())
    return near_one.sum().item() // 2


def main():
    print("=" * 70)
    print("NEURAL SEARCH FOR 5-CHROMATIC UNIT-DISTANCE GRAPHS")
    print("=" * 70)

    # Start with small graph
    n_vertices = 50

    print(f"\nSearching for {n_vertices}-vertex unit-distance graph...")
    print("Goal: Maximize resistance to 4-coloring")

    # Define target edge structure (for now, use random sparse)
    # In a real implementation, we'd learn this too
    np.random.seed(42)
    edge_prob = 0.15
    edge_mask = torch.zeros(n_vertices, n_vertices)
    for i in range(n_vertices):
        for j in range(i+1, n_vertices):
            if np.random.random() < edge_prob:
                edge_mask[i, j] = 1
                edge_mask[j, i] = 1

    non_edge_mask = 1 - edge_mask - torch.eye(n_vertices)

    print(f"Target edge count: {edge_mask.sum().item() // 2}")

    # Create network
    net = GraphCoordinateNet(n_vertices, hidden_dim=32)
    optimizer = optim.Adam(net.parameters(), lr=0.01)

    # Training loop
    best_energy = 0
    best_coords = None

    print("\nTraining...")
    for epoch in range(500):
        coords = net()
        dists = compute_distances(coords)

        # Unit distance loss
        ud_loss = unit_distance_loss(dists, edge_mask, non_edge_mask)

        # Total loss (minimize unit distance violation)
        loss = ud_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch % 100 == 0:
            actual_edges = count_edges(dists.detach())
            energy = optimal_coloring_energy(dists.detach(), k=4)
            print(f"  Epoch {epoch}: loss={loss.item():.4f}, edges={actual_edges}, 4-color energy={energy:.4f}")

            if energy > best_energy:
                best_energy = energy
                best_coords = coords.detach().clone()

    # Final analysis
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    coords = best_coords
    dists = compute_distances(coords)
    actual_edges = count_edges(dists)

    print(f"\nBest graph found:")
    print(f"  Vertices: {n_vertices}")
    print(f"  Unit-distance edges: {actual_edges}")

    # Test coloring energies for k=3,4,5
    for k in [3, 4, 5]:
        energy = optimal_coloring_energy(dists, k=k)
        print(f"  {k}-coloring energy: {energy:.4f}")

    print("""
INTERPRETATION:
- Higher energy = harder to color with that many colors
- If 4-color energy >> 5-color energy, graph might be 5-chromatic
- This is a PROOF OF CONCEPT - real search would need:
  * Larger graphs
  * More sophisticated edge learning
  * Integration with SAT solver for verification
""")

if __name__ == "__main__":
    main()
