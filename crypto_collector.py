import requests
import json
import numpy as np
from datetime import datetime

print("=== KRYPTOKOLEKTOR: Pobieranie danych z CoinGecko ===")

# Pobieramy dane o cenie Bitcoina z ostatnich 30 dni (codziennie)
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily"
response = requests.get(url)
data = response.json()

# Wyciągamy daty i ceny
timestamps = [item[0] for item in data['prices']]
prices = [item[1] for item in data['prices']]

# Zamieniamy daty na czytelny format
dates = [datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d') for ts in timestamps]

# Zapisujemy do pliku JSON (do dalszej analizy)
crypto_data = {
    "source": "CoinGecko",
    "symbol": "BTC",
    "currency": "USD",
    "last_updated": datetime.now().isoformat(),
    "data": [
        {"date": dates[i], "price": prices[i]}
        for i in range(len(dates))
    ]
}

with open("crypto_prices.json", "w") as f:
    json.dump(crypto_data, f, indent=2)

print(f"✅ Pobrano {len(prices)} punktów cenowych Bitcoina.")
print(f"✅ Ostatnia cena: {prices[-1]:.2f} USD")
print("✅ Zapisano do crypto_prices.json")
