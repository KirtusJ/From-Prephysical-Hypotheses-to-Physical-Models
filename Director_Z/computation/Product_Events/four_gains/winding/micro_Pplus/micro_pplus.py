"""Micro-review of property P+ for Director G's one-gain preparation on rings.

Predicates (fixed before first run):
 H  hypothesis: own census at the end equals requested multisets U on (x,R), V on (x,L), nothing elsewhere.
 P1 at target site, per rail, the set of left-step counts has at most one value.
 P2 over both rails together the set has at most one value (P+).
 C  control: word RLLRR from rail R has 2 left steps, 1 left-after-left.
Masks come from Director_G prepare(); propagation is this file's own.
Run: python3 -B micro_pplus.py NEW_RESULT_FILE
"""
import sys, json
from collections import Counter
from itertools import combinations_with_replacement, product
from math import gcd
sys.path.insert(0, "/home/user/From-Prephysical-Hypotheses-to-Physical-Models/Director_G")
sys.dont_write_bytecode = True
from check_one_gain_preparation import prepare

def control(word="RLLRR"):
    prev, l, ll = "R", 0, 0
    for s in word:
        l += s == "L"; ll += (s == "L" and prev == "L"); prev = s
    return l, ll

def propagate(q, masks, N):
    st = Counter({(0, "R", 0, 0): 1})
    for m in masks:
        nx = Counter()
        for (x, rail, g, nl), c in st.items():
            y = (x + 1) % N
            if y in m: nx[y, "R", g, nl] += c
            y = (x - 1) % N
            if y in m: nx[y, "L", (g + (rail == "L")) % q, nl + 1] += c
        st = nx
    return st

out = open(sys.argv[1], "x")
ctl = control()
out.write(json.dumps({"control_RLLRR": ctl}) + "\n")
runs = qual = multi = rl_differ = errors = 0
first = None
for N in (7, 9, 11, 12, 13, 14, 16, 24):
    M = N // gcd(N, 2)
    for q in (1, 2, 3, 4):
        kmax = 2 if q <= 3 else 1
        ch = [v for k in range(kmax + 1) for v in combinations_with_replacement(range(q), k)]
        for U, V, x, matched in product(ch, ch, (0, 1, N - 1), (False, True)):
            runs += 1
            try:
                masks, rec = prepare(q, list(U), list(V), x, N, matched)
            except Exception as e:
                errors += 1
                out.write(json.dumps(dict(N=N, q=q, U=U, V=V, x=x, matched=matched, error=repr(e))) + "\n")
                continue
            st = propagate(q, masks, N)
            gains = Counter(); lefts = {"R": set(), "L": set()}; elsewhere = 0
            for (y, rail, g, nl), c in st.items():
                if y == x:
                    gains[rail, g] += c; lefts[rail].add(nl)
                else: elsewhere += c
            want = Counter([("R", g) for g in U] + [("L", g) for g in V])
            ok = gains == want and elsewhere == 0
            qual += ok
            allv = lefts["R"] | lefts["L"]
            T = len(masks)
            row = dict(N=N, M=M, q=q, U=U, V=V, x=x, matched=matched, ticks=T, qualifies=ok,
                       elsewhere=elsewhere, lefts_R=sorted(lefts["R"]), lefts_L=sorted(lefts["L"]),
                       lifted_end=sorted(T - 2 * n for n in allv),
                       P1=len(lefts["R"]) <= 1 and len(lefts["L"]) <= 1, P2=len(allv) <= 1)
            if len(allv) > 1:
                multi += 1
                if lefts["R"] and lefts["L"] and len(lefts["R"]) == 1 and len(lefts["L"]) == 1: rl_differ += 1
                if first is None:
                    first = dict(row, masks=[sorted(m) for m in masks], receipt=rec)
            out.write(json.dumps(row) + "\n")
summary = dict(runs=runs, qualifying=qual, errors=errors, multi_value=multi,
               multi_only_R_vs_L=rl_differ, first_multi=first, control=ctl)
out.write(json.dumps({"summary": summary}) + "\n"); out.close()
print(json.dumps(summary))
