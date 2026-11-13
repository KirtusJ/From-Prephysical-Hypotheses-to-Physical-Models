"""Second program: B_8 (two vertices, step [[1,z],[1,-z]], z = exp(2 pi i/8)), a carrier with k = 2 classes.
PREDICATES fixed before the first run. Exact arithmetic in Z[z] (4-tuples, z^4 = -1).
H   out-degree 2, loop at (0,g) so derived digraph aperiodic; strongly connected checked; U(D) computed,
    expected non-empty.  Classes of U(D) up to inverse computed.
Q1  for every tested pair (product enumerated as pairs of walks) and every j in U:
    ||v^j_{S1xS2}||^2 = ||v^j_S1||^2 ||v^j_S2||^2 and |S1xS2| = |S1||S2|.
Q2  rules e = (e0,e1,e2) on (count, class 1, class 2): multiplicative on all tested pairs  <=>
    e in {(0,0,0),(1,0,0),(0,1,0),(0,0,1)}; tested e also (0,1,1),(0,1/2,1/2),(1,1,0),(1,0,1),(1/2,1/2,0),
    (1/2,0,1/2),(1,1,-1),(1/3,1/3,1/3),(0,2,0),(0,1,-1).  Violating pair recorded.
Q3  rank of (f_i(S)) over tested events = 3 (measured first; if < 3 at length 3 the length is raised to 4
    with a fixed-seed sample of 300 events, seed 20261113).
Tested pairs: all ordered pairs of the tested events.  results_b8.json not overwritten.
"""
import json, os, sys, random
from fractions import Fraction as Fr
from collections import Counter
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_b8.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite")
q = 8
def z(e):
    e %= 8; v = [0, 0, 0, 0]; v[e % 4] = 1 if e < 4 else -1; return tuple(v)
def add(a, b): return tuple(x+y for x, y in zip(a, b))
def mul(a, b):
    r = [0]*4
    for i in range(4):
        for j in range(4):
            k = i+j
            if k < 4: r[k] += a[i]*b[j]
            else: r[k-4] -= a[i]*b[j]
    return tuple(r)
def conj(a): return (a[0], -a[3], -a[2], -a[1])
ZERO = (0, 0, 0, 0)
out = {0: [(0, 0), (1, 0)], 1: [(0, 1), (1, 5)]}   # A_{yx}: column 0 = (1,1), column 1 = (z,-z)
# hypothesis
nodes = [(x, g) for x in (0, 1) for g in range(8)]
succ = {u: [(y, (u[1]+h) % 8) for y, h in out[u[0]]] for u in nodes}
def reach(s, sc):
    seen = {s}; st = [s]
    while st:
        u = st.pop()
        for v in sc[u]:
            if v not in seen: seen.add(v); st.append(v)
    return seen
strong = all(len(reach(u, succ)) == 16 for u in nodes)
U = []
for j in range(8):
    ok = True
    for x in (0, 1):
        for x1 in (0, 1):
            s = ZERO
            for y, g in out[x]:
                for y1, g1 in out[x1]:
                    if y == y1: s = add(s, z(j*(g1-g)))
            if s != ((2, 0, 0, 0) if x == x1 else ZERO): ok = False
    if ok: U.append(j)
classes = sorted({tuple(sorted({j, (-j) % 8})) for j in U})
H = strong and len(U) > 0
reps = [c[0] for c in classes]
def walks(n):
    ws = [((), 0, 0)]
    for _ in range(n): ws = [(w+(y,), y, g+h) for w, x, g in ws for y, h in out[x]]
    return ws
def fam(S):
    f = {}
    for _, y, g in S: f.setdefault(y, Counter())[g % 8] += 1
    return f
def n2(f, j):
    t = ZERO
    for m in f.values():
        s = ZERO
        for g, c in m.items(): s = add(s, tuple(c*x for x in z(j*g)))
        t = add(t, mul(s, conj(s)))
    assert t[2] == 0 and t[1] == -t[3]      # real: a + b*sqrt2 with b = t[1]
    return (t[0], t[1])                       # element a + b sqrt 2
