import os
import json
import shutil
from datetime import datetime

print("[START] Inicjalizacja NFT Preparer (generowanie NFT z metadanych)...")

source_dir = "nft_ready"
output_dir = "nft_ready/final"
os.makedirs(output_dir, exist_ok=True)

json_files = [f for f in os.listdir(source_dir) if f.endswith(".json") and f != "metadata.json"]

if not json_files:
    print("[SKIP] Brak plików JSON do przetworzenia.")
    exit()

print(f"[INFO] Znaleziono {len(json_files)} plików JSON.")

for json_file in json_files:
    json_path = os.path.join(source_dir, json_file)
    
    try:
        with open(json_path, "r") as f:
            metadata = json.load(f)
        
        name = metadata.get("name", "AINUMPSA_NFT")
        description = metadata.get("description", "Autonomicznie wygenerowane NFT przez AINUMPSA.")
        
        nft_data = {
            "name": name,
            "description": description,
            "image": metadata.get("image", "ipfs://placeholder"),
            "attributes": metadata.get("attributes", []),
            "timestamp": datetime.now().isoformat(),
            "status": "1>0 LOCKED"
        }
        
        output_filename = os.path.join(output_dir, json_file)
        with open(output_filename, "w") as f:
            json.dump(nft_data, f, indent=2)
        
        print(f"[SUCCESS] Wygenerowano NFT: {output_filename}")
        
        base_name = json_file.replace(".json", "")
        for ext in [".png", ".jpg", ".jpeg", ".gif"]:
            img_path = os.path.join(source_dir, base_name + ext)
            if os.path.exists(img_path):
                shutil.copy(img_path, os.path.join(output_dir, base_name + ext))
                print(f"[INFO] Skopiowano obraz: {base_name + ext}")
                break
            
    except Exception as e:
        print(f"[ERROR] Błąd przetwarzania {json_file}: {e}")

print(f"[FINISHED] Przygotowano {len(json_files)} NFT w folderze {output_dir}")
