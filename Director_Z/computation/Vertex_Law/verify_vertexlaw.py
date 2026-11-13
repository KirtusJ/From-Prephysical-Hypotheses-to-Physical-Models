#!/usr/bin/env python3
"""Verification program for Theorem thm:vertexlaw (vertex-dependent global law).

Law (GL):  sum_z F_z( sum_{y->z} A_zy . m_y ) = d sum_y F_y(m_y)  for all (m_y) in M^V,
F_y: M -> R with F_y(0)=0, M = N[C], C finite abelian.

PREDICATES (fixed before the first run of this program; written after explore.py).
Carriers: C in {C2, C3, C4, C2xC2}; the fixed list of structured carriers and the
random carriers produced by seed 4711 below.  Arithmetic: ranks over Q are exact
(fmpz_mat.rank); characters are handled exactly in Z[zeta_e] through companion matrices.

 H0 (hypothesis of the theorem, tested per carrier): at most one arc y->z for each pair,
    every vertex has exactly d >= 2 outgoing arcs.  Reported: number qualifying.  All
    other predicates are evaluated on the qualifying carriers only.
 Q1 dim2 = LIN + QUAD, where dim2 is the exact nullity over Q of the law restricted to
    inputs of total size <= 2 (unknowns: values on multisets of size 1, 2 at each vertex),
    LIN  = sum_psi nullity( A^(psi)T - d ),
    QUAD = sum over unordered pairs {psi,lambda} of the nullity of
           c -> A^(psi)T diag(c) A^(lambda) - d diag(c),   c in K^V, K = Q(zeta_e).
 Q2 LIN = sum over terminal strongly connected classes T of |C| / |Gamma_T|, Gamma_T the
    set of gains of closed walks of positive length through a vertex of T.
 Q3 the nullity of the law restricted to total size <= 3, modulo each of the primes
    1000003 and 998244353, equals dim2.  (Nullity mod p >= nullity over Q >= number of
    independent polynomial solutions = dim2 by Step 2; so equality is a certificate.)
 Q4 the same for total size <= 4, on the carriers with |V||C| <= 16 (number reported).
 Q5 (hypothesis tested per carrier: D strongly connected and Gamma = C; number reported)
    dim2 = 1 + number of classes {psi, psi^-1} contained in U,
    U = {psi : A^(psi)* A^(psi) = d}, and LIN = 1.
 Q6 for every carrier and every psi in U, the family F_y = |sigma_psi|^2 (all y), and the
    family F_y = |m|, satisfy (GL) exactly on 30 random inputs of total size 1..12.
 Q7 every vector of a basis of the rational solutions of the size <= 2 system, extended
    to the polynomials P_y of Step 2, satisfies (GL) exactly on 20 random inputs of total
    size 3..8.
 Q8 counterexamples (not carriers of the theorem):
    (a) one vertex with two parallel loops of gain 1 (d=2): the law is F(2m)=2F(m); the
        function F(m)=|m| if m = 2^k e_h for some k>=0 and h, else 0, satisfies it for all
        |m| <= 8 and has F(3e)-3F(2e)+3F(e) != 0, so it is not a polynomial of degree <= 2;
    (b) d = 1, one vertex with one loop of gain g != 1 in C2: F = n_0 n_1 (n_0+n_1)
        satisfies F(g.m) = F(m) for all |m| <= 8 and has a non-zero mixed third
        difference D_0 D_0 D_1 F at the empty multiset, so its degree exceeds two;
        (run 1 tested this by an ill-formed expression; the check was replaced, the
        predicate is unchanged, and the result of run 1 is kept as
        verify_vertexlaw_result_run1_superseded.json; all other results are identical)
    (c) two disjoint Hadamard blocks over C2: the family F_y = |sigma_psi|^2 on the first
        block and 0 on the second satisfies (GL) on 30 random inputs (weights depend on
        the vertex when D is not strongly connected);
    (d) a Hadamard block with one more vertex whose two arcs enter the block: QUAD = 0
        although the block alone has QUAD = 1.
 Fixed seed 4711.  The result file verify_vertexlaw_result.json is never overwritten.
 Failed predicates are kept in the result file under "failed".
"""
import itertools, json, os, random, sys
from flint import fmpz_mat, nmod_mat

PRIMES = (1000003, 998244353)
SEED = 4711
RESULT = 'verify_vertexlaw_result.json'

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
        s.ginv = [[b for b in range(s.n) if s.mul[a][b] == 0][0] for a in range(s.n)]
        s.chinv = [[k for k in range(s.n) if all((s.chi[j][h] + s.chi[k][h]) % s.e == 0 for h in range(s.n))][0] for j in range(s.n)]

