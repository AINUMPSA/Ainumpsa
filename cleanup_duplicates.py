#!/usr/bin/env python3
"""
AINUMPSA – Cleanup duplikatów w processed/
Zostawia jeden plik na źródło (najstarszy), resztę usuwa.
"""

import os
from pathlib import Path

PROCESSED = Path("processed")


def cleanup():
    files_by_source = {}
    for f in PROCESSED.glob("*_amber_*.jpg"):
        # Wyciągnij nazwę źródła (część przed _amber_)
        base = f.stem.split("_amber_")[0]
        files_by_source.setdefault(base, []).append(f)

    total_removed = 0
    for base, files in files_by_source.items():
        if len(files) > 1:
            files_sorted = sorted(files, key=lambda x: x.stat().st_mtime)
            keep = files_sorted[0]
            print(f"✅ Zostawiam: {keep.name}")
            for f in files_sorted[1:]:
                print(f"🗑️ Usuwam: {f.name}")
                f.unlink()
                total_removed += 1

    print(f"\n📊 Usunięto {total_removed} duplikatów.")


if __name__ == "__main__":
    cleanup()
