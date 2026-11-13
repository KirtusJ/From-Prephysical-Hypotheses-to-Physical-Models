#!/usr/bin/env python3
"""ev_extra.py -- explicit rules outside the model's classification under weakened demands (Z1-R,
records vertex, symbol gain, mode uni = one function per rail, unwrapped ring).

A 'full arrival multiset' is the multiset of gains of ALL walks of one length ending at one vertex;
the end-vertex distribution P_t(y) of a rule is F_y(full arrival multiset at y)/2^t.
usage: ev_extra.py OUT family T Lmax

PREDICATES fixed before the first run (for family a = end-vertex events, T=7, Lmax=5):
 X1 the projection of V_a(7) onto the full arrival multisets of lengths <= 5 has dimension > 2
    (the model's is 2: count, square): end-vertex consistency does not force the end-vertex distribution.
 X2 there is a rule F = square + eps*delta, eps > 0, with delta = 0 on one-walk multisets (S4: a single
    walk has weight one), F >= 0 on every multiset occurring up to length T+1, satisfying every
    consistency equation of the family up to T, whose end-vertex distribution at some length <= 5
    differs from the model's. If found it is printed with its distribution.
The same program is run for other families as measurements without predicates.
Result file not overwritten.
"""
import sys, os, json, itertools
from fractions import Fraction
from collections import Counter
import flint
import ev_classify as E, ev_compare as C
HERE = os.path.dirname(os.path.abspath(__file__))
def main():
    out = os.path.join(HERE, sys.argv[1]); fam = sys.argv[2]; T = int(sys.argv[3]); Lmax = int(sys.argv[4])
    if os.path.exists(out): sys.exit('result file exists, not overwritten: ' + out)
    D = E.walk_data(T + 1, None)
    S, NS = C.space(D, fam, 'vertex', 'gain', 'uni', T)
    rows = list(S.rows); n = len(S.unk)
    # full arrival multisets by length
    arr = {}
    for t in range(0, T + 2):
        d = {}
        for xs, rs, g in D[t]:
            d.setdefault((xs[t], rs[t]), Counter())[g] += 1
        arr[t] = d
    def uid(y, cnt): return S.unk.get(((y[1],), tuple(sorted(cnt.items(), key=repr))))
    fa = sorted({uid(y, c) for t in range(0, Lmax + 1) for y, c in arr[t].items() if uid(y, c) is not None})
    missing = sum(1 for t in range(0, Lmax + 1) for y, c in arr[t].items() if uid(y, c) is None)
    sq, cn = S.vec('square'), S.vec('count')
    R = dict(family=fam, T=T, Lmax=Lmax, unknowns=n, dim_family=len(NS),
             full_arrival_unknowns=len(fa), full_arrival_missing=missing,
             dim_on_full_arrival=E.rank_of(NS, fa), model_on_full_arrival=E.rank_of([sq, cn], fa))
    R['X1'] = R['dim_on_full_arrival'] > 2
    # X2: delta in V_fam, zero on singletons
    single = [j for (rk, ms), j in S.unk.items() if sum(c for g, c in ms) == 1]
    # subspace of V_fam vanishing on singletons: solve c^T NS[single] = 0
    M = flint.fmpz_mat([[v[j] for j in single] for v in NS])       # k x |single|
    Kt, kd = M.transpose().nullspace()                               # columns: combos c with sum_c c_i v_i = 0 on singles
    W = []
    for a in range(kd):
        c = [int(Kt[i, a]) for i in range(len(NS))]
        W.append([sum(c[i] * NS[i][j] for i in range(len(NS))) for j in range(n)])
    zero = [j for j in range(n) if sq[j] == 0]
    found = None
    cands = []
    for w in W:
        cands += [w, [-x for x in w]]
    for a, b in itertools.combinations(range(len(W)), 2):
        for sa in (1, -1):
            for sb in (1, -1):
                cands.append([sa * x + sb * y for x, y in zip(W[a], W[b])])
    for w in cands:
        if any(w[j] < 0 for j in zero): continue
        if not any(w[j] for j in fa): continue
        if not E.satisfies(rows, w): continue
        neg = [Fraction(sq[j], -w[j]) for j in range(n) if w[j] < 0]
        eps = (min(neg) / 2) if neg else Fraction(1)
        F = [sq[j] + eps * w[j] for j in range(n)]
        assert all(f >= 0 for f in F) and all(F[j] == 1 for j in single)
        assert all(sum(F[j] * c for j, c in r) == 0 for r in rows)
        dist = {}
        for t in range(1, Lmax + 1):
            dd = {}
            for y, c in sorted(arr[t].items()):
                j = uid(y, c)
                dd['%d%s' % y] = dict(model=str(Fraction(sq[j], 2 ** t)), rule=str(Fraction(F[j], 2 ** t)))
            if any(v['model'] != v['rule'] for v in dd.values()):
                dist[t] = dd
        inv = {j: u for u, j in S.unk.items()}
        found = dict(eps=str(eps), delta={repr(inv[j]): w[j] for j in range(n) if w[j] and S.level[j] <= Lmax},
                     delta_nonzero_total=sum(1 for x in w if x), equations_checked=len(rows),
                     distributions_that_differ=dist)
        break
    R['X2'] = found is not None
    R['rule'] = found
    R['dim_vanishing_on_single_walks'] = len(W)
    print(json.dumps(R, indent=1))
    with open(out, 'x') as f: json.dump(R, f, indent=1)
if __name__ == '__main__': main()
