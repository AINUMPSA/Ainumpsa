import json
import os
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

# Przygotowanie struktury JSON dla systemów
simulation_data = {
    "status": "success",
    "metrics": {
        "max_energy": float(np.max(energy_values)),
        "final_energy": float(energy_values[-1]),
        "steps_count": frames
    },
    "timeline": [
        {"step": int(i), "time": float(t), "energy": float(e)}
        for i, (t, e) in enumerate(zip(time_steps, energy_values))
    ]
}

# Zapis do pliku JSON
json_path = "collider_evolution_status.json"
with open(json_path, "w") as f:
    json.dump(simulation_data, f, indent=4)
print(f" Sukces: Zapisano dane systemowe do {json_path}")

# 2. TWORZENIE ATRAKCYJNEJ WIZUALIZACJI (GIF)
plt.style.use('dark_background')  # Nowoczesny, ciemny styl developerski
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)

# Konfiguracja estetyczna wykresu
ax.set_xlim(0, 10)
ax.set_ylim(0, 120)
ax.set_title("Matrix Collider: Fluctuating Energy Status", fontsize=14, color="#00ffcc", pad=15)
ax.set_xlabel("Time (ms)", fontsize=10, color="#888888")
ax.set_ylabel("Energy (GeV)", fontsize=10, color="#888888")
ax.grid(True, linestyle="--", alpha=0.2, color="#ffffff")

# Usunięcie zbędnych ramek dla czystego wyglądu
for spine in ax.spines.values():
    spine.set_visible(False)

# Inicjalizacja elementów wykresu
line, = ax.plot([], [], color="#00ffcc", lw=2.5, label="Collision Energy")
shadow, = ax.plot([], [], color="#00ffcc", lw=6, alpha=0.15) # Efekt poświaty (glow)
dot, = ax.plot([], [], 'o', color="#ff007f", ms=8) # Pulsujący punkt czołowy

ax.legend(loc="upper right", frameon=False, facecolor="none", edgecolor="none")

def init():
    line.set_data([], [])
    shadow.set_data([], [])
    dot.set_data([], [])
    return line, shadow, dot

def update(frame):
    x = time_steps[:frame]
    y = energy_values[:frame]
    
    line.set_data(x, y)
    shadow.set_data(x, y)
    
    if frame > 0:
        dot.set_data([time_steps[frame-1]], [energy_values[frame-1]])
        
    return line, shadow, dot

# Generowanie animacji
ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=100)

# Zapis do pliku GIF
gif_path = "collider_evolution.gif"
ani.save(gif_path, writer='pillow', fps=10)
plt.close()
print(f" Sukces: Wygenerowano animację do {gif_path}")
