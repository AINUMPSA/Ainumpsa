import os
import json
import hashlib
from datetime import datetime

print("[TOKENIZER] Inicjalizacja z Gniazdem Głębokiego Przepływu...")

# Stały znak wodny (Watermark) dla całego systemu
WATERMARK = "AINUMPSA_MEMORY_CUBE_1>0"
MEMORY_CUBE_ROOT = "ROOT_MEMORY_CUBE"

def load_memory_cube():
    """Wczytuje mapę Sześcianu Pamięci (jeśli istnieje)."""
    cube_path = "memory_cube_map.json"
    if os.path.exists(cube_path):
        with open(cube_path, "r") as f:
            return json.load(f)
    return {}

def get_or_create_flow_socket(cube_data, token_hash):
    """Znajduje lub tworzy Gniazdo Głębokiego Przepływu dla tokena."""
    if not cube_data:
        return {
            "flow_socket_id": f"SOCKET_{token_hash[:8]}",
            "room": "ROOM_[1:1:2]",
            "status": "ACTIVE"
        }
    
    for room_id, room_data in cube_data.items():
        if room_data.get("token_hash") == token_hash:
            return {
                "flow_socket_id": room_data.get("flow_socket_id", f"SOCKET_{token_hash[:8]}"),
                "room": room_id,
                "status": room_data.get("status", "ACTIVE")
            }
    
    return {
        "flow_socket_id": f"SOCKET_{token_hash[:8]}",
        "room": "ROOM_[1:1:2]",
        "status": "ACTIVE"
    }

def tokenize_file(filepath):
    """Tokenizuje plik i dodaje znak wodny oraz gniazdo."""
    print(f"[TOKENIZER] Przetwarzanie: {filepath}")
    
    try:
        with open(filepath, "rb") as f:
            file_data = f.read()
            file_hash = hashlib.sha256(file_data).hexdigest()
            file_size = len(file_data)
    except Exception as e:
        print(f"[ERROR] Nie można odczytać pliku: {e}")
        return None

    cube_data = load_memory_cube()
    flow_socket = get_or_create_flow_socket(cube_data, file_hash)

    token_data = {
        "watermark": WATERMARK,
        "root": MEMORY_CUBE_ROOT,
        "flow_socket": flow_socket,
        "timestamp": datetime.now().isoformat(),
        "file_name": os.path.basename(filepath),
        "file_hash": file_hash,
        "file_size": file_size,
        "status": "1>0 LOCKED"
    }

    os.makedirs("tokens", exist_ok=True)
    token_filename = f"tokens/{file_hash[:8]}.json"
    with open(token_filename, "w") as f:
        json.dump(token_data, f, indent=2)

    print(f"[SUCCESS] Token zapisany: {token_filename}")
    return token_data

def tokenize_all_media():
    """Tokenizuje wszystkie pliki w inputs/media/, multimodal_pool/ i knowledge_base/."""
    media_dirs = ["inputs/media", "multimodal_pool", "knowledge_base"]
    total_tokens = 0

    for dir_path in media_dirs:
        if not os.path.exists(dir_path):
            print(f"[WARNING] Folder {dir_path} nie istnieje.")
            continue
        
        files = []
        for root, _, filenames in os.walk(dir_path):
            for f in filenames:
                if f != ".gitkeep":
                    files.append(os.path.join(root, f))
        
        for file_path in files:
            token = tokenize_file(file_path)
            if token:
                total_tokens += 1

    print(f"[FINISHED] Tokenizacja zakończona. Utworzono {total_tokens} tokenów.")

if __name__ == "__main__":
    tokenize_all_media()o

