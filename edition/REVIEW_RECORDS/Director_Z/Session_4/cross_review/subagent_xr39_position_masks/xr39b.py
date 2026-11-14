"""Follow-up to xr39.py (first run kept; its P6 used pulse order A only). Predicates fixed before run:
Q1 rings N=3..30, orders A (corridor 0 first), B (corridor 6 first), C (seeded shuffle): count of 256 targets exactly realized.
   Expectation from note: all pass iff N/gcd(N,2)>11. Observed in run 1: N=11,22 pass under order A (note's criterion says not covered).
Q2 rings N=11,13,22,24 with prefix to every x_* in 0..N-1 for 4 targets, order A: exact.
"""
import json, sys, random, importlib.util
src = open('/tmp/claude-0/-home-user/1b3e59a6-be8f-5e36-be7c-26b1885eea91/scratchpad/xr39/xr39.py').read().rsplit('\nmain()', 1)[0]
exec(src)
targets = [((a, b), (c, d)) for a in range(4) for b in range(4) for c in range(4) for d in range(4)]
res = {'Q1': {}, 'Q2': {}}
for N in range(3, 31):
    for o in 'ABC':
        rng = random.Random(39); ok = 0; first = None
        for U, V in targets:
            D = deficits(U, V, o, rng); T = len(D); g = run(layers_from(D), N) == want(T - 20, U, V, N); ok += g
            if not g and first is None: first = [U, V]
        res['Q1'][f'{N}{o}'] = [ok, first]
for N in (11, 13, 22, 24):
    ok = n = 0
    for U, V in [((1, 0), (0, 0)), ((0, 0), (0, 1)), ((2, 1), (1, 3)), ((3, 3), (3, 3))]:
        for xs in range(N):
            D = deficits(U, V); T = len(D)
            for h in (xs - (T - 20), xs - (T - 20) - 5 * N):
                lay = prefix(h) + [{h + p for p in s} for s in layers_from(D)]
                n += 1; ok += run(lay, N) == want(xs, U, V, N)
    res['Q2'][N] = [ok, n]
json.dump(res, open(sys.argv[1], 'x'), indent=1)
print({k: v for k, v in res['Q1'].items() if v[0] > 1}); print(res['Q2'])
