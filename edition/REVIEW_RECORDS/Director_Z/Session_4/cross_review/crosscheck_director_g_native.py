#!/usr/bin/env python3
"""Director Z cross-check of numbers in Director G's Native_preparations_and_probability_embeddings.md (commit 00b8e26).  Exact arithmetic
(integers, Fractions; Q(sqrt5) as pairs).  Nothing is imported from Director G's programs.  Predicates fixed before the run:
 N1  with d = (T - T^-1)|0> on five sheets and B = T + T^-1, the squared counts C_s = |B^s d|^2 satisfy C_0 = C_1 = 2 and
     C_{s+2} = 3 C_{s+1} - C_s for s <= 40;
 N2  q_s = C_{s+1} / (8 C_s) equals 1/8, 1/4, 5/16, 13/40, 233/712, 5473/16724 at s = 0, 1, 2, 3, 6, 10, is increasing for s >= 0,
     and 8 q_40 is within 1e-15 of (3 + sqrt5)/2;
 N3  for the filtered vector A_s = B^s d, a_s b_s = 5 exactly, where a_s = |A_s(zeta)|^2, b_s = |A_s(zeta^2)|^2 are computed in Q(sqrt5),
     and the smaller plane weight equals 1/(1 + phi^(4s-2)) for s >= 1 (to 1e-12, s <= 12);
 N4  bound (2): for 2000 random integer zero-sum sheet vectors with entries in -6..6, e (1 - e) >= 4/(5 C^2) with e the smaller plane
     weight, and a b is a positive integer divisible by 5;
 N5  branch invariant in an instance: for all 2^6 direction-record words of six native steps from a localized sheet on five sheets,
     the unnormalized branch vector times 2^(t/2) is an integer vector (so its probability is the rational 2^-t sum m_i^2), and the
     probabilities of the 64 words sum to 1.
Writes Crosscheck_Director_G_Native_Results.json; refuses to overwrite."""
import itertools, json, math, os, random, sys
from fractions import Fraction as Fr
OUT = "Crosscheck_Director_G_Native_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
R = {}; ok = lambda name, val, **info: R.__setitem__(name, dict(passed=bool(val), **info))
M = 5
def Bop(v): return [v[(y - 1) % M] + v[(y + 1) % M] for y in range(M)]
d = [0, 1, 0, 0, -1]
vecs = [d]
for s in range(42): vecs.append(Bop(vecs[-1]))
C = [sum(x * x for x in v) for v in vecs]
ok("N1_squared_counts_recurrence", C[0] == 2 and C[1] == 2 and all(C[s + 2] == 3 * C[s + 1] - C[s] for s in range(40)), first=C[:8])
q = [Fr(C[s + 1], 8 * C[s]) for s in range(41)]
want = {0: Fr(1, 8), 1: Fr(1, 4), 2: Fr(5, 16), 3: Fr(13, 40), 6: Fr(233, 712), 10: Fr(5473, 16724)}
ok("N2_record_ratios_and_limit", all(q[s] == w for s, w in want.items()) and all(q[s + 1] > q[s] for s in range(40)) and abs(8 * float(q[40]) - (3 + math.sqrt(5)) / 2) < 1e-15,
   values={str(s): str(q[s]) for s in want}, eight_q40=8 * float(q[40]))
# Q(sqrt5): |A(zeta^j)|^2 = sum_{y,y'} m_y m_y' cos(2 pi j (y - y')/5); cos(2pi/5) = (sqrt5 - 1)/4, cos(4pi/5) = (-sqrt5 - 1)/4.  Pair (r, s) = r + s sqrt5.
def plane_weights(m):
    def val(j):
        r = Fr(0); s5 = Fr(0)
        for y in range(M):
            for y2 in range(M):
                k = (j * (y - y2)) % M; c = m[y] * m[y2]
                if k == 0: r += c
                elif k in (1, 4): r += Fr(-c, 4); s5 += Fr(c, 4)
                else: r += Fr(-c, 4); s5 += Fr(-c, 4)
        return (r, s5)
    return val(1), val(2)
def mul(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
fl = lambda x: float(x[0]) + float(x[1]) * math.sqrt(5)
phi = (1 + math.sqrt(5)) / 2; rows = []; n3 = True
for s in range(0, 13):
    a, b = plane_weights(vecs[s]); prod = mul(a, b); n3 &= (prod == (Fr(5), Fr(0)))
    e = min(fl(a), fl(b)) / (fl(a) + fl(b)); rows.append(dict(s=s, a=fl(a), b=fl(b), smaller_weight=e, formula=1 / (1 + phi ** (4 * s - 2))))
    if s >= 1: n3 &= abs(e - 1 / (1 + phi ** (4 * s - 2))) < 1e-12
ok("N3_norm_five_and_wrong_plane_weight", n3, rows=rows)
random.seed(20261118); worst = None; n4 = True
for _ in range(2000):
    m = [random.randint(-6, 6) for _ in range(M - 1)]; m.append(-sum(m))
    if not any(m): continue
    a, b = plane_weights(m); prod = mul(a, b); Cc = sum(x * x for x in m)
    integer = prod[1] == 0 and prod[0].denominator == 1 and prod[0] > 0 and prod[0] % 5 == 0
    e = min(fl(a), fl(b)) / (fl(a) + fl(b)); slack = e * (1 - e) - 4 / (5 * Cc * Cc)
    n4 &= integer and slack >= -1e-15 and abs(fl(a) + fl(b) - 2.5 * Cc) < 1e-9
    if worst is None or slack < worst[0]: worst = (slack, m, int(prod[0]) if integer else str(prod))
ok("N4_five_sheet_bound", n4, smallest_slack=worst[0], at_vector=worst[1], norm_ab=worst[2], seed=20261118)
# N5: native steps: state on (site x, direction c, sheet y); step: sheet translated by the departure site, coin, shift.  Integer vectors with a factor 2^(-t/2).
def step(state):
    out = {}
    for (x, c, y), amp in state.items():
        y2 = (y + x) % M
        for c2, x2, sign in ((0, x + 1, 1), (1, x - 1, -1 if c == 1 else 1)):
            out[(x2, c2, y2)] = out.get((x2, c2, y2), 0) + sign * amp
    return out
total = Fr(0); integral = True; words = 0
def rec(state, t, prob_num):
    global total, integral, words
    if t == 6:
        total += Fr(sum(a * a for a in state.values()), 2 ** t); words += 1; return
    nxt = step(state)
    for c in (0, 1):                                      # record the direction; sheets and sites stay coherent
        br = {k: a for k, a in nxt.items() if k[1] == c}
        integral &= all(isinstance(a, int) for a in br.values())
        rec(br, t + 1, None)
rec({(0, 0, 0): 1}, 0, None)
ok("N5_branch_invariant_instance", integral and total == 1 and words == 64, words=words, total_probability=str(total))
R["_summary"] = dict(predicates=sum(1 for k in R if not k.startswith("_")), passed=sum(1 for k, v in R.items() if not k.startswith("_") and v["passed"]))
json.dump(R, open(OUT, "w"), indent=1, default=str)
for k, v in R.items():
    if not k.startswith("_"): print(("PASS " if v["passed"] else "FAIL ") + k)
print(R["_summary"])
