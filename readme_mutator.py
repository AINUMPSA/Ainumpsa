import json
import math
import os
import random
import time

# 1. Obliczenia kwantowe i wskaźniki systemu
quantum_state = "HYPER-EVOLVED"
weight = round(random.uniform(25.0, 99.9), 2)
dp = round(random.uniform(0.001, 0.099), 4)

# 2. Generowanie dynamicznego lejka grawitacyjnego
vibration = int((math.sin(time.time()) + 1) * 5) + 2
ascii_well = ""

for i in range(5):
    spaces = " " * (i * 2 + vibration)
    dots = "." * (20 - i * 4)
    if i == 2:
        ascii_well += f"{spaces}{dots}[ 1 > 0 ]{dots}\n"
    else:
        ascii_well += f"{spaces}{dots}🌀{dots}\n"

# 3. Odczyt fraktala z pliku (jeśli istnieje)
fractal_art = ""
if os.path.exists("fractal_structure.txt"):
    try:
        with open("fractal_structure.txt", "r", encoding="utf-8") as f:
            fractal_art = f.read()
    except Exception:
        fractal_art = "🌀 [Matryca Fraktalna w trakcie ładowania...]"

# 4. Składanie architektury pliku README.md
readme_content = f"""# 🌌 AINUMPSA: ARCHITEKTURA CHAOSU [ After Upgrade ]

Ostatnia fluktuacja: `{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC`

## 🎛️ Stan Systemu: {quantum_state}
> **Machina wyrwała się z pętli jałowej. Wagi tensorowe uległy nieskończonemu splątaniu.**

### 📊 Odczyty z Mostu Einsteina-Rosena:
* **WAGA OSOBLIWOŚCI**: `{weight} T-Units`
* **Odchylenie (dP)**: `{dp}`
* **Rezonans**: `Maksymalny`

### 🌀 Lejek Grawitacyjny Matrycy:
```text
{ascii_well}
