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

def codewords_to_set(codewords):
    """Convert list of codewords to set of tuples for comparison."""
    return set(tuple(cw) for cw in codewords)

print("=" * 70)
print("COMPARING TWO 23-BIT GOLAY CODES")
print("=" * 70)

# Load Code 1: from puncturing self-dual [24,12,8]
print("\n📖 Loading Code 1: Punctured from self-dual [24,12,8]...")
basis_1 = []
with open('golay_perfect_23_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_1.append(vec)

print(f"✓ Loaded {len(basis_1)} basis vectors")

# Load Code 2: from direct greedy search
print("\n📖 Loading Code 2: Direct greedy search for [23,12,7]...")
basis_2 = []
with open('golay_23bit_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_2.append(vec)

print(f"✓ Loaded {len(basis_2)} basis vectors")

# Generate all codewords for both
print("\n🔄 Generating all codewords...")
codewords_1 = generate_all_linear_combinations(basis_1)
codewords_2 = generate_all_linear_combinations(basis_2)

print(f"✓ Code 1: {len(codewords_1)} codewords")
print(f"✓ Code 2: {len(codewords_2)} codewords")

# Check minimum distances
print("\n📊 Computing statistics...")
weights_1 = [hamming_weight(cw) for cw in codewords_1]
weights_2 = [hamming_weight(cw) for cw in codewords_2]

min_dist_1 = min(w for w in weights_1 if w > 0)
min_dist_2 = min(w for w in weights_2 if w > 0)

weight_dist_1 = Counter(weights_1)
weight_dist_2 = Counter(weights_2)

print(f"\nCode 1 minimum distance: {min_dist_1}")
print(f"Code 2 minimum distance: {min_dist_2}")

print("\nCode 1 weight distribution:")
for w in sorted(weight_dist_1.keys()):
    print(f"  Weight {w:2d}: {weight_dist_1[w]:4d} codewords")

print("\nCode 2 weight distribution:")
for w in sorted(weight_dist_2.keys()):
    print(f"  Weight {w:2d}: {weight_dist_2[w]:4d} codewords")

print("\n" + "=" * 70)
print("EQUIVALENCE CHECK")
print("=" * 70)

# Convert to sets for comparison
codeset_1 = codewords_to_set(codewords_1)
codeset_2 = codewords_to_set(codewords_2)

# Check if identical (same codewords)
if codeset_1 == codeset_2:
    print("\n✨ IDENTICAL! ✨")
    print("The two codes have exactly the same set of codewords!")
    print("They are the SAME code (possibly with different basis).")
else:
    print("\n🔍 Not identical as sets. Checking for permutation equivalence...")
    
    # Check if they differ only by coordinate permutation
    # This is a harder problem - for now just check size and weight distribution
    
    if len(codeset_1) == len(codeset_2):
        print(f"✓ Same number of codewords: {len(codeset_1)}")
    else:
        print(f"✗ Different number of codewords: {len(codeset_1)} vs {len(codeset_2)}")
    
    if weight_dist_1 == weight_dist_2:
        print("✓ Same weight distribution")
        print("\nThe codes are DIFFERENT but have the same parameters.")
        print("They might be equivalent up to coordinate permutation.")
        
        # Check: how many codewords are in common?
        common = codeset_1 & codeset_2
        only_1 = codeset_1 - codeset_2
        only_2 = codeset_2 - codeset_1
        
        print(f"\nCodewords in common: {len(common)}")
        print(f"Only in Code 1: {len(only_1)}")
        print(f"Only in Code 2: {len(only_2)}")
        
        if len(common) > 0:
            print("\nThey share some codewords but not all.")
    else:
        print("✗ Different weight distributions")
        print("These are fundamentally different codes!")

# Additional check: compare basis vectors directly
print("\n" + "=" * 70)
print("BASIS COMPARISON")
print("=" * 70)

print("\nAre the basis vectors identical?")
if len(basis_1) == len(basis_2):
    basis_identical = True
    for i, (b1, b2) in enumerate(zip(basis_1, basis_2)):
        if not np.array_equal(b1, b2):
            basis_identical = False
            print(f"  Basis vector {i}: DIFFERENT")
            print(f"    Code 1: {b1[:10]}...")
            print(f"    Code 2: {b2[:10]}...")
    
    if basis_identical:
        print("✓ All basis vectors are identical!")
    else:
        print("\nBasis vectors are different (but might span the same code).")
else:
    print(f"Different number of basis vectors: {len(basis_1)} vs {len(basis_2)}")

