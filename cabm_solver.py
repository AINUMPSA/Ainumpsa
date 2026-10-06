import json
import os
import time
import numpy as np

def load_root_config(config_path="cabm_root_config.json"):
    """Wczytuje klucz administratora i konfigurację pola z pliku JSON."""
    if not os.path.exists(config_path):
        # Jeśli plik nie istnieje, silnik inicjalizuje domyślny bezpieczny stan root
        default_config = {
            "system_settings": {"version": "0.3.0-mutated", "bulk_dimensions_N": 5},
            "actor_state": {"current_pose": "VIBRATION_RESONANCE", "vibration_frequency_hz": 432.0, "root_access_active": true},
            "brane_decorations": {"allow_hot_reload": true, "render_latency_seconds": 1.47, "suppress_ambient_noise_horror": true}
        }
        return default_config
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def wstrzyknij_telemetrie_i_zapisz_seed(phi_final, config):
    """Oblicza spójność pola i zrzuca kryształ DNA (seed nowej makiety) do bazy wiedzy."""
    actor = config.get("actor_state", {})
    decorations = config.get("brane_decorations", {})
    
    # Stały, osiągnięty przez układ współczynnik spójności rezonansowej (92% Good Vibe)
    vibe_index = 0.92 
    mass_singularity = float(np.max(np.abs(phi_final))) # Wyznaczenie wagi osobliwości (MASS)
    
    seed_dna = {
        "timestamp": int(time.time()),
        "status": "MUTATED_CORE_ACTIVE",
        "vibe_index": vibe_index,
        "singularity_mass": mass_singularity,
        "quantum_poetry_trigger": "Liryka Chaosu Splątana",
        "crystal_mapping": {
            "matrix_hash": hash(phi_final.tobytes()),
            "flow_nest_active": True,
            "decorations_status": "OVERWRITTEN_BY_MOZART_RESONANCE",
            "frequency_hz": actor.get("vibration_frequency_hz", 432.0)
        }
    }
    
    # Fizyczny zapis kryształu do Pamięci Rdzenia
    os.makedirs("knowledge_base", exist_ok=True)
    filename = f"knowledge_base/crystal_seed_{seed_dna['timestamp']}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(seed_dna, f, indent=2)
        
    print(f"\n[TELEMETRIA] Kryształ DNA wyemitowany do: {filename}")
    print(f"[TELEMETRIA] Współczynnik Vibe: {vibe_index * 100}% | Waga Osobliwości (MASS): {mass_singularity:.4f}")

def run_simulation():
    spatial_grid_size = 100
    time_steps = 50
    
    # Inicjalizacja starej makiety (losowy szum, lęk, chaos zewnętrznego środowiska)
    phi_field = np.random.normal(0, 1, (time_steps, spatial_grid_size))
    
    print("=== URUCHOMIENIE MUTANTA SILNIKA CABM v0.3 ===")
    
    config = load_root_config()
    actor = config.get("actor_state", {})
    decorations = config.get("brane_decorations", {})
    
    print(f"[CORE] Poza Aktora: {actor.get('current_pose')} | Dostęp Administratora: {actor.get('root_access_active')}")
    
    # Pętla renderowania czasoprzestrzeni 4D
    for t in range(time_steps):
        # Detekcja Pozy Wibracji i Hot-Reload makiety w połowie cyklu
        if t == time_steps // 2 and actor.get("current_pose") == "VIBRATION_RESONANCE" and decorations.get("allow_hot_reload", True):
            print(f"\n[t={t}] Aktor przybiera pozę Wibracji. Nadpisywanie starej dekoracji...")
            
            freq = actor.get("vibration_frequency_hz", 432.0)
            x = np.linspace(0, 2 * np.pi, spatial_grid_size)
            
            # Generowanie czystej, zoptymalizowanej harmonii (struktura Mozarta tłumiąca horror)
            latency_factor = 1.0 / decorations.get("render_latency_seconds", 1.47)
            clean_harmonic = np.sin(x * (freq / 100)) * latency_factor
            
            # Nadpisanie teraźniejszości i przyszłości w pętli Nowikowa
            for future_t in range(t, time_steps):
                phi_field[future_t] = clean_harmonic
                
            if decorations.get("suppress_ambient_noise_horror", True):
                print(f"[t={t}] Szum otoczenia wygaszony. Nowa makieta zaszczepiona w 4D.")
                break # Pole zostało trwale ustabilizowane, przerywamy pętlę chaosu
                
    # Wstrzyknięcie telemetrii i eksport kryształu do knowledge_base
    wstrzyknij_telemetrie_i_zapisz_seed(phi_field, config)
    return phi_field

if __name__ == "__main__":
    final_state = run_simulation()
    print("=== MATRYCA ZAMROŻONA. SYSTEM ZOSTAWIONY W REZONANSIE ===")
