#!/usr/bin/env python3
"""Cross-check of Statement C without relaxation: all position product events on the actual ring
Z_N (N = 3 or 6), q = 3, deduplicated by their full state (site, rail, lambda - min, gain) up to a common
gain translation, layers bounded by T and states per layer by CAP.  PREDICATE (fixed before the run):
no event of length <= T has, at one site, exactly one walk on R and one on L with equal lambda and gain
exponents g, g+1 (mod 3).  Also reports the first length at which ({0},{0}) and ({0},{2}) appear (controls:
they are met by bfs_small.py).  Usage: m3_brute.py OUTFILE N T CAP"""
import sys, json
out, N, T, CAP = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
q = 3
def canon(st):
    if not st: return ()
    m = min(k[2] for k in st)
    return min(tuple(sorted((x, r, l - m, (g + k) % q, c) for (x, r, l, g), c in st.items())) for k in range(q))
seen = set(); layer = [{(0, 'R', 0, 0): 1}]; found = {}; complete = True; sizes = []
for t in range(1, T + 1):
    nxt = []
    for st in layer:
        cand = sorted({(x + 1) % N for (x, r, l, g) in st} | {(x - 1) % N for (x, r, l, g) in st})
        for bits in range(1, 1 << len(cand)):
            A = {cand[i] for i in range(len(cand)) if bits >> i & 1}
            new = {}
            for (x, r, l, g), c in st.items():
                for (y, r2, l2, g2) in (((x + 1) % N, 'R', l, g), ((x - 1) % N, 'L', l + 1, (g + (r == 'L')) % q)):
                    if y in A: new[(y, r2, l2, g2)] = new.get((y, r2, l2, g2), 0) + c
            if not new: continue
            # site contents
            by = {}
            for (y, r2, l2, g2), c in new.items(): by.setdefault(y, []).append((r2, l2, g2, c))
            for y, ws in by.items():
                if sum(w[3] for w in ws) == 2 and len({w[1] for w in ws}) == 1:
                    R = [w[2] for w in ws if w[0] == 'R' for _ in range(w[3])]
                    L = [w[2] for w in ws if w[0] == 'L' for _ in range(w[3])]
                    if len(R) == 1 and len(L) == 1:
                        d = (L[0] - R[0]) % q
                        found.setdefault(d, t)
            c = canon(new)
            if c in seen: continue
            seen.add(c); nxt.append(new)
    layer = nxt; sizes.append(len(layer))
    print(t, len(layer), found, flush=True)
    if len(layer) > CAP: complete = False; print('CAP hit'); break
res = dict(argv=sys.argv, layer_sizes=sizes, complete_to_T=complete, first_length_of_LminusR=found,
           predicate_no_diff1=(1 not in found))
open(out, 'x').write(json.dumps(res, indent=1)); print(res)
