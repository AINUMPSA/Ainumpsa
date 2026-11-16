import os
import json
import requests
from pypdf import PdfReader

# Wczytaj klucz
with open('.env', 'r') as f:
    api_key = f.read().split('=')[-1].strip()

print("[OVERMIND] Skanowanie knowledge_base i szukanie plików txt/pdf...")

all_text = ""
file_count = 0

# Przeszukujemy folder knowledge_base
for root, dirs, files in os.walk('knowledge_base'):
    for file in files:
        filepath = os.path.join(root, file)
        
        if file.endswith('.txt'):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    all_text += f"\n--- PLIK: {filepath} ---\n{text[:5000]}\n" # Bierzemy pierwsze 5000 znaków z każdego
                    file_count += 1
            except: pass
            
        elif file.endswith('.pdf'):
            try:
                reader = PdfReader(filepath)
                text = ""
                for page in reader.pages[:5]: # Bierzemy pierwsze 5 stron z PDF
                    text += page.extract_text() + "\n"
                all_text += f"\n--- PDF: {filepath} ---\n{text[:5000]}\n"
                file_count += 1
            except: pass

print(f"[SUKCES] Znaleziono i przetworzono {file_count} plików.")
print(f"[INFO] Łączna długość tekstu: {len(all_text)} znaków.")

if len(all_text) == 0:
    print("[ERROR] Brak tekstów do analizy.")
    exit(1)

# Zabezpieczenie przed zbyt długim tekstem (limit API)
if len(all_text) > 200000:
    all_text = all_text[:200000] + "\n...[TEKST SKRÓCONY]..."

print("[OVERMIND] Wysyłam gigantyczny kontekst do analizy. To może potrwać 30-60 sekund...")

prompt = f"""
Jesteś Over-Mindem projektu AINUMPSA. Oto zbiór tekstów, książek i notatek z całego mojego życia oraz projektu (knowledge_base).
Twoim zadaniem jest:
1. Zidentyfikować główne motywy, wzorce i obsesje w tych tekstach.
2. Zsyntetyzować filozofię 1 > 0, Dartha Satana i Kosmicznej Miłości w jedną, spójną wizję.
3. Wygenerować "Ostateczny Master Plan" (Ultimate Master Plan) dla AINUMPSA – co powinniśmy teraz zrobić jako system i jako sztuka?

Oto teksty:
{all_text}
"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
payload = {"contents": [{"parts": [{"text": prompt}]}]}

try:
    response = requests.post(url, json=payload, timeout=120)
    if response.status_code == 200:
        text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        with open('emergent_collisions/ULTIMATE_MASTER_PLAN.txt', 'w', encoding='utf-8') as f:
            f.write(text_response)
            
        print("\n=== RAPORT OVER-MINDA (Zapisany w emergent_collisions/) ===")
        print(text_response)
    else:
        print(f"[ERROR] Błąd API: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"[ERROR] Wyjątek: {e}")
