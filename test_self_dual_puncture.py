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

print("=" * 70)
print("TESTING PUNCTURE OF SELF-DUAL [24,12,8] CODE")
print("=" * 70)

# Load the self-dual basis
basis_24 = []
with open('golay_self_dual_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_24.append(vec)

print(f"\n✓ Loaded self-dual basis with {len(basis_24)} vectors")

# Try puncturing at different positions
print("\n" + "=" * 70)
print("Trying all puncturing positions...")
print("=" * 70)

best_min_dist = 0
best_position = -1

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
    
    marker = ""
    if min_dist >= best_min_dist:
        best_min_dist = min_dist
        best_position = pos
        if min_dist == 7:
            marker = " ✨ PERFECT!"
    
    print(f"Position {pos:2d}: {len(unique_codewords):4d} unique codewords, min_dist = {min_dist}{marker}")

print("\n" + "=" * 70)
print(f"Best puncturing position: {best_position} (min_dist = {best_min_dist})")
print("=" * 70)

if best_min_dist == 7:
    print("\n🎉 SUCCESS! We can puncture to get [23,12,7]!")
    
    # Generate the perfect code
    basis_23 = [vec[:best_position].tolist() + vec[best_position+1:].tolist() for vec in basis_24]
    basis_23 = [np.array(v, dtype=int) for v in basis_23]
    
    codewords_23 = generate_all_linear_combinations(basis_23)
    
    # Perfect code check
    n = 23
    k = 12
    t = 3
    
    num_codewords = len(codewords_23)
    sphere_size = sum(comb(n, i) for i in range(t + 1))
    total_space = 2**n
    coverage = num_codewords * sphere_size
    
    print(f"\nPerfect Code Verification:")
    print(f"  • Codewords: {num_codewords:,}")
    print(f"  • Sphere size (radius {t}): {sphere_size:,}")
    print(f"  • Total space: {total_space:,}")
    print(f"  • Coverage: {coverage:,}")
    print(f"  • Perfect? {coverage == total_space}")
    
    if coverage == total_space:
        print("\n✨✨✨ PERFECT CODE ACHIEVED! ✨✨✨")
        print("The self-dual [24,12,8] punctures to the perfect [23,12,7]!")
        
        # Save the 23-bit basis
        print("\nSaving to golay_perfect_23_basis.txt...")
        with open('golay_perfect_23_basis.txt', 'w') as f:
            f.write("# Perfect Binary Golay Code [23,12,7]\n")
            f.write(f"# Obtained by puncturing position {best_position} of self-dual [24,12,8]\n\n")
            for vec in basis_23:
                f.write(' '.join(map(str, vec)) + '\n')
        print("✓ Saved!")
else:
    print(f"\n⚠️  Best minimum distance is only {best_min_dist}, not 7")
    print("This shouldn't happen with the true self-dual extended Golay code...")

