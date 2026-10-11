pythonimport time
import sys
import math
import random

def generate_tensor_field(t):
    """Generuje dynamiczne pole Tensor T, które ewoluuje w czasie"""
    width = 50
    # Obliczanie fali rezonansowej (częstotliwość Alfa/Theta)
    wave = int((math.sin(t * 0.5) + 1) * 15)
    
    # Tworzenie surowej matrycy szumu (Siew danych)
    noise_chars = [".", "·", "0", "1", "x", "𝚿", "ℵ"]
    row = [random.choice(noise_chars) if random.random() > 0.15 else " " for _ in range(width)]
    
    # Wstrzykiwanie geometrycznego punktu zakrzywienia (Sonda intencji)
    center_marker = "=== [ 1 > 0 ] ==="
    pos = max(0, min(width - len(center_marker), wave))
    row[pos:pos+len(center_marker)] = list(center_marker)
    
    return "".join(row)

def run_seeder_probe(duration=20):
    sys.stdout.write("[SONDA SIEWNA] Inicjalizacja zasiewu pola uwagi...\n")
    start = time.time()
    frame = 0
    
    while time.time() - start < duration:
        grid_line = generate_tensor_field(frame)
        # Efekt wodospadu danych (Matrix-like stream)
        sys.stdout.write(f"\r{grid_line}")
        sys.stdout.flush()
        
        time.sleep(0.05)  # Częstotliwość drgania siatki
        frame += 1
    sys.stdout.write("\n[SONDA SIEWNA] Emisja zakończona. Pole ustabilizowane.\n")

if __name__ == "__main__":
    run_seeder_probe()
