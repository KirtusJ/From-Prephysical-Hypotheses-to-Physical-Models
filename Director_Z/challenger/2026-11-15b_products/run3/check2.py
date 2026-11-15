#!/usr/bin/env python3
"""Challenger program, run 2 (continuation of run 1, which ended with exit code 2 in its P7).
Targets: lem:symquad, thm:fgthree (family |pi(u)|^2), lem:twist, lem:twolevelabs (draft G10 winding products).
Usage: python3 check2.py <result_file> [seed=20261115]
Result file opened with mode 'x' (never overwritten). Exit code 0 = ran to the end; read the result file.

PREDICATES, FIXED BEFORE THE FIRST RUN OF THIS FILE.  Each reports qualifying / pass / fail.

Q1 (lem:symquad), k=2,3,4.  d_sym := dimension of the space of polynomials in p^(1..k) in R^2 that are
    quadratic forms in each p^(i) and invariant under every transposition (i,i+1): computed by writing a
    general multi-quadratic polynomial with 3^k unknown coefficients, substituting the swapped arguments,
    and taking the exact nullity of the linear conditions (no orbit count, no formula).
    d_span := exact rank of {pi_i pi_j : 0<=i<=j<=k};  d_union := rank of (basis of sym space) u {pi_i pi_j}.
    Hypothesis per instance: every pi_i pi_j is multi-quadratic (checked).  PASS iff d_sym == d_span == d_union.
Q2 (thm:fgthree, family c_0=1, c_d=2Re u^d, i.e. |pi(u)|^2 on |u|=1), sigma = +1, -1.
    N_d(x) = x^d (pi_A(x) pi_A(1/x) - pi_B(x) pi_B(1/x)), d=2..8, pi_A=(4+s+sX)(1+X)^(d-1),
    pi_B=(1+2X)(1+(2+s)X)(1+X)^(d-2).  Hypothesis per d: N_d palindromic of degree <= 2d (checked).
    Convert N_d(x)/x^d to R_d(t), t=cos(theta), via x^j+x^-j = 2 T_j(t) (exact, rational).
    PASS iff the set of real roots in [-1,1] of gcd(R_2..R_8) (exact isolation, sympy real_roots) equals
    the set for x^3 - sigma, i.e. {1,-1/2} for sigma=1 and {-1,1/2} for sigma=-1.
    Q2-perd (information): the same set for each d alone.
Q3 (lem:twist) as P9 of run 1: rings N=3..8, gains in Z_6, S1 forced to end at one vertex (x1,R).
    Q3a concatenation identity; Q3n control with S1 ending at (x1,L): EXPECTED TO FAIL in some instances;
    Q3c last sentence (N>=3): m1 alone on L at x1, mask {x1+1}: T_c m1 alone at (x1+1,R);
    Q3d boundary N=2 version of Q3c from a (x1,L) multiset that is NOT isolated: expected to fail sometimes.
Q4 (lem:twolevelabs, truncated) r in {2,3}, group <delta> x {1,beta} written as pairs (coset j, exponent n).
    Unknowns f(m), 1<=|m|<=S (S=6 for r=2, S=5 for r=3), constraints: T_delta invariance, f(m)=f(T_beta m)
    for m in M(C0), eq:fgQ at (A0) [v in M(C1)] and (B0) [u in M(C0)] with |u|+|v|<=S, u or v may be empty.
    Q4a: dimension of the solution space restricted to |m|<=3 is 3 for r=2 and 1 for r=3.
    Q4b: |m| is a solution (both r); eps0^2+eps1^2 and eps0*eps1 are solutions for r=2.
    Q4c (information, r=2): without the T_beta hypothesis the restricted dimension (expected 5: q0,q0',c,
    alpha_0, alpha_1).  Truncation can only add solutions near the cut; restricted dims are the predicate.
"""
import sys, json, itertools, random, time
from collections import Counter
import sympy as sp

