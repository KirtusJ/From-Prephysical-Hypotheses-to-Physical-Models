#!/usr/bin/env python3
"""Bounded exhaustive search over ALL position product events (no packet model) for the count profiles of
prop:threegroups with q = 1 (delta = 1, gains ignored).

Reduction used (R1): after t steps a walk with e left steps is at site t-2e; e mod M -> site is a bijection onto
the sites reachable at time t, so a mask is an arbitrary subset E of Z_M of deficits, and shifting all deficits by
an integer c is matched by shifting the masks.  A state is the multiset of integer deficits, normalised so that
its least deficit is 0.  One tick with mask E sends a walk at e to e (if e mod M in E) and to e+1 (if (e+1) mod M
in E).

TARGETS (q=1), for sizes (n1,n2,n3) = (|G1|,|G2|,|G3|), not all zero:
  mode (i):  a state whose walks in residues {r-1, r} are exactly n3 at l-1, n1 at l-1+M (residue r-1) and n2 at l
             (residue r); then the final mask {r} gives the profile and kills every other walk.
  mode (ii): exactly n2 at l+M-1 (residue r-1) and n3 at l, n1 at l+M (residue r).
  (Residues r-1 and r are distinct for M >= 2; empty groups impose nothing.)
PREDICATE E1(M, mode, sizes): some state reachable within the bounds meets the target.
BOUNDS (stated, reported if hit): total walks <= WMAX (states above are discarded: the search is then
  incomplete, reported as 'pruned_by_count'), deficit spread <= SMAX (likewise), layers <= LMAX, states <= SCAP.
Hypothesis per case: M >= 2 (residues r-1, r distinct); number qualifying reported.
Usage: tg_exh.py OUTFILE WMAX SMAX LMAX M1 [M2 ...]; result file opened with mode 'x'.  No randomness.
"""
import sys, json
from itertools import product

SCAP = 3_000_000

def step(state, E, M):
    out = {}
    for e, c in state:
        if e % M in E:
            out[e] = out.get(e, 0) + c
        if (e + 1) % M in E:
            out[e + 1] = out.get(e + 1, 0) + c
    if not out:
        return None
    m = min(out)
    return tuple(sorted((e - m, c) for e, c in out.items()))

def meets(state, M, mode, n1, n2, n3):
    d = dict(state)
    byres = {}
    for e, c in state:
        byres.setdefault(e % M, []).append((e, c))
    for r in range(M):
        lo = byres.get((r - 1) % M, []); hi = byres.get(r, [])
        if mode == 'i':
            # residue r: only deficit l with n2; residue r-1: l-1 (n3), l-1+M (n1)
            want_cands = set()
            if n2: want_cands |= {e for e, c in hi}
            if n3: want_cands |= {e + 1 for e, c in lo}
            if n1: want_cands |= {e + 1 - M for e, c in lo}
            for l in want_cands:
                exp_hi = {l: n2} if n2 else {}
                exp_lo = {}
                if n3: exp_lo[l - 1] = n3
                if n1: exp_lo[l - 1 + M] = n1
                if dict(hi) == exp_hi and dict(lo) == exp_lo:
                    return True
        else:
            want_cands = set()
            if n3: want_cands |= {e for e, c in hi}
            if n1: want_cands |= {e - M for e, c in hi}
            if n2: want_cands |= {e + 1 - M for e, c in lo}
            for l in want_cands:
                exp_hi = {}
                if n3: exp_hi[l] = n3
                if n1: exp_hi[l + M] = n1
                exp_lo = {l + M - 1: n2} if n2 else {}
                if dict(hi) == exp_hi and dict(lo) == exp_lo:
                    return True
    return False

def run(M, WMAX, SMAX, LMAX):
    masks = [frozenset(i for i in range(M) if (b >> i) & 1) for b in range(1, 2 ** M)]
    start = ((0, 1),)
    seen = {start}
    layer = [start]
    pruned_count = pruned_spread = 0
    capped = False
    layers_done = 0
    for L in range(LMAX):
        nxt = []
        for s in layer:
            for E in masks:
                t = step(s, E, M)
                if t is None or t in seen:
                    continue
                if sum(c for _, c in t) > WMAX:
                    pruned_count += 1; continue
                if t[-1][0] > SMAX:
                    pruned_spread += 1; continue
                if len(seen) >= SCAP:
                    capped = True; continue
                seen.add(t); nxt.append(t)
        layers_done = L + 1
        layer = nxt
        if not layer:
            break
    return seen, {'layers_done': layers_done, 'frontier_empty': not layer, 'states': len(seen),
                  'pruned_by_count': pruned_count, 'pruned_by_spread': pruned_spread, 'state_cap_hit': capped}

if __name__ == '__main__':
    out, WMAX, SMAX, LMAX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    Ms = [int(a) for a in sys.argv[5:]]
    with open(out, 'x') as fh:
        fh.write(json.dumps({'argv': sys.argv, 'SCAP': SCAP}) + '\n')
        fh.write(json.dumps({'hypothesis_M_ge_2_qualifying': sum(1 for M in Ms if M >= 2), 'of': len(Ms)}) + '\n')
        for M in Ms:
            seen, info = run(M, WMAX, SMAX, LMAX)
            res = {}
            for n1 in range(WMAX + 1):
                for n2 in range(WMAX + 1 - n1):
                    for n3 in range(WMAX + 1 - n1 - n2):
                        if n1 + n2 + n3 == 0: continue
                        for mode in ('i', 'ii'):
                            res['%s:%d,%d,%d' % (mode, n1, n2, n3)] = any(meets(s, M, mode, n1, n2, n3) for s in seen)
            miss = sorted(k for k, v in res.items() if not v)
            line = {'M': M, 'info': info, 'targets': len(res), 'found': sum(res.values()), 'missing': miss}
            fh.write(json.dumps(line) + '\n'); fh.flush()
            print(json.dumps(line))
