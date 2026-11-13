#!/usr/bin/env python3
"""verify_multiset_abelian.py -- exact guard for the block law on multisets over
finite abelian groups (Theorem thm:multiset, abelian form) and exact evidence for
the non-abelian form on S_3.

THE LAW.  C a finite group, M = N[C] (count vectors), C acting by left translation,
B a d x d matrix with entries in C, d >= 2.  Unknowns: F(m) for every multiset m
of size <= N (the empty multiset included).  Equations: for every tuple
(m_1..m_d) with sum |m_y| <= N,
    sum_z F( sum_y B_zy . m_y ) - d sum_y F(m_y) = 0.
nullity(N) = number of unknowns minus the rank of this integer system.

PREDICATES (fixed before the first run; a failed predicate is kept in the result
file and gets a follow-up, it is not edited away).

Abelian instances (C given by moduli, dual group = tuples of residues):
 H0  hypothesis: d >= 2 and every entry lies in C.  Counted per matrix; the
     generated subgroup H and whether H = C are recorded.  Every other predicate
     is evaluated only on matrices that satisfy H0.
 P1  for every feasible N in {2,3,4}: nullity(N) modulo p1 equals
     DIM = |J_0| + #{unordered {psi,lam} : psi*lam in J_0, psi in U},
     where J_0 and U are computed from the characters alone, exactly
     (integer exponents; a sum of roots of unity is zero iff the cyclotomic
     polynomial divides the exponent polynomial).
 P2  the same modulo p2.
 P3  rational cross-check: for every (matrix, N) whose deduplicated system has
     rows*cols <= 3,000,000 (a cost limit, not a tolerance) the rank over Q
     (fmpz_mat.rank) equals the rank modulo p1.
 P4  explicit solutions: with a primitive e-th root of unity in F_p1 (p1 = 1 mod
     e, e the exponent of C) the vectors sigma_psi (psi in J_0) and
     sigma_psi*sigma_lam (the pairs of DIM) restricted to sizes <= N are
     annihilated by every equation and have rank DIM modulo p1.  (For N >= 2.
     Together with P1 the kernel modulo p1 is exactly their span.)
 P5  corollary: qualifies if H = C.  Then J_0 is trivial and
     DIM = 1 + #(U / (psi ~ psi^-1)).
 P6  structure of U: U = U^-1, U*J_0 = U, the trivial character is not in U,
     and membership in U depends only on the kernel of the character
     (equivalently U is closed under psi -> psi^j, gcd(j,e)=1).
 P7  second independent count (no characters): DIM = [C:H] + dim of the space
     of symmetric b on C x C with b(kg,kh)=b(g,h) for every entry k and
     sum_z b(g, B_zy^-1 B_zy' h) = 0 for y != y' (rank over Q).
 E1  cyclic example 1 of the corollary (q=6, d=3): U = {1,2,4,5}.
 E2  cyclic example 2 of the corollary (q=6, d=4): U = {1,3,5}.
 E3  C_2 x C_2, B = rows (1,1,1,1),(1,a,b,ab),(1,b,ab,a),(1,ab,a,b):
     entries generate C, U = all three non-trivial characters, DIM = 4.
 E4  C_2 x C_2, B = rows (1,1,1,1),(1,1,a,a),(1,a,1,a),(1,a,a,b):
     entries generate C, U = {the character with kernel {1,b}}, DIM = 2.

Non-abelian instances (C = S_3; irreducibles: trivial, sign, standard of
degree 2, all of real type):
 NA0 hypothesis: d >= 2, entries in S_3; H recorded.
 NA1 nullity(N) modulo p1 and modulo p2 is the same for every feasible N in
     {2,3,4} (solutions are determined by sizes <= 2 and every solution on
     sizes <= 2 extends).
 NA2 nullity(N) = [C:H] + dim of the b-space of P7, for every feasible N.
 NA3 qualifies if H = S_3: nullity(N) = 1 + sum over rho in U of
     d_rho(d_rho+1)/2, U = {rho irreducible : sum_z rho(B_zy)^-1 rho(B_zy') = 0
     for all y != y'}.

FEASIBILITY RULE for N: N is run iff C(d|C|+N, N) * C(|C|+N, N) <= 30,000,000
(raw equations times unknowns; memory of the dense modular matrix).  N = 2 is
always run.  This is a cost limit.

Fixed seed 20261113.  The result file is deterministic (no times) and the
program refuses to overwrite it.  Usage: verify_multiset_abelian.py [outdir]
"""
import sys, os, json, random, itertools
from math import comb, gcd
from flint import nmod_mat, fmpz_mat, fmpz_poly

