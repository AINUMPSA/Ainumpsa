import asyncio
import aiohttp
import json
from datetime import datetime

class AsyncQuantumDiscoveryBot:
    def __init__(self):
        # PEŁNE ŚCIEŻKI INTERFEJSÓW API (Endpointy zwracające dane strukturalne JSON)
        self.seismic_api_url = "https://usgs.gov"
        self.weather_api_url = "https://open-meteo.com"
        self.eu_data_api_url = "https://europa.eu"
        self.cern_api_url = "https://cern.ch"
        self.nasa_api_url = "https://nasa.gov"
        self.wb_onu_api_url = "https://worldbank.org"
        self.air_quality_api_url = "https://open-meteo.com"

    async def fetch_seismic_activity(self, session, min_magnitude=4.5):
        print(f"[{datetime.now()}] -> Start: Skaner Sejsmiczny")
        params = {
            "format": "geojson",
            "starttime": datetime.utcnow().strftime("%Y-%m-%dT00:00:00"),
            "minmagnitude": min_magnitude
        }
        try:
            async with session.get(self.seismic_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("features", [])
        except Exception:
            pass
        return []

    async def fetch_weather_for_event(self, session, lat, lon):
        params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
        try:
            async with session.get(self.weather_api_url, params=params, timeout=8) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("current_weather", {})
        except:
            pass
        return {}

    async def fetch_eu_open_data(self, session, query="climate change"):
        print(f"[{datetime.now()}] -> Start: API Unii Europejskiej")
        payload = {"q": query, "rows": 2, "sort": "modified desc"}
        try:
            async with session.post(self.eu_data_api_url, json=payload, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("result", {}).get("results", [])
                    extracted = []
                    for doc in results:
                        title_dict = doc.get("title", {})
                        title = title_dict.get("en", list(title_dict.values()) if title_dict else "Bez tytułu")
                        extracted.append({
                            "title": title,
                            "publisher": doc.get("publisher", {}).get("name", "EU Institution")
                        })
                    return extracted
        except:
            pass
        return []

    async def fetch_cern_physics_data(self, session, query="higgs"):
        print(f"[{datetime.now()}] -> Start: CERN Open Data API")
        params = {"q": query, "size": 2, "sort": "-mostrecent"}
        try:
            async with session.get(self.cern_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get("hits", {}).get("hits", [])
                    extracted = []
                    for hit in hits:
                        metadata = hit.get("metadata", {})
                        extracted.append({
                            "title": metadata.get("title", "CERN Data"),
                            "experiment": metadata.get("experiment", {}).get("name", "LHC")
                        })
                    return extracted
        except:
            pass
        return []

    async def fetch_nasa_asteroids(self, session):
        print(f"[{datetime.now()}] -> Start: NASA Skaner Asteroid")
        today = datetime.utcnow().strftime("%Y-%m-%d")
        params = {"start_date": today, "end_date": today, "api_key": "DEMO_KEY"}
        try:
            async with session.get(self.nasa_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    asteroids_today = data.get("near_earth_objects", {}).get(today, [])
                    extracted = []
                    for neo in asteroids_today[:3]:
                        close_data = neo.get("close_approach_data", [{}])
                        first_approach = close_data if close_data else {}
                        extracted.append({
                            "name": neo.get("name"),
                            "potentially_hazardous": neo.get("is_potentially_hazardous_asteroid"),
                            "close_approach_distance_km": first_approach.get("miss_distance", {}).get("kilometers"),
                            "velocity_km_h": first_approach.get("relative_velocity", {}).get("kilometers_per_hour")
                        })
                    return extracted
        except:
            pass
        return []

    async def fetch_un_world_bank_data(self, session):
        print(f"[{datetime.now()}] -> Start: ONZ / Bank Światowy")
        params = {"format": "json", "per_page": 5}
        try:
            async with session.get(self.wb_onu_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    if len(data) > 1 and data:
                        latest_record = data
                        return {
                            "indicator_name": latest_record.get("indicator", {}).get("value"),
                            "global_value": latest_record.get("value"),
                            "last_updated_year": latest_record.get("date")
                        }
        except:
            pass
        return {}

    async def fetch_global_air_quality(self, session):
        print(f"[{datetime.now()}] -> Start: Globalny Skan Jakości Powietrza")
        params = {"latitude": 52.52, "longitude": 13.41, "current": "pm2_5,pm10"}
        try:
            async with session.get(self.air_quality_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("current", {})
        except:
            pass
        return {}

    async def execute_pipeline(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_seismic_activity(session),
                self.fetch_eu_open_data(session),
                self.fetch_cern_physics_data(session),
                self.fetch_nasa_asteroids(session),
                self.fetch_un_world_bank_data(session),
                self.fetch_global_air_quality(session)
            ]

            seismic_events, eu_datasets, cern_datasets, nasa_asteroids, un_data, air_quality = await asyncio.gather(*tasks)

            seismic_data = []
            weather_tasks = []
            active_events = seismic_events[:2]
            
            for event in active_events:
                coords = event.get("geometry", {}).get("coordinates",)
                lon, lat = coords, coords
                weather_tasks.append(self.fetch_weather_for_event(session, lat, lon))
            
            weather_results = await asyncio.gather(*weather_tasks)

            for i, event in enumerate(active_events):
                seismic_data.append({
                    "location": event.get("properties", {}).get("place"),
                    "magnitude": event.get("properties", {}).get("mag"),
                    "current_weather": weather_results[i] if i  Sukces! Wszystkie bazy zintegrowane w {output_filename}")
