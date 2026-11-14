"""Cross-review program for Director_G/Window_source_cost.md (written from the note's
definitions, not from its checker).  Seed 20261113.  OMP_NUM_THREADS=1.

CONVENTIONS
  Walk: raw step A sends (R,L) at site x to R+L on the right rail at x+1 and R-L on the
  left rail at x-1; U=A/sqrt2; start (0,R).  Fourier kernel exp(-ikx), measure dk/2pi,
  U(k)=diag(e^{-ik},e^{ik})H.  Windows are inclusive at both edges.  Velocity of an
  eigenvector with eigenvalue lam(k): the band with Re lam>0 has nu=+cos k/sqrt(1+cos^2 k),
  the band with Re lam<0 has nu=-cos k/sqrt(1+cos^2 k) (checked in P0 against the drift
  of the mean position, not assumed).  L = number of sites of the occupied parity
  (x = T mod 2) in the window.

PREDICATES (fixed before the first run)
  P0  band/velocity convention: for 5 random packets on 12 sites, the spectral mean
      velocity equals (<x>_n - <x>_0)/n at n=4000 within 2*span/n + 1e-9, where the basis
      is that <x>_n - <x>_0 - n<V> is bounded by the position-operator commutator term,
      measured here and reported (no free threshold: the measured gap is recorded).
  P1  exact acceptance (integers): T=16,W=[0,2] is 1275/16384 with 37 trials for failure
      <=1/20; T=64,W=[2,6] is 282728967155285175/2^63 with 97 trials.  Trials counted by
      exact rational powers.  Unreported panels T=32,W=[0,2]; T=128,W=[2,6]; T=17,W=[0,2]
      (odd T) are computed and the note's formula ceil(log a/log(1-p)) (floating) is
      compared with the exact count on every panel.
  P2  Fourier bound: for every tested packet h supported on L sites and every tested
      region K, integral_K |hhat|^2 dk/2pi <= L|K|/2pi (exact inequality; tolerance 1e-12
      = quadrature rounding on O(1) quantities).  Hypothesis tested per instance:
      normalisation |h|=1 within 1e-12 and support size == L; number qualifying reported.
  P3  |K| <= C*delta*eta: measured C = |K|/(delta*eta) over the grid delta in
      {1/5,1/10,1/20,1/40,1/80,1/160}, p0 in {0,0.5,1,3}, eta in {0.1,0.5,1,2}; instances
      qualify if delta*(|p0|+eta) < 1/sqrt2 (inside the velocity cone).  Predicate: C
      bounded on the qualifying grid and -> 8 as delta->0 (regular roots, slope 1); report
      sup C.  No threshold; the sup is the result.
  P4  velocity bound on PREPARED states: for the published scaling w=delta^(11/10),
      T=round(delta^(-14/5)), p0=1, delta in {1/10,1/20,1/30,1/40}, eta in {0.25,0.5,1}:
      Pr_h(|V/delta-p0|<=eta) <= L|K|/2pi, and report Pr, L*delta, and the tail 1-Pr.
  P5  interior sharp-launch bound: M(T)=max over |x|<=0.3T of T*P_T(x).  The note's C/T law
      predicts M(4096)/M(64) -> 1; a T^(-2/3) (caustic) law would give 64^(1/3)=4.
      Predicate: ratio < 2 (geometric midpoint of the two laws).  Also report the same
      ratio at the caustic |x|/T in [0.68,0.73], where the note claims no bound.
  P6  p <= C(w+1/T): report sup of p/(w+1/T) over T in {64,256,1024,4096}, v in
      {0,0.05,0.1,0.2}, w in {0.5/T,1/T,0.01,0.03,0.1}; and p/(2w/pi) at the published
      scaling for the four delta of P4 (note: p ~ 2w/pi).
  P7  serial accounting: (a) for p=1e-2..1e-6, b=c*p, B=1, c in {0.5,1,3}:
      |1-(1-p)^floor(B/b) - (1-exp(-B/c))| decreases with p and is < 2p*(B/c+1) (basis:
      first-order expansion error p*K*p/2 plus one-trial floor error p); (b) exactly-one
      success probability J p (1-p)^(J-1) maximised over J for p in {1e-2,1e-3}: max <=
      1/e + p (so a finite fraction >= 1-1/e-p is lost).
  P8  exponents (exact rationals): duration power r+2-14/5, mean power minus 11/10:
      r=1 -> 1/5, -9/10; r=9/10 -> 1/10, -1.  Published-theorem conditions at r=9/10:
      a/w power 4/5>0, aTw power 1/5>0.
  P9  threshold r>3/2: for r in {1,5/4,3/2,1501/1000,7/4,2,3} a rational grid search over
      beta in (1, r+1) step 1/200 and gamma step 1/200 finds a point with
      beta>1, 5beta/2<gamma<r+2-beta, gamma<r+1+beta, beta<r+1 iff r>3/2 AND the closed
      form sup beta=(2r+4)/7 >1 iff r>3/2.  (Grid may miss a thin region: for r=1501/1000
      the closed form decides; grid outcome is recorded either way.)  The example
      (7/4,51/50,13/5) satisfies all conditions with mean power 13/100.
  P10 lower-bound identity: T*tau/w == (eps*delta/w^2)*(delta*T*w) symbolically.
  P11 lane count: number of integer multiples of l within distance c*B of an arbitrary
      port position y is <= 1+2cB/l for 2000 random (l,cB,y).
"""
import json, os, sys, math, time
from fractions import Fraction as Fr
import numpy as np, sympy as sp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'xcost_result.json')
if os.path.exists(OUT):
    sys.exit('refusing to overwrite ' + OUT)
