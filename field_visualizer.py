import json
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

class FieldVisualizer:
    def __init__(self):
        self.output_image = 'matrix_field_map.png'

    def find_latest_discovery_file(self):
        # Szukamy plików wygenerowanych przez api_hunter.py
        files = glob.glob("quantum_discovery_*.json")
        if not files:
            return None
        # Zwracamy najnowszy plik na podstawie czasu modyfikacji
        return max(files, key=os.path.getmtime)

    def generate_field_art(self):
        print("=== [AINUMPSA] INICJACJA SILNIKA WIZUALIZACJI: SZTUKA MATRYCY ===")
        
        # 1. Dynamiczne pobieranie danych z najnowszego skanu
        latest_file = self.find_latest_discovery_file()
        
        if not latest_file:
            print("[OSTRZEŻENIE] Brak plików quantum_discovery_*.json. Wizualizator nie ma danych.")
            return

        print(f"[INFO] Przetwarzanie danych tensorowych z pliku: {latest_file}")
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ekstrakcja danych planetarnych do wyliczenia rezonansu
        seismic_events = data.get('seismic_events', [])
        nasa_asteroids = data.get('nasa_asteroids', [])
        
        correlations = []
        
        # Mapujemy trzęsienia ziemi na fale tensorowe
        for i, event in enumerate(seismic_events):
            if isinstance(event, dict) and "magnitude" in event:
                mag = event.get("magnitude", 5.0)
                # Normalizacja magnitudy do indeksu rezonansu (0.1 - 1.0)
                resonance = min(max(mag / 9.0, 0.1), 1.0)
                correlations.append({
                    "label": event.get("location", "Seismic Anomaly"),
                    "resonance_index": resonance
                })
                
        # Mapujemy obiekty NASA na fale tensorowe
        for i, asteroid in enumerate(nasa_asteroids):
            if isinstance(asteroid, dict) and "velocity_km_h" in asteroid:
                try:
                    vel = float(asteroid.get("velocity_km_h", 50000))
                    # Normalizacja prędkości do indeksu rezonansu
                    resonance = min(max(vel / 150000.0, 0.1), 1.0)
                except:
                    resonance = 0.5
                correlations.append({
                    "label": f"Neo: {asteroid.get('name', 'Unknown')}",
                    "resonance_index": resonance
                })

        if not correlations:
            print("Brak poprawnych anomalii do wyrenderowania. Generowanie domyślnej orbity testowej.")
            correlations = [{"label": "Eter T-Matrix (Test)", "resonance_index": 0.7}]

        # 2. Inicjalizacja płótna artystycznego (Ciemne tło kosmiczne)
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
        
        # Centralny Punkt Skupienia (Atraktor Numpsa 1999)
        ax.plot(0, 0, 'wo', markersize=15, alpha=0.9, label="Atraktor (1>0)")
        ax.plot(0, 0, 'yo', markersize=25, alpha=0.3)

        # 3. Generowanie geometrii fal dla każdej anomalii planetarnej
        colors = ['#00FFCC', '#FF007F', '#9900FF', '#CCFF00', '#0099FF']
        
        for i, corr in enumerate(correlations[:5]): # Renderujemy max 5 głównych fal dla czytelności
            score = corr.get('resonance_index', 0.5)
            label = corr.get('label', 'Wymiar')
            color = colors[i % len(colors)]
            
            # Tworzenie matematycznej orbity falowej na podstawie indeksu rezonansu
            theta = np.linspace(0, 2 * np.pi, 500)
            frequency = int(score * 15)
            amplitude = (1.0 - score) * 0.4
            
            # Promień orbity z wbudowaną sygnaturą wibracji planety/kosmosu
            r = (i + 1) * 2 + amplitude * np.sin(frequency * theta)
            
            # Rysowanie orbity (Sztuka generatywna)
            ax.plot(theta, r, color=color, linewidth=2, alpha=0.8, label=f"{label[:30]}... ({score:.2f})")
            ax.fill_between(theta, r - 0.1, r + 0.1, color=color, alpha=0.1)

        # 4. Stylizacja siatki geometrycznej
        ax.set_rticks([]) 
        ax.set_xticklabels([]) 
        ax.grid(True, color='#333333', linestyle='--')
        
        plt.title("AINUMPSA - GEOMETRIA POLA REZONANSU TENSORA T\n[SZTUKA x NAUKA]", 
                  color='white', fontsize=14, pad=20, weight='bold')
        
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=1, frameon=False)
        
        # Zapis gotowego dzieła do pliku graficznego PNG
        plt.savefig(self.output_image, bbox_inches='tight', dpi=150)
        plt.close()
        print(f"[SUKCES] Wygenerowano mapę pola na podstawie danych planetarnych i zapisano jako '{self.output_image}'.")

if __name__ == "__main__":
    visualizer = FieldVisualizer()
    visualizer.generate_field_art()
