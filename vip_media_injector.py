import os
import json
import hashlib

def inject_vip_media():
    print("\n[START] Inicjalizacja VIP Media Injector...")
    
    # Folder z mediami wejściowymi
    input_dir = "inputs/media"
    
    # Sprawdź, czy folder istnieje, jeśli nie - stwórz
    if not os.path.exists(input_dir):
        print(f"[INFO] Tworzę folder: {input_dir}")
        os.makedirs(input_dir)
        # Tworzymy pusty plik tekstowy w środku, żeby Git zachował folder
        with open(f"{input_dir}/.gitkeep", "w") as f:
            f.write("")

    print(f"[OK] Katalog {input_dir} jest gotowy.")

    # Lista plików w katalogu (pomijamy .gitkeep)
    files = [f for f in os.listdir(input_dir) if f != ".gitkeep"]

    if not files:
        print("[SKIP] Katalog inputs/media jest pusty. Nie ma nic do przetworzenia.")
        return

    # Przetwarzamy pierwszy znaleziony plik
    media_file_name = files[0]
    media_path = os.path.join(input_dir, media_file_name)
    print(f"[INFO] Znaleziono plik do przetworzenia: {media_file_name}")

    # Generowanie HASH'a pliku (unikalny identyfikator)
    try:
        with open(media_path, "rb") as f:
            file_data = f.read()
            file_hash = hashlib.sha256(file_data).hexdigest()
            file_size = len(file_data)
        print(f"[OK] Hash SHA256: {file_hash}")
        print(f"[OK] Rozmiar pliku: {file_size} bajtów")
    except Exception as e:
        print(f"[ERROR] Nie można odczytać pliku: {e}")
        return

    # --- Generowanie metadanych JSON ---
    metadata = {
        "description": "AINUMPSA: Automatyczny rzut kwantowy matrycy.",
        "image": f"ipfs://{file_hash}", # Tu w normalnym systemie byłby link IPFS
        "name": f"AINUMPSA_MATRIX_MINT_{media_file_name}",
        "attributes": [
            {"trait_type": "Origin", "value": "VIP_MEDIA_INJECTOR_V1"},
            {"trait_type": "File_Hash", "value": file_hash},
            {"trait_type": "File_Size_Bytes", "value": file_size},
            {"trait_type": "Kwantowy_Status", "value": "Stabilny_1>0"},
            {"trait_type": "Hyper_Version", "value": "2.14"}
        ]
    }

    # Zapisanie metadanych do pliku metadata.json
    output_metadata_path = "metadata.json"
    try:
        with open(output_metadata_path, "w", encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        print(f"[SUCCESS] Zapisano metadane do: {output_metadata_path}")
    except Exception as e:
        print(f"[ERROR] Nie można zapisać metadanych: {e}")

    print("[FINISHED] VIP Media Injector zakończył pracę.\n")

if __name__ == "__main__":
    inject_vip_media()

