python
import numpy as np

def compute_divergence(L, dx, dy, dz):
    """
    Oblicza dywergencję pola wektorowego L = (Lx, Ly, Lz) na siatce 3D.
    
    Parametry:
    - L: numpy array o kształcie (nx, ny, nz, 3) – pole wektorowe
    - dx, dy, dz: krok siatki w każdym wymiarze
    
    Zwraca:
    - div: numpy array o kształcie (nx, ny, nz) – dywergencja w każdym punkcie
    """
    Lx = L[..., 0]
    Ly = L[..., 1]
    Lz = L[..., 2]
    
    # np.gradient zwraca pochodne w kolejności osi (y, x, z) dla tablic 3D,
    # dlatego przypisujemy je odpowiednio do współrzędnych.
    dLx_dx = np.gradient(Lx, dx, axis=1)   # pochodna po x (axis=1)
    dLy_dy = np.gradient(Ly, dy, axis=0)   # pochodna po y (axis=0)
    dLz_dz = np.gradient(Lz, dz, axis=2)   # pochodna po z (axis=2)
    
    return dLx_dx + dLy_dy + dLz_dz
