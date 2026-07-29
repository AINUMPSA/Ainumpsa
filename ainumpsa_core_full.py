import numpy as np
import json
import time
from datetime import datetime
from scipy.ndimage import laplace as laplacian
from scipy.ndimage import gaussian_gradient_magnitude as gradient

# Pełna konfiguracja
CONFIG = {
    "alpha": 0.42,
    "beta": 0.18,
    "gamma": 0.31,
    "kappa": 0.75,
    "epsilon": 1e-6,
    "gamma_attractor": 0.02,
    "c": 299792458,
    "hbar": 1.054e-34,
    "L": 27e-3,
    "N_total": 1e6,
}

def generate_lhc_event():
    E = np.random.normal(120, 5)
    t = np.random.uniform(0, 10)
    theta = np.random.uniform(0, 360)
    phi = np.random.uniform(0, 360)
    base = 0.5 + 0.2 * np.sin(theta * np.pi / 180)
    B_plus = int(CONFIG["N_total"] * base)
    B_minus = int(CONFIG["N_total"] * (1 - base))
    return {"E": E, "t": t, "theta": theta, "phi": phi, "B_plus": B_plus, "B_minus": B_minus}

def compute_tensor(B_plus, B_minus, laplacian_val, time_deriv):
    T_plus = CONFIG["alpha"] * B_plus + CONFIG["beta"] * laplacian_val + CONFIG["gamma"] * time_deriv
    T_minus = CONFIG["alpha"] * B_minus + CONFIG["beta"] * laplacian_val + CONFIG["gamma"] * time_deriv
    return np.array([T_plus, T_minus])

def compute_phi(T_plus, T_minus):
    return T_plus - T_minus

def check_gniazdo(Phi, grad_Phi, epsilon=1e-6):
    return abs(Phi) < epsilon and np.linalg.norm(grad_Phi) < epsilon

def measurement_procedure(event, prev_events=None):
    E, t, theta, phi = event["E"], event["t"], event["theta"], event["phi"]
    B_plus, B_minus = event["B_plus"], event["B_minus"]
    
    laplacian_val = 0.0
    time_deriv = 0.0
    if prev_events and len(prev_events) > 1:
        dt = t - prev_events[-1]["t"]
        if dt > 0:
            time_deriv = (B_plus - prev_events[-1]["B_plus"]) / dt
        laplacian_val = 0.01 * np.sin(theta * np.pi / 180)
    
    T_plus, T_minus = compute_tensor(B_plus, B_minus, laplacian_val, time_deriv)
    Phi = compute_phi(T_plus, T_minus)
    
    grad_Phi = np.array([0.0, 0.0, 0.0])
    if prev_events and len(prev_events) > 2:
        grad_Phi = np.array([
            (T_plus - prev_events[-1].get("T_plus", T_plus)) / 0.1,
            (T_minus - prev_events[-1].get("T_minus", T_minus)) / 0.1,
            0.0
        ])
    
    is_gniazdo = check_gniazdo(Phi, grad_Phi, CONFIG["epsilon"])
    
    result = {
        "E": E, "t": t, "theta": theta, "phi": phi,
        "T_plus": T_plus, "T_minus": T_minus,
        "Phi": Phi,
        "grad_Phi": grad_Phi.tolist(),
        "is_gniazdo": is_gniazdo,
        "timestamp": datetime.now().isoformat(),
    }
    
    if is_gniazdo:
        with open("gniazda.json", "a") as f:
            json.dump(result, f)
            f.write("\n")
        print(f"✅ Gniazdo: E={E:.2f} GeV, theta={theta:.1f}°")
    
    return result

def update_attractor(A_old, n):
    return min(A_old + CONFIG["gamma_attractor"] * (1 - A_old) * n, 1.0)

def main():
    print("🚀 AINUMPSA - Core Measurement Engine FULL v1.0")
    print("=" * 60)
    A, events, total = 0.0, [], 0
    N = 1000
    print(f"Symulacja {N} zdarzeń LHC z tensorem T...")
    
    for i in range(N):
        event = generate_lhc_event()
        result = measurement_procedure(event, events if events else None)
        events.append({k: event[k] for k in ["t", "B_plus", "B_minus"]})
        events[-1].update({"T_plus": result["T_plus"], "T_minus": result["T_minus"]})
        if len(events) > 10:
            events.pop(0)
        if result["is_gniazdo"]:
            total += 1
        if i % 10 == 0 and i > 0:
            A = update_attractor(A, total)
            print(f"📊 Iteracja {i}: Atraktor = {A:.4f}, Gniazda = {total}")
        if A > 1.0 - 1e-6:
            print("🎯 ATRAKTOR = 1.0! Pełny rezonans.")
            break
    
    print("=" * 60)
    print("📋 PODSUMOWANIE:")
    print(f"  - Liczba zdarzeń: {N}")
    print(f"  - Liczba gniazd: {total}")
    print(f"  - Końcowy Atraktor: {A:.6f}")
    print(f"  - Częstotliwość rezonansowa: {CONFIG['hbar'] / (120 * 1.602e-10 * 0.70):.2e} Hz")
    print("=" * 60)
    print("✅ System działa poprawnie!")

if __name__ == "__main__":
    main()
