"""Target 2: H as an entropy. Command: python3 t2.py   (seed 20261115)
Pair carrier: two copies of the carrier; an event = set of pairs (w, w') of walks of one length T.
n(v,v') = number of pairs ending at (v,v'); eps(v,v') = sum of sign(w)sign(w'); p, H as in S3-S5.
Marginals: first walks / second walks, (m) with multiplicity (each pair counts) and (s) as sets.
PREDICATES fixed before the first run; hypothesis per event: W12 > 0 and W1 > 0 and W2 > 0 (qualifies), else not counted.
 P_sub  H12 <= H1 + H2          (m and s)
 P_mon1 H12 >= H1 ; P_mon2 H12 >= H2   (m and s)
 P_prod (control) for product sets A x B: H12 = H1 + H2 exactly (m: not expected; s: T-2).
Families: (i) every non-empty set of pairs, ring 1 and ring 3, T=2 (65535 sets each);
 (ii) joint-mask events (mask = non-empty set of reachable site pairs after each step): ring 3 T<=2 exhaustive, ring 3 and line T=3 sampled 4000 each;
 (iii) random sets of pairs, rings 1,3,4, T=3, 20000 each; (iv) 'same end site' and 'same end vertex' events T=1..4 rings 1..6 (run 2; run 1 planned T<=5).
 (b) coarse-graining: for every distinct qualifying single-world event state of ring 3 (T<=5), ring 4 (T<=5 in run 2; T<=7 planned in run 1), line (T<=4), merge each pair of
 records into one with eps = sum, n = sum; qualifies if merged W > 0; count H rises / falls / equal.
All violations counted, smallest (fewest pairs) kept."""
import json, random, itertools
from lib import *
random.seed(20261115)
import lib
lib.BITLIM = 100_000   # run 2: run 1 was killed after 9 min without output (BITLIM 3e6 too slow); decimal fallback counted
def walks(N, T):
    ws = [((0, 0), 1, "")]
    for _ in range(T):
        ws = [w for (x, s), sg, h in ws for w in ((((x + 1) % N if N else x + 1, 0), sg, h + "R"), (((x - 1) % N if N else x - 1, 1), -sg if s == 1 else sg, h + "L"))]
    return ws
def analyse(pairs, ws1, ws2):
    """pairs: iterable of (i,j)"""
    st, m1, m2, s1, s2 = {}, {}, {}, {}, {}
    I, J = set(), set()
    def add(d, v, sg):
        a, n = d.get(v, (0, 0)); d[v] = (a + sg, n + 1)
    for i, j in pairs:
        (v, a, _), (u, b, _) = ws1[i], ws2[j]
        add(st, (v, u), a * b); add(m1, v, a); add(m2, u, b); I.add(i); J.add(j)
    for i in I: add(s1, ws1[i][0], ws1[i][1])
    for j in J: add(s2, ws2[j][0], ws2[j][1])
    out = {}
    if not any(e for e, n in st.values()): return None
    for tag, a, b in (("m", m1, m2), ("s", s1, s2)):
        if not any(e for e, n in a.values()) or not any(e for e, n in b.values()): out[tag] = None; continue
        h12, h1, h2 = Hterms(st), Hterms(a), Hterms(b)
        out[tag] = (sign_lin(h1 + h2 + neg(h12)) if (h1 or h2 or h12) else 0, sign_lin(h12 + neg(h1)), sign_lin(h12 + neg(h2)))
    return out
res = {"command": "python3 t2.py > t2_run2.log 2>&1", "seed": 20261115, "families": {}}
best = {}
def run(name, gen, ws1, ws2):
    c = {"events": 0, "zero_pair_weight": 0}
    for tag in "ms":
        c[tag] = dict(qualify=0, sub_viol=0, mon1_viol=0, mon2_viol=0, additive=0)
    for pairs in gen:
        pairs = list(pairs)
        if not pairs: continue
        c["events"] += 1
        r = analyse(pairs, ws1, ws2)
        if r is None: c["zero_pair_weight"] += 1; continue
        for tag in "ms":
            if r[tag] is None: continue
            d = c[tag]; d["qualify"] += 1
            sub, m1, m2 = r[tag]
            for nm, bad in (("sub_viol", sub < 0), ("mon1_viol", m1 < 0), ("mon2_viol", m2 < 0)):
                if bad:
                    d[nm] += 1
                    k = (tag, nm)
                    if k not in best or len(pairs) < len(best[k][1]):
                        best[k] = (name, [(ws1[i][2], ws2[j][2]) for i, j in pairs])
            if sub == 0: d["additive"] += 1
    res["families"][name] = c
    print(name, c, flush=True)
def allsets(m):
    idx = list(itertools.product(range(m), range(m)))
    for b in range(1, 1 << len(idx)):
        yield [idx[k] for k in range(len(idx)) if b >> k & 1]
for N in (1, 3):
    ws = walks(N, 2); run("i_allsets_ring%d_T2" % N, allsets(len(ws)), ws, ws)
