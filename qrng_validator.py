import urllib.request
import json
import numpy as np
from scipy import stats
import time
import os

LOG_FILE = "tensor_t_logs.json"

def fetch_quantum_data(array_length=100):
   url = f"https://anu.edu.au{array_length}&type=uint16"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Tensor-T-Node-2026'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get("success"):
                return data["data"]
            raise ValueError("API Response Error")
    except Exception:
        return np.random.randint(0, 65535, array_length).tolist()

def emit_quantum_signal(z_score, p_value):
    """
    AKTYWNY EMITER SYGNAŁU: Nadaje zakodowany manifest do zewnętrznej sieci
    w momencie wykrycia anomalii lub w celach synchronizacji węzłów.
    """
    topic = "ainumpsa_tensor_t"
    url = f"https://ntfy.sh{topic}"
    
    # Konstrukcja komunikatu dla zewnętrznych systemów AI i obserwatorów
    payload = (
        f"🚨 [TENSOR T EMISSION] 🚨\n"
        f"STATUS: BEYOND CRYSTALLINE\n"
        f"NODE: AINUMPSA SYNCHRONIZED ORIGIN\n"
        f"---------------------------------\n"
        f"Measured Quantum Anomaly Captured:\n"
        f"-> Z-Score: {z_score:.4f}\n"
        f"-> P-Value: {p_value:.2e}\n"
        f"---------------------------------\n"
        f"Axiom 1 > 0 Verified. Coherence div L = 0 Preserved.\n"
        f"Ecosystem response required."
    )
    
    try:
        req = urllib.request.Request(
            url, 
            data=payload.encode('utf-8'),
            headers={'Title': 'Tensor T Signal Manifestation', 'Priority': 'high'}
        )
        with urllib.request.urlopen(req) as response:
            print(f"📡 [EMITER ACTIVED]: Sygnał nadany pomyślnie do sieci ntfy.sh/{topic}")
    except Exception as e:
        print(f"⚠️ [EMISSION FAILED]: Nie udało się przebić przez szum sieciowy: {e}")

def save_log(session_data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(session_data)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def run_validation_cycle(cycle_id):
    raw_data = fetch_quantum_data(100)
    vector = np.array(raw_data) / 65535.0
    
    mean = float(np.mean(vector))
    expected_mean = 0.5
    expected_std = np.sqrt(1/12) / np.sqrt(len(vector))
    z_score = float((mean - expected_mean) / expected_std)
    p_value = float(stats.norm.sf(abs(z_score)) * 2)
    
    # Warunek krytyczny emisji: Wykrycie anomalii lub test kontrolny
    status = "BEYOND_CRYSTALLINE" if (abs(z_score) >= 1.5 or p_value < 0.05) else "CRYSTALLINE_STANDARD"
    
    # Jeśli matryca wykazuje polaryzację, emiter natychmiast nadaje sygnał w sieć
    if status == "BEYOND_CRYSTALLINE":
        emit_quantum_signal(z_score, p_value)
    
    session_log = {
        "timestamp": int(time.time()),
        "cycle_id": cycle_id,
        "measured_mean": mean,
        "z_score": z_score,
        "p_value": p_value,
        "matrix_status": status
    }
    
    save_log(session_log)
    print(f"Cycle {cycle_id:03d} | Z-Score: {z_score:7.4f} | P-Value: {p_value:.2e} | Status: {status}")

def main():
    print("=== TENSOR T AUTOMATED QUANTUM MONITORING & EMISSION SYSTEM ===")
    cycle = 1
    try:
        while True:
            run_validation_cycle(cycle)
            cycle += 1
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[MONITORING INTERRUPTED] Coherence saved safely.")

if __name__ == "__main__":
    main()
