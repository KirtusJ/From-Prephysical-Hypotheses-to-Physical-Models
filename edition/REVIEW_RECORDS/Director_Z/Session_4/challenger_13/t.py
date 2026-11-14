"""Extension replay of Position_mask_preparation.md (revised). Integers only, seed 20261113. Predicates fixed before first run.
Stated order S: all corridor-0 pulses (store JV) then all corridor-6 pulses (store U); inside a corridor: positives then negatives (variant 'pn').
EXACT(target, N): final state == {(x,R):U,(x,L):V} (empty absent) with x=T-20 (mod N), nothing else anywhere.
Q1 line, all 1296 targets entries 0..5, order S: EXACT; T==15+6(pR+qL)+5(qR+pL); layer width<=5 (record max).
Q2 line, 300 seeded random targets entries 0..20: same.
Q3 rings 23,24,25,26,40, 256 targets entries 0..3, order S: EXACT, T formula, width<=5.
Q4 rings 11,22, 256 targets entries 0..3 AND 1296 entries 0..5, order S: EXACT.
Q5 daughters: after one further free tick (all sites allowed) state == {(x+1,R):U+V,(x-1,L):U+JV} exactly (line all 1296; rings 11,13,22,23,24 for 256).
Q6 within-corridor order variants 'np' (negatives first) and 'sh' (seeded shuffle inside each corridor, corridor order kept): EXACT on line, rings 11,22,13,24 for 256 targets. (note does not state inner order; measured, expectation pass)
Q7 extreme targets: one entry 60 others 0 (4 targets), (60,0),(0,60); (0,60),(60,0); (60,60),(60,60): line, rings 11,13,22,24: EXACT + daughters.
Q8 prefix to prescribed site x_* on rings 11,22,13,24 (x_* all residues) and line x_* in -9..9 for 6 targets: EXACT at x_*.
Q9 measured only: reversed corridor order on rings 11,22 (note says 31/256) ; rings 12, 20 order S (note: no guarantee).
Q10 mid-run invariant on rings 11,22 (order S, 256 targets): at the end of every pulse, state on deficits 4 and 10 equals required partial multisets (R rail only), i.e. the induction the note's proof uses. Deficit 0 surplus measured (max count).
"""
import json, random, sys
def step(state, allowed, N=None):
    new = {}
    for (x, r), (p, q) in state.items():
        for d in 'RL':
            nx = x + 1 if d == 'R' else x - 1
            if N: nx %= N
            if allowed is not None and nx not in allowed: continue
            pp, qq = (q, p) if (r == 'L' and d == 'L') else (p, q)
            a, b = new.get((nx, d), (0, 0)); new[(nx, d)] = (a + pp, b + qq)
    return new
def run(layers, N=None, hook=None):
    st = {(0, 'R'): (1, 0)}
    for t, al in enumerate(layers, 1):
        if N: al = {a % N for a in al}
        st = step(st, al, N)
        if hook: hook(t, st)
    return st
P = {0, 4, 6, 10}
def neg(b): return [P | {b + 1}, P | {b + 2}, P | {b + 3}, set(P), set(P)]
def pos(b): return [P | {b + 1}, P | {b + 2}, P | {b + 2}, P | {b + 3}, set(P), set(P)]
def pulses(U, V, inner='pn', corr='S', rng=None):
    c0 = [(0, '+')] * V[1] + [(0, '-')] * V[0]
    c6 = [(6, '+')] * U[0] + [(6, '-')] * U[1]
    if inner == 'np': c0.reverse(); c6.reverse()
    if inner == 'sh': rng.shuffle(c0); rng.shuffle(c6)
    return c0 + c6 if corr == 'S' else c6 + c0
def deficits(pl):
    L = [{0, d} for d in (1, 2, 3, 3, 4, 5, 6, 6)]; ends = []
    for b, s in pl:
        L += pos(b) if s == '+' else neg(b); ends.append(len(L))
    L.append({4, 10})
    for i in range(1, 7): L.append({4 + i, 10})
    return L, ends
def layers_from(D, h=0, t0=0): return [{h + t - 2 * d for d in ds} for t, ds in enumerate(D, 1)]
def want(x, U, V, N=None):
    if N: x %= N
    w = {}
    if U != (0, 0): w[(x, 'R')] = U
    if V != (0, 0): w[(x, 'L')] = V
    return w
def daughters(x, U, V, N=None):
    a = (U[0] + V[0], U[1] + V[1]); b = (U[0] + V[1], U[1] + V[0]); w = {}
    xr, xl = x + 1, x - 1
    if N: xr %= N; xl %= N
    if a != (0, 0): w[(xr, 'R')] = a; w[(xl, 'L')] = b
    return w
def prefix(h):
    w = 'R' * h if h >= 0 else 'L' * (1 - h) + 'R'
    if h < 0 and (-h) % 2 == 1: w += 'RLRLLR'
    x = 0; out = []
    for c in w: x += 1 if c == 'R' else -1; out.append({x})
    assert x == h; return out
