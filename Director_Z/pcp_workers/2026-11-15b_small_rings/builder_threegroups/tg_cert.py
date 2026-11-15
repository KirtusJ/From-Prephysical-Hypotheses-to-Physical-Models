#!/usr/bin/env python3
"""Explicit finite certificate for prop:threegroups at a given M (used for M = 7), in the packet model of
tg_search.py (restricted=False; mixed-rail packets never step left in phases 1-3).

The certificate consists of nodes h_1, h_2, h_3 of the packet graph (no copy in transit) and tick sequences
  U_0          closed walk at the S-alone node with rail L, psi_0 = +1 (S steps L from L),
  U_k (k=1,2,3) closed walk at h_k with no deposit and no split, psi_k = dS - dX_k = +1 exactly,
  D_k (k=1,2,3) closed walk at h_k with exactly one split of S and exactly one deposit into X_k,
  P_0          from the S-alone node with rail L to h_1, whose only split is the creation of A,
  P_1, P_2     from h_k to h_{k+1}, whose only split is the creation of X_{k+1},
  E_i, E_ii    from h_3 through the kill and the lap merge to FINAL of mode i / ii, with no split,
and the gain data of each sequence (increments of S, A, B, C; for D_k and the creation ticks also the
exponent offset of the new walk relative to S before its split).

PREDICATES (fixed before the first run):
  C1: every tick of every sequence is valid by tg_search.step (recomputed independently by verify()).
  C2: the shapes above hold (split / deposit counts, start and end nodes, psi values).
Search bounds: BFS over (node, psi) with |psi| <= PSIMAX = 8 and path length <= LMAX = 60; reported if hit.
Usage: tg_cert.py OUTFILE M ; result file opened with mode 'x'.  No randomness.
"""
import sys, json
from collections import deque
import tg_search as T

PSIMAX = 8
LMAX = 60

def graph(M):
    out, states, edges, good = T.analyse(M, False)
    adj = [[] for _ in states]
    for (u, v, dS, dep, kind, acts) in edges:
        adj[u].append((v, acts, dep, kind))
    return states, adj, good

def incs(st, acts):
    return {lab: (1 if (a == 'L' and rail == 'L') else 0) for (lab, pos, rail), a in zip(st[1], acts)}

def bfs(states, adj, src, accept, allow, psi_of, track_psi=True):
    """shortest path from src; state (node, psi, extra); allow(u,v,acts,dep,kind,extra)->new extra or None."""
    start = (src, 0, 0)
    prev = {start: None}
    dq = deque([(start, 0)])
    hit_len_bound = False
    while dq:
        s, L = dq.popleft()
        node, psi, ex = s
        if L >= LMAX:
            hit_len_bound = True
            continue
        for (v, acts, dep, kind) in adj[node]:
            ne = allow(node, v, acts, dep, kind, ex)
            if ne is None:
                continue
            npsi = psi + (psi_of(node, acts) if track_psi else 0)
            if abs(npsi) > PSIMAX:
                continue
            ns = (v, npsi, ne)
            if ns in prev:
                continue
            prev[ns] = (s, acts)
            if accept(ns):
                path = []
                p = ns
                while prev[p] is not None:
                    pp, a = prev[p]
                    path.append((pp[0], a))
                    p = pp
                return list(reversed(path)), ns, hit_len_bound
            dq.append((ns, L + 1))
    return None, None, hit_len_bound

