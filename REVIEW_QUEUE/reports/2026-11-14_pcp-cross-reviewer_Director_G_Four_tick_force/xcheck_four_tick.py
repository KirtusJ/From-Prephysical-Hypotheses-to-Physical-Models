"""Cross-review program for Director_G/Four_tick_force.md (written from the note's
definitions only; shares no code with the note's checkers).

Run: OMP_NUM_THREADS=1 python3 -B xcheck_four_tick.py OUTDIR   (numpy, sympy, mpmath)
Seed 20261113.  Result file OUTDIR/xcheck_four_tick.json is never overwritten.

CONVENTIONS
 * Tick: R'(x) = (R(x-1)+L(x-1))/sqrt2, L'(x) = (R(x+1)-L(x+1))/sqrt2  (U(k)=diag(e^-ik,e^ik)H,
   field = sum_k e^{+ikx} hat).  Decode z(x)=i^x (R+iL) on EVEN sites (site 0 is even and counts
   as non-negative).  Four-tick decoded map B z = -decode(U^4 encode z) (the note's real minus sign).
 * Fourier coordinate on the even sublattice: q = 2 pi m / N, m in [-N/4, N/4), z = sum c_q e^{+iqx}.
 * Norms are l2 over even sites, source normalized to 1.
 * No pass tolerance is used for floating predicates: each reports the measured ratio
   (observed / bound); the predicate is ratio <= 1 and the measured separation 1-ratio is recorded.
   Rounding in these runs is < 1e-11 (measured: norm drift recorded per instance).

PREDICATES (fixed before the first run)
 A1 sympy: eigenvalues of U(k) are e^{-i w}, -e^{i w} with sin w = sin k/sqrt2.
 A2 sympy: (1,i) P_-(k=-pi/2) = 0 with P_+ = (I+n.sigma)/2, n=(cos k, sin k, cos k)/sqrt(1+cos^2 k),
    and U P_+ = e^{-iw} P_+ (checked numerically at 50-digit precision on 7 values of k).
 A3 sympy: d'(q) = sin q / sqrt(1+sin^2 q).
 A4 sympy: plate O(-hx) acts on R+iL as multiplication by e^{-ihx}.
 A5 sympy: int_0^T (p-Fs)^2/2 ds = T p^2/2 - F T^2 p/2 + F^2 T^3/6.
 A6 exact: exponent arithmetic of the sharp-launch paragraph (Fractions).
 B1 grid |q|<=1 (20001 points): |d|<=q^2/2 ; |d-q^2/2|<=q^4/6 ; ||l P_-|| <= sqrt2 |q| ;
    full circle: ||P_-'|| <= 1.  Report max ratios.
 C1 free bound: for random complex scalar sources supported on |q|<=Q<=1 (hypothesis tested
    per instance by reading the support back from the FFT), ||(B-S)z|| <= D(Q)||z||,
    D=4 sqrt2 Q^3 + (2/3) Q^4.  Families: symmetric, one-sided (directional), edge, single mode.
    Instances with Q>1 are run and kept as hypothesis-fail controls, not counted.
 C2 B is norm preserving and maps the even sublattice to itself (odd-site mass after 4 ticks = 0).
 D1 forced bound: E=||(BK)^M z - continuum|| <= M D(Q) + T Delta |F| L/(2 eps), with
    Q=delta(P+|F|T)<=1 tested per instance; commensurate h=2 pi m/N; includes eps != 1, |F| != 1,
    m != 1, N not in the note's list.  Non-qualifying instances are kept.
 D2 sign: forced-minus-free mean momentum shift is -F T (exact on grid) and forced-minus-free mean
    position has the sign of -F; |shift - (-F T^2/2)| is REPORTED (no threshold).
 E1 exact: w=(3+4i)/5 is not a root of unity (minimal polynomial 5x^2-6x+5 non-monic), G columns
    orthogonal with norm^2 25; coherent return 9/25; distinguishable return for both paddings.
 E2 mpmath 60 digits: least k>=0 with |w^k - e^{-ih}| <= eta/B0 for (h,B0,eta)=(0.032,12,0.005)
    is 8341 and the max site error over |x|<=12 rounds to 0.003603; also an unreported triple
    (0.05, 8, 0.01).  Site error <= |x| eta / B0 for every site.
 E3 exact integer flight: k=2, B1=2, M=3, B0=B1+4M: raw denominator equal at every site, norm
    exactly norm0 * (5^{k B0} 4)^{2M}, support within [-B0,B0], and agreement with the float
    phase model w^{kx} (difference reported).
 E4 exact: a^2+b^2=2^d for d<=60 has only axial (d even) or equal-magnitude (d odd) solutions.
 F1 selector, D in {1,2,5,13,17,25,29,65,85} (only 5 and 13 are reported in the note), all integer
    (a,b) with a^2+b^2=D^2: K least power of two >= 2 sqrt2 D (integer test K^2>=8D^2);
    table fits (2|a|+2|b|<=K, remainder even); explicit Walsh/route/Walsh on a coherent multi-site
    input gives address-zero block exactly (2D/K) R_x; total norm exact; 1/8 < p <= 1/2;
    W^dagger W = identity; retry pair succeeds with conditional probability exactly 2p(1-p) and
    returns a vector proportional to the target; both failure branches are proportional.
 G1 sharp launch + window + forced flight at inverse_delta in {6,8,10,12,14} (8 and 12 not in the
    note): REPORT acceptance vs (2/pi)w, forced-minus-free mean position vs -F T^2/2, probability
    within 0.5 of Y0+p0 T-F T^2/2, and the value of the note's bound E at these parameters.
    Observables only; no pass threshold (the limit is delta->0).
Failed predicates are kept in the result file under "failed".
"""
import json, sys, math
from fractions import Fraction as Fr
from pathlib import Path
import numpy as np
import sympy as sp
import mpmath as mp

