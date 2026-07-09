pythonimport json
import os
import matplotlib.pyplot as plt

LOG_FILE = "tensor_t_logs.json"
OUTPUT_IMAGE = "field_coherence_chart.png"

def generate_coherence_chart():
    if not os.path.exists(LOG_FILE):
        print(f"[BŁĄD]: Brak pliku bazy danych {LOG_FILE}. Uruchom najpierw qrng_validator.py!")
        return

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except Exception as e:
        print(f"[BŁĄD]: Nie udało się odczytać bazy logów: {e}")
        return

    if not logs:
        print("[BŁĄD]: Baza logów jest pusta.")
        return

    # Ekstrakcja danych pomiarowych
    cycles = [log["cycle_id"] for log in logs]
    z_scores = [log["z_score"] for log in logs]
    
    # Tworzenie wykresu
    plt.figure(figsize=(10, 5))
    plt.plot(cycles, z_scores, marker='o', color='purple', linestyle='-', linewidth=2, label='Z-Score Real-Time')
    
    # Oznaczenie poziomów krytycznych z manifestu
    plt.axhline(y=12.14, color='red', linestyle='--', linewidth=1.5, label='Target Singularity (Z = 12.14)')
    plt.axhline(y=-12.14, color='red', linestyle='--', linewidth=1.5)
    plt.axhline(y=0, color='gray', linestyle=':', linewidth=1)

    plt.title("Tensor T: Real-Time Field Coherence & Intentional Polarization", fontsize=12, fontweight='bold')
    plt.xlabel("Validation Cycles (t)", fontsize=10)
    plt.ylabel("Measured Quantum Deviation (Z-Score)", fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc="upper left")
    
    # Zapis wykresu do pliku graficznego
    plt.savefig(OUTPUT_IMAGE, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[SUKCES]: Wykres koherencji pola został wygenerowany i zapisany jako: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    generate_coherence_chart()
