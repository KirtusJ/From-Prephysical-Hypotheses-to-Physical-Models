"""xr91 cross-review program (own implementation; exact arithmetic unless marked).

Convention: state (x,flag)->(r,l) integer amplitudes, coin (r,l)->(r+l, r-l), R moves +1,
L moves -1, common factor 2^(-T/2) omitted. A mark (t0,x0) acts after t0 ticks, before the
next coin. 'sign' multiplies both rails by -1; 'flag' toggles a retained bit.
Non-integer exponents: Decimal at 60 digits; no tolerance is used: each such predicate
reports the smallest |separation| seen, and counts as pass only if it exceeds 1e-40
(basis: 60-digit working precision, values of order 1e-3..1, so rounding < 1e-50).

PREDICATES (fixed before first run; each records qualifying / pass / fail):
C1 control: tick-2 site probabilities (1/4,1/2,1/4) by brute path enumeration; q=2 -> (1/6,2/3,1/6).
A1 five-tick tables bare (1,5,4,4,17,1), sign (1,5,0,8,17,1); seven-tick bare
   (1,17,5,9,17,41,37,1), sign (1,17,5,25,25,17,37,1); path enumeration == propagation.
A2 cone: monitors satisfy |x-x0| > T-t0 AND their rail amplitudes are identical in both settings.
A3 q=2 rates 289/348, 289/380, 1/348, 1/380.
A4 W5(q)>0 for every q in GRID, q!=1; W5(1)=0; support limit q->0 equals 8/15.
A5 W7(q)>0 for q in GRID, q!=1; support limit 0; 1-W7(64) < 1e-3 (direction of limit only).
A6 blank tables: five (1,5,2,6,17,1), seven (1,17,5,17,21,29,37,1), = average of bare and sign;
   ring bare (0,128,256,128), flagged (64,96,256,96); R(0)=1/12; R>0 on GRID<1, R<0 on GRID>1.
A7 blank witnesses >0 on GRID q!=1, and support limit 0 for both.
A8 dark wells: fair 10/32 at -1 (5 ticks), 136/512 at ring site 1; Born blank rate at -1 = 2/32.
A9 clock cut: q=2 deficit 2/21.
B1 five-tick flag cells (0,1),(0,5),(1,1),(5,1),(17,0),(1,0); Z=348,356,344; 89/261 mixture cancels.
B2 seven-tick and ring flag tables as printed; bare strictly majorizes all 8 partitions (each).
B3 L(q,p)>0 for all 8 partitions, GRID q!=1; J(q,r)>=0 for q<1, <0 for q>1, all 8 ring partitions.
B4 extension not in note: bare vs RAIL-resolved refinements of marked cells (majorization still holds?)
   and rail-resolved in BOTH arms (does the sign survive?).
U1 UNREPORTED PARAMETERS: every line instance T in 3..9, 1<=t0<T, x0 occupied at t0, kinds sign and
   flag. Hypothesis per instance: table changes AND >=2 occupied wells outside cone. Predicate:
   sign(Zb(q)-Zm(q)) == sign(q-1) on GRID. Fails kept with the exponents of sign failure.
R1 rival (a) unnormalised f(p)=p^2: remote differences exactly 0; total rate != 1.
R2 rival (b) rail-resolved power law and |r+l|^2 power law: do remote rates change (q=2)?
R3 rival (c) setting-dependent mixtures on integer exponents 1..8: exact weights matching both remote rates.
R4 rival (d) site-dependent exponent (q=1 on {-1,1,3}, q=2 elsewhere): all four line tests pass exactly, differs from Born.
R5 rival block-normalised law, blocks {-7,-5,-3},{-1,1},{3},{5,7}, q=2 in block, Born between blocks.
R6 loss: setting-dependent efficiency eta_b/eta_m = Zb/Zm makes q=2 pass; makes q=1 fail unless ratio 1.
R7 pure exponent, setting-dependent (q,q'): both remote equalities force q=q'=1 (grid of pairs).
Fixed seed 20261114 (used only for nothing random: recorded for form; all scans exhaustive).
"""
import sys, json, itertools, hashlib
from fractions import Fraction as F
from decimal import Decimal, getcontext
from math import comb
getcontext().prec = 60
SEED = 20261114
GRID = [F(n, 20) for n in range(1, 41)] + [F(n) for n in range(3, 13)] + [F(16), F(24), F(40), F(64)]
RES = {"seed": SEED, "predicates": {}, "data": {}}

