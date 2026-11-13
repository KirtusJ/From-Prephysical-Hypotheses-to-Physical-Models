"""Exploration for the periodic extension of G10 Corollary cor:vertexlaw (exact arithmetic, python-flint).

Core routines (also imported by verify_periodic.py) and a table for named carriers.

Setting: finite gain digraph D, gains in a finite abelian group C = Z/m1 x ... x Z/mk (written additively here),
at most one arc per ordered pair, d >= 2 outgoing arcs at every vertex, derived digraph Dhat on V x C strongly
connected with period r.  Cyclic classes X_0..X_{r-1}, X_0 containing (x0, 0).  Fibre S_i(y) = {g : (y,g) in X_i}.

Unknowns: values F_y(m) for the non-empty multisets m of size <= N supported on one fibre S_i(y).
Equations: sum_z F_z(w_z) = d sum_y F_y(m_y) for the families (m_y) of total size 1..N supported on one class X_i.
Conjectured dimension of the solution space: 1 + number of classes {psi', psi'^-1} of restrictions psi' = psi|C_0
of the characters psi in U(D) = {psi : A^(psi)* A^(psi) = d}, C_0 = S_0(x0).

Conventions: arcs are triples (from, to, gain index); A_zy is the gain of the arc y -> z; characters are index
tuples j with psi_j(g) = exp(2 pi i sum_k j_k g_k / m_k); a root of unity is stored as an exponent modulo
n = lcm(m_k), and an element of Z[zeta_n] as a list of n integer coefficients, tested for zero by reduction modulo
the n-th cyclotomic polynomial.  Rank: exact (fmpz_mat.rank).
"""
import itertools, sys
from math import gcd
from flint import fmpz_mat, fmpz_poly, nmod_mat

