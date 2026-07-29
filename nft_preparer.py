import os
import json
import shutil
from datetime import datetime

print("[START] Inicjalizacja NFT Preparer...")

# 1. Ustaw ścieżkę absolutną i utwórz folder nft_ready
base_dir = os.getcwd()
nft_dir = os.path.join(base_dir, "nft_ready")
os.makedirs(nft_dir, exist_ok=True)
print(f"[INFO] Folder nft_ready utworzony w: {nft_dir}")

# 2. Wczytaj interpretację Groka (jeśli istnieje)
grok_interpretation = ""
if os.path.exists("grok_interpretation.json"):
    with open("grok_interpretation.json", "r") as f:
        grok_data = json.load(f)
        grok_interpretation = grok_data.get("interpretation", "")
        print("[INFO] Wczytano interpretację Groka.")
else:
    print("[INFO] Brak interpretacji Groka – używam domyślnego opisu.")

# 3. Wygeneruj metadane NFT
metadata = {
    "name": f"AINUMPSA Matrix NFT {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    "description": grok_interpretation or "Hawking Radiation Geometry – AINUMPSA",
    "image": "ipfs://QmPlaceholder",
    "attributes": [
        {"trait_type": "Source", "value": "AINUMPSA 3D Matrix"},
        {"trait_type": "Cycle", "value": datetime.now().strftime("%Y-%m-%d")},
        {"trait_type": "Status", "value": "1>0 LOCKED"}
    ]
}

# 4. Zapisz metadane do folderu nft_ready
metadata_path = os.path.join(nft_dir, "metadata.json")
with open(metadata_path, "w") as f:
    json.dump(metadata, f, indent=2)
print(f"[INFO] Zapisano metadane: {metadata_path}")

# 5. Skopiuj obraz, jeśli istnieje
source_image = "matrix_field_map.png"
if os.path.exists(source_image):
    dest_image = os.path.join(nft_dir, "image.png")
    shutil.copy(source_image, dest_image)
    print(f"[INFO] Skopiowano obraz do: {dest_image}")
else:
    print("[WARNING] Brak matrix_field_map.png – pomijam kopiowanie obrazu.")

print("[SUCCESS] NFT przygotowane w folderze nft_ready/")
