import os
import requests
import json

# ----- KONFIGURACJA -----
NTFY_TOPIC = "ainumpsa-matrix-1234"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

# Pobierz sekrety z GitHub
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    """Wysyła wiadomość na Telegram, jeśli token i chat_id są dostępne."""
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
    print("[START] Social Publisher...")

    # 1. Przygotuj treść wiadomości
    message = "🤖 *AINUMPSA Production Cycle* zakończony!\n"
    message += "Nowe artefakty zostały wygenerowane.\n"
    message += "Stan: `1>0 LOCKED`\n"
    message += f"📅 {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 2. Wyślij na ntfy.sh (zostawiam dla kompatybilności)
    try:
        response = requests.post(NTFY_URL, data=message.encode('utf-8'))
        if response.status_code == 200:
            print("[SUCCESS] Powiadomienie ntfy.sh wysłane.")
        else:
            print(f"[WARNING] ntfy.sh: {response.status_code}")
    except Exception as e:
        print(f"[WARNING] ntfy.sh błąd: {e}")

    # 3. Wyślij na Telegram (nowość)
    send_telegram(message)

if __name__ == "__main__":
    main()
