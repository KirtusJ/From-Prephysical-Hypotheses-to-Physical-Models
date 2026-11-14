"""Wildcard (seed 'margin'): the margin of Lemma 5.30/5.34 of G10 -- the small signed rings on which
Remark 5.33(d) says the conclusion of the preparation lemma 'is not known'.

Object (body.tex l.779): signed arc digraph of Z_N, vertices (x,R),(x,L), arcs from either to (x+1,R),(x-1,L),
gain -1 only on (x,L)->(x-1,L); walks from (0,R); position product event of length T>=1 = all walks whose
position after s steps is in A_s, s=1..T. m_S(x,R)=U, m_S(x,L)=V in N^2 (gain +1 count, gain -1 count).

Method: exact integer closure. State after s steps = (U_x,V_x) at every site. One step: extend
(new (x+1,R)=U_x+V_x, new (x-1,L)=U_x+JV_x), then keep any subset of sites (the mask A_s).
Pruning (exact, proved in NOTES.txt): a site whose total |U|+|V| exceeds B may be masked at once, because all
walks at one site at one time have the same number d of continuations to the target site, so d>=1 would give
a target total > B. Hence the set of site-states with total <= B that occur at some T>=1 is the closure below.

Predicates, fixed before the first run:
 P0 (control, known answer, Remark 5.33(d)): for N=1 and N=2 the reachable site-states with total<=B at T>=1 are
    only the zero pair and those of the event of all walks.  [checked as: some pair with total<=B is unreachable]
 P1 (cross-check of the closure): for N=3, the site-states with total<=B found by brute force over all 8^T mask
    sequences, T=1..4, are a subset of the closure's set, and equal the closure's set restricted to depth<=4.
 P2 (hypothesis check): for every N>=3 all four unit pairs (one walk) are reachable at every site.
 Q  (the question, no expected answer): for N in the list and B, is every (U,V) with |U|+|V|<=B reachable at
    every site x?  Reported per N: number reachable per site out of C(B+4,4), and the missing pairs.
No tolerance: integers only. Result file opened with mode 'x'.
"""
import sys, json, itertools
def step_states(state, N, B):
    new = [[0,0,0,0] for _ in range(N)]
    for x,(pR,qR,pL,qL) in enumerate(state):
        if pR+qR+pL+qL == 0: continue
        a = new[(x+1)%N]; a[0] += pR+pL; a[1] += qR+qL
        b = new[(x-1)%N]; b[2] += pR+qL; b[3] += qR+pL
    new = [tuple(v) if sum(v) <= B else (0,0,0,0) for v in new]
    occ = [x for x in range(N) if sum(new[x])]
    Z = (0,0,0,0)
    for r in range(len(occ)+1):
        for keep in itertools.combinations(occ, r):
            ks = set(keep)
            yield tuple(new[x] if x in ks else Z for x in range(N))
def closure(N, B, maxdepth=None):
    init = tuple((1,0,0,0) if x == 0 else (0,0,0,0) for x in range(N))
    frontier = {init}; seen = set(); depth = 0
    site = [set() for _ in range(N)]
    first = {}
    while frontier and (maxdepth is None or depth < maxdepth):
        depth += 1; nxt = set()
        for st in frontier:
            for t in step_states(st, N, B):
                if t not in seen:
                    seen.add(t); nxt.add(t)
                    for x in range(N):
                        if t[x] not in site[x]:
                            site[x].add(t[x]); first[(x, t[x])] = depth
        frontier = nxt
    return site, len(seen), depth, first
def brute(N, B, T):
    out = [set() for _ in range(N)]
    init = [(0,(1,0))]  # list of (pos, endvertex R=1, gain sign) ; enumerate walks explicitly
    for masks in itertools.product(range(2**N), repeat=T):
        walks = [(0,'R',1)]
        for s in range(T):
            nw = []
            for (x,c,g) in walks:
                y = (x+1)%N
                if masks[s]>>y & 1: nw.append((y,'R',g))
                y = (x-1)%N
                if masks[s]>>y & 1: nw.append((y,'L',-g if c=='L' else g))
            walks = nw
        for x in range(N):
            v = (sum(1 for w in walks if w==(x,'R',1)), sum(1 for w in walks if w==(x,'R',-1)),
                 sum(1 for w in walks if w==(x,'L',1)), sum(1 for w in walks if w==(x,'L',-1)))
            if sum(v) <= B: out[x].add(v)
    return out
def allpairs(B):
    return [v for v in itertools.product(range(B+1), repeat=4) if sum(v) <= B]
def main():
    cases = json.loads(sys.argv[1]); outname = sys.argv[2]
    f = open(outname, 'x')
    res = {"convention": "site-state (pR,qR,pL,qL): counts at (x,R) gain +1,-1 and at (x,L) gain +1,-1; start (0,R), T>=1", "cases": []}
    units = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    for N,B in cases:
        site, nstates, depth, first = closure(N, B)
        full = allpairs(B)
        rec = {"N": N, "B": B, "states": nstates, "closure_depth": depth, "pairs_total": len(full),
               "reachable_per_site": [len([v for v in full if v in s]) for s in site],
               "missing_at_site0": [v for v in full if v not in site[0]][:60],
               "n_missing_per_site": [len([v for v in full if v not in s]) for s in site],
               "max_first_depth": max(first.values()) if first else 0}
        if N <= 2: rec["P0_some_unreachable"] = any(n > 0 for n in rec["n_missing_per_site"])
        else: rec["P2_units_everywhere"] = all(u in s for s in site for u in units)
        rec["Q_all_reachable_every_site"] = all(n == 0 for n in rec["n_missing_per_site"])
        res["cases"].append(rec); print(json.dumps(rec)[:600], flush=True)
    # P1
    B = 3; bf = [set() for _ in range(3)]
    for T in range(1,5):
        o = brute(3, B, T)
        for x in range(3): bf[x] |= o[x]
    s4, _, _, _ = closure(3, B, maxdepth=4)
    res["P1"] = {"N": 3, "B": B, "equal_depth4": all(bf[x] == s4[x] for x in range(3)),
                 "sizes": [len(b) for b in bf]}
    print(res["P1"])
    json.dump(res, f, indent=1); f.close()
main()
