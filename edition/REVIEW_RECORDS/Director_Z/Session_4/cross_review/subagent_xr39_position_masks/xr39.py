"""xr39 own check of Position_mask_preparation.md. Integers/Fractions only. Predicates fixed before first run:
P1 after 8 ticks state == {(8,R):(1,0), (-4,R):(1,0)} exactly.
P2 for all 256 targets U,V entries 0..3 (line): final state == {(x,R):U,(x,L):V} (empty entries absent), nothing else anywhere,
   T == 15+6(pR+qL)+5(qR+pL), x == T-20, max layer size <= 5. Pulse order A: corridor0 first; order B: corridor6 first; order C: seeded shuffle.
P3 prefix: targets subset, x_* in -7..7: final state exactly U,V at x_*.
P4 tamper: target U=(1,0),V=0 (order B so corridor-6 pulse occupies ticks 9..14), add position -4 at tick 10 -> R count (2,1).
P5 three-tick: (-1,L)=(1,1), (1,R)=(2,0), nothing else.
P6 rings N=3..30: per N number of 256 targets (order A) exactly realized (state compared mod N); note predicts all pass iff N/gcd(N,2)>11.
P7 deduction: unknowns F_R,F_L on pairs with p+q<=M (M=4..8), equations for all U,V with |U|+|V|<=M; exact nullity == 2.
   P7b same with only three families (V=0 / U=0; V=(1,1); U=(j,0),V=(1,0)) -- measured only.
P8 site-dependent single-input equations on ring N=3..30 for fixed m!=Jm: nullity == 1 (constant, even). measured for all N.
"""
import json, random, itertools, sys
from fractions import Fraction
def step(state, allowed, N=None):
    new = {}
    for (x, r), (p, q) in state.items():
        for d in 'RL':
            nx = x + 1 if d == 'R' else x - 1
            if N: nx %= N
            if nx not in allowed: continue
            pp, qq = (q, p) if (r == 'L' and d == 'L') else (p, q)
            a, b = new.get((nx, d), (0, 0)); new[(nx, d)] = (a + pp, b + qq)
    return new
def run(layers, N=None, start=(0, 'R'), tamper=None):
    st = {((start[0] % N) if N else start[0], start[1]): (1, 0)}
    for t, al in enumerate(layers, 1):
        al = set(al)
        if tamper and t in tamper: al |= tamper[t]
        if N: al = {a % N for a in al}
        st = step(st, al, N)
    return st
def deficits(U, V, order='A', rng=None):
    """list of deficit sets for ticks 1.."""
    L = [{0, d} for d in (1, 2, 3, 3, 4, 5, 6, 6)]
    P = {0, 4, 6, 10}
    neg = lambda b: [P | {b + 1}, P | {b + 2}, P | {b + 3}, set(P), set(P)]
    pos = lambda b: [P | {b + 1}, P | {b + 2}, P | {b + 2}, P | {b + 3}, set(P), set(P)]
    JV = (V[1], V[0])
    pulses = [(0, '+')] * JV[0] + [(0, '-')] * JV[1]
    p6 = [(6, '+')] * U[0] + [(6, '-')] * U[1]
    if order == 'A': pulses = pulses + p6
    elif order == 'B': pulses = p6 + pulses
    else: pulses = pulses + p6; rng.shuffle(pulses)
    for b, s in pulses: L += pos(b) if s == '+' else neg(b)
    L.append({4, 10})
    for i in range(1, 7): L.append({4 + i, 10})
    return L
def layers_from(D, t0=0, x0=0):
    return [{x0 + (t) - 2 * d for d in ds} for t, ds in enumerate(D, 1)]
def prefix(h):
    w = 'R' * h if h >= 0 else 'L' * (1 - h) + 'R'
    if h < 0 and (-h) % 2 == 1: w += 'RLRLLR'
    x = 0; out = []
    for c in w:
        x += 1 if c == 'R' else -1; out.append({x})
    assert x == h
    return out
def want(x, U, V, N=None):
    if N: x %= N
    w = {}
    if U != (0, 0): w[(x, 'R')] = U
    if V != (0, 0): w[(x, 'L')] = V
    return w
def nullity(rows, n):
    rows = [r[:] for r in rows]; rk = 0
    for c in range(n):
        pv = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if pv is None: continue
        rows[rk], rows[pv] = rows[pv], rows[rk]
        pr = rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i][c] != 0:
                f = Fraction(rows[i][c]) / pr[c]
                rows[i] = [a - f * b for a, b in zip(rows[i], pr)]
        rk += 1
    return n - rk
