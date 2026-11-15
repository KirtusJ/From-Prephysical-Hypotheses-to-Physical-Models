#!/usr/bin/env python3
"""Challenger attack on Z10, target 2: the limit c*.

Usage: python3 t2_limit.py t1_result_4_9600.json OUT.json

Input: exact gaps and exact position distributions written by t1_exact.py.
(a) Fits of gap(T), T in {300,600,1200,2400,4800,9600}, least squares in
    relative error (each residual divided by the gap):
      M1 a/T ; M2 a*log2(T)/T + b/T ; M3 a/sqrt(T).
    Free-limit fit: Lambda/T = L - a*log2(T)/T - b/T, three parameters, L free.
    Diagnostic B(T) = T*gap(T) - (1/2)*log2(T) (should tend to a constant if
    Lambda(T) = c* T - (1/2) log2 T - b + o(1)).
  Predicates (fixed before the run):
    F1: M2 has max relative residual < 1e-3 and M1, M3 each > 1e-2
        (basis: the three forms differ by a factor log T or sqrt T over a
        32-fold range of T; a wrong form cannot fit to 1e-3).
    F2: |L - c*| < 1e-5 in the free-limit fit (basis: gap(9600)=7.8e-4; a
        limit differing from c* by more than 1e-5 is resolvable; smaller
        differences are tested by F3).
    F3: successive differences of B(T) shrink monotonically in modulus
        (a limit c*+delta would add delta*T to B and make them grow).
(b) Limiting law: candidate density f(v)=1/(pi (1-v^2) sqrt(1-2v^2)) on
    |v|<1/sqrt2.  Three laws compared with the exact distribution of x/T:
      K+ : f(v)(1+v)   K- : f(v)(1-v)   K0 : f(v)
    at ten points v and by first and second moments, T=1200,2400,4800.
  Predicates:
    D1: exactly one of K+,K- has max |CDF diff| over the ten points < 5/T^(1/2)*0.1
        ... replaced before the run by the threshold-free form:
    D1: for one of K+,K- the max |CDF diff| decreases from T=1200 to 4800 and
        is at least 10 times smaller than for the other two laws at T=4800.
    D2: |second moment - (1-1/sqrt2)| decreases with T and is < 1e-5 at 4800.
    D3: the three laws give the same value of E[h((1+v)/2)] to 1e-40 (h even),
        equal to c*.
"""
import sys, json
import mpmath as mp
import numpy as np
INP, OUT = sys.argv[1], sys.argv[2]
fout = open(OUT, 'x')
d = json.load(open(INP))
mp.mp.dps = 50
CS = mp.mpf(d["cstar"]["trap"]["512"])
Ts = [300, 600, 1200, 2400, 4800, 9600]
gap = {T: mp.mpf(d["rows"][str(T)]["gap"]) for T in Ts}
res = {"command": " ".join(sys.argv), "failed": []}
res["gaps"] = {T: mp.nstr(gap[T], 20) for T in Ts}
res["ratios"] = {f"{Ts[i+1]}/{Ts[i]}": mp.nstr(gap[Ts[i + 1]] / gap[Ts[i]], 10) for i in range(len(Ts) - 1)}
def lsq(cols, y, w):
    A = mp.matrix(len(y), len(cols))
    for i in range(len(y)):
        for j, c in enumerate(cols): A[i, j] = c[i] * w[i]
    b = mp.matrix([y[i] * w[i] for i in range(len(y))])
    x = mp.lu_solve(A.T * A, A.T * b)
    r = [abs(sum(cols[j][i] * x[j] for j in range(len(cols))) - y[i]) * w[i] for i in range(len(y))]
    return [x[j] for j in range(len(cols))], max(r)
y = [gap[T] for T in Ts]; w = [1 / g for g in y]
inv = [mp.mpf(1) / T for T in Ts]; lg = [mp.log(T, 2) / T for T in Ts]; sq = [1 / mp.sqrt(T) for T in Ts]
fits = {}
for name, cols in (("M1_a/T", [inv]), ("M2_a*log2T/T+b/T", [lg, inv]), ("M3_a/sqrtT", [sq])):
    x, r = lsq(cols, y, w)
    fits[name] = {"params": [mp.nstr(v, 12) for v in x], "max_rel_residual": mp.nstr(r, 5)}
    fits[name]["_r"] = r
F1 = fits["M2_a*log2T/T+b/T"]["_r"] < mp.mpf("1e-3") and fits["M1_a/T"]["_r"] > mp.mpf("1e-2") and fits["M3_a/sqrtT"]["_r"] > mp.mpf("1e-2")
for v in fits.values(): del v["_r"]
res["fits"] = fits; res["F1"] = bool(F1)
# free limit: Lambda/T = L - a lg - b inv
lam = [CS - g for g in y]
x, r = lsq([[mp.mpf(1)] * len(Ts), [-v for v in lg], [-v for v in inv]], lam, [mp.mpf(1)] * len(Ts))
res["free_limit_fit"] = {"L": mp.nstr(x[0], 15), "a": mp.nstr(x[1], 10), "b": mp.nstr(x[2], 10),
                         "L_minus_cstar": mp.nstr(x[0] - CS, 5), "max_abs_residual": mp.nstr(r, 5)}