rng = np.random.default_rng(20261113)
res = {'seed': 20261113, 'predicates': {}, 'failed': []}
t0 = time.time()


def put(name, ok, **kw):
    res['predicates'][name] = dict(passed=bool(ok), **kw)
    if not ok:
        res['failed'].append(name)
    print(name, 'PASS' if ok else 'FAIL', json.dumps(kw, default=str)[:600], flush=True)


def raw_walk(T):
    st = {0: (1, 0)}
    for _ in range(T):
        nx = {}
        for x, (r, l) in st.items():
            a = nx.get(x + 1, (0, 0)); nx[x + 1] = (a[0] + r + l, a[1])
            b = nx.get(x - 1, (0, 0)); nx[x - 1] = (b[0], b[1] + r - l)
        st = nx
    return st


def fwalk(T):
    """float amplitudes, index x+T"""
    R = np.zeros(2 * T + 3); L = np.zeros(2 * T + 3)
    R[T + 1] = 1.0
    s = 1 / math.sqrt(2)
    for _ in range(T):
        a = (R + L) * s; b = (R - L) * s
        R = np.roll(a, 1); L = np.roll(b, -1)
    return R[1:-1], L[1:-1]  # index i <-> x=i-T


def nu(k):
    return np.cos(k) / np.sqrt(1 + np.cos(k) ** 2)


def bands(k):
    """projectors onto Re lam>0 (velocity +nu) and Re lam<0 (velocity -nu) at each k."""
    s = 1 / math.sqrt(2)
    U = np.empty((len(k), 2, 2), complex)
    U[:, 0, 0] = np.exp(-1j * k) * s; U[:, 0, 1] = np.exp(-1j * k) * s
    U[:, 1, 0] = np.exp(1j * k) * s; U[:, 1, 1] = -np.exp(1j * k) * s
    w = np.arcsin(np.sin(k) / math.sqrt(2))
    lam = np.exp(-1j * w)          # Re>0 ; other eigenvalue is -conj(lam)
    I = np.eye(2)[None]
    Pp = (U + np.conj(lam)[:, None, None] * I) / (lam + np.conj(lam))[:, None, None]
    return Pp, I - Pp


def hhat(k, xs, hR, hL):
    E = np.exp(-1j * np.outer(k, xs))
    return np.stack([E @ hR, E @ hL], axis=1)