class Carrier:
    """arcs: list of (y, z, gain); parallel arcs allowed here, H0 tests simplicity."""
    def __init__(s, name, G, nV, arcs, d):
        s.name, s.G, s.nV, s.d = name, G, nV, d
        s.arclist = sorted(arcs)
        s.out = [[(z, g) for (y2, z, g) in s.arclist if y2 == y] for y in range(nV)]
        s.inn = [[(y, g) for (y, z2, g) in s.arclist if z2 == z] for z in range(nV)]
        s.arcs = {(y, z): g for (y, z, g) in s.arclist}
        s.succ = [sorted(set(z for z, g in o)) for o in s.out]
    def h0(s):
        simple = len(s.arcs) == len(s.arclist)
        return simple and s.d >= 2 and all(len(o) == s.d for o in s.out)

def apply_law(c, my):
    """my: dict y -> list of group elements. returns dict z -> sorted tuple w_z (nonempty)."""
    out = {}
    for z in range(c.nV):
        w = sorted(c.G.mul[g][h] for (y, g) in c.inn[z] if y in my for h in my[y])
        if w: out[z] = tuple(w)
    return out

def system(c, N):
    G = c.G; idx = {}
    for y in range(c.nV):
        for n in range(1, N + 1):
            for m in itertools.combinations_with_replacement(range(G.n), n): idx[(y, m)] = len(idx)
    rows = set(); pairs = [(y, h) for y in range(c.nV) for h in range(G.n)]
    for n in range(1, N + 1):
        for inp in itertools.combinations_with_replacement(pairs, n):
            my = {}
            for y, h in inp: my.setdefault(y, []).append(h)
            row = {}
            for y, m in my.items():
                k = idx[(y, tuple(m))]; row[k] = row.get(k, 0) - c.d
            for z, w in apply_law(c, my).items():
                k = idx[(z, w)]; row[k] = row.get(k, 0) + 1
            rows.add(tuple(sorted(row.items())))
    return sorted(rows), idx

def dense(rows, ncols):
    M = [[0] * ncols for _ in rows]
    for i, r in enumerate(rows):
        for k, v in r: M[i][k] = v
    return M

COMP = {1: [[1]], 2: [[-1]], 3: [[0, -1], [1, -1]], 4: [[0, -1], [1, 0]]}
def mmul(a, b): return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def zpow(e, k):
    f = len(COMP[e]); r = [[int(i == j) for j in range(f)] for i in range(f)]
    for _ in range(k % e): r = mmul(r, COMP[e])
    return r
def nullity_K(e, eqs, nvar):
    f = len(COMP[e]); pw = [zpow(e, k) for k in range(e)]; M = []
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
        for z, g in c.out[y]: add(eq.setdefault(z, {}), G.chi[j][g], 1)
        add(eq.setdefault(y, {}), 0, -c.d); eqs.append(eq)
    return nullity_K(G.e, eqs, c.nV)

def quad_char(c, j, k):
    G = c.G; eqs = []
    for y in range(c.nV):
        for y2 in range(c.nV):
            eq = {}
            for z, g in c.out[y]:
                if (y2, z) in c.arcs: add(eq.setdefault(z, {}), (G.chi[j][g] + G.chi[k][c.arcs[(y2, z)]]) % G.e, 1)
            if y == y2: add(eq.setdefault(y, {}), 0, -c.d)
            if eq: eqs.append(eq)
    return nullity_K(G.e, eqs, c.nV)

def reach(c, y):
    seen = {y}; st = [y]
    while st:
        u = st.pop()
        for z in c.succ[u]:
            if z not in seen: seen.add(z); st.append(z)
    return seen
def terminal_classes(c):
    R = [reach(c, y) for y in range(c.nV)]
    return [sorted(R[y]) for y in range(c.nV) if all(y in R[z] for z in R[y]) and min(R[y]) == y]
def closed_gains(c, T):
    b = T[0]; seen = set(); st = [(b, 0)]
    while st:
        u, g = st.pop()
        for z, a in c.out[u]:
            s = (z, c.G.mul[a][g])
            if s not in seen: seen.add(s); st.append(s)
    return sorted(g for (v, g) in seen if v == b)

def is_zero(e, n):
    """n[k] integer coefficient of zeta_e^k; exact test of sum n[k] zeta^k = 0."""
    if e == 1: return n[0] == 0
    if e == 2: return n[0] == n[1]
    if e == 3: return n[0] == n[1] == n[2]
    if e == 4: return n[0] == n[2] and n[1] == n[3]