def jointmask(N, T, sample=None):
    def rec(t, prs):   # prs: list of (walk1, walk2) as (vertex, sign, hist)
        yield t, prs
        if t == T: return
        ext = [(a2, b2) for a, b in prs for a2 in ext1(a) for b2 in ext1(b)]
        sp = sorted({(a[0][0], b[0][0]) for a, b in ext})
        if sample is None: masks = subsets(sp)
        else: masks = [frozenset(s for s in sp if random.random() < .6)]
        for m in masks:
            sub = [(a, b) for a, b in ext if (a[0][0], b[0][0]) in m]
            if sub: yield from rec(t + 1, sub)
    def ext1(w):
        (x, s), sg, h = w
        return ((((x + 1) % N if N else x + 1, 0), sg, h + "R"), (((x - 1) % N if N else x - 1, 1), -sg if s == 1 else sg, h + "L"))
    reps = 1 if sample is None else sample
    for _ in range(reps):
        for t, prs in rec(0, [(((0, 0), 1, ""), ((0, 0), 1, ""))]):
            if sample is not None and t < T: continue
            wl = {}
            l1 = sorted({a for a, b in prs}); l2 = sorted({b for a, b in prs})
            i1 = {a: i for i, a in enumerate(l1)}; i2 = {b: i for i, b in enumerate(l2)}
            yield l1, l2, [(i1[a], i2[b]) for a, b in prs]
def runjm(name, N, T, sample=None):
    c = {"events": 0, "zero_pair_weight": 0}
    for tag in "ms": c[tag] = dict(qualify=0, sub_viol=0, mon1_viol=0, mon2_viol=0, additive=0)
    for l1, l2, pairs in jointmask(N, T, sample):
        c["events"] += 1
        r = analyse(pairs, l1, l2)
        if r is None: c["zero_pair_weight"] += 1; continue
        for tag in "ms":
            if r[tag] is None: continue
            d = c[tag]; d["qualify"] += 1
            sub, m1, m2 = r[tag]
            for nm, bad in (("sub_viol", sub < 0), ("mon1_viol", m1 < 0), ("mon2_viol", m2 < 0)):
                if bad:
                    d[nm] += 1
                    k = ("jointmask_" + tag, nm)
                    if k not in best or len(pairs) < len(best[k][1]):
                        best[k] = (name, [(l1[i][2], l2[j][2]) for i, j in pairs])
            if sub == 0: d["additive"] += 1
    res["families"][name] = c
    print(name, c, flush=True)
runjm("ii_jointmask_ring3_Tle2_exhaustive", 3, 2)
runjm("ii_jointmask_ring3_T3_sample4000", 3, 3, 4000)
runjm("ii_jointmask_line_T3_sample4000", None, 3, 4000)
runjm("ii_jointmask_ring4_T4_sample2000", 4, 4, 2000)
for N in (1, 3, 4):
    ws = walks(N, 3); m = len(ws)
    def g():
        for _ in range(20000):
            d = random.random()
            yield [(i, j) for i in range(m) for j in range(m) if random.random() < d]
    run("iii_random_ring%d_T3" % N, g(), ws, ws)
for N in range(1, 7):
    for T in range(1, 5):
        ws = walks(N, T); m = len(ws)
        run("iv_same_site_ring%d_T%d" % (N, T), [[(i, j) for i in range(m) for j in range(m) if ws[i][0][0] == ws[j][0][0]]], ws, ws)
        run("iv_same_vertex_ring%d_T%d" % (N, T), [[(i, j) for i in range(m) for j in range(m) if ws[i][0] == ws[j][0]]], ws, ws)
res["smallest_violations"] = {"%s/%s" % k: v for k, v in best.items()}
# (b) coarse-graining
cg = {}
for N, Tmax in ((3, 5), (4, 5), (None, 4)):
    seen = set(); c = dict(states=0, merges=0, qualify=0, rise=0, fall=0, equal=0); ex = {}
    for T, ms, st in events(N, Tmax):
        k = key(st)
        if k in seen or not any(e for e, n in st.values()): continue
        seen.add(k); c["states"] += 1
        for u, v in itertools.combinations(sorted(st), 2):
            c["merges"] += 1
            m = {w: d for w, d in st.items() if w not in (u, v)}
            m["merged"] = (st[u][0] + st[v][0], st[u][1] + st[v][1])
            if not any(e for e, n in m.values()): continue
            c["qualify"] += 1
            s = sign_lin(Hterms(m) + neg(Hterms(st))) if (Hterms(m) + Hterms(st)) else 0
            nm = "rise" if s > 0 else "fall" if s < 0 else "equal"
            c[nm] += 1
            if nm not in ex or len(st) < len(ex[nm]["state"]):
                ex[nm] = {"T": T, "masks": ms, "state": sorted(st.items()), "merge": [u, v], "H": Hval(st), "H_merged": Hval(m)}
    cg["line" if N is None else "ring%d" % N] = {"counts": c, "examples": ex}
    print(N, c, flush=True)
res["coarse_graining"] = cg
res["sign_fallbacks_to_decimal"] = FALLBACK[0]
json.dump(res, open("result_t2_run2.json", "x"), indent=1, default=str)
print(json.dumps(res["smallest_violations"], indent=0, default=str))
print(json.dumps({k: v["examples"] for k, v in cg.items() if k == "ring3"}, default=str))
