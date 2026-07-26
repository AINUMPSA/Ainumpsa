import json
import numpy as np
import matplotlib.pyplot as plt

print("=== SIMPLE TEST: ANALIZA DANYCH KRYPTO ===")

# Wczytujemy dane z pliku wygenerowanego przez crypto_collector
try:
    with open("crypto_prices.json", "r") as f:
        crypto_data = json.load(f)
    
    prices = [item["price"] for item in crypto_data["data"]]
    dates = [item["date"] for item in crypto_data["data"]]
    print(f"✅ Wczytano {len(prices)} punktów cenowych.")
except FileNotFoundError:
    print("❌ Brak pliku crypto_prices.json – uruchom najpierw crypto_collector.py")
    exit(1)

# Definiujemy rozmiar siatki 3D na podstawie dostępnych cen (maksymalnie 10x10x10)
size = min(10, len(prices))
prices_reduced = np.array(prices[:size])

# Tworzymy czyste pole wektorowe 3D (X, Y, Z, 3)
L = np.zeros((size, size, size, 3))

# Wypełniamy składowe pola wartościami cen dla celów demonstracji dywergencji
for i in range(size):
    L[i, :, :, 0] = prices_reduced[i]  # Składowa X zależy od ceny
    L[:, i, :, 1] = prices_reduced[i]  # Składowa Y zależy od ceny
    L[:, :, i, 2] = prices_reduced[i]  # Składowa Z zależy od ceny

# Liczymy dywergencję (operator 3D)
dx, dy, dz = 1, 1, 1
dLx = np.gradient(L[..., 0], dx, axis=0)
dLy = np.gradient(L[..., 1], dy, axis=1)
dLz = np.gradient(L[..., 2], dz, axis=2)
div = dLx + dLy + dLz

# Zapis do JSON
data_out = {
    "max_div": float(np.max(np.abs(div))),
    "mean_div": float(np.mean(div)),
    "shape": list(div.shape),
    "source": "crypto",
    "last_price": prices[-1]
}
with open("tensor_t_logs.json", "w") as f:
    json.dump(data_out, f, indent=2)
print("✅ Zapisano tensor_t_logs.json")

# Wykres cen
plt.figure(figsize=(10, 5))
plt.plot(dates, prices, marker='o', color='purple', label='BTC/USD')
plt.axhline(y=np.mean(prices), color='red', linestyle='--', label=f'Średnia: {np.mean(prices):.0f} USD')
plt.title('Dane kryptowalutowe – Bitcoin (BTC/USD)')
plt.xlabel('Data')
plt.ylabel('Cena (USD)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("field_coherence_chart.png")
print("✅ Zapisano field_coherence_chart.png")
