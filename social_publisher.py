import os
import requests

# Stałe – BEZ emoji w nagłówkach (unikamy błędów kodowania)
TOPIC_NAME = "ainumpsa-matrix-1234"
URL = f"https://ntfy.sh/{TOPIC_NAME}"
TITLE = "AINUMPSA 3D Matrix Engine"
MESSAGE = "Nowy cykl skanowania zakończony. Plik wizualizacji wygenerowany pomyslnie."
GIF_PATH = "collider_evolution.gif"

def main():
    print("[START] Inicjalizacja Social Publisher...")

    try:
        if os.path.exists(GIF_PATH):
            print(f"Znaleziono plik {GIF_PATH}. Wysyłanie z załącznikiem...")
            with open(GIF_PATH, "rb") as f:
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
            print("Brak pliku załącznika. Wysyłanie wiadomości tekstowej...")
            response = requests.post(
                URL,
                data=MESSAGE.encode("utf-8"),
                headers={
                    "Title": TITLE,
                    "Tags": "robot,warning"
                }
            )

        if response.status_code == 200:
            print("Pomyślnie wysłano powiadomienie na ntfy.sh!")
        else:
            print(f"Blad wysylania: status {response.status_code} – {response.text}")

    except Exception as e:
        print(f"Wyjątek w social_publisher: {e}")

if __name__ == "__main__":
    main()
