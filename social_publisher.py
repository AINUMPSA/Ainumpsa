import os
import requests

def main():
    print("[START] Inicjalizacja Social Publisher...")
    
    # Dedykowany kanał odbiorczy ntfy
    TOPIC_NAME = "ainumpsa-matrix-1234"
    URL = f"https://ntfy.sh/{TOPIC_NAME}"
    
    # Treść powiadomienia (Emoji są tu bezpieczne)
    TITLE = "AINUMPSA 3D Matrix Engine"
    MESSAGE = "Nowy cykl skanowania zakończony! Plik wizualizacji wygenerowany pomyślnie. 🤖"
    
    # Czyste nagłówki HTTP (BEZ znaków specjalnych/emoji w nagłówkach!)
    headers = {
        "Title": TITLE,
        "Priority": "default",
        "Tags": "robot,matrix"
    }

    try:
        # Sprawdzamy, czy istnieje plik do załączenia
        gif_path = "collider_evolution.gif"
        if os.path.exists(gif_path):
            print(f"Znaleziono plik {gif_path}. Wysyłanie z załącznikiem...")
            with open(gif_path, "rb") as f:
                response = requests.post(URL, data=f, headers=headers)
        else:
            print("Brak pliku załącznika. Wysyłanie zwykłego powiadomienia tekstowego...")
            response = requests.post(URL, data=MESSAGE.encode('utf-8'), headers=headers)

        if response.status_code == 200:
            print("[SUCCESS] Powiadomienie wysłane pomyślnie na ntfy.sh!")
        else:
            print(f"[ERROR] Błąd podczas wysyłania powiadomienia: HTTP {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[ERROR] Wyjątek w social_publisher: {e}")

if __name__ == "__main__":
    main()
