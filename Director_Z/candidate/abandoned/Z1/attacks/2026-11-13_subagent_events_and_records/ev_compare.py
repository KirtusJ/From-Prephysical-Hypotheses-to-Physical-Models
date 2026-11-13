#!/usr/bin/env python3
"""ev_compare.py -- follow-up to ev_classify.py (same carrier Z1-R, same rule class, same code).

Why: ev_classify.py projected onto the unknowns of lengths <= 3; that yardstick does not discriminate
(only multisets of one or two walks occur there). Here the yardstick is the model's own demand at the
SAME truncation. For each T (events of lengths 0..T, continuations to T+1):
   V_all = exact space of rules consistent for EVERY event (S2 as stipulated),
   V_fam = exact space of rules consistent for the events of the family only,
both as functions on the multisets that occur in the family's equations (the family's unknowns U_fam).
V_all restricted to U_fam is contained in V_fam. Reported:
   dim V_fam, dim (V_all restricted to U_fam), excess = their difference,
   rank of the model's vectors (count, square, and x*count in mode 'per' unwrapped) on U_fam.
excess > 0 means: a rule consistent on all instrument events of the family up to length T+1 that is
not the restriction of any rule consistent on all events up to that length.
'all' at lengths >= 5 is computed by components: walks of one length are joined if they share a record
at that length or at the next; since F(empty)=0 the equation of an event is the sum of the equations
of its parts in the components, so all subsets of each component give the same solution space.

PREDICATES fixed before the first run:
 Q1 family b (vertex product events), records vertex, gain: excess = 0 at T=3 and T=4, modes uni and per.
 Q2 family a (end-vertex events): excess > 0 at T=5, both modes.
 Q3 family c (cylinders): excess > 0 at T=5, both modes.
 Q4 family b1 (one read): excess > 0 at T=5.
 Q5 family bpos (position product events): excess > 0 at T=5 (the last rail is not read).
 Q6 family bs (single-vertex reads): excess > 0 at T=5.
 Q7 family b2 (two reads): excess > 0 at T=5.
 Q8 family b at T=5 (if the family can be enumerated): excess = 0. UNCERTAIN.
Result file not overwritten. Explicit extra rules are written out for the families with excess > 0
(a basis vector of V_fam outside V_all, reduced modulo the model's vectors is not attempted; the
vector is given as it is, with the equation count it satisfies).
"""
import sys, os, json, time
import flint
import ev_classify as E

HERE = os.path.dirname(os.path.abspath(__file__))

def components(S, t):
    """masks of the components of walks of length t (shared record at t or at t+1)."""
    D = S.D
    n = 1 << t
    par = list(range(n))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    first = {}
    for i in range(n):
        ks = [('t', E.rec_key(D[t][i], t, S.rec)),
              ('u', E.rec_key(D[t + 1][i], t + 1, S.rec)),
              ('u', E.rec_key(D[t + 1][i | (1 << t)], t + 1, S.rec))]
        for k in ks:
            if k in first: par[find(i)] = find(first[k])
            else: first[k] = i
    comp = {}
    for i in range(n): comp.setdefault(find(i), []).append(i)
    return list(comp.values())

def add_all_by_components(S, t, cap=22):
    L, inv = S.classes(t)
    for comp in components(S, t):
        pass
        # enumerate count vectors over the classes inside the component (walks of one class are interchangeable)
        from collections import Counter
        cc = Counter(L[i] for i in comp)
        cl = list(cc)
        import itertools
        for counts in itertools.product(*[range(cc[c] + 1) for c in cl]):
            if not any(counts): continue
            S.nevents += 1
            at, at1 = {}, {}
            for c, n_ in zip(cl, counts):
                if not n_: continue
                k, s, k0, s0, k1, s1 = inv[c]
                at.setdefault(k, Counter())[s] += n_
                at1.setdefault(k0, Counter())[s0] += n_
                at1.setdefault(k1, Counter())[s1] += n_
            row = Counter()
            for k, cnt in at.items():  row[S.uidx(k, cnt, t)] -= 2
            for k, cnt in at1.items(): row[S.uidx(k, cnt, t + 1)] += 1
            row = {j: v for j, v in row.items() if v}
            if row: S.rows[frozenset(row.items())] = None

def space(D, fam, rec, sym, mode, T):
    S = E.System(D, rec, sym, mode)
    for t in range(T + 1):
        if fam == 'all': add_all_by_components(S, t)
        else: S.add_family(fam, t)
    NS = E.solve(list(S.rows), len(S.unk))
    return S, NS

