"""Target 1 (and 5, 6-part, 3-mirror): T-1 on position product events, exact.
Command: python3 t1.py   (no arguments; seed 20261115 for the sampled parts)
PREDICATES, fixed before the first run. Hypothesis tested per event: W = sum eps^2 > 0 (qualifies).
 A0 the aggregated propagation equals explicit walk enumeration (ring 3, 1, 2, line; all mask sequences to length 4).
 A1 for each qualifying event, each occupied site x: child (x+1,R) has (eps_R+eps_L, n_R+n_L), child (x-1,L) has
    (eps_R-eps_L, n_R+n_L), and the number of end vertices after the step is 2 * (number of occupied sites)
    [= "receive walks from no other site"].
 A2 W(after) = 2 W(before).
 A3 H(after) >= H(before)  (exact sign).
 A4 H(after) = H(before)  iff  every site carrying chance has n_R = 0 or n_L = 0   (FORM wording).
 A5 H(after) = H(before)  iff  every OCCUPIED site has n_R = 0 or n_L = 0          (BRAND commitment 1 wording).
 B3 as A3 with p = n / sum n (plain count).           [target 5]
 C3 as A3 with weight |eps| ; D3 with weight eps^4.   [target 5: not conserved site by site; expected to fail]
 N1 arbitrary sets of walks of one length (not position product events): A2, A3, A4.
 M3 mirror carrier (walks ending at a pinned vertex, prepend a step, masks on the new start site): A3. [target 3]
 R1 non-injectivity: two qualifying events of equal length on one carrier with equal after-state and different before-state.
 T4 1 <= n(v) <= 2^T at every record of every event; H = 0 at T = 0.
Ranges: rings N=1,2 to T=10; N=3 to T=6; N=4 to T=9; N=5 to T=4; N=6 to T=5; N=7 to T=4; line to T=4.
Masks = non-empty subsets of the sites reachable at that step. Failures are all kept (first 5 of each written out)."""
import json, random, sys, itertools
from lib import *
random.seed(20261115)
res = {"command": "python3 t1.py", "seed": 20261115}
# A0
def walks_explicit(N, masks):
    ws = [((0, 0), 1)]
    for m in masks:
        nw = []
        for (x, s), sg in ws:
            for (y, t, f) in ((x + 1, 0, 1), (x - 1, 1, -1 if s == 1 else 1)):
                if N: y %= N
                if y in m: nw.append(((y, t), sg * f))
        ws = nw
    st = {}
    for v, sg in ws:
        a, b = st.get(v, (0, 0)); st[v] = (a + sg, b + 1)
    return st
a0 = [0, 0]
for N in (1, 2, 3, None):
    for T, ms, st in events(N, 4):
        a0[0] += 1
        if walks_explicit(N, [set(m) for m in ms]) != st: a0[1] += 1
res["A0"] = {"cases": a0[0], "fail": a0[1]}
W_ = {"sq": lambda e, n: e * e, "count": lambda e, n: n, "abs": lambda e, n: abs(e), "quart": lambda e, n: e ** 4}
def t1(st, N, stepf=step, w="sq"):
    a = stepf(st, N)
    return sign_lin(Hterms(a, W_[w]) + neg(Hterms(st, W_[w])))
def sites(st):
    d = {}
    for (x, s), (e, n) in st.items(): d.setdefault(x, {})[s] = (e, n)
    return d
def eqcond(st, occupied=False):
    for x, r in sites(st).items():
        (eR, nR), (eL, nL) = r.get(0, (0, 0)), r.get(1, (0, 0))
        if (occupied or eR or eL) and nR and nL: return False
    return True
ranges = [(1, 10), (2, 10), (3, 6), (4, 9), (5, 4), (6, 5), (7, 4), (None, 4)]
fails = {k: [] for k in "A1 A2 A3 A4 A5 B3 C3 D3 M3 T4".split()}
cnt = {}
per = {}
after_map = {}
for N, Tmax in ranges:
    c = dict(seqs=0, qualify=0, zero_weight=0, equal=0, strict=0, distinct_states=0, A5_exceptions=0,
             C3_fail=0, D3_fail=0, B3_fail=0)
    memo = {}
    for T, ms, st in events(N, Tmax):
        c["seqs"] += 1
        if any(not (1 <= n <= 2 ** T) for e, n in st.values()): fails["T4"].append([N, ms])
        W = sum(e * e for e, n in st.values())
        if W == 0: c["zero_weight"] += 1; continue
        c["qualify"] += 1
        k = (T, key(st))
        if k not in memo:
            c["distinct_states"] += 1
            a = step(st, N)
            ok1 = len(a) == 2 * len(sites(st))
            for x, r in sites(st).items():
                (eR, nR), (eL, nL) = r.get(0, (0, 0)), r.get(1, (0, 0))
                y, z = (x + 1, x - 1) if not N else ((x + 1) % N, (x - 1) % N)
                ok1 &= a[(y, 0)] == (eR + eL, nR + nL) and a[(z, 1)] == (eR - eL, nR + nL)
            ok2 = sum(e * e for e, n in a.values()) == 2 * W
            s = t1(st, N)
            memo[k] = (ok1, ok2, s, eqcond(st), eqcond(st, True), t1(st, N, w="count"), t1(st, N, w="abs"), t1(st, N, w="quart"))
            after_map.setdefault((N, T, key(a)), set()).add(key(st))
        ok1, ok2, s, eq, eqb, sB, sC, sD = memo[k]
        rec = [N, T, ms, sorted(st.items())]
        if not ok1: fails["A1"].append(rec)
        if not ok2: fails["A2"].append(rec)
        if s < 0: fails["A3"].append(rec)
        if (s == 0) != eq: fails["A4"].append(rec)
        if (s == 0) != eqb: fails["A5"].append(rec); c["A5_exceptions"] += 1
        if sB < 0: fails["B3"].append(rec); c["B3_fail"] += 1
        if sC < 0: fails["C3"].append(rec); c["C3_fail"] += 1
        if sD < 0: fails["D3"].append(rec); c["D3_fail"] += 1
        c["equal" if s == 0 else "strict"] += 1
    per["line" if N is None else "ring%d" % N] = dict(Tmax=Tmax, **c)
    print(N, c, flush=True)
