"""Cross-review program xr20 (own code; imports nothing of the author's).

Targets: Director_G/Counting_and_character_records.md (note A) and
Director_G/Optical_multiset_weights.md (note B).  Exact arithmetic: integers,
Fractions, and Q(sqrt2) pairs with exact sign.  Seed 20.  Refuses to overwrite.

Data inputs taken from the note / stored JSON (shared source, not recomputed):
the five pixel extents of the plotted markers and the printed 0.660 +/- 0.012.

PREDICATES, fixed before the first run.  Each is 'met', 'failed' or
'measured' (no pass/fail criterion).  Hypothesis per instance: M >= 3 (A*).

Note A, staircase walk g(x)=floor(x/2) mod M, start (0,R), minus on L->L.
 A1  for each M in MS and n=1..M+1: the port (n-1,R) at t=n+1 has exactly n
     histories, all positive, unfolded gains n consecutive integers, and no
     other line endpoint at tick t is congruent to n-1 mod 4M.
 A2  integer form of eq (2): at that port N=n and the folded-free signed
     autocorrelation is A_0=n, A_h=2(n-h)/2 per unordered lag, i.e. the
     ordered-pair count at lag h (1<=h<=n-1) is n-h.  Hence
     W_n = n + 2 sum (n-h) C(h) given c+sum b=1.
 A2f float check of eq (2) and of W_{n+1}-2W_n+W_{n-1}=2C(n), C(M)=1-c, with
     seeded random weights (measured: max abs deviation; no threshold).
 A3  tick 5, port (1,R): six histories with gain/sign pairs
     (1,-),(0,+),(-1,-),(-1,+),(-2,+),(-3,-); row autocorrelation gives
     32P = 4+2c-4C1+2C2-4C3+2C4 for M>=5; folded: M=3 gives 6c, M=4 gives a
     c-coefficient 0 (signed energy 6 = history count).
 A4  count vs uniform squares at the interval ports: equal for n<=M, differ
     by exactly 2 (units 2^-t) at n=M+1.
 A5  M=4: at every direction-resolved port through tick 5, N = sum_j D_j^2
     (folded mod 4), so count = uniform squares on the complete output.
 A6  M=64: affine rank of all direction-combined position histograms through
     tick 14 in the parameters (c, C(1..32)) is 33.  (rank mod p=2^61-1; a
     full value 33 mod p proves rank 33.)
 A7  normalisation: for each M, t: sum over ports of N = 2^t, of A_0 = 2^t,
     and of each folded lag h>=1 is 0 (each character walk is normalised).
 A8  measured: at which (M,t) does some port first have N != sum_j D_j^2,
     i.e. where a count term first separates from the uniform character
     mixture (they agree exactly on collision-free ports, by Parseval).
 A9  control, measured: a law with c=0 at every depth but depth-dependent
     character weights (uniform for n<=M, b_0=1/(M+2) rest uniform at n=M+1)
     reproduces the pure-count interval records W_n=n for all n<=M+1.
 A10 unreported order: A1-A4 at M=11 and M=6; rank growth at M=10 (measured).

Note B, ten-step optical walk, H left, V right, minus on V->V, launch
weights 1 and -i, phase z^setting on each departure from the origin.
 B1  count centre return = 63/256 at every setting.
 B2  squared centre returns 9/128, 51/128, 85/128, 85/128 at 0,45,90,180 for
     both pairs; at 135: 43/128 +- 15 sqrt2/64, plus for the ordinary pair.
 B3  equal efficiencies, graphic intervals: feasible vertices (c,a,w) are
     (0.046462,0,0.953538),(0.121819,0,0.878181),(0.046462,0.047892,0.905646)
     to the six printed decimals; printed 135 alone needs w>=0.953967; with
     the other four graphic intervals it is infeasible; c>=0.0464619493 and
     max 135 return 0.647819382, deficit 0.000180618 (printed decimals).
 B4  D_j(count)>=0 and D_j(alternate)>=0 at all 22 modes, >0 at both centre
     modes, for U=57/560 and L in {69/112, 81/125}, lambda=L/(4U).
 B5  floor = min_j m_j/(m_j-D_j(ord)) over modes with D_j(ord)<0 equals
     1/2-(36403/392160)sqrt2 (graph) and 1/2-(21563/401280)sqrt2 (printed),
     attained at both centre modes and strictly larger elsewhere.
 B6  extremizer: c=0, w=floor, collection only at (0,H),(0,V),(-4,H) with
     nonnegative efficiencies gives detected returns exactly U and L, and
     return 1 at 90 and 180.
 B7  control (one setting-independent loss per mode), measured: seeded
     random efficiencies and mixtures with w<floor; number qualifying
     (positive detected totals) and number satisfying both inequalities.
 B8  control (separate loss per component): (a) scalar attenuation per
     component, incident w=1/1000, eta_c=eta_a=10^-6: both inequalities
     hold (so no positive bound on incident w); (b) per-component per-mode
     random losses with w=0: number satisfying both inequalities (measured;
     the note claims the exclusion survives).
 B9  unreported input: unexpanded extents U=53/560, L=349/560: B4 and the
     floor (measured).
"""
import json, random, sys, math
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations

