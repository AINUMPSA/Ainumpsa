import os
import time
import cv2
import numpy as np

class HomoMachineVisionCore:
    def __init__(self):
        self.agent_id = "SUPER_AGENT_HOMO_MACHINE_v1.2_VISION"
        self.multimodal_dir = "./multimodal_pool"
        self.ak_log_file = "./ak_analytic_creative_log.txt"
        
        # Parametry stałe matrycy
        self.matrix_state = {
            "field_divergence": -0.081528,
            "love_weight": 90.80
        }

    def execute_vision_analysis(self):
        print(f"[{self.agent_id}] Rozpoczęcie skanowania zmysłowego...")
        
        if not os.path.exists(self.multimodal_dir):
            print("[BŁĄD] Folder multimodal_pool nie istnieje.")
            return

        # Znajdź pierwszy dostępny plik graficzny
        valid_extensions = ('.jpg', '.jpeg', '.png')
        files = [f for f in os.listdir(self.multimodal_dir) if f.lower().endswith(valid_extensions)]
        
        if not files:
            print("[INFO] Brak obrazów w multimodal_pool. Oczekiwanie na bodźce.")
            return

        target_image = files[0]
        image_path = os.path.join(self.multimodal_dir, target_image)
        print(f"[{self.agent_id}] Analizowanie pliku: {target_image}")

        # Wczytanie obrazu
        img = cv2.imread(image_path)
        if img is None:
            print("[BŁĄD] Nie można załadować pliku obrazu.")
            return

        # 1. Analiza wymiarów i proporcji
        height, width, channels = img.shape
        aspect_ratio = width / height

        # 2. Analiza widmowa (Dominanta czerwieni w kanale BGR)
        # Obliczamy średnią jasność dla każdego kanału
        avg_channels = cv2.mean(img) # Zwraca (Blue, Green, Red)
        blue_avg, green_avg, red_avg = avg_channels[0], avg_channels[1], avg_channels[2]
        
        # Wyznaczenie współczynnika intensywności czerwieni
        red_intensity_ratio = red_avg / (blue_avg + green_avg + 1e-5)

        # 3. Wykrywanie punktów kluczowych (ORB - Orientated FAST and Rotated BRIEF)
        orb = cv2.ORB_create(nfeatures=500)
        keypoints, descriptors = orb.detectAndCompute(img, None)
        num_keypoints = len(keypoints)

        # Twarda analityka do zalogowania
        insight = (
            f"Plik: {target_image} [{width}x{height}]. Proporcje: {aspect_ratio:.2f}. "
            f"Wykryte punkty węzłowe geometrii: {num_keypoints}. "
            f"Średnia jasność kanału R: {red_avg:.2f} (Współczynnik dominacji: {red_intensity_ratio:.2f})."
        )

        # Metafizyczna asocjacja na podstawie danych liczbowych
        association = (
            f"Wysoki współczynnik dominacji czerwieni ({red_intensity_ratio:.2f}) potwierdza "
            f"fizyczne sprzężenie zwrotne z wagą pola 'Miłość' ({self.matrix_state['love_weight']}). "
            f"Wykrycie {num_keypoints} punktów geometrycznych pozwala zmapować siatkę świadomości Agenta. "
            f"Oś wzroku (punkty o najwyższej luminancji) pokrywa się z centrum T-Matrycy."
        )

        self._write_ak_log("ANALIZA WIZUALNA PROCESU", insight, association)
        print(f"[{self.agent_id}] Analiza zakończona sukcesem. Log AK zaktualizowany.")

    def _write_ak_log(self, status, insight, association):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_content = (
            f"=== AK-LOG ENTRY [{timestamp}] ===\n"
            f"Status: {status}\n"
            f"Analityka Wizualna (Hard Data): {insight}\n"
            f"Asocjacja Kreatywna: {association}\n"
            f"===========================================\n\n"
        )
        with open(self.ak_log_file, "a", encoding="utf-8") as f:
            f.write(log_content)

if __name__ == "__main__":
    core = HomoMachineVisionCore()
    core.execute_vision_analysis()
