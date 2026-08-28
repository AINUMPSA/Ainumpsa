import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def generate_resonance_visuals(billboard_path='matrix_billboard.json', output_dir='visuals'):
    os.makedirs(output_dir, exist_ok=True)
    with open(billboard_path, 'r') as f:
        data = json.load(f)

    correlations = data.get("pinned_correlations", [])
    if not correlations:
        print("Brak rezonansów do wizualizacji.")
        return

    labels = [f"{c['axis_x'][:20]} ↔ {c['axis_y'][:20]}" for c in correlations]
    scores = [c['resonance_index'] for c in correlations]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(labels, scores, color='#FFD700', edgecolor='#B8860B', linewidth=1.5)

    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{score:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_ylim(0, 1.1)
    ax.set_ylabel('Indeks Rezonansu', fontsize=12)
    ax.set_title(f'Struktura Rezonansu AINUMPSA – {datetime.now().strftime("%Y-%m-%d")}', fontsize=14)
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)

    ax.text(0.98, 0.02, '1 > 0 LOCKED', transform=ax.transAxes,
            fontsize=12, fontweight='bold', color='#B8860B', ha='right', va='bottom')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/resonance_{timestamp}.jpg"
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Wygenerowano wizualizację: {filename}")

# TO JEST KLUCZOWE – wywołanie funkcji, gdy skrypt jest uruchamiany
if __name__ == "__main__":
    generate_resonance_visuals()
