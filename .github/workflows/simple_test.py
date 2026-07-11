python
import numpy as np
import json
import matplotlib.pyplot as plt

print("=== SIMPLE TEST: OBLICZENIA Z NUMPY ===")

x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
z = np.linspace(-5, 5, 30)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
L = np.stack([X, Y, Z], axis=-1)

dx = x[1] - x[0]
dy = y[1] - y[0]
dz = z[1] - z[0]

dLx = np.gradient(L[..., 0], dx, axis=0)
dLy = np.gradient(L[..., 1], dy, axis=1)
dLz = np.gradient(L[..., 2], dz, axis=2)
div = dLx + dLy + dLz

data = {
    "max_div": float(np.max(np.abs(div))),
    "mean_div": float(np.mean(div)),
    "shape": list(div.shape)
}
with open("tensor_t_logs.json", "w") as f:
    json.dump(data, f, indent=2)
print("✅ Zapisano tensor_t_logs.json")

plt.figure(figsize=(6, 5))
plt.imshow(div[:, :, 0], cmap='RdBu', aspect='auto')
plt.colorbar(label='div L')
plt.title('Simple test: div L = 3')
plt.savefig("field_coherence_chart.png")
print("✅ Zapisano field_coherence_chart.png")
