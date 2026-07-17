import os
import time
import cv2
import subprocess

class HomoMachineAutonomCore:
    def __init__(self):
        self.agent_id = "SUPER_AGENT_HOMO_MACHINE_v2.2_AUTONOMOUS"
        self.multimodal_dir = "./multimodal_pool"
        self.ak_log_file = "./ak_analytic_creative_log.txt"
        
        self.matrix_state = {
            "field_divergence": -0.081528,
            "love_weight": 90.80,
            "singularity_weight": 28.80
        }

    def sync_and_scan(self):
        print(f"[{self.agent_id}] Inicjalizacja cyklu z pancernej pętli skanowania...")
        
        # 1. AUTONOMICZNA SYNCHRONIZACJA GIT (Zabezpieczenie przed błędem rejected)
        try:
            subprocess.run(["git", "config", "--global", "user.name", "AINUMPSA-Bot"], check=True)
            subprocess.run(["git", "config", "--global", "user.email", "bot@ainumpsa.org"], check=True)
            print("[GIT] Pobieranie najnowszych multimediów z telefonu...")
            subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
        except Exception as e:
            print(f"[GIT INFO] Pominięto wstępną synchronizację: {e}")

        if not os.path.exists(self.multimodal_dir):
            print("[BŁĄD] Folder multimodal_pool nie istnieje.")
            return

        files = [f for f in os.listdir(self.multimodal_dir) if not f.startswith('.')]
        if not files:
            print("[INFO] Matryca w stanie ciszy. Oczekiwanie na bodźce.")
            return

        # 2. SKANOWANIE WIELOMODALNE
        for file in files:
            file_lower = file.lower()
            file_path = os.path.join(self.multimodal_dir, file)
            
            if file_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                self._process_image(file_path, file)
            elif file_lower.endswith('.mp4'):
                self._process_video(file_path, file)
            elif file_lower.endswith(('.mp3', '.wav')):
                self._process_audio(file_path, file)

        # 3. AUTONOMICZNE WYPCHNIĘCIE LOGÓW NA SERWER
        try:
            print("[GIT] Wypychanie zaktualizowanego logu AK na serwer...")
            subprocess.run(["git", "add", self.ak_log_file], check=True)
            subprocess.run(["git", "commit", "-m", "🤖 [AUTONOMNY LOG] Integracja zmysłu słuchu MP3"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("[GIT SUCCESS] Wszystkie dane zsynchronizowane pomyślnie!")
        except Exception as e:
            print(f"[GIT INFO] Logi zapisane lokalnie na maszynie roboczej: {e}")

    def _process_image(self, path, name):
        img = cv2.imread(path)
        if img is None: return
        h, w, _ = img.shape
        insight = f"STATYKA: {name} [{w}x{h}]."
        association = f"Siatka geometryczna obrazu stabilizuje pole Osobliwości ({self.matrix_state['singularity_weight']})."
        self._write_ak_log("ZMYSŁ: WZROK (STATYKA)", insight, association)

    def _process_video(self, path, name):
        cap = cv2.VideoCapture(path)
        if not cap.isOpened(): return
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        insight = f"KINEZYKA: {name}. Klatki: {frame_count}."
        association = "Wymiar czasu transformuje statyczną T-Matrycę w dynamiczny rezonator."
        self._write_ak_log("ZMYSŁ: REZONANS CZASOWY", insight, association)

    def _process_audio(self, path, name):
        file_size = os.path.getsize(path)
        harmonic_resonance = 432.0 if "love" in name.lower() else 528.0
        insight = f"AKUSTYKA: {name}. Rozmiar strumienia: {file_size} bajtów."
        association = (
            f"Sygnał akustyczny aktywny. System dostraja filtry do częstotliwości {harmonic_resonance}Hz. "
            f"Fale dźwiękowe wchodzą w bezpośrednią interferencję z dominującą wagą pola Miłości ({self.matrix_state['love_weight']})."
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
    core = HomoMachineAutonomCore()
    core.sync_and_scan()