SEED = 20261113
P1 = 2147483629 - 0  # replaced below by primes = 1 mod 12
RESULT = "results_multiset_abelian.json"
FEAS = 30_000_000
QLIM = 3_000_000


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def primes_1_mod_12(start, count):
    out = []
    n = start - (start % 12) + 1
    while len(out) < count:
        if is_prime(n):
            out.append(n)
        n -= 12
    return out


P1, P2 = primes_1_mod_12(2 ** 31 - 1, 2)


# ---------------------------------------------------------------- groups
class Group:
    """elements 0..n-1, mul table, identity 0."""

    def __init__(self, name, n, mul):
        self.name, self.n, self.mul = name, n, mul
        self.inv = [next(h for h in range(n) if mul[g][h] == 0) for g in range(n)]

    def generated(self, gens):
        S = {0}
        frontier = [0]
        while frontier:
            x = frontier.pop()
            for g in gens:
                y = self.mul[g][x]
                if y not in S:
                    S.add(y)
                    frontier.append(y)
        return S


def abelian(moduli):
    els = list(itertools.product(*[range(n) for n in moduli]))
    idx = {e: i for i, e in enumerate(els)}
    mul = [[idx[tuple((a + b) % n for a, b, n in zip(x, y, moduli))] for y in els] for x in els]
    G = Group("x".join("C%d" % n for n in moduli), len(els), mul)
    G.moduli, G.els, G.idx = moduli, els, idx
    e = 1
    for n in moduli:
        e = e * n // gcd(e, n)
    G.e = e
    G.chars = els  # dual group: same tuples
    # exponent table: psi_c(h) = zeta_e ^ ex[c][h]
    G.ex = [[sum(ci * hi * (e // n) for ci, hi, n in zip(c, h, moduli)) % e for h in els] for c in els]
    G.cmul = mul  # product of characters = sum of tuples
    return G


def s3():
    els = list(itertools.permutations(range(3)))
    idx = {e: i for i, e in enumerate(els)}
    mul = [[idx[tuple(p[q[i]] for i in range(3))] for q in els] for p in els]
    G = Group("S3", 6, mul)
    G.els, G.idx = els, idx
    G.sign = []
    G.std = []
    for p in els:
        s = 1
        for i in range(3):
            for j in range(i):
                if p[j] > p[i]:
                    s = -s
        G.sign.append(s)
        # standard rep on sum-zero lattice, basis v1=e0-e1, v2=e1-e2; coords (x0,-x2)
        cols = []
        for v in ((1, -1, 0), (0, 1, -1)):
            w = [0, 0, 0]
            for i in range(3):
                w[p[i]] += v[i]
            cols.append((w[0], -w[2]))
        G.std.append(((cols[0][0], cols[1][0]), (cols[0][1], cols[1][1])))
    return G


# ---------------------------------------------------------------- the law
def multisets(n, N):
    out = []
    for k in range(N + 1):
        out.extend(itertools.combinations_with_replacement(range(n), k))
    return out


def law_rows(G, B, N):
    d = len(B)
    ms = multisets(G.n, N)
    idx = {m: i for i, m in enumerate(ms)}
    slots = [(y, h) for y in range(d) for h in range(G.n)]
    rows = set()
    raw = 0
    for k in range(N + 1):
        for comb_ in itertools.combinations_with_replacement(range(len(slots)), k):
            raw += 1
            row = {}
            my = [[] for _ in range(d)]
            for s in comb_:
                y, h = slots[s]
                my[y].append(h)
            for z in range(d):
                w = tuple(sorted(G.mul[B[z][y]][h] for y in range(d) for h in my[y]))
                i = idx[w]
                row[i] = row.get(i, 0) + 1
            for y in range(d):
                i = idx[tuple(my[y])]
                row[i] = row.get(i, 0) - d
            t = tuple(sorted((i, c) for i, c in row.items() if c != 0))
            if t:
                rows.add(t)
    return ms, sorted(rows), raw


def rank_mod(rows, ncols, p):
    if not rows:
        return 0, None
    M = nmod_mat(len(rows), ncols, p)
    for r, row in enumerate(rows):
        for i, c in row:
            M[r, i] = c % p
    return M.rank(), M


def rank_q(rows, ncols):
    if not rows:
        return 0
    M = fmpz_mat(len(rows), ncols)
    for r, row in enumerate(rows):
        for i, c in row:
            M[r, i] = c
    return M.rank()


# ---------------------------------------------------------------- characters
_cyc = {}


def cyclotomic(n):
    if n not in _cyc:
        num = fmpz_poly([-1] + [0] * (n - 1) + [1])
        for k in range(1, n):
            if n % k == 0:
                num = num // cyclotomic(k)
        _cyc[n] = num
    return _cyc[n]


def roots_sum_zero(exps, e):
    """sum_k zeta_e^exps[k] == 0, exactly."""
    co = [0] * e
    for k in exps:
        co[k % e] += 1
    if e == 1:
        return sum(co) == 0
    q, r = divmod(fmpz_poly(co), cyclotomic(e))
    return r == fmpz_poly([0])


def char_data(G, B):
    d = len(B)
    J0, U = [], []
    for c in range(G.n):
        ex = G.ex[c]
        if all(ex[B[z][y]] == 0 for z in range(d) for y in range(d)):
            J0.append(c)
        if all(roots_sum_zero([ex[B[z][y]] - ex[B[z][y2]] for z in range(d)], G.e)
               for y in range(d) for y2 in range(y)):
            U.append(c)
    J0s, Us = set(J0), set(U)
    pairs = sorted({tuple(sorted((c, l))) for c in U for l in range(G.n) if G.cmul[c][l] in J0s})
    return J0, U, pairs


def check_P6(G, B, J0, U):
    Us, J0s = set(U), set(J0)
    ok = 0 not in Us
    ok = ok and all(G.inv[c] in Us for c in U)
    ok = ok and all(G.cmul[c][j] in Us for c in U for j in J0)
    ker = lambda c: frozenset(h for h in range(G.n) if G.ex[c][h] == 0)
    kU = {ker(c) for c in U}
    ok = ok and all((c in Us) == (ker(c) in kU) for c in range(G.n))
    return ok


def b_space_dim(G, B):
    """dimension over Q of symmetric b with diagonal invariance under the entries
    and the off-diagonal conditions."""
    d = len(B)
    n = G.n
    pid = {}
    for g in range(n):
        for h in range(g, n):
            pid[(g, h)] = len(pid)
    P = lambda g, h: pid[(g, h) if g <= h else (h, g)]
    rows = set()
    entries = sorted({B[z][y] for z in range(d) for y in range(d)})
    for k in entries:
        for g in range(n):
            for h in range(g, n):
                row = {}
                row[P(G.mul[k][g], G.mul[k][h])] = row.get(P(G.mul[k][g], G.mul[k][h]), 0) + 1
                row[P(g, h)] = row.get(P(g, h), 0) - 1
                t = tuple(sorted((i, c) for i, c in row.items() if c))
                if t:
                    rows.add(t)
    for y in range(d):
        for y2 in range(d):
            if y == y2:
                continue
            for g in range(n):
                for h in range(n):
                    row = {}
                    for z in range(d):
                        k = G.mul[G.inv[B[z][y]]][B[z][y2]]
                        i = P(g, G.mul[k][h])
                        row[i] = row.get(i, 0) + 1
                    t = tuple(sorted(row.items()))
                    rows.add(t)
    return len(pid) - rank_q(sorted(rows), len(pid))


def prim_root(e, p):
    for g in range(2, 1000):
        w = pow(g, (p - 1) // e, p)
        if all(pow(w, e // q, p) != 1 for q in range(2, e + 1) if e % q == 0 and is_prime(q)):
            return w
    raise RuntimeError


def solution_vectors(G, J0, pairs, ms, p):
    w = prim_root(G.e, p) if G.e > 1 else 1
    pw = [pow(w, k, p) for k in range(G.e)]
    sig = [[sum(pw[G.ex[c][h]] for h in m) % p for m in ms] for c in range(G.n)]
    vecs = [sig[c] for c in J0] + [[a * b % p for a, b in zip(sig[c], sig[l])] for c, l in pairs]
    return vecs


# ---------------------------------------------------------------- matrices
def fourier(G, g, n):
    def power(k):
        x = 0
        for _ in range(k % n):
            x = G.mul[g][x]
        return x
    return [[power(z * y) for y in range(n)] for z in range(n)]


def kron(G, A, Bm):
    da, db = len(A), len(Bm)
    return [[G.mul[A[z // db][y // db]][Bm[z % db][y % db]] for y in range(da * db)] for z in range(da * db)]


def rephase(G, Bm, rowm, colm):
    d = len(Bm)
    return [[G.mul[rowm[z]][G.mul[Bm[z][y]][colm[y]]] for y in range(d)] for z in range(d)]


def abelian_instances(rng):
    inst = []
    for moduli in [(2, 2), (2, 4), (3, 3), (2, 2, 2), (2, 6)]:
        G = abelian(moduli)
        gens = [G.idx[tuple(1 if i == j else 0 for i in range(len(moduli)))] for j in range(len(moduli))]
        n = G.n
        rnd = lambda d: [[rng.randrange(n) for _ in range(d)] for _ in range(d)]
        F1 = fourier(G, gens[0], moduli[0])
        F2 = fourier(G, gens[1], moduli[1])
        K = kron(G, F1, F2)
        L = []
        L.append(("fourier(g1) [Hadamard type, proper subgroup]", F1))
        L.append(("fourier(g2) [Hadamard type, proper subgroup]", F2))
        L.append(("fourier(g1) x fourier(g2) [Hadamard type]", K))
        d1 = len(F1)
        L.append(("fourier(g1) rephased by random rows and columns [Hadamard type]",
                  rephase(G, F1, [rng.randrange(n) for _ in range(d1)], [rng.randrange(n) for _ in range(d1)])))
        d2 = len(F2)
        L.append(("fourier(g2) rephased by random rows and columns [Hadamard type]",
                  rephase(G, F2, [rng.randrange(n) for _ in range(d2)], [rng.randrange(n) for _ in range(d2)])))
        NB = [r[:] for r in F2]
        NB[-1][-1] = G.mul[NB[-1][-1]][gens[0]]
        L.append(("fourier(g2) with one entry changed [non-block]", NB))
        L.append(("all ones, d=2", [[0, 0], [0, 0]]))
        R = rnd(3)
        for z in range(3):
            R[z][1] = R[z][0]
        L.append(("random d=3 with repeated column", R))
        L.append(("random d=2", rnd(2)))
        L.append(("random d=3", rnd(3)))
        L.append(("random d=4", rnd(4)))
        sub = sorted(G.generated([gens[-1]]))
        L.append(("random d=3 with entries in the subgroup <last generator>",
                  [[rng.choice(sub) for _ in range(3)] for _ in range(3)]))
        if moduli == (2, 2):
            a, b = gens
            ab = G.mul[a][b]
            L.append(("E3: GH(4; C2xC2)", [[0, 0, 0, 0], [0, a, b, ab], [0, b, ab, a], [0, ab, a, b]]))
            L.append(("E4", [[0, 0, 0, 0], [0, 0, a, a], [0, a, 0, a], [0, a, a, b]]))
        if moduli == (2, 2, 2):
            K3 = kron(G, K, fourier(G, gens[2], 2))
            L.append(("fourier(g1) x fourier(g2) x fourier(g3) [Hadamard type, d=8]", K3))
            L.append(("fourier(g1) x fourier(g2) rephased by g3 [Hadamard type, generates C]",
                      rephase(G, K, [0, gens[2], 0, gens[2]], [0, 0, gens[2], 0])))
        for name, Bm in L:
            inst.append((G, name, Bm))
    return inst


def cyclic_examples():
    G = abelian((6,))
    z = lambda k: G.idx[(k % 6,)]
    B1 = [[z(0), z(0), z(3)], [z(0), z(2), z(1)], [z(0), z(4), z(5)]]
    B2 = [[z(0)] * 4, [z(0), z(0), z(3), z(3)], [z(0), z(3), z(1), z(4)], [z(0), z(3), z(4), z(1)]]
    return [(G, "E1: cyclic q=6 d=3", B1), (G, "E2: cyclic q=6 d=4", B2)]


def s3_instances(rng):
    G = s3()
    e = 0
    c = G.idx[(1, 2, 0)]
    t = G.idx[(1, 0, 2)]
    t2 = G.idx[(0, 2, 1)]
    rnd = lambda d: [[rng.randrange(6) for _ in range(d)] for _ in range(d)]
    F3 = fourier(G, c, 3)
    L = [
        ("[[1,c],[1,t]]", [[e, c], [e, t]]),
        ("[[1,1],[1,t]]", [[e, e], [e, t]]),
        ("[[1,1],[1,c]]", [[e, e], [e, c]]),
        ("all ones d=2", [[e, e], [e, e]]),
        ("fourier(c) d=3 [entries in C3]", F3),
        ("fourier(c) rephased rows (1,t,c) cols (1,t2,1)", rephase(G, F3, [e, t, c], [e, t2, e])),
        ("fourier(c) rephased rows (t,t,t2) cols (1,1,t)", rephase(G, F3, [t, t, t2], [e, e, t])),
        ("fourier(c) with one entry changed", [F3[0], F3[1], [e, G.mul[c][c], t]]),
        ("random d=2 #1", rnd(2)), ("random d=2 #2", rnd(2)), ("random d=2 #3", rnd(2)),
        ("random d=3 #1", rnd(3)), ("random d=3 #2", rnd(3)), ("random d=3 #3", rnd(3)),
        ("random d=4", rnd(4)),
        ("fourier(c) x [[1,1],[1,t]] d=6", kron(G, F3, [[e, e], [e, t]])),
    ]
    R = rnd(3)
    for z in range(3):
        R[z][2] = R[z][0]
    L.append(("random d=3 repeated column", R))
    return [(G, name, Bm) for name, Bm in L]


def s3_U(G, B):
    d = len(B)
    U = []
    okS = all(sum(G.sign[B[z][y]] * G.sign[B[z][y2]] for z in range(d)) == 0
              for y in range(d) for y2 in range(y))
    if okS:
        U.append("sign")
    okT = True
    for y in range(d):
        for y2 in range(d):
            if y == y2:
                continue
            S = [[0, 0], [0, 0]]
            for z in range(d):
                m = G.std[G.mul[G.inv[B[z][y]]][B[z][y2]]]
                for i in range(2):
                    for j in range(2):
                        S[i][j] += m[i][j]
            if S != [[0, 0], [0, 0]]:
                okT = False
    if okT:
        U.append("std")
    return U


def feasible_N(G, d):
    return [N for N in (2, 3, 4) if N == 2 or comb(d * G.n + N, N) * comb(G.n + N, N) <= FEAS]


# ---------------------------------------------------------------- main
def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    path = os.path.join(outdir, RESULT)
    if os.path.exists(path):
        sys.exit("refusing to overwrite " + path)
    rng = random.Random(SEED)
    preds = {}

    def rec(name, ok, where):
        q = preds.setdefault(name, {"qualify": 0, "pass": 0, "failed": []})
        q["qualify"] += 1
        if ok:
            q["pass"] += 1
        else:
            q["failed"].append(where)

    records = []
    ab = abelian_instances(rng) + cyclic_examples()
    for G, name, B in ab:
        d = len(B)
        tag = "%s | %s" % (G.name, name)
        h0 = d >= 2 and all(0 <= x < G.n for r in B for x in r) and all(len(r) == d for r in B)
        rec("H0", h0, tag)
        if not h0:
            continue
        H = G.generated({x for r in B for x in r})
        J0, U, pairs = char_data(G, B)
        DIM = len(J0) + len(pairs)
        r = {"group": G.name, "matrix": name, "B": [[list(G.els[x]) for x in row] for row in B],
             "d": d, "H_order": len(H), "generates": len(H) == G.n,
             "J0": [list(G.els[c]) for c in J0], "U": [list(G.els[c]) for c in U],
             "pairs": len(pairs), "DIM": DIM, "runs": []}
        rec("P6", check_P6(G, B, J0, U), tag)
        bdim = b_space_dim(G, B)
        r["b_space_dim"] = bdim
        rec("P7", DIM == G.n // len(H) + bdim, tag)
        if len(H) == G.n:
            invcls = {tuple(sorted((c, G.inv[c]))) for c in U}
            rec("P5", len(J0) == 1 and DIM == 1 + len(invcls), tag)
        if name.startswith("E1"):
            rec("E1", sorted(G.els[c][0] for c in U) == [1, 2, 4, 5], tag)
        if name.startswith("E2"):
            rec("E2", sorted(G.els[c][0] for c in U) == [1, 3, 5], tag)
        if name.startswith("E3"):
            rec("E3", len(H) == 4 and sorted(U) == [1, 2, 3] and DIM == 4, tag)
        if name.startswith("E4"):
            kerb = [c for c in range(G.n) if c != 0 and G.ex[c][G.idx[(0, 1)]] == 0]
            rec("E4", len(H) == 4 and U == kerb and DIM == 2, tag)
        for N in feasible_N(G, d):
            ms, rows, raw = law_rows(G, B, N)
            r1, M1 = rank_mod(rows, len(ms), P1)
            r2, _ = rank_mod(rows, len(ms), P2)
            run = {"N": N, "unknowns": len(ms), "raw_equations": raw, "distinct_equations": len(rows),
                   "nullity_p1": len(ms) - r1, "nullity_p2": len(ms) - r2}
            w = "%s | N=%d" % (tag, N)
            rec("P1", len(ms) - r1 == DIM, w)
            rec("P2", len(ms) - r2 == DIM, w)
            if len(rows) * len(ms) <= QLIM:
                rq = rank_q(rows, len(ms))
                run["nullity_Q"] = len(ms) - rq
                rec("P3", rq == r1, w)
            vecs = solution_vectors(G, J0, pairs, ms, P1)
            V = nmod_mat(len(ms), len(vecs), P1)
            for j, v in enumerate(vecs):
                for i, x in enumerate(v):
                    V[i, j] = x
            ann = (M1 * V).rank() == 0
            rv = V.rank()
            run["solutions_annihilated"] = ann
            run["solutions_rank"] = rv
            rec("P4", ann and rv == DIM, w)
            r["runs"].append(run)
        records.append(r)
        print(tag, "d=%d |H|=%d |J0|=%d |U|=%d DIM=%d" % (d, len(H), len(J0), len(U), DIM),
              [(x["N"], x["nullity_p1"]) for x in r["runs"]], flush=True)

    na = []
    for G, name, B in s3_instances(rng):
        d = len(B)
        tag = "S3 | " + name
        h0 = d >= 2 and all(0 <= x < 6 for r in B for x in r)
        rec("NA0", h0, tag)
        H = G.generated({x for r in B for x in r})
        U = s3_U(G, B)
        bdim = b_space_dim(G, B)
        count = 6 // len(H) + bdim
        rep = 1 + sum(1 if u == "sign" else 3 for u in U)
        r = {"group": "S3", "matrix": name, "B": [[list(G.els[x]) for x in row] for row in B], "d": d,
             "H_order": len(H), "U": U, "b_space_dim": bdim, "count_L_plus_b": count,
             "rep_count_if_generates": rep if len(H) == 6 else None, "runs": []}
        nul = []
        for N in feasible_N(G, d):
            ms, rows, raw = law_rows(G, B, N)
            r1, _ = rank_mod(rows, len(ms), P1)
            r2, _ = rank_mod(rows, len(ms), P2)
            run = {"N": N, "unknowns": len(ms), "raw_equations": raw, "distinct_equations": len(rows),
                   "nullity_p1": len(ms) - r1, "nullity_p2": len(ms) - r2}
            if len(rows) * len(ms) <= QLIM:
                run["nullity_Q"] = len(ms) - rank_q(rows, len(ms))
            r["runs"].append(run)
            nul += [len(ms) - r1, len(ms) - r2]
            w = "%s | N=%d" % (tag, N)
            rec("NA2", len(ms) - r1 == count and len(ms) - r2 == count, w)
            if len(H) == 6:
                rec("NA3", len(ms) - r1 == rep and len(ms) - r2 == rep, w)
        rec("NA1", len(set(nul)) == 1, tag)
        na.append(r)
        print(tag, "d=%d |H|=%d U=%s count=%d rep=%s" % (d, len(H), U, count, r["rep_count_if_generates"]),
              [(x["N"], x["nullity_p1"]) for x in r["runs"]], flush=True)

    out = {"program": "verify_multiset_abelian.py", "seed": SEED, "primes": [P1, P2],
           "predicates": preds,
           "counts": {"abelian_matrices_noncyclic": len(ab) - 2, "cyclic_examples": 2, "S3_matrices": len(na)},
           "abelian": records, "S3": na}
    with open(path, "x") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")
    print("\nPREDICATE  qualify  pass")
    for k in sorted(preds):
        print("%-9s %7d %5d %s" % (k, preds[k]["qualify"], preds[k]["pass"],
                                   "" if not preds[k]["failed"] else "FAILED: %s" % preds[k]["failed"]))


if __name__ == "__main__":
    main()
