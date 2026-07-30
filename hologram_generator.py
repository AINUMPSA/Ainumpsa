import numpy as np
import json
from PIL import Image
import os

# Wczytaj dane
with open("light_shadow_merged.json", "r") as f:
    data = json.load(f)

# Stwórz hologram
size = 1024
hologram = np.zeros((size, size))

# Zaznacz punkty
for point in data["light"] + data["shadow"]:
    x = int((point["theta"] / 360) * size)
    y = int((point["phi"] / 360) * size)
    if 0 <= x < size and 0 <= y < size:
        hologram[x, y] += 1

# Normalizacja
hologram = np.clip(hologram, 0, 255).astype(np.uint8)

# Zapisz
os.makedirs("multimodal_pool", exist_ok=True)
img = Image.fromarray(hologram, mode='L')
img.save("multimodal_pool/hologram_0.5c_to_horizon.png")
print("✅ Hologram zapisany")
