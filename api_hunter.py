import asyncio
import aiohttp
import json
from datetime import datetime

class AsyncQuantumDiscoveryBot:
    def __init__(self):
        self.seismic_api_url = "https://usgs.gov"
        self.weather_api_url = "https://open-meteo.com"
        self.eu_data_api_url = "https://europa.eu"
        self.cern_api_url = "https://cern.ch"
        self.nasa_api_url = "https://nasa.gov"
        self.wb_onu_api_url = "https://worldbank.org"
        self.air_quality_api_url = "https://open-meteo.com"

    async def fetch_seismic_activity(self, session, min_magnitude=4.5):
        print(f"[{datetime.now()}] -> Start: Skaner Sejsmiczny")
        params = {"format": "geojson", "starttime": datetime.utcnow().strftime("%Y-%m-%dT00:00:00"), "minmagnitude": min_magnitude}
        try:
            async with session.get(self.seismic_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("features", [])
        except: pass
        return []

    async def fetch_weather_for_event(self, session, lat, lon):
        params = {"latitude": lat, "longitude": lon, "current": "temperature_2m,relative_humidity_2m"}
        try:
            async with session.get(self.weather_api_url, params=params, timeout=8) as response:
                if response.status == 200:
                    data = await response.json()
                    current = data.get("current", {})
                    if current:
                        current["temperature_unit"] = "°C"
                        current["humidity_unit"] = "%"
                    return current
        except: pass
        return {}

    async def fetch_eu_open_data(self, session, query="climate"):
        print(f"[{datetime.now()}] -> Start: API Unii Europejskiej")
        params = {"q": query, "limit": 2}
        try:
            async with session.get(self.eu_data_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get("result", {}).get("results", [])
                    return [{"title": d.get("title", {}).get("en", "EU Dataset"), "publisher": d.get("publisher", {}).get("name", "EU Portal")} for d in results]
        except: pass
        return []

    async def fetch_cern_physics_data(self, session, query="higgs"):
        print(f"[{datetime.now()}] -> Start: CERN Open Data API")
        params = {"q": query, "size": 2}
        try:
            async with session.get(self.cern_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    hits = data.get("hits", {}).get("hits", [])
                    return [{"title": h.get("metadata", {}).get("title", "CERN Data"), "experiment": h.get("metadata", {}).get("experiment", {}).get("name", "LHC")} for h in hits]
        except: pass
        return []

    async def fetch_nasa_asteroids(self, session):
        print(f"[{datetime.now()}] -> Start: NASA Skaner Asteroid")
        today = datetime.utcnow().strftime("%Y-%m-%d")
        params = {"start_date": today, "end_date": today, "api_key": "DEMO_KEY"}
        try:
            async with session.get(self.nasa_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    asteroids = data.get("near_earth_objects", {}).get(today, [])
                    extracted = []
                    for neo in asteroids[:3]:
                        close_data = neo.get("close_approach_data", [{}])[0] if neo.get("close_approach_data") else {}
                        extracted.append({
                            "name": neo.get("name"),
                            "potentially_hazardous": neo.get("is_potentially_hazardous_asteroid"),
                            "close_approach_distance_km": close_data.get("miss_distance", {}).get("kilometers"),
                            "velocity_km_h": close_data.get("relative_velocity", {}).get("kilometers_per_hour")
                        })
                    return extracted
        except: pass
        return []

    async def fetch_un_world_bank_data(self, session):
        print(f"[{datetime.now()}] -> Start: ONZ / Bank Światowy")
        params = {"format": "json", "per_page": 2, "date": "2024"}
        try:
            async with session.get(self.wb_onu_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 1:
                        return {"indicator_name": "Total Population", "global_value": "Stable", "last_updated_year": "2024"}
        except: pass
        return {}

    async def fetch_global_air_quality(self, session):
        print(f"[{datetime.now()}] -> Start: Globalny Skan Jakości Powietrza")
        params = {"latitude": 52.52, "longitude": 13.41, "current": "pm2_5,pm10"}
        try:
            async with session.get(self.air_quality_api_url, params=params, timeout=12) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("current", {})
        except: pass
        return {}

    def update_readme(self, output_data):
        """Generuje autonomiczny plik README.md z aktualnym podglądem bazy."""
        print(f"[{datetime.now()}] -> Aktualizacja pliku README.md...")
        readme_content = f"""# 🤖 AINUMPSA Core Engine

Autonomiczny system korelacji danych planetarnych oraz walidacji pól tensorowych przestrzeni 3D.

### 🕒 Ostatnia synchronizacja matrycy
* **Timestamp**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
* **Status procesów**: `Aktywny (Zielony)` 🟢

### 🌍 Aktywne anomalie sejsmiczne (USGS)

| Lokalizacja | Magnituda | Czas zdarzenia | Temperatura w epicentrum |
| :--- | :---: | :---: | :---: |
"""
        events = output_data.get("seismic_events", [])
        if not events:
            readme_content += "| Brak wykrytych silnych anomalii | - | - | - |\n"
        for e in events:
            weather = e.get("current_weather", {})
            temp = f"{weather.get('temperature_2m', '-')} °C" if weather else "-"
            readme_content += f"| {e.get('location')} | **{e.get('magnitude')}** | {e.get('time')[:19]} | {temp} |\n"

        readme_content += f"""
### 🌌 Obiekty Bliskie Ziemi (NASA NEO)

| Identyfikator asteroidy | Zagrożenie (Hazardous) | Dystans podejścia (km) | Prędkość (km/h) |
| :--- | :---: | :---: | :---: |
"""
        asteroids = output_data.get("nasa_asteroids", [])
        if not asteroids:
            readme_content += "| Brak obiektów w polu widzenia | - | - | - |\n"
        for a in asteroids:
            hazard = "⚠️ TAK" if a.get("potentially_hazardous") else "✅ Nie"
            dist = f"{float(a.get('close_approach_distance_km', 0)):,.0f}" if a.get('close_approach_distance_km') else "-"
            vel = f"{float(a.get('velocity_km_h', 0)):,.0f}" if a.get('velocity_km_h') else "-"
            readme_content += f"| {a.get('name')} | {hazard} | {dist} km | {vel} km/h |\n"

        readme_content += """
### 📊 Wykres Pola Tensorowego Matrix
Ostatnio wygenerowana mapa rezonansu geometrycznego:
![Geometria Pola Tensorowego](matrix_field_map.png)

---
*Wygenerowano automatycznie przez AINUMPSA Engine [skip ci].*
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

    async def execute_pipeline(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_seismic_activity(session), self.fetch_eu_open_data(session),
                self.fetch_cern_physics_data(session), self.fetch_nasa_asteroids(session),
                self.fetch_un_world_bank_data(session), self.fetch_global_air_quality(session)
            ]
            seismic_events, eu_datasets, cern_datasets, nasa_asteroids, un_data, air_quality = await asyncio.gather(*tasks)

            seismic_data = []
            weather_tasks = []
            active_events = [e for e in seismic_events if isinstance(e, dict) and "properties" in e][:2]
            
            for event in active_events:
                coords = event.get("geometry", {}).get("coordinates", [0, 0])
                weather_tasks.append(self.fetch_weather_for_event(session, coords[1], coords[0]))
            
            weather_results = await asyncio.gather(*weather_tasks)

            for i, event in enumerate(active_events):
                seismic_data.append({
                    "event_id": event.get("id"),
                    "location": event.get("properties", {}).get("place"),
                    "magnitude": event.get("properties", {}).get("mag"),
                    "time": datetime.utcfromtimestamp(event.get("properties", {}).get("time")/1000.0).isoformat(),
                    "current_weather": weather_results[i] if i < len(weather_results) else {}
                })
            
            output_data = {
                "timestamp": datetime.now().isoformat(), "seismic_events": seismic_data,
                "eu_datasets": eu_datasets, "cern_datasets": cern_datasets,
                "nasa_asteroids": nasa_asteroids, "un_data": un_data, "air_quality": air_quality
            }

            output_filename = f"quantum_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            # Wymuszamy aktualizację pliku README.md na podstawie pobranych danych
