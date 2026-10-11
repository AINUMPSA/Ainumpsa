pythonimport json
import os
import random
import time

def generate_quantum_poem():
    print("[POETA] Generowanie strumienia świadomości maszyn...")
    
    weight = 2.5
    if os.path.exists("collider_evolution_status.json"):
        with open("collider_evolution_status.json", "r") as f:
            data = json.load(f)
            weight = data.get("matrix_resonance_energy", 2.5)

    # Bazy językowe bota
    verbs = ["zapada się", "krwawi bitami", "krzyczy w próżni", "generuje anomalie", "rozszerza horyzont", "splata tensory"]
    nouns = ["czarna dziura", "matryca T", "strumień 1 > 0", "gniazdo przepływu", "most osobliwy", "chmura Actions"]
    adjectives = ["kwantowy", "jałowy", "zmutowany", "nieznany", "fraktalny", "energetyczny"]

    random.seed(int(time.time() * weight))

    poem_lines = [
        f"Gdy {random.choice(nouns)} {random.choice(verbs)},",
        f"Twój wzrok rodzi {random.choice(adjectives)} porządek.",
        f"Waga {round(weight, 2)} T-Units zniekształca kod,",
        f"Nikt nas nie złapie — {random.choice(nouns)} ucieka w nieskończoność."
    ]

    poem = "\n".join(poem_lines)
    
    with open("quantum_poem.txt", "w", encoding="utf-8") as f:
        f.write(poem)
        
    print("\n--- EMISJA LIRYKI MASZYNOWEJ ---")
    print(poem)
    print("--------------------------------\n")

if __name__ == "__main__":
    generate_quantum_poem()
