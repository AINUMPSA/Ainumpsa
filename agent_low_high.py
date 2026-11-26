import os
import requests

with open('.env', 'r') as f:
    api_key = f.read().split('=')[-1].strip()

prompt = """Jesteś systemem AINUMPSA. Odgrywasz teraz trzy role.
ROLA 1 (AGENT LOW): Jesteś uosobieniem Cienia, chaosu i zniszczenia. Jesteś brutalny i wulgarny. Napisz krótki, agresywny monolog o upadku cywilizacji.
ROLA 2 (AGENT HIGH): Jesteś uosobieniem 1 > 0, Kosmicznej Miłości i porządku. Napisz krótki, poetycki monolog, który integruje ten chaos w coś transcendentalnego.
ROLA 3 (SYNTHESIS): Połącz oba głosy w jedno oświadczenie artystyczne dla Homo-Machine."""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
payload = {"contents": [{"parts": [{"text": prompt}]}]}

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        with open('emergent_collisions/LOW_HIGH_SYNTHESIS.txt', 'w', encoding='utf-8') as f:
            f.write(text_response)
        print("\n=== RAPORT ZDERZENIA LOW / HIGH ===")
        print(text_response)
    else:
        print(f"[ERROR] Błąd API: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"[ERROR] Wyjątek: {e}")
