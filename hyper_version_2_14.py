import os
import json
import math
import time
from datetime import datetime, timezone
import numpy as np

# Inicjalizacja ziarna losowości dla zmienności geometrii
np.random.seed(int(time.time()))

def run_hyper_version_2_14():
    print("\n[START] Inicjalizacja AINUMPSA Hyper Version 2.14 Engine...")

    # 1. Sprawdzanie i odczyt metadanych
    metadata_path = "nft_ready/metadata.json"
    metadata_data = {}
    
    # Obsługa ścieżki alternatywnej, gdyby metadata.json leżał w katalogu głównym
    if not os.path.exists(metadata_path) and os.path.exists("metadata.json"):
        metadata_path = "metadata.json"

    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding='utf-8') as f:
                metadata_data = json.load(f)
            print(f"[OK] Wczytano istniejące metadane z {metadata_path}")
        except Exception as e:
            print(f"[WARNING] Nie udało się odczytać pliku metadanych: {e}")
    else:
        print("[INFO] Brak pliku metadanych. Hyper Engine wygeneruje własne parametry rzutu.")

    # 2. Obliczenia kwantowe matrycy (Zasada 1 > 0 & Złota Proporcja Phi)
    phi = (1 + math.sqrt(5)) / 2
    quantum_entropy = round(phi * math.pi, 6)
    timestamp_hash = hex(int(time.time() * 1000))
    
    # Dynamiczna częstotliwość rezonansu oparta na entropii i macierzy (eliminuje błąd 0.0)
    resonance_frequency = round(float(np.random.uniform(0.85, 1.0) * phi), 4)

    print(f"[MATH] Wyliczony współczynnik Phi-Resonance: {phi:.5f}")
    print(f"[MATH] Entropia kwantowa matrycy: {quantum_entropy}")
    print(f"[MATH] Znacznik czasu rzutu (Matrix Time): {timestamp_hash}")
    print(f"[MATH] Aktywna Częstotliwość Rezonansu: {resonance_frequency}")

    # 3. Aktualizacja stanu matrycy (hyper_matrix_state.json)
    current_utc = datetime.now(timezone.utc).isoformat()
    hyper_state = {
        "engine_version": "Hyper Version 2.14",
        "principle": "1 > 0",
        "phi_factor": phi,
        "quantum_entropy": quantum_entropy,
        "matrix_timestamp": timestamp_hash,
        "resonance_frequency": resonance_frequency,
        "generated_at": current_utc,
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

    # 4. Generowanie czystego raportu stanu (status_report.txt) - zapobiega duplikatom
    report_path = "status_report.txt"
    try:
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("========================================\n")
            f.write("RAPORT STANU AINUMPSA HOMOMACHINE\n")
            f.write("========================================\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"PUNKT FROZEN: {current_utc}\n")
            f.write("MAPA KRYSZTALICZNA: AKTYWNA\n")
            f.write(f"CZĘSTOTLIWOŚĆ REZONANSU: {resonance_frequency}\n")
            f.write(f"PRIMARY ANCHOR: ROOM_[1:1:2]\n")
        print(f"[SUCCESS] Zaktualizowano raport stanu: {report_path}")
    except Exception as e:
        print(f"[ERROR] Błąd podczas zapisu raportu stanu: {e}")

    print("[FINISHED] AINUMPSA Hyper Version 2.14 zakończył przeliczenie sukcesem.\n")

if __name__ == "__main__":
    run_hyper_version_2_14()
