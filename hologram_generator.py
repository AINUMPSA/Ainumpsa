import numpy as np
import json
from PIL import Image
import os

print("🌀 Generowanie hologramu...")

with open("light_shadow_merged.json", "r") as f:
    data = json.load(f)

size = 1024
hologram = np.zeros((size, size))

for point in data["light"] + data["shadow"]:
    x = int((point["theta"] / 360) * size)
    y = int((point["phi"] / 360) * size)
    if 0 <= x < size and 0 <= y < size:
        hologram[x, y] += 1

hologram = np.clip(hologram, 0, 255).astype(np.uint8)

os.makedirs("multimodal_pool", exist_ok=True)
img = Image.fromarray(hologram, mode='L')
img.save("multimodal_pool/hologram_0.5c_to_horizon.png")
print("✅ Hologram zapisany")
