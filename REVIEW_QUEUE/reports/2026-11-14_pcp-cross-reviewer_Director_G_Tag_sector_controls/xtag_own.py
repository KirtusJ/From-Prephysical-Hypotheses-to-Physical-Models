"""Own program for Director_G/Tag_sector_controls.md lines 1-118 (cross-review, same model family as author side).
Seed 20261113 (unused: everything is exhaustive and exact; recorded for the protocol).
Conventions: rail 0 = R holds u, rail 1 = L holds v; pair (u,v) at x sends u+v to (x+1,R), u-v to (x-1,L).
Mask: tag ^= 1 on arrival at tick 1 at x>0 (setting O). Plate '-': negate all tag-zero amplitudes right after that XOR.
Zero denominator -> fair 1/2. All arithmetic is fractions.Fraction (exact), so equality tests need no tolerance.
Only P12's curvature grid uses mpmath at 60 digits; it is reported as a measured value, no threshold applied.
Field is propagated by the linear recursion (not by word enumeration, which is the note's checker's method).

PREDICATES (fixed before first run). Each returns pass/fail; failures are kept in the result file.
P1  sector rule: marker mass == amplitude^2 / 2^(t-t0) at every cell, settings O,O',pure0,pure1,S, through tick 10.
P2  sector, sum, max rules give identical panels on pure0, pure1, S through tick 10.
P3  O: three rules coincide through tick 3; at t=3,x=1 pairs tag0=(1,0), tag1=(1,1); tag-one parent mass 1/4;
    right fractions 1, 5/6, 1; (0,L,1) at t=4 equals 0, 1/24, 0 (sector, sum, max).
P4  table: O_A=(-2,L,1), O_B=(2,R,1), S_A, S_B at tick 4 and cross ratio: sector (1/16,1/4,1/8,1/2,1),
    sum (1/16,5/24,1/8,1/2,6/5), max = sector row.
P5  max == sector at every cell through tick 4 in O,O',pure0,pure1,S; and the stated reason: at every tag-parent at
    ticks <=3 (hypothesis counted: parents with positive mass) u_b v_b = 0 or s_b >= s_other. Report first tick where
    max != sector in O (measured, not a predicate).
P6  O, tick 7, x=-1, tag 1: pair (1,2), other norm 8, mass 5/128 under sector and max; (-2,L,1) at tick 8 is 1/256, 5/512.
P7  A from all O panels through tick 8 (parents ticks 0..7, u_b v_b != 0, both b, plus 1) has 12 values; 37/38 not in A;
    parent (t=8,x=6,b=1) mass 37/256; tick-9 cells (7,R,1),(5,L,1): sector 49/512,25/512; c1 43/512,31/512; c2 40/512,34/512;
    c1 and c2 rules equal sector at every cell through tick 8; every right fraction of c1,c2 visited lies in [0,1].
P8  (not in note) for calibration depth T=3..12: hypothesis r_n notin A_T with n=T-2 tested per T and counted; for qualifying T
    rules c1=r/H(r), c2=3c1 equal sector through tick T and at tick T+1 give tag-one right fractions 1/2+n/(2(n^2+1)) and
    1/2+n/(4(n^2+1)) at the parent x=T-2 with parent mass (n^2+1)/2^T.
P9  edge words: t=3..14, x=t-2: tag-one pair (t-2,1), tag-zero pair (+1,0) (identity plate) and (-1,0) (sign plate).
P10 relative-sign rule: q+_n = 1/2 and q-_n = 1/2+2n/(n^2+5), n=0..12 (note's checker stops at n=6); X_0=1,
    X_{n+1}=2 q_n X_n+1 matches 2^(n+2) * parent mass; X+_n=n+1; X-_n >= X-_3 n(n+1)/12 for 3<=n<=12; n=2 masses 3/16, 13/48;
    equal mean 13/18; pooled 151/198. Scaled excesses n(mean-1/2), n(pooled-1/2) reported (measured).
P11 cusp rule: both edge fractions exactly 1/2 for n=0..12 under both plates; equals sector panels on pure0, pure1 through tick 10.
P12 curvature: required lower bounds 2 n^2 |49/74 - q| at n=6 are 216/37 (c1), 324/37 (c2); Taylor bound
    |mean - (1/2+n/(n^2+1))| <= M/(2n^2) with M = grid max of |g_zz(1/n,z)| on 401 rational points of [-1/n,1/n]
    (a lower estimate of the sup, so a pass with it implies a pass with the sup) for the sum rule and the relative-sign
    rule, n=1..12. Actual grid max of |g_zz(1/6,z)| for c1, c2 reported (measured).
P13 ring: O and S on a ring of N sites agree with the line through tick 4 for N=9..12, three rules. First differing tick for
    N=5..12 reported (measured).
P14 boundary: sector right fraction with other sector (1,0) is exactly 1 on (a,a) and 0 on (a,-a) for a=10^-k, k=1..12;
    sum and max rules there give |K-1/2| = a^2/(2a^2+1) and a^2/max(2a^2,1), both -> 0.
P15 stored results/tag_sector_controls.json: 464 cells, 24 panels, 5 settings; every stored (signed words, sector mass,
    spectator mass) equals mine.
"""
import json, sys, os
from fractions import Fraction as F
from math import prod
SEED = 20261113
HALF = F(1, 2)

