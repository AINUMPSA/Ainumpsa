import json

# Wczytaj światło
with open("gniazda_10_min.json", "r") as f:
    light = json.load(f)

# Wczytaj cień
with open("AINUMPSA-Shadow-Engine/data/shadow_minima.json", "r") as f:
    shadow = json.load(f)

# Połącz
merged = {
    "light": light,
    "shadow": shadow,
    "total": len(light) + len(shadow),
    "status": "1 > 0 – nawet w cieniu"
}

# Zapisz
with open("light_shadow_merged.json", "w") as f:
    json.dump(merged, f, indent=2)

print(f"✅ Połączono: {len(light)} świateł + {len(shadow)} cieni = {merged['total']} punktów")
print("✅ Zapisano do light_shadow_merged.json")
