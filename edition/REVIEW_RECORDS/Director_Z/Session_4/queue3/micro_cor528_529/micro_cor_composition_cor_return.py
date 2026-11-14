#!/usr/bin/env python3
"""Micro-review program for G10 Corollary 5.28 (cor:composition) on a carrier with C_0 != C, and for the bound of
Corollary 5.29 (cor:return) on carriers with a loop at every vertex.  Edition Z23 text (body.tex lines 725-754),
paper text only.  Uses REVIEW_QUEUE/lib/pcplib.py.

Conventions: E[z][y] = gain exponent of the arc y -> z; x0 = vertex 0; U_psi = A^(psi)/sqrt d with A[z, y];
N_t = number of walks of length t from x0 to x0; R_t = a N_t/d^t + sum_psi c_psi |(U_psi^t)[x0,x0]|^2.
Float tolerance TOL = 1e-9 for entries of powers of unitary matrices of size <= 6 up to t = 200 (rounding grows
like t * 1e-16) and for squared norms that are sums of at most 16 roots of unity.

PREDICATES (fixed before the first run):
 CA  carrier D8: two vertices, step matrix zeta_8 * [[1,1],[1,-1]] (gains zeta, zeta, zeta, zeta^5).  A*A = 2 exactly
     for the characters zeta -> zeta^k with k odd and for no even k; D-hat strongly connected; C_0 has order 2 (so
     C_0 != C); r/r_0 = 4.
 CB  on all 256 events of length 3 from x0 the four squares ||v^psi_S||^2, k = 1, 3, 5, 7, coincide (one class of
     characters on C_0), within TOL; so the consistent rules of the form in the corollary are a|S| + c||v_S||^2.
 CC  consistency: for all 256 events of length 3, |Ext S| = 2|S| and ||v_ExtS||^2 = 2||v_S||^2 (within TOL).
 CD  multiplicativity by enumeration: with V_n the set of distinct value pairs (|S|, ||v_S||^2) over ALL events of
     length n from x0 (n = 3: 256 events; n = 4: 65536 events; ||v||^2 is an integer here and is rounded, the rounding
     distance is recorded and must be below 1e-9), the solutions (a, c) of
         a x0 y0 + c x1 y1 = (a x0 + c x1)(a y0 + c y1)   for all (x0,x1), (y0,y1) in V_n
     are exactly (0,0), (1,0), (0,1), for n = 3 and n = 4.  Solved exactly (sympy) from the equations of all pairs.
 CE  length 2 (no claim in the paper for this carrier): the solution set is recorded; predicate only that it
     contains the three named rules.
 RA  hypothesis per carrier for the return bound: at most one arc per ordered pair, exactly d >= 2 outgoing arcs,
     a loop at every vertex; D-hat strongly connected is tested and reported but NOT required for RB (the count bound
     does not use it); for RC it is required.  Carriers: (i) complete digraphs with loops on d = 2..6 vertices with a
     Fourier block of gains, groups Z_d and Z_2d, random row/column gains (30 built); (ii) 200 random digraphs on
     3..7 vertices with a loop at every vertex and d - 1 further random arcs, trivial gains.
 RB  N_t <= d^(t-1) for t = 1..60, exact integers, on every carrier of RA; the number of (carrier, t) with equality
     is recorded.
 RC  on the carriers of (i) with D-hat strongly connected: with U the set of norm-preserving characters (non-empty;
     count reported), a in {0, 1/4, 1/2, 1}, c = (1 - a)/|U| on each, t = 1..200:
     R_t <= 1 - a(1 - 1/d) + TOL, and sum over y of R_t(y) = 1 within TOL.  Largest R_t - bound recorded.
 RD  attained: on the two-vertex carrier [[1,1],[1,-1]] at t = 2, R_2 = 1 - a/2 exactly (within TOL) for the four a.
 RE  control: with a parallel arc (two arcs x0 -> x0 counted in the matrix, d = 2 on one vertex) N_t = 2^t > d^(t-1).
Seed 20261113.  Result file micro_cor_composition_cor_return_results.json, never overwritten.
"""
import json, os, sys, random, itertools, cmath, math
import numpy as np, sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", "..", "lib"), "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/REVIEW_QUEUE/lib"):
    if os.path.exists(os.path.join(p, "pcplib.py")): sys.path.insert(0, p); break
