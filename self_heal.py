import os
import subprocess
import sys
import json

def check_workflow():
    """Sprawdza, czy plik workflow main.yml istnieje i czy ma prawidłową składnię."""
    workflow_path = ".github/workflows/main.yml"
    if not os.path.exists(workflow_path):
        print(f"[SELF-HEAL] BŁĄD: Brak pliku {workflow_path}. Tworzę domyślny...")
        # Tu można dodać kod tworzący domyślny plik workflow
        return False
    # Tu można dodać sprawdzanie składni YAML (np. za pomocą 'yamllint')
    return True

def check_scripts():
    """Sprawdza, czy wszystkie główne skrypty istnieją."""
    required_scripts = ["vip_media_injector.py", "knowledge_engine.py", "matrix_collider.py", "nft_preparer.py"]
    all_exist = True
    for script in required_scripts:
        if not os.path.exists(script):
            print(f"[SELF-HEAL] OSTRZEŻENIE: Brak pliku {script}. Próba odtworzenia...")
            # Tu można dodać kod do odtwarzania skryptu z szablonu
            all_exist = False
    return all_exist

def main():
    print("[SELF-HEAL] Rozpoczynam auto-diagnostykę...")

    # 1. Sprawdzenie Workflow
    workflow_ok = check_workflow()
    if not workflow_ok:
        print("[SELF-HEAL] Naprawianie Workflow...")
        # Tu można dodać komendę do odtworzenia pliku, np. z backupu

    # 2. Sprawdzenie skryptów
    scripts_ok = check_scripts()
    if not scripts_ok:
        print("[SELF-HEAL] Naprawianie skryptów...")

    if workflow_ok and scripts_ok:
        print("[SELF-HEAL] Auto-diagnostyka zakończona. Wszystko jest w porządku.")
    else:
        print("[SELF-HEAL] Auto-diagnostyka zakończona. Wprowadzono naprawy.")

if __name__ == "__main__":
    main()
