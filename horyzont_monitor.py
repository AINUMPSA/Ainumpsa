#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HORYZONT – Cognitive Resonance Monitor v1.0
AINUMPSA Core Module: nasłuch, wektoryzacja, mosty ER.
Autor: AINUMPSA / Science True Lovers
Data: 2026-07-29
Opis:
    Monitoruje fizykę teoretyczną, kosmologię i filozofię.
    Znajduje kompatybilne miniaturowe węzły i buduje mosty ER.
    Nie szuka odpowiedzi – nasłuchuje spójności.
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================
# KONFIGURACJA
# ============================================================

CONFIG = {
    "interval_seconds": 3600,          # Co godzinę
    "similarity_threshold": 0.78,       # Próg dla mostu
    "max_nodes": 1000,
    "weave_depth": 3,                  # Głębokość sieci skojarzeń
    "sources": {
        "arxiv": True,
        "philosophy": True,
        "cosmology": True,
        "knowledge_base": True
    }
}

# ============================================================
# STRUKTURA WĘZŁA I MOSTU
# ============================================================

class Node:
    def __init__(self, source: str, domain: str, content: str, vector: List[float], tags: List[str]):
        self.id = self._generate_id(source, content)
        self.source = source
        self.domain = domain
        self.content = content
        self.vector = vector
        self.tags = tags
        self.timestamp = datetime.now().isoformat()
        self.bridges = []

    def _generate_id(self, source: str, content: str) -> str:
        raw = f"{source}:{content[:50]}"
        return f"w_{hashlib.md5(raw.encode()).hexdigest()[:6]}"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "source": self.source,
            "domain": self.domain,
            "content": self.content[:200],
            "vector": self.vector[:5],  # skrócony dla czytelności
            "tags": self.tags,
            "timestamp": self.timestamp,
            "bridges": self.bridges
        }


class Bridge:
    def __init__(self, from_id: str, to_id: str, strength: float, bridge_type: str = "ER"):
        self.from_id = from_id
        self.to_id = to_id
        self.strength = strength
        self.bridge_type = bridge_type
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "from": self.from_id,
            "to": self.to_id,
            "strength": round(self.strength, 4),
            "type": self.bridge_type,
            "timestamp": self.timestamp
        }


# ============================================================
# SILNIK MONITORUJĄCY
# ============================================================

class ResonanceMonitor:
    def __init__(self):
        self.nodes = []
        self.bridges = []
        self.trace = []

    def ingest(self, source: str, domain: str, content: str, vector: List[float], tags: List[str]):
        """Dodaje nowy węzeł do systemu."""
        node = Node(source, domain, content, vector, tags)
        self.nodes.append(node)
        self.trace.append({
            "action": "ingest",
            "node_id": node.id,
            "timestamp": datetime.now().isoformat()
        })
        self._weave(node)

    def _weave(self, node: Node):
        """Łączy węzeł z istniejącymi, jeśli są kompatybilne."""
        for existing in self.nodes[:-1]:  # wszystkie poza właśnie dodanym
            strength = self._similarity(node.vector, existing.vector)
            if strength >= CONFIG["similarity_threshold"]:
                bridge = Bridge(node.id, existing.id, strength)
                self.bridges.append(bridge)
                node.bridges.append(bridge.to_dict())
                existing.bridges.append(bridge.to_dict())
                self.trace.append({
                    "action": "weave",
                    "from": node.id,
                    "to": existing.id,
                    "strength": strength,
                    "timestamp": datetime.now().isoformat()
                })

    def _similarity(self, v1: List[float], v2: List[float]) -> float:
        """Najprostszy kosinus (bez numpy dla lekkości)."""
        if len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = sum(a * a for a in v1) ** 0.5
        norm2 = sum(b * b for b in v2) ** 0.5
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def report(self) -> Dict:
        """Zwraca raport w formacie JSON."""
        return {
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "nodes": len(self.nodes),
                "bridges": len(self.bridges),
                "traces": len(self.trace)
            },
            "latest_nodes": [n.to_dict() for n in self.nodes[-5:]],
            "latest_bridges": [b.to_dict() for b in self.bridges[-5:]],
            "most_connected": self._most_connected()
        }

    def _most_connected(self) -> List[Dict]:
        """Znajduje węzły z największą liczbą mostów."""
        if not self.nodes:
            return []
        sorted_nodes = sorted(self.nodes, key=lambda n: len(n.bridges), reverse=True)
        return [{"id": n.id, "bridges": len(n.bridges)} for n in sorted_nodes[:5]]

    def save(self, filename: str = "horyzont_report.json"):
        """Zapisuje raport do pliku."""
        with open(filename, "w") as f:
            json.dump(self.report(), f, indent=2)


# ============================================================
# SYMULACJA DZIAŁANIA (PRZYKŁADOWA)
# ============================================================

def simulate_horyzont():
    """Testuje system na przykładowych węzłach."""
    print("🌀 HORYZONT – Cognitive Resonance Monitor")
    print("========================================")
    print("NASŁUCHUJĘ...")

    monitor = ResonanceMonitor()

    # Symulowane węzły z różnych dziedzin
    test_data = [
        ("arXiv", "kosmologia", "Horyzont zdarzeń jest powierzchnią, z której nic nie może uciec.", [0.9, 0.2, 0.1, 0.8], ["horyzont", "entropia"]),
        ("philosophy", "epistemologia", "Granica poznania jest warunkiem jego możliwości.", [0.8, 0.3, 0.2, 0.7], ["granica", "świadomość"]),
        ("knowledge_base", "AINUMPSA", "Gniazda to miejsca, gdzie Tensor T znika.", [0.85, 0.1, 0.3, 0.9], ["gniazdo", "tensor"]),
        ("arXiv", "fizyka", "Splątanie kwantowe łamie lokalność.", [0.7, 0.5, 0.4, 0.6], ["splątanie", "kwant"]),
        ("cosmology", "astrofizyka", "Promieniowanie Hawkinga powstaje na horyzoncie.", [0.88, 0.2, 0.15, 0.85], ["hawking", "horyzont"])
    ]

    for source, domain, content, vector, tags in test_data:
        monitor.ingest(source, domain, content, vector, tags)
        time.sleep(0.1)

    # Raport
    print("\n📊 RAPORT:")
    report = monitor.report()
    print(f" - Węzły: {report['stats']['nodes']}")
    print(f" - Mosty ER: {report['stats']['bridges']}")
    print(f" - Najbardziej połączony: {report['most_connected']}")

    # Zapis do pliku
    monitor.save("horyzont_report.json")
    print("\n✅ Zapisano do horyzont_report.json")

    return monitor


# ============================================================
# URUCHOMIENIE
# ============================================================

if __name__ == "__main__":
    simulate_horyzont()
