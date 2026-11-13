#!/usr/bin/env python3
"""Challenger 9 program for Lemma lem:classes, Theorem thm:periodic, Corollary cor:periodic.

PREDICATES (fixed before the first run). Seed 20261113. Result file refused if it exists.

Hypothesis test per carrier (H): finite, gains in finite abelian C, at most one arc per ordered
pair, exactly d>=2 out-arcs at every vertex, derived digraph hatD strongly connected. A carrier
that fails H is counted as "not qualifying" and no predicate is evaluated on it. Qualifying
carriers with period r>1 are the target; r=1 qualifiers are evaluated too and counted apart.

Per qualifying carrier:
 L1  kappa (BFS level mod r from (x0,1)) satisfies kappa(v)=kappa(u)+1 on every arc of hatD, and r
     (gcd of lev[u]+1-lev[v]) equals the gcd of closed-walk lengths n<=2|V||C| found by matrix powers;
     there is n0 at which the reachability pattern is exactly "n = kappa(v)-kappa(u) mod r".
     (n0 itself is MEASURED ONLY.)
 L2  for k=0..4 and n=n0+k..n0+k+r-1: every admissible pair (u,v) has >= d^k/(|V||C|) walks.
 L3  C0=S_0(x0) is a subgroup; every non-empty fibre is a coset of C0; for fixed y the non-empty
     fibres partition C into all cosets; S_{i+1}(z)=A_zy S_i(y) for every arc with S_i(y) non-empty;
     |C|/|C0| = r/r0.
 L4  at lengths n=1..5 the set of (end, gain) of walks from x0 equals a subset of X_n, and the number
     of D-walks from x0 to y with gain g equals the number of hatD-walks (x0,1)->(y,g).
 Q1  D' has gains in C0, <=1 arc per ordered pair, d out-arcs at each vertex of V'; the stated map
     V x C -> V' x C0 is a bijection carrying the arc set of hatD onto the arc set of the derived
     digraph of D'; the latter is strongly connected.
 Q2  if y != y1 have a common successor then S_i(y) non-empty <=> S_i(y1) non-empty, all i.
 U1  for every character psi of C: psi in U(D)  <=>  psi|C0 in U(D') (U(D') computed with the
     gains of D' through psi). Hence U(D) is a union of cosets of C0^perp.
 U2  U(D) is disjoint from C0^perp.
 A   for psi, lambda with equal or inverse restrictions to C0: |sigma_psi(m)|^2=|sigma_lambda(m)|^2
     on all fibre-supported multisets of size <=3.
 DIM dimension of the solution space of the law (GL) imposed on class-supported families of total
     size <=3, unknowns F_y(m) for fibre-supported m of size 1..3, equals 1+#(U(D)|C0/~).
     (Upper bound by rank modulo the prime 2^61-1, lower bound by SOL+IND; exact if both meet;
     fmpz rank used if they do not meet.)
 SOL |m| and |sigma_psi|^2 (one psi in U(D) per class of restrictions) satisfy every equation.
 IND these functions are linearly independent on the fibre-supported multisets of size <=3.
 NC  count restricted to class 0 (F_y(m)=|m| if m on S_0(y), else 0) is NOT a solution, and for every
     class rep psi the square restricted to class 0 is NOT a solution (constants cannot depend on class).
 NV  count restricted to the vertex x0 is NOT a solution (constants cannot depend on vertex).
 DP  (only if |V||C|<=32) the law on D' for ALL families of total size <=3 over C0 has solution
     dimension (rank mod p) 1+#(U(D')/~)  [layer decomposition claim].
 C2  (only if |C|<=8) for all psi != lambda: with F=Re(c sigma_psi conj sigma_lambda), the real
     space of c for which F solves the law consists of c with F=0 on all fibre multisets of size <=3
     (tested as rank[[r1|F1],[ri|Fi]] == rank[[r1],[ri]] over Q, c=1 and c=i).
 PER (r=r0 only) C0=C and every fibre is empty or all of C; if r>1 no length class has all vertices.

Named examples (EX): ring N=4,6: r=r0=2, U(D)={sign}, DIM=2. zeta*H over Z8: r=4,r0=1,C0={+-1},
U(D)=4 faithful characters, DIM=2. a*[[1,1],[1,b]] over C2xC2: r=2,r0=1,C0={1,b},U(D)={psi(b)=-1},
DIM=2. Four-vertex example: r=2,r0=1,C0={+-1},U(D)={chi,chi^-1},DIM=2 (arc triples read as
(source,target,exponent); the other reading is run as well and reported).
"""
import sys, os, json, itertools, random
from math import gcd
from functools import reduce
import numpy as np
from flint import fmpz_mat, nmod_mat, fmpz_poly