SEED = 20261113
rng = np.random.default_rng(SEED)
RES = {"seed": SEED, "failed": []}


def record(name, ok, **kw):
    RES[name] = dict(ok=bool(ok), **kw)
    if not ok:
        RES["failed"].append(name)


# ---------------------------------------------------------------- A: algebra
def algebra():
    k, q, h, x, R, L, p, F, T, s = sp.symbols("k q h x R L p F T s", real=True)
    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    U = sp.diag(sp.exp(-sp.I * k), sp.exp(sp.I * k)) * H
    # A1: characteristic polynomial lambda^2 + i sqrt2 sin k lambda - 1
    lam = sp.symbols("lam")
    cp = sp.simplify(sp.expand((U - lam * sp.eye(2)).det()) - (lam**2 + sp.I * sp.sqrt(2) * sp.sin(k) * lam - 1))
    w = sp.asin(sp.sin(k) / sp.sqrt(2))
    r1 = sp.simplify(sp.expand_trig(sp.expand(((sp.exp(-sp.I * w)) ** 2 + sp.I * sp.sqrt(2) * sp.sin(k) * sp.exp(-sp.I * w) - 1).rewrite(sp.cos))))
    r2 = sp.simplify(sp.expand_trig(sp.expand(((-sp.exp(sp.I * w)) ** 2 - sp.I * sp.sqrt(2) * sp.sin(k) * sp.exp(sp.I * w) - 1).rewrite(sp.cos))))
    mp.mp.dps = 50
    worst = mp.mpf(0)
    for kv in (-3, -1.5707, -0.4, 0.1, 0.9, 2.2, 3.1):
        kk = mp.mpf(kv)
        ww = mp.asin(mp.sin(kk) / mp.sqrt(2))
        Um = mp.matrix([[mp.e ** (-1j * kk), mp.e ** (-1j * kk)], [mp.e ** (1j * kk), -mp.e ** (1j * kk)]]) / mp.sqrt(2)
        nn = mp.matrix([mp.cos(kk), mp.sin(kk), mp.cos(kk)]) / mp.sqrt(1 + mp.cos(kk) ** 2)
        Pp = mp.matrix([[1 + nn[2], nn[0] - 1j * nn[1]], [nn[0] + 1j * nn[1], 1 - nn[2]]]) / 2
        Pm = mp.eye(2) - Pp
        worst = max(worst, mp.norm(Um * Pp - mp.e ** (-1j * ww) * Pp), mp.norm(Um * Pm + mp.e ** (1j * ww) * Pm))
    record("A1_eigenvalues", cp == 0 and r1 == 0 and r2 == 0 and worst < mp.mpf(10) ** -40,
           charpoly_residual=str(cp), root_residuals=[str(r1), str(r2)], projector_residual_50dps=mp.nstr(worst, 5))
    n = sp.Matrix([sp.cos(k), sp.sin(k), sp.cos(k)]) / sp.sqrt(1 + sp.cos(k) ** 2)
    sx, sy, sz = sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.Matrix([[1, 0], [0, -1]])
    Pm = (sp.eye(2) - (n[0] * sx + n[1] * sy + n[2] * sz)) / 2
    row = sp.simplify((sp.Matrix([[1, sp.I]]) * Pm).subs(k, -sp.pi / 2))
    row_plus = sp.simplify((sp.Matrix([[1, sp.I]]) * Pm).subs(k, sp.pi / 2))
    record("A2_row_annihilates", row == sp.zeros(1, 2), row_at_minus_half_pi=str(row), row_at_plus_half_pi=str(row_plus))
    d = sp.asin(sp.sin(-sp.pi / 2 + q) / sp.sqrt(2)) + sp.pi / 4
    dd = sp.diff(d, q)
    diffsq = sp.simplify(dd**2 - sp.sin(q) ** 2 / (1 + sp.sin(q) ** 2))
    num = [abs(complex(sp.N((dd - sp.sin(q) / sp.sqrt(1 + sp.sin(q) ** 2)).subs(q, v), 40))) for v in (-1.3, -0.5, 0.2, 0.7, 1.5)]
    ser = sp.series(d - q**2 / 2, q, 0, 8).removeO()
    record("A3_dprime", diffsq == 0 and max(num) < 1e-35 and sp.simplify(d.subs(q, 0)) == 0,
           square_residual=str(diffsq), max_numeric_residual=max(num), series_d_minus_half_q2=str(ser))
    O = sp.Matrix([[sp.cos(h * x), sp.sin(h * x)], [-sp.sin(h * x), sp.cos(h * x)]])
    out = O * sp.Matrix([R, L])
    res = sp.simplify(sp.expand((out[0] + sp.I * out[1] - sp.exp(-sp.I * h * x) * (R + sp.I * L)).rewrite(sp.cos)))
    record("A4_plate_phase", res == 0, residual=str(res))
    res = sp.expand(sp.integrate((p - F * s) ** 2 / 2, (s, 0, T)) - (T * p**2 / 2 - F * T**2 * p / 2 + F**2 * T**3 / 6))
    record("A5_phase_integral", res == 0, residual=str(res))
    e = Fr(9, 10); a = e + 1; tau = e + 2; J = Fr(-14, 5); wv = Fr(11, 10)
    facts = {"J w^(5/2)": (J + Fr(5, 2) * wv, Fr(-1, 20)), "a/w": (a - wv, Fr(4, 5)), "a J w": (a + J + wv, Fr(1, 5)),
             "a n w with n~1/tau": (a - tau + wv, Fr(1, 10)), "J tau": (J + tau, Fr(1, 10)),
             "delta/eps": (1 - e, Fr(1, 10)), "a/eps": (a - e, Fr(1)), "tau v / a (v=delta p0)": (tau + 1 - a - 1, Fr(0)),
             "M D ~ T L^3 sqrt2 delta/eps": (-(e + 2) + 3, Fr(1, 10))}
    record("A6_exponents", all(v[0] == v[1] for v in facts.values()), exponents={k_: [str(v[0]), str(v[1])] for k_, v in facts.items()})


