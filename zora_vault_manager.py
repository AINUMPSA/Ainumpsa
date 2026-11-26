#!/usr/bin/env python3
import argparse
import glob
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone

VAULT_DIR = "zora_vault"
IMAGES_DIR = os.path.join(VAULT_DIR, "images")
CATALOG_PATH = os.path.join(VAULT_DIR, "catalog.json")
MANUAL_ITEMS_PATH = os.path.join(VAULT_DIR, "manual_zora_items.json")

CODEX_V2_ENTRY = {
    "id": "codex-variant-02",
    "title": "CODEX VARIANT 02 [1 > 0]",
    "author": "Krzysztof & Agnieszka Numpsa",
    "network": "Base Mainnet",
    "contract": "0x5facb8ef9ce24b12217e2ea36ef90894d8dfc2a8",
    "zora_url": "https://zora.co/coin/base:0x5facb8ef9ce24b12217e2ea36ef90894d8dfc2a8",
    "ipfs_cid": "bafybeidrzgwwe3oykewk5njxdz6hywrtlcg5dvjt67oah6odyyb4onehba",
    "image": "https://magic.decentralized-content.com/ipfs/bafybeidrzgwwe3oykewk5njxdz6hywrtlcg5dvjt67oah6odyyb4onehba",
    "description": "Primary Stego-Carrier & Quine DNA Master Key anchored on Base and IPFS.",
    "source": "onchain_anchor"
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def rebuild_catalog():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    manual_items = load_json(MANUAL_ITEMS_PATH, [])
    items = [CODEX_V2_ENTRY] + manual_items

    seen_files = {item.get("image") for item in items}
    card_paths = sorted(glob.glob("ready_to_mint/*_MINT_CARD.json"))
    for cp in card_paths:
        card = load_json(cp, {})
        img_path = card.get("mint_ready_file", "")
        if not img_path or not os.path.exists(img_path) or img_path in seen_files:
            continue
        seen_files.add(img_path)
        items.append({
            "id": os.path.splitext(os.path.basename(img_path))[0],
            "title": card.get("suggested_name", os.path.basename(img_path)),
            "author": "AINUMPSA HOMOMACHINE COLLECTIVE",
            "network": "Base Mainnet",
            "contract": "0x5facb8ef9ce24b12217e2ea36ef90894d8dfc2a8",
            "zora_url": card.get("zora_url", "https://zora.co/@numpsa"),
            "image": img_path,
            "sha256": card.get("sha256", ""),
            "description": card.get("suggested_description", ""),
            "source": "ready_to_mint"
        })

    catalog = {
        "axiom": "1 > 0",
        "collective": "AINUMPSA HOMOMACHINE COLLECTIVE",
        "zora_profile": "https://zora.co/@numpsa",
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "total_items": len(items),
        "items": items
    }
    save_json(CATALOG_PATH, catalog)
    print(f"[OK] Zbudowano {CATALOG_PATH} -> łączna liczba węzłów NFT: {len(items)}")

def add_nft(title, zora_url, image_src, contract="", description="", author="Krzysztof & Agnieszka Numpsa"):
    os.makedirs(IMAGES_DIR, exist_ok=True)
    if image_src.startswith("http://") or image_src.startswith("https://"):
        final_image = image_src
        digest = ""
    else:
        if not os.path.exists(image_src):
            raise FileNotFoundError(f"Nie znaleziono pliku graficznego: {image_src}")
        safe_name = os.path.basename(image_src).replace(" ", "_")
        dest_path = os.path.join(IMAGES_DIR, safe_name)
        if os.path.abspath(image_src) != os.path.abspath(dest_path):
            shutil.copy2(image_src, dest_path)
        final_image = dest_path.replace("\\", "/")
        digest = sha256_file(dest_path)

    # Wyciągnij adres kontraktu z linku Zora jeśli nie podano osobno
    if not contract and "base:" in zora_url:
        contract = zora_url.split("base:")[-1].split("?")[0].split("/")[0]

    manual_items = load_json(MANUAL_ITEMS_PATH, [])
    entry = {
        "id": f"zora-{len(manual_items) + 1:03d}",
        "title": title,
        "author": author,
        "network": "Base Mainnet",
        "contract": contract or "0x5facb8ef9ce24b12217e2ea36ef90894d8dfc2a8",
        "zora_url": zora_url,
        "image": final_image,
        "sha256": digest,
        "description": description or f"{title} — AINUMPSA HOMOMACHINE COLLECTIVE [1 > 0]",
        "added_utc": datetime.now(timezone.utc).isoformat(),
        "source": "zora_vault"
    }
    manual_items.append(entry)
    save_json(MANUAL_ITEMS_PATH, manual_items)
    print(f"[DODANO] {title} -> {final_image}")
    rebuild_catalog()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AINUMPSA Zora Vault Catalog Manager [1 > 0]")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("sync", help="Przebuduj zora_vault/catalog.json z ready_to_mint i zora_vault")

    p_add = sub.add_parser("add", help="Dodaj nowe NFT z Zora do zora_vault")
    p_add.add_argument("--title", required=True, help="Tytuł dzieła / tokena")
    p_add.add_argument("--url", required=True, help="Link do tokena na Zora (np. https://zora.co/coin/base:0x...)")
    p_add.add_argument("--img", required=True, help="Ścieżka do pliku PNG/JPG na tablecie lub URL obrazu")
    p_add.add_argument("--contract", default="", help="Adres kontraktu 0x... (opcjonalnie, wykrywa z URL)")
    p_add.add_argument("--desc", default="", help="Krótki opis dzieła")
    p_add.add_argument("--author", default="Krzysztof & Agnieszka Numpsa", help="Autor dzieła")

    args = parser.parse_args()
    if args.cmd == "add":
        add_nft(args.title, args.url, args.img, args.contract, args.desc, args.author)
    else:
        rebuild_catalog()
