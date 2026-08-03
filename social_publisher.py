import os
import json
from datetime import datetime

print("[START] Generowanie raportu stanu...")

# 1. Wczytaj dane z systemu
data = {}
if os.path.exists("tensor_t_logs.json"):
    with open("tensor_t_logs.json", "r") as f:
        data = json.load(f)

# 2. Wczytaj rezonans (jeśli istnieje)
resonance = "0.0"
if os.path.exists("collision_report.json"):
    with open("collision_report.json", "r") as f:
        collision = json.load(f)
        resonance = collision.get("resonance", "0.0")

# 3. Wygeneruj raport
report = f"""
========================================
RAPORT STANU AINUMPSA
========================================
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PUNKT FROZEN: {datetime.now().isoformat()}
MAP KRYSZTALICZNA: AKTYWNA
CZĘSTOTLIWOŚĆ REZONANSU: {resonance}

STAN POLA:
- max_div: {data.get('max_div', 'N/A')}
- mean_div: {data.get('mean_div', 'N/A')}
- kształt: {data.get('shape', 'N/A')}

STATUS: 1>0 LOCKED
========================================
"""

# 4. Zapisz raport
with open("status_report.txt", "w") as f:
    f.write(report)

print("[SUCCESS] Zapisano status_report.txt")