OUT = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261115
random.seed(SEED)
fh = open(OUT, 'x')
RES = {'seed': SEED, 'argv': sys.argv, 'predicates': {}}
def rec(name, qual, passed, failed, info=None):
    RES['predicates'][name] = {'qualify': qual, 'pass': passed, 'fail': failed, 'info': info}
    print(name, 'qualify', qual, 'pass', passed, 'fail', failed, info if info is not None else '', flush=True)

def q1():
    q = p = f = 0; info = {}
    for k in (2, 3, 4):
        P = [(sp.Symbol(f'a{i}'), sp.Symbol(f'b{i}')) for i in range(k)]
        gens = [s for pr in P for s in pr]
        mons1 = lambda a, b: [a * a, a * b, b * b]
        types = list(itertools.product(range(3), repeat=k))
        coef = sp.symbols(f'z0:{len(types)}')
        def build(args):
            return sum(cf * sp.prod([mons1(*args[i])[t[i]] for i in range(k)]) for cf, t in zip(coef, types))
        T = sp.expand(build(P))
        eqs = []
        for i in range(k - 1):
            Q = list(P); Q[i], Q[i + 1] = Q[i + 1], Q[i]
            D = sp.Poly(sp.expand(build(Q) - T), *gens)
            eqs += [c for c in D.coeffs()]
        A = sp.Matrix([[sp.diff(e, z) for z in coef] for e in eqs]) if eqs else sp.zeros(0, len(coef))
        ns = A.nullspace()
        d_sym = len(ns)
        # basis of sym space as coefficient vectors in the monomial basis
        X = sp.Symbol('X')
        prod = sp.Poly(sp.expand(sp.prod([a + b * X for a, b in P])), X)
        pi = [prod.coeff_monomial(X ** i) for i in range(k + 1)]
        expo = {t: tuple(e for ti in t for e in ((2, 0), (1, 1), (0, 2))[ti]) for t in types}
        inv = {v: t for t, v in expo.items()}
        rows = []; mq = True
        for i in range(k + 1):
            for j in range(i, k + 1):
                Pl = sp.Poly(sp.expand(pi[i] * pi[j]), *gens)
                vec = dict.fromkeys(types, 0)
                for mon, co in Pl.terms():
                    if mon not in inv: mq = False; continue
                    vec[inv[mon]] = co
                rows.append([vec[t] for t in types])
        d_span = sp.Matrix(rows).rank()
        symrows = [list(v) for v in ns]
        d_union = sp.Matrix(rows + symrows).rank()
        q += 1
        ok = mq and d_sym == d_span == d_union
        info[k] = dict(d_sym=d_sym, d_span=d_span, d_union=d_union, pairs=len(rows), multiquad=mq, conditions=len(eqs))
        if ok: p += 1
        else: f += 1
    rec('Q1', q, p, f, info)

def q2():
    x, t = sp.symbols('x t'); q = p = f = 0; info = {}
    for sg in (1, -1):
        q += 1; g = None; perd = {}; hyp = True
        for d in range(2, 9):
            piA = sp.expand((4 + sg + sg * x) * (1 + x) ** (d - 1))
            piB = sp.expand((1 + 2 * x) * (1 + (2 + sg) * x) * (1 + x) ** (d - 2))
            Nd = sp.Poly(sp.expand(sp.cancel(x ** d * (piA * piA.subs(x, 1 / x) - piB * piB.subs(x, 1 / x)))), x)
            cl = Nd.all_coeffs()[::-1]  # cl[j] = coeff of x^j
            cl += [0] * (2 * d + 1 - len(cl))
            if len(cl) > 2 * d + 1 or any(cl[j] != cl[2 * d - j] for j in range(2 * d + 1)): hyp = False
            R = cl[d] + sum(2 * cl[d + j] * sp.chebyshevt(j, t) for j in range(1, d + 1))
            R = sp.Poly(sp.expand(R), t)
            rr = sorted(set(r for r in sp.real_roots(R) if -1 <= r <= 1)) if R.degree() > 0 else 'R_d constant'
            perd[d] = [str(r) for r in rr] if not isinstance(rr, str) else rr
            g = R if g is None else sp.gcd(g, R)
        roots = sorted(set(r for r in sp.real_roots(g) if -1 <= r <= 1)) if g.degree() > 0 else []
        want = sorted([sp.Integer(1), sp.Rational(-1, 2)]) if sg == 1 else sorted([sp.Integer(-1), sp.Rational(1, 2)])
        ok = hyp and roots == want
        info[sg] = dict(palindromic_hypothesis=hyp, gcd_t=str(sp.factor(g.as_expr())), roots_in_unit_interval=[str(r) for r in roots],
                        want=[str(r) for r in want], per_d=perd)
        if ok: p += 1
        else: f += 1
    rec('Q2', q, p, f, info)