def in_U(c, j):
    G = c.G
    for y in range(c.nV):
        for y2 in range(y + 1, c.nV):
            n = [0] * G.e
            for z, g in c.out[y]:
                if (y2, z) in c.arcs: n[(G.chi[j][g] - G.chi[j][c.arcs[(y2, z)]]) % G.e] += 1
            if not is_zero(G.e, n): return False
    return True

def norm2(G, j, m):
    """|sigma_psi_j(m)|^2 as coefficient vector in Z[zeta_e]."""
    n = [0] * G.e
    for h in m:
        for h2 in m: n[(G.chi[j][h] - G.chi[j][h2]) % G.e] += 1
    return n

def rand_input(rng, c, lo, hi):
    my = {}
    for _ in range(rng.randint(lo, hi)): my.setdefault(rng.randrange(c.nV), []).append(rng.randrange(c.G.n))
    return {y: sorted(m) for y, m in my.items()}

def law_holds_norm(c, j, my, weight=None):
    e = c.G.e; tot = [0] * e
    for z, w in apply_law(c, my).items():
        wt = 1 if weight is None else weight[z]
        for k, v in enumerate(norm2(c.G, j, w)): tot[k] += wt * v
    for y, m in my.items():
        wt = 1 if weight is None else weight[y]
        for k, v in enumerate(norm2(c.G, j, m)): tot[k] -= wt * c.d * v
    return is_zero(e, tot)

def law_holds_count(c, my):
    return sum(len(w) for w in apply_law(c, my).values()) == c.d * sum(len(m) for m in my.values())

def poly_eval(G, val, y, m):
    """Step 2 polynomial with the values val[(y, multiset)] on sizes 1 and 2, at multiset m."""
    cnt = [0] * G.n
    for h in m: cnt[h] += 1
    a = [val[(y, (h,))] for h in range(G.n)]
    s = 0
    for h in range(G.n):
        s += a[h] * cnt[h]
        s += (val[(y, (h, h))] - 2 * a[h]) * (cnt[h] * (cnt[h] - 1) // 2)
        for k in range(h + 1, G.n): s += (val[(y, (h, k))] - a[h] - a[k]) * cnt[h] * cnt[k]
    return s

# ---- carriers ----------------------------------------------------------------------
def block(name, G, B):
    d = len(B)
    return Carrier(name, G, d, [(y, z, B[z][y]) for y in range(d) for z in range(d)], d)
def ring(n):
    G = Group('C2'); arcs = []
    R = lambda x: 2 * (x % n); L = lambda x: 2 * (x % n) + 1
    for x in range(n):
        arcs += [(R(x), R(x + 1), 0), (R(x), L(x - 1), 0), (L(x), R(x + 1), 0), (L(x), L(x - 1), 1)]
    return Carrier('ring%d' % n, G, 2 * n, arcs, 2)
def union(name, c1, c2):
    return Carrier(name, c1.G, c1.nV + c2.nV, c1.arclist + [(y + c1.nV, z + c1.nV, g) for (y, z, g) in c2.arclist], c1.d)
def with_source(name, c, targets, gains):
    return Carrier(name, c.G, c.nV + 1, c.arclist + [(c.nV, z, g) for z, g in zip(targets, gains)], c.d)
def switched(name, c, rng):
    G = c.G; pot = [rng.randrange(G.n) for _ in range(c.nV)]
    return Carrier(name, G, c.nV, [(y, z, G.mul[G.mul[pot[z]][g]][G.ginv[pot[y]]]) for (y, z, g) in c.arclist], c.d)
def rand_carrier(rng, gname, nV, d, tag):
    G = Group(gname); arcs = []
    for y in range(nV):
        for z in rng.sample(range(nV), d): arcs.append((y, z, rng.randrange(G.n)))
    return Carrier('rand_%s_V%d_d%d_%s' % (gname, nV, d, tag), G, nV, arcs, d)

def carriers(rng):
    C2, C3, C4, K = Group('C2'), Group('C3'), Group('C4'), Group('C2xC2')
    H2 = block('H2 C2', C2, [[0, 0], [0, 1]])
    B4 = block('B_4 [[1,i],[1,-i]] C4', C4, [[0, 1], [0, 3]])
    J2 = block('all-ones C2', C2, [[0, 0], [0, 0]])
    N4 = block('non-norm [[1,i],[1,1]] C4', C4, [[0, 1], [0, 0]])
    F3 = block('Fourier3 C3', C3, [[0, 0, 0], [0, 1, 2], [0, 2, 1]])
    HK = block('[[1,a],[1,ab]] C2xC2', K, [[0, 1], [0, 3]])
    H4 = block('Hadamard4 C2', C2, [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1], [0, 1, 1, 0]])
    HK4 = block('char table C2xC2 as gains', K, [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]])
    base = [H2, B4, J2, N4, F3, HK, H4, HK4, ring(3), ring(4)]
    out = list(base)
    out += [switched(c.name + ' switched', c, rng) for c in base]
    out += [union('H2+H2', H2, H2), union('H2+J2', H2, J2), union('B4+N4', B4, N4), union('B4+B4', B4, B4),
            union('HK+HK', HK, HK), union('ring3+H2', ring(3), H2), union('F3+F3', F3, F3),
            with_source('H2+source', H2, [0, 1], [0, 0]), with_source('H2+source(-)', H2, [0, 1], [0, 1]),
            with_source('B4+source', B4, [0, 1], [1, 2]), with_source('F3+source', F3, [0, 1, 2], [0, 1, 1]),
            with_source('H2+H2+source across', union('u', H2, H2), [0, 2], [0, 0]),
            with_source('ring3+source', ring(3), [0, 3], [0, 1])]
    for G in (C2, C3, C4, K):
        out.append(Carrier('indeg1 %s' % G.name, G, 3, [(0, 1, 0), (0, 2, 1), (1, 0, 0), (1, 2, 0), (2, 0, 1), (2, 2, G.n - 1)], 2))
    out.append(Carrier('H2 + tail', C2, 4, [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 1), (2, 0, 0), (2, 1, 0), (3, 2, 0), (3, 0, 1)], 2))
    n = 0
    for gname in ('C2', 'C3', 'C4', 'C2xC2'):
        for nV in (2, 3, 4, 5, 6):
            for d in (2, 3):
                if d <= nV:
                    for _ in range(3):
                        out.append(rand_carrier(rng, gname, nV, d, '%03d' % n)); n += 1
    # carriers that do not satisfy H0, kept to show that the hypothesis test acts
    out.append(Carrier('NOT-H0 parallel loops C2', C2, 1, [(0, 0, 0), (0, 0, 0)], 2))
    out.append(Carrier('NOT-H0 d=1 loop C2', C2, 1, [(0, 0, 1)], 1))
    return out

