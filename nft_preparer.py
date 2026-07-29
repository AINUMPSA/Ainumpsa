from datetime import datetime
import json
import os
import shutil

print("[START] Inicjalizacja NFT Preparer...")

# 1. Wyznaczenie stabilnej ścieżki roboczej względem skryptu
script_dir = os.path.dirname(os.path.abspath(__file__))
nft_dir = os.path.join(script_dir, "nft_ready")

try:
    os.makedirs(nft_dir, exist_ok=True)
    print(f"[INFO] Folder nft_ready potwierdzony w: {nft_dir}")
except Exception as e:
    print(f"[ERROR] Błąd podczas tworzenia folderu: {e}")

# 2. Odczyt opisu wygenerowanego przez Groka
grok_interpretation = ""
if os.path.exists("grok_interpretation.json"):
    try:
        with open("grok_interpretation.json", "r", encoding="utf-8") as f:
            grok_data = json.load(f)
            grok_interpretation = grok_data.get("interpretation", "")
            print("[INFO] Wczytano unikalną interpretację Groka.")
    except Exception as e:
        print(f"[WARNING] Błąd odczytu grok_interpretation.json: {e}")
else:
    print("[INFO] Brak pliku grok_interpretation.json – używam domyślnego opisu.")

# 3. Kopiowanie obrazu z matrycy
source_image = "matrix_field_map.png"
dest_image_path = os.path.join(nft_dir, "image.png")

if os.path.exists(source_image):
    shutil.copy(source_image, dest_image_path)
    print(f"[INFO] Zaktualizowano obraz NFT w: {dest_image_path}")
else:
    print("[WARNING] Brak matrix_field_map.png – pomijam obraz.")

# 4. Generowanie unikalnych metadanych z dynamicznym Timestampem
timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
unix_timestamp = int(datetime.now().timestamp())

metadata = {
    "name": f"AINUMPSA Resonance #{unix_timestamp}",
    "description": grok_interpretation
    or f"Dynamic Tensor T Resonance Field generated at {timestamp_str}.",
    "image": "image.png",
    "attributes": [
        {"trait_type": "Source", "value": "AINUMPSA 3D Matrix"},
        {"trait_type": "Timestamp", "value": timestamp_str},
        {"trait_type": "Status", "value": "1>0 LOCKED"},
    ],
}

# 5. Zapis metadanych do JSON
metadata_path = os.path.join(nft_dir, "metadata.json")
with open(metadata_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(
    f"[SUCCESS] Nowa wersja NFT zaktualizowana w nft_ready/ ({timestamp_str})"
)
