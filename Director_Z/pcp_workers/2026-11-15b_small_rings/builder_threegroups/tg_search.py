#!/usr/bin/env python3
"""Packet-model search for Proposition prop:threegroups on rings with M = N/gcd(N,2) small.

MODEL (deficit picture, carrier D_delta: a=b=c=1, d=delta).
  A packet is the set of walks at one deficit residue mod M.  A tick chooses for every packet an action
  R (land at j), L (land at j+1), RL (split; only the source S), K (die; only S, only at the kill).
  The mask is the set of landings.  A tick is VALID iff for every packet the set of its candidates
  {j, j+1} that lie in the mask equals the set of its chosen landings, and two packets land on one
  residue only in an allowed merge: (a) the copy made by the split of S, or the copy-in-transit D,
  onto the front stock (the stock next above S in the lift); (b) after the kill, A onto C (one lap up);
  (c) the final tick.  Positions are integers relative to S (phases 0-3) or to C (phases 4-5);
  stocks stay in the open lap (0, M).  Increment of a gain exponent = 1 iff action L from rail L.
  RESTRICTED mode (first run, run1): in phases 1-3 no packet other than S takes an increment.
  In all runs a packet whose walks arrived on different rails (rail 'M') may not take L in phases 1-3.
  Run2 onward: restricted=False, and the edge weight is psi_k = (increment of S) - (increment of X_k),
  X_k the front stock of phase k (in phase 0 the weight is the increment of S).  P2 uses gcd of psi_k.

PHASES: 0 = S alone; 1 = S,A; 2 = S,B,A; 3 = S,C,B,A (D may be present in 1-3); 4 = C,B,A after kill;
  5 = CA,B after the lap merge; FINAL_i / FINAL_ii.

PREDICATES (fixed before the first run):
  P1(M): the reachable graph is finite and its size is reported (bound: positions in [0,M), at most
         6 packets, rails in {R,L,M}; the BFS has an explicit state cap STATE_CAP and reports if hit).
  P2(M,k), k=1,2,3: some strongly connected component of the phase-k internal graph contains a deposit
         edge into the front stock X_k and has gcd of cycle sums of Delta e_S equal to 1.
  P3(M,mode): there is a path start -> creation of A -> good SCC_1 -> creation of B -> good SCC_2 ->
         creation of C -> good SCC_3 -> kill -> lap merge -> FINAL_mode, every segment inside its phase.
  Hypothesis tested per case: M >= 3 (the model needs residues j, j+1 distinct and the lap (0,M) nonempty);
  the number of M values qualifying is reported.
Usage: tg_search.py OUTFILE M1 [M2 ...]   (no randomness; result file opened with mode 'x').
"""
import sys, json, math
from collections import deque
from itertools import product

STATE_CAP = 2_000_000
STOCK_OF_PHASE = {1: 'A', 2: 'B', 3: 'C'}

def actions_for(label, phase):
    if label == 'S':
        acts = ['R', 'L', 'RL']
        if phase == 3:
            acts.append('K')
        return acts
    return ['R', 'L']

