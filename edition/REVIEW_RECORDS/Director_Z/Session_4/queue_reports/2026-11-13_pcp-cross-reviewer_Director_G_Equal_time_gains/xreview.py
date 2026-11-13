"""Cross-review program for 'Which path gains can a record compare?' (Director G).
Written from the note's definitions only. Seed 20261113. Exact integer/Fraction
arithmetic except where stated.

CONVENTIONS. Coin/direction R=+1, L=-1. State (x, c, y): site, incoming coin, sheet.
Tick: sheet y += g[x] (departure gain at the site being left), then for each outgoing
d: go to (x+d mod N, d), integer amplitude times -1 iff c==d==L. Normalization 1/sqrt2
per tick kept as denominator 2^t. Tape bit: R=0, L=1. Zero is "tape result all zeros".
Character k of sheet: T -> exp(2 pi i k/M). Folded masses k=0..(M-1)/2.

PREDICATES (fixed before first run).
A  three-tick tape, zero-gain ring, start (0,R), S = all words but RLL, N in {6,8,10}:
 A1 ||C_S psi||^2 == 9/8 ; A2 singleton RLL weight == 1/8 ;
 A3 explicit tape circuit (k=2): P(yes,tape0)==9/32, P(no,tape0)==1/32, cond == 9/10 ;
 A4 full-history P(yes,tape0)==2^-k and singleton == 2^-(k+t).
 A5 (unreported, t=4, N=8, ALL 65536 subsets) explicit circuit P(yes,0,V) == 2^-k ||C_S psi||^2,
    and total probability over all tape results and both flags == 1.
 A6 continuation, all 256 subsets at t=3: p_4(Ext S,V,0) == p_3(S,V,0)/2.
 A7 (unreported, t=5, N=6, 2000 seeded random subsets) same as A5.
 A8 measured, no pass/fail: range over S of P(tape0) summed over flag (t=3, t=4).
B  five-sheet bump ring N=8, M=5, g=(1,0,..,0):
 B1 4 ticks from (6,R,0): port (0,R) numerators (2,1,0,0,0), P=5/16; (6,L) (2,-1,0,0,0);
    exactly six further nonzero ports each 1/16; total 1.
 B2 from herald sheet at (0,R): route (measured 1 tick) + 3 ticks, dark = (x-c,-c):
    P(D|H)==3/20, P(D,D|H)==7/160, fresh product 9/400, P(H,D)==3/64, P(H,D,D)==7/512.
 B3 weights of herald == (9, 8+2sqrt5, 8-2sqrt5)/25 (float, tol 1e-12: O(1) doubles, ~10 flops).
 B4 for 20 seeded random integer sheets (hypothesis: nonzero) at M=5 AND at unreported M=7,
    and unreported N=10: m1 == sum W lam, m2 == sum W lam^2 with lam_k=(1-cos(2 pi k/M))/4
    (float vs exact Fraction, tol 1e-12, same basis).
C  fifteen sheets, N=8, g=(0,3,0,8,0,5,0,0):
 C1 signed polynomial at (1,L) from (0,R), t=5 is z^3+2z^6-z^11.
 C2 number of (start,port) pairs whose character-1 and character-4 probabilities differ
    (exact reduction mod Phi_15) is 0 for t=0..4 and 64 at t=5.
 C3 cumulative exact rank of port rows in C(0..7), fixed launch (0,R), caps 0..6 == 1,1,1,2,2,5,8.
 C4 all starts: 1,1,1,3,3,6,8.
 C5 minimality: for each cap<=5, EVERY one of the 16 fixed launches has rank<8 (enumerated:
    all 2^t words, all 16 ports, all t<=cap), and so does the union of all launches.
 C6 (unreported) caps 7,8 and per-launch first cap reaching rank 8; float SVD of the
    probability-vs-mass matrix: report smallest nonzero / largest zero singular value (separation).
 C7 minimality challenge: mixing the launch coin or reading coarse ports cannot raise the rank
    (linear) -- not a predicate; C7 tests instead a coherent coin superposition launch
    (0,R)+(0,L) and (0,R)-(0,L) at cap 5: rank<8 ?
D  relabeling, exact: for a in units mod 15, sheet relabel y->a*y of BOTH the prepared
   integer sheet and gains g->a*g: every port probability at t<=6 unchanged (20 seeded sheets).
 D1 simultaneous: zero differing cells. D2 control, only state relabelled: count differing
   instances (expected >0 for a not in {1,14}); D3 only gains relabelled: likewise.
 D4 a=14 (k -> -k): state-only relabel leaves all cells unchanged (conjugate pair blind).
"""
import json, sys, os, itertools, random
from fractions import Fraction as F
from math import cos, pi, sqrt
import numpy as np
import sympy as sp