def rec(name, qualifying, passed, failed, detail=None):
    RES["predicates"][name] = dict(qualifying=qualifying, passed=passed, failed=failed, detail=detail)

def step(state, ring=None):
    out = {}
    for (x, f), (r, l) in state.items():
        for dx, rail, a in ((1, 0, r + l), (-1, 1, r - l)):
            y = (x + dx) % ring if ring else x + dx
            v = out.setdefault((y, f), [0, 0]); v[rail] += a
    return {k: tuple(v) for k, v in out.items()}

def run(T, mark=None, kind=None, ring=None):
    st = {(0, 0): (1, 0)}
    for t in range(T):
        if mark and mark[0] == t:
            new = {}
            for (x, f), (r, l) in st.items():
                if x == mark[1]:
                    if kind == "sign": new[(x, f)] = (-r, -l)
                    else: new[(x, f ^ 1)] = (r, l)
                else: new[(x, f)] = (r, l)
            st = new
        st = step(st, ring)
    return st

def paths(T, mark=None, kind=None, ring=None):
    """Independent: sum over direction words. Entering rail d (0=R,1=L); coin entry sign - iff L->L."""
    tot = {}
    for w in itertools.product((0, 1), repeat=T):
        x, rail, s, f = 0, 0, 1, 0
        for t, d in enumerate(w):
            if mark and mark[0] == t and x == mark[1]:
                if kind == "sign": s = -s
                else: f ^= 1
            if rail == 1 and d == 1: s = -s
            x += 1 - 2 * d
            if ring: x %= ring
            rail = d
        v = tot.setdefault((x, f), [0, 0]); v[rail] += s
    return {k: tuple(v) for k, v in tot.items() if v != [0, 0]}

def clean(st): return {k: v for k, v in st.items() if v != (0, 0)}
def sites(T, ring=None): return list(range(T % 2, ring, 2)) if ring else list(range(-T, T + 1, 2))
def mass(st, T, ring=None):
    m = {x: 0 for x in sites(T, ring)}
    for (x, f), (r, l) in st.items(): m[x] += r * r + l * l
    return m
def cells(st, T, ring=None):
    return {x: tuple(sum(v * v for v in st.get((x, f), (0, 0))) for f in (0, 1)) for x in sites(T, ring)}
def powr(n, q):
    if n == 0: return 0
    if q == 0: return 1
    if q.denominator == 1: return F(n) ** int(q)
    return Decimal(n) ** (Decimal(q.numerator) / Decimal(q.denominator))
def Z(vals, q): return sum(powr(n, q) for n in vals)
def sgn(v): return (v > 0) - (v < 0)
def majorizes(a, b):
    n = max(len(a), len(b)); A = sorted(a + [0] * (n - len(a)), reverse=True); B = sorted(b + [0] * (n - len(b)), reverse=True)
    ca = list(itertools.accumulate(A)); cb = list(itertools.accumulate(B))
    return ca[-1] == cb[-1] and ca != cb and all(x >= y for x, y in zip(ca, cb))

minsep = [None]
def sep(v):
    a = abs(v)
    if isinstance(v, Decimal) and (minsep[0] is None or a < minsep[0]): minsep[0] = a
    return v

# C1
p2 = mass(paths(2), 2); ok = [F(p2[x], 4) for x in (-2, 0, 2)] == [F(1, 4), F(1, 2), F(1, 4)]
z = sum(v * v for v in p2.values()); q2 = [F(p2[x] ** 2, z) for x in (-2, 0, 2)]
ok2 = q2 == [F(1, 6), F(2, 3), F(1, 6)]
rec("C1", 2, ok + ok2, 2 - ok - ok2, dict(born=[str(F(p2[x], 4)) for x in (-2, 0, 2)], q2=[str(v) for v in q2]))

# A1
exp = {(5, None): [1, 5, 4, 4, 17, 1], (5, (2, -2)): [1, 5, 0, 8, 17, 1],
       (7, None): [1, 17, 5, 9, 17, 41, 37, 1], (7, (5, 1)): [1, 17, 5, 25, 25, 17, 37, 1]}
p = f = 0; tabs = {}
for (T, mk), e in exp.items():
    st = run(T, mk, "sign"); tabs[(T, mk)] = mass(st, T)
    for c in (list(tabs[(T, mk)].values()) == e, clean(st) == paths(T, mk, "sign"), sum(tabs[(T, mk)].values()) == 2 ** T):
        p += c; f += not c
