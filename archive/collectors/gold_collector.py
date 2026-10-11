import requests
import json
from datetime import datetime

print("=== GOLD COLLECTOR: Pobieranie danych o złocie ===")

# Pobieramy dane o złocie (XAU/USD) z ostatnich 30 dni
url = "https://api.gold-api.com/price/XAU"
response = requests.get(url)
data = response.json()

# Wyciągamy cenę i datę
price = data.get("price", 0)
timestamp = datetime.now().isoformat()

# Zapisujemy do pliku (z historią – nadpisujemy za każdym razem)
gold_data = {
    "source": "Gold-API",
    "symbol": "XAU",
    "currency": "USD",
    "last_updated": timestamp,
    "price": price
}

with open("gold_price.json", "w") as f:
    json.dump(gold_data, f, indent=2)

print(f"✅ Cena złota: {price:.2f} USD")
print("✅ Zapisano do gold_price.json")
