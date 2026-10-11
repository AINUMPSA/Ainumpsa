import json
import os
import hashlib
from datetime import datetime

class MatrixProcessor:
    def __init__(self):
        self.billboard_path = 'matrix_billboard.json'
        self.image_filename = 'matrix_field_map.png'
        
    def generate_token(self, correlation):
        """
        Generuje unikalny, kryptograficzny identyfikator (Hash SHA-256)
        stanowiący cyfrowy Proof of Existence dla wykrytego rezonansu.
        Bezpiecznie pobiera klucze za pomocą metody .get()
        """
        c_id = correlation.get('id', correlation.get('correlation_id', '000'))
        c_idx = correlation.get('resonance_index', correlation.get('resonance_score', 0.0))
        c_time = correlation.get('timestamp', correlation.get('timestamp_utc', ''))
        
        raw_data = f"{c_id}_{c_idx}_{c_time}"
        token_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
        return f"NUMPSA-TOKEN-{token_hash[:16].upper()}"

    def process_and_present(self):
        print("=== [AINUMPSA] INICJACJA PROCESORA: TWO-WAY UPGRADE ===")
        
        if not os.path.exists(self.billboard_path):
            print("Brak pliku matrix_billboard.json. Matryca pusta.")
            return

        with open(self.billboard_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                print("Błąd odczytu pliku JSON.")
                return

        correlations = data.get('pinned_correlations', [])
        
        # 1. Budowanie dynamicznej tabeli i osadzanie obrazu graficznego
        markdown_table = "## 📡 PUBLICZNA TABLICA ANOMALII I REZONANSÓW (TENSOR T)\n\n"
        markdown_table += "### 🌌 Wizualizacja Geometrii Pola Rezonansu\n"
        markdown_table += f"![Geometria Pola AINUMPSA]({self.image_filename})\n\n"
        
        markdown_table += (
            "| ID | OŚ X (ŹRÓDŁO) | OŚ Y (REZONANS) | INDEKS | CYFROWY TOKEN (PROOF OF EXISTENCE) | STATUS |\n"
            "| :--- | :--- | :--- | :---: | :--- | :---: |\n"
        )

        for corr in correlations:
            token = self.generate_token(corr)
            c_id = corr.get('id', corr.get('correlation_id', 'N/A'))
            c_x = corr.get('axis_x', corr.get('cross_points', ['N/A'])[0])
            c_y = corr.get('axis_y', corr.get('cross_points', ['N/A', 'N/A'])[1] if len(corr.get('cross_points', [])) > 1 else 'N/A')
            c_idx = corr.get('resonance_index', corr.get('resonance_score', 0.0))
            
            markdown_table += f"| {c_id} | {c_x} | {c_y} | **{c_idx}** | `{token}` | `1>0 LOCKED` |\n"

        markdown_table += "\n*Ostatnia automatyczna synchronizacja matrycy: " + datetime.utcnow().isoformat() + "Z*\n"

        # 2. Mutacja pliku README.md (Zabezpieczone podmienianie sekcji)
        readme_path = 'README.md'
        readme_content = ""
        
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()

        marker_start = "<!-- START_NUMPSA_BOARD -->"
        marker_end = "<!-- END_NUMPSA_BOARD -->"
        new_section = f"{marker_start}\n\n{markdown_table}\n{marker_end}"

        if marker_start in readme_content and marker_end in readme_content:
            try:
                start_idx = readme_content.find(marker_start)
                end_idx = readme_content.find(marker_end) + len(marker_end)
                updated_content = readme_content[:start_idx] + new_section + readme_content[end_idx:]
            except Exception:
                updated_content = f"{readme_content}\n\n{new_section}"
        else:
            updated_content = f"{readme_content}\n\n{new_section}"

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print("[SUKCES] Wygenerowano tokeny, zintegrowano mapę PNG i bezpiecznie zaktualizowano README.md.")

if __name__ == "__main__":
    processor = MatrixProcessor()
    processor.process_and_present()