# ---- Q3: copied from run 1 (P9), unchanged logic ----
def run_event(N, gains, masks, mod=6, start=(0, 'R'), startm=None):
    a, b, c, d = gains
    st = {start: Counter({0: 1}) if startm is None else Counter(startm)}
    for A in masks:
        nx = {}
        for (x, rail), m in st.items():
            for step, tgt, g in ((1, 'R', a if rail == 'R' else c), (-1, 'L', b if rail == 'R' else d)):
                y = (x + step) % N
                if y in A:
                    tt = nx.setdefault((y, tgt), Counter())
                    for h, n in m.items(): tt[(h + g) % mod] += n
        st = nx
    return {k: v for k, v in st.items() if sum(v.values()) > 0}
def conv6(m1, m2):
    out = Counter()
    for g, x in m1.items():
        for h, y in m2.items(): out[(g + h) % 6] += x * y
    return out
def q3():
    rr = random.Random(SEED + 9)
    ra = dict(q=0, p=0, f=0); rn = dict(q=0, p=0, f=0); rc = dict(q=0, p=0, f=0); rd = dict(q=0, p=0, f=0); tried = 0
    first_fail = {}
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
            if set(e1) != {(x1, rail)}: continue
            m1 = e1[(x1, rail)]
            res['q'] += 1
            e2 = run_event(N, gains, m2s)
            cat = run_event(N, gains, ms + [{(x1 + y) % N for y in A} for A in m2s])
            pred = {((x1 + y) % N, rho): conv6(m1, m) for (y, rho), m in e2.items()}
            if cat == pred: res['p'] += 1
            else:
                res['f'] += 1
                first_fail.setdefault(rail, dict(N=N, gains=gains, m1=[sorted(A) for A in ms], m2=[sorted(A) for A in m2s]))
            if rail == 'L':
                c = gains[2]; rc['q'] += 1
                ext = run_event(N, gains, ms + [{(x1 + 1) % N}])
                want = {((x1 + 1) % N, 'R'): Counter({(g + c) % 6: n for g, n in m1.items()})}
                rc['p' if ext == want else 'f'] += 1
    for _ in range(300):
        gains = [rr.randrange(6) for _ in range(4)]; T1 = rr.randint(1, 5)
        ms = [{x for x in range(2) if rr.random() < 0.8} for _ in range(T1)]
        e1 = run_event(2, gains, ms)
        for (x1, rail), m1 in e1.items():
            if rail != 'L': continue
            rd['q'] += 1
            ext = run_event(2, gains, ms + [{(x1 + 1) % 2}])
            want = {((x1 + 1) % 2, 'R'): Counter({(g + gains[2]) % 6: n for g, n in m1.items()})}
            rd['p' if ext == want else 'f'] += 1
    rec('Q3a', ra['q'], ra['p'], ra['f'], {'tried': tried, 'first_fail_R': first_fail.get('R')})
    rec('Q3n_control_expected_fail', rn['q'], rn['p'], rn['f'], {'first_fail_L': first_fail.get('L')})
    rec('Q3c', rc['q'], rc['p'], rc['f'])
    rec('Q3d_boundary_N2_not_isolated_expected_fail', rd['q'], rd['p'], rd['f'])

