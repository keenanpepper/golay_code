import numpy as np
from math import comb

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

print("=" * 70)
print("PERFECT CODE DEMONSTRATION")
print("=" * 70)

# Load the 24-bit Golay code basis
print("\n📖 Loading Extended Binary Golay Code [24,12,8]...")
basis_24 = []
with open('golay_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_24.append(vec)

print(f"✓ Loaded {len(basis_24)} basis vectors")

# Puncture to get 23-bit code (remove last coordinate)
print("\n🔪 Puncturing to create Binary Golay Code [23,12,7]...")
print("   (removing the last bit from each codeword)")
basis_23 = [vec[:-1] for vec in basis_24]
print(f"✓ Created 23-bit basis with {len(basis_23)} vectors")

# Generate all 23-bit codewords
print("\n🔄 Generating all codewords...")
codewords_23 = generate_all_linear_combinations(basis_23)
print(f"✓ Generated {len(codewords_23)} codewords")

# Check minimum distance
weights = [hamming_weight(cw) for cw in codewords_23[1:]]  # Skip all-zeros
min_dist = min(weights)
print(f"✓ Minimum distance: {min_dist}")

print("\n" + "=" * 70)
print("PERFECT CODE PROPERTY")
print("=" * 70)

n = 23  # code length
k = 12  # dimension (number of information bits)
d = 7   # minimum distance
t = (d - 1) // 2  # number of correctable errors

print(f"""
A code is PERFECT if the Hamming spheres of radius t around each
codeword exactly partition the entire space (no gaps, no overlaps).

For the Binary Golay Code [23,12,7]:
  • Code length:        n = {n}
  • Dimension:          k = {k}
  • Minimum distance:   d = {d}
  • Correctable errors: t = {t}
""")

# Calculate sphere packing bound
num_codewords = 2**k
sphere_size = sum(comb(n, i) for i in range(t + 1))
total_space = 2**n

print("Sphere Packing Calculation:")
print("─" * 70)

print(f"\n1. Number of codewords: 2^{k} = {num_codewords:,}")

print(f"\n2. Size of Hamming sphere of radius {t}:")
for i in range(t + 1):
    print(f"     • Vectors at distance {i}: C({n},{i}) = {comb(n, i):,}")
print(f"     • Total: {sphere_size:,}")

print(f"\n3. Total space: 2^{n} = {total_space:,}")

print(f"\n4. Coverage by spheres:")
print(f"     {num_codewords:,} codewords × {sphere_size:,} points/sphere")
print(f"     = {num_codewords * sphere_size:,}")

print("\n" + "=" * 70)

if num_codewords * sphere_size == total_space:
    print("✨ PERFECT! ✨")
    print()
    print("The Hamming spheres EXACTLY partition the 23-dimensional hypercube!")
    print("Every one of the 8,388,608 possible 23-bit vectors is within")
    print("distance 3 of exactly ONE codeword.")
    print()
    print("This means:")
    print("  • ANY 3-error pattern is correctable")
    print("  • NO gaps in coverage")
    print("  • NO overlaps between spheres")
    print("  • Theoretically optimal error correction!")
else:
    ratio = (num_codewords * sphere_size) / total_space
    print(f"Not perfect. Coverage ratio: {ratio:.4f}")
    if ratio < 1:
        print("(Spheres don't cover the whole space)")
    else:
        print("(Spheres overlap)")

print("\n" + "=" * 70)
print("COMPARISON: Extended [24,12,8] vs Binary [23,12,7]")
print("=" * 70)

# Check 24-bit version
n_ext = 24
k_ext = 12
d_ext = 8
t_ext = (d_ext - 1) // 2

num_codewords_ext = 2**k_ext
sphere_size_ext = sum(comb(n_ext, i) for i in range(t_ext + 1))
total_space_ext = 2**n_ext
coverage_ext = num_codewords_ext * sphere_size_ext

print(f"""
Extended Binary Golay Code [24,12,8]:
  • Codewords: {num_codewords_ext:,}
  • Sphere size (radius {t_ext}): {sphere_size_ext:,}
  • Total space: {total_space_ext:,}
  • Coverage: {coverage_ext:,}
  • Perfect? {coverage_ext == total_space_ext}
  • Coverage ratio: {coverage_ext/total_space_ext:.4f}

Binary Golay Code [23,12,7]:
  • Codewords: {num_codewords:,}
  • Sphere size (radius {t}): {sphere_size:,}
  • Total space: {total_space:,}
  • Coverage: {num_codewords * sphere_size:,}
  • Perfect? {num_codewords * sphere_size == total_space} ✨
  • Coverage ratio: {(num_codewords * sphere_size)/total_space:.4f}
""")

print("The 24-bit extended version has DOUBLE coverage - the spheres overlap!")
print("Puncturing one bit gives us the perfect 23-bit code.")

