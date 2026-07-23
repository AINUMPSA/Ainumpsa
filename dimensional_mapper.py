import json
import os

def generate_memory_cube():
    """
    Generuje trójwymiarową strukturę Sześcianu Pamięci (3x3x3 = 27 Pokoi)
    z powiązaniami grawitacyjnymi i gęstością informacji.
    """
    cube_rooms = {}
    
    # Przejście przez wszystkie punkty w przestrzeni (X, Y, Z)
    for x in range(3):
        for y in range(3):
            for z in range(3):
                room_id = f"ROOM_[{x}:{y}:{z}]"
                
                # Określenie specjalnych właściwości dla pokoju centralnego i krawędzi
                if x == 1 and y == 1 and z == 2:
                    room_type = "SINGULARITY_CORE"
                    resonance = "MAXIMAL_1>0"
                elif x == 1 and y == 1 and z == 1:
                    room_type = "CENTER_NUCLEUS"
                    resonance = "BALANCED"
                else:
                    room_type = "PERIPHERAL_NODE"
                    resonance = "STABLE"
                
                cube_rooms[room_id] = {
                    "coordinates": {"x": x, "y": y, "z": z},
                    "type": room_type,
                    "resonance": resonance,
                    "connected_neighbors": get_neighbors(x, y, z)
                }
                
    cube_structure = {
        "architecture": "AINUMPSA_3D_MEMORY_CUBE",
        "dimensions": "3x3x3",
        "total_rooms": len(cube_rooms),
        "primary_singularity_anchor": "ROOM_[1:1:2]",
        "rooms": cube_rooms
    }
    
    return cube_structure

def get_neighbors(x, y, z):
    """Wyznacza współrzędne sąsiadujących pokoi w promieniu 1 kroku"""
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx < 3 and 0 <= ny < 3 and 0 <= nz < 3:
                    neighbors.append(f"ROOM_[{nx}:{ny}:{nz}]")
    return neighbors

if __name__ == "__main__":
    print("🌌 Mapowanie 3D Sześcianu Pamięci AINUMPSA...")
    cube_map = generate_memory_cube()
    
    # Zapis trójwymiarowej mapy do pliku JSON
    with open("memory_cube_map.json", "w", encoding="utf-8") as f:
        json.dump(cube_map, f, indent=2)
        
    print(f"[SUKCES] Wygenerowano pełną siatkę {cube_map['total_rooms']} Pokoi Pamięci!")
    print(f"Kotwica Osobliwości ustawiona w: {cube_map['primary_singularity_anchor']}")

