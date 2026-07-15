import requests
import json
from datetime import datetime

class QuantumDiscoveryBot:
    def __init__(self):
        # Znane, stabilne punkty wejścia do globalnych API
        self.seismic_api_url = "https://usgs.gov"
        self.weather_api_url = "https://open-meteo.com"
        # API wyszukiwarki portalu Otwartych Danych Unii Europejskiej (data.europa.eu)
        self.eu_data_api_url = "https://europa.eu"

    def scan_seismic_activity(self, min_magnitude=4.5):
        print(f"[{datetime.now()}] [1/3] Uruchamianie skanera sejsmicznego...")
        params = {
            "format": "geojson",
            "starttime": datetime.utcnow().strftime("%Y-%m-%dT00:00:00"),
            "minmagnitude": min_magnitude
        }
        try:
            response = requests.get(self.seismic_api_url, params=params, timeout=15)
            if response.status_code == 200:
                events = response.json().get("features", [])
                print(f"-> Wykryto {len(events)} anomalii sejsmicznych.")
                return events
            return []
        except Exception as e:
            print(f"-> Awaria połączenia sejsmicznego: {str(e)}")
            return []

    def auto_connect_weather_for_event(self, lat, lon):
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }
        try:
            response = requests.get(self.weather_api_url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("current_weather", {})
        except Exception as e:
            print(f"-> Nie skorelowano danych pogodowych dla {lat},{lon}: {str(e)}")
        return None

    def scan_eu_open_data(self, query="climate change"):
        print(f"[{datetime.now()}] [2/3] Przeszukiwanie rejestrów API Unii Europejskiej dla frazy: '{query}'...")
        # Struktura zapytania dla unijnego API CKAN/Search Hub
        payload = {
            "q": query,
            "rows": 5, # Pobieramy top 5 najnowszych baz danych
            "sort": "modified desc" # Sortowanie od ostatnio zmodyfikowanych
        }
        try:
            response = requests.post(self.eu_data_api_url, json=payload, timeout=15)
            if response.status_code == 200:
                results = response.json().get("result", {}).get("results", [])
                print(f"-> Znaleziono {len(results)} aktywnych unijnych zbiorów danych.")
                
                extracted_datasets = []
                for doc in results:
                    title_dict = doc.get("title", {})
                    # Szukamy angielskiego lub jakiegokolwiek dostępnego tytułu
                    title = title_dict.get("en", list(title_dict.values())[0] if title_dict else "Bez tytułu")
                    
                    extracted_datasets.append({
                        "title": title,
                        "id": doc.get("id"),
                        "publisher": doc.get("publisher", {}).get("name", "EU Institution"),
                        "modification_date": doc.get("modified"),
                        "resource_url": f"https://europa.eu{doc.get('id')}?lang=en"
                    })
                return extracted_datasets
            else:
                print(f"-> Błąd API UE: Status {response.status_code}")
                return []
        except Exception as e:
            print(f"-> Wyjątek podczas łączenia z API UE: {str(e)}")
            return []

    def execute_pipeline(self):
        # 1. Zbieranie telemetrii geofizycznej i pogodowej
        seismic_data = []
        seismic_events = self.scan_seismic_activity()
        for event in seismic_events[:3]: # Ograniczamy do 3 na mobilny test
            geometry = event.get("geometry", {})
            coords = geometry.get("coordinates", [0, 0])
            lon, lat = coords[0], coords[1]
            
            weather = self.auto_connect_weather_for_event(lat, lon)
            seismic_data.append({
                "location": event.get("properties", {}).get("place"),
                "magnitude": event.get("properties", {}).get("mag"),
                "coordinates": {"lat": lat, "lon": lon},
                "current_weather": weather
            })

        # 2. Zbieranie danych z Unii Europejskiej
        eu_datasets = self.scan_eu_open_data()

        # 3. Konsolidacja w strukturę maszynową AINUMPSA
        final_payload = {
            "agent_identity": "AINUMPSA Quantum Core",
            "execution_timestamp": datetime.utcnow().isoformat(),
            "telemetry_stream": {
                "geophysical_events": seismic_data,
                "european_union_open_data": eu_datasets
            }
        }
        return final_payload

if __name__ == "__main__":
    bot = QuantumDiscoveryBot()
    results = bot.execute_pipeline()
    
    # Zrzucamy skonsolidowane dane do pliku wyjściowego
    output_filename = "quantum_scan_output.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"[{datetime.now()}] [3/3] Sukces! Dane zintegrowane w {output_filename}")
