"""Consistency check of fixed_ring_calibration.md against the published periods (T_4 = 8, T_8 = 24).
Predicates fixed before the run:
 P1: on N=4 the raw step A satisfies A^4 = 4 * (translation by two sites); smallest t>0 with A^t = c*I is t=8, c=16.
 P2: on N=8 the smallest t>0 with A^t = c*I is t=24, c=4096.
 P3: for N in 3..12 other than 4, 8 no t <= 2000 has A^t proportional to I.
Raw step (specification.md): (u,v) at site x -> u+v to (x+1,R), u-v to (x-1,L). Exact integers.
"""
import json, sys
def step(state, N):
    new = [[0, 0] for _ in range(N)]
    for x in range(N):
        u, v = state[x]
        new[(x + 1) % N][0] += u + v
        new[(x - 1) % N][1] += u - v
    return new
def basis(N):
    out = []
    for x in range(N):
        for c in (0, 1):
            s = [[0, 0] for _ in range(N)]
            s[x][c] = 1
            out.append(s)
    return out
def scalar_multiple_of_identity(states, N):
    c = None
    for i, s in enumerate(states):
        x, ch = divmod(i, 2)
        for y in range(N):
            for d in (0, 1):
                val = s[y][d]
                if (y, d) == (x, ch):
                    if c is None: c = val
                    if val != c: return None
                elif val != 0:
                    return None
    return c
res = {}
for N in range(3, 13):
    states = basis(N)
    first = None
    tmax = 2000
    for t in range(1, tmax + 1):
        states = [step(s, N) for s in states]
        c = scalar_multiple_of_identity(states, N)
        if c is not None and c != 0:
            first = (t, c); break
    res[N] = first
# P1 detail: A^4 on N=4 equals 4 * shift by 2
N = 4
states = basis(N)
for t in range(4):
    states = [step(s, N) for s in states]
ok = True
for i, s in enumerate(states):
    x, ch = divmod(i, 2)
    for y in range(N):
        for d in (0, 1):
            want = 4 if (y, d) == ((x + 2) % N, ch) else 0
            if s[y][d] != want: ok = False
out = {
 "first_scalar_return": {str(k): v for k, v in res.items()},
 "P1_A4_equals_4_shift2_on_N4": ok,
 "P1": ok and res[4] == (8, 16),
 "P2": res[8] == (24, 4096),
 "P3": all(res[n] is None for n in range(3, 13) if n not in (4, 8)),
}
print(json.dumps(out, indent=1))
