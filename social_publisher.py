import os
import requests

# Dedykowany kanał odbiorczy ntfy
TOPIC_NAME = "ainumpsa-matrix-1234"
URL = f"https://ntfy.sh/{TOPIC_NAME}"

# Treść powiadomienia
TITLE = "🤖 AINUMPSA 3D Matrix Engine"
MESSAGE = "Nowy cykl skanowania zakończony! Plik wizualizacji wygenerowany pomyślnie."

gif_path = "collider_evolution.gif"

if os.path.exists(gif_path):
    print(f"Znaleziono plik {gif_path}. Wysyłanie z załącznikiem...")
    with open(gif_path, "rb") as f:
        response = requests.post(
            URL,
            data=f,
            headers={
                "Title": TITLE,
                "Message": MESSAGE,
                "Filename": "collider_evolution.gif",
                "Tags": "robot,chart_with_upwards_trend"
            }
        )
else:
    print(f"Nie znaleziono pliku {gif_path}. Wysyłanie wiadomości tekstowej...")
    response = requests.post(
        URL,
        data=MESSAGE.encode("utf-8"),
        headers={
            "Title": TITLE,
            "Tags": "robot,warning"
        }
    )

if response.status_code == 200:
    print("✅ Pomyślnie wysłano powiadomienie na ntfy.sh!")
else:
    print(f"❌ Błąd wysyłania: status {response.status_code}")