rec("A1", p + f, p, f)

# A2
p = f = 0
for T, mk, mons, ring in ((5, (2, -2), (3, 5), None), (7, (5, 1), (5, 7), None), (9, (7, 1), (5,), 8)):
    for kind in ("sign", "flag"):
        b = run(T, ring=ring); m = run(T, mk, kind, ring)
        for x in mons:
            d = abs(x - mk[1]); d = min(d, ring - d) if ring else d
            c = d > T - mk[0] and b.get((x, 0)) == m.get((x, 0)) and m.get((x, 1), (0, 0)) == (0, 0)
            p += c; f += not c
rec("A2", p + f, p, f)

# A3
b5, m5 = list(tabs[(5, None)].values()), list(tabs[(5, (2, -2))].values())
got = [F(289, Z(b5, F(2))), F(289, Z(m5, F(2))), F(1, Z(b5, F(2))), F(1, Z(m5, F(2)))]
c = got == [F(289, 348), F(289, 380), F(1, 348), F(1, 380)]
rec("A3", 1, int(c), int(not c), [str(g) for g in got])

def witness(bare, marked, big, q, reverse=False):
    Zb, Zm = Z(bare, q), Z(marked, q)
    w = (powr(big, q) - big) * (1 / Zb - 1 / Zm)
    return -w if reverse else w

def grid_pos(fn, name, lim0, extra=None):
    p = f = 0; fails = []
    for q in GRID:
        w = sep(fn(q)) if q != 1 else fn(q)
        c = (w == 0) if q == 1 else (w > 0 and (not isinstance(w, Decimal) or w > Decimal("1e-40")))
        p += c; f += not c
        if not c: fails.append(str(q))
    l0 = fn(F(0)); c = l0 == lim0; p += c; f += not c
    if not c: fails.append("q->0 gives %s" % l0)
    d = dict(fails=fails, lim0=str(l0), at64=float(fn(F(64))))
    if extra: d.update(extra)
    rec(name, p + f, p, f, d)

b7, m7 = list(tabs[(7, None)].values()), list(tabs[(7, (5, 1))].values())
grid_pos(lambda q: witness(b5, m5, 17, q), "A4", F(8, 15))
grid_pos(lambda q: witness(b7, m7, 37, q, True), "A5", F(0))
RES["predicates"]["A5"]["detail"]["one_minus_W7_at_64_lt_1e-3"] = bool(1 - witness(b7, m7, 37, F(64), True) < F(1, 1000))

# A6
p = f = 0; d = {}
f5 = list(mass(run(5, (2, -2), "flag"), 5).values()); f7 = list(mass(run(7, (5, 1), "flag"), 7).values())
rb = list(mass(run(9, ring=8), 9, 8).values()); rf = list(mass(run(9, (7, 1), "flag", 8), 9, 8).values())
for c in (f5 == [1, 5, 2, 6, 17, 1], f7 == [1, 17, 5, 17, 21, 29, 37, 1],
          all(2 * a == x + y for a, x, y in zip(f5, b5, m5)), all(2 * a == x + y for a, x, y in zip(f7, b7, m7)),
          rb == [0, 128, 256, 128], rf == [64, 96, 256, 96],
          clean(run(9, (7, 1), "flag", 8)) == paths(9, (7, 1), "flag", 8)):
    p += c; f += not c
def R(q): return powr(256, q) / Z(rb, q) - powr(256, q) / Z(rf, q)
c = R(F(0)) == F(1, 12); p += c; f += not c
bad = [str(q) for q in GRID if q != 1 and sgn(sep(R(q))) != (1 if q < 1 else -1)]
p += len(GRID) - 1 - len(bad); f += len(bad)
rec("A6", p + f, p, f, dict(f5=f5, f7=f7, ring_bare=rb, ring_flag=rf, R0=str(R(F(0))), R_sign_fail=bad))
# A7
grid_pos(lambda q: witness(b5, f5, 17, q), "A7_five_blank", F(0))
grid_pos(lambda q: witness(b7, f7, 37, q, True), "A7_seven_blank", F(0))
# A8
fair5 = F(sum(1 for w in itertools.product((0, 1), repeat=5) if sum(1 - 2 * d for d in w) == -1), 32)
fair9 = F(sum(1 for w in itertools.product((0, 1), repeat=9) if sum(1 - 2 * d for d in w) % 8 == 1), 512)
cs = [fair5 == F(10, 32), fair9 == F(136, 512), m5[2] == 0, rb[0] == 0, F(f5[2], 32) == F(2, 32), comb(9, 1) + comb(9, 5) + comb(9, 9) == 136]
rec("A8", len(cs), sum(cs), len(cs) - sum(cs), dict(fair5=str(fair5), fair9=str(fair9)))
# A9
t2 = mass(run(2), 2); t3 = mass(run(3), 3)
e = F(t2[-2] ** 2, sum(v * v for v in t2.values())); l = F(t3[-3] ** 2 + t3[-1] ** 2, sum(v * v for v in t3.values()))
rec("A9", 1, int(e - l == F(2, 21)), int(e - l != F(2, 21)), dict(early=str(e), reach=str(l), deficit=str(e - l)))

