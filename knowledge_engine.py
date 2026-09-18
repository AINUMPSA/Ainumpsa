#!/usr/bin/env python3
"""
AINUMPSA – Knowledge Engine (v3)
- Hash SHA-256 (16 znaków) — praktycznie bez kolizji
- Sprawdza source + weight + nft_count (poza timestampem)
- Nie nadpisuje pliku, jeśli treść się nie zmieniła
"""

import os
import json
import hashlib
from datetime import datetime
import numpy as np

HASH_LENGTH = 16  # było 8 → teraz 16


class KnowledgeEngine:
    def __init__(self):
        self.base_weight = 1.0
        self.hawking_factor = 0.0
        self.nft_count = 0
        self.flux = 0.0

    def measure_weight(self, filepath):
        """Mierzy wagę pliku i oblicza gęstość fantomową."""
        size = os.path.getsize(filepath) / 1024  # KB
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        entropy = self._calculate_entropy(content)
        density = size * entropy
        return {
            "size_kb": size,
            "entropy": entropy,
            "density": density,
            "hash": hashlib.sha256(content.encode("utf-8")).hexdigest()[:HASH_LENGTH],
        }

    def _calculate_entropy(self, text):
        """Oblicza entropię tekstu (miara złożoności)."""
        if not text:
            return 0.0
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        total = len(text)
        entropy = -sum((count / total) * np.log2(count / total) for count in freq.values())
        return entropy

    def calculate_nft_emission(self, weight_data, modalites=1):
        """Oblicza liczbę NFT do wyemitowania (wzór Hawkinga)."""
        size = weight_data["size_kb"]
        entropy = weight_data["entropy"]
        density = weight_data["density"]

        hawking_factor = np.exp(-density / (size + 1))
        nft_count = int(size * entropy * modalites * (1 + hawking_factor))

        return max(nft_count, 1)

    def process_file(self, filepath, modalites=1):
        """Przetwarza pojedynczy plik i emituje NFT."""
        weight_data = self.measure_weight(filepath)
        nft_count = self.calculate_nft_emission(weight_data, modalites)

        source_name = os.path.basename(filepath)

        nft_data = {
            "source": source_name,
            "weight": weight_data,
            "nft_count": nft_count,
            "timestamp": datetime.now().isoformat(),
            "hash": weight_data["hash"],
            "status": "emitted",
        }

        os.makedirs("nft_ready", exist_ok=True)
        path = f"nft_ready/{weight_data['hash']}.json"

        # Sprawdź, czy plik istnieje i czy treść (poza timestampem) jest ta sama
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    old = json.load(f)

                old_copy = {k: v for k, v in old.items() if k != "timestamp"}
                new_copy = {k: v for k, v in nft_data.items() if k != "timestamp"}

                if old_copy == new_copy:
                    print(f"[SKIP] {path} - brak zmian w tresci")
                    return nft_data

                # Kolizja wykryta: ten sam hash, ale inny source
                if old.get("source") != source_name:
                    print(f"[COLLISION] {path} — hash kolizja z {old.get('source')} → {source_name}")

            except Exception as e:
                print(f"[WARN] Nie mozna odczytac {path}: {e}")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(nft_data, f, indent=2, ensure_ascii=False)

        print(f"✅ {nft_count} NFT wyemitowanych z {filepath}")
        return nft_data


if __name__ == "__main__":
    engine = KnowledgeEngine()

    if os.path.exists("knowledge_base"):
        for file in os.listdir("knowledge_base"):
            if file.endswith(".txt"):
                engine.process_file(f"knowledge_base/{file}")
    else:
        print("❌ Brak folderu knowledge_base – utwórz go i dodaj pliki.")
