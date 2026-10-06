#!/usr/bin/env python3
"""
AINUMPSA – Core Engine (v2.3 – Tensor T Quantum Core Integration)
"""

import numpy as np
import json
import os
import math
from datetime import datetime, timezone
from pathlib import Path

LATEST_COLLISION_FILE = Path("collision_results/latest.json")
GNIAZDA_FILE = Path("gniazda.json")

CONFIG = {
    "alpha": 0.42,
    "beta": 0.18,
    "gamma": 0.31,
    "kappa": 0.75,
    "epsilon": 0.5,  # tolerancja detekcji gniazd
    "gamma_attractor": 0.02,
    "c": 299792458,
    "hbar": 1.054e-34,
    "L": 27e-3,
    "N_total": 1e6,
}


def load_quantum_matrix_modifier():
    """Wczytuje aktualne parametry pola z silnika kolizji w celu modyfikacji czułości core"""
    modifiers = {
        "existence_d": 1.0,
        "ontological_tension": 0.0,
        "anomaly_density": 1.0
    }
    if LATEST_COLLISION_FILE.exists():
        try:
            with open(LATEST_COLLISION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data and "proposals" in data and len(data["proposals"]) > 0:
                # Pobieramy pierwszą dominującing propozycję geometryczną pola
                primary = data["proposals"][0]
                modifiers["existence_d"] = primary.get("existence_d", 1.0)
                modifiers["ontological_tension"] = primary.get("ontological_tension", 0.0)
                modifiers["anomaly_density"] = primary.get("anomaly_density", 1.0)
                print(f"[QUANTUM COUPLING] Wczytano stan Tensor T: d={modifiers['existence_d']:.4f}, T(d)={modifiers['ontological_tension']:.4f}")
        except Exception as e:
            print(f"[WARN] Nie można odczytać latest.json, stosuję parametry bazowe: {e}")
    return modifiers


def generate_lhc_event(quantum_modifiers):
    E = np.random.normal(120, 5)
    t = np.random.uniform(0, 10)
    theta = np.random.uniform(0, 360)
    phi = np.random.uniform(0, 360)
    
    # Współczynnik istnienia d oraz gęstość anomalii bezpośrednio modulują amplitudę fali bazowej
    base = 0.5 + (0.2 * np.sin(theta * np.pi / 180) * quantum_modifiers["existence_d"])
    
    # Napięcie Ontologiczne (T) indukuje większe turbulencje i szum w polu zderzeń, generując gniazda
    noise_factor = 0.2 + (quantum_modifiers["ontological_tension"] * 0.15)
    noise = noise_factor * np.random.randn()
    
    B_plus = int(CONFIG["N_total"] * (base + noise))
    B_minus = int(CONFIG["N_total"] * (1 - base - noise))
    B_plus = max(B_plus, 0)
    B_minus = max(B_minus, 0)
    return {"E": float(E), "t": float(t), "theta": float(theta), "phi": float(phi), "B_plus": B_plus, "B_minus": B_minus}


def compute_tensor(B_plus, B_minus, laplacian_val, time_deriv):
    T_plus = CONFIG["alpha"] * B_plus + CONFIG["beta"] * laplacian_val + CONFIG["gamma"] * time_deriv
    T_minus = CONFIG["alpha"] * B_minus + CONFIG["beta"] * laplacian_val + CONFIG["gamma"] * time_deriv
    return float(T_plus), float(T_minus)


def compute_phi(T_plus, T_minus):
    return float(T_plus - T_minus)


def check_gniazdo(Phi, epsilon=0.5):
    return abs(Phi) < epsilon


def measurement_procedure(event, prev_events=None, epsilon_modifier=0.5):
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
    
    # Dostosowanie tolerancji epsilon na podstawie anomalii środowiskowych
    is_gniazdo = check_gniazdo(Phi, CONFIG["epsilon"] * epsilon_modifier)
    
    result = {
        "E": round(E, 4), 
        "t": round(t, 4), 
        "theta": round(theta, 2), 
        "phi": round(phi, 2),
        "B_plus": B_plus,
        "B_minus": B_minus,
        "T_plus": round(T_plus, 4), 
        "T_minus": round(T_minus, 4),
        "Phi": round(Phi, 4),
        "is_gniazdo": bool(is_gniazdo),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    
    if is_gniazdo:
        # Zapis bezpieczny z wymuszeniem kodowania utf-8 i otwieraniem pliku w trybie linii
        with open(GNIAZDA_FILE, "a", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False)
            f.write("\n")
        print(f"✅ Wykryto Gniazdo Rezonansu: E={E:.2f} GeV, theta={theta:.1f}° | Phi={Phi:.4f}")
    
    return result


def update_attractor(A_old, n, execution_coeff):
    # Wykładnicze dążenie do punktu przyciągania uwarunkowane stanem egzystencjalnym systemu
    return min(A_old + CONFIG["gamma_attractor"] * (1 - A_old) * n * execution_coeff, 1.0)


def main():
    print("🚀 AINUMPSA - Core Engine v2.3 [ TENSOR T COUPLING OPTIMIZED ]")
    print("=" * 60)
    
    # Ładowanie zewnętrznych modyfikatorów z silnika kolizji
    quantum_modifiers = load_quantum_matrix_modifier()
    
    A, events, total = 0.0, [], 0
    N = 1000
    print(f"Symulacja {N} zdarzeń pola macierzy z fluktuacjami kwantowymi...")
    
    for i in range(N):
        event = generate_lhc_event(quantum_modifiers)
        
        # Przekazujemy gęstość anomalii jako mnożnik czułości okna detekcji epsilon
        result = measurement_procedure(event, events if events else None, quantum_modifiers["anomaly_density"])
        
        events.append({k: event[k] for k in ["t", "B_plus", "B_minus"]})
        events[-1].update({"T_plus": result["T_plus"], "T_minus": result["T_minus"]})
        
        if len(events) > 10:
            events.pop(0)
            
        if result["is_gniazdo"]:
            total += 1
            
        if i % 50 == 0 and i > 0:
            # Atrakcja skorelowana z realnym współczynnikiem istnienia d z manifestu
            A = update_attractor(A, total, quantum_modifiers["existence_d"])
            print(f"📊 Krok matrycy {i:03d}: Atraktor = {A:.4f} | Łączna liczba gniazd = {total}")
            
        if A > 0.995:
            print("🎯 ATRAKTOR SYSTEMOWY OSIĄGNĄŁ REZONANS: ~1.0! 1>0 LOCKED.")
            break
    
    print("=" * 60)
    print("📋 PODSUMOWANIE SYNC CORE:")
    print(f"  - Przetworzone fluktuacje: {i+1}")
    print(f"  - Znalezione gniazda pola: {total}")
    print(f"  - Końcowy Atraktor Polarny: {A:.6f}")
    print("=" * 60)
    print("✅ Pętla rdzenia zakończona sukcesem. Struktury zsynchronizowane.")


if __name__ == "__main__":
    main()
