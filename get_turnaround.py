import os
import json
import requests

# Pobierz klucz
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('KREA_API_TOKEN='):
            api_key = line.strip().split('=')[1]

files = [
    "turnaround_front.json", "turnaround_front_right.json", "turnaround_right.json", 
    "turnaround_back_right.json", "turnaround_back.json", "turnaround_back_left.json", 
    "turnaround_left.json", "turnaround_front_left.json"
]

for file in files:
    if not os.path.exists(file):
        continue
        
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            
        # Czasem plik ma dict, czasem listę
        if isinstance(data, dict):
            job_id = data.get('job_id')
        elif isinstance(data, list) and len(data) > 0:
            job_id = data[-1].get('job_id') # bierzemy ostatni
        else:
            job_id = None
            
        if job_id:
            url = f"https://api.krea.ai/jobs/{job_id}"
            res = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
            if res.status_code == 200:
                res_data = res.json()
                urls = res_data.get('result', {}).get('urls', [])
                if urls:
                    print(f"=== {file} ===")
                    print(urls[0])
    except Exception as e:
        print(f"Błąd przy {file}: {e}")
