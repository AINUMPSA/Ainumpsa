import numpy as np
import json
import time
from datetime import datetime
from scipy.ndimage import laplacian, gradient
from scipy.optimize import minimize

# ============================================================
# KONFIGURACJA SYSTEMOWA (do kalibracji)
# ============================================================

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

# ============================================================
# SYMULACJA DANYCH LHC (ZASTĘPCZA - DO TESTÓW)
# ============================================================

def generate_lhc_event():
    E = np.random.normal(120, 5)
    t = np.random.uniform(0, 10)
    theta = np.random.uniform(0, 360)
    phi = np.random.uniform(0, 360)
    base = 0.5 + 0.2 * np.sin(theta * np.pi / 180)
    B_plus = int(CONFIG["N_total"] * base)
    B_minus = int(CONFIG["N_total"] * (1 - base))
    return {
        "E": E,
        "t": t,
        "theta": theta,
        "phi": phi,
        "B_plus": B_plus,
        "B_minus": B_minus,
    }

# ============================================================
# FUNKCJE POMIAROWE
# ============================================================

def compute_tensor(B_plus, B_minus, laplacian_val, time_deriv):
    T_plus = (CONFIG["alpha"] * B_plus + 
              CONFIG["beta"] * laplacian_val + 
              CONFIG["gamma"] * time_deriv)
    T_minus = (CONFIG["alpha"] * B_minus + 
               CONFIG["beta"] * laplacian_val + 
               CONFIG["gamma"] * time_deriv)
    return np.array([T_plus, T_minus])

def compute_phi(T_plus, T_minus):
    return T_plus - T_minus

def check_gniazdo(Phi, grad_Phi, epsilon=1e-6):
    return abs(Phi) < epsilon and np.linalg.norm(grad_Phi) < epsilon

def compute_flow_tensor(J, dx=0.01):
    N = J.shape[1]
    F = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            if nu + 1 < N and nu - 1 >= 0:
                dJ_mu = (J[mu, nu+1] - J[mu, nu-1]) / (2 * dx)
                dJ_nu = (J[nu, mu+1] - J[nu, mu-1]) / (2 * dx)
                F[mu, nu] = dJ_mu - dJ_nu
    return F

def check_continuity(J, dt=0.01, dx=0.01):
    dJ0_dt = (J[0, 1] - J[0, -1]) / (2 * dt)
    div_J = (J[1, 1] - J[1, -1]) / (2 * dx) + (J[2, 1] - J[2, -1]) / (2 * dx)
    return abs(dJ0_dt + div_J) < 1e-3

# ============================================================
# PROCEDURA POMIAROWA
# ============================================================

def measurement_procedure(event, prev_events=None):
    E = event["E"]
    t = event["t"]
    theta = event["theta"]
    phi = event["phi"]
    B_plus = event["B_plus"]
    B_minus = event["B_minus"]

    laplacian_val = 0.0
    time_deriv = 0.0
    if prev_events is not None and len(prev_events) > 1:
        dt = t - prev_events[-1]["t"]
        if dt > 0:
            time_deriv = (B_plus - prev_events[-1]["B_plus"]) / dt
        laplacian_val = 0.01 * np.sin(theta * np.pi / 180)

    T = compute_tensor(B_plus, B_minus, laplacian_val, time_deriv)
    T_plus, T_minus = T[0], T[1]

    Phi = compute_phi(T_plus, T_minus)

    grad_Phi = np.array([0.0, 0.0, 0.0])
    if prev_events is not None and len(prev_events) > 2:
        grad_Phi = np.array([
            (T_plus - prev_events[-1]["T_plus"]) / 0.1,
            (T_minus - prev_events[-1]["T_minus"]) / 0.1,
            0.0
        ])

    is_gniazdo = check_gniazdo(Phi, grad_Phi, CONFIG["epsilon"])

    result = {
        "E": E,
        "t": t,
        "theta": theta,
        "phi": phi,
        "T_plus": T_plus,
        "T_minus": T_minus,
        "Phi": Phi,
        "grad_Phi": grad_Phi.tolist(),
        "is_gniazdo": is_gniazdo,
        "timestamp": datetime.now().isoformat(),
    }

    if is_gniazdo:
        with open("gniazda.json", "a") as f:
            json.dump(result, f)
            f.write("\n")
        print(f"✅ Gniazdo znalezione: E={E:.2f} GeV, theta={theta:.1f}°")

    return result

# ============================================================
# ATRAKTOR SZEŚCIANU
# ============================================================

def update_attractor(A_old, number_of_gniazda):
    gamma = CONFIG["gamma_attractor"]
    A_new = A_old + gamma * (1 - A_old) * number_of_gniazda
    return min(A_new, 1.0)

# ============================================================
# GŁÓWNA PĘTLA SYMULACYJNA
# ============================================================

def main():
    print("🚀 AINUMPSA - Core Measurement Engine v1.0")
    print("=" * 60)
    
    A = 0.0
    events_history = []
    total_gniazda = 0

    N_events = 1000
    print(f"Symulacja {N_events} zdarzeń LHC...")

    for i in range(N_events):
        event = generate_lhc_event()
        result = measurement_procedure(event, events_history if events_history else None)
        
        events_history.append({
            "t": event["t"],
            "B_plus": event["B_plus"],
            "B_minus": event["B_minus"],
            "T_plus": result["T_plus"],
            "T_minus": result["T_minus"],
        })
        if len(events_history) > 10:
            events_history.pop(0)

        if result["is_gniazdo"]:
            total_gniazda += 1

        if i % 10 == 0 and i > 0:
            A = update_attractor(A, total_gniazda)
            print(f"📊 Iteracja {i}: Atraktor = {A:.4f}, Gniazda = {total_gniazda}")

        if A > 1.0 - 1e-6:
            print("🎯 ATRAKTOR OSIĄGNĄŁ WARTOŚĆ 1.0!")
            print("System osiągnął stan pełnego rezonansu.")
            break

    print("=" * 60)
    print("📋 PODSUMOWANIE:")
    print(f"  - Liczba zdarzeń: {N_events}")
    print(f"  - Liczba gniazd: {total_gniazda}")
    print(f"  - Końcowy Atraktor: {A:.6f}")
    print(f"  - Częstotliwość rezonansowa (z danych): {CONFIG['hbar'] / (120 * 1.602e-10 * 0.70):.2e} Hz")
    print("=" * 60)

if __name__ == "__main__":
    main()
