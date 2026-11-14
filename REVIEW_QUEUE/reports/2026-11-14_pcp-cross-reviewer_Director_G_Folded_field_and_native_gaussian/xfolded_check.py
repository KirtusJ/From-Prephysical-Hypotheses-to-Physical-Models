"""Cross-review program for Director_G/Folded_field_and_native_gaussian.md.
Run: OMP_NUM_THREADS=1 python3 -B xfolded_check.py OUTDIR   (numpy, sympy/mpmath; seed 20261113)
Refuses to overwrite OUTDIR/xfolded_result.json. Failed predicates are kept in the file.

CONVENTIONS. Walk: R'(x)=(R(x-1)+L(x-1))/sqrt2, L'(x)=(R(x+1)-L(x+1))/sqrt2 (R moves to x+1).
Fourier kernel e^{-ikx}; U(k)=diag(e^{-ik},e^{ik})H. Encoding f_t(x)=i^x e^{-i pi t/4}(R+iL).
s = launch parity, occupied parity at tick t is s+t mod 2. Chart q in [-pi/2,pi/2) (left end included).
Norm of Z is in dq/pi; on a ring of N sites (4|N) this is (2/N) * sum over chart frequencies.
Y=x/sqrt(m), tau=n/m with the ACTUAL n of each run. Variance is about the mean.

PREDICATES (fixed before first run).
P1  Exact integers: 2^(t+1) f_{t+1}(x) = F(x-1)+F(x+1) + (-1)^s i^(t+1) [conj F(x-1) - conj F(x+1)], F=2^t f_t,
    for random integer rails on one parity, s=0,1, rings N=16,20,64, 6 ticks. Hypothesis (single parity, 4|N) tested
    per instance. P1c control: N=18 (4 does not divide N) is expected to violate the rule somewhere.
P2  Unit R launch at 0: f_1(+1)=(1+i)/2, f_1(-1)=(1-i)/2 (sympy exact).
P3  sympy exact: U(k*)(1,-i)/sqrt2 = e^{i pi/4}(1,-i)/sqrt2; ell P_-(k*)=0; eigenvalues e^{-iw}, -e^{iw};
    off-diagonals of U^2 are -i e^{-ik} sin k and -i e^{ik} sin k; group slope at k*+q is sin q/sqrt(1+sin^2 q).
    Numeric: min over k of |lambda_+ - lambda_-| >= sqrt2 (measured min reported; tolerance 4 ulp of sqrt2).
P4  sup over 0<|q|<=1 of |w(k*+q)+pi/4-q^2/2| / (q^4/6) <= 1 (grid of 400001 points; sup reported; no tolerance).
P5  sup over 0<|q|<=1 of ||ell P_-(k*+q)||/|q| <= sqrt2, and of ||P_-(k*+q)-P_-(k*)||/|q| <= 1 (sups reported).
P6  For random real single-parity rails: |Z(q)|^2+|Z(-q)|^2 = 2||F(q)||^2 at every chart frequency;
    residual reported relative to the largest term (tolerance 1e-12 = ~N*eps for N<=1024 sums).
P7  Main bound, 400 random instances: err = ||Z_{t+n} - e^{-i n q^2/2} Z_t|| <= 2*sqrt2*Q + n Q^4/6 + 2 e_Q.
    Hypothesis per instance: rails real, single parity (leak<1e-12), unit norm, 4|N, 0<Q<=1. n log-uniform in
    [1,1e6], Q uniform (0.02,1]. Count qualifying, count with bound<2 (non-vacuous), count violating; no tolerance
    added to the bound. Spectral evolution is first checked against direct stepping (P7a, max diff reported).
P8  Exact integers: the alternating-switch word (rail after block j is L for odd j, R for even j) from (0,R):
    raw amplitude at x=m-2j equals (-1)^j C(m,j) (rail R), squared sum C(2m,m), for even m=2..40; so success
    probability C(2m,m)/4^m. (-1)^(m/2) i^x raw is >0 on its support. Odd m (outside hypothesis) recorded only.
P9  ||sqrt(delta/pi) c_m cos^m(delta p) - G||_{L2(dp)} strictly decreases along m=8,32,128,512,2048,8192.
P10 ||psi_n - G e^{-i tau p^2/2}||_{L2(dp)} (tau=n/m actual, n=tau0*m) strictly decreases along
    m=32,128,512,2048 for tau0=0.5,1,2,3 (tau0=0.5,3 are not in the note).
P11 m=512: direct real-space stepping reproduces d_512=+0.778054, d_513=-0.320574 (|diff|<5e-7, half a unit of the
    last printed digit), variance 0.997912 (5e-7) and release-site-read variance 106.737 (5e-4).
    Reference C(1)=(1+i)^(-1/2) = 0.776887 - 0.321797 i (5e-7).
P12 For tau0 in (0.5,1,3) and m=64,256,1024 (not in the note), n=tau0*m (multiple of 4):
    |d_n - Re C(n/m)| and |d_{n+1} - Im C((n+1)/m)| each strictly decrease in m; sign(d_{n+1})<0.
    Identity d = (-1)^s Re[(-i)^n sum f^2] for launch at site 0 and at site 1 (residual reported, tol 1e-12).
P13 Blocks B=[-1,1],[0.5,1.5],[-0.3,0.7] (last not in the note), tau0=1: |d_n(B)-Re int_B g^2| and
    |d_{n+1}(B)-Im int_B g^2| strictly decrease along m=64,256,1024,4096. Closed endpoints.
P14 sum_x f(x)^2 = (2/N) sum_chart Z(q)Z(-q) on the ring (residual reported, tol 1e-12).
P15 Variance -> (1+tau^2)/2: |var - (1+tau^2)/2| strictly decreases along m=64,256,1024 for tau0=0.5,1,3.
P16 Yield of one window |x/T - v|<=w from (0,R), w=delta^1.1, T=round(delta^-2.8), v=delta*p0, p0=1:
    |p_yes/(2w/pi) - 1| strictly decreases along delta=0.2,0.14,0.1,0.07,0.05. (Ratios reported.)
"""
import sys, os, json, math, cmath
from math import comb
from fractions import Fraction
import numpy as np, sympy as sp, mpmath as mp

