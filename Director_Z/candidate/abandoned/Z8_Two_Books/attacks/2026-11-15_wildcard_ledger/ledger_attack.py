"""Attack on candidate Z8 "Two Books" (STIPULATED CANDIDATE FOR DISPROOF). Wildcard, seed word 'ledger', 15 Nov 2026.
Own implementation of S1-S5: state = {(x,rail): (eps, n)}, rail 0 = R, 1 = L; start {(0,R): (1,1)};
right step -> (x+1,R) sign +1; left step -> (x-1,L), sign -1 iff from rail L. Mask = set of admitted sites.
H is held exactly as {n: Fraction coefficient of log n} over vertices with eps != 0 (n = 1 dropped).
PREDICATES, fixed before the first run (True = the attack's claim is confirmed):
 A1 RECURRENCE. On some ring N in 1..8, running free from the sharp start with NO mask, there is T > 0 with
    eps_T = c * eps_0 (all signed weight at (0,R), so every chance now and under every continuation equals
    that of the sharp start), while H_T > 0 = H_0.  Reported: every (N, T <= 60) where it happens, with H_T.
 A2 SAME STATE, DIFFERENT H AT EQUAL LENGTH. Among all mask sequences on rings 3 and 4 (lengths <= 5, <= 4) there
    are two events of the SAME ring and SAME length with proportional eps vectors and different H.
 A3 BRAND/OVERVIEW EQUALITY WORDING. Among all events on rings 3,4,5 (lengths <= 5,4,3) there is one whose H is
    unchanged by a free step (exact integer equality) although some OCCUPIED site has walks on both rails.
    Also reported: number of equality cases, and number violating FORM's wording (expected 0).
 A4 Q4 RECOMPUTED. Ring 3, an event of length 5, further mask {2}: H falls from exactly (2/3) log 2 to 0 exists.
 A5 Q5 RECOMPUTED (80-digit decimals). Line H at T=8,32,64 rounds to 2.637, 14.799, 31.571 and gaps to 2.908, 7.381,
    12.791.  A5b: "rises at every step" is FALSE as worded: some step T-1 -> T in 1..64 has H unchanged.
 A6 CONTROL. For every event of length 3 on rings 1..7, max n(v) <= 4 = 2^(T-1), and H = 2 log 2 exactly is attained;
    so the largest H at length 3 is 2 log 2 < 3 log 2 (the T-4 ceiling is not attained).
 A7 PLOT. Every interval [lo,hi] in function/plot_mean_entropy.json has width 1e-6 and contains the 80-digit value
    of the series quantity at that length (H or T log2 - H); reported: count, failures.
 A8 n FROM MASKS ALONE. n(v) obtained by propagating counts only (no signs) equals n(v) from brute enumeration of
    signed walks, on 300 random masked events (seed 20261115, ring 5, length 6).
Usage: python3 ledger_attack.py RESULT.json PLOT.json   (result opened with mode 'x')."""
import sys, json, itertools, random, collections
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
getcontext().prec = 80
OUT, PLOT = sys.argv[1], sys.argv[2]
START = {(0, 0): (1, 1)}
def step(st, N, mask=None):
    new = {}
    for (x, r), (e, n) in st.items():
        for y, r2, s in ((x + 1, 0, 1), (x - 1, 1, -1 if r == 1 else 1)):
            if N is not None: y %= N
            if mask is not None and y not in mask: continue
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + e * s, b + n)
    return new
def weight(st): return sum(e * e for e, n in st.values())
def H(st):
    W = weight(st); d = collections.defaultdict(Fr)
    for e, n in st.values():
        if e and n > 1: d[n] += Fr(e * e, W)
    return tuple(sorted(d.items()))
def Hdec(st):
    W = weight(st); return sum(Decimal(e * e) / Decimal(W) * Decimal(n).ln() for e, n in st.values() if e)
