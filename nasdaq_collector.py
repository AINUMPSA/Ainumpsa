import requests
import json
from datetime import datetime

print("=== NASDAQ COLLECTOR: Pobieranie danych indeksu Nasdaq100 ===")

# Używamy darmowego API Alpha Vantage (wymaga klucza – ale na potrzeby testu użyjemy publicznego)
# UWAGA: Wersja darmowa ma limit 5 zapytań na minutę – na razie wystarczy.
# W przyszłości warto zastąpić własnym kluczem API.

API_KEY = "demo"  # zastąp swoim kluczem, jeśli masz
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QQQ&apikey={API_KEY}"

response = requests.get(url)
data = response.json()

# Wyciągamy ostatnią cenę zamknięcia
try:
    time_series = data.get("Time Series (Daily)", {})
    dates = sorted(time_series.keys(), reverse=True)
    if dates:
        latest_date = dates[0]
        latest_price = float(time_series[latest_date]["4. close"])
    else:
        latest_price = 0
except Exception as e:
    print(f"❌ Błąd podczas przetwarzania danych: {e}")
    latest_price = 0
    latest_date = "N/A"

# Zapisujemy do pliku
nasdaq_data = {
    "source": "Alpha Vantage (NASDAQ100)",
    "symbol": "QQQ",
    "currency": "USD",
    "last_updated": datetime.now().isoformat(),
    "date": latest_date,
    "close_price": latest_price
}

with open("nasdaq_price.json", "w") as f:
    json.dump(nasdaq_data, f, indent=2)

print(f"✅ Cena zamknięcia Nasdaq100 (QQQ): {latest_price:.2f} USD")
print("✅ Zapisano do nasdaq_price.json")
