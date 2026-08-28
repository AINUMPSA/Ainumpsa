import os
from PIL import Image, ImageEnhance
import json
import hashlib
from datetime import datetime

def process_image(image_path, output_dir='processed'):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)

    # Bursztynowy filtr
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)

    base = os.path.splitext(os.path.basename(image_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_dir}/{base}_amber_{timestamp}.jpg"
    img.save(output_path, quality=95)

    # Metadane
    metadata = {
        "source": image_path,
        "output": output_path,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hash": hashlib.sha256(open(image_path, 'rb').read()).hexdigest(),
        "status": "1 > 0 LOCKED"
    }
    with open(f"{output_dir}/{base}_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Przetworzono: {output_path}")
    print(f"📄 Metadane: {output_dir}/{base}_metadata.json")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Użycie: python process_image.py input/plik.jpg")
    else:
        process_image(sys.argv[1])