def sector(u, v, a, b):
    s = u*u+v*v
    return HALF + (F(u*v, s) if s else 0)
def summ(u, v, a, b):
    s = u*u+v*v+a*a+b*b
    return HALF + (F(u*v, s) if s else 0)
def maxr(u, v, a, b):
    s = max(u*u+v*v, a*a+b*b)
    return HALF + (F(u*v, s) if s else 0)
def relsign(u, v, a, b):
    d = u*u+(v-a)**2+a*a+b*b
    return HALF + (F(u*(v-a), d) if d else 0)
def cusp(u, v, a, b):
    S = u*u+v*v+a*a+b*b
    if not S: return HALF
    return HALF + min(HALF, max(-HALF, F(u*v-abs(u*a), S)))
def analytic(A, c):
    def rule(u, v, a, b):
        sb = u*u+v*v; S = sb+a*a+b*b
        if not S: return HALF
        r = F(sb, S)
        return HALF + F(u*v, S)/(r + c*prod((r-x)**2 for x in A))
    return rule

# settings: (start tick, site, tag, mask)
SET = {"O": (0, 0, 0, True), "O1": (0, 0, 1, True), "pure0": (0, 0, 0, False), "pure1": (0, 0, 1, False), "S": (1, 1, 1, False)}

def norm(x, N):
    return x if N is None else x % N

def run(setting, rule, T, plate=False, N=None, probs=None):
    """returns {tick: (amp, mass)}; amp, mass dicts keyed (x,b,rail)."""
    t0, x0, b0, mask = setting
    amp = {(norm(x0, N), b0, 0): 1}; mass = {(norm(x0, N), b0, 0): F(1)}
    out = {t0: (amp, mass)}
    for t in range(t0, T):
        namp, nmass = {}, {}
        sites = {(x, b) for (x, b, r) in amp} | {(x, b) for (x, b, r) in mass}
        for x, b in sites:
            u, v = amp.get((x, b, 0), 0), amp.get((x, b, 1), 0)
            a, bb = amp.get((x, b ^ 1, 0), 0), amp.get((x, b ^ 1, 1), 0)
            m = mass.get((x, b, 0), F(0)) + mass.get((x, b, 1), F(0))
            K = rule(u, v, a, bb)
            if probs is not None: probs.append(K)
            for rail, val, k in ((0, u+v, K), (1, u-v, 1-K)):
                y = norm(x + 1 - 2*rail, N)
                nb = b ^ int(mask and t+1 == 1 and (x + 1 - 2*rail) > 0)
                key = (y, nb, rail)
                assert key not in nmass, "unique parent"
                if plate and mask and t+1 == 1 and nb == 0: val = -val
                if val: namp[key] = namp.get(key, 0) + val
                nmass[key] = m*k
        amp = namp; mass = {k: v for k, v in nmass.items()}
        out[t+1] = (amp, mass)
    return out

