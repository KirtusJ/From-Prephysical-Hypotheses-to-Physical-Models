"""Wildcard attack "dial" on candidate Z10 "Slow Clock" (STIPULATED CANDIDATE FOR DISPROOF; nothing here is a claim
about the world). Own program: exact integer propagation of eps and n on the signed two-rail line from (0,R), T <= 1200
only (R7, T = 2400, is NOT computed here). Logs in 60-digit decimals; comparisons of ages use the margin 1e-40 (basis:
60 working digits, sums of < 2500 terms of size < 1200, so rounding error < 1e-50). Seed: none (no randomness).
PREDICATES, fixed before the first run (15 November 2026). Expected value is what the candidate's text asserts; a False
is a finding against the text and is kept.
 D1 (control) At T = 3 the records of non-zero chance are exactly (1,R) chance 1/2 with 2 histories and (3,R), (1,L),
    (-1,R), (-3,L) chance 1/8 with 1 history each; (-1,L) has 2 histories and chance 0; Lambda(3) = 1/2 exactly.
 D2 (C5, dial) Lambda(0) = Lambda(1) = Lambda(2) = 0: the map T -> age is not injective, so the age cannot tell 0, 1
    and 2 ticks apart, while the supports of the chances at T = 0, 1, 2 are pairwise different (records do tell them apart).
 D3 (C5, dial) No record tells the age: for T = 100 and T' = 102 there is a record v with non-zero chance at both
    lengths (so one observed record is compatible with two different ages).
 D4 (E2, counting) Lambda_c(T+1) >= Lambda_c(T) for T = 1..1199 and Lambda(T+1) >= Lambda(T) for T = 1..1199.
 D5 (E3) max_v n(v) = C(T-1, floor((T-1)/2)) <= 2^(T-1) for T = 1..1200.
 D6 (OVERVIEW "favour records far from the middle, which have fewer histories behind them") At T = 100: the record of
    largest interfering chance has |x| >= 50 and fewer histories than the record of largest count; and the interfering
    chance of |x| >= 50 exceeds the counting chance of |x| >= 50.
 D7 (OVERVIEW "There the age grows by very nearly one bit per tick") the counting increment Lambda_c(T+1)-Lambda_c(T)
    is >= 0.99 for every T from 1 to 1199. (Expected to FAIL at small T; the first T from which it holds is reported.)
 D8 (BRAND one line "ages at a fixed fraction of a tick per tick in the long run") the interfering increments
    Lambda(T+1)-Lambda(T) for T = 1000..1199 all lie within 0.01 of c*. Reported: min and max over that range.
 D9 (BRAND "c* = 0.7715533031636 to thirteen places") c* recomputed by another method (the integrand is an analytic
    2pi-periodic function of theta, symmetric about pi/2, so the periodic trapezoid rule converges geometrically;
    50-digit decimals with own sine series, N = 200 and N = 400 points per period) agrees with itself to 1e-40 and
    rounds to 0.7715533031636 at 13 places.
 D10 (SPEC "two programs written separately give the same rates at T = 300, 600") the rates in
    function/result_instances_run1.json and ../SPRINT_2026-11-15/result_kill_z10_run1.json agree on their common digits
    at 300 and 600 AND the two programs share fewer than 5 byte-identical code lines of 40+ characters.
 D11 (plot) every interval of function/plot_age_rate.json contains the value of this program at that T, for all 3 series.
 D12 (E6/E5) Lambda <= Lambda_c for T = 1..1200 with equality exactly at T <= 4; Lambda/T < c* for T = 1..1200; my rates
    at 300, 600, 1200 round to 0.755081, 0.762485, 0.766603.
Usage: python3 dial_attack.py RESULT.json (refuses to overwrite)."""
import sys, os, json, math
from fractions import Fraction as F
from decimal import Decimal as D, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
HERE = os.path.dirname(os.path.abspath(__file__)); Z = os.path.dirname(os.path.dirname(HERE))
LN2 = D(2).ln(); E = D(10) ** -40
def lg(n): return D(n).ln() / LN2
# --- c* by periodic trapezoid, decimals
def dsin(x):
    t = x; s = x; k = 1
    while abs(t) > D(10) ** -58:
        t = -t * x * x / ((2 * k) * (2 * k + 1)); s += t; k += 1
    return s
PI = D("3.14159265358979323846264338327950288419716939937510582097494")
def hD(x): return -(x * x.ln() + (1 - x) * (1 - x).ln()) / LN2
def gD(t):
    s = dsin(t); return hD((1 + s / D(2).sqrt()) / 2) / (1 - s * s / 2)
