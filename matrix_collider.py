import os
import json
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

print("[START] Inicjalizacja Matrix Collider...")

# 1. Symulacja danych (np. z QRNG lub innego źródła)
data = np.random.rand(100, 100) * 10  # przykładowe dane

# 2. Wczytaj parametry wizualizacji od Groka (jeśli istnieją)
visual_params = {}
if os.path.exists("visual_params.json"):
    with open("visual_params.json", "r") as f:
        visual_params = json.load(f)
        print("[INFO] Wczytano parametry wizualizacji od Groka.")

# 3. Ustawienia domyślne
cmap = visual_params.get("colors", ["#FFD700", "#FF8C00", "#4A90D9"])
style = visual_params.get("style", "spiral")
composition = visual_params.get("composition", "symmetry")

# 4. Dodaj losowe przesunięcie, aby obraz był unikalny
random_offset = random.uniform(-0.5, 0.5)
data_modified = data + random_offset

# 5. Generowanie obrazu
plt.figure(figsize=(8, 8))
plt.imshow(data_modified, cmap='plasma', interpolation='bilinear')
plt.axis('off')

# 6. Dodanie tytułu z datą i parametrami
title = f"AINUMPSA Resonance Field\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
plt.title(title, fontsize=10, color='white', backgroundcolor='black')

# 7. Zapis obrazu (nadpisuje poprzedni)
plt.savefig("matrix_field_map.png", dpi=150, bbox_inches='tight', pad_inches=0.1)
print("[SUCCESS] Zapisano matrix_field_map.png")

# 8. Zapisanie informacji o parametrach do pliku (opcjonalnie)
params_log = {
    "timestamp": datetime.now().isoformat(),
    "cmap": cmap,
    "style": style,
    "composition": composition,
    "random_offset": random_offset
}
with open("collider_params_log.json", "w") as f:
    json.dump(params_log, f, indent=2)

print("[INFO] Zapisano collider_params_log.json")
print("[FINISHED] Matrix Collider zakończył pracę.")
