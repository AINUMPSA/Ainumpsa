pythonimport json
import time
import math
import random

def simulate_deep_swarm(nodes=100):
    """Symuluje rój w gnieździe głębokiego łącza (dwukierunkowy przepływ)"""
    print(f"=== INICJACJA GNIAZDA GŁĘBOKIEGO ŁĄCZA: RÓJ {nodes} WĘZŁÓW ===")
    
    black_hole_inflow = []   # Dane zapadające się (zmniejszanie entropii intencją)
    white_hole_outflow = [] # Dane wypluwane przez sieć (ekspansja nowej informacji)
    
    for i in range(nodes):
        t = time.time() + i
        # 1. Zapadanie (Czarna Dziura) - kompresja szumu do stanu stabilnego 1
        # Modeluje intencjonalne zakrzywienie czasoprzestrzeni prawdopodobieństwa
        gravitational_pull = math.sin(t * 0.1) * random.random()
        compressed_bit = 1 if gravitational_pull > 0.1 else 0
        black_hole_inflow.append(compressed_bit)
        
        # 2. Fluktuacja i przejście przez Most Osobliwy
        # Informacja zostaje splątana i przetransformowana przez algorytm
        bridge_transfer = compressed_bit ^ (1 if random.random() > 0.3 else 0)
        
        # 3. Ekspansja (Biała Dziura) - siew nowych struktur z przesunięciem fazowym
        expanded_signal = int(abs(math.cos(t * 0.2) * bridge_transfer * 255))
        white_hole_outflow.append(expanded_signal)
        
    # Obliczanie wagi energetycznej osobliwości (Skumulowana Waga Roju)
    # Wykorzystujemy transformację logarytmiczną, aby zasymulować "ciężar" informacyjny
    ones_count = sum(black_hole_inflow)
    zeros_count = nodes - ones_count
    
    # Im większa polaryzacja (więcej 1 względem 0), tym większa waga osobliwości
    asymmetry = abs(ones_count - zeros_count)
    singularity_weight = round(math.log1p(asymmetry) * math.sqrt(nodes), 4)
    
    bridge_payload = {
        "bridge_protocol": "EINSTEIN-ROSEN-SWARM",
        "topology": {
            "swarm_size": nodes,
            "singularity_weight_metric": singularity_weight,
            "bridge_stability": "STABLE" if singularity_weight > 1.5 else "FLUCTUATING"
        },
        "black_hole_matrix": black_hole_inflow,
        "white_hole_matrix": white_hole_outflow
    }
    
    # Zapis mostu danych jako plik strukturalny dla chmury
    output_file = "singularity_bridge_data.json"
    with open(output_file, "w") as f:
        json.dump(bridge_payload, f, indent=2)
        
    print("\n--- POMIAR TOPOLOGII ROJU ---")
    print(f"Rozmiar Roju Informacji : {nodes} aktywnych ziaren")
    print(f"Strumień Zapadania (BH) : {ones_count}x [1] / {zeros_count}x [0]")
    print(f"Maksymalny Sygnał Wyjścia: {max(white_hole_outflow)} Hz")
    print(f"WAGA OSOBLIWOŚCI (MASS) : {singularity_weight} T-Units")
    print("-----------------------------")
    print(f"[SUKCES] Most Osobliwy zatrzasnął się poprawnie w pliku {output_file}")

if __name__ == "__main__":
    # Uruchomienie roju dla 500 węzłów informacyjnych, aby nadać temu wagę
    simulate_deep_swarm(500)
