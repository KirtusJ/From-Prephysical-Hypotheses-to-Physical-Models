#!/usr/bin/env python3
"""four_gain.py -- one-site equation of the two-rail walk with four arc gains.

Carrier: vertices (x,R),(x,L); arcs (x,R)->(x+1,R) gain a, (x,R)->(x-1,L) gain b,
(x,L)->(x+1,R) gain c, (x,L)->(x-1,L) gain d, in a finite abelian group A.
Equation (E4):  F_R(T_a U + T_c V) + F_L(T_b U + T_d V) = 2 F_R(U) + 2 F_L(V),  F(0)=0.
Notation: delta = a d (b c)^-1, H = <a, d, bc>, r = order of delta.
For a subgroup Delta containing delta, the Delta-restricted problem has unknowns F_R on non-empty
multisets supported in ONE coset of Delta inside H.Delta, F_L likewise inside b.H.Delta, and the
equations (E4) for U supported in kappa.Delta, V supported in kappa.b.d^-1.Delta, kappa in H.Delta.
Delta = A is the full equation.  Delta = <delta> is the line.  Delta = <delta,(a/d)^k> is ring-like.

Arithmetic: exact, in the prime field F_p, p = largest prime below 2^31 with p = 1 mod 12.
The rank over F_p is at most the rank over Q, so nullity over F_p >= nullity over Q >= number of
explicit independent solutions; when the F_p value equals the formula the value over Q is the formula
PROVIDED the explicit solutions exist (that part is proof, not computation).
dim reported = rank of the projection of the solution space of the box |U|+|V| <= n onto the
unknowns with |m| <= 2 ("proj"), and the raw nullity of the box ("null").

PREDICATES (fixed before the first run; seed 20261113):
 P1  full equation (Delta = A): proj at the largest n computed equals
       f_full = |A/H| + #{unordered {chi,chi'} : chi(delta)=chi'(delta)=-1, chi.chi' trivial on H}.
 P1c the brief's conjecture c_conj = 1 + #{classes {chi, conj chi} : chi(delta) = -1} equals the
       found dimension IF AND ONLY IF H = A.  (Hypothesis H = A tested per case, counts reported.)
 P2  line problem (Delta = <delta>): proj at the largest n equals 1 + [r even].
 P3  ring-like problem (Delta = <delta, (a/d)^k>, k = 1, 3): proj at largest n equals
       f_Delta = |Delta/(H cap Delta)| + #{unordered {chi,chi'} characters of Delta with
       chi(delta)=chi'(delta)=-1 and chi.chi' trivial on H cap Delta}.
 P4  mixed forms, full equation: for every ordered pair (chi,chi') of characters of A the system
       F_R = qR sigma_chi sigma_chi', F_L = qL sigma_chi sigma_chi' has a non-zero solution (qR,qL)
       iff chi(delta) = chi'(delta) = -1 and chi.chi' trivial on H; then (qR,qL) = (1, (chi chi')(c)).
       (Re(sigma_chi conj sigma_psi) is the pair (chi, conj psi).)
 P5  linear forms: F_R = l sigma_chi, F_L = m sigma_chi has a non-zero solution iff chi trivial on H;
       then (l,m) = (1, chi(c)).
 P6  line: for all lengths T <= 12 and vertices, the set of gains of walks from (0,R) lies in the
       coset a^rho d^lam <delta> at (x,R), a^rho d^(lam-1) b <delta> at (x,L), rho=(T+x)/2, lam=(T-x)/2.
 P7  ring Z_N, N in 3..7: for T <= 14 the set of gains at a vertex lies in ONE coset of
       <delta, (a/d)^(N/gcd(N,2))>.
 P8  converse on all events (line, random sets of walks of length <= 7): the rule
       F_y(m) = 3|m| + 5 eps(m)^2 (r even; eps = alternating sum along the <delta>-coset), 3|m| (r odd),
       same formula on both rails, satisfies mu(Ext S) = 2 mu(S).
 P9  stability: proj is the same at n = 3 and at n = 4 in every case where both are computed.
Every failed predicate is written to the result file; exit code 0 iff no predicate failed.
Result file is opened with mode 'x' and is never overwritten.
"""
import sys, itertools, random, math, json, hashlib
import numpy as np

