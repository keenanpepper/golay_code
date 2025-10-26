import numpy as np
from collections import Counter

def hamming_weight(v):
    return np.sum(v)

def generate_all_linear_combinations(basis_vectors):
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

# Load 24-bit basis
basis_24 = []
with open('golay_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_24.append(vec)

print("Analyzing puncturing options...")
print("=" * 70)

# Try puncturing each position
for pos in range(24):
    basis_punctured = [vec[:pos].tolist() + vec[pos+1:].tolist() for vec in basis_24]
    basis_punctured = [np.array(v, dtype=int) for v in basis_punctured]
    
    codewords = generate_all_linear_combinations(basis_punctured)
    
    # Check for duplicates
    unique_codewords = []
    seen = set()
    for cw in codewords:
        cw_tuple = tuple(cw)
        if cw_tuple not in seen:
            seen.add(cw_tuple)
            unique_codewords.append(cw)
    
    # Find minimum distance
    weights = [hamming_weight(cw) for cw in unique_codewords[1:]]
    min_dist = min(weights) if weights else 0
    
    print(f"Position {pos:2d}: {len(unique_codewords):4d} unique codewords, min_dist = {min_dist}")

print("\n" + "=" * 70)
print("Issue: We need to puncture at a position where all 4096 codewords")
print("remain distinct and the minimum distance stays at 7.")
print("\nThe problem is that when puncturing the extended [24,12,8] code,")
print("we might get duplicate codewords if we pick the wrong position!")

