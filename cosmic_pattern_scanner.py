import requests
import json
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

print("🌌 KOSMICZNY SZPERACZ SYSTEMOWY – inicjalizacja...")

# ============================================================
# KROK 1 – Pobieranie danych z kosmicznych źródeł
# ============================================================
def simulate_cosmic_data():
    """Generuje symulowane dane kosmiczne (do testów / fallback)."""
    np.random.seed(42)
    n = 100
    return {
        "sources": [
            {
                "ra": float(np.random.uniform(0, 360)),
                "dec": float(np.random.uniform(-90, 90)),
                "parallax": float(np.random.uniform(0.1, 20)),
                "phot_g_mean_mag": float(np.random.uniform(8, 22))
            } for _ in range(n)
        ]
    }

def fetch_gaia_data():
    """Pobiera dane z katalogu Gaia ESA lub włącza bezpieczny fallback."""
    url = "https://gea.esac.esa.int/archive-api/v1/query"
    payload = {
        "query": "SELECT TOP 100 source_id, ra, dec, parallax, phot_g_mean_mag FROM gaiadr3.gaia_source WHERE parallax > 10"
    }
    try:
        response = requests.get(url, params=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Pobrano dane Gaia: {len(data)} rekordów")
            return data
        else:
            print(f"⚠️ API ESA odpowiedziało kodem {response.status_code}. Uruchamiam symulację...")
            return simulate_cosmic_data()
    except Exception as e:
        print(f"⚠️ Błąd pobierania danych Gaia: {e}. Uruchamiam symulację...")
        return simulate_cosmic_data()

# ============================================================
# KROK 2 – Szukanie wzorców (Patterns)
# ============================================================
def find_patterns(data):
    """Szuka nietypowych struktur w danych kosmicznych za pomocą Random Forest."""
    if not data or "sources" not in data:
        print("⚠️ Brak danych do analizy")
        return []

    # Przygotowanie danych
    features = []
    for source in data["sources"]:
        features.append([
            float(source.get("ra", 0)),
            float(source.get("dec", 0)),
            float(source.get("parallax", 0)),
            float(source.get("phot_g_mean_mag", 0))
        ])
    
    features = np.array(features)
    
    # Normalizacja
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Trenowanie modelu do wykrywania anomalii
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(features_scaled[:, 1:], features_scaled[:, 0])  # przewidujemy ra na podstawie reszty
    
    # Obliczenie reszt
    predictions = model.predict(features_scaled[:, 1:])
    residuals = np.abs(features_scaled[:, 0] - predictions)
    
    # Indeksy z największymi resztami (top 10)
    anomaly_indices = np.argsort(residuals)[-10:][::-1]
    
    patterns = []
    for idx in anomaly_indices:
        patterns.append({
            "source_index": int(idx),
            "ra": float(features[idx][0]),
            "dec": float(features[idx][1]),
            "parallax": float(features[idx][2]),
            "magnitude": float(features[idx][3]),
            "anomaly_score": float(residuals[idx]),
            "type": "kosmiczna_anomalia"
        })
    
    print(f"✅ Znaleziono {len(patterns)} potencjalnych wzorców/anomalii")
    return patterns

# ============================================================
# KROK 3 – Zapis do systemu (DNA Sealer + Memory Cube)
# ============================================================
def save_patterns_to_system(patterns):
    """Zapisuje znalezione wzorce w formacie zgodnym z Ainumpsa."""
    
    memory_cube_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": "cosmic_patterns",
        "patterns": patterns,
        "count": len(patterns)
    }
    
    # Zapis do pliku głównego
    with open("cosmic_patterns_log.json", "w", encoding="utf-8") as f:
        json.dump(memory_cube_entry, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Zapisano {len(patterns)} wzorców do cosmic_patterns_log.json")
    
    # Przygotowanie danych dla Sześcianu Pamięci
    if patterns:
        cube_entry = {
            "room": "ROOM_[0:0:0]",
            "timestamp": datetime.utcnow().isoformat(),
            "seal": "1>0",
            "patterns": patterns[:3]  # pierwsze 3 wzorce do Sześcianu
        }
        with open("memory_cube_update.json", "w", encoding="utf-8") as f:
            json.dump(cube_entry, f, indent=2, ensure_ascii=False)
            
        print("✅ Zaktualizowano plik memory_cube_update.json z pieczęcią 1>0")

# ============================================================
# KROK 4 – Główna pętla
# ============================================================
if __name__ == "__main__":
    print("🚀 Uruchamianie Kosmicznego Szperacza Systemowego...")
    
    cosmic_data = fetch_gaia_data()
    patterns = find_patterns(cosmic_data)
    save_patterns_to_system(patterns)
    
    print("✨ Kosmiczny Szperacz Systemowy zakończył pracę z sukcesem.")
