#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")"

cleanup() {
  echo -e "\n[1 > 0] Zatrzymuję strażnika i serwer..."
  kill $WATCHER_PID 2>/dev/null
  exit 0
}
trap cleanup SIGINT SIGTERM

LAST_STATE=""
(
  while true; do
    STATE=$(find multimodal_pool input_hub inputs/media visuals -maxdepth 3 -type f ! -name "*_overlord.*" -printf "%p:%T@\n" 2>/dev/null | sort | md5sum)
    if [ "$STATE" != "$LAST_STATE" ]; then
      LAST_STATE="$STATE"
      python3 dna_pipeline.py > /dev/null 2>&1
    fi
    sleep 3
  done
) &
WATCHER_PID=$!

echo "[1 > 0 HUB AKTYWNY] Galeria: http://localhost:8080 (Ctrl+C aby wyłączyć oba)"
python3 -m http.server 8080 --bind 127.0.0.1 -d ready_to_mint
