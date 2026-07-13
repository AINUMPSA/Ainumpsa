import json
import hashlib
from datetime import datetime
import os

print("=== TOKENIZATOR: Materializacja fluktuacji ===")

# Wczytujemy raport zderzeń (jeśli istnieje)
try:
    with open("collision_report.json", "r") as f:
        report = json.load(f)
except:
    print("⚠️ Brak raportu zderzeń – uruchom najpierw thought_collider.py")
    exit(0)

# Wczytujemy historię tokenów (jeśli istnieje)
tokens_file = "tokens_history.json"
tokens = []
if os.path.exists(tokens_file):
    with open(tokens_file, "r") as f:
        tokens = json.load(f)

# Generujemy nowe tokeny na podstawie silnych korelacji
new_tokens = []

for link in report.get("strong_links", []):
    # Tworzymy unikalny identyfikator tokena
    token_data = {
        "source1": link["source1"],
        "source2": link["source2"],
        "correlation": link["correlation"],
        "strength": link["strength"],
        "timestamp": report.get("timestamp", datetime.now().isoformat())
    }
    # Hash jako identyfikator
    token_id = hashlib.sha256(
        f"{token_data['source1']}{token_data['source2']}{token_data['timestamp']}".encode()
    ).hexdigest()[:8]
    
    token_data["id"] = token_id
    new_tokens.append(token_data)

# Dodajemy nowe tokeny do historii (jeśli nie istnieją)
added = 0
for token in new_tokens:
    # Sprawdzamy, czy taki token już istnieje (po hash)
    exists = any(t.get("id") == token["id"] for t in tokens)
    if not exists:
        tokens.append(token)
        added += 1

# Zapisujemy zaktualizowaną historię
with open(tokens_file, "w") as f:
    json.dump(tokens, f, indent=2)

print(f"✅ Dodano {added} nowych tokenów")
print(f"📊 Łączna liczba tokenów w historii: {len(tokens)}")

# Generujemy podsumowanie
if tokens:
    summary = {
        "total_tokens": len(tokens),
        "last_token": tokens[-1] if tokens else None,
        "sources": list(set([t["source1"] for t in tokens] + [t["source2"] for t in tokens])),
        "timestamp": datetime.now().isoformat()
    }
    with open("token_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("✅ Zapisano token_summary.json")