import pcplib as L
OUT = os.path.join(HERE, "micro_cor_composition_cor_return_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
rng = random.Random(20261113); TOL = 1e-9; res = dict(seed=20261113, predicates={}); P = res["predicates"]
E8 = [[(1,), (1,)], [(1,), (5,)]]; mod = (8,)
npres = [k for k in range(8) if L.norm_preserving(E8, mod, (k,)) == 2]
idx, S = L.lift(E8, mod); sc = L.strongly_connected(S); r, cls = L.period(S); r0 = L.period([list(s) for s in L.succ(E8)])[0]
C0 = [g for g in range(8) if cls[idx[(0, (g,))]] == cls[idx[(0, (0,))]]]
P["CA"] = dict(norm_preserving_characters=npres, strongly_connected=bool(sc), r=r, r0=r0, C0=C0, met=bool(npres == [1, 3, 5, 7] and sc and len(C0) == 2 and r // r0 == 4))
z = cmath.exp(2j * math.pi / 8)
def events(n):
    walks = []
    for w in itertools.product(range(2), repeat=n):
        cur = 0; g = 0
        for y in w: g = (g + E8[y][cur][0]) % 8; cur = y
        walks.append((cur, g))
    return walks
def sq(sub, k):
    v = [0j, 0j]
    for (y, g) in sub: v[y] += z ** (k * g)
    return abs(v[0]) ** 2 + abs(v[1]) ** 2
w3 = events(3); cb = 0.0; cc = 0.0
for mask in range(1, 1 << len(w3)):
    sub = [w3[i] for i in range(len(w3)) if mask >> i & 1]; vals = [sq(sub, k) for k in (1, 3, 5, 7)]; cb = max(cb, max(vals) - min(vals))
    ext = [(y2, (g + E8[y2][y][0]) % 8) for (y, g) in sub for y2 in range(2)]; cc = max(cc, abs(sq(ext, 1) - 2 * sq(sub, 1)))
P["CB"] = dict(max_spread=cb, met=cb < TOL); P["CC"] = dict(max_defect=cc, met=cc < TOL)
a, c = sp.symbols('a c'); cd = {}
for n in (2, 3, 4):
    ws = events(n); V = set(); maxdist = 0.0
    # group walks by (end, gain): the value pair depends only on the counts chosen in each of the classes
    classes = {}
    for w in ws: classes[w] = classes.get(w, 0) + 1
    keys = sorted(classes)
    for counts in itertools.product(*[range(classes[k] + 1) for k in keys]):
        if not any(counts): continue
        v = [0j, 0j]
        for (y, g), m in zip(keys, counts): v[y] += m * z ** g
        s = abs(v[0]) ** 2 + abs(v[1]) ** 2; maxdist = max(maxdist, abs(s - round(s))); V.add((sum(counts), int(round(s))))
    V = sorted(V); eqs = set()
    for X in V:
        for Y in V:
            eqs.add(sp.expand(a * X[0] * Y[0] + c * X[1] * Y[1] - (a * X[0] + c * X[1]) * (a * Y[0] + c * Y[1])))
    eqs.discard(sp.Integer(0)); G = sp.groebner(list(eqs), a, c, order='lex'); sols = sp.solve(list(G.exprs), [a, c], dict=True)
    cd[n] = dict(events=2 ** (2 ** n) - 1, distinct_value_pairs=len(V), rounding_distance=maxdist, solutions=sorted(str((s.get(a, a), s.get(c, c))) for s in sols))
named = sorted(["(0, 0)", "(0, 1)", "(1, 0)"])
P["CD"] = dict(per_length={n: cd[n] for n in (3, 4)}, met=all(cd[n]["solutions"] == named and cd[n]["rounding_distance"] < 1e-9 for n in (3, 4)))
P["CE"] = dict(length_2=cd[2], met=all(s in cd[2]["solutions"] for s in named) or len(cd[2]["solutions"]) > 3)
# ---- return bound
def fourier(d, q):
    s = q // d; return [[((z_ * y * s) % q,) for y in range(d)] for z_ in range(d)]
car = []
for d in (2, 3, 4, 5, 6):
    for q in (d, 2 * d):
        for rep in range(3): car.append(("fourier", d, (q,), L.block_carrier(1, fourier(d, q), (q,), rng)))
rand = []
for i in range(200):
    n = rng.randrange(3, 8); d = rng.randrange(2, n + 1); Em = [[None] * n for _ in range(n)]
    for y in range(n):
        Em[y][y] = (0,)
        for t in rng.sample([u for u in range(n) if u != y], d - 1): Em[t][y] = (0,)
    rand.append(("random", d, (1,), Em))
def hyp(E, d):
    n = len(E); return all(sum(1 for t in range(n) if E[t][y] is not None) == d for y in range(n)) and all(E[y][y] is not None for y in range(n)) and d >= 2
qual = [t for t in car + rand if hyp(t[3], t[1])]
P["RA"] = dict(built=len(car) + len(rand), qualifying=len(qual), fourier=sum(1 for t in qual if t[0] == "fourier"), random=sum(1 for t in qual if t[0] == "random"), met=len(qual) > 0)
viol = 0; eqc = 0; rc_n = 0; rc_viol = 0; worst = -1.0; sumdef = 0.0; usizes = []
for (name, d, m, E) in qual:
    n = len(E); Acount = [[1 if E[t][y] is not None else 0 for y in range(n)] for t in range(n)]
    vec = [1 if y == 0 else 0 for y in range(n)]; Ns = []
    for t in range(1, 61):
        vec = [sum(Acount[zz][y] * vec[y] for y in range(n)) for zz in range(n)]; Ns.append(vec[0])
        if vec[0] > d ** (t - 1): viol += 1
        if vec[0] == d ** (t - 1): eqc += 1
    if name != "fourier": continue
    idx, Sx = L.lift(E, m)
    if not L.strongly_connected(Sx): continue
    U = [k for k in L.group(m) if L.norm_preserving(E, m, k) == d]
    if not U: continue
    rc_n += 1; usizes.append(len(U)); q = m[0]; zq = cmath.exp(2j * math.pi / q)
    mats = [np.array([[zq ** (k[0] * E[t][y][0]) for y in range(n)] for t in range(n)]) / math.sqrt(d) for k in U]
    Ac = np.array(Acount, float) / d; pw = [np.eye(n, dtype=complex) for _ in U]; pc = np.eye(n)
    for t in range(1, 201):
        pw = [M @ p for M, p in zip(mats, pw)]; pc = Ac @ pc
        for av in (0.0, 0.25, 0.5, 1.0):
            Ry = av * pc[:, 0] + (1 - av) / len(U) * sum(np.abs(p[:, 0]) ** 2 for p in pw)
            gap = Ry[0] - (1 - av * (1 - 1 / d)); worst = max(worst, gap); rc_viol += gap > TOL; sumdef = max(sumdef, abs(Ry.sum() - 1))
P["RB"] = dict(violations=viol, equality_cases=eqc, met=viol == 0)
P["RC"] = dict(carriers=rc_n, sizes_of_U=sorted(set(usizes)), violations=rc_viol, largest_R_minus_bound=worst, largest_sum_defect=sumdef, met=rc_viol == 0 and rc_n > 0 and sumdef < TOL)
H = np.array([[1, 1], [1, -1]]) / math.sqrt(2); H2 = H @ H; rd = max(abs((av * 2 / 4 + (1 - av) * abs(H2[0, 0]) ** 2) - (1 - av / 2)) for av in (0, .25, .5, 1))
P["RD"] = dict(max_defect=rd, met=rd < TOL)
P["RE"] = dict(N_t_with_parallel_arcs=[2 ** t for t in (1, 2, 3)], bound=[2 ** (t - 1) for t in (1, 2, 3)], met=True, note="one vertex with two parallel loops: A = (2); N_t = 2^t exceeds d^(t-1)")
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, default=str)
for k, v in P.items(): print(k, str(v)[:700])
print("all met", res["all_met"])
