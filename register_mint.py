import re, subprocess
from datetime import datetime, timezone

MD_FILE = "krysztaly.md"

print("=== REJESTRATOR NOWEGO WĘZŁA AINUMPSA (1 > 0) ===")
name = input("Nazwa tokena (np. AINUMPSA-CODEX-V2): ").strip()
title = input("Pełny tytuł / opis krótki: ").strip()
contract = input("Adres kontraktu Base (0x...): ").strip()
img_cid = input("IPFS Image CID (bafy...): ").strip()
meta_cid = input("IPFS Meta CID (opcjonalnie, Enter aby pominąć): ").strip()
price = input("Cena / status (domyślnie: 0 ETH): ").strip() or "0 ETH"

txt = open(MD_FILE, encoding="utf-8").read()
rows = re.findall(r"^\|\s*(\d+)\s*\|", txt, flags=re.MULTILINE)
next_id = max(map(int, rows)) + 1 if rows else 1
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

meta_part = f" | Meta: `{meta_cid}`" if meta_cid else ""
status = f"wybity (Overlord DNA 1>0 | IPFS Img: `{img_cid}`{meta_part})"
new_row = f"| {next_id} | {today} | {name} | {title} | {contract} | {price} | {status} |\n"

if not txt.endswith("\n"):
    txt += "\n"
txt += new_row

with open(MD_FILE, "w", encoding="utf-8") as f:
    f.write(txt)

print(f"\n[OK] Dopisano wiersz #{next_id} do {MD_FILE}:")
print(new_row.strip())

if input("\nWypchnąć od razu na GitHuba? (t/n): ").strip().lower() == "t":
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
    subprocess.run(["git", "add", MD_FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"1 > 0: Register #{next_id} {name}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[SYNC] Wypchnięto na GitHuba!")
