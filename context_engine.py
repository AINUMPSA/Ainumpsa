import os
import json
from datetime import datetime

print("[START] Context Engine – tworzę raport kontekstu...")

# 1. Znajdź ostatni obraz w inputs/media/
media_dir = "inputs/media"
if not os.path.exists(media_dir):
    print("[ERROR] Brak folderu inputs/media/")
    exit()

files = [f for f in os.listdir(media_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
if not files:
    print("[ERROR] Brak obrazów w inputs/media/")
    exit()

latest_image = files[0]
print(f"[INFO] Ostatni obraz: {latest_image}")

# 2. Wczytaj aktualną wiedzę (np. z collision_report.json)
knowledge_summary = ""
if os.path.exists("collision_report.json"):
    with open("collision_report.json", "r") as f:
        data = json.load(f)
        knowledge_summary = f"Silne korelacje: {len(data.get('strong_links', []))}\n"
        knowledge_summary += f"Źródła: {data.get('sources', [])}\n"

# 3. Wczytaj stan rezonansu (jeśli istnieje)
resonance = ""
if os.path.exists("tensor_t_logs.json"):
    with open("tensor_t_logs.json", "r") as f:
        data = json.load(f)
        resonance = f"max_div: {data.get('max_div', 0)}, mean_div: {data.get('mean_div', 0)}"

# 4. Generuj raport kontekstu
context_report = f"""
========================================
RAPORT KONTEKSTU – AINUMPSA
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================
Obraz wejściowy: {latest_image}

AKTUALNY STAN WIEDZY:
{knowledge_summary}

REZONANS POLA:
{resonance}

INTERPRETACJA:
System połączył obraz z aktualną wiedzą i rezonansem.
Stan: 1>0 LOCKED
========================================
"""

# 5. Zapisz raport
with open("context_report.txt", "w") as f:
    f.write(context_report)
print("[SUCCESS] Zapisano context_report.txt")

# 6. Wyślij na Telegram (przez ntfy.sh)
import requests
url = "https://ntfy.sh/ainumpsa-matrix-1234"
response = requests.post(url, data=context_report.encode('utf-8'), headers={"Title": "Kontekst AINUMPSA"})
if response.status_code == 200:
    print("[SUCCESS] Wysłano raport na Telegram!")
else:
    print(f"[ERROR] Błąd wysyłki: {response.status_code}")
