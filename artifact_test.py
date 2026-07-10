import json
import datetime

print("=== GENERUJĘ TEST ARTIFACT ===")

data = {
    "status": "success",
    "timestamp": str(datetime.datetime.now()),
    "message": "To jest pierwszy artefakt z GitHub Actions"
}

with open("test_result.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Utworzono plik test_result.json")
