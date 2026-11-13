"""Cross-review program xr9 for "A position-dependent interaction from one shared sheet".
Independent code (no import of Director G's checkers). Predicates fixed BEFORE the first run.

Conventions. Ring Z/N, 4 | N, a = 2 pi/N = eps*delta, tau = eps*delta^2. Coin basis (R, L);
coin H = [[1,1],[1,-1]]/sqrt2 (sign -1 on incoming L -> outgoing L); R moves x -> x+1, L moves
x -> x-1. One tick = sector phase exp(-i*angle(x1-x2)) at departure, both coins, both shifts.
Fourier mode exp(+i k x); U(k) = diag(e^{-ik}, e^{ik}) H; plus band eigenvalue exp(-i omega(k)),
omega = arcsin(sin k / sqrt2); band edge k* = -pi/2, omega(k*) = -pi/4. Scalar reference
i eps f_t = (K+W) f, K = eps^2 (l1^2+l2^2)/2, W = kappa (1 - cos(Y1-Y2)), solved by dense
eigendecomposition on Fourier indices |l_j| <= Lc. Encoding: global smooth plus section
u(k) = (sqrt(1+c^2)+c, c+i s)/norm, no cutoff (all retained l have |a l| <= pi/2 is tested).
F(d) = 1 - cos(a d). Origin d = 0 counts as coincidence.

PREDICATES
P1  count bound: for N in {8,12,16,20,28,36,40} (hypothesis N>=8, 4|N, denominator>0 tested
    per N) and m in {1, N, N^2, N^2*ceil(log2 N)}: max_d |R_m(d)-F(d)| <= (N-3)(lam2/lam1)^m,
    exact integers, 120-digit mpmath for the cosine. At the full depth also <= N^(1-3pi^2/ln2).
P1x (information, hypothesis violated) same for N in {10,14} (4 does not divide N).
P2  the ACTUAL relative coordinate of the synchronized pair moves by {-2,0,0,+2}. Its count
    profile D'(d)=C'(0)-C'(d) (same depth rule on the ring N) satisfies D'(N/2)/max_d D' < 1e-6
    for N in {16,28}: i.e. the pair's own relative walk does NOT give 1-cos(a d) (which is
    maximal at N/2); the note's unit-adjacency operator is a separate input. Basis of 1e-6:
    predicted value is a spectral tail of size < N^-40.
P3  phase bound: g = round(L R_m) (ties up), L = round(M kappa delta^2/2pi), M = N^3+1;
    max_d |2 pi g(d)/M - kappa delta^2 F(d)| <= (3+rho)pi/M + |kappa| delta^2 rho with the
    measured rho; N in {20,28,40}, kappa in {1,-1,0.37}, eps in {1, delta}. Hypothesis L != 0
    reported per case.
P4  exact symmetries of the walk (N=20, eps=1, count-built gain, 30 ticks, random start):
    (a) norm drift < 1e-12; (b) joint translation commutes, difference < 1e-12; (c) distribution
    of total lattice momentum (l1+l2 mod N) changes by < 1e-12; (d) power control: a gain
    depending on x1 only changes that distribution by > 1e-3. Basis of 1e-12: 30 ticks of
    double-precision unitary updates.
P5  fixed action eps=1, kappa=1, f0 = (e0 + 0.5 e^{0.7i} e1 + 0.4i e_{-1}) x (e0 + 0.7 e^{-0.3i} e2),
    t ~ 0.5, sampled-rounded phase with M=N^3+1, N in {20,40,80,160}: err(N) =
    || e^{2 i n omega*} U^n E f0 - E f(n tau) ||. Predicate: err strictly decreasing and
    err(2N)/err(N) <= 0.6 for each doubling (bound (1) is O(1/N): asymptotic ratio <= 0.5,
    0.1 slack for pre-asymptotic sizes). N=20,40 also with count-built gains (reported).
P6  shrinking action eps=delta=sqrt(2pi/N), N in {40,160,640}, kappa in {1,-1}, periodized
    Gaussians width sqrt(eps), centres (0.9,-0.8), momenta nearest grid to (0.3,-0.5), t ~ 0.6:
    (a) state error err(4N)/err(N) <= 0.6 (bound O(delta), delta halves);
    (b) |<Z1 conj Z2>_walk - e^{i r(t)}| strictly decreasing in N (r from own RK4 Newton);
    (c) centre: |<Z1 Z2>_walk| - product statistic reported only.
P7  entanglement minor, eps=1, N=80, product of uniform modes, kappa=1, t ~ 0.1:
    (a) |a_{0,-1}|,|a_{1,0}| < 1e-12 (exact momentum conservation);
    (b) |det - i kappa t/2| <= 0.25 * kappa t/2 (O(t)+O(delta) relative corrections at t=0.1).
P8  |omega(k*+q) - omega(k*) - q^2/2| <= q^4/6 for 20001 q in [-1,1] (tolerance 1e-15).
P9  folded preparation: (a) m alternating two-step opposite-direction block entries multiply
    to sin^m k up to a unimodular constant times site phase (|.| compared, 1e-12);
    (b) for delta in {0.3,0.2,0.1,0.05}, N = 4*round(2pi/delta^2/4), even m nearest delta^-2.5:
    S_N = mean_j sin^{2m}(2 pi j/N) vs binom(2m,m)/4^m, relative error <= 1.2*a*sqrt(m)
    (basis: total variation 4 gives abs error <= 4/N, divided by S ~ 1/sqrt(pi m));
    (c) yield*pi*m within 5% of 1 at delta=0.05 (asymptotic 1 - 1/(4m)).
Failed predicates are kept in the JSON; follow-ups are separate programs.
"""
import json, sys, os, time
from math import pi, sqrt, ceil, log2, comb
from fractions import Fraction
import numpy as np
import mpmath as mp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xr9_result.json")
if os.path.exists(OUT):
    sys.exit("refusing to overwrite " + OUT)
