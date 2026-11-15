"""Director's attack on candidate Z8 "Two Books", weak point 2 (STIPULATED CANDIDATE FOR DISPROOF).
Question: is the mean entropy H a function of the state that the book of chance sees? The signed sums eps(v) at
all vertices at one length determine every chance now and after any further masks. If two position product events
of one length on one ring have the same eps at every vertex and different H, then H is not a function of that state.
PREDICATE fixed before the run (15 November 2026): on rings of 3 and 4 sites, among all sequences of non-empty masks
of length up to 5 (ring of 3) and 4 (ring of 4), there is NO pair of events of equal length with equal signed sums at
every vertex, non-zero weight, and different multisets of (signed sum, count) at the vertices of non-zero chance
(which is what H depends on). If such a pair exists the predicate FAILS and H is not a state function.
Usage: python3 state_function.py RESULT.json  (refuses to overwrite)."""
import sys, os, json, itertools, math
OUT = sys.argv[1]; assert not os.path.exists(OUT)
def stepf(st, N, mask):
    new = {}
    for (x, r), (sg, n) in st.items():
        for y, r2, flip in (((x + 1) % N, 0, 1), ((x - 1) % N, 1, -1 if r == 1 else 1)):
            if y not in mask: continue
            a, b = new.get((y, r2), (0, 0)); new[(y, r2)] = (a + sg * flip, b + n)
    return new
rep = {"argv": sys.argv[1:], "rings": []}; found_any = False
for N, Lmax in ((3, 5), (4, 4)):
    masks = [frozenset(c) for k in range(1, N + 1) for c in itertools.combinations(range(N), k)]
    seen = {}; first = None; pairs = 0; events = 0
    def rec(st, depth, hist):
        global first, pairs, events
        if depth and any(s for s, n in st.values()):
            events += 1
            key = (depth, tuple(sorted((v, s) for v, (s, n) in st.items() if s)))
            val = tuple(sorted((v, n) for v, (s, n) in st.items() if s))
            if key in seen and seen[key][0] != val:
                pairs += 1
                if first is None: first = {"length": depth, "signed_sums": [[list(v), s] for v, s in key[1]], "counts_A": [[list(v), n] for v, n in seen[key][0]], "masks_A": seen[key][1], "counts_B": [[list(v), n] for v, n in val], "masks_B": hist}
            seen.setdefault(key, (val, hist))
        if depth == Lmax: return
        for m in masks:
            nx = stepf(st, N, m)
            if nx: rec(nx, depth + 1, hist + [sorted(m)])
    rec({(0, 0): (1, 1)}, 0, [])
    if first:
        found_any = True
        def Hval(cnts, sums):
            tot = sum(s * s for _, s in sums); d = dict((tuple(v), n) for v, n in cnts)
            return sum((s * s / tot) * math.log(d[tuple(v)]) for v, s in sums)
        first["H_A"] = Hval(first["counts_A"], first["signed_sums"]); first["H_B"] = Hval(first["counts_B"], first["signed_sums"])
    rep["rings"].append({"N": N, "Lmax": Lmax, "events_of_nonzero_weight": events, "later_events_with_same_sums_and_other_counts": pairs, "first": first})
rep["predicate_no_such_pair"] = not found_any
json.dump(rep, open(OUT, "x"), indent=1); print(rep["predicate_no_such_pair"]); [print(r["N"], r["events_of_nonzero_weight"], r["later_events_with_same_sums_and_other_counts"], r["first"]) for r in rep["rings"]]
