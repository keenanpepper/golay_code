import numpy as np
from itertools import combinations
import time

def hamming_weight(v):
    """Calculate Hamming weight (number of 1s) of a binary vector."""
    return np.sum(v)

def generate_all_linear_combinations(basis_vectors):
    """Generate all 2^k linear combinations of k basis vectors."""
    if len(basis_vectors) == 0:
        return [np.zeros(24, dtype=int)]
    
    k = len(basis_vectors)
    n = len(basis_vectors[0])
    codewords = []
    
    # Try all 2^k possible combinations
    for i in range(2**k):
        codeword = np.zeros(n, dtype=int)
        for j in range(k):
            if (i >> j) & 1:
                codeword ^= basis_vectors[j]
        codewords.append(codeword)
    
    return codewords

def check_min_distance_with_existing(candidate, existing_codewords, target_dist=8):
    """Check if candidate has at least target_dist distance from all existing codewords."""
    for cw in existing_codewords:
        dist = hamming_weight(candidate ^ cw)
        if dist < target_dist:
            return False
    return True

# GREEDY CONSTRUCTION
print("=" * 70, flush=True)
print("GREEDY GOLAY CODE CONSTRUCTION", flush=True)
print("=" * 70, flush=True)

n = 24  # codeword length
target_min_dist = 8
target_basis_size = 12
basis = []

# Start with the all-zeros vector (implicit - always there)
print("\n✓ Starting with all-zeros vector (always in a linear code)", flush=True)

# Add all-ones vector (known to be in extended Golay code)
all_ones = np.ones(n, dtype=int)
basis.append(all_ones)
print(f"✓ Added all-ones vector: weight = {hamming_weight(all_ones)}", flush=True)

print(f"\nCurrent basis size: {len(basis)}", flush=True)
print(f"Current codebook size: {2**len(basis)} codewords", flush=True)

# Keep searching for basis vectors until we have 12
while len(basis) < target_basis_size:
    print("\n" + "=" * 70, flush=True)
    print(f"SEARCHING for basis vector #{len(basis) + 1}...", flush=True)
    print("=" * 70, flush=True)
    
    found = False
    attempts = 0
    max_attempts = 500000
    start_time = time.time()
    
    # Try different weights in order: 8, 12, 16, etc.
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
            
            # Generate all current codewords
            current_codewords = generate_all_linear_combinations(basis)
            
            # Check if this candidate maintains min distance 8
            if check_min_distance_with_existing(candidate, current_codewords, target_min_dist):
                basis.append(candidate)
                elapsed = time.time() - start_time
                print(f"\n✓ FOUND basis vector #{len(basis)}!", flush=True)
                print(f"  Positions with 1s: {positions[:10]}{'...' if len(positions) > 10 else ''}", flush=True)
                print(f"  Weight: {hamming_weight(candidate)}", flush=True)
                print(f"  Search time: {elapsed:.2f}s", flush=True)
                found = True
                break
            
            if attempts >= max_attempts:
                break
        
        if attempts >= max_attempts:
            break
    
    if found:
        print(f"\n✓ Current basis size: {len(basis)}")
        print(f"✓ Current codebook size: {2**len(basis)} codewords")
    else:
        print(f"\n✗ Didn't find suitable vector in {attempts} attempts")
        print("Need to rethink strategy...")
        break

print("\n" + "=" * 70)
print("FINAL STATUS")
print("=" * 70)
print(f"Basis size: {len(basis)}/{target_basis_size}")
print(f"Codebook size: {2**len(basis)}/{2**target_basis_size}")

if len(basis) == target_basis_size:
    print("\n🎉 SUCCESS! We found all 12 basis vectors!")
else:
    print(f"\n⚠️  Only found {len(basis)} basis vectors so far.")
    print("Let's analyze what we have and see what's needed...")
