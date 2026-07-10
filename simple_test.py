python
import numpy as np
import json
import matplotlib.pyplot as plt

# Tworzymy siatkę i pole testowe
x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 40)
z = np.linspace(-5, 5, 50)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
L = np.stack([X, Y, Z], axis=-1)  # pole L = (x, y, z)

# Liczymy dywergencję
def compute_div(L, dx, dy, dz):
    dLx_dx = np.gradient(L[..., 0], dx, axis=0)
    dLy_dy = np.gradient(L[..., 1], dy, axis=1)
    dLz_dz = np.gradient(L[..., 2], dz, axis=2)
    return dLx_dx + dLy_dy + dLz_dz

dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]
div = compute_div(L, dx, dy, dz)

# Zapis do JSON
data = {
    "max_div": float(np.max(np.abs(div))),
    "mean_div": float(np.mean(div)),
    "shape": list(div.shape)
}
with open("tensor_t_logs.json", "w") as f:
    json.dump(data, f, indent=2)

# Wykres
plt.figure()
plt.imshow(div[:, :, 0], cmap='RdBu', aspect='auto')
plt.colorbar(label='div L')
plt.title('Dywergencja pola testowego (simple_test)')
plt.savefig("field_coherence_chart.png")
print("✅ Pliki zapisane")
