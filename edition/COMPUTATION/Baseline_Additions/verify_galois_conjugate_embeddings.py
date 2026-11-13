#!/usr/bin/env python3
"""Part D of the computations for edition Z2 (cited by paper G7). Galois conjugation of a finitely generated dense subgroup of U(2):
the abstract group does not determine the transition probabilities of its orbit.  Exact arithmetic in Q(zeta_8)."""
import json, itertools, math
from fractions import Fraction as Fr
import numpy as np
R, ok = {}, {}

class Z8:                       # element sum_j c_j zeta^j, zeta^4 = -1, c_j rational
    __slots__ = ("c",)
    def __init__(s, c): s.c = tuple(Fr(x) for x in c)
    def __add__(s, o): return Z8([a + b for a, b in zip(s.c, o.c)])
    def __sub__(s, o): return Z8([a - b for a, b in zip(s.c, o.c)])
    def __mul__(s, o):
        r = [Fr(0)] * 4
        for i, a in enumerate(s.c):
            for j, b in enumerate(o.c):
                k = i + j
                if k >= 4: r[k - 4] -= a * b
                else: r[k] += a * b
        return Z8(r)
    def conj(s):                # complex conjugation: zeta -> zeta^-1 = -zeta^3
        c = s.c; return Z8([c[0], -c[3], -c[2], -c[1]])
    def sigma(s, k):            # zeta -> zeta^k, k odd
        r = [Fr(0)] * 4
        for j, a in enumerate(s.c):
            e = (j * k) % 8
            if e >= 4: r[e - 4] -= a
            else: r[e] += a
        return Z8(r)
    def val(s, k=1): return sum(float(a) * np.exp(1j * math.pi * k * j / 4) for j, a in enumerate(s.c))
    def real_parts(s):          # for a real element a + b*sqrt2 (sqrt2 = zeta - zeta^3): returns (a, b)
        c = s.c; assert c[2] == 0 and c[1] == -c[3]; return c[0], c[1]
ONE, ZERO = Z8([1, 0, 0, 0]), Z8([0, 0, 0, 0])
ZETA = Z8([0, 1, 0, 0]); RT2INV = Z8([0, Fr(1, 2), 0, Fr(-1, 2)])     # 1/sqrt2 = (zeta - zeta^3)/2
def mm(A, B): return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]
H = [[RT2INV, RT2INV], [RT2INV, ZERO - RT2INV]]; T = [[ONE, ZERO], [ZERO, ZETA]]
I2 = [[ONE, ZERO], [ZERO, ONE]]
def num(M, k=1): return np.array([[M[i][j].val(k) for j in range(2)] for i in range(2)])
def sig(M, k): return [[M[i][j].sigma(k) for j in range(2)] for i in range(2)]

# the conjugate embedding is again unitary and is the substitution H -> -H, T -> T^3
ok["D_sigma3_H_is_minus_H_and_sigma3_T_is_T_cubed"] = (np.allclose(num(sig(H, 3)), -num(H)) and np.allclose(num(sig(T, 3)), np.linalg.matrix_power(num(T), 3)))
ok["D_conjugate_generators_unitary"] = all(np.allclose(num(M, 3).conj().T @ num(M, 3), np.eye(2)) for M in (H, T))

# exact transition probabilities p(W) = |<0|W|0>|^2 = a + b sqrt2 and the conjugate a - b sqrt2
rows = []
def word_matrix(w):
    M = I2
    for ch in w: M = mm(M, H if ch == "H" else T)
    return M
for w in ["HTH", "HTTH", "HTHTH", "HTHTTTH", "THTHTTHTH", "HTHTHTTHTTTH"]:
    M = word_matrix(w); a00 = M[0][0]; p = a00 * a00.conj(); a, b = p.real_parts()
    p1 = float(a) + float(b) * 2 ** .5; p3 = float(a) - float(b) * 2 ** .5
    rows.append(dict(word=w, p_exact=f"{a} + {b}*sqrt2", p_standard=p1, p_conjugate=p3,
                     check_standard=float(abs(num(M)[0, 0]) ** 2), check_conjugate=float(abs(num(M, 3)[0, 0]) ** 2)))
