#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FANTOM MAPPER v1.0
AINUMPSA Core Module: wizualizacja odwróconej siły fantomowej
Autor: AINUMPSA / Science True Lovers
Data: 2026-07-30

Opis:
    Generuje obrazy mapowania struktury fantomowej w zależności od danych.
    Wzór: F_fantom = ∇ · ((Φ_lewa - Φ_prawa) / M_ER) · (1/√(-1))
    Obraz jest generowany na nowo za każdym razem – żywy rebus.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.ndimage import gaussian_filter

# ============================================================
# KONFIGURACJA
# ============================================================

CONFIG = {
    "data_source": "gniazda.json",          # główne źródło danych
    "output_dir": "multimodal_pool",        # gdzie zapisywać obrazy
    "output_prefix": "fantom_map_",         # prefiks nazwy pliku
    "resolution": 512,                     # rozdzielczość obrazu (kwadrat)
    "cmap": "plasma",                      # kolorystyka
    "smooth": 1.5,                         # wygładzenie dla lepszego efektu
}

# ============================================================
# FUNKCJE
# ============================================================

def load_data(filepath):
    """Wczytuje dane z pliku JSON – zwraca listę lub słownik."""
    if not os.path.exists(filepath):
        print(f"⚠️ Brak pliku: {filepath}. Używam danych zastępczych.")
        # Symulacja danych, gdy plik nie istnieje
        return {
            "Phi_left": np.random.randn(10).tolist(),
            "Phi_right": np.random.randn(10).tolist(),
            "MER": 0.7 + 0.1 * np.random.randn()
        }
    with open(filepath, "r") as f:
        try:
            data = json.load(f)
            # Jeśli to lista, weź ostatni element
            if isinstance(data, list):
                data = data[-1] if data else {}
            return data
        except json.JSONDecodeError:
            print(f"⚠️ Błąd odczytu JSON w {filepath}. Używam danych zastępczych.")
            return {
                "Phi_left": np.random.randn(10).tolist(),
                "Phi_right": np.random.randn(10).tolist(),
                "MER": 0.7 + 0.1 * np.random.randn()
            }


def compute_fantom_field(phi_left, phi_right, mer, resolution=512):
    """
    Tworzy pole 2D dla siły fantomowej.
    Wzór: F_fantom = ∇ · ((Φ_lewa - Φ_prawa) / M_ER) · (1/√(-1))
    """
    # Oblicz różnicę
    diff = np.array(phi_left) - np.array(phi_right)
    if len(diff) == 0:
        diff = np.random.randn(resolution, resolution)
    
    # Przekształć do macierzy 2D (jeśli to lista 1D, stwórz pole)
    if diff.ndim == 1:
        # Jeśli mamy za mało punktów, interpolujemy
        if len(diff) < 4:
            diff = np.random.randn(resolution, resolution)
        else:
            # Wypełnij pole wartościami
            size = int(np.sqrt(len(diff)))
            if size * size < len(diff):
                size += 1
            padded = np.pad(diff, (0, size*size - len(diff)), mode='wrap')
            field = padded.reshape(size, size)
            # Przeskaluj do rozdzielczości
            from scipy.ndimage import zoom
            scale = resolution / size
            field = zoom(field, scale, order=1)
    else:
        field = diff
    
    # Wytnij do rozdzielczości
    if field.shape[0] != resolution or field.shape[1] != resolution:
        from scipy.ndimage import zoom
        scale_x = resolution / field.shape[0]
        scale_y = resolution / field.shape[1]
        field = zoom(field, (scale_x, scale_y), order=1)
    
    # Normalizacja
    field = (field - np.mean(field)) / (np.std(field) + 1e-10)
    
    # Oblicz gradient (∇ ·)
    grad_x = np.gradient(field, axis=0)
    grad_y = np.gradient(field, axis=1)
    div = grad_x + grad_y
    
    # Podziel przez M_ER
    mer = mer if mer != 0 else 0.7
    div = div / mer
    
    # Pomnóż przez (1/√(-1)) czyli -i → obrót fazowy
    # Dla wizualizacji używamy wartości zespolonej
    fantom = div * 1j  # urojona część
    
    return np.abs(fantom)  # moduł do wizualizacji


def generate_image(fantom_field, timestamp=None):
    """Generuje obraz z pola fantomowego."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Przygotuj figurę
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Wygładź pole
    smoothed = gaussian_filter(fantom_field, sigma=CONFIG["smooth"])
    
    # Wyświetl
    im = ax.imshow(smoothed, cmap=CONFIG["cmap"], origin='lower')
    ax.set_title(f"Mapa Siły Fantomowej\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    ax.axis('off')
    
    # Dodaj kolorową legendę
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('|Siła Fantomowa|')
    
    # Zapisz
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    filename = f"{CONFIG['output_prefix']}{timestamp}.png"
    filepath = os.path.join(CONFIG["output_dir"], filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Obraz zapisany: {filepath}")
    return filepath


def main():
    """Główna pętla: wczytaj dane → oblicz → wygeneruj obraz."""
    print("🌀 FANTOM MAPPER v1.0")
    print("=" * 50)
    
    # Wczytaj dane
    data = load_data(CONFIG["data_source"])
    
    # Wyciągnij wartości
    phi_left = data.get("Phi_left", [])
    phi_right = data.get("Phi_right", [])
    mer = data.get("MER", 0.7)
    
    # Jeśli brak danych – symulacja
    if not phi_left or not phi_right:
        print("⚠️ Brak danych w źródle. Generuję obraz zastępczy z szumem.")
        resolution = CONFIG["resolution"]
        field = np.random.randn(resolution, resolution)
        field = gaussian_filter(field, sigma=2.0)
    else:
        # Oblicz pole fantomowe
        field = compute_fantom_field(
            phi_left, phi_right, mer,
            resolution=CONFIG["resolution"]
        )
    
    # Wygeneruj obraz
    generate_image(field)
    print("=" * 50)
    print("✅ Gotowe.")


# ============================================================
# URUCHOMIENIE
# ============================================================

if __name__ == "__main__":
    main()
