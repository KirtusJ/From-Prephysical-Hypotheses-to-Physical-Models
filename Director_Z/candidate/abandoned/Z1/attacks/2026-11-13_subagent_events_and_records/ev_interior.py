#!/usr/bin/env python3
"""ev_interior.py -- second follow-up (Z1-R, records vertex, symbol gain; code of ev_classify/ev_compare).

Why: in ev_compare the explicit extra rules found at T=6 for b1 and bpos are supported on multisets of
the LAST length (T+1), which occur in few equations: a truncation effect. Here the comparison is made
in the interior. For a family, truncation T and depth L < T:
   I_fam(L,T) = dimension of the projection of V_fam(T) onto the family's unknowns first occurring at
                length <= L   (rules on the family's short events that extend, consistently on the
                family, up to length T+1),
   I_all(L,T) = the same for V_all(T) restricted to the family's unknowns,
   interior excess = I_fam - I_all >= 0,   model = rank of the model's vectors on those unknowns.
usage: ev_interior.py OUT Tmax families [modes]

PREDICATES fixed before the first run:
 R1 family b  (vertex product events): interior excess = 0 for every computed (L,T), L <= T-1.
 R2 family b2 (two reads): interior excess = 0 for every computed (L,T), L <= T-1.
 R3 families a, c, bs: interior excess > 0 at L = T-1 for the largest T computed, both modes.
 R4 family bpos: interior excess = 0 for L <= T-2 at the largest T computed. UNCERTAIN.
 R5 family b1: interior excess > 0 at L = T-1 for the largest T computed.
Result file not overwritten.
"""
import sys, os, json, time
import ev_classify as E, ev_compare as C
HERE = os.path.dirname(os.path.abspath(__file__))
def main():
    out = os.path.join(HERE, sys.argv[1])
    if os.path.exists(out): sys.exit('result file exists, not overwritten: ' + out)
    Tmax = int(sys.argv[2]); fams = sys.argv[3].split(',')
    modes = sys.argv[4].split(',') if len(sys.argv) > 4 else ['uni', 'per']
    Tmin = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    D = E.walk_data(Tmax + 1, None)
    res = []
    for mode in modes:
        for T in range(Tmin, Tmax + 1):
            SA, NA = C.space(D, 'all', 'vertex', 'gain', mode, T)
            for fam in fams:
                t0 = time.time()
                SF, NF = C.space(D, fam, 'vertex', 'gain', mode, T)
                idx = [SA.unk[u] for u in SF.unk]
                restr = [[v[i] for i in idx] for v in NA]
                rows = list(SF.rows)
                assert all(E.satisfies(rows, v) for v in restr)
                names = ['count', 'square'] + (['xcount'] if mode == 'per' else [])
                model = [SF.vec(nm) for nm in names]
                assert all(E.satisfies(rows, v) for v in model)
                r = dict(family=fam, mode=mode, T=T, events=SF.nevents, equations=len(rows), unknowns=len(SF.unk),
                         dim_family=len(NF), dim_all_restricted=E.rank_of(restr), interior={})
                for L in range(2, T + 2):
                    sub = [j for j in range(len(SF.unk)) if SF.level[j] <= L]
                    a, b, m = E.rank_of(NF, sub), E.rank_of(restr, sub), E.rank_of(model, sub)
                    r['interior'][str(L)] = dict(unknowns=len(sub), I_fam=a, I_all=b, excess=a - b, model=m)
                r['seconds'] = round(time.time() - t0, 1)
                res.append(r)
                print(fam, mode, 'T', T, 'ev', r['events'], 'n', r['unknowns'],
                      ' '.join('L%s:%d/%d/%d(m%d,u%d)' % (L, v['I_fam'], v['I_all'], v['excess'], v['model'], v['unknowns']) for L, v in r['interior'].items()),
                      r['seconds'], flush=True)
    with open(out, 'x') as f: json.dump(dict(results=res), f, indent=1)
if __name__ == '__main__': main()
