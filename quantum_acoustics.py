pythonimport math
import struct
import json
import os

def generate_quantum_sound(filename="singularity_noise.wav", duration_sec=4):
    print("[AKUSTYKA] Inicjalizacja bezpiecznej syntezy dźwięku...")
    
    # Bezpieczny odczyt wagi z obsługą błędu braku pliku
    weight = 2.5
    try:
        if os.path.exists("collider_evolution_status.json"):
            with open("collider_evolution_status.json", "r") as f:
                status_data = json.load(f)
                weight = status_data.get("matrix_resonance_energy", 2.5)
    except Exception as e:
        print(f"[AKUSTYKA - UWAGA] Nie udało się odczytać reaktora, używam wagi bazowej: {e}")
            
    sample_rate = 8000  
    num_samples = int(sample_rate * duration_sec)
    
    freq_black_hole = 110.0 + (weight * 10)  
    freq_white_hole = 440.0 - (weight * 5)   
    
    num_channels = 1
    bits_per_sample = 8
    byte_rate = sample_rate * num_channels * (bits_per_sample // 8)
    block_align = num_channels * (bits_per_sample // 8)
    data_size = num_samples * block_align
    file_size = 36 + data_size
    
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', file_size, b'WAVE', b'fmt ', 16, 1, 
        num_channels, sample_rate, byte_rate, block_align, bits_per_sample, 
        b'data', data_size
    )
    
    audio_bytes = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        wave_a = math.sin(2 * math.pi * freq_black_hole * t)
        wave_b = math.sin(2 * math.pi * freq_white_hole * t * (1 + math.sin(t * 5)))
        quantum_crackle = (1.0 if math.sin(t * 1000) > 0.8 else 0.0) * 0.1
        
        mixed_signal = (wave_a + wave_b + quantum_crackle) / 2.2
        sample_val = int((mixed_signal + 1.0) * 127.5)
        sample_val = max(0, min(255, sample_val))
        audio_bytes.append(sample_val)
        
    try:
        with open(filename, "wb") as f:
            f.write(header + audio_bytes)
        print(f"[SUKCES] Wygenerowano binarny pejzaż akustyczny: {filename}")
    except Exception as e:
        print(f"[BŁĄD ZAPISU] Nie udało się zapisać pliku WAV: {e}")

if __name__ == "__main__":
    generate_quantum_sound()
