#!/usr/bin/env python3
"""Exhaustive search over ALL position product events with gains (carrier D_delta, a=b=c=1, d=delta of order q),
complete for requests with |G1|+|G2|+|G3| <= WMAX by the shrinking lemma (FINDINGS: L-shrink): shrinking every
mask to the sites visited by the final walks keeps the final walks and leaves at most n walks at every time.

State: multiset of (integer deficit e, rail of last step, exponent mod q), deficits normalised to min 0.
Tick with mask E (subset of Z_M of deficits, by reduction R1): (e,rho,g) -> (e,'R',g) if e mod M in E;
-> (e+1,'L',g+[rho=='L']) if (e+1) mod M in E.  Initial state {(0,'R',0)}.
TARGET mode (i): at residues r-1 and r exactly: residue r: n2 walks at deficit l whose exponents form G2 (final
  R step keeps the exponent); residue r-1: walks at l-1 forming G3 and at l-1+M forming G1 after the final L step
  (exponent + [rail==L]).  Mode (ii): residue r: G3 at l, G1 at l+M; residue r-1: G2 at l+M-1 (after L step).
PREDICATE G1(M,q,mode,G): some reachable state (within the bounds) meets the target.  All requests with
  total <= WMAX, multisets of Z_q, both modes.  Hypothesis per case: M >= 2, q >= 1; count reported.
BOUNDS: total walks <= WMAX (complete by L-shrink), spread <= SMAX, layers <= LMAX, states <= SCAP; reported.
Usage: tg_exhg.py OUTFILE q WMAX SMAX LMAX M1 [M2 ...]; result file opened with mode 'x'. No randomness.
"""
import sys, json
from itertools import combinations_with_replacement as cwr
from collections import Counter

SCAP = 4_000_000

def step(state, E, M, q):
    out = Counter()
    for (e, rho, g), c in state:
        if e % M in E:
            out[(e, 'R', g)] += c
        if (e + 1) % M in E:
            out[(e + 1, 'L', (g + (1 if rho == 'L' else 0)) % q)] += c
    if not out:
        return None
    m = min(k[0] for k in out)
    return tuple(sorted(((e - m, r, g), c) for (e, r, g), c in out.items()))

def finals(state, M, q):
    """for each r, the multiset of final (rail, lambda, exponent) for mask {r}; lambda relative."""
    res = {}
    for r in range(M):
        f = Counter()
        for (e, rho, g), c in state:
            if e % M == r:
                f[('R', e, g)] += c
            elif (e + 1) % M == r:
                f[('L', e + 1, (g + (1 if rho == 'L' else 0)) % q)] += c
        if f:
            res[r] = f
    return res

def key_profile(f, M, mode):
    """normalise a final multiset into (G1,G2,G3) if it has the shape of the mode, else None."""
    items = list(f.items())
    lams = sorted({k[1] for k in f})
    # try every l
    out = []
    for l in set(lams) | {x - M for x in lams}:
        G1, G2, G3 = [], [], []
        ok = True
        for (rail, lam, g), c in items:
            if mode == 'i':
                if rail == 'R' and lam == l: G2 += [g] * c
                elif rail == 'L' and lam == l: G3 += [g] * c
                elif rail == 'L' and lam == l + M: G1 += [g] * c
                else: ok = False; break
            else:
                if rail == 'R' and lam == l: G3 += [g] * c
                elif rail == 'R' and lam == l + M: G1 += [g] * c
                elif rail == 'L' and lam == l + M: G2 += [g] * c
                else: ok = False; break
        if ok:
            out.append((tuple(sorted(G1)), tuple(sorted(G2)), tuple(sorted(G3))))
    return out

def run(M, q, WMAX, SMAX, LMAX):
    masks = [frozenset(i for i in range(M) if (b >> i) & 1) for b in range(1, 2 ** M)]
    start = (((0, 'R', 0), 1),)
    seen = {start}; layer = [start]
    pc = ps = 0; capped = False; L = 0
    for L in range(1, LMAX + 1):
        nxt = []
        for s in layer:
            for E in masks:
                t = step(s, E, M, q)
                if t is None or t in seen: continue
                if sum(c for _, c in t) > WMAX: pc += 1; continue
                if max(k[0] for k, _ in t) > SMAX: ps += 1; continue
                if len(seen) >= SCAP: capped = True; continue
                seen.add(t); nxt.append(t)
        layer = nxt
        if not layer: break
    met = {'i': set(), 'ii': set()}
    for s in seen:
        for r, f in finals(s, M, q).items():
            for mode in ('i', 'ii'):
                for p in key_profile(f, M, mode):
                    met[mode].add(p)
    return met, {'layers': L, 'frontier_empty': not layer, 'states': len(seen), 'pruned_by_count': pc,
                 'pruned_by_spread': ps, 'state_cap_hit': capped}

def all_requests(q, WMAX):
    ms = {n: list(cwr(range(q), n)) for n in range(WMAX + 1)}
    for n1 in range(WMAX + 1):
        for n2 in range(WMAX + 1 - n1):
            for n3 in range(WMAX + 1 - n1 - n2):
                if n1 + n2 + n3 == 0: continue
                for a in ms[n1]:
                    for b in ms[n2]:
                        for c in ms[n3]:
                            yield (a, b, c)

if __name__ == '__main__':
    out, q, WMAX, SMAX, LMAX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    Ms = [int(a) for a in sys.argv[6:]]
    with open(out, 'x') as fh:
        fh.write(json.dumps({'argv': sys.argv, 'SCAP': SCAP}) + '\n')
        fh.write(json.dumps({'hypothesis_qualifying': sum(1 for M in Ms if M >= 2 and q >= 1), 'of': len(Ms)}) + '\n')
        for M in Ms:
            met, info = run(M, q, WMAX, SMAX, LMAX)
            reqs = list(all_requests(q, WMAX))
            miss = {mode: [r for r in reqs if r not in met[mode]] for mode in ('i', 'ii')}
            line = {'M': M, 'q': q, 'info': info, 'requests_per_mode': len(reqs),
                    'missing_count': {m: len(v) for m, v in miss.items()},
                    'missing_first': {m: v[:30] for m, v in miss.items()}}
            fh.write(json.dumps(line) + '\n'); fh.flush()
            print(json.dumps(line)[:1500])