R["D_exact_words"] = rows
ok["D_exact_matches_numeric_both_embeddings"] = all(abs(r["p_standard"] - r["check_standard"]) < 1e-12 and abs(r["p_conjugate"] - r["check_conjugate"]) < 1e-12 for r in rows)
ok["D_probabilities_differ"] = any(abs(r["p_standard"] - r["p_conjugate"]) > 0.1 for r in rows)
ok["D_HTH_is_(2+sqrt2)/4_vs_(2-sqrt2)/4"] = rows[0]["p_exact"] == "1/2 + 1/4*sqrt2"

# breadth-first enumeration of group elements (numerically, both embeddings carried together)
Hs, Ts = num(H), num(T); Hc, Tc = num(H, 3), num(T, 3)
def key(U):                      # projective class: normalize phase
    f = U.flatten(); i = np.argmax(np.abs(f) > 1e-9); ph = f[i] / abs(f[i]); return tuple(np.round((U / ph).flatten(), 7))
seen = {key(np.eye(2)): (np.eye(2, dtype=complex), np.eye(2, dtype=complex))}
frontier = list(seen.values()); stats = []
best = dict(p=0, pc=1, gap=0)
for L in range(1, 27):
    new = []
    for (U, V) in frontier:
        for (g, gc) in ((Hs, Hc), (Ts, Tc)):
            U2, V2 = U @ g, V @ gc; k = key(U2)
            if k not in seen: seen[k] = (U2, V2); new.append((U2, V2))
    frontier = new
    P = np.array([[abs(U[0, 0]) ** 2, abs(V[0, 0]) ** 2] for U, V in seen.values()])
    nontriv = P[(P[:, 0] < 1 - 1e-9)]
    i = np.argmax(nontriv[:, 0] - nontriv[:, 1]); 
    close = nontriv[nontriv[:, 0] > 0.99]
    stats.append(dict(word_length=L, elements=len(seen), max_p_minus_pconj=float((nontriv[:, 0] - nontriv[:, 1]).max()),
                      largest_p_below_1=float(nontriv[:, 0].max()), pconj_at_that_element=float(nontriv[np.argmax(nontriv[:, 0]), 1]),
                      min_pconj_among_p_above_0p99=(float(close[:, 1].min()) if len(close) else None)))
    if len(seen) > 400000: break
R["D_orbit_statistics"] = stats
_c = P[(P[:, 0] > 0.99) & (P[:, 0] < 1 - 1e-9)]; _i = np.argmin(_c[:, 1])
R["D_extreme_element"] = dict(p_standard=float(_c[_i, 0]), p_conjugate=float(_c[_i, 1]), elements_enumerated=len(seen))
last = stats[-1]
ok["D_elements_with_p_above_0.99_and_conjugate_below_0.1"] = last["min_pconj_among_p_above_0p99"] is not None and last["min_pconj_among_p_above_0p99"] < 0.1

# rigidity of cyclic phases: for which n is Re(zeta_n^{jk}) independent of the unit j for every k
rig = []
for n in range(1, 31):
    units = [j for j in range(1, n + 1) if math.gcd(j, n) == 1]
    indep = all(abs(math.cos(2 * math.pi * j * k / n) - math.cos(2 * math.pi * units[0] * k / n)) < 1e-12 for j in units for k in range(n))
    if indep: rig.append(n)
R["D_galois_rigid_cyclic_orders"] = rig
ok["D_rigid_orders_are_1_2_3_4_6"] = rig == [1, 2, 3, 4, 6]
R["ok"] = ok
json.dump(R, open("Galois_Conjugate_Embeddings_Results.json", "w"), indent=1)
for k_, v_ in ok.items(): print(("PASS " if v_ else "FAIL ") + k_)