def main(outfile, M):
    states, adj, good = graph(M)
    idx = {s: i for i, s in enumerate(states)}
    ph = [s[0] for s in states]
    def psi_k(k):
        X = T.STOCK_OF_PHASE.get(k)
        def f(node, acts):
            inc = incs(states[node], acts)
            return inc.get('S', 0) - (inc.get(X, 0) if X else 0)
        return f
    cert = {}
    bounds_hit = False
    s0L = idx[(0, (('S', 0, 'L'),))]
    s0R = idx[(0, (('S', 0, 'R'),))]
    # U_0
    cert['U0'] = [(s0L, ('L',))]
    hs = {}
    for k in (1, 2, 3):
        cands = [v for v in sorted(good[k]) if not any(p[0] == 'D' for p in states[v][1])]
        best = None
        for h in cands:
            # U_k: no split, no deposit, phase k only, psi = +1
            U, _, b1 = bfs(states, adj, h, lambda ns, h=h: ns[0] == h and ns[1] == 1,
                           lambda u, v, a, dep, kind, ex: ex if (ph[v] == k and a[0] != 'RL' and not dep) else None,
                           psi_k(k))
            if U is None:
                continue
            # D_k: exactly one split and one deposit, back at h
            def allowD(u, v, a, dep, kind, ex):
                if ph[v] != k: return None
                ns_ = ex
                if a[0] == 'RL':
                    if ex & 1: return None
                    ns_ |= 1
                if dep:
                    if ex & 2: return None
                    ns_ |= 2
                return ns_
            D, _, b2 = bfs(states, adj, h, lambda ns, h=h: ns[0] == h and ns[2] == 3, allowD, psi_k(k), track_psi=False)
            if D is None:
                continue
            bounds_hit = bounds_hit or b1 or b2
            cand = (len(U) + len(D), h, U, D)
            if best is None or cand[0] < best[0]:
                best = cand
        if best is None:
            raise SystemExit('no h_%d' % k)
        hs[k] = best[1]
        cert['h%d' % k] = states[best[1]]
        cert['U%d' % k] = best[2]
        cert['D%d' % k] = best[3]
    # P_0, P_1, P_2: only split = creation into phase k+1, then reach h_{k+1} without split/deposit
    def allowP(k):
        def f(u, v, a, dep, kind, ex):
            if dep: return None
            if a[0] == 'RL':
                if kind == 'create' and ph[v] == k + 1 and ex == 0:
                    return 1
                return None
            if ph[v] != (k if ex == 0 else k + 1): return None
            return ex
        return f
    srcs = {0: s0L, 1: hs[1], 2: hs[2]}
    for k in (0, 1, 2):
        P, _, b = bfs(states, adj, srcs[k], lambda ns, k=k: ns[0] == hs[k + 1] and ns[2] == 1, allowP(k),
                      psi_k(k), track_psi=False)
        bounds_hit = bounds_hit or b
        if P is None:
            raise SystemExit('no P_%d' % k)
        cert['P%d' % k] = P
    for mode in ('i', 'ii'):
        tgt = idx[('FINAL', mode)]
        E, _, b = bfs(states, adj, hs[3], lambda ns, tgt=tgt: ns[0] == tgt,
                      lambda u, v, a, dep, kind, ex: ex if (a[0] != 'RL' and not dep) else None,
                      psi_k(3), track_psi=False)
        bounds_hit = bounds_hit or b
        if E is None:
            raise SystemExit('no E_' + mode)
        cert['E_' + mode] = E
    # verify C1, C2 independently
    report = verify(M, states, cert, hs, s0L)
    with open(outfile, 'x') as fh:
        fh.write(json.dumps({'argv': sys.argv, 'PSIMAX': PSIMAX, 'LMAX': LMAX, 'bounds_hit': bounds_hit}) + '\n')
        fh.write(json.dumps({'verify': report}) + '\n')
        for key in ['U0', 'h1', 'U1', 'D1', 'h2', 'U2', 'D2', 'h3', 'U3', 'D3', 'P0', 'P1', 'P2', 'E_i', 'E_ii']:
            val = cert[key]
            if key.startswith('h'):
                fh.write(json.dumps({key: val}) + '\n')
            else:
                fh.write(json.dumps({key: [{'node': states[n], 'acts': a, 'inc': incs(states[n], a)} for n, a in val]}) + '\n')
    print(json.dumps({'M': M, 'verify': report, 'bounds_hit': bounds_hit,
                      'lengths': {k: len(v) for k, v in cert.items() if not k.startswith('h')}}))

def verify(M, states, cert, hs, s0L):
    """C1/C2: replay each sequence with tg_search.step; the successor of each tick must be the next node
    listed (or, for the last tick, the stated end node); count splits and deposits."""
    idx = {s: i for i, s in enumerate(states)}
    ends = {'U0': s0L, 'U1': hs[1], 'D1': hs[1], 'U2': hs[2], 'D2': hs[2], 'U3': hs[3], 'D3': hs[3],
            'P0': hs[1], 'P1': hs[2], 'P2': hs[3], 'E_i': idx[('FINAL', 'i')], 'E_ii': idx[('FINAL', 'ii')]}
    starts = {'U0': s0L, 'U1': hs[1], 'D1': hs[1], 'U2': hs[2], 'D2': hs[2], 'U3': hs[3], 'D3': hs[3],
              'P0': s0L, 'P1': hs[1], 'P2': hs[2], 'E_i': hs[3], 'E_ii': hs[3]}
    rep = {}
    for key in ends:
        seq = cert[key]
        ok = states[seq[0][0]] == states[starts[key]]
        sp = dp = cr = 0
        for t, (n, a) in enumerate(seq):
            res = T.step(states[n], a, M, False)
            if res is None:
                ok = False; break
            if isinstance(res, tuple):
                res = [res]
            want = states[seq[t + 1][0]] if t + 1 < len(seq) else states[ends[key]]
            match = [info for ns, info in res if ns == want]
            if not match:
                ok = False; break
            info = match[0]
            sp += 1 if a[0] == 'RL' else 0
            dp += 1 if info['deposit'] else 0
            cr += 1 if info['kind'] == 'create' else 0
        rep[key] = {'valid': ok, 'ticks': len(seq), 'splits': sp, 'deposits': dp, 'creations': cr}
    return rep

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
