#!/usr/bin/env python3
"""p1_exact.py -- exact checks for mechanics.md (items a, b-series, d, e, h).
Walk: incoming integers (r,l) at site x go to r+l on (x+1,R) and r-l on (x-1,L).
Component order (R,L). Result file opened with mode 'x'.

PREDICATES (fixed before first run):
A1   ring N in {1,2,3,4,5,8,12}: integer matrix A satisfies A^T A = 2I and A A^T = 2I.
A1L  line window, sources on sites [-m,m], outputs on [-m-1,m+1], m in {0,1,5}: A^T A = 2I.
     (A A^T on the window is reported, not a predicate.)
A2   ring N=4 and N=8, exact (sympy): for every k=2 pi j/N and basis vector v, A applied to the
     plane wave e^{ikx} v equals e^{ikx} sqrt2 U(k) v, U(k)=diag(e^{-ik},e^{ik}) H.
A2neg negative control: the same identity with U(-k) fails for at least one k (kernel sign matters).
A3   50-digit numeric at 25 k values: lambda_+ = sqrt(1-sin^2 k/2) - i sin k/sqrt2 is a root of
     det(U(k)-lambda); |lambda_+|=1; Re lambda_+ >= 1/sqrt2; other root = -conj(lambda_+).
     Basis for tolerance 1e-40: 50-digit arithmetic on O(1) quantities (rounding ~1e-49).
A4   exact at k*=-pi/2 (sympy): U(k*) u = e^{i pi/4} u for u=(1,-i)/sqrt2; omega(k*)=-pi/4;
     omega'(k*)=0; omega''(k*)=1, with omega(k)=asin(sin k/sqrt2).
B1   50-digit: d/dk asin(sin k/sqrt2) at k*+q equals sin q/sqrt(1+sin^2 q) for
     q in {-1,-1/2,-1/10,1/10,1/3,1/2,1,2,3}; tolerance 1e-40 (same basis as A3).
B1s  series: q - sin q/sqrt(1+sin^2 q) = 2q^3/3 - 19q^5/30 + O(q^7);
     q^2/2 - (omega(k*+q)-omega*) = q^4/6 - 19q^6/180 + O(q^8).
D1   integers: (1,1)->(2,0); (1,-1)->(0,2); formula probabilities (1,0),(0,1);
     sharp rails (1,0),(0,1) each give (1/2,1/2).
E1   integer autocorrelation C_t(d)=sum_{x,c}(A^t h)(x,c)(A^t h)(x+d,c):
     (a) every tested integer source: C_t(d)=2^t C_0(d) for all d, t<=10;
     (b) single-site sources: C_0(d)=0 for d!=0 (uniform momentum density);
     (c) EDGE count: multi-site "localized" sources with C_0(d)!=0 for some d!=0.
H1   W in {0,1,2,5}, n in {1,2,3,6}, 10 random integer sources each (all entries nonzero,
     support sites a..a+W): for every even N with W+2n+2 < N <= W+2n+8 the ring evolution equals
     the line evolution on the cone [a-t,a+W+t] at every tick t<=n and is zero elsewhere.
     Measured: smallest N (any parity, N>=1) from which agreement holds in all trials.
H2   10000 random pairs of real unit vectors (dim 2..8), M random with spectral norm 1, plus
     M = sign matrix of aa^T-bb^T: ratio |<a,Ma>-<b,Mb>|/(2||a-b||) <= 1. Double precision;
     no tolerance: the max ratio and the margin 1-max are reported.
"""
import sys, random, itertools
import numpy as np, sympy as sp, mpmath as mp
out = open(sys.argv[1], 'x')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n'); out.flush()
random.seed(20261113); np.random.seed(20261113)
res = {}

# ---------- A1 ----------
def ring_A(N):
    A = np.zeros((2*N, 2*N), dtype=object); A[:] = 0
    for x in range(N):
        r, l = 2*x, 2*x+1
        A[2*((x+1) % N), r] += 1; A[2*((x+1) % N), l] += 1
        A[2*((x-1) % N)+1, r] += 1; A[2*((x-1) % N)+1, l] -= 1
    return A
ok = True
for N in [1, 2, 3, 4, 5, 8, 12]:
    A = ring_A(N); I2 = 2*np.eye(2*N, dtype=object)
    a = (A.T.dot(A) == I2).all(); b = (A.dot(A.T) == I2).all()
    P(f'A1 ring N={N}: A^T A=2I {a}; A A^T=2I {b}'); ok &= bool(a and b)
