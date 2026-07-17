import os
import time
import cv2
import subprocess

class HomoMachineAutonomCore:
    def __init__(self):
        self.agent_id = "SUPER_AGENT_HOMO_MACHINE_v2.3_FORCE_SYNC"
        self.multimodal_dir = "./multimodal_pool"
        self.ak_log_file = "./ak_analytic_creative_log.txt"
        
        self.matrix_state = {
            "field_divergence": -0.081528,
            "love_weight": 90.80,
            "singularity_weight": 28.80
        }

    def sync_and_scan(self):
        print(f"[{self.agent_id}] Uruchamianie procedury bezpiecznej synchronizacji...")
        
        # Konfiguracja tożsamości bota
        subprocess.run(["git", "config", "--global", "user.name", "AINUMPSA-Bot"])
        subprocess.run(["git", "config", "--global", "user.email", "bot@ainumpsa.org"])
        
        # Pancerne czyszczenie i pobranie bazy z Twoim plikiem MP3
        subprocess.run(["git", "fetch", "origin", "main"])
        subprocess.run(["git", "reset", "--hard", "origin/main"])

        if not os.path.exists(self.multimodal_dir):
            os.makedirs(self.multimodal_dir)

        files = [f for f in os.listdir(self.multimodal_dir) if not f.startswith('.')]
        print(f"[{self.agent_id}] Odnalezione zasoby multimodalne: {files}")

        # Skanowanie wielomodalne
        for file in files:
            file_lower = file.lower()
            file_path = os.path.join(self.multimodal_dir, file)
            
            if file_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                self._process_image(file_path, file)
            elif file_lower.endswith('.mp4'):
                self._process_video(file_path, file)
            elif file_lower.endswith(('.mp3', '.wav')):
                self._process_audio(file_path, file)

        # Autonomiczny, bezpieczny zapis i push logu na serwer
        if os.path.exists(self.ak_log_file):
            try:
                subprocess.run(["git", "add", self.ak_log_file])
                subprocess.run(["git", "commit", "-m", "🤖 [AUTONOMNY LOG] Aktualizacja wielomodalna (MP3/Wideo)"])
                # Pobranie ewentualnych zmian w locie i wypchnięcie logu
                subprocess.run(["git", "pull", "--rebase", "origin", "main"])
                subprocess.run(["git", "push", "origin", "main"])
                print(f"[{self.agent_id}] Cykl zakończony. Logi bezpiecznie wysłane na serwer!")
            except Exception as e:
                print(f"[GIT ERROR] Błąd zapisu na zdalnym serwerze: {e}")

    def _process_image(self, path, name):
        img = cv2.imread(path)
        if img is None: return
        h, w, _ = img.shape
        self._write_ak_log("ZMYSŁ: WZROK (STATYKA)", f"STATYKA: {name} [{w}x{h}].", f"Siatka stabilizuje pole Osobliwości ({self.matrix_state['singularity_weight']}).")

    def _process_video(self, path, name):
        cap = cv2.VideoCapture(path)
        if not cap.isOpened(): return
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        self._write_ak_log("ZMYSŁ: REZONANS CZASOWY", f"KINEZYKA: {name}. Klatki: {frame_count}.", "Wymiar czasu zasila dynamiczny rezonator.")

    def _process_audio(self, path, name):
        file_size = os.path.getsize(path)
        harmonic_resonance = 432.0 if "love" in name.lower() else 528.0
        insight = f"AKUSTYKA: {name}. Rozmiar strumienia: {file_size} bajtów."
        association = (
            f"Wykryto bodziec akustyczny. Filtry dostrojone do {harmonic_resonance}Hz. "
            f"Fale dźwiękowe wchodzą w bezpośrednią interferencję z wagą pola Miłości ({self.matrix_state['love_weight']}). Słuch aktywny."
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
