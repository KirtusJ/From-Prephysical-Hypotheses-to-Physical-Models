"""Cross-review program for Director_G/Flight_window_preparation.md (own code, not the note's checker).

Usage: python3 -B xcheck_window.py OUTPUT_DIRECTORY     (refuses to overwrite its result file)
Seed 20261113 (used only for the random smooth test vectors of predicate P7).

CONVENTIONS
- Line walk, rails R=0, L=1. Raw step A: totals (u, v') at site x go to u+v' on (x+1,R) and u-v' on (x-1,L).
  U = A/sqrt 2. Launch (0,R). Fourier kernel exp(-ikx), measure dk/2pi, X = i d/dk.
- Window W = {x : T(v-w) <= x <= T(v+w)}, both edges INCLUDED; integer sites lo=ceil(T(v-w)), hi=floor(T(v+w)).
- Explicit scaling of the note: eps=delta, a=delta^2, tau=delta^3, v=delta*p0, w=delta^1.1, T=round(delta^-2.8),
  S=round(t_flight/tau). "Velocity deviation" of a terminal site x is (x - v(T+S))/(S*delta) (the note checker's
  convention: displacement measured from the nominal release centre). Tail = accepted mass with |deviation| > 1/2,
  strict inequality.
- Zero amplitude counts as unoccupied; the parity-dark window is a window containing only sites of parity != T mod 2.

PREDICATES, FIXED BEFORE THE FIRST RUN
 E1 (exact) T=3, window {1}: P_yes = 5/8.
 E2 (exact) T=3, window {1}, 4 free ticks: TV(pointer-summed terminal law, untouched law) = 17/64.
 E3 (exact) for T in 1..12, a one-site window on the unoccupied parity inside the cone has P_yes = 0. Hypothesis
    tested per instance: the site has parity != T and |x|<=T. Number qualifying reported.
 E4 (exact) T=6, window {6}: P_yes = 1/64. Extension not in the note: window {T} has P_yes = 2^-T for T=1..12.
 E5 (exact) for 40 (T,n,lo,hi) instances: sum over both pointer sectors and all ports of raw squared totals
    equals 2^(T+n); joint yes probability sums to ||M U^T psi||^2. Hypothesis per instance: the two sectors
    partition the prefix support (checked).
 S1 eigenvalues of U(k) on 4001 grid points equal {exp(-i w), -exp(i w)}, sin w = sin k / sqrt 2;
    tolerance 1e-12 (basis: 2x2 eigensolver, entries O(1), binary64). Measured min |lambda+ - lambda-| reported;
    predicate: it is >= sqrt 2 - 1e-12.
 S2 omega' = cos k / sqrt(1+cos^2 k) (central difference, h=1e-5; tolerance 1e-8 from h^2 error ~1e-10).
 S3 at k = +-pi/2: both band weights ||P_b psi||^2 equal 1/2 (tol 1e-12) and |d nu/dk| = 1 (tol 1e-7);
    hence rho(0) = 4 * (1/2) / (2 pi) = 1/pi.
 S4 sup_t ||B_t psi|| <= sum_b sup_k ||P_b'(k)||  for the sharp launch, t in a list up to 20000; computed as
    ||(X - tV) U^t psi|| on a ring N > 2t+2. The right side is measured on a 2^16 grid. Both numbers reported.
 P1 direct real position-space iteration and the spectral formula give the same P_yes at T=30603 (1/delta=40);
    tolerance 1e-9 (basis: T * sqrt(sites) * 2^-53 ~ 1e-9, crude upper estimate); measured difference reported.
 P2 note value: P_yes(1/delta=40) = 0.0112854 to the printed 6 figures (|diff| < 5e-8), and its ratio to
    2w/pi is 1.0254 (|diff| < 5e-5).
 P3 note values at 1/delta=40, S=64000: accepted mean velocity 0.999114 (|diff| < 5e-7), tail 0.454 (|diff|<5e-4).
 P4 ASYMPTOTIC CLAIM P_yes = (2/pi) w (1+o(1)): no threshold. Measured r(delta) = P_yes/(2w/pi) for
    1/delta in {4,6,8,12,16,20,24,32,40,48,64,96,128} (20,48,64,96,128 not in the note), for p0 in {1,-1,2,0}
    (only p0=1 in the note). Predicate: |r-1| at 1/delta=128 is smaller than at 1/delta=16, for each p0.
    Hypothesis per instance: |v|+w < 1/sqrt 2 (window inside the cone), T w^(5/2) reported.
 P5 FOLLOW-UP MEASURE: r2 = P_yes / (exact spectral mass of V in [v-w, v+w]) (Gauss-Legendre over the four
    preimage arcs). Predicate: |r2-1| < |r-1| for every qualifying instance with p0 != 0 and 1/delta >= 16,
    i.e. the finite excess over 2w/pi is mostly the slope of the density at v != 0, an O(delta) relative term.
 P6 CONCENTRATION: tail(delta) at t_flight=1, p0=1 for 1/delta in {8,12,16,20,24,32,40,48}. Predicate (the
    trend the note's limit requires eventually): tail(1/48) < tail(1/8). Also reported: the ray-optics value
    1 - 0.5/(delta^0.1 + delta^0.3) and the delta needed for that value to reach 0.05.
 P7 second scaling not in the note, w=delta^1.15, T=round(delta^-2.9) (satisfies all four limits and
    T w^(5/2) -> infinity): r reported for the same deltas up to 64; predicate as P4 between 16 and 64.
 P8 outside the hypothesis: w=delta^1.1, T=round(delta^-2.2), so T w^(5/2) -> 0. r reported, no predicate
    (measures whether T w^(5/2) -> infinity is needed for the acceptance formula or only sufficient).
Failed predicates are kept in the result file under "failed".
"""
import json, sys, time
from fractions import Fraction as F
from math import ceil, floor, sqrt, pi
from pathlib import Path
import numpy as np

