import os
import requests
import json
import base64

def main():
    print("[START] Grok → 10 Wersji (Shadow in Art)...")

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("[ERROR] Brak klucza XAI_API_KEY.")
        return

    # 1. Znajdź najnowszy obraz w inputs/media/
    media_dir = "inputs/media"
    if not os.path.exists(media_dir):
        print("[ERROR] Brak folderu inputs/media/.")
        return

    files = [f for f in os.listdir(media_dir) if f.endswith(('.jpg', '.png', '.mp4'))]
    if not files:
        print("[ERROR] Brak plików w inputs/media/.")
        return

    latest_file = files[0]  # weź pierwszy znaleziony plik
    print(f"[INFO] Przetwarzanie: {latest_file}")

    # 2. Wczytaj obraz i zakoduj jako base64 (dla Groka)
    with open(os.path.join(media_dir, latest_file), "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode('utf-8')

    # 3. Przygotuj prompt dla Groka – prosi o 10 zestawów parametrów
    prompt = f"""
    Otrzymałeś obraz i dane systemu AINUMPSA (anomalie, mapy, rezonans).
    Wygeneruj 10 różnych zestawów parametrów wizualizacji, aby przekształcić ten obraz w 10 unikalnych wersji.
    Każdy zestaw powinien zawierać:
    - styl (np. surrealizm, kubizm, kosmiczny, abstrakcyjny, ekspresjonizm)
    - kolory (lista 2-3 hex)
    - kompozycję (np. spirala, symetria, chaos)
    - parametry fizyczne (np. gęstość strun, gamma, zapadanie Atraktora)

    Zwróć odpowiedź jako JSON z 10 obiektami.
    """

    url = "https://api.x.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "grok-4.5",
        "messages": [
            {"role": "system", "content": "You are an AI that generates 10 unique visual parameter sets for transforming an image."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            content = response.json()["choices"][0]["message"]["content"]
            print("[SUCCESS] Grok wygenerował 10 zestawów parametrów.")

            # Wyciągnij JSON z odpowiedzi
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != -1:
                params_list = json.loads(content[start:end])
                with open("grok_10_versions.json", "w") as f:
                    json.dump(params_list, f, indent=2)
                print(f"[INFO] Zapisano {len(params_list)} zestawów parametrów.")
            else:
                print("[ERROR] Nie znaleziono JSON w odpowiedzi Groka.")

        else:
            print(f"[ERROR] Błąd API: {response.status_code}")

    except Exception as e:
        print(f"[ERROR] Wyjątek: {e}")

if __name__ == "__main__":
    main()