SEED = 20261113
rng = np.random.default_rng(SEED)
res = {"seed": SEED, "omp_num_threads": os.environ.get("OMP_NUM_THREADS"), "predicates": {}}
def put(name, ok, **kw):
    res["predicates"][name] = dict(passed=bool(ok), **kw); print(name, "PASS" if ok else "FAIL", json.dumps(kw, default=str)[:400])

# ---------- P1
def raw_step(R, L):
    N = len(R); return [R[x-1]+L[x-1] for x in range(N)], [R[(x+1) % N]-L[(x+1) % N] for x in range(N)]
I4 = [1, 1j, -1, -1j]
def scaledF(R, L, t):  # (1-i)^t i^x (R+iL) = 2^t f_t for raw integer rails; exact in small-integer complex floats
    fac = (1-1j)**t
    return [fac*I4[x % 4]*complex(R[x], L[x]) for x in range(len(R))]
def rule_violations(N, s, ticks=6):
    R = [0]*N; L = [0]*N
    for x in range(s, N, 2): R[x] = int(rng.integers(-5, 6)); L[x] = int(rng.integers(-5, 6))
    bad = 0; hyp = all(R[x] == 0 and L[x] == 0 for x in range(N) if (x-s) % 2)
    for t in range(ticks):
        F = scaledF(R, L, t); R, L = raw_step(R, L); G = scaledF(R, L, t+1)
        for x in range(N):
            a, b = F[x-1], F[(x+1) % N]
            pred = a+b+(-1)**s*I4[(t+1) % 4]*(a.conjugate()-b.conjugate())
            if pred != G[x]: bad += 1
    return bad, hyp
