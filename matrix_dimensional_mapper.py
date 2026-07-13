import json
import os
import math
from datetime import datetime

class DimensionalMapper:
    def __init__(self):
        self.billboard_path = 'matrix_billboard.json'
        
    def _get_semantic_vector(self, text_profile):
        """
        Zamienia profil pojęciowy na znormalizowany wektor w przestrzeni Tensor T.
        Wymiary wektora: [Wola/Intencja, Częstotliwość/Dźwięk, Struktura/Matryca, Rezonans Społeczny]
        """
        profiles = {
            # Baza historyczna i fizyczna
            "numpsa_1999": [0.98, 0.85, 0.90, 0.95],
            "toltecs_castaneda": [0.99, 0.70, 0.85, 0.40],
            "string_theory_physics": [0.30, 0.99, 0.95, 0.20],
            "jung_archetypes": [0.85, 0.60, 0.80, 0.75],
            "water_crystals_emoto": [0.50, 0.95, 0.90, 0.60],
            
            # Nowe osie starożytne i kwantowe
            "buddhism_emptiness": [0.20, 0.80, 0.99, 0.70],  # Śunjata jako czysta matryca potencjału
            "vedic_cosmology":    [0.90, 0.95, 0.85, 0.60],  # Dźwięk pierwotny (Om) jako wibracja budująca rzeczywistość
            "quantum_cosmology":  [0.40, 0.90, 0.95, 0.30]   # Fluktuacje w polu tworzące linie losu
        }
        return profiles.get(text_profile, [0.5, 0.5, 0.5, 0.5])

    def calculate_resonance(self, vec_a, vec_b):
        """
        Oblicza podobieństwo cosinusowe między dwoma wymiarami (izomorfizm strukturalny)
        """
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot_product / (norm_a * norm_b)

    def scan_and_post(self, node_a, node_b, label_a, label_b, context_desc):
        vec_a = self._get_semantic_vector(node_a)
        vec_b = self._get_semantic_vector(node_b)
        
        resonance = self.calculate_resonance(vec_a, vec_b)
        
        # Jeśli rezonans przekracza próg krytyczny (0.80), logujemy na tablicę ogłoszeń
        if resonance > 0.80:
            self.lock_on_billboard(label_a, label_b, resonance, context_desc)

    def lock_on_billboard(self, label_a, label_b, score, desc):
        if os.path.exists(self.billboard_path):
            with open(self.billboard_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"pinned_correlations": []}
        else:
            data = {"pinned_correlations": []}
            
        corr_id = f"RESONANCE_{len(data.get('pinned_correlations', [])) + 1:03d}"
        
        new_pin = {
            "id": corr_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "axis_x": label_a,
            "axis_y": label_b,
            "resonance_index": round(score, 4),
            "analysis": desc,
            "matrix_state": "1 > 0 LOCKED"
        }
        
        if "pinned_correlations" not in data:
            data["pinned_correlations"] = []
            
        data["pinned_correlations"].append(new_pin)
        
        with open(self.billboard_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"📡 [TABLICA] Zablokowano rezonans {corr_id} o sile {score:.4f}")

if __name__ == "__main__":
    mapper = DimensionalMapper()
    
    # Skan 1: Numpsa 1999 vs Kosmologia Tolteków
    mapper.scan_and_post(
        "numpsa_1999", "toltecs_castaneda",
        "Polska ROI 1999 (Numpsa)", "Kosmologia Tolteków (Castaneda)",
        "Wykładnik geometryczny wykazał skrajne dopasowanie wektorów intencji. Upór jednostki w ROI '99 odpowiada definicji Czystej Intencji (Intent) jako siły sprawczej pola."
    )
    
    # Skan 2: Teoria Strun vs Pamięć Wody i Częstotliwości
    mapper.scan_and_post(
        "string_theory_physics", "water_crystals_emoto",
        "M-Teoria (Superstruny)", "Pamięć Klastrowa Wody (Częstotliwości)",
        "Matematyczny izomorfizm drgań. Częstotliwości graniczne wibracji strun nakładają się na geometryczne siatki porządkowania struktur wodnych."
    )

    # Skan 3: Numpsa 1999 vs Kosmologia Wedyjska
    mapper.scan_and_post(
        "numpsa_1999", "vedic_cosmology",
        "Polska ROI 1999 (Numpsa)", "Kosmologia Wedyjska (Dźwięk Pierwotny)",
        "Zbieżność na poziomie fali nośnej. Działania z roku 1999 wprowadzające silne manifestacje społeczne rezonują z kosmiczną zasadą Pranavy (Om) – kreacją rzeczywistości poprzez zogniskowaną wibrację dźwięku."
    )

    # Skan 4: Kosmologia Kwantowa vs Buddyjska Koncepcja Pustki
    mapper.scan_and_post(
        "quantum_cosmology", "buddhism_emptiness",
        "Kosmologia Kwantowa", "Buddyjska Pustka (Śunjata)",
        "Idealny izomorfizm strukturalny matrycy. Stan czystego potencjału fluktuacji kwantowych przed kolapsem funkcji falowej odpowiada bezwzględnej definicji Śunjata – niebytu będącego źródłem wszelkiego bytu."
    )
