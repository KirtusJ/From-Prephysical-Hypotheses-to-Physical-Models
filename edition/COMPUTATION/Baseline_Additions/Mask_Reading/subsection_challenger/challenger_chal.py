#!/usr/bin/env python3
"""Challenger program for the draft subsection "What position masks read of a character".
Written from the definitions in the .tex only. Exact arithmetic: characters take values zeta_K^e,
amplitudes are integer vectors over exponents mod K (Z[x]/(x^K-1)); equality is tested after
reduction modulo the K-th cyclotomic polynomial (integer vectors of length phi(K)). Starts are
(A,B,den) with A,B in Z[zeta_K]; every probability is compared scaled by 2^t*den^2. No floats.
Seed 20261114. Result file opened with mode 'x' (never overwritten).

PREDICATES (fixed before the first run). "qual" = cases satisfying the statement's hypothesis.
 C0    control: Z/4, chi(a,b,c,d)=(1,1,i,-i), start (1,1)/sqrt2, port (3,3,L), brute words: P == 1/4.
 L1    Lemma, first formula as group elements, every word of length 0..7, 40 carriers (no hypothesis).
 L2    Lemma, second formula, same words.
 L3    m' = m+1 iff first step is left.
 I1/I2 (i) ports (3,1,R): 8P=4|alpha|^2 ; (3,-1,L): 8P=4|beta|^2. N=3..10, hypothesis eta=-1 per case.
 I1n2/I2n2  same on N=1,2 (outside hypothesis; expected to fail; kept), sharp starts counted apart (I1n2s).
 II1/II2 (ii). II1 also for any eta (II1any).
 F1    fork: admitted words ending at port are exactly R^{M+1}, L^M R (N=3..10).
 III   fork formula (S_{M+1}={M+1} included), any start. IIIn2: same on N=1,2 (outside hypothesis).
 IV    fork after one tick formula. IVm: mirror (x->-x, rails exchanged, S_1={-1}, port (M+2,-M-2,L)).
 IVn2/IVmn2 same on N=1,2 (outside hypothesis).
 ETA   N>=3, sharp alpha=1, no mask, port (3,-1,L): 8P == 2+eta+conj(eta) for every carrier (any eta).
       (If it passes, a position-mask port reads Re eta, against Remark (a) "not measured by these events".)
 N2a   N=1,2, eta=-1: P_R+P_L at the one occupied site, no mask, every length 1..6, equals n.
 N2b   same with eta != -1 (outside hypothesis; expected to fail).
 N2c   N=1,2, any eta, sharp: port (2,2 mod N,R): 4P = |alpha|^2 (2+u+conj u).
 Ra    for K<=120 and all K-th roots u,u': (Re u^M=Re u'^M for M=2,3,5) => u' in {u,conj u}. Also which
       proper subsets of {2,3,5} fail (informative).
 Rb    for 2<=M1,M2<=10: the proof's construction gives u' != u, u' != conj u, equal real parts for both.
 Rc    q<=60, M<=12, gcd(M,q)=1: Re u^M = Re u'^M => u' in {u,conj u}; and count failures when gcd>1.
 PREP1 eta real, sharp alpha=1, random events, every site: conj(psi_R) psi_L gamma equal for carrier
       (a,b,c,d) and (a,b/g,cg,d) (same B,H; gamma changed), and for (ag,bg,cg,dg).
 PREP2 amplitude identity: event with S_t={x} continued by r masks == start psi_R|x,R>+psi_L|x,L>
       (unnormalised sums) run through the continuation. PREP2f: is the factor between the two
       probabilities 1 (literal reading "the later statistics are those of the start")? expected fail t>=1.
 LINE  "line" = ring N=17 with t<=6 (no word can wind): P unchanged when (b,d)->(bg,dg) for any g
       (u changes, eta, gamma unchanged), eta real.
 DP    vectorised dynamic programme == brute word enumeration on all events to length 3 (N=3,4).
 INV   exhaustive masks (N=3 to length 5, N=4 to 4, N=5 to 3 plus named events), eta real, any start:
       equal (|alpha|^2,|beta|^2,eta,Re omega,Re kappa,Im omega Im kappa) => equal statistics.
 LIST  same events, eta=-1 and n=1: equal 4-tuple <=> equal statistics (both directions, all pairs).
 SHARP eta=-1, sharp |alpha|=1: equal statistics <=> equal Re omega; ports of length <= M all equal;
       fork port differs exactly when Re omega differs.
 CONJ  eta=-1,n=1: chi vs conj chi equal statistics <=> (Im(conj(alpha)beta)=0 or (gamma=+-1 and omega=+-1)).
 FAIR  (informative) non-sharp n=1 data with Re omega != 0 and fork P = 2^-M: count.
"""
import sys, os, itertools, random, hashlib
from math import gcd
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols

