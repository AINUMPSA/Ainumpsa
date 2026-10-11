import numpy as np
import json
from datetime import datetime

CONFIG = {
    "alpha": 0.42,
    "beta": 0.18,
    "gamma": 0.31,
    "N_total": 1e6,
}

def generate_lhc_event():
    E = np.random.normal(120, 5)
    t = np.random.uniform(0, 10)
    theta = np.random.uniform(0, 360)
    phi = np.random.uniform(0, 360)
    base = 0.5 + 0.2 * np.sin(theta * np.pi / 180)
    noise = 0.2 * np.random.randn()
    B_plus = int(CONFIG["N_total"] * (base + noise))
    B_minus = int(CONFIG["N_total"] * (1 - base - noise))
    B_plus = max(B_plus, 0)
    B_minus = max(B_minus, 0)
    return {
        "E": E,
        "t": t,
        "theta": theta,
        "phi": phi,
        "B_plus": B_plus,
        "B_minus": B_minus
    }

def compute_phi(event):
    B_plus = event["B_plus"]
    B_minus = event["B_minus"]
    # Uproszczony tensor T – tylko różnica
    Phi = B_plus - B_minus
    return Phi

def main():
    print("🌀 AINUMPSA – znajduję 10 minimów Phi")
    print("=" * 50)
    events = []
    N = 1000

    for i in range(N):
        event = generate_lhc_event()
        event["Phi"] = compute_phi(event)
        events.append(event)

    # Sortuj po |Phi|
    sorted_events = sorted(events, key=lambda x: abs(x["Phi"]))[:10]

    print("\n🔍 10 NAJBLIŻSZYCH ZERU:")
    print("-" * 40)
    for idx, e in enumerate(sorted_events, 1):
        print(f"{idx}. E={e['E']:.2f} GeV, theta={e['theta']:.1f}°, Phi={e['Phi']:.0f}")

    with open("gniazda_10_min.json", "w") as f:
        json.dump(sorted_events, f, indent=2)
    print("\n✅ Zapisano do gniazda_10_min.json")

if __name__ == "__main__":
    main()
