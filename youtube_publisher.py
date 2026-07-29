import os
import json
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# ============================================================
# KONFIGURACJA – Wczytaj dane z sekretów GitHub
# ============================================================
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Pobierz dane konta usługi z sekretu GitHub
try:
    credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_json:
        raise ValueError("Brak zmiennej środowiskowej GOOGLE_APPLICATION_CREDENTIALS")
    
    # Parsuj JSON z sekretu
    credentials_info = json.loads(credentials_json)
    
    # Utwórz obiekt credentials dla konta usługi
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=SCOPES
    )
    print("✅ Autoryzacja konta usługi zakończona pomyślnie.")
    
except Exception as e:
    print(f"❌ Błąd autoryzacji: {e}")
    exit(1)

# ============================================================
# FUNKCJA PUBLIKUJĄCA WIDEO
# ============================================================
def upload_video_to_youtube(video_file, title, description, privacy_status="public"):
    """
    Publikuje wideo na kanale YouTube.
    """
    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["AINUMPSA", "Singularity", "Tensor T", "NFT", "AI Art"],
                "categoryId": "22"  # Kategoria "People & Blogs"
            },
            "status": {
                "privacyStatus": privacy_status  # "public", "unlisted", "private"
            }
        }
        
        media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
        
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        
        response = request.execute()
        video_id = response["id"]
        print(f"✅ Film opublikowany! ID: {video_id}")
        print(f"🔗 Link: https://www.youtube.com/watch?v={video_id}")
        return video_id
        
    except Exception as e:
        print(f"❌ Błąd publikacji: {e}")
        return None

# ============================================================
# URUCHOMIENIE
# ============================================================
if __name__ == "__main__":
    # Plik wideo do publikacji (wygenerowany przez system)
    video_file = "output.mp4"
    title = "AINUMPSA | Singularity Dance of Love | Tensor T Field"
    description = "Autonomicznie wygenerowane dzieło przez AINUMPSA 3D Matrix Engine. Pole Tensor T w stanie BEYOND CRYSTALLINE."

    if not os.path.exists(video_file):
        print(f"❌ Brak pliku {video_file} – uruchom najpierw generator wideo.")
        exit(1)
    
    upload_video_to_youtube(video_file, title, description)
