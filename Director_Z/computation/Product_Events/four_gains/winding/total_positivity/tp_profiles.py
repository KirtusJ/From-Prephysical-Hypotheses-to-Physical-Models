#!/usr/bin/env python3
"""Total positivity of the winding profiles at one site.  No randomness unless a layer is cut (seed 20261115).

Usage: python3 -B tp_profiles.py OUT.json N B CAP        (OUT opened with mode 'x')

Carrier: two-rail digraph of the ring Z_N, no gains (q = 1).  A walk from (0,R); lambda = number of left steps.
State = counts indexed (site, rail, lambda); both arcs applied, then a mask (a non-empty set of sites) keeps the
sites named.  Breadth-first over ALL masks with deduplication (lambda shifted so the least is 0).  A site whose
total exceeds B is dropped (lossless for sites of total <= B: all walks of a site move together to each
neighbour, so totals of descendants never fall below it).  If a layer exceeds CAP states it is cut to CAP states
by random.Random(20261115) and every later layer is SAMPLED; the last exhaustive length is recorded.

At a site with walks, l0 = least lambda on both rails, M = N/gcd(N,2); level j = (lambda-l0)/M (asserted integer).
u(x) = sum_j nR(j) x^j,  v(x) = sum_j nL(j) x^j,  W(y) = v(y^2) + y u(y^2).

PREDICATES (fixed before the first run; exact arithmetic, sympy real root isolation, no tolerance).
 P0 control: N=6, masks {1,5},{2,4},{3}: the site 3 carries one walk on R with lambda 0 and one on L with lambda 3.
 P1 (claimed): for every site profile seen, u and v each have only real roots (as polynomials in x; the zero
    polynomial and constants pass).  Hypothesis counted: number of profiles in which u or v has degree >= 2
    after removing the power of x.
 P2 (claimed): for every site profile seen with u != 0 and v != 0: with g = gcd(u,v), the roots of u/g and v/g
    are real, simple and strictly interlace, and the largest root of (u/g)(v/g) is a root of v/g when
    deg(u/g)+deg(v/g) >= 1 ... precisely: listing the roots of v/g and u/g in decreasing order they alternate
    v,u,v,u,...  starting with v, OR u/g is constant and v/g has degree <= 1, OR both are constant.
    (This is the Hermite-Biehler form of: W has no root in the open right half-plane.)
    Hypothesis counted: profiles with u != 0, v != 0 and deg(u/g)+deg(v/g) >= 2.
 P3 (no claim; tabulation): CAND = all (u,v) with total <= B, at most 4 levels on the combined range, least
    level 0 occupied, satisfying P1 and P2 (and, if one rail is empty, P1 only).  Report |CAND|, |SEEN|
    (restricted to <= 4 levels), CAND minus SEEN, SEEN minus CAND (must be empty if P1, P2 hold).
 P4 (no claim; tabulation): OLD = the same list under the two lemmas of the paper only (lem:winding (i),(ii),
    lem:windingrails), to compare |OLD minus SEEN| with |CAND minus SEEN|.
"""
import sys, json, random, itertools
from collections import defaultdict
from math import gcd
import sympy as sp
x = sp.symbols('x')
OUT, N, B, CAP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
fout = open(OUT, 'x')
M = N // gcd(N, 2)

def step(st):
    nw = defaultdict(int)
    for (s, rail, lam), c in st.items():
        nw[((s + 1) % N, 0, lam)] += c
        nw[((s - 1) % N, 1, lam + 1)] += c
    return nw

def norm(st):
    if not st: return ()
    tot = defaultdict(int)
    for (s, r, l), c in st.items(): tot[s] += c
    st = {k: c for k, c in st.items() if tot[k[0]] <= B}
    if not st: return ()
    l0 = min(k[2] for k in st)
    return tuple(sorted(((s, r, l - l0), c) for (s, r, l), c in st.items()))