def step(state, acts, M, restricted=True):
    """state = (phase, packets) packets = tuple of (label,pos,rail) sorted by pos.
    Returns (newstate, info) or None if invalid.  info: dict(dS, deposit, kind)."""
    phase, packets = state
    landings = []  # (residue, idx, kind, abspos)
    for i, ((lab, pos, rail), a) in enumerate(zip(packets, acts)):
        if a in ('R', 'RL'):
            landings.append((pos % M, i, 'R', pos))
        if a in ('L', 'RL'):
            landings.append((((pos + 1) % M), i, 'L', pos + 1))
    E = {r for r, _, _, _ in landings}
    # determinism / survival check
    for i, ((lab, pos, rail), a) in enumerate(zip(packets, acts)):
        surv = set()
        if pos % M in E: surv.add('R')
        if (pos + 1) % M in E: surv.add('L')
        want = {'R': {'R'}, 'L': {'L'}, 'RL': {'R', 'L'}, 'K': set()}[a]
        if surv != want:
            return None
    # restricted increments / mixed rails
    dS = 0
    dX = 0
    for (lab, pos, rail), a in zip(packets, acts):
        inc = 1 if (a == 'L' and rail == 'L') else 0
        if lab == 'S':
            dS = inc
        elif phase in (1, 2, 3):
            if a == 'L' and rail == 'M':
                return None
            if restricted and inc:
                return None
            if lab == STOCK_OF_PHASE[phase]:
                dX = inc
    # group by residue
    byres = {}
    for r, i, kind, ap in landings:
        byres.setdefault(r, []).append((i, kind, ap))
    labels = [p[0] for p in packets]
    newp = []
    deposit = False
    kind_edge = 'int'
    newphase = phase
    created = None
    final_mode = None
    for r, lst in byres.items():
        if len(lst) == 1:
            i, kind, ap = lst[0]
            lab = labels[i]
            if lab == 'S' and kind == 'L' and acts[i] == 'RL':
                # copy alone: new stock (phase transition) or D
                if phase == 0 or (phase in (1, 2)):
                    # decide later (both options); mark
                    created = ap
                    continue
                elif phase == 3:
                    created = ap
                    continue
                else:
                    return None
            newp.append((lab, ap, kind))
        elif len(lst) == 2:
            (i1, k1, a1), (i2, k2, a2) = lst
            l1, l2 = labels[i1], labels[i2]
            pair = {l1, l2}
            if phase in (1, 2, 3):
                X = STOCK_OF_PHASE[phase]
                # copy from split of S onto front stock
                if 'S' in pair and X in pair:
                    iS = i1 if l1 == 'S' else i2
                    kS = k1 if l1 == 'S' else k2
                    aX = a2 if l1 == 'S' else a1
                    kX = k2 if l1 == 'S' else k1
                    if acts[iS] != 'RL' or kS != 'L' or aX != packets[iS][1] + 1:
                        return None
                    if any(l == 'D' for l in labels):
                        return None
                    newp.append((X, aX, kX if kX == 'L' and False else ('M' if kX != 'L' else 'L')))
                    deposit = True
                    continue
                if pair == {'D', X}:
                    iD = i1 if l1 == 'D' else i2
                    kD = k1 if l1 == 'D' else k2
                    kX = k2 if l1 == 'D' else k1
                    aX = a2 if l1 == 'D' else a1
                    rail = kD if kD == kX else 'M'
                    newp.append((X, aX, rail))
                    deposit = True
                    continue
                return None
            elif phase == 4:
                if pair == {'A', 'C'}:
                    iA = i1 if l1 == 'A' else i2
                    aA = a1 if l1 == 'A' else a2
                    aC = a2 if l1 == 'A' else a1
                    if aA != aC + M:
                        return None
                    newp.append(('CA', aC, 'M'))
                    newphase = 5
                    kind_edge = 'lap'
                    continue
                return None
            elif phase == 5:
                # final tick: only if exactly CA and B and both land here, nothing else anywhere
                if pair == {'CA', 'B'} and len(packets) == 2:
                    iB = i1 if l1 == 'B' else i2
                    kB = k1 if l1 == 'B' else k2
                    aB = a1 if l1 == 'B' else a2
                    aC = a2 if l1 == 'B' else a1
                    if kB == 'R' and aB == aC:
                        final_mode = 'i'
                    elif kB == 'L' and aB == aC + M:
                        final_mode = 'ii'
                    else:
                        return None
                    continue
                return None
            else:
                return None
        else:
            return None
    if final_mode is not None:
        if len(byres) != 1:
            return None
        return (('FINAL', final_mode), {'dS': 0, 'deposit': False, 'kind': 'final'})
    # kill
    if 'K' in acts:
        newphase = 4
        kind_edge = 'kill'
    results = []
    options = [None]
    if created is not None:
        options = []
        if phase in (0, 1, 2) and not any(l == 'D' for l in labels):
            options.append(('new', STOCK_OF_PHASE[phase + 1]))
        if phase in (1, 2, 3) and not any(l == 'D' for l in labels):
            options.append(('D', 'D'))
    for opt in options:
        pk = list(newp)
        ph = newphase
        ke = kind_edge
        if opt is not None:
            pk.append((opt[1], created, 'L'))
            if opt[0] == 'new':
                ph = phase + 1
                ke = 'create'
        # normalize
        if ph in (0, 1, 2, 3):
            spos = [p for p in pk if p[0] == 'S']
            if len(spos) != 1:
                continue
            base = spos[0][1]
        else:
            cpos = [p for p in pk if p[0] in ('C', 'CA')]
            if len(cpos) != 1:
                continue
            base = cpos[0][1]
        pk = [(l, p - base, r) for (l, p, r) in pk]
        baselabs = ('S',) if ph in (0, 1, 2, 3) else ('C', 'CA')
        ok = all(0 < p < M for (l, p, r) in pk if l not in baselabs) and \
            all(p == 0 for (l, p, r) in pk if l in baselabs)
        if not ok:
            continue
        poss = [p for (_, p, _) in pk]
        if len(set(poss)) != len(poss):
            continue
        pk.sort(key=lambda t: t[1])
        # lift order of stocks must be S < (D) < C < B < A (phases) ; after kill C < B < A
        order = [l for (l, _, _) in pk]
        expect = {0: ['S'], 1: ['S', 'A'], 2: ['S', 'B', 'A'], 3: ['S', 'C', 'B', 'A'],
                  4: ['C', 'B', 'A'], 5: ['CA', 'B']}[ph]
        if [l for l in order if l != 'D'] != expect:
            continue
        if 'D' in order:
            iD = order.index('D')
            if ph not in (1, 2, 3) or order[iD - 1] != 'S' or order[iD + 1] != STOCK_OF_PHASE[ph]:
                continue
        results.append(((ph, tuple(pk)), {'dS': dS - dX, 'deposit': deposit, 'kind': ke}))
    return results

