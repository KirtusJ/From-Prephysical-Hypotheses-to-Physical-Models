"""alt_rules.py -- Attack A(iv) on candidate model Z1: alternative rules on the signed ring Z1-R.

Carrier: signed ring, N = 8 sites, vertices (x,R),(x,L), arcs (x,*)->(x+1,R), (x,*)->(x-1,L),
gain -1 on (x,L)->(x-1,L), +1 otherwise, d = 2, x0 = (0,R).  Exact arithmetic (Fraction/int).
Convention: v_S(y) = sum of gains (+1/-1) of the walks of S ending at y; return weight
R_t = mu(all walks of length t ending at x0) / 2^t; "S5" is read LITERALLY: there is t >= 1
with R_t arbitrarily close to 1; here tested as R_t == 1 exactly for some 1 <= t <= 48.

Rules (each a function of the event):
  MODEL   ||v_S||^2
  COUNT   |S|                                   (intended: violates S5 only)
  MIX     (|S| + ||v_S||^2)/2                   (intended: violates S5 only)
  NEG     (1+s)||v_S||^2 - s|S|, s = (1-q)/(q-p) at the first t>=1 with p_t < q_t < 1,
          p_t = N_t/2^t, q_t = model return weight   (intended: violates S4 non-negativity only)
  UNNORM  a|S| + c||v_S||^2, a = 1/2, c = 1 - a*N_24/2^24  (intended: violates S4 normalization only)
  GRAM    v^T G v, G = (I + e(U^2 + U^-2))/(1+e), e = 1/4, U = A/sqrt2
          (intended: violates S3 additivity over end vertices only)
  ALTGAIN ||v'_S||^2 with v' built from other gains g': -1 on (x,R)->(x+1,R), +1 otherwise
          (intended: violates S3 "only through the multiset of gains" only)
  LOCAL   sum_y F_y, F_x0 = sigma^2, F_y = count for y != x0   (intended: violates S2 only)

Predicates, fixed before the first run.  For each rule, on ALL events of lengths 0..4:
  S2    mu(Ext S) == 2 mu(S) for every event S of length 0..3
  S3add mu(S) == sum over end vertices y of mu(S restricted to y), all events length <= 4
  S3gain mu is constant on events with the same family (multiset of gains g at each end vertex),
         all events of length <= 4; hypothesis check: number of families shared by >1 event is reported
  S4nn  mu(S) >= 0 for all events of length <= 4
  S4norm mu({w}) == 1 for every walk of length <= 4
  S5    exists 1 <= t <= 48 with R_t == 1
  DIFF  mu differs from MODEL on some event of length <= 3
P1  MODEL passes S2,S3add,S3gain,S4nn,S4norm,S5.
P2  COUNT and MIX: fail S5, pass all others, DIFF true.
P3  NEG: fails S4nn, passes all others, DIFF true.
P4  UNNORM: fails S4norm, passes all others, DIFF true.
P5  GRAM: fails S3add, passes all others, DIFF true.
P6  ALTGAIN: fails S3gain, passes all others, DIFF true.
P7  LOCAL: fails S2, passes all others, DIFF true.
P8  matrix identities: A^T A = 2I; A^T G A = 2 G; G has unit diagonal; G = ((1-2e)I + e(U+U^T)^2)/(1+e)
    (hence positive semidefinite); A'^T A' = 2I for the other gains.
Failed predicates are kept in the result file.  The result file is not overwritten.
"""
import sys, os, json, itertools
from fractions import Fraction as Fr
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alt_rules_result.json")
if os.path.exists(OUT): sys.exit("result exists; refusing to overwrite")
N = 8
V = [(x, c) for x in range(N) for c in "RL"]; idx = {v: i for i, v in enumerate(V)}; n = len(V)
x0 = idx[(0, "R")]
def arcs(v):
    x, c = v
    return [((x+1) % N, "R"), ((x-1) % N, "L")]
def g(v, w):  return -1 if (v[1] == "L" and w[1] == "L") else 1
def g2(v, w): return -1 if (v[1] == "R" and w[1] == "R") else 1
A  = [[0]*n for _ in range(n)]; A2 = [[0]*n for _ in range(n)]
for v in V:
    for w in arcs(v):
        A[idx[w]][idx[v]] = g(v, w); A2[idx[w]][idx[v]] = g2(v, w)
