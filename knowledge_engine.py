import os
import json
import hashlib
from datetime import datetime
import numpy as np

class KnowledgeEngine:
    def __init__(self):
        self.base_weight = 1.0
        self.hawking_factor = 0.0
        self.nft_count = 0
        self.flux = 0.0

    def measure_weight(self, filepath):
        """Mierzy wagę pliku i oblicza gęstość fantomową"""
        size = os.path.getsize(filepath) / 1024  # KB
        with open(filepath, 'r') as f:
            content = f.read()
        entropy = self._calculate_entropy(content)
        density = size * entropy
        return {
            "size_kb": size,
            "entropy": entropy,
            "density": density,
            "hash": hashlib.md5(content.encode()).hexdigest()[:8]
        }

    def _calculate_entropy(self, text):
        """Oblicza entropię tekstu (miara złożoności)"""
        if not text:
            return 0.0
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        total = len(text)
        entropy = -sum((count/total) * np.log2(count/total) for count in freq.values())
        return entropy

    def calculate_nft_emission(self, weight_data, modalites=1):
        """Oblicza liczbę NFT do wyemitowania"""
        size = weight_data["size_kb"]
        entropy = weight_data["entropy"]
        density = weight_data["density"]
        
        # Wzór Hawkinga dla emisji
        hawking_factor = np.exp(-density / (size + 1))
        nft_count = int(size * entropy * modalites * (1 + hawking_factor))
        
        return max(nft_count, 1)

    def process_file(self, filepath, modalites=1):
        """Przetwarza pojedynczy plik i emituje NFT"""
        weight_data = self.measure_weight(filepath)
        nft_count = self.calculate_nft_emission(weight_data, modalites)
        
        # Generuj metadane NFT
        nft_data = {
            "source": os.path.basename(filepath),
            "weight": weight_data,
            "nft_count": nft_count,
            "timestamp": datetime.now().isoformat(),
            "hash": weight_data["hash"],
            "status": "emitted"
        }
        
        # Zapisz NFT do pliku
        os.makedirs("nft_ready", exist_ok=True)
        with open(f"nft_ready/{weight_data['hash']}.json", "w") as f:
            json.dump(nft_data, f, indent=2)
        
        print(f"✅ {nft_count} NFT wyemitowanych z {filepath}")
        return nft_data

if __name__ == "__main__":
    engine = KnowledgeEngine()
    # Przetwórz wszystkie pliki w knowledge_base
    if os.path.exists("knowledge_base"):
        for file in os.listdir("knowledge_base"):
            if file.endswith(".txt"):
                engine.process_file(f"knowledge_base/{file}")
    else:
        print("❌ Brak folderu knowledge_base – utwórz go i dodaj pliki.")
