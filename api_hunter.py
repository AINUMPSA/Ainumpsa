import requests
import json
from datetime import datetime

class QuantumDiscoveryBot:
    def __init__(self):
        self.seismic_api_url = "https://usgs.gov"
        self.weather_api_url = "https://open-meteo.com"

    def scan_seismic_activity(self, min_magnitude=4.5):
        print(f"[{datetime.now()}] Uruchamianie skanera sejsmicznego (Mag > {min_magnitude})...")
        params = {
            "format": "geojson",
            "starttime": datetime.utcnow().strftime("%Y-%m-%dT00:00:00"), # Skan od początku dzisiejszego dnia
            "minmagnitude": min_magnitude
        }
        try:
            response = requests.get(self.seismic_api_url, params=params, timeout=10)
            if response.status_code == 200:
                events = response.json().get("features", [])
                print(f"Wykryto {len(events)} anomalii sejsmicznych.")
                return events
            return []
        except Exception as e:
            print(f"Awaria połączenia sejsmicznego: {str(e)}")
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
            print(f"Nie skorelowano danych pogodowych: {str(e)}")
        return None

    def execute_pipeline(self):
        discovered_data = []
        seismic_events = self.scan_seismic_activity()
        
        for event in seismic_events[:5]: # Na start bierzemy maksymalnie 5 najnowszych zdarzeń
            properties = event.get("properties", {})
            geometry = event.get("geometry", {})
            coords = geometry.get("coordinates", [0, 0, 0])
            
            lon, lat = coords[0], coords[1]
            place = properties.get("place", "Nieznana lokalizacja")
            mag = properties.get("mag", 0.0)
            
            weather = self.auto_connect_weather_for_event(lat, lon)
            
            payload = {
                "source": "USGS + Open-Meteo Automatic Core",
                "location": place,
                "coordinates": {"lat": lat, "lon": lon},
                "magnitude": mag,
                "local_weather_at_incident": weather,
                "timestamp": datetime.utcnow().isoformat()
            }
            discovered_data.append(payload)
        return discovered_data

if __name__ == "__main__":
    bot = QuantumDiscoveryBot()
    results = bot.execute_pipeline()
    with open("quantum_scan_output.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Skanowanie zakończone. Dane zapisane w pliku.")
