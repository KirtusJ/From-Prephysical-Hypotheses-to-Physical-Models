"""Shared helpers for review-queue programs (written by the queue session; reviewer side only).

Conventions: a carrier is a list E with E[z][y] = gain of the arc y -> z (None if no arc); gains are
elements of a finite abelian group written as tuples of exponents, group = tuple of moduli (q1, q2, ...);
a character is a tuple k with chi(g) = exp(2 pi i sum k_i g_i / q_i).  For cyclic groups use moduli (q,).
"""
import itertools, math, random
from fractions import Fraction as Fr
from sympy import cyclotomic_poly, Poly, symbols
_x = symbols('x'); _phi = {}

def gadd(a, b, mod): return tuple((u + v) % m for u, v, m in zip(a, b, mod))
def gneg(a, mod): return tuple((-u) % m for u, m in zip(a, mod))
def gsub(a, b, mod): return gadd(a, gneg(b, mod), mod)
def gzero(mod): return tuple(0 for _ in mod)
def group(mod): return list(itertools.product(*[range(m) for m in mod]))
def lcm(mod):
    l = 1
    for m in mod: l = l * m // math.gcd(l, m)
    return l
def chi_exp(k, g, mod):
    """exponent e (mod L = lcm) with chi_k(g) = zeta_L^e"""
    L = lcm(mod); return sum(ki * gi * (L // m) for ki, gi, m in zip(k, g, mod)) % L
def zero_sum(exps, q):
    """exact: is the sum of zeta_q^e over e in exps zero?"""
    co = [0] * q
    for e in exps: co[e % q] += 1
    if q not in _phi: _phi[q] = Poly(cyclotomic_poly(q, _x), _x)
    return Poly(co[::-1], _x).rem(_phi[q]).is_zero if any(co) else True
def norm_preserving(E, mod, k):
    """exact test of A*A = d for the character k; returns d or None"""
    n = len(E); L = lcm(mod)
    degs = {sum(1 for z in range(n) if E[z][y] is not None) for y in range(n)}
    if len(degs) != 1: return None
    for y1 in range(n):
        for y2 in range(y1 + 1, n):
            com = [chi_exp(k, gsub(E[z][y2], E[z][y1], mod), mod) for z in range(n) if E[z][y1] is not None and E[z][y2] is not None]
            if com and not zero_sum(com, L): return None
    return degs.pop()
def block_carrier(nodes, M, mod, rng, switch=True):
    """arc digraph of a random d-in d-out multidigraph on `nodes` nodes; at each node the d x d block of gains is
    rho_z + kappa_y + M[z][y] (group elements, additive notation) with random rho, kappa if switch."""
    d = len(M); perms = [list(range(nodes)) for _ in range(d)]
    for p in perms: rng.shuffle(p)
    arcs = [(i, p[i]) for p in perms for i in range(nodes)]
    n = len(arcs); E = [[None] * n for _ in range(n)]; G = group(mod)
    for node in range(nodes):
        ins = [a for a in range(n) if arcs[a][1] == node]; outs = [a for a in range(n) if arcs[a][0] == node]
        rho = [rng.choice(G) if switch else gzero(mod) for _ in range(d)]; kap = [rng.choice(G) if switch else gzero(mod) for _ in range(d)]
        for zi, z in enumerate(outs):
            for yi, y in enumerate(ins): E[z][y] = gadd(gadd(rho[zi], kap[yi], mod), M[zi][yi], mod)
    return E
def succ(E): 
    n = len(E); return [[z for z in range(n) if E[z][y] is not None] for y in range(n)]
def lift(E, mod):
    """D-hat: vertices (y, g); returns (vertex list, successor index lists)"""
    n = len(E); G = group(mod); idx = {(y, g): i for i, (y, g) in enumerate(itertools.product(range(n), G))}
    S = [[] for _ in idx]
    for (y, g), i in idx.items():
        for z in range(n):
            if E[z][y] is not None: S[i].append(idx[(z, gadd(g, E[z][y], mod))])
    return idx, S
def strongly_connected(S):
    n = len(S)
    def reach(adj):
        seen = {0}; st = [0]
        while st:
            v = st.pop()
            for u in adj[v]:
                if u not in seen: seen.add(u); st.append(u)
        return len(seen) == n
    R = [[] for _ in range(n)]
    for v in range(n):
        for u in S[v]: R[u].append(v)
    return reach(S) and reach(R)
def period(S):
    """period of a strongly connected digraph and the cyclic class of each vertex (class of vertex 0 is 0)"""
    n = len(S); lev = [None] * n; lev[0] = 0; st = [0]; g = 0
    while st:
        v = st.pop()
        for u in S[v]:
            if lev[u] is None: lev[u] = lev[v] + 1; st.append(u)
            else: g = math.gcd(g, lev[v] + 1 - lev[u])
    return g, [l % g for l in lev]
def walk_counts(S, start, L):
    """list over lengths 0..L of dict vertex -> number of walks from start"""
    cur = {start: 1}; out = [cur]
    for _ in range(L):
        nxt = {}
        for v, c in cur.items():
            for u in S[v]: nxt[u] = nxt.get(u, 0) + c
        cur = nxt; out.append(cur)
    return out

class Ring:
    """Z[zeta_q], exact; an element is a tuple of phi(q) integers."""
    def __init__(self, q):
        self.q = q; self.phi = [int(c) for c in Poly(cyclotomic_poly(q, _x), _x).all_coeffs()][::-1]
        self.n = len(self.phi) - 1
        self.J = [1] if q <= 2 else [j for j in range(1, (q + 1) // 2) if math.gcd(j, q) == 1]
        import cmath; self.z = cmath.exp(2j * math.pi / q)
        self.pw = [self._red([1 if i == k else 0 for i in range(q)]) for k in range(q)]
    def _red(self, co):
        co = list(co)
        for k in range(len(co) - 1, self.n - 1, -1):
            c = co[k]
            if c:
                for i in range(self.n + 1): co[k - self.n + i] -= c * self.phi[i]
        return tuple((co + [0] * self.n)[:self.n])
    def zero(self): return tuple([0] * self.n)
    def add(self, a, b): return tuple(u + v for u, v in zip(a, b))
    def neg(self, a): return tuple(-u for u in a)
    def mulz(self, a, k):
        out = [0] * self.n
        for i, c in enumerate(a):
            if c:
                p = self.pw[(i + k) % self.q]
                for t in range(self.n): out[t] += c * p[t]
        return tuple(out)
    def mul(self, a, b):
        out = self.zero()
        for i, c in enumerate(b):
            if c: out = self.add(out, tuple(c * v for v in self.mulz(a, i)))
        return out
    def conj(self, a):
        out = self.zero()
        for i, c in enumerate(a):
            if c: out = self.add(out, tuple(c * v for v in self.pw[(-i) % self.q]))
        return out
    def N(self, a): return self.mul(a, self.conj(a))
    def emb(self, a, j=1): return sum(c * self.z ** (j * i) for i, c in enumerate(a))
    def Nj(self, a, j): return abs(self.emb(a, j)) ** 2

def null_dim(M, gap=1e6):
    """dimension of the null space of a real matrix, decided by the largest relative gap of singular values;
    returns (dimension, gap ratio, smallest kept, largest dropped)."""
    import numpy as np
    sv = np.linalg.svd(M, compute_uv=False); sv = np.concatenate([sv, np.zeros(max(0, M.shape[1] - len(sv)))])
    o = np.sort(sv)[::-1]
    if o[0] == 0: return M.shape[1], float('inf'), 0.0, 0.0
    best = max(((o[i] / max(o[i + 1], 1e-300), i) for i in range(len(o) - 1) if o[i] > 0), default=(1.0, len(o) - 1))
    if best[0] < gap: return 0, float(best[0]), float(o[-1]), 0.0
    i = best[1]; return len(o) - (i + 1), float(best[0]), float(o[i]), float(o[i + 1])

# ---- added in the second working period ----
def ring_carrier(N):
    """signed arc digraph of a ring of N sites (G9/G10): vertex 2x+s, s=0 R, 1 L; gains in Z2 as (e,)"""
    n = 2 * N; E = [[None] * n for _ in range(n)]
    for x in range(N):
        for s in (0, 1):
            E[2 * ((x + 1) % N)][2 * x + s] = (0,)
            E[2 * ((x - 1) % N) + 1][2 * x + s] = (1,) if s == 1 else (0,)
    return E
def sign_carrier(M, q=2):
    """matrix with entries 0, +1, -1 (M[z][y]) -> carrier with gains in Z_q, q even"""
    return [[None if v == 0 else ((0,) if v == 1 else (q // 2,)) for v in row] for row in M]
W43 = [[0, 1, 1, 1], [-1, 0, 1, -1], [-1, -1, 0, 1], [-1, 1, -1, 0]]
C6 = [[0, 1, 1, 1, 1, 1], [1, 0, 1, -1, -1, 1], [1, 1, 0, 1, -1, -1], [1, -1, 1, 0, 1, -1], [1, -1, -1, 1, 0, 1], [1, 1, -1, -1, 1, 0]]
def event_rows(E, q, d, start, rng, n_events=400, maxlen=8, maxwalks=10, ring=None):
    """consistency equations mu(Ext S) = d mu(S) for random events from `start`, cyclic gains (e,) mod q.
    Returns (rows, keys): rows are dicts column -> integer coefficient, keys maps exact |v|^2 (tuple) -> column."""
    R = ring or Ring(q); sD = succ(E); keys = {}; rows = []
    def ix(k):
        if k not in keys: keys[k] = len(keys)
        return keys[k]
    for _ in range(n_events):
        Lw = rng.randrange(0, maxlen + 1); walks = set()
        for _ in range(rng.randrange(1, maxwalks + 1)):
            w = [start]
            for _ in range(Lw): w.append(rng.choice(sD[w[-1]]))
            walks.add(tuple(w))
        v = {}; ext = {}
        for w in walks:
            g = sum(E[w[i + 1]][w[i]][0] for i in range(Lw)) % q
            v[w[-1]] = R.add(v.get(w[-1], R.zero()), R.pw[g])
            for z in sD[w[-1]]: ext[z] = R.add(ext.get(z, R.zero()), R.pw[(g + E[z][w[-1]][0]) % q])
        row = {}
        for val in ext.values(): j = ix(R.N(val)); row[j] = row.get(j, 0) + 1
        for val in v.values(): j = ix(R.N(val)); row[j] = row.get(j, 0) - d
        rows.append(row)
    return rows, keys, R
def null_space(rows, ncols, zero_col=None):
    """null space of the integer system via eigenvalues of M^T M (below 1e-9 of the largest); returns (dim, basis)"""
    import numpy as np
    G = np.zeros((ncols, ncols))
    for row in rows:
        js = [j for j, v in row.items() if v]
        if js: vs = np.array([row[j] for j in js], float); G[np.ix_(js, js)] += np.outer(vs, vs)
    if zero_col is not None: G[zero_col, zero_col] += 1
    ev, U = np.linalg.eigh(G); dim = int((ev < 1e-9 * max(ev[-1], 1e-300)).sum()); return dim, U[:, :dim], ev