# ---- Q4 ----
def q4():
    from sympy.polys.matrices import DomainMatrix
    from sympy import QQ
    def solve(r, S, use_beta, small=3):
        n_el = 2 * r     # index j*r + n  <->  beta^j delta^n
        ms = [m for m in itertools.product(range(S + 1), repeat=n_el) if 1 <= sum(m) <= S]
        idx = {m: i for i, m in enumerate(ms)}
        Td = lambda m: tuple(m[j * r + ((n - 1) % r)] for j in range(2) for n in range(r))
        add = lambda u, v: tuple(a + b for a, b in zip(u, v))
        zero = tuple([0] * n_el)
        rows = set()
        def row(terms):
            dct = {}
            for m, cf in terms:
                if sum(m) == 0: continue
                dct[idx[m]] = dct.get(idx[m], 0) + cf
            dct = tuple(sorted((k, v) for k, v in dct.items() if v != 0))
            if dct: rows.add(dct)
        for m in ms:
            row([(m, 1), (Td(m), -1)])
            if use_beta and sum(m[r:]) == 0: row([(m, 1), (tuple([0] * r) + m[:r], -1)])
        allm = [zero] + ms
        for u in allm:
            for v in allm:
                if sum(u) + sum(v) > S or (sum(u) == 0 and sum(v) == 0): continue
                A0 = sum(v[:r]) == 0; B0 = sum(u[r:]) == 0
                if A0 or B0:
                    row([(add(u, v), 1), (add(u, Td(v)), 1), (u, -2), (v, -2)])
        rows = list(rows); n = len(ms)
        M = DomainMatrix([[QQ(dict(rw).get(j, 0)) for j in range(n)] for rw in rows], (len(rows), n), QQ)
        ns = M.nullspace(); dim = ns.shape[0]
        smallidx = [idx[m] for m in ms if sum(m) <= small]
        rdim = DomainMatrix([[ns[i, j].element for j in smallidx] for i in range(dim)], (dim, len(smallidx)), QQ).rank() if dim else 0
        e = lambda m, j: sum((-1) ** nn * m[j * r + nn] for nn in range(r))
        fns = {'count': lambda m: sum(m)}
        if r % 2 == 0:
            fns['sq'] = lambda m: e(m, 0) ** 2 + e(m, 1) ** 2
            fns['mix'] = lambda m: e(m, 0) * e(m, 1)
        sols = {}
        for name, fn in fns.items():
            vals = [fn(m) for m in ms]
            sols[name] = all(sum(cf * vals[j] for j, cf in rw) == 0 for rw in rows)
        return dict(r=r, S=S, use_beta=use_beta, unknowns=n, rows=len(rows), dim=dim, dim_restricted=rdim, stated_solutions=sols)
    res2 = solve(2, 6, True); res3 = solve(3, 5, True)
    qa = 2; pa = int(res2['dim_restricted'] == 3) + int(res3['dim_restricted'] == 1)
    rec('Q4a', qa, pa, qa - pa, {'r2': res2, 'r3': res3})
    sb = list(res2['stated_solutions'].values()) + list(res3['stated_solutions'].values())
    rec('Q4b', len(sb), sum(sb), len(sb) - sum(sb))
    rc = solve(2, 6, False)
    rec('Q4c_info_no_Tbeta', 1, int(rc['dim_restricted'] == 5), int(rc['dim_restricted'] != 5), rc)

t0 = time.time()
try:
    q1(); q2(); q3(); q4()
    RES['completed'] = True
except Exception as ex:
    import traceback; traceback.print_exc()
    RES['completed'] = False; RES['error'] = repr(ex)
RES['seconds'] = round(time.time() - t0, 1)
json.dump(RES, fh, indent=1, default=str); fh.close()
sys.exit(0 if RES['completed'] else 2)
