import numpy as np
from itertools import combinations

def hamming_distance(v1, v2):
    """Calculate Hamming distance between two binary vectors."""
    return np.sum(v1 != v2)

def hamming_weight(v):
    """Calculate Hamming weight (number of 1s) of a binary vector."""
    return np.sum(v)

def generate_all_codewords(generator_matrix):
    """Generate all 2^k codewords from a k×n generator matrix."""
    k, n = generator_matrix.shape
    codewords = []
    
    # Try all 2^k possible data vectors
    for i in range(2**k):
        # Convert i to binary vector
        data = np.array([(i >> j) & 1 for j in range(k)], dtype=int)
        # Encode: codeword = data @ G (mod 2)
        codeword = (data @ generator_matrix) % 2
        codewords.append(codeword)
    
    return np.array(codewords)

def check_minimum_distance(generator_matrix):
    """Find the minimum Hamming distance of the code."""
    codewords = generate_all_codewords(generator_matrix)
    min_dist = float('inf')
    
    # Check all pairs (but we can skip the all-zeros codeword)
    # Actually, for linear codes, min distance = min weight of non-zero codewords
    for cw in codewords[1:]:  # Skip all-zeros
        weight = hamming_weight(cw)
        if weight < min_dist:
            min_dist = weight
    
    return min_dist

# Let's start with a simple systematic generator matrix [I | P]
# where I is 12×12 identity and P is 12×12 parity matrix

def create_generator_matrix(parity_matrix):
    """Create systematic generator matrix [I | P]."""
    k = parity_matrix.shape[0]
    identity = np.eye(k, dtype=int)
    return np.hstack([identity, parity_matrix])

# EXPERIMENT 1: Let's try the simplest thing - all 1s for parity
print("=" * 60)
print("EXPERIMENT 1: Parity matrix = all 1s")
print("=" * 60)

P_simple = np.ones((12, 12), dtype=int)
G_simple = create_generator_matrix(P_simple)

print("\nGenerator matrix shape:", G_simple.shape)
print("\nFirst few rows of G:")
print(G_simple[:3])

min_d = check_minimum_distance(G_simple)
print(f"\nMinimum distance: {min_d}")
print(f"Target: 8")
print(f"Result: {'✓ Success!' if min_d == 8 else '✗ Need to try something else'}")