SEED = 20261113
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1] if len(sys.argv) > 1 else "results.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)
P61 = (1 << 61) - 1

def lcm(a, b): return a * b // gcd(a, b)

class Grp:
    def __init__(self, ns):
        self.ns = tuple(ns)
        self.el = list(itertools.product(*[range(n) for n in ns]))
        self.idx = {e: i for i, e in enumerate(self.el)}
        self.n = len(self.el)
        self.e = reduce(lcm, ns, 1)
        self.E = lcm(self.e, 4)
        self.mul = [[self.idx[tuple((a + b) % n for a, b, n in zip(x, y, ns))] for y in self.el] for x in self.el]
        self.inv = [self.idx[tuple((-a) % n for a, n in zip(x, ns))] for x in self.el]
        # characters: tuple j ; exponent of psi_j(g) as power of zeta_E
        self.chars = self.el
        self.chi = [[sum(j[t] * g[t] * (self.E // ns[t]) for t in range(len(ns))) % self.E for g in self.el] for j in self.chars]
        # reduction matrix x^k mod Phi_E
        phi = fmpz_poly.cyclotomic(self.E) if hasattr(fmpz_poly, "cyclotomic") else None
        if phi is None:
            raise RuntimeError("no cyclotomic")
        deg = phi.degree()
        R = np.zeros((self.E, deg), dtype=np.int64)
        for k in range(self.E):
            p = fmpz_poly([0] * k + [1]) % phi
            c = [int(x) for x in p.coeffs()]
            R[k, :len(c)] = c
        self.R = R; self.deg = deg

def red(G, hist):
    """hist: int array (..., E) -> (..., deg) exact reduction mod Phi_E"""
    return hist @ G.R

def strongly_connected(n, succ):
    def reach(adj):
        seen = {0}; st = [0]
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v); st.append(v)
        return len(seen) == n
    pred = [[] for _ in range(n)]
    for u in range(n):
        for v in succ[u]: pred[v].append(u)
    return reach(succ) and reach(pred)

def period_levels(n, succ, root):
    lev = [None] * n; lev[root] = 0; q = [root]
    for u in q:
        for v in succ[u]:
            if lev[v] is None: lev[v] = lev[u] + 1; q.append(v)
    r = 0
    for u in range(n):
        for v in succ[u]: r = gcd(r, lev[u] + 1 - lev[v])
    return r, lev

def multisets(pool, maxsize=3):
    for s in range(1, maxsize + 1):
        yield from itertools.combinations_with_replacement(pool, s)

def rank_mod(rows, ncols):
    if not rows: return 0
    return nmod_mat(len(rows), ncols, [x % P61 for r in rows for x in r], P61).rank()

def rank_Z(rows):
    if not rows: return 0
    return fmpz_mat(len(rows), len(rows[0]), [int(x) for r in rows for x in r]).rank()

def law_system(nv, succ, mul, supports, pools, d):
    """supports[y] = list of frozensets of group elements (allowed supports of unknown multisets at y)
    pools = list of lists of (y,g). Returns unknown index dict and dense int rows (deduped)."""
    unk = {}
    for y in range(nv):
        for S in supports[y]:
            for m in multisets(sorted(S)):
                unk.setdefault((y, m), len(unk))
    rows = set()
    for pool in pools:
        for fam in multisets(pool):
            row = {}
            my = {}; wz = {}
            for (y, g) in fam:
                my.setdefault(y, []).append(g)
                for (z, a) in succ[y]:
                    wz.setdefault(z, []).append(mul[a][g])
            for z, w in wz.items():
                k = unk[(z, tuple(sorted(w)))]  # KeyError here would mean w_z is not fibre supported
                row[k] = row.get(k, 0) + 1
            for y, m in my.items():
                k = unk[(y, tuple(sorted(m)))]
                row[k] = row.get(k, 0) - d
            rows.add(tuple(sorted(row.items())))
    dense = []
    for r in rows:
        v = [0] * len(unk)
        for k, c in r: v[k] = c
        dense.append(v)
    return unk, dense

def analyse(name, ns, nv, arcs, heavy=True):
    """arcs: list of (y, z, gtuple) meaning arc y->z with gain g. Returns record dict."""
    G = Grp(ns)
    rec = {"name": name, "group": list(ns), "nV": nv, "pred": {}, "meas": {}}
    A = {}
    simple = True
    for (y, z, g) in arcs:
        if (y, z) in A: simple = False
        A[(y, z)] = G.idx[tuple(g)]
    succ = [[] for _ in range(nv)]
    for (y, z), g in A.items(): succ[y].append((z, g))
    degs = {len(s) for s in succ}
    d = len(succ[0])
    nC = G.n; N = nv * nC
    hs = [[] for _ in range(N)]
    for y in range(nv):
        for g in range(nC):
            for (z, a) in succ[y]: hs[y * nC + g].append(z * nC + G.mul[a][g])
    H = simple and degs == {d} and d >= 2 and strongly_connected(N, hs)
    rec["H"] = bool(H)
    if not H:
        rec["why"] = "simple=%s degs=%s hat_sc=%s" % (simple, sorted(degs), strongly_connected(N, hs) if simple else None)
        return rec
    x0 = 0; one = G.idx[tuple(0 for _ in ns)]
    r, lev = period_levels(N, hs, x0 * nC + one)
    r0, _ = period_levels(nv, [[z for z, _ in s] for s in succ], x0)
    kap = [l % r for l in lev]
    rec.update(d=d, r=r, r0=r0)
    P = rec["pred"]
    # L1
    ok = all(kap[v] == (kap[u] + 1) % r for u in range(N) for v in hs[u])
    B = np.zeros((N, N), dtype=np.int64)
    for u in range(N):
        for v in hs[u]: B[v, u] = 1
    Bn = np.eye(N, dtype=np.int64); gg = 0; n0 = None
    pat = [np.array([[1 if (kap[v] - kap[u] - n) % r == 0 else 0 for u in range(N)] for v in range(N)]) for n in range(r)]
    for n in range(1, 4 * N + 1):
        Bn = ((B @ Bn) > 0).astype(np.int64)
        if n <= 2 * N and np.trace(Bn) > 0: gg = gcd(gg, n)
        if n0 is None and np.array_equal(Bn, pat[n % r]): n0 = n
        if n0 is not None and n > 2 * N: break
    P["L1"] = bool(ok and gg == r and n0 is not None)
    rec["meas"]["n0"] = n0
    # L2 and L4 (exact walk counts with python ints)
    Bo = B.astype(object); Wn = np.eye(N, dtype=object); cnt = {}
    top = (n0 or 0) + 4 + r
    okL2 = n0 is not None; minratio = None
    # D-walk enumeration for L4
    walks = {(x0, one): 1}; okL4 = True
    for n in range(1, top + 1):
        Wn = Bo.dot(Wn)
        if n <= 5:
            nw = {}
            for (y, g), c in walks.items():
                for (z, a) in succ[y]:
                    key = (z, G.mul[a][g]); nw[key] = nw.get(key, 0) + c
            walks = nw
            for y in range(nv):
                for g in range(nC):
                    c = walks.get((y, g), 0)
                    if c != Wn[y * nC + g, x0 * nC + one]: okL4 = False
                    if c > 0 and kap[y * nC + g] != n % r: okL4 = False
        if n0 is not None and n >= n0:
            for k in range(0, 5):
                if n0 + k <= n <= n0 + k + r - 1:
                    for u in range(N):
                        for v in range(N):
                            if (kap[v] - kap[u] - n) % r == 0:
                                if Wn[v, u] * N < d ** k: okL2 = False
                                rt = Wn[v, u] * N / d ** k
                                minratio = rt if minratio is None else min(minratio, rt)
    P["L2"] = bool(okL2); P["L4"] = bool(okL4)
    rec["meas"]["L2_min_count_over_bound"] = minratio
    # L3
    fib = {(y, i): frozenset(g for g in range(nC) if kap[y * nC + g] == i) for y in range(nv) for i in range(r)}
    C0 = fib[(x0, 0)]
    sub = one in C0 and all(G.mul[a][b] in C0 for a in C0 for b in C0)
    cos = all((not S) or S == frozenset(G.mul[min(S)][h] for h in C0) for S in fib.values())
    part = all(sum(len(fib[(y, i)]) for i in range(r)) == nC for y in range(nv))
    shift = all(fib[(z, (i + 1) % r)] == frozenset(G.mul[a][g] for g in fib[(y, i)])
                for y in range(nv) for i in range(r) if fib[(y, i)] for (z, a) in succ[y])
    P["L3"] = bool(sub and cos and part and shift and nC * r0 == len(C0) * r)
    rec["C0"] = [list(G.el[g]) for g in sorted(C0)]
    rec["fibres"] = {"%d,%d" % k: sorted(v) for k, v in fib.items() if v}
    # Q1: quotient carrier
    Vp = [k for k in sorted(fib) if fib[k]]; vpi = {k: i for i, k in enumerate(Vp)}
    b = {k: min(fib[k]) for k in Vp}
    succp = [[] for _ in Vp]; q1 = True; pairs = set()
    for (y, i) in Vp:
        for (z, a) in succ[y]:
            k2 = (z, (i + 1) % r)
            if k2 not in vpi: q1 = False; continue
            ga = G.mul[G.mul[a][b[(y, i)]]][G.inv[b[k2]]]
            if ga not in C0: q1 = False
            if (vpi[(y, i)], vpi[k2]) in pairs: q1 = False
            pairs.add((vpi[(y, i)], vpi[k2]))
            succp[vpi[(y, i)]].append((vpi[k2], ga))
    q1 = q1 and all(len(s) == d for s in succp)
    C0l = sorted(C0)
    def bij(y, g):
        k = (y, kap[y * nC + g]); return (vpi[k], G.mul[g][G.inv[b[k]]])
    img = {bij(y, g) for y in range(nv) for g in range(nC)}
    q1 = q1 and len(img) == N and img == {(v, h) for v in range(len(Vp)) for h in C0l}
    arcs_hat = {(bij(y, g), bij(z, G.mul[a][g])) for y in range(nv) for g in range(nC) for (z, a) in succ[y]}
    arcs_der = {((v, h), (w, G.mul[a][h])) for v in range(len(Vp)) for h in C0l for (w, a) in succp[v]}
    q1 = q1 and arcs_hat == arcs_der
    P["Q1"] = bool(q1)
    # Q2
    q2 = True
    for z in range(nv):
        pr = [y for y in range(nv) if (y, z) in A]
        for y in pr:
            for y1 in pr:
                for i in range(r):
                    if bool(fib[(y, i)]) != bool(fib[(y1, i)]): q2 = False
    P["Q2"] = bool(q2)
    # U(D), U(D')
    def inU(nvv, sc, j):
        ch = G.chi[j]; E = G.E
        prd = {}
        for y in range(nvv):
            for (z, a) in sc[y]: prd.setdefault(z, []).append((y, ch[a]))
        acc = {}
        for z, lst in prd.items():
            for (y, ey) in lst:
                for (y1, e1) in lst:
                    if y < y1:
                        h = acc.setdefault((y, y1), np.zeros(E, dtype=np.int64)); h[(e1 - ey) % E] += 1
        return all(not red(G, h).any() for h in acc.values())
    U = [j for j in range(nC) if inU(nv, succ, j)]
    Up = [j for j in range(nC) if inU(len(Vp), succp, j)]
    rest = lambda j: tuple(G.chi[j][g] for g in C0l)
    P["U1"] = bool(set(U) == set(Up) and
                   all((rest(j) == rest(k)) <= ((j in Up) == (k in Up)) for j in range(nC) for k in range(nC)))
    perp = [j for j in range(nC) if all(e == 0 for e in rest(j))]
    P["U2"] = bool(not set(U) & set(perp))
    rec["U"] = [list(G.chars[j]) for j in U]; rec["perp_order"] = len(perp)
    cls = {}
    for j in U:
        key = frozenset({rest(j), tuple((-e) % G.E for e in rest(j))})
        cls.setdefault(key, j)
    reps = list(cls.values())
    predicted = 1 + len(reps)
    rec["predicted_dim"] = predicted; rec["naive_dim"] = 1 + len({frozenset({j, G.idx[tuple((-a) % n for a, n in zip(G.chars[j], ns))]}) for j in U})
    # PER
    if r == r0:
        P["PER"] = bool(len(C0) == nC and all(len(S) in (0, nC) for S in fib.values())
                        and (r == 1 or all(any(not fib[(y, i)] for y in range(nv)) for i in range(r))))
    if not heavy:
        rec["skipped_heavy"] = True; return rec
    # law system on D, class-supported families
    supports = [[fib[(y, i)] for i in range(r) if fib[(y, i)]] for y in range(nv)]
    pools = [[(y, g) for y in range(nv) for g in sorted(fib[(y, i)])] for i in range(r)]
    try:
        unk, rows = law_system(nv, succ, G.mul, supports, pools, d)
    except KeyError:
        P["DIM"] = False; rec["meas"]["note"] = "w_z not fibre supported"; return rec
    ncol = len(unk); M = np.array(rows, dtype=np.int64)
    rk = rank_mod(rows, ncol); dim_ub = ncol - rk
    rec["meas"].update(unknowns=ncol, equations=len(rows), rank_mod_p=rk)
    keys = sorted(unk, key=unk.get)
    def sq_hist(j, k, t=0):
        """hist of zeta^t * sigma_j(m) * conj sigma_k(m) for each unknown"""
        Hh = np.zeros((ncol, G.E), dtype=np.int64)
        for (y, m), c in unk.items():
            for g in m:
                for h in m: Hh[c, (t + G.chi[j][g] - G.chi[k][h]) % G.E] += 1
        return Hh
    cnt_vec = np.array([[len(m)] + [0] * (G.deg - 1) for (y, m) in keys], dtype=np.int64)
    basis = [cnt_vec] + [red(G, sq_hist(j, j)) for j in reps]
    P["SOL"] = bool(all(not (M @ F).any() for F in basis))
    ind = rank_Z([list(F.flatten()) for F in basis])
    P["IND"] = bool(ind == predicted)
    if dim_ub != predicted or not (P["SOL"] and P["IND"]):
        rkz = rank_Z(rows); rec["meas"]["rank_Z"] = rkz; dim = ncol - rkz
    else:
        dim = predicted
    rec["dim"] = dim
    P["DIM"] = bool(dim == predicted)
    in0 = np.array([1 if set(m) <= fib[(y, 0)] else 0 for (y, m) in keys], dtype=np.int64)[:, None]
    atx = np.array([1 if y == x0 else 0 for (y, m) in keys], dtype=np.int64)[:, None]
    if r > 1:
        P["NC"] = bool(all((M @ (F * in0)).any() for F in basis))
    P["NV"] = bool((M @ (cnt_vec * atx)).any())
    # A
    okA = True
    for j in range(nC):
        for k in range(j + 1, nC):
            if rest(j) == rest(k) or rest(j) == tuple((-e) % G.E for e in rest(k)):
                if (red(G, sq_hist(j, j)) != red(G, sq_hist(k, k))).any(): okA = False
    P["A"] = bool(okA)
    # DP
    if N <= 32:
        unk2, rows2 = law_system(len(Vp), succp, G.mul, [[C0] for _ in Vp], [[(v, h) for v in range(len(Vp)) for h in C0l]], d)
        dimp = len(unk2) - rank_mod(rows2, len(unk2))
        clsp = {frozenset({rest(j), tuple((-e) % G.E for e in rest(j))}) for j in Up}
        rec["meas"]["Dprime_dim_mod_p"] = dimp
        P["DP"] = bool(dimp == 1 + len(clsp))
    # C2
    if nC <= 8:
        okC = True; nfree = 0
        q = G.E // 4
        for j in range(nC):
            for k in range(nC):
                if j == k: continue
                Fs = []
                for t in (0, q):
                    Hh = sq_hist(j, k, t)
                    Hc = Hh[:, [(-e) % G.E for e in range(G.E)]]
                    Fs.append(red(G, Hh + Hc))  # = 2 Re(c sigma_j conj sigma_k)
                rr = [list((M @ F).flatten()) for F in Fs]
                ff = [list((M @ F).flatten()) + list(F.flatten()) for F in Fs]
                a_, b_ = rank_Z(rr), rank_Z(ff)
                if a_ != b_: okC = False
                if a_ < 2: nfree += 1
        P["C2"] = bool(okC); rec["meas"]["C2_pairs_with_consistent_nonzero_c"] = nfree
    return rec

# ---------------------------------------------------------------- carriers
def ring(Nn):
    V = lambda x, s: 2 * (x % Nn) + s  # s=0 R, 1 L
    arcs = []
    for x in range(Nn):
        for s in (0, 1):
            arcs.append((V(x, s), V(x + 1, 0), (0,)))
            arcs.append((V(x, s), V(x - 1, 1), (1,) if s == 1 else (0,)))
    return (2,), 2 * Nn, arcs

def block(ns, Bm, scale, k, rng=None):
    """cycle of length k tensor block: vertices (p,a); arc (p,a)->(p+1,b) with gain scale*Bm[b][a]; random switching"""
    dd = len(Bm); nv = k * dd
    add = lambda x, y: tuple((a + b) % n for a, b, n in zip(x, y, ns))
    neg = lambda x: tuple((-a) % n for a, n in zip(x, ns))
    sw = [tuple(rng.randrange(n) for n in ns) if rng else tuple(0 for _ in ns) for _ in range(nv)]
    arcs = []
    for p in range(k):
        for a in range(dd):
            for bb in range(dd):
                y = p * dd + a; z = ((p + 1) % k) * dd + bb
                arcs.append((y, z, add(add(add(scale, Bm[bb][a]), sw[z]), neg(sw[y]))))
    return ns, nv, arcs

def rand_carrier(rng, ns, nv, d, parts, grade):
    """random d-out digraph, vertices in `parts` cyclic layers, gain = grade + random element"""
    lay = [v % parts for v in range(nv)]
    arcs = []
    for y in range(nv):
        cand = [z for z in range(nv) if lay[z] == (lay[y] + 1) % parts]
        if len(cand) < d: return None
        for z in rng.sample(cand, d):
            g = tuple((rng.randrange(n) * s + t) % n for n, s, t in zip(ns, grade[0], grade[1]))
            arcs.append((y, z, g))
    return ns, nv, arcs

def main():
    rng = random.Random(SEED)
    L = []
    L.append(("ring4",) + ring(4)); L.append(("ring6",) + ring(6)); L.append(("ring8",) + ring(8))
    L.append(("ring3_odd",) + ring(3))
    H2 = lambda z, m: [[z, z], [z, m]]
    L.append(("ex_zeta8_H",) + block((8,), H2((0,), (4,)), (1,), 1))
    L.append(("ex_C2xC2",) + block((2, 2), H2((0, 0), (0, 1)), (1, 0), 1))
    four = [(0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 3), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 3, 3)]
    L.append(("ex_four_src_tgt", (4,), 4, [(a, b_, (e,)) for a, b_, e in four]))
    L.append(("ex_four_tgt_src", (4,), 4, [(b_, a, (e,)) for a, b_, e in four]))
    F3 = lambda u: [[tuple(0 for _ in u)] * 3, [tuple(0 for _ in u), u, tuple(2 * x for x in u)], [tuple(0 for _ in u), tuple(2 * x for x in u), tuple(4 * x for x in u)]]
    F3m = lambda ns, u: [[tuple(x % n for x, n in zip(e, ns)) for e in row] for row in F3(u)]
    specs = [((2,), H2((0,), (1,)), (0,)), ((2,), H2((0,), (1,)), (1,)),
             ((4,), H2((0,), (2,)), (1,)), ((4,), H2((0,), (2,)), (0,)),
             ((8,), H2((0,), (4,)), (1,)), ((8,), H2((0,), (4,)), (2,)),
             ((2, 2), H2((0, 0), (0, 1)), (1, 0)), ((2, 2), H2((0, 0), (0, 1)), (0, 0)), ((2, 2), H2((0, 0), (1, 1)), (1, 0)),
             ((4, 2), H2((0, 0), (2, 0)), (1, 1)), ((4, 2), H2((0, 0), (0, 1)), (1, 0)),
             ((3,), F3m((3,), (1,)), (0,)), ((3,), F3m((3,), (1,)), (1,)),
             ((9,), F3m((9,), (3,)), (1,)), ((3, 3), F3m((3, 3), (0, 1)), (1, 0)),
             ((6,), H2((0,), (3,)), (1,)), ((6,), H2((0,), (3,)), (2,)), ((6,), F3m((6,), (2,)), (1,)),
             ((4,), [[(0,), (0,)], [(1,), (3,)]], (0,)), ((4,), [[(0,), (0,)], [(1,), (3,)]], (1,))]
    for si, (ns, Bm, sc) in enumerate(specs):
        for k in (1, 2, 3):
            L.append(("blk%d_k%d" % (si, k),) + block(ns, Bm, sc, k))
            if k > 1: L.append(("blk%d_k%d_sw" % (si, k),) + block(ns, Bm, sc, k, rng))
    rspecs = [((2,), 4, 2, 2, ((1,), (0,))), ((2,), 6, 2, 3, ((1,), (0,))), ((2,), 6, 3, 2, ((1,), (0,))),
              ((4,), 4, 2, 2, ((1,), (0,))), ((4,), 4, 2, 1, ((2,), (1,))), ((4,), 6, 2, 2, ((2,), (1,))),
              ((4,), 5, 2, 1, ((2,), (1,))), ((2, 2), 4, 2, 2, ((1, 1), (0, 0))), ((2, 2), 4, 2, 1, ((0, 1), (1, 0))),
              ((2, 2), 6, 2, 2, ((0, 1), (1, 0))), ((6,), 4, 2, 1, ((3,), (1,))), ((6,), 4, 2, 1, ((2,), (1,))),
              ((8,), 3, 2, 1, ((4,), (1,))), ((4,), 6, 3, 2, ((1,), (0,))), ((3,), 6, 2, 3, ((1,), (0,)))]
    for ri, (ns, nv, d, parts, grade) in enumerate(rspecs):
        for t in range(4):
            c = rand_carrier(rng, ns, nv, d, parts, grade)
            if c: L.append(("rand%d_%d" % (ri, t),) + c)
    recs = []
    for (name, ns, nv, arcs) in L:
        nC = int(np.prod(ns)); N = nv * nC
        heavy = N <= 72
        if N > 200:
            recs.append({"name": name, "H": None, "why": "skipped: size %d" % N}); continue
        rec = analyse(name, ns, nv, arcs, heavy=heavy)
        recs.append(rec)
        print(name, "H=%s" % rec["H"], {k: rec.get(k) for k in ("r", "r0", "predicted_dim", "naive_dim", "dim")},
              "FAIL:" + ",".join(k for k, v in rec.get("pred", {}).items() if not v), flush=True)
    q = [r for r in recs if r.get("H")]
    summ = {"seed": SEED, "generated": len(recs), "qualifying": len(q),
            "qualifying_r_gt_1": sum(1 for r in q if r["r"] > 1),
            "qualifying_r_ne_r0": sum(1 for r in q if r["r"] != r["r0"]),
            "with_dim_computed": sum(1 for r in q if "dim" in r),
            "predicted_lt_naive": sum(1 for r in q if r["predicted_dim"] < r["naive_dim"]),
            "pred_counts": {}}
    for r in q:
        for k, v in r["pred"].items():
            c = summ["pred_counts"].setdefault(k, [0, 0]); c[0 if v else 1] += 1
    print(json.dumps(summ, indent=1))
    with open(OUT, "x") as f:
        json.dump({"summary": summ, "records": recs}, f, indent=1, default=str)

if __name__ == "__main__":
    main()
