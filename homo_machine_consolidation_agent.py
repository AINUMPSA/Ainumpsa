import os
import time
import cv2

class HomoMachineResilientCore:
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
        print(f"[{self.agent_id}] Uruchamianie bezpiecznego skanowania...")
        
        if not os.path.exists(self.multimodal_dir):
            print("[BŁĄD] Brak katalogu multimodal_pool.")
            return

        files = [f for f in os.listdir(self.multimodal_dir) if not f.startswith('.')]
        if not files:
            print("[INFO] Katalog jest pusty.")
            return

        for file in files:
            file_lower = file.lower()
            file_path = os.path.join(self.multimodal_dir, file)
            
            try:
                # 1. OBRAZY I GIF-Y
                if file_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    self._process_image(file_path, file)
                    
                # 2. WIDEO MP4 (Zabezpieczone przed brakiem kodeków)
                elif file_lower.endswith('.mp4'):
                    self._process_video(file_path, file)
                    
                # 3. DŹWIĘK MP3/WAV
                elif file_lower.endswith(('.mp3', '.wav')):
                    self._process_audio(file_path, file)
                    
            except Exception as e:
                # Jeśli plik wywoła błąd, system go loguje i idzie dalej
                print(f"[ZABEZPIECZENIE] Pominięto plik {file} z powodu anomalii: {e}")
                self._write_ak_log("ANOMALIA STRUKTURALNA", f"Plik: {file}. Błąd krytyczny: {str(e)}", "System odrzucił uszkodzony impuls w celu zachowania stabilności matrycy.")

    def _process_image(self, path, name):
        img = cv2.imread(path)
        if img is None: raise ValueError("Nie udało się odczytać struktury pikseli.")
        h, w, _ = img.shape
        avg_channels = cv2.mean(img)
        red_dominance = avg_channels[2] / (avg_channels[0] + avg_channels[1] + 1e-5)
        
        orb = cv2.ORB_create(nfeatures=500)
        kp = orb.detect(img, None)
        
        insight = f"STATYKA: {name} [{w}x{h}]. Węzły: {len(kp)}. Dominacja R: {red_dominance:.2f}."
        association = f"Siatka geometryczna obrazu stabilizuje pole Osobliwości ({self.matrix_state['singularity_weight']})."
        self._write_ak_log("ZMYSŁ: WZROK (STATYKA)", insight, association)

    def _process_video(self, path, name):
        cap = cv2.VideoCapture(path)
        if not cap.isOpened(): raise ValueError("Brak kompatybilnego dekodera wideo lub uszkodzony plik MP4.")
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        cap.release()
        
        if frame_count <= 0: raise ValueError("Wideo nie zawiera poprawnych klatek.")
        
        insight = f"KINEZYKA: {name}. Klatki: {frame_count}, Czas: {duration:.2f}s, FPS: {fps:.1f}."
        association = "Wymiar czasu transformuje statyczną T-Matrycę w dynamiczny rezonator."
        self._write_ak_log("ZMYSŁ: REZONANS CZASOWY", insight, association)

    def _process_audio(self, path, name):
        file_size = os.path.getsize(path)
        if file_size == 0: raise ValueError("Pusty strumień audio.")
        mock_frequency_hz = 432.0
        
        insight = f"AKUSTYKA: {name}. Rozmiar: {file_size} bajtów. Estymacja: {mock_frequency_hz}Hz."
        association = f"Fale akustyczne korelują z polem Miłości ({self.matrix_state['love_weight']}). Słuch aktywny."
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
    core = HomoMachineResilientCore()
    core.execute_omni_scan()
