#!/usr/bin/env python3
"""Exploration for the vertex-dependent global law (prints freely; no predicates).

Law:  sum_z F_z( sum_{y->z} A_zy . m_y ) = d sum_y F_y(m_y),  F_y(0)=0.
For each carrier prints: dimension of the truncated solution space for N=2 (exact,
over Q) and N=3,4 (mod two primes), and the dimension predicted from characters.
"""
import itertools, random, sys, time
from flint import fmpz_mat, nmod_mat

P1, P2 = 1000003, 998244353

class Group:
    def __init__(s, name):
        s.name = name
        if name == 'C2xC2':
            s.n, s.e = 4, 2
            s.mul = [[a ^ b for b in range(4)] for a in range(4)]
            s.chi = [[bin(j & h).count('1') % 2 for h in range(4)] for j in range(4)]
        else:
            n = int(name[1:]); s.n = s.e = n
            s.mul = [[(a + b) % n for b in range(n)] for a in range(n)]
            s.chi = [[(j * h) % n for h in range(n)] for j in range(n)]
        s.inv = [[b for b in range(s.n) if s.mul[a][b] == 0][0] for a in range(s.n)]
        s.chinv = [[j2 for j2 in range(s.n) if all((s.chi[j][h] + s.chi[j2][h]) % s.e == 0 for h in range(s.n))][0] for j in range(s.n)]

class Carrier:
    def __init__(s, name, G, nV, arcs, d):
        s.name, s.G, s.nV, s.arcs, s.d = name, G, nV, dict(arcs), d
        s.succ = [[z for z in range(nV) if (y, z) in s.arcs] for y in range(nV)]
        s.pred = [[y for y in range(nV) if (y, z) in s.arcs] for z in range(nV)]
        assert all(len(x) == d for x in s.succ), name

def system(c, N):
    """rows of the law for all inputs of total size 1..N; unknowns (y, multiset)."""
    G = c.G; idx = {}
    for y in range(c.nV):
        for n in range(1, N + 1):
            for m in itertools.combinations_with_replacement(range(G.n), n):
                idx[(y, m)] = len(idx)
    rows = set()
    pairs = [(y, h) for y in range(c.nV) for h in range(G.n)]
    for n in range(1, N + 1):
        for inp in itertools.combinations_with_replacement(pairs, n):
            row = {}
            my = {}
            for y, h in inp: my.setdefault(y, []).append(h)
            for y, m in my.items():
                k = idx[(y, tuple(m))]; row[k] = row.get(k, 0) - c.d
            for z in range(c.nV):
                w = sorted(G.mul[c.arcs[(y, z)]][h] for y in c.pred[z] if y in my for h in my[y])
                if w:
                    k = idx[(z, tuple(w))]; row[k] = row.get(k, 0) + 1
            rows.add(tuple(sorted(row.items())))
    return sorted(rows), idx

def dense(rows, ncols):
    M = [[0] * ncols for _ in rows]
    for i, r in enumerate(rows):
        for k, v in r: M[i][k] = v
    return M

def dim_exact(c, N):
    rows, idx = system(c, N)
    return len(idx) - fmpz_mat(dense(rows, len(idx))).rank()

def dim_modp(c, N):
    rows, idx = system(c, N)
    M = dense(rows, len(idx))
    return tuple(len(idx) - nmod_mat(M, p).rank() for p in (P1, P2))

# ---- cyclotomic companion matrices -------------------------------------------------
COMP = {1: [[1]], 2: [[-1]], 3: [[0, -1], [1, -1]], 4: [[0, -1], [1, 0]]}
def mmul(a, b): return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def zpow(e, k):
    f = len(COMP[e]); r = [[int(i == j) for j in range(f)] for i in range(f)]
    for _ in range(k % e): r = mmul(r, COMP[e])
    return r

def nullity_K(e, eqs, nvar):
    """eqs: list of dict var -> dict exponent -> integer coefficient (element of Z[zeta_e])."""
    f = len(COMP[e]); pw = [zpow(e, k) for k in range(e)]
    M = []
    for eq in eqs:
        blk = [[0] * (nvar * f) for _ in range(f)]
        for v, el in eq.items():
            for k, co in el.items():
                for i in range(f):
                    for j in range(f): blk[i][v * f + j] += co * pw[k][i][j]
        M.extend(blk)
    if not M: return nvar
    nq = nvar * f - fmpz_mat(M).rank()
    assert nq % f == 0
    return nq // f

