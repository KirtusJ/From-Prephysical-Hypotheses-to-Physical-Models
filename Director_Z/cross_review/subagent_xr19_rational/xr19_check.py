#!/usr/bin/env python3
"""Cross-review program xr19 for three Director G notes. Own code; nothing imported from the author.

PREDICATES (fixed before the first run). Each records met / failed / measured-only.
Tolerances: exact (Fraction / Q(sqrt2)) unless marked FLOAT. FLOAT tolerance TOL=1e-9;
basis: all float quantities are O(1) results of <=2000 products of unit-norm 2x2 doubles or
16x16 double linear algebra, so rounding is <~1e-12; 1e-9 leaves three orders. Minimum slack
is reported so that the tolerance itself can be judged.

A. Rational Hadamard family and Cauchy identification
 A0 (hypothesis, per t=1..40) a,b>0, a^2+b^2=c^2, |a-b|=1 for the stated recurrence.
 A1 (U-H)^2 = (2 - sqrt2 (a+b)/c) I exactly in Q(sqrt2), 2x2 Z=diag(1,-1), X=swap.
 A2 (2 - sqrt2 (a+b)/c) * c^2 * (1+s) = 1 with s=(a+b)/(sqrt2 c), s^2 = 1-1/(2c^2).
 A3 1/8 < (c/K)^2 <= 25/49, K least power of two >= a+b.
 A4 consecutive members: ||U_t-U_{t+1}||^2 <= (1/c_t+1/c_{t+1})^2 and strictly decreasing (Cauchy).
 A5 contrast <e0|U U'|e0> = (aa'+bb')/(cc') exactly, random pairs of triples.
 A6 explicit index/flag/arm circuit (Walsh, select, inverse Walsh): hypothesis a^2+b^2=c^2,
    K>=max(a+b,c) dyadic, input nonzero. Accepted block = (c/K)(U (+) I) v exactly; p=c^2/K^2.
 A7 retry pair after failure succeeds with probability 2p(1-p) exactly; both failure branches
    are proportional to the first failure vector; both successes proportional to the first success.
 A8 (measured only) contrast of U_t against candidate H under the two embeddings of sqrt2.
B. Optical bound
 B0 P_A, P_B commute and P_A P_B is the ideal Choi ray projector (FLOAT).
 B1 bound at a=0.0632,b=0.0395,s=0.47 equals 179860054/211515275 exactly.
 B2 printed numbers: 0.8973, 0.8736, 0.84151, 0.24332, 0.21452 reproduced to printed digits.
 B3 per random trace-decreasing CP instance; hypothesis: every tested input has success>1e-12
    and 4b<1. Then z<=a; each B-input weight <= (sqrt f+sqrt(3z))^2/4+delta;
    delta<=4b max q; f>=bound(s=0.47). (FLOAT)
 B4 (measured only) how often the unweighted two-basis sum F_A+F_B-1 exceeds f.
 B5 ideal + two one-basis errors gives F_A=0.9368,F_B=0.9605,f=0.8973; unchanged under scaling.
 B6 transfer: trace-decreasing f_psi >= 4f-3 ; trace-preserving f_psi >= (4 sqrt f -3)_+^2,
    hypothesis TP tested per instance; non-vacuous counts reported. (FLOAT)
C. Signed sheet source spectrum
 C0 hypothesis 1<=B, 2B<=M.
 C1 FFT weights equal 2 sin^4(pi k B/M)/(M B sin^2(pi k/M)), k!=0 (FLOAT, TOL).
 C2 w_0=0 exactly (integer sum) and sum w =1 (FLOAT).
 C3 tail over folded |k|>K <= min(1, M/(BK)) for every K=1..floor(M/2) (FLOAT).
 C4 M even, B even: k=M/2 absent exactly (integer alternating sum). Odd B: measured only.
 C5 (measured only) B=M/4: weight of k=+-2 minus 4/pi^2.
 C6 M even: dipole and single-site sources have equal weight on each pair {k,k+M/2} (FLOAT).
 C7 exponents: M=2^(16r),B=M^(7/8),K=M^(3/16): M/(BK)=M^(-1/16) exactly, 2B dyadic.
D. Clock with unit sheet moves
 D0 hypothesis N>=1, mu>0, c>0.
 D1 |j_n| <= 1+|F|cT0/mu for all n<=N (exact rationals).
 D2 |Q_n-A_n| <= 1/2 (exact).
 D3 operator norm ||V_rounded(n)-V_vector(n)|| <= |k|theta/2 + n k^2 theta^2 for every n<=N,
    all k tested, base momenta on a grid (FLOAT; difference of two SU(2) matrices has
    operator norm = Frobenius/sqrt2). Non-vacuous = bound<2.
 D4 isolated rounding gives all strokes zero when |F|cT0/mu<1/2 (exact); else measured.
 D5 J=ceil(|F|cT0/mu)+1 >= max|j_n| (exact).
 D6 (measured only) sheet speed at fixed circumference times epsilon, and coordinate count
    times tau^2/epsilon, over a sequence of epsilon (pi factored out).
 D7 |relativistic rest ray - Newton| <= |F|^3 T^4/(8 m^3 c^2) (FLOAT relative 1e-12).
E. Cyclic-phase reference (light)
 E1 (7735,23808,25033) is Pythagorean, equals (D^2-n^2,2Dn,D^2+n^2) at D=128,n=93.
 E2 winding hypothesis |5 phi-2pi|<pi/2; then |phi-alpha| <= 2|Im(a+ib)^5|/(5c^5) < 0.000053.
 E3 first bright 1/2 and double bright 3/8 for q in 5,7,12,13 (FLOAT).
 E4 p=c^2/K^2>1/8 for random signed triples (exact); count of p=1 reported.
Seed 20261113. Result file is never overwritten.
"""
import sys, os, json, math, random
from fractions import Fraction as Fr
import numpy as np

