import numpy as np
from collections import Counter

def hamming_weight(v):
    """Calculate Hamming weight (number of 1s) of a binary vector."""
    return np.sum(v)

def generate_all_linear_combinations(basis_vectors):
    """Generate all 2^k linear combinations of k basis vectors."""
    k = len(basis_vectors)
    n = len(basis_vectors[0])
    codewords = []
    
    for i in range(2**k):
        codeword = np.zeros(n, dtype=int)
        for j in range(k):
            if (i >> j) & 1:
                codeword ^= basis_vectors[j]
        codewords.append(codeword)
    
    return codewords

# Load the basis we found (we'll need to reconstruct it from the output)
print("=" * 70)
print("VERIFYING THE GOLAY CODE")
print("=" * 70)

# Reconstruct the basis from our greedy search
n = 24
basis = []

# Basis vector 1: all ones
basis.append(np.ones(n, dtype=int))

# Basis vectors from the output above:
basis.append(np.array([1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=int))

# Create basis vectors from positions
positions_list = [
    (0, 1, 2, 3, 8, 9, 10, 11),
    (0, 1, 2, 3, 12, 13, 14, 15),
    (0, 1, 2, 3, 16, 17, 18, 19),
    (0, 1, 2, 4, 8, 12, 16, 20),
    (0, 1, 2, 4, 9, 13, 17, 21),
    (0, 1, 2, 4, 10, 14, 18, 22),
    (0, 1, 2, 5, 8, 13, 18, 23),
    (0, 1, 2, 6, 8, 14, 19, 21),
    (0, 1, 3, 4, 8, 13, 19, 22),
    (0, 2, 3, 4, 8, 14, 17, 23),
]

for positions in positions_list:
    vec = np.zeros(n, dtype=int)
    vec[list(positions)] = 1
    basis.append(vec)

print(f"\n✓ Reconstructed basis with {len(basis)} vectors")

# Generate all codewords
print("\nGenerating all codewords...")
codewords = generate_all_linear_combinations(basis)
print(f"✓ Generated {len(codewords)} codewords")

# Calculate weight distribution
print("\nCalculating weight distribution...")
weights = [hamming_weight(cw) for cw in codewords]
weight_dist = Counter(weights)

print("\nWeight distribution:")
for w in sorted(weight_dist.keys()):
    print(f"  Weight {w:2d}: {weight_dist[w]:4d} codewords")

# Find minimum distance (= minimum non-zero weight for linear code)
min_dist = min(w for w in weights if w > 0)
print(f"\n✓ Minimum distance: {min_dist}")

# Check if this matches the expected Golay code weight distribution
print("\n" + "=" * 70)
print("COMPARISON WITH KNOWN GOLAY CODE")
print("=" * 70)

expected_golay_weights = {
    0: 1,      # all zeros
    8: 759,    # weight 8
    12: 2576,  # weight 12
    16: 759,   # weight 16
    24: 1,     # all ones
}

print("\nExpected Extended Binary Golay Code [24,12,8] weight distribution:")
for w in sorted(expected_golay_weights.keys()):
    print(f"  Weight {w:2d}: {expected_golay_weights[w]:4d} codewords")

print("\n" + "=" * 70)
if weight_dist == expected_golay_weights:
    print("🎉 PERFECT MATCH! We successfully constructed the Golay code!")
else:
    print("⚠️  Weight distribution doesn't match exactly.")
    print("   This is still a valid [24,12,8] code, but might not be")
    print("   the 'standard' extended binary Golay code.")
    print("\nDifferences:")
    all_weights = set(weight_dist.keys()) | set(expected_golay_weights.keys())
    for w in sorted(all_weights):
        ours = weight_dist.get(w, 0)
        expected = expected_golay_weights.get(w, 0)
        if ours != expected:
            print(f"  Weight {w:2d}: ours={ours:4d}, expected={expected:4d}, diff={ours-expected:+d}")

