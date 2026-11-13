#!/usr/bin/env python3
"""abund_v2.py (follow-up to abund.py; abund_result.json is KEPT with its failures:
P4 and P1 failed on carriers 265 and 283 because v1 stated the coset at y2 as
K-u; the derivation gives K+u [(y1,g)->(z,g+a1), (y2,g+u)->(z,g+u+a2), u=a1-a2].
The two signs agree unless 2*phi(u) != 0, i.e. only when m >= 3.  Only that sign
is changed here; sampling and seed are identical.) -- test of the corrected "abundance" lemma on finite gain digraphs.

PREDICATES (fixed before the first run; failures are kept in the result file).

Carrier: line digraph D of a random d-regular base multidigraph (union of d
permutations of n points), gains in C = Z/q (written additively as exponents
of zeta_q), one d x d block per base vertex:
  d=2: [[k0,k1],[k2,k2+k1-k0+q/2]], q in {2,4,6,8,12}
  d=3: rho_z+kappa_y+(q/3) z y,       q in {3,6,9,12}
  d=4: rho_z+kappa_y+(q/4) z y,       q in {4,8}
Two sampling modes per (d,q), 30 carriers each, seed 20261113:
  'uniform': free exponents uniform in Z/q;
  'coset'  : free exponents in s+tZ (rho in s+tZ, kappa in tZ for d>=3), t>1 a
             divisor of q/2 (d=2) or q/d (d>=3), chosen at random; if no such t
             exists the mode degenerates to uniform (recorded as t=1).
Derived digraph D^ on V x C.  r = period of D^, r0 = period of D (BFS levels,
gcd over all arcs; exact).  c = class function of D^ mod r.
phi(h) = c(x,g+h)-c(x,g);  C0 = ker phi;  m = |C/C0|.

H   (hypothesis, tested per carrier): A*A = d exactly (cyclotomic remainder,
    integer arithmetic), d >= 2, D^ strongly connected.  Pairs: all unordered
    y1 != y2 with a common successor.
P0a every vertex of D has exactly d successors and d predecessors.
P0b D weakly connected => strongly connected; same for D^.
P0c D^ strongly connected  <=>  D strongly connected and the gains of the
    fundamental closed walks of a BFS tree generate Z/q.
P6  (under H) phi is well defined (independent of (x,g)) and additive.
P7  (under H) r0 | r, image(phi) = r0 Z/r, m = r/r0.
P4  (under H) for each pair and each common successor z, with
    u = gain(y1->z) - gain(y2->z): c(y1,g) = c(y2,g+u) for all g
    [so gains at y2 lie in the coset (gains at y1) + u], and the coset of u
    mod C0 does not depend on z.
P5  (under H) at every length L <= Lstop, every x0, y: the set of gains of
    walks of length L from x0 to y lies in ONE coset of C0 (or is empty).
P1  (under H) CORRECTED LEMMA: for every x0 in V, every pair, every coset K of
    C0 there is L <= LCAP at which: >= N walks x0->y1 with gain g for every g
    in K, none for g outside K; >= N walks x0->y2 with gain g for every g in
    K+u, none outside.  N = 5.  LCAP = 400 is a search budget, not a
    tolerance; hitting it counts as a FAILURE of P1 and is kept.
P3  (under H) NAIVE statement ("at one L, every g in C has >= N walks to y1
    and to y2") holds for all x0 and pairs  <=>  r = r0 (i.e. C0 = C).  When
    r != r0 it must fail for every x0 and every pair at every L <= Lstop+r
    (obstruction = P5: support in a proper coset).  Counterexamples recorded.
P2  counts: carriers, carriers with H, periodic (r>1), with r != r0.

Walk counts are exact: int64 while d^L < 2^62, Python integers afterwards.
The result file is never overwritten.
"""
import sys, os, json, math
import numpy as np

SEED = 20261113
N = 5
LCAP = 400
OUT = "abund_result_v2.json"

# ---------- exact zero test for sums of q-th roots of unity ----------
def polydiv(a, b):
    a = a[:]; q = [0]*(max(len(a)-len(b)+1, 1))
    while len(a) >= len(b) and any(a):
        c = a[-1] // b[-1]
        assert c*b[-1] == a[-1]
        sh = len(a)-len(b); q[sh] = c
        for i, bi in enumerate(b): a[sh+i] -= c*bi
        a.pop()
    return q, a