SEED = 20261113
TOL = 1e-9
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xr19_results.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)
random.seed(SEED)
rng = np.random.default_rng(SEED)
REC = {}


def pred(name, ok, detail=None, kind="test"):
    r = REC.setdefault(name, {"met": 0, "failed": 0, "measured": 0, "failures": [], "notes": []})
    if kind == "measure":
        r["measured"] += 1
        if detail is not None and len(r["notes"]) < 40:
            r["notes"].append(detail)
        return
    if ok:
        r["met"] += 1
    else:
        r["failed"] += 1
        if len(r["failures"]) < 20:
            r["failures"].append(detail)


def note(name, detail):
    REC.setdefault(name, {"met": 0, "failed": 0, "measured": 0, "failures": [], "notes": []})["notes"].append(detail)


# ---------- Q(sqrt2)
class Q2:
    __slots__ = ("x", "y")

    def __init__(s, x, y=0):
        s.x, s.y = Fr(x), Fr(y)

    def __add__(s, o): return Q2(s.x + o.x, s.y + o.y)
    def __sub__(s, o): return Q2(s.x - o.x, s.y - o.y)
    def __mul__(s, o): return Q2(s.x * o.x + 2 * s.y * o.y, s.x * o.y + s.y * o.x)
    def __eq__(s, o): return s.x == o.x and s.y == o.y
    def val(s, sign=1): return float(s.x) + sign * math.sqrt(2) * float(s.y)


def mm(A, B):
    return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]


def family(T):
    u, v = 1, 1
    out = []
    for t in range(1, T + 1):
        m, n = u + v, v
        out.append((m * m - n * n, 2 * m * n, m * m + n * n))
        u, v = u + 2 * v, u + v
    return out


def dyadic(x):
    K = 1
    while K < x:
        K *= 2
    return K


def Umat(a, b, c):
    return [[Q2(Fr(a, c)), Q2(Fr(b, c))], [Q2(Fr(b, c)), Q2(Fr(-a, c))]]


RT = Q2(0, Fr(1, 2))  # 1/sqrt2
Hm = [[RT, RT], [RT, Q2(0, Fr(-1, 2))]]


def section_A():
    fam = family(40)
    prev_d = None
    for t, (a, b, c) in enumerate(fam, 1):
        hyp = a > 0 and b > 0 and a * a + b * b == c * c and abs(a - b) == 1
        pred("A0", hyp, [t, a, b, c])
        if not hyp:
            continue
        U = Umat(a, b, c)
        D = [[U[i][j] - Hm[i][j] for j in range(2)] for i in range(2)]
        D2 = mm(D, D)
        lam = Q2(2, Fr(-(a + b), c))
        zero = Q2(0)
        pred("A1", D2[0][0] == lam and D2[1][1] == lam and D2[0][1] == zero and D2[1][0] == zero, [t])
        s = Q2(0, Fr(a + b, 2 * c))
        pred("A2", (s * s) == Q2(1 - Fr(1, 2 * c * c)) and lam * Q2(c * c) * (Q2(1) + s) == Q2(1), [t])
        K = dyadic(a + b)
        p = Fr(c * c, K * K)
        pred("A3", Fr(1, 8) < p <= Fr(25, 49), [t, str(p)])
        if t < len(fam):
            a2, b2, c2 = fam[t]
            U2 = Umat(a2, b2, c2)
            E = [[U[i][j] - U2[i][j] for j in range(2)] for i in range(2)]
            E2 = mm(E, E)
            d2 = E2[0][0].x
            ok = E2[0][0].y == 0 and d2 == 2 - 2 * Fr(a * a2 + b * b2, c * c2) and d2 <= (Fr(1, c) + Fr(1, c2)) ** 2
            ok = ok and (prev_d is None or d2 < prev_d)
            pred("A4", ok, [t, float(d2)])
            prev_d = d2
        if t <= 6:
            cH = Q2(0, Fr(a + b, 2 * c))
            pred("A8", None, {"t": t, "abc": [a, b, c], "contrast_vs_H_embedding_plus": cH.val(1),
                              "embedding_minus": cH.val(-1), "p": str(p)}, kind="measure")
    # A5
    trip = fam[:8] + [(5, 12, 13), (8, 15, 17), (7735, 23808, 25033), (-3, 4, 5), (20, -21, 29)]
    for _ in range(200):
        (a, b, c), (a2, b2, c2) = random.choice(trip), random.choice(trip)
        P = mm(Umat(a, b, c), Umat(a2, b2, c2))
        pred("A5", P[0][0] == Q2(Fr(a * a2 + b * b2, c * c2)), [a, b, c, a2, b2, c2])


