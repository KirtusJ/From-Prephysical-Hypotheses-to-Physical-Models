"""Follow-up to KZ6(c) of the candidate sprint. The first run could test the fork only for even M (its carrier, with
gains in Z2 x Z4, has two classes with k even only for M = 2 mod 4). This program uses gains in Z2 x Z2
(a = 0, b = (0,1), c = 0, d = (1,1); delta = (1,0), B = (0,1), beta = B^M = (0,1) for odd M: two classes, k even)
on rings with odd M: N = 6, 10, 14 (M = 3, 5, 7) and odd N = 7, 9, 11 (M = N).
PREDICATE fixed before the run (15 November 2026): with the fork event (masks {t, -t} for t = 1..M, then all sites),
length M + 1, and the Odd Lap rule (eps_0 - eps_1)^2: the weight at the vertex (M+1 mod N, R) is 0 and the weight at
(M-1 mod N, L) is 4, for every ring listed; and no other vertex carries walks. With the other square,
(eps_0 + eps_1)^2, the two values are exchanged (reported for contrast).
Usage: python3 kill_test_z6_followup.py RESULT.json  (refuses to overwrite)."""
import sys, os, json, collections
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def add(g, h): return ((g[0] + h[0]) % 2, (g[1] + h[1]) % 2)
GA, GB, GC, GD = (0, 0), (0, 1), (0, 0), (1, 1)
rows = []; ok = True
for N in (6, 10, 14, 7, 9, 11):
    M = N // 2 if N % 2 == 0 else N
    masks = [{t % N, (-t) % N} for t in range(1, M + 1)] + [set(range(N))]
    st = collections.Counter({(0, 0, (0, 0), 0): 1})      # site, rail, gain, left steps
    for t in range(1, M + 2):
        new = collections.Counter()
        for (x, r, g, l), c in st.items():
            y = (x + 1) % N
            if y in masks[t - 1]: new[(y, 0, add(g, GA if r == 0 else GC), l)] += c
            y = (x - 1) % N
            if y in masks[t - 1]: new[(y, 1, add(g, GB if r == 0 else GD), l + 1)] += c
        st = new
    by = collections.defaultdict(list)
    for (x, r, g, l), c in st.items(): by[(x, r)].append((g, l, c))
    res = {}
    for v, items in by.items():
        lmin = min(l for _, l, _ in items); e = [0, 0]
        for g, l, c in items:
            assert (l - lmin) % M == 0
            e[((l - lmin) // M) % 2] += c * (-1) ** g[0]       # classes are the winding levels modulo 2
        res[v] = {"walks": sum(c for *_, c in items), "odd_lap": (e[0] - e[1]) ** 2, "even_lap": (e[0] + e[1]) ** 2}
    vr, vl = ((M + 1) % N, 0), ((M - 1) % N, 1)
    good = set(res) == {vr, vl} and res[vr]["odd_lap"] == 0 and res[vl]["odd_lap"] == 4
    ok &= good
    rows.append({"N": N, "M": M, "vertex_R": str(vr), "vertex_L": str(vl), "weights": {str(k): v for k, v in res.items()}, "predicate": good})
json.dump({"argv": sys.argv[1:], "rows": rows, "predicate_all": ok, "verdict_for_Z6": "STANDS" if ok else "KILLED"}, open(OUT, "x"), indent=1)
print("all" , ok); [print(r["N"], r["weights"], r["predicate"]) for r in rows]