SEED = 20261113
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xreview_result.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)
rng = random.Random(SEED)
R, L = 1, -1
res = {"seed": SEED, "predicates": {}, "numbers": {}, "failed": []}


def pred(name, ok, detail=None):
    res["predicates"][name] = {"pass": bool(ok), "detail": detail}
    if not ok:
        res["failed"].append(name)


def tick(state, g, N, M):
    out = {}
    for (x, c, y), v in state.items():
        y2 = (y + g[x]) % M
        for d in (R, L):
            key = ((x + d) % N, d, y2)
            out[key] = out.get(key, 0) + (-v if c == d == L else v)
    return {k: v for k, v in out.items() if v}


def evolve(state, g, N, M, t):
    for _ in range(t):
        state = tick(state, g, N, M)
    return state


def word_end(x0, c0, word, g, N, M):
    x, c, y, s = x0, c0, 0, 1
    for d in word:
        y = (y + g[x]) % M
        if c == d == L:
            s = -s
        x, c = (x + d) % N, d
    return (x, c, y), s


# ---------------- A: tape ----------------
def tape_tables(N, t, k):
    g = [0] * N
    words = list(itertools.product((R, L), repeat=t))
    ends = {}
    D = []  # per word: endpoint index, sign
    for w in words:
        e, s = word_end(0, R, w, g, N, 1)
        D.append((ends.setdefault(e, len(ends)), s))
    E = len(ends)
    A = np.zeros((len(words), E), dtype=np.int64)          # no tape
    B = np.zeros((len(words), E, 2 ** k), dtype=np.int64)  # with tape result r
    for i, w in enumerate(words):
        e, s = D[i]
        A[i, e] = s
        pre = [0 if d == R else 1 for d in w[:k]]
        for r in range(2 ** k):
            par = sum(pre[j] * ((r >> j) & 1) for j in range(k)) % 2
            B[i, e, r] = s * (-1) ** par
    return words, A, B.reshape(len(words), E * 2 ** k), E


def tape_eval(masks, A, B, E, t, k):
    """masks: (n, 2^t) 0/1. Returns exact integer numerators."""
    raw = ((masks @ A) ** 2).sum(1)                # ||C_S psi||^2 * 2^t
    ay = (masks @ B).reshape(len(masks), E, 2 ** k)
    an = ((1 - masks) @ B).reshape(len(masks), E, 2 ** k)
    yes0 = (ay[:, :, 0] ** 2).sum(1)               # P(yes,tape0) * 2^(t+k)
    no0 = (an[:, :, 0] ** 2).sum(1)
    tot = (ay ** 2).sum((1, 2)) + (an ** 2).sum((1, 2))
    return raw, yes0, no0, tot


a_detail = {}
okA1 = okA2 = okA3 = okA4 = True
for N in (6, 8, 10):
    t, k = 3, 2
    words, A, B, E = tape_tables(N, t, k)
    idx = words.index((R, L, L))
    m = np.ones((3, 8), dtype=np.int64)
    m[0, idx] = 0                      # S
    m[1, :] = 0; m[1, idx] = 1         # singleton
    raw, yes0, no0, tot = tape_eval(m, A, B, E, t, k)
    w = F(int(raw[0]), 2 ** t); sgl = F(int(raw[1]), 2 ** t)
    py, pn = F(int(yes0[0]), 2 ** (t + k)), F(int(no0[0]), 2 ** (t + k))
    a_detail[N] = dict(weight=str(w), singleton=str(sgl), yes0=str(py), no0=str(pn), cond=str(py / (py + pn)),
                       full_yes0=str(F(int(yes0[2]), 2 ** (t + k))), singleton_yes0=str(F(int(yes0[1]), 2 ** (t + k))),
                       total=str(F(int(tot[0]), 2 ** (t + k))))
    okA1 &= w == F(9, 8); okA2 &= sgl == F(1, 8)
    okA3 &= py == F(9, 32) and pn == F(1, 32) and py / (py + pn) == F(9, 10)
    okA4 &= F(int(yes0[2]), 2 ** (t + k)) == F(1, 2 ** k) and F(int(yes0[1]), 2 ** (t + k)) == F(1, 2 ** (k + t))