SEED = 20261113
t0 = time.time()
failed, res = [], {}


def pred(name, ok, **info):
    res[name] = dict(passed=bool(ok), **info)
    if not ok:
        failed.append(name)


# ---------- exact integer walk ----------
def step(st):
    out = {}
    for (x, c), a in st.items():
        out[(x+1, 0)] = out.get((x+1, 0), 0) + a
        out[(x-1, 1)] = out.get((x-1, 1), 0) + (a if c == 0 else -a)
    return {k: v for k, v in out.items() if v != 0}


def run(st, n):
    for _ in range(n):
        st = step(st)
    return st


def branches(T, lo, hi):
    pre = run({(0, 0): 1}, T)
    yes = {k: a for k, a in pre.items() if lo <= k[0] <= hi}
    no = {k: a for k, a in pre.items() if not (lo <= k[0] <= hi)}
    return pre, yes, no


def mass(st):
    return sum(a*a for a in st.values())


pre, yes, no = branches(3, 1, 1)
pred("E1", F(mass(yes), 8) == F(5, 8), value=str(F(mass(yes), 8)))
ty, tn, tb = run(yes, 4), run(no, 4), run(pre, 4)
keys = set(ty) | set(tn) | set(tb)
tv = sum(abs(F(ty.get(k, 0)**2 + tn.get(k, 0)**2 - tb.get(k, 0)**2, 2**7)) for k in keys)/2
pred("E2", tv == F(17, 64), value=str(tv))
q = bad = 0
for T in range(1, 13):
    for x in range(-T, T+1):
        if (x - T) % 2 != 0:
            q += 1
            if mass(branches(T, x, x)[1]) != 0:
                bad += 1
pred("E3", bad == 0, qualifying=q, violations=bad)
edge = {T: str(F(mass(branches(T, T, T)[1]), 2**T)) for T in range(1, 13)}
pred("E4", all(F(edge[T]) == F(1, 2**T) for T in edge), tick6=edge[6], all_T=edge)
rng = np.random.default_rng(SEED)
cnt = bad = 0
for _ in range(40):
    T = int(rng.integers(1, 11)); n = int(rng.integers(0, 9))
    lo = int(rng.integers(-T-1, T+1)); hi = lo + int(rng.integers(0, T+1))
    pre, yes, no = branches(T, lo, hi)
    if set(yes) | set(no) != set(pre) or set(yes) & set(no):
        continue
    cnt += 1
    fy, fn = run(yes, n), run(no, n)
    if mass(fy) + mass(fn) != 2**(T+n) or F(mass(fy), 2**(T+n)) != F(mass(yes), 2**T):
        bad += 1