def K_intervals(delta, p0, eta):
    """k-intervals per band where |nu_b - delta p0| <= delta eta. returns (plus, minus)."""
    lo, hi = delta * (p0 - eta), delta * (p0 + eta)
    c = lambda u: u / math.sqrt(1 - u * u)
    def pre(lo, hi):  # k in [0,pi] with cos k in [c(lo),c(hi)], and mirror
        a, b = math.acos(min(1, c(hi))), math.acos(max(-1, c(lo)))
        return [(a, b), (-b, -a)]
    return pre(lo, hi), pre(-hi, -lo)


def union_len(iv):
    iv = sorted(iv); tot = 0; cur = None
    for a, b in iv:
        if cur is None: cur = [a, b]
        elif a <= cur[1]: cur[1] = max(cur[1], b)
        else: tot += cur[1] - cur[0]; cur = [a, b]
    return tot + cur[1] - cur[0]


GLx, GLw = np.polynomial.legendre.leggauss(40)
def integ(f, a, b, pieces):
    tot = 0.0
    ed = np.linspace(a, b, pieces + 1)
    for u, v in zip(ed[:-1], ed[1:]):
        k = (u + v) / 2 + (v - u) / 2 * GLx
        tot += (v - u) / 2 * np.dot(GLw, f(k))
    return tot


def vel_prob(xs, hR, hL, delta, p0, eta):
    plus, minus = K_intervals(delta, p0, eta)
    span = xs.max() - xs.min() + 1
    def fb(which):
        def f(k):
            H = hhat(k, xs, hR, hL); Pp, Pm = bands(k)
            P = Pp if which == 0 else Pm
            v = np.einsum('kij,kj->ki', P, H)
            return (np.abs(v) ** 2).sum(1)
        return f
    def ft(k):
        return (np.abs(hhat(k, xs, hR, hL)) ** 2).sum(1)
    pr = 0.0; full = 0.0
    for which, ivs in ((0, plus), (1, minus)):
        for a, b in ivs:
            pcs = max(4, int(2 * span * (b - a) / 10) + 4)
            pr += integ(fb(which), a, b, pcs) / (2 * math.pi)
    allk = plus + minus
    # integral of the full spinor norm over the union K (merge overlaps)
    iv = sorted(allk); merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], b)
        else: merged.append([a, b])
    for a, b in merged:
        pcs = max(4, int(2 * span * (b - a) / 10) + 4)
        full += integ(ft, a, b, pcs) / (2 * math.pi)
    return pr, full, union_len(allk)


# ---------- P0
gaps = []; ok = True
for _ in range(5):
    xs = np.arange(12); hR = rng.normal(size=12) + 1j * rng.normal(size=12); hL = rng.normal(size=12) + 1j * rng.normal(size=12)
    n0 = math.sqrt((abs(hR) ** 2 + abs(hL) ** 2).sum()); hR /= n0; hL /= n0
    def f(k):
        H = hhat(k, xs, hR, hL); Pp, Pm = bands(k)
        vp = (np.abs(np.einsum('kij,kj->ki', Pp, H)) ** 2).sum(1); vm = (np.abs(np.einsum('kij,kj->ki', Pm, H)) ** 2).sum(1)
        return nu(k) * (vp - vm)
    Vm = integ(f, -math.pi, math.pi, 64) / (2 * math.pi)
    n = 4000; N = 2 * n + 40
    R = np.zeros(N, complex); L = np.zeros(N, complex); R[n + 10:n + 22] = hR; L[n + 10:n + 22] = hL
    X = np.arange(N); x0 = (X * (abs(R) ** 2 + abs(L) ** 2)).sum()
    s = 1 / math.sqrt(2)
    for _ in range(n):
        a = (R + L) * s; b = (R - L) * s; R = np.roll(a, 1); L = np.roll(b, -1)
    xn = (X * (abs(R) ** 2 + abs(L) ** 2)).sum()
    g = abs((xn - x0) / n - Vm); gaps.append(g); ok &= g < 2 * 12 / n + 1e-9
