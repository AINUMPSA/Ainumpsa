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
        """
        raw_data = f"{correlation['id']}_{correlation['resonance_index']}_{correlation['timestamp']}"
        token_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
        return f"NUMPSA-TOKEN-{token_hash[:16].upper()}"

    def process_and_present(self):
        print("=== [AINUMPSA] INICJACJA PROCESORA: TWO-WAY UPGRADE ===")
        
        if not os.path.exists(self.billboard_path):
            print("Brak pliku matrix_billboard.json. Matryca pusta.")
            return

        with open(self.billboard_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        correlations = data.get('pinned_correlations', [])
        
        # 1. Budowanie dynamicznej tabeli i osadzanie obrazu graficznego
        markdown_table = "## 📡 PUBLICZNA TABLICA ANOMALII I REZONANSÓW (TENSOR T)\n\n"
        
        # Wstrzyknięcie wyrenderowanej mapy pola jako interfejsu wizualnego
        if os.path.exists(self.image_filename) or True: # Wymuszamy znacznik obrazu
            markdown_table += "### 🌌 Wizualizacja Geometrii Pola Rezonansu\n"
            markdown_table += f"![Geometria Pola AINUMPSA]({self.image_filename})\n\n"
        
        markdown_table += (
            "| ID | OŚ X (ŹRÓDŁO) | OŚ Y (REZONANS) | INDEKS | CYFROWY TOKEN (PROOF OF EXISTENCE) | STATUS |\n"
            "| :--- | :--- | :--- | :---: | :--- | :---: |\n"
        )

        for corr in correlations:
            token = self.generate_token(corr)
            markdown_table += f"| {corr['id']} | {corr['axis_x']} | {corr['axis_y']} | **{corr['resonance_index']}** | `{token}` | `1>0 LOCKED` |\n"

        markdown_table += "\n*Ostatnia automatyczna synchronizacja matrycy: " + datetime.utcnow().isoformat() + "Z*\n"

        # 2. Mutacja pliku README.md
        readme_path = 'README.md'
        readme_content = ""
        
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()

        marker_start = "<!-- START_NUMPSA_BOARD -->"
        marker_end = "<!-- END_NUMPSA_BOARD -->"
        new_section = f"{marker_start}\n\n{markdown_table}\n{marker_end}"

        if marker_start in readme_content and marker_end in readme_content:
            parts = readme_content.split(marker_start)
            top = parts[0]
            bottom = parts[1].split(marker_end)[1]
            updated_content = f"{top}{new_section}{bottom}"
        else:
            updated_content = f"{readme_content}\n\n{new_section}"

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print("[SUKCES] Wygenerowano tokeny, zintegrowano mapę PNG i zaktualizowano README.md.")

if __name__ == "__main__":
    processor = MatrixProcessor()
    processor.process_and_present()
