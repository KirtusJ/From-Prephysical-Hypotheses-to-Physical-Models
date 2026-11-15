#!/usr/bin/env python3
"""Lemma W' against exact enumeration.  Seed 20261113 (used only if a layer exceeds CAP).

Usage: python3 -B check_wprime.py OUTFILE B CAP     (OUTFILE opened with mode 'x')

Uses bfs/site_view of explore.py (q=1, site totals <= B, rings N=3,4,5,6).
PREDICATES (fixed before the first run).
PW1 (claimed, Lemma W'): at every vertex of every site profile seen, for every l with n(l)>0, n(l+2M)>0 and
    (n(l)==1 or n(l+2M)==1):  n(l)*n(l+2M) <= C(n(l+M),2).   Hypothesis counted: such (profile, vertex, l).
PW2 (no claim; is the hypothesis 'an outer level is single' needed?): the same inequality for n(l)>=2 and
    n(l+2M)>=2.  Instances and violations recorded with the profiles.
PW3 (no claim): one-vertex profiles (other rail empty) of total <= B allowed by lem:winding and by W' but not seen,
    per ring, listed.
"""
import sys, json, random, itertools
from collections import defaultdict
from math import comb
import explore as E

def main():
    out = open(sys.argv[1], 'x'); B, CAP = int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(20261113)
    res = {'command_line': ' '.join(['python3', '-B'] + sys.argv), 'seed': 20261113, 'rings': {}}
    def lem_ok(t):
        n = dict(enumerate(t))
        for l in n:
            for l2 in n:
                if l2 - l >= 2 and n[l] * n[l2] > n.get(l + 1, 0) * n.get(l2 - 1, 0): return False
                if l2 - l == 2 and n[l] * n[l2] > n[l + 1] * (n[l + 1] - 1): return False
        return True
    def wp_ok(t):
        return all(not (min(t[i], t[i + 2]) == 1 and t[i] * t[i + 2] > comb(t[i + 1], 2)) for i in range(len(t) - 2))
    cands = set()
    for L in range(1, 6):
        for t in itertools.product(range(1, B + 1), repeat=L):
            if sum(t) <= B and lem_ok(t): cands.add(t)
    for N in (3, 4, 5, 6):
        profs = set()
        def visit(N_, st):
            for s, items in E.site_view(N_, st).items():
                nR = defaultdict(int); nL = defaultdict(int)
                for rail, e, lev, c in items: (nL if rail else nR)[lev] += c
                profs.add((tuple(sorted(nR.items())), tuple(sorted(nL.items()))))
        info = E.bfs(N, 1, B, CAP, 4 * N + 8, rng, visit)
        r = {'bfs_exhaustive_to': info['exhaustive_to'], 'closed': info['layers'][-1][1] == 0 and not info['layers'][-1][2],
             'profiles': len(profs), 'PW1_inst': 0, 'PW1_fail': [], 'PW2_inst': 0, 'PW2_viol': []}
        single = set()
        for p in profs:
            for side in (0, 1):
                n = dict(p[side])
                if n and not p[1 - side]:
                    lo = min(n); single.add(tuple(n.get(lo + i, 0) for i in range(max(n) - lo + 1)))
                for l in n:
                    if l + 2 in n:
                        ok = n[l] * n[l + 2] <= comb(n.get(l + 1, 0), 2)
                        if min(n[l], n[l + 2]) == 1:
                            r['PW1_inst'] += 1
                            if not ok: r['PW1_fail'].append(str(p))
                        else:
                            r['PW2_inst'] += 1
                            if not ok: r['PW2_viol'].append(str(p))
        r['one_vertex_seen'] = sorted(map(str, single))
        r['one_vertex_lemma_allowed'] = len(cands)
        r['one_vertex_allowed_by_lemma_and_Wprime_not_seen'] = sorted(str(t) for t in cands if wp_ok(t) and t not in single)
        r['one_vertex_excluded_by_Wprime_only'] = sorted(str(t) for t in cands if not wp_ok(t))
        r['seen_not_allowed'] = sorted(str(t) for t in single if t not in cands or not wp_ok(t))
        res['rings'][str(N)] = r
        print(N, {k: (v if not isinstance(v, list) or len(v) < 30 else v[:30]) for k, v in r.items() if k != 'one_vertex_seen'}, flush=True)
    json.dump(res, out, indent=1, sort_keys=True); out.close()
main()
