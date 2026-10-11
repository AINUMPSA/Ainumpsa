import numpy as np
from PIL import Image
import json
import os

def analyze_image(path):
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert('L')
    arr = np.array(img)
    
    # Szukamy miejsc o najmniejszym kontraście (symulacja gniazd)
    grad = np.gradient(arr)
    laplacian = np.gradient(grad[0])[0] + np.gradient(grad[1])[1]
    
    gniazda = np.where(np.abs(laplacian) < np.std(laplacian) * 0.1)
    
    return {
        "shape": arr.shape,
        "mean": float(arr.mean()),
        "gniazda_count": int(len(gniazda[0])),
        "gniazda_positions": list(zip(gniazda[0].tolist(), gniazda[1].tolist()))[:10]
    }

if __name__ == "__main__":
    result = analyze_image("multimodal_pool/AINUMPSA chmury oil .jpg")
    if result:
        print(json.dumps(result, indent=2))
        with open("image_analysis.json", "w") as f:
            json.dump(result, f)
