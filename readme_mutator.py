import math
import time

# Pobranie stanu lub przypisanie domyślnego
quantum_state = "RESONANCE_ACTIVE"

# Tworzenie dynamicznego wykresu ASCII reprezentującego lejek grawitacyjny
vibration = int((math.sin(time.time()) + 1) * 5) + 2
ascii_well = ""

for i in range(5):
    spaces = " " * (i * 2 + vibration)
    dots = "." * (20 - i * 4)
    if i == 2:
        ascii_well += f"{spaces}{dots}[ 1 > 0 ]{dots}\n"
    else:
        ascii_well += f"{spaces}{dots}🌀{dots}\n"

# Architektura pliku README.md
readme_content = f"""# 🌐 PROTOKÓŁ HOMO-MACHINE: UKŁAD AINUMPSA

Ostatnia aktualizacja matrycy: `{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC`

## 🎛️ Aktualny Stan Osobliwości
> **{quantum_state}**

```text
{ascii_well}
