"""Targets 5 and 6. Command: python3 t5.py   (seed 20261115)
PREDICATES fixed before the first run. Hypothesis per event: total weight > 0 (qualifies).
 V(w) for weight w in {sq: eps^2, count: n, abs: |eps|, quart: eps^4, support: 1 if eps != 0 else 0, invn: 1/n}:
   H_w(after one free step) >= H_w(before), H_w = sum w/W log n. Float screening (margin 1e-9), every reported failure
   confirmed by the exact sign routine. sq and count are conserved site by site (children of a site carry twice its weight);
   abs, quart, support, invn are not. Events: random masked events (each reachable site admitted with probability q, q drawn
   uniformly per event from {0.5,0.7,0.9}; a step that would empty the event is taken free) on rings 3..10 and the line, length 3..12, 3000 events per carrier.
 T2 for 400 random pairs of qualifying ring-3 events (lengths <= 5): H(product) = H1 + H2 exactly (sign routine returns 0).
 T3 ring 3, all qualifying events of length 5, then one step with mask {2}: list those with W>0 after, H before > 0 and H after = 0;
    report whether one has H before = 0.462...
 T4 checked in t1.py (n bounds); here: H <= T log 2 and H >= 0 exactly on the T2 sample."""
import json, random, math
from fractions import Fraction as F
from lib import *
random.seed(20261115)
WS = {"sq": lambda e, n: e * e, "count": lambda e, n: n, "abs": lambda e, n: abs(e), "quart": lambda e, n: e ** 4,
      "support": lambda e, n: 1 if e else 0, "invn": lambda e, n: F(1, n)}
def Hf(st, w):
    W = sum(w(e, n) for e, n in st.values())
    return sum(float(w(e, n)) / float(W) * math.log(n) for e, n in st.values() if w(e, n))
res = {"command": "python3 t5.py", "seed": 20261115, "V": {}, }
cnt = {k: dict(qualify=0, fail=0, first=None, smallest=None) for k in WS}
tot = 0
for N in list(range(3, 11)) + [None]:
    for _ in range(3000):
        T = random.randint(3, 12); q = random.choice((.5, .7, .9)); st = {(0, 0): (1, 1)}; ms = []
        for t in range(T):
            full = step(st, N); m = {x for x in {v[0] for v in full} if random.random() < q}
            if not m: m = {v[0] for v in full}
            st = {v: d for v, d in full.items() if v[0] in m}; ms.append(sorted(m))
        tot += 1
        a = step(st, N)
        for k, w in WS.items():
            if sum(w(e, n) for e, n in st.values()) == 0: continue
            cnt[k]["qualify"] += 1
            if Hf(a, w) < Hf(st, w) - 1e-9:
                s = sign_lin(Hterms(a, w) + neg(Hterms(st, w)))
                assert s < 0
                cnt[k]["fail"] += 1
                rec = {"N": N, "T": T, "masks": ms, "state": sorted(st.items()), "H_before": Hf(st, w), "H_after": Hf(a, w), "exact_sign": s}
                if cnt[k]["first"] is None: cnt[k]["first"] = rec
                if cnt[k]["smallest"] is None or len(st) < len(cnt[k]["smallest"]["state"]): cnt[k]["smallest"] = rec
res["V"] = cnt; res["events_drawn"] = tot
for k in cnt: print(k, cnt[k]["qualify"], cnt[k]["fail"], cnt[k]["smallest"], flush=True)
# T2
pool = []
seen = set()
for T, ms, st in events(3, 5):
    if any(e for e, n in st.values()) and key(st) not in seen: seen.add(key(st)); pool.append((T, st))
t2 = dict(pairs=0, fail=0, bound_fail=0)
for _ in range(400):
    (T1, a), (T2, b) = random.choice(pool), random.choice(pool)
    pr = {(u, v): (ea * eb, na * nb) for u, (ea, na) in a.items() for v, (eb, nb) in b.items()}
    t2["pairs"] += 1
    tt = Hterms(pr) + neg(Hterms(a)) + neg(Hterms(b))
    if tt and sign_lin(tt) != 0: t2["fail"] += 1
    ha = Hterms(a)
    if ha and (sign_lin(ha) < 0 or sign_lin([(F(T1), 2)] + neg(ha)) < 0): t2["bound_fail"] += 1
res["T2"] = t2; print(t2)
# T3
t3 = dict(events=0, qualify_after=0, fall_to_zero=0, examples=[], Hbefore_values=set())
for T, ms, st in events(3, 5):
    if T != 5 or not any(e for e, n in st.values()): continue
    t3["events"] += 1
    a = step(st, 3, {2})
    if not any(e for e, n in a.values()): continue
    t3["qualify_after"] += 1
    hb, ha = Hterms(st), Hterms(a)
    if all(n == 1 for c, n in ha) and any(n > 1 for c, n in hb):
        t3["fall_to_zero"] += 1; h = round(Hf(st, WS["sq"]), 6); t3["Hbefore_values"].add(h)
        if abs(h - 0.462) < 1e-3 and len(t3["examples"]) < 2: t3["examples"].append({"masks": ms, "state": sorted(st.items()), "after": sorted(a.items()), "H_before": Hf(st, WS["sq"])})
t3["Hbefore_values"] = sorted(t3["Hbefore_values"])
res["T3"] = t3; print(t3)
json.dump(res, open("result_t5_run1.json", "x"), indent=1, default=str)
