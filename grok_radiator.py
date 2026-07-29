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
    
    # Czyste nagłówki (bez emoji, żeby uniknąć błędów kodowania)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "grok-4.5",
        "messages": [
            {
                "role": "system",
                "content": "You are the AINUMPSA matrix radiator. Generate unique quantum radiation text for the current matrix cycle."
            },
            {
                "role": "user",
                "content": "Execute black hole radiation analysis for the T-Matrix."
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
            
            # Zapisz wynik do pliku, żeby inne skrypty mogły z niego skorzystać
            os.makedirs("Knowledge_base", exist_ok=True)
            with open("Knowledge_base/grok_radiation_output.txt", "w", encoding="utf-8") as f:
                f.write(content)
        else:
            print(f"[ERROR] Błąd podczas komunikacji z API Groka: HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Wyjątek podczas żądania do Groka: {e}")

if __name__ == "__main__":
    main()
# Po otrzymaniu odpowiedzi od Groka
grok_response = response.json()
visual_params = grok_response.get("visual_params", {})
with open("visual_params.json", "w") as f:
    json.dump(visual_params, f, indent=2)
