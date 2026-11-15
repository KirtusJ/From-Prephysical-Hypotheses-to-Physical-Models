"""Winding offsets of the walks of a position product event at one vertex of a ring.

Setting (G10, subsection "Four arc gains"): two-rail digraph of the ring Z_N, walks from (0,R),
a right step from either rail of x goes to (x+1,R), a left step to (x-1,L). A position product
event of length T is the set of all walks whose site after s steps lies in A_s, s = 1..T.
For a walk w, lam(w) is its number of left steps; M = N/gcd(N,2). For an event S, a vertex y and
an integer l, n(l) is the number of walks of S that end at y with lam = l.

PREDICATES, fixed before the first run (15 November 2026). For every event, length and vertex examined:
 P1  all l with n(l) > 0 are congruent modulo M.
 P2  no gap: if n(l) > 0 and n(l') > 0 with l < l', l' - l a multiple of M, then n(l + M) > 0.
 P3  n(l+M) * (n(l+M) - 1) >= n(l) * n(l+2M) for every l.
 P4  n(l+M) * n(l'-M) >= n(l) * n(l') for all l, l' with l' - l a multiple of M and l' - l >= 2M.
 P5  coverage, reported and not a pass/fail matter except that it must not be zero: the number of
     vertices examined at which three or more values of l occur (so that P2 to P4 are not vacuous),
     per N.
Conventions: N = 1 and N = 2 are included; there both steps lead to the same site (N = 1) or the
two neighbours coincide (N = 2), and a walk is its sequence of step directions.
Parts: EXHAUSTIVE over every sequence of masks (non-empty subsets of sites) for the (N, T) pairs
listed in EXH; RANDOM with seed 20261115 for the (N, trials) listed in RND, each trial a random
length up to 6N and independent masks of density 0.3, 0.5, 0.7 or 0.9.
Usage: python3 winding_offsets.py RESULT.json   (refuses to overwrite). No other argument.
"""
import sys, os, json, random, collections, itertools
EXH = [(1, 10), (2, 8), (3, 7), (4, 5), (5, 4)]
RND = [(3, 4000), (4, 4000), (5, 4000), (6, 4000), (7, 4000), (8, 4000), (9, 2000), (10, 2000), (12, 2000), (14, 1000)]
def step(st, N, mask):
    new = collections.Counter()
    for (x, r, l), c in st.items():
        y = (x + 1) % N
        if y in mask: new[(y, 0, l)] += c
        y = (x - 1) % N
        if y in mask: new[(y, 1, l + 1)] += c
    return new
class Tally:
    def __init__(s): s.v = collections.Counter(); s.fail = {k: 0 for k in ("P1", "P2", "P3", "P4")}; s.first = {}
    def check(s, st, N):
        M = N // 2 if N % 2 == 0 else N
        d = collections.defaultdict(dict)
        for (x, r, l), c in st.items(): d[(x, r)][l] = c
        for v, n in d.items():
            s.v[(N, "vertices")] += 1
            ls = sorted(n)
            if len(ls) >= 3: s.v[(N, "three_or_more")] += 1
            if any((l - ls[0]) % M for l in ls):
                s.fail["P1"] += 1; s.first.setdefault("P1", [N, n]); continue
            g = lambda l: n.get(l, 0)
            for l in range(ls[0], ls[-1] + 1, M):
                if g(l) == 0: s.fail["P2"] += 1; s.first.setdefault("P2", [N, n])
                if g(l + M) * (g(l + M) - 1) < g(l) * g(l + 2 * M): s.fail["P3"] += 1; s.first.setdefault("P3", [N, n])
            for i, l in enumerate(ls):
                for l2 in ls[i + 1:]:
                    if l2 - l >= 2 * M and g(l + M) * g(l2 - M) < g(l) * g(l2): s.fail["P4"] += 1; s.first.setdefault("P4", [N, n])
def exhaustive(N, T, t):
    masks = [set(c) for k in range(1, N + 1) for c in itertools.combinations(range(N), k)]
    events = 0
    def rec(st, depth):
        nonlocal events
        if depth == T: return
        for m in masks:
            new = step(st, N, m)
            if not new: continue
            events += 1; t.check(new, N); rec(new, depth + 1)
    rec(collections.Counter({(0, 0, 0): 1}), 0)
    return events
def main():
    if len(sys.argv) != 2: sys.exit("usage: winding_offsets.py RESULT.json")
    out = sys.argv[1]
    if os.path.exists(out): sys.exit("refusing to overwrite " + out)
    t = Tally(); rep = {"program": "winding_offsets.py", "argv": sys.argv[1:], "seed": 20261115, "exhaustive": [], "random": []}
    for N, T in EXH:
        rep["exhaustive"].append({"N": N, "T": T, "nonempty_events": exhaustive(N, T, t)})
    rng = random.Random(20261115)
    for N, trials in RND:
        ev = 0
        for _ in range(trials):
            st = collections.Counter({(0, 0, 0): 1}); T = rng.randint(2, 6 * N); p = rng.choice([0.3, 0.5, 0.7, 0.9])
            for _s in range(T):
                st = step(st, N, {x for x in range(N) if rng.random() < p})
                if not st: break
                ev += 1; t.check(st, N)
        rep["random"].append({"N": N, "trials": trials, "nonempty_events": ev})
    Ns = sorted({k[0] for k in t.v})
    rep["P5_coverage"] = {str(N): {"vertices": t.v[(N, "vertices")], "three_or_more_values": t.v[(N, "three_or_more")]} for N in Ns}
    rep["failures"] = t.fail; rep["first_failing_case"] = {k: [v[0], sorted(v[1].items())] for k, v in t.first.items()}
    rep["predicates"] = {k: ("PASS" if t.fail[k] == 0 else "FAIL") for k in t.fail}
    rep["predicates"]["P5"] = "PASS" if all(t.v[(N, "three_or_more")] > 0 for N in Ns if N >= 3) else "FAIL"
    json.dump(rep, open(out, "x"), indent=1, sort_keys=True)
    print(json.dumps(rep["predicates"]), json.dumps(rep["P5_coverage"]))
if __name__ == "__main__": main()