def explore(M, restricted=True):
    start = (0, (('S', 0, 'R'),))
    seen = {start: 0}
    states = [start]
    edges = []  # (u, v, dS, deposit, kind)
    dq = deque([start])
    capped = False
    while dq:
        s = dq.popleft()
        if s[0] == 'FINAL':
            continue
        u = seen[s]
        packets = s[1]
        for acts in product(*[actions_for(p[0], s[0]) for p in packets]):
            res = step(s, acts, M, restricted)
            if res is None:
                continue
            if isinstance(res, tuple):
                res = [res]
            for ns, info in res:
                if ns not in seen:
                    if len(seen) >= STATE_CAP:
                        capped = True
                        continue
                    seen[ns] = len(states)
                    states.append(ns)
                    dq.append(ns)
                edges.append((u, seen[ns], info['dS'], info['deposit'], info['kind'], acts))
    return states, edges, capped

def sccs(n, adj):
    index = [None] * n; low = [0] * n; onst = [False] * n; st = []; comp = [-1] * n
    c = 0; idx = 0
    sys.setrecursionlimit(1000000)
    for root in range(n):
        if index[root] is not None:
            continue
        work = [(root, 0)]
        while work:
            v, pi = work.pop()
            if pi == 0:
                index[v] = idx; low[v] = idx; idx += 1; st.append(v); onst[v] = True
            recurse = False
            nb = adj[v]
            for j in range(pi, len(nb)):
                w = nb[j]
                if index[w] is None:
                    work.append((v, j + 1)); work.append((w, 0)); recurse = True; break
                elif onst[w]:
                    low[v] = min(low[v], index[w])
            if recurse:
                continue
            if low[v] == index[v]:
                while True:
                    w = st.pop(); onst[w] = False; comp[w] = c
                    if w == v: break
                c += 1
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[v])
    return comp, c