def panel_eq(p, q, upto):
    for t in p:
        if t > upto: continue
        ks = set(p[t][1]) | set(q[t][1])
        if any(p[t][1].get(k, 0) != q[t][1].get(k, 0) for k in ks): return False
    return True
def first_diff(p, q):
    for t in sorted(p):
        if not panel_eq({t: p[t]}, {t: q[t]}, t): return t
    return None

R = {"seed": SEED, "predicates": {}, "measured": {}, "failed": []}
def rec(name, ok, detail=None):
    R["predicates"][name] = {"pass": bool(ok), "detail": detail}
    if not ok: R["failed"].append(name)

def pair(amp, x, b): return (amp.get((x, b, 0), 0), amp.get((x, b, 1), 0))
def pm(mass, x, b): return mass.get((x, b, 0), F(0)) + mass.get((x, b, 1), F(0))

# P1
ok = True; n = 0
for s in SET.values():
    p = run(s, sector, 10)
    for t, (amp, mass) in p.items():
        for k in set(amp) | set(mass):
            n += 1; ok &= mass.get(k, 0) == F(amp.get(k, 0)**2, 2**(t-s[0]))
        ok &= sum(mass.values()) == 1
rec("P1", ok, f"{n} cells")
# P2
ok = all(panel_eq(run(SET[s], sector, 10), run(SET[s], r, 10), 10) for s in ("pure0", "pure1", "S") for r in (summ, maxr))
rec("P2", ok)
# P3
O = {nm: run(SET["O"], r, 10) for nm, r in (("sector", sector), ("sum", summ), ("max", maxr))}
Sx = {nm: run(SET["S"], r, 10) for nm, r in (("sector", sector), ("sum", summ), ("max", maxr))}
amp3 = O["sector"][3][0]
d = {"coincide3": panel_eq(O["sector"], O["sum"], 3) and panel_eq(O["sector"], O["max"], 3),
     "pairs": [pair(amp3, 1, 0), pair(amp3, 1, 1)],
     "parent": [str(pm(O[k][3][1], 1, 1)) for k in O],
     "fractions": [str(r(1, 1, 1, 0)) for r in (sector, summ, maxr)],
     "cell(0,L,1)@4": [str(O[k][4][1].get((0, 1, 1), 0)) for k in O]}
rec("P3", d["coincide3"] and d["pairs"] == [(1, 0), (1, 1)] and d["parent"] == ["1/4"]*3 and d["fractions"] == ["1", "5/6", "1"]
    and d["cell(0,L,1)@4"] == ["0", "1/24", "0"], d)
# P4
tab = {}
for k in O:
    oa, ob = O[k][4][1].get((-2, 1, 1), 0), O[k][4][1].get((2, 1, 0), 0)
    sa, sb = Sx[k][4][1].get((-2, 1, 1), 0), Sx[k][4][1].get((2, 1, 0), 0)
    tab[k] = [str(z) for z in (oa, ob, sa, sb, oa*sb/(ob*sa))]
exp = {"sector": ["1/16", "1/4", "1/8", "1/2", "1"], "sum": ["1/16", "5/24", "1/8", "1/2", "6/5"], "max": ["1/16", "1/4", "1/8", "1/2", "1"]}
rec("P4", tab == exp, tab)
# P5
ok = True; q = 0; bad = []
for nm, s in SET.items():
    ps, pmx = run(s, sector, 10), run(s, maxr, 10)
    ok &= panel_eq(ps, pmx, 4)
    for t in range(s[0], 4):
        amp, mass = ps[t]
        for (x, b) in {(x, b) for (x, b, r) in mass}:
            if pm(mass, x, b) > 0:
                q += 1
                u, v = pair(amp, x, b); a, bb = pair(amp, x, b ^ 1)
                if not (u*v == 0 or u*u+v*v >= a*a+bb*bb): bad.append((nm, t, x, b))
