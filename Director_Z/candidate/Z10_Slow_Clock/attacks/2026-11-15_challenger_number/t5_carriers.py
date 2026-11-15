#!/usr/bin/env python3
"""Challenger attack on Z10, target 5 (weak point 5): other carriers.

Usage: python3 t5_carriers.py OUT.json        (seed fixed: 20261115)

A "sign rule" assigns to each (site x, tick t) a tuple (sRR,sLR,sRL,sLL) of
signs: s_PQ is the sign of a step Q taken after a step P (P = rail occupied).
  eR'[x+1] = sRR*eR[x] + sLR*eL[x] ;  eL'[x-1] = sRL*eR[x] + sLL*eL[x]
HYPOTHESIS TESTED PER CARRIER (norm preservation, needed for p = eps^2/2^T to
be a probability, E1): sRR*sLR*sRL*sLL = -1 at every (x,t).  It is tested per
carrier and, in the exact part, sum eps^2 == N0*2^T is checked at every T.
Rules that fail the hypothesis are run only as labelled out-of-hypothesis
probes (p renormalised by sum eps^2) and never counted for a verdict.
Candidate carrier C1 = (+,+,+,-) everywhere, start (0,R).
Counts n(v) do not depend on signs or on the start rail: nR = C(T-1,r-1),
nL = C(T-1,r).  For a two-start combination the ledger still uses the same n
(a constant added to log2 n would shift Lambda and Lambda_c equally).

PART A (exact integers, mpmath logs 200 bits), T = 1..600, named carriers:
  A0 C1 base                         A1 start (0,L), signs of C1
  A2 -1 on R after R (-,+,+,+)       A3 -1 on L after R (+,+,-,+)
  A4 -1 on R after L (+,-,+,+)       A5 start (0,R)+(0,L)   (N0=2)
  A6 start (0,R)-(0,L) (N0=2)        A7 start (0,R)+i(0,L): |eps|^2=eR^2+eL^2 (N0=2)
  A8 probe, all signs + (hypothesis FAILS; renormalised)
 Predicates per carrier:
  QA1: Lambda(T) <= Lambda_c(T) for all T<=600 (list violations, equal lengths)
  QA2: gap(T)=c*-Lambda/T is positive at 150,300,600 and decreasing
  QA3: |gap(600) - gap_C1(600)| < 0.2*gap_C1(600)  (basis: same limit and same
       leading (1/2)log2(T)/T term would leave only an O(1/T) difference)
PART B (float64 search, T=200; float error ~1e-12, margin 1e-6 bits):
  B1 time-periodic rules of period 2 (8^2) and 3 (8^3), uniform in x
  B2 static rules depending on x mod 4 (8^4)
  B3 C1 with one of the 7 other admissible matrices at the origin only
  B4 static random admissible matrix per site, 40 seeds
 Predicate QB: no admissible carrier has Lambda(200) > Lambda_c(200) + 1e-6.
  (If QB FAILS, the best of each family is recomputed exactly at 200,400,600:
   PART C, predicate QC: exact Lambda > exact Lambda_c at all three.)
"""
import sys, json, itertools, random, math
from math import comb
import numpy as np
import mpmath as mp

OUT = sys.argv[1]
fout = open(OUT, 'x')
mp.mp.prec = 200
SC = 160; ONE = 1 << SC; LN2 = mp.log(2)
TM = 600
lf = [0] * (TM + 2); acc = mp.mpf(0)
for k in range(2, TM + 2):
    acc += mp.log(k) / LN2; lf[k] = int(mp.floor(mp.ldexp(acc, SC) + 0.5))
def l2c(m, a): return lf[m] - lf[a] - lf[m - a]
CSTAR = mp.mpf("0.77155330316361197264361236985146426157255923726521")
ADM = [s for s in itertools.product((1, -1), repeat=4) if s[0] * s[1] * s[2] * s[3] == -1]
C1 = (1, 1, 1, -1)
def f(num, T=1): return float(mp.mpf(num) / ONE / T)