SEED = 20261113

def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
P = 2**31 - 1
while not (P % 12 == 1 and is_prime(P)): P -= 1

def rref(M):
    """row reduce mod P; returns (M, pivot columns)."""
    M = M % P
    rows, cols = M.shape
    piv = []; r = 0
    for c in range(cols):
        if r >= rows: break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        k = r + nz[0]
        if k != r: M[[r, k]] = M[[k, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, P)) % P
        idx = np.nonzero(M[:, c])[0]; idx = idx[idx != r]
        if len(idx):
            M[idx] = (M[idx] - (M[idx, c][:, None] * M[r][None, :]) % P) % P
        piv.append(c); r += 1
    return M, piv

def nullspace(M, ncols):
    if M.shape[0] == 0:
        return np.eye(ncols, dtype=np.int64)
    M, piv = rref(M)
    free = [c for c in range(ncols) if c not in set(piv)]
    NS = np.zeros((len(free), ncols), dtype=np.int64)
    for i, f in enumerate(free):
        NS[i, f] = 1
        for j, pc in enumerate(piv):
            NS[i, pc] = (-M[j, f]) % P
    return NS

def rank(M):
    if M.size == 0: return 0
    return len(rref(M.copy())[1])

class Grp:
    def __init__(self, ns):
        self.ns = tuple(ns)
        self.els = list(itertools.product(*[range(n) for n in ns]))
        self.idx = {e: i for i, e in enumerate(self.els)}
        self.q = len(self.els)
        self.E = 1
        for n in ns: self.E = self.E * n // math.gcd(self.E, n)
        q = self.q
        self.mul = [[self.idx[tuple((x + y) % n for x, y, n in zip(self.els[i], self.els[j], ns))]
                     for j in range(q)] for i in range(q)]
        self.inv = [self.idx[tuple((-x) % n for x, n in zip(self.els[i], ns))] for i in range(q)]
        # characters as exponent tables mod E
        self.chars = [tuple(sum(k * x * (self.E // n) for k, x, n in zip(kk, self.els[i], ns)) % self.E
                            for i in range(q)) for kk in self.els]
    def gen(self, gens):
        S = {0}; fr = [0]
        while fr:
            x = fr.pop()
            for g in gens:
                y = self.mul[x][g]
                if y not in S: S.add(y); fr.append(y)
        return frozenset(S)
    def pw(self, g, k):
        x = 0
        for _ in range(k): x = self.mul[x][g]
        return x
    def order(self, g): return len(self.gen([g]))
    def tr(self, m, g):
        out = [0] * self.q
        for x in range(self.q):
            if m[x]: out[self.mul[x][g]] = m[x]
        return tuple(out)

def msets(q, support, s):
    """multisets of size s supported on `support` (sorted list of element indices)."""
    for comb in itertools.combinations_with_replacement(support, s):
        m = [0] * q
        for x in comb: m[x] += 1
        yield tuple(m)

def add(m1, m2): return tuple(x + y for x, y in zip(m1, m2))

def invariants(G, a, b, c, d):
    bc = G.mul[b][c]; delta = G.mul[G.mul[a][d]][G.inv[bc]]
    H = G.gen([a, d, bc])
    return delta, H

def formula(G, delta, H, Delta):
    """|Delta/(H cap Delta)| + #unordered pairs of characters of Delta in N with product trivial on H cap Delta."""
    HD = sorted(H & Delta); Dl = sorted(Delta)
    restr = sorted(set(tuple(ch[x] for x in Dl) for ch in G.chars))
    pos = {x: i for i, x in enumerate(Dl)}
    E = G.E
    N = [ch for ch in restr if E % 2 == 0 and ch[pos[delta]] == E // 2]
    pairs = 0
    for i in range(len(N)):
        for j in range(i, len(N)):
            if all((N[i][pos[h]] + N[j][pos[h]]) % E == 0 for h in HD): pairs += 1
    classes = len(set(frozenset([ch, tuple((-v) % E for v in ch)]) for ch in N))
    return len(Dl) // len(HD) + pairs, 1 + classes, len(N)

def solve(G, a, b, c, d, Delta, n):
    """returns (nullity, proj rank onto |m|<=2) of the Delta-restricted box |U|+|V| <= n."""
    q = G.q
    delta, H = invariants(G, a, b, c, d)
    HDel = G.gen(list(H) + list(Delta))
    bdinv = G.mul[b][G.inv[d]]
    def cosets(base):
        seen = set(); out = []
        for k in sorted(HDel):
            cs = frozenset(G.mul[G.mul[k][base]][x] for x in Delta)
            if cs not in seen: seen.add(cs); out.append(sorted(cs))
        return out
    cosR = cosets(0); cosL = cosets(b)
    col = {}
    for rail, cs_list in (('R', cosR), ('L', cosL)):
        for cs in cs_list:
            for s in range(1, n + 1):
                for m in msets(q, cs, s):
                    if (rail, m) not in col: col[(rail, m)] = len(col)
    zero = tuple([0] * q)
    rows = set()
    for cs in cosR:
        csV = sorted(G.mul[x][bdinv] for x in cs)
        for su in range(0, n + 1):
            for U in msets(q, cs, su):
                for sv in range(0, n - su + 1):
                    if su + sv == 0: continue
                    for V in msets(q, csV, sv):
                        W1 = add(G.tr(U, a), G.tr(V, c)); W2 = add(G.tr(U, b), G.tr(V, d))
                        row = {}
                        for key, coef in ((('R', W1), 1), (('L', W2), 1), (('R', U), -2), (('L', V), -2)):
                            if key[1] == zero: continue
                            j = col[key]            # KeyError here would mean the domain is not closed
                            row[j] = row.get(j, 0) + coef
                        rows.add(tuple(sorted((j, v) for j, v in row.items() if v)))
    rows.discard(())
    M = np.zeros((len(rows), len(col)), dtype=np.int64)
    for i, rw in enumerate(sorted(rows)):
        for j, v in rw: M[i, j] = v % P
    NS = nullspace(M, len(col))
    small = [j for (rail, m), j in col.items() if sum(m) <= 2]
    return NS.shape[0], rank(NS[:, small])

def zeta_of_order(E):
    for g in range(2, 200):
        z = pow(g, (P - 1) // E, P)
        if all(pow(z, E // f, P) != 1 for f in (2, 3) if E % f == 0): return z
    raise RuntimeError

def forms_test(G, a, b, c, d):
    """P4 and P5. returns (n_pairs, n_pair_fail, n_solution_pairs, n_lin, n_lin_fail, n_lin_sol)."""
    q = G.q; delta, H = invariants(G, a, b, c, d)
    E = G.E; z = zeta_of_order(E)
    X = np.array([[pow(z, ch[x], P) for ch in G.chars] for x in range(q)], dtype=np.int64)  # q x nchar
    zero = tuple([0] * q); allx = list(range(q))
    Us, Vs, W1s, W2s = [], [], [], []
    for su in range(0, 4):
        for U in msets(q, allx, su):
            for sv in range(0, 4 - su):
                for V in msets(q, allx, sv):
                    Us.append(U); Vs.append(V)
                    W1s.append(add(G.tr(U, a), G.tr(V, c))); W2s.append(add(G.tr(U, b), G.tr(V, d)))
    sU, sV, s1, s2 = [(np.array(L, dtype=np.int64) @ X) % P for L in (Us, Vs, W1s, W2s)]
    inN = [E % 2 == 0 and ch[delta] == E // 2 for ch in G.chars]
    trivH = lambda ex: all(ex[h] % E == 0 for h in H)
    npair = fail = nsol = 0
    for i, ci in enumerate(G.chars):
        for j, cj in enumerate(G.chars):
            npair += 1
            A1 = (s1[:, i] * s1[:, j] - 2 * (sU[:, i] * sU[:, j] % P)) % P
            A2 = (s2[:, i] * s2[:, j] - 2 * (sV[:, i] * sV[:, j] % P)) % P
            Mx = np.stack([A1, A2], axis=1)
            nul = 2 - rank(Mx)
            om = tuple((x + y) % E for x, y in zip(ci, cj))
            exp = 1 if (inN[i] and inN[j] and trivH(om)) else 0
            ok = (nul == exp)
            if ok and exp == 1:
                w = pow(z, om[c], P)
                ok = bool(np.all((A1 + A2 * w) % P == 0))
            if not ok: fail += 1
            nsol += (nul >= 1)
    nlin = lfail = lsol = 0
    for i, ci in enumerate(G.chars):
        nlin += 1
        A1 = (s1[:, i] - 2 * sU[:, i]) % P; A2 = (s2[:, i] - 2 * sV[:, i]) % P
        nul = 2 - rank(np.stack([A1, A2], axis=1))
        exp = 1 if trivH(ci) else 0
        ok = (nul == exp)
        if ok and exp == 1: ok = bool(np.all((A1 + A2 * pow(z, ci[c], P)) % P == 0))
        if not ok: lfail += 1
        lsol += (nul >= 1)
    return npair, fail, nsol, nlin, lfail, lsol

def step_sets(G, a, b, c, d, state, N=None):
    new = {}
    for (x, rail), gs in state.items():
        xr = x + 1 if N is None else (x + 1) % N
        xl = x - 1 if N is None else (x - 1) % N
        gR, gL = (a, b) if rail == 'R' else (c, d)
        new.setdefault((xr, 'R'), set()).update(G.mul[g][gR] for g in gs)
        new.setdefault((xl, 'L'), set()).update(G.mul[g][gL] for g in gs)
    return new

def lemma0_line(G, a, b, c, d, Tmax=12):
    delta, H = invariants(G, a, b, c, d); Dl = G.gen([delta])
    state = {(0, 'R'): {0}}; checked = bad = full = 0
    for T in range(1, Tmax + 1):
        state = step_sets(G, a, b, c, d, state)
        for (x, rail), gs in state.items():
            rho, lam = (T + x) // 2, (T - x) // 2
            k = G.mul[G.pw(a, rho)][G.pw(d, lam)]
            if rail == 'L': k = G.mul[G.mul[k][G.inv[d]]][b]
            cs = {G.mul[k][u] for u in Dl}
            checked += 1; bad += (not gs <= cs); full += (gs == cs)
    return checked, bad, full

def lemma0_ring(G, a, b, c, d, N, Tmax=14):
    delta, H = invariants(G, a, b, c, d)
    w = G.pw(G.mul[a][G.inv[d]], N // math.gcd(N, 2))
    Dl = G.gen([delta, w])
    state = {(0, 'R'): {0}}; checked = bad = 0
    for T in range(1, Tmax + 1):
        state = step_sets(G, a, b, c, d, state, N)
        for key, gs in state.items():
            g0 = next(iter(gs)); cs = {G.mul[g0][u] for u in Dl}
            checked += 1; bad += (not gs <= cs)
    return checked, bad

def converse(G, a, b, c, d, rng, trials=6, Tmax=7):
    delta, H = invariants(G, a, b, c, d); r = G.order(delta); Dl = G.gen([delta])
    def F(m):   # m: dict gain->count, supported on one coset of <delta>
        tot = sum(m.values())
        if tot == 0: return 0
        if r % 2: return 3 * tot
        g0 = next(iter(m)); assert all(G.mul[g][G.inv[g0]] in Dl for g in m)
        eps = 0; g = g0
        for j in range(r):
            eps += (-1) ** j * m.get(g, 0); g = G.mul[g][delta]
        return 3 * tot + 5 * eps * eps
    def mu(S):
        fam = {}
        for (x, rail, g) in S:
            fam.setdefault((x, rail), {}); fam[(x, rail)][g] = fam[(x, rail)].get(g, 0) + 1
        return sum(F(m) for m in fam.values())
    def ext(S):
        out = []
        for (x, rail, g) in S:
            gR, gL = (a, b) if rail == 'R' else (c, d)
            out.append((x + 1, 'R', G.mul[g][gR])); out.append((x - 1, 'L', G.mul[g][gL]))
        return out
    n = bad = 0
    walks = [(0, 'R', 0)]
    for T in range(0, Tmax + 1):
        for _ in range(trials):
            S = [w for w in walks if rng.random() < 0.5]
            n += 1; bad += (mu(ext(S)) != 2 * mu(S))
        walks = ext(walks)
    return n, bad

def main():
    out = open(sys.argv[1] if len(sys.argv) > 1 else 'four_gain_result.txt', 'x')
    def W(s=''):
        out.write(s + '\n'); out.flush()
    rng = random.Random(SEED)
    W('four_gain.py  seed %d  prime %d' % (SEED, P))
    fails = []
    groups = [((2,), 'Z2'), ((3,), 'Z3'), ((4,), 'Z4'), ((2, 2), 'Z2xZ2'), ((6,), 'Z6'), ((2, 4), 'Z2xZ4')]
    # box sizes per problem kind and group; cases: all quadruples or a seeded sample
    plan = {
        'Z2':    dict(cases=None, full=[2, 3, 4, 5], line=[2, 3, 4, 5], ring=[2, 3, 4]),
        'Z3':    dict(cases=None, full=[2, 3, 4], line=[2, 3, 4], ring=[2, 3, 4]),
        'Z4':    dict(cases=None, full=[2, 3], line=[2, 3, 4], ring=[2, 3]),
        'Z2xZ2': dict(cases=None, full=[2, 3], line=[2, 3, 4], ring=[2, 3]),
        'Z6':    dict(cases=120, full=[2, 3], line=[2, 3, 4], ring=[2, 3]),
        'Z2xZ4': dict(cases=60, full=[2, 3], line=[2, 3, 4], ring=[2, 3]),
    }
    extra4 = {'Z4': 40, 'Z2xZ2': 40, 'Z6': 8}      # sampled cases of the full equation also at n = 4
    W('columns of the summary: group | problem | cases | pass | fail ; details of every failure follow')
    summary = []
    table = {}
    for ns, name in groups:
        G = Grp(ns); q = G.q
        allq = list(itertools.product(range(q), repeat=4))
        pl = plan[name]
        cases = allq if pl['cases'] is None else rng.sample(allq, pl['cases'])
        ex4 = set(rng.sample(cases, extra4[name])) if name in extra4 else set()
        st = {k: [0, 0] for k in ('P1', 'P1c', 'P2', 'P3k1', 'P3k3', 'P9')}
        hyp = dict(cases=len(cases), r_even=0, H_eq_A=0, delta_gen_A=0, conj_eq_found=0,
                   conj_eq_found_and_H_eq_A=0, conj_ne_found_and_H_ne_A=0, spurious_null_at_top_n=0)
        f4 = [0, 0, 0, 0, 0, 0]
        for (a, b, c, d) in cases:
            delta, H = invariants(G, a, b, c, d); r = G.order(delta)
            full = frozenset(range(q)); Dline = G.gen([delta])
            hyp['r_even'] += (r % 2 == 0); hyp['H_eq_A'] += (H == full); hyp['delta_gen_A'] += (Dline == full)
            # ---- full equation
            ff, cconj, nN = formula(G, delta, H, full)
            nsz = list(pl['full']) + ([4] if (a, b, c, d) in ex4 and 4 not in pl['full'] else [])
            res = {n: solve(G, a, b, c, d, full, n) for n in nsz}
            found = res[nsz[-1]][1]
            key = (name, r, len(H), ff, cconj, tuple((n, res[n][0], res[n][1]) for n in nsz))
            table[key] = table.get(key, 0) + 1
            ok = (found == ff); st['P1'][0 if ok else 1] += 1
            if not ok: fails.append('P1 %s gains %s found %d formula %d %s' % (name, (a, b, c, d), found, ff, res))
            eq = (cconj == found); hyp['conj_eq_found'] += eq
            hyp['conj_eq_found_and_H_eq_A'] += (eq and H == full); hyp['conj_ne_found_and_H_ne_A'] += ((not eq) and H != full)
            ok = (eq == (H == full)); st['P1c'][0 if ok else 1] += 1
            if not ok: fails.append('P1c %s gains %s found %d conj %d H=A %s' % (name, (a, b, c, d), found, cconj, H == full))
            hyp['spurious_null_at_top_n'] += (res[nsz[-1]][0] != found)
            if 3 in res and 4 in res:
                ok = (res[3][1] == res[4][1]); st['P9'][0 if ok else 1] += 1
                if not ok: fails.append('P9 full %s gains %s %s' % (name, (a, b, c, d), res))
            # ---- line
            res = {n: solve(G, a, b, c, d, Dline, n) for n in pl['line']}
            found = res[pl['line'][-1]][1]; exp = 1 + (r % 2 == 0)
            ok = (found == exp); st['P2'][0 if ok else 1] += 1
            if not ok: fails.append('P2 %s gains %s found %d expected %d %s' % (name, (a, b, c, d), found, exp, res))
            if 3 in res and 4 in res:
                ok = (res[3][1] == res[4][1]); st['P9'][0 if ok else 1] += 1
                if not ok: fails.append('P9 line %s gains %s %s' % (name, (a, b, c, d), res))
            # ---- ring-like
            for k in (1, 3):
                w = G.pw(G.mul[a][G.inv[d]], k); Dr = G.gen([delta, w])
                fr, _, _ = formula(G, delta, H, Dr)
                res = {n: solve(G, a, b, c, d, Dr, n) for n in pl['ring']}
                found = res[pl['ring'][-1]][1]
                ok = (found == fr); st['P3k%d' % k][0 if ok else 1] += 1
                if not ok: fails.append('P3 k=%d %s gains %s found %d formula %d %s' % (k, name, (a, b, c, d), found, fr, res))
                if 3 in res and 4 in res:
                    ok = (res[3][1] == res[4][1]); st['P9'][0 if ok else 1] += 1
                    if not ok: fails.append('P9 ring %s gains %s %s' % (name, (a, b, c, d), res))
            # ---- forms
            t = forms_test(G, a, b, c, d)
            for i in range(6): f4[i] += t[i]
            if t[1]: fails.append('P4 %s gains %s: %d pairs fail' % (name, (a, b, c, d), t[1]))
            if t[4]: fails.append('P5 %s gains %s: %d characters fail' % (name, (a, b, c, d), t[4]))
        # ---- lemma 0 and converse, on a seeded sub-sample
        sub = cases if len(cases) <= 81 else rng.sample(cases, 60)
        l6 = [0, 0, 0]; l7 = [0, 0]; l8 = [0, 0]
        for (a, b, c, d) in sub:
            t = lemma0_line(G, a, b, c, d); l6 = [x + y for x, y in zip(l6, t)]
            if t[1]: fails.append('P6 %s gains %s' % (name, (a, b, c, d)))
            for N in range(3, 8):
                t = lemma0_ring(G, a, b, c, d, N); l7 = [x + y for x, y in zip(l7, t)]
                if t[1]: fails.append('P7 %s N=%d gains %s' % (name, N, (a, b, c, d)))
            t = converse(G, a, b, c, d, rng); l8 = [x + y for x, y in zip(l8, t)]
            if t[1]: fails.append('P8 %s gains %s' % (name, (a, b, c, d)))
        W('')
        W('GROUP %s  |A|=%d  cases=%d (%s)' % (name, q, len(cases), 'all quadruples' if pl['cases'] is None else 'seeded sample of %d' % q**4))
        W('  hypotheses per case: ' + json.dumps(hyp, sort_keys=True))
        for k in ('P1', 'P1c', 'P2', 'P3k1', 'P3k3', 'P9'):
            W('  %-5s pass %d fail %d' % (k, st[k][0], st[k][1]))
        W('  P4    ordered pairs of characters tested %d, fail %d, pairs with a solution %d' % (f4[0], f4[1], f4[2]))
        W('  P5    characters tested %d, fail %d, with a solution %d' % (f4[3], f4[4], f4[5]))
        W('  P6    line vertex-length instances %d, outside predicted coset %d, equal to the whole coset %d (on %d gain choices)' % (l6[0], l6[1], l6[2], len(sub)))
        W('  P7    ring vertex-length instances %d, not in one coset %d' % (l7[0], l7[1]))
        W('  P8    events %d, mu(Ext S) != 2 mu(S): %d' % (l8[0], l8[1]))
    W('')
    W('TABLE full equation: group | r=ord(delta) | |H| | formula | brief-conjecture | (n, null, proj)... | number of cases')
    for key in sorted(table):
        W('  %-6s r=%d |H|=%d formula=%d conj=%d %s : %d' % (key[0], key[1], key[2], key[3], key[4], list(key[5]), table[key]))
    W('')
    W('FAILED PREDICATES: %d' % len(fails))
    for f in fails: W('  ' + f)
    out.close()
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