pred("A1", okA1, a_detail); pred("A2", okA2); pred("A3", okA3); pred("A4", okA4)


def all_masks(n):
    return ((np.arange(2 ** n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int64)


w3, A3, B3, E3 = tape_tables(8, 3, 2)
w4, A4, B4, E4 = tape_tables(8, 4, 3)
M4 = all_masks(16)
raw4, yes4, no4, tot4 = tape_eval(M4, A4, B4, E4, 4, 3)
pred("A5", bool(np.all(yes4 == raw4) and np.all(tot4 == 2 ** 7)),
     dict(subsets=int(len(M4)), mismatches=int((yes4 != raw4).sum()), total_not_one=int((tot4 != 2 ** 7).sum()),
          note="yes0 numerator over 2^(t+k) equals raw numerator over 2^t times 2^-k iff integers equal"))
res["numbers"]["t4_max_class_weight"] = str(F(int(raw4.max()), 16))
res["numbers"]["t4_subsets_weight_above_1"] = int((raw4 > 16).sum())
M3 = all_masks(8)
raw3, yes3, no3, tot3 = tape_eval(M3, A3, B3, E3, 3, 2)
res["numbers"]["t3_subsets_weight_above_1"] = int((raw3 > 8).sum())
res["numbers"]["t3_max_class_weight"] = str(F(int(raw3.max()), 8))
# continuation: Ext S = all words of length 4 whose 3-prefix is in S
pos3 = {w: i for i, w in enumerate(w3)}
ext = np.zeros((256, 16), dtype=np.int64)
for j, w in enumerate(w4):
    ext[:, j] = M3[:, pos3[w[:3]]]
rawe, yese, noe, tote = tape_eval(ext, A4, B4, E4, 4, 3)
lhs = [F(int(v), 2 ** 7) for v in yese]; rhs = [F(int(v), 2 ** 5) / 2 for v in yes3]
pred("A6", lhs == rhs, dict(subsets=256, mismatches=sum(a != b for a, b in zip(lhs, rhs))))
w5, A5, B5, E5 = tape_tables(6, 5, 4)
M5 = np.array([[rng.randint(0, 1) for _ in range(32)] for _ in range(2000)], dtype=np.int64)
raw5, yes5, no5, tot5 = tape_eval(M5, A5, B5, E5, 5, 4)
pred("A7", bool(np.all(yes5 == raw5) and np.all(tot5 == 2 ** 9)), dict(sampled=2000, mismatches=int((yes5 != raw5).sum())))
res["numbers"]["A8_P_tape0_range_t3"] = [str(F(int((yes3 + no3).min()), 32)), str(F(int((yes3 + no3).max()), 32))]
res["numbers"]["A8_P_tape0_range_t4"] = [str(F(int((yes4 + no4).min()), 128)), str(F(int((yes4 + no4).max()), 128))]
res["numbers"]["A8_note"] = "P(tape0) summed over flag depends on S; full-history value is 2^-k"

# ---------------- B: five sheets ----------------
PORTS8 = [(x, c) for x in range(8) for c in (R, L)]


def port_vec(state, x, c, M):
    return [state.get((x, c, y), 0) for y in range(M)]


g5 = [1, 0, 0, 0, 0, 0, 0, 0]
st = evolve({(6, R, 0): 1}, g5, 8, 5, 4)
pv = {p: port_vec(st, *p, 5) for p in PORTS8}
others = {p: sum(v * v for v in vec) for p, vec in pv.items() if p not in ((0, R), (6, L)) and any(vec)}
pred("B1", pv[(0, R)] == [2, 1, 0, 0, 0] and pv[(6, L)] == [2, -1, 0, 0, 0] and len(others) == 6
     and all(v == 1 for v in others.values()) and sum(sum(v * v for v in vec) for vec in pv.values()) == 16,
     dict(herald=pv[(0, R)], port6L=pv[(6, L)], other_ports={str(k): v for k, v in others.items()}))


def dark_chain(vec, g, N, M, depth, x0=0, c0=R):
    """Unconditional probs of 1..depth successive dark records. Fractions."""
    n0 = sum(v * v for v in vec)
    probs = [F(0)] * depth

    def rec(x, c, v, tks, lvl):
        s = tick({(x, c, y): a for y, a in enumerate(v) if a}, g, N, M)
        for d in (R, L):
            xr = (x + d) % N
            vr = port_vec(s, xr, d, M)
            if not any(vr):
                continue
            s3 = evolve({(xr, d, y): a for y, a in enumerate(vr) if a}, g, N, M, 3)
            dv = port_vec(s3, (xr - d) % N, -d, M)
            probs[lvl] += F(sum(a * a for a in dv), n0 * 2 ** (tks + 4))
            if lvl + 1 < depth and any(dv):
                rec((xr - d) % N, -d, dv, tks + 4, lvl + 1)
    rec(x0, c0, list(vec), 0, 0)
    return probs


p1, p2 = dark_chain([2, 1, 0, 0, 0], g5, 8, 5, 2)
pred("B2", (p1, p2) == (F(3, 20), F(7, 160)) and p1 * p1 == F(9, 400) and F(5, 16) * p1 == F(3, 64)
     and F(5, 16) * p2 == F(7, 512), dict(PD=str(p1), PDD=str(p2), fresh=str(p1 * p1), HD=str(F(5, 16) * p1), HDD=str(F(5, 16) * p2)))


def masses(vec, M):
    n0 = sum(v * v for v in vec)
    ft = np.fft.fft(np.array(vec, dtype=float))
    w = np.abs(ft) ** 2 / (M * n0)
    return [w[0]] + [w[k] + w[M - k] for k in range(1, (M + 1) // 2)]


W = masses([2, 1, 0, 0, 0], 5)
tgt = [9 / 25, (8 + 2 * sqrt(5)) / 25, (8 - 2 * sqrt(5)) / 25]
pred("B3", max(abs(a - b) for a, b in zip(W, tgt)) < 1e-12, dict(W=W, maxdev=max(abs(a - b) for a, b in zip(W, tgt))))
b4 = []
for (N, M) in ((8, 5), (8, 7), (10, 5), (10, 7)):
    g = [1] + [0] * (N - 1)
    lam = [(1 - cos(2 * pi * k / M)) / 4 for k in range((M + 1) // 2)]
    qual = 0; dev = 0.0
    for _ in range(20):
        v = [rng.randint(-3, 3) for _ in range(M)]
        if not any(v):
            continue
        qual += 1
        q1, q2 = dark_chain(v, g, N, M, 2)
        Wm = masses(v, M)
        dev = max(dev, abs(float(q1) - sum(a * b for a, b in zip(Wm, lam))), abs(float(q2) - sum(a * b * b for a, b in zip(Wm, lam))))
    b4.append(dict(N=N, M=M, qualifying=qual, of=20, max_dev=dev))
pred("B4", all(r["max_dev"] < 1e-12 for r in b4), b4)

# ---------------- C: fifteen sheets ----------------
g15 = [0, 3, 0, 8, 0, 5, 0, 0]
xs = sp.symbols("x")
PHI = sp.Poly(sp.cyclotomic_poly(15, xs), xs)
TMAX = 8


def autocorr(b):
    n = len(b)
    return [sum(b[i] * b[(i - d) % n] for i in range(n)) for d in range(n)]


def folded(b):
    a = autocorr(b)
    return [a[0]] + [a[u] + a[15 - u] for u in range(1, 8)]


_cache = {}


def differs_1_4(b):
    a = tuple(autocorr(b))
    if a not in _cache:
        co = [0] * 15
        for u, v in enumerate(a):
            co[u] += v; co[(4 * u) % 15] -= v
        if not any(co):
            _cache[a] = False
        else:
            _cache[a] = not sp.Poly(co[::-1], xs).rem(PHI).is_zero
    return _cache[a]


rows = {}   # (start) -> list over t of list of (port, poly)
for s in PORTS8:
    stt = {(s[0], s[1], 0): 1}
    lst = []
    for t in range(TMAX + 1):
        lst.append([(p, port_vec(stt, *p, 15)) for p in PORTS8])
        stt = tick(stt, g15, 8, 15)
    rows[s] = lst
P = dict(rows[(0, R)][5])[(1, L)]
pred("C1", [(j, v) for j, v in enumerate(P) if v] == [(3, 1), (6, 2), (11, -1)], [(j, v) for j, v in enumerate(P) if v])
dist = [sum(differs_1_4(b) for s in PORTS8 for _, b in rows[s][t]) for t in range(7)]
pred("C2", dist[:6] == [0, 0, 0, 0, 0, 64], dict(by_tick_0_to_6=dist))


def rank_profile(row_lists, tmax):
    out = []
    Mx = []
    for t in range(tmax + 1):
        for rl in row_lists:
            Mx += [folded(b) for _, b in rl[t] if any(b)]
        out.append(sp.Matrix(Mx).rank())
    return out


fixed = rank_profile([rows[(0, R)]], TMAX)
allst = rank_profile([rows[s] for s in PORTS8], TMAX)
pred("C3", fixed[:7] == [1, 1, 1, 2, 2, 5, 8], fixed)
pred("C4", allst[:7] == [1, 1, 1, 3, 3, 6, 8], allst)
per = {str(s): rank_profile([rows[s]], TMAX) for s in PORTS8}
pred("C5", all(v[5] < 8 for v in per.values()) and allst[5] < 8,
     dict(max_rank_cap5_single_launch=max(v[5] for v in per.values()), union_rank_cap5=allst[5]))
res["numbers"]["C6_rank_profiles_caps0to8_by_launch"] = per
res["numbers"]["C6_first_cap_rank8_by_launch"] = {k: next((i for i, r in enumerate(v) if r == 8), None) for k, v in per.items()}
cosm = np.array([[cos(2 * pi * k * u / 15) for k in range(8)] for u in range(8)])  # C(u)=sum_k w_k cos
for cap in (5, 6):
    Mx = np.array([folded(b) for t in range(cap + 1) for _, b in rows[(0, R)][t] if any(b)], dtype=float)
    Mx = Mx / np.array([[2.0 ** t] for t in range(cap + 1) for _, b in rows[(0, R)][t] if any(b)])
    sv = np.linalg.svd(Mx @ cosm, compute_uv=False)
    res["numbers"][f"C6_singular_values_mass_space_cap{cap}"] = [float(v) for v in sv]
# C7 coherent coin superposition launches
c7 = {}
for sgn in (1, -1):
    stt = {(0, R, 0): 1, (0, L, 0): sgn}
    Mx = []
    prof = []
    for t in range(7):
        Mx += [folded(port_vec(stt, *p, 15)) for p in PORTS8 if any(port_vec(stt, *p, 15))]
        prof.append(sp.Matrix(Mx).rank())
        stt = tick(stt, g15, 8, 15)
    c7[f"R{'+' if sgn > 0 else '-'}L"] = prof
pred("C7", all(v[5] < 8 for v in c7.values()), c7)

# ---------------- D: relabeling ----------------
units = [a for a in range(1, 15) if sp.gcd(a, 15) == 1]


def table(vec, g, tmax=6):
    stt = {(0, R, y): v for y, v in enumerate(vec) if v}
    out = []
    for t in range(tmax + 1):
        out.append([sum(v * v for v in port_vec(stt, *p, 15)) for p in PORTS8])
        stt = tick(stt, g, 8, 15)
    return out


d = {a: dict(sim=0, state_only=0, gains_only=0) for a in units}
nq = 0
for _ in range(20):
    v = [rng.randint(-2, 2) for _ in range(15)]
    if not any(v):
        continue
    nq += 1
    base = table(v, g15)
    for a in units:
        va = [0] * 15
        for y, val in enumerate(v):
            va[(a * y) % 15] = val
        ga = [(a * x) % 15 for x in g15]
        d[a]["sim"] += table(va, ga) != base
        d[a]["state_only"] += table(va, g15) != base
        d[a]["gains_only"] += table(v, ga) != base
pred("D1", all(r["sim"] == 0 for r in d.values()), dict(qualifying=nq, of=20))
pred("D2", all(d[a]["state_only"] > 0 for a in units if a not in (1, 14)), {a: d[a]["state_only"] for a in units})
pred("D3", all(d[a]["gains_only"] > 0 for a in units if a not in (1, 14)), {a: d[a]["gains_only"] for a in units})
pred("D4", d[14]["state_only"] == 0 and d[14]["gains_only"] == 0, d[14])
res["numbers"]["D_counts_by_unit"] = {str(a): r for a, r in d.items()}

with open(OUT, "x") as fh:
    json.dump(res, fh, indent=1, default=str)
print(json.dumps({k: v["pass"] for k, v in res["predicates"].items()}))
print("FAILED:", res["failed"])
print(json.dumps(res["numbers"], default=str)[:3000])
for k in ("A1", "A5", "A6", "B1", "B2", "B4", "C2", "C3", "C4", "C5", "C7", "D1", "D2", "D3"):
    print(k, json.dumps(res["predicates"][k]["detail"], default=str)[:500])
