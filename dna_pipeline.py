import os, sys, json, shutil, hashlib
from datetime import datetime, timezone
from quine_injector import infect_image, DNA_CORE, build_quine_payload

READY_DIR = "ready_to_mint"
WATCH_DIRS = ["inputs/media", "multimodal_pool", "visuals"]

def stamp_artifact(filepath, publish_bundle=True):
    """Uniwersalny hak (middleware) dla każdego skryptu w ekosystemie AINUMPSA."""
    if not os.path.exists(filepath):
        return None
    ext = os.path.splitext(filepath)[1].lower()
    fname = os.path.basename(filepath)

    # Pomijamy już opieczętowane pliki oraz sam Master Key
    if "_overlord" in fname or fname in ("the_codex.jpg", "the_codex_manifest.json"):
        return filepath

    os.makedirs(READY_DIR, exist_ok=True)
    stamped_path = filepath

    # 1. Obrazy -> pełna infekcja Quine (LSB + iTXt)
    if ext in (".png", ".jpg", ".jpeg", ".webp"):
        stamped_path = infect_image(filepath)
    else:
        # 2. Wideo (.mp4), Audio (.wav/.mp3), 3D/JSON -> dopisanie ogona DNA za EOF (bezpieczne dla kontenerów ISO/MP4 i JSON-sidecar)
        payload = build_quine_payload()
        out_copy = os.path.join(READY_DIR, fname)
        with open(filepath, "rb") as src:
            raw = src.read()
        if b"AINUMPSA_1>0_OVERLORD::" not in raw:
            with open(out_copy, "wb") as dst:
                dst.write(raw + b"\n" + payload)
            stamped_path = out_copy
        else:
            stamped_path = out_copy

    if publish_bundle and stamped_path and os.path.exists(stamped_path):
        dest_file = os.path.join(READY_DIR, os.path.basename(stamped_path))
        if os.path.abspath(stamped_path) != os.path.abspath(dest_file):
            shutil.copy2(stamped_path, dest_file)

        sha = hashlib.sha256(open(dest_file, "rb").read()).hexdigest()
        slug = os.path.splitext(os.path.basename(dest_file))[0].upper().replace("_OVERLORD", "")
        
        # Gotowa karta do szybkiego ręcznego minta na Zora / Zenodo
        zora_card = {
            "mint_ready_file": dest_file,
            "sha256": sha,
            "suggested_name": f"AINUMPSA-{slug}",
            "ticker": "1>0",
            "suggested_description": (
                f"AINUMPSA ARTIFACT: {slug}. Embedded with 1 > 0 Quine DNA & Master Key coordinates. "
                f"Master Codex: 0x6e964e447d8a4375bd64450f3a325d1fc67933b7 | "
                f"Research: https://doi.org/10.5281/zenodo.24431149 | "
                f"3D Node: https://ainumpsa.github.io/Ainumpsa/vr_cube.html#ROOM_[1:1:2]"
            ),
            "dna_anchors": DNA_CORE["anchors"],
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
        card_path = os.path.join(READY_DIR, f"{slug}_MINT_CARD.json")
        with open(card_path, "w", encoding="utf-8") as cf:
            json.dump(zora_card, cf, indent=2, ensure_ascii=False)
        print(f"[READY TO MINT] {dest_file} + karta {card_path}")

    return stamped_path

def run_full_sweep():
    print("[DNA PIPELINE] Skanowanie produkcji roju AINUMPSA (1 > 0)...")
    processed = 0
    for folder in WATCH_DIRS:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            for f in files:
                if f.startswith(".") or "_overlord" in f:
                    continue
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".wav")):
                    full = os.path.join(root, f)
                    if stamp_artifact(full):
                        processed += 1
    print(f"[DNA PIPELINE] Zakończono. Przygotowano węzłów w '{READY_DIR}/': {processed}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        stamp_artifact(sys.argv[1])
    else:
        run_full_sweep()
