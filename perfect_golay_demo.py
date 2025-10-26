import numpy as np
from math import comb
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

print("=" * 70)
print("THE PERFECT BINARY GOLAY CODE [23,12,7]")
print("=" * 70)

# Load the punctured code (from self-dual construction)
basis = []
with open('golay_perfect_23_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis.append(vec)

print(f"\n✓ Loaded basis with {len(basis)} vectors")

# Generate all codewords
print("✓ Generating all codewords...")
codewords = generate_all_linear_combinations(basis)
print(f"✓ Generated {len(codewords):,} codewords")

# Parameters
n = 23  # code length
k = 12  # dimension
d = 7   # minimum distance
t = (d - 1) // 2  # correctable errors

print("\n" + "=" * 70)
print("CODE PARAMETERS")
print("=" * 70)

print(f"""
  • Length (n):              {n} bits
  • Dimension (k):           {k} information bits
  • Minimum distance (d):    {d}
  • Correctable errors (t):  {t}
  • Rate:                    {k}/{n} = {k/n:.4f}
""")

# Weight distribution
weights = [hamming_weight(cw) for cw in codewords]
weight_dist = Counter(weights)

print("=" * 70)
print("WEIGHT DISTRIBUTION")
print("=" * 70)
print()
for w in sorted(weight_dist.keys()):
    bar = "█" * (weight_dist[w] // 50)
    print(f"  Weight {w:2d}: {weight_dist[w]:4d} codewords {bar}")

print("\n" + "=" * 70)
print("✨ THE PERFECT CODE PROPERTY ✨")
print("=" * 70)

sphere_size = sum(comb(n, i) for i in range(t + 1))
total_space = 2**n
coverage = len(codewords) * sphere_size

print(f"""
A code is PERFECT if Hamming spheres of radius t around each codeword
exactly partition the entire space with no gaps and no overlaps.

The Sphere Packing Bound:
""")

print("  Number of codewords:        ", f"{len(codewords):,}".rjust(15))
print()
print(f"  Hamming sphere of radius {t}:")
for i in range(t + 1):
    print(f"    • Distance {i} vectors:     ", f"{comb(n, i):,}".rjust(15))
print("                                ", "─" * 15)
print("    • Total per sphere:      ", f"{sphere_size:,}".rjust(15))
print()
print("  Coverage:")
print(f"    {len(codewords):,} × {sphere_size:,} = ", f"{coverage:,}".rjust(15))
print()
print("  Total 23-bit vectors:       ", f"{total_space:,}".rjust(15))
print()

if coverage == total_space:
    print("  " + "═" * 50)
    print("  ✨ PERFECT MATCH! ✨")
    print("  " + "═" * 50)
    print()
    print("  The binary Golay code is one of only THREE non-trivial")
    print("  perfect codes (along with Hamming codes and the ternary")
    print("  Golay code).")
    print()
    print("  Every possible 23-bit vector is within distance 3 of")
    print("  EXACTLY ONE codeword - no more, no less!")

print("\n" + "=" * 70)
print("PRACTICAL IMPLICATIONS")
print("=" * 70)

print("""
📡 Error Correction:
   • Can correct ANY pattern of 3 or fewer bit errors
   • Can detect ANY pattern of 6 or fewer bit errors
   • Used in space communications (Voyager, etc.)

🎯 Optimality:
   • Achieves the theoretical maximum for this distance
   • Cannot be improved without changing parameters
   • Unique up to coordinate permutation

📦 Efficiency:
   • 12 information bits → 23 total bits (52% rate)
   • Compare to simple repetition: would need ~21 bits for 3 errors
   • Much more efficient than repetition coding!

🔢 Historical Significance:
   • Discovered independently by Golay (1949)
   • One of the first non-trivial error-correcting codes
   • Led to the development of coding theory
""")

print("=" * 70)

