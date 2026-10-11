import numpy as np
import json

CONFIG = {"N_total": 1e6}

def generate_lhc_event():
    E = np.random.normal(120, 5)
    theta = np.random.uniform(0, 360)
    base = 0.5 + 0.2 * np.sin(theta * np.pi / 180)
    noise = 0.05 * np.random.randn()
    B_plus = int(CONFIG["N_total"] * (base + noise))
    B_minus = int(CONFIG["N_total"] * (1 - base - noise))
    return {"E": E, "theta": theta, "B_plus": max(B_plus,0), "B_minus": max(B_minus,0)}

# Generujemy 10000 zdarzeń
events = [generate_lhc_event() for _ in range(10000)]

# Obliczamy Phi dla każdego
for e in events:
    e["Phi"] = e["B_plus"] - e["B_minus"]

# Znajdujemy 10 najmniejszych Phi (najbliższych zeru)
sorted_events = sorted(events, key=lambda x: abs(x["Phi"]))[:10]

print("🔍 10 NAJBLIŻSZYCH ZERU (GNIAZDA):")
for i, e in enumerate(sorted_events):
    print(f"{i+1}. E={e['E']:.2f} GeV, theta={e['theta']:.1f}°, Phi={e['Phi']:.0f}")

# Zapisujemy do pliku
with open("gniazda_min.json", "w") as f:
    json.dump(sorted_events, f, indent=2)

print("\n✅ Zapisano do gniazda_min.json")