put('P0_band_velocity_convention', ok, max_gap=max(gaps), allowed=2 * 12 / 4000 + 1e-9)

# ---------- P1
def panel(T, lo, hi):
    st = raw_walk(T)
    assert sum(r * r + l * l for r, l in st.values()) == 2 ** T
    mass = sum(sum(v * v for v in st.get(x, (0, 0))) for x in range(lo, hi + 1))
    p = Fr(mass, 2 ** T); n = 0; resid = Fr(1)
    while 20 * resid > 1:
        n += 1; resid *= (1 - p)
    nf = math.ceil(math.log(0.05) / math.log(1 - float(p)))
    return dict(T=T, W=[lo, hi], p=str(p), p_float=float(p), trials_exact=n, trials_note_formula_float=nf,
                rows=[[x, *st.get(x, (0, 0))] for x in range(lo, hi + 1)])
pan = [panel(16, 0, 2), panel(64, 2, 6), panel(32, 0, 2), panel(128, 2, 6), panel(17, 0, 2)]
ok = (pan[0]['p'] == '1275/16384' and pan[0]['trials_exact'] == 37 and
      pan[1]['p'] == '282728967155285175/9223372036854775808' and pan[1]['trials_exact'] == 97 and
      all(q['trials_exact'] == q['trials_note_formula_float'] for q in pan))
put('P1_exact_panels', ok, panels=pan)

# ---------- P2 random packets
cnt = 0; qual = 0; worst = -1e9; ok = True
for _ in range(300):
    Lc = int(rng.integers(1, 40)); gap = int(rng.integers(1, 3))
    xs = np.arange(Lc) * gap
    hR = rng.normal(size=Lc) + 1j * rng.normal(size=Lc); hL = rng.normal(size=Lc) + 1j * rng.normal(size=Lc)
    if rng.random() < 0.3:  # adversarial: constant-phase packet peaked at a k inside K
        k0 = rng.uniform(-math.pi, math.pi); hR = np.exp(1j * k0 * xs); hL = 0 * hR
    n0 = math.sqrt((abs(hR) ** 2 + abs(hL) ** 2).sum()); hR /= n0; hL /= n0
    cnt += 1
    if abs((abs(hR) ** 2 + abs(hL) ** 2).sum() - 1) > 1e-12 or len(xs) != Lc: continue
    qual += 1
    a = rng.uniform(-math.pi, math.pi); ln = rng.uniform(0, 1.0) * rng.choice([0.01, 0.1, 1.0])
    if rng.random() < 0.3 and Lc > 1: a = k0 - ln / 2 if 'k0' in dir() else a
    val = integ(lambda k: (np.abs(hhat(k, xs, hR, hL)) ** 2).sum(1), a, a + ln, 8 + 2 * Lc) / (2 * math.pi)
    slack = val - Lc * ln / (2 * math.pi); worst = max(worst, slack / (Lc * ln / (2 * math.pi)))
    ok &= slack <= 1e-12
put('P2_fourier_bound_random', ok, instances=cnt, qualifying=qual, max_relative_excess=worst,
    note='max_relative_excess is (lhs-rhs)/rhs; 0 would be saturation, negative means strict')

# ---------- P3
Cs = []; nq = 0; tot = 0
for d in [1 / 5, 1 / 10, 1 / 20, 1 / 40, 1 / 80, 1 / 160]:
    for p0 in [0, 0.5, 1, 3]:
        for eta in [0.1, 0.5, 1, 2]:
            tot += 1
            if d * (abs(p0) + eta) >= 1 / math.sqrt(2): continue
            nq += 1
            pl, mi = K_intervals(d, p0, eta)
            Cs.append((union_len(pl + mi) / (d * eta), d, p0, eta, (union_len(pl) + union_len(mi)) / (d * eta)))