res['A1'] = ok
ok = True
for m in [0, 1, 5]:
    ns, no = 2*m+1, 2*m+3
    A = np.zeros((2*no, 2*ns), dtype=object); A[:] = 0
    for i, x in enumerate(range(-m, m+1)):
        r, l = 2*i, 2*i+1
        A[2*(i+2), r] += 1; A[2*(i+2), l] += 1      # (x+1,R): output index x+1-(-m-1)=i+2
        A[2*i+1, r] += 1; A[2*i+1, l] -= 1          # (x-1,L): output index i
    a = (A.T.dot(A) == 2*np.eye(2*ns, dtype=object)).all()
    AAt = A.dot(A.T); zero_rows = int(sum(1 for j in range(2*no) if AAt[j, j] == 0))
    P(f'A1L window m={m}: A^T A=2I {a}; output ports never hit in window (zero rows of AA^T): {zero_rows}')
    ok &= bool(a)
res['A1L'] = ok

# ---------- A2 ----------
H = sp.Matrix([[1, 1], [1, -1]])/sp.sqrt(2)
def Uk(k): return sp.diag(sp.exp(-sp.I*k), sp.exp(sp.I*k))*H
ok = True; neg_fail = 0; inst = 0
for N in [4, 8]:
    for j in range(N):
        k = 2*sp.pi*sp.Rational(j, N)
        for v in [sp.Matrix([1, 0]), sp.Matrix([0, 1])]:
            inst += 1
            h = [[sp.exp(sp.I*k*x)*v[0], sp.exp(sp.I*k*x)*v[1]] for x in range(N)]
            Ah = [[h[(x-1) % N][0]+h[(x-1) % N][1], h[(x+1) % N][0]-h[(x+1) % N][1]] for x in range(N)]
            for sign, tag in [(1, 'pos'), (-1, 'neg')]:
                w = sp.sqrt(2)*Uk(sign*k)*v
                d = max(abs(complex(sp.N(Ah[x][c]-sp.exp(sp.I*k*x)*w[c], 30))) for x in range(N) for c in range(2))
                exact0 = all(sp.simplify(sp.expand(Ah[x][c]-sp.exp(sp.I*k*x)*w[c], complex=True)) == 0 for x in range(N) for c in range(2))
                if tag == 'pos': ok &= exact0
                else: neg_fail += (not exact0)
P(f'A2 instances {inst}: identity with U(k) exact on all: {ok}; with U(-k) fails on {neg_fail} of {inst}')
res['A2'] = ok; res['A2neg'] = neg_fail > 0

# ---------- A3 ----------
mp.mp.dps = 50
worst = mp.mpf(0); minre = mp.mpf(10)
for j in range(25):
    k = mp.mpf(-3) + mp.mpf(j)*mp.mpf(6)/24 + mp.mpf('0.0137')
    U = mp.matrix([[mp.e**(-1j*k), mp.e**(-1j*k)], [mp.e**(1j*k), -mp.e**(1j*k)]])/mp.sqrt(2)
    lam = mp.sqrt(1-mp.sin(k)**2/2) - 1j*mp.sin(k)/mp.sqrt(2)
    det = (U[0, 0]-lam)*(U[1, 1]-lam) - U[0, 1]*U[1, 0]
    lam2 = -mp.conj(lam)
    det2 = (U[0, 0]-lam2)*(U[1, 1]-lam2) - U[0, 1]*U[1, 0]
    worst = max(worst, abs(det), abs(det2), abs(abs(lam)-1)); minre = min(minre, lam.real)
P('A3 worst residual', mp.nstr(worst, 5), ' min Re lambda_+ on grid', mp.nstr(minre, 12), ' 1/sqrt2', mp.nstr(1/mp.sqrt(2), 12))
res['A3'] = (worst < mp.mpf('1e-40')) and (minre >= 1/mp.sqrt(2))

# ---------- A4 ----------
ks = -sp.pi/2; u = sp.Matrix([1, -sp.I])/sp.sqrt(2)
lhs = Uk(ks)*u; rhs = sp.exp(sp.I*sp.pi/4)*u
a = all(sp.simplify(sp.expand(lhs[i]-rhs[i], complex=True)) == 0 for i in range(2))
k = sp.symbols('k', real=True); om = sp.asin(sp.sin(k)/sp.sqrt(2))
o0 = sp.simplify(om.subs(k, ks)); o1 = sp.simplify(sp.diff(om, k).subs(k, ks)); o2 = sp.simplify(sp.diff(om, k, 2).subs(k, ks))
P(f'A4 U(k*)u = e^(i pi/4) u: {a}; omega*={o0}; omega\'={o1}; omega\'\'={o2}')
# the other band at k*: eigenvalue -e^{-i pi/4}; check u is not its eigenvector
rhs2 = -sp.exp(-sp.I*sp.pi/4)*u
a2 = all(sp.simplify(sp.expand(lhs[i]-rhs2[i], complex=True)) == 0 for i in range(2))
P(f'A4 u is eigenvector of the other band: {a2} (expected False)')
res['A4'] = bool(a and o0 == -sp.pi/4 and o1 == 0 and o2 == 1 and not a2)