# ---------- explicit circuit
def fwht(v):
    v = list(v)
    n = len(v)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                x, y = v[j], v[j + h]
                v[j], v[j + h] = x + y, x - y
        h *= 2
    return v


KEYS = [(f, r, x) for f in (0, 1) for r in (0, 1) for x in (0, 1)]


def Wop(st, a, b, c, K):
    """st: dict key(f,r,x)->list len K. Unnormalised Walsh twice, divided by K: exact unitary."""
    st = {k: fwht(st[k]) for k in KEYS}
    new = {k: [Fr(0)] * K for k in KEYS}
    A, Bb = abs(a), abs(b)
    sa, sb = (1 if a >= 0 else -1), (1 if b >= 0 else -1)
    for (f, r, x) in KEYS:
        src = st[(f, r, x)]
        for i in range(K):
            amp = src[i]
            if amp == 0:
                continue
            if r == 0:
                if i < A:
                    new[(f, r, x)][i] += sa * (amp if x == 0 else -amp)
                elif i < A + Bb:
                    new[(f, r, 1 - x)][i] += sb * amp
                else:
                    new[(1 - f, r, x)][i] += amp
            else:
                if i < c:
                    new[(f, r, x)][i] += amp
                else:
                    new[(1 - f, r, x)][i] += amp
    return {k: [z / K for z in fwht(new[k])] for k in KEYS}


def nrm(st):
    return sum(z * z for k in KEYS for z in st[k])


def split(st, K):
    good = {k: [Fr(0)] * K for k in KEYS}
    bad = {k: list(st[k]) for k in KEYS}
    for k in KEYS:
        if k[0] == 0:
            good[k][0] = st[k][0]
            bad[k][0] = Fr(0)
    return good, bad


def prop(s1, s2):
    f1 = [z for k in KEYS for z in s1[k]]
    f2 = [z for k in KEYS for z in s2[k]]
    piv = next((i for i, z in enumerate(f2) if z != 0), None)
    if piv is None:
        return all(z == 0 for z in f1)
    lam = f1[piv] / f2[piv]
    return all(x == lam * y for x, y in zip(f1, f2))


def section_A_circuit():
    trips = [(3, 4, 5), (21, 20, 29), (119, 120, 169), (5, 12, 13), (8, 15, 17), (-3, 4, 5), (4, -3, 5)]
    for (a, b, c) in trips:
        K = dyadic(abs(a) + abs(b))
        hyp = a * a + b * b == c * c and K >= max(abs(a) + abs(b), c) and K & (K - 1) == 0
        p = Fr(c * c, K * K)
        inputs = [[1, 0, 0, 0], [0, 0, 0, 1], [1, 0, 1, 0]] + [[random.randint(-5, 5) for _ in range(4)] for _ in range(3)]
        for v in inputs:
            if not hyp or all(z == 0 for z in v):
                pred("A6_hypothesis", False, [a, b, c, v])
                continue
            pred("A6_hypothesis", True)
            st = {k: [Fr(0)] * K for k in KEYS}
            for r in (0, 1):
                for x in (0, 1):
                    st[(0, r, x)][0] = Fr(v[2 * r + x])
            n0 = nrm(st)
            out = Wop(st, a, b, c, K)
            # W is an involution and norm-preserving?
            back = Wop(out, a, b, c, K)
            unit_ok = nrm(out) == n0 and all(back[k] == st[k] for k in KEYS)
            good, bad = split(out, K)
            exp = {(0, 0, 0): Fr(a * v[0] + b * v[1], K), (0, 0, 1): Fr(b * v[0] - a * v[1], K),
                   (0, 1, 0): Fr(c * v[2], K), (0, 1, 1): Fr(c * v[3], K)}
            okA6 = unit_ok and all(good[k][0] == exp[k] for k in exp) and nrm(good) == p * n0
            pred("A6", okA6, [a, b, c, v])
            if p == 1:
                pred("A7", None, {"abc": [a, b, c], "p": 1}, kind="measure")
                continue
            Y = Wop(bad, a, b, c, K)
            Rp, Ap = split(Y, K)
            g1, b1 = split(Wop(Rp, a, b, c, K), K)
            g2, b2 = split(Wop(Ap, a, b, c, K), K)
            ps = (nrm(g1) + nrm(g2)) / nrm(bad)
            okA7 = ps == 2 * p * (1 - p) and prop(b1, bad) and prop(b2, bad) and prop(g1, good) and prop(g2, good)
            okA7 = okA7 and nrm(Rp) == (1 - p) * nrm(bad)
            pred("A7", okA7, [a, b, c, v, str(ps), str(2 * p * (1 - p))])
        note("A6", {"abc": [a, b, c], "K": K, "p": str(p), "mean_calls_1+1/p": float(1 + 1 / p)})