supC = max(Cs); smallC = [c[0] for c in Cs if c[1] == 1 / 160]
put('P3_K_length_constant', True, instances=tot, qualifying=nq, sup_C_union=supC[0], at=supC[1:4],
    sup_C_sum_of_bands=max(c[4] for c in Cs), C_range_at_delta_1_160=[min(smallC), max(smallC)],
    note='C counts the union over both bands; sum over bands (what the projector argument needs if K is taken per band) is also given')

# ---------- P4, P6b prepared states at published scaling
p4 = []; ok4 = True
for inv in [10, 20, 30, 40]:
    d = 1 / inv; w = d ** 1.1; T = round(d ** -2.8); v = d
    R, L = fwalk(T)
    lo = math.ceil(T * (v - w) - 1e-12); hi = math.floor(T * (v + w) + 1e-12)
    xs_all = np.arange(lo, hi + 1); m = (abs(R[xs_all + T]) + abs(L[xs_all + T])) > 0
    par = (xs_all - T) % 2 == 0
    xs = xs_all[par]; hR = R[xs + T].astype(complex); hL = L[xs + T].astype(complex)
    p = float((abs(hR) ** 2 + abs(hL) ** 2).sum()); hR /= math.sqrt(p); hL /= math.sqrt(p)
    Lc = len(xs)
    row = dict(inv_delta=inv, T=T, w=w, window=[lo, hi], L=Lc, L_bound_Tw_plus_1=T * w + 1, L_delta=Lc * d,
               delta_T_w=d * T * w, p=p, p_over_2w_pi=p / (2 * w / math.pi), p_over_w_plus_1_T=p / (w + 1 / T),
               mean_serial_time_over_pi2_delta_m09=(T * d ** 3 / p) / (math.pi / 2 * d ** -0.9), eta=[])
    ok4 &= Lc <= T * w + 1 and int(m.sum()) <= Lc
    for eta in [0.25, 0.5, 1.0]:
        pr, full, Kl = vel_prob(xs, hR, hL, d, 1.0, eta)
        bound = Lc * Kl / (2 * math.pi)
        row['eta'].append(dict(eta=eta, Pr=pr, tail=1 - pr, spinor_mass_on_K=full, bound_L_K_over_2pi=bound, K_len=Kl))
        ok4 &= pr <= full + 1e-10 and full <= bound + 1e-10
    p4.append(row); print(' P4 row', inv, round(time.time() - t0, 1), flush=True)
put('P4_velocity_bound_prepared_states', ok4, rows=p4)

# ---------- P5
M = {}; Mc = {}
for T in [64, 256, 1024, 4096]:
    R, L = fwalk(T); P = R ** 2 + L ** 2; x = np.arange(-T, T + 1)
    M[T] = float(T * P[abs(x) <= 0.3 * T].max())
    Mc[T] = float(T * P[(abs(x) >= 0.68 * T) & (abs(x) <= 0.73 * T)].max())
put('P5_interior_C_over_T', M[4096] / M[64] < 2, T_times_maxP_interior=M, ratio=M[4096] / M[64],
    T_times_maxP_caustic=Mc, caustic_ratio=Mc[4096] / Mc[64])

# ---------- P6
sup = (0,)
for T in [64, 256, 1024, 4096]:
    R, L = fwalk(T); P = R ** 2 + L ** 2
    for v in [0, 0.05, 0.1, 0.2]:
        for w in [0.5 / T, 1 / T, 0.01, 0.03, 0.1]:
            lo = math.ceil(T * (v - w) - 1e-12); hi = math.floor(T * (v + w) + 1e-12)
            p = float(P[lo + T:hi + T + 1].sum()) if hi >= lo else 0.0
            sup = max(sup, (p / (w + 1 / T), T, v, w, p))
put('P6_p_le_C_w_plus_1_over_T', True, sup_ratio=sup[0], at=dict(T=sup[1], v=sup[2], w=sup[3], p=sup[4]),
    published_scaling_p_over_2w_pi=[(r['inv_delta'], r['p_over_2w_pi']) for r in p4])

