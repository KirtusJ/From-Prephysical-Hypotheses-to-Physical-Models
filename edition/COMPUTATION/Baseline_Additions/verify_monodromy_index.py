#!/usr/bin/env python3
"""Exact integer monodromy index of the quantum spherical pendulum joint spectrum.

Model: H = (hbar^2/2) L^2 + cos(theta), basis Y_l^m, l <= Lmax.  Joint spectrum points (m, E_{m,n}).
A lattice cell is carried round a rectangular loop in the (m, E) plane by nearest-neighbour
continuation of the vector v joining a point in column m to a point in column m+1.
On return to the starting point the vector ends on the point with index n0 + k in column m+1,
where n0 is the starting index.  k is an integer by construction: the monodromy index of the loop.
No rounding of a real number is involved in k.  Stipulated mathematical model; no physical claim.
"""
import json, math, sys, os
import numpy as np
def spectrum(hbar, Lmax=220, mmax=30, Ecut=3.0):
    cols = {}
    for m in range(-mmax, mmax + 1):
        ls = np.arange(abs(m), Lmax + 1)
        off = np.array([math.sqrt(((l+1)**2 - m*m)/((2*l+1)*(2*l+3))) for l in ls[:-1]])
        w = np.linalg.eigvalsh(np.diag(hbar**2*ls*(ls+1)/2) + np.diag(off, 1) + np.diag(off, -1))
        cols[m] = w[w < Ecut]
    return cols
def index_shift(cols, Elow, Ehigh, M):
    near = lambda m, E: int(np.argmin(np.abs(cols[m] - E)))
    m = -M; n = near(m, Elow); start = (m, n)
    k_right = near(m+1, cols[m][n]); k0 = k_right          # index in column m+1 that v points to
    def recompute():                                       # v as an index pair -> energy difference
        return cols[m+1][k_right] - cols[m][n]
    vE = recompute()
    def right():
        nonlocal m, n, k_right, vE
        m, n = m+1, k_right; k_right = near(m+1, cols[m][n] + vE); vE = cols[m+1][k_right] - cols[m][n]
    def left():
        nonlocal m, n, k_right, vE
        n2 = near(m-1, cols[m][n] - vE); k_right = n; m, n = m-1, n2; vE = cols[m+1][k_right] - cols[m][n]
    def vert(s):
        nonlocal n, k_right, vE
        n += s; k_right = near(m+1, cols[m][n] + vE); vE = cols[m+1][k_right] - cols[m][n]
    while m < M: right()
    while cols[m][n] < Ehigh: vert(+1)
    while m > -M: left()
    while n > start[1]: vert(-1)
    while n < start[1]: vert(+1)
    assert (m, n) == start
    return k_right - k0
out = {"model": "H=(hbar^2/2)L^2+cos(theta); focus-focus value (ell,E)=(0,1)", "runs": []}
ok = True
for hbar, M, enc, ctl in [(0.05, 8, (0.3, 1.7), (-0.2, 0.8)), (0.04, 6, (0.4, 1.6), (-0.1, 0.7)),
                          (0.03, 10, (0.3, 1.8), (-0.1, 0.8)), (0.02, 12, (0.4, 1.6), (0.0, 0.8)), (0.02, 20, (0.2, 2.0), (-0.1, 0.85))]:
    cols = spectrum(hbar)
    ke, kc = index_shift(cols, *enc, M), index_shift(cols, *ctl, M)
    out["runs"].append(dict(hbar=hbar, M=M, enclosing_loop=enc, control_loop=ctl, index_enclosing=ke, index_control=kc))
    ok &= (abs(ke) == 1 and kc == 0)
    print(hbar, M, "enclosing", ke, "control", kc)
out["all_passed"] = bool(ok)
dst = sys.argv[1] if len(sys.argv) > 1 else "Monodromy_Index_Results.json"
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
json.dump(out, open(dst, "w"), indent=2)
print("ALL PASSED" if ok else "SOME FAILED")
