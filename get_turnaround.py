import os
import json
import requests
from dna_pipeline import stamp_artifact

api_key = ""
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('KREA_API_TOKEN='):
            api_key = line.strip().split('=')[1]

files = [
    "turnaround_front.json", "turnaround_front_right.json", "turnaround_right.json",
    "turnaround_back_right.json", "turnaround_back.json", "turnaround_back_left.json",
    "turnaround_left.json", "turnaround_front_left.json"
]

os.makedirs("input_hub/pictures", exist_ok=True)

for file in files:
    if not os.path.exists(file):
        continue

    try:
        with open(file, 'r') as f:
            data = json.load(f)

        if isinstance(data, dict):
            job_id = data.get('job_id')
        elif isinstance(data, list) and len(data) > 0:
            job_id = data[-1].get('job_id')
        else:
            job_id = None

        if job_id:
            url = f"https://api.krea.ai/jobs/{job_id}"
            res = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
            if res.status_code == 200:
                res_data = res.json()
                urls = res_data.get('result', {}).get('urls', [])
                if urls:
                    img_url = urls[0]
                    base_name = os.path.splitext(file)[0]
                    raw_path = os.path.join("input_hub/pictures", f"{base_name}.png")
                    print(f"=== {file} ===\n[URL] {img_url}")
                    
                    img_res = requests.get(img_url, timeout=60)
                    if img_res.status_code == 200:
                        with open(raw_path, "wb") as out_img:
                            out_img.write(img_res.content)
                        print(f"[SAVED] {raw_path} -> Wstrzykuję DNA Overlorda...")
                        stamp_artifact(raw_path)
    except Exception as e:
        print(f"Błąd przy {file}: {e}")