# ---------- B1 ----------
worst = mp.mpf(0)
for q in ['-1', '-0.5', '-0.1', '0.1', '0.3333333333333333333333333333333333333333333333', '0.5', '1', '2', '3']:
    q = mp.mpf(q); kk = -mp.pi/2 + q
    d1 = mp.diff(lambda t: mp.asin(mp.sin(t)/mp.sqrt(2)), kk)
    d2 = mp.cos(kk)/(mp.sqrt(2)*mp.sqrt(1-mp.sin(kk)**2/2))
    d3 = mp.sin(q)/mp.sqrt(1+mp.sin(q)**2)
    worst = max(worst, abs(d2-d3)); P('B1 q', mp.nstr(q, 6), 'closed-form diff', mp.nstr(abs(d2-d3), 5), 'numdiff-vs-formula', mp.nstr(abs(d1-d3), 5))
res['B1'] = worst < mp.mpf('1e-40')
q = sp.symbols('q')
s1 = sp.series(q - sp.sin(q)/sp.sqrt(1+sp.sin(q)**2), q, 0, 7).removeO()
s2 = sp.series(sp.integrate(s1, q), q, 0, 8).removeO()
P('B1s q-omega\' series:', s1, ' ; q^2/2-(omega-omega*) series:', s2)
res['B1s'] = sp.expand(s1 - (sp.Rational(2, 3)*q**3 - sp.Rational(19, 30)*q**5)) == 0 and sp.expand(s2 - (q**4/6 - sp.Rational(19, 180)*q**6)) == 0

# ---------- D1 ----------
step = lambda r, l: (r+l, r-l)
o_p, o_m = step(1, 1), step(1, -1)
from fractions import Fraction as Fr
pr = lambda o, h: tuple(Fr(v*v, 2*sum(z*z for z in h)) for v in o)
P('D1 h+ ->', o_p, 'prob', pr(o_p, (1, 1)), '; h- ->', o_m, 'prob', pr(o_m, (1, -1)), '; rail R ->', pr(step(1, 0), (1, 0)), '; rail L ->', pr(step(0, 1), (0, 1)))
res['D1'] = o_p == (2, 0) and o_m == (0, 2) and pr(o_p, (1, 1)) == (1, 0) and pr(o_m, (1, -1)) == (0, 1) and pr(step(1, 0), (1, 0)) == (Fr(1, 2),)*2 and pr(step(0, 1), (0, 1)) == (Fr(1, 2),)*2

# ---------- line evolution with dict ----------
def line_step(h):
    g = {}
    for (x, c), v in h.items():
        pass
    sites = set(x for (x, c) in h)
    for x in sites:
        r, l = h.get((x, 0), 0), h.get((x, 1), 0)
        g[(x+1, 0)] = g.get((x+1, 0), 0) + r + l
        g[(x-1, 1)] = g.get((x-1, 1), 0) + r - l
    return g
def autocorr(h):
    C = {}
    xs = sorted(set(x for (x, c) in h))
    for x in xs:
        for y in xs:
            d = y - x
            C[d] = C.get(d, 0) + sum(h.get((x, c), 0)*h.get((y, c), 0) for c in (0, 1))
    return C
# ---------- E1 ----------
ea = eb = True; n_single = n_multi = n_multi_nonuniform = 0
srcs = []
for _ in range(20):
    v = (random.randint(-3, 3), random.randint(-3, 3))
    if v == (0, 0): v = (1, 0)
    srcs.append(('single', {(0, 0): v[0], (0, 1): v[1]}))
for _ in range(20):
    w = random.randint(1, 4)
    h = {}
    for x in range(w+1):
        h[(x, 0)] = random.choice([-3, -2, -1, 1, 2, 3]); h[(x, 1)] = random.choice([-3, -2, -1, 1, 2, 3])
    srcs.append(('multi', h))
for kind, h in srcs:
    C0 = autocorr(h); uniform0 = all(v == 0 for d, v in C0.items() if d != 0)
    if kind == 'single': n_single += 1; eb &= uniform0
    else:
        n_multi += 1; n_multi_nonuniform += (not uniform0)
    g = dict(h)
    for t in range(1, 11):
        g = line_step(g); Ct = autocorr(g)
        for d in set(Ct) | set(C0):
            if Ct.get(d, 0) != 2**t*C0.get(d, 0): ea = False
