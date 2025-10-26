import numpy as np
from itertools import permutations
import time

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
    
    return np.array(codewords, dtype=int)

def apply_permutation(codewords, perm):
    """Apply coordinate permutation to all codewords."""
    return codewords[:, perm]

def codewords_to_set(codewords):
    """Convert array of codewords to set of tuples."""
    return set(tuple(cw) for cw in codewords)

print("=" * 70)
print("FINDING PERMUTATION BETWEEN TWO GOLAY CODES")
print("=" * 70)

# Load both codes
print("\n📖 Loading codes...")
basis_1 = []
with open('golay_perfect_23_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_1.append(vec)

basis_2 = []
with open('golay_23bit_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_2.append(vec)

print(f"✓ Loaded both codes")

# Generate codewords
print("\n🔄 Generating codewords...")
codewords_1 = generate_all_linear_combinations(basis_1)
codewords_2 = generate_all_linear_combinations(basis_2)
print(f"✓ Code 1: {len(codewords_1)} codewords")
print(f"✓ Code 2: {len(codewords_2)} codewords")

# Convert to sets for fast lookup
codeset_2 = codewords_to_set(codewords_2)

print("\n" + "=" * 70)
print("STRATEGY: Use weight-7 codewords as anchors")
print("=" * 70)

# Find minimum weight codewords (these are most constrained)
min_weight_1 = [cw for cw in codewords_1 if hamming_weight(cw) == 7]
min_weight_2 = [cw for cw in codewords_2 if hamming_weight(cw) == 7]

print(f"\n✓ Code 1 has {len(min_weight_1)} weight-7 codewords")
print(f"✓ Code 2 has {len(min_weight_2)} weight-7 codewords")

print("""
Strategy: Pick a weight-7 codeword from Code 1 and try to map it to
each weight-7 codeword in Code 2. This constrains the permutation
significantly since we need to map 1-bits to 1-bits (7 out of 23).
""")

# Pick the first weight-7 codeword from Code 1
anchor_1 = min_weight_1[0]
positions_1 = np.where(anchor_1 == 1)[0]
print(f"\nAnchor from Code 1: positions {list(positions_1)}")

print("\nTrying to match with weight-7 codewords from Code 2...")
print("(This will take a moment...)")

found_permutation = None
attempts = 0
start_time = time.time()

# For each weight-7 codeword in Code 2
for candidate_2 in min_weight_2[:50]:  # Try first 50 to keep it reasonable
    positions_2 = np.where(candidate_2 == 1)[0]
    
    # Try all possible mappings of the 7 one-positions
    for perm_7 in permutations(positions_2):
        attempts += 1
        if attempts % 10000 == 0:
            print(f"  Tried {attempts} permutations...")
        
        # Build a candidate permutation
        # Map positions_1[i] -> perm_7[i] for the 7 ones
        # For the 16 zeros, try all possible mappings to remaining positions
        
        zero_positions_1 = np.where(anchor_1 == 0)[0]
        zero_positions_2 = np.array([i for i in range(23) if i not in perm_7])
        
        # Try just one mapping of zeros (there are too many to try all!)
        # Use identity mapping for zero positions as a heuristic
        perm = np.zeros(23, dtype=int)
        for i, p in enumerate(perm_7):
            perm[positions_1[i]] = p
        for i, zp in enumerate(zero_positions_2):
            if i < len(zero_positions_1):
                perm[zero_positions_1[i]] = zp
        
        # Check if this permutation maps Code 1 to Code 2
        permuted_1 = apply_permutation(codewords_1, perm)
        permuted_set = codewords_to_set(permuted_1)
        
        if permuted_set == codeset_2:
            found_permutation = perm
            print(f"\n✨ FOUND PERMUTATION after {attempts} attempts!")
            break
    
    if found_permutation is not None:
        break
    
    if attempts > 100000:
        print("\n⏱️ Taking too long, trying simpler approach...")
        break

elapsed = time.time() - start_time

if found_permutation is not None:
    print(f"✓ Search completed in {elapsed:.2f}s")
    print(f"\nPermutation: {list(found_permutation)}")
    print("\nThis means: position i in Code 1 → position perm[i] in Code 2")
    
    # Verify
    print("\n🔍 Verifying permutation works for all codewords...")
    permuted_1 = apply_permutation(codewords_1, found_permutation)
    permuted_set = codewords_to_set(permuted_1)
    
    if permuted_set == codeset_2:
        print("✅ VERIFIED! The permutation correctly maps Code 1 to Code 2!")
    else:
        print("❌ Verification failed (this shouldn't happen)")
else:
    print(f"\n⏱️ Didn't find permutation in {elapsed:.2f}s with simple search.")
    print("\nThis is a hard computational problem (testing 23! ≈ 2.5×10^22 permutations).")
    print("But we KNOW such a permutation exists because both are the Golay code.")
    print("\nWe could use more sophisticated algorithms (automorphism groups, etc.)")
    print("or verify equivalence through other properties.")