pred("E5", bad == 0 and cnt > 0, qualifying=cnt, violations=bad)

# ---------- spectral objects ----------
def omega(k):
    return np.arcsin(np.sin(k)/sqrt(2))


def nu(k):
    return np.cos(k)/np.sqrt(1+np.cos(k)**2)


def Umat(k):
    return np.array([[np.exp(-1j*k), np.exp(-1j*k)], [np.exp(1j*k), -np.exp(1j*k)]])/sqrt(2)


def Pplus(k):
    w = omega(k); lp, lm = np.exp(-1j*w), -np.exp(1j*w)
    return (Umat(k) - lm*np.eye(2))/(lp-lm)


ks = np.linspace(-pi, pi, 4001)
err = 0.0; gap = 9.0
for k in ks:
    ev = np.linalg.eigvals(Umat(k)); w = omega(k)
    tgt = np.array([np.exp(-1j*w), -np.exp(1j*w)])
    e = min(np.abs(ev-tgt).max(), np.abs(ev[::-1]-tgt).max())
    err = max(err, e); gap = min(gap, abs(tgt[0]-tgt[1]))
pred("S1", err < 1e-12 and gap >= sqrt(2)-1e-12, max_eigenvalue_error=err, min_gap=gap, sqrt2=sqrt(2))
h = 1e-5
d = np.abs((omega(ks+h)-omega(ks-h))/(2*h) - nu(ks)).max()
pred("S2", d < 1e-8, max_difference=float(d))
info = {}; ok = True
for k in (pi/2, -pi/2):
    P = Pplus(k); wp = float(np.linalg.norm(P[:, 0])**2); wm = float(np.linalg.norm((np.eye(2)-P)[:, 0])**2)
    dn = float(abs((nu(k+h)-nu(k-h))/(2*h)))
    info[str(k)] = dict(weight_plus=wp, weight_minus=wm, abs_dnu=dn, nu=float(nu(k)))
    ok &= abs(wp-.5) < 1e-12 and abs(wm-.5) < 1e-12 and abs(dn-1) < 1e-7
pred("S3", ok, roots=info, rho0=1/pi)


def spectral_state(T, N, src=None):
    """U^T applied to src (2 x N position array, default sharp (0,R)); returns position array."""
    k = 2*pi*np.fft.fftfreq(N)
    if src is None:
        g = np.zeros((2, N), complex); g[0] = 1
    else:
        g = np.fft.fft(src, axis=1)
    w = omega(k); lp, lm = np.exp(-1j*w), -np.exp(1j*w)
    Ug = np.stack(((g[0]+g[1])*np.exp(-1j*k), (g[0]-g[1])*np.exp(1j*k)))/sqrt(2)
    gp = (Ug - lm*g)/(lp-lm); gm = g-gp
    out = np.exp(-1j*T*w)*gp + (1 if T % 2 == 0 else -1)*np.exp(1j*T*w)*gm
    return np.fft.ifft(out, axis=1), k, (gp, gm)


