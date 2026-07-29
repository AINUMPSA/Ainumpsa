import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image, ImageFilter, ImageEnhance

print("[START] Inicjalizacja Matrix Collider – 10 wersji...")

# 1. Sprawdź, czy istnieje obraz wejściowy z inputs/media/
input_image_path = None
if os.path.exists("inputs/media"):
    files = [f for f in os.listdir("inputs/media") if f.endswith(('.jpg', '.png', '.jpeg'))]
    if files:
        input_image_path = os.path.join("inputs/media", files[0])
        print(f"[INFO] Znaleziono obraz wejściowy: {input_image_path}")

# 2. Wczytaj 10 zestawów parametrów od Groka
params_list = []
if os.path.exists("grok_10_versions.json"):
    with open("grok_10_versions.json", "r") as f:
        params_list = json.load(f)
        print(f"[INFO] Wczytano {len(params_list)} zestawów parametrów od Groka.")

# 3. Jeśli brak parametrów – użyj domyślnych (10 różnych stylów)
if not params_list:
    params_list = [
        {"style": "surrealism", "colors": ["#FFD700", "#FF8C00", "#4A90D9"], "composition": "spiral"},
        {"style": "cubism", "colors": ["#FF5733", "#33FF57", "#3357FF"], "composition": "symmetry"},
        {"style": "abstract", "colors": ["#FF33A8", "#33FFF5", "#F5FF33"], "composition": "chaos"},
        {"style": "expressionism", "colors": ["#8B0000", "#FF4500", "#FFD700"], "composition": "radial"},
        {"style": "cosmic", "colors": ["#0B0B3B", "#1A1A5E", "#3A3A8A"], "composition": "spiral"},
        {"style": "minimalism", "colors": ["#FFFFFF", "#808080", "#000000"], "composition": "grid"},
        {"style": "pop_art", "colors": ["#FF0000", "#00FF00", "#0000FF"], "composition": "dots"},
        {"style": "impressionism", "colors": ["#FFB6C1", "#FFD700", "#98FB98"], "composition": "blur"},
        {"style": "futurism", "colors": ["#FF00FF", "#00FFFF", "#FFFF00"], "composition": "dynamic"},
        {"style": "kubizm", "colors": ["#8B4513", "#D2B48C", "#F5DEB3"], "composition": "fragments"}
    ]
    print("[INFO] Użyto domyślnych 10 stylów.")

# 4. Generowanie 10 wersji
os.makedirs("variant_images", exist_ok=True)

for i, params in enumerate(params_list[:10]):  # ograniczamy do 10
    try:
        print(f"[INFO] Generowanie wersji {i+1}: {params.get('style', 'default')}")

        # Jeśli istnieje obraz wejściowy – użyj go, w przeciwnym razie wygeneruj losowe dane
        if input_image_path and os.path.exists(input_image_path):
            img = Image.open(input_image_path).convert('RGB')
            # Przekształcenia w zależności od stylu
            if params.get('style') == 'surrealism':
                img = img.filter(ImageFilter.EMBOSS)
            elif params.get('style') == 'cubism':
                img = img.resize((img.width // 4, img.height // 4)).resize((img.width, img.height), Image.NEAREST)
            elif params.get('style') == 'impressionism':
                img = img.filter(ImageFilter.GaussianBlur(radius=3))
            elif params.get('style') == 'abstract':
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(np.random.uniform(0.5, 1.5))
            # Konwersja do numpy dla matplotlib
            data = np.array(img)
        else:
            # Generowanie losowego pola
            data = np.random.rand(100, 100) * 10

        # Dodanie losowego przesunięcia, aby każda wersja była unikalna
        random_offset = np.random.uniform(-0.5, 0.5)
        data_modified = data + random_offset

        # Wybór colormap na podstawie kolorów
        cmap = params.get('colors', ['#FFD700', '#FF8C00', '#4A90D9'])
        # Użyj pierwszego koloru jako nazwy cmap (lub 'plasma' jako domyślny)
        cmap_name = 'plasma'  # domyślnie

        # Generowanie obrazu
        plt.figure(figsize=(8, 8))
        plt.imshow(data_modified, cmap=cmap_name, interpolation='bilinear')
        plt.axis('off')

        # Dodanie tytułu z datą i stylem
        title = f"AINUMPSA – {params.get('style', 'style')}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        plt.title(title, fontsize=10, color='white', backgroundcolor='black')

        # Zapis obrazu jako variant_{i+1}.png
        filename = f"variant_{i+1}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight', pad_inches=0.1)
        plt.close()
        print(f"[SUCCESS] Zapisano {filename}")

    except Exception as e:
        print(f"[ERROR] Błąd przy generowaniu wersji {i+1}: {e}")

# 5. Zapisanie podsumowania
summary = {
    "timestamp": datetime.now().isoformat(),
    "input_image": input_image_path,
    "versions_generated": len(params_list[:10]),
    "styles": [p.get('style') for p in params_list[:10]]
}
with open("collider_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("[INFO] Zapisano collider_summary.json")
print("[FINISHED] Matrix Collider zakończył pracę – wygenerowano 10 wersji.")