def analyse(M, restricted=True):
    states, edges, capped = explore(M, restricted)
    n = len(states)
    phase = [s[0] for s in states]
    out = {'M': M, 'restricted': restricted, 'states': n, 'edges': len(edges), 'state_cap_hit': capped}
    good = {}
    for k in (0, 1, 2, 3):
        adj = [[] for _ in range(n)]
        for (u, v, dS, dep, kind, acts) in edges:
            if phase[u] == k and phase[v] == k:
                adj[u].append(v)
        comp, nc = sccs(n, adj)
        # potentials and gcd per component
        pot = {}
        g = {}
        hasdep = {}
        for (u, v, dS, dep, kind, acts) in edges:
            if phase[u] == k and phase[v] == k and comp[u] == comp[v]:
                hasdep.setdefault(comp[u], False)
                if dep:
                    hasdep[comp[u]] = True
        # BFS potentials inside each comp
        cadj = {}
        for (u, v, dS, dep, kind, acts) in edges:
            if phase[u] == k and phase[v] == k and comp[u] == comp[v]:
                cadj.setdefault(u, []).append((v, dS))
                cadj.setdefault(v, []).append((u, -dS))
        for s0 in range(n):
            if phase[s0] != k or s0 in pot or s0 not in cadj:
                continue
            pot[s0] = 0
            dq = deque([s0])
            while dq:
                x = dq.popleft()
                for y, w in cadj[x]:
                    if y not in pot:
                        pot[y] = pot[x] + w; dq.append(y)
        for (u, v, dS, dep, kind, acts) in edges:
            if phase[u] == k and phase[v] == k and comp[u] == comp[v]:
                c = comp[u]
                g[c] = math.gcd(g.get(c, 0), abs(pot[u] + dS - pot[v]))
        if k == 0:
            goodc = {c for c in g if g[c] == 1}
        else:
            goodc = {c for c in g if g[c] == 1 and hasdep.get(c)}
        good[k] = {v for v in range(n) if phase[v] == k and comp[v] in goodc}
        out['phase%d_good_scc_count' % k] = len(goodc)
        out['phase%d_good_nodes' % k] = len(good[k])
        out['phase%d_nodes' % k] = sum(1 for p in phase if p == k)
    # chained reachability: layered search over (node, stage) where stage counts good SCCs visited
    # stage s: 0 = in phase 0 before visiting good0 ; we require visiting good_k in phase k for k=0..3
    fwd = [[] for _ in range(n)]
    for (u, v, dS, dep, kind, acts) in edges:
        fwd[u].append(v)
    start = 0
    st0 = (start, 1 if start in good[0] else 0)
    seen = {st0}
    dq = deque([st0])
    finals = set()
    while dq:
        v, s = dq.popleft()
        for w in fwd[v]:
            pv, pw = phase[v], phase[w]
            ns = s
            if isinstance(pw, int) and pw <= 3:
                if pw != pv:
                    if s != pv + 1:  # must have visited good of phase pv
                        continue
                if w in good[pw] and ns == pw:
                    ns = pw + 1
            else:
                if isinstance(pv, int) and pv == 3 and s != 4:
                    continue
            if pw == 'FINAL':
                finals.add(states[w][1])
                continue
            if (w, ns) not in seen:
                seen.add((w, ns)); dq.append((w, ns))
    out['P3_mode_i'] = 'i' in finals
    out['P3_mode_ii'] = 'ii' in finals
    return out, states, edges, good

if __name__ == '__main__':
    outfile = sys.argv[1]
    RESTRICTED = False
    Ms = [int(a) for a in sys.argv[2:]]
    with open(outfile, 'x') as f:
        f.write(json.dumps({'argv': sys.argv, 'STATE_CAP': STATE_CAP}) + '\n')
        qual = [M for M in Ms if M >= 3]
        f.write(json.dumps({'hypothesis_M_ge_3_qualifying': len(qual), 'of': len(Ms)}) + '\n')
        for M in qual:
            out, *_ = analyse(M, RESTRICTED)
            f.write(json.dumps(out) + '\n')
            f.flush()
            print(json.dumps(out))
