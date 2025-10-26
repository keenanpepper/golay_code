import numpy as np

print("=" * 70)
print("CHECKING IF OUR [24,12,8] CODE IS SELF-DUAL")
print("=" * 70)

# Load the 24-bit basis
basis_24 = []
with open('golay_basis.txt', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            vec = np.array([int(x) for x in line.split()], dtype=int)
            basis_24.append(vec)

print(f"\n✓ Loaded {len(basis_24)} basis vectors")

# Create generator matrix G (12 x 24)
G = np.array(basis_24, dtype=int)
print(f"✓ Generator matrix G shape: {G.shape}")

print("\n" + "=" * 70)
print("Self-Dual Test: G @ G^T = 0 (mod 2)?")
print("=" * 70)

# Compute G @ G^T mod 2
GT = G.T
product = (G @ GT) % 2

print("\nG @ G^T (mod 2):")
print(product)

# Check if it's all zeros
is_self_dual = np.all(product == 0)

print("\n" + "=" * 70)
if is_self_dual:
    print("✨ YES! The code IS self-dual! ✨")
    print("\nThis means:")
    print("  • Every basis vector is orthogonal to every other basis vector")
    print("  • The code equals its own dual code: C = C⊥")
    print("  • This is a special property of the extended Golay code!")
else:
    print("✗ NO - The code is NOT self-dual")
    print("\nNon-zero entries in G @ G^T:")
    non_zero = np.argwhere(product != 0)
    for i, j in non_zero:
        print(f"  Row {i} · Row {j} = {product[i,j]} (should be 0)")
    
    print("\nThis means our greedy-constructed code has the right weight")
    print("distribution but is NOT equivalent to the standard extended")
    print("Golay code (which is self-dual).")

print("\n" + "=" * 70)
print("DETAILED ANALYSIS")
print("=" * 70)

print("\nBinary dot products between basis vectors:")
print("(diagonal = self dot product, off-diagonal = pairwise)")
print()
print("    ", end="")
for j in range(12):
    print(f"{j:2d} ", end="")
print()

for i in range(12):
    print(f"{i:2d}: ", end="")
    for j in range(12):
        print(f"{product[i,j]:2d} ", end="")
    print()

print("\nInterpretation:")
print("  • Diagonal (i=j): 0 means vector has even weight ✓")
print("  • Off-diagonal (i≠j): 0 means vectors are orthogonal")

