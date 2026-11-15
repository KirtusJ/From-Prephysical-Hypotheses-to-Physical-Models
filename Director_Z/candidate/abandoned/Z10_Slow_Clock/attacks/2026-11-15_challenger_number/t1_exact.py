#!/usr/bin/env python3
"""Challenger attack on candidate Z10 "Slow Clock": targets 1, 3, 4 and data for 2.

Usage: python3 t1_exact.py TFULL TMAX OUT.json
  TFULL: every T in 1..TFULL is evaluated (Lambda, Lambda_c, E1..E4, E6).
  TMAX : propagation continues to TMAX; Lambda, Lambda_c only at T = 300*2^k.

Carrier (C1): vertices (x,R),(x,L); start (0,R) at T=0; right step from either
rail of x -> (x+1,R), sign +1; left step -> (x-1,L), sign -1 iff the previous
step was a left step (the walker is on rail L), else +1.  Index r = number of
right steps, x = 2r - T.
  eR'[r+1] = eR[r] + eL[r] ;  eL'[r] = eR[r] - eL[r]
  nR'[r+1] = nR[r] + nL[r] ;  nL'[r] = nR[r] + nL[r]
Lambda(T)   = sum_{v: eps(v)!=0} eps(v)^2/2^T * log2 n(v)
Lambda_c(T) = sum_v n(v)/2^T * log2 n(v)
gap(T) = c* - Lambda(T)/T.

Arithmetic: eps and n are exact Python integers.  For T <= TFULL the integer
counts n are propagated and checked EXACTLY against nR[r]=C(T-1,r-1),
nL[r]=C(T-1,r); log2 n is then taken as lf[T-1]-lf[a]-lf[T-1-a] with
lf[k]=log2(k!) accumulated from mpmath logs at 400 bits and held as fixed-point
integers scaled 2^360 (error per lf entry < k*2^-395; per log2 n < 2^-380 for
k<10^4; the weighted sums have nonnegative weights of total 1, so the error of
Lambda is < 2^-380 ~ 4e-115).  Cross-check: at T in {300,600,1200,2400} log2 of
the propagated integer n is computed directly by mpmath (400 bits) and Lambda
recomputed; predicate PX: the two agree to < 1e-100.

c*: (1/(pi sqrt2)) * int_{-pi/2}^{pi/2} h((1+sin t/sqrt2)/2)/(1-sin^2 t/2) dt.
Rule A: my own midpoint/trapezoid rule on the half-period (integrand is an
analytic function of sin t, so the rule on a half period symmetric about the
turning points converges geometrically) at N and 2N panels, N=64..512.
Rule B: mpmath tanh-sinh quad; Rule C: mpmath Gauss-Legendre quad.  All at 60
digits.  Error estimate = max pairwise difference of A(256),A(512),B,C.
This is agreement of rules, not a certified enclosure.

PREDICATES (fixed before the first run):
 P0 control: T=3 table; Lambda(3), Lambda_c(3).
 P1 (R7): 0.0020 < gap(2400) < 0.0035 strictly.  Failure = KILL.
 P1b: Lambda(T)/T < c* for every 1 <= T <= TFULL (and the selected larger T).
 P1c: gaps at 300,600,1200 reproduce 0.016472, 0.009068, 0.004950 to 6 places.
 P3 (E6): Lambda(T) <= Lambda_c(T) for all T <= TFULL; equality iff T <= 4.
      Comparison on exact fixed-point numerators; "equal" means |diff| < 2^-300.
 P4a (E1): sum eps^2 == 2^T exactly, all T <= TMAX.
 P4b (E2): Lambda(T+1) >= Lambda(T), Lambda_c(T+1) >= Lambda_c(T), T < TFULL.
 P4c (E3): Lambda(T) <= T-1 and Lambda_c(T) <= T-1, 1 <= T <= TFULL;
           and max n(v) <= 2^(T-1).
 P4d (E4): Lambda(1)=Lambda(2)=0 exactly; Lambda(T) > Lambda(T-1), 3<=T<=TFULL.
 PB: counts equal the binomials, every T <= TFULL (hypothesis of the log table).
 PX: direct-log cross-check as above.
Every failure is kept in the output under "failed".
"""
import sys, json, time
from math import comb
import mpmath as mp

TFULL, TMAX, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
fout = open(OUT, 'x')
t0 = time.time()
mp.mp.prec = 400
SC = 360
ONE = 1 << SC
LN2 = mp.log(2)

def fp(x):  # mpf -> fixed int
    return int(mp.floor(mp.ldexp(x, SC) + mp.mpf(1) / 2))

lf = [0] * (TMAX + 2)
acc = mp.mpf(0)
for k in range(2, TMAX + 2):
    acc += mp.log(k) / LN2
    lf[k] = fp(acc)

def l2c(m, a):
    return lf[m] - lf[a] - lf[m - a]

