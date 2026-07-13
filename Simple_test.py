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

# Tworzymy sztuczne pole 3D z danych cenowych (używamy cen jako wartości w siatce)
# Dla uproszczenia – tworzymy siatkę 1D, która będzie reprezentować szereg czasowy
# Można to rozszerzyć do 3D, ale na początek wystarczy analiza 1D

x = np.arange(len(prices))
y = np.array(prices)

# Dla potrzeb dywergencji (która jest operatorem 3D) – przekształcamy dane na siatkę 3D
# np. powtarzamy szereg czasowy w dwóch innych wymiarach jako stałą
size = min(10, len(prices))  # ograniczamy do 10 punktów dla prostoty
prices_reduced = prices[:size]

X, Y, Z = np.meshgrid(np.arange(size), np.arange(size), np.arange(size), indexing='ij')
L = np.stack([
    np.full_like(X, prices_reduced)[..., np.newaxis],
    np.full_like(Y, prices_reduced)[..., np.newaxis],
    np.full_like(Z, prices_reduced)[..., np.newaxis]
], axis=-1).squeeze()  # upraszczamy do postaci 3D

# Liczymy dywergencję (dla uproszczenia – na danych 1D przekształconych na 3D)
# UWAGA: To tylko demonstracja – prawdziwa analiza będzie wymagać lepszego przekształcenia
dx = 1
dy = 1
dz = 1

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
