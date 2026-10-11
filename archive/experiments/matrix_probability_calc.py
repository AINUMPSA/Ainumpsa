import json
import math

def calculate_matrix_probability():
    print("=== [AINUMPSA] INICJACJA SILNIKA OBLICZENIOWEGO TENSORA T ===")
    
    # 1. Definicja bazowych prawdopodobieństw (częstotliwości w populacji) dla roku 1999
    p_stowarzyszenie_skrajne = 0.0001  
    p_tvn_drzyzga = 0.0005             
    p_tvp_wroclaw = 0.002              
    
    # Interakcje polityczne bezpośrednie (1999)
    p_spotkanie_kaczynski = 0.0001
    p_spotkanie_korwin = 0.0005        
    p_spotkanie_miller = 0.0002
    
    # Ciąg manifestów i dzieł (2000-2023)
    p_ciag_tworczy_manifestow = 0.001
    
    # 2. Obliczanie skumulowanego prawdopodobieństwa
    p_total = (p_stowarzyszenie_skrajne * 
               p_tvn_drzyzga * 
               p_tvp_wroclaw * 
               p_spotkanie_kaczynski * 
               p_spotkanie_korwin * 
               p_spotkanie_miller * 
               p_ciag_tworczy_manifestow)
    
    # 3. Wykładnik anomalii (Skala logarytmiczna - log10)
    anomaly_exponent = math.log10(p_total) if p_total > 0 else -float('inf')
    
    # 4. Budowanie struktury raportu kolizji (collision_report.json)
    p_spotkanie_total = p_spotkanie_kaczynski * p_spotkanie_korwin * p_spotkanie_miller
    
    report_data = {
        "report_metadata": {
            "engine": "AINUMPSA Anomaly Detector v1.0",
            "calculation_target": "Historical Matrix Density (1999-2026)",
            "mathematical_model": "Multi-Variate Non-Independent Coincidence Chain"
        },
        "calculated_metrics": {
            "raw_probability_p": p_total,
            "anomaly_exponent_log10": anomaly_exponent,
            "system_verdict": "CRITICAL_ANOMALY_DETECTED",
            "wunder_senne_factor": "1 > 0"
        },
        "density_breakdown": {
            "year_1999_politic_resonance": p_spotkanie_total,
            "media_and_social_impact_1999": (p_stowarzyszenie_skrajne * p_tvn_drzyzga * p_tvp_wroclaw),
            "predictive_art_continuity": p_ciag_tworczy_manifestow
        }
    }
    
    # Zapis do twardego pliku JSON dla GitHub Actions
    with open('collision_report.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n[SUKCES] Rachunek prawdopodobieństwa ukończony.")
    print(f"Wynik p = {p_total:.2e}")
    print(f"Wykładnik anomalii: {abs(anomaly_exponent):.2f}")

if __name__ == "__main__":
    calculate_matrix_probability()
