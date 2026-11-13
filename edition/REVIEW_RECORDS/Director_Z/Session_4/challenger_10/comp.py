"""Challenger program for Corollary cor:composition (written from the paper text only).

PREDICATES, fixed before the first run.  Exact arithmetic: gains are exponents in Z_q,
character values are Gaussian integers (q in {2,4}), coefficients are Fractions.

Carriers: T2 = two vertices, step [[1,1],[1,-1]] over C_2; B4 = two vertices, step [[1,i],[1,-i]]
over C_4; R4 = signed arc digraph of the ring N=4 over C_2 (vertices (x,R),(x,L); arcs to
(x+1,R) and (x-1,L); gain -1 on (x,L)->(x-1,L)).  x_0 = vertex 0.  Test length n = 3 (256 events,
65536 ordered pairs), also n = 2.

H  (hypothesis, per carrier): at most one arc per ordered pair; constant out-degree d>=2; derived
   digraph strongly connected; U(D) non-empty.  Report r, r_0, C_0, U(D), classes of U(D)|C_0.
   A carrier failing H is reported and not used.
P1 for every ordered pair (S1,S2) of events of length n from x_0, with the product event enumerated
   as pairs of walks: |S1xS2| = |S1||S2|; for every character psi of C and every (y1,y2),
   sigma_psi(multiset at (y1,y2)) = sigma_psi(m_S1(y1)) * sigma_psi(m_S2(y2)); and
   ||v^psi_{S1xS2}||^2 = ||v^psi_S1||^2 ||v^psi_S2||^2.
P2 for every pair, the multiset at each (y1,y2) is supported on one coset of C_0, and
   ||v^psi_{S1xS2}||^2 is the same for all psi in U(D) with the same restriction to C_0 up to inverse.
P3 for (a,c) in {(1,0),(0,1),(1,1),(1/2,1/2),(2,0),(0,2),(1,-1),(0,0)} with c on the first class:
   mu(S1xS2) = mu(S1)mu(S2) for all pairs  <=>  (a,c) in {(1,0),(0,1),(0,0)}.  A violating pair is
   recorded for each other choice.  mu on the product is computed from the product multisets.
P4 (measured, then predicate) rank of the vectors (f_i(S))_i over all events of length n equals k+1;
   measured only: the rank over events with all walks at one end vertex and at most two walks.
P5 on carriers with k>=2 classes: e=(0,1,1), (0,1/2,1/2), (1,0,1) fail and e=(0,0,1) holds.
P6 (sample) P1 for pairs of events of different lengths (2 and 3) and different starting vertices.
P7 the three single rules are consistent with factor d at lengths 2->3 (mu(Ext S) = d mu(S)), all events
   of length 2; (1,1) too (it is consistent but not multiplicative).
Result file results.json is not overwritten.
"""
import itertools, json, os, sys
from fractions import Fraction as Fr
from collections import Counter
from math import gcd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)

def gmul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def gadd(a, b): return (a[0]+b[0], a[1]+b[1])
def gabs2(a): return a[0]*a[0]+a[1]*a[1]
def omega(q, e):
    e %= q
    if q == 2: return [(1, 0), (-1, 0)][e]
    return [(1, 0), (0, 1), (-1, 0), (0, -1)][e]

def carrier_T2(): return dict(name="T2", q=2, V=2, arcs={(0,0):0,(0,1):0,(1,0):0,(1,1):1})  # (src,dst):gain
def carrier_B4(): return dict(name="B4", q=4, V=2, arcs={(0,0):0,(1,0):1,(0,1):0,(1,1):3})
def carrier_R4():
    N = 4; arcs = {}
    idx = lambda x, s: 2*(x % N)+s  # s=0 R, s=1 L
    for x in range(N):
        for s in (0, 1):
            arcs[(idx(x, s), idx(x+1, 0))] = 0
            arcs[(idx(x, s), idx(x-1, 1))] = 1 if s == 1 else 0
    return dict(name="R4", q=2, V=2*N, arcs=arcs)
