#!/usr/bin/env python3
"""Challenger program for lem:twist, lem:twolevelabs, lem:symquad, thm:fgprod, thm:fgthree
(draft G10 subsection "winding products").  Written from the paper text only.
Usage:  python3 check_products.py <result_file> [seed=20261115]
The result file is opened with mode 'x' (never overwritten).  Exit code 0 = program ran to the end
(NOT "all predicates pass": read the result file).

PREDICATES, FIXED BEFORE THE FIRST RUN.  Each reports qualifying instances / passes / fails.

P1  (lem:symquad) for k=2,3,4: d_sym := number of S_k-orbits on {00,01,11}^k (dimension of the symmetric
    multi-quadratic polynomials, by enumeration), d_form := number of pairs i<=j in 0..k, rk := exact rank of
    the polynomials pi_i*pi_j in the 3^k monomial basis.  PASS iff every pi_i*pi_j is multi-quadratic and
    constant on orbits, and d_sym == d_form == rk.
P2  (thm:fgthree) in each group instance (hypothesis tested per instance: r even, s==3, beta^3=delta^k0):
    e_beta * A == B as multisets, A, B as in the text.
P3  the factors of A, B, C lie in M(C0 u C1); pi computed from the factors equals the stated polynomials
    (4+s+sX)(1+X)^(d-1), (1+2X)(1+(2+s)X)(1+X)^(d-2); pi_0*pi_d equals s(4+s), 2(2+s); these differ; d=2..8.
P4  eps_j(m) == pibar_j for every product generated in P6 (eps computed from the multiset itself).
P5  Qbar(phi(X pi)) == Qbar(phi(pi)) on random integer pi (deg<=8), for (q,c)=(1,0),(0,1); and the Gram
    coefficients of Qbar o phi depend on j-i only, with c*_0=q, c*_1=c.
P6  unknowns c_0..c_K (K=6).  Constraint set: all pairs of products P1*..*Pk (k<=K, factors from a fixed
    list in M(C0 u C1)) whose multisets coincide up to translation by <delta,beta>.
    P6a: solution space has dimension exactly 2.   P6b: with ONLY the A*C / B*C coincidences d=2..K it is 2.
    P6c: the vectors c* of Qbar o phi for (q,c)=(1,0),(0,1) lie in the solution space of P6a.
P7  (search for a function not of the stated form) family c_0=1, c_d=2Re(u^d), i.e. |pi(u)|^2, |u|=1.
    N_d(x)=x^d(pi_A(x)pi_A(1/x)-pi_B(x)pi_B(1/x)).  PASS iff the roots on the unit circle of gcd(N_2..N_6)
    are exactly the roots of x^3-sigma.  (Exact: gcd in Q[x], then factor.)
P8  (thm:fgprod, scalar transfer) for A in M(C0), P in M(C0 u C1): |A*P|=|A||P|, eps(A*P)=eps0(A)*eps(P),
    A*P in M(C0 u C1); and an A with |A| != eps0(A)^2 exists (A=2e_1).  Random instances.
P9  (lem:twist) rings N=3..8, four random gains in Z_6 / Z_2xZ_3 written as Z_6.  S1 random masks with the
    walks forced to one vertex (x1,R); qualifies iff non-empty.  S2 random masks.
    P9a: concatenated event has multiset m1*m_{S2}(y,rho) at every vertex (x1+y,rho), empty elsewhere.
    P9n (control, EXPECTED TO FAIL in some instances): same with S1 forced to (x1,L).
    P9c: m1 alone on L at x1, then mask {x1+1}: T_c m1 at (x1+1,R) and nothing else (N>=3).
    P9d (boundary, N=2): same as P9c on the ring of 2 sites -- expected to fail ("alone").
P10 (lem:twolevelabs, truncated) r=2: unknowns f(m), 1<=|m|<=S on the 4 elements of C0 u C1; constraints:
    T_delta invariance, f(m)=f(T_beta m) for m in M(C0), eq:fgQ at pairs (A0),(B0) with |u|+|v|<=S.
    P10a: for S=6 the solution space restricted to |m|<=3 has dimension 3.
    P10b: |m|, eps0^2+eps1^2, eps0*eps1 are solutions.
    P10c (information): the same without the T_beta hypothesis has restricted dimension 5.
    Truncation can leave extra solutions near the cut; that is why the restriction to |m|<=3 is the predicate.
"""
import sys, json, itertools, random, time
from fractions import Fraction
from collections import Counter
import sympy as sp