SEED = 20261114
out_path = sys.argv[1]
OUT = open(out_path, 'x')
def say(s):
    OUT.write(s + '\n'); OUT.flush(); print(s)

TAB = {}
def rec(name, ok, info=None):
    q, p, f, ex = TAB.setdefault(name, [0, 0, 0, []])
    TAB[name][0] += 1
    if ok: TAB[name][1] += 1
    else:
        TAB[name][2] += 1
        if len(TAB[name][3]) < 3 and info is not None: TAB[name][3].append(info)

class Ctx:
    def __init__(s, K):
        s.K = K
        x = symbols('x')
        c = [int(v) for v in Poly(cyclotomic_poly(K, x), x).all_coeffs()][::-1]
        d = len(c) - 1; s.phi = d
        R = np.zeros((K, d), dtype=np.int64)
        cur = [0] * d; cur[0] = 1
        for j in range(K):
            R[j] = cur
            top = cur[-1]; cur = [0] + cur[:-1]
            if top: cur = [cur[i] - top * c[i] for i in range(d)]
        s.R = R
    def root(s, e):
        v = np.zeros(s.K, dtype=np.int64); v[e % s.K] = 1; return v
    def mul(s, a, b):
        assert int(np.abs(a).max()) * int(np.abs(b).max()) * s.K < 2 ** 62
        c = np.convolve(a, b); r = c[:s.K].copy(); r[:s.K - 1] += c[s.K:]; return r
    def conj(s, a): return np.roll(a[::-1], 1)
    def canon(s, a): return tuple(int(v) for v in a @ s.R)
    def zero(s, a): return not np.any(a @ s.R)
    def eq(s, a, b): return s.zero(a - b)
    def circ(s, A):
        K = s.K; return np.array([[A[(j - i) % K] for j in range(K)] for i in range(K)], dtype=np.int64)

