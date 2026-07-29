import os
import json
import math
import time

def run_hyper_version_2_14():
    print("\n[START] Inicjalizacja AINUMPSA Hyper Version 2.14 Engine...")
    
    # 1. Sprawdzanie i odczyt metadanych zebranych przez VIP Media Injector
    metadata_path = "metadata.json"
    metadata_data = {}
    
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding='utf-8') as f:
                metadata_data = json.load(f)
            print(f"[OK] Wczytano istniejące metadane z {metadata_path}")
        except Exception as e:
            print(f"[WARNING] Nie udało się odczytać metadata.json: {e}")
    else:
        print("[INFO] Brak pliku metadata.json. Hyper Engine wygeneruje własne parametry rzutu.")

    # 2. Obliczenia kwantowe matrycy (Zasada 1 > 0 & Złota Proporcja Phi)
    phi = (1 + math.sqrt(5)) / 2
    quantum_entropy = round(phi * math.pi, 6)
    timestamp_hash = hex(int(time.time() * 1000))
    
    print(f"[MATH] Wyliczony współczynnik Phi-Resonance: {phi:.5f}")
    print(f"[MATH] Entropia kwantowa matrycy: {quantum_entropy}")
    print(f"[MATH] Znacznik czasu rzutu (Matrix Time): {timestamp_hash}")

    # 3. Aktualizacja lub utworzenie raportu wyjściowego hyper_matrix_state.json
    hyper_state = {
        "engine_version": "Hyper Version 2.14",
        "principle": "1 > 0",
        "phi_factor": phi,
        "quantum_entropy": quantum_entropy,
        "matrix_timestamp": timestamp_hash,
        "linked_metadata": metadata_data,
        "status": "CALCULATED_AND_STABLE"
    }

    output_state_path = "hyper_matrix_state.json"
    try:
        with open(output_state_path, "w", encoding='utf-8') as f:
            json.dump(hyper_state, f, indent=4, ensure_ascii=False)
        print(f"[SUCCESS] Zapisano stan matrycy do pliku: {output_state_path}")
    except Exception as e:
        print(f"[ERROR] Błąd podczas zapisu stanu matrycy: {e}")

    print("[FINISHED] AINUMPSA Hyper Version 2.14 zakończył przeliczenie sukcesem.\n")

if __name__ == "__main__":
    run_hyper_version_2_14()