# ---------- optical
def bound(a, b, s):
    return (1 - a * (1 + b * (3 + 3 / s) / (1 - 4 * b))) / (1 + b * (1 + s) / (1 - 4 * b))


def transfer(f, mode):
    p = (2 + math.sqrt(2)) / 4
    fp = max(4 * math.sqrt(f) - 3, 0) ** 2 if mode == "tp" else max(4 * f - 3, 0)
    ang = math.acos(math.sqrt(p)) + math.acos(math.sqrt(fp))
    return math.cos(min(ang, math.pi / 2)) ** 2


def section_B():
    a, b, s = Fr(632, 10000), Fr(395, 10000), Fr(47, 100)
    val = bound(a, b, s)
    pred("B1", val == Fr(179860054, 211515275), str(val))
    note("B1", {"value": str(val), "float": float(val)})
    sens = bound(Fr(632 + 27, 10000), Fr(395 + 21, 10000), s)
    checks = {"0.8973": (float(Fr(9368, 10000) + Fr(9605, 10000) - 1), 0.8973, 5e-5),
              "0.8736": (2 * 0.9368 - 1, 0.8736, 5e-5),
              "0.84151": (float(sens), 0.84151, 5e-6),
              "0.24332": (transfer(0.8971, "tp"), 0.24332, 5e-6),
              "0.21452": (transfer(0.8971, "td"), 0.21452, 5e-6),
              "0.85034": (float(val), 0.85034, 5e-6)}
    for k, (got, want, hw) in checks.items():
        pred("B2", abs(got - want) <= hw, {k: got})
        note("B2", {k: got})
    alt = (2 - math.sqrt(2)) / 4
    note("B2", {"alternate_Ramsey_value": alt,
                "lower_bound_tp_at_0.85034": transfer(float(val), "tp"),
                "lower_bound_td_at_0.85034": transfer(float(val), "td"),
                "best_s_bound_at_central": max(float(bound(a, b, Fr(i, 1000))) for i in range(1, 3000))})

    c8, s8 = math.cos(math.pi / 8), math.sin(math.pi / 8)
    hp, hmn = np.array([c8, s8]), np.array([-s8, c8])
    t0, t1 = np.array([c8, -s8]), np.array([s8, c8])
    pl, mi = np.array([1, 1]) / math.sqrt(2), np.array([1, -1]) / math.sqrt(2)
    e0, e1 = np.array([1.0, 0]), np.array([0, 1.0])
    Abas = [np.kron(x, y) for x in (pl, mi) for y in (hp, hmn)]
    Bbas = [np.kron(x, y) for x in (e0, e1) for y in (t0, t1)]
    Hh = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    U = np.block([[np.eye(2), np.zeros((2, 2))], [np.zeros((2, 2)), Hh]])
    mub = max(abs(abs(x @ y) ** 2 - 0.25) for x in Abas for y in Bbas)
    PA = sum(np.outer(np.kron(x, U @ x), np.kron(x, U @ x)) for x in Abas)
    PB = sum(np.outer(np.kron(x, U @ x), np.kron(x, U @ x)) for x in Bbas)
    phi = U.T.reshape(16) / 2
    Pid = np.outer(phi, phi)
    pred("B0", mub < 1e-12 and np.abs(PA @ PB - PB @ PA).max() < 1e-12 and np.abs(PA @ PB - Pid).max() < 1e-12,
         float(np.abs(PA @ PB - Pid).max()))
    Xc, Zc = np.kron([[0, 1], [1, 0]], np.eye(2)), np.kron([[1, 0], [0, -1]], np.eye(2))

    def stats(Ks):
        vs = [K.T.reshape(16) / 2 for K in Ks]
        rho = sum(np.outer(v, v.conj()) for v in vs)
        tr = rho.trace().real
        rho = rho / tr

        def cond(x):
            num = sum(abs((U @ x) @ (K @ x)) ** 2 for K in Ks)
            den = sum(np.linalg.norm(K @ x) ** 2 for K in Ks)
            return num, den
        FA = [cond(x) for x in Abas]
        FB = [cond(x) for x in Bbas]
        return rho, tr, FA, FB, cond

    def filt(kind):
        e = 10.0 ** (-rng.uniform(0, 2, 4))
        if kind == 0:
            return np.eye(4)
        if kind == 1:
            Bm = np.array(Abas).T
        elif kind == 2:
            Bm = np.array(Bbas).T
        elif kind == 3:
            Bm = U @ np.array(Bbas).T
        else:
            Bm, _ = np.linalg.qr(rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)))
        return Bm @ np.diag(e) @ Bm.conj().T

    slack = {"z<=a": 9.0, "column": 9.0, "delta": 9.0, "f>=bound": 9.0, "td": 9.0, "tp": 9.0}
    qual = 0
    hof = 0
    psis = [np.kron(pl, e0)]
    N = 6000
    for it in range(N):
        kind = it % 3
        if kind == 0:
            eps = [0.01, 0.05, 0.2, 0.6][rng.integers(4)]
            nK = int(rng.integers(1, 5))
            L, R = filt(int(rng.integers(5))), filt(int(rng.integers(5)))
            Ks = [L @ U @ ((j == 0) * np.eye(4) + eps * (rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)))) @ R
                  for j in range(nK)]
        elif kind == 1:
            w = rng.dirichlet([8, 1, 1, 0.3])
            L, R = filt(int(rng.integers(5))), filt(int(rng.integers(5)))
            Ks = [math.sqrt(w[0]) * L @ U @ R, math.sqrt(w[1]) * L @ U @ Xc @ R, math.sqrt(w[2]) * L @ U @ Zc @ R,
                  math.sqrt(w[3]) * L @ U @ Xc @ Zc @ R]
        else:
            eps = [0.01, 0.05, 0.2, 0.6][rng.integers(4)]
            w = rng.dirichlet([3, 1, 1])
            Ks = []
            for j in range(3):
                Wj, _ = np.linalg.qr(np.eye(4) + eps * (rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))))
                Ks.append(math.sqrt(w[j]) * U @ Wj)
        S = sum(K.conj().T @ K for K in Ks)
        lam = np.linalg.eigvalsh(S).max()
        sc = (1.0 if kind == 2 else rng.uniform(0.05, 1)) / math.sqrt(lam)
        Ks = [K * sc for K in Ks]
        S = sum(K.conj().T @ K for K in Ks)
        is_tp = np.abs(S - np.eye(4)).max() < 1e-10
        rho, tr, FA, FB, cond = stats(Ks)
        minsucc = min(d for _, d in FA + FB)
        a_ = 1 - np.mean([n / d for n, d in FA]) if minsucc > 1e-12 else None
        b_ = 1 - np.mean([n / d for n, d in FB]) if minsucc > 1e-12 else None
        f = (phi @ rho @ phi).real
        # transfer predicates (hypothesis: TD always; TP tested)
        for psi in psis + [rng.normal(size=4) + 1j * rng.normal(size=4) for _ in range(2)]:
            psi = psi / np.linalg.norm(psi)
            num = sum(abs((U @ psi).conj() @ (K @ psi)) ** 2 for K in Ks)
            den = sum(np.linalg.norm(K @ psi) ** 2 for K in Ks)
            if den <= 1e-12:
                continue
            fpsi = num / den
            if 4 * f - 3 > 0:
                sl = fpsi - (4 * f - 3)
                slack["td"] = min(slack["td"], sl)
                pred("B6_trace_decreasing_nonvacuous", sl >= -TOL, [it, f, fpsi])
            if is_tp and 4 * math.sqrt(f) - 3 > 0:
                sl = fpsi - (4 * math.sqrt(f) - 3) ** 2
                slack["tp"] = min(slack["tp"], sl)
                pred("B6_trace_preserving_nonvacuous", sl >= -TOL, [it, f, fpsi])
        hyp = minsucc > 1e-12 and b_ is not None and 4 * b_ < 1
        pred("B3_hypothesis", hyp, None if hyp else [it, kind, minsucc, b_])
        if not hyp:
            continue
        qual += 1
        z = (np.trace(rho @ PB)).real - f
        z = max(z, 0.0)
        delta = 1 - f - z
        qB = [(np.kron(x, np.eye(4)[i]) @ rho @ np.kron(x, np.eye(4)[i])).real for x in Bbas for i in range(4)]
        qB = [sum(qB[4 * j:4 * j + 4]) for j in range(4)]
        s1 = a_ - z
        slack["z<=a"] = min(slack["z<=a"], s1)
        pred("B3_z<=a", s1 >= -TOL, [it, kind, z, a_])
        s2 = min((math.sqrt(max(f, 0)) + math.sqrt(3 * z)) ** 2 / 4 + delta - q for q in qB)
        slack["column"] = min(slack["column"], s2)
        pred("B3_column", s2 >= -TOL, [it, kind, s2])
        s3 = 4 * b_ * max(qB) - delta
        slack["delta"] = min(slack["delta"], s3)
        pred("B3_delta", s3 >= -TOL, [it, kind, s3])
        s4 = f - bound(a_, b_, 0.47)
        slack["f>=bound"] = min(slack["f>=bound"], s4)
        pred("B3_f>=bound", s4 >= -TOL, [it, kind, f, a_, b_])
        if (1 - a_) + (1 - b_) - 1 > f + TOL:
            hof += 1
            if hof <= 3:
                note("B4", {"instance": it, "FA+FB-1": 1 - a_ - b_, "f": f, "bound_s047": bound(a_, b_, 0.47)})
    pred("B4", None, {"instances_where_unweighted_FA+FB-1_exceeds_f": hof, "qualifying": qual, "generated": N}, kind="measure")
    note("B3_f>=bound", {"min_slacks": slack, "qualifying": qual, "generated": N})
    # B5
    for scale in (1.0, 1e-6):
        Ks = [math.sqrt(scale * 0.8973) * U, math.sqrt(scale * 0.0395) * U @ Xc, math.sqrt(scale * 0.0632) * U @ Zc]
        rho, tr, FA, FB, _ = stats(Ks)
        fa, fb = np.mean([n / d for n, d in FA]), np.mean([n / d for n, d in FB])
        f = (phi @ rho @ phi).real
        pred("B5", abs(fa - 0.9368) < 1e-12 and abs(fb - 0.9605) < 1e-12 and abs(f - 0.8973) < 1e-12, [scale, fa, fb, f])


