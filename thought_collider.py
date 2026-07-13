import json
import numpy as np
from datetime import datetime

print("=== ZDERZACZ MYŚLI: Analiza korelacji między źródłami ===")

# Wczytujemy wszystkie źródła (jeśli istnieją)
sources = {}

try:
    with open("crypto_prices.json", "r") as f:
        crypto = json.load(f)
        sources["BTC"] = [item["price"] for item in crypto.get("data", [])]
except:
    sources["BTC"] = []

try:
    with open("gold_price.json", "r") as f:
        gold = json.load(f)
        sources["Gold"] = [gold.get("price", 0)]
except:
    sources["Gold"] = []

try:
    with open("nasdaq_price.json", "r") as f:
        nasdaq = json.load(f)
        sources["Nasdaq"] = [nasdaq.get("close_price", 0)]
except:
    sources["Nasdaq"] = []

try:
    with open("unicef_raw.json", "r") as f:
        unicef = json.load(f)
        # Jeśli to błąd, nie dodawaj
        if "error" not in unicef:
            sources["UNICEF"] = [1]  # placeholder, bo dane UNICEF są złożone
        else:
            sources["UNICEF"] = []
except:
    sources["UNICEF"] = []

# Przycinamy wszystkie listy do jednakowej długości (minimum)
min_len = min([len(v) for v in sources.values() if v])
if min_len == 0:
    print("⚠️ Brak wystarczających danych do analizy.")
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "no_data",
        "message": "Nie wszystkie źródła mają dane. Sprawdź kolektory."
    }
else:
    # Tworzymy macierz korelacji
    names = list(sources.keys())
    matrix = np.zeros((len(names), len(names)))
    
    for i, name1 in enumerate(names):
        for j, name2 in enumerate(names):
            if i == j:
                matrix[i][j] = 1.0
            else:
                # Obcinamy do tej samej długości
                a = np.array(sources[name1][:min_len])
                b = np.array(sources[name2][:min_len])
                if len(a) > 1 and len(b) > 1:
                    corr = np.corrcoef(a, b)[0][1]
                    matrix[i][j] = round(corr, 3)
                else:
                    matrix[i][j] = 0.0

    # Szukamy najsilniejszych korelacji
    strong_links = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            corr = matrix[i][j]
            if abs(corr) > 0.5:
                strong_links.append({
                    "source1": names[i],
                    "source2": names[j],
                    "correlation": corr,
                    "strength": "strong" if abs(corr) > 0.7 else "moderate"
                })

    # Raport
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": "success",
        "sources": names,
        "correlation_matrix": matrix.tolist(),
        "strong_links": strong_links,
        "summary": {
            "total_sources": len(names),
            "active_sources": len([s for s in sources.values() if s]),
            "strong_correlations_found": len(strong_links)
        }
    }

    # Dodatkowo – jeśli brak danych, informacja
    if not strong_links:
        report["note"] = "Brak silnych korelacji między źródłami w tym cyklu."

# Zapis do pliku
with open("collision_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("✅ Zapisano collision_report.json")
print(f"📊 Aktywne źródła: {report.get('summary', {}).get('active_sources', 0)}")
print(f"🔗 Silne korelacje: {report.get('summary', {}).get('strong_correlations_found', 0)}")
