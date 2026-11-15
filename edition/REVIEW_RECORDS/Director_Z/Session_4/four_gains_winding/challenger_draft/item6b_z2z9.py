#!/usr/bin/env python3
"""Item 6(b), second claim: 'On the ring of 3 sites with gains in Z_2 x Z_9 (s=3) [the function
|sum_w u^lambda(w) psi(w)|^2] is a function of the multiset of gains on every event of length at most 8 and not
at length 9'. The draft does not name the gains; this program scans carriers. Reviewer's own program.

Usage: python3 item6b_z2z9.py <seed> <outfile> <n_sample> <Tmax>

Ring N=3 (M=3). Gains (a,b,c,d) in Z_2 x Z_9, additive. delta=a+d-b-c, beta=3(b+c-2a), s as in the draft.
HYPOTHESIS per carrier: s == 3 and ord(delta) even (so that psi with psi(delta)=-1 exists). Number qualifying reported.
For generic unit u (u of infinite order) the value on a set of walks at a vertex is determined by the multiset of
(gain, lambda) up to a common shift of lambda, and on two walks it is 2+2Re(u^{l1-l2} psi(g1) conj psi(g2)).
Criterion used (two-walk events, which are events; necessary for 'every event', and sufficient because consistent
pairwise differences determine the whole sum): pooled over all lengths T <= T0 and all vertices of one rail,
 for ordered pairs of distinct walks at one vertex at one length with gains g1 != g2 the difference l1-l2 is a
 function of (g1,g2), and for g1 == g2 the difference is 0.
 Variant A: separately for rail R and rail L (F_R, F_L unrelated). Variant B: one table for both rails.
PREDICATE Z1 (the draft's sentence, per qualifying carrier): first failing T0 == 9 (variant A).
PREDICATE Z1B: the same in variant B.
Recorded: histogram of first failing T0 (None = no failure up to Tmax) over the qualifying carriers sampled.
"""
import sys, random, itertools, json
from collections import defaultdict, Counter

def main():
    seed = int(sys.argv[1]); outfile = sys.argv[2]; ns = int(sys.argv[3]); Tmax = int(sys.argv[4])
    out = open(outfile, 'x'); out.write(json.dumps({"cmd": " ".join(sys.argv)}) + "\n")
    rng = random.Random(seed)
    mods = (2, 9); N = 3; M = 3
    els = list(itertools.product(range(2), range(9)))
    add = lambda x, y: ((x[0] + y[0]) % 2, (x[1] + y[1]) % 9)
    mul = lambda n, x: ((n * x[0]) % 2, (n * x[1]) % 9)
    neg = lambda x: mul(-1, x)
    # walk types per length: (site, rail, lam, nRR, nRL, nLR, nLL) with multiplicity
    types = {}
    for T in range(1, Tmax + 1):
        cnt = Counter()
        for w in itertools.product((0, 1), repeat=T):
            rail = 0; n = [0, 0, 0, 0]
            for st in w:
                n[2 * rail + st] += 1; rail = st
            lam = sum(w)
            cnt[((T - 2 * lam) % N, rail, lam, tuple(n))] += 1
        types[T] = cnt
    quals = []
    for a, b, c, d in itertools.product(els, repeat=4):
        delta = add(add(a, d), neg(add(b, c))); beta = mul(3, add(add(b, c), neg(mul(2, a))))
        D = set(); x = (0, 0)
        while True:
            D.add(x); x = add(x, delta)
            if x == (0, 0): break
        s = 1
        while mul(s, beta) not in D: s += 1
        if s == 3 and len(D) % 2 == 0: quals.append((a, b, c, d))
    out.write(json.dumps({"carriers_enumerated": len(els) ** 4, "qualifying_s3_r_even": len(quals)}) + "\n")
    sample = quals if ns >= len(quals) else rng.sample(quals, ns)
    histA = Counter(); histB = Counter(); examples = {}
    for (a, b, c, d) in sample:
        tabA = {}; tabB = {}; failA = None; failB = None
        for T in range(1, Tmax + 1):
            byv = defaultdict(list)
            for (site, rail, lam, n), mult in types[T].items():
                g = add(add(mul(n[0], a), mul(n[1], b)), add(mul(n[2], c), mul(n[3], d)))
                byv[(site, rail)].append((g, lam, mult))
            for (site, rail), lst in byv.items():
                for i, (g1, l1, m1) in enumerate(lst):
                    for j, (g2, l2, m2) in enumerate(lst):
                        if i == j and m1 < 2: continue
                        dl = l1 - l2
                        for tab, key, which in ((tabA, (rail, g1, g2), 'A'), (tabB, (g1, g2), 'B')):
                            want = tab.setdefault(key, dl)
                            ok = (want == dl) and not (g1 == g2 and dl != 0)
                            if not ok:
                                if which == 'A' and failA is None:
                                    failA = T; examples.setdefault(("A", T), [str((a, b, c, d)), rail, g1, g2, want, dl])
                                if which == 'B' and failB is None:
                                    failB = T; examples.setdefault(("B", T), [str((a, b, c, d)), rail, g1, g2, want, dl])
            if failA is not None and failB is not None: break
        histA[str(failA)] += 1; histB[str(failB)] += 1
    res = {"sampled": len(sample), "first_fail_hist_variantA": dict(histA), "first_fail_hist_variantB": dict(histB),
           "Z1_holds_for": histA.get("9", 0), "Z1B_holds_for": histB.get("9", 0),
           "examples": {str(k): v for k, v in examples.items()}}
    out.write(json.dumps(res) + "\n"); out.close()
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