# B4 step matrix [[1,i],[1,-i]]: A_{yx}; column x=0 -> entries 1,1; column x=1 -> i,-i
def fixB4(c):
    c["arcs"] = {(0,0):0,(0,1):0,(1,0):1,(1,1):3}; return c

def analyse(c):
    q, V, arcs = c["q"], c["V"], c["arcs"]
    out = {x: [(y, g) for (s, y), g in arcs.items() if s == x] for x in range(V)}
    degs = {len(out[x]) for x in range(V)}
    d = len(out[0])
    # derived digraph
    nodes = [(x, g) for x in range(V) for g in range(q)]
    succ = {u: [(y, (u[1]+g) % q) for (y, g) in out[u[0]]] for u in nodes}
    def reach(start, sc):
        seen = {start}; st = [start]
        while st:
            u = st.pop()
            for v in sc[u]:
                if v not in seen: seen.add(v); st.append(v)
        return seen
    pred = {u: [] for u in nodes}
    for u in nodes:
        for v in succ[u]: pred[v].append(u)
    strong = len(reach((0, 0), succ)) == len(nodes) and len(reach((0, 0), pred)) == len(nodes)
    # period via BFS levels
    def period(start, sc, nd):
        lev = {start: 0}; st = [start]; r = 0
        while st:
            u = st.pop(0)
            for v in sc[u]:
                if v not in lev: lev[v] = lev[u]+1; st.append(v)
                else: r = gcd(r, lev[u]+1-lev[v])
        return r, lev
    r, lev = period((0, 0), succ, nodes)
    r0, _ = period(0, {x: [y for y, _ in out[x]] for x in range(V)}, range(V))
    C0 = sorted(g for g in range(q) if lev[(0, g)] % r == 0)
    U = []
    for j in range(q):
        ok = True
        for x in range(V):
            for x1 in range(V):
                s = (0, 0)
                for (y, g) in out[x]:
                    for (y1, g1) in out[x1]:
                        if y == y1: s = gadd(s, omega(q, j*(g1-g)))
                want = (d, 0) if x == x1 else (0, 0)
                if s != want: ok = False
        if ok: U.append(j)
    # classes of U|C0 up to inverse
    key = lambda j: tuple(sorted([tuple(omega(q, j*g) for g in C0), tuple(omega(q, -j*g) for g in C0)]))
    classes = {}
    for j in U: classes.setdefault(key(j), []).append(j)
    classes = sorted(classes.values())
    H = (degs == {d}) and d >= 2 and strong and len(U) > 0
    return dict(d=d, r=r, r0=r0, C0=C0, U=U, classes=classes, strong=strong, H=H, out=out, lev=lev)

def walks(out, x0, n):
    ws = [((), x0, 0)]
    for _ in range(n):
        ws = [(w+(y,), y, g+h) for (w, x, g) in ws for (y, h) in out[x]]
    return ws  # (vertex sequence, end, gain exponent (not reduced))

def events(ws):
    for bits in range(1 << len(ws)):
        yield bits, [ws[i] for i in range(len(ws)) if bits >> i & 1]

def family(S, q):
    f = {}
    for (_, y, g) in S: f.setdefault(y, Counter())[g % q] += 1
    return f
def sigma(m, q, j):
    s = (0, 0)
    for g, cnt in m.items():
        o = omega(q, j*g); s = gadd(s, (o[0]*cnt, o[1]*cnt))
    return s
def norm2(f, q, j): return sum(gabs2(sigma(m, q, j)) for m in f.values())
def prodfamily(S1, S2, q):
    f = {}
    for (_, y1, g1) in S1:
        for (_, y2, g2) in S2:
            f.setdefault((y1, y2), Counter())[(g1+g2) % q] += 1
    return f

