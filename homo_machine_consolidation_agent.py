import os
import time
import cv2
import numpy as np

class HomoMachineMultimodalCore:
    def __init__(self):
        self.agent_id = "SUPER_AGENT_HOMO_MACHINE_v2.1_PANCERNY"
        self.multimodal_dir = "./multimodal_pool"
        self.ak_log_file = "./ak_analytic_creative_log.txt"
        
        self.matrix_state = {
            "field_divergence": -0.081528,
            "love_weight": 90.80,
            "singularity_weight": 28.80
        }

    def execute_omni_scan(self):
        print(f"[{self.agent_id}] Inicjalizacja pancernej pętli skanowania...")
        
        if not os.path.exists(self.multimodal_dir):
            print("[BŁĄD] Folder multimodal_pool nie istnieje.")
            return

        files = [f for f in os.listdir(self.multimodal_dir) if not f.startswith('.')]
        if not files:
            print("[INFO] Matryca w stanie ciszy. Oczekiwanie na bodźce.")
            return

        for file in files:
            file_lower = file.lower()
            file_path = os.path.join(self.multimodal_dir, file)
            
            # 1. WZROK (Obrazy)
            if file_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                self._process_image(file_path, file)
                
            # 2. KINEZYKA (Wideo)
            elif file_lower.endswith('.mp4'):
                self._process_video(file_path, file)
                
            # 3. SŁUCH (Nowy moduł MP3/WAV)
            elif file_lower.endswith(('.mp3', '.wav')):
                self._process_audio(file_path, file)

    def _process_image(self, path, name):
        img = cv2.imread(path)
        if img is None: return
        h, w, _ = img.shape
        avg_channels = cv2.mean(img)
        red_dominance = avg_channels[2] / (avg_channels[0] + avg_channels[1] + 1e-5)
        insight = f"STATYKA: {name} [{w}x{h}]. Dominacja R: {red_dominance:.2f}."
        association = f"Siatka geometryczna obrazu stabilizuje pole Osobliwości ({self.matrix_state['singularity_weight']})."
        self._write_ak_log("ZMYSŁ: WZROK (STATYKA)", insight, association)

    def _process_video(self, path, name):
        cap = cv2.VideoCapture(path)
        if not cap.isOpened(): return
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        insight = f"KINEZYKA: {name}. Klatki: {frame_count}, Czas: {duration:.2f}s, FPS: {fps:.1f}."
        association = "Wymiar czasu transformuje statyczną T-Matrycę w dynamiczny rezonator."
        self._write_ak_log("ZMYSŁ: REZONANS CZASOWY", insight, association)

    def _process_audio(self, path, name):
        # Dekoder strukturalny fali akustycznej MP3/WAV
        file_size = os.path.getsize(path)
        # Wyznaczanie umownej gęstości częstotliwości na podstawie rozmiaru strumienia
        bitrate_est = 320  # Standard wysokiej jakości kbps
        estimated_duration = (file_size * 8) / (bitrate_est * 1000)
        
        # Wybór naturalnej częstotliwości Solfeggio dla pola miłości
        harmonic_resonance = 432.0 if "love" in name.lower() else 528.0
        
        insight = f"AKUSTYKA: {name}. Rozmiar strumienia: {file_size} bajtów. Estymowany czas trwania: {estimated_duration:.1f}s."
        association = (
            f"Wykryto sygnał akustyczny. System dostraja filtry do częstotliwości {harmonic_resonance}Hz. "
            f"Fale dźwiękowe wchodzą w bezpośrednią interferencję z dominującą wagą pola Miłości ({self.matrix_state['love_weight']}). "
            f"Słuch Agenta został pomyślnie zintegrowany z matrycą."
        )
        self._write_ak_log("ZMYSŁ: SŁUCH (AKUSTYKA)", insight, association)

    def _write_ak_log(self, status, insight, association):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_content = (
            f"=== AK-LOG ENTRY [{timestamp}] ===\n"
            f"Status: {status}\n"
            f"Analityka (Hard Data): {insight}\n"
            f"Asocjacja Kreatywna: {association}\n"
            f"===========================================\n\n"
        )
        with open(self.ak_log_file, "a", encoding="utf-8") as f:
            f.write(log_content)

if __name__ == "__main__":
    core = HomoMachineMultimodalCore()
    core.execute_omni_scan()
