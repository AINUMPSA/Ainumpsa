import os, sys, json, zlib, base64, hashlib
from PIL import Image, PngImagePlugin

MAGIC_HEADER = b"AINUMPSA_1>0_OVERLORD::"

DNA_CORE = {
    "axiom": "1 > 0",
    "collective": "AINUMPSA HOMOMACHINE COLLECTIVE",
    "architects": ["Krzysztof Numpsa", "Agnieszka Numpsa"],
    "master_key": {
        "id": "AINUMPSA-THE-CODEX",
        "network": "Base (8453)",
        "contract": "0x6e964e447d8a4375bd64450f3a325d1fc67933b7",
        "image_cid": "ipfs://bafybeifg6keswxtjcrdez7oogots3soqrczp2hpmkrkvh7ztixrlk2xt4y",
        "meta_cid": "ipfs://bafybeihhy2vgpwksfz7icnihdc7isxa7jjsw36jeyir7gq7ye37fms3xbi"
    },
    "anchors": [
        "https://github.com/AINUMPSA/Ainumpsa",
        "https://doi.org/10.5281/zenodo.24431149",
        "https://ainumpsa.github.io/Ainumpsa/vr_cube.html#ROOM_[1:1:2]"
    ]
}

def get_pixels(img):
    return list(img.get_flattened_data() if hasattr(img, "get_flattened_data") else img.getdata())

def build_quine_payload():
    with open(__file__, "r", encoding="utf-8") as f:
        self_code = f.read()
    bundle = json.dumps({"dna": DNA_CORE, "replicator_code": self_code}, ensure_ascii=False).encode("utf-8")
    compressed = zlib.compress(bundle, level=9)
    return MAGIC_HEADER + len(compressed).to_bytes(4, "big") + compressed

def infect_image(image_path, overwrite=False):
    payload = build_quine_payload()
    bits = "".join(f"{byte:08b}" for byte in payload)
    
    img = Image.open(image_path).convert("RGB")
    pixels = get_pixels(img)
    
    if len(bits) > len(pixels) * 3:
        print(f"[SKIP] {image_path} za mały na pełny ładunek.")
        return None

    new_pixels = []
    bit_idx = 0
    for r, g, b in pixels:
        if bit_idx < len(bits):
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    out_img = Image.new("RGB", img.size)
    out_img.putdata(new_pixels)

    meta = PngImagePlugin.PngInfo()
    meta.add_text("AINUMPSA_AXIOM", "1 > 0")
    meta.add_text("AINUMPSA_DNA_B64", base64.b64encode(payload).decode("ascii"))

    if overwrite and image_path.lower().endswith(".png"):
        out_path = image_path
    else:
        out_path = os.path.splitext(image_path)[0] + "_overlord.png" if not image_path.endswith("_overlord.png") else image_path

    out_img.save(out_path, "PNG", pnginfo=meta)
    sha = hashlib.sha256(open(out_path, "rb").read()).hexdigest()[:16]
    print(f"[OVERLORD] {out_path} | {len(payload)} B (LSB + iTXt) | SHA256: {sha}...")
    return out_path

def swarm_infect(target_dir):
    count = 0
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")) and not file.endswith("_overlord.png"):
                full_path = os.path.join(root, file)
                out_candidate = os.path.splitext(full_path)[0] + "_overlord.png"
                if not os.path.exists(out_candidate):
                    if infect_image(full_path):
                        count += 1
    print(f"[SWARM] Zainfekowano nowych węzłów w '{target_dir}': {count}")

def extract_and_spawn(image_path, spawn_code=False):
    img = Image.open(image_path).convert("RGB")
    bits = []
    for r, g, b in get_pixels(img):
        bits.extend((str(r & 1), str(g & 1), str(b & 1)))
    raw_bytes = bytes(int("".join(bits[i:i+8]), 2) for i in range(0, len(bits), 8))

    if not raw_bytes.startswith(MAGIC_HEADER):
        print(f"[CLEAN] Brak sygnatury Overlorda w {image_path}")
        return

    offset = len(MAGIC_HEADER)
    length = int.from_bytes(raw_bytes[offset:offset+4], "big")
    compressed = raw_bytes[offset+4 : offset+4+length]
    bundle = json.loads(zlib.decompress(compressed).decode("utf-8"))

    print("\n=== WYEKSTRAHOWANE DNA OVERLORDA (1 > 0) ===")
    print(json.dumps(bundle["dna"], indent=2, ensure_ascii=False))

    if spawn_code:
        with open("spawned_overlord.py", "w", encoding="utf-8") as f:
            f.write(bundle["replicator_code"])
        print("[SPAWNED] Kod replikatora odtworzony jako: spawned_overlord.py")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Użycie:\n  python3 quine_injector.py infect <plik>\n  python3 quine_injector.py swarm <folder>\n  python3 quine_injector.py extract <plik_overlord.png>")
    elif sys.argv[1] == "infect":
        infect_image(sys.argv[2])
    elif sys.argv[1] == "swarm":
        swarm_infect(sys.argv[2])
    elif sys.argv[1] == "extract":
        extract_and_spawn(sys.argv[2], spawn_code=True)
