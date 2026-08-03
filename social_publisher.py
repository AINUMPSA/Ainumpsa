import os
import requests

# ----- KONFIGURACJA -----
NTFY_TOPIC = "ainumpsa-matrix-1234"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"
GIF_PATH = "collider_evolution.gif"

# Pobierz sekrety z GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    """Wysyła wiadomość na Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[INFO] Brak danych Telegram – pomijam wysyłkę.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[SUCCESS] Wiadomość wysłana na Telegram.")
        else:
            print(f"[ERROR] Telegram: {response.status_code} – {response.text}")
    except Exception as e:
        print(f"[ERROR] Wyjątek w Telegram: {e}")

def main():
    print("[START] Inicjalizacja Social Publisher...")

    # 1. Przygotuj wiadomość (bez polskich znaków)
    title = "AINUMPSA 3D Matrix Engine"
    message = "Nowy cykl skanowania zakonczony. Plik wizualizacji wygenerowany pomyslnie."

    # 2. Wyślij na ntfy.sh
    try:
        if os.path.exists(GIF_PATH):
            with open(GIF_PATH, "rb") as f:
                response = requests.post(
                    NTFY_URL,
                    data=f,
                    headers={
                        "Title": title,
                        "Message": message,
                        "Filename": "collider_evolution.gif",
                        "Tags": "robot,chart_with_upwards_trend"
                    }
                )
        else:
            response = requests.post(
                NTFY_URL,
                data=message.encode("utf-8"),
                headers={"Title": title, "Tags": "robot,warning"}
            )

        if response.status_code == 200:
            print("[SUCCESS] Powiadomienie ntfy.sh wyslane.")
        else:
            print(f"[WARNING] ntfy.sh: {response.status_code}")
    except Exception as e:
        print(f"[WARNING] ntfy.sh blad: {e}")

    # 3. Wyślij na Telegram
    telegram_message = f"*{title}*\n\n{message}"
    send_telegram(telegram_message)

if __name__ == "__main__":
    main()