rec("P5", ok and not bad, {"positive-mass parents tested": q, "violations": bad})
R["measured"]["first tick max != sector in O (ticks to 10)"] = first_diff(O["sector"], O["max"])
R["measured"]["first tick sum != sector in O"] = first_diff(O["sector"], O["sum"])
# P6
a7 = O["sector"][7][0]
d = {"pair": pair(a7, -1, 1), "other": sum(z*z for z in pair(a7, -1, 0)),
     "mass": [str(pm(O[k][7][1], -1, 1)) for k in ("sector", "max")],
     "daughter": [str(O[k][8][1].get((-2, 1, 1), 0)) for k in ("sector", "max")]}
rec("P6", d["pair"] == (1, 2) and d["other"] == 8 and d["mass"] == ["5/128"]*2 and d["daughter"] == ["1/256", "5/512"], d)

def Aset(T):
    """r values at parents of ticks 0..T-1 with u_b v_b != 0, plus 1 (setting O)."""
    A = {F(1)}
    p = run(SET["O"], sector, T)
    for t in range(T):
        amp = p[t][0]
        for (x, b) in {(x, b) for (x, b, r) in amp}:
            u, v = pair(amp, x, b); a, bb = pair(amp, x, b ^ 1)
            if u*v: A.add(F(u*u+v*v, u*u+v*v+a*a+bb*bb))
    return A
# P7
A8 = Aset(8); rs = F(37, 38)
H = lambda A, r: prod((r-x)**2 for x in A)
c1 = rs/H(A8, rs)
ref = run(SET["O"], sector, 9)
d = {"|A|": len(A8), "A": sorted(str(x) for x in A8), "37/38 in A": rs in A8, "mass": str(pm(ref[8][1], 6, 1)), "rows": {}}
ok = len(A8) == 12 and rs not in A8 and pm(ref[8][1], 6, 1) == F(37, 256)
for nm, rule, e in (("sector", sector, (49, 25)), ("c1", analytic(A8, c1), (43, 31)), ("c2", analytic(A8, 3*c1), (40, 34))):
    pr = []
    p = run(SET["O"], rule, 9, probs=pr)
    got = (p[9][1].get((7, 1, 0), 0), p[9][1].get((5, 1, 1), 0))
    d["rows"][nm] = [str(g) for g in got] + [panel_eq(p, ref, 8), all(0 <= k <= 1 for k in pr), first_diff(p, ref)]
    ok &= got == (F(e[0], 512), F(e[1], 512)) and panel_eq(p, ref, 8) and all(0 <= k <= 1 for k in pr)
rec("P7", ok, d)
# P8
d = {}; ok = True; qual = 0
for T in range(3, 13):
    n = T-2; A = Aset(T); r = F(n*n+1, n*n+2)
    if r in A: d[T] = "hypothesis r_n notin A FAILS; not tested"; continue
    qual += 1
    c = r/H(A, r); ref = run(SET["O"], sector, T+1)
    row = [len(A)]
    for mult, den in ((1, 2), (3, 4)):
        pr = []
        p = run(SET["O"], analytic(A, mult*c), T+1, probs=pr)
        m = pm(p[T][1], n, 1); right = p[T+1][1].get((n+1, 1, 0), 0)
        good = panel_eq(p, ref, T) and m == F(n*n+1, 2**T) and right/m == HALF + F(n, den*(n*n+1)) and not panel_eq(p, ref, T+1) \
            and all(0 <= k <= 1 for k in pr)
        ok &= good; row += [str(right/m), good]
    d[T] = row