inst = [(N, s) for N in (16, 20, 64) for s in (0, 1) for _ in range(10)]
out = [rule_violations(N, s) for N, s in inst]
put("P1", all(b == 0 for b, h in out) and all(h for b, h in out), instances=len(inst), qualifying=sum(h for b, h in out), violations=sum(b for b, h in out))
c = [rule_violations(18, s)[0] for s in (0, 1) for _ in range(5)]
put("P1c_control_N18_expected_to_violate", all(v > 0 for v in c), violations_per_instance=c)

# ---------- P2, P3
i = sp.I; r2 = sp.sqrt(2)
f1p = i**1*sp.exp(-i*sp.pi/4)*(1/r2 + i*0); f1m = i**(-1)*sp.exp(-i*sp.pi/4)*(0 + i/r2)
put("P2", sp.simplify(f1p-(1+i)/2) == 0 and sp.simplify(f1m-(1-i)/2) == 0, f1_plus=str(sp.nsimplify(sp.simplify(f1p))), f1_minus=str(sp.simplify(f1m)))
k, q = sp.symbols("k q", real=True)
H = sp.Matrix([[1, 1], [1, -1]])/r2
U = sp.diag(sp.exp(-i*k), sp.exp(i*k))*H
Us = U.subs(k, -sp.pi/2); v = sp.Matrix([1, -i])/r2
e1 = sp.simplify(Us*v - sp.exp(i*sp.pi/4)*v) == sp.zeros(2, 1)
vm = sp.Matrix([1, i])/r2
e2 = sp.simplify(Us*vm - (-sp.exp(-i*sp.pi/4))*vm) == sp.zeros(2, 1)   # lambda_-(k*) = -e^{i w}, w=-pi/4
ell = sp.Matrix([[1, i]]); Pm = vm*vm.H
e3 = sp.simplify(ell*Pm) == sp.zeros(1, 2)
w = sp.asin(sp.sin(k)/r2)
tr_ok = sp.simplify(sp.expand((U.trace() - (sp.exp(-i*w) - sp.exp(i*w))).rewrite(sp.cos))) == 0
det_ok = sp.simplify(U.det() + 1) == 0
U2 = sp.simplify(U*U)
o1 = sp.simplify(sp.expand((U2[0, 1] + i*sp.exp(-i*k)*sp.sin(k)).rewrite(sp.exp))) == 0
o2 = sp.simplify(sp.expand((U2[1, 0] + i*sp.exp(i*k)*sp.sin(k)).rewrite(sp.exp))) == 0
slope = sp.diff(w, k).subs(k, q - sp.pi/2)
qq = np.linspace(-1.5, 1.5, 3001)
sl_num = sp.lambdify(q, slope, "numpy")(qq); sl_res = float(np.max(abs(sl_num - np.sin(qq)/np.sqrt(1+np.sin(qq)**2))))
kk = np.linspace(-np.pi, np.pi, 200001); gap = float(np.min(2*np.cos(np.arcsin(np.sin(kk)/np.sqrt(2)))))
put("P3", e1 and e2 and e3 and tr_ok and det_ok and o1 and o2 and sl_res < 1e-12 and gap >= math.sqrt(2)-4*np.finfo(float).eps*math.sqrt(2),
    eigvec=e1, minus_eigvec=e2, ellPminus_zero=e3, trace_matches=tr_ok, det_minus_one=det_ok, offdiag=[o1, o2], slope_residual=sl_res, min_gap=gap, sqrt2=math.sqrt(2))

# ---------- P4, P5
def omega(kv): return np.arcsin(np.sin(kv)/np.sqrt(2))
def sup_ratio(qmax):
    qg = np.linspace(-qmax, qmax, 400001); qg = qg[np.abs(qg) > 1e-2]   # below 1e-2 the q^4 difference is lost to rounding
    return float(np.max(np.abs(omega(qg-np.pi/2)+np.pi/4-qg**2/2)/(qg**4/6)))
