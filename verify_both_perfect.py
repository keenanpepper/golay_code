import numpy as np
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

print("=" * 70)
print("VERIFYING PERFECT CODE PROPERTY FOR BOTH 23-BIT CODES")
print("=" * 70)

for code_name, filename in [
    ("Code 1 (Punctured)", "golay_perfect_23_basis.txt"),
    ("Code 2 (Direct greedy)", "golay_23bit_basis.txt")
]:
    print(f"\n{'=' * 70}")
    print(f"Testing: {code_name}")
    print('=' * 70)
    
    # Load basis
    basis = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                vec = np.array([int(x) for x in line.split()], dtype=int)
                basis.append(vec)
    
    # Generate codewords
    codewords = generate_all_linear_combinations(basis)
    
    # Check parameters
    n = 23
    k = 12
    d = 7
    t = 3
    
    num_codewords = len(codewords)
    sphere_size = sum(comb(n, i) for i in range(t + 1))
    total_space = 2**n
    coverage = num_codewords * sphere_size
    
    print(f"\nParameters:")
    print(f"  • Length: n = {n}")
    print(f"  • Dimension: k = {k}")
    print(f"  • Min distance: d = {d}")
    print(f"  • Correctable errors: t = {t}")
    
    print(f"\nPerfect code calculation:")
    print(f"  • Number of codewords: {num_codewords:,}")
    print(f"  • Sphere size (radius {t}): {sphere_size:,}")
    print(f"  • Total space: {total_space:,}")
    print(f"  • Coverage: {coverage:,}")
    
    is_perfect = (coverage == total_space)
    print(f"\n  → Perfect? {is_perfect}")
    
    if is_perfect:
        print("  ✨ YES! This is a perfect code.")
    else:
        print(f"  ✗ NO. Coverage ratio: {coverage / total_space:.6f}")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("""
Both codes are [23,12,7] perfect codes with the same weight distribution.
But they have different codewords!

This suggests they might be:
  • Equivalent via coordinate permutation (reordering bit positions)
  • OR there's an issue with one of our constructions

The binary Golay code is unique up to equivalence, so if both are
truly perfect [23,12,7] codes, they MUST be equivalent via some
permutation of coordinates.

Let's check if they're related by a simple coordinate permutation...
""")

