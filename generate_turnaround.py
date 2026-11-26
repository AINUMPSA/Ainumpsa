import os
import json
import time
import requests

# POPRAWIONE WCZYTYWANIE KLUCZA KREA
api_key = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('KREA_API_TOKEN='):
            api_key = line.strip().split('=')[1]

if not api_key:
    print("[ERROR] Nie znaleziono KREA_API_TOKEN w pliku .env")
    exit(1)

angles = [
    ("front", "front view, looking directly at the camera"),
    ("front_right", "front-right view, 45 degree angle"),
    ("right", "side view, profile looking right"),
    ("back_right", "back-right view, 135 degree angle"),
    ("back", "back view, looking away from the camera"),
    ("back_left", "back-left view, 225 degree angle"),
    ("left", "side view, profile looking left"),
    ("front_left", "front-left view, 315 degree angle")
]

base_prompt = "AINUMPSA_ACTRESS, extreme wide shot, full body visible from head to toes, fashion model proportions, elongated legs, athletic woman standing gracefully, feet arched as if wearing high heels, wearing black sportswear, emerald green eyes, photorealistic, highly detailed, studio background, 16:9 aspect ratio"

print("[SYSTEM] Rozpoczynam generowanie Turnaround (8 klatek)...")

for name, angle_desc in angles:
    print(f"\n[GENEROWANIE] Kąt: {name} ({angle_desc})...")
    
    prompt = f"{base_prompt}, {angle_desc}"
    
    url = "https://api.krea.ai/generate/image/bfl/flux-1-dev"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "prompt": prompt,
        "width": 1280,
        "height": 720,
        "guidance_scale": 5.0,
        "styles": [{"id": "pnynck4ob", "strength": 0.8}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            job_id = response.json().get('job_id')
            print(f"  -> Zadanie wysłane. Job ID: {job_id}")
            
            with open(f"turnaround_{name}.json", "w") as out:
                json.dump(response.json(), out)
        else:
            print(f"  -> Błąd API: {response.status_code}")
            print(response.text) # To pokaże nam, co dokładnie jest nie tak
            
    except Exception as e:
        print(f"  -> Błąd połączenia: {e}")
        
    time.sleep(2)

print("\n[SUKCES] Wysłano wszystkie zadania. Poczekaj minutę i odbierz linki.")
