#!/usr/bin/env python3
"""
AINUMPSA – Collision Engine (minimal)
-------------------------------------
Wejście: najnowszy plik z knowledge_base/
Wyjście: 3 namiary (pozycje) według 3 matryc stylów
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

# === KONFIGURACJA ===
KNOWLEDGE_DIR = Path("knowledge_base")
RESULTS_DIR = Path("collision_results")
RESULTS_DIR.mkdir(exist_ok=True)

# 3 matryce stylów
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


def get_latest_input():
    """Znajdź najnowszy plik w knowledge_base/"""
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
        content = latest.name  # fallback dla obrazów / binariów

    return latest.name, content


def text_to_seed(text: str) -> int:
    """Prosty, deterministyczny seed z treści pliku"""
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)


def compute_position(style: dict, seed: int) -> dict:
    """Wylicz pozycję na podstawie stylu + seedu z wejścia"""
    # małe, deterministyczne przesunięcie zależne od treści
    angle_offset = (seed % 1000) / 1000 * 40 - 20          # ±20°
    radius_offset = ((seed // 1000) % 1000) / 1000 * 0.25 - 0.12  # ±0.12

    angle = (style["base_angle"] + angle_offset) % 360
    radius = max(0.05, min(0.95, style["base_radius"] + radius_offset))

    # siła zderzenia (0.4 – 0.95)
    strength = 0.4 + ((seed % 560) / 560) * 0.55

    return {
        "style_id": style["id"],
        "style_name": style["name"],
        "angle_deg": round(angle, 2),
        "radius": round(radius, 3),
        "type": style["type"],
        "collision_strength": round(strength, 3),
        "layer": 1 if style["type"] == "collapse" else 2
    }


def run_collision():
    print("[COLLISION ENGINE] Start")

    filename, content = get_latest_input()
    if not filename:
        print("[ERROR] Brak plików w knowledge_base/")
        return None

    print(f"[INFO] Wejście: {filename}")
    seed = text_to_seed(content if content else filename)

    proposals = []
    for style in STYLES:
        pos = compute_position(style, seed)
        pos["source"] = filename
        proposals.append(pos)

    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input_file": filename,
        "seed": seed,
        "proposals": proposals,
        "status": "ok"
    }

    # zapis
    out_name = f"collision_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    out_path = RESULTS_DIR / out_name
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # dodatkowo latest.json dla łatwego podglądu
    with open(RESULTS_DIR / "latest.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] Zapisano: {out_path}")
    print(f"[SUCCESS] Zapisano: collision_results/latest.json")
    return result


if __name__ == "__main__":
    run_collision()
