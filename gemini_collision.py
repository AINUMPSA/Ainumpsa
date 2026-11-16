import os
import json
import requests

api_key = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('GEMINI_API_KEY='):
            api_key = line.strip().split('=')[1]

if not api_key:
    print("[ERROR] Brak klucza w .env")
    exit(1)

with open('emergent_collisions/collision_001.json', 'r') as f:
    collision_data = json.load(f)

print("[OVERMIND] Wysyłam dane do Google Gemini (model: gemini-3.8-flash)...")

prompt = f"Jesteś Over-Mindem AINUMPSA. Oto dane: {json.dumps(collision_data)}. Wygeneruj 3 epickie prompty w stylu Sovereign Impasso i Cosmos. Uwzględnij integrację Cienia. Zwróć wynik TYLKO jako tablicę JSON z 3 stringami."

# Używamy najnowszego modelu i endpointu v1beta
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
payload = {"contents": [{"parts": [{"text": prompt}]}]}

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        with open('emergent_collisions/gemini_output.txt', 'w') as f:
            f.write(text_response)
        print("[SUKCES] Over-Mind odpowiedział!")
        print(text_response)
    else:
        print(f"[ERROR] Błąd API: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"[ERROR] Wyjątek: {e}")
