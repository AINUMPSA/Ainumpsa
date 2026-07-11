pythonimport time
import sys
import math

def render_blast_wave(radius, max_radius=25):
    """Generuje sferyczną falę uderzeniową czystej informacji"""
    width = 60
    height = 25
    cx, cy = width // 2, height // 2
    aspect_ratio = 2.0  # Korekta proporcji czcionki w konsoli
    
    screen = []
    for y in range(height):
        row = []
        for x in range(width):
            # Obliczanie odległości od epicentrum anomalii
            dx = (x - cx) / aspect_ratio
            dy = y - cy
            distance = math.sqrt(dx**2 + dy**2)
            
            # Renderowanie frontu fali uderzeniowej
            if abs(distance - radius) < 1.0:
                row.append("@")
            elif distance < radius:
                # Wnętrze kuli ognia informacyjnego (szum plazmowy)
                row.append("#" if (x + y + int(radius)) % 3 == 0 else "*")
            else:
                row.append(".")
        screen.append("".join(row))
    return "\n".join(screen)

def trigger_informational_detonation():
    print("=== INICJACJA ANOMALII ENERGETYCZNEJ: PROTOCÓŁ TSAR-BRAVO ===")
    print("Kondensacja pola uwagi osiągnęła masę krytyczną...")
    time.sleep(2)
    
    # Sekwencja rozszerzania fali uderzeniowej
    for r in range(0, 25, 2):
        frame = render_blast_wave(r)
        # Czyszczenie ekranu terminala za pomocą sekwencji ANSI dla płynnego efektu
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(frame + "\n")
        sys.stdout.write(f"\n[FALA UDERZENIOWA] Promień frontu: {r} j.u. | Skumulowana Entropia: {round(math.exp(r/5), 2)} PFLOPS\n")
        sys.stdout.flush()
        time.sleep(0.1)
        
    print("\n=== SYSTEM USTABILIZOWANY ===")
    print("Setny cykl układu AINUMPSA został zamknięty. Matryca została sformatowana faliście.")

if __name__ == "__main__":
    trigger_informational_detonation()