# ---------- sheet spectrum
def section_C():
    cases = [(16, 4), (16, 8), (64, 16), (64, 8), (64, 5), (256, 32), (1000, 37), (1000, 250), (1000, 500), (81, 13), (81, 40),
             (3200, 800), (3200, 3), (4096, 1024), (65536, 16384), (10, 6)]
    for M, B in cases:
        hyp = B >= 1 and 2 * B <= M
        pred("C0", hyp, None if hyp else [M, B])
        if not hyp:
            continue
        sgn = [1] * B + [-1] * B + [0] * (M - 2 * B)
        v = np.array(sgn, dtype=float) / math.sqrt(2 * B)
        w = np.abs(np.fft.fft(v)) ** 2 / M
        k = np.arange(M)
        kf = np.where(k > M // 2, k - M, k)
        form = np.zeros(M)
        nz = k != 0
        form[nz] = 2 * np.sin(math.pi * k[nz] * B / M) ** 4 / (M * B * np.sin(math.pi * k[nz] / M) ** 2)
        err = float(np.abs(w - form).max())
        pred("C1", err <= TOL, [M, B, err])
        pred("C2", sum(sgn) == 0 and abs(w.sum() - 1) <= TOL, [M, B, float(w.sum())])
        absk = np.abs(kf)
        cum = np.bincount(absk, weights=w, minlength=M // 2 + 1)
        tail = 1 - np.cumsum(cum)  # tail[K] = sum_{|k|>K}
        Ks = np.arange(1, M // 2 + 1)
        bnd = np.minimum(1.0, M / (B * Ks))
        sl = bnd - tail[1:M // 2 + 1]
        i = int(sl.argmin())
        pred("C3", sl.min() >= -TOL, [M, B, float(sl.min())])
        note("C3", {"M": M, "B": B, "K_tested": int(len(Ks)), "min_slack": float(sl.min()), "at_K": int(Ks[i]),
                    "max_ratio_tail_over_bound": float((tail[1:M // 2 + 1] / bnd).max())})
        if M % 2 == 0:
            alt = sum(sg * (-1) ** y for y, sg in enumerate(sgn))
            if B % 2 == 0:
                pred("C4", alt == 0, [M, B, alt])
            else:
                pred("C4_oddB", None, {"M": M, "B": B, "w_{M/2}": float(w[M // 2])}, kind="measure")
            dip = np.zeros(M); dip[0], dip[1] = 1 / math.sqrt(2), -1 / math.sqrt(2)
            sing = np.zeros(M); sing[0] = 1
            wd, ws = np.abs(np.fft.fft(dip)) ** 2 / M, np.abs(np.fft.fft(sing)) ** 2 / M
            h = M // 2
            pred("C6", np.abs((wd[:h] + wd[h:]) - (ws[:h] + ws[h:])).max() <= 1e-14, [M])
        if 4 * B == M:
            pred("C5", None, {"M": M, "pair_weight_minus_4/pi^2": float(w[2] + w[M - 2] - 4 / math.pi ** 2)}, kind="measure")
    for r in (1, 2, 3, 4):
        M, B, K = 2 ** (16 * r), 2 ** (14 * r), 2 ** (3 * r)
        pred("C7", Fr(M, B * K) == Fr(1, 2 ** r) and (2 ** r) ** 16 == M and B ** 8 == M ** 7 and K ** 16 == M ** 3
             and (2 * B) & (2 * B - 1) == 0 and 2 * B <= M, [r])
    note("C7", "r=1 instance (M=65536,B=16384) is in the C1-C3 list; tail bound there at K=8 is 1/2")


# ---------- clock
def section_D():
    inst = [dict(M=3200, N=200, F=Fr(1, 2), c=Fr(1), mu=Fr(1), T0=Fr(1, 2)),
            dict(M=3200, N=1000, F=Fr(1, 2), c=Fr(1), mu=Fr(1), T0=Fr(1, 2)),
            dict(M=3200, N=1000, F=Fr(-1, 2), c=Fr(1), mu=Fr(1), T0=Fr(1, 2)),
            dict(M=3200, N=500, F=Fr(0), c=Fr(1), mu=Fr(1), T0=Fr(1, 2)),
            dict(M=1024, N=500, F=Fr(3), c=Fr(1), mu=Fr(1), T0=Fr(2)),
            dict(M=512, N=300, F=Fr(-5, 2), c=Fr(2), mu=Fr(1, 3), T0=Fr(1)),
            dict(M=65536, N=2000, F=Fr(1), c=Fr(1), mu=Fr(1), T0=Fr(1)),
            dict(M=97, N=150, F=Fr(7, 3), c=Fr(1), mu=Fr(1), T0=Fr(3, 2))]
    for _ in range(12):
        inst.append(dict(M=random.choice([64, 300, 1000, 4096, 20001]), N=random.randint(1, 800),
                         F=Fr(random.randint(-40, 40), random.randint(1, 9)), c=Fr(random.randint(1, 5), random.randint(1, 3)),
                         mu=Fr(random.randint(1, 9), random.randint(1, 9)), T0=Fr(random.randint(1, 12), 4)))
    qs = np.linspace(0, math.pi, 9)[:-1] + 0.1234
    gmin = 9.0
    rmax = 0.0
    for I in inst:
        M, N, F, c, mu, T0 = (I[k] for k in ("M", "N", "F", "c", "mu", "T0"))
        hyp = N >= 1 and mu > 0 and c > 0
        pred("D0", hyp, None if hyp else str(I))
        if not hyp:
            continue
        g = F * c * T0 / (mu * N)  # h/theta = F c tau/mu
        lim = abs(F) * c * T0 / mu
        Q = [0]
        A = [Fr(0)]
        for n in range(1, N + 1):
            An = g * n * (n + 1) / 2
            A.append(An)
            Q.append(math.floor(An + Fr(1, 2)))
        j = [Q[n] - Q[n - 1] for n in range(1, N + 1)]
        mj = max(abs(x) for x in j)
        pred("D1", mj <= 1 + lim, [str(I), mj])
        pred("D2", all(abs(Q[n] - A[n]) <= Fr(1, 2) for n in range(N + 1)), str(I))
        iso = [math.floor(g * n + Fr(1, 2)) for n in range(1, N + 1)]
        if lim < Fr(1, 2):
            pred("D4", all(x == 0 for x in iso), str(I))
        else:
            pred("D4_outside_hypothesis", None, {"lim": float(lim), "nonzero_isolated": sum(1 for x in iso if x)}, kind="measure")
        J = math.ceil(lim) + 1
        pred("D5", J >= mj, [str(I), J, mj])
        note("D5", {"M": M, "N": N, "F": str(F), "lim": float(lim), "J": J, "max|j|": mj, "sum_j": Q[N]})
        th = 2 * math.pi / M
        h = float(g) * th
        Kn = max(1, int(M ** (3 / 16)))
        for k in sorted({1, 2, 3, -1, 7, Kn}):
            ck, sk = math.cos(k * th), math.sin(k * th)
            C = np.array([[ck, -1j * sk], [-1j * sk, ck]])
            Vv = np.tile(np.eye(2, dtype=complex), (len(qs), 1, 1))
            Vr = Vv.copy()
            for n in range(1, N + 1):
                pv = qs - k * n * h
                pr = qs - k * th * j[n - 1]
                Vv = C @ Vv
                Vr = C @ Vr
                Vv[:, 0, :] *= np.exp(-1j * pv)[:, None]; Vv[:, 1, :] *= np.exp(1j * pv)[:, None]
                Vr[:, 0, :] *= np.exp(-1j * pr)[:, None]; Vr[:, 1, :] *= np.exp(1j * pr)[:, None]
                d = np.sqrt((np.abs(Vv - Vr) ** 2).sum(axis=(1, 2)) / 2).max()
                bd = abs(k) * th / 2 + n * k * k * th * th
                if bd < 2:
                    gmin = min(gmin, bd - d)
                    rmax = max(rmax, d / bd)
                    pred("D3_nonvacuous", bd - d >= -TOL, [str(I), k, n, float(d), bd])
                else:
                    pred("D3_vacuous_bound>=2", None, None, kind="measure")
    note("D3_nonvacuous", {"min_slack": gmin, "max_ratio_error_over_bound": rmax, "momenta": len(qs)})
    # D6: speeds, pi factored out. mu=c=1, v=1, J fixed, tau = eps^3 (tau=o(eps^2)), circumference C=1.
    for m in (4, 8, 12, 16):
        eps = Fr(1, 2 ** m); tau = eps ** 3; J = 2; v = Fr(1); mu = Fr(1); L = Fr(1); c = Fr(1)
        M_over_2pi = eps / (mu * tau)
        b_bounded = v * tau / (J + 4)
        circ_over_2pi = M_over_2pi * b_bounded
        Cfix = Fr(1)
        b_fixed_times_2pi = Cfix / M_over_2pi
        speed_fixed_times_2pi = b_fixed_times_2pi * (J + 4) / tau
        count_over_2pi = M_over_2pi * L / (c * tau)
        pred("D6", None, {"eps": str(eps), "bounded_pitch_circumference/(2pi eps)": str(circ_over_2pi / eps),
                          "bounded_sheet_speed": str(b_bounded * (J + 4) / tau), "base_speed": str(c * (J + 4)),
                          "fixed_circumference_speed*2pi*eps": str(speed_fixed_times_2pi * eps),
                          "count*tau^2/(2pi eps)": str(count_over_2pi * tau ** 2 / eps)}, kind="measure")
    for _ in range(2000):
        F = random.uniform(-5, 5); m = random.uniform(0.1, 5); c = random.uniform(0.2, 5); T = random.uniform(0, 3)
        if abs(F) < 1e-3:
            continue
        mu = m * c * c
        # stable form of (sqrt(mu^2+c^2F^2T^2)-mu)/|F|
        x = c * c * abs(F) * T * T / (math.sqrt(mu * mu + c * c * F * F * T * T) + mu)
        newton = abs(F) * T * T / (2 * m)
        bd = abs(F) ** 3 * T ** 4 / (8 * m ** 3 * c * c)
        pred("D7", abs(x - newton) <= bd * (1 + 1e-12) + 1e-15, [F, m, c, T, x, newton, bd])


def section_E():
    import mpmath as mp
    mp.mp.dps = 60
    a, b, c = 7735, 23808, 25033
    pred("E1", a * a + b * b == c * c and (a, b, c) == (128 ** 2 - 93 ** 2, 2 * 128 * 93, 128 ** 2 + 93 ** 2), None)
    re, im = 1, 0
    for _ in range(5):
        re, im = re * a - im * b, re * b + im * a
    rhs = Fr(2 * abs(im), 5 * c ** 5)
    phi = mp.atan2(b, a)
    alpha = 2 * mp.pi / 5
    hyp = abs(5 * phi - 2 * mp.pi) < mp.pi / 2 and re > 0
    pred("E2_hypothesis", bool(hyp), None)
    true = abs(phi - alpha)
    pred("E2", bool(true <= mp.mpf(rhs.numerator) / rhs.denominator) and rhs < Fr(53, 10 ** 6),
         [float(true), float(rhs)])
    note("E2", {"true_error": float(true), "integer_bound": float(rhs), "sharper_pi/2_constant": float(rhs) * math.pi / 4})
    for q in (5, 7, 12, 13):
        al = 2 * math.pi / q
        ph = al + 0.013
        ps = [(1 + math.cos(k * al - s * ph)) / 2 for k in range(q) for s in (1, -1)]
        pred("E3", abs(sum(ps) / (2 * q) - 0.5) < 1e-12 and abs(sum(x * x for x in ps) / (2 * q) - 0.375) < 1e-12, [q])
    for q in (2, 3, 4):
        al = 2 * math.pi / q; ph = al + 0.013
        ps = [(1 + math.cos(k * al - s * ph)) / 2 for k in range(q) for s in (1, -1)]
        pred("E3_below_stated_range", None, {"q": q, "first": sum(ps) / (2 * q), "double": sum(x * x for x in ps) / (2 * q)}, kind="measure")
    ones = 0
    for _ in range(3000):
        D = random.randint(1, 300); n = random.randint(0, D)
        a, b, c = D * D - n * n, 2 * D * n, D * D + n * n
        gg = math.gcd(math.gcd(a, b), c); a, b, c = a // gg, b // gg, c // gg
        if random.random() < 0.5: a, b = b, a
        K = dyadic(abs(a) + abs(b))
        p = Fr(c * c, K * K)
        ones += p == 1
        pred("E4", p > Fr(1, 8) and p <= 1 and K >= c, [a, b, c, K])
    note("E4", {"p_equal_1_count": ones})


for sec in (section_A, section_A_circuit, section_B, section_C, section_D, section_E):
    try:
        sec()
    except Exception as ex:  # keep the failure, do not hide it
        import traceback
        note("PROGRAM_ERRORS", {"section": sec.__name__, "error": traceback.format_exc()})

tot = {"met": sum(r["met"] for r in REC.values()), "failed": sum(r["failed"] for r in REC.values()),
       "measured": sum(r["measured"] for r in REC.values())}
with open(OUT, "x") as fh:
    json.dump({"seed": SEED, "tol": TOL, "totals": tot, "predicates": REC}, fh, indent=1, default=str)
for k in sorted(REC):
    r = REC[k]
    print(f"{k:34s} met={r['met']:7d} failed={r['failed']:5d} measured={r['measured']:6d}")
    for fl in r["failures"][:3]:
        print("    FAIL", fl)
print("TOTAL", tot)
