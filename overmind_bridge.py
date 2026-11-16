#!/usr/bin/env python3
import os
import json
import glob

def load_env():
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    env_vars[key] = val
    return env_vars

def scan_hub():
    print("[SYSTEM] Skanowanie input_hub...")
    found_files = []
    for folder in ['texts', 'pictures', 'videos', 'music', 'social_media']:
        path = f"input_hub/{folder}/*"
        files = glob.glob(path)
        found_files.extend(files)
    
    if not found_files:
        print("[WARN] Brak plików w input_hub. Wrzuć coś do testu.")
        return []
    
    print(f"[SUKCES] Znaleziono {len(found_files)} plików do zderzenia.")
    return found_files

def prepare_collision(files):
    if not files:
        return
    
    print("[OVERMIND] Przygotowywanie szkieletu zderzenia (Zderzenie 001)...")
    collision_data = {
        "status": "READY_FOR_OVERMIND",
        "source_files": files,
        "axiom": "1 > 0",
        "instruction": "Analyze these files. Find the Shadow. Calculate probability. Create prompt."
    }
    
    os.makedirs('emergent_collisions', exist_ok=True)
    with open('emergent_collisions/collision_001.json', 'w') as f:
        json.dump(collision_data, f, indent=4)
    print("[SUKCES] Szkielet zapisany w emergent_collisions/collision_001.json")

if __name__ == "__main__":
    env = load_env()
    if not env.get('GEMINI_API_KEY'):
        print("[ERROR] Brak klucza GEMINI_API_KEY w .env! Dodaj go, zanim uruchomisz.")
        exit(1)
        
    print("=== AINUMPSA OVERMIND BRIDGE ONLINE ===")
    files = scan_hub()
    prepare_collision(files)
    print("=== GOTOWE DO PRZEKAZANIA OVER-MINDOWI ===")