OUT = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261115
random.seed(SEED)
fh = open(OUT, 'x')
RES = {'seed': SEED, 'argv': sys.argv, 'predicates': {}}
def rec(name, qual, passed, failed, info=None):
    RES['predicates'][name] = {'qualify': qual, 'pass': passed, 'fail': failed, 'info': info}
    print(name, 'qualify', qual, 'pass', passed, 'fail', failed, info if info else '', flush=True)

# ---------- exact rank helper ----------
class Basis:
    def __init__(self, n): self.n = n; self.rows = {}   # pivot -> row
    def add(self, v):
        v = [Fraction(x) for x in v]
        for p, r in self.rows.items():
            if v[p] != 0:
                f = v[p]; v = [a - f * b for a, b in zip(v, r)]
        for p in range(self.n):
            if v[p] != 0:
                f = v[p]; v = [a / f for a in v]
                for q, r in list(self.rows.items()):
                    if r[p] != 0:
                        g = r[p]; self.rows[q] = [a - g * b for a, b in zip(r, v)]
                self.rows[p] = v; return True
        return False
    def rank(self): return len(self.rows)
    def contains_in_null(self, c):   # c orthogonal to all rows
        return all(sum(a * b for a, b in zip(r, c)) == 0 for r in self.rows.values())

# ---------- P1 ----------
def p1():
    q = p = f = 0; info = {}
    for k in (2, 3, 4):
        q += 1
        X = sp.Symbol('X')
        ps = [(sp.Symbol(f'a{i}'), sp.Symbol(f'b{i}')) for i in range(k)]
        gens = [s for pr in ps for s in pr]
        prod = sp.Poly(sp.expand(sp.prod([a + b * X for a, b in ps])), X)
        pi = [prod.coeff_monomial(X**i) for i in range(k + 1)]
        types = list(itertools.product(range(3), repeat=k))      # 0: a^2, 1: ab, 2: b^2
        expo = {t: tuple(e for ti in t for e in ((2, 0), (1, 1), (0, 2))[ti]) for t in types}
        inv = {v: t for t, v in expo.items()}
        orbits = {tuple(sorted(t)) for t in types}
        d_sym = len(orbits)
        B = Basis(len(types)); ok = True; d_form = 0
        for i in range(k + 1):
            for j in range(i, k + 1):
                d_form += 1
                P = sp.Poly(sp.expand(pi[i] * pi[j]), *gens)
                vec = dict.fromkeys(types, 0)
                for mon, co in P.terms():
                    if mon not in inv: ok = False; continue
                    vec[inv[mon]] = co
                for t in types:
                    if vec[t] != vec[tuple(sorted(t))]: ok = False
                B.add([vec[t] for t in types])
        rk = B.rank()
        info[k] = {'d_sym_orbits': d_sym, 'd_form_pairs': d_form, 'rank_G_of_pi': rk, 'multiquad_and_symmetric': ok}
        if ok and d_sym == d_form == rk: p += 1
        else: f += 1
    rec('P1', q, p, f, info)

