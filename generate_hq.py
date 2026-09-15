import replicate
import requests
from pathlib import Path
from PIL import Image

# Token z environment variable
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

def generate_hq(source_image, style_prompt):
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        input={
            "prompt": style_prompt,
            "image": open(source_image, "rb"),
            "strength": 0.65,
            "num_outputs": 1
        }
    )
    return output[0]