OUT = Path(__file__).with_name("xr20_weights_result.json")
if OUT.exists():
    sys.exit("result file exists; refusing to overwrite")
random.seed(20)
R = {}
def rec(k, status, **kw):
    R[k] = dict(status=status, **kw)

# ---------------------------------------------------------------- note A
def g(x, M):
    return (x // 2) % M

def walk(tmax, M=None):
    """yield t, {(x,dir): {gain: [pos,neg]}}; dir 1=R, 0=L; gain unfolded if M None-fold"""
    st = {(0, 1): {0: [1, 0]}}
    for t in range(1, tmax + 1):
        nx = {}
        for (x, d), row in st.items():
            for d2 in (0, 1):
                flip = (d == 0 and d2 == 0)
                key = (x + (1 if d2 else -1), d2)
                tgt = nx.setdefault(key, {})
                for gn, (p, n) in row.items():
                    cell = tgt.setdefault(gn + (x // 2), [0, 0])
                    if flip:
                        cell[0] += n; cell[1] += p
                    else:
                        cell[0] += p; cell[1] += n
        st = nx
        yield t, st

def fold(row, M):
    D = [0] * M; N = 0; coll = False
    cnt = [0] * M
    for gn, (p, n) in row.items():
        D[gn % M] += p - n; N += p + n; cnt[gn % M] += p + n
    return N, D, cnt

def autoc(D, M):
    """A[h] = sum_j D_j D_{j+h mod M}; sum_s b_s|sigma_s|^2 = sum_h A[h] C(h)"""
    return [sum(D[j] * D[(j + h) % M] for j in range(M)) for h in range(M)]

MS = [3, 4, 5, 6, 7, 8, 11]
a1 = []; a2 = []; a4 = []; a7 = []; a8 = {}
for M in MS:
    assert M >= 3
    first_sep = None
    for t, st in walk(M + 2):
        # A7
        ports = {}
        for (x, d), row in st.items():
            ports.setdefault((x % (4 * M), d), {})
            tgt = ports[(x % (4 * M), d)]
            for gn, (p, n) in row.items():
                c = tgt.setdefault(gn % M, [0, 0]); c[0] += p; c[1] += n
        totN = 0; totA = [0] * M
        for row in ports.values():
            N, D, cnt = fold(row, M)
            totN += N
            A = autoc(D, M)
            totA = [u + v for u, v in zip(totA, A)]
            if first_sep is None and N != sum(v * v for v in D):
                first_sep = t
        a7.append((M, t, totN == 2 ** t and totA[0] == 2 ** t and not any(totA[1:])))
        n = t - 1
        if n >= 1:
            row = st[(n - 1, 1)]
            gains = sorted(row)
            okA1 = (len(gains) == n and all(row[k] == [1, 0] for k in gains)
                    and gains == list(range(gains[0], gains[0] + n))
                    and sum(1 for (x, d) in st if d == 1 and (x - (n - 1)) % (4 * M) == 0) == 1)
            a1.append((M, n, okA1))
            N, D, cnt = fold(row, M)
            A = autoc(D, M)
            # expected folded: lag h unfolded ordered count (n-|h|) for |h|<n, folded mod M
            exp = [0] * M
            for h in range(-(n - 1), n):
                exp[h % M] += n - abs(h)
            a2.append((M, n, N == n and A == exp))
            uni = sum(v * v for v in D)          # uniform squares = sum_j D_j^2
            a4.append((M, n, (N - uni) == (0 if n <= M else -2), N - uni))
    a8[M] = first_sep
rec("A1", "met" if all(x[2] for x in a1) else "failed", instances=len(a1),
    qualifying=len(a1), failures=[x for x in a1 if not x[2]])
rec("A2", "met" if all(x[2] for x in a2) else "failed", instances=len(a2),
    failures=[x for x in a2 if not x[2]])
rec("A4", "met" if all(x[2] for x in a4) else "failed", instances=len(a4),
    failures=[x for x in a4 if not x[2]],
    note="count minus uniform at n=M+1 is -2: uniform squares exceed count by 2")
rec("A7", "met" if all(x[2] for x in a7) else "failed", instances=len(a7),
    failures=[x for x in a7 if not x[2]])
rec("A8", "measured", first_tick_where_count_differs_from_uniform_squares_at_some_port=a8,
    searched_through="t=M+2")

# A2f floats
dev = 0.0; dev2 = 0.0
for M in MS:
    for _ in range(5):
        raw = [random.random() for _ in range(M + 1)]
        s = sum(raw); c = raw[0] / s; b = [v / s for v in raw[1:]]
        C = lambda h: sum(b[k] * math.cos(2 * math.pi * k * h / M) for k in range(M))
        W = [0.0]
        for t, st in walk(M + 2):
            n = t - 1
            if n < 1: continue
            N, D, cnt = fold(st[(n - 1, 1)], M)
            val = c * N + sum(b[k] * abs(sum(D[j] * complex(math.cos(2 * math.pi * k * j / M), math.sin(2 * math.pi * k * j / M)) for j in range(M))) ** 2 for k in range(M))
            W.append(val)
            dev = max(dev, abs(val - (n + 2 * sum((n - h) * C(h) for h in range(1, n)))))
        for n in range(1, M + 1):
            dev2 = max(dev2, abs(W[n + 1] - 2 * W[n] + W[n - 1] - 2 * C(n)))
        dev2 = max(dev2, abs(C(M) - (1 - c)))
rec("A2f", "measured", max_abs_dev_eq2=dev, max_abs_dev_second_difference_and_CM=dev2,
    basis="double precision; exact statement is A2")

# A3
a3 = {}
for M in (3, 4, 5, 6, 7, 11, None):
    for t, st in walk(5):
        pass
    row = st[(1, 1)]
    pairs = sorted(((gn, +1) for gn, (p, n) in row.items() for _ in range(p)), reverse=True)
    pairs = sorted([(gn, s) for gn, (p, n) in row.items() for s, k in ((1, p), (-1, n)) for _ in range(k)], reverse=True)
    if M is None:
        claim = sorted([(1, -1), (0, 1), (-1, -1), (-1, 1), (-2, 1), (-3, -1)], reverse=True)
        a3["raw_pairs"] = pairs; a3["raw_ok"] = pairs == claim
        continue
    N, D, cnt = fold(row, M)
    A = autoc(D, M)
    # 32P = c*N + sum_h A[h] C(h), C(0)=1-c  -> const A0, c-coefficient N-A0
    a3[M] = dict(N=N, A=A, const=A[0], c_coeff=N - A[0])
ok3 = a3["raw_ok"] and a3[3]["A"] == [0, 0, 0] and a3[3]["c_coeff"] == 6 and a3[4]["c_coeff"] == 0 \
    and a3[4]["A"][0] == 6 and all(a3[M]["const"] == 4 and a3[M]["c_coeff"] == 2 for M in (5, 6, 7, 11)) \
    and a3[11]["A"][1:5] == [-2, 1, -2, 1] and a3[11]["A"][7:] == [1, -2, 1, -2] and not any(a3[11]["A"][5:7])
rec("A3", "met" if ok3 else "failed", detail={str(k): v for k, v in a3.items()},
    note="A[h]+A[M-h] is the coefficient of C(h): -4,2,-4,2 at M>=9; at M=5..8 lags fold (e.g. M=5: C(4)=C(1))")

# A5
bad = []
for t, st in walk(5):
    for key, row in st.items():
        N, D, cnt = fold(row, 4)
        if N != sum(v * v for v in D):
            bad.append((t, key, N, D))
rec("A5", "met" if not bad else "failed", exceptions=[str(b) for b in bad])

# A6 rank
P = 2 ** 61 - 1
def rank_mod(rows):
    rows = [[v % P for v in r] for r in rows]; rk = 0
    ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][col]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][col], P - 2, P)
        for i in range(rk + 1, len(rows)):
            if rows[i][col]:
                f = rows[i][col] * inv % P
                rows[i] = [(a - f * b) % P for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk

def rank_profile(M, tmax, combine=True):
    rows = []; prof = {}
    K = M // 2
    for t, st in walk(tmax):
        grp = {}
        for (x, d), row in st.items():
            N, D, cnt = fold(row, M)
            A = autoc(D, M)
            # P*2^t = A0 + c (N-A0) + sum_{h=1..K} coef_h C(h); coef_h = A_h + A_{M-h} (once if 2h=M)
            vec = [N - A[0]] + [A[h] + (A[M - h] if (M - h) != h else 0) for h in range(1, K + 1)]
            k = (x % (4 * M)) if combine else (x % (4 * M), d)
            if k in grp: grp[k] = [u + v for u, v in zip(grp[k], vec)]
            else: grp[k] = vec
        rows += [[v * 2 ** (tmax - t) for v in r] for r in grp.values()]
        prof[t] = rank_mod(rows)
    return prof
p64 = rank_profile(64, 14, True)
rec("A6", "met" if p64[14] == 33 else "failed", rank_by_tick_direction_combined=p64,
    note="parameters c and C(1..32): 33 affine dimensions")
p4c = rank_profile(4, 8, False); p10 = rank_profile(10, 12, True); p11 = rank_profile(11, 12, True)
rec("A10", "measured", M4_direction_resolved_rank_by_tick=p4c, M4_full=3,
    M10_combined_rank_by_tick=p10, M10_full=6, M11_combined_rank_by_tick=p11, M11_full=6,
    note="A1-A4 at M=6 and M=11 are inside A1-A4")

# A9 control
a9 = {}
for M in (5, 11):
    ok = True
    for n in range(1, M + 2):
        # c=0. uniform b for n<=M: W = sum_j D_j^2 ; at n=M+1: b0=1/(M+2), others equal
        D = [0] * M
        for j in range(n): D[j % M] += 1
        if n <= M:
            W = F(sum(v * v for v in D))
        else:
            # |sigma_0|^2=(M+1)^2, |sigma_s|^2=1 for s!=0 (interval = all residues + one)
            b0 = F(1, M + 2); W = b0 * (M + 1) ** 2 + (1 - b0) * 1
        ok &= (W == n)
    a9[M] = ok
rec("A9", "measured", pure_character_depth_dependent_law_reproduces_count_records=a9,
    meaning="identification of c by (2) needs weights fixed across launch depths; premise is stated in the note's text")

# ---------------------------------------------------------------- note B
class Q2:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = F(a); s.b = F(b)
    def __add__(s, o): o = q(o); return Q2(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Q2(-s.a, -s.b)
    def __sub__(s, o): return s + (-q(o))
    def __rsub__(s, o): return q(o) - s
    def __mul__(s, o): o = q(o); return Q2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 2 * s.b * s.b; return Q2(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * q(o).inv()
    def sgn(s):
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        d = a * a - 2 * b * b
        return ((1 if a > 0 else -1) if d > 0 else (1 if b > 0 else -1))
    def __eq__(s, o): o = q(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def conj(s): return Q2(s.a, -s.b)
    def fl(s): return float(s.a) + float(s.b) * math.sqrt(2)
    def js(s): return dict(a=str(s.a), b=str(s.b), decimal=s.fl())
def q(x): return x if isinstance(x, Q2) else Q2(x)
def lt(x, y): return (q(y) - q(x)).sgn() > 0
def le(x, y): return (q(y) - q(x)).sgn() >= 0

MODES = [(x, d) for x in range(-10, 11, 2) for d in (0, 1)]
def optical(setting):
    amp = {(0, 0): [1, 0, 0, 0]}
    v = [0, 0, 0, 0]; v[2] = -1  # z^6 = -z^2
    amp[(0, 1)] = v
    cnt = {(0, 0): 1, (0, 1): 1}
    def mulz(vec, e):
        e %= 8; out = [0] * 4
        for j, a in enumerate(vec):
            per, r = divmod((j + e) % 8, 4); out[r] += a * (-1) ** per
        return out
    for _ in range(10):
        na = {}; nc = {}
        for (x, coin), vec in amp.items():
            for dest in (0, 1):
                e = (setting if x == 0 else 0) + (4 if coin == dest == 1 else 0)
                w = mulz(vec, e); key = (x + 2 * dest - 1, dest)
                cur = na.setdefault(key, [0] * 4)
                for i in range(4): cur[i] += w[i]
                nc[key] = nc.get(key, 0) + cnt[(x, coin)]
        amp, cnt = na, nc
    ordi = {}; alt = {}; count = {}
    for m in MODES:
        a0, a1, a2, a3 = amp.get(m, [0] * 4)
        # |a0+a1 z+a2 z^2+a3 z^3|^2 = sum a_i^2 + sqrt2 (a0a1+a1a2+a2a3-a0a3)
        ra = a0 * a0 + a1 * a1 + a2 * a2 + a3 * a3
        rb = a0 * a1 + a1 * a2 + a2 * a3 - a0 * a3
        ordi[m] = Q2(F(ra, 2048), F(rb, 2048)); alt[m] = ordi[m].conj()
        count[m] = Q2(F(cnt.get(m, 0), 2048))
    return dict(count=count, alternate=alt, ordinary=ordi)
PR = [optical(s) for s in range(5)]
tot_ok = all(sum(PR[s][k].values(), Q2()) == 1 for s in range(5) for k in PR[s])
cen = lambda s, k: PR[s][k][(0, 0)] + PR[s][k][(0, 1)]
rec("B0_normalisation", "met" if tot_ok else "failed")
rec("B1", "met" if all(cen(s, "count") == F(63, 256) for s in range(5)) else "failed")
exp = {0: F(9, 128), 1: F(51, 128), 2: F(85, 128), 4: F(85, 128)}
okB2 = all(cen(s, k) == v for s, v in exp.items() for k in ("ordinary", "alternate")) and \
    cen(3, "ordinary") == Q2(F(43, 128), F(15, 64)) and cen(3, "alternate") == Q2(F(43, 128), F(-15, 64))
rec("B2", "met" if okB2 else "failed", centre={k: [cen(s, k).js() for s in range(5)] for k in PR[0]})

EXT = ((239, 244), (156, 161), (87, 95), (82, 91), (86, 95))
px = lambda y: (F(531, 2) - y) / 280
GR = [(px(bot + 2), px(top - 2)) for top, bot in EXT]
RAW = [(px(bot), px(top)) for top, bot in EXT]
PRN = list(GR); PRN[3] = (F(648, 1000), F(672, 1000))

def vertices(intervals):
    # unknowns (c,a); return r_s = O_s + c (K_s-O_s) + a (A_s-O_s)
    cons = []  # (p,q,r): p c + q a <= r
    for s, (lo, hi) in enumerate(intervals):
        O = cen(s, "ordinary"); pc = cen(s, "count") - O; pa = cen(s, "alternate") - O
        cons.append((pc, pa, q(hi) - O)); cons.append((-pc, -pa, O - q(lo)))
    cons += [(Q2(-1), Q2(0), Q2(0)), (Q2(0), Q2(-1), Q2(0)), (Q2(1), Q2(1), Q2(1))]
    vs = []
    for (p1, q1, r1), (p2, q2, r2) in combinations(cons, 2):
        det = p1 * q2 - p2 * q1
        if det.sgn() == 0: continue
        c = (r1 * q2 - r2 * q1) / det; a = (p1 * r2 - p2 * r1) / det
        if all(le(p * c + qq * a, r) for p, qq, r in cons) and (c, a) not in vs:
            vs.append((c, a))
    return vs
vg = vertices(GR); vp = vertices(PRN)
vg_dec = sorted((round(c.fl(), 6), round(a.fl(), 6), round(1 - c.fl() - a.fl(), 6)) for c, a in vg)
claimV = sorted([(0.046462, 0.0, 0.953538), (0.121819, 0.0, 0.878181), (0.046462, 0.047892, 0.905646)])
O3 = cen(3, "ordinary"); K = Q2(F(63, 256))
w_alone = (Q2(F(648, 1000)) - K) / (O3 - K)
cmin = (Q2(F(85, 128)) - q(GR[2][1])) / (Q2(F(85, 128)) - K)
max135 = cmin * K + (1 - cmin) * O3
okB3 = vg_dec == claimV and len(vp) == 0 and round(w_alone.fl(), 6) == 0.953967 and \
    round(cmin.fl(), 10) == 0.0464619493 and round(max135.fl(), 9) == 0.647819382 and \
    round(0.648 - max135.fl(), 9) == 0.000180618
rec("B3", "met" if okB3 else "failed", vertices_graphic=vg_dec, n_vertices_printed=len(vp),
    w_printed_alone=w_alone.fl(), cmin=cmin.fl(), max135=max135.fl(), deficit=0.648 - max135.fl(),
    basis="comparison at the note's printed number of decimals")

def cert(U, L):
    lam = L / (4 * U); D = {}
    for m in MODES:
        h = 1 if m[0] == 0 else 0
        D[m] = {k: Q2(lam * (h - U)) * PR[0][k][m] + Q2(L - h) * PR[3][k][m] for k in PR[0]}
    nonneg = all(D[m][k].sgn() >= 0 for m in MODES for k in ("count", "alternate"))
    pos_c = all(D[m][k].sgn() > 0 for m in ((0, 0), (0, 1)) for k in ("count", "alternate"))
    thr = {}
    for m in MODES:
        mm = D[m]["count"] if le(D[m]["count"], D[m]["alternate"]) else D[m]["alternate"]
        if D[m]["ordinary"].sgn() < 0:
            thr[m] = (mm / (mm - D[m]["ordinary"]), "count" if le(D[m]["count"], D[m]["alternate"]) and not D[m]["count"] == D[m]["alternate"] else "alternate_or_tie")
    floor = None
    for m, (v, _) in thr.items():
        if floor is None or lt(v, floor): floor = v
    return D, nonneg, pos_c, thr, floor
CERT = {}
okB4 = True; okB5 = True; b5d = {}
for name, U, L, claim in (("graph", F(57, 560), F(69, 112), Q2(F(1, 2), F(-36403, 392160))),
                          ("printed", F(57, 560), F(81, 125), Q2(F(1, 2), F(-21563, 401280)))):
    D, nonneg, pos_c, thr, floor = cert(U, L)
    CERT[name] = (U, L, D, floor)
    okB4 &= nonneg and pos_c
    at = [m for m, (v, _) in thr.items() if v == floor]
    okB5 &= (floor == claim) and sorted(at) == [(0, 0), (0, 1)]
    b5d[name] = dict(floor=floor.js(), attained_at=at, negative_ordinary_modes=[str(m) for m in thr],
                     binding_minimum_at_centre=[thr[m][1] for m in at])
rec("B4", "met" if okB4 else "failed")
rec("B5", "met" if okB5 else "failed", detail=b5d)

def detected(weights, eff, s, percomp=None):
    num = Q2(); den = Q2()
    for m in MODES:
        for k, wk in weights.items():
            e = percomp[k][m] if percomp else eff[m]
            v = q(e) * q(wk) * PR[s][k][m]
            den = den + v
            if m[0] == 0: num = num + v
    return num, den

b6 = {}; okB6 = True
for name, (U, L, D, floor) in CERT.items():
    wts = dict(count=Q2(0), alternate=1 - floor, ordinary=floor)
    mix = lambda s, m: wts["alternate"] * PR[s]["alternate"][m] + wts["ordinary"] * PR[s]["ordinary"][m]
    # unknown e=(e1,e2,1) on (0,H),(0,V),(-4,H); two linear equations
    ms = [(0, 0), (0, 1), (-4, 0)]
    r0 = [Q2(1 - U) * mix(0, ms[0]), Q2(1 - U) * mix(0, ms[1]), Q2(-U) * mix(0, ms[2])]
    r1 = [Q2(L - 1) * mix(3, ms[0]), Q2(L - 1) * mix(3, ms[1]), Q2(L) * mix(3, ms[2])]
    det = r0[0] * r1[1] - r0[1] * r1[0]
    sol = None
    if det.sgn() != 0:
        e1 = ((-r0[2]) * r1[1] - r0[1] * (-r1[2])) / det
        e2 = (r0[0] * (-r1[2]) - (-r0[2]) * r1[0]) / det
        sol = [e1, e2, Q2(1)]
    info = dict(det_zero=det.sgn() == 0)
    if sol is None:
        # degenerate: equations dependent in (e1,e2); look for any nonneg solution by setting e2=0 or e1=0
        cands = []
        for idx in (0, 1):
            if r0[idx].sgn() != 0:
                e = (-r0[2]) / r0[idx]; v = [Q2(0), Q2(0), Q2(1)]; v[idx] = e
                cands.append(v)
        sol = cands[0] if cands else None
        info["degenerate_candidates"] = [[x.js() for x in v] for v in cands]
    eff = {m: Q2(0) for m in MODES}
    for m, e in zip(ms, sol): eff[m] = e
    rets = []
    for s in range(5):
        n_, d_ = detected(wts, eff, s); rets.append(n_ / d_ if d_.sgn() != 0 else None)
    good = all(e.sgn() >= 0 for e in sol) and rets[0] == U and rets[3] == L and rets[2] == 1 and rets[4] == 1
    okB6 &= good
    info.update(eff=[e.js() for e in sol], returns=[r.js() if r is not None else None for r in rets], ok=good)
    b6[name] = info
rec("B6", "met" if okB6 else "failed", detail=b6)

def rnd_eff():
    return {m: F(random.randint(0, 1000), 1000) if random.random() < 0.8 else F(0) for m in MODES}
b7 = {}
for name, (U, L, D, floor) in CERT.items():
    qual = sat = 0; sat_above = 0; qual_above = 0
    for i in range(3000):
        eff = rnd_eff()
        if i % 3 == 0:  # concentrate on the extremizer support
            eff = {m: F(0) for m in MODES}
            for m in ((0, 0), (0, 1), (-4, 0), random.choice(MODES)): eff[m] = F(random.randint(1, 1000), 1000)
        below = i % 2 == 0
        w = floor * F(random.randint(0, 999), 1000) if below else floor + (1 - floor) * F(random.randint(1, 1000), 1000)
        cfr = F(random.randint(0, 1000), 1000) if random.random() < 0.7 else F(0)
        wts = dict(count=(1 - w) * cfr, alternate=(1 - w) * (1 - cfr), ordinary=w)
        n0, d0 = detected(wts, eff, 0); n3, d3 = detected(wts, eff, 3)
        if d0.sgn() <= 0 or d3.sgn() <= 0: continue
        ok = le(n0, Q2(U) * d0) and le(Q2(L) * d3, n3)
        if below: qual += 1; sat += ok
        else: qual_above += 1; sat_above += ok
    b7[name] = dict(below_floor_qualifying=qual, below_floor_satisfying_both=sat,
                    above_floor_qualifying=qual_above, above_floor_satisfying_both=sat_above)
rec("B7", "measured", detail=b7, note="random search cannot prove the floor; B4/B5 are the proof steps, B6 the sharpness")

b8 = {}
for name, (U, L, D, floor) in CERT.items():
    eta = dict(count=F(1, 10 ** 6), alternate=F(1, 10 ** 6), ordinary=F(1))
    inc = dict(count=F(999, 2000), alternate=F(999, 2000), ordinary=F(1, 1000))
    pc = {k: {m: eta[k] for m in MODES} for k in eta}
    n0, d0 = detected(inc, None, 0, pc); n3, d3 = detected(inc, None, 3, pc)
    okA = le(n0, Q2(U) * d0) and le(Q2(L) * d3, n3)
    qual = sat = 0
    for i in range(2000):
        pcm = {k: rnd_eff() for k in eta}
        cfr = F(random.randint(0, 1000), 1000)
        wts = dict(count=cfr, alternate=1 - cfr, ordinary=F(0))
        n0, d0 = detected(wts, None, 0, pcm); n3, d3 = detected(wts, None, 3, pcm)
        if d0.sgn() <= 0 or d3.sgn() <= 0: continue
        qual += 1; sat += le(n0, Q2(U) * d0) and le(Q2(L) * d3, n3)
    b8[name] = dict(a_incident_w_0p001_satisfies_both=okA, r0=(n0 / d0).fl() if False else None,
                    b_w0_qualifying=qual, b_w0_satisfying_both=sat)
rec("B8", "met" if all(v["a_incident_w_0p001_satisfies_both"] and v["b_w0_satisfying_both"] == 0 for v in b8.values()) else "failed", detail=b8)

U9, L9 = RAW[0][1], RAW[3][0]
D, nonneg, pos_c, thr, floor = cert(U9, L9)
rec("B9", "measured", U=str(U9), L=str(L9), count_alt_nonneg=nonneg, centre_positive=pos_c,
    floor=floor.js() if floor is not None else None,
    attained_at=[str(m) for m, (v, _) in thr.items() if v == floor])

summ = {}
for k, v in R.items(): summ.setdefault(v["status"], []).append(k)
R["_summary"] = summ
OUT.write_text(json.dumps(R, indent=1, default=str) + "\n")
print(json.dumps(summ));
for k in ("A1","A2","A3","A4","A5","A6","A8","A9","A10","A2f","B3","B5","B6","B7","B8","B9"):
    print(k, json.dumps(R[k], default=str)[:900])
