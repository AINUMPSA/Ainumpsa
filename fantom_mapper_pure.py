import numpy as np
from PIL import Image
import os
from datetime import datetime

print("🌀 FANTOM MAPPER PURE v1.0")
print("=" * 40)

# Tworzymy obraz z szumu (bo nie mamy danych)
size = 512
field = np.random.randn(size, size)
field = (field - np.min(field)) / (np.max(field) - np.min(field) + 1e-10)
field = (field * 255).astype(np.uint8)

# Zapisujemy
os.makedirs("multimodal_pool", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"multimodal_pool/fantom_map_{timestamp}.png"
img = Image.fromarray(field, mode='L')
img.save(filename)

print(f"✅ Obraz zapisany: {filename}")
print("✅ Gotowe.")