# ---------- groups ----------
class Group:
    def __init__(self, mods):
        self.mods = tuple(mods); self.elts = list(itertools.product(*[range(m) for m in mods]))
        self.idx = {e: i for i, e in enumerate(self.elts)}; self.order = len(self.elts)
        n = 1
        for m in mods: n = n * m // gcd(n, m)
        self.n = n
        self.chars = list(self.elts)  # same index tuples
    def add(self, a, b): return self.idx[tuple((x + y) % m for x, y, m in zip(self.elts[a], self.elts[b], self.mods))]
    def neg(self, a): return self.idx[tuple((-x) % m for x, m in zip(self.elts[a], self.mods))]
    def cexp(self, j, g):  # exponent of psi_j(g) modulo n
        return sum(jk * gk * (self.n // m) for jk, gk, m in zip(j, self.elts[g], self.mods)) % self.n

_cyc = {}
def cyclotomic(n):
    if n not in _cyc:
        p = fmpz_poly([-1] + [0] * (n - 1) + [1])
        for dd in range(1, n):
            if n % dd == 0: p = p // cyclotomic(dd)
        _cyc[n] = p
    return _cyc[n]
def cyc_zero(vec, n):
    if not any(vec): return True
    return (fmpz_poly(list(vec)) % cyclotomic(n)) == fmpz_poly([0]) or len(list(fmpz_poly(list(vec)) % cyclotomic(n))) == 0

# ---------- carriers ----------
class Carrier:
    def __init__(self, name, mods, nv, arcs):
        self.name, self.G, self.nv, self.arcs = name, Group(mods), nv, [tuple(a) for a in arcs]
        self.out = {y: [] for y in range(nv)}
        for y, z, g in self.arcs: self.out[y].append((z, g))

def ring(N):
    V = [(x, s) for x in range(N) for s in "RL"]; ix = {v: i for i, v in enumerate(V)}; arcs = []
    for (x, s) in V:
        arcs.append((ix[(x, s)], ix[((x + 1) % N, "R")], 0)); arcs.append((ix[(x, s)], ix[((x - 1) % N, "L")], 1 if s == "L" else 0))
    return Carrier(f"ring{N}", (2,), 2 * N, arcs)
def Bq(q): return Carrier(f"B{q}", (q,), 2, [(0, 0, 0), (0, 1, 0), (1, 0, 1), (1, 1, (1 + q // 2) % q)])
def four():  # the example after cor:abund, q = 4
    return Carrier("four", (4,), 4, [(0, 2, 0), (0, 3, 1), (1, 0, 1), (1, 1, 3), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 3, 3)])
def three():  # the three-vertex example after thm:vertexlaw (sign character qualifies for a block, not for the step)
    return Carrier("three", (2,), 3, [(0, 1, 0), (0, 2, 0), (1, 1, 0), (2, 0, 0), (2, 2, 0), (1, 2, 1)])
def block(name, mods, B):  # complete digraph with loops, B[z][y] = gain (tuple) of the arc y -> z
    G = Group(mods); k = len(B)
    return Carrier(name, mods, k, [(y, z, G.idx[tuple(B[z][y])]) for y in range(k) for z in range(k)])
def H1():
    o, a, b, c = (0, 0), (1, 0), (0, 1), (1, 1)
    return block("H1", (2, 2), [[o, o, o, o], [o, a, b, c], [o, b, c, a], [o, c, a, b]])
def H2():
    o, a, b, c = (0, 0), (1, 0), (0, 1), (1, 1)
    return block("H2", (2, 2), [[o, o, o, o], [o, o, a, a], [o, a, o, a], [o, a, a, b]])
def times_cycle(c, k):  # vertices (y, j), arcs (y, j) -> (z, j+1 mod k), same gains
    return Carrier(f"{c.name}xZ{k}", c.G.mods, c.nv * k,
                   [(y * k + j, z * k + (j + 1) % k, g) for (y, z, g) in c.arcs for j in range(k)])
def shift(c, u):  # multiply every gain by the group element with index u
    return Carrier(f"{c.name}+u{u}", c.G.mods, c.nv, [(y, z, c.G.add(g, u)) for (y, z, g) in c.arcs])

# ---------- structure ----------
def analyse(c, x0=0):
    """Returns None with a reason if a hypothesis fails, else a dict with r, r0, classes, fibres, C0."""
    G, nv, q = c.G, c.nv, c.G.order
    degs = {len(v) for v in c.out.values()}
    if len(degs) != 1: return None, "out-degrees differ"
    d = degs.pop()
    if d < 2: return None, "d < 2"
    if len({(y, z) for y, z, g in c.arcs}) != len(c.arcs): return None, "parallel arcs"
    succ = lambda u: [(z, G.add(u[1], g)) for z, g in c.out[u[0]]]
    start = (x0, 0); lev = {start: 0}; st = [start]
    while st:
        nxt = []
        for u in st:
            for w in succ(u):
                if w not in lev: lev[w] = lev[u] + 1; nxt.append(w)
        st = nxt
    if len(lev) != nv * q: return None, "Dhat not strongly connected (forward)"
    pred = {}
    for u in lev:
        for w in succ(u): pred.setdefault(w, []).append(u)
    seen = {start}; st = [start]
    while st:
        u = st.pop()
        for w in pred.get(u, []):
            if w not in seen: seen.add(w); st.append(w)
    if len(seen) != nv * q: return None, "Dhat not strongly connected (backward)"
    r = 0
    for u in lev:
        for w in succ(u): r = gcd(r, lev[u] + 1 - lev[w])
    lev0 = {x0: 0}; st = [x0]
    while st:
        u = st.pop()
        for w, _ in c.out[u]:
            if w not in lev0: lev0[w] = lev0[u] + 1; st.append(w)
    r0 = 0
    for u in lev0:
        for w, _ in c.out[u]: r0 = gcd(r0, lev0[u] + 1 - lev0[w])
    cls = {u: lev[u] % r for u in lev}
    for u in lev:
        for w in succ(u): assert cls[w] == (cls[u] + 1) % r
    fib = {(y, i): sorted(g for g in range(q) if cls[(y, g)] == i) for y in range(nv) for i in range(r)}
    C0 = fib[(x0, 0)]
    return dict(d=d, r=r, r0=r0, cls=cls, fib=fib, C0=C0), "ok"

def in_U(c, j):
    """A^(psi_j)* A^(psi_j) = d, exactly: for y != y' the sum over common successors of conj(psi(A_zy)) psi(A_zy') is 0."""
    G = c.G
    for y in range(c.nv):
        for y2 in range(y + 1, c.nv):
            vec = [0] * G.n; oy = dict(c.out[y])
            for z, g2 in c.out[y2]:
                if z in oy: vec[(G.cexp(j, g2) - G.cexp(j, oy[z])) % G.n] += 1
            if not cyc_zero(vec, G.n): return False
    return True

def restricted_classes(c, C0):
    """Classes {psi', psi'^-1} of restrictions to C0 of the characters in U(D); returns dict class -> list of characters."""
    G = c.G; out = {}
    for j in G.chars:
        if in_U(c, j):
            t = tuple(G.cexp(j, h) for h in C0); tn = tuple((-e) % G.n for e in t)
            out.setdefault(frozenset([t, tn]), []).append(j)
    return out

# ---------- the linear system ----------
def system(c, S, N):
    """Unknown columns (y, m) with m a sorted tuple supported on one fibre; equation rows as dicts col -> coefficient."""
    G, nv, d, r, fib = c.G, c.nv, S["d"], S["r"], S["fib"]
    cols = {}
    for y in range(nv):
        for i in range(r):
            for n in range(1, N + 1):
                for m in itertools.combinations_with_replacement(fib[(y, i)], n): cols[(y, m)] = len(cols)
    rows = []
    for i in range(r):
        nodes = [(y, g) for y in range(nv) for g in fib[(y, i)]]
        for n in range(1, N + 1):
            for fam in itertools.combinations_with_replacement(nodes, n):
                row = {}; my = {}; wz = {}
                for y, g in fam:
                    my.setdefault(y, []).append(g)
                    for z, a in c.out[y]: wz.setdefault(z, []).append(G.add(g, a))
                for z, w in wz.items():
                    k = cols[(z, tuple(sorted(w)))]; row[k] = row.get(k, 0) + 1
                for y, m in my.items():
                    k = cols[(y, tuple(sorted(m)))]; row[k] = row.get(k, 0) - d
                row = {k: v for k, v in row.items() if v}
                if row: rows.append(row)
    return cols, rows

def exact_rank(rows, ncols):
    uniq = sorted({tuple(sorted(r.items())) for r in rows})
    if not uniq: return 0
    M = [[0] * ncols for _ in uniq]
    for a, r in enumerate(uniq):
        for k, v in r: M[a][k] = v
    return fmpz_mat(M).rank()

def sq_value(G, j, m):
    """|sigma_psi_j(m)|^2 as a coefficient list in Z[zeta_n]."""
    vec = [0] * G.n; e = [G.cexp(j, g) for g in m]
    for a in e:
        for b in e: vec[(a - b) % G.n] += 1
    return vec

def satisfies(G, cols, rows, val):
    """val: dict col index -> coefficient list.  True if every equation holds exactly."""
    for r in rows:
        acc = [0] * G.n
        for k, v in r.items():
            for t, x in enumerate(val[k]):
                if x: acc[t] += v * x
        if not cyc_zero(acc, G.n): return False
    return True

def find_prime(n):
    p = 1000003
    while True:
        if (p - 1) % n == 0 and all(p % t for t in range(2, int(p ** 0.5) + 1)): return p
        p += 1
def prim_root(p, n):
    for a in range(2, p):
        z = pow(a, (p - 1) // n, p)
        if all(pow(z, n // t, p) != 1 for t in range(2, n + 1) if n % t == 0): return z
def indep_rank(G, vals, ncols):
    """Rank of the value vectors after zeta -> a primitive n-th root modulo a prime p = 1 mod n (a lower bound of the rank)."""
    p = find_prime(G.n); z = prim_root(p, G.n) if G.n > 1 else 1
    M = [[sum(x * pow(z, t, p) for t, x in enumerate(v[k])) % p for k in range(ncols)] for v in vals]
    return nmod_mat(M, p).rank()

def formula_functions(c, S, cols):
    G = c.G; cl = restricted_classes(c, S["C0"])
    one = [1] + [0] * (G.n - 1)
    vals = [{k: [len(m) * x for x in one] for (y, m), k in cols.items()}]
    names = ["count"]
    for key in sorted(cl, key=lambda s: sorted(s)):
        j = cl[key][0]
        vals.append({k: sq_value(G, j, m) for (y, m), k in cols.items()}); names.append("sq%s" % (j,))
    return names, vals, cl

def report(c, N=3):
    S, why = analyse(c)
    if S is None: return f"{c.name}: not qualifying ({why})"
    cols, rows = system(c, S, N)
    dim = len(cols) - exact_rank(rows, len(cols))
    names, vals, cl = formula_functions(c, S, cols)
    ok = all(satisfies(c.G, cols, rows, v) for v in vals)
    ind = indep_rank(c.G, vals, len(cols))
    nU = sum(len(v) for v in cl.values())
    return (f"{c.name}: C={c.G.mods} |V|={c.nv} d={S['d']} r={S['r']} r0={S['r0']} |C0|={len(S['C0'])} N={N} unknowns={len(cols)} "
            f"equations={len(rows)} dim={dim} formula={len(vals)} |U(D)|={nU} classes_of_U_in_hat_C={len({frozenset([j, tuple((-a) % m for a, m in zip(j, c.G.mods))]) for v in cl.values() for j in v})} "
            f"formula_functions_solve={ok} independent={ind == len(vals)}")

if __name__ == "__main__":
    L = [ring(3), ring(4), ring(6), Bq(2), Bq(4), Bq(8), four(), three(), H1(), H2(),
         times_cycle(Bq(2), 2), times_cycle(Bq(4), 2), times_cycle(Bq(4), 3), shift(Bq(4), 1), shift(Bq(8), 1),
         times_cycle(four(), 2), shift(four(), 1), shift(H1(), 1), shift(H2(), 3), times_cycle(H1(), 2),
         shift(Bq(8), 2), times_cycle(shift(Bq(8), 1), 2)]
    for c in L:
        print(report(c, 3)); sys.stdout.flush()
    for c in [ring(4), four(), Bq(4)]: print(report(c, 4))