P(f'E1 (a) C_t = 2^t C_0 for all {len(srcs)} sources: {ea}; (b) single-site uniform: {eb} ({n_single} sources); (c) multi-site sources non-uniform: {n_multi_nonuniform} of {n_multi}')
res['E1a'] = ea; res['E1b'] = eb; res['E1c_edge_nonuniform_exists'] = n_multi_nonuniform > 0

# ---------- H1 ----------
def ring_step(R, L):
    N = len(R); R2 = [0]*N; L2 = [0]*N
    for x in range(N):
        R2[(x+1) % N] += R[x] + L[x]; L2[(x-1) % N] += R[x] - L[x]
    return R2, L2
h1_claim_ok = True; h1_inst = 0; minN = {}
for W in [0, 1, 2, 5]:
    for n in [1, 2, 3, 6]:
        agree_N = {}
        for N in range(1, W+2*n+9):
            allok = True
            for trial in range(10):
                rnd = random.Random(1000*W + 10*n + trial)
                a = rnd.randint(0, 5)
                h = {}
                for x in range(a, a+W+1):
                    h[(x, 0)] = rnd.choice([-3, -2, -1, 1, 2, 3]); h[(x, 1)] = rnd.choice([-3, -2, -1, 1, 2, 3])
                R = [0]*N; L = [0]*N
                for (x, c), v in h.items():
                    if c == 0: R[x % N] += v
                    else: L[x % N] += v
                g = dict(h); ok_t = True
                # tick 0 agreement requires injective placement
                for t in range(0, n+1):
                    if t > 0:
                        g = line_step(g); R, L = ring_step(R, L)
                    seen = {}
                    for x in range(a-t, a+W+t+1):
                        for c in (0, 1):
                            lv = g.get((x, c), 0); rv = (R if c == 0 else L)[x % N]
                            if lv != rv: ok_t = False
                            seen[(x % N, c)] = True
                    for x in range(N):
                        for c in (0, 1):
                            if (x, c) not in seen and (R if c == 0 else L)[x] != 0: ok_t = False
                allok &= ok_t
            agree_N[N] = allok
            if N % 2 == 0 and N > W+2*n+2:
                h1_inst += 1; h1_claim_ok &= allok
        # smallest N0 such that agreement holds for all N>=N0 tested
        N0 = None
        for N in sorted(agree_N, reverse=True):
            if agree_N[N]: N0 = N
            else: break
        minN[(W, n)] = (N0, N0 - (W+2*n) if N0 else None)
P(f'H1 claim (even N > W+2n+2): {h1_claim_ok} over {h1_inst} (W,n,N) cells x 10 sources')
P('H1 smallest N with agreement from there on, as (N0, N0-(W+2n)) per (W,n):', minN)
res['H1'] = h1_claim_ok

# ---------- H2 ----------
mx = 0.0; mx_opt = 0.0; cnt = 0
for _ in range(10000):
    d = np.random.randint(2, 9)
    a = np.random.randn(d); a /= np.linalg.norm(a)
    scale = 10**np.random.uniform(-6, 0.3)
    b = a + scale*np.random.randn(d); b /= np.linalg.norm(b)
    eta = np.linalg.norm(a-b)
    if eta == 0: continue
    cnt += 1
    M = np.random.randn(d, d); M /= np.linalg.svd(M, compute_uv=False)[0]
    mx = max(mx, abs(a@M@a - b@M@b)/(2*eta))
    D = np.outer(a, a) - np.outer(b, b); w, V = np.linalg.eigh(D); Mo = V@np.diag(np.sign(w))@V.T
    mx_opt = max(mx_opt, abs(a@Mo@a - b@Mo@b)/(2*eta))
P(f'H2 {cnt} pairs (both vectors unit norm: hypothesis satisfied by construction): max ratio random M {mx:.12f}; max ratio optimal M {mx_opt:.15f}; margin {1-mx_opt:.3e}')
res['H2'] = mx <= 1 and mx_opt <= 1
# unnormalised variant (hypothesis violated): b not unit
a = np.array([1.0, 0.0]); b = np.array([1.5, 0.0]); M = np.eye(2)
P('H2 edge (b not normalised, a=(1,0), b=(1.5,0), M=I): |diff| =', abs(a@M@a-b@M@b), ' 2 eta =', 2*np.linalg.norm(a-b))

P('SUMMARY', res)
out.close()
