import numpy as np
from itertools import combinations
import time

def hamming_weight(v):
    return np.sum(v)

def binary_dot_product(v1, v2):
    """Binary dot product mod 2."""
    return np.sum(v1 * v2) % 2

def generate_all_linear_combinations(basis_vectors):
    if len(basis_vectors) == 0:
        return [np.zeros(24, dtype=int)]
    
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

def check_min_distance_with_existing(candidate, existing_codewords, target_dist=8):
    for cw in existing_codewords:
        dist = hamming_weight(candidate ^ cw)
        if dist < target_dist:
            return False
    return True

def check_orthogonal_to_all(candidate, existing_basis):
    """Check if candidate is orthogonal to all existing basis vectors."""
    # First check if orthogonal to itself (i.e., has even weight)
    if binary_dot_product(candidate, candidate) != 0:
        return False
    
    # Then check orthogonality with all existing basis vectors
    for basis_vec in existing_basis:
        if binary_dot_product(candidate, basis_vec) != 0:
            return False
    
    return True

print("=" * 70, flush=True)
print("GREEDY CONSTRUCTION OF SELF-DUAL [24,12,8] CODE", flush=True)
print("=" * 70, flush=True)

n = 24
target_min_dist = 8
target_basis_size = 12
basis = []

print("\n✓ Starting with all-zeros vector (implicit)", flush=True)

# Start with all-ones vector (weight 24, orthogonal to itself)
all_ones = np.ones(n, dtype=int)
basis.append(all_ones)
print(f"✓ Added all-ones vector: weight = {hamming_weight(all_ones)}", flush=True)
print(f"  Self-orthogonal? {binary_dot_product(all_ones, all_ones) == 0}", flush=True)

print(f"\nCurrent basis size: {len(basis)}", flush=True)
print(f"Current codebook size: {2**len(basis)} codewords", flush=True)

# Keep searching with BOTH constraints
while len(basis) < target_basis_size:
    print("\n" + "=" * 70, flush=True)
    print(f"SEARCHING for basis vector #{len(basis) + 1}...", flush=True)
    print("=" * 70, flush=True)
    
    found = False
    attempts = 0
    max_attempts = 500000
    start_time = time.time()
    
    # Try only even weights (required for self-orthogonality)
    for weight in [8, 12, 16, 20]:
        if found:
            break
            
        print(f"Trying weight-{weight} vectors...", flush=True)
        
        for positions in combinations(range(n), weight):
            attempts += 1
            if attempts % 50000 == 0:
                elapsed = time.time() - start_time
                print(f"  Tried {attempts} combinations so far... ({elapsed:.1f}s elapsed)", flush=True)
            
            candidate = np.zeros(n, dtype=int)
            candidate[list(positions)] = 1
            
            # NEW: Check orthogonality constraint FIRST (faster to check)
            if not check_orthogonal_to_all(candidate, basis):
                continue
            
            # Then check distance constraint
            current_codewords = generate_all_linear_combinations(basis)
            
            if check_min_distance_with_existing(candidate, current_codewords, target_min_dist):
                basis.append(candidate)
                elapsed = time.time() - start_time
                print(f"\n✓ FOUND basis vector #{len(basis)}!", flush=True)
                print(f"  Positions with 1s: {positions[:10]}{'...' if len(positions) > 10 else ''}", flush=True)
                print(f"  Weight: {hamming_weight(candidate)}", flush=True)
                print(f"  Search time: {elapsed:.2f}s", flush=True)
                
                # Verify orthogonality
                print(f"  ✓ Orthogonal to all previous basis vectors", flush=True)
                
                found = True
                break
            
            if attempts >= max_attempts:
                break
        
        if attempts >= max_attempts:
            break
    
    if found:
        print(f"\n✓ Current basis size: {len(basis)}", flush=True)
        print(f"✓ Current codebook size: {2**len(basis)} codewords", flush=True)
    else:
        print(f"\n✗ Didn't find suitable vector in {attempts} attempts", flush=True)
        break

print("\n" + "=" * 70, flush=True)
print("FINAL STATUS", flush=True)
print("=" * 70, flush=True)
print(f"Basis size: {len(basis)}/{target_basis_size}", flush=True)

if len(basis) == target_basis_size:
    print("\n🎉 Found all 12 basis vectors!", flush=True)
    
    # Verify self-duality
    print("\nVerifying self-duality...", flush=True)
    G = np.array(basis, dtype=int)
    product = (G @ G.T) % 2
    is_self_dual = np.all(product == 0)
    
    if is_self_dual:
        print("✨ CONFIRMED: The code IS self-dual!", flush=True)
    else:
        print("⚠️  WARNING: Self-duality check failed!", flush=True)
    
    # Save the basis
    print("\nSaving basis to golay_self_dual_basis.txt...", flush=True)
    with open('golay_self_dual_basis.txt', 'w') as f:
        f.write("# Self-Dual Extended Binary Golay Code [24,12,8]\n")
        f.write("# Each row is a basis vector\n\n")
        for vec in basis:
            f.write(' '.join(map(str, vec)) + '\n')
    print("✓ Saved!", flush=True)
else:
    print(f"\n⚠️  Only found {len(basis)} basis vectors so far.", flush=True)

