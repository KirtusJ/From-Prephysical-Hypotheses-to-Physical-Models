#!/usr/bin/env python3
"""Session 2 (Director Z), parts A-C. Independent recomputation of items in the Director A, B, G packets
by routes that do not reuse their programs, and checks of the phase-recovery corollary and the
generator/observable count.  Double precision unless 'exact' is stated; fixed seed."""
import json, itertools, math
import numpy as np, sympy as sp
from scipy.linalg import null_space
rng = np.random.default_rng(2026111202)
R, ok = {}, {}

# ---------- shared projective geometry (unit representatives, d = arccos|<a|b>|) ----------
def align(a, x):
    ip = np.vdot(a, x); return x * (np.conj(ip) / abs(ip))
def plog(a, x):
    xa = align(a, x); c = np.vdot(a, xa).real; u = xa - c * a; nu = np.linalg.norm(u)
    return np.zeros_like(a) if nu < 1e-300 else np.arctan2(nu, c) * u / nu
def pexp(a, v):
    t = np.linalg.norm(v); return a.copy() if t < 1e-300 else np.cos(t) * a + np.sin(t) * v / t
def rand_state(n, cplx=True):
    x = rng.normal(size=n) + (1j * rng.normal(size=n) if cplx else 0); return x / np.linalg.norm(x)
def transport(verts, v):
    """closed-form Levi-Civita transport round a geodesic polygon (G7 Lemma 4.2); returns vector at verts[0]"""
    a = verts[0].copy(); w = v.copy(); k = len(verts)
    for i in range(k):
        q = align(a, verts[(i + 1) % k]); c = np.vdot(a, q).real
        u = q - c * a; nu = np.linalg.norm(u); T = np.arctan2(nu, c); u = u / nu
        ca = np.vdot(a, w); cu = np.vdot(u, w)
        w = w - ca * a - cu * u + ca * (np.cos(T) * a + np.sin(T) * u) + cu * (-np.sin(T) * a + np.cos(T) * u)
        a = np.cos(T) * a + np.sin(T) * u
    ph = np.vdot(verts[0], a); ph /= abs(ph)
    return w * np.conj(ph)
def hol_matrix(verts, Q):
    return np.column_stack([Q.conj().T @ transport(verts, Q[:, j]) for j in range(Q.shape[1])])
def barg(verts):
    b = 1.0 + 0j
    for i in range(len(verts)): b *= np.vdot(verts[i], verts[(i + 1) % len(verts)])
    return b


def fan_phase(verts, Q, N, J=1):
    a0 = verts[0]; n = Q.shape[1]; tot = 1.0 + 0j; maxcell = 0.0
    for j in range(1, len(verts) - 1):
        p, q = verts[j], verts[j + 1]; L = plog(p, q)
        pts = [pexp(p, L * i / N) for i in range(N + 1)]
        for i in range(N):
            T = hol_matrix([a0, pts[i], pts[i + 1]], Q)
            d = np.linalg.det(T); d = d if J == 1 else np.conj(d)
            ang = np.angle(d); maxcell = max(maxcell, abs(ang)); tot *= np.exp(1j * ang / (n + 1))
    return tot, maxcell