def cstar(N):  # full period [-pi/2, 3pi/2), then halve
    return sum(gD(-PI / 2 + 2 * PI * D(j) / N) for j in range(N)) * (2 * PI / N) / 2 / (PI * D(2).sqrt())
c200, c400 = cstar(200), cstar(400); C = c400
# --- walk
st = {(0, 0): (1, 1)}; lam = {0: D(0)}; lamc = {0: D(0)}; supp = {0: {(0, 0)}}; keep = {}; maxn_ok = True
for T in range(1, 1201):
    new = {}
    for (x, r), (sg, n) in st.items():
        a, b = new.get((x + 1, 0), (0, 0)); new[(x + 1, 0)] = (a + sg, b + n)
        a, b = new.get((x - 1, 1), (0, 0)); new[(x - 1, 1)] = (a + (-sg if r == 1 else sg), b + n)
    st = new
    assert sum(s * s for s, n in st.values()) == 2 ** T and sum(n for s, n in st.values()) == 2 ** T
    lam[T] = sum(D(s * s) * lg(n) for s, n in st.values() if s) / D(2) ** T
    lamc[T] = sum(D(n) * lg(n) for s, n in st.values()) / D(2) ** T
    mx = max(n for s, n in st.values()); maxn_ok &= (mx == math.comb(T - 1, (T - 1) // 2) and mx <= 2 ** (T - 1))
    if T <= 3 or T in (100, 102): keep[T] = dict(st)
    if T <= 2: supp[T] = {v for v, (s, n) in st.items() if s}
P = {}; R = {}
t3 = {f"({x},{'RL'[r]})": [str(F(s * s, 8)), n] for (x, r), (s, n) in sorted(keep[3].items())}
R["T3_records_chance_histories"] = t3
P["D1"] = t3 == {"(-3,L)": ["1/8", 1], "(-1,R)": ["1/8", 1], "(-1,L)": ["0", 2], "(1,R)": ["1/2", 2], "(1,L)": ["1/8", 1], "(3,R)": ["1/8", 1]} \
    and sum(F(s * s, 8) * (0 if n == 1 else 1) for s, n in keep[3].values()) == F(1, 2) and all(n in (1, 2) for s, n in keep[3].values())
P["D2"] = lam[0] == 0 and lam[1] == 0 and lam[2] == 0 and supp[0] != supp[1] != supp[2] != supp[0]
common = [v for v, (s, n) in keep[100].items() if s and keep[102].get(v, (0, 0))[0]]
P["D3"] = len(common) > 0 and abs(lam[100] - lam[102]) > E
R["D3_common_records_100_102"] = len(common); R["ages_100_102"] = [str(lam[100])[:14], str(lam[102])[:14]]
v0 = common[len(common) // 2]; R["D3_example"] = [list(v0), "ledger entry at 100", str(lg(keep[100][v0][1]))[:10], "at 102", str(lg(keep[102][v0][1]))[:10]]
P["D4"] = all(lamc[T + 1] >= lamc[T] - E for T in range(1, 1200)) and all(lam[T + 1] >= lam[T] - E for T in range(1, 1200))
P["D5"] = maxn_ok
s100 = keep[100]; W = 2 ** 100
vq = max(s100, key=lambda v: s100[v][0] ** 2); vc = max(s100, key=lambda v: s100[v][1])
far_q = F(sum(s * s for (x, r), (s, n) in s100.items() if abs(x) >= 50), W); far_c = F(sum(n for (x, r), (s, n) in s100.items() if abs(x) >= 50), W)
R["T100"] = {"record_of_largest_interfering_chance": [list(vq), float(F(s100[vq][0] ** 2, W)), "log2 n", float(lg(s100[vq][1]))],
             "record_of_largest_count": [list(vc), "interfering chance", float(F(s100[vc][0] ** 2, W)), "log2 n", float(lg(s100[vc][1]))],
             "interfering_chance_absx_ge_50": float(far_q), "counting_chance_absx_ge_50": float(far_c),
             "interfering_chance_absx_le_10": float(F(sum(s * s for (x, r), (s, n) in s100.items() if abs(x) <= 10), W)),
             "counting_chance_absx_le_10": float(F(sum(n for (x, r), (s, n) in s100.items() if abs(x) <= 10), W)),
             "interfering_chance_x_gt_0": float(F(sum(s * s for (x, r), (s, n) in s100.items() if x > 0), W)),
             "interfering_mean_x": float(F(sum(s * s * x for (x, r), (s, n) in s100.items()), W))}
P["D6"] = abs(vq[0]) >= 50 and s100[vq][1] < s100[vc][1] and far_q > far_c
dc = {T: lamc[T + 1] - lamc[T] for T in range(0, 1200)}; dq = {T: lam[T + 1] - lam[T] for T in range(0, 1200)}
bad = [T for T in range(1, 1200) if dc[T] < D("0.99")]
P["D7"] = not bad
R["counting_increment"] = {"T_below_0.99": [bad[0], bad[-1], len(bad)] if bad else [], "samples": {str(T): str(dc[T])[:10] for T in (1, 2, 3, 4, 5, 10, 20, 50, 100, 600, 1199)},
                           "rate_Lc_over_T": {str(T): str(lamc[T] / T)[:10] for T in (5, 10, 20, 50, 100, 600, 1200)}}
rng = [dq[T] for T in range(1000, 1200)]
P["D8"] = all(abs(d - C) < D("0.01") for d in rng)
R["interfering_increment"] = {"min_1000_1199": str(min(rng))[:12], "max_1000_1199": str(max(rng))[:12], "mean_1000_1199": str(sum(rng) / len(rng))[:12],
                              "samples": {str(T): str(dq[T])[:10] for T in (2, 3, 4, 5, 6, 7, 8, 50, 51, 100, 101, 600, 601, 1198, 1199)},
                              "min_100_1199": str(min(dq[T] for T in range(100, 1200)))[:12], "max_100_1199": str(max(dq[T] for T in range(100, 1200)))[:12]}
P["D9"] = abs(c200 - c400) < E and str(c400.quantize(D("1e-13"))) == "0.7715533031636"
R["c_star_trapezoid_N400"] = str(c400)[:45]; R["c_star_N200_minus_N400"] = str(c200 - c400)
a = json.load(open(os.path.join(Z, "function", "result_instances_run1.json"))); b = json.load(open(os.path.join(os.path.dirname(Z), "SPRINT_2026-11-15", "result_kill_z10_run1.json")))
R["author_c_star_minus_mine"] = str(D(repr(a["c_star"])) - c400)[:12]
ta = {r[0]: r[1] for r in a["table"]}
agree = all(b["rates"][str(T)].startswith(ta[T]) or ta[T].startswith(b["rates"][str(T)]) for T in (300, 600))
la = [l.strip() for l in open(os.path.join(Z, "function", "slow_clock_instances.py")) if len(l.strip()) >= 40]
lb = set(l.strip() for l in open(os.path.join(os.path.dirname(Z), "SPRINT_2026-11-15", "kill_test_z10.py")) if len(l.strip()) >= 40)
code_a = [l for l in la if not l.startswith(('"""', 'K', 'PRED', 'Sign', 'eps', 'coun', 'c*', 'Repo', 'Usage', 'then', '1/(')) ]
shared = [l for l in code_a if l in lb]
R["D10"] = {"rates_agree": agree, "identical_code_lines_40plus_chars": len(shared), "of_code_lines_in_instances_program": len(code_a), "examples": shared[:4]}
P["D10"] = agree and len(shared) < 5
pl = json.load(open(os.path.join(Z, "function", "plot_age_rate.json"))); miss = []
for ser, val in zip(pl["series"], (lambda T: lam[T] / T, lambda T: C, lambda T: lamc[T] / T)):
    for T, lo, hi in ser["data"]:
        if not (D(int(lo.split("/")[0])) / 10 ** 6 <= val(T) <= D(int(hi.split("/")[0])) / 10 ** 6): miss.append([ser["name"], T])
P["D11"] = not miss; R["plot_misses"] = miss
R["plot_min_value_vs_y_floor"] = [str(min(lam[T] / T for T in range(50, 601, 50)))[:8], pl["y_domain"]]
eq = [T for T in range(1, 1201) if abs(lam[T] - lamc[T]) <= E]; gt = [T for T in range(1, 1201) if lam[T] > lamc[T] + E]
R["rates"] = {str(T): str(lam[T] / T)[:12] for T in (300, 600, 1200)}
P["D12"] = eq == [1, 2, 3, 4] and not gt and all(lam[T] / T < C for T in range(1, 1201)) and \
    [str((lam[T] / T).quantize(D("1e-6"))) for T in (300, 600, 1200)] == ["0.755081", "0.762485", "0.766603"]
R["strict_rise_3_to_1199"] = all(lam[T + 1] > lam[T] + E for T in range(2, 1200))
rep = {"argv": sys.argv, "predicates": P, "report": R}
json.dump(rep, open(OUT, "x"), indent=1); print(json.dumps(rep, indent=1))
