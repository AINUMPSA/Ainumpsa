import os

# Definicja ścieżki do folderu
folder_path = "./multimodal_pool"

# Bezpieczne tworzenie katalogu, jeśli jeszcze nie istnieje
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"[SUKCES] Folder '{folder_path}' został pomyślnie utworzony.")
else:
    print(f"[INFO] Folder '{folder_path}' już istnieje w strukturze projektu.")

# Tworzenie pliku .gitkeep wewnątrz folderu, aby Git nie zgłaszał błędów (na czerwono)
gitkeep_path = os.path.join(folder_path, ".gitkeep")
with open(gitkeep_path, "w") as f:
    f.write("# Ten plik pozwala systemowi Git na śledzenie tego folderu, dopóki nie wgrasz multimediów.\n")

print(f"[SUKCES] Wygenerowano plik zabezpieczający: {gitkeep_path}")

