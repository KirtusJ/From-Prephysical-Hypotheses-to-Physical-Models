"""alt_rules_followup.py -- follow-up to failed predicate P6 of alt_rules.py.

Same carrier (signed ring N=8, x0=(0,R)).  Candidate rules ||v'_S||^2 where v' sums other gains g':
the model's gains except that at ONE site j the minus sign sits on another of the four arcs leaving
site j (types RR, RL, LR instead of LL).  24 candidates (j in 0..7, 3 types).  Exact integers.
For each candidate (hypothesis first: A'^T A' = 2I is tested per candidate and the number qualifying reported):
  S2    mu(Ext S) = 2 mu(S), all events of length 0..3
  S3add additive over end vertices, all events length <= 4
  S3gain mu constant on events with the same family of MODEL gains (length <= 4)
  S4    mu >= 0 and single walks have weight 1 (length <= 4)
  S5x   R_t == 1 for some 1 <= t <= 4000 ; otherwise max R_t over that range is reported (float of exact fraction)
  DIFF  differs from the model on an event of length <= 3
F1  at least one qualifying candidate fails S3gain, passes S2, S3add, S4, has DIFF.
F2  such a candidate also has S5x (exact return).  If F2 fails, the largest R_t found is reported;
    near-return then rests on unitarity of A'/sqrt2 (Corollary 5.29 proof, part 2), not on this program.
Result file not overwritten; failures kept.
"""
import sys, os, json
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alt_rules_followup_result.json")
if os.path.exists(OUT): sys.exit("result exists; refusing to overwrite")
N = 8
V = [(x, c) for x in range(N) for c in "RL"]; idx = {v: i for i, v in enumerate(V)}; n = len(V); x0 = idx[(0, "R")]
def arcs(v): return [((v[0]+1) % N, "R"), ((v[0]-1) % N, "L")]
def g(v, w): return -1 if v[1]+w[1] == "LL" else 1
def mk(j, typ):
    def g2(v, w):
        if v[0] == j: return -1 if v[1]+w[1] == typ else 1
        return g(v, w)
    return g2
L = 4
def run(g2):
    A2 = [[0]*n for _ in range(n)]
    for v in V:
        for w in arcs(v): A2[idx[w]][idx[v]] = g2(v, w)
    unit = all(sum(A2[k][i]*A2[k][j] for k in range(n)) == (2 if i == j else 0) for i in range(n) for j in range(n))
    Wt = [[((x0,), 1, 1)]]
    for _ in range(L+1):
        Wt.append([(p+(idx[w],), a*g(V[p[-1]], w), b*g2(V[p[-1]], w)) for (p, a, b) in Wt[-1] for w in arcs(V[p[-1]])])
    def mu(ws, which=2):
        v = {}
        for w in ws: v[w[0][-1]] = v.get(w[0][-1], 0) + w[which]
        return sum(z*z for z in v.values())
    def ext(ws): return [(p+(idx[w],), a*g(V[p[-1]], w), b*g2(V[p[-1]], w)) for (p, a, b) in ws for w in arcs(V[p[-1]])]
    r = dict(unitary=unit, S2=True, S3add=True, S3gain=True, S4=True, DIFF=False)
    fam = {}
    for t in range(L+1):
        W = Wt[t]
        for mask in range(1 << len(W)):
            ws = [W[i] for i in range(len(W)) if mask >> i & 1]; m = mu(ws)
            if len(ws) == 1 and m != 1: r["S4"] = False
            ends = {}
            for w in ws: ends.setdefault(w[0][-1], []).append(w)
            if sum(mu(x) for x in ends.values()) != m: r["S3add"] = False
            if t < L and mu(ext(ws)) != 2*m: r["S2"] = False
            key = (t, tuple(sorted((w[0][-1], w[1]) for w in ws)))
            if fam.setdefault(key, m) != m: r["S3gain"] = False
            if t <= 3 and m != mu(ws, 1) and not r["DIFF"]:
                r["DIFF"] = True
                r["first_diff"] = dict(t=t, walks=[[list(V[i]) for i in w[0]] for w in ws], rule=m, model=mu(ws, 1))
    full = Wt[3]; ends = {}
    for w in full: ends.setdefault(w[0][-1], []).append(w)
    r["P_3(y)"] = {str(V[y]): "%d/8" % mu(x) for y, x in sorted(ends.items())}
    vec = [0]*n; vec[x0] = 1; best = (0.0, 0); hit = None
    for t in range(1, 4001):
        vec = [sum(A2[i][k]*vec[k] for k in range(n) if A2[i][k]) for i in range(n)]
        num = vec[x0]**2
        if num == 1 << t: hit = t; break
        f = num/(1 << t)
        if f > best[0]: best = (f, t)
    r["S5x_first_exact_t"] = hit; r["max_R_t_float"] = best
    return r
res = {"candidates": {}}
for j in range(N):
    for typ in ("RR", "RL", "LR"):
        res["candidates"]["site%d_%s" % (j, typ)] = run(mk(j, typ))
C = res["candidates"]
res["n_qualifying_unitary"] = sum(c["unitary"] for c in C.values())
good = [k for k, c in C.items() if c["unitary"] and not c["S3gain"] and c["S2"] and c["S3add"] and c["S4"] and c["DIFF"]]
res["F1"] = bool(good); res["F1_candidates"] = good
res["F2"] = any(C[k]["S5x_first_exact_t"] for k in good); res["F2_candidates"] = [k for k in good if C[k]["S5x_first_exact_t"]]
json.dump(res, open(OUT, "x"), indent=1)
print(res["n_qualifying_unitary"], res["F1"], res["F2"])
for k in good: print(k, C[k]["S5x_first_exact_t"], C[k]["max_R_t_float"], C[k]["first_diff"], C[k]["P_3(y)"])
