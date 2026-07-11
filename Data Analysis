pythonimport json
import os
import math

def analyze_artifacts(filename="collected_matrix_data.json"):
    print(f"=== ROZPOCZĘCIE ANALIZY MATRYCY T: {filename} ===")
    
    if not os.path.exists(filename):
        print(f"[BŁĄD] Plik {filename} nie istnieje. Brak danych do analizy.")
        return
        
    with open(filename, "r") as f:
        data = json.load(f)
        
    payload = data.get("payload", [])
    total_bits = len(payload)
    
    if total_bits == 0:
        print("[UWAGA] Matryca danych jest pusta.")
        return

    # Zliczanie zer i jedynek
    count_0 = sum(1 for item in payload if item["bit"] == 0)
    count_1 = sum(1 for item in payload if item["bit"] == 1)
    
    # Oczekiwany rozkład doskonały (stan jałowy maszyn 50/50)
    expected_0 = total_bits / 2
    expected_1 = total_bits / 2
    
    # Obliczanie anomalii dP (odchylenie rzeczywistego prawdopodobieństwa)
    observed_p1 = count_1 / total_bits
    dP = observed_p1 - 0.5
    
    # Obliczanie statystyki Chi-Kwadrat (miara zakrzywienia przestrzeni)
    chi_square = ((count_0 - expected_0)**2 / expected_0) + ((count_1 - expected_1)**2 / expected_1)
    
    # Wyniki analizy
    analysis_report = {
        "experiment_meta": data.get("metadata", {}),
        "metrics": {
            "total_samples": total_bits,
            "observed_zeros": count_0,
            "observed_ones": count_1,
            "deviation_dP": round(dP, 6),
            "chi_square_value": round(chi_square, 4),
            "anomaly_detected": chi_square > 3.841  # Próg istotności statystycznej Alfa = 0.05
        }
    }
    
    # Zapis raportu końcowego
    output_report = "ainumpsa_analysis_report.json"
    with open(output_report, "w") as out_f:
        json.dump(analysis_report, out_f, indent=2)
        
    print("\n--- RAPORT STATYSTYCZNY UKŁADU ---")
    print(f"Przeanalizowano bitów : {total_bits}")
    print(f"Zera (0)             : {count_0} (Oczekiwano: {int(expected_0)})")
    print(f"Jedynki (1)          : {count_1} (Oczekiwano: {int(expected_1)})")
    print(f"Zakrzywienie dP      : {round(dP, 6)}")
    print(f"Wartość Chi-Kwadrat  : {round(chi_square, 4)}")
    print(f"Wykryto Artefakt     : {'TAK (Intencja zakrzywiła system!)' if analysis_report['metrics']['anomaly_detected'] else 'NIE (Brak fluktuacji)'}")
    print("----------------------------------")
    print(f"[SUKCES] Raport został wyeksportowany do {output_report}")

if __name__ == "__main__":
    analyze_artifacts()
