import requests
import json
from datetime import datetime

print("=== NASDAQ COLLECTOR: Pobieranie danych indeksu Nasdaq100 ===")

API_KEY = "demo"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=QQQ&apikey={API_KEY}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Inicjalizujemy zmienne domyślnymi wartościami (na wypadek braku danych)
    latest_date = "N/A"
    latest_price = 0.0

    time_series = data.get("Time Series (Daily)", {})
    if time_series:
        dates = sorted(time_series.keys(), reverse=True)
        if dates:
            latest_date = dates[0]
            latest_price = float(time_series[latest_date]["4. close"])
            print(f"✅ Cena zamknięcia Nasdaq100 (QQQ) na dzień {latest_date}: {latest_price:.2f} USD")
        else:
            print("⚠️ Brak danych w odpowiedzi API")
    else:
        print("⚠️ API nie zwróciło oczekiwanej struktury danych")

except Exception as e:
    print(f"❌ Błąd podczas pobierania danych: {e}")
    latest_date = datetime.now().strftime("%Y-%m-%d")
    latest_price = 0.0

# Zapisujemy do pliku – zawsze, nawet jeśli dane są niepełne
nasdaq_data = {
    "source": "Alpha Vantage (NASDAQ100)",
    "symbol": "QQQ",
    "currency": "USD",
    "last_updated": datetime.now().isoformat(),
    "date": latest_date,
    "close_price": latest_price,
    "status": "success" if latest_price > 0 else "no_data"
}

with open("nasdaq_price.json", "w") as f:
    json.dump(nasdaq_data, f, indent=2)

print("✅ Zapisano do nasdaq_price.json")