def tostr(num, T, digits=60):
    """fixed numerator num (scaled 2^SC) -> decimal string of num/2^SC/T"""
    mp.mp.dps = 110
    v = mp.mpf(num) / mp.mpf(ONE) / T
    s = mp.nstr(v, digits)
    mp.mp.prec = 400
    return s

# ---- c* ----
mp.mp.dps = 60
def h(p):
    return -(p * mp.log(p) + (1 - p) * mp.log(1 - p)) / mp.log(2)
def g(t):
    s = mp.sin(t)
    return h((1 + s / mp.sqrt(2)) / 2) / (1 - s * s / 2)
def trap(N):
    a = -mp.pi / 2; w = mp.pi / N
    tot = (g(a) + g(-a)) / 2
    for i in range(1, N):
        tot += g(a + i * w)
    return tot * w / (mp.pi * mp.sqrt(2))
cA = {N: trap(N) for N in (64, 128, 256, 512)}
cB = mp.quad(g, [-mp.pi / 2, 0, mp.pi / 2]) / (mp.pi * mp.sqrt(2))
cC = mp.quadgl(g, [-mp.pi / 2, 0, mp.pi / 2]) / (mp.pi * mp.sqrt(2))
vals = [cA[256], cA[512], cB, cC]
cerr = max(abs(a - b) for a in vals for b in vals)
CSTAR = cA[512]
# density normalisation check (weight 1/(pi sqrt2 (1-sin^2/2)))
def wgt(t):
    s = mp.sin(t); return 1 / (1 - s * s / 2)
norm = mp.quad(wgt, [-mp.pi / 2, 0, mp.pi / 2]) / (mp.pi * mp.sqrt(2))
res = {"command": " ".join(sys.argv), "TFULL": TFULL, "TMAX": TMAX,
       "cstar": {"trap": {str(N): mp.nstr(v, 50) for N, v in cA.items()},
                 "tanh_sinh": mp.nstr(cB, 50), "gauss_legendre": mp.nstr(cC, 50),
                 "max_pairwise_diff": mp.nstr(cerr, 5),
                 "weight_integral_minus_1": mp.nstr(norm - 1, 5)},
       "failed": []}
mp.mp.prec = 400
CS_FP = fp(CSTAR)

sel = set()
k = 300
while k <= TMAX:
    sel.add(k); k *= 2
direct_T = {300, 600, 1200, 2400}
dist_T = {1200, 2400, 4800}
CDFV = [-0.65, -0.6, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.6, 0.65]

