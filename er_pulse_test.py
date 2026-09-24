import json
import math
import random
import time

def calculate_er_wormhole_flux(nodes_count):
    # Symulacja tuneli ER (Mostków Einsteina-Rosena) między węzłami danych
    return [random.uniform(0.1, 1.0) * math.exp(i / 5.0) for i in range(nodes_count)]

def dark_em_phantom_fluctuation():
    # Pobieranie szumu z emergentnego pola fantomowych fluktuacji Dark E/M
    return random.gauss(0.5, 0.2) * math.sin(time.time())

def compute_intent_weight(entropy, tensor_mass, spacetime_inversion):
    # Wzór na wagę intencji: uwzględnia masę tensorową, entropię 
    # oraz punkt, w którym czas i przestrzeń rozchodzą się w przeciwnych kierunkach.
    denominator = max(0.01, 1.0 - abs(spacetime_inversion))
    return (tensor_mass * entropy) / denominator

def run_er_pulse_simulation():
    print("--- INICJALIZACJA TESTU POLA ER / DARK E/M ---")
    
    nodes = 16
    tensor_mass = 54.2
    entropy = 0.91
    
    # Przepływ przez tunele ER
    er_flux = calculate_er_wormhole_flux(nodes)
    
    # Fluktuacje z przyszłego pola Dark E/M
    phantom_noise = dark_em_phantom_fluctuation()
    
    # Zakrzywienie: przestrzeń ekspanduje, podczas gdy czas ulega inwersji (przeciwne kierunki)
    space_expansion = sum(er_flux) / nodes
    time_inversion = -space_expansion * phantom_noise  # Ujemny wektor czasu
    
    # Obliczenie wagi intencji w punkcie kolapsu
    intent_weight = compute_intent_weight(entropy, tensor_mass, time_inversion)
    
    simulation_packet = {
        "timestamp": time.time(),
        "active_er_nodes": nodes,
        "space_expansion_vector": round(space_expansion, 4),
        "time_inversion_vector": round(time_inversion, 4),
        "dark_em_phantom_noise": round(phantom_noise, 4),
        "intent_weight": round(intent_weight, 4),
        "metric_status": "CONVERGENCE_STABLE"
    }
    
    print(json.dumps(simulation_packet, indent=4))
    
    # Zapis wynikowego bufora do pliku testowego
    with open("er_pulse_output.json", "w") as f:
        json.dump(simulation_packet, f, indent=4)
        
    print("--- TEST ZAKOŃCZONY: Wygenerowano bufor fali w er_pulse_output.json ---")

if __name__ == "__main__":
    run_er_pulse_simulation()

