#!/usr/bin/env python3
"""ev_quantum.py -- Z1-R: the model's weights against sequential quantum measurement, and records.

Model weight (D4): mu(S) = sum over end vertices y of (sum of gains of the walks of S ending at y)^2,
an integer; probability-like value mu(S)/2^t. Unwrapped ring; exact integers throughout.
Quantum comparison: psi_0 = e_(0,R); one step psi -> A psi with A the signed step matrix (U = A/sqrt 2);
a projective read at time s with outcome set A_s applies the projector onto A_s. The unnormalised
sequential probability of the outcomes (A_1..A_t) is ||P_{A_t} A ... P_{A_1} A psi_0||^2 (to be divided
by 2^t), computed by propagating integer vectors, independently of the walk enumeration.

PREDICATES fixed before the first run:
 S1 W1 reproduces: at t=3 the event of all walks but R,L,L has weight 9 (9/8), and it is NOT a vertex
    product event (family b).
 S2 for EVERY vertex product event at t <= 4 the model weight equals the sequential quantum value.
 S3 for every set of read times and the finest (single-vertex) outcomes, and also for single-position
    outcomes, t <= 5, the cell weights sum to 2^t and no cell exceeds 2^t; the same for 300 seeded
    random coarse partitions (a random partition of the vertices at each read time).
 S4 the maximum of mu(S)/2^t over ALL events is > 1 for t = 3 and t = 4, and over vertex product
    events it is exactly 1 for t <= 4.
 S5 (post-processed records) reads at every time, fine outcomes, t=3: for a set E of outcome
    sequences, quantum mechanics gives the sum of the cell probabilities; the model gives mu(union).
    There is an E on which they differ; the complement of the walk R,L,L gives 7/8 against 9/8.
 S6 (the task's expectation, kept as stated) for some s < t <= 5 the weight of the FULL event of
    length t differs from the sum over vertices z of the weights of 'through z at time s'.
    EXPECTED BY THE ATTACKER TO FAIL: both are 2^t by norm preservation.
 S7 (follow-up to S6) for END-VERTEX events: there are t, s < t and y with
    mu(ends at y) != sum_z mu(through z at s and ends at y); the smallest t is 3; none at t <= 2.
 S8 (permanent records) rules additive over single walks, F_y(m) = sum_g a_{y,g} n_g: the consistent
    ones (all events, T=5) form a space of dimension 1 (count) in mode uni and on the ring of 3 sites.
 S9 under the count rule the return weight to (0,R) divided by 2^t is <= 1/2 for all 1 <= t <= 40 on
    the rings of 3, 4, 5, 8 sites; under the model's rule it reaches 1 on the ring of 4 at t=8.
Result file not overwritten.
"""
import sys, os, json, random, itertools
from collections import defaultdict
import ev_classify as E, ev_compare as C
HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261113

def step(psi, N=None):
    out = defaultdict(int)
    for (x, r), a in psi.items():
        xr, xl = x + 1, x - 1
        if N: xr %= N; xl %= N
        out[(xr, 'R')] += a
        out[(xl, 'L')] += (-a if r == 'L' else a)
    return {k: v for k, v in out.items() if v}

def mu(D, t, S):
    v = defaultdict(int); i = 0
    while S:
        if S & 1:
            xs, rs, g = D[t][i]; v[(xs[t], rs[t])] += g
        S >>= 1; i += 1
    return sum(a * a for a in v.values())