# B1
c5 = cells(run(5, (2, -2), "flag"), 5); c7 = cells(run(7, (5, 1), "flag"), 7); c9 = cells(run(9, (7, 1), "flag", 8), 9, 8)
comb5 = [a + b for a, b in c5.values()]; res5 = [v for ab in c5.values() for v in ab if v]
cs = [list(c5.values()) == [(0, 1), (0, 5), (1, 1), (5, 1), (17, 0), (1, 0)], Z(b5, F(2)) == 348, Z(comb5, F(2)) == 356, Z(res5, F(2)) == 344,
      F(89, 261) * F(1, 356) + F(172, 261) * F(1, 344) == F(1, 348)]
rec("B1", len(cs), sum(cs), len(cs) - sum(cs), dict(cells=list(c5.values())))
# B2
def partitions(cl):
    idx = [x for x, (a, b) in cl.items() if a and b]
    for cuts in itertools.product((0, 1), repeat=len(idx)):
        out = []
        for x, (a, b) in cl.items():
            if x in idx and cuts[idx.index(x)]: out += [a, b]
            elif a + b: out.append(a + b)
        yield cuts, out
cs = [[c7[x][0] for x in c7] == [1, 17, 5, 13, 13, 25, 37, 1], [c7[x][1] for x in c7] == [0, 0, 0, 4, 8, 4, 0, 0],
      [c9[x][0] for x in c9] == [32, 80, 256, 80], [c9[x][1] for x in c9] == [32, 16, 0, 16]]
P7 = list(partitions(c7)); P9 = list(partitions(c9))
cs += [len(P7) == 8, len(P9) == 8] + [majorizes(b7, c) for _, c in P7] + [majorizes(rb, c) for _, c in P9]
cs += [max(c) == 37 and c.count(37) == 1 for _, c in P7] + [sum(1 for v in c if v) >= 4 for _, c in P9]
rec("B2", len(cs), sum(cs), len(cs) - sum(cs))
# B3
p = f = 0; fails = []
for cuts, c in P7:
    for q in GRID:
        if q == 1: continue
        w = sep(witness(b7, c, 37, q, True)); ok = w > 0; p += ok; f += not ok
        if not ok: fails.append(("L", cuts, str(q)))
for cuts, c in P9:
    for q in GRID:
        if q == 1: continue
        j = sep(powr(256, q) / Z(rb, q) - powr(256, q) / Z(c, q)); ok = sgn(j) == (1 if q < 1 else -1); p += ok; f += not ok
        if not ok: fails.append(("J", cuts, str(q)))
    j0 = F(1, 3) - F(1, sum(1 for v in c if v)); ok = j0 >= F(1, 12); p += ok; f += not ok
rec("B3", p + f, p, f, dict(fails=fails))
# B4 rail refinements
def railcells(st): return [v * v for (x, fl), rl in sorted(st.items()) for v in rl if v]
br7 = railcells(run(7)); mr7 = railcells(run(7, (5, 1), "flag"))
d = dict(bare_site_majorizes_marked_rail=majorizes(b7, mr7), bare_rail_majorizes_marked_rail=majorizes(br7, mr7),
         bare_rail=sorted(br7, reverse=True), marked_rail=sorted(mr7, reverse=True))