mp.mp.dps = 120
RES = {"predicates": {}, "data": {}}
T0 = time.time()

def record(name, ok, **kw):
    RES["predicates"][name] = bool(ok)
    RES["data"][name] = kw
    print(name, "PASS" if ok else "FAIL", flush=True)

# ---------- counts ----------
def counts(N, m, step=1):
    row = [0]*N; row[0] = 1
    for _ in range(m):
        row = [row[(d-step) % N] + 2*row[d] + row[(d+step) % N] for d in range(N)]
    return row

def profile(N, m):
    c = counts(N, m)
    gaps = [c[0]-v for v in c]
    return gaps, gaps[N//2]

def rho_of(N, m):
    gaps, top = profile(N, m)
    if top <= 0:
        return None, gaps, top
    errs = [abs(mp.mpf(2*g)/top - (1-mp.cos(2*mp.pi*d/N))) for d, g in enumerate(gaps)]
    return max(errs), gaps, top

def full_depth(N):
    return N*N*ceil(log2(N))

rows = []; ok = True
for N in (8, 12, 16, 20, 28, 36, 40, 10, 14):
    hyp = (N >= 8 and N % 4 == 0)
    for m in (1, N, N*N, full_depth(N)):
        rho, gaps, top = rho_of(N, m)
        r = (mp.cos(2*mp.pi/N)/mp.cos(mp.pi/N))**2
        bound = (N-3)*r**m
        good = (top > 0) and (rho <= bound)
        extra = None
        if m == full_depth(N):
            poly = mp.mpf(N)**(1-3*mp.pi**2/mp.log(2))
            extra = bool(rho <= poly); good = good and extra
        rows.append(dict(N=N, m=m, hypothesis=hyp, denom_positive=top > 0,
                         rho=mp.nstr(rho, 8), bound=mp.nstr(bound, 8), within=bool(good), poly_bound_ok=extra))
        if hyp: ok = ok and good
record("P1", ok, rows=[r for r in rows if r["hypothesis"]], qualifying=sum(r["hypothesis"] for r in rows))
record("P1x_info", all(r["within"] for r in rows if not r["hypothesis"]), rows=[r for r in rows if not r["hypothesis"]])

# P2
d2 = {}; ok = True
for N in (16, 28):
    c = counts(N, full_depth(N), step=2)
    gaps = [c[0]-v for v in c]
    mx = max(gaps)
    ratio = float(Fraction(gaps[N//2], mx))
    odd_reached = any(c[d] != 0 for d in range(1, N, 2))
    dev = max(abs(float(Fraction(2*gaps[d], mx)) - (1-np.cos(2*pi*d/N))) for d in range(0, N, 2))
    dev2 = max(abs(float(Fraction(2*gaps[d], mx)) - (1-np.cos(4*pi*d/N))) for d in range(0, N, 2))
    d2[N] = dict(antipode_over_max=ratio, odd_sites_reached=odd_reached,
                 max_dev_from_1_minus_cos_ad_even_d=dev, max_dev_from_1_minus_cos_2ad_even_d=dev2)
    ok = ok and ratio < 1e-6
record("P2", ok, **{str(k): v for k, v in d2.items()})

# P3
def count_gain(N, M, kappa, delta, m=None):
    m = full_depth(N) if m is None else m
    gaps, top = profile(N, m)
    L = round(M*kappa*delta**2/(2*pi))
    g = [(4*L*gap + top)//(2*top) for gap in gaps]      # nearest, ties up
    return g, L
rows = []; ok = True
for N in (20, 28, 40):
    rho, _, _ = rho_of(N, full_depth(N))
    M = N**3+1
    for eps_mode in ("one", "delta"):
        if eps_mode == "one": eps = 1.0; delta = 2*pi/N
        else: eps = delta = sqrt(2*pi/N)
        for kappa in (1.0, -1.0, 0.37):
            g, L = count_gain(N, M, kappa, delta)
            err = max(abs(2*pi*g[d]/M - kappa*delta**2*(1-np.cos(2*pi*d/N))) for d in range(N))
            bound = float((3+rho)*mp.pi/M + abs(kappa)*delta**2*rho)
            good = err <= bound*(1+1e-12)
            ok = ok and good
            rows.append(dict(N=N, M=M, eps=eps, kappa=kappa, L=L, L_nonzero=L != 0, err=err, bound=bound, within=good))
record("P3", ok, rows=rows)

# ---------- walk ----------
def step(psi, phase):
    # psi[x1,x2,c1,c2]; c=0 is R, c=1 is L
    psi = psi*phase[:, :, None, None]
    a = (psi[:, :, 0, :] + psi[:, :, 1, :])/sqrt(2); b = (psi[:, :, 0, :] - psi[:, :, 1, :])/sqrt(2)
    psi = np.stack((a, b), axis=2)
    a = (psi[:, :, :, 0] + psi[:, :, :, 1])/sqrt(2); b = (psi[:, :, :, 0] - psi[:, :, :, 1])/sqrt(2)
    psi = np.stack((a, b), axis=3)
    out = np.empty_like(psi)
    for c1 in (0, 1):
        for c2 in (0, 1):
            out[:, :, c1, c2] = np.roll(np.roll(psi[:, :, c1, c2], 1-2*c1, axis=0), 1-2*c2, axis=1)
    return out

def rel_phase(N, angle_of_d):
    x = np.arange(N)
    d = (x[:, None]-x[None, :]) % N
    return np.exp(-1j*np.asarray(angle_of_d)[d])

def sampled_angles(N, M, kappa, delta):
    d = np.arange(N)
    target = kappa*delta**2*(1-np.cos(2*pi*d/N))
    g = np.floor(M*target/(2*pi)+0.5)
    return 2*pi*g/M, float(np.max(np.abs(2*pi*g/M-target)))

def section(k):
    c, s = np.cos(k), np.sin(k)
    u = np.stack((np.sqrt(1+c*c)+c, c+1j*s), axis=-1)
    return u/np.linalg.norm(u, axis=-1, keepdims=True)

def encode(N, coeff, Lc):
    """coeff[(l1+Lc),(l2+Lc)] -> lattice spinor. mode k_j = k* + a l_j."""
    a = 2*pi/N
    ls = np.arange(-Lc, Lc+1)
    k = -pi/2 + a*ls
    u = section(k)
    x = np.arange(N)
    basis = np.exp(1j*np.outer(x, k))/sqrt(N)            # [x, l]
    A = basis[:, :, None]*u[None, :, :]                   # [x, l, c]
    return np.einsum('xlc,lm,ymd->xycd', A, coeff, A, optimize=True)

def hamiltonian(Lc, eps, kappa):
    ls = np.arange(-Lc, Lc+1); n = len(ls)
    idx = lambda i, j: i*n+j
    H = np.zeros((n*n, n*n))
    for i in range(n):
        for j in range(n):
            H[idx(i, j), idx(i, j)] = eps**2*(ls[i]**2+ls[j]**2)/2 + kappa
            if i+1 < n and j-1 >= 0:
                H[idx(i+1, j-1), idx(i, j)] = -kappa/2
                H[idx(i, j), idx(i+1, j-1)] = -kappa/2
    return H

class Ref:
    def __init__(self, Lc, eps, kappa):
        self.Lc, self.eps = Lc, eps
        self.w, self.V = np.linalg.eigh(hamiltonian(Lc, eps, kappa))
    def evolve(self, coeff, t):
        v = coeff.reshape(-1)
        out = self.V @ (np.exp(-1j*self.w*t/self.eps)*(self.V.T @ v))
        return out.reshape(coeff.shape)

def run_walk(N, psi, angles, n):
    ph = rel_phase(N, angles)
    for _ in range(n):
        psi = step(psi, ph)
    return psi*np.exp(2j*n*(-pi/4))

def vnorm(v): return float(np.sqrt(np.sum(np.abs(v)**2)))

# P4
N = 20; delta = 2*pi/N; M = N**3+1
g, L = count_gain(N, M, 1.0, delta)
ang = 2*pi*np.array(g, dtype=float)/M
rng = np.random.default_rng(20261113)
psi0 = rng.normal(size=(N, N, 2, 2)) + 1j*rng.normal(size=(N, N, 2, 2)); psi0 /= vnorm(psi0)
def momdist(psi):
    F = np.fft.fft2(psi, axes=(0, 1))/N
    p = np.sum(np.abs(F)**2, axis=(2, 3))
    l = np.arange(N); tot = (l[:, None]+l[None, :]) % N
    return np.bincount(tot.reshape(-1), weights=p.reshape(-1), minlength=N)
ph = rel_phase(N, ang)
psi = psi0.copy(); psiT = np.roll(psi0, (3, 3), axis=(0, 1))
for _ in range(30):
    psi = step(psi, ph); psiT = step(psiT, ph)
norm_drift = abs(vnorm(psi)-1)
trans = vnorm(np.roll(psi, (3, 3), axis=(0, 1))-psiT)
mom = float(np.max(np.abs(momdist(psi)-momdist(psi0))))
x = np.arange(N)
ph_bad = np.exp(-1j*0.3*(1-np.cos(2*pi*x/N)))[:, None]*np.ones((1, N))
psib = psi0.copy()
for _ in range(30): psib = step(psib, ph_bad)
mom_bad = float(np.max(np.abs(momdist(psib)-momdist(psi0))))
record("P4", norm_drift < 1e-12 and trans < 1e-12 and mom < 1e-12 and mom_bad > 1e-3,
       norm_drift=norm_drift, translation_difference=trans, total_momentum_change=mom,
       control_x1_only_gain_change=mom_bad, L=L)

# P5
def coeff_quantum(Lc):
    n = 2*Lc+1
    f1 = np.zeros(n, complex); f2 = np.zeros(n, complex)
    f1[Lc] = 1; f1[Lc+1] = 0.5*np.exp(0.7j); f1[Lc-1] = 0.4j
    f2[Lc] = 1; f2[Lc+2] = 0.7*np.exp(-0.3j)
    c = np.outer(f1, f2); return c/vnorm(c)
rows = []
ref_cache = {}
for N in (20, 40, 80, 160):
    Lc = min(9, N//4)                       # |a l| <= pi/2 for every retained index
    eps = 1.0; delta = 2*pi/N; tau = eps*delta**2; M = N**3+1
    n = max(1, round(0.5/tau)); t = n*tau
    if Lc not in ref_cache: ref_cache[Lc] = Ref(Lc, eps, 1.0)
    ref = ref_cache[Lc]
    c0 = coeff_quantum(Lc); ct = ref.evolve(c0, t)
    # reference truncation check with larger Lc for the smallest and largest
    ang, th = sampled_angles(N, M, 1.0, delta)
    psi = run_walk(N, encode(N, c0, Lc), ang, n)
    err = vnorm(psi-encode(N, ct, Lc))
    row = dict(N=N, Lc=Lc, chart_ok=bool(2*pi*Lc/N <= pi/2+1e-12), steps=n, t=t, err=err,
               n_theta=n*th, edge_weight=float(np.sum(np.abs(ct[[0, -1], :])**2)+np.sum(np.abs(ct[:, [0, -1]])**2)))
    if N <= 40:
        g, L = count_gain(N, M, 1.0, delta)
        psi2 = run_walk(N, encode(N, c0, Lc), 2*pi*np.array(g, float)/M, n)
        row["err_count_built"] = vnorm(psi2-encode(N, ct, Lc)); row["L"] = L
    rows.append(row)
ratios = [rows[i+1]["err"]/rows[i]["err"] for i in range(3)]
record("P5", all(r <= 0.6 for r in ratios) and all(r < 1 for r in ratios), rows=rows, ratios=ratios)

# P6
def newton(q, p, kappa, t, steps=20000):
    def f(s):
        q1, q2, p1, p2 = s
        F = kappa*np.sin(q1-q2)
        return np.array([p1, p2, -F, F])
    s = np.array([q[0], q[1], p[0], p[1]], float); h = t/steps
    for _ in range(steps):
        k1 = f(s); k2 = f(s+h/2*k1); k3 = f(s+h/2*k2); k4 = f(s+h*k3)
        s = s+h/6*(k1+2*k2+2*k3+k4)
    return s
def stat_rel(psi, N):
    P = np.sum(np.abs(psi)**2, axis=(2, 3)); x = np.arange(N)
    return complex(np.sum(P*np.exp(2j*pi*(x[:, None]-x[None, :])/N))), complex(np.sum(P*np.exp(2j*pi*(x[:, None]+x[None, :])/N)))
rows = []
for kappa in (1.0, -1.0):
    for N in (40, 160, 640):
        eps = delta = sqrt(2*pi/N); tau = eps*delta**2; M = N**3+1
        Lc = min(20, N//4)
        ls = np.arange(-Lc, Lc+1)
        q0 = (0.9, -0.8); l0 = (round(0.3/eps), round(-0.5/eps)); p0 = (l0[0]*eps, l0[1]*eps)
        f1 = np.exp(-eps*(ls-l0[0])**2/2 - 1j*ls*q0[0]); f2 = np.exp(-eps*(ls-l0[1])**2/2 - 1j*ls*q0[1])
        c0 = np.outer(f1, f2); c0 /= vnorm(c0)
        n = max(1, round(0.6/tau)); t = n*tau
        ref = Ref(Lc, eps, kappa); ct = ref.evolve(c0, t)
        ang, th = sampled_angles(N, M, kappa, delta)
        psi = run_walk(N, encode(N, c0, Lc), ang, n)
        err = vnorm(psi-encode(N, ct, Lc))
        s = newton(q0, p0, kappa, t)
        zrel, zsum = stat_rel(psi, N)
        # reference statistic from Fourier coefficients: <e^{i(Y1-Y2)}> = sum conj(c[l1+1,l2-1]) c[l1,l2]
        ref_rel = complex(np.sum(np.conj(ct[1:, :-1])*ct[:-1, 1:]))
        rows.append(dict(kappa=kappa, N=N, eps=eps, Lc=Lc, chart_ok=bool(2*pi*Lc/N <= pi/2+1e-12), steps=n, t=t,
                         p0=p0, err=err, n_theta=n*th,
                         edge_weight=float(np.sum(np.abs(ct[[0, -1], :])**2)+np.sum(np.abs(ct[:, [0, -1]])**2)),
                         walk_rel=[zrel.real, zrel.imag], ref_rel=[ref_rel.real, ref_rel.imag],
                         classical_rel=[float(np.cos(s[0]-s[1])), float(np.sin(s[0]-s[1]))],
                         rel_gap_walk_classical=abs(zrel-np.exp(1j*(s[0]-s[1]))),
                         rel_gap_walk_ref=abs(zrel-ref_rel),
                         sum_gap_walk_classical=abs(zsum-np.exp(1j*(s[0]+s[1])))))
        print("  P6", kappa, N, round(time.time()-T0, 1), flush=True)
okA = all(rows[i+j+1]["err"]/rows[i+j]["err"] <= 0.6 for i in (0, 3) for j in (0, 1))
okB = all(rows[i+j+1]["rel_gap_walk_classical"] < rows[i+j]["rel_gap_walk_classical"] for i in (0, 3) for j in (0, 1))
record("P6a", okA, ratios=[rows[i+j+1]["err"]/rows[i+j]["err"] for i in (0, 3) for j in (0, 1)])
record("P6b", okB, rows=rows)

# P7
N = 80; eps = 1.0; delta = 2*pi/N; tau = delta**2; M = N**3+1; Lc = 3
n = round(0.1/tau); t = n*tau
c0 = np.zeros((2*Lc+1, 2*Lc+1), complex); c0[Lc, Lc] = 1
ang, th = sampled_angles(N, M, 1.0, delta)
psi = run_walk(N, encode(N, c0, Lc), ang, n)
def amp(l1, l2):
    e = np.zeros((2*Lc+1, 2*Lc+1), complex); e[Lc+l1, Lc+l2] = 1
    return complex(np.vdot(encode(N, e, Lc), psi))
a00, a0m, a10, a1m = amp(0, 0), amp(0, -1), amp(1, 0), amp(1, -1)
det = a00*a1m-a0m*a10
record("P7", abs(a0m) < 1e-12 and abs(a10) < 1e-12 and abs(det-0.5j*t) <= 0.25*0.5*t,
       t=t, a00=[a00.real, a00.imag], a1m1=[a1m.real, a1m.imag], a0m1=abs(a0m), a10=abs(a10),
       det=[det.real, det.imag], predicted_det_imag=0.5*t)

# P8
q = np.linspace(-1, 1, 20001)
om = np.arcsin(np.sin(-pi/2+q)/sqrt(2))
resid = np.abs(om+pi/4-q*q/2)
record("P8", bool(np.all(resid <= q**4/6+1e-15)), max_ratio=float(np.max(resid[q != 0]/(q[q != 0]**4/6))),
       ratio_at_1=float(resid[-1]*6))

# P9
k = np.linspace(-pi, pi, 721)
H = np.array([[1, 1], [1, -1]])/sqrt(2)
dev = 0.0
for kk in k:
    U = np.diag([np.exp(-1j*kk), np.exp(1j*kk)]) @ H
    U2 = U @ U
    prod = 1.0; m = 6
    for b in range(m):
        prod *= U2[1, 0] if b % 2 == 0 else U2[0, 1]     # R->L then L->R ...
    dev = max(dev, abs(abs(prod)-abs(np.sin(kk))**m))
rows = []; okb = True
for delta in (0.3, 0.2, 0.1, 0.05):
    N = 4*round(2*pi/delta**2/4); a = 2*pi/N
    m = 2*round(delta**-2.5/2)
    j = np.arange(N)
    S = float(np.mean(np.sin(2*pi*j/N)**(2*m)))
    exact = float(Fraction(comb(2*m, m), 4**m))
    rel = abs(S-exact)/exact
    rows.append(dict(delta=delta, N=N, m=m, m_exceeds_half_N=m >= N/2, S=S, binom=exact, rel_err=rel,
                     allowed=1.2*a*sqrt(m), yield_times_pi_m=S*S*pi*m))
    okb = okb and rel <= 1.2*a*sqrt(m)
record("P9", dev < 1e-12 and okb and abs(rows[-1]["yield_times_pi_m"]-1) < 0.05, block_modulus_dev=dev, rows=rows)

RES["runtime_seconds"] = time.time()-T0
RES["all_pass"] = all(RES["predicates"].values())
with open(OUT, "x") as fh:
    json.dump(RES, fh, indent=1, default=str)
print(RES["predicates"], RES["runtime_seconds"])
