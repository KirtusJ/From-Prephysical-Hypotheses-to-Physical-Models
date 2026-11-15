"""Exhaustive BFS over position product events of D_delta (a=b=c=1, d=delta, ord delta=q) on Z_N.
Assumed definition: event = walks from (0,R) whose position at time t lies in mask A_t (nonempty subset of Z_N).
State = multiset of (site, rail, lambda - min lambda, gain - min-normalised gain mod q) with counts.
Symmetries used: (1) lambda translation: extension increments of lambda do not depend on prior lambda;
(2) common gain translation by delta^k: extension gains do not depend on prior gain, so a translated state
has translated futures and the target pattern is translation-invariant; normalise to lexicographically least.
PREDICATES (fixed before first run):
 P1 (target): no state at any length <= TMAX has a site with exactly two walks, one on R gain g, one on L gain g+1,
    same lambda. Reported as first length found or 'none'.
 P2 (control): same with L-R gain difference 0; report first length (expected to appear; else flag).
 P3 (control): same with difference 2 (= -1 mod 3); report first length.
 P4: peak memory under RLIMIT_AS 2 GB; layers fully exhausted to TMAX (report largest exhausted length).
Usage: python3 enum_pp.py N q TMAX outfile
"""
import sys, resource, itertools
resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
N, q, TMAX, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
f = open(out, 'x')
masks = [frozenset(s) for k in range(1, N+1) for s in itertools.combinations(range(N), k)]
def norm(d):
    if not d: return None
    lm = min(k[2] for k in d)
    best = None
    for s in range(q):
        t = tuple(sorted(((x, r, l-lm, (g+s) % q), c) for (x, r, l, g), c in d.items()))
        if best is None or t < best: best = t
    return best
def step(state, mask):
    d = {}
    for (x, r, l, g), c in state:
        for nx, nr, dl, dg in (((x+1) % N, 0, 0, 0), ((x-1) % N, 1, 1, 1 if r == 1 else 0)):
            if nx in mask:
                k = (nx, nr, l+dl, (g+dg) % q); d[k] = d.get(k, 0) + c
    return norm(d)
def check(state):
    found = set()
    by = {}
    for (x, r, l, g), c in state: by.setdefault(x, []).append((r, l, g, c))
    for x, w in by.items():
        if sum(c for *_, c in w) == 2 and len(w) == 2:
            w.sort()
            (r1, l1, g1, _), (r2, l2, g2, _) = w
            if r1 == 0 and r2 == 1 and l1 == l2: found.add((g2-g1) % q)
    return found
first = {}
layer = {((0, 0, 0, 0), 1),}
layer = {tuple(sorted(layer))}
seen_total = 0
for T in range(0, TMAX+1):
    for s in layer:
        for dg in check(s):
            if dg not in first: first[dg] = (T, s)
    seen_total += len(layer)
    f.write(f"T={T} states={len(layer)} maxrss_MB={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss//1024} first={ {k:v[0] for k,v in first.items()} }\n"); f.flush()
    if T == TMAX: break
    nl = set()
    for s in layer:
        for m in masks:
            n = step(s, m)
            if n is not None: nl.add(n)
    layer = nl
f.write(f"EXHAUSTED_TO={T}\n")
for k in sorted(first): f.write(f"diff={k} firstT={first[k][0]} example_state={first[k][1]}\n")
f.write("P1 " + ("FAIL" if 1 in first else "PASS") + "\n")
f.close()
