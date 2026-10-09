#!/usr/bin/env python3
"""
AINUMPSA – Knowledge Registry & Hash Sealer (v1.1)
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge_base")
META_OUTPUT_DIR = Path("nft_ready")

def register_file(filepath: Path):
    try:
        # Odczyt pliku w bezpiecznym kodowaniu UTF-8
        content = filepath.read_text(encoding="utf-8")
        
        # Generowanie unikalnego hasha MD5
        hash_id = hashlib.md5(content.encode("utf-8")).hexdigest()[:16]
        
        metadata = {
            "source": str(filepath),
            "hash": hash_id,
            "timestamp": datetime.now().isoformat(),
            "type": "knowledge_matrix",
            "status": "active"
        }
        
        # Upewnienie się, że katalog docelowy istnieje
        META_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Zapis metadanych w czytelnym formacie JSON
        meta_filename = META_OUTPUT_DIR / f"{hash_id}.json"
        with open(meta_filename, "w", encoding="utf-8") as m:
            json.dump(metadata, m, indent=2, ensure_ascii=False)
            
        print(f"[SUCCESS] Zarejestrowano strukturę: {filepath.name} -> Hash: {hash_id}")
        return metadata

    except Exception as e:
        print(f"[WARN] Błąd podczas przetwarzania pliku {filepath}: {e}")
        return None

def main():
    print("\n[START] Inicjalizacja rejestru bazy wiedzy AINUMPSA...")
    
    if not KNOWLEDGE_DIR.exists():
        print(f"[SKIP] Katalog {KNOWLEDGE_DIR} nie istnieje. Tworzę pustą strukturę.")
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        return

    processed_count = 0
    for root, dirs, files in os.walk(KNOWLEDGE_DIR):
        for file in files:
            if file.endswith(".txt") and not file.endswith(".meta"):
                file_path = Path(root) / file
                register_file(file_path)
                processed_count += 1

    print(f"[FINISHED] Przetwarzanie zakończone. Przeanalizowano {processed_count} struktur.")

if __name__ == "__main__":
    main()
