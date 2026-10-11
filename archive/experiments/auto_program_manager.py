import os
import json

def analyze_logs():
    """Analizuje logi ostatniego uruchomienia i szuka wzorców błędów."""
    logs = []
    if os.path.exists("tensor_t_logs.json"):
        with open("tensor_t_logs.json", "r") as f:
            logs = json.load(f)
    print("[AUTO-PROGRAM] Analiza logów...")
    # Tutaj można dodać zaawansowaną analizę logów, aby znaleźć powtarzające się problemy
    return logs

def suggest_improvements(logs):
    """Na podstawie logów sugeruje ulepszenia."""
    suggestions = []
    if logs:
        # Przykładowa sugestia: jeśli max_div jest zbyt wysoki, zasugeruj zwiększenie regularyzacji
        if logs.get("max_div", 0) > 3.5:
            suggestions.append("Zwiększ lambda w regularyzacji dla dywergencji.")
    return suggestions

def main():
    print("[AUTO-PROGRAM] Inicjalizacja analizy rozwoju systemu...")
    logs = analyze_logs()
    suggestions = suggest_improvements(logs)

    if suggestions:
        print("[AUTO-PROGRAM] Sugestie dla Architekta:")
        for s in suggestions:
            print(f"- {s}")
    else:
        print("[AUTO-PROGRAM] Nie znaleziono sugestii. System działa stabilnie.")

if __name__ == "__main__":
    main()