def mm(X, Y): return [[sum(X[i][k]*Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def T(X): return [list(r) for r in zip(*X)]
I = [[int(i == j) for j in range(n)] for i in range(n)]
e = Fr(1, 4)
AA = mm(A, A); AAT = T(AA)              # U^2 = AA/2, U^-2 = AAT/2
G = [[(I[i][j] + e*Fr(AA[i][j] + AAT[i][j], 2))/(1+e) for j in range(n)] for i in range(n)]
S_ = [[A[i][j] + A[j][i] for j in range(n)] for i in range(n)]; SS = mm(S_, S_)   # (U+U^T)^2 = SS/2
P8 = {
 "ATA=2I": mm(T(A), A) == [[2*I[i][j] for j in range(n)] for i in range(n)],
 "ATGA=2G": mm(mm(T(A), G), A) == [[2*G[i][j] for j in range(n)] for i in range(n)],
 "G unit diagonal": all(G[i][i] == 1 for i in range(n)),
 "G=((1-2e)I+e(U+UT)^2)/(1+e)": G == [[((1-2*e)*I[i][j] + e*Fr(SS[i][j], 2))/(1+e) for j in range(n)] for i in range(n)],
 "A'TA'=2I": mm(T(A2), A2) == [[2*I[i][j] for j in range(n)] for i in range(n)],
}
# walks: tuple of vertex indices; data (end, g, g')
def walks(t):
    W = [((x0,), 1, 1)]
    for _ in range(t):
        W = [(p+(idx[w],), a*g(V[p[-1]], w), b*g2(V[p[-1]], w)) for (p, a, b) in W for w in arcs(V[p[-1]])]
    return W
# an event is represented by its counts: dict (end, g, g') -> number
def counts_of(ws):
    c = {}
    for (p, a, b) in ws: c[(p[-1], a, b)] = c.get((p[-1], a, b), 0) + 1
    return c
def vec(c, which):
    v = [0]*n
    for (y, a, b), k in c.items(): v[y] += k*(a if which == 0 else b)
    return v
def size(c): return sum(c.values())
def norm2(c, which=0): return sum(z*z for z in vec(c, which))
# all-walks return counts by transfer over (end,g,g')
def full_counts(t):
    c = {(x0, 1, 1): 1}
    for _ in range(t):
        d = {}
        for (y, a, b), k in c.items():
            for w in arcs(V[y]):
                key = (idx[w], a*g(V[y], w), b*g2(V[y], w)); d[key] = d.get(key, 0) + k
        c = d
    return c
def ret_counts(t): return {k: v for k, v in full_counts(t).items() if k[0] == x0}
TMAX = 48
RC = {t: ret_counts(t) for t in range(1, TMAX+1)}
p = {t: Fr(size(RC[t]), 2**t) for t in RC}; q = {t: Fr(norm2(RC[t]), 2**t) for t in RC}
tneg = next(t for t in range(1, TMAX+1) if p[t] < q[t] < 1)
s = (1-q[tneg])/(q[tneg]-p[tneg])
a_un = Fr(1, 2); c_un = 1 - a_un*p[24]
def gram(c):
    v = vec(c, 0); return sum(v[i]*G[i][j]*v[j] for i in range(n) if v[i] for j in range(n) if v[j])
def local(c):
    v = vec(c, 0); return v[x0]**2 + sum(k for (y, a, b), k in c.items() if y != x0)
RULES = {
 "MODEL": lambda c: Fr(norm2(c)),
 "COUNT": lambda c: Fr(size(c)),
 "MIX": lambda c: Fr(size(c) + norm2(c), 2),
 "NEG": lambda c: (1+s)*norm2(c) - s*size(c),
 "UNNORM": lambda c: a_un*size(c) + c_un*norm2(c),
 "GRAM": lambda c: Fr(gram(c)),
 "ALTGAIN": lambda c: Fr(norm2(c, 1)),
 "LOCAL": lambda c: Fr(local(c)),
}
L = 4
Wt = {t: walks(t) for t in range(L+2)}
def subsets(t):
    W = Wt[t]
    for mask in range(1 << len(W)):
        yield mask, [W[i] for i in range(len(W)) if mask >> i & 1]
def ext(ws):
    out = []
    for (pth, a, b) in ws:
        for w in arcs(V[pth[-1]]):
            out.append((pth+(idx[w],), a*g(V[pth[-1]], w), b*g2(V[pth[-1]], w)))
    return out
res = {"carrier": "signed ring N=8, x0=(0,R)", "P8_matrix": P8, "tneg": tneg, "s": str(s),
       "a_unnorm": str(a_un), "c_unnorm": str(c_un), "rules": {}, "values_len_le_3": {}}
# precompute events
EV = {t: list(subsets(t)) for t in range(L+1)}
fam_groups = {}
for t in range(L+1):
    for mask, ws in EV[t]:
        key = (t, tuple(sorted((pth[-1], a) for (pth, a, b) in ws)))
        fam_groups.setdefault(key, []).append((t, mask))
shared = sum(1 for k, vv in fam_groups.items() if len(vv) > 1)
res["families_shared_by_more_than_one_event(len<=4)"] = shared
res["events_checked"] = {t: len(EV[t]) for t in EV}
for name, mu in RULES.items():
    val = {}
    r = {}
    bad = {k: [] for k in ("S2", "S3add", "S3gain", "S4nn", "S4norm")}
    for t in range(L+1):
        for mask, ws in EV[t]:
            m = mu(counts_of(ws)); val[(t, mask)] = m
            if m < 0: bad["S4nn"].append((t, mask, str(m)))
            if len(ws) == 1 and m != 1: bad["S4norm"].append((t, mask, str(m)))
            ends = {}
            for w in ws: ends.setdefault(w[0][-1], []).append(w)
            if sum(mu(counts_of(x)) for x in ends.values()) != m: bad["S3add"].append((t, mask))
            if t <= L-1:
                if mu(counts_of(ext(ws))) != 2*m: bad["S2"].append((t, mask))
    for key, evs in fam_groups.items():
        if len({val[e_] for e_ in evs}) > 1: bad["S3gain"].append([key[0], evs[0][1], evs[1][1]])
    Rt = {t: mu(RC[t])/2**t for t in RC}
    hits = [t for t in Rt if Rt[t] == 1]
    r["S5"] = bool(hits); r["S5_first_t_with_R=1"] = hits[0] if hits else None
    r["max_R_t(1..48)"] = str(max(Rt.values()))
    for k in bad:
        r[k] = not bad[k]; r[k+"_violations"] = len(bad[k]); r[k+"_first"] = bad[k][:2]
    model = RULES["MODEL"]
    diffs = [(t, mask) for t in range(4) for mask, ws in EV[t] if val[(t, mask)] != model(counts_of(ws))]
    r["DIFF"] = bool(diffs); r["n_diff_len_le_3"] = len(diffs)
    if diffs:
        t, mask = diffs[0]; ws = [Wt[t][i] for i in range(len(Wt[t])) if mask >> i & 1]
        r["first_diff"] = {"t": t, "walks": [[list(V[i]) for i in w[0]] for w in ws],
                           "rule": str(val[(t, mask)]), "model": str(model(counts_of(ws)))}
    res["rules"][name] = r
    res["values_len_le_3"][name] = {"%d:%d" % (t, mask): str(val[(t, mask)]) for t in range(4) for mask, _ in EV[t]}
    # end-vertex probabilities of the full event at t=3
    full = Wt[3]; ends = {}
    for w in full: ends.setdefault(w[0][-1], []).append(w)
    r["P_3(y)"] = {str(V[y]): str(mu(counts_of(x))/8) for y, x in sorted(ends.items())}
res["walk_index_len3"] = [[list(V[i]) for i in w[0]] + [w[1]] for w in Wt[3]]
keys = ["S2", "S3add", "S3gain", "S4nn", "S4norm", "S5"]
def only_fails(name, f): 
    r = res["rules"][name]; return all((r[k] is False) if k == f else r[k] for k in keys) and r["DIFF"]
R = res["rules"]
pred = {
 "P1": all(R["MODEL"][k] for k in keys),
 "P2": only_fails("COUNT", "S5") and only_fails("MIX", "S5"),
 "P3": only_fails("NEG", "S4nn"), "P4": only_fails("UNNORM", "S4norm"),
 "P5": only_fails("GRAM", "S3add"), "P6": only_fails("ALTGAIN", "S3gain"),
 "P7": only_fails("LOCAL", "S2"), "P8": all(P8.values()),
}
res["predicates"] = pred
json.dump(res, open(OUT, "x"), indent=1)
print(json.dumps(pred)); 
for k, r in R.items(): print(k, {x: r[x] for x in keys}, r["S5_first_t_with_R=1"], r["max_R_t(1..48)"], r.get("first_diff"), r["P_3(y)"])
print("shared families", shared, "tneg", tneg, "s", s, "c_un", c_un)