def rmul(a, b): return (a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def pfam(S1, S2):
    f = {}
    for _, y1, g1 in S1:
        for _, y2, g2 in S2: f.setdefault((y1, y2), Counter())[(g1+g2) % 8] += 1
    return f
def rank(rows):
    rows = [list(map(Fr, r)) for r in rows]; rk = 0
    for col in range(len(rows[0])):
        p = next((i for i in range(rk, len(rows)) if rows[i][col] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][col] != 0:
                f = rows[i][col]/rows[rk][col]; rows[i] = [a-f*b for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def vec(S, f): return [(len(S), 0)]+[n2(f, j) for j in reps]
def flat(v): return [x for p in v for x in p]   # coordinates over Q in basis 1, sqrt2
def realrank(vs):
    # rank over R of vectors with entries a+b sqrt2: equals rank over Q(sqrt2); bounded below by testing
    # Q-independence of the rows as functions: use numeric-free method: rank over Q of [a-part | b-part] is
    # an upper bound; use exact Gaussian elimination over Q(sqrt2) instead.
    rows = [list(v) for v in vs]; rk = 0
    def inv(a):
        d = Fr(a[0]*a[0]-2*a[1]*a[1]); return (Fr(a[0])/d, Fr(-a[1])/d)
    for col in range(3):
        p = next((i for i in range(rk, len(rows)) if rows[i][col] != (0, 0)), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][col] != (0, 0):
                f = rmul(rows[i][col], inv(rows[rk][col]))
                rows[i] = [(a[0]-rmul(f, b)[0], a[1]-rmul(f, b)[1]) for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
res = dict(strong=strong, U=U, classes=classes, H=H)
log = {}
for n in (3, 4):
    ws = walks(n)
    if n == 3: evs = [[ws[i] for i in range(8) if b >> i & 1] for b in range(256)]
    else:
        rnd = random.Random(20261113)
        evs = [[w for w in ws if rnd.random() < 0.4] for _ in range(300)]
    data = [(S, vec(S, fam(S))) for S in evs]
    rk = realrank(list({tuple(v) for _, v in data}))
    log[n] = dict(events=len(evs), rank=rk)
    if rk == 3: break
E = {"(0,0,0)": (0,0,0), "(1,0,0)": (1,0,0), "(0,1,0)": (0,1,0), "(0,0,1)": (0,0,1), "(0,1,1)": (0,1,1),
     "(0,1/2,1/2)": (0,Fr(1,2),Fr(1,2)), "(1,1,0)": (1,1,0), "(1,0,1)": (1,0,1), "(1/2,1/2,0)": (Fr(1,2),Fr(1,2),0),
     "(1/2,0,1/2)": (Fr(1,2),0,Fr(1,2)), "(1,1,-1)": (1,1,-1), "(1/3,1/3,1/3)": (Fr(1,3),)*3, "(0,2,0)": (0,2,0),
     "(0,1,-1)": (0,1,-1)}
GOOD = {"(0,0,0)", "(1,0,0)", "(0,1,0)", "(0,0,1)"}
def mu(e, v): return (sum(ei*vi[0] for ei, vi in zip(e, v)), sum(ei*vi[1] for ei, vi in zip(e, v)))
viol = {k: None for k in E}; q1 = 0; npairs = 0
for S1, v1 in data:
    for S2, v2 in data:
        npairs += 1
        pf = pfam(S1, S2)
        pv = [(sum(sum(m.values()) for m in pf.values()), 0)]+[n2(pf, j) for j in reps]
        q1 += all(pv[i] == rmul(v1[i], v2[i]) for i in range(3))
        for k, e in E.items():
            if viol[k] is None and mu(e, pv) != rmul(mu(e, v1), mu(e, v2)):
                viol[k] = dict(S1=[list(w[0]) for w in S1], S2=[list(w[0]) for w in S2], mu_prod=str(mu(e, pv)),
                               mu1=str(mu(e, v1)), mu2=str(mu(e, v2)))
q2 = {k: dict(multiplicative=viol[k] is None, predicate_met=(viol[k] is None) == (k in GOOD), violating_pair=viol[k]) for k in E}
res.update(lengths=log, length_used=n, pairs=npairs, Q1_ok=q1, Q2=q2,
           Q2_met=sum(v["predicate_met"] for v in q2.values()), Q2_failed=sum(not v["predicate_met"] for v in q2.values()))
with open(OUT, "x") as fh: json.dump(res, fh, indent=1, default=str)
print({k: res[k] for k in ("strong", "U", "classes", "H", "lengths", "length_used", "pairs", "Q1_ok", "Q2_met", "Q2_failed")})
for k, v in q2.items(): print(k, v["multiplicative"], v["predicate_met"], str(v["violating_pair"])[:200])