res["per_carrier"] = per
coll = [(k[0], k[1], [list(map(list, b)) for b in v]) for k, v in after_map.items() if len(v) > 1]
res["R1"] = {"collisions": len(coll), "first": coll[:2]}
# mirror
mc = dict(seqs=0, qualify=0, fail=0, equal=0, strict=0)
for N, Tmax in [(1, 8), (2, 8), (3, 5), (4, 7), (5, 4), (None, 4)]:
    memo = {}
    for T, ms, st in events(N, Tmax, mstep):
        mc["seqs"] += 1
        if sum(e * e for e, n in st.values()) == 0: continue
        mc["qualify"] += 1
        k = key(st)
        if k not in memo: memo[k] = t1(st, N, mstep)
        s = memo[k]
        if s < 0: mc["fail"] += 1; fails["M3"].append([N, T, ms])
        mc["equal" if s == 0 else "strict"] += 1
res["M3_mirror"] = mc
# N1 arbitrary sets of walks
def allwalks(N, T):
    ws = [((0, 0), 1)]
    for _ in range(T):
        ws = [((((x + 1) % N if N else x + 1), 0), sg) for (x, s), sg in ws] and \
             [w for (x, s), sg in ws for w in ((((x + 1) % N if N else x + 1, 0), sg), (((x - 1) % N if N else x - 1, 1), -sg if s == 1 else sg))]
    return ws
n1 = {}
fails["N1"] = []
for N, T, mode in [(1, 3, "all"), (2, 3, "all"), (3, 3, "all"), (4, 3, "all"), (5, 3, "all"), (None, 3, "all"), (3, 4, "all"), (1, 4, "all"),
                   (3, 5, 20000), (4, 6, 20000), (5, 5, 20000), (None, 5, 20000), (2, 6, 20000)]:
    ws = allwalks(N, T); m = len(ws)
    c = dict(sets=0, qualify=0, A2_fail=0, A3_fail=0, A4_fail=0, equal=0, strict=0, product_like="not tested")
    it = range(1, 1 << m) if mode == "all" else (random.getrandbits(m) & random.getrandbits(m) if random.random() < .5 else random.getrandbits(m) for _ in range(mode))
    for b in it:
        if b == 0: continue
        st = {}
        for i in range(m):
            if b >> i & 1:
                v, sg = ws[i]; a, n = st.get(v, (0, 0)); st[v] = (a + sg, n + 1)
        c["sets"] += 1
        W = sum(e * e for e, n in st.values())
        if W == 0: continue
        c["qualify"] += 1
        a = step(st, N)
        if sum(e * e for e, n in a.values()) != 2 * W: c["A2_fail"] += 1
        s = t1(st, N)
        if s < 0: c["A3_fail"] += 1; fails["N1"].append([N, T, b])
        if (s == 0) != eqcond(st): c["A4_fail"] += 1; fails["N1"].append([N, T, b, "A4"])
        c["equal" if s == 0 else "strict"] += 1
    n1["%s_T%d_%s" % ("line" if N is None else "ring%d" % N, T, mode)] = c
    print(N, T, c, flush=True)
res["N1_arbitrary_walk_sets"] = n1
res["fail_counts"] = {k: len(v) for k, v in fails.items()}
res["fail_first5"] = {k: v[:5] for k, v in fails.items()}
res["sign_fallbacks_to_decimal"] = FALLBACK[0]
res["fallback_min_relative_margin"] = str(MINABS[0])
json.dump(res, open("result_t1_run1.json", "x"), indent=1, default=str)
print(json.dumps({k: res[k] for k in ("A0", "fail_counts", "R1", "M3_mirror", "sign_fallbacks_to_decimal", "fallback_min_relative_margin")}, default=str)[:3000])
