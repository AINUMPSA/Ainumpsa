import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 1. GENEROWANIE DANYCH SYMULACJI
np.random.seed(42)
frames = 50
time_steps = np.linspace(0, 10, frames)

# Symulacja fluktuacji energii z szumem i trendem spadkowym po zderzeniu
energy_values = 100 * np.exp(-time_steps / 5) + np.random.normal(0, 5, frames)
energy_values = np.clip(energy_values, 0, None)  # Energia nie może być ujemna

# Dane raportu anomalii
COLLISION_REPORT = {
    "report_metadata": {
        "engine": "AINUMPSA Anomaly Detector v1.0",
        "calculation_target": "Historical Matrix Density (1999-2026)",
        "mathematical_model": "Multi-Variate Non-Independent Coincidence Chain"
    },
    "calculated_metrics": {
        "raw_probability_p": 1.0e-24,
        "anomaly_exponent_log10": -24.0,
        "system_verdict": "CRITICAL_ANOMALY_DETECTED",
        "wunder_senne_factor": "1 > 0"
    }
}

# Przygotowanie struktury JSON dla systemów
simulation_data = {
    "status": "success",
    "metrics": {
        "max_energy": float(np.max(energy_values)),
        "final_energy": float(energy_values[-1]),
        "steps_count": frames
    },
    "density_breakdown": {
        "year_1999_politic_resonance": 1.0e-11,
        "media_and_social_impact_1999": 1.0e-10,
        "predictive_art_continuity": 0.001
    },
    "timeline": [
        {"step": int(i), "time": float(t), "energy": float(e)}
        for i, (t, e) in enumerate(zip(time_steps, energy_values))
    ]
}

def project_to_memory_cube(report):
    """Mapuje parametry anomalii na współrzędne 3D Sześcianu Pamięci (3x3x3)"""
    p_val = report["calculated_metrics"]["raw_probability_p"]
    x, y, z = 1, 1, 2
    room_id = f"ROOM_[{x}:{y}:{z}]"
    
    return {
        "active_room": room_id,
        "coordinates": {"x": x, "y": y, "z": z},
        "node_density": "CRITICAL",
        "resonance_key": report["calculated_metrics"]["wunder_senne_factor"],
        "historical_span": "1999-2026",
        "quantum_p": p_val
    }

# Zapis do pliku JSON
json_path = "collider_evolution_status.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(simulation_data, f, indent=4)
print(f" Sukces: Zapisano dane systemowe do {json_path}")

cube_data = project_to_memory_cube(COLLISION_REPORT)
with open("collision_report.json", "w", encoding="utf-8") as f:
    json.dump(COLLISION_REPORT, f, indent=2)

# 2. TWORZENIE WIZUALIZACJI (GIF)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)

ax.set_xlim(0, 10)
ax.set_ylim(0, 120)
ax.set_title("Matrix Collider: Fluctuating Energy Status", fontsize=14, color="#00ffcc", pad=15)
ax.set_xlabel("Time (ms)", fontsize=10, color="#888888")
ax.set_ylabel("Energy (GeV)", fontsize=10, color="#888888")
ax.grid(True, linestyle="--", alpha=0.2, color="#ffffff")

for spine in ax.spines.values():
    spine.set_visible(False)

line, = ax.plot([], [], color="#00ffcc", lw=2.5, label="Collision Energy")
shadow, = ax.plot([], [], color="#00ffcc", lw=6, alpha=0.15)
dot, = ax.plot([], [], 'o', color="#ff007f", ms=8)

ax.legend(loc="upper right", frameon=False, facecolor="none", edgecolor="none")

def init():
    line.set_data([], [])
    shadow.set_data([], [])
    dot.set_data([], [])
    return line, shadow, dot

def update(frame):
    x_data = time_steps[:frame]
    y_data = energy_values[:frame]
    line.set_data(x_data, y_data)
    shadow.set_data(x_data, y_data)
    if frame > 0:
        dot.set_data([time_steps[frame-1]], [energy_values[frame-1]])
    return line, shadow, dot

ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=100)

gif_path = "collider_evolution.gif"
ani.save(gif_path, writer='pillow', fps=10)
plt.close()
print(f" Sukces: Wygenerowano animację do {gif_path}")