# ---------- group instances ----------
class Grp:
    def __init__(self, mods, delta, beta, name):
        self.mods, self.delta, self.beta, self.name = mods, delta, beta, name
        self.e = tuple(0 for _ in mods)
    def mul(self, g, h): return tuple((a + b) % m for a, b, m in zip(g, h, self.mods))
    def pw(self, g, n):
        r = self.e
        for _ in range(n): r = self.mul(r, g)
        return r
    def setup(self):
        D = [self.e]
        while True:
            x = self.mul(D[-1], self.delta)
            if x == self.e: break
            D.append(x)
        self.D = D; self.r = len(D)
        s = 1
        while self.pw(self.beta, s) not in D: s += 1
        self.s = s
        self.k0 = D.index(self.pw(self.beta, s))
        self.sigma = (-1) ** self.k0
        # coordinates: element -> (coset j, exponent n) with element = beta^j delta^n, 0<=j<s
        self.coord = {}
        for j in range(s):
            for n in range(self.r):
                self.coord[self.mul(self.pw(self.beta, j), self.pw(self.delta, n))] = (j, n)
        self.Delta = list(self.coord)
        return self.r % 2 == 0 and self.s == 3
    def conv(self, m1, m2):
        out = Counter()
        for g, x in m1.items():
            for h, y in m2.items(): out[self.mul(g, h)] += x * y
        return out
    def tr(self, g, m): return Counter({self.mul(g, h): x for h, x in m.items()})
    def eps(self, m):
        e = [0] * self.s
        for g, x in m.items():
            j, n = self.coord[g]; e[j] += (-1) ** n * x
        return e
    def canon(self, m):
        return min(tuple(sorted(self.tr(g, m).items())) for g in self.Delta)
    def inM01(self, m): return all(self.coord[g][0] in (0, 1) for g in m)

INST = [Grp((2, 3), (1, 0), (0, 1), 'Z2xZ3 d=(1,0) b=(0,1)'),
        Grp((6,), (3,), (1,), 'Z6 d=3 b=1'),
        Grp((4, 3), (1, 0), (0, 1), 'Z4xZ3 d=(1,0) b=(0,1)'),
        Grp((12,), (3,), (1,), 'Z12 d=3 b=1'),
        Grp((12,), (3,), (2,), 'Z12 d=3 b=2'),
        Grp((2, 9), (1, 0), (0, 1), 'Z2xZ9 d=(1,0) b=(0,1)  [control: s=9, must NOT qualify]'),
        Grp((3, 3), (1, 0), (0, 1), 'Z3xZ3 [control: r odd, must NOT qualify]')]

def polymul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] += x * y
    return out
