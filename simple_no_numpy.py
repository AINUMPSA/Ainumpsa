import json

print("=== SIMPLE TEST: BEZ NUMPY ===")

# Generujemy dane testowe bez numpy
data = {
    "max_div": 3.0,
    "mean_div": 3.0,
    "shape": [20, 20, 20],
    "status": "test bez numpy"
}

with open("tensor_t_logs.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Zapisano tensor_t_logs.json")
