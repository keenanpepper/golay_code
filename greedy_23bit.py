import numpy as np
from itertools import combinations
import time

def hamming_weight(v):
    return np.sum(v)

def generate_all_linear_combinations(basis_vectors):
    if len(basis_vectors) == 0:
        return [np.zeros(23, dtype=int)]
    
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

def check_min_distance_with_existing(candidate, existing_codewords, target_dist=7):
    for cw in existing_codewords:
        dist = hamming_weight(candidate ^ cw)
        if dist < target_dist:
            return False
    return True

print("=" * 70, flush=True)
print("GREEDY CONSTRUCTION OF [23,12,7] PERFECT GOLAY CODE", flush=True)
print("=" * 70, flush=True)

n = 23
target_min_dist = 7
target_basis_size = 12
basis = []

print("\n✓ Starting with all-zeros vector (implicit)", flush=True)

# For a 23-bit code, let's NOT start with all-ones
# (since 23 is odd, all-ones might not be in a d=7 code)
# Let's start with a simple weight-7 vector

first_vector = np.zeros(n, dtype=int)
first_vector[:7] = 1
basis.append(first_vector)
print(f"✓ Added first basis vector: weight = {hamming_weight(first_vector)}", flush=True)

print(f"\nCurrent basis size: {len(basis)}", flush=True)
print(f"Current codebook size: {2**len(basis)} codewords", flush=True)

# Keep searching
while len(basis) < target_basis_size:
    print("\n" + "=" * 70, flush=True)
    print(f"SEARCHING for basis vector #{len(basis) + 1}...", flush=True)
    print("=" * 70, flush=True)
    
    found = False
    attempts = 0
    max_attempts = 500000
    start_time = time.time()
    
    for weight in [7, 11, 15, 19]:  # Odd weights for 23-bit code
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
            
            current_codewords = generate_all_linear_combinations(basis)
            
            if check_min_distance_with_existing(candidate, current_codewords, target_min_dist):
                basis.append(candidate)
                elapsed = time.time() - start_time
                print(f"\n✓ FOUND basis vector #{len(basis)}!", flush=True)
                print(f"  Weight: {hamming_weight(candidate)}", flush=True)
                print(f"  Search time: {elapsed:.2f}s", flush=True)
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
    
    # Save the basis
    print("\nSaving basis to golay_23bit_basis.txt...", flush=True)
    with open('golay_23bit_basis.txt', 'w') as f:
        f.write("# Binary Golay Code [23,12,7] - Perfect Code\n")
        f.write("# Each row is a basis vector\n\n")
        for vec in basis:
            f.write(' '.join(map(str, vec)) + '\n')
    print("✓ Saved!", flush=True)

