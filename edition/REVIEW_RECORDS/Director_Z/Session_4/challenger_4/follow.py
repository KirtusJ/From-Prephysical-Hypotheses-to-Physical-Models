"""Follow-ups (predicates fixed before run):
F1: the single P7 failure of run_full.json (q0=12, T capped at 3): rerun with T up to 5. Predicate: dim on core
    equals pred_dim at T=4 or T=5 and is never below. If still above at T=5: counterexample candidate.
F2: non-faithful character test of prop:abund(c). C = Z2 x Z2 encoded as Z2xZ2, chi(a,b)=(-1)^a.
    Carrier: 2 vertices, arcs 0->0 (0,1), 0->1 (0,1), 1->0 (0,1), 1->1 (1,0).  Predicates: A*A=2; Dhat (8 vertices)
    strongly connected; r, r0; cor:vsl hypothesis (both values +1,-1 of chi occur on >=1000 walks to vertex 0 and
    to vertex 1 at one length).  Statement (c) predicts hypothesis <=> r==r0.
"""
import json, sys, re, math
from collections import deque
src = open('chal4.py').read()
src = src.split("results = []\n# 1.")[0].replace('OUT = sys.argv[1]\nif os.path.exists(OUT):\n    sys.exit("refuse to overwrite " + OUT)\n', '')
src = src.replace("Tmax = 5 if q0 <= 4 else (4 if q0 <= 8 else 3)", "Tmax = 5")
exec(src)
res = json.load(open('run_full.json'))
out = {}
bad = [r for r in res if r.get("H") and "P7" in r and not r["P7"]]
for r in bad:
    rr = analyse(r["n"], r["q"], [tuple(a) for a in r["arcs"]], r["d"], r["label"]+"-followup")
    print("F1", rr["label"], rr["r"], rr["r0"], rr["q0"], rr["pred_dim"], rr["dim_levels"], rr["P7"])
    out["F1"] = rr
# F2
V = 2; G = [(a, b) for a in range(2) for b in range(2)]
arcs = [(0, 0, (0, 1)), (0, 1, (0, 1)), (1, 0, (0, 1)), (1, 1, (1, 0))]
A = [[0, 0], [0, 0]]
for x, y, (a, b) in arcs: A[y][x] = (-1)**a
AsA = [[sum(A[k][i]*A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
idx = {(x, g): i for i, (x, g) in enumerate((x, g) for x in range(V) for g in G)}
hs = [[] for _ in idx]
for (x, g), i in idx.items():
    for xx, y, e in arcs:
        if xx == x: hs[i].append(idx[(y, ((g[0]+e[0]) % 2, (g[1]+e[1]) % 2))])
sc = strongly_connected(8, hs); r, _ = period_levels(8, hs)
r0, _ = period_levels(2, [[0, 1], [0, 1]])
cur = [0]*8; cur[idx[(0, (0, 0))]] = 1; hyp = False
for L in range(1, 60):
    nxt = [0]*8
    for a in range(8):
        for b in hs[a]: nxt[b] += cur[a]
    cur = nxt
    okL = True
    for y in range(2):
        for val in (0, 1):
            if sum(cur[idx[(y, (val, b))]] for b in range(2)) < 1000: okL = False
    hyp = hyp or okL
out["F2"] = {"AstarA": AsA, "hat_sc": sc, "r": r, "r0": r0, "cor_vsl_hypothesis": hyp, "c_predicts": r == r0, "P_c_holds": hyp == (r == r0)}
print("F2", out["F2"])
json.dump(out, open('follow.json', 'x'), indent=1)
