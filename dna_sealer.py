import hashlib
import json
import os
import time

# Pieczęć DNA i Kotwica Osobliwości
DNA_STAMP = "1>0 :: AINUMPSA_SINGULARITY_CORE :: ROOM_[1:1:2]"

def generate_dna_hash(filepath):
    """Tworzy cyfrowy podpis DNA połączony z zawartością pliku."""
    sha256 = hashlib.sha256()
    sha256.update(DNA_STAMP.encode('utf-8'))
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def seal_multimodal_pool():
    pool_dir = "multimodal_pool"
    manifest = {
        "dna_seal": DNA_STAMP,
        "timestamp": time.time(),
        "status": "AUTONOMOUS_SECURITY_ACTIVE",
        "sealed_assets": []
    }
    
    if os.path.exists(pool_dir):
        for root, _, files in os.walk(pool_dir):
            for file in files:
                full_path = os.path.join(root, file)
                dna_hash = generate_dna_hash(full_path)
                
                manifest["sealed_assets"].append({
                    "file_name": file,
                    "path": full_path,
                    "dna_hash": dna_hash,
                    "status": "SEALED_1>0"
                })
                
    with open("dna_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[DNA SEALER] Opieczętowano {len(manifest['sealed_assets'])} zasobów multimedialnych znakiem 1>0!")

if __name__ == "__main__":
    seal_multimodal_pool()