# small q by mpmath (50 digits) so the leading-order tightness is examined too
mp.mp.dps = 50
small = [float(abs(mp.asin(mp.sin(mp.mpf(x)-mp.pi/2)/mp.sqrt(2))+mp.pi/4-mp.mpf(x)**2/2)/(mp.mpf(x)**4/6)) for x in (1e-6, 1e-4, 1e-3, 1e-2, 0.1)]
s1 = sup_ratio(1.0)
put("P4", s1 <= 1 and max(small) <= 1, sup_ratio_on_0p01_to_1=s1, ratios_at_small_q=small, sup_ratio_on_whole_chart_info=sup_ratio(np.pi/2))
def Pminus(kv):
    w_ = omega(kv); lp = np.exp(-1j*w_); lm = -np.exp(1j*w_)
    Uk = np.array([[np.exp(-1j*kv), np.exp(-1j*kv)], [np.exp(1j*kv), -np.exp(1j*kv)]])/np.sqrt(2)
    return (Uk - lp*np.eye(2))/(lm-lp)
P0 = Pminus(-np.pi/2); ellv = np.array([1, 1j])
qg = np.linspace(-1, 1, 20001); qg = qg[np.abs(qg) > 1e-6]
ra = max(np.linalg.norm(ellv @ Pminus(x-np.pi/2))/abs(x) for x in qg)
rb = max(np.linalg.norm(Pminus(x-np.pi/2)-P0, 2)/abs(x) for x in qg)
put("P5", ra <= math.sqrt(2) and rb <= 1, sup_ellPminus_over_q=float(ra), sup_dP_over_q=float(rb), ellPminus_at_kstar=float(np.linalg.norm(ellv @ P0)))

# ---------- ring machinery
class Ring:
    def __init__(self, N):
        self.N = N; self.x = np.arange(N); self.k = 2*np.pi*np.fft.fftfreq(N)
        self.car = np.array(I4)[self.x % 4]
        self.w = omega(self.k); self.lp = np.exp(-1j*self.w); self.lm = -np.exp(1j*self.w)
        e = np.exp(-1j*self.k)
        self.U = np.empty((N, 2, 2), complex)
        self.U[:, 0, 0] = e; self.U[:, 0, 1] = e; self.U[:, 1, 0] = e.conj(); self.U[:, 1, 1] = -e.conj()
        self.U /= np.sqrt(2)
        self.chart = (self.k >= -np.pi/2) & (self.k < np.pi/2)
    def enc(self, rails, t): return self.car*np.exp(-1j*np.pi*t/4)*(rails[0]+1j*rails[1])
    def dec(self, f, t):
        z = self.car.conj()*np.exp(1j*np.pi*t/4)*f; return np.array([z.real, z.imag]), float(np.max(abs(z.imag))) if False else np.array([z.real, z.imag])
    def spectral(self, rails, n):
        h = np.fft.fft(rails, axis=1).T                      # (N,2)
        Pp = (self.U - self.lm[:, None, None]*np.eye(2))/(self.lp-self.lm)[:, None, None]
        a = np.einsum("nij,nj->ni", Pp, h)
        h2 = np.exp(-1j*n*self.w)[:, None]*a + ((-1.0)**(n % 2))*np.exp(1j*n*self.w)[:, None]*(h-a)
        o = np.fft.ifft(h2.T, axis=1); return o.real, float(np.max(abs(o.imag)))
def step(R, L):
    return np.roll(R+L, 1)/np.sqrt(2), np.roll(R-L, -1)/np.sqrt(2)
def direct(rails, n):
    R, L = rails
    for _ in range(n): R, L = step(R, L)
    return np.array([R, L])

# P7a spectral vs direct
g = Ring(128); rails = np.zeros((2, 128)); rails[:, 1::2] = rng.standard_normal((2, 64))
d7 = max(float(np.max(abs(g.spectral(rails, n)[0]-direct(rails, n)))) for n in (1, 2, 5, 33, 200))
put("P7a", d7 < 1e-12, max_diff_spectral_vs_direct=d7, basis="200 steps of unit-norm data at eps=2.2e-16")

