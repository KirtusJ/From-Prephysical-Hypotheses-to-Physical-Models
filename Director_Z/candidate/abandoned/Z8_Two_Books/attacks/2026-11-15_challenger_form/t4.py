"""Target 4: sharp start, free running. Command: python3 t4.py   (no randomness)
PREDICATES fixed before the first run. Carriers: rings N = 1..12 and the line; steps T = 0 -> 240.
 E1 exact: the step T -> T+1 has zero increment iff every site carrying chance has n_R = 0 or n_L = 0 (equality case of T-1,
    tested exactly in t1.py); count the zero steps and list the T at which they occur.
 E2 numeric (Decimal, 60 digits): H(T+1) - H(T) for every step; smallest increment over T >= 2 and where; no increment
    below -1e-40; an increment with |.| < 1e-40 must be an E1 zero step and conversely.
 E3 recorded: T log 2 - H(T) at T = 8, 32, 64 on the line (FORM quotes 2.908, 7.381, 12.791)."""
import json
from decimal import Decimal, getcontext
from lib import step
getcontext().prec = 60
LN = {}
def ln(n):
    if n not in LN: LN[n] = Decimal(n).ln()
    return LN[n]
def H(st):
    W = sum(e * e for e, n in st.values())
    return sum(Decimal(e * e) * ln(n) for e, n in st.values() if e) / Decimal(W)
def eq(st):
    d = {}
    for (x, s), (e, n) in st.items(): d.setdefault(x, {})[s] = (e, n)
    return all(not ((r.get(0, (0, 0))[0] or r.get(1, (0, 0))[0]) and r.get(0, (0, 0))[1] and r.get(1, (0, 0))[1]) for r in d.values())
res = {"command": "python3 t4.py", "steps": 240, "carriers": {}}
for N in list(range(1, 13)) + [None]:
    st = {(0, 0): (1, 1)}; h = H(st); zeros = []; incs = []; mism = 0; LN.clear(); gaps = {}
    for T in range(240):
        z = eq(st); st = step(st, N); h2 = H(st); d = h2 - h
        if z: zeros.append(T)
        if (abs(d) < Decimal("1e-40")) != z: mism += 1
        incs.append(d); h = h2
        if T + 1 in (8, 32, 64, 240): gaps[T + 1] = str((Decimal(T + 1) * ln(2) - h).quantize(Decimal("1e-6")))
    late = [(d, T) for T, d in enumerate(incs) if T >= 2]
    mn = min(late)
    name = "line" if N is None else "ring%d" % N
    res["carriers"][name] = {"zero_steps_T_to_T+1": zeros, "E1_E2_mismatch": mism, "negative_increments": sum(1 for d in incs if d < Decimal("-1e-40")),
        "min_increment_T>=2": str(mn[0].quantize(Decimal("1e-30"))), "at_T": mn[1], "min_last_100": str(min(incs[140:]).quantize(Decimal("1e-30"))),
        "H240": str(h.quantize(Decimal("1e-20"))), "Tlog2_minus_H": gaps, "increments": [str(d.quantize(Decimal("1e-25"))) for d in incs]}
    print(name, {k: v for k, v in res["carriers"][name].items() if k != "increments"}, flush=True)
json.dump(res, open("result_t4_run1.json", "x"), indent=1)