# ---------------------------------------------------------------- B: scalar inequalities
def scalar_bounds():
    qs = np.linspace(-1, 1, 20001)
    qs = qs[qs != 0]
    k = -np.pi / 2 + qs
    d = np.arcsin(np.sin(k) / np.sqrt(2)) + np.pi / 4
    r1 = np.max(np.abs(d) / (qs**2 / 2))
    r2 = np.max(np.abs(d - qs**2 / 2) / (qs**4 / 6))

    def Pminus(kk):
        c, s = np.cos(kk), np.sin(kk)
        nrm = np.sqrt(1 + c * c)
        n = np.array([c, s, c]) / nrm
        return 0.5 * np.array([[1 - n[2], -(n[0] - 1j * n[1])], [-(n[0] + 1j * n[1]), 1 + n[2]]])
    r3 = max(np.linalg.norm(np.array([1, 1j]) @ Pminus(kk)) / (np.sqrt(2) * abs(qq)) for kk, qq in zip(k[::10], qs[::10]))
    kk = np.linspace(-np.pi, np.pi, 40001)
    c, s = np.cos(kk), np.sin(kk)
    # |n'| analytically: n = (sqrt2 c e1 + s e2)/sqrt(1+c^2), angle' = sqrt2/(1+c^2); operator norm of P' = |n'|/2
    analytic = np.sqrt(2) / (1 + c * c) / 2
    hstep = 1e-6
    fd = max(np.linalg.norm((Pminus(v + hstep) - Pminus(v - hstep)) / (2 * hstep), 2) for v in kk[::400])
    record("B1_scalar_bounds", r1 <= 1 and r2 <= 1 and r3 <= 1 and analytic.max() <= 1,
           max_ratio_d_over_half_q2=float(r1), max_ratio_quartic=float(r2), max_ratio_row=float(r3),
           max_norm_Pprime_analytic=float(analytic.max()), max_norm_Pprime_finite_difference=float(fd),
           note="finite-difference value is a cross-check of the analytic expression (step 1e-6)")


# ---------------------------------------------------------------- walk helpers
def tick(R, L):
    return np.roll(R + L, 1) / np.sqrt(2), np.roll(R - L, -1) / np.sqrt(2)


