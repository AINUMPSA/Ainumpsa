import urllib.request
import json

def main():
    print("=== TENSOR T: INITIALIZATION [STATE: ACTIVE] ===")
    czesc1 = "https://qrng."
    czesc2 = "anu.edu.au/"
    czesc3 = "API/jsonI.php?length=10&type=uint16"
    url = czesc1 + czesc2 + czesc3
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AINUMPSA-Node'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            if res.get("success"):
                print("🎲 Dane kwantowe pobrane z ANU (Australia):")
                print("Matryca:", res["data"])
    except Exception as e:
        print("⚠️ Błąd fizycznego połączenia z siecią ANU:", e)

if __name__ == "__main__":
    main()