rec("P8", ok, {"qualifying": f"{qual} of 10", "rows [|A|, K_c1, ok, K_c2, ok]": d})
# P9
okp = True
for plate, sg in ((False, 1), (True, -1)):
    p = run(SET["O"], sector, 14, plate=plate)
    for t in range(3, 15):
        okp &= pair(p[t][0], t-2, 1) == (t-2, 1) and pair(p[t][0], t-2, 0) == (sg, 0)
rec("P9", okp)
# P10, P11
d = {}; ok = True; okc = True; X = {}; q = {}
for plate, lab in ((False, "+"), (True, "-")):
    p = run(SET["O"], relsign, 15, plate=plate); pc = run(SET["O"], cusp, 15, plate=plate)
    Xn = F(1); X[lab] = []; q[lab] = []
    for n in range(0, 13):
        t = n+2; m = pm(p[t][1], n, 1)
        Rr, L = p[t+1][1].get((n+1, 1, 0), 0), p[t+1][1].get((n-1, 1, 1), 0)
        e = HALF + (F(2*n, n*n+5) if plate else 0)
        ok &= Rr+L == m and Rr/(Rr+L) == e and 2**t*m == Xn
        X[lab].append(Xn); q[lab].append((Rr, L, m)); Xn = 2*e*Xn+1
        mc = pm(pc[t][1], n, 1); Rc, Lc = pc[t+1][1].get((n+1, 1, 0), 0), pc[t+1][1].get((n-1, 1, 1), 0)
        okc &= mc > 0 and Rc == Lc
ok &= all(X["+"][n] == n+1 for n in range(13)) and all(X["-"][n] >= X["-"][3]*F(n*(n+1), 12) for n in range(3, 13))
ok &= q["+"][2][2] == F(3, 16) and q["-"][2][2] == F(13, 48)
mean2 = (q["+"][2][0]/q["+"][2][2] + q["-"][2][0]/q["-"][2][2])/2
pool2 = (q["+"][2][0]+q["-"][2][0])/(q["+"][2][2]+q["-"][2][2])
ok &= mean2 == F(13, 18) and pool2 == F(151, 198)
sc = {}
for n in range(1, 13):
    mean = (q["+"][n][0]/q["+"][n][2] + q["-"][n][0]/q["-"][n][2])/2
    pool = (q["+"][n][0]+q["-"][n][0])/(q["+"][n][2]+q["-"][n][2])
    sc[n] = [round(float(n*(mean-HALF)), 6), round(float(n*(pool-HALF)), 6),
             round(float(F(n, 2)*(q["+"][n][0]/q["+"][n][2] - q["-"][n][0]/q["-"][n][2])), 6)]
rec("P10", ok, {"mean n=2": str(mean2), "pooled n=2": str(pool2), "X-": [str(x) for x in X["-"]]})
R["measured"]["relsign n: [n(mean-1/2), n(pooled-1/2), (n/2)(q+ - q-)] (limits claimed 1, 2, gamma=-1)"] = sc
okc &= all(panel_eq(run(SET[s], cusp, 10), run(SET[s], sector, 10), 10) for s in ("pure0", "pure1"))
okr = all(panel_eq(run(SET[s], relsign, 10), run(SET[s], sector, 10), 10) for s in ("pure0", "pure1"))
rec("P11", okc, {"relsign also equals pure panels": okr})
# P12
import sympy as sp, mpmath as mp
mp.mp.dps = 60
z = sp.Symbol("z")
def gz2(expr): return sp.diff(expr, z, 2)
def gridmax(expr, n, pts=401):
    f = sp.lambdify(z, gz2(expr), "mpmath")
    return max(abs(f(mp.mpf(-1)/n + mp.mpf(2*i)/(n*(pts-1)))) for i in range(pts))
