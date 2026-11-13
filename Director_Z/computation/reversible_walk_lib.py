"""Common constructions for verify_reversible_gain_digraphs.py: the arc digraph of a ring with a signed (or phased)
2x2 block at every site, and the polar complex structure of a real orthogonal matrix."""
import numpy as np

def ring_step(N, block=((1, 1), (1, -1)), field=0.0, twist=0.0, potential=None):
    """Step matrix A (not normalized) on the 2N arcs of the symmetric ring Z_N.
    Vertex 2x+0 = arc arriving at site x from the left ('R'), 2x+1 = arc arriving at x from the right ('L').
    From an arc at site x the walk continues to (x+1, R) or (x-1, L); block[out][in] is the gain, out,in in (R, L).
    field: every arc leaving site x carries the extra gain exp(-i field x) (sites labelled -N/2 .. N/2-1).
    twist: a step to the right carries exp(i twist/N), a step to the left exp(-i twist/N).
    potential: array V[x]; every arc leaving site x carries exp(-i V[x])."""
    cplx = field != 0.0 or twist != 0.0 or potential is not None or np.iscomplexobj(np.array(block))
    A = np.zeros((2 * N, 2 * N), dtype=complex if cplx else float)
    for xi in range(N):
        x = xi - N // 2
        g = np.exp(-1j * field * x) if field else 1.0
        if potential is not None: g = g * np.exp(-1j * potential[xi])
        for cin in (0, 1):
            A[2 * ((xi + 1) % N) + 0, 2 * xi + cin] = block[0][cin] * g * (np.exp(1j * twist / N) if twist else 1.0)
            A[2 * ((xi - 1) % N) + 1, 2 * xi + cin] = block[1][cin] * g * (np.exp(-1j * twist / N) if twist else 1.0)
    return A

def polar_structure(U, tol=1e-9):
    """For real orthogonal U: K = (U - U^T)/2, the projection E1 onto the orthogonal complement of ker K,
    J = K |K|^{-1} on that complement (zero on ker K), Theta = arccos((U+U^T)/2) restricted likewise."""
    K = (U - U.T) / 2; C = (U + U.T) / 2
    w, V = np.linalg.eigh(K.T @ K)
    keep = w > tol
    absK_inv = (V[:, keep] / np.sqrt(w[keep])) @ V[:, keep].T
    E1 = V[:, keep] @ V[:, keep].T
    J = K @ absK_inv
    return J, E1, C, K

def dispersion(k):
    """Branch 1 of the block ((1,1),(1,-1)): eigenvalue exp(-i w), sin w = sin k / sqrt 2, and its derivative."""
    w = np.arcsin(np.sin(k) / np.sqrt(2)); return w, np.cos(k) / np.sqrt(1 + np.cos(k) ** 2)