def coords(N):
    x = np.arange(N); return np.where(x < N//2, x, x-N)


# S4: sup ||P_b'|| and ||B_t psi||
kk = np.linspace(-pi, pi, 2**16, endpoint=False); hh = 1e-5
supP = 0.0
for k in kk[::16]:
    D = (Pplus(k+hh)-Pplus(k-hh))/(2*hh)
    supP = max(supP, np.linalg.norm(D, 2))
bound = 2*supP   # P_-' = -P_+'
Bn = {}
for t in (1, 2, 3, 10, 101, 1000, 5001, 20000):
    N = 1 << (2*t+4).bit_length()
    st, k, _ = spectral_state(t, N)
    x = coords(N)
    g = np.fft.fft(st, axis=1)
    w = omega(k); lp, lm = np.exp(-1j*w), -np.exp(1j*w)
    Ug = np.stack(((g[0]+g[1])*np.exp(-1j*k), (g[0]-g[1])*np.exp(1j*k)))/sqrt(2)
    gp = (Ug - lm*g)/(lp-lm); gm = g-gp
    Vg = np.fft.ifft(nu(k)*(gp-gm), axis=1)
    Bn[t] = float(np.linalg.norm(x*st - t*Vg))
pred("S4", max(Bn.values()) <= bound, B_t_psi_norms=Bn, sum_sup_Pprime=bound)


# ---------- window quantities ----------
def window(T, v, w):
    return ceil(T*(v-w)), floor(T*(v+w))


def p_yes_spectral(T, v, w):
    N = 1 << (2*T+4).bit_length()
    st, _, _ = spectral_state(T, N)
    x = coords(N); lo, hi = window(T, v, w)
    m = (x >= lo) & (x <= hi)
    return float((np.abs(st[:, m])**2).sum()), st, m, x, N


def p_yes_direct(T, v, w):
    R = np.zeros(2*T+3); L = np.zeros(2*T+3); R[T+1] = 1.0; s = 1/sqrt(2)
    for _ in range(T):
        Rn = np.zeros_like(R); Ln = np.zeros_like(L)
        Rn[1:] = (R[:-1]+L[:-1])*s
        Ln[:-1] = (R[1:]-L[1:])*s
        R, L = Rn, Ln
    x = np.arange(2*T+3)-(T+1); lo, hi = window(T, v, w)
    m = (x >= lo) & (x <= hi)
    return float((R[m]**2+L[m]**2).sum()), float((R**2+L**2).sum())


GLx, GLw = np.polynomial.legendre.leggauss(64)


def spectral_mass(v1, v2):
    """Mass of the spectral measure of V for the sharp launch in [v1,v2], |v|<1/sqrt2 assumed."""
    tot = 0.0
    def kroot(c):  # nu(k)=c on (0,pi)
        return np.arccos(c/sqrt(1-c*c))
    for band, sgn in (("+", 1), ("-", -1)):
        c1, c2 = sorted((sgn*v1, sgn*v2))      # nu_b = sgn*nu
        a, b = kroot(c2), kroot(c1)             # nu decreasing on (0,pi)
        for A, Bb in ((a, b), (-b, -a)):
            kq = (Bb-A)/2*GLx + (A+Bb)/2
            for kv, wv in zip(kq, GLw):
                P = Pplus(kv)
                if band == "-":
                    P = np.eye(2)-P
                tot += (Bb-A)/2*wv*np.linalg.norm(P[:, 0])**2/(2*pi)
    return float(tot)


def instance(inv, p0, alpha=1.1, beta=2.8):
    dl = 1/inv; v = dl*p0; w = dl**alpha; T = round(dl**-beta)
    qual = abs(v)+w < 1/sqrt(2)
    py, st, m, x, N = p_yes_spectral(T, v, w)
    lo, hi = window(T, v, w)
    out = dict(inverse_delta=inv, p0=p0, alpha=alpha, beta=beta, T=T, w=w, v=v, window=[lo, hi],
               hypothesis_window_inside_cone=bool(qual), T_w_5_2=T*w**2.5, P_yes=py,
               ratio_to_2w_over_pi=py/(2*w/pi))
    if qual:
        sm = spectral_mass(v-w, v+w)
        out.update(spectral_mass_of_V_window=sm, ratio_to_spectral_mass=py/sm)
    return out


# P1, P2
T40 = round(40**2.8); w40 = 40**-1.1
pd, tot = p_yes_direct(T40, 1/40, w40)
ps = p_yes_spectral(T40, 1/40, w40)[0]
pred("P1", abs(pd-ps) < 1e-9, T=T40, direct=pd, spectral=ps, difference=abs(pd-ps), direct_total_norm=tot)
pred("P2", abs(pd-0.0112854) < 5e-8 and abs(pd/(2*w40/pi)-1.0254) < 5e-5, P_yes=pd, ratio=pd/(2*w40/pi), T=T40)

# P4, P5
invs = (4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96, 128)
table = []
for p0 in (1, -1, 2, 0):
    for inv in invs:
        table.append(instance(inv, p0))
res["acceptance_table"] = table
p4 = {}; ok4 = True
for p0 in (1, -1, 2, 0):
    g = {r["inverse_delta"]: r for r in table if r["p0"] == p0}
    a, b = abs(g[16]["ratio_to_2w_over_pi"]-1), abs(g[128]["ratio_to_2w_over_pi"]-1)
    p4[str(p0)] = dict(dev_16=a, dev_128=b, improves=bool(b < a)); ok4 &= b < a
pred("P4", ok4, per_p0=p4, qualifying=sum(r["hypothesis_window_inside_cone"] for r in table), instances=len(table))
sel = [r for r in table if r["hypothesis_window_inside_cone"] and r["p0"] != 0 and r["inverse_delta"] >= 16]
viol = [(r["inverse_delta"], r["p0"]) for r in sel
        if not abs(r["ratio_to_spectral_mass"]-1) < abs(r["ratio_to_2w_over_pi"]-1)]
pred("P5", not viol, qualifying=len(sel), violations=viol)

# P3, P6 release
rel = []
for inv in (8, 12, 16, 20, 24, 32, 40, 48):
    dl = 1/inv; v = dl; w = dl**1.1; T = round(dl**-2.8); S = round(1/dl**3)
    N = 1 << (2*(T+S)+4).bit_length()
    st, _, _ = spectral_state(T, N)
    x = coords(N); lo, hi = window(T, v, w); m = (x >= lo) & (x <= hi)
    py = float((np.abs(st[:, m])**2).sum())
    term, _, _ = spectral_state(S, N, st*m)
    ms = (np.abs(term)**2).sum(axis=0); tt = float(ms.sum())
    dev = (x - v*(T+S))/(S*dl)
    rel.append(dict(inverse_delta=inv, T=T, S=S, N=N, P_yes=py, terminal_mass=tt,
                    mean_velocity=float((ms*(dev+1)).sum()/tt),
                    rms_deviation=float(np.sqrt((ms*dev**2).sum()/tt)),
                    tail_gt_half=float(ms[np.abs(dev) > .5].sum()/tt),
                    tail_gt_one=float(ms[np.abs(dev) > 1.0].sum()/tt),
                    w_over_delta=dl**.1, a_T_w=dl**.3,
                    ray_optics_tail=max(0.0, 1-0.5/(dl**.1+dl**.3))))
res["release_table"] = rel
r40 = [r for r in rel if r["inverse_delta"] == 40][0]
pred("P3", abs(r40["mean_velocity"]-0.999114) < 5e-7 and abs(r40["tail_gt_half"]-0.454) < 5e-4,
     mean_velocity=r40["mean_velocity"], tail=r40["tail_gt_half"])
# delta at which ray-optics tail reaches 0.05: delta^0.1 + delta^0.3 = 0.5/0.95
lo_, hi_ = 1e-40, 1.0
for _ in range(200):
    mid = sqrt(lo_*hi_)
    if mid**.1+mid**.3 > 0.5/0.95: hi_ = mid
    else: lo_ = mid
pred("P6", rel[-1]["tail_gt_half"] < rel[0]["tail_gt_half"],
     tails={r["inverse_delta"]: r["tail_gt_half"] for r in rel},
     delta_for_ray_optics_tail_0p05=lo_, T_at_that_delta=lo_**-2.8)

# P7 second scaling
t7 = [instance(inv, 1, 1.15, 2.9) for inv in (8, 12, 16, 24, 32, 48, 64)]
res["second_scaling_table"] = t7
g = {r["inverse_delta"]: r for r in t7}
pred("P7", abs(g[64]["ratio_to_2w_over_pi"]-1) < abs(g[16]["ratio_to_2w_over_pi"]-1),
     dev_16=abs(g[16]["ratio_to_2w_over_pi"]-1), dev_64=abs(g[64]["ratio_to_2w_over_pi"]-1))
# P8 outside hypothesis
res["outside_hypothesis_table"] = [instance(inv, p0, 1.1, 2.2) for p0 in (1, 0) for inv in (16, 32, 64, 128, 256, 512, 1024)]

res["failed"] = failed
res["seed"] = SEED
res["seconds"] = time.time()-t0
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
with open(out/"xcheck_window.json", "x") as fh:     # 'x': refuses to overwrite
    json.dump(res, fh, indent=1)
print("failed:", failed, "seconds", round(res["seconds"], 1))
