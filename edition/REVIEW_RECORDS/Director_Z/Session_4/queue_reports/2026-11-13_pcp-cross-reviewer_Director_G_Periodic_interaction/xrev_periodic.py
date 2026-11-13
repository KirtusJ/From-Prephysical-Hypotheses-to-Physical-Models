"""Cross-review program for Director_G/Periodic_interaction_and_two_limits.md.

Written from the note's definitions. Not a copy of the note's checker. Three items are
taken from the checker because the note does not state them and the reported numbers
depend on them: (i) the initial data of the two regimes, (ii) the band-section gauge
(first column of the plus-band projector, normalised), (iii) target time 0.75 for the
dynamics and round(0.5/delta^2) ticks for the count-built flights. They are flagged CHK.

CONVENTIONS
  coin index 0 = right (x -> x+1), 1 = left. Hadamard: out0=(in0+in1)/sqrt2, out1=(in0-in1)/sqrt2
  (the minus sign is on left->left). Fourier: psi(x) = sum_k c_k exp(+i k x); a right shift
  multiplies c_k by exp(-ik). One-walker step U(k)=diag(e^{-ik},e^{ik})H, eigenvalue e^{-i omega},
  omega(k)=arcsin(sin k/sqrt2) on the selected band; k*=-pi/2, omega(k*)=-pi/4.
  Sheet character: departure phase exp(-2 pi i g/M) ("selected sector"); the conjugate sector
  is exp(+2 pi i g/M). kappa>0 is attractive: W=kappa(1-cos(Y1-Y2)) has its minimum at coincidence.
  All quantities dimensionless. a=2pi/N=eps*delta, tau=eps*delta^2.
  Rounding: nearest integer, ties to the greater integer, (2a+d)//(2d) with d>0.
  "Zero" for exact integer/rational predicates means ==0. Floating "zero" thresholds are stated
  with their basis next to each predicate.

PREDICATES (fixed before the first run; none is edited afterwards)
 Hypothesis H(N): N>=8 and N%4==0. Instances failing H are computed, labelled, and not counted.
 A. Count construction, exact rationals, N in {8,12,16,20,24,28,32,40} (28,32,40 not in the note's
    checker), depths m in {1, N, N^2, N^2*ceil(log2 N)}; non-qualifying N in {4,6,10,14}.
  A1  R_m(0)==0 and R_m(N/2)==2 exactly (denominator>0 tested first).
  A2  rho(N,m) <= (N-3)(lambda2/lambda1)^m, 60-digit arithmetic, every depth listed.
  A3  at m=N^2 ceil(log2 N): rho <= N^(1-3 pi^2/ln 2).
  A4  log(lambda2/lambda1) <= -3 pi^2/N^2.
  A5  sum_d C_m(d) == 4^m and C_m(d)==C_m(-d).
  A6  theta bound: max_d |2 pi g(d)/M - delta^2 kappa F(d)| <= (3+rho)pi/M + |kappa| delta^2 rho,
      with L=round(M kappa delta^2/2pi), g=round(L R_m); for eps in {1, delta}, M in {101, 40001, N^3+1},
      kappa in {1,-1} plus three seeded draws from U[-3,3]; depths {N, N^2 ceil(log2 N)}. 60 digits.
 B. Dispersion.
  B1  |omega(k*+q)-omega(k*)-q^2/2| <= q^4/6 for 4001 values of q in [-1,1] (50 digits), where
      omega is defined as above; and separately -arg of an eigenvalue of U(k) equals omega(k)
      to 1e-12 (double rounding) for the same q.
  B2  each basis coin has squared overlap 1/2 with each band at k=+-pi/2, to 1e-14.
 C. Two-walker dynamics, own position-space walk, own reference (block diagonalisation of the
    Fourier Hamiltonian by total momentum; no time splitting). N in {32,48,64,96,128} (96,128 not in
    the note), eps=1 ("fixed") and eps=delta=sqrt(2pi/N) ("shrinking"), kappa in {1,-1,0}, M=0 meaning
    the unrounded phase and M=2*ceil(1e5*steps)+1 (CHK) for the reported numbers.
  C1  |norm(U^n psi0)-1| < 1e-12 for every run (basis: n<=500 unitary steps in double precision).
  C2  N=64,kappa=1: distance (fixed) rounds to 0.00697, i.e. |x-0.00697|<=5e-6; (shrinking)
      |x-0.03582|<=5e-6. Basis of tolerance: half a unit of the last printed digit.
  C3  N=64,kappa=1,shrinking: walk statistic <1-cos(Y1-Y2)> within 5e-6 of 0.80963, scalar reference
      within 5e-6 of 0.80733, Newton point value within 5e-6 of 0.69736 (own RK4, r''=-2 kappa sin r).
  C4  the distance decreases strictly along N=32,48,64,96,128 in each regime, kappa=+-1.
      (The note's estimate is O(delta); the measured log-log slope is reported, no threshold.)
  C5  total lattice momentum: the distribution of (l1+l2) mod N is unchanged by the walk to 1e-12
      (basis: exact symmetry, double rounding only).
  C6  conjugate character exp(+2 pi i g/M) with kappa=1 is closer to the kappa=-1 reference than to
      the kappa=+1 reference (sign convention test), N=64 fixed action.
  C7  entanglement minor, fixed action, product of uniform modes, n steps with n*tau nearest 0.1:
      walk coefficients a(0,-1), a(1,0) vanish to 1e-12 (exact symmetry); and
      |minor_walk - minor_scalar| < |minor_scalar| at N in {32,64,128} (this is exactly the condition
      under which norm closeness transfers non-vanishing). Scalar: a00=1-i kappa t+O(t^2),
      a(1,-1)=i kappa t/2+O(t^2): tested by |a(1,-1)-i kappa t/2| <= (kappa t)^2 and
      |a00-(1-i kappa t)| <= (kappa t)^2 at t=0.01 (basis: second-order remainder with |W|<=2|kappa|,
      constant of order one; a failure here would show a wrong leading coefficient).
  C8  count-built gains, N=24, M=40001, eps=1, kappa=1, ticks=round(0.5/delta^2) (CHK): distance from
      the unrounded cosine walk within 5e-6 of 0.48353 at depth 1 and within 5e-7 of 0.000439 at
      depth 2880; and for N in {24,32} (32 not in the note) at the note's depth, kappa=+-1:
      distance <= ticks * measured theta.
 D. Folded preparation and branches.
  D1  N=96: m = even integer nearest delta^(-5/2) with delta=sqrt(2pi/N); (ring mean of sin^(2m) k)^2
      within 5e-8 of 0.0105223.
  D2  integral ratio  int|(sin^m)'|^2 / int sin^(2m) == m^2/(2m-1) exactly (sympy) for m in {2,4,10,30}.
  D3  sympy: with H=sum b_j p_j^2/2 + kappa(1-cos(q1-q2)), r''=-(b1+b2) kappa sin r, and the four
      acceleration vectors at p=0 are pairwise distinct iff kappa sin r0 != 0 (tested at r0=1.8,kappa=1
      and r0=0).
  D4  sympy: [K,Z]f = Z(eps P + eps^2/2) f for K=P^2/2, P=-i eps d/dY, Z=e^{iY}, on f=e^{i n Y}.
"""
import json, sys, os, random
from fractions import Fraction
from math import ceil, log2, pi, sqrt
import numpy as np
import mpmath as mp
import sympy as sy

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "xrev_periodic_result.json")
if os.path.exists(OUT):
    sys.exit("result file exists; refusing to overwrite: " + OUT)
