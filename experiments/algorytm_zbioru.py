pythonimport json
import time
import random
import math

def run_collector_probe(sample_size=5000):
    print("[SONDA ZBIERAJĄCA] Aktywacja nasłuchu na fluktuacje kwantowe...")
    
    data_points = []
    start_time = time.time()
    
    for i in range(sample_size):
        # Pobranie mikro-sekundy jako kotwicy czasowej
        current_timestamp = time.time()
        
        # Generowanie surowego bitu (0 lub 1)
        raw_bit = 1 if random.random() > 0.5 else 0
        
        # Zapis punktu danych: znacznik czasu i wylosowana wartość
        data_points.append({
            "ts": current_timestamp,
            "bit": raw_bit
        })
        
        # Ekstremalnie szybkie próbkowanie, aby uchwycić momenty skupienia wzroku
        if i % 500 == 0:
            time.sleep(0.001)
            
    end_time = time.time()
    
    # Budowanie struktury artefaktu
    artifact = {
        "metadata": {
            "experiment": "AINUMPSA_T_MATRIX",
            "samples": sample_size,
            "duration_sec": end_time - start_time
        },
        "payload": data_points
    }
    
    # Siew danych do pliku strukturalnego
    with open("collected_matrix_data.json", "w") as f:
        json.dump(artifact, f, indent=2)
        
    print(f"[SONDA ZBIERAJĄCA] Sukces. Zebrano {sample_size} bitów w pliku collected_matrix_data.json.")

if __name__ == "__main__":
    run_collector_probe()
