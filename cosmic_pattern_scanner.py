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
def fetch_gaia_data():
    """
    Pobiera dane z katalogu Gaia (przykładowe API).
    W rzeczywistości – to może być publiczny endpoint ESA lub plik CSV.
    """
    # Przykładowe dane – w rzeczywistości pobieramy z API
    url = "https://gea.esac.esa.int/archive-api/v1/query"
    payload = {
        "query": "SELECT TOP 100 source_id, ra, dec, parallax, phot_g_mean_mag FROM gaiadr3.gaia_source WHERE parallax > 10"
    }
    try:
        response = requests.get(url, params=payload, timeout=30)
        data = response.json()
        print(f"✅ Pobrano dane Gaia: {len(data)} rekordów")
        return data
    except Exception as e:
        print(f"⚠️ Błąd pobierania danych Gaia: {e}")
        # Symulacja danych na potrzeby testu
        return simulate_cosmic_data()

def simulate_cosmic_data():
    """Generuje symulowane dane kosmiczne (do testów)."""
    np.random.seed(42)
    n = 100
    return {
        "sources": [
            {
                "ra": np.random.uniform(0, 360),
                "dec": np.random.uniform(-90, 90),
                "parallax": np.random.uniform(0.1, 20),
                "phot_g_mean_mag": np.random.uniform(8, 22)
            } for _ in range(n)
        ]
    }

# ============================================================
# KROK 2 – Szukanie wzorców (Patterns)
# ============================================================
def find_patterns(data):
    """
    Szuka nietypowych struktur w danych kosmicznych.
    Używa Random Forest do wykrycia anomalii.
    """
    if not data or "sources" not in data:
        print("⚠️ Brak danych do analizy")
        return []

    # Przygotowanie danych
    features = []
    for source in data["sources"]:
        features.append([
            source.get("ra", 0),
            source.get("dec", 0),
            source.get("parallax", 0),
            source.get("phot_g_mean_mag", 0)
        ])
    
    features = np.array(features)
    
    # Normalizacja
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Trenowanie modelu do wykrywania anomalii (na podstawie reszt)
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(features_scaled, features_scaled[:, 0])  # prognozujemy pierwszą cechę
    
    # Obliczenie reszt
    predictions = model.predict(features_scaled)
    residuals = np.abs(features_scaled[:, 0] - predictions)
    
    # Znajdź anomalie (indeksy z największymi resztami)
    anomaly_indices = np.argsort(residuals)[-10:][::-1]  # top 10 anomalii
    
    patterns = []
    for idx in anomaly_indices:
        if residuals[idx] > 1.5:  # próg anomalii
            patterns.append({
                "source_index": int(idx),
                "ra": float(features[idx][0]),
                "dec": float(features[idx][1]),
                "parallax": float(features[idx][2]),
                "magnitude": float(features[idx][3]),
                "residual": float(residuals[idx]),
                "type": "kosmiczna anomalia"
            })
    
    print(f"✅ Znaleziono {len(patterns)} potencjalnych wzorców/anomalii")
    return patterns

# ============================================================
# KROK 3 – Zapis do systemu (DNA Sealer + Memory Cube)
# ============================================================
def save_patterns_to_system(patterns):
    """Zapisuje znalezione wzorce w formacie zgodnym z systemem AINUMPSA."""
    
    # Generowanie mapy pamięci
    memory_cube_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "cosmic_patterns",
        "patterns": patterns,
        "count": len(patterns)
    }
    
    # Zapis do pliku (symulacja DNA Sealer)
    with open("cosmic_patterns_log.json", "w") as f:
        json.dump(memory_cube_entry, f, indent=2)
    
    print(f"✅ Zapisano {len(patterns)} wzorców do systemu")
    
    # Przygotowanie danych dla Sześcianu Pamięci
    if patterns:
        cube_entry = {
            "room": "ROOM_[0:0:0]",  # docelowo będzie przypisany przez system
            "timestamp": datetime.now().isoformat(),
            "patterns": patterns[:3]  # pierwsze 3 wzorce jako próbka
        }
        with open("memory_cube_update.json", "w") as f:
            json.dump(cube_entry, f, indent=2)

# ============================================================
# KROK 4 – Główna pętla
# ============================================================
if __name__ == "__main__":
    print("🚀 Uruchamianie Kosmicznego Szperacza Systemowego...")
    
    # Pobierz dane
    cosmic_data = fetch_gaia_data()
    
    # Znajdź wzorce
    patterns = find_patterns(cosmic_data)
    
    # Zapisz do systemu
    save_patterns_to_system(patterns)
    
    print("✅ Kosmiczny Szperacz Systemowy zakończył pracę.")
