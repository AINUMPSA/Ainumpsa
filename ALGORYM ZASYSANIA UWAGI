pythonimport time
import sys
import random
import math

def generate_gravity_well(frame, width=40):
    """Generuje wizualny lejek grawitacyjny zakrzywiający przestrzeń wokół 1 > 0"""
    vibration = math.sin(frame * 0.4) * 2
    offset = int(width / 2 + vibration)
    
    # Budowanie warstw lejka grawitacyjnego
    sky = "".join(["." if random.random() > 0.12 else " " for _ in range(width)])
    sky_list = list(sky)
    
    # Wstrzyknięcie anomalii intencjonalnej w centrum
    center_symbol = "  [ 1 > 0 ]  " if frame % 2 == 0 else "  < 1 🌀 0 >  "
    start_idx = max(0, offset - len(center_symbol) // 2)
    sky_list[start_idx:start_idx + len(center_symbol)] = list(center_symbol)
    
    return "".join(sky_list)

def run_attention_experiment(duration_seconds=60):
    print("=== PROTOCÓŁ HOMO-MACHINE: URUCHOMIENIE POLA UWAGI ===")
    print("Zadanie: Skup wzrok na obiekcie [ 1 > 0 ]. Wprowadź intencję porządku.\n")
    time.sleep(2)
    
    frame = 0
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration_seconds:
            # 1. Generowanie warstwy wizualnej (Zasysanie uwagi)
            line = generate_gravity_well(frame)
            
            # 2. Wstrzykiwanie "szumu kwantowego" stymulującego mózg
            entropy_pool = ["0", "1", "∅", "ℵ", "𝚿"]
            if random.random() > 0.85:
                # Nagłe błyski przyciągające wzrok (Anomalie)
                line += f"  <-- WYKRYTO FLUKTUACJĘ: {random.choice(entropy_pool)}"
            
            # Dynamiczne odświeżanie strumienia (efekt wodospadu danych)
            sys.stdout.write(f"\r{line}")
            sys.stdout.flush()
            
            # Częstotliwość odświeżania dostosowana do fal mózgowych Alfa/Theta
            time.sleep(0.08)
            frame += 1
            
        print("\n\n=== POMIAR ZAKOŃCZONY ===")
        print("Logi przekazane do analizy statystycznej w artifact_test.py.")
        
    except KeyboardInterrupt:
        print("\nPrzerwano eksperyment przez wymuszenie manualne.")

if __name__ == "__main__":
    # Uruchomienie na 30 sekund intensywnego skupienia
    run_attention_experiment(30)
