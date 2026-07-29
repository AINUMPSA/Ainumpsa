#!/usr/bin/env python3
import os
import json
import hashlib
from datetime import datetime

def register_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    hash_id = hashlib.md5(content.encode()).hexdigest()[:8]
    metadata = {
        "file": filepath,
        "hash": hash_id,
        "timestamp": datetime.now().isoformat(),
        "type": "knowledge",
        "status": "active"
    }
    with open(f"{filepath}.meta", 'w') as m:
        json.dump(metadata, m, indent=2)
    print(f"✅ Zarejestrowano: {filepath} ({hash_id})")
    return metadata

if __name__ == "__main__":
    for root, dirs, files in os.walk("knowledge_base"):
        for file in files:
            if file.endswith(".txt") and not file.endswith(".meta"):
                register_file(os.path.join(root, file))