random.seed(20261113)
np.random.seed(20261113)
mp.mp.dps = 60
res = {"predicates": {}, "data": {}, "failed": []}


def record(name, ok, detail=None):
    res["predicates"][name] = {"pass": bool(ok), "detail": detail}
    if not ok:
        res["failed"].append(name)
    print(("PASS " if ok else "FAIL ") + name, detail if detail is not None else "")


def nearest(a, d):
    assert d > 0
    return (2 * a + d) // (2 * d)


# ---------------------------------------------------------------- A
def counts(n, m):
    row = [1] + [0] * (n - 1)
    for _ in range(m):
        row = [row[d - 1] + 2 * row[d] + row[(d + 1) % n] for d in range(n)]
    return row


def shape(n, m):
    c = counts(n, m)
    den = c[0] - c[n // 2]
    return c, den


A = {"qualifying": [], "nonqualifying": []}
kappas = [1.0, -1.0] + [random.uniform(-3, 3) for _ in range(3)]
A["kappas"] = kappas
a1 = a2 = a3 = a4 = a5 = a6 = True
n_a6 = 0
worst_a6 = mp.mpf(0)
for n in (4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 40):
    qual = n >= 8 and n % 4 == 0
    lam1 = 4 * mp.cos(mp.pi / n) ** 2
    lam2 = 4 * mp.cos(2 * mp.pi / n) ** 2
    logratio = mp.log(lam2 / lam1) if lam2 > 0 else mp.mpf("-inf")
    entry = {"N": n, "log_ratio": mp.nstr(logratio, 12), "minus_3pi2_over_N2": mp.nstr(-3 * mp.pi ** 2 / n ** 2, 12),
             "A4": bool(logratio <= -3 * mp.pi ** 2 / n ** 2), "depths": []}
    mfull = n * n * ceil(log2(n))
    for m in (1, n, n * n, mfull):
        c, den = shape(n, m)
        d5 = (sum(c) == 4 ** m) and all(c[d] == c[-d % n] for d in range(n))
        if den <= 0:
            entry["depths"].append({"m": m, "denominator_positive": False})
            if qual:
                a1 = False
            continue
        R = [Fraction(2 * (c[0] - c[d]), den) for d in range(n)]
        e1 = (R[0] == 0 and R[n // 2] == 2)
        F = [1 - mp.cos(2 * mp.pi * d / n) for d in range(n)]
        rho = max(abs(mp.mpf(R[d].numerator) / R[d].denominator - F[d]) for d in range(n))
        bound = (n - 3) * (lam2 / lam1) ** m
        e2 = rho <= bound
        de = {"m": m, "rho": mp.nstr(rho, 8), "bound": mp.nstr(bound, 8), "A1": e1, "A2": bool(e2), "A5": d5}
        if m == mfull:
            pw = mp.mpf(n) ** (1 - 3 * mp.pi ** 2 / mp.log(2))
            de["power_bound"] = mp.nstr(pw, 8)
            de["A3"] = bool(rho <= pw)
            if qual and not de["A3"]:
                a3 = False
        if m in (n, mfull):
            for epsname in ("fixed", "shrinking"):
                aa = 2 * mp.pi / n
                delta = aa if epsname == "fixed" else mp.sqrt(aa)
                for M in (101, 40001, n ** 3 + 1):
                    for k in kappas:
                        kk = mp.mpf(k)
                        target = M * kk * delta ** 2 / (2 * mp.pi)
                        L = int(mp.floor(target + mp.mpf(1) / 2))
                        g = [nearest(L * R[d].numerator, R[d].denominator) for d in range(n)]
                        th = max(abs(2 * mp.pi * g[d] / M - delta ** 2 * kk * F[d]) for d in range(n))
                        bd = (3 + rho) * mp.pi / M + abs(kk) * delta ** 2 * rho
                        ok = th <= bd
                        if qual:
                            n_a6 += 1
                            worst_a6 = max(worst_a6, th / bd)
                            if not ok:
                                a6 = False
                                de.setdefault("A6_fail", []).append([epsname, M, k, mp.nstr(th, 8), mp.nstr(bd, 8)])
        entry["depths"].append(de)
        if qual:
            a1 &= e1
            a2 &= bool(e2)
            a5 &= d5
    if qual:
        a4 &= entry["A4"]
    A["qualifying" if qual else "nonqualifying"].append(entry)
res["data"]["A"] = A
nq = len(A["qualifying"])
record("A1_endpoints", a1, f"{nq} qualifying N")
record("A2_rho_bound", a2, f"{nq} qualifying N x 4 depths")
record("A3_power_bound", a3)
record("A4_log_ratio", a4)
record("A5_count_total_reflection", a5)
record("A6_theta_bound", a6, f"{n_a6} qualifying instances, worst theta/bound={mp.nstr(worst_a6, 6)}")

# ---------------------------------------------------------------- B
H = np.array([[1, 1], [1, -1]]) / sqrt(2)


def Uk(k):
    return np.diag([np.exp(-1j * k), np.exp(1j * k)]) @ H


worst = mp.mpf(0)
b1 = True
eig_dev = 0.0
for i in range(4001):
    q = mp.mpf(-1) + mp.mpf(2) * i / 4000
    om = mp.asin(mp.sin(-mp.pi / 2 + q) / mp.sqrt(2))
    lhs = abs(om + mp.pi / 4 - q * q / 2)
    if q != 0:
        worst = max(worst, lhs / q ** 4)
    if lhs > q ** 4 / 6:
        b1 = False
    ev = np.linalg.eigvals(Uk(-pi / 2 + float(q)))
    eig_dev = max(eig_dev, min(abs(-np.angle(e) - float(om)) for e in ev))
record("B1_edge_estimate", b1 and eig_dev < 1e-12,
       {"sup_ratio_over_q4": mp.nstr(worst, 12), "one_sixth": mp.nstr(mp.mpf(1) / 6, 12), "eig_dev": eig_dev})
b2dev = 0.0
for k in (pi / 2, -pi / 2):
    w, v = np.linalg.eig(Uk(k))
    for j in range(2):
        vec = v[:, j] / np.linalg.norm(v[:, j])
        b2dev = max(b2dev, abs(abs(vec[0]) ** 2 - 0.5), abs(abs(vec[1]) ** 2 - 0.5))
record("B2_equal_split_at_edges", b2dev < 1e-14, b2dev)

# ---------------------------------------------------------------- C
KSTAR = -pi / 2


def modes(n):
    return np.array([(j + n // 2) % n - n // 2 for j in range(n)])


def section(n, gauge=0):
    """Plus-band (eigenvalue e^{-i omega}, omega=arcsin(sin k/sqrt2)) eigenvector at k*+a*l.
    gauge 0: normalised first column of the band projector (CHK). gauge 1: second column."""
    out = np.zeros((n, 2), complex)
    for j, l in enumerate(modes(n)):
        k = KSTAR + 2 * pi * l / n
        w, v = np.linalg.eig(Uk(k))
        om = np.arcsin(np.sin(k) / sqrt(2))
        j0 = int(np.argmin(abs(w - np.exp(-1j * om))))
        vec = v[:, j0] / np.linalg.norm(v[:, j0])
        proj = np.outer(vec, vec.conj())
        col = proj[:, gauge]
        out[j] = col / np.linalg.norm(col)
    return out


def encode(coef, sec):
    return coef[:, :, None, None] * sec[:, None, :, None] * sec[None, :, None, :]


def initial(n, eps, regime, lmax=None):
    """CHK: initial data. Returned on index set modes(n) (or -lmax..lmax as a dict-free dense array)."""
    ell = modes(n) if lmax is None else np.arange(-lmax, lmax + 1)
    if regime == "fixed":
        f1 = (ell == 0) + 0.65 * np.exp(-1.2j) * (ell == 1) + 0.3j * (ell == -2)
        f2 = (ell == 0) + 0.6 * np.exp(0.5j) * (ell == -1)
    elif regime == "uniform":
        f1 = (ell == 0) + 0j
        f2 = (ell == 0) + 0j
    else:
        g = np.exp(-eps * ell ** 2 / 2)
        f1 = g * np.exp(-1j * ell * 1.2)
        f2 = g * np.exp(-1j * ell * (-0.6))
    pair = f1[:, None] * f2[None, :]
    return pair / np.sqrt(np.sum(abs(pair) ** 2))


def walk(n, phase, steps, coef, sec):
    """phase: N x N array of departure phases exp(-i angle(x1,x2)). Returns demodulated Fourier spinor."""
    fs = encode(coef, sec)                      # index [l1,l2,c1,c2] on modes(n)
    x = np.arange(n)
    lm = modes(n)
    # psi(x) = sum_l c_l exp(i (k* + a l) x)/sqrt(n)
    basis = np.exp(1j * np.outer(x, KSTAR + 2 * pi * lm / n)) / sqrt(n)   # [x,l]
    psi = np.einsum("xl,ym,lmcd->xycd", basis, basis, fs)
    for _ in range(steps):
        psi = psi * phase[:, :, None, None]
        # coin on walker 1
        p0 = (psi[:, :, 0, :] + psi[:, :, 1, :]) / sqrt(2)
        p1 = (psi[:, :, 0, :] - psi[:, :, 1, :]) / sqrt(2)
        psi = np.stack((p0, p1), axis=2)
        q0 = (psi[:, :, :, 0] + psi[:, :, :, 1]) / sqrt(2)
        q1 = (psi[:, :, :, 0] - psi[:, :, :, 1]) / sqrt(2)
        psi = np.stack((q0, q1), axis=3)
        new = np.empty_like(psi)
        for c1 in (0, 1):
            for c2 in (0, 1):
                new[:, :, c1, c2] = np.roll(psi[:, :, c1, c2], (1 if c1 == 0 else -1, 1 if c2 == 0 else -1), axis=(0, 1))
        psi = new
    stat = float(np.sum(abs(psi) ** 2 * (1 - np.cos(2 * pi * (x[:, None] - x[None, :]) / n))[:, :, None, None]))
    out = np.einsum("xl,ym,xycd->lmcd", basis.conj(), basis.conj(), psi)
    out = out * np.exp(2j * steps * (-pi / 4))
    return out, stat, float(np.sqrt(np.sum(abs(psi) ** 2)))


def scalar(lmax, eps, kappa, t, f0):
    """Exact evolution of i eps f_t=(K+W)f on Fourier indices -lmax..lmax (per walker), by blocks of
    fixed total index s=l1+l2. H block: diag eps^2(l1^2+l2^2)/2+kappa, off-diagonal -kappa/2 (l1->l1+-1)."""
    out = np.zeros_like(f0)
    for s in range(-2 * lmax, 2 * lmax + 1):
        l1 = np.arange(max(-lmax, s - lmax), min(lmax, s + lmax) + 1)
        l2 = s - l1
        m = len(l1)
        Hb = np.diag(eps ** 2 * (l1 ** 2 + l2 ** 2) / 2.0 + kappa)
        if m > 1:
            Hb = Hb + np.diag(-kappa / 2 * np.ones(m - 1), 1) + np.diag(-kappa / 2 * np.ones(m - 1), -1)
        w, v = np.linalg.eigh(Hb)
        vec = f0[l1 + lmax, l2 + lmax]
        out[l1 + lmax, l2 + lmax] = v @ (np.exp(-1j * t * w / eps) * (v.conj().T @ vec))
    return out


def scalar_stat(f, lmax):
    # <1-cos(Y1-Y2)> = 1 - Re sum conj(f[l1+1,l2-1]) f[l1,l2]
    return float(1 - np.real(np.sum(np.conj(f[1:, :-1]) * f[:-1, 1:])))


def restrict(f, lmax, n):
    lm = modes(n)
    ret = f[np.ix_(lm + lmax, lm + lmax)]
    tail2 = max(0.0, float(np.sum(abs(f) ** 2) - np.sum(abs(ret) ** 2)))
    return ret, sqrt(tail2)


def newton_stat(t, kappa, r0, steps=4000):
    r, v = r0, 0.0
    h = t / steps
    f = lambda r, v: (v, -2 * kappa * np.sin(r))
    for _ in range(steps):
        k1 = f(r, v); k2 = f(r + h * k1[0] / 2, v + h * k1[1] / 2)
        k3 = f(r + h * k2[0] / 2, v + h * k2[1] / 2); k4 = f(r + h * k3[0], v + h * k3[1])
        r += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        v += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
    return float(1 - np.cos(r))


def Fshape(n):
    x = np.arange(n)
    return 1 - np.cos(2 * pi * (x[:, None] - x[None, :]) / n)


C = {"runs": []}
c1 = True
dist = {}
secs = {}
for n in (32, 48, 64, 96, 128):
    secs[n] = section(n)
    for regime in ("fixed", "shrinking"):
        a = 2 * pi / n
        eps = 1.0 if regime == "fixed" else sqrt(a)
        delta = a / eps
        tau = eps * delta ** 2
        steps = round(0.75 / tau)
        t = steps * tau
        lmax = max(n // 2, 64)
        f0 = initial(n, eps, regime, lmax)
        c0 = initial(n, eps, regime)
        M = 2 * ceil(1e5 * steps) + 1
        for kappa in (1.0, -1.0, 0.0):
            ft = scalar(lmax, eps, kappa, t, f0)
            ret, tail = restrict(ft, lmax, n)
            ang = delta ** 2 * kappa * Fshape(n)
            row = {"N": n, "regime": regime, "kappa": kappa, "steps": steps, "t": t, "eps": eps, "delta": delta,
                   "tail": tail, "scalar_stat": scalar_stat(ft, lmax)}
            for label, ph in (("unrounded", np.exp(-1j * ang)),
                              ("integer", np.exp(-2j * pi * np.rint(M * ang / (2 * pi)) / M))):
                out, stat, nrm = walk(n, ph, steps, c0, secs[n])
                d = float(np.hypot(np.sqrt(np.sum(abs(out - encode(ret, secs[n])) ** 2)), tail))
                row[label] = {"distance": d, "walk_stat": stat, "norm_dev": abs(nrm - 1)}
                c1 &= abs(nrm - 1) < 1e-12
                if label == "integer":
                    dist[(n, regime, kappa)] = d
                    if n == 64 and kappa == 1.0:
                        # C5 momentum distribution
                        lm = modes(n)
                        tot = (lm[:, None] + lm[None, :]) % n
                        p_in = np.bincount(tot.ravel(), weights=(abs(c0) ** 2).ravel(), minlength=n)
                        p_out = np.bincount(tot.ravel(), weights=np.sum(abs(out) ** 2, axis=(2, 3)).ravel(), minlength=n)
                        row["momentum_dev"] = float(np.max(abs(p_in - p_out)))
                        if regime == "fixed":
                            # C6 conjugate character and gauge sensitivity
                            outc, _, _ = walk(n, np.conj(ph), steps, c0, secs[n])
                            ftm = scalar(lmax, eps, -1.0, t, f0)
                            retm, tailm = restrict(ftm, lmax, n)
                            row["conj_vs_plus"] = float(np.hypot(np.sqrt(np.sum(abs(outc - encode(ret, secs[n])) ** 2)), tail))
                            row["conj_vs_minus"] = float(np.hypot(np.sqrt(np.sum(abs(outc - encode(retm, secs[n])) ** 2)), tailm))
                            s1 = section(n, 1)
                            o1, _, _ = walk(n, ph, steps, c0, s1)
                            row["distance_other_gauge"] = float(np.hypot(np.sqrt(np.sum(abs(o1 - encode(ret, s1)) ** 2)), tail))
            if regime == "shrinking":
                row["newton_stat"] = newton_stat(t, kappa, 1.8)
            C["runs"].append(row)
            print(n, regime, kappa, steps, {k: (round(v["distance"], 6), round(v["walk_stat"], 6)) for k, v in row.items() if isinstance(v, dict)},
                  round(row["scalar_stat"], 6), row.get("newton_stat"))

record("C1_norm", c1)
get = lambda n, reg, k: [r for r in C["runs"] if r["N"] == n and r["regime"] == reg and r["kappa"] == k][0]
r64f, r64s = get(64, "fixed", 1.0), get(64, "shrinking", 1.0)
record("C2_reported_distances", abs(r64f["integer"]["distance"] - 0.00697) <= 5e-6 and abs(r64s["integer"]["distance"] - 0.03582) <= 5e-6,
       [r64f["integer"]["distance"], r64s["integer"]["distance"]])
record("C3_reported_statistics", abs(r64s["integer"]["walk_stat"] - 0.80963) <= 5e-6 and abs(r64s["scalar_stat"] - 0.80733) <= 5e-6
       and abs(r64s["newton_stat"] - 0.69736) <= 5e-6, [r64s["integer"]["walk_stat"], r64s["scalar_stat"], r64s["newton_stat"]])
c4 = True
slopes = {}
for reg in ("fixed", "shrinking"):
    for k in (1.0, -1.0):
        seq = [dist[(n, reg, k)] for n in (32, 48, 64, 96, 128)]
        c4 &= all(seq[i + 1] < seq[i] for i in range(4))
        slopes[f"{reg},{k}"] = {"distances": seq, "loglog_slope_in_N": float(np.polyfit(np.log([32, 48, 64, 96, 128]), np.log(seq), 1)[0])}
record("C4_monotone_decrease", c4, slopes)
record("C5_total_momentum", r64f["momentum_dev"] < 1e-12 and r64s["momentum_dev"] < 1e-12, [r64f["momentum_dev"], r64s["momentum_dev"]])
record("C6_conjugate_sector_sign", r64f["conj_vs_minus"] < r64f["conj_vs_plus"], [r64f["conj_vs_minus"], r64f["conj_vs_plus"]])
C["gauge_sensitivity_N64_fixed"] = [r64f["integer"]["distance"], r64f["distance_other_gauge"]]

# C7
c7 = True
ent = []
for kappa in (1.0, -1.0):
    lmax = 16
    f0 = initial(8, 1.0, "uniform", lmax)
    ft = scalar(lmax, 1.0, kappa, 0.01, f0)
    a00, a1m = ft[lmax, lmax], ft[lmax + 1, lmax - 1]
    okc = abs(a1m - 1j * kappa * 0.01 / 2) <= (kappa * 0.01) ** 2 and abs(a00 - (1 - 1j * kappa * 0.01)) <= (kappa * 0.01) ** 2
    c7 &= okc
    ent.append({"kappa": kappa, "t": 0.01, "a00": [a00.real, a00.imag], "a1m1": [a1m.real, a1m.imag], "leading_ok": bool(okc)})
    for n in (32, 64, 128):
        a = 2 * pi / n
        tau = a * a
        steps = max(1, round(0.1 / tau))
        t = steps * tau
        lmax = max(n // 2, 32)
        ft = scalar(lmax, 1.0, kappa, t, initial(n, 1.0, "uniform", lmax))
        sec = secs.get(n)
        if sec is None:
            sec = section(n)
        out, _, _ = walk(n, np.exp(-1j * a * a * kappa * Fshape(n)), steps, initial(n, 1.0, "uniform"), sec)
        dec = np.einsum("lmcd,lc,md->lm", out, sec.conj(), sec.conj())   # decoded coefficients on modes(n)
        idx = lambda l: l % n
        w = {"00": dec[idx(0), idx(0)], "0m": dec[idx(0), idx(-1)], "10": dec[idx(1), idx(0)], "1m": dec[idx(1), idx(-1)]}
        s = {"00": ft[lmax, lmax], "0m": ft[lmax, lmax - 1], "10": ft[lmax + 1, lmax], "1m": ft[lmax + 1, lmax - 1]}
        mw = w["00"] * w["1m"] - w["0m"] * w["10"]
        ms = s["00"] * s["1m"] - s["0m"] * s["10"]
        sv = np.linalg.svd(dec, compute_uv=False)
        ok = abs(w["0m"]) < 1e-12 and abs(w["10"]) < 1e-12 and abs(mw - ms) < abs(ms)
        c7 &= ok
        ent.append({"kappa": kappa, "N": n, "t": t, "steps": steps, "minor_walk_abs": abs(mw), "minor_scalar_abs": abs(ms),
                    "minor_diff_abs": abs(mw - ms), "zeros": [abs(w["0m"]), abs(w["10"])],
                    "decoded_singular_values_top3": [float(x) for x in sv[:3]], "ok": bool(ok)})
C["entanglement"] = ent
record("C7_entanglement_minor", c7, ent)

# C8
c8 = True
fl = []
for n, depths in ((24, (1, 2880)), (32, (32 * 32 * 5,))):
    a = 2 * pi / n
    delta = a
    M = 40001
    ticks = max(1, round(0.5 / delta ** 2))
    c0 = initial(n, 1.0, "fixed")
    sec = secs.get(n)
    if sec is None:
        sec = section(n)
    x = np.arange(n)
    rel = (x[:, None] - x[None, :]) % n
    for kappa in (1.0, -1.0):
        ideal, _, _ = walk(n, np.exp(-1j * delta ** 2 * kappa * Fshape(n)), ticks, c0, sec)
        for m in depths:
            c, den = shape(n, m)
            L = round(M * kappa * delta ** 2 / (2 * pi))
            g = np.array([nearest(2 * L * (c[0] - c[d]), den) for d in range(n)], dtype=float)
            ang = 2 * pi * g[rel] / M
            theta = float(np.max(abs(ang - delta ** 2 * kappa * Fshape(n))))
            out, _, nrm = walk(n, np.exp(-1j * ang), ticks, c0, sec)
            d = float(np.sqrt(np.sum(abs(out - ideal) ** 2)))
            ok = d <= ticks * theta + 1e-12
            if n == 24 and kappa == 1.0:
                ok &= abs(d - (0.48353 if m == 1 else 0.000439)) <= (5e-6 if m == 1 else 5e-7)
            c8 &= ok
            fl.append({"N": n, "depth": m, "kappa": kappa, "L": L, "ticks": ticks, "distance": d, "ticks_theta": ticks * theta, "ok": bool(ok)})
C["count_flights"] = fl
record("C8_count_built_flights", c8, fl)
res["data"]["C"] = C

# ---------------------------------------------------------------- D
n = 96
delta = sqrt(2 * pi / n)
target = delta ** (-2.5)
m = 2 * round(target / 2)
k = 2 * pi * np.arange(n) / n
ring = float(np.mean(np.sin(k) ** (2 * m)))
integ = float(sy.binomial(2 * m, m) / sy.Integer(4) ** m)
record("D1_folded_yield", abs(ring ** 2 - 0.0105223) <= 5e-8,
       {"delta^-5/2": target, "m": m, "ring_mean_sq": ring ** 2, "integral_mean_sq": integ ** 2, "1/(pi m)": 1 / (pi * m),
        "rel_diff_ring_vs_integral": abs(ring - integ) / integ, "a_sqrt_m": 2 * pi / n * sqrt(m)})
kk = sy.symbols("k", real=True)
d2 = True
for mm in (2, 4, 10, 30):
    num = sy.integrate(sy.expand((mm * sy.sin(kk) ** (mm - 1) * sy.cos(kk)) ** 2), (kk, 0, 2 * sy.pi))
    den = sy.integrate(sy.sin(kk) ** (2 * mm), (kk, 0, 2 * sy.pi))
    d2 &= sy.simplify(num / den - sy.Rational(mm * mm, 2 * mm - 1)) == 0
record("D2_derivative_ratio", d2)
q1, q2, p1, p2, kap, b1s, b2s = sy.symbols("q1 q2 p1 p2 kappa b1 b2", real=True)
Hs = b1s * p1 ** 2 / 2 + b2s * p2 ** 2 / 2 + kap * (1 - sy.cos(q1 - q2))
qd = [sy.diff(Hs, p1), sy.diff(Hs, p2)]
pd = [-sy.diff(Hs, q1), -sy.diff(Hs, q2)]
acc = [b1s * pd[0], b2s * pd[1]]            # q_j'' = b_j p_j'
rdd = sy.simplify(acc[0] - acc[1] + (b1s + b2s) * kap * sy.sin(q1 - q2))
vecs = lambda r0, kv: {(bb1, bb2): tuple(float(x.subs({b1s: bb1, b2s: bb2, kap: kv, q1: r0, q2: 0})) for x in acc)
                       for bb1 in (1, -1) for bb2 in (1, -1)}
v1, v0 = vecs(1.8, 1), vecs(0.0, 1)
record("D3_branches", rdd == 0 and len(set(v1.values())) == 4 and len(set(v0.values())) == 1,
       {"accelerations_r0=1.8": {str(k_): v for k_, v in v1.items()}, "distinct_at_r0=0": len(set(v0.values()))})
Y, e = sy.symbols("Y epsilon", real=True)
nn = sy.symbols("n", integer=True)
f = sy.exp(sy.I * nn * Y)
P = lambda g: -sy.I * e * sy.diff(g, Y)
Kop = lambda g: P(P(g)) / 2
Z = sy.exp(sy.I * Y)
lhs = Kop(Z * f) - Z * Kop(f)
rhs = Z * (e * P(f) + e ** 2 / 2 * f)
record("D4_commutator_KZ", sy.simplify(lhs - rhs) == 0)

with open(OUT, "x") as fh:
    json.dump(res, fh, indent=1, default=str)
print("FAILED:", res["failed"])
