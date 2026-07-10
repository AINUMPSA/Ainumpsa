import numpy as np

def compute_divergence(L, dx, dy, dz):
    """Oblicza dywergencję pola wektorowego L = (Lx, Ly, Lz) na siatce 3D."""
    # Składowe L mają osie (x, y, z) -> axis 0, 1, 2
    dLx_dx = np.gradient(L[..., 0], dx, axis=0)  # Poprawione: axis=0 dla x
    dLy_dy = np.gradient(L[..., 1], dy, axis=1)  # Poprawione: axis=1 dla y
    dLz_dz = np.gradient(L[..., 2], dz, axis=2)  # Bez zmian
    return dLx_dx + dLy_dy + dLz_dz

# --- TEST (Sanity Check) ---
nx, ny, nz = 30, 40, 50
x, y, z = np.linspace(-5, 5, nx), np.linspace(-5, 5, ny), np.linspace(-5, 5, nz)
dx, dy, dz = x[1]-x[0], y[1]-y[0], z[1]-z[0]

# Generowanie siatki 'ij' (x, y, z) i pola testowego L = (x, y, z)
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
L = np.stack([X, Y, Z], axis=-1)

div_L = compute_divergence(L, dx, dy, dz)
print(f"Kształt: {div_L.shape}, Średnia (powinno być 3.0): {np.mean(div_L):.1f}")
print(f"Czy wynik poprawny? {np.allclose(div_L, 3.0)}")
