import requests
import json
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

print("🌌 AINUMPSA MULTIVERSE SCANNER – inicjalizacja...")

# ============================================================
# KROK 1 – Pobieranie danych: ZIEMIA / KOSMOS / MIKROŚWIAT
# ============================================================

def simulate_data(source_name):
    """Fallback w przypadku braku odpowiedzi API."""
    np.random.seed(42)
    return [
        {
            "ra": float(np.random.uniform(0, 360)),
            "dec": float(np.random.uniform(-90, 90)),
            "parallax": float(np.random.uniform(0.1, 20)),
            "phot_g_mean_mag": float(np.random.uniform(8, 22)),
            "origin": f"{source_name}_simulated"
        } for _ in range(50)
    ]

def fetch_gaia_data():
    """Źródło 1: ESA Gaia (Makro - Kosmos)"""
    url = "https://gea.esac.esa.int/archive-api/v1/query"
    payload = {
        "query": "SELECT TOP 50 source_id, ra, dec, parallax, phot_g_mean_mag FROM gaiadr3.gaia_source WHERE parallax > 10"
    }
    try:
        response = requests.get(url, params=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            sources = []
            for item in data.get("sources", []):
                item["origin"] = "ESA_GAIA"
                sources.append(item)
            print(f"✅ Pobrano dane ESA Gaia: {len(sources)} obiektów")
            return sources if sources else simulate_data("ESA_GAIA")
        return simulate_data("ESA_GAIA")
    except Exception as e:
        print(f"⚠️ ESA Gaia offline ({e}) -> Przełączam na próbkę symulowaną.")
        return simulate_data("ESA_GAIA")

def fetch_cern_data():
    """Źródło 2: CERN Open Data (Mikro - Zderzenia Cząstek)"""
    url = "https://opendata.cern.ch/record/5200/files/4mu_2011.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw_cern = response.json()
            sources = []
            for event in raw_cern[:50]:
                sources.append({
                    "ra": float(event.get("M", 0)),         # Masa niezmiennicza
                    "dec": float(event.get("pt", 0)),       # Pęd poprzeczny
                    "parallax": float(event.get("eta", 0)), # Kąt pseudorapidity
                    "phot_g_mean_mag": float(event.get("phi", 0)), # Kąt azymutalny
                    "origin": "CERN_LHC"
                })
            print(f"✅ Pobrano dane CERN LHC: {len(sources)} zdarzeń zderzeń")
            return sources
        return simulate_data("CERN_LHC")
    except Exception as e:
        print(f"⚠️ CERN Open Data offline ({e}) -> Przełączam na próbkę symulowaną.")
        return simulate_data("CERN_LHC")

# ============================================================
# KROK 2 – Szukanie wzorców we wspólnej macierzy
# ============================================================

def find_anomalies(combined_sources):
    if not combined_sources:
        return []

    features = []
    for s in combined_sources:
        features.append([
            float(s.get("ra", 0)),
            float(s.get("dec", 0)),
            float(s.get("parallax", 0)),
            float(s.get("phot_g_mean_mag", 0))
        ])
    
    features = np.array(features)
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Model uczenia maszynowego
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(features_scaled[:, 1:], features_scaled[:, 0])
    
    predictions = model.predict(features_scaled[:, 1:])
    residuals = np.abs(features_scaled[:, 0] - predictions)
    
    anomaly_indices = np.argsort(residuals)[-10:][::-1]
    
    anomalies = []
    for idx in anomaly_indices:
        item = combined_sources[idx]
        anomalies.append({
            "source": item["origin"],
            "ra": float(features[idx][0]),
            "dec": float(features[idx][1]),
            "parallax": float(features[idx][2]),
            "magnitude": float(features[idx][3]),
            "anomaly_score": float(residuals[idx]),
            "type": "multi_dimensional_anomaly"
        })
    
    print(f"✅ Znaleziono {len(anomalies)} zagęszczeń/anomalii w połączonych matrycach.")
    return anomalies

# ============================================================
# KROK 3 – Zapis do Sześcianu Pamięci (DNA Sealer)
# ============================================================

def save_to_memory(anomalies):
    memory_cube_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "seal": "1>0",
        "sources_scanned": ["ESA_GAIA", "CERN_LHC"],
        "count": len(anomalies),
        "patterns": anomalies
    }
    
    with open("cosmic_patterns_log.json", "w", encoding="utf-8") as f:
        json.dump(memory_cube_entry, f, indent=2, ensure_ascii=False)
        
    print("💾 Wyniki scalone i zapisane do cosmic_patterns_log.json [1>0]")

if __name__ == "__main__":
    # Pobranie danych ze wszystkich kraników
    data_gaia = fetch_gaia_data()
    data_cern = fetch_cern_data()
    
    # Połączenie w jeden strumień
    all_data = data_gaia + data_cern
    
    # Analiza i zapis
    found_anomalies = find_anomalies(all_data)
    save_to_memory(found_anomalies)
    
    print("✨ Skanowanie wielowymiarowe zakończone pomyślnie.")
