import os
import json
import shutil
from datetime import datetime

print("[START] Inicjalizacja NFT Preparer (Grok + generacja)...")

# 1. Stwórz folder nft_ready
os.makedirs("nft_ready", exist_ok=True)

# 2. Wczytaj interpretację Groka (jeśli istnieje)
grok_interpretation = ""
if os.path.exists("grok_interpretation.json"):
    with open("grok_interpretation.json", "r") as f:
        grok_data = json.load(f)
        grok_interpretation = grok_data.get("interpretation", "")

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
with open("nft_ready/metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
print("[INFO] Zapisano nft_ready/metadata.json")

# 5. Skopiuj obraz, jeśli istnieje
if os.path.exists("matrix_field_map.png"):
    shutil.copy("matrix_field_map.png", "nft_ready/image.png")
    print("[INFO] Skopiowano obraz do nft_ready/image.png")
else:
    print("[WARNING] Brak matrix_field_map.png – pomijam kopiowanie obrazu.")

print("[SUCCESS] NFT przygotowane w folderze nft_ready/")
print("[INFO] Możesz teraz ręcznie wgrać pliki na Zora lub IPFS.")
os.makedirs("nft_ready", exist_ok=True)
