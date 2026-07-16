import os
import numpy as np
from pypdf import PdfReader

def diagnose_pdf(folder_path="knowledge_base"):
    print("\n=== ROZPOCZĘCIE DIAGNOSTYKI TEKSTU PDF ===")
    if not os.path.exists(folder_path):
        print("Brak folderu!")
        return
        
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        print("Brak plików PDF!")
        return

    path = os.path.join(folder_path, pdf_files[0])
    try:
        reader = PdfReader(path)
        print(f"Plik: {pdf_files[0]}")
        print(f"Liczba stron: {len(reader.pages)}")
        
        # Wyciągamy surowy tekst z pierwszej strony
        raw_text = reader.pages[0].extract_text()
        
        print("\n--- SUROWA ZAWARTOŚĆ POCZĄTKU DOKUMENTU (PIERWSZE 400 ZNAKÓW) ---")
        if raw_text:
            print(raw_text[:400])
            print(f"\nCałkowita długość wyciągniętego tekstu ze strony 1: {len(raw_text)} znaków")
        else:
            print("[ALARM] pypdf zwrócił zupełnie pusty tekst (None lub pusty ciąg)!")
            print("Prawdopodobna przyczyna: kompresor usunął warstwę tekstową i zamienił plik w obrazek.")
            
    except Exception as e:
        print(f"Błąd diagnostyki: {e}")

print("=== Uruchamianie testów diagnostycznych AINUMPSA ===")
diagnose_pdf()
