import numpy as np
from collections import Counter
from math import comb

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

print("=" * 70)
print("TRYING SHORTENING vs PUNCTURING")
print("=" * 70)

# Generate all 24-bit codewords
codewords_24 = generate_all_linear_combinations(basis_24)
print(f"\n✓ Generated {len(codewords_24)} codewords for [24,12,8] code")

# Try shortening at position 0
print("\nShortening at position 0:")
print("  (keep only codewords with 0 in position 0, then remove that position)")

shortened_codewords = []
for cw in codewords_24:
    if cw[0] == 0:  # Keep only if position 0 is 0
        shortened_codewords.append(cw[1:])  # Remove position 0

print(f"  • Result: {len(shortened_codewords)} codewords")

if len(shortened_codewords) > 0:
    # Find minimum distance
    min_dist = float('inf')
    for cw in shortened_codewords:
        w = hamming_weight(cw)
        if w > 0 and w < min_dist:
            min_dist = w
    
    print(f"  • Minimum distance: {min_dist}")
    print(f"  • Code parameters: [{len(shortened_codewords[0])}, {int(np.log2(len(shortened_codewords)))}, {min_dist}]")
    
    # Check if perfect
    n = len(shortened_codewords[0])
    k = int(np.log2(len(shortened_codewords)))
    t = (min_dist - 1) // 2
    sphere_size = sum(comb(n, i) for i in range(t + 1))
    coverage = len(shortened_codewords) * sphere_size
    total_space = 2**n
    
    print(f"\n  Perfect code check:")
    print(f"    Spheres of radius {t}: {len(shortened_codewords)} × {sphere_size} = {coverage}")
    print(f"    Total space: {total_space}")
    print(f"    Perfect? {coverage == total_space}")

print("\n" + "=" * 70)
print("INSIGHT: Shortening vs Puncturing")
print("=" * 70)
print("""
Shortening: Remove codewords with 1 in position i, then remove position i
  • Reduces both n and k by 1
  • From [24,12,8] → [23,11,8]
  
Puncturing: Remove position i from all codewords
  • Reduces n by 1, keeps k the same
  • From [24,12,8] → [23,12,≥7]

For the perfect [23,12,7] Golay code, we need puncturing!
But it seems our [24,12,8] code doesn't puncture to give d=7.

Let me check: maybe the "true" extended Golay code has a special
structure we didn't capture with our greedy search?
""")