def add(el, k, co): el[k] = el.get(k, 0) + co

def lin_char(c, j):
    G = c.G; eqs = []
    for y in range(c.nV):
        eq = {}
        for z in c.succ[y]: add(eq.setdefault(z, {}), G.chi[j][c.arcs[(y, z)]], 1)
        add(eq.setdefault(y, {}), 0, -c.d); eqs.append(eq)
    return nullity_K(G.e, eqs, c.nV)

def quad_char(c, j, k):
    G = c.G; eqs = []
    for y in range(c.nV):
        for y2 in range(c.nV):
            eq = {}
            for z in c.succ[y]:
                if (y2, z) in c.arcs:
                    add(eq.setdefault(z, {}), (G.chi[j][c.arcs[(y, z)]] + G.chi[k][c.arcs[(y2, z)]]) % G.e, 1)
            if y == y2: add(eq.setdefault(y, {}), 0, -c.d)
            if eq: eqs.append(eq)
    return nullity_K(G.e, eqs, c.nV)

def predicted(c):
    n = c.G.n
    lin = sum(lin_char(c, j) for j in range(n))
    quad = sum(quad_char(c, j, k) for j in range(n) for k in range(j, n))
    return lin, quad

# ---- combinatorics -----------------------------------------------------------------
def reach(c, y):
    seen = {y}; st = [y]
    while st:
        u = st.pop()
        for z in c.succ[u]:
            if z not in seen: seen.add(z); st.append(z)
    return seen

def terminal_classes(c):
    R = [reach(c, y) for y in range(c.nV)]
    out = []
    for y in range(c.nV):
        if all(y in R[z] for z in R[y]) and min(R[y]) == y: out.append(sorted(R[y]))
    return out

def closed_gains(c, T):
    """gains of the closed walks of positive length through T[0] (by definition)."""
    b = T[0]; seen = set(); st = [(b, 0)]; first = True
    while st:
        u, g = st.pop()
        for z in c.succ[u]:
            s = (z, c.G.mul[c.arcs[(u, z)]][g])
            if s not in seen: seen.add(s); st.append(s)
    return sorted(g for (v, g) in seen if v == b)

