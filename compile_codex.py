import os
from pypdf import PdfReader

# Foldery, w których szukamy wiedzy
folders = ["knowledge_base", "multimodal_pool"]
output_file = "knowledge_base/THE_AINUMPSA_CODEX.txt"

print("[SYSTEM] Rozpoczynam kompilację Kodeksu AINUMPSA...")

all_text = ""
pdf_count = 0
txt_count = 0

for folder in folders:
    if not os.path.exists(folder):
        continue
    for root, dirs, files in os.walk(folder):
        # Pomijamy foldery ukryte i .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            if file.endswith(".pdf"):
                print(f"  -> PDF: {filepath}")
                try:
                    reader = PdfReader(filepath)
                    all_text += f"\n\n{'='*60}\n--- DOKUMENT PDF: {filepath} ---\n{'='*60}\n\n"
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            all_text += text + "\n"
                    pdf_count += 1
                except Exception as e:
                    print(f"     [BŁĄD] {e}")
                    
            elif file.endswith(".txt"):
                print(f"  -> TXT: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        all_text += f"\n\n{'='*60}\n--- DOKUMENT TXT: {filepath} ---\n{'='*60}\n\n"
                        all_text += content + "\n"
                    txt_count += 1
                except Exception as e:
                    print(f"     [BŁĄD] {e}")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"\n[SUKCES] Kodeks został utworzony: {output_file}")
print(f"[INFO] Przetworzono PDF-ów: {pdf_count}")
print(f"[INFO] Przetworzono TXT: {txt_count}")
print(f"[INFO] Rozmiar pliku końcowego: {len(all_text)} znaków.")