def main():
    out = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'ev_compare_results.json')
    if os.path.exists(out): sys.exit('result file exists, not overwritten: ' + out)
    Tmax = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    fams = sys.argv[3].split(',') if len(sys.argv) > 3 else ['a', 'apos', 'b1', 'b1pos', 'b2', 'bs', 'c', 'bpos', 'b']
    Ns = [None] if len(sys.argv) <= 4 else [None if x == 'None' else int(x) for x in sys.argv[4].split(',')]
    results, extras = [], []
    for N in Ns:
        D = E.walk_data(Tmax + 1, N)
        for mode in ('uni', 'per'):
            for T in range(3, Tmax + 1):
                t0 = time.time()
                SA, NA = space(D, 'all', 'vertex', 'gain', mode, T)
                print('all', N, mode, T, 'unknowns', len(SA.unk), 'dim', len(NA), round(time.time() - t0, 1), flush=True)
                results.append(dict(family='all', N=N, mode=mode, T=T, events=SA.nevents, equations=len(SA.rows),
                                    unknowns=len(SA.unk), dim=len(NA)))
                for fam in fams:
                    if fam == 'b' and T > 5: continue
                    if fam == 'b2' and T > 5: continue
                    t0 = time.time()
                    try:
                        SF, NF = space(D, fam, 'vertex', 'gain', mode, T)
                    except MemoryError:
                        results.append(dict(family=fam, N=N, mode=mode, T=T, error='not enumerated')); continue
                    missing = [u for u in SF.unk if u not in SA.unk]
                    assert not missing, missing[:3]
                    idx = [SA.unk[u] for u in SF.unk]          # U_fam in the order of SF
                    restr = [[v[i] for i in idx] for v in NA]   # V_all restricted to U_fam
                    rows = list(SF.rows)
                    # hypothesis check: every restricted vector satisfies the family's equations
                    contained = all(E.satisfies(rows, v) for v in restr)
                    dA = E.rank_of(restr) if restr else 0
                    names = ['count', 'square'] + (['xcount'] if mode == 'per' else [])
                    model = [SF.vec(nm) for nm in names if E.satisfies(rows, SF.vec(nm))]
                    r = dict(family=fam, N=N, mode=mode, T=T, events=SF.nevents, equations=len(rows),
                             unknowns=len(SF.unk), dim_family=len(NF), dim_all_restricted=dA,
                             excess=len(NF) - dA, all_contained_in_family=contained,
                             model_rank=E.rank_of(model), seconds=round(time.time() - t0, 1))
                    results.append(r); print(json.dumps(r), flush=True)
                    if r['excess'] > 0 and mode == 'uni' and T == Tmax:
                        # an explicit extra rule: first basis vector of V_fam outside V_all|U_fam
                        for v in NF:
                            if E.rank_of(restr + [v]) > dA:
                                inv = {j: u for u, j in SF.unk.items()}
                                extras.append(dict(family=fam, N=N, T=T, satisfies_equations=E.satisfies(rows, v),
                                                   rule={repr(inv[j]): v[j] for j in range(len(v)) if v[j]}))
                                break
    def get(f, mode, T, N=None):
        for r in results:
            if r['family'] == f and r['mode'] == mode and r['T'] == T and r['N'] == N and 'excess' in r: return r
    def P(name, text, items, cond):
        rs = [get(*it) for it in items]
        if any(r is None for r in rs): return dict(predicate=name, text=text, passed=None, note='not computed')
        return dict(predicate=name, text=text, passed=all(cond(r) for r in rs), values=[r['excess'] for r in rs])
    preds = [
        P('Q1', 'b: excess 0 at T=3,4, uni and per', [('b', m, T) for m in ('uni', 'per') for T in (3, 4)], lambda r: r['excess'] == 0),
        P('Q2', 'a: excess > 0 at T=5', [('a', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] > 0),
        P('Q3', 'c: excess > 0 at T=5', [('c', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] > 0),
        P('Q4', 'b1: excess > 0 at T=5', [('b1', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] > 0),
        P('Q5', 'bpos: excess > 0 at T=5', [('bpos', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] > 0),
        P('Q6', 'bs: excess > 0 at T=5', [('bs', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] > 0),
        P('Q7', 'b2: excess > 0 at T=5', [('b2', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] > 0),
        P('Q8', 'b: excess 0 at T=5', [('b', m, 5) for m in ('uni', 'per')], lambda r: r['excess'] == 0),
    ]
    for p in preds: print(p)
    with open(out, 'x') as f:
        json.dump(dict(results=results, predicates=preds, explicit_extra_rules=extras), f, indent=1)

if __name__ == '__main__':
    main()