def main():
    if os.path.exists(RESULT):
        sys.exit('refusing to overwrite ' + RESULT)
    rng = random.Random(SEED)
    cs = carriers(rng)
    preds = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7']
    tested = {p: 0 for p in preds}; passed = {p: 0 for p in preds}; failed = []
    recs = []; nH0 = 0
    def note(p, c, ok, detail):
        tested[p] += 1; passed[p] += bool(ok)
        if not ok: failed.append({'predicate': p, 'carrier': c.name, 'detail': detail})
    for c in cs:
        G = c.G
        if not c.h0():
            recs.append({'name': c.name, 'H0': False}); continue
        nH0 += 1
        lins = [lin_char(c, j) for j in range(G.n)]; LIN = sum(lins)
        quads = {'%d,%d' % (j, k): quad_char(c, j, k) for j in range(G.n) for k in range(j, G.n)}
        QUAD = sum(quads.values())
        rows2, idx2 = system(c, 2); M2 = fmpz_mat(dense(rows2, len(idx2)))
        dim2 = len(idx2) - M2.rank()
        note('Q1', c, dim2 == LIN + QUAD, [dim2, LIN, QUAD])
        T = terminal_classes(c); gam = [len(closed_gains(c, t)) for t in T]
        comb = sum(G.n // x for x in gam)
        note('Q2', c, LIN == comb, [LIN, comb])
        rows3, idx3 = system(c, 3); D3 = dense(rows3, len(idx3))
        d3 = [len(idx3) - nmod_mat(D3, p).rank() for p in PRIMES]
        note('Q3', c, d3 == [dim2, dim2], [d3, dim2])
        d4 = None
        if c.nV * G.n <= 16:
            rows4, idx4 = system(c, 4); D4 = dense(rows4, len(idx4))
            d4 = [len(idx4) - nmod_mat(D4, p).rank() for p in PRIMES]
            note('Q4', c, d4 == [dim2, dim2], [d4, dim2])
        U = [j for j in range(G.n) if in_U(c, j)]
        sc = len(T) == 1 and len(T[0]) == c.nV
        full = sc and gam[0] == G.n
        if full:
            classes = len({frozenset((j, G.chinv[j])) for j in U})
            note('Q5', c, dim2 == 1 + classes and LIN == 1, [dim2, classes, LIN])
        ok6 = True
        for _ in range(30):
            my = rand_input(rng, c, 1, 12)
            ok6 &= law_holds_count(c, my) and all(law_holds_norm(c, j, my) for j in U)
        note('Q6', c, ok6, U)
        X, nul = M2.nullspace(); X = X.tolist(); inv = sorted(idx2, key=idx2.get); ok7 = nul == dim2
        for col in range(nul):
            val = {inv[i]: int(X[i][col]) for i in range(len(inv))}
            for _ in range(20):
                my = rand_input(rng, c, 3, 8)
                lhs = sum(poly_eval(G, val, z, w) for z, w in apply_law(c, my).items())
                rhs = c.d * sum(poly_eval(G, val, y, m) for y, m in my.items())
                ok7 &= lhs == rhs
        note('Q7', c, ok7, nul)
        recs.append({'name': c.name, 'H0': True, 'group': G.name, 'V': c.nV, 'd': c.d,
                     'indegrees': sorted(len(set(y for y, g in i)) for i in c.inn),
                     'arcs': [list(a) for a in c.arclist], 'LIN_by_character': lins, 'QUAD_by_pair': quads,
                     'dim2': dim2, 'dim3_mod_p': d3, 'dim4_mod_p': d4, 'terminal_classes': T, 'closed_gain_orders': gam,
                     'strongly_connected': sc, 'full': full, 'U': U})
    # ---- Q8 counterexamples ---------------------------------------------------------
    q8 = {}
    def Fa(m):
        if len(set(m)) != 1: return 0
        n = len(m)
        return n if n & (n - 1) == 0 else 0
    ok = all(Fa(m + m) == 2 * Fa(m) for n in range(1, 9) for m in itertools.combinations_with_replacement(range(2), n))
    q8['a_parallel_loops'] = bool(ok and Fa((0,) * 3) - 3 * Fa((0,) * 2) + 3 * Fa((0,)) != 0)
    Fb = lambda m: m.count(0) * m.count(1) * len(m)
    ok = all(Fb(tuple(sorted(1 - h for h in m))) == Fb(m) for n in range(1, 9) for m in itertools.combinations_with_replacement(range(2), n))
    # mixed third difference D_0 D_0 D_1 F at the empty multiset; zero for degree <= 2
    third = Fb((0, 0, 1)) - 2 * Fb((0, 1)) + Fb((1,)) - Fb((0, 0)) + 2 * Fb((0,)) - 0
    q8['b_d_equals_1'] = bool(ok and third != 0)
    byname = {c.name: c for c in cs}
    cu = byname['H2+H2']; ok = True
    for _ in range(30): ok &= law_holds_norm(cu, 1, rand_input(rng, cu, 1, 12), weight=[1, 1, 0, 0])
    q8['c_vertex_dependent_weights'] = bool(ok)
    rec = {r['name']: r for r in recs}
    q8['d_source_kills_square'] = (sum(rec['H2 C2']['QUAD_by_pair'].values()) == 1 and sum(rec['H2+source']['QUAD_by_pair'].values()) == 0
                                   and sum(rec['H2+source(-)']['QUAD_by_pair'].values()) == 0)
    for k, v in q8.items():
        if not v: failed.append({'predicate': 'Q8', 'carrier': k, 'detail': None})
    res = {'seed': SEED, 'primes': list(PRIMES), 'carriers_total': len(cs), 'carriers_qualifying_H0': nH0,
           'tested': tested, 'passed': passed, 'Q5_qualifying': tested['Q5'], 'Q4_qualifying': tested['Q4'],
           'Q8': q8, 'failed': failed,
           'summary': {'with_U_nonempty': sum(1 for r in recs if r.get('U')),
                       'strongly_connected': sum(1 for r in recs if r.get('strongly_connected')),
                       'with_vertex_of_one_or_no_predecessor': sum(1 for r in recs if r['H0'] and r['indegrees'][0] <= 1),
                       'dim2_values': sorted(set(r['dim2'] for r in recs if r['H0']))},
           'carriers': recs}
    with open(RESULT, 'x') as f: json.dump(res, f, indent=1, sort_keys=True)
    print(json.dumps({k: res[k] for k in ('carriers_total', 'carriers_qualifying_H0', 'tested', 'passed', 'Q8', 'failed', 'summary')}, indent=1))

if __name__ == '__main__':
    main()
