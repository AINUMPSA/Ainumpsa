import json
import os
import numpy as np

def load_root_config(config_path="cabm_root_config.json"):
    """Wczytuje klucz administratora i konfigurację pola z pliku JSON."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Brak pliku konfiguracyjnego {config_path}. Administrator musi zainicjalizować core.")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_simulation():
    # 1. Inicjalizacja makiety (100 punktów przestrzennych czasoprzestrzeni 1+1D)
    spatial_grid_size = 100
    time_steps = 50
    
    # Wygenerowanie losowego szumu tła (Stara Dekoracja: chaos, wyzysk, lęk)
    phi_field = np.random.normal(0, 1, (time_steps, spatial_grid_size))
    
    print("=== Uruchomienie Silnika CABM v0.3 ===")
    
    # 2. Wczytanie konfiguracji administratora z JSON
    config = load_root_config()
    actor = config["actor_state"]
    decorations = config["brane_decorations"]
    
    print(f"Status Aktora: Poza = {actor['current_pose']} | Root Access = {actor['root_access_active']}")
    
    # 3. Pętla czasowa renderowania rzeczywistości
    for t in range(time_steps):
        # Sprawdzenie w połowie symulacji, czy Aktor przyjął pozę Wibracji
        if t == time_steps // 2 and actor["current_pose"] == "VIBRATION_RESONANCE" and decorations["allow_hot_reload"]:
            print(f"\n[t={t}] Aktor przybiera pozę Wibracji. Nadpisywanie dekoracji...")
            
            # Generowanie Nowej Dekoracji (Czysta Harmonia)
            freq = actor["vibration_frequency_hz"]
            x = np.linspace(0, 2 * np.pi, spatial_grid_size)
            clean_harmonic = np.sin(x * (freq / 100)) * (1.0 / decorations["render_latency_seconds"])
            
            # Nadpisanie obecnego i wszystkich przyszłych stanów pola w pamięci
            for future_t in range(t, time_steps):
                phi_field[future_t] = clean_harmonic
                
            if decorations["suppress_ambient_noise_horror"]:
                print(f"[t={t}] Szum otoczenia wygaszony pomyślnie. Nowa makieta załadowana.")
                
    return phi_field

if __name__ == "__main__":
    final_field_state = run_simulation()
    print("\n=== Proces skończony. Geometria pola ustabilizowana. ===")