# ---------- P7
ok = True; rows = []
for c in [0.5, 1, 3]:
    prev = None
    for p in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        K = math.floor(1 / (c * p) + 1e-9); s = -math.expm1(K * math.log1p(-p)); e = abs(s - (1 - math.exp(-1 / c)))
        ok &= e < 2 * p * (1 / c + 1) and (prev is None or e < prev); prev = e; rows.append((c, p, s, e))
one = []
for p in [1e-2, 1e-3]:
    best = max(J * p * (1 - p) ** (J - 1) for J in range(1, int(5 / p)))
    one.append((p, best)); ok &= best <= 1 / math.e + p
put('P7_serial_limits', ok, limit_rows=rows, exactly_one_max=one, one_over_e=1 / math.e)

# ---------- P8
def powers(r):
    dur = r + 2 - Fr(14, 5); return dur, dur - Fr(11, 10)
ok = powers(Fr(1)) == (Fr(1, 5), Fr(-9, 10)) and powers(Fr(9, 10)) == (Fr(1, 10), Fr(-1))
r = Fr(9, 10); aw = r + 1 - Fr(11, 10); aTw = r + 1 - Fr(14, 5) + Fr(11, 10); Tw52 = Fr(14, 5) - Fr(5, 2) * Fr(11, 10)
ok &= aw == Fr(4, 5) and aTw == Fr(1, 5) and Tw52 > 0
put('P8_exponents', ok, r1=[str(x) for x in powers(Fr(1))], r09=[str(x) for x in powers(Fr(9, 10))],
    a_over_w_power=str(aw), aTw_power=str(aTw), T_w52_divergence_power=str(Tw52),
    lanes_fixed_deadline=['9/10', '1'], single_round='11/10')

# ---------- P9
rows = []; ok = True
for r in [Fr(1), Fr(5, 4), Fr(3, 2), Fr(1501, 1000), Fr(7, 4), Fr(2), Fr(3)]:
    found = None; b = Fr(1) + Fr(1, 200)
    while b < r + 1 and found is None:
        g = Fr(math.floor(Fr(5, 2) * b * 200) + 1, 200)
        if Fr(5, 2) * b < g < r + 2 - b and g < r + 1 + b: found = (str(b), str(g))
        b += Fr(1, 200)
    closed = (2 * r + 4) / 7 > 1
    rows.append(dict(r=str(r), grid_point=found, closed_form_sup_beta=str((2 * r + 4) / 7), closed_feasible=closed, expected=r > Fr(3, 2)))
    ok &= closed == (r > Fr(3, 2)) and (found is None or closed)
r, b, g = Fr(7, 4), Fr(51, 50), Fr(13, 5)
ex = b > 1 and Fr(5, 2) * b < g < r + 2 - b and g < r + 1 + b and b < r + 1 and (r + 2 - g - b) == Fr(13, 100)
put('P9_threshold_three_halves', ok and ex, rows=rows, example_mean_power=str(r + 2 - g - b), example_ok=ex)

# ---------- P10
e, d, T, w = sp.symbols('epsilon delta T w', positive=True)
put('P10_lower_bound_identity', sp.simplify(T * e * d ** 2 / w - (e * d / w ** 2) * (d * T * w)) == 0, expr='T*tau/w - (eps*delta/w^2)(delta*T*w) simplifies to 0')

# ---------- P11
ok = True; worst = -1e9
for _ in range(2000):
    l = rng.uniform(0.1, 3); cB = rng.uniform(0, 20); y = rng.uniform(-5, 5)
    n = math.floor((y + cB) / l) - math.ceil((y - cB) / l) + 1
    ok &= n <= 1 + 2 * cB / l + 1e-12; worst = max(worst, n - (1 + 2 * cB / l))
put('P11_lane_count', ok, max_count_minus_bound=worst)

res['seconds'] = time.time() - t0
with open(OUT, 'x') as f:
    json.dump(res, f, indent=1, default=str)
print('failed:', res['failed'], 'seconds', res['seconds'])
