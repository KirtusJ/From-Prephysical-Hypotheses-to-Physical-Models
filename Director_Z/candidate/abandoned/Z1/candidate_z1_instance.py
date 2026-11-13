#!/usr/bin/env python3
"""Candidate model Z1, primary instance Z1-R: exact tables.  Written with the model's first formulation (13 November 2026).
Carrier: signed arc digraph of a ring of N sites.  Vertices (x,R), (x,L).  From either vertex at x one arc goes to (x+1,R) and one
to (x-1,L).  Gain -1 on the arc (x,L) -> (x-1,L), +1 on the other three kinds.  Start x0 = (0,R).
Rule of the model: mu(S) = ||v_S||^2, v_S(y) = sum of the gains of the walks of S that end at y.
Predicates, fixed before the first run:
 I1  A^T A = 2 (the step is norm-preserving of degree two), for N = 3, 4, 5, 8, 16;
 I2  for every t = 0..T the numbers P_t(y) = mu(S_t(y))/2^t over all end vertices y are non-negative and sum to 1 (exact rationals);
 I3  consistency on a sample: for 2000 random events S (random subsets of the walks of a length t <= 8), mu(Ext S) = 2 mu(S) exactly;
 I4  the count rule nu(S) = |S| is also consistent on the same sample (it is what the near-return stipulation excludes);
 I5  the return weight R_t = P_t(x0): under the count it is at most 1/2 for t >= 1; under the model it reaches 1 at some t <= T_return
     for N = 4 and N = 8 (exact), which is recorded with the first such t;
 I6  a formal event with normalized weight above one exists: some subset S of the walks of one length t <= 6 from x0 has
     mu(S)/2^t > 1 (recorded with the smallest t found and the subset); this is a recorded weakness of the event algebra, not a pass.
Writes Candidate_Z1_Instance_Results.json; refuses to overwrite.  Seed fixed."""
import itertools, json, os, random, sys
from fractions import Fraction as Fr
OUT = "Candidate_Z1_Instance_Results.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
SEED = 20261124; random.seed(SEED)
def carrier(N):
    idx = lambda x, s: 2 * (x % N) + s           # s = 0: R, 1: L
    succ = {}
    for x in range(N):
        for s in (0, 1):
            succ[idx(x, s)] = [(idx(x + 1, 0), 1), (idx(x - 1, 1), -1 if s == 1 else 1)]
    return 2 * N, succ
def walks(succ, t, x0=0):
    W = [((x0,), 1)]
    for _ in range(t): W = [(w + (y,), g * h) for w, g in W for y, h in succ[w[-1]]]
    return W
def vec(S, n):
    v = [0] * n
    for w, g in S: v[w[-1]] += g
    return v
mu = lambda S, n: sum(c * c for c in vec(S, n))
def ext(S, succ): return [(w + (y,), g * h) for w, g in S for y, h in succ[w[-1]]]
R = {"seed": SEED}
# I1
ok1 = True
for N in (3, 4, 5, 8, 16):
    n, succ = carrier(N); A = [[0] * n for _ in range(n)]
    for y in succ:
        for z, h in succ[y]: A[z][y] = h
    ok1 &= all(sum(A[z][a] * A[z][b] for z in range(n)) == (2 if a == b else 0) for a in range(n) for b in range(n))
R["I1"] = dict(passed=ok1)
# I2 and tables, N = 16 (no wrap up to t = 7), by amplitude propagation
def distribution(N, T):
    n, succ = carrier(N); amp = [0] * n; amp[0] = 1; cnt = [0] * n; cnt[0] = 1; rows = []
    for t in range(T + 1):
        rows.append(dict(t=t, model=[str(Fr(a * a, 2 ** t)) for a in amp], count=[str(Fr(c, 2 ** t)) for c in cnt],
                         model_sum=str(sum(Fr(a * a, 2 ** t) for a in amp)), amplitudes=amp[:]))
        na = [0] * n; nc = [0] * n
        for y in range(n):
            for z, h in succ[y]: na[z] += amp[y] * h; nc[z] += cnt[y]
        amp, cnt = na, nc
    return rows
rows16 = distribution(16, 8)
R["I2"] = dict(passed=all(r["model_sum"] == "1" for r in rows16), ring=16, note="vertex index 2x+s, s=0 for R and 1 for L",
               table=[dict(t=r["t"], amplitudes_by_vertex={str(i): a for i, a in enumerate(r["amplitudes"]) if a},
                           model_probability_by_vertex={str(i): p for i, p in enumerate(r["model"]) if p != "0"},
                           count_probability_by_vertex={str(i): p for i, p in enumerate(r["count"]) if p != "0"}) for r in rows16[:7]])
# I3, I4
n, succ = carrier(16); ok3 = ok4 = True; tested = 0
pools = {t: walks(succ, t) for t in range(1, 9)}
for _ in range(2000):
    t = random.randint(1, 8); W = pools[t]; S = random.sample(W, random.randint(1, min(len(W), 12)))
    E = ext(S, succ); tested += 1
    ok3 &= mu(E, n) == 2 * mu(S, n); ok4 &= len(E) == 2 * len(S)
R["I3"] = dict(passed=ok3, events=tested); R["I4"] = dict(passed=ok4, events=tested)
# I5 return weights
ret = {}
for N in (4, 8):
    n, succ = carrier(N); amp = [0] * n; amp[0] = 1; cnt = [0] * n; cnt[0] = 1; first = None; cmax = Fr(0)
    for t in range(1, 2001):
        na = [0] * n; nc = [0] * n
        for y in range(n):
            for z, h in succ[y]: na[z] += amp[y] * h; nc[z] += cnt[y]
        amp, cnt = na, nc
        cmax = max(cmax, Fr(cnt[0], 2 ** t))
        if first is None and amp[0] * amp[0] == 2 ** t: first = t
    ret[str(N)] = dict(first_exact_return_of_the_model=first, largest_count_return_weight=str(cmax))
R["I5"] = dict(passed=all(v["first_exact_return_of_the_model"] is not None and Fr(v["largest_count_return_weight"]) <= Fr(1, 2) for v in ret.values()), rings=ret)
# I6 formal event with weight above one
n, succ = carrier(16); found = None
for t in range(1, 7):
    W = walks(succ, t); full = vec(W, n)
    best = None
    for i, (w, g) in enumerate(W):                      # remove one walk
        v = full[:]; v[w[-1]] -= g
        val = Fr(sum(c * c for c in v), 2 ** t)
        if val > 1 and (best is None or val > best[0]): best = (val, i)
    if best:
        w, g = W[best[1]]
        found = dict(t=t, normalized_weight=str(best[0]), removed_walk_vertices=list(w), removed_walk_gain=g,
                     count_rule_weight_of_the_same_event=str(Fr(len(W) - 1, 2 ** t))); break
R["I6"] = dict(passed=found is not None, event=found)
R["_summary"] = dict(predicates=6, passed=sum(1 for k in ("I1", "I2", "I3", "I4", "I5", "I6") if R[k]["passed"]))
json.dump(R, open(OUT, "w"), indent=1)
print(json.dumps(R["_summary"])); print("I5", json.dumps(R["I5"]["rings"])); print("I6", json.dumps(R["I6"]["event"]))
for r in R["I2"]["table"][:5]: print(r["t"], r["model_probability_by_vertex"], "| count", r["count_probability_by_vertex"])
