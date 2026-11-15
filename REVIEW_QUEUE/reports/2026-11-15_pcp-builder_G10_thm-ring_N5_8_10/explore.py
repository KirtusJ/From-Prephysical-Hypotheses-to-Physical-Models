"""G10 Thm (posprodq)(i) on rings with M = N/gcd(N,2) in {4,5}, i.e. N in {5,8,10}.

Carrier D_h on ring Z_N, gain h of order q (gains stored as exponents mod q).
Position product events (PPE) explored by BFS from the walk at (0,R): each step
extends every walk by one arc and keeps walks whose new site lies in a chosen
nonempty set A_s.  Bounds: length <= TMAX, total walks <= WMAX (argv).

Hypothesis test per carrier (done first, reported): carrier qualifies iff it is a
ring with M in {4,5}; control carriers (M>=6, where Lemma prepq is claimed) are
run too and labelled CONTROL.

Predicates, fixed before the first run:
 P1 (one-site reach): every pair (U,V) of gain multisets with |U|+|V| <= B,
    at every site x, is the restriction to site x of some explored PPE.
    Reports reached/total.  (Bounded search: a failure is only "not found".)
 P2 (forcing): let Z be the space of site-independent (F_R,F_L), F(0)=0,
    satisfying mu(Ext S) = 2 mu(S) for every explored PPE S (unknowns = all
    multisets occurring).  Projected to coordinates |m| <= 2 of both F_R,F_L,
    Z equals the projection of span{|m|, eps(m)^2} (q even) / span{|m|} (q odd).
    Exact rational arithmetic.
Usage: python3 explore.py OUTFILE TMAX WMAX B
"""
import sys, random, itertools
from fractions import Fraction
random.seed(20261113)

def step(state, N, q, A):
    new = {}
    for (x, d), ms in state.items():
        for (nx, nd, dg) in (((x+1) % N, 'R', 0), ((x-1) % N, 'L', 1 if d == 'L' else 0)):
            if nx not in A: continue
            key = (nx, nd)
            arr = list(new.get(key, (0,)*q))
            for g in range(q):
                if ms[g]: arr[(g+dg) % q] += ms[g]
            new[key] = tuple(arr)
    return frozenset(new.items())

def total(st): return sum(sum(m) for _, m in st)

def explore(N, q, TMAX, WMAX):
    start = frozenset({((0, 'R'), tuple(1 if g == 0 else 0 for g in range(q)))})
    allsites = set(range(N))
    subsets = [set(c) for r in range(1, N+1) for c in itertools.combinations(range(N), r)]
    seen = set(); frontier = {start}; events = set()
    for T in range(1, TMAX+1):
        nf = set()
        for st in frontier:
            d = dict(st)
            for A in subsets:
                s2 = step(d, N, q, A)
                if s2 and total(s2) <= WMAX and s2 not in seen:
                    seen.add(s2); nf.add(s2)
        events |= nf; frontier = nf
    return events

def ext(st, N, q): return step(dict(st), N, q, set(range(N)))

def nullspace_rows(eqs, nvar):
    # eqs: list of dict var->int. Return reduced row echelon (pivots) over Q.
    piv = {}  # pivot var -> row dict
    for e in eqs:
        r = {k: Fraction(v) for k, v in e.items() if v}
        for pv in sorted(piv):
            pass
        changed = True
        while r:
            k = min(r)
            if k in piv:
                c = r[k]; pr = piv[k]
                for kk, vv in pr.items():
                    r[kk] = r.get(kk, 0) - c*vv
                    if r[kk] == 0: del r[kk]
            else:
                c = r[k]
                r = {kk: vv/c for kk, vv in r.items()}
                piv[k] = r; break
    return piv

def main():
    out, TMAX, WMAX, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    f = open(out, 'x')
    def w(s): print(s); f.write(s+'\n'); f.flush()
    w(f"argv={sys.argv}")
    carriers = [(N, q) for N in (5, 8, 10, 6, 12) for q in (2, 3, 4)]
    nq = 0
    for N, q in carriers:
        M = N // (2 if N % 2 == 0 else 1)
        qual = M in (4, 5)
        nq += qual
        tag = 'QUALIFIES' if qual else ('CONTROL(M>=6)' if M >= 6 else 'OTHER')
        ev = explore(N, q, TMAX, WMAX)
        # P1
        reach = set()
        for st in ev:
            d = dict(st); z = (0,)*q
            for x in range(N):
                reach.add((x, d.get((x, 'R'), z), d.get((x, 'L'), z)))
        ms = [m for m in itertools.product(range(B+1), repeat=q) if sum(m) <= B]
        tot = 0; got = 0; miss = []
        for x in range(N):
            for U in ms:
                for V in ms:
                    if sum(U)+sum(V) <= B and sum(U)+sum(V) > 0:
                        tot += 1
                        if (x, U, V) in reach: got += 1
                        elif len(miss) < 4: miss.append((x, U, V))
        w(f"N={N} q={q} M={M} {tag} events={len(ev)} P1 reached {got}/{tot} {'PASS' if got==tot else 'FAIL'} sample_missing={miss}")
        # P2
        var = {}
        def vid(t, m):
            if (t, m) not in var: var[(t, m)] = len(var)
            return var[(t, m)]
        smallR = [m for m in itertools.product(range(3), repeat=q) if 0 < sum(m) <= 2]
        for t in 'RL':
            for m in smallR: vid(t, m)
        nsmall = len(var)
        eqs = []
        for st in ev:
            e = {}
            for (y, m) in ext(st, N, q):
                k = vid(y[1], m); e[k] = e.get(k, 0) + 1
            for (y, m) in st:
                k = vid(y[1], m); e[k] = e.get(k, 0) - 2
            eqs.append(e)
        piv = nullspace_rows(eqs, len(var))
        # dim of projection of nullspace onto small coords: = nsmall - rank of
        # constraints implied purely on small coords. Order: big vars must be
        # eliminated first -> recompute with big vars given smaller index.
        nv = len(var)
        remap = {i: (i - nsmall if i >= nsmall else nv - nsmall + i) for i in range(nv)}
        eqs2 = [{remap[k]: v for k, v in e.items()} for e in eqs]
        piv2 = nullspace_rows(eqs2, nv)
        small_constraints = [r for p, r in piv2.items() if p >= nv - nsmall]
        projdim = nsmall - len(small_constraints)
        expdim = 2 if q % 2 == 0 else 1
        w(f"   P2 unknowns={nv} rank={len(piv)} projected_dim(|m|<=2)={projdim} expected={expdim} {'PASS' if projdim==expdim else 'FAIL'}")
    w(f"carriers qualifying={nq} of {len(carriers)}")
    f.close()

main()
