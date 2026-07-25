import json
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

print("🎨 AINUMPSA VISUALIZER – Generowanie mapy realnych zderzeń i wiedzy...")

# 1. Pobieranie danych z wyników skanera
LOG_FILE = "cosmic_patterns_log.json"
KB_DIR = "knowledge_base"
OUTPUT_IMAGE = "cosmic_anomalies_map.png"

patterns = []

# Odczyt danych z kosmicznego skanera
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        try:
            log_data = json.load(f)
            patterns.extend(log_data.get("patterns", []))
            print(f"✅ Wczytano {len(log_data.get('patterns', []))} anomalii ze skanera.")
        except Exception as e:
            print(f"⚠️ Błąd odczytu {LOG_FILE}: {e}")

# Odczyt plików z folderu knowledge_base (jeśli istnieją)
if os.path.exists(KB_DIR):
    kb_files = glob.glob(os.path.join(KB_DIR, "*.json"))
    for file_path in kb_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                kb_data = json.load(f)
                if isinstance(kb_data, list):
                    patterns.extend(kb_data)
                elif isinstance(kb_data, dict) and "patterns" in kb_data:
                    patterns.extend(kb_data["patterns"])
            print(f"📚 Dołączono dane z bazy wiedzy: {file_path}")
        except Exception as e:
            print(f"⚠️ Nie udało się wczytać {file_path}: {e}")

# 2. Jeśli brak danych - wygeneruj przykładową siatkę zderzeń z fallbacku
if not patterns:
    print("⚠️ Brak danych – tworzenie mapy z domyślnej macierzy kolizji...")
    patterns = [
        {"ra": 45.2, "dec": 12.8, "anomaly_score": 2.1, "source": "CERN_LHC"},
        {"ra": 180.5, "dec": -45.1, "anomaly_score": 1.8, "source": "ESA_GAIA"},
        {"ra": 290.1, "dec": 60.3, "anomaly_score": 3.4, "source": "CERN_LHC"},
        {"ra": 120.0, "dec": 15.0, "anomaly_score": 2.9, "source": "ESA_GAIA"},
    ]

# 3. Tworzenie WYKRESU BIEGUNOWEGO z PRAWDZIWYMI PUNKAMI (Kolidor & Kosmos)
plt.style.use('dark_background')
fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='polar')

# Rysowanie punktów centralnego Atraktora [1>0]
ax.plot(0, 0, 'o', color='#ffe600', markersize=15, label='Atraktor Singularności [1>0]', zorder=5)

# Przetwarzanie i nanoszenie współrzędnych
for p in patterns:
    # Konwersja RA (0-360 deg) na radiany do wykresu polarnego
    ra_deg = p.get("ra", 0)
    theta = np.radians(ra_deg)
    
    # DEC lub Score jako promień (odległość od środka)
    r = np.abs(p.get("dec", p.get("anomaly_score", 1.0)))
    score = p.get("anomaly_score", 1.5)
    source = p.get("source", "UNKNOWN")
    
    # Koloryzacja w zależności od źródła zderzeń/paternu
    if "CERN" in source:
        color = '#ff0055'  # Róż/Czerwień dla zderzacza
        marker = 'x'
    elif "GAIA" in source:
        color = '#00f3ff'  # Turkus dla makro-kosmosu
        marker = 'o'
    else:
        color = '#00ff88'  # Zielony dla pól z Knowledge Base
        marker = '^'
        
    ax.scatter(theta, r, c=color, s=score * 60, alpha=0.8, marker=marker, edgecolors='white', linewidth=0.5)

# Stylizacja mapy
ax.set_title("AINUMPSA – MAPA ZDERZEŃ I PATERNÓW ANOMALII [1>0]\n(CERN LHC x ESA Gaia x Knowledge Base)", fontsize=12, pad=20, color='#ffffff')
ax.grid(True, color='#222222', linestyle='--')
ax.set_yticklabels([]) # ukrywamy surowe cyfry promienia dla czytelności

# Zapis gotowej, dynamicznej mapy punktowej
plt.savefig(OUTPUT_IMAGE, dpi=200, bbox_inches='tight')
plt.close()

print(f"✨ Nowa, dynamiczna mapa została pomyślnie wygenerowana: {OUTPUT_IMAGE}")
