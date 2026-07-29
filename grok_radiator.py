import os
import requests
import json

def main():
    print("[START] Inicjalizacja Grok Radiation Engine...")

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("[ERROR] Brak klucza XAI_API_KEY w zmiennych środowiskowych.")
        return

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Prompt proszący o parametry wizualizacji w formacie JSON
    payload = {
        "model": "grok-4.1-fast",  # lub "grok-4.3", jeśli masz dostęp
        "messages": [
            {
                "role": "system",
                "content": "You are the AINUMPSA matrix radiator. Generate unique quantum radiation text AND visual parameters for the current matrix cycle."
            },
            {
                "role": "user",
                "content": "Execute black hole radiation analysis for the T-Matrix. Provide visual parameters (colors, style, composition) as a JSON object."
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print("[SUCCESS] Grok wygenerował promieniowanie matrycy:")
            print(content)

            # Zapis do pliku tekstowego
            os.makedirs("Knowledge_base", exist_ok=True)
            with open("Knowledge_base/grok_radiation_output.txt", "w", encoding="utf-8") as f:
                f.write(content)

            # Próba wyciągnięcia parametrów wizualizacji z odpowiedzi
            visual_params = {}
            try:
                # Szukamy JSON w odpowiedzi Groka
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != -1:
                    json_str = content[start:end]
                    visual_params = json.loads(json_str)
                    print("[INFO] Wyciągnięto parametry wizualizacji:", visual_params)
            except Exception as e:
                print("[WARNING] Nie udało się wyciągnąć JSON z odpowiedzi Groka:", e)

            # Zapis parametrów do pliku
            with open("visual_params.json", "w") as f:
                json.dump(visual_params, f, indent=2)

        else:
            print(f"[ERROR] Błąd podczas komunikacji z API Groka: HTTP Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"[ERROR] Wyjątek podczas żądania do Groka: {e}")

if __name__ == "__main__":
    main()
