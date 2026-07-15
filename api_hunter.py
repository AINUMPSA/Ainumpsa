import requests
import json
from datetime import datetime

class QuantumDiscoveryBot:
    def __init__(self):
        # Definicje punktów wejścia do globalnych API
        self.seismic_api_url = "https://usgs.gov"
        self.weather_api_url = "https://open-meteo.com"
        self.eu_data_api_url = "https://europa.eu"
        # Portal CERN Open Data API do przeszukiwania rekordów fizyki wysokich energii
        self.cern_api_url = "https://cern.ch"

    def scan_seismic_activity(self, min_magnitude=4.5):
        print(f"[{datetime.now()}] [1/5] Uruchamianie skanera sejsmicznego...")
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
        params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
        try:
            response = requests.get(self.weather_api_url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("current_weather", {})
        except Exception as e:
            print(f"-> Brak danych pogodowych dla {lat},{lon}: {str(e)}")
        return None

    def scan_eu_open_data(self, query="climate change"):
        print(f"[{datetime.now()}] [2/5] Przeszukiwanie rejestrów API Unii Europejskiej...")
        payload = {"q": query, "rows": 3, "sort": "modified desc"}
        try:
            response = requests.post(self.eu_data_api_url, json=payload, timeout=15)
            if response.status_code == 200:
                results = response.json().get("result", {}).get("results", [])
                print(f"-> Znaleziono {len(results)} aktywnych unijnych zbiorów danych.")
                extracted = []
                for doc in results:
                    title_dict = doc.get("title", {})
                    title = title_dict.get("en", list(title_dict.values()) if title_dict else "Bez tytułu")
                    extracted.append({
                        "title": title,
                        "publisher": doc.get("publisher", {}).get("name", "EU Institution"),
                        "resource_url": f"https://europa.eu{doc.get('id')}?lang=en"
                    })
                return extracted
            return []
        except Exception as e:
            print(f"-> Wyjątek API UE: {str(e)}")
            return []

    def scan_cern_physics_data(self, query="higgs"):
        print(f"[{datetime.now()}] [3/5] Odpytywanie CERN Open Data API dla frazy: '{query}'...")
        params = {
            "q": query,
            "size": 3, # Pobieramy top 3 publikacje/zbiory danych z akceleratorów (np. LHC)
            "sort": "-mostrecent"
        }
        try:
            response = requests.get(self.cern_api_url, params=params, timeout=15)
            if response.status_code == 200:
                hits = response.json().get("hits", {}).get("hits", [])
                print(f"-> Wykryto {len(hits)} otwartych rekordów naukowych z CERN.")
                extracted_cern = []
                for hit in hits:
                    metadata = hit.get("metadata", {})
                    extracted_cern.append({
                        "title": metadata.get("title", "CERN Experiment Data"),
                        "creation_date": metadata.get("creation_date"),
                        "accelerator": metadata.get("accelerator", {}).get("name", "LHC"),
                        "experiment": metadata.get("experiment", {}).get("name", "Unknown"),
                        "doi_url": f"https://doi.org{metadata.get('doi')}" if metadata.get('doi') else None
                    })
                return extracted_cern
            return []
        except Exception as e:
            print(f"-> Wyjątek podczas łączenia z CERN: {str(e)}")
            return []

    def execute_pipeline(self):
        # 1. Telemetria Geofizyczna + Pogoda
        seismic_data = []
        seismic_events = self.scan_seismic_activity()
        for event in seismic_events[:2]:
            coords = event.get("geometry", {}).get("coordinates", [0, 0])
            lon, lat = coords, coords
            weather = self.auto_connect_weather_for_event(lat, lon)
            seismic_data.append({
                "location": event.get("properties", {}).get("place"),
                "magnitude": event.get("properties", {}).get("mag"),
                "current_weather": weather
            })

        # 2. Dane Unii Europejskiej
        eu_datasets = self.scan_eu_open_data()

        # 3. Dane CERN (Fizyka Kwantowa i Cząstek)
        cern_datasets = self.scan_cern_physics_data()

        # 4. Konsolidacja struktury maszynowej
        final_payload = {
            "agent_identity": "AINUMPSA Quantum Core v3.0",
            "execution_timestamp": datetime.utcnow().isoformat(),
            "telemetry_stream": {
                "geophysical_events": seismic_data,
                "european_union_open_data": eu_datasets,
                "cern_quantum_physics_data": cern_datasets
            }
        }
        return final_payload

if __name__ == "__main__":
    bot = QuantumDiscoveryBot()
    results = bot.execute_pipeline()
    
    output_filename = "quantum_scan_output.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"[{datetime.now()}] [4/5] Sukces! Zintegrowane dane zapisane w {output_filename}")