def box(n): return [((a, b), (c, d)) for a in range(n) for b in range(n) for c in range(n) for d in range(n)]
fails = []
def census(name, targets, N=None, inner='pn', corr='S', daughter=False, rng=None):
    ok = dok = 0; first = None; mxw = 0; mxT = 0; tform = 0
    for U, V in targets:
        pl = pulses(U, V, inner, corr, rng); D, _ = deficits(pl); T = len(D)
        lay = layers_from(D)
        w = max(len({a % N for a in s} if N else s) for s in lay); mxw = max(mxw, w); mxT = max(mxT, T)
        tf = T == 15 + 6 * (U[0] + V[1]) + 5 * (U[1] + V[0]); tform += tf
        st = run(lay, N); g = st == want(T - 20, U, V, N) and tf and w <= 5; ok += g
        if not g:
            rec = {'pred': name, 'N': N, 'U': U, 'V': V, 'T': T, 'pulses': pl, 'got': sorted([list(k), list(v)] for k, v in st.items())}
            fails.append(rec); first = first or rec
        if daughter:
            s2 = step(st, None, N); g2 = s2 == daughters(T - 20, U, V, N); dok += g2
            if not g2: fails.append({'pred': name + '_daughter', 'N': N, 'U': U, 'V': V, 'got': sorted([list(k), list(v)] for k, v in s2.items())})
    r = {'pass': ok, 'of': len(targets), 'T_formula_ok': tform, 'max_width': mxw, 'max_T': mxT, 'first_fail': first}
    if daughter: r['daughter_pass'] = dok
    return r
def main():
    res = {}; rng = random.Random(20261113)
    b6 = box(6); b4 = box(4)
    res['Q1_line_0..5'] = census('Q1', b6, daughter=True)
    rt = [((rng.randint(0, 20), rng.randint(0, 20)), (rng.randint(0, 20), rng.randint(0, 20))) for _ in range(300)]
    res['Q2_line_random300'] = census('Q2', rt, daughter=True)
    for N in (23, 24, 25, 26, 40, 13): res['Q3_ring%d' % N] = census('Q3', b4, N, daughter=True)
    for N in (11, 22):
        res['Q4_ring%d_0..3' % N] = census('Q4', b4, N, daughter=True)
        res['Q4_ring%d_0..5' % N] = census('Q4b', b6, N, daughter=True)
    for inner in ('np', 'sh'):
        for N in (None, 11, 22, 13, 24): res['Q6_%s_%s' % (inner, N or 'line')] = census('Q6' + inner, b4, N, inner=inner, rng=rng)
    ext = [((60, 0), (0, 0)), ((0, 60), (0, 0)), ((0, 0), (60, 0)), ((0, 0), (0, 60)), ((60, 0), (0, 60)), ((0, 60), (60, 0)), ((60, 60), (60, 60)), ((0, 0), (0, 0)), ((0, 1), (37, 0)), ((1, 0), (0, 53))]
    for N in (None, 11, 13, 22, 24): res['Q7_extreme_%s' % (N or 'line')] = census('Q7', ext, N, daughter=True)
    q8 = {}
    for N in (None, 11, 22, 13, 24):
        ok = n = 0
        for U, V in [((0, 0), (0, 0)), ((1, 0), (0, 0)), ((0, 0), (0, 1)), ((2, 1), (1, 3)), ((3, 3), (3, 3)), ((0, 2), (1, 0))]:
            D, _ = deficits(pulses(U, V)); T = len(D)
            for xs in (range(-9, 10) if N is None else range(N)):
                hs = [xs - (T - 20)] if N is None else [xs - (T - 20), (xs - (T - 20)) % N, (xs - (T - 20)) % N - N]
                for h in hs:
                    lay = prefix(h) + layers_from(D, h)
                    st = run(lay, N); g = st == want(xs, U, V, N); n += 1; ok += g
                    if not g: fails.append({'pred': 'Q8', 'N': N, 'U': U, 'V': V, 'xs': xs, 'h': h})
        q8[str(N or 'line')] = {'pass': ok, 'of': n}
    res['Q8_prefix'] = q8
    for N in (11, 22): res['Q9_measured_reversed_ring%d' % N] = census('Q9rev', b4, N, corr='B')
    for N in (12, 20, 21, 10): res['Q9_measured_ring%d' % N] = census('Q9small', b4, N)
    q10 = {}
    for N in (11, 22):
        ok = 0; mx0 = 0
        for U, V in b4:
            pl = pulses(U, V); D, ends = deficits(pl); lay = layers_from(D); good = [True]; acc = {4: [0, 0], 10: [0, 0]}; exp = {}
            for (b, s), e in zip(pl, ends):
                acc[b + 4][0 if s == '+' else 1] += 1; exp[e] = (tuple(acc[4]), tuple(acc[10]))
            def hook(t, st):
                nonlocal mx0
                if t in exp:
                    for d, m in zip((4, 10), exp[t]):
                        x = (t - 2 * d) % N
                        if st.get((x, 'R'), (0, 0)) != m or (x, 'L') in st: good[0] = False
                    x0 = t % N
                    for r in 'RL':
                        if (x0, r) in st: mx0 = max(mx0, sum(st[(x0, r)]))
            run(lay, N, hook); ok += good[0]
            if not good[0]: fails.append({'pred': 'Q10', 'N': N, 'U': U, 'V': V})
        q10[str(N)] = {'pass': ok, 'of': 256, 'max_count_at_deficit0_after_a_pulse': mx0}
    res['Q10_invariant'] = q10
    res['failed_predicates_kept'] = fails
    with open(sys.argv[1], 'x') as f: json.dump(res, f, indent=1, sort_keys=True)
    for k, v in res.items():
        if k != 'failed_predicates_kept': print(k, json.dumps({a: b for a, b in v.items() if a != 'first_fail'}), 'FIRST', (v.get('first_fail') or {}).get('U'), (v.get('first_fail') or {}).get('V'))
    print('fails', len(fails))
main()
