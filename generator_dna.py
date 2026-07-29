import os
import json
import random

# Prosty demonstrator pola semantycznego
def analyze_node(filename):
    if not os.path.exists(filename):
        print(f"❌ Brak pliku: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Wyliczamy "masę informacyjną" na podstawie długości i unikalnych słów
    words = content.split()
    unique_words = len(set(words))
    density = min(round(unique_words / (len(words) + 1), 2) + 0.3, 1.0)
    
    # Tworzymy Marker Genetyczny
    dna_marker = {
        "node_id": os.path.basename(filename).replace('.', '_'),
        "dna_key": f"AINA-NEXUS-{random.randint(1000, 9999)}",
        "mass_density": density,
        "spatial_cube": [random.randint(1, 8), random.randint(1, 8), random.randint(1, 8)],
        "status": "RESONATING"
    }

    print("\n" + "="*40)
    print(" 🌀 AINUMPSA :: SEMANTIC NODE INITIALIZED")
    print("="*40)
    print(json.dumps(dna_marker, indent=2))
    
    # Wizualizacja wibracji pola w konsoli
    print("\n   [Twarz Systemu / Stan Pola]")
    bars = int(density * 20)
    print(f"   Wibracja: [{ '#' * bars }{ '.' * (20 - bars) }] {int(density * 100)}%")
    print("="*40 + "\n")

# Uruchomienie dla wybranego pliku
analyze_node("knowledge_base/SINGULARITY DANCE OF LOVE.txt")