def exact(rule, starts, Ts, every=False, N0=1, admissible=True):
    """rule(x,t)->signs ; starts: list of (eR0,eL0) components whose squared
    moduli are added (to represent a complex start). returns dict."""
    comps = [([a], [b]) for a, b in starts]
    out = {"viol": [], "equal": [], "rows": {}, "norm_ok": True}
    for T in range(1, max(Ts) + 1):
        new = []
        for eR, eL in comps:
            L = len(eR); nr = [0] * (L + 1); nl = [0] * (L + 1)
            for r in range(L):
                x = 2 * r - (T - 1)
                s = rule(x, T - 1)
                a = eR[r]; b = eL[r]
                nr[r + 1] = s[0] * a + s[1] * b
                nl[r] = s[2] * a + s[3] * b
            new.append((nr, nl))
        comps = new
        if every or T in Ts:
            m = T - 1; S = 0; Sc = 0; tot = 0
            for r in range(T + 1):
                wR = sum(c[0][r] ** 2 for c in comps); wL = sum(c[1][r] ** 2 for c in comps)
                tot += wR + wL
                if r >= 1:
                    lg = l2c(m, r - 1); S += wR * lg; Sc += comb(m, r - 1) * lg
                if r <= m:
                    lg = l2c(m, r); S += wL * lg; Sc += comb(m, r) * lg
            if tot != N0 << T:
                out["norm_ok"] = False
            # Lambda = S/tot ; Lambda_c = Sc/2^T  -> compare S*2^T vs Sc*tot
            lhs = S << T; rhs = Sc * tot
            d = rhs - lhs
            if abs(d) < (tot << (T + SC - 140)): out["equal"].append(T)
            elif d < 0: out["viol"].append(T)
            if T in Ts:
                lam = S // tot; lamc = Sc >> T
                out["rows"][T] = {"lam_over_T": f(lam, T), "lamc_over_T": f(lamc, T),
                                  "gap": float(CSTAR - mp.mpf(lam) / ONE / T),
                                  "lam_minus_lamc_bits": float(mp.mpf(lam - lamc) / ONE)}
    return out

res = {"command": " ".join(sys.argv), "seed": 20261115, "failed": [], "A": {}, "B": {}, "C": {}}
TS = (150, 300, 600)
named = [
 ("A0_C1_base", lambda x, t: C1, [(1, 0)], 1, True),
 ("A1_start_0L", lambda x, t: C1, [(0, 1)], 1, True),
 ("A2_minus_on_R_after_R", lambda x, t: (-1, 1, 1, 1), [(1, 0)], 1, True),
 ("A3_minus_on_L_after_R", lambda x, t: (1, 1, -1, 1), [(1, 0)], 1, True),
 ("A4_minus_on_R_after_L", lambda x, t: (1, -1, 1, 1), [(1, 0)], 1, True),
 ("A5_start_R_plus_L", lambda x, t: C1, [(1, 1)], 2, True),
 ("A6_start_R_minus_L", lambda x, t: C1, [(1, -1)], 2, True),
 ("A7_start_R_plus_iL", lambda x, t: C1, [(1, 0), (0, 1)], 2, True),
 ("A8_PROBE_all_plus_HYPOTHESIS_FAILS", lambda x, t: (1, 1, 1, 1), [(1, 0)], 1, False),
]
base600 = None
for name, rule, starts, N0, adm in named:
    o = exact(rule, starts, TS, every=True, N0=N0, admissible=adm)
    o["admissible"] = adm
    o["n_viol"] = len(o["viol"]); o["viol"] = o["viol"][:12]
    g = [o["rows"][T]["gap"] for T in TS]
    if name.startswith("A0"): base600 = g[2]
    o["QA1"] = o["n_viol"] == 0
    o["QA2"] = g[0] > g[1] > g[2] > 0
    o["QA3"] = abs(g[2] - base600) < 0.2 * base600
    if adm:
        for q in ("QA1", "QA2", "QA3"):
            if not o[q]: res["failed"].append([q, name])
        if not o["norm_ok"]: res["failed"].append(["norm", name])
    res["A"][name] = o
    print(name, o["rows"][600], "viol", o["n_viol"], "equal", o["equal"], o["QA1"], o["QA2"], o["QA3"], flush=True)

# ---------------- PART B: float search ----------------
T = 200
m = T - 1
lgam = [math.lgamma(k + 1) for k in range(T + 1)]
def ln_c(a): return lgam[m] - lgam[a] - lgam[m - a]
W = 2 * T + 3; off = T + 1
logR = np.zeros(W); logL = np.zeros(W); pcR = np.zeros(W); pcL = np.zeros(W)
for r in range(T + 1):
    x = 2 * r - T
    if r >= 1:
        logR[x + off] = ln_c(r - 1) / math.log(2); pcR[x + off] = math.exp(ln_c(r - 1) - T * math.log(2))
    if r <= m:
        logL[x + off] = ln_c(r) / math.log(2); pcL[x + off] = math.exp(ln_c(r) - T * math.log(2))
LAMC = float((pcR * logR + pcL * logL).sum())
ADMA = np.array(ADM, dtype=float)       # 8 x 4
RT = 1 / math.sqrt(2)
def run_static(Sx):
    """Sx: (ncar, W, 4) signs by site. returns Lambda(T) per carrier."""
    nc = Sx.shape[0]
    eR = np.zeros((nc, W)); eL = np.zeros((nc, W)); eR[:, off] = 1
    for t in range(T):
        nR = np.zeros_like(eR); nL = np.zeros_like(eL)
        nR[:, 1:] = (Sx[:, :-1, 0] * eR[:, :-1] + Sx[:, :-1, 1] * eL[:, :-1]) * RT
        nL[:, :-1] = (Sx[:, 1:, 2] * eR[:, 1:] + Sx[:, 1:, 3] * eL[:, 1:]) * RT
        eR, eL = nR, nL
    return (eR ** 2 * logR + eL ** 2 * logL).sum(axis=1), (eR ** 2 + eL ** 2).sum(axis=1)