def main():
    out = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'ev_quantum_results.json')
    if os.path.exists(out): sys.exit('result file exists, not overwritten: ' + out)
    D = E.walk_data(6, None)
    R = {}
    # S1
    idx = {tuple('R' if (i >> k) & 1 else 'L' for k in range(3)): i for i in range(8)}
    S7walk = 255 ^ (1 << idx[('R', 'L', 'L')])
    famb3 = E.family(D, 'b', 3)
    R['S1'] = dict(weight=mu(D, 3, S7walk), is_product_event=S7walk in famb3,
                   passed=mu(D, 3, S7walk) == 9 and S7walk not in famb3)
    # S2: enumerate tuples of outcome sets directly (not through the family code) for t<=3; for t=4 use masks
    cnt = bad = 0
    for t in range(1, 5):
        vm = [E.masks_by(D, t, s, 'vertex') for s in range(1, t + 1)]
        def rec(s, mask, psi):
            nonlocal cnt, bad
            if s == t:
                cnt += 1
                if mu(D, t, mask) != sum(a * a for a in psi.values()): bad += 1
                return
            p2 = step(psi)
            verts = sorted(vm[s])
            # all subsets of the vertices at time s+1
            for bits in range(1, 1 << len(verts)):
                A = [verts[j] for j in range(len(verts)) if (bits >> j) & 1]
                m2 = 0
                for a in A: m2 |= vm[s][a]
                q = {k: v for k, v in p2.items() if k in A}
                if t == 4 and s < 3 and bits % 3 == 1 and len(verts) > 4:   # thin the enumeration at t=4 (documented)
                    pass
                rec(s + 1, mask & m2, q)
        rec(0, (1 << (1 << t)) - 1, {(0, 'R'): 1})
    R['S2'] = dict(outcome_sequences_checked=cnt, mismatches=bad, passed=bad == 0)
    # S3
    rng = random.Random(SEED); tot_bad = cells_over = npart = 0
    for t in range(1, 6):
        full = (1 << (1 << t)) - 1
        for what in ('vertex', 'pos'):
            for k in range(0, t + 1):
                for times in itertools.combinations(range(1, t + 1), k):
                    cells = [full]
                    for s in times:
                        ms = list(E.masks_by(D, t, s, what).values())
                        cells = [c & m for c in cells for m in ms if c & m]
                    w = [mu(D, t, c) for c in cells]
                    npart += 1
                    if sum(w) != 2 ** t: tot_bad += 1
                    if max(w) > 2 ** t: cells_over += 1
    for _ in range(300):
        t = rng.randint(2, 5); full = (1 << (1 << t)) - 1
        times = [s for s in range(1, t + 1) if rng.random() < 0.6] or [t]
        cells = [full]
        for s in times:
            ms = list(E.masks_by(D, t, s, 'vertex').values())
            nb = rng.randint(1, len(ms)); blocks = [0] * nb
            for m in ms: blocks[rng.randrange(nb)] |= m
            cells = [c & m for c in cells for m in blocks if c & m]
        w = [mu(D, t, c) for c in cells]; npart += 1
        if sum(w) != 2 ** t: tot_bad += 1
        if max(w) > 2 ** t: cells_over += 1
    R['S3'] = dict(partitions=npart, sum_not_total=tot_bad, cell_over_total=cells_over, passed=tot_bad == 0 and cells_over == 0)
    # S4
    mx = {}
    for t in range(1, 5):
        full = (1 << (1 << t)) - 1
        m_all = max(range(1, full + 1), key=lambda S: mu(D, t, S))
        fb = E.family(D, 'b', t)
        m_b = max(fb, key=lambda S: mu(D, t, S))
        n_over = sum(1 for S in range(1, full + 1) if mu(D, t, S) > 2 ** t)
        mx[t] = dict(max_all='%d/%d' % (mu(D, t, m_all), 2 ** t), max_product='%d/%d' % (mu(D, t, m_b), 2 ** t),
                     events=full, product_events=len(fb), events_over_total=n_over,
                     product_events_over_total=sum(1 for S in fb if mu(D, t, S) > 2 ** t))
    R['S4'] = dict(by_length=mx, passed=all(mx[t]['events_over_total'] > 0 for t in (3, 4)) and
                   all(mx[t]['product_events_over_total'] == 0 and mx[t]['max_product'] == '%d/%d' % (2 ** t, 2 ** t) for t in mx))
    # S5: fine reads at every time = single walks, each of quantum probability 1/8; union E: QM |E|/8, model mu(E)/8
    diff = sum(1 for S in range(1, 256) if mu(D, 3, S) != bin(S).count('1'))
    R['S5'] = dict(sets_of_outcome_sequences=255, model_differs_from_quantum=diff,
                   example=dict(E='all but R,L,L', quantum='7/8', model='%d/8' % mu(D, 3, S7walk)),
                   passed=diff > 0 and mu(D, 3, S7walk) == 9)
    # S6, S7
    s6 = []; s7 = []
    for t in range(1, 6):
        full = (1 << (1 << t)) - 1
        endm = E.masks_by(D, t, t, 'vertex')
        for s in range(1, t):
            thr = E.masks_by(D, t, s, 'vertex')
            tot = sum(mu(D, t, m) for m in thr.values())
            if tot != mu(D, t, full): s6.append((t, s, tot))
            for y, my in endm.items():
                parts = sum(mu(D, t, my & m) for m in thr.values())
                if parts != mu(D, t, my): s7.append(dict(t=t, s=s, y=list(y), weight=mu(D, t, my), sum_over_z=parts))
    R['S6'] = dict(counterexamples=s6, passed=len(s6) > 0)
    R['S7'] = dict(number=len(s7), smallest=[e for e in s7 if e['t'] == min(x['t'] for x in s7)],
                   passed=len(s7) > 0 and min(x['t'] for x in s7) == 3)
    # S8: first-order rules: restrict the unknowns to one-element multisets by solving the full system and
    # counting the solutions that are additive over walks: F(m) = sum_g n_g F({g}).
    s8 = {}
    for N in (None, 3):
        DD = E.walk_data(6, N)
        for mode in ('uni', 'per'):
            S, NS = C.space(DD, 'all', 'vertex', 'gain', mode, 5)
            # impose additivity as extra equations: F_k(m) - sum_g n_g F_k({g}) = 0 for every unknown
            rows = list(S.rows)
            miss = 0
            for (rk, ms), j in list(S.unk.items()):
                if sum(c for g, c in ms) == 1: continue
                row = {j: 1}
                for g, c in ms:
                    u = (rk, ((g, 1),))
                    if u not in S.unk: miss += 1; row = None; break
                    row[S.unk[u]] = row.get(S.unk[u], 0) - c
                if row: rows.append(frozenset(row.items()))
            NS2 = E.solve(rows, len(S.unk))
            s8['%s/%s' % (N, mode)] = dict(dim=len(NS2), count_ok=E.satisfies(rows, S.vec('count')),
                                           xcount_ok=E.satisfies(rows, S.vec('xcount')) if mode == 'per' else None,
                                           unknowns_without_singletons=miss)
    R['S8'] = dict(spaces=s8, passed=s8['None/uni']['dim'] == 1 and s8['3/uni']['dim'] == 1 and s8['3/per']['dim'] == 1)
    # S9
    s9 = {}
    for N in (3, 4, 5, 8):
        psi = {(0, 'R'): 1}; cnt_ = {(0, 'R'): 1}; best_c = (0, 0); best_m = (0, 0); first1 = None
        for t in range(1, 41):
            psi = step(psi, N)
            nc = defaultdict(int)
            for (x, r), a in cnt_.items():
                nc[((x + 1) % N, 'R')] += a; nc[((x - 1) % N, 'L')] += a
            cnt_ = nc
            from fractions import Fraction
            fc = Fraction(cnt_.get((0, 'R'), 0), 2 ** t); fm = Fraction(psi.get((0, 'R'), 0) ** 2, 2 ** t)
            if fc > best_c[0]: best_c = (fc, t)
            if fm > best_m[0]: best_m = (fm, t)
            if fm == 1 and first1 is None: first1 = t
        s9[N] = dict(count_max=str(best_c[0]), count_max_at=best_c[1], model_max=str(best_m[0]), model_max_at=best_m[1], model_first_one=first1)
    from fractions import Fraction
    R['S9'] = dict(by_ring=s9, passed=all(Fraction(v['count_max']) <= Fraction(1, 2) for v in s9.values()) and s9[4]['model_first_one'] == 8)
    for k, v in R.items(): print(k, json.dumps(v))
    with open(out, 'x') as f: json.dump(R, f, indent=1)
if __name__ == '__main__': main()
