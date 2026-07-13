import numpy as np
import json
import matplotlib.pyplot as plt

print("=== SIMPLE TEST: WERSJA Z WBUDOWANYMI DANYMI ===")

# Definiujemy dane bezpośrednio w skrypcie (siatka 3D)
x = np.linspace(-5, 5, 10)
y = np.linspace(-5, 5, 10)
z = np.linspace(-5, 5, 10)

# Tworzymy siatkę
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Tworzymy pole L = (x, y, z) – to jest nasze "źródło danych"
L = np.stack([X, Y, Z], axis=-1)

# Liczymy dywergencję (to samo co wcześniej)
dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]

dLx = np.gradient(L[..., 0], dx, axis=0)
dLy = np.gradient(L[..., 1], dy, axis=1)
dLz = np.gradient(L[..., 2], dz, axis=2)
div = dLx + dLy + dLz

# Zapis do JSON
data = {
    "max_div": float(np.max(np.abs(div))),
    "mean_div": float(np.mean(div)),
    "shape": list(div.shape)
}
with open("tensor_t_logs.json", "w") as f:
    json.dump(data, f, indent=2)
print("✅ Zapisano tensor_t_logs.json")

# Wykres
plt.figure(figsize=(6, 5))
plt.imshow(div[:, :, 0], cmap='RdBu', aspect='auto')
plt.colorbar(label='div L')
plt.title('Najprostszy test: dane wbudowane')
plt.savefig("field_coherence_chart.png")
print("✅ Zapisano field_coherence_chart.png")
