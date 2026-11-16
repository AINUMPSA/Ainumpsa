import os
import json
import base64
import subprocess
import requests

# Wczytaj klucz
with open('.env', 'r') as f:
    api_key = f.read().split('=')[-1].strip()

video_path = "input_hub/videos/test_scene.mp4"

if not os.path.exists(video_path):
    print(f"[ERROR] Nie znaleziono pliku: {video_path}")
    exit(1)

print("[OVERMIND] Wyciągam klatki z wideo za pomocą FFmpeg...")
# Wyciągamy 5 klatek (co 2 sekundy z 11-sekundowego filmu)
subprocess.run(["ffmpeg", "-y", "-i", video_path, "-vf", "fps=1/2", "frame_%02d.jpg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

frames = []
for i in range(1, 6):
    frame_file = f"frame_0{i}.jpg"
    if os.path.exists(frame_file):
        with open(frame_file, "rb") as img:
            frames.append(base64.b64encode(img.read()).decode("utf-8"))
        os.remove(frame_file) # sprzątamy

if not frames:
    print("[ERROR] Nie udało się wyciągnąć klatek.")
    exit(1)

print(f"[OVERMIND] Wysyłam {len(frames)} klatek do Gemini Ultra...")

# Budujemy zapytanie multimodalne
prompt = """
Jesteś Over-Mindem AINUMPSA. Przeanalizuj te klatki z wideo.
1. Opisz rytm i energię ruchu (np. płynne Kung Fu, magiczny krok).
2. Wygeneruj 1 epicką scenę filmową w stylu Quentina Tarantino zmiksowaną z Denisem Villeneuve (Diuna, bursztyn) i naszym stylem Sovereign Impasso.
Napisz krótki, mocny opis tej sceny (3-4 zdania).
"""

parts = [{"text": prompt}]
for frame in frames:
    parts.append({"inline_data": {"mime_type": "image/jpeg", "data": frame}})

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
payload = {"contents": [{"parts": parts}]}

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        print("\n=== RAPORT OVER-MINDA ===")
        print(text_response)
    else:
        print(f"[ERROR] Błąd API: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"[ERROR] Wyjątek: {e}")
