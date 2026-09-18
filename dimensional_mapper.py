#!/usr/bin/env python3
"""
AINUMPSA - Dimensional Mapper (v2)
- Generuje 27 Pokoi Pamieci (3x3x3)
- Czyta nft_ready/*.json i przypisuje NFT do Pokoi
- Zapisuje memory_cube_map.json z NFT i DNA
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

NFT_DIR = Path("nft_ready")
CUBE_FILE = Path("memory_cube_map.json")


def hash_to_coords(hash_str: str):
    """Mapuje hash na wspolrzedne 3D (0-2 kazda os)."""
    if len(hash_str) < 6:
        return (0, 0, 0)
    try:
        x = int(hash_str[0:2], 16) % 3
        y = int(hash_str[2:4], 16) % 3
        z = int(hash_str[4:6], 16) % 3
        return (x, y, z)
    except ValueError:
        return (0, 0, 0)


def collect_nfts():
    """Zbiera wszystkie NFT z nft_ready/ (bez final/)."""
    nfts = []
    if not NFT_DIR.exists():
        return nfts
    for f in NFT_DIR.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as mf:
                data = json.load(mf)
            h = data.get("hash", f.stem)
            nfts.append({
                "hash": h,
                "file": f.name,
                "source": data.get("source", "unknown"),
                "nft_count": data.get("nft_count", 0),
            })
        except Exception as e:
            print(f"[WARN] Nie mozna odczytac {f}: {e}")
    return nfts


def attach_nfts_to_rooms(rooms, nfts):
    """Przypisuje NFT do Pokoi na podstawie hasha."""
    # Inicjalizuj liste NFT w kazdym pokoju
    for room_name in rooms:
        rooms[room_name]["nfts"] = []
        rooms[room_name]["nft_total"] = 0

    # Rozdziel NFT
    for nft in nfts:
        x, y, z = hash_to_coords(nft["hash"])
        room_name = f"ROOM_[{x}:{y}:{z}]"
        if room_name in rooms:
            rooms[room_name]["nfts"].append({
                "hash": nft["hash"][:16],
                "source": nft["source"],
                "nft_count": nft["nft_count"],
            })
            rooms[room_name]["nft_total"] += nft["nft_count"]

    return rooms


def generate_cube():
    """Generuje pelna siatke 27 Pokoi z NFT."""
    print("Mapowanie 3D Szescianu Pamieci AINUMPSA...")

    rooms = {}
    for x in range(3):
        for y in range(3):
            for z in range(3):
                name = f"ROOM_[{x}:{y}:{z}]"
                if x == 1 and y == 1 and z == 2:
                    typ = "SINGULARITY_CORE"
                    resonance = "MAXIMAL_1>0"
                elif x == 1 and y == 1 and z == 1:
                    typ = "CENTER_NUCLEUS"
                    resonance = "BALANCED"
                else:
                    typ = "PERIPHERAL_NODE"
                    resonance = "STABLE"

                rooms[name] = {
                    "coordinates": {"x": x, "y": y, "z": z},
                    "type": typ,
                    "resonance": resonance,
                    "connected_neighbors": [],
                    "nfts": [],
                    "nft_total": 0,
                }

    # Dodaj polaczenia miedzy sasiadami (mostER)
    for name, info in rooms.items():
        x, y, z = info["coordinates"].values()
        neighbors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if dx == dy == dz == 0:
                        continue
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < 3 and 0 <= ny < 3 and 0 <= nz < 3:
                        neighbors.append(f"ROOM_[{nx}:{ny}:{nz}]")
        info["connected_neighbors"] = sorted(set(neighbors))

    # Dodaj NFT
    nfts = collect_nfts()
    rooms = attach_nfts_to_rooms(rooms, nfts)

    total_nft = sum(r["nft_total"] for r in rooms.values())

    data = {
        "architecture": "AINUMPSA_3D_MEMORY_CUBE",
        "dimensions": "3x3x3",
        "total_rooms": 27,
        "total_nfts": total_nft,
        "total_nft_files": len(nfts),
        "primary_singularity_anchor": "ROOM_[1:1:2]",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "rooms": rooms,
    }

    with open(CUBE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("[SUKCES] Wygenerowano pelna siatke 27 Pokoi Pamieci!")
    print(f"[INFO] Przypisano {len(nfts)} plikow NFT (lacznie {total_nft} NFT) do Pokoi")
    print(f"[INFO] Kotwica Osobliwosci: ROOM_[1:1:2]")


if __name__ == "__main__":
    generate_cube()