def lin_comb(c):
    return sum(c.G.n // len(closed_gains(c, T)) for T in terminal_classes(c))

def zero_sum(e, exps):
    n = [0] * e
    for k in exps: n[k % e] += 1
    if e == 1: return n[0] == 0
    if e == 2: return n[0] == n[1]
    if e == 3: return n[0] == n[1] == n[2]
    if e == 4: return n[0] == n[2] and n[1] == n[3]

def in_U(c, j):
    G = c.G
    for y in range(c.nV):
        for y2 in range(y + 1, c.nV):
            ex = [(G.chi[j][c.arcs[(y, z)]] - G.chi[j][c.arcs[(y2, z)]]) % G.e for z in c.succ[y] if (y2, z) in c.arcs]
            if not zero_sum(G.e, ex): return False
    return True

# ---- carriers ----------------------------------------------------------------------
def block(name, G, B):
    d = len(B)
    return Carrier(name, G, d, {(y, z): B[z][y] for y in range(d) for z in range(d)}, d)

def ring(n):
    G = Group('C2'); arcs = {}
    R = lambda x: 2 * (x % n); L = lambda x: 2 * (x % n) + 1
    for x in range(n):
        arcs[(R(x), R(x + 1))] = 0; arcs[(R(x), L(x - 1))] = 0
        arcs[(L(x), R(x + 1))] = 0; arcs[(L(x), L(x - 1))] = 1
    return Carrier('ring%d' % n, G, 2 * n, arcs, 2)

def union(name, c1, c2):
    arcs = dict(c1.arcs)
    for (y, z), g in c2.arcs.items(): arcs[(y + c1.nV, z + c1.nV)] = g
    return Carrier(name, c1.G, c1.nV + c2.nV, arcs, c1.d)

def with_source(name, c, targets, gains):
    arcs = dict(c.arcs)
    for z, g in zip(targets, gains): arcs[(c.nV, z)] = g
    return Carrier(name, c.G, c.nV + 1, arcs, c.d)

def rand_carrier(rng, gname, nV, d):
    G = Group(gname); arcs = {}
    for y in range(nV):
        for z in rng.sample(range(nV), d): arcs[(y, z)] = rng.randrange(G.n)
    return Carrier('rand_%s_V%d_d%d_%06d' % (gname, nV, d, rng.randrange(10**6)), G, nV, arcs, d)

def structured():
    C2, C3, C4, K = Group('C2'), Group('C3'), Group('C4'), Group('C2xC2')
    H2 = block('B_2 (Hadamard) C2', C2, [[0, 0], [0, 1]])
    B4 = block('B_4 [[1,i],[1,-i]] C4', C4, [[0, 1], [0, 3]])
    J2 = block('all-ones C2', C2, [[0, 0], [0, 0]])
    N4 = block('non-norm [[1,i],[1,1]] C4', C4, [[0, 1], [0, 0]])
    F3 = block('Fourier3 C3', C3, [[0, 0, 0], [0, 1, 2], [0, 2, 1]])
    HK = block('H2 in C2xC2 [[1,a],[1,ab]]', K, [[0, 1], [0, 3]])
    out = [H2, B4, J2, N4, F3, HK, ring(3), ring(4),
           union('H2+H2', H2, H2), union('H2+J2', H2, J2), union('B4+N4', B4, N4), union('B4+B4', B4, B4),
           with_source('H2+source', H2, [0, 1], [0, 0]), with_source('H2+source(-)', H2, [0, 1], [0, 1]),
           with_source('B4+source', B4, [0, 1], [1, 2]), with_source('F3+source', F3, [0, 1, 2], [0, 1, 1]),
           with_source('H2+H2+source across', union('u', H2, H2), [0, 2], [0, 0])]
    # in-degree one: 0->{1,2}, 1->{0,2}, 2->{0,2}: vertex 1 has the single predecessor 0
    for G in (C2, C4):
        out.append(Carrier('indeg1 %s' % G.name, G, 3, {(0, 1): 0, (0, 2): 1, (1, 0): 0, (1, 2): 0, (2, 0): 1 % G.n, (2, 2): G.n - 1}, 2))
    # chain of in-degree-one vertices feeding a Hadamard block
    out.append(Carrier('H2 + tail', C2, 4, {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1, (2, 0): 0, (2, 1): 0, (3, 2): 0, (3, 0): 1}, 2))
    return out

if __name__ == '__main__':
    rng = random.Random(20261113)
    cs = structured()
    for gname in ('C2', 'C3', 'C4', 'C2xC2'):
        for nV in (2, 3, 4, 5, 6):
            for d in (2, 3):
                if d <= nV:
                    for _ in range(2): cs.append(rand_carrier(rng, gname, nV, d))
    bad = 0
    for c in cs:
        t = time.time()
        lin, quad = predicted(c); lc = lin_comb(c)
        d2 = dim_exact(c, 2); d3 = dim_modp(c, 3)
        size = c.nV * c.G.n
        d4 = dim_modp(c, 4) if size <= 16 else None
        T = terminal_classes(c); sc = len(T) == 1 and len(T[0]) == c.nV
        gam = [len(closed_gains(c, t_)) for t_ in T]
        U = [j for j in range(c.G.n) if in_U(c, j)]
        indeg = sorted(len(p) for p in c.pred)
        ok = (d2 == lin + quad and lin == lc and d3 == (d2, d2) and (d4 is None or d4 == (d2, d2)))
        bad += not ok
        print('%-34s |V|=%d d=%d indeg=%s  lin=%d(comb %d) quad=%d  N2=%d N3=%s N4=%s  sc=%s |Gam|=%s U=%s %s %.1fs' % (
            c.name, c.nV, c.d, indeg, lin, lc, quad, d2, d3, d4, sc, gam, U, 'OK' if ok else '***MISMATCH***', time.time() - t))
        sys.stdout.flush()
    print('carriers', len(cs), 'mismatches', bad)
