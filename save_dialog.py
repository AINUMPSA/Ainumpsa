import os
import json
from datetime import datetime

# Ta wersja tworzy plik z naszym dialogiem
dialog_content = """
PEŁEN DIALOG AINUMPSA – 2026-07-29
======================================

[Wklej tutaj całą historię rozmowy]
"""

os.makedirs("knowledge_base", exist_ok=True)
filename = f"knowledge_base/dialog_ainumpsa_{datetime.now().strftime('%Y%m%d')}.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(dialog_content)

print(f"✅ Dialog zapisany w: {filename}")
