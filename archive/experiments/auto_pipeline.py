import os
import subprocess
import time
from datetime import datetime

def run_pipeline(input_file):
    print(f"🚀 Uruchamiam pipeline dla: {input_file}")
    subprocess.run(["python", "collision_engine.py", input_file])
    subprocess.run(["python", "process_image.py", input_file])
    subprocess.run(["python", "generate_nft.py", input_file])
    print(f"✅ Zakończono dla: {input_file}")

if __name__ == "__main__":
    # Przykład – uruchom na wszystkich plikach w input/
    for file in os.listdir("input/"):
        if file.endswith((".jpg", ".png", ".txt")):
            run_pipeline(os.path.join("input/", file))
