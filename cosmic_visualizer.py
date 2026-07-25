import json
import os
import matplotlib.pyplot as plt

print("🎨 KOSMICZNY WIZUALIZATOR – generowanie mapy anomalii...")

LOG_FILE = "cosmic_patterns_log.json"
OUTPUT_IMAGE = "cosmic_anomalies_map.png"

def generate_map():
    if not os.path.exists(LOG_FILE):
        print(f"⚠️ Brak pliku {LOG_FILE}. Wizualizacja pominięta.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    patterns = data.get("patterns", [])
    if not patterns:
        print("⚠️ Brak anomalii do wykreślenia.")
        return

    # Przygotowanie danych do wykresu
    ra_gaia, dec_gaia = [], []
    ra_cern, dec_cern = [], []

    for p in patterns:
        source = p.get("source", "")
        ra = p.get("ra", 0)
        dec = p.get("dec", 0)
        
        if "GAIA" in source:
            ra_gaia.append(ra)
            dec_gaia.append(dec)
        else:
            ra_cern.append(ra)
            dec_cern.append(dec)

    # Tworzenie ciemnego, kosmicznego wykresu
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Naniesienie punktów z ESA Gaia i CERN LHC
    if ra_gaia:
        ax.scatter(ra_gaia, dec_gaia, c='#00f3ff', s=120, label='ESA Gaia (Kosmos)', alpha=0.8, edgecolors='white')
    if ra_cern:
        ax.scatter(ra_cern, dec_cern, c='#ff0055', s=120, label='CERN LHC (Mikro)', alpha=0.8, edgecolors='white')

    # Stylizacja i opis mapy
    ax.set_title("AINUMPSA – MAPA ANOMALII WIELOWYMIAROWYCH [1>0]", fontsize=14, pad=15, color='#ffffff')
    ax.set_xlabel("Współrzędna RA / Masa [M]", fontsize=10)
    ax.set_ylabel("Współrzędna DEC / Pęd [pt]", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')

    # Zapis pliku PNG
    plt.savefig(OUTPUT_IMAGE, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✅ Wygenerowano obraz mapy: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    generate_map()