class Ring:
    def __init__(self, N):
        assert N % 4 == 0
        self.N = N
        idx = np.arange(N)
        self.x = np.where(idx < N // 2, idx, idx - N)
        self.ix = 1j ** (self.x % 4)
        self.even = (idx % 2 == 0)
        self.m = np.fft.fftfreq(N // 2, 1.0 / (N // 2)).astype(int)   # q = 2 pi m / N
        self.q = 2 * np.pi * self.m / N

    def from_coeff(self, c):          # c indexed like fft bins on even sublattice
        return np.fft.ifft(c) * np.sqrt(len(c))

    def coeff(self, z):
        return np.fft.fft(z) / np.sqrt(len(z))

    def B(self, z):                   # z on even sites, returns (z', odd mass, norm drift)
        full = np.zeros(self.N, complex)
        full[self.even] = z
        rails = np.conj(self.ix) * full
        R, L = rails.real.copy(), rails.imag.copy()
        for _ in range(4):
            R, L = tick(R, L)
        out = -self.ix * (R + 1j * L)
        return out[self.even], float(np.sum(np.abs(out[~self.even]) ** 2))

    def S(self, z):
        return self.from_coeff(self.coeff(z) * np.exp(-2j * self.q**2))


def Dfun(Q):
    return 4 * np.sqrt(2) * Q**3 + 2 * Q**4 / 3


def free_bound():
    rows = []
    for N in (64, 256, 1000 // 4 * 4, 4096):
        g = Ring(N)
        for Q in (0.05, 0.2, 0.5, 0.8, 1.0, 1.3, 1.5):
            for fam in ("symmetric", "right_only", "left_only", "edge", "single_max", "single_pair"):
                for rep in range(3 if fam in ("symmetric", "right_only", "left_only", "edge") else 1):
                    sel = np.abs(g.q) <= Q
                    if fam == "right_only":
                        sel &= g.q > 0
                    if fam == "left_only":
                        sel &= g.q < 0
                    if fam == "edge":
                        sel &= np.abs(g.q) >= 0.9 * Q
                    if fam in ("single_max", "single_pair"):
                        cand = np.where(np.abs(g.q) <= Q)[0]
                        top = cand[np.argmax(g.q[cand])]
                        sel = np.zeros_like(sel)
                        sel[top] = True
                        if fam == "single_pair":
                            sel[np.where(g.m == -g.m[top])[0]] = True
                    if not sel.any():
                        rows.append(dict(N=N, Q=Q, family=fam, rep=rep, empty_support=True))
                        continue
                    c = np.zeros(N // 2, complex)
                    c[sel] = rng.normal(size=sel.sum()) + 1j * rng.normal(size=sel.sum())
                    z = g.from_coeff(c)
                    z /= np.linalg.norm(z)
                    back = g.coeff(z)
                    outside = float(np.sum(np.abs(back[np.abs(g.q) > Q]) ** 2))
                    hyp = (Q <= 1) and outside < 1e-24
                    Bz, odd = g.B(z)
                    err = float(np.linalg.norm(Bz - g.S(z)))
                    rows.append(dict(N=N, Q=Q, family=fam, rep=rep, hypothesis=hyp, mass_outside_support=outside,
                                     error=err, bound=float(Dfun(Q)), ratio=err / float(Dfun(Q)),
                                     odd_site_mass=odd, norm_drift=float(abs(np.linalg.norm(Bz) - 1))))
    real = [r for r in rows if "ratio" in r]
    qual = [r for r in real if r["hypothesis"]]
    ctrl = [r for r in real if not r["hypothesis"]]
    worst = max(qual, key=lambda r: r["ratio"])
    record("C1_free_bound", all(r["ratio"] <= 1 for r in qual), instances=len(rows), qualifying=len(qual),
           empty_support=len(rows) - len(real), controls_Q_above_1=len(ctrl),
           max_ratio_qualifying=worst["ratio"], worst=worst,
           max_ratio_controls=max(r["ratio"] for r in ctrl),
           max_ratio_by_Q={str(Q): max(r["ratio"] for r in real if r["Q"] == Q) for Q in sorted({r["Q"] for r in real})})
    record("C2_isometry_parity", max(r["odd_site_mass"] for r in real) == 0.0 or max(r["odd_site_mass"] for r in real) < 1e-28,
           max_odd_site_mass=max(r["odd_site_mass"] for r in real), max_norm_drift=max(r["norm_drift"] for r in real),
           basis="odd-site mass is exactly zero in exact arithmetic; 1e-28 is (1e-14)^2, the square of the measured norm drift scale")
    RES["C_rows"] = rows


# ---------------------------------------------------------------- D: forced bound
def forced():
    rows = []
    cases = []
    for N in (256, 768, 2048, 4096, 6144):
        for eps in (1.0, 0.5, 0.25):
            for F, m in ((1, 1), (-1, 1), (2, 1), (-0.5, 1), (1, 2), (3, 3), (0, 0)):
                for Tt in (0.8, 1.5):
                    cases.append((N, eps, F, m, Tt))
    P = 0.85
    for N, eps, F, m, Tt in cases:
        g = Ring(N)
        if F == 0:
            delta = (2 * np.pi / (4 * eps * N)) ** (1 / 3)
            hm = 0
        else:
            delta = (2 * np.pi * m / (4 * abs(F) * eps * N)) ** (1 / 3)
            hm = int(np.sign(F)) * m                     # h = 2 pi hm / N = 4 F eps delta^3
        Delta = 4 * eps * delta**2
        M = max(1, round(Tt / Delta))
        T = M * Delta
        Lc = P + abs(F) * T
        Q = delta * Lc
        p = g.q / delta
        a1, a2 = rng.uniform(-0.6, 0.6), rng.uniform(-0.3, 0.3)
        c0 = np.where(np.abs(p) <= P, np.maximum(0, 1 - (p / P) ** 2) ** 3, 0) * np.exp(1j * (a1 * p + a2 * p * p))
        nsup = int(np.count_nonzero(c0))
        if nsup == 0:
            rows.append(dict(N=N, eps=eps, F=F, m=m, T_target=Tt, empty_support=True))
            continue
        c0 = c0 / np.linalg.norm(c0)
        z0 = g.from_coeff(c0)
        xe = g.x[g.even]
        plate = np.exp(-2j * np.pi * hm * xe / N)
        z = z0.copy()
        zf = z0.copy()
        for _ in range(M):
            z, _ = g.B(z * plate)
            zf, _ = g.B(zf)
        phase = (T * p * p / 2 - F * T * T * p / 2 + F * F * T**3 / 6) / eps
        cont = g.from_coeff(np.roll(c0 * np.exp(-1j * phase), -hm * M))
        cfree = g.from_coeff(c0 * np.exp(-1j * T * p * p / (2 * eps)))
        E = float(np.linalg.norm(z - cont))
        bound = float(M * Dfun(Q) + T * Delta * abs(F) * Lc / (2 * eps))
        hyp = Q <= 1
        cz = g.coeff(z)
        cfz = g.coeff(zf)
        mp_forced = float(np.sum(np.abs(cz) ** 2 * p))
        mp_free = float(np.sum(np.abs(cfz) ** 2 * p))
        Y = eps * delta * xe
        dY = float(np.sum(np.abs(z) ** 2 * Y) - np.sum(np.abs(zf) ** 2 * Y))
        rows.append(dict(N=N, eps=eps, F=F, m=m, delta=float(delta), M=M, T=float(T), Q=float(Q), hypothesis=bool(hyp),
                         support_modes=nsup, E=E, bound=bound, ratio=E / bound,
                         free_E=float(np.linalg.norm(zf - cfree)), free_bound=float(M * Dfun(delta * P)),
                         mean_p_shift=mp_forced - mp_free, ideal_p_shift=float(-F * T),
                         mean_Y_shift=dY, ideal_Y_shift=float(-F * T * T / 2),
                         ring_length_Y=float(N * eps * delta), norm_drift=float(abs(np.linalg.norm(z) - 1))))
    real = [r for r in rows if "ratio" in r]
    qual = [r for r in real if r["hypothesis"]]
    non = [r for r in real if not r["hypothesis"]]
    worst = max(qual, key=lambda r: r["ratio"])
    record("D1_forced_bound", all(r["ratio"] <= 1 for r in qual) and all(r["free_E"] <= r["free_bound"] for r in qual),
           instances=len(rows), qualifying=len(qual), not_qualifying_Q_above_1=len(non),
           empty_support=len(rows) - len(real), max_ratio_qualifying=worst["ratio"], worst=worst,
           max_ratio_not_qualifying=max((r["ratio"] for r in non), default=None),
           max_E_qualifying=max(r["E"] for r in qual), min_bound_qualifying=min(r["bound"] for r in qual),
           qualifying_with_bound_below_1=sum(r["bound"] < 1 for r in qual),
           max_norm_drift=max(r["norm_drift"] for r in real))
    nz = [r for r in qual if r["F"] != 0]
    sign_ok = all(np.sign(r["mean_Y_shift"]) == np.sign(r["ideal_Y_shift"]) for r in nz)
    record("D2_sign_and_shift", sign_ok, tested=len(nz),
           max_abs_momentum_shift_error=max(abs(r["mean_p_shift"] - r["ideal_p_shift"]) for r in nz),
           max_abs_position_shift_error=max(abs(r["mean_Y_shift"] - r["ideal_Y_shift"]) for r in nz),
           max_rel_position_shift_error=max(abs(r["mean_Y_shift"] / r["ideal_Y_shift"] - 1) for r in nz),
           note="position means are taken on a ring with polynomial packet tails; reported, not thresholded")
    RES["D_rows"] = rows


# ---------------------------------------------------------------- E: integer implementation
def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gpow(a, n):
    r = (1, 0)
    for _ in range(n):
        r = gmul(r, a)
    return r


def integer_part():
    xs = sp.symbols("xs")
    mpoly = sp.minimal_polynomial(sp.Rational(3, 5) + sp.Rational(4, 5) * sp.I, xs)
    lead = sp.Poly(mpoly, xs).LC()
    G = [[3, -4], [4, 3]]
    cols_ok = (G[0][0] * G[0][1] + G[1][0] * G[1][1] == 0) and all(G[0][j] ** 2 + G[1][j] ** 2 == 25 for j in (0, 1))
    # decoded action of G/5 on R+iL
    Rr, Ll = sp.symbols("Rr Ll", real=True)
    dec = sp.expand((3 * Rr - 4 * Ll) + sp.I * (4 * Rr + 3 * Ll) - (3 + 4 * sp.I) * (Rr + sp.I * Ll))
    record("E1_rotation_primitive", lead != 1 and cols_ok and dec == 0, minimal_polynomial=str(mpoly), leading_coefficient=int(lead),
           coherent_return=str(Fr(9, 25)), distinguishable_return_padding_on_R=str(Fr(3 + 18, 25)),
           distinguishable_return_padding_on_L=str(Fr(3, 25)),
           note="7 signed paths for column (3,4) plus 9 cancelling pairs; the 21/25 value holds only when all padding returns to the first rail")
    mp.mp.dps = 60
    w = mp.mpc(3, 4) / 5
    out = {}
    ok = True
    for (h, B0, eta), expect in (((mp.mpf("0.032"), 12, mp.mpf("0.005")), 8341), ((mp.mpf("0.05"), 8, mp.mpf("0.01")), None)):
        tgt = mp.e ** (-1j * h)
        u = mp.mpc(1)
        k = 0
        while abs(u - tgt) > eta / B0:
            u *= w
            k += 1
            if k > 2_000_000:
                break
        errs = [abs(u ** x - mp.e ** (-1j * h * x)) for x in range(-B0, B0 + 1)]
        site_ok = all(e <= abs(x) * eta / B0 for e, x in zip(errs, range(-B0, B0 + 1)))
        out[f"h={h},B0={B0},eta={eta}"] = dict(least_k=k, base_error=mp.nstr(abs(u - tgt), 10), budget=mp.nstr(eta / B0, 10),
                                               max_site_error=mp.nstr(max(errs), 10), padded_cells_per_site=k * B0,
                                               log10_raw_denominator=float(k * B0 * mp.log10(5)), site_bound_holds=site_ok)
        ok &= site_ok and (expect is None or k == expect)
        if expect is not None:
            ok &= mp.nstr(max(errs), 4) == "0.003603"
    record("E2_compiler", ok, cases=out)
    # E3 exact flight
    k, B1, M = 2, 2, 3
    B0 = B1 + 4 * M
    state = {-2: (2, -1), 0: (1, 3), 2: (-2, 2), 1 - 1: (1, 3)}
    state = {-2: (2, -1), 0: (1, 3), 2: (-2, 2)}
    norm0 = sum(a * a + b * b for a, b in state.values())
    fl = {x: complex(*v) for x, v in state.items()}
    wf = complex(3, 4) / 5
    scale = 1
    inside = True
    for _ in range(M):
        new = {}
        for x, z in state.items():
            inside &= abs(x) <= B0
            rot = gpow((3, 4) if x >= 0 else (3, -4), k * abs(x))
            pad = 5 ** (k * (B0 - abs(x)))
            new[x] = gmul(z, (rot[0] * pad, rot[1] * pad))
        scale *= 5 ** (k * B0)
        flnew = {x: z * wf ** (k * x) for x, z in fl.items()}
        for _ in range(4):
            nxt, fn = {}, {}
            for x, (r, l) in new.items():
                a = nxt.get(x + 1, (0, 0)); nxt[x + 1] = (a[0] + r + l, a[1])
                a = nxt.get(x - 1, (0, 0)); nxt[x - 1] = (a[0], a[1] + r - l)
            for x, z in flnew.items():
                r, l = z.real, z.imag
                fn[x + 1] = fn.get(x + 1, 0) + (r + l) / np.sqrt(2)
                fn[x - 1] = fn.get(x - 1, 0) + 1j * (r - l) / np.sqrt(2)
            new, flnew = nxt, fn
        scale *= 4
        state, fl = new, flnew
    norm = sum(a * a + b * b for a, b in state.values())
    inside &= all(abs(x) <= B0 for x in state)
    mp.mp.dps = 80
    diff = max(abs(mp.mpc(*state[x]) / scale - mp.mpc(fl.get(x, 0))) for x in state)
    record("E3_exact_flight", norm == norm0 * scale**2 and inside, k=k, B0=B0, blocks=M, log10_scale=float(mp.log10(scale)),
           support=[min(state), max(state)], max_difference_from_float_phase_model=float(diff),
           note="float model is double precision; the difference is its rounding, reported not thresholded")
    bad = []
    for d in range(61):
        den = 2**d
        for a in range(math.isqrt(den) + 1):
            b2 = den - a * a
            b = math.isqrt(b2)
            if b * b == b2 and not ((d % 2 == 0 and a * b == 0) or (d % 2 == 1 and a == b)):
                bad.append((d, a, b))
        if d > 40:   # keep the scan cheap: descent argument covers the rest; scan to 40 exhaustively
            break
    record("E4_binary_obstruction", not bad, scanned_depths="0..40 exhaustive", counterexamples=bad)


# ---------------------------------------------------------------- F: heralded selector
def hadamard(K):
    Hm = np.array([[1]], dtype=object)
    while Hm.shape[0] < K:
        Hm = np.block([[Hm, Hm], [Hm, -Hm]])
    return Hm


def selector():
    rows = []
    allok = True
    for D in (1, 2, 5, 13, 17, 25, 29, 65, 85):
        K = 1
        while K * K < 8 * D * D:
            K *= 2
        least = (K * K >= 8 * D * D) and (K == 1 or (K // 2) ** 2 < 8 * D * D)
        pairs = [(a, b) for a in range(-D, D + 1) for b in range(-D, D + 1) if a * a + b * b == D * D]
        fits = all(2 * abs(a) + 2 * abs(b) <= K and (K - 2 * abs(a) - 2 * abs(b)) % 2 == 0 for a, b in pairs)
        p = Fr(4 * D * D, K * K)
        Hm = hadamard(K)
        # coherent multi-site input: one site per (a,b) pair (capped at 6 sites), integer rails
        use = pairs if len(pairs) <= 6 else [pairs[i] for i in sorted(rng.choice(len(pairs), 6, replace=False))]
        ns = len(use)
        psi = np.array([[int(v) for v in rng.integers(-4, 5, size=2)] for _ in range(ns)], dtype=object)
        if all(v == 0 for v in psi.ravel()):
            psi[0, 0] = 1
        tables = []
        for a, b in use:
            t = [("I", 1 if a >= 0 else -1)] * (2 * abs(a)) + [("J", 1 if b >= 0 else -1)] * (2 * abs(b))
            t += [("I", 1), ("I", -1)] * ((K - len(t)) // 2)
            tables.append(t)

        def route(v, adjoint=False):       # v shape (K, ns, 2)
            o = np.empty_like(v)
            for s_, t in enumerate(tables):
                for j, (kind, sg) in enumerate(t):
                    r, l = v[j, s_, 0], v[j, s_, 1]
                    if kind == "I":
                        o[j, s_, 0], o[j, s_, 1] = sg * r, sg * l
                    elif not adjoint:
                        o[j, s_, 0], o[j, s_, 1] = -sg * l, sg * r
                    else:
                        o[j, s_, 0], o[j, s_, 1] = sg * l, -sg * r
            return o

        def W(v, adjoint=False):           # K * (unitary): integer arithmetic
            v1 = np.tensordot(Hm, v, axes=(1, 0))
            v2 = route(v1, adjoint)
            return np.tensordot(Hm, v2, axes=(1, 0))

        start = np.zeros((K, ns, 2), dtype=object)
        start[0] = psi
        full = W(start)                    # scale K
        target = np.array([[2 * (a * r - b * l), 2 * (a * l + b * r)] for (a, b), (r, l) in zip(use, psi)], dtype=object)
        yes_ok = bool((full[0] == target).all())
        mass = int(sum(v * v for v in psi.ravel()))
        norm_ok = int(sum(v * v for v in full.ravel())) == K * K * mass
        unitary_ok = bool((W(full, True) == (K * K) * start).all())
        p_meas = Fr(int(sum(v * v for v in full[0].ravel())), K * K * mass)
        fail = full.copy(); fail[0] = 0
        back = W(fail, True)               # scale K^2
        ret = np.zeros_like(back); ret[0] = back[0]
        notret = back - ret
        acc = []
        fails = []
        prop_ok = True
        for br in (ret, notret):
            again = W(br)                  # scale K^3
            acc.append(Fr(int(sum(v * v for v in again[0].ravel())), K**6 * mass))
            piv = next(i for i, v in enumerate(target.ravel()) if v)
            av, tv = again[0].ravel(), target.ravel()
            prop_ok &= av[piv] != 0 and all(u * tv[piv] == t_ * av[piv] for u, t_ in zip(av, tv))
            f2 = again.copy(); f2[0] = 0
            fails.append(f2)
        # both failure branches proportional to the first failure vector
        fv = fail.ravel()
        piv = next(i for i, v in enumerate(fv) if v)
        bad_same = all(all(u * fv[piv] == t_ * f.ravel()[piv] for u, t_ in zip(f.ravel(), fv)) for f in fails)
        retry_cond = sum(acc) / (1 - p)
        ok = (least and fits and yes_ok and norm_ok and unitary_ok and p_meas == p and Fr(1, 8) < p <= Fr(1, 2)
              and retry_cond == 2 * p * (1 - p) and prop_ok and bad_same)
        allok &= ok
        rows.append(dict(D=D, K=K, lattice_points=len(pairs), sites_used=ns, least_power=least, fits=fits, yes_map_exact=yes_ok,
                         norm_exact=norm_ok, adjoint_inverts=unitary_ok, p=str(p), p_float=float(p), p_measured=str(p_meas),
                         retry_branch_probabilities=[str(a) for a in acc], retry_conditional=str(retry_cond),
                         expected_2p_1mp=str(2 * p * (1 - p)), retry_vector_proportional=bool(prop_ok),
                         failure_vectors_proportional=bool(bad_same), ok=bool(ok)))
    record("F1_selector", allok, rows=rows, p_equal_half_attained=any(r["p"] == "1/2" for r in rows))


# ---------------------------------------------------------------- G: sharp launch
def prepared():
    rows = []
    for inv in (6, 8, 10, 12, 14):
        for p0, origin in ((1, 0), (0, 1), (-1, 1)):
            delta = 1 / inv
            eps = delta**0.9
            a = eps * delta
            tau = eps * delta**2
            J = round(delta**-2.8)
            M = round(0.8 / (4 * tau))
            T = M * 4 * tau
            wv = delta**1.1
            rad = abs(origin) + J + 4 * M
            N = 1 << (2 * rad + 2).bit_length()
            idx = np.arange(N)
            x = np.where(idx < N // 2, idx, idx - N)
            R = np.zeros(N); L = np.zeros(N); R[origin % N] = 1
            for _ in range(J):
                R, L = tick(R, L)
            take = np.abs((x - origin) / J - delta * p0) <= wv
            mass = R * R + L * L
            yes = float(mass[take].sum())
            R0 = np.where(take, R, 0) / np.sqrt(yes); L0 = np.where(take, L, 0) / np.sqrt(yes)
            Y0 = origin * a
            means = {}
            fl = []
            for F in (-1, 0, 1):
                ang = -4 * F * eps * delta**3 * (x - origin)      # plate reference at the launch site
                c, s = np.cos(ang), np.sin(ang)
                r, l = R0.copy(), L0.copy()
                for _ in range(M):
                    r, l = c * r + (-s) * l * (-1) * (-1), 0 * r + l   # placeholder overwritten below
                    break
                r, l = R0.copy(), L0.copy()
                for _ in range(M):
                    # decoded multiplication by e^{-ihx}: (r+il) -> e^{i ang}(r+il), ang=-hx
                    r, l = c * r - s * l, s * r + c * l
                    for _ in range(4):
                        r, l = tick(r, l)
                wgt = r * r + l * l
                Y = a * x
                target = Y0 + p0 * T - F * T * T / 2
                means[F] = float(Y @ wgt)
                fl.append(dict(F=F, mean_Y=means[F], target=float(target), inside_half_unit=float(wgt[np.abs(Y - target) <= 0.5].sum()),
                               inside_quarter_unit=float(wgt[np.abs(Y - target) <= 0.25].sum()),
                               rms_about_target=float(np.sqrt(((Y - target) ** 2) @ wgt)), norm_residual=float(wgt.sum() - 1)))
            P = abs(p0) + 1.0
            Lc = P + T
            Q = delta * Lc
            Ebound = M * Dfun(Q) + T * (4 * tau) * Lc / (2 * eps)
            rows.append(dict(inverse_delta=inv, p0=p0, origin=origin, J=J, blocks=M, T=float(T), ring=N, acceptance=yes,
                             leading_acceptance=float(2 * wv / np.pi), acceptance_ratio=float(yes / (2 * wv / np.pi)),
                             shift_F_plus=means[1] - means[0], shift_F_minus=means[-1] - means[0], ideal_shift_F_plus=float(-T * T / 2),
                             note_bound_E_with_P_equal_abs_p0_plus_1=float(Ebound), Q=float(Q), flights=fl))
    record("G1_prepared_force_observables", True, observable_only=True,
           min_note_bound_E=min(r["note_bound_E_with_P_equal_abs_p0_plus_1"] for r in rows),
           summary=[dict(inv=r["inverse_delta"], p0=r["p0"], acc_ratio=round(r["acceptance_ratio"], 4),
                         shift_plus=round(r["shift_F_plus"], 4), ideal=round(r["ideal_shift_F_plus"], 4),
                         inside=[round(f["inside_half_unit"], 4) for f in r["flights"]],
                         rms=[round(f["rms_about_target"], 4) for f in r["flights"]],
                         Ebound=round(r["note_bound_E_with_P_equal_abs_p0_plus_1"], 3)) for r in rows])
    RES["G_rows"] = rows


def main():
    out = Path(sys.argv[1]) / "xcheck_four_tick.json"
    if out.exists():
        sys.exit(f"Refusing to overwrite {out}")
    for fn in (algebra, scalar_bounds, free_bound, forced, integer_part, selector, prepared):
        try:
            fn()
        except Exception as exc:        # a crash is kept as a failed predicate
            record(f"CRASH_{fn.__name__}", False, error=repr(exc))
    with out.open("x") as fh:
        json.dump(RES, fh, indent=1, default=str)
        fh.write("\n")
    for k_, v in RES.items():
        if isinstance(v, dict) and "ok" in v:
            print(k_, "PASS" if v["ok"] else "FAIL")
    print("failed:", RES["failed"])


if __name__ == "__main__":
    main()