def Hstr(h): return " + ".join("%s*log(%d)" % (c, n) for n, c in h) or "0"
def prim(st):
    from math import gcd
    items = sorted((v, e) for v, (e, n) in st.items() if e); g = 0
    for v, e in items: g = gcd(g, abs(e))
    sg = 1 if items[0][1] > 0 else -1
    return tuple((v, sg * e // g) for v, e in items)
def events(N, Lmax):
    masks = [frozenset(c) for k in range(1, N + 1) for c in itertools.combinations(range(N), k)]
    def rec(st, d, seq):
        if d: yield st, d, seq
        if d == Lmax: return
        for m in masks:
            nx = step(st, N, m)
            if nx: yield from rec(nx, d + 1, seq + (tuple(sorted(m)),))
    yield from rec(START, 0, ())
rep = {"argv": sys.argv}
# A1
a1 = []
for N in range(1, 9):
    st = START
    for T in range(1, 61):
        st = step(st, N)
        if prim(st) == (((0, 0), 1),): a1.append({"N": N, "T": T, "eps_at_0R": st[(0, 0)][0], "n_at_0R": st[(0, 0)][1], "H": Hstr(H(st)), "H_float": float(Hdec(st))})
rep["A1"] = a1; P = {"A1": any(r["H_float"] > 0 for r in a1)}
# A2
a2 = None; a2_groups = 0
for N, L in ((3, 5), (4, 4)):
    grp = collections.defaultdict(dict)
    for st, d, seq in events(N, L):
        if weight(st): grp[(N, d, prim(st))].setdefault(H(st), seq)
    for k, hs in grp.items():
        if len(hs) > 1:
            a2_groups += 1
            if a2 is None or k[1] < a2["length"]:
                (h1, s1), (h2, s2) = sorted(hs.items())[:2]
                a2 = {"N": k[0], "length": k[1], "eps_primitive": [[list(v), e] for v, e in k[2]], "event_1_masks": s1, "H_1": Hstr(h1), "event_2_masks": s2, "H_2": Hstr(h2)}
rep["A2"] = {"groups_with_more_than_one_H": a2_groups, "smallest_example": a2}; P["A2"] = a2 is not None
# A3
eqc = formbad = brandbad = 0; a3 = None; cases = 0; g1fail = 0
for N, L in ((3, 5), (4, 4), (5, 3)):
    for st, d, seq in events(N, L):
        if not weight(st): continue
        cases += 1; by = collections.defaultdict(lambda: [(0, 0), (0, 0)])
        for (x, r), v in st.items(): by[x][r] = v
        lhs = rhs = 1; form_ok = True; both = False
        for x, ((eR, nR), (eL, nL)) in by.items():
            lhs *= (nR + nL) ** (eR * eR + eL * eL); rhs *= nR ** (eR * eR) * nL ** (eL * eL)
            if (eR or eL) and nR and nL: form_ok = False        # FORM: site carrying chance has walks on both rails
            if nR and nL: both = True                           # BRAND: occupied site has walks on both rails
        if lhs < rhs: g1fail += 1
        if lhs == rhs:
            eqc += 1
            if not form_ok: formbad += 1
            if both:
                brandbad += 1
                if a3 is None or d < a3["length"]: a3 = {"N": N, "length": d, "masks": seq, "state": [[list(v), e, n] for v, (e, n) in sorted(st.items())], "H_before": Hstr(H(st)), "H_after": Hstr(H(step(st, N)))}
        elif form_ok: formbad += 1
rep["A3"] = {"events": cases, "T1_failures": g1fail, "equality_cases": eqc, "FORM_wording_mismatches": formbad, "equality_cases_where_an_occupied_site_has_walks_on_both_rails": brandbad, "smallest_example": a3}
P["A3"] = brandbad > 0
# A4
a4 = None
for st, d, seq in events(3, 5):
    if d == 5 and weight(st) and H(st) == ((2, Fr(2, 3)),):
        nx = step(st, 3, {2})
        if nx and weight(nx) and H(nx) == ():
            a4 = {"masks": seq, "H_before": Hstr(H(st)), "H_before_float": float(Hdec(st)), "H_after": "0", "state_before": [[list(v), e, n] for v, (e, n) in sorted(st.items())]}; break
rep["A4"] = a4; P["A4"] = a4 is not None
# A5
st = START; hs = {0: Decimal(0)}; ln2 = Decimal(2).ln(); flat = []
for T in range(1, 65):
    st = step(st, None); hs[T] = Hdec(st)
    if hs[T] == hs[T - 1]: flat.append(T)
q = lambda x: str(x.quantize(Decimal("0.001")))
rep["A5"] = {"H": {T: q(hs[T]) for T in (8, 32, 64)}, "gap": {T: q(T * ln2 - hs[T]) for T in (8, 32, 64)}, "steps_T_with_H_unchanged_from_T_minus_1": flat}
P["A5"] = rep["A5"]["H"] == {8: "2.637", 32: "14.799", 64: "31.571"} and rep["A5"]["gap"] == {8: "2.908", 32: "7.381", 64: "12.791"}; P["A5b"] = bool(flat)
# A6
mx = 0; att = []; best = Decimal(0)
for N in range(1, 8):
    for st, d, seq in events(N, 3):
        if d != 3: continue
        mx = max(mx, max(n for e, n in st.values()))
        if weight(st):
            best = max(best, Hdec(st))
            if H(st) == ((4, Fr(1)),): att.append([N, seq])
rep["A6"] = {"max_n_at_length_3": mx, "events_with_H_exactly_2log2": len(att), "first": att[0] if att else None, "max_H_float": float(best), "2log2": float(2 * ln2), "3log2": float(3 * ln2)}
P["A6"] = mx <= 4 and bool(att) and abs(best - 2 * ln2) < Decimal("1e-70")   # 80-digit arithmetic; exact attainment is the Fraction test
# A7
pl = json.load(open(PLOT)); cnt = bad = 0; badl = []
for s in pl["series"]:
    gap = "gap" in s["name"].lower() or "ceiling" in s["name"].lower()
    for T, lo, hi in s["data"]:
        lo, hi = Fr(lo), Fr(hi); val = T * ln2 - hs[T] if gap else hs[T]; cnt += 1
        ok = hi - lo == Fr(1, 10**6) and Decimal(lo.numerator) / Decimal(lo.denominator) <= val <= Decimal(hi.numerator) / Decimal(hi.denominator)
        if not ok: bad += 1; badl.append([s["name"], T, str(lo), str(hi), str(val)[:20]])
rep["A7"] = {"series": [s["name"] for s in pl["series"]], "intervals": cnt, "failures": bad, "failed": badl}; P["A7"] = cnt > 0 and bad == 0
# A8
rng = random.Random(20261115); a8bad = 0; a8n = 0
for _ in range(300):
    N, L = 5, 6; seq = [set(rng.sample(range(N), rng.randint(2, N))) for _ in range(L)]
    cnt_only = {(0, 0): 1}
    for m in seq:
        nw = collections.defaultdict(int)
        for (x, r), n in cnt_only.items():
            for y, r2 in (((x + 1) % N, 0), ((x - 1) % N, 1)):
                if y in m: nw[(y, r2)] += n
        cnt_only = dict(nw)
    brute = collections.defaultdict(int)
    for w in itertools.product((1, -1), repeat=L):
        x = 0; ok = True
        for s, m in zip(w, seq):
            x = (x + s) % N
            if x not in m: ok = False; break
        if ok: brute[(x, 0 if w[-1] == 1 else 1)] += 1
    a8n += 1
    if dict(brute) != cnt_only: a8bad += 1
rep["A8"] = {"events": a8n, "mismatches": a8bad}; P["A8"] = a8bad == 0
rep["predicates"] = P
json.dump(rep, open(OUT, "x"), indent=1); print(P)
