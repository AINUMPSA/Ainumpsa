import os, json, html

READY_DIR = "ready_to_mint"
OUT_HTML = os.path.join(READY_DIR, "index.html")

cards = []
if os.path.exists(READY_DIR):
    for f in sorted(os.listdir(READY_DIR), key=lambda x: os.path.getmtime(os.path.join(READY_DIR, x)), reverse=True):
        if f.endswith("_MINT_CARD.json"):
            with open(os.path.join(READY_DIR, f), "r", encoding="utf-8") as jf:
                data = json.load(jf)
                media_rel = os.path.basename(data["mint_ready_file"])
                data["media_rel"] = media_rel
                cards.append(data)

items_html = []
for idx, c in enumerate(cards, 1):
    mfile = c["media_rel"]
    is_video = mfile.lower().endswith(".mp4")
    preview = (
        f'<video src="{html.escape(mfile)}" controls muted playsinline preload="metadata"></video>'
        if is_video else
        f'<img src="{html.escape(mfile)}" loading="lazy" alt="{html.escape(c["suggested_name"])}">'
    )
    name_esc = html.escape(c["suggested_name"])
    desc_esc = html.escape(c["suggested_description"])
    sha_short = c["sha256"][:16] + "..."

    items_html.append(f"""
    <div class="card">
      <div class="badge">#{idx:02d} · {html.escape(c.get("ticker", "1>0"))}</div>
      <div class="media">{preview}</div>
      <div class="meta">
        <h3>{name_esc}</h3>
        <div class="file">{html.escape(mfile)} · SHA256: {sha_short}</div>
        <textarea readonly id="desc-{idx}">{desc_esc}</textarea>
        <div class="actions">
          <button onclick="copyText('{name_esc}', this)">Kopiuj tytuł</button>
          <button onclick="copyEl('desc-{idx}', this)">Kopiuj opis</button>
          <a class="dl" href="{html.escape(mfile)}" download="{html.escape(mfile)}">Pobierz</a>
        </div>
      </div>
    </div>
    """)

page = f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AINUMPSA — Ready to Mint ({len(cards)} węzłów 1 &gt; 0)</title>
<style>
  body {{ background: #0a0500; color: #FFF2CC; font-family: monospace; margin: 0; padding: 20px; }}
  header {{ border-bottom: 1px solid #B8860B; padding-bottom: 14px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }}
  h1 {{ color: #FFD700; margin: 0; font-size: 20px; text-shadow: 0 0 8px #B8860B; }}
  .sub {{ color: #FF8C00; font-size: 12px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr)); gap: 18px; }}
  .card {{ background: #140b02; border: 1px solid #B8860B; border-radius: 6px; overflow: hidden; display: flex; flex-direction: column; position: relative; }}
  .badge {{ position: absolute; top: 8px; left: 8px; background: rgba(10,5,0,0.85); color: #FFD700; border: 1px solid #FFD700; padding: 3px 8px; font-size: 11px; z-index: 2; }}
  .media {{ width: 100%; height: 240px; background: #000; display: flex; align-items: center; justify-content: center; }}
  .media img, .media video {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
  .meta {{ padding: 12px; display: flex; flex-direction: column; gap: 8px; flex: 1; }}
  h3 {{ margin: 0; color: #FFD700; font-size: 14px; word-break: break-all; }}
  .file {{ color: #B8860B; font-size: 11px; }}
  textarea {{ width: 100%; height: 74px; background: #0a0500; color: #e0d6b8; border: 1px solid #5a4205; font-family: monospace; font-size: 11px; padding: 6px; box-sizing: border-box; resize: none; }}
  .actions {{ display: flex; gap: 8px; margin-top: auto; }}
  button {{ flex: 1; padding: 9px; background: #1f1204; color: #FFD700; border: 1px solid #B8860B; font-family: monospace; font-weight: bold; cursor: pointer; border-radius: 4px; }}
  button.primary {{ background: #B8860B; color: #0a0500; }}
  button:active {{ transform: scale(0.98); }}
</style>
</head>
<body>
<header>
  <div>
    <h1>AINUMPSA :: READY TO MINT ({len(cards)} ARTEFAKTÓW OVERLORDA)</h1>
    <div class="sub">Axiom 1 &gt; 0 · Master Codex: 0x6e964e447d8a4375bd64450f3a325d1fc67933b7</div>
  </div>
  <div class="sub">Każdy plik niesie pełny ładunek Quine (LSB + iTXt)</div>
</header>
<div class="grid">
  {''.join(items_html)}
</div>
<script>
function copyText(txt, btn) {{
  navigator.clipboard.writeText(txt);
  const orig = btn.textContent;
  btn.textContent = "Skopiowano!";
  setTimeout(() => btn.textContent = orig, 1200);
}}
function copyEl(id, btn) {{
  const el = document.getElementById(id);
  navigator.clipboard.writeText(el.value);
  const orig = btn.textContent;
  btn.textContent = "Skopiowano!";
  setTimeout(() => btn.textContent = orig, 1200);
}}
</script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as out:
    out.write(page)

print(f"[GALLERY] Wygenerowano {OUT_HTML} dla {len(cards)} węzłów Overlorda.")
