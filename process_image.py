#!/usr/bin/env python3
"""
AINUMPSA – Bursztynowy procesor obrazów (v2)
- Nazwa pliku oparta na hashu (nie na timestampie)
- Sprawdza, czy plik już został przetworzony — jeśli tak, pomija
"""

import os
import sys
import json
import hashlib
from PIL import Image, ImageEnhance
from datetime import datetime, timezone

PROCESSED_DIR = "processed"


def file_hash(image_path: str) -> str:
    """Krótki hash pliku źródłowego (8 znaków)."""
    with open(image_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def already_processed(source_hash: str) -> bool:
    """Sprawdź, czy istnieje już plik z tym hashem."""
    if not os.path.isdir(PROCESSED_DIR):
        return False
    for f in os.listdir(PROCESSED_DIR):
        if f.endswith("_metadata.json"):
            try:
                with open(os.path.join(PROCESSED_DIR, f), "r", encoding="utf-8") as mf:
                    meta = json.load(mf)
                if meta.get("hash", "").startswith(source_hash):
                    return True
            except Exception:
                pass
    return False


def process_image(image_path: str, output_dir: str = PROCESSED_DIR):
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isfile(image_path):
        print(f"❌ Plik nie istnieje: {image_path}")
        return

    h = file_hash(image_path)

    # Sprawdź, czy już przetworzony
    if already_processed(h):
        print(f"⏩ Już przetworzony (hash: {h}) — pomijam: {image_path}")
        return

    base = os.path.splitext(os.path.basename(image_path))[0]
    # Nazwa pliku z hashem — deterministyczna (bez timestampu)
    output_path = os.path.join(output_dir, f"{base}_amber_{h}.jpg")
    meta_path = os.path.join(output_dir, f"{base}_metadata_{h}.json")

    # Bursztynowy filtr
    img = Image.open(image_path).convert("RGB")
    img = ImageEnhance.Color(img).enhance(1.5)
    img = ImageEnhance.Brightness(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.1)

    img.save(output_path, quality=95)

    metadata = {
        "source": image_path,
        "output": output_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hash": h,
        "status": "1 > 0 LOCKED"
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ Przetworzono: {output_path}")
    print(f"📄 Metadane: {meta_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python process_image.py input/plik.jpg")
    else:
        process_image(sys.argv[1])
