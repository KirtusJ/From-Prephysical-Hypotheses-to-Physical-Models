#!/usr/bin/env python3
"""ev_linegraph.py -- the line digraph L(D) of the signed ring D = Z1-R as a second carrier.

L(D): vertices = arcs (p -> y) of D; an arc from (p -> y) to (y -> z) for every arc y -> z of D, with
the gain of y -> z. Start vertex of L(D): the arc ((N-1,R) -> (0,R)), which ends at x0 = (0,R).
Records on L(D) in the sense of S3 = its vertices = (end vertex of the walk in D, its last arc).

PREDICATES fixed before the first run (rings N = 3, 4, 5):
 G1 L(D) satisfies S1: exactly 2 arcs leave every vertex, at most one arc for each ordered pair of
    vertices, and the derived digraph (vertex, gain) is strongly connected.
 G2 for t <= 6 the walks of L(D) of length t from the start arc correspond one to one to the walks of
    D of length t from x0 (same sequence of vertices of D after the start), with the same gains.
 G3 for neither character of C = {+1,-1} does the step matrix of L(D) satisfy A* A = 2: so by the
    model's own D1 the only consistent rule on L(D) is a|S|.
 G4 (control) D itself: A* A = 2 for the sign character and not for the trivial one.
Result file not overwritten.
"""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
def ring(N):
    arcs = {}
    for x in range(N):
        for r in 'RL':
            arcs[((x, r), ((x + 1) % N, 'R'))] = 1
            arcs[((x, r), ((x - 1) % N, 'L'))] = -1 if r == 'L' else 1
    return arcs
def line(arcs):
    L = {}
    for e in arcs:
        for f, g in arcs.items():
            if f[0] == e[1]: L[(e, f)] = g
    return L
def check_S1(arcs):
    V = sorted({a[0] for a in arcs} | {a[1] for a in arcs})
    outdeg = {v: sum(1 for a in arcs if a[0] == v) for v in V}
    simple = len(set(arcs)) == len(arcs)   # dict keys are ordered pairs: one arc per pair by construction
    # derived digraph strongly connected
    nodes = [(v, g) for v in V for g in (1, -1)]
    succ = {n: [] for n in nodes}
    for (u, v), g in arcs.items():
        for h in (1, -1): succ[(u, h)].append((v, h * g))
    def reach(start, fwd=True):
        adj = succ if fwd else {n: [m for m in nodes if n in succ[m]] for n in nodes}
        seen = {start}; st = [start]
        while st:
            a = st.pop()
            for b in adj[a]:
                if b not in seen: seen.add(b); st.append(b)
        return seen
    sc = len(reach(nodes[0])) == len(nodes) and len(reach(nodes[0], False)) == len(nodes)
    return dict(vertices=len(V), outdegree_2=all(d == 2 for d in outdeg.values()), one_arc_per_pair=simple, derived_strongly_connected=sc)
def AstarA(arcs, char):
    V = sorted({a[0] for a in arcs} | {a[1] for a in arcs})
    val = lambda g: g if char == 'sign' else 1
    ok = True
    for u in V:
        for w in V:
            s = sum(val(arcs[(u, z)]) * val(arcs[(w, z)]) for z in V if (u, z) in arcs and (w, z) in arcs)
            if s != (2 if u == w else 0): ok = False
    return ok
def walks(arcs, start, t):
    out = [([start], 1)]
    for _ in range(t):
        out = [(p + [v], g * h) for p, g in out for (u, v), h in arcs.items() if u == p[-1]]
    return out
def main():
    out = os.path.join(HERE, 'ev_linegraph_results.json')
    if os.path.exists(out): sys.exit('result file exists, not overwritten')
    R = {}
    for N in (3, 4, 5):
        D = ring(N); L = line(D)
        start = (((N - 1) % N, 'R'), (0, 'R'))
        g2 = True
        for t in range(0, 7):
            wD = sorted((tuple(p), g) for p, g in walks(D, (0, 'R'), t))
            wL = sorted((tuple([e[1] for e in p]), g) for p, g in walks(L, start, t))
            if wD != wL: g2 = False
        R[N] = dict(G1=check_S1(L), G2=g2, G3=dict(sign=AstarA(L, 'sign'), trivial=AstarA(L, 'trivial')),
                    G4=dict(S1_of_D=check_S1(D), sign=AstarA(D, 'sign'), trivial=AstarA(D, 'trivial')))
    print(json.dumps(R, indent=1))
    with open(out, 'x') as f: json.dump(R, f, indent=1)
main()
