#!/usr/bin/env python3
"""ev_records.py -- attack on S3 (Z1-R): how the consistent rules depend on what the records are and
on what the rule may see. Consistency is demanded for ALL events (the model's S2), lengths 0..T,
computed by components (exact; see ev_compare.py). Configurations:
   vertex/gain      the model (records (x,rail), rule sees the gains)
   arc/gain         records (x, rail, previous rail) = (vertex, last arc)
   vertex/gainprev  records (x,rail), rule sees the multiset of pairs (gain, previous rail)
   pos/gain         records x only: T=4 by exhaustive enumeration in ev_classify.py (runs P8, M11, M14,
                    M20); not repeated here because at length 5 all 32 walks form one component.
Reported: exact dimension of the solution space; which closed forms are consistent; and, for each
depth L, I(L,T) = dimension of the projection onto the unknowns first occurring at length <= L, with
the rank there of the consistent model vectors (count, square if consistent, x*count in mode per).

PREDICATES fixed before the first run:
 U1 arc/gain, uni, T=5: the arc-indexed square is not consistent and I(L,5) = 1 for L <= 4 (count only).
 U2 vertex/gainprev, uni, T=5: I(L,5) = 2 for L <= 4: no rule beyond count and square appears.
 U3 vertex/gain, uni, T=5: I(L,5) = 2 for 3 <= L <= 4 (baseline).
 U4 vertex/gainprev: 'sqprev' (sum over previous rail of squared partial sums, i.e. the arc square
    read as a vertex rule) is not consistent; 'countprevR' (number of walks arriving from rail R) is not.
Result file not overwritten.
"""
import sys, os, json, time
import ev_classify as E, ev_compare as C
HERE = os.path.dirname(os.path.abspath(__file__))
def main():
    out = os.path.join(HERE, sys.argv[1])
    if os.path.exists(out): sys.exit('result file exists, not overwritten: ' + out)
    Tmax = int(sys.argv[2])
    res = []
    for N in (None, 3):
        D = E.walk_data(Tmax + 1, N)
        for rec, sym in (('vertex', 'gain'), ('arc', 'gain'), ('vertex', 'gainprev')):
            for mode in ('uni', 'per'):
                for T in range(3, Tmax + 1):
                    t0 = time.time()
                    S, NS = C.space(D, 'all', rec, sym, mode, T)
                    rows = list(S.rows)
                    names = ['count', 'square', 'n2', 'sum', 'occupied'] + (['xcount'] if mode == 'per' and N is None else []) \
                            + (['sqprev', 'crossprev', 'countprevR'] if sym == 'gainprev' else [])
                    ok = {nm: E.satisfies(rows, S.vec(nm)) for nm in names}
                    model = [S.vec(nm) for nm in ('count', 'square', 'xcount') if ok.get(nm)]
                    r = dict(N=N, records=rec, symbol=sym, mode=mode, T=T, equations=len(rows), unknowns=len(S.unk),
                             dim=len(NS), consistent=ok, interior={})
                    for L in range(1, T + 2):
                        sub = [j for j in range(len(S.unk)) if S.level[j] <= L]
                        r['interior'][str(L)] = dict(unknowns=len(sub), I=E.rank_of(NS, sub), model=E.rank_of(model, sub))
                    r['seconds'] = round(time.time() - t0, 1)
                    res.append(r)
                    print(N, rec, sym, mode, 'T', T, 'eq', len(rows), 'n', len(S.unk), 'dim', len(NS),
                          [k for k, v in ok.items() if v],
                          ' '.join('L%s:%d(m%d,u%d)' % (L, v['I'], v['model'], v['unknowns']) for L, v in r['interior'].items()),
                          r['seconds'], flush=True)
    with open(out, 'x') as f: json.dump(dict(results=res), f, indent=1)
if __name__ == '__main__': main()