req = [str(2*36*abs(F(49, 74)-F(k, 74))) for k in (43, 40)]
ok = req == ["216/37", "324/37"]; rows = {}
for n in range(1, 13):
    y = sp.Rational(1, n); pure = HALF + F(n, n*n+1)
    for nm, expr, rule in (("sum", sp.Rational(1, 2)+y/(1+y**2+z**2), summ), ("relsign", sp.Rational(1, 2)+(y-z)/(1+(y-z)**2+z**2), relsign)):
        mean = (rule(n, 1, 1, 0)+rule(n, 1, -1, 0))/2
        M = gridmax(expr, n); lhs = abs(mean-pure)
        good = mp.mpf(lhs.numerator)/lhs.denominator <= M/(2*n*n)
        ok &= bool(good); rows[f"{nm} n={n}"] = [float(lhs), float(M/(2*n*n)), bool(good)]
act = {}
y6 = sp.Rational(1, 6)
for nm, mult in (("c1", 1), ("c2", 3)):
    S_ = 1+y6**2+z**2; r_ = (1+y6**2)/S_
    Hs = sp.Integer(1)
    for a in A8: Hs *= (r_-sp.Rational(a.numerator, a.denominator))**2
    cc = sp.Rational(c1.numerator, c1.denominator)*mult
    expr = sp.Rational(1, 2)+(y6/S_)/(r_+cc*Hs)
    f0 = sp.lambdify(z, expr, "mpmath")
    act[nm] = {"g(1/6,1/6)": mp.nstr(f0(mp.mpf(1)/6), 20), "grid max |g_zz|, 401 pts": mp.nstr(gridmax(expr, 6), 20),
               "grid max |g_zz|, 4001 pts": mp.nstr(gridmax(expr, 6, 4001), 20)}
rec("P12", ok, {"required": req, "taylor rows [|mean-pure|, M/(2n^2), ok]": rows})
R["measured"]["actual curvature of the note's analytic rules on z in [-1/6,1/6] at y=1/6"] = act
# P13
ok = True; fd = {}
for N in range(5, 13):
    worst = None
    for sn in ("O", "S"):
        for rule in (sector, summ, maxr):
            line = run(SET[sn], rule, 10); ring = run(SET[sn], rule, 10, N=N)
            for t in sorted(line):
                fold = {}
                for (x, b, r), m in line[t][1].items(): fold[(x % N, b, r)] = fold.get((x % N, b, r), 0)+m
                ks = set(fold) | set(ring[t][1])
                if any(fold.get(k, 0) != ring[t][1].get(k, 0) for k in ks):
                    worst = t if worst is None else min(worst, t); break
    fd[N] = worst
    if N >= 9: ok &= worst is None or worst > 4
rec("P13", ok, {"first differing tick per N (None = none through tick 10)": fd})
# P14
ok = True
for k in range(1, 13):
    a = F(1, 10**k)
    ok &= sector(a, a, 1, 0) == 1 and sector(a, -a, 1, 0) == 0
    ok &= abs(summ(a, a, 1, 0)-HALF) == a*a/(2*a*a+1) and abs(maxr(a, -a, 1, 0)-HALF) == a*a/max(2*a*a, 1)
rec("P14", ok)
# P15
stored = json.load(open(sys.argv[1]))
nm_map = {"pure_0": "pure0", "pure_1": "pure1", "overlap_0": "O", "overlap_1": "O1", "shield": "S"}
cells = 0; panels_n = 0; ok = True
for name, plist in stored["settings"].items():
    ps, pq = run(SET[nm_map[name]], sector, 4), run(SET[nm_map[name]], summ, 4)
    for pan in plist:
        panels_n += 1; t = pan["tick"]
        for x, b, r, w, ms, mq in pan["cells"]:
            cells += 1
            ok &= ps[t][0].get((x, b, r), 0) == w and ps[t][1].get((x, b, r), 0) == F(ms) and pq[t][1].get((x, b, r), 0) == F(mq)
        ok &= sum(1 for v in ps[t][1].values() if v) <= len(pan["cells"])
rec("P15", ok and cells == 464 and panels_n == 24 and len(stored["settings"]) == 5, {"cells": cells, "panels": panels_n})

out = sys.argv[2]
with open(out, "x") as f:
    json.dump(R, f, indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