eR = [1]; eL = [0]; nR = [1]; nL = [0]
lam = {}; lamc = {}
prevS = prevSc = None
rows = {}
control = None
eq_T = []; viol_E6 = []; pb_ok = True
min_gap_fp = None; viol_c = []
min_d = None
for T in range(1, TMAX + 1):
    L = len(eR)
    nr = [0] * (L + 1); nl = [0] * (L + 1)
    for r in range(L):
        a = eR[r]; b = eL[r]
        nr[r + 1] = a + b; nl[r] = a - b
    eR, eL = nr, nl
    full = T <= TFULL
    if full:
        cr = [0] * (L + 1); cl = [0] * (L + 1)
        for r in range(L):
            s = nR[r] + nL[r]
            cr[r + 1] = s; cl[r] = s
        nR, nL = cr, cl
        # PB
        for r in range(T + 1):
            if nR[r] != (comb(T - 1, r - 1) if r >= 1 else 0) or nL[r] != (comb(T - 1, r) if r <= T - 1 else 0):
                pb_ok = False; res["failed"].append(["PB", T, r])
        if max(max(nR), max(nL)) > (1 << (T - 1)):
            res["failed"].append(["P4c_n", T])
    if T == 3:
        control = [{"x": 2 * r - 3, "rail": rail, "eps": e[r], "n": n[r]}
                   for r in range(4) for rail, e, n in (("R", eR, nR), ("L", eL, nL)) if n[r] > 0]
    if full or T in sel:
        # P4a
        tot = sum(a * a for a in eR) + sum(b * b for b in eL)
        if tot != (1 << T):
            res["failed"].append(["P4a", T])
        S = 0; Sc = 0
        m = T - 1
        for r in range(T + 1):
            if r >= 1:
                lg = l2c(m, r - 1)
                a = eR[r]
                if a: S += a * a * lg
                Sc += comb(m, r - 1) * lg if not full else nR[r] * lg
            if r <= m:
                lg = l2c(m, r)
                b = eL[r]
                if b: S += b * b * lg
                Sc += comb(m, r) * lg if not full else nL[r] * lg
        # S, Sc are numerators over 2^T, scaled 2^SC
        lamT = S >> T; lamcT = Sc >> T   # fixed-point floor
        if full:
            d = Sc - S
            tol = 1 << (T + SC - 300)
            if abs(d) < tol:
                eq_T.append(T)
            elif d < 0:
                viol_E6.append(T); res["failed"].append(["P3", T])
            else:
                dd = mp.mpf(d) / mp.mpf(1 << T) / ONE
                if T > 4 and (min_d is None or dd < min_d[1]):
                    min_d = (T, dd)
            if prevS is not None:
                if 2 * prevS > S: res["failed"].append(["P4b_lam", T])
                if 2 * prevSc > Sc: res["failed"].append(["P4b_lamc", T])
                if T >= 3 and not (S > 2 * prevS): res["failed"].append(["P4d_strict", T])
            if T in (1, 2) and S != 0: res["failed"].append(["P4d_zero", T])
            if lamT > (T - 1) * ONE or lamcT > (T - 1) * ONE: res["failed"].append(["P4c", T])
            prevS, prevSc = S, Sc
        gfp = CS_FP * T - lamT       # = T*gap scaled
        if gfp <= 0:
            viol_c.append(T); res["failed"].append(["P1b", T])
        if T in sel or T in (1, 2, 3, 4, 5, 6, 10, 50, 100) or T % 100 == 0:
            rows[T] = {"lam_over_T": tostr(lamT, T), "lamc_over_T": tostr(lamcT, T),
                       "gap": tostr(gfp, T), "lam": tostr(lamT, 1), "lamc": tostr(lamcT, 1)}
        if T in direct_T and full:
            Sd = mp.mpf(0)
            for r in range(T + 1):
                if eR[r]: Sd += eR[r] ** 2 * (mp.log(nR[r]) / LN2)
                if eL[r]: Sd += eL[r] ** 2 * (mp.log(nL[r]) / LN2)
            diff = abs(mp.ldexp(Sd, -T) - mp.mpf(S) / mp.mpf(1 << T) / ONE)
            rows[T]["direct_log_diff"] = mp.nstr(diff, 5)
            if diff > mp.mpf(10) ** -100: res["failed"].append(["PX", T])
        if T in dist_T:
            tw = 1 << T
            cum = 0; cdf = {}; vi = 0; m1 = 0; m2 = 0; pR = 0
            for r in range(T + 1):
                x = 2 * r - T
                while vi < len(CDFV) and x > CDFV[vi] * T:
                    cdf[str(CDFV[vi])] = float(mp.mpf(cum) / tw); vi += 1
                w = eR[r] ** 2 + eL[r] ** 2
                cum += w; m1 += w * x; m2 += w * x * x; pR += eR[r] ** 2
            while vi < len(CDFV):
                cdf[str(CDFV[vi])] = float(mp.mpf(cum) / tw); vi += 1
            rows[T]["dist"] = {"cdf_P(x/T<=v)": cdf, "mean_v": float(mp.mpf(m1) / tw / T),
                               "second_moment_v": float(mp.mpf(m2) / tw / T / T),
                               "P_rail_R": float(mp.mpf(pR) / tw)}
            # uniformity of log2 n / T against h((1+v)/2): max abs deviation over v
            mx = mp.mpf(0)
            mp.mp.dps = 30
            for r in range(1, T):
                p = mp.mpf(r) / T
                hh = -(p * mp.log(p) + (1 - p) * mp.log(1 - p)) / LN2
                for lg in (l2c(T - 1, r - 1), l2c(T - 1, r)):
                    dv = abs(mp.mpf(lg) / ONE / T - hh)
                    if dv > mx: mx = dv
            rows[T]["max_abs(log2n/T - h)"] = mp.nstr(mx, 6)
            mp.mp.prec = 400
    if T % 400 == 0:
        print(T, round(time.time() - t0, 1), flush=True)

g2400 = mp.mpf(rows[2400]["gap"]) if 2400 in rows else None
P1 = (g2400 is not None) and (mp.mpf("0.0020") < g2400 < mp.mpf("0.0035"))
if not P1: res["failed"].append(["P1_R7", str(g2400)])
for T, ref in ((300, "0.016472"), (600, "0.009068"), (1200, "0.004950")):
    if T in rows and abs(mp.mpf(rows[T]["gap"]) - mp.mpf(ref)) > mp.mpf("6e-7"):
        res["failed"].append(["P1c", T, rows[T]["gap"]])
res.update({"control_T3": control, "rows": rows,
            "P1_R7_gap2400_in_(0.0020,0.0035)": bool(P1),
            "P1b_violations": viol_c, "P3_equal_T": eq_T, "P3_violations": viol_E6,
            "P3_min_positive_diff_T>4": [min_d[0], mp.nstr(min_d[1], 20)] if min_d else None,
            "PB_counts_are_binomials": pb_ok,
            "seconds": round(time.time() - t0, 1)})
json.dump(res, fout, indent=1)
fout.close()
print("failed:", res["failed"][:20], len(res["failed"]))
print("gap2400", rows.get(2400, {}).get("gap"))