def main():
    res = {}; fails = []
    st = run(layers_from(deficits((0, 0), (0, 0))[:8]))
    res['P1'] = st == {(8, 'R'): (1, 0), (-4, 'R'): (1, 0)}
    targets = [((a, b), (c, d)) for a in range(4) for b in range(4) for c in range(4) for d in range(4)]
    rng = random.Random(39)
    for order in 'ABC':
        ok = 0; first = None; mx = 0
        for U, V in targets:
            D = deficits(U, V, order, rng); T = len(D); mx = max(mx, max(len(s) for s in D))
            good = T == 15 + 6 * (U[0] + V[1]) + 5 * (U[1] + V[0]) and run(layers_from(D)) == want(T - 20, U, V)
            ok += good
            if not good:
                fails.append(['P2', order, U, V]); first = first or [U, V]
        res['P2_' + order] = {'pass': ok, 'of': len(targets), 'first_fail': first, 'max_layer': mx}
    ok = n = 0
    for U, V in [((0, 0), (0, 0)), ((1, 0), (0, 0)), ((0, 0), (0, 1)), ((2, 1), (1, 3)), ((3, 3), (3, 3)), ((0, 2), (1, 0))]:
        for xs in range(-7, 8):
            D = deficits(U, V); T = len(D); h = xs - (T - 20); pre = prefix(h)
            lay = pre + [{h + p for p in s} for s in layers_from(D)]
            n += 1; g = run(lay) == want(xs, U, V); ok += g
            if not g: fails.append(['P3', U, V, xs])
    res['P3'] = {'pass': ok, 'of': n}
    D = deficits((1, 0), (0, 0), 'B')
    st = run(layers_from(D), tamper={10: {-4}}); res['P4'] = {'state': sorted([list(k), list(v)] for k, v in st.items()), 'ok': st == {(1, 'R'): (2, 1)}}
    st = run([{1, -1}, {0}, {1, -1}]); res['P5'] = st == {(-1, 'L'): (1, 1), (1, 'R'): (2, 0)}
    ring = {}
    for N in range(3, 31):
        ok = 0; first = None
        for U, V in targets:
            D = deficits(U, V); T = len(D)
            g = run(layers_from(D), N) == want(T - 20, U, V, N); ok += g
            if not g and first is None: first = [U, V]
            if not g: fails.append(['P6', N, U, V])
        g2 = N // (2 if N % 2 == 0 else 1) > 11
        ring[N] = {'pass': ok, 'of': 256, 'first_fail': first, 'note_predicts_all': g2, 'agree_with_note': (ok == 256) == g2}
    res['P6'] = ring
    ded = {}
    for M in range(4, 9):
        pairs = [(p, q) for p in range(M + 1) for q in range(M + 1 - p) if p + q > 0]
        idx = {(r, m): i for i, (r, m) in enumerate((r, m) for r in 'RL' for m in pairs)}
        def eq(U, V):
            row = [0] * len(idx)
            def add(r, m, c):
                if m != (0, 0): row[idx[(r, m)]] += c
            add('R', (U[0] + V[0], U[1] + V[1]), 1); add('L', (U[0] + V[1], U[1] + V[0]), 1); add('R', U, -2); add('L', V, -2)
            return row
        allp = [(0, 0)] + pairs
        full = [eq(U, V) for U in allp for V in allp if sum(U) + sum(V) <= M]
        three = [eq(U, V) for U in allp for V in allp if sum(U) + sum(V) <= M and (U == (0, 0) or V == (0, 0) or V == (1, 1) or (U[1] == 0 and V == (1, 0)))]
        ded[M] = {'unknowns': len(idx), 'eqs': len(full), 'nullity_full': nullity(full, len(idx)), 'eqs_three': len(three), 'nullity_three': nullity(three, len(idx))}
    res['P7'] = ded
    sp = {}
    for N in range(3, 31):
        # unknowns A_x(m),A_x(Jm),B_x(m),B_x(Jm)
        ix = lambda k, x: 4 * (x % N) + k; rows = []
        for x in range(N):
            for k in (0, 1):  # R input m / Jm
                r = [0] * (4 * N); r[ix(k, x + 1)] += 1; r[ix(2 + k, x - 1)] += 1; r[ix(k, x)] -= 2; rows.append(r)
                r = [0] * (4 * N); r[ix(k, x + 1)] += 1; r[ix(2 + (1 - k), x - 1)] += 1; r[ix(2 + k, x)] -= 2; rows.append(r)
        sp[N] = nullity(rows, 4 * N)
    res['P8'] = sp
    res['failed_predicates_kept'] = fails
    with open(sys.argv[1], 'x') as f: json.dump(res, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in res.items() if k not in ('failed_predicates_kept', 'P6')}, sort_keys=True))
    print({N: (v['pass'], v['agree_with_note'], v['first_fail']) for N, v in ring.items()}); print(len(fails))
main()