_cyc = {}
def cyclo(n):
    if n in _cyc: return _cyc[n]
    p = [-1]+[0]*(n-1)+[1]
    for dd in range(1, n):
        if n % dd == 0:
            p, rem = polydiv(p, cyclo(dd)); assert not any(rem)
            while p[-1] == 0: p.pop()
    _cyc[n] = p; return p
def root_sum_is_zero(exps, q):
    a = [0]*q
    for e in exps: a[e % q] += 1
    while len(a) > 1 and a[-1] == 0: a.pop()
    phi = cyclo(q)
    if len(a) < len(phi): return not any(a)
    _, rem = polydiv(a, phi)
    return not any(rem)

# ---------- carrier ----------
def make_carrier(rng, d, q, mode):
    n = int(rng.integers(2, 6 if d < 4 else 5))
    perms = [rng.permutation(n) for _ in range(d)]
    V = n*d                               # vertex = base arc (i,j) -> i*d+j
    head = [int(perms[j][i]) for i in range(n) for j in range(d)]
    inarcs = [[] for _ in range(n)]
    for a in range(V): inarcs[head[a]].append(a)
    t, s = 1, 0
    if mode == 'coset':
        base = q//2 if d == 2 else q//d
        divs = [x for x in range(2, base+1) if base % x == 0]
        if divs:
            t = int(divs[int(rng.integers(len(divs)))]); s = int(rng.integers(t))
    def draw(shift):
        return int((shift + t*int(rng.integers(q//t))) % q)
    arcs = {}                             # (x,y) -> exponent
    blocks = []
    for v in range(n):
        if d == 2:
            k0, k1, k2 = draw(s), draw(s), draw(s)
            blk = [[k0, k1], [k2, (k2+k1-k0+q//2) % q]]
        else:
            rho = [draw(s) for _ in range(d)]; kap = [draw(0) for _ in range(d)]
            blk = [[(rho[z]+kap[y]+(q//d)*z*y) % q for y in range(d)] for z in range(d)]
        blocks.append(blk)
        for yi, x in enumerate(inarcs[v]):
            for z in range(d):
                arcs[(x, v*d+z)] = blk[z][yi]
    return dict(n=n, d=d, q=q, mode=mode, t=t, s=s, V=V, arcs=arcs,
                perms=[[int(a) for a in p] for p in perms], blocks=blocks)

def reach(adj, root):
    seen = {root}; st = [root]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); st.append(v)
    return seen
def conn(nv, arclist):
    out = [[] for _ in range(nv)]; inn = [[] for _ in range(nv)]; und = [[] for _ in range(nv)]
    for u, v in arclist:
        out[u].append(v); inn[v].append(u); und[u].append(v); und[v].append(u)
    weak = len(reach(und, 0)) == nv
    strong = len(reach(out, 0)) == nv and len(reach(inn, 0)) == nv
    return weak, strong, out
def period_classes(nv, out):
    lev = [None]*nv; lev[0] = 0; qu = [0]
    for u in qu:
        for v in out[u]:
            if lev[v] is None: lev[v] = lev[u]+1; qu.append(v)
    r = 0
    for u in range(nv):
        for v in out[u]: r = math.gcd(r, lev[u]+1-lev[v])
    return r, [l % r for l in lev]

def analyse(car):
    d, q, V, arcs = car['d'], car['q'], car['V'], car['arcs']
    res = dict(d=d, q=q, n=car['n'], mode=car['mode'], t=car['t'], s=car['s'])
    fails = []
    succ = [[] for _ in range(V)]; pred = [[] for _ in range(V)]
    for (x, y), k in arcs.items(): succ[x].append(y); pred[y].append(x)
    # exact A*A = d
    ok = all(len(succ[x]) == d for x in range(V))
    for x in range(V):
        for x2 in range(x+1, V):
            common = [y for y in succ[x] if (x2, y) in arcs]
            if common and not root_sum_is_zero([arcs[(x2, y)]-arcs[(x, y)] for y in common], q):
                ok = False
    res['AstarA_eq_d'] = ok
    p0a = all(len(succ[x]) == d and len(pred[x]) == d for x in range(V))
    if not p0a: fails.append('P0a')
    wD, sD, outD = conn(V, list(arcs.keys()))
    NV = V*q
    harcs = [(x*q+g, y*q+(g+k) % q) for (x, y), k in arcs.items() for g in range(q)]
    wH, sH, outH = conn(NV, harcs)
    if (wD and not sD) or (wH and not sH): fails.append('P0b')
    # closed-walk gain group via BFS tree potentials (independent of D^)
    gam = {0: 0}; qu = [0]
    for u in qu:
        for v in succ[u]:
            if v not in gam: gam[v] = (gam[u]+arcs[(u, v)]) % q; qu.append(v)
    gg = q
    for (u, v), k in arcs.items():
        if u in gam and v in gam: gg = math.gcd(gg, (gam[u]+k-gam[v]) % q)
    gen_all = (gg == 1) or q == 1
    if sH != (sD and gen_all): fails.append('P0c')
    res.update(D_weak=wD, D_strong=sD, Dhat_weak=wH, Dhat_strong=sH, closed_gain_index=gg)
    H = ok and d >= 2 and sH
    res['H'] = H
    if not H:
        res['failed'] = fails; return res
    r0, c0 = period_classes(V, outD)
    r, c = period_classes(NV, outH)
    c = np.array(c).reshape(V, q)
    # P6
    phi = [int((c[0, h]-c[0, 0]) % r) for h in range(q)]
    p6 = all(((c[x, (g+h) % q]-c[x, g]) % r) == phi[h] for x in range(V) for g in range(q) for h in range(q))
    p6 = p6 and all(phi[(h+h2) % q] == (phi[h]+phi[h2]) % r for h in range(q) for h2 in range(q))
    if not p6: fails.append('P6')
    C0 = [h for h in range(q) if phi[h] == 0]
    img = sorted(set(phi)); m = len(img)
    p7 = (r % r0 == 0) and img == [(r0*j) % r for j in range(r//r0)] and m == r//r0 and m*len(C0) == q
    if not p7: fails.append('P7')
    res.update(r=r, r0=r0, m=m, C0=C0, phi=phi)
    if not (p6 and p7):
        res['failed'] = fails; return res
    cos = np.array([p//r0 for p in phi])            # coset index of g
    # pairs
    pairs = []; p4 = True
    for y1 in range(V):
        for y2 in range(y1+1, V):
            zs = [z for z in succ[y1] if (y2, z) in arcs]
            if not zs: continue
            us = [(arcs[(y1, z)]-arcs[(y2, z)]) % q for z in zs]
            for u in us:
                if not all(c[y1, g] == c[y2, (g+u) % q] for g in range(q)): p4 = False
            if len({int(cos[u]) for u in us}) != 1: p4 = False
            pairs.append((y1, y2, int(cos[us[0]])))
    if not p4: fails.append('P4')
    res['pairs'] = len(pairs)
    # exact walk counting from all (x0,0)
    M = np.zeros((NV, NV), dtype=np.int64)
    for a, b in harcs: M[b, a] += 1
    W = np.zeros((NV, V), dtype=np.int64)
    for x0 in range(V): W[x0*q, x0] = 1
    P = len(pairs); y1s = np.array([p[0] for p in pairs]); y2s = np.array([p[1] for p in pairs])
    su = np.array([p[2] for p in pairs])
    sat = np.zeros((P, m, V), dtype=bool); naive = np.zeros((P, V), dtype=bool)
    p5 = True; Lsat = None; Lnaive_first = None; L = 0; extra = None
    while L < LCAP:
        L += 1
        if d**L >= 2**62 and W.dtype != object:
            W = W.astype(object); M = M.astype(object)
        W = M.dot(W)
        assert all(int(W[:, x0].sum()) == d**L for x0 in (0, V-1))
        T = W.reshape(V, q, V)
        pos = (T > 0); big = (T >= N)
        hit = np.stack([pos[:, cos == j, :].any(axis=1) for j in range(m)])     # m,V,V
        if (hit.sum(axis=0) > 1).any(): p5 = False
        clean = np.stack([big[:, cos == j, :].all(axis=1) & (hit.sum(axis=0) == 1) & hit[j] for j in range(m)])
        for j in range(m):
            sat[:, j, :] |= clean[j][y1s, :] & clean[(j+su) % m, y2s, :]
        allb = big.all(axis=1)
        nv_ = allb[y1s, :] & allb[y2s, :]
        if nv_.any() and Lnaive_first is None: Lnaive_first = L
        naive |= nv_
        if Lsat is None and sat.all(): Lsat = L; extra = L+r
        if extra is not None and L >= extra: break
    res.update(L_all_satisfied=Lsat, L_stop=L, naive_all=bool(naive.all()), naive_any=bool(naive.any()),
               L_naive_first=Lnaive_first)
    if not p5: fails.append('P5')
    if Lsat is None: fails.append('P1')
    if r == r0:
        if not naive.all(): fails.append('P3')
    else:
        if naive.any(): fails.append('P3')
    res['failed'] = fails
    return res

def main():
    if os.path.exists(OUT):
        sys.exit("refusing to overwrite " + OUT)
    rng = np.random.default_rng(SEED)
    combos = [(2, q) for q in (2, 4, 6, 8, 12)] + [(3, q) for q in (3, 6, 9, 12)] + [(4, q) for q in (4, 8)]
    recs = []; examples = []
    for d, q in combos:
        for mode in ('uniform', 'coset'):
            for i in range(30):
                car = make_carrier(rng, d, q, mode)
                res = analyse(car); res['id'] = len(recs)
                if res.get('H') and res['r'] != res['r0'] and len(examples) < 6 and not any(e['d'] == d and e['q'] == q for e in examples):
                    ex = dict(res); ex['perms'] = car['perms']; ex['blocks'] = car['blocks']
                    ex['arcs'] = [[x, y, k] for (x, y), k in sorted(car['arcs'].items())]
                    examples.append(ex)
                recs.append(res)
    Hs = [r_ for r_ in recs if r_['H']]
    summ = dict(
        carriers=len(recs), AstarA_exact=sum(r_['AstarA_eq_d'] for r_ in recs),
        H_holds=len(Hs), Dhat_not_strong=sum(not r_['Dhat_strong'] for r_ in recs),
        D_not_strong=sum(not r_['D_strong'] for r_ in recs),
        periodic_r_gt_1=sum(r_['r'] > 1 for r_ in Hs), aperiodic=sum(r_['r'] == 1 for r_ in Hs),
        r_ne_r0=sum(r_['r'] != r_['r0'] for r_ in Hs),
        r_eq_r0_gt_1=sum(r_['r'] == r_['r0'] and r_['r'] > 1 for r_ in Hs),
        naive_fails=sum(not r_.get('naive_all', True) for r_ in Hs),
        pairs_tested=sum(r_.get('pairs', 0) for r_ in Hs),
        max_L_all_satisfied=max([r_['L_all_satisfied'] or -1 for r_ in Hs] + [-1]),
        failed_predicates={p: [r_['id'] for r_ in recs if p in r_['failed']]
                           for p in ('P0a', 'P0b', 'P0c', 'P1', 'P3', 'P4', 'P5', 'P6', 'P7')},
        by_combo={f"d{d}_q{q}_{mode}": dict(
            H=sum(r_['H'] for r_ in recs if (r_['d'], r_['q'], r_['mode']) == (d, q, mode)),
            r_ne_r0=sum(r_['H'] and r_['r'] != r_['r0'] for r_ in recs if (r_['d'], r_['q'], r_['mode']) == (d, q, mode)),
            periodic=sum(r_['H'] and r_['r'] > 1 for r_ in recs if (r_['d'], r_['q'], r_['mode']) == (d, q, mode)))
            for d, q in combos for mode in ('uniform', 'coset')})
    out = dict(seed=SEED, N=N, LCAP=LCAP, summary=summ, counterexamples_to_naive=examples, carriers=recs)
    with open(OUT, 'x') as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(summ, indent=1))

if __name__ == '__main__':
    main()