def profiles(key):
    by = defaultdict(list)
    for (s, r, l), c in key: by[s].append((r, l, c))
    out = []
    for s, items in by.items():
        l0 = min(i[1] for i in items)
        assert all((i[1] - l0) % M == 0 for i in items)
        top = max((i[1] - l0) // M for i in items)
        u = [0] * (top + 1); v = [0] * (top + 1)
        for r, l, c in items: (u if r == 0 else v)[(l - l0) // M] += c
        out.append((tuple(u), tuple(v)))
    return out

_rr = {}
def real_roots_sorted(coeffs):
    """roots (with multiplicity) if all real, else None; coeffs low to high, nonzero polynomial"""
    c = tuple(coeffs)
    if c in _rr: return _rr[c]
    p = sp.Poly(list(reversed(c)), x)
    rr = sp.real_roots(p)
    res = sorted(rr, reverse=True) if len(rr) == p.degree() else None
    _rr[c] = res; return res

def p1(u, v):
    for w in (u, v):
        if any(w) and real_roots_sorted(w) is None: return False
    return True

_p2 = {}
def p2(u, v):
    key = (u, v)
    if key in _p2: return _p2[key]
    pu = sp.Poly(list(reversed(u)), x); pv = sp.Poly(list(reversed(v)), x)
    g = sp.gcd(pu, pv); a = sp.quo(pu, g); b = sp.quo(pv, g)
    ra = sp.real_roots(a); rb = sp.real_roots(b)
    ok = len(ra) == a.degree() and len(rb) == b.degree() and len(set(ra)) == len(ra) and len(set(rb)) == len(rb)
    if ok:
        lab = sorted([(r, 'u') for r in ra] + [(r, 'v') for r in rb], key=lambda t: t[0], reverse=True)
        seq = ''.join(t[1] for t in lab)
        ok = all(seq[i] == ('v' if i % 2 == 0 else 'u') for i in range(len(seq)))
    _p2[key] = ok; return ok

def old(u, v):
    L = len(u)
    for w in (u, v):
        for i in range(L):
            for j in range(i + 2, L):
                if w[i] * w[j] > w[i + 1] * w[j - 1]: return False
            if i + 2 < L and w[i] * w[i + 2] > w[i + 1] * (w[i + 1] - 1): return False
    for l in range(L):
        for l2 in range(L):
            if l2 - l >= 1 and v[l] * u[l2] > v[l + 1] * u[l2 - 1]: return False
            if l2 - l >= 2 and u[l] * v[l2] > u[l + 1] * v[l2 - 1]: return False
    return True

res = {"command": " ".join(sys.argv), "N": N, "M": M, "B": B, "CAP": CAP, "seed": 20261115}
# P0
if N == 6:
    st = {(0, 0, 0): 1}
    for A in ({1, 5}, {2, 4}, {3}):
        st = {k: c for k, c in step(st).items() if k[0] in A}
    res["P0"] = (st == {(3, 0, 0): 1, (3, 1, 3): 1})
masks = [set(c) for k in range(1, N + 1) for c in itertools.combinations(range(N), k)]
rng = random.Random(20261115)
frontier = {norm({(0, 0, 0): 1})}; visited = set(frontier); seen = set(); layers = []; sampled = False; last_exh = 0
t = 0
while frontier and t < 400:
    t += 1; nxt = set()
    for key in frontier:
        full = step({k: c for k, c in key})
        for A in masks:
            k2 = norm({k: c for k, c in full.items() if k[0] in A})
            if k2 and k2 not in visited: visited.add(k2); nxt.add(k2)
    cut = len(nxt) > CAP
    if cut: nxt = set(rng.sample(sorted(nxt), CAP)); sampled = True
    if not sampled: last_exh = t
    for key in nxt:
        for pr in profiles(key): seen.add(pr)
    layers.append([t, len(nxt), sampled]); frontier = nxt
res["layers"] = layers[-3:]; res["n_layers"] = t; res["closed"] = (not frontier) and not sampled
res["last_exhaustive_length"] = last_exh; res["profiles_seen"] = len(seen)
f1 = []; h1 = 0; f2 = []; h2 = 0
def strip(w):
    w = list(w)
    while w and w[0] == 0: w = w[1:]
    while w and w[-1] == 0: w = w[:-1]
    return w
for (u, v) in sorted(seen):
    if max(len(strip(u)), len(strip(v))) >= 3:
        h1 += 1
    if not p1(u, v): f1.append([u, v])
    if any(u) and any(v):
        ok = p2(u, v)
        pu = sp.Poly(list(reversed(u)), x); pv = sp.Poly(list(reversed(v)), x); g = sp.gcd(pu, pv)
        if sp.quo(pu, g).degree() + sp.quo(pv, g).degree() >= 2: h2 += 1
        if not ok: f2.append([u, v])
res["P1"] = {"hypothesis_count": h1, "failures": f1}
res["P2"] = {"hypothesis_count": h2, "failures": f2}
# P3, P4
def comps(total, L):
    if L == 0:
        if total == 0: yield ()
        return
    for a in range(total + 1):
        for rest in comps(total - a, L - 1): yield (a,) + rest
cand = set(); oldset = set()
for L in range(1, 5):
    for tot in range(1, B + 1):
        for w in comps(tot, 2 * L):
            u, v = w[:L], w[L:]
            if u[0] + v[0] == 0 or u[-1] + v[-1] == 0: continue
            if old(u, v): oldset.add((u, v))
            if not p1(u, v): continue
            if any(u) and any(v) and not p2(u, v): continue
            cand.add((u, v))
seen4 = {p for p in seen if len(p[0]) <= 4}
res["P3"] = {"CAND": len(cand), "SEEN_le4": len(seen4), "CAND_minus_SEEN": len(cand - seen4),
             "SEEN_minus_CAND": sorted(seen4 - cand), "examples_CAND_minus_SEEN": sorted(cand - seen4)[:40]}
res["P4"] = {"OLD": len(oldset), "OLD_minus_SEEN": len(oldset - seen4), "SEEN_minus_OLD": sorted(seen4 - oldset)}
res["max_levels_seen"] = max(len(p[0]) for p in seen)
json.dump(res, fout, indent=1); fout.close()
print(json.dumps({k: res[k] for k in ("N", "closed", "last_exhaustive_length", "profiles_seen", "max_levels_seen")}))
print("P0", res.get("P0"), "P1", h1, len(f1), "P2", h2, len(f2), "P3", {k: res["P3"][k] for k in ("CAND", "SEEN_le4", "CAND_minus_SEEN")}, "SEEN-CAND", len(res["P3"]["SEEN_minus_CAND"]), "P4", res["P4"]["OLD"], res["P4"]["OLD_minus_SEEN"])
