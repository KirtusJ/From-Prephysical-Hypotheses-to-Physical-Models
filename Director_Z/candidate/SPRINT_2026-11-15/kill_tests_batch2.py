"""Kill tests KZ7 and KZ8 of the candidate sprint (second batch). Predicates as fixed in 00_PLAN.md before this
program was written. Signed carrier: gain -1 on a left step that follows a left step; walks from (0,R).
Usage: python3 kill_tests_batch2.py RESULT.json  (refuses to overwrite). Seed 20261115."""
import sys, os, json, random, collections
from fractions import Fraction as Fr
from decimal import Decimal, getcontext
getcontext().prec = 60
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def stepf(st, N, mask=None):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in (((x + 1) if N is None else (x + 1) % N, 0, 1), ((x - 1) if N is None else (x - 1) % N, 1, -1 if r == 1 else 1)):
            if mask is not None and y not in mask: continue
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    return new
def H(st, T):
    tot = sum(sg * sg for sg, n in st.values())
    h = Decimal(0)
    for sg, n in st.values():
        if sg: h += (Decimal(sg * sg) / Decimal(tot)) * Decimal(n).ln()
    return h
rep = {"argv": sys.argv[1:]}
# KZ7
z7 = []
for name, N in (("line", None), ("ring16", 16), ("ring18", 18)):
    st = {(0, 0): (1, 1)}; prev = None; first = None; series = []
    for T in range(1, 61):
        st = stepf(st, N); dark = sum(1 for sg, n in st.values() if sg == 0 and n > 0); series.append(dark)
        if prev is not None and dark < prev and first is None: first = [T - 1, prev, T, dark]
        prev = dark
    z7.append({"carrier": name, "dark_counts_T1_to_60": series, "first_decrease": first})
rep["KZ7"] = {"carriers": z7, "predicate": all(c["first_decrease"] is None for c in z7)}
rep["KZ7"]["verdict"] = "STANDS" if rep["KZ7"]["predicate"] else "KILLED"
# KZ8
z8a = []
for name, N in (("line", None), ("ring16", 16), ("ring18", 18)):
    st = {(0, 0): (1, 1)}; prev = None; first = None; series = []
    for T in range(1, 81):
        st = stepf(st, N); h = H(st, T); series.append(str(h)[:22])
        if prev is not None and h < prev - Decimal(10) ** -40 and first is None: first = [T - 1, str(prev)[:30], T, str(h)[:30]]
        prev = h
    z8a.append({"carrier": name, "H_T1_to_80": series, "first_decrease": first})
rng = random.Random(20261115); z8b_fail = 0; z8b_events = 0; z8b_first = None
for _ in range(200):
    N = 16; T0 = rng.randint(4, 16); p = rng.uniform(0.5, 0.9)
    st = {(0, 0): (1, 1)}; ok = True
    for t in range(T0):
        st = stepf(st, N, {x for x in range(N) if rng.random() < p})
        if not st or all(sg == 0 for sg, n in st.values()): ok = False; break
    if not ok: continue
    z8b_events += 1; prev = H(st, T0)
    for k in range(12):
        st = stepf(st, N); h = H(st, T0 + k + 1)
        if h < prev - Decimal(10) ** -40:
            z8b_fail += 1
            if z8b_first is None: z8b_first = {"prepared_length": T0, "free_step": k + 1, "H_before": str(prev)[:30], "H_after": str(h)[:30]}
            break
        prev = h
rep["KZ8"] = {"a": z8a, "b_events": z8b_events, "b_events_with_a_decrease": z8b_fail, "b_first": z8b_first,
              "predicate": all(c["first_decrease"] is None for c in z8a) and z8b_fail == 0}
rep["KZ8"]["verdict"] = "STANDS" if rep["KZ8"]["predicate"] else "KILLED"
json.dump(rep, open(OUT, "x"), indent=1)
print(rep["KZ7"]["verdict"], [(c["carrier"], c["first_decrease"], c["dark_counts_T1_to_60"][:14]) for c in z7])
print(rep["KZ8"]["verdict"], [(c["carrier"], c["first_decrease"]) for c in z8a], z8b_events, z8b_fail, z8b_first)
print([c["H_T1_to_80"][:8] for c in z8a][:1])