sg = {str(q): sgn(Z(br7, q) - Z(mr7, q)) * (1 if q > 1 else -1) for q in GRID if q != 1}
d["both_rail_resolved_sign_ok_count"] = sum(1 for v in sg.values() if v == 1); d["both_rail_resolved_sign_bad"] = [k for k, v in sg.items() if v != 1]
br5 = railcells(run(5)); mr5 = railcells(run(5, (2, -2), "sign")); d["five_sign_rail_Z2"] = [int(Z(br5, F(2))), int(Z(mr5, F(2)))]
d["five_sign_rail_cells"] = [sorted(br5), sorted(mr5)]
rec("B4", 2, int(d["bare_site_majorizes_marked_rail"]) + int(not d["both_rail_resolved_sign_bad"]), 2 - int(d["bare_site_majorizes_marked_rail"]) - int(not d["both_rail_resolved_sign_bad"]), d)

# U1
tot = qual = p = f = 0; fails = []; nonq = 0
for T in range(3, 10):
    bst = run(T); bm = mass(bst, T); bl = list(bm.values())
    for t0 in range(1, T):
        occ = sorted({x for (x, _) in clean(run(t0))})
        for x0 in occ:
            for kind in ("sign", "flag"):
                tot += 1
                mst = run(T, (t0, x0), kind); mm = mass(mst, T); ml = list(mm.values())
                remote = [x for x in bm if abs(x - x0) > T - t0 and bm[x] > 0 and bm[x] == mm[x]]
                if ml == bl or len(remote) < 2: nonq += 1; continue
                qual += 1
                bad = [str(q) for q in GRID if q != 1 and sgn(sep(Z(bl, q) - Z(ml, q))) != sgn(q - 1)]
                if bad: f += 1; fails.append(dict(T=T, t0=t0, x0=x0, kind=kind, bare=bl, marked=ml, bad_q=bad, majorized=majorizes(bl, ml)))
                else: p += 1
rec("U1", qual, p, f, dict(instances=tot, not_qualifying=nonq, fails=fails))

# R1
def f2(tab, T): return {x: F(n, 2 ** T) ** 2 for x, n in tab.items()}
ub, um = f2(tabs[(5, None)], 5), f2(tabs[(5, (2, -2))], 5)
c = ub[3] == um[3] and ub[5] == um[5]
rec("R1", 1, int(c), int(not c), dict(rate3=str(ub[3]), rate5=str(ub[5]), total_bare=str(sum(ub.values())), total_marked=str(sum(um.values())),
    note="rival passes remote test at f(p)=p^2; totals differ from 1 and from each other"))
# R2
def amp(st): return {k: v for k, v in clean(st).items()}
sb, sm = amp(run(5)), amp(run(5, (2, -2), "sign"))
plus_b = {x: sum(v) ** 2 for (x, _), v in sb.items()}; plus_m = {x: sum(v) ** 2 for (x, _), v in sm.items()}
d = dict(rail_Z2=[int(Z(br5, F(2))), int(Z(mr5, F(2)))], rail_Z3=[int(Z(br5, F(3))), int(Z(mr5, F(3)))],
         plus_q1=[plus_b, plus_m], plus_Z1=[sum(plus_b.values()), sum(plus_m.values())],
         plus_Z2=[sum(v * v for v in plus_b.values()), sum(v * v for v in plus_m.values())])
d["rail_power_q2_signals"] = d["rail_Z2"][0] != d["rail_Z2"][1]; d["plus_q1_normalised_signals"] = d["plus_Z1"][0] != d["plus_Z1"][1]
rec("R2", 2, int(d["rail_power_q2_signals"]) + int(d["plus_q1_normalised_signals"]), 2 - int(d["rail_power_q2_signals"]) - int(d["plus_q1_normalised_signals"]), d)
# R3
QS = [F(n) for n in range(1, 9)]
def pt(tab, q): z = Z(tab, q); return (powr(17, q) / z, 1 / z)
found = None
for qa, qb in itertools.combinations(QS, 2):
    A, B = pt(b5, qa), pt(b5, qb)
    for qc, qd in itertools.combinations(QS, 2):
        C, Dd = pt(m5, qc), pt(m5, qd)
        # s*A+(1-s)*B = u*C+(1-u)*D  -> 2 eq, 2 unknowns
        a11, a12, r1 = A[0] - B[0], -(C[0] - Dd[0]), Dd[0] - B[0]
        a21, a22, r2 = A[1] - B[1], -(C[1] - Dd[1]), Dd[1] - B[1]
        det = a11 * a22 - a12 * a21
        if det == 0: continue
        s = (r1 * a22 - a12 * r2) / det; u = (a11 * r2 - r1 * a21) / det
        if 0 < s < 1 and 0 < u < 1 and not (qa == qc and qb == qd and s == u):
            found = dict(bare={str(qa): str(s), str(qb): str(1 - s)}, marked={str(qc): str(u), str(qd): str(1 - u)},
                         rate3=str(s * A[0] + (1 - s) * B[0]), rate5=str(s * A[1] + (1 - s) * B[1]),
                         check=(s * A[0] + (1 - s) * B[0] == u * C[0] + (1 - u) * Dd[0] and s * A[1] + (1 - s) * B[1] == u * C[1] + (1 - u) * Dd[1]))
            break
    if found: break