def run_time(seq):
    """seq: (ncar, P, 4) signs by tick mod P."""
    nc, P, _ = seq.shape
    eR = np.zeros((nc, W)); eL = np.zeros((nc, W)); eR[:, off] = 1
    for t in range(T):
        s = seq[:, t % P, :]
        nR = np.zeros_like(eR); nL = np.zeros_like(eL)
        nR[:, 1:] = (s[:, 0:1] * eR[:, :-1] + s[:, 1:2] * eL[:, :-1]) * RT
        nL[:, :-1] = (s[:, 2:3] * eR[:, 1:] + s[:, 3:4] * eL[:, 1:]) * RT
        eR, eL = nR, nL
    return (eR ** 2 * logR + eL ** 2 * logL).sum(axis=1), (eR ** 2 + eL ** 2).sum(axis=1)
xs = np.arange(W) - off
best = {}
def record(fam, lam, nrm, descr):
    i = int(np.argmax(lam)); j = int(np.argmin(lam))
    res["B"][fam] = {"n_carriers": int(len(lam)), "all_admissible": True,
                     "max_norm_err": float(np.abs(nrm - 1).max()),
                     "n_above_counting": int((lam > LAMC + 1e-6).sum()),
                     "max_lam": float(lam[i]), "max_lam_minus_lamc": float(lam[i] - LAMC), "argmax": descr(i),
                     "min_lam_over_T": float(lam[j] / T), "argmin": descr(j),
                     "max_lam_over_T": float(lam[i] / T)}
    best[fam] = descr(i)
    print(fam, res["B"][fam], flush=True)
res["B"]["T"] = T; res["B"]["lamc"] = LAMC
for P in (2, 3):
    combos = list(itertools.product(range(8), repeat=P))
    seq = ADMA[np.array(combos)]
    lam, nrm = run_time(seq)
    record(f"B1_time_period_{P}", lam, nrm, lambda i, c=combos: [list(ADM[k]) for k in c[i]])
combos = list(itertools.product(range(8), repeat=4))
idx = np.array(combos)                      # ncar x 4
Sx = ADMA[idx[:, xs % 4]]                   # ncar x W x 4
lam, nrm = run_static(Sx)
record("B2_static_x_mod_4", lam, nrm, lambda i: [list(ADM[k]) for k in combos[i]])
others = [k for k in range(8) if ADM[k] != C1]
Sx = np.tile(np.array(C1, dtype=float), (len(others), W, 1))
for c, k in enumerate(others): Sx[c, off, :] = ADMA[k]
lam, nrm = run_static(Sx)
record("B3_origin_defect", lam, nrm, lambda i: list(ADM[others[i]]))
rng = random.Random(20261115)
seeds = [rng.randrange(10 ** 9) for _ in range(40)]
pat = []
for s in seeds:
    r2 = random.Random(s); pat.append([r2.randrange(8) for _ in range(W)])
Sx = ADMA[np.array(pat)]
lam, nrm = run_static(Sx)
record("B4_random_static", lam, nrm, lambda i: {"seed": seeds[i]})
QB = all(res["B"][k]["n_above_counting"] == 0 for k in res["B"] if k.startswith("B"))
res["QB_no_admissible_carrier_above_counting_at_T200"] = QB
if not QB:
    res["failed"].append(["QB"])
    # ---- PART C exact confirmation of each family's best ----
    def mk(fam, d):
        if fam.startswith("B1"): return lambda x, t: tuple(d[t % len(d)])
        if fam.startswith("B2"): return lambda x, t: tuple(d[x % 4])
        if fam.startswith("B3"): return lambda x, t: tuple(d) if x == 0 else C1
        r2 = random.Random(d["seed"]); p = [r2.randrange(8) for _ in range(W)]
        # outside the stored window (|x|>201) continue the pattern periodically
        return lambda x, t: ADM[p[(x + off) % W]]
    for fam, d in best.items():
        if res["B"][fam]["n_above_counting"] == 0: continue
        o = exact(mk(fam, d), [(1, 0)], (200, 400, 600), every=True)
        o["n_viol"] = len(o["viol"]); o["first_viol"] = o["viol"][:5]; del o["viol"]
        o["QC"] = all(o["rows"][t]["lam_minus_lamc_bits"] > 0 for t in (200, 400, 600))
        o["rule"] = d
        res["C"][fam] = o
        print("C", fam, o["rows"], "n_viol", o["n_viol"], o["first_viol"], "norm", o["norm_ok"], flush=True)
json.dump(res, fout, indent=1); fout.close()
print("failed", res["failed"])
