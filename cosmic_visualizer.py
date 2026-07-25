import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

print("🌌 KOSMICZNY WIZUALIZATOR – generowanie mapy anomalii...")

# ============================================================
# KROK 1 – Wczytaj dane anomalii
# ============================================================
def load_anomalies():
    """Wczytuje dane z pliku cosmic_patterns_log.json."""
    try:
        with open("cosmic_patterns_log.json", "r") as f:
            data = json.load(f)
        print(f"✅ Wczytano {data.get('count', 0)} anomalii")
        return data.get("patterns", [])
    except FileNotFoundError:
        print("⚠️ Brak pliku cosmic_patterns_log.json – uruchom najpierw cosmic_pattern_scanner.py")
        return []
    except Exception as e:
        print(f"❌ Błąd wczytywania danych: {e}")
        return []

# ============================================================
# KROK 2 – Wygeneruj mapę nieba
# ============================================================
def generate_sky_map(anomalies):
    """Generuje mapę nieba z zaznaczonymi anomaliami."""
    if not anomalies:
        print("⚠️ Brak anomalii do wizualizacji")
        return

    # Przygotowanie danych
    ra = [a.get("ra", 0) for a in anomalies]
    dec = [a.get("dec", 0) for a in anomalies]
    scores = [a.get("anomaly_score", 0) for a in anomalies]

    # Tworzenie mapy nieba (projekcja Mollweide)
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection="mollweide")

    # Konwersja RA (0-360) na radiany (0-2π) z przesunięciem
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    # Normalizacja kolorów na podstawie anomaly_score
    sc = ax.scatter(ra_rad, dec_rad, c=scores, cmap="hot", s=100, alpha=0.8, edgecolors="white", linewidth=0.5)

    # Dodanie kolorbar
    cbar = plt.colorbar(sc, orientation="vertical", pad=0.05)
    cbar.set_label("Anomaly Score", fontsize=10)

    # Opisy osi
    ax.set_title("Mapa Nieba – Anomalie Kosmiczne (Gaia + CERN)", fontsize=14)
    ax.set_xlabel("RA [rad]", fontsize=10)
    ax.set_ylabel("Dec [rad]", fontsize=10)

    # Dodanie siatki
    ax.grid(True, linestyle="--", alpha=0.3)

    # Zapis do pliku
    output_file = "cosmic_anomalies_map.png"
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Zapisano mapę nieba: {output_file}")

# ============================================================
# KROK 3 – Generowanie raportu tekstowego
# ============================================================
def generate_report(anomalies):
    """Generuje krótki raport tekstowy o znalezionych anomaliach."""
    if not anomalies:
        return

    report = f"""
🌌 RAPORT KOSMICZNYCH ANOMALII
================================
Data: {datetime.now().isoformat()}
Liczba anomalii: {len(anomalies)}
Najwyższy wynik anomalii: {max([a.get('anomaly_score', 0) for a in anomalies]):.3f}
Średni wynik anomalii: {np.mean([a.get('anomaly_score', 0) for a in anomalies]):.3f}

Top 3 anomalie:
"""
    sorted_anomalies = sorted(anomalies, key=lambda x: x.get("anomaly_score", 0), reverse=True)
    for i, a in enumerate(sorted_anomalies[:3]):
        report += f"  {i+1}. RA: {a.get('ra', 0):.2f}, Dec: {a.get('dec', 0):.2f}, Score: {a.get('anomaly_score', 0):.3f}\n"

    with open("cosmic_anomalies_report.txt", "w") as f:
        f.write(report)
    print("✅ Zapisano raport tekstowy: cosmic_anomalies_report.txt")

# ============================================================
# KROK 4 – Główna pętla
# ============================================================
if __name__ == "__main__":
    # Wczytaj anomalie
    anomalies = load_anomalies()

    if anomalies:
        # Generuj mapę nieba
        generate_sky_map(anomalies)
        # Generuj raport tekstowy
        generate_report(anomalies)
        print("✅ Kosmiczny Wizualizator zakończył pracę.")
    else:
        print("⚠️ Brak danych – zakończono.")
