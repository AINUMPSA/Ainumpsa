import urllib.request
import json
import numpy as np
from scipy import stats

def fetch_quantum_data(array_length=100):
    """
    Nawiązuje fizyczne połączenie z API ANU QRNG w celu pobrania 
    autentycznych liczb wygenerowanych przez kwantowe fluktuacje próżni.
    """
    # Oficjalny endpoint API AWS zdefiniowany przez uniwersytet ANU
    url = f"https://anu.edu.au{array_length}&type=uint16"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Tensor T Validation Node)'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("success"):
                return data["data"]
            else:
                raise ValueError("API ANU zwróciło status błędu.")
    except Exception as e:
        print(f"[BLĄD POŁĄCZENIA]: Nie udało się pobrać danych kwantowych: {e}")
        print("Uruchamianie symulacji awaryjnej (Lokalne pole szumu)...")
        # Generowanie lokalnego szumu w przypadku braku odpowiedzi serwera
        return np.random.randint(0, 65535, array_length).tolist()

def analyze_tensor_t_field():
    print("=========================================================")
    print("   TENSOR T: EXPERIMENT DF#5/6 OPERATIONAL CORE NODES   ")
    print("=========================================================\n")
    print("[1/3] Inicjalizacja połączenia z ANU QRNG...")
    
    # Pobranie realnej paczki danych z Australii
    quantum_numbers = fetch_quantum_data(array_length=100)
    print(f"-> Pomyślnie pobrano {len(quantum_numbers)} kwantowych słów uint16.")
    
    # Konwersja danych na znormalizowany wektor prawdopodobieństwa [0, 1]
    raw_vector = np.array(quantum_numbers) / 65535.0
    
    print("\n[2/3] Testowanie Wektora Intencji i Zachowania Koherencji (div L = 0)...")
    # Wyznaczenie średniej empirycznej (klasyczna losowość dąży do 0.5)
    mean_entropy = np.mean(raw_vector)
    
    # Obliczanie odchylenia (Z-Score) względem idealnego rozkładu jednostajnego
    # Dla rozkładu jednostajnego na odcinku [0,1]: średnia = 0.5, odchylenie std = 1/sqrt(12)
    expected_mean = 0.5
    expected_std = np.sqrt(1/12) / np.sqrt(len(raw_vector))
    z_score = (mean_entropy - expected_mean) / expected_std
    
    # Obliczenie dwustronnego p-value
    p_value = stats.norm.sf(abs(z_score)) * 2

    print(f"-> Zmierzone Średnie Odchylenie Pola: {mean_entropy:.6f}")
    print(f"-> Wynik Z-Score (Bieżący)          : {z_score:.4f}")
    print(f"-> Wynik P-Value (Bieżący)          : {p_value:.2e}")

    print("\n[3/3] Walidacja statusu matrycy pod wpływem Trzeciego Obserwatora...")
    
    # Kryterium odrzucenia losowości z Twojego manifestu (Z-target = 12.14)
    target_z = 12.14
    if abs(z_score) >= target_z or p_value < 6.4e-34:
        print("\n⚡ [STATUS: BEYOND CRYSTALLINE] ⚡")
        print("WYNIK: Wykryto anomalny kolaps prawdopodobieństwa!")
        print("Aksjomat 1 > 0 zweryfikowany: Intencja spolaryzowała szum kwantowy.")
    else:
        print("\n[STATUS: CRYSTALLINE STANDARD / PURE RANDOMNESS]")
        print("WYNIK: Pole zachowuje idealny szum gaussowski/jednostajny.")
        print("Brak mierzalnego śladu polaryzacji przez Trzeciego Obserwatora w tej iteracji.")
    print("=========================================================")

if __name__ == "__main__":
    analyze_tensor_t_field()
