#!/usr/bin/env python3
"""
AINUMPSA – Collision Engine (v2 – z geometrią warstw)
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

KNOWLEDGE_DIR = Path("knowledge_base")
RESULTS_DIR = Path("collision_results")
GEOMETRY_FILE = Path("tensor_t_field_geometry.json")
RESULTS_DIR.mkdir(exist_ok=True)

STYLES = [
    {
        "id": "sovereign_impasse_expressive",
        "name": "Sovereign Impasso – Ekspresyjny",
        "base_angle": 45.0,
        "base_radius": 0.55,
        "type": "resonance"
    },
    {
        "id": "sovereign_impasse_dark",
        "name": "Sovereign Impasso – Ciemny / Dualistyczny",
        "base_angle": 225.0,
        "base_radius": 0.62,
        "type": "resonance"
    },
    {
        "id": "collapse_to_attractor",
        "name": "Kolaps Informacji do Atraktora 1>0",
        "base_angle": 0.0,
        "base_radius": 0.12,
        "type": "collapse"
    }
]


def load_geometry():
    if GEOMETRY_FILE.exists():
        with open(GEOMETRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_layer_info(radius: float, geometry: dict):
    """Dopasuj warstwę na podstawie promienia"""
    if not geometry or "layers" not in geometry:
        return {
            "layer": 2,
            "label": "Nieznana",
            "resonance_value": 0.5,
            "color_hex": "#888888"
        }

    # sortujemy warstwy od najmniejszego promienia
    layers = sorted(geometry["layers"], key=lambda x: x["radius"])
    chosen = layers[-1]  # domyślnie ostatnia

    for layer in layers:
        if radius <= layer["radius"]:
            chosen = layer
            break

    return {
        "layer": chosen["layer"],
        "label": chosen.get("label", ""),
        "resonance_value": chosen.get("resonance_value", 0.5),
        "color_hex": chosen.get("color_hex", "#888888")
    }


def get_latest_input():
    if not KNOWLEDGE_DIR.exists():
        return None, None

    files = sorted(
        [f for f in KNOWLEDGE_DIR.iterdir() if f.is_file()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    if not files:
        return None, None

    latest = files[0]
    try:
        content = latest.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        content = latest.name
    return latest.name, content


def text_to_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def compute_position(style: dict, seed: int, geometry: dict) -> dict:
    angle_offset = (seed % 1000) / 1000 * 40 - 20
    radius_offset = ((seed // 1000) % 1000) / 1000 * 0.25 - 0.12

    angle = (style["base_angle"] + angle_offset) % 360
    radius = max(0.05, min(0.95, style["base_radius"] + radius_offset))
    strength = 0.4 + ((seed % 560) / 560) * 0.55

    layer_info = get_layer_info(radius, geometry)

    return {
        "style_id": style["id"],
        "style_name": style["name"],
        "angle_deg": round(angle, 2),
        "radius": round(radius, 3),
        "type": style["type"],
        "collision_strength": round(strength, 3),
        "layer": layer_info["layer"],
        "layer_label": layer_info["label"],
        "resonance_value": layer_info["resonance_value"],
        "color_hex": layer_info["color_hex"]
    }


def run_collision():
    print("[COLLISION ENGINE v2] Start")

    filename, content = get_latest_input()
    if not filename:
        print("[ERROR] Brak plików w knowledge_base/")
        return None

    print(f"[INFO] Wejście: {filename}")
    seed = text_to_seed(content if content else filename)
    geometry = load_geometry()

    proposals = []
    for style in STYLES:
        pos = compute_position(style, seed, geometry)
        pos["source"] = filename
        proposals.append(pos)

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input_file": filename,
        "seed": seed,
        "proposals": proposals,
        "status": "ok"
    }

    out_name = f"collision_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    out_path = RESULTS_DIR / out_name

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    with open(RESULTS_DIR / "latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Zapisano: {out_path}")
    print(f"[SUCCESS] Zapisano: collision_results/latest.json")
    return result


if __name__ == "__main__":
    run_collision()
