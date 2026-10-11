import os
import json
import hashlib
from PIL import Image
from datetime import datetime

def analyze_image(filepath):
    """Analizuje obraz i wyciąga metadane"""
    img = Image.open(filepath)
    width, height = img.size
    mode = img.mode
    
    # Podstawowe metadane
    metadata = {
        "filename": os.path.basename(filepath),
        "width": width,
        "height": height,
        "mode": mode,
        "size_kb": os.path.getsize(filepath) / 1024,
        "timestamp": datetime.now().isoformat(),
        "hash": hashlib.md5(open(filepath, 'rb').read()).hexdigest()[:8],
        "artist": "deep_metadane",  # tutaj będzie nick
        "status": "active",
        "radiation": "outside_spacetime"  # promieniowanie poza czasoprzestrzenne
    }
    
    return metadata

if __name__ == "__main__":
    filepath = "multimodal_pool/PSX_20260730_074549.jpg"
    if os.path.exists(filepath):
        metadata = analyze_image(filepath)
        print(json.dumps(metadata, indent=2))
        
        # Zapisz metadane do pliku
        with open("multimodal_pool/PSX_20260730_074549.meta", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Metadane zapisane")
    else:
        print("❌ Plik nie istnieje")