F2 = abs(x[0] - CS) < mp.mpf("1e-5"); res["F2"] = bool(F2)
B = [Ts[i] * y[i] - mp.log(Ts[i], 2) / 2 for i in range(len(Ts))]
dB = [B[i + 1] - B[i] for i in range(len(B) - 1)]
res["B(T)=T*gap-0.5*log2T"] = {Ts[i]: mp.nstr(B[i], 12) for i in range(len(Ts))}
res["B_differences"] = [mp.nstr(v, 6) for v in dB]
F3 = all(abs(dB[i + 1]) < abs(dB[i]) for i in range(len(dB) - 1)); res["F3"] = bool(F3)
# bound on delta: a limit c*+delta adds delta*T to B; last difference over dT=4800
res["implied_bound_on_|limit-cstar|"] = mp.nstr(abs(dB[-1]) / 4800, 4) + \
    "  (= |B(9600)-B(4800)|/4800; numerical, assumes the form c*T-(1/2)log2T-b+o(1); not a proof)"
# Richardson of B assuming B = b + c/T
res["B_extrapolated(b + c/T)"] = mp.nstr(2 * B[-1] - B[-2], 10)
# (b) laws
s2 = 1 / mp.sqrt(2)
def f0(v): return 1 / (mp.pi * (1 - v * v) * mp.sqrt(1 - 2 * v * v))
# run 1 failed (TypeError: quad in v returned mpc at the endpoint singularity; kept as
# t2_stdout_run1_FAILED_typeerror.txt). Run 2 integrates in theta, v = sin(theta)/sqrt2,
# where the weight is smooth: f0(v) dv = dtheta/(pi sqrt2 (1-v^2)). Predicates unchanged.
def th(fn):
    def gth(t):
        v = mp.sin(t) * s2
        return fn(v) / (mp.pi * mp.sqrt(2) * (1 - v * v))
    return gth
laws = {"K+": th(lambda v: 1 + v), "K-": th(lambda v: 1 - v), "K0": th(lambda v: mp.mpf(1))}
def vq(fn_v, lawfn, a, b):
    return mp.quad(lambda t: fn_v(mp.sin(t) * s2) * lawfn(t), [a, b])
HP = mp.pi / 2
def hh(v):
    p = (1 + v) / 2
    return -(p * mp.log(p) + (1 - p) * mp.log(1 - p)) / mp.log(2)
vs = [-0.65, -0.6, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.6, 0.65]
lawres = {}
for name, fn in laws.items():
    cdf = {str(v): float(mp.quad(fn, [-HP, mp.asin(mp.mpf(str(v)) / s2)])) for v in vs}
    lawres[name] = {"cdf": cdf, "total": mp.nstr(mp.quad(fn, [-HP, 0, HP]), 20),
                    "mean": mp.nstr(vq(lambda v: v, fn, -HP, HP), 15),
                    "second_moment": mp.nstr(vq(lambda v: v * v, fn, -HP, HP), 15),
                    "E_h_minus_cstar": mp.nstr(vq(hh, fn, -HP, HP) - CS, 5)}
res["laws"] = lawres
res["second_moment_exact_1-1/sqrt2"] = mp.nstr(1 - s2, 15)
cmpd = {}
for T in (1200, 2400, 4800):
    dist = d["rows"][str(T)]["dist"]
    e = {"mean_v": dist["mean_v"], "second_moment_v": dist["second_moment_v"],
         "second_moment_minus_limit": dist["second_moment_v"] - float(1 - s2),
         "mean_minus_(1-1/sqrt2)": dist["mean_v"] - float(1 - s2),
         "max_abs(log2n/T-h)": d["rows"][str(T)]["max_abs(log2n/T - h)"]}
    for name in laws:
        diffs = {str(v): dist["cdf_P(x/T<=v)"][str(v)] - lawres[name]["cdf"][str(v)] for v in vs}
        e[name + "_cdf_diff"] = diffs; e[name + "_max_abs_cdf_diff"] = max(abs(q) for q in diffs.values())
    cmpd[T] = e
res["distribution_vs_laws"] = cmpd
m = {n: [cmpd[T][n + "_max_abs_cdf_diff"] for T in (1200, 2400, 4800)] for n in laws}
D1 = any(m[a][2] < m[a][0] and all(m[a][2] * 10 < m[o][2] for o in laws if o != a) for a in ("K+", "K-"))
sm = [abs(cmpd[T]["second_moment_minus_limit"]) for T in (1200, 2400, 4800)]
D2 = sm[0] > sm[1] > sm[2] and sm[2] < 1e-5
D3 = all(abs(mp.mpf(lawres[n]["E_h_minus_cstar"])) < mp.mpf("1e-40") for n in laws)
res.update({"D1": bool(D1), "D2": bool(D2), "D3": bool(D3)})
for k in ("F1", "F2", "F3", "D1", "D2", "D3"):
    if not res[k]: res["failed"].append(k)
json.dump(res, fout, indent=1, default=str); fout.close()
print(json.dumps({k: res[k] for k in ("gaps", "ratios", "fits", "free_limit_fit", "B(T)=T*gap-0.5*log2T", "B_differences",
      "implied_bound_on_|limit-cstar|", "B_extrapolated(b + c/T)", "failed")}, indent=1, default=str))
for T in cmpd:
    print(T, {k: v for k, v in cmpd[T].items() if not k.endswith("_cdf_diff") or "max" in k})
print({n: {k: v for k, v in lawres[n].items() if k != "cdf"} for n in lawres})
print("K+ cdf", lawres["K+"]["cdf"]); print("K+ diff 2400", cmpd[2400]["K+_cdf_diff"])
