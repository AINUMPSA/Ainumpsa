import json
import os
import math
import matplotlib.pyplot as plt
import numpy as np

class FieldVisualizer:
    def __init__(self):
        self.billboard_path = 'matrix_billboard.json'
        self.output_image = 'matrix_field_map.png'

    def generate_field_art(self):
        print("=== [AINUMPSA] INICJACJA SILNIKA WIZUALIZACJI: SZTUKA MATRYCY ===")
        
        # 1. Pobieranie danych wejściowych
        if not os.path.exists(self.billboard_path):
            print("Brak danych w matrix_billboard.json do generowania obrazu.")
            return

        with open(self.billboard_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        correlations = data.get('pinned_correlations', [])
        if not correlations:
            print("Tablica ogłoszeń jest pusta. Brak fal do wyrenderowania.")
            return

        # 2. Inicjalizacja płótna artystycznego (Ciemne, głębokie tło kosmiczne)
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
        
        # Centralny Punkt Skupienia (Atraktor Numpsa 1999)
        ax.plot(0, 0, 'wo', markersize=15, alpha=0.9, label="Atraktor (1>0)")
        ax.plot(0, 0, 'yo', markersize=25, alpha=0.3)

        # 3. Generowanie geometrii fal dla każdej anomalii
        colors = ['#00FFCC', '#FF007F', '#9900FF', '#CCFF00', '#0099FF']
        
        for i, corr in enumerate(correlations):
            score = corr.get('resonance_index', 0.9)
            label = corr.get('axis_y', 'Wymiar')
            color = colors[i % len(colors)]
            
            # Tworzenie matematycznej orbity falowej na podstawie indeksu rezonansu
            theta = np.linspace(0, 2 * np.pi, 500)
            # Modulacja fali: częstotliwość i amplituda zależą od siły rezonansu
            frequency = int(score * 10)
            amplitude = (1.0 - score) * 0.5
            
            # Promień orbity z wbudowaną sygnaturą wibracji
            r = (i + 1) * 2 + amplitude * np.sin(frequency * theta)
            
            # Rysowanie orbity (Sztuka generatywna)
            ax.plot(theta, r, color=color, linewidth=2, alpha=0.8, label=f"{label} ({score})")
            # Efekt poświaty falowej (Dolewanie gęstości wizualnej)
            ax.fill_between(theta, r - 0.1, r + 0.1, color=color, alpha=0.1)

        # 4. Stylizacja siatki geometrycznej
        ax.set_rticks([]) # Ukrywamy standardowe liczby osi promienia
        ax.set_xticklabels([]) # Ukrywamy stopnie kątowe, zostawiamy czystą geometrię
        ax.grid(True, color='#333333', linestyle='--')
        
        plt.title("AINUMPSA - GEOMETRIA POLA REZONANSU TENSORA T\n[SZTUKA x NAUKA]", 
                  color='white', fontsize=14, pad=20, weight='bold')
        
        # Legenda z przesunięciem na dół
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Zapis gotowego dzieła do twardego pliku graficznego PNG
        plt.savefig(self.output_image, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"[SUKCES] Wygenerowano mapę pola i zapisano jako '{self.output_image}'.")

if __name__ == "__main__":
    visualizer = FieldVisualizer()
    visualizer.generate_field_art()