# ---------- P6, P7, P14
p6 = 0.0; p14 = 0.0; rows = []; viol = 0; qual = 0; nonvac = 0; maxratio = 0.0; minslack = 1e9
for it in range(400):
    N = int(rng.choice([64, 128, 256, 512, 1024])); g = Ring(N); par = int(rng.integers(0, 2)); t = int(rng.integers(0, 8))
    Q0 = float(rng.uniform(2*np.pi/N*1.5, 0.6)); eps_tail = float(rng.choice([0.0, 0.01, 0.1, 0.5]))
    core = np.where(g.chart & (abs(g.k) <= Q0), rng.standard_normal(N)+1j*rng.standard_normal(N), 0)
    tail = np.where(g.chart, rng.standard_normal(N)+1j*rng.standard_normal(N), 0)
    hat = core/np.linalg.norm(core) + eps_tail*tail/np.linalg.norm(tail)
    hat = hat + (-1)**par*np.roll(hat, N//2)          # replica at kappa+pi gives single-parity support
    f = np.fft.ifft(hat); f /= np.linalg.norm(f)
    leak = float(np.max(abs(f[(g.x-par) % 2 == 1])))
    f[(g.x-par) % 2 == 1] = 0.0
    z = g.car.conj()*np.exp(1j*np.pi*t/4)*f; rails = np.array([z.real, z.imag])
    Q = float(rng.uniform(0.02, 1.0)); n = int(round(10**rng.uniform(0, 6)))
    hyp = (N % 4 == 0) and leak < 1e-12 and abs(np.sum(rails**2)-1) < 1e-12 and 0 < Q <= 1
    qual += hyp
    Zt = np.fft.fft(g.enc(rails, t)); Fh = np.fft.fft(rails, axis=1)
    out_, im = g.spectral(rails, n); Zn = np.fft.fft(g.enc(out_, t+n))
    ch = g.chart; kq = g.k
    err = math.sqrt(2/N*np.sum(abs(Zn[ch]-np.exp(-0.5j*n*kq[ch]**2)*Zt[ch])**2))
    eQ = math.sqrt(2/N*np.sum(abs(Zt[ch & (abs(kq) > Q)])**2))
    bound = 2*math.sqrt(2)*Q + n*Q**4/6 + 2*eQ
    if err > bound: viol += 1
    if bound < 2: nonvac += 1; maxratio = max(maxratio, err/bound)
    minslack = min(minslack, bound-err)
    # P6: partner of chart frequency index j is (-j) mod N; F at k*+q is Fh at index shifted by -N/4
    idx = np.arange(N); Fq = np.roll(Fh, N//4, axis=1)          # Fq[:,j] = Fh[:, j-N/4] i.e. frequency k_j - pi/2
    lhs = abs(Zt[idx])**2 + abs(Zt[(-idx) % N])**2; rhs = 2*np.sum(abs(Fq)**2, axis=0)
    p6 = max(p6, float(np.max(abs(lhs-rhs))/np.max(rhs)))
    ff = g.enc(rails, t); p14 = max(p14, abs(np.sum(ff**2) - (2/N)*np.sum(Zt[ch]*Zt[(-idx) % N][ch])))
    if it < 12 or err > bound: rows.append(dict(N=N, parity=par, t=t, n=n, Q=Q, Q0=Q0, tail_weight=eps_tail, e_Q=eQ, err=err, bound=bound, leak=leak))
put("P6", p6 < 1e-12, max_relative_residual=p6)
put("P7", viol == 0 and qual == 400, instances=400, qualifying=int(qual), bound_below_2_nonvacuous=int(nonvac), violations=int(viol), max_err_over_bound_among_nonvacuous=maxratio, min_slack=minslack, sample=rows)
put("P14", p14 < 1e-12, max_abs_residual=float(p14))

# ---------- P8 exact preparation
def prep_exact(m):
    st = {(0, 0): 1}                                   # (site, rail) rail 0=R,1=L ; raw integer amplitudes
    for j in range(1, m+1):
        for _ in range(2):
            nw = {}
            for (x, c), a in st.items():
                nw[(x+1, 0)] = nw.get((x+1, 0), 0) + a           # R' gets R+L from x-1
                nw[(x-1, 1)] = nw.get((x-1, 1), 0) + (a if c == 0 else -a)
            st = {kk_: v_ for kk_, v_ in nw.items() if v_}
        want = j % 2                                   # odd block ends L (1), even block ends R (0)
        st = {kk_: v_ for kk_, v_ in st.items() if kk_[1] == want}
    return st
p8 = []; ok8 = True
for m in range(2, 41, 2):
    st = prep_exact(m)
    form = {(m-2*j, 0): (-1)**j*comb(m, j) for j in range(m+1)}
    pos = all(((-1)**(m//2)*I4[x % 4]*a).real > 0 and ((-1)**(m//2)*I4[x % 4]*a).imag == 0 for (x, c), a in st.items())
    okm = st == form and sum(a*a for a in st.values()) == comb(2*m, m) and pos
    ok8 &= okm; p8.append(dict(m=m, ok=okm, success=str(Fraction(comb(2*m, m), 4**m))))
odd = []
for m in (1, 3, 5):
    st = prep_exact(m); odd.append(dict(m=m, rails=sorted({c for (x, c) in st}), sites=sorted(x for (x, c) in st), mass=str(Fraction(sum(a*a for a in st.values()), 4**m))))
put("P8", ok8, even_m_checked=[r["m"] for r in p8], all_ok=ok8, success_m2_m4_m40=[p8[0]["success"], p8[1]["success"], p8[-1]["success"]], odd_m_info=odd,
    asymptotic_ratio_m40=float(Fraction(comb(80, 40), 4**40))*math.sqrt(math.pi*40))

# ---------- P9
def gauss_dist(m):
    d = 1/math.sqrt(m); p = np.linspace(-math.pi/(2*d), math.pi/(2*d), 400001)
    logc = 0.5*(m*math.log(4) - (math.lgamma(2*m+1)-2*math.lgamma(m+1)))
    with np.errstate(divide="ignore"):
        prof = np.exp(logc + 0.5*math.log(d/math.pi) + m*np.log(np.abs(np.cos(d*p))))
    G = math.pi**-0.25*np.exp(-p*p/2); h = p[1]-p[0]
    return math.sqrt(np.sum((prof-G)**2)*h + math.erfc(math.pi/(2*d)))
ms = [8, 32, 128, 512, 2048, 8192]; d9 = [gauss_dist(m) for m in ms]
put("P9", all(a > b for a, b in zip(d9, d9[1:])), m=ms, L2_distance=d9, ratio_successive=[a/b for a, b in zip(d9, d9[1:])])

# ---------- source and flights (direct real-space stepping on a ring larger than the light cone)
def source(m, N, shift=0):
    R = np.zeros(N); cen = comb(m, m//2)
    for j in range(m+1): R[(m-2*j+shift) % N] = (-1)**(m//2)*(-1)**j*(comb(m, j)/cen)
    R /= np.linalg.norm(R); return R
def ringsize(m, n): 
    N = 4
    while N <= 2*(m+n+2)+2: N *= 2
    return N
def coords(N):
    x = np.arange(N); return np.where(x < N//2, x, x-N)
def Cfun(tau): return 1/cmath.sqrt(1+1j*tau)
def block_int(tau, lo, hi):
    qq_ = mp.mpc(1, tau); return complex(mp.quad(lambda y: mp.exp(-y*y/qq_)/(mp.sqrt(mp.pi)*qq_), [lo, hi]))
mp.mp.dps = 20
BLOCKS = {"center": (-1.0, 1.0), "right": (0.5, 1.5), "offcenter_new": (-0.3, 0.7)}
def flight(m, n0, blocks=False, mixture=False, psi=False):
    N = ringsize(m, n0+1); x = coords(N); Y = x/math.sqrt(m)
    R = source(m, N); L = np.zeros(N); o = {}
    src_var = float(Y**2 @ R**2)
    for _ in range(n0): R, L = step(R, L)
    for n in (n0, n0+1):
        if n > n0: R, L = step(R, L)
        tot = R*R+L*L; mean = float(Y @ tot); tau = n/m
        d = float(np.sum(R*R-L*L)); f = np.array(I4)[x % 4]*np.exp(-1j*np.pi*n/4)*(R+1j*L)
        e = dict(n=n, tau=tau, d=d, var=float((Y-mean)**2 @ tot), norm=float(tot.sum()), wrong_parity=float(tot[(x-n) % 2 != 0].sum()),
                 enc_identity_residual=abs(d-((-1j)**(n % 4)*np.sum(f*f)).real))
        if blocks:
            for lab, (lo, hi) in BLOCKS.items():
                mk = (Y >= lo) & (Y <= hi); e["block_"+lab] = float(np.sum((R*R-L*L)[mk])); e["ref_"+lab] = list(map(float, (block_int(tau, lo, hi).real, block_int(tau, lo, hi).imag)))
        if psi and n == n0:
            g = Ring(N); Z = np.fft.fft(f); ch = g.chart; dl = 1/math.sqrt(m)
            T = math.sqrt(math.pi/dl)*math.pi**-0.25*np.exp(-(g.k[ch]/dl)**2/2*(1+1j*tau))
            e["psi_distance"] = math.sqrt(2/N*np.sum(abs(Z[ch]-T)**2) + math.erfc(math.pi/(2*dl)))
        o[n-n0] = e
    if mixture:
        N2 = ringsize(0, n0); x2 = coords(N2); R2 = np.zeros(N2); L2 = np.zeros(N2); R2[0] = 1
        for _ in range(n0): R2, L2 = step(R2, L2)
        dens = np.fft.fftshift(R2*R2+L2*L2); xs = np.fft.fftshift(x2)
        srcd = np.array([comb(m, j)**2 for j in range(m+1)], dtype=object); tot_ = sum(srcd); srcp = np.array([float(Fraction(int(a), int(tot_))) for a in srcd])
        srcx = np.array([m-2*j for j in range(m+1)])
        full = np.zeros(4*(len(dens)+m)); off = len(full)//2
        for a, sx in zip(srcp, srcx):
            if a > 0: full[off+sx+xs[0]: off+sx+xs[0]+len(dens)] += a*dens
        xx = (np.arange(len(full))-off)/math.sqrt(m); mu = float(xx @ full)
        o["release_site_read_variance"] = float((xx-mu)**2 @ full); o["mixture_norm"] = float(full.sum()); o["source_var"] = src_var
    return o

# ---------- P11
F512 = flight(512, 512, mixture=True)
c1 = Cfun(1.0)
chk = dict(d512=F512[0]["d"], d513=F512[1]["d"], var512=F512[0]["var"], site_read_var=F512["release_site_read_variance"], C1=[c1.real, c1.imag],
           norm=F512[0]["norm"], wrong_parity_mass=F512[0]["wrong_parity"], mixture_norm=F512["mixture_norm"])
put("P11", abs(chk["d512"]-0.778054) < 5e-7 and abs(chk["d513"]+0.320574) < 5e-7 and abs(chk["var512"]-0.997912) < 5e-7 and abs(chk["site_read_var"]-106.737) < 5e-4
    and abs(c1.real-0.776887) < 5e-7 and abs(c1.imag+0.321797) < 5e-7, **chk)

# ---------- P10, P12, P13, P15
p10 = {}; ok10 = True
for tau0 in (0.5, 1, 2, 3):
    ds = [flight(m, int(tau0*m), psi=True)[0]["psi_distance"] for m in (32, 128, 512, 2048)]
    p10[str(tau0)] = ds; ok10 &= all(a > b for a, b in zip(ds, ds[1:]))
put("P10", ok10, m=[32, 128, 512, 2048], distances=p10)
p12 = {}; ok12 = True; ok15 = True; p15 = {}; idres = 0.0
for tau0 in (0.5, 1, 3):
    e0 = []; e1 = []; ev = []; sg = []
    for m in (64, 256, 1024):
        fl = flight(m, int(tau0*m)); a, b = fl[0], fl[1]
        e0.append(abs(a["d"]-Cfun(a["tau"]).real)); e1.append(abs(b["d"]-Cfun(b["tau"]).imag)); sg.append(b["d"])
        ev.append(abs(a["var"]-(1+a["tau"]**2)/2)); idres = max(idres, a["enc_identity_residual"], b["enc_identity_residual"])
    p12[str(tau0)] = dict(err_real=e0, err_imag=e1, d_n_plus_1=sg); p15[str(tau0)] = ev
    ok12 &= all(x_ > y_ for x_, y_ in zip(e0, e0[1:])) and all(x_ > y_ for x_, y_ in zip(e1, e1[1:])) and all(v_ < 0 for v_ in sg)
    ok15 &= all(x_ > y_ for x_, y_ in zip(ev, ev[1:]))
# odd launch site: same physical d, encoded expression changes sign
m, n = 64, 64; N = ringsize(m, n+2); x = coords(N); odd_res = []
for shift in (0, 1):
    R = source(m, N, shift); L = np.zeros(N)
    for nn in range(1, n+2):
        R, L = step(R, L)
        if nn >= n:
            f = np.array(I4)[x % 4]*np.exp(-1j*np.pi*nn/4)*(R+1j*L); d = float(np.sum(R*R-L*L))
            odd_res.append(dict(launch=shift, n=nn, d=d, residual=abs(d-(-1)**shift*((-1j)**(nn % 4)*np.sum(f*f)).real)))
put("P12", ok12 and idres < 1e-12 and all(r["residual"] < 1e-12 for r in odd_res), m=[64, 256, 1024], by_tau=p12, identity_residual_even=idres, odd_launch=odd_res)
put("P15", ok15, m=[64, 256, 1024], abs_variance_error=p15)
p13 = {lab: dict(err_real=[], err_imag=[]) for lab in BLOCKS}
for m in (64, 256, 1024, 4096):
    fl = flight(m, m, blocks=True)
    for lab in BLOCKS:
        p13[lab]["err_real"].append(abs(fl[0]["block_"+lab]-fl[0]["ref_"+lab][0])); p13[lab]["err_imag"].append(abs(fl[1]["block_"+lab]-fl[1]["ref_"+lab][1]))
ok13 = all(all(a > b for a, b in zip(v_, v_[1:])) for lab in BLOCKS for v_ in p13[lab].values())
put("P13", ok13, m=[64, 256, 1024, 4096], errors=p13)

# ---------- P16
rat = []
for dl in (0.2, 0.14, 0.1, 0.07, 0.05):
    T = round(dl**-2.8); w_ = dl**1.1; v_ = dl*1.0; N = ringsize(0, T); x = coords(N)
    R = np.zeros(N); L = np.zeros(N); R[0] = 1
    for _ in range(T): R, L = step(R, L)
    p = float(np.sum((R*R+L*L)[abs(x/T-v_) <= w_])); pneg = float(np.sum((R*R+L*L)[abs(x/T+v_) <= w_]))
    konno = (1-v_)/(math.pi*(1-v_**2)*math.sqrt(1-2*v_**2))*2*w_
    rat.append(dict(delta=dl, T=T, w=w_, v=v_, p_yes=p, ratio_to_2w_over_pi=p/(2*w_/math.pi), ratio_window_at_minus_v=pneg/(2*w_/math.pi), konno_density_times_2w_ratio=konno/(2*w_/math.pi)))
dev = [abs(r["ratio_to_2w_over_pi"]-1) for r in rat]
put("P16", all(a > b for a, b in zip(dev, dev[1:])), rows=rat, abs_dev=dev)

res["failed"] = [k_ for k_, v_ in res["predicates"].items() if not v_["passed"]]
print("FAILED:", res["failed"])
os.makedirs(sys.argv[1], exist_ok=True)
with open(os.path.join(sys.argv[1], "xfolded_result.json"), "x") as fh:
    json.dump(res, fh, indent=1, default=str); fh.write("\n")
