import os
import json
import hashlib
from datetime import datetime

def inject_vip_media():
    print("\n[START] Inicjalizacja VIP Media Injector...")

    input_dir = "inputs/media"

    if not os.path.exists(input_dir):
        print(f"[INFO] Tworzę folder: {input_dir}")
        os.makedirs(input_dir)
        with open(f"{input_dir}/.gitkeep", "w") as f:
            f.write("")

    print(f"[OK] Katalog {input_dir} jest gotowy.")

    files = [f for f in os.listdir(input_dir) if f != ".gitkeep"]

    if not files:
        print("[SKIP] Katalog inputs/media jest pusty.")
        return

    for media_file_name in files:
        media_path = os.path.join(input_dir, media_file_name)
        print(f"\n[INFO] Przetwarzanie: {media_file_name}")

        try:
            with open(media_path, "rb") as f:
                file_data = f.read()
                file_hash = hashlib.sha256(file_data).hexdigest()
                file_size = len(file_data)
            print(f"[OK] Hash SHA256: {file_hash[:16]}...")
            print(f"[OK] Rozmiar pliku: {file_size} bajtów")
        except Exception as e:
            print(f"[ERROR] Nie można odczytać pliku: {e}")
            continue

        metadata = {
            "description": f"AINUMPSA: Automatyczny rzut kwantowy matrycy z pliku {media_file_name}.",
            "image": f"ipfs://{file_hash}",
            "name": f"AINUMPSA_MATRIX_MINT_{media_file_name}",
            "attributes": [
                {"trait_type": "Origin", "value": "VIP_MEDIA_INJECTOR_V2"},
                {"trait_type": "File_Hash", "value": file_hash},
                {"trait_type": "File_Size_Bytes", "value": file_size},
                {"trait_type": "File_Name", "value": media_file_name},
                {"trait_type": "Kwantowy_Status", "value": "Stabilny_1>0"},
                {"trait_type": "Hyper_Version", "value": "2.14"}
            ]
        }

        os.makedirs("nft_ready", exist_ok=True)
        output_filename = f"nft_ready/{file_hash[:8]}.json"
        try:
            with open(output_filename, "w", encoding='utf-8') as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
            print(f"[SUCCESS] Zapisano metadane do: {output_filename}")
        except Exception as e:
            print(f"[ERROR] Nie można zapisać metadanych: {e}")

    print(f"\n[FINISHED] Przetworzono {len(files)} plików.")

if __name__ == "__main__":
    inject_vip_media()