def rank(rows):
    rows = [list(map(Fr, r)) for r in rows]; rk = 0
    ncol = len(rows[0]) if rows else 0
    for col in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][col] != 0), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][col] != 0:
                fct = rows[i][col]/rows[rk][col]
                rows[i] = [a-fct*b for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk

RULES = [(1,0),(0,1),(1,1),(Fr(1,2),Fr(1,2)),(2,0),(0,2),(1,-1),(0,0)]
EXPECT_MULT = {(1,0),(0,1),(0,0)}
res = {"note": "predicates in docstring of comp.py", "carriers": {}}
tot = Counter()

for c in (carrier_T2(), fixB4(carrier_B4()), carrier_R4()):
    A = analyse(c); q = c["q"]; name = c["name"]
    R = dict(d=A["d"], r=A["r"], r0=A["r0"], C0=A["C0"], U=A["U"], classes=A["classes"],
             strongly_connected=A["strong"], H=A["H"])
    res["carriers"][name] = R
    tot["H_met" if A["H"] else "H_failed"] += 1
    if not A["H"]: continue
    reps = [cl[0] for cl in A["classes"]]; k = len(reps)
    C0set = set(A["C0"])
    for n in (2, 3):
        ws = walks(A["out"], 0, n)
        evs = [(b, S, family(S, q)) for b, S in events(ws)]
        fvec = {b: [len(S)]+[norm2(f, q, j) for j in reps] for b, S, f in evs}
        nallpsi = {b: [norm2(f, q, j) for j in range(q)] for b, S, f in evs}
        p1 = p2 = 0; p1f = []; p2f = []
        viol = {str(rc): None for rc in RULES}
        e_extra = {"(0,1,1)": [0,1,1], "(0,1/2,1/2)": [0,Fr(1,2),Fr(1,2)], "(1,0,1)": [1,0,1], "(0,0,1)": [0,0,1]} if k >= 2 else {}
        viol5 = {kk: None for kk in e_extra}
        for b1, S1, f1 in evs:
            for b2, S2, f2 in evs:
                pf = prodfamily(S1, S2, q)
                ok = sum(sum(m.values()) for m in pf.values()) == len(S1)*len(S2)
                pn = [norm2(pf, q, j) for j in range(q)]
                for j in range(q):
                    if pn[j] != nallpsi[b1][j]*nallpsi[b2][j]: ok = False
                    for (y1, y2), m in pf.items():
                        if sigma(m, q, j) != gmul(sigma(f1[y1], q, j), sigma(f2[y2], q, j)): ok = False
                    # zero components where one factor has no walk are absent on both sides
                if ok: p1 += 1
                elif len(p1f) < 3: p1f.append([b1, b2])
                ok2 = True
                for m in pf.values():
                    gs = list(m)
                    if any(((g-gs[0]) % q) not in C0set for g in gs): ok2 = False
                for cl in A["classes"]:
                    if len({pn[j] for j in cl}) != 1: ok2 = False
                if ok2: p2 += 1
                elif len(p2f) < 3: p2f.append([b1, b2])
                # rules, mu on product from product multisets
                pv = [sum(sum(m.values()) for m in pf.values())]+[pn[j] for j in reps]
                for (a, cc) in RULES:
                    if viol[str((a, cc))] is None:
                        mu = lambda v: a*v[0]+cc*v[1]
                        if mu(pv) != mu(fvec[b1])*mu(fvec[b2]):
                            viol[str((a, cc))] = dict(S1=[list(w[0]) for w in S1], S2=[list(w[0]) for w in S2],
                                                     mu_prod=str(mu(pv)), mu1=str(mu(fvec[b1])), mu2=str(mu(fvec[b2])))
                for kk, e in e_extra.items():
                    if viol5[kk] is None:
                        mu = lambda v: sum(ei*vi for ei, vi in zip(e, v))
                        if mu(pv) != mu(fvec[b1])*mu(fvec[b2]):
                            viol5[kk] = dict(S1=[list(w[0]) for w in S1], S2=[list(w[0]) for w in S2],
                                             mu_prod=str(mu(pv)), mu1=str(mu(fvec[b1])), mu2=str(mu(fvec[b2])))
        npairs = len(evs)**2
        p3 = {}
        for rc in RULES:
            mult = viol[str(rc)] is None
            met = mult == (rc in EXPECT_MULT)
            p3[str(rc)] = dict(multiplicative_all_pairs=mult, predicate_met=met, violating_pair=viol[str(rc)])
            tot["P3_met" if met else "P3_failed"] += 1
        p5 = {}
        for kk in e_extra:
            mult = viol5[kk] is None; met = mult == (kk == "(0,0,1)")
            p5[kk] = dict(multiplicative_all_pairs=mult, predicate_met=met, violating_pair=viol5[kk])
            tot["P5_met" if met else "P5_failed"] += 1
        rk_all = rank(list({tuple(v) for v in fvec.values()}))
        one = [fvec[b] for b, S, f in evs if len(f) == 1 and len(S) <= 2]
        rk_one = {}
        for y in range(c["V"]):
            rows = [fvec[b] for b, S, f in evs if len(S) <= 2 and set(f) <= {y}]
            rk_one[y] = rank(rows) if rows else 0
        tot["P1_met" if p1 == npairs else "P1_failed"] += 1
        tot["P2_met" if p2 == npairs else "P2_failed"] += 1
        tot["P4_met" if rk_all == k+1 else "P4_failed"] += 1
        R["length_%d" % n] = dict(events=len(evs), pairs=npairs, P1_pairs_ok=p1, P1_fail_examples=p1f,
                                  P2_pairs_ok=p2, P2_fail_examples=p2f, P3=p3, P5=p5, k=k,
                                  P4_rank_all_events=rk_all, P4_needed=k+1,
                                  measured_rank_one_end_vertex_size_le_2=rk_one)
    # P6: different lengths and starting vertices
    ok6 = n6 = 0
    for x1 in range(c["V"]):
        for x2 in range(c["V"]):
            e1 = [(S, family(S, q)) for b, S in events(walks(A["out"], x1, 2))]
            e2 = [(S, family(S, q)) for b, S in events(walks(A["out"], x2, 3))][::7]
            for S1, f1 in e1:
                for S2, f2 in e2:
                    pf = prodfamily(S1, S2, q); n6 += 1
                    good = all(norm2(pf, q, j) == norm2(f1, q, j)*norm2(f2, q, j) for j in range(q)) and \
                        sum(sum(m.values()) for m in pf.values()) == len(S1)*len(S2)
                    ok6 += good
    R["P6"] = dict(pairs=n6, ok=ok6); tot["P6_met" if ok6 == n6 else "P6_failed"] += 1
    # P7 consistency 2->3
    ws2 = walks(A["out"], 0, 2); ok7 = n7 = 0
    for b, S in events(ws2):
        ext = [(w+(y,), y, g+h) for (w, x, g) in S for (y, h) in A["out"][x]]
        f, fe = family(S, q), family(ext, q)
        for j in reps:
            n7 += 1
            ok7 += (len(ext) == A["d"]*len(S)) and (norm2(fe, q, j) == A["d"]*norm2(f, q, j))
    R["P7"] = dict(instances=n7, ok=ok7); tot["P7_met" if ok7 == n7 else "P7_failed"] += 1

res["totals"] = dict(tot)
with open(OUT, "x") as fh: json.dump(res, fh, indent=1, default=str)
print(json.dumps(res["totals"]))
for nm, R in res["carriers"].items():
    print(nm, {kk: R[kk] for kk in ("d", "r", "r0", "C0", "U", "classes", "H")})
    for n in (2, 3):
        L = R.get("length_%d" % n)
        if not L: continue
        print(" n=%d pairs=%d P1=%d P2=%d rank=%d/%d one-vertex=%s" % (n, L["pairs"], L["P1_pairs_ok"], L["P2_pairs_ok"], L["P4_rank_all_events"], L["P4_needed"], L["measured_rank_one_end_vertex_size_le_2"]))
        for rc, v in L["P3"].items(): print("   ", rc, v["multiplicative_all_pairs"], v["predicate_met"], v["violating_pair"])
        for rc, v in L["P5"].items(): print("   P5", rc, v["multiplicative_all_pairs"], v["predicate_met"], v["violating_pair"])
    print(" P6", R.get("P6"), "P7", R.get("P7"))