def pibar(pi, sigma):
    e = [0, 0, 0]
    for i, x in enumerate(pi): e[i % 3] += sigma ** (i // 3) * x
    return e
def Sd(pi, K):
    return [sum(pi[i] * pi[i + d] for i in range(len(pi) - d)) if d < len(pi) else 0 for d in range(K + 1)]
def Qbar(e, q, c, sigma):
    return q * sum(x * x for x in e) + c * (e[0] * e[1] + e[1] * e[2] + sigma * e[2] * e[0])
def cstar(q, c, sigma, K):
    # coefficient of pi_0 pi_d in Qbar(phi(pi)) by polarisation on unit vectors
    out = []
    for d in range(K + 1):
        u = [0] * (K + 1); u[0] = 1; v = [0] * (K + 1); v[d] = 1
        if d == 0: out.append(Fraction(Qbar(pibar(u, sigma), q, c, sigma)))
        else:
            w = [a + b for a, b in zip(u, v)]
            out.append(Fraction(Qbar(pibar(w, sigma), q, c, sigma) - Qbar(pibar(u, sigma), q, c, sigma) - Qbar(pibar(v, sigma), q, c, sigma)))
    return out

def group_predicates():
    K = 6
    qual = []; notq = []
    r2 = dict(q=0, p=0, f=0); r3 = dict(q=0, p=0, f=0); r4 = dict(q=0, p=0, f=0)
    r6a = dict(q=0, p=0, f=0); r6b = dict(q=0, p=0, f=0); r6c = dict(q=0, p=0, f=0); r8 = dict(q=0, p=0, f=0)
    info6 = {}
    for G in INST:
        if not G.setup(): notq.append((G.name, G.r, G.s)); continue
        qual.append((G.name, G.r, G.s, G.k0, G.sigma))
        sg = G.sigma; e1 = G.e; b = G.beta
        eta = G.pw(G.delta, (G.r - G.k0) % G.r); etab = G.mul(eta, b)
        fA = [Counter({e1: 4}) + Counter({eta: 1}) + Counter({etab: 1}), Counter({e1: 1}) + Counter({b: 1})]
        fB = [Counter({e1: 1}) + Counter({b: 2}), Counter({e1: 1}) + Counter({b: 2}) + Counter({etab: 1})]
        fC = Counter({e1: 1}) + Counter({b: 1})
        A = G.conv(fA[0], fA[1]); Bm = G.conv(fB[0], fB[1])
        r2['q'] += 1
        if G.tr(b, A) == Bm: r2['p'] += 1
        else: r2['f'] += 1
        def pi_of(factors):
            pi = [1]
            for P in factors:
                e = G.eps(P); pi = polymul(pi, [e[0], e[1]])
            return pi
        def mset(factors):
            m = Counter({e1: 1})
            for P in factors: m = G.conv(m, P)
            return m
        # P3
        ABrows = []
        for d in range(2, 9):
            r3['q'] += 1
            FA = fA + [fC] * (d - 2); FB = fB + [fC] * (d - 2)
            piA = pi_of(FA); piB = pi_of(FB)
            sA = polymul([4 + sg, sg], [1]);
            for _ in range(d - 1): sA = polymul(sA, [1, 1])
            sB = polymul([1, 2], [1, 2 + sg])
            for _ in range(d - 2): sB = polymul(sB, [1, 1])
            ok = all(G.inM01(P) for P in FA + FB) and piA == sA and piB == sB and len(piA) == d + 1 == len(piB)
            ok = ok and piA[0] * piA[d] == sg * (4 + sg) and piB[0] * piB[d] == 2 * (2 + sg) and sg * (4 + sg) != 2 * (2 + sg)
            ok = ok and G.tr(b, mset(FA)) == mset(FB)
            if ok: r3['p'] += 1
            else: r3['f'] += 1
            if d <= K: ABrows.append([x - y for x, y in zip(Sd(piA, K), Sd(piB, K))])
        # factor list
        C01 = [g for g in G.Delta if G.coord[g][0] in (0, 1)]
        fl = [Counter({g: 1}) for g in C01] + [Counter({g: 1}) + Counter({h: 1}) for g, h in itertools.combinations_with_replacement(C01, 2)]
        if len(fl) > 14:
            rr = random.Random(SEED); fl = rr.sample(fl, 14)
        fl += [fA[0], fB[1]]
        groups = {}
        nprod = 0
        for k in range(1, K + 1):
            combos = itertools.combinations_with_replacement(range(len(fl)), k)
            if k >= 5:   # sample to bound time
                rr = random.Random(SEED + k); combos = [tuple(sorted(rr.randrange(len(fl)) for _ in range(k))) for _ in range(4000)]
            for cmb in combos:
                F = [fl[i] for i in cmb]; m = mset(F); pi = pi_of(F); nprod += 1
                r4['q'] += 1
                if G.eps(m) == pibar(pi, sg): r4['p'] += 1
                else: r4['f'] += 1
                groups.setdefault(G.canon(m), set()).add(tuple(Sd(pi, K)))
        for d in range(2, K + 1):
            FA = fA + [fC] * (d - 2); FB = fB + [fC] * (d - 2)
            groups.setdefault(G.canon(mset(FA)), set()).add(tuple(Sd(pi_of(FA), K)))
            groups.setdefault(G.canon(mset(FB)), set()).add(tuple(Sd(pi_of(FB), K)))
        Bs = Basis(K + 1); ncoin = 0
        for key, rows in groups.items():
            rows = list(rows)
            if len(rows) > 1:
                ncoin += 1
                for rw in rows[1:]: Bs.add([x - y for x, y in zip(rw, rows[0])])
        dim_a = K + 1 - Bs.rank()
        Bb = Basis(K + 1)
        for rw in ABrows: Bb.add(rw)
        dim_b = K + 1 - Bb.rank()
        cs = [cstar(1, 0, sg, K), cstar(0, 1, sg, K)]
        okc = all(Bs.contains_in_null(c) for c in cs)
        r6a['q'] += 1; r6b['q'] += 1; r6c['q'] += 1
        r6a['p' if dim_a == 2 else 'f'] += 1; r6b['p' if dim_b == 2 else 'f'] += 1; r6c['p' if okc else 'f'] += 1
        info6[G.name] = {'products': nprod, 'distinct_multisets_up_to_translation': len(groups),
                         'multisets_with_two_different_S_rows': ncoin, 'dim_all': dim_a, 'dim_ABC_only': dim_b,
                         'cstar_q': [str(x) for x in cs[0]], 'cstar_c': [str(x) for x in cs[1]]}
        # P8
        rr = random.Random(SEED + 8)
        C0 = [g for g in G.Delta if G.coord[g][0] == 0]
        for _ in range(500):
            Am = Counter(rr.choice(C0) for _ in range(rr.randint(1, 4)))
            P = Counter(rr.choice(C01) for _ in range(rr.randint(1, 4)))
            AP = G.conv(Am, P); r8['q'] += 1
            eA = G.eps(Am)[0]; eP = G.eps(P); eAP = G.eps(AP)
            ok = G.inM01(AP) and sum(AP.values()) == sum(Am.values()) * sum(P.values()) and eAP[:2] == [eA * eP[0], eA * eP[1]] and eAP[2] == 0
            r8['p' if ok else 'f'] += 1
        A2 = Counter({e1: 2}); r8['q'] += 1
        r8['p' if sum(A2.values()) != G.eps(A2)[0] ** 2 else 'f'] += 1
    RES['instances_qualifying'] = qual; RES['instances_not_qualifying'] = notq
    print('qualifying instances', qual); print('not qualifying', notq)
    rec('P2', r2['q'], r2['p'], r2['f'])
    rec('P3', r3['q'], r3['p'], r3['f'])
    rec('P4', r4['q'], r4['p'], r4['f'])
    rec('P6a', r6a['q'], r6a['p'], r6a['f'], info6)
    rec('P6b', r6b['q'], r6b['p'], r6b['f'])
    rec('P6c', r6c['q'], r6c['p'], r6c['f'])
    rec('P8', r8['q'], r8['p'], r8['f'])

def p5():
    rr = random.Random(SEED + 5); q = p = f = 0
    for sg in (1, -1):
        for (qq, cc) in ((1, 0), (0, 1)):
            for _ in range(2000):
                n = rr.randint(1, 9); pi = [rr.randint(-9, 9) for _ in range(n)]
                q += 1
                if Qbar(pibar([0] + pi, sg), qq, cc, sg) == Qbar(pibar(pi, sg), qq, cc, sg): p += 1
                else: f += 1
            # Gram coefficients depend on j-i only
            K = 9; q += 1; ok = True
            def coef(i, j):
                u = [0] * (K + 1); u[i] = 1; v = [0] * (K + 1); v[j] = 1
                if i == j: return Qbar(pibar(u, sg), qq, cc, sg)
                w = [a + b for a, b in zip(u, v)]
                return Qbar(pibar(w, sg), qq, cc, sg) - Qbar(pibar(u, sg), qq, cc, sg) - Qbar(pibar(v, sg), qq, cc, sg)
            for i in range(K + 1):
                for j in range(i, K + 1):
                    if coef(i, j) != coef(0, j - i): ok = False
            if coef(0, 0) != qq or coef(0, 1) != cc: ok = False
            if ok: p += 1
            else: f += 1
    rec('P5', q, p, f)

def p7():
    x = sp.Symbol('x'); q = p = f = 0; info = {}
    for sg in (1, -1):
        q += 1
        g = None; perd = {}
        for d in range(2, 7):
            piA = sp.expand((4 + sg + sg * x) * (1 + x) ** (d - 1))
            piB = sp.expand((1 + 2 * x) * (1 + (2 + sg) * x) * (1 + x) ** (d - 2))
            Nd = sp.expand(sp.simplify(x ** d * (piA * piA.subs(x, 1 / x) - piB * piB.subs(x, 1 / x))))
            Nd = sp.Poly(sp.together(Nd), x)
            perd[d] = str(sp.factor(Nd.as_expr()))
            g = Nd if g is None else sp.gcd(g, Nd)
        # v2 (after run 1 crashed in nroots): exact decision.  g3 = gcd(g, x^3-sigma); rest = g/g3.
        # PASS iff g3 has degree 3 and rest is a constant times a power of x (then g has no other root at all).
        # If rest is anything else the predicate is recorded FAIL/UNDECIDED with numpy root moduli as information.
        g3 = sp.gcd(g, sp.Poly(x ** 3 - sg, x))
        rest = sp.div(g, g3)[0]
        rest_monomial = len(rest.terms()) == 1
        rest_on_circle = None
        if not rest_monomial:
            import numpy as np
            rest_on_circle = [abs(abs(z) - 1) for z in np.roots([float(c) for c in rest.all_coeffs()])]
        ok = (g3.degree() == 3) and rest_monomial
        info[sg] = {'gcd': str(sp.factor(g.as_expr())), 'N_d_factored': perd, 'gcd_with_x3_minus_sigma_degree': g3.degree(),
                    'rest': str(rest.as_expr()), 'rest_is_monomial': rest_monomial, 'rest_root_distance_from_circle': rest_on_circle}
        if ok: p += 1
        else: f += 1
    rec('P7', q, p, f, info)

# ---------- P9 twist ----------
def run_event(N, gains, masks, mod=6, start=(0, 'R'), startm=None):
    a, b, c, d = gains
    st = {start: Counter({0: 1}) if startm is None else Counter(startm)}
    for A in masks:
        nx = {}
        for (x, rail), m in st.items():
            for step, tgt, g in ((1, 'R', a if rail == 'R' else c), (-1, 'L', b if rail == 'R' else d)):
                y = (x + step) % N
                if y in A:
                    t = nx.setdefault((y, tgt), Counter())
                    for h, n in m.items(): t[(h + g) % mod] += n
        st = nx
    return {k: v for k, v in st.items() if sum(v.values()) > 0}
def conv6(m1, m2):
    out = Counter()
    for g, x in m1.items():
        for h, y in m2.items(): out[(g + h) % 6] += x * y
    return out
def p9():
    rr = random.Random(SEED + 9)
    ra = dict(q=0, p=0, f=0); rn = dict(q=0, p=0, f=0); rc = dict(q=0, p=0, f=0); rd = dict(q=0, p=0, f=0); tried = 0
    first_fail = None
    for _ in range(6000):
        tried += 1
        N = rr.randint(3, 8); gains = [rr.randrange(6) for _ in range(4)]
        T1 = rr.randint(2, 7); T2 = rr.randint(1, 6)
        def rmask(): return {x for x in range(N) if rr.random() < 0.75}
        m1s = [rmask() for _ in range(T1)]; m2s = [rmask() for _ in range(T2)]
        x1 = rr.randrange(N)
        for rail, res in (('R', ra), ('L', rn)):
            ms = [set(A) for A in m1s]
            ms[-1] = {x1}; ms[-2] = ms[-2] & {(x1 - 1) % N if rail == 'R' else (x1 + 1) % N}
            e1 = run_event(N, gains, ms)
            if set(e1) != {(x1, rail)}:
                continue
            m1 = e1[(x1, rail)]
            res['q'] += 1
            e2 = run_event(N, gains, m2s)
            cat = run_event(N, gains, ms + [{(x1 + y) % N for y in A} for A in m2s])
            pred = {((x1 + y) % N, rho): conv6(m1, m) for (y, rho), m in e2.items()}
            if cat == pred: res['p'] += 1
            else:
                res['f'] += 1
                if rail == 'R' and first_fail is None: first_fail = dict(N=N, gains=gains, m1=[sorted(A) for A in ms], m2=[sorted(A) for A in m2s])
            if rail == 'L':
                c = gains[2]; rc['q'] += 1
                ext = run_event(N, gains, ms + [{(x1 + 1) % N}])
                want = {((x1 + 1) % N, 'R'): Counter({(g + c) % 6: n for g, n in m1.items()})}
                rc['p' if ext == want else 'f'] += 1
    # boundary N=2
    for _ in range(300):
        gains = [rr.randrange(6) for _ in range(4)]; T1 = rr.randint(1, 5)
        ms = [{x for x in range(2) if rr.random() < 0.8} for _ in range(T1)]
        e1 = run_event(2, gains, ms)
        for (x1, rail), m1 in e1.items():
            if rail != 'L': continue
            # the L multiset at x1 (cannot be isolated on N=2 by the fginv device); extend from that vertex alone
            rd['q'] += 1
            ext = run_event(2, gains, [{(x1 + 1) % 2}], start=(x1, 'L'), startm=m1)
            want = {((x1 + 1) % 2, 'R'): Counter({(g + gains[2]) % 6: n for g, n in m1.items()})}
            rd['p' if ext == want else 'f'] += 1
    rec('P9a', ra['q'], ra['p'], ra['f'], {'tried': tried, 'first_fail': first_fail})
    rec('P9n_control_expected_fail', rn['q'], rn['p'], rn['f'])
    rec('P9c', rc['q'], rc['p'], rc['f'])
    rec('P9d_boundary_N2_expected_fail', rd['q'], rd['p'], rd['f'])

# ---------- P10 ----------
def p10():
    from sympy.polys.matrices import DomainMatrix
    from sympy import QQ
    info = {}
    def solve(S, use_beta, small=3):
        ms = [m for m in itertools.product(range(S + 1), repeat=4) if 1 <= sum(m) <= S]
        idx = {m: i for i, m in enumerate(ms)}
        rows = []
        def row(terms):
            r = {}
            for m, cf in terms:
                if sum(m) == 0: continue
                r[idx[m]] = r.get(idx[m], 0) + cf
            if any(r.values()): rows.append(r)
        Td = lambda m: (m[1], m[0], m[3], m[2])
        add = lambda u, v: tuple(a + b for a, b in zip(u, v))
        allm = [(0, 0, 0, 0)] + ms
        for m in ms:
            row([(m, 1), (Td(m), -1)])
            if use_beta and m[2] == 0 and m[3] == 0: row([(m, 1), ((0, 0, m[0], m[1]), -1)])
        npairs = 0
        for u in allm:
            for v in allm:
                if sum(u) + sum(v) > S or sum(u) == 0 or sum(v) == 0: continue
                A0 = (v[0] == 0 and v[1] == 0); B0 = (u[2] == 0 and u[3] == 0)
                if A0 or B0:
                    npairs += 1
                    row([(add(u, v), 1), (add(u, Td(v)), 1), (u, -2), (v, -2)])
        n = len(ms)
        M = DomainMatrix([[QQ(r.get(j, 0)) for j in range(n)] for r in rows], (len(rows), n), QQ)
        ns = M.nullspace()
        dim = ns.shape[0]
        smallidx = [idx[m] for m in ms if sum(m) <= small]
        if dim:
            sub = DomainMatrix([[ns[i, j].element for j in smallidx] for i in range(dim)], (dim, len(smallidx)), QQ)
            rdim = sub.rank()
        else: rdim = 0
        # P10b
        def e0(m): return m[0] - m[1]
        def e1(m): return m[2] - m[3]
        ok = True
        for fn in (lambda m: sum(m), lambda m: e0(m) ** 2 + e1(m) ** 2, lambda m: e0(m) * e1(m)):
            vals = [fn(m) for m in ms]
            for r in rows:
                if sum(cf * vals[j] for j, cf in r.items()) != 0: ok = False
        return dict(S=S, unknowns=n, rows=len(rows), pairs=npairs, dim=dim, dim_restricted=rdim, stated_three_are_solutions=ok)
    qa = pa = fa = 0
    for S in (4, 5, 6):
        r = solve(S, True); info[f'S={S}'] = r
    qa = 1; pa = int(info['S=6']['dim_restricted'] == 3); fa = 1 - pa
    rec('P10a', qa, pa, fa, info)
    okb = all(v['stated_three_are_solutions'] for v in info.values())
    rec('P10b', 3, 3 if okb else 0, 0 if okb else 3)
    r = solve(6, False)
    rec('P10c_info_no_Tbeta', 1, int(r['dim_restricted'] == 5), int(r['dim_restricted'] != 5), r)

t0 = time.time()
try:
    p1(); group_predicates(); p5(); p7(); p9(); p10()
    RES['completed'] = True
except Exception as ex:
    import traceback; traceback.print_exc()
    RES['completed'] = False; RES['error'] = repr(ex)
RES['seconds'] = round(time.time() - t0, 1)
json.dump(RES, fh, indent=1, default=str); fh.close()
sys.exit(0 if RES['completed'] else 2)