# ---------- carriers ----------
def rand_carrier(rng, K, steer):
    """steer: None = d random; else desired eta exponent (try to reach it by changing d)."""
    divs = [n for n in range(2, K + 1) if K % n == 0]
    r = rng.choice([1, 2, 3]); ns = [rng.choice(divs) for _ in range(r)]
    ks = [rng.randrange(n) for n in ns]
    el = lambda: tuple(rng.randrange(n) for n in ns)
    chi = lambda g: sum(k * gi * (K // n) for k, gi, n in zip(ks, g, ns)) % K
    a, b, c, d = el(), el(), el(), el()
    if steer is not None:
        for _ in range(300):
            if (chi(a) + chi(d) - chi(b) - chi(c)) % K == steer: break
            d = el()
    return dict(ns=ns, ks=ks, g=(a, b, c, d), e=tuple(chi(z) for z in (a, b, c, d)))
def derived(e, K):
    ea, eb, ec, ed = e
    return dict(eB=(eb + ec - 2 * ea) % K, eH=(ea + ed - eb - ec) % K, eg=(ec - ea) % K)

# ---------- brute word enumeration ----------
def enum_ports(N, e, masks, K, want_words=False):
    """masks: list of (set of sites mod N) or None. Returns {(x,rail):(vR,vL)}, rail 0=R,1=L.
    N=None is not used; the line is modelled by a long ring."""
    ea, eb, ec, ed = e; t = len(masks); res = {}; words = {}
    if t == 0:
        z = np.zeros(K, dtype=np.int64); o = z.copy(); o[0] = 1
        return {(0, 0): (o, z.copy()), (0, 1): (z.copy(), o.copy())}
    for w in itertools.product((0, 1), repeat=t):  # 0 = right step, 1 = left step
        x = 0; ok = True; gR = gL = 0; rail = None
        for j, st in enumerate(w):
            if j == 0:
                gR = ea if st == 0 else eb; gL = ec if st == 0 else ed
            else:
                g = (ea if rail == 0 else ec) if st == 0 else (eb if rail == 0 else ed)
                gR += g; gL += g
            x = (x + (1 if st == 0 else -1)) % N; rail = st
            if masks[j] is not None and x not in masks[j]: ok = False; break
        if not ok: continue
        key = (x, rail)
        if key not in res: res[key] = (np.zeros(K, dtype=np.int64), np.zeros(K, dtype=np.int64))
        res[key][0][gR % K] += 1; res[key][1][gL % K] += 1
        words.setdefault(key, []).append(w)
    return (res, words) if want_words else res

def pnum(cx, st, vv):
    """2^t * den^2 * P as cyclotomic integer vector."""
    A, B, den = st
    if vv is None: return np.zeros(cx.K, dtype=np.int64)
    amp = cx.mul(A, vv[0]) + cx.mul(B, vv[1]); return cx.mul(amp, cx.conj(amp))

def quantities(cx, st, e, N):
    K = cx.K; A, B, den = st; D = derived(e, K); M = N // gcd(N, 2)
    aa = cx.mul(A, cx.conj(A)); bb = cx.mul(B, cx.conj(B))
    kap = cx.mul(cx.mul(cx.conj(A), B), cx.root(D['eg']))
    w = cx.root(M * D['eB'])
    rk2 = kap + cx.conj(kap)                    # 2 Re kappa * den^2
    rw2 = w + cx.conj(w)                        # 2 Re omega
    ii = -cx.mul(w - cx.conj(w), kap - cx.conj(kap))   # 4 Im omega Im kappa * den^2
    s = (-1) ** (M - 1)
    return dict(aa=aa, bb=bb, nn=aa + bb, rk2=rk2, rw2=rw2, ii=ii, s=s, M=M, **D)

def starts(cx, rng, normalized_only=False):
    K = cx.K; r = lambda: cx.root(rng.randrange(K)); z = np.zeros(K, dtype=np.int64)
    L = [(cx.root(0), z.copy(), 1), (r(), z.copy(), 1), (z.copy(), r(), 1),
         (3 * r(), 4 * r(), 5), (4 * r(), 3 * r(), 5), (5 * r(), 12 * r(), 13)]
    if K % 12 == 0:
        s3 = cx.root(K // 12) + cx.root(-K // 12)
        L.append((r(), cx.mul(s3, r()), 2)); L.append((cx.mul(s3, r()), r(), 2))
    if K % 8 == 0:
        s2 = cx.root(K // 8) + cx.root(-K // 8)
        L.append((cx.mul(s2, r()), cx.mul(s2, r()), 2))
    if not normalized_only:
        L.append((2 * r() + r(), r() - 3 * r(), 1)); L.append((r() + r(), 2 * r(), 3)); L.append((3 * r(), z.copy(), 1))
    return L
def is_norm(cx, st):
    A, B, den = st
    return cx.eq(cx.mul(A, cx.conj(A)) + cx.mul(B, cx.conj(B)), den * den * cx.root(0))

rng = random.Random(SEED)

# ================= C0 control =================
cx4 = Ctx(8)
e_ctl = (0, 0, 2, 6)  # exponents of zeta_8: 1,1,i,-i
res = enum_ports(4, e_ctl, [None] * 3, 8)
s2 = cx4.root(1) + cx4.root(-1)
pv = pnum(cx4, (s2, s2, 2), res.get((3, 1)))       # 2^3 * 4 * P
say("C0 control: 32*P as cyclotomic vector canon = %s ; expected 8 (P=1/4)" % (cx4.canon(pv),))
rec('C0', cx4.eq(pv, 8 * cx4.root(0)))

# ================= Lemma =================
def gadd(ns, *terms):
    return tuple(sum(c * g[i] for c, g in terms) % n for i, n in enumerate(ns))
for _ in range(40):
    car = rand_carrier(rng, 120, None); ns = car['ns']; a, b, c, d = car['g']
    Bg = gadd(ns, (1, b), (1, c), (-2, a)); Hg = gadd(ns, (1, a), (1, d), (-1, b), (-1, c))
    for t in range(0, 8):
        for w in itertools.product((0, 1), repeat=t):
            def walk(rail0):
                rail = rail0; G = tuple(0 for _ in ns); m = 0
                for st in w:
                    g = (a if rail == 0 else c) if st == 0 else (b if rail == 0 else d)
                    if rail == 1 and st == 1: m += 1
                    G = gadd(ns, (1, G), (1, g)); rail = st
                return G, m, rail
            GR, m, eR = walk(0); GL, mp, eL = walk(1); l = sum(w)
            F1_ = gadd(ns, (t, a), (eR, a), (-eR, c), (l, Bg), (m, Hg))
            F2_ = gadd(ns, (1, c), (-1, a), (t, a), (eL, a), (-eL, c), (l, Bg), (mp, Hg))
            rec('L1', GR == F1_, (car, w)); rec('L2', GL == F2_, (car, w))
            if t >= 1: rec('L3', mp == m + (1 if w[0] == 1 else 0), (w,))

# ================= named formulas =================
def fork_masks(N, M, shift=0, sign=1):
    ms = [{(sign * (shift + j)) % N, (sign * (shift - j)) % N} for j in range(1, M)]
    ms.append({(sign * (shift + M)) % N}); ms.append({(sign * (shift + M + 1)) % N}); return ms
def named_tests(N, K, ncar, tag):
    cx = Ctx(K)
    for i in range(ncar):
        mode = i % 4
        car = rand_carrier(rng, K, [K // 2, K // 2, None, 0][mode]); e = car['e']
        D = derived(e, K); hyp = (D['eH'] == K // 2)
        M = N // gcd(N, 2)
        nm = enum_ports(N, e, [None] * 3, K); n1 = enum_ports(N, e, [None], K)
        fk, fkw = enum_ports(N, e, fork_masks(N, M), K, True)
        ft = enum_ports(N, e, [{1 % N}] + fork_masks(N, M, 1), K)
        fm = enum_ports(N, e, [{(-1) % N}] + fork_masks(N, M, 1, -1), K)
        if N >= 3:
            ws = sorted(fkw.get(((M + 1) % N, 0), []))
            rec('F1', ws == sorted([tuple([0] * (M + 1)), tuple([1] * M + [0])]) and len(fkw) == 1, (N, e, ws))
        sts = starts(cx, rng)
        for st in sts:
            q = quantities(cx, st, e, N); A, B, den = st; s = q['s']
            sharp = not np.any(B)
            two = 2 * cx.root(0)
            c1 = cx.eq(pnum(cx, st, nm.get((1 % N, 0))), 4 * q['aa'])
            c2 = cx.eq(pnum(cx, st, nm.get(((-1) % N, 1))), 4 * q['bb'])
            c3 = cx.eq(pnum(cx, st, n1.get((1 % N, 0))), q['nn'] + q['rk2'])
            c4 = cx.eq(pnum(cx, st, n1.get(((-1) % N, 1))), q['nn'] - q['rk2'])
            f = cx.mul(q['aa'], two + s * q['rw2']) + cx.mul(q['bb'], two - s * q['rw2']) + s * q['ii']
            c5 = cx.eq(pnum(cx, st, fk.get(((M + 1) % N, 0))), f)
            c6 = cx.eq(pnum(cx, st, ft.get(((M + 2) % N, 0))), cx.mul(q['nn'] + q['rk2'], two + s * q['rw2']))
            c7 = cx.eq(pnum(cx, st, fm.get(((-M - 2) % N, 1))), cx.mul(q['nn'] - q['rk2'], two + s * q['rw2']))
            info = (N, car['ns'], e, 'den=%d' % den, 'sharp' if sharp else 'both', 'n=1' if is_norm(cx, st) else 'n!=1')
            if N >= 3:
                rec('II1any', c3, info)
                if sharp and den == 1 and cx.eq(A, cx.root(0)):
                    eta = cx.root(D['eH'])
                    rec('ETA', cx.eq(pnum(cx, st, nm.get(((-1) % N, 1))), two + eta + cx.conj(eta)), info)
                if hyp:
                    nn_ = '' if is_norm(cx, st) else '_n!=1'
                    for nmn, cc in (('I1', c1), ('I2', c2), ('II1', c3), ('II2', c4), ('III', c5), ('IV', c6), ('IVm', c7)):
                        rec(nmn, cc, info); rec(nmn + nn_ if nn_ else nmn + '_n=1', cc, info)
                else:
                    for nmn, cc in (('I1_etaNot-1', c1), ('I2_etaNot-1', c2), ('III_etaNot-1', c5)): rec(nmn, cc, info)
            else:
                if hyp:
                    for nmn, cc in (('I1n2', c1), ('I2n2', c2), ('II1n2', c3), ('II2n2', c4), ('IIIn2', c5), ('IVn2', c6), ('IVmn2', c7)):
                        rec(nmn, cc, info)
                        if sharp: rec(nmn + 's(sharp)', cc, info)
                # N2
                u = cx.root(D['eB'])
                if sharp:
                    r2 = enum_ports(N, e, [None, None], K)
                    rec('N2c', cx.eq(pnum(cx, st, r2.get((2 % N, 0))), cx.mul(q['aa'], two + u + cx.conj(u))), info)
                for t in range(1, 7):
                    rr = enum_ports(N, e, [None] * t, K); x = t % N
                    tot = pnum(cx, st, rr.get((x, 0))) + pnum(cx, st, rr.get((x, 1)))
                    rec('N2a' if hyp else 'N2b', cx.eq(tot, (2 ** t) * q['nn']), info + (t,))
for N in range(3, 11): named_tests(N, 120, 24, 'ring')
for N in (1, 2): named_tests(N, 120, 24, 'small')
say("named formulas done")

# ================= Prop rings =================
def reeq(K, m, mp): return (m - mp) % K == 0 or (m + mp) % K == 0
bad_a = 0; tot_a = 0; sub_fail = {}
for K in range(1, 121):
    for j in range(K):
        for jp in range(K):
            for name, Ms in (('235', (2, 3, 5)), ('23', (2, 3)), ('25', (2, 5)), ('35', (3, 5))):
                if all(reeq(K, M * j, M * jp) for M in Ms):
                    good = reeq(K, j, jp)
                    if name == '235':
                        tot_a += 1; rec('Ra', good, (K, j, jp))
                    elif not good and name not in sub_fail: sub_fail[name] = (K, j, jp)
say("Ra: qualifying pairs %d ; first counterexamples for proper subsets (K,j,j'): %s" % (tot_a, sub_fail))
for M1 in range(2, 11):
    for M2 in range(2, 11):
        K = 2 * M1 * M2
        # eps = zeta^(K/M1), tau = zeta^(K/M2), u^2 = tau/eps: u = zeta^j with 2j = K/M2-K/M1 mod K
        de = (K // M2 - K // M1) % K; assert de % 2 == 0
        j = de // 2; jp = (j + K // M1) % K
        ok = (jp - j) % K != 0 and (jp + j) % K != 0 and reeq(K, M1 * j, M1 * jp) and reeq(K, M2 * j, M2 * jp)
        rec('Rb', ok, (M1, M2, K, j, jp))
gfail = 0
for q in range(1, 61):
    for M in range(1, 13):
        for j in range(q):
            for jp in range(q):
                if reeq(q, M * j, M * jp):
                    if gcd(M, q) == 1: rec('Rc', reeq(q, j, jp), (q, M, j, jp))
                    elif not reeq(q, j, jp): gfail += 1
say("Rc: pairs failing when gcd(M,q)>1 (outside hypothesis, informative): %d" % gfail)

# ================= PREP, LINE =================
def rand_masks(rng, N, t, last=None):
    ms = []
    for j in range(t):
        if rng.random() < 0.35: ms.append(None)
        else: ms.append({x for x in range(N) if rng.random() < 0.6} or {rng.randrange(N)})
    if last is not None: ms[-1] = {last}
    return ms
K = 24; cx = Ctx(K)
for it in range(400):
    N = rng.choice([3, 4, 5, 6, 7]); t = rng.randrange(1, 7)
    car = rand_carrier(rng, K, rng.choice([K // 2, 0, None])); e = car['e']; D = derived(e, K)
    if D['eH'] not in (0, K // 2):
        rec('PREP_not_qualifying(eta not real)', True); continue
    g = rng.randrange(1, K); h = rng.randrange(K)
    e2 = (e[0], (e[1] - g) % K, (e[2] + g) % K, e[3]); e3 = tuple((v + h) % K for v in e)
    assert derived(e2, K)['eB'] == D['eB'] and derived(e2, K)['eH'] == D['eH'] and derived(e2, K)['eg'] != D['eg']
    ms = rand_masks(rng, N, t)
    r1 = enum_ports(N, e, ms, K); r2 = enum_ports(N, e2, ms, K); r3 = enum_ports(N, e3, ms, K)
    zz = np.zeros(K, dtype=np.int64)
    def comb(r, ee, x):
        pR = r.get((x, 0), (zz, zz))[0]; pL = r.get((x, 1), (zz, zz))[0]
        return cx.mul(cx.mul(cx.conj(pR), pL), cx.root(derived(ee, K)['eg']))
    for x in range(N):
        v1 = comb(r1, e, x)
        rec('PREP1', cx.eq(v1, comb(r2, e2, x)) and cx.eq(v1, comb(r3, e3, x)), (N, e, ms, x))
        if not cx.zero(v1): rec('PREP1_nonzero_cases', True)
    # continuation
    x = rng.randrange(N); ms2 = rand_masks(rng, N, t, last=x); r = rng.randrange(1, 4); cont = rand_masks(rng, N, r)
    ra = enum_ports(N, e, ms2, K); full = enum_ports(N, e, ms2 + cont, K)
    psiR = ra.get((x, 0), (zz, zz))[0]; psiL = ra.get((x, 1), (zz, zz))[0]
    sh = [None if m is None else {(y - x) % N for y in m} for m in cont]
    rb = enum_ports(N, e, sh, K)
    okA = True; okP = True; nonz = False
    for y in range(N):
        for rail in (0, 1):
            V = full.get((y, rail), (zz, zz))[0]
            vv = rb.get(((y - x) % N, rail), (zz, zz))
            W = cx.mul(psiR, vv[0]) + cx.mul(psiL, vv[1])
            okA &= cx.eq(V, W)
            # P_full*2^(t+r) = |V|^2 ; P_start*2^r = |W|^2 ; literal equality of P needs 2^t |V|^2... i.e. |W|^2 == 2^t |V|^2 ? no:
            # P_full = |V|^2/2^(t+r), P_start = |W|^2/2^r ; equal iff |V|^2 == 2^t |W|^2
            nV = cx.mul(V, cx.conj(V)); nW = cx.mul(W, cx.conj(W))
            if not cx.zero(nV): nonz = True
            okP &= cx.eq(nV, (2 ** t) * nW)
    rec('PREP2', okA, (N, e, ms2, cont))
    if nonz: rec('PREP2f(literal, no factor 2^-t)', okP, (N, e, 't=%d' % t))
for it in range(300):
    N = 17; t = rng.randrange(1, 7)
    car = rand_carrier(rng, K, rng.choice([K // 2, 0, None])); e = car['e']; D = derived(e, K)
    if D['eH'] not in (0, K // 2):
        rec('LINE_not_qualifying(eta not real)', True); continue
    g = rng.randrange(1, K); e2 = (e[0], (e[1] + g) % K, e[2], (e[3] + g) % K)
    ms = [None if rng.random() < .4 else {x % N for x in range(-7, 8) if rng.random() < .7} for _ in range(t)]
    r1 = enum_ports(N, e, ms, K); r2 = enum_ports(N, e2, ms, K)
    for st in starts(cx, rng)[:8]:
        ok = all(cx.eq(pnum(cx, st, r1.get(k)), pnum(cx, st, r2.get(k))) for k in set(r1) | set(r2))
        rec('LINE', ok, (e, e2, ms))
say("PREP, LINE done")

# ================= exhaustive masks =================
def dp_levels(N, e, K, Lmax, subs):
    ea, eb, ec, ed = e
    st = np.zeros((1, 2, N, 2, K), dtype=np.int64); st[0, 0, 0, 0, 0] = 1; st[0, 1, 0, 1, 0] = 1
    lv = []
    for L in range(1, Lmax + 1):
        new = np.zeros_like(st)
        new[:, :, :, 0, :] = np.roll(np.roll(st[:, :, :, 0, :], ea, -1) + np.roll(st[:, :, :, 1, :], ec, -1), 1, 2)
        new[:, :, :, 1, :] = np.roll(np.roll(st[:, :, :, 0, :], eb, -1) + np.roll(st[:, :, :, 1, :], ed, -1), -1, 2)
        st = np.concatenate([new * mk[None, None, :, None, None] for mk in subs], 0)
        lv.append(st)
    return lv
def subsets(N):
    return [np.array([(b >> x) & 1 for x in range(N)], dtype=np.int64) for b in range(1, 2 ** N)]
LD = 2 * 5 * 13 * 3
def level_sig(cx, lev, st):
    A, B, den = st; K = cx.K; sc = (LD // den) ** 2
    amp = lev[:, 0] @ cx.circ(A) + lev[:, 1] @ cx.circ(B)
    o = np.stack([(np.roll(amp, -m, -1) * amp).sum(-1) for m in range(K)], -1) @ cx.R
    return (o * sc)
# DP check
for N in (3, 4):
    Kc = 12; cxc = Ctx(Kc); subs = subsets(N)
    for _ in range(3):
        car = rand_carrier(rng, Kc, None); e = car['e']; lv = dp_levels(N, e, Kc, 3, subs)
        for L in (1, 2, 3):
            for idx in itertools.product(range(len(subs)), repeat=L):
                ms = [{x for x in range(N) if subs[i][x]} for i in idx]
                r = enum_ports(N, e, ms, Kc)
                ev = 0
                for j, i in enumerate(idx): ev += i * (len(subs) ** j)   # level j+1 index = sidx*E_prev + prev
                ok = True
                zz = np.zeros(Kc, dtype=np.int64)
                for x in range(N):
                    for rail in (0, 1):
                        vv = r.get((x, rail), (zz, zz))
                        ok &= np.array_equal(lv[L - 1][ev, 0, x, rail], vv[0]) and np.array_equal(lv[L - 1][ev, 1, x, rail], vv[1])
                rec('DP', ok, (N, e, idx))
say("DP check done")

def exhaustive(N, Lmax, K, ncar):
    cx = Ctx(K); subs = subsets(N); M = N // gcd(N, 2)
    pool = []
    for i in range(ncar):
        car = rand_carrier(rng, K, [K // 2, K // 2, K // 2, 0, None][i % 5]); e = car['e']
        pool.append((e, 'grp%s' % car['ns']))
        if i % 5 == 0:
            g = rng.randrange(1, K)
            pool.append((tuple((v + g) % K for v in e), 'T1'))
            pool.append(((e[0], (e[1] - g) % K, (e[2] + g) % K, e[3]), 'T2'))
            gm = (K // gcd(K, M)) * rng.randrange(1, max(2, gcd(K, M)))
            pool.append(((e[0], (e[1] + gm) % K, e[2], (e[3] + gm) % K), 'T4'))
    data = []
    for e, lab in pool:
        D = derived(e, K)
        ebar = tuple((-v) % K for v in e)
        lv = dp_levels(N, e, K, Lmax, subs); lvb = dp_levels(N, ebar, K, Lmax, subs)
        named = [fork_masks(N, M), [{1 % N}] + fork_masks(N, M, 1), [{(-1) % N}] + fork_masks(N, M, 1, -1)]
        nr = [enum_ports(N, e, m, K) for m in named]; nrb = [enum_ports(N, ebar, m, K) for m in named]
        for st in starts(cx, rng):
            def sig(lv_, nr_):
                hs = hashlib.sha256(); hlow = hashlib.sha256()
                for L, lev in enumerate(lv_, 1):
                    b = level_sig(cx, lev, st).tobytes(); hs.update(b)
                    if L <= M: hlow.update(b)
                sc = (LD // st[2]) ** 2
                for r in nr_:
                    for x in range(N):
                        for rail in (0, 1):
                            hs.update(repr(cx.canon(sc * pnum(cx, st, r.get((x, rail))))).encode())
                return hs.hexdigest(), hlow.hexdigest()
            h, hl = sig(lv, nr); hb, _ = sig(lvb, nrb)
            q = quantities(cx, st, e, N); sc = (LD // st[2]) ** 2
            k4 = (cx.canon(sc * q['aa']), cx.canon(q['rw2']), cx.canon(sc * q['rk2']), cx.canon(sc * q['ii']))
            k6 = k4 + (cx.canon(sc * q['bb']), D['eH'])
            A, B, den = st; z = cx.mul(cx.conj(A), B)
            imz0 = cx.zero(z - cx.conj(z))
            gpm = D['eg'] in (0, K // 2); wpm = (M * D['eB']) % K in (0, K // 2)
            fkP = cx.canon(sc * pnum(cx, st, nr[0].get(((M + 1) % N, 0))))
            data.append(dict(h=h, hl=hl, hb=hb, k4=k4, k6=k6, eH=D['eH'], norm=is_norm(cx, st), sharp=not np.any(B),
                             unitA=cx.eq(q['aa'], den * den * cx.root(0)), lab=lab, e=e, den=den,
                             conjpred=(imz0 or (gpm and wpm)), fkP=fkP, rw2=cx.canon(q['rw2']), sc=sc))
    # INV
    real = [d for d in data if d['eH'] in (0, K // 2)]
    npair = 0
    for i in range(len(real)):
        for j in range(i):
            if real[i]['k6'] == real[j]['k6']:
                npair += 1; rec('INV_N%d' % N, real[i]['h'] == real[j]['h'], (real[i]['e'], real[j]['e']))
    hyp = [d for d in data if d['eH'] == K // 2 and d['norm']]
    eqp = dif = 0
    for i in range(len(hyp)):
        for j in range(i):
            same = hyp[i]['k4'] == hyp[j]['k4']
            if same: eqp += 1
            else: dif += 1
            rec('LIST_N%d_%s' % (N, 'equal_tuple=>equal_stats' if same else 'diff_tuple=>diff_stats'),
                (hyp[i]['h'] == hyp[j]['h']) == same, (hyp[i]['e'], hyp[i]['lab'], hyp[j]['e'], hyp[j]['lab']))
    sh = [d for d in hyp if d['sharp'] and d['unitA']]
    for i in range(len(sh)):
        for j in range(i):
            same = sh[i]['rw2'] == sh[j]['rw2']
            rec('SHARP_N%d_stats<=>Re_omega' % N, (sh[i]['h'] == sh[j]['h']) == same, (sh[i]['e'], sh[j]['e']))
            rec('SHARP_N%d_len<=M_equal' % N, sh[i]['hl'] == sh[j]['hl'], (sh[i]['e'], sh[j]['e']))
            rec('SHARP_N%d_fork_separates_iff' % N, (sh[i]['fkP'] == sh[j]['fkP']) == same, (sh[i]['e'], sh[j]['e']))
    for d in hyp:
        rec('CONJ_N%d_%s' % (N, 'pred_true' if d['conjpred'] else 'pred_false'), (d['h'] == d['hb']) == d['conjpred'], (d['e'], d['lab']))
    fair = 0
    for d in hyp:
        if not d['sharp'] and d['rw2'] != cx.canon(0 * cx.root(0)):
            if d['fkP'] == cx.canon(d['sc'] * d['den'] ** 2 * 2 * cx.root(0)): fair += 1
    say("N=%d K=%d Lmax=%d: data %d, eta real %d, eta=-1&n=1 %d, sharp unit %d, distinct Re omega among sharp %d; "
        "pairs equal tuple %d, different tuple %d; INV pairs %d; FAIR non-sharp with Re omega!=0 and fork P=2^-M: %d; groups: %s"
        % (N, K, Lmax, len(data), len(real), len(hyp), len(sh), len({d['rw2'] for d in sh}), eqp, dif, npair, fair,
           sorted({d['lab'] for d in data})[:12]))
cfg = [(3, 5, 12, int(sys.argv[2])), (4, 4, 12, int(sys.argv[2])), (5, 3, 12, int(sys.argv[2])), (3, 4, 24, max(4, int(sys.argv[2]) // 2))]
for N, Lmax, K, nc in cfg: exhaustive(N, Lmax, K, nc)

say("\nPREDICATE TABLE: name | cases tested (qualifying) | pass | fail | first failing cases")
anyfail = False
for k in sorted(TAB):
    q, p, f, ex = TAB[k]
    say("%-44s | %8d | %8d | %8d | %s" % (k, q, p, f, ex if f else ''))
say("END seed %d" % SEED)
OUT.close()
