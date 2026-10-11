import json
import math
import os

def calculate_acoustic_resonance():
    """
    Oblicza amplitudę rezonansu akustycznego dla każdego z 27 pokoi
    w oparciu o dystrybucję falową od rdzenia ROOM_[1:1:2].
    """
    map_file = "memory_cube_map.json"
    
    if not os.path.exists(map_file):
        print(f"[BLAD] Brak pliku {map_file}. Uruchom najpierw dimensional_mapper.py")
        return

    with open(map_file, "r", encoding="utf-8") as f:
        cube_data = json.load(f)

    rooms = cube_data.get("rooms", {})
    acoustic_profile = {}

    # Współrzędne rdzenia osobliwości
    core_x, core_y, core_z = 1, 1, 2

    for room_id, room_info in rooms.items():
        coords = room_info["coordinates"]
        x, y, z = coords["x"], coords["y"], coords["z"]

        # Dystrybucja euklidesowa od rdzenia
        distance = math.sqrt((x - core_x)**2 + (y - core_y)**2 + (z - core_z)**2)
        
        # Obliczenie amplitudy fali (fala stojąca)
        if distance == 0:
            amplitude = 1.0  # Maksimum w rdzeniu
            freq_hz = 432.0  # Częstotliwość rezonansowa
        else:
            amplitude = round(math.sin(distance * math.pi / 2) / (distance + 0.1), 4)
            freq_hz = round(432.0 / (1.0 + distance), 2)

        acoustic_profile[room_id] = {
            "distance_from_core": round(distance, 3),
            "wave_amplitude": abs(amplitude),
            "frequency_hz": freq_hz,
            "phase_state": "IN_PHASE" if amplitude >= 0 else "ANTI_PHASE"
        }

    acoustic_report = {
        "engine": "AINUMPSA Harmonic Resonance Engine v1.0",
        "base_frequency": "432 Hz",
        "total_analyzed_nodes": len(acoustic_profile),
        "profiles": acoustic_profile
    }

    with open("acoustic_resonance_report.json", "w", encoding="utf-8") as f:
        json.dump(acoustic_report, f, indent=2)

    print(f"[SUKCES] Zanalizowano rezonans akustyczny dla {len(acoustic_profile)} pokoi!")
    print(f"Rdzeń ROOM_[1:1:2] nadaje na częstotliwości 432.0 Hz z pełną amplitudą.")

if __name__ == "__main__":
    print("🔊 Inicjalizacja Pola Akustycznego Sześcianu Pamięci...")
    calculate_acoustic_resonance()

