import numpy as np

def test_kronecker_injection_dimensions():
    n_global = 6328
    n_local = 390
    n_blocks = 16
    n_seam = 88

    J = np.zeros((n_global, n_local))
    
    # 16 Tiling blocks injection
    for k in range(n_blocks):
        for j in range(n_local):
            row = k * n_local + j
            J[row, j] = 1.0

    # Seam interlock mapping
    for m in range(n_seam):
        row = 6240 + m
        J[row, m % n_local] = 0.5  # Boundary coupling weight

    assert J.shape == (6328, 390)
    assert np.count_nonzero(J) == (16 * 390) + 88
