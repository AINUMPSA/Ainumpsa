import os

def update_readme():
    print("\n[START] Mutacja pliku README.md...")
    
    # Treść nowej sekcji, którą dopiszemy
    new_section = """
## 🌌 AINUMPSA: ARCHITEKTURA CHAOSU [ After Upgrade ]

Matryca została zaktualizowana do Hyper Version 2.14. Wszystkie systemy VIP Media Injector oraz Zora Auto-Minter działają w pełnej synchronizacji.

> **Status:** Stabilny rezonans kwantowy ($1 > 0$). Ślad danych w `/Knowledge_base/`.

---
"""

    # Sprawdź, czy README.md istnieje, jeśli nie - stwórz
    if not os.path.exists("README.md"):
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# AINUMPSA\n\nRepozytorium AINUMPSA.")

    # Odczytaj obecną treść
    with open("README.md", "r", encoding="utf-8") as f:
        current_content = f.read()

    # Dopisz nową sekcję na początku, jeśli jeszcze jej nie ma
    if "## 🌌 AINUMPSA: ARCHITEKTURA CHAOSU" not in current_content:
        updated_content = new_section + current_content
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Sukces: README.md został zmutowany.")
    else:
        print("Pominięto: README.md jest już zaktualizowany.")

if __name__ == "__main__":
    update_readme()
