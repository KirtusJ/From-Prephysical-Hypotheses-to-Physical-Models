"""Scan of the author's stored JSON (read as data only). Run: python3 -I -B scan_stored_json.py STORED.json OWN_DIR
Checks fixed before running: per panel (1) on-site masses sum to 1, (2) radius-one masses sum to 1,
(3) on-site mass = tally^2/2^t in every row, (4) decoded bit = [y = h mod 2] and logical = y - b,
(5) blind squares sum to 2^t, routed squares sum to 2^t, (6) every row equals my own program's value
(field, both masses, blind), (7) list rows with tally 0 and radius-one mass != 0, (8) window covers all
ports my program populates, (9) negative or >1 masses."""
import json, sys, importlib.util
from fractions import Fraction as F
spec = importlib.util.spec_from_file_location("own", sys.argv[2] + "/own_parity_check.py")
own = importlib.util.module_from_spec(spec); spec.loader.exec_module(own)
d = json.load(open(sys.argv[1], encoding="utf8"))
print("top-level keys:", list(d)); print("columns:", d["columns"]); print("panels:", [p["native_ticks"] for p in d["panels"]])
A = own.routed_start(); B = own.tick({(0, 0): 1}); c = {"h0_undefined_events": 0}
m0 = {p: F(1, 2) for p in A}; m1 = dict(m0)
bad = {k: 0 for k in "sum0 sum1 born decode norm own window range".split()}
dark = []; rows = 0
for p in d["panels"]:
    t = p["native_ticks"]; h = t - 1
    assert p["timestamps_including_route_or_hold"] == t + 1
    recs = p["records"]; rows += len(recs)
    seen = set()
    s0 = s1 = F(0); nr = nb = 0
    for y, cc, b, x, a, on, nb1, bl in recs:
        on, nb1 = F(on), F(nb1); seen.add((y, cc))
        s0 += on; s1 += nb1; nr += a * a; nb += bl * bl
        if on != F(a * a, 2 ** t): bad["born"] += 1
        if b != int((y - h) % 2 == 0) or x != y - b: bad["decode"] += 1
        if not (0 <= on <= 1 and 0 <= nb1 <= 1): bad["range"] += 1
        if (A.get((y, cc), 0), m0.get((y, cc), 0), m1.get((y, cc), 0), B.get((y, cc), 0)) != (a, on, nb1, bl): bad["own"] += 1
        if a == 0 and nb1 != 0: dark.append((t, y, "RL"[cc], b, x, str(on), str(nb1)))
    bad["sum0"] += s0 != 1; bad["sum1"] += s1 != 1; bad["norm"] += (nr != 2 ** t) + (nb != 2 ** t)
    bad["window"] += len((set(A) | set(B) | set(m0) | set(m1)) - seen)
    m0 = own.marker_step(A, m0, 0, c); m1 = own.marker_step(A, m1, 1, c); A = own.tick(A); B = own.tick(B)
print("rows:", rows, "violations:", bad)
print("rows with routed tally 0 and radius-one mass != 0 (t, y, rail, b, x, onsite, radius1):")
for r in dark: print("  ", r)
print("t=4 rows at sites 0,1:", [r for r in d["panels"][3]["records"] if r[0] in (0, 1)])
print("t=3 rows at sites -1,0,1,2,3:", [r for r in d["panels"][2]["records"] if r[0] in (-1, 0, 1, 2, 3)])
print("first_run_correction:", d["first_run_correction"])
