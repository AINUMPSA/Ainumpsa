import requests
import json
from datetime import datetime

print("=== UNICEF COLLECTOR: Pobieranie danych o dzieciach i zdrowiu ===")

# UNICEF udostępnia dane w standardzie SDMX – bez klucza API
# Przykład: wskaźnik śmiertelności dzieci poniżej 5 lat (MDG_0000000011)
url = "https://sdmx.cloud.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,MDG_0000000011,1.0/all?format=json"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Zapisujemy surowe dane
    with open("unicef_raw.json", "w") as f:
        json.dump(data, f, indent=2)

    print("✅ Pobrano dane UNICEF (śmiertelność dzieci <5 lat)")
    print("✅ Zapisano do unicef_raw.json")

    # Próbujemy wyciągnąć ostatnią wartość (dla celów testowych)
    try:
        obs = data.get("data", {}).get("dataSets", [{}])[0].get("observations", {})
        if obs:
            first_key = list(obs.keys())[0]
            first_value = obs[first_key][0]
            print(f"📊 Przykładowa wartość: {first_value}")
    except Exception as e:
        print(f"⚠️ Nie udało się wyciągnąć pojedynczej wartości: {e}")

except Exception as e:
    print(f"❌ Błąd podczas pobierania danych UNICEF: {e}")
    # Zapisujemy plik z informacją o błędzie
    with open("unicef_raw.json", "w") as f:
        json.dump({"error": str(e), "timestamp": datetime.now().isoformat()}, f, indent=2)
    print("⚠️ Zapisano plik błędu jako unicef_raw.json")

print("=== ZAKOŃCZONO ===")