rec("R3", 1, int(bool(found)), int(not found), found)
# R4 / R5
def siteexp(tab, qmap, qdef):
    w = {x: powr(n, qmap.get(x, qdef)) for x, n in tab.items()}; z = sum(w.values()); return {x: F(v) / z for x, v in w.items()}
def block(tab, T, blocks, q):
    out = {}
    for bl in blocks:
        xs = [x for x in bl if x in tab]; M = sum(tab[x] for x in xs); zz = sum(powr(tab[x], q) for x in xs)
        for x in xs: out[x] = F(M, 2 ** T) * (F(powr(tab[x], q)) / zz if zz else 0)
    return out
tests = [(5, (2, -2), "sign", (3, 5)), (5, (2, -2), "flag", (3, 5)), (7, (5, 1), "sign", (5, 7)), (7, (5, 1), "flag", (5, 7))]
qm = {-1: F(1), 1: F(1), 3: F(1)}; BL = [(-9, -7, -5, -3), (-1, 1), (3,), (5, 7, 9)]
for name, law in (("R4", lambda tab, T: siteexp(tab, qm, F(2))), ("R5", lambda tab, T: block(tab, T, BL, F(2)))):
    p = f = 0; d = {}
    for T, mk, kind, mons in tests:
        bt = mass(run(T), T); mt = mass(run(T, mk, kind), T); lb, lm = law(bt, T), law(mt, T)
        ok = all(lb[x] == lm[x] for x in mons); p += ok; f += not ok
        d["%d_%s" % (T, kind)] = dict(remote=[str(lb[x]) for x in mons], born=[str(F(bt[x], 2 ** T)) for x in mons], total=[str(sum(lb.values())), str(sum(lm.values()))], equal=ok)
    rec(name, 4, p, f, d)
# R6
Zb2, Zm2 = Z(b5, F(2)), Z(m5, F(2)); ratio = F(Zb2, Zm2)   # eta_b/eta_m
ok = ratio * F(289, Zb2) == F(289, Zm2) and ratio * F(1, Zb2) == F(1, Zm2)
bornfail = ratio * F(17, 32) != F(17, 32)
rec("R6", 2, int(ok) + int(bornfail), 2 - int(ok) - int(bornfail), dict(eta_b_over_eta_m=str(ratio), q2_passes_with_it=ok, q1_fails_with_it=bornfail))
# R7
p = f = 0
for q in GRID:
    for q_ in GRID:
        if q == q_ == 1: continue
        if q.denominator != 1 or q_.denominator != 1:
            dc = lambda v: v if isinstance(v, Decimal) else Decimal(v.numerator) / Decimal(v.denominator) if isinstance(v, F) else Decimal(v)
            d3 = sep(dc(powr(17, q)) / dc(Z(b5, q)) - dc(powr(17, q_)) / dc(Z(m5, q_))); d5 = sep(1 / dc(Z(b5, q)) - 1 / dc(Z(m5, q_)))
            ok = not (abs(d3) < Decimal("1e-40") and abs(d5) < Decimal("1e-40"))
        else:
            ok = not (powr(17, q) / Z(b5, q) == powr(17, q_) / Z(m5, q_) and 1 / Z(b5, q) == 1 / Z(m5, q_))
        p += ok; f += not ok
rec("R7", p + f, p, f)
RES["data"]["min_decimal_separation_seen"] = str(minsep[0])
tf = sum(v["failed"] for v in RES["predicates"].values())
RES["total_failed_predicates"] = tf
with open(sys.argv[1], "x", encoding="utf8", newline="\n") as h:
    json.dump(RES, h, indent=1, default=str); h.write("\n")
for k, v in RES["predicates"].items(): print(k, v["qualifying"], v["passed"], v["failed"])
print("min sep", minsep[0])
sys.exit(1 if tf else 0)
