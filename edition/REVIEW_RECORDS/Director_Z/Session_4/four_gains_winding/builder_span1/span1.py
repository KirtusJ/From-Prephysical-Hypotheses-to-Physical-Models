#!/usr/bin/env python3
"""Two-level preparation in D_delta on rings: exact replay.  Seed 20261113.

Usage: python3 -B span1.py OUTFILE      (OUTFILE is opened with mode 'x')

PREDICATES (fixed before the first run).

P0 (control). N=6, masks {1,5},{2,4},{3}: terminal field is exactly
   (3,R,exp 0,lambda 0):1 and (3,L,exp 2 mod q,lambda 3):1, for q=1..4.

PX (cross-rail winding, the obstruction).  For random position product events
   on rings N=3..10 (masks random subsets of the sites, length <= 2N+4),
   nR(x,l), nL(x,l) = numbers of walks ending at (x,R),(x,L) with lambda=l:
   PX1: for l'-l in M*Z, l'-l >= M :  nL(l)*nR(l') <= nL(l+M)*nR(l'-M)
   PX2: for l'-l in M*Z, l'-l >= 2M:  nR(l)*nL(l') <= nR(l+M)*nL(l'-M)
   Hypothesis counted per case: the left side is > 0 (non-vacuous instances).

PC (three-group construction).  For ring N, order q, site x, mode in {i,ii},
   and three multisets of exponents:
   mode i : request  R: {lambda=l: G_P0}          L: {l: G_Q0, l+M: G_Q1}
   mode ii: request  R: {l: G_P0, l+M: G_P1}      L: {l+M: G_Q1}
   the builder returns site masks, l and T; the replay propagates counts
   indexed (site, rail, exponent, lambda) from (0,R) by the two arcs before
   each mask; the case QUALIFIES iff the WHOLE terminal field (all sites)
   equals the request placed at site x and nothing else.
   Ranges: q in 1..4; every triple of multisets with <= 2 items each for
   q<=2 and <= 1 item each for q in {3,4}; all sites x; rings N=16 (M=8),
   N=9 (M=9), N=11, N=20.  Claim: all qualify.
   Sub-bound rings N in {3,5,6,7,10,12,14} (M=3,5,3,7,5,6,7), sites 0,1:
   no claim; the numbers qualifying and the first failure are recorded.
PR (random larger). 300 cases, q in 1..7, <=5 items per group, N in
   {16,9,17,22,40}, random site, random mode: all qualify.
"""
import sys, json, random, itertools
from collections import defaultdict

def replay(N, q, masks):
    st = {(0, 'R', 0, 0): 1}
    for A in masks:
        nw = defaultdict(int)
        for (s, rail, e, lam), c in st.items():
            s2 = (s + 1) % N
            if s2 in A: nw[(s2, 'R', e, lam)] += c
            s2 = (s - 1) % N
            if s2 in A: nw[(s2, 'L', (e + (1 if rail == 'L' else 0)) % q, lam + 1)] += c
        st = dict(nw)
    return st

CONST = {'i': {'A': ('Q1', 3), 'B': ('P0', 1), 'C': ('Q0', 2)},
         'ii': {'A': ('P1', 2), 'B': ('Q1', 2), 'C': ('P0', 1)}}

def build(N, q, mode, groups, x):
    """groups: dict name->list of exponents.  Returns (site masks, l, T)."""
    M = N // (2 if N % 2 == 0 else 1)
    dm = []                       # deficit masks (unwrapped integers)
    pos = {'S': 0}
    r = 0
    def others(ex=()):
        return [p for k, p in pos.items() if k not in ex]
    def adv():
        s = pos['S']; st = [p for k, p in pos.items() if k != 'S']
        for ds, dk in ((1, 1), (2, 1), (2, 2), (2, 2)):
            dm.append([s + ds] + [p + dk for p in st])
        for k in pos: pos[k] += 2
    def dep(name):
        s = pos['S']; pos.setdefault(name, s + 2)
        assert pos[name] == s + 2
        o = others(('S',))
        dm.append(o + [s, s + 1, s + 2]); dm.append(o + [s, s + 2]); dm.append(o + [s, s + 2])
    def run(name, target):
        if name not in pos: return
        while pos[name] < target:
            o = others((name,))
            dm.append(o + [pos[name] + 1]); dm.append(o + [pos[name] + 1])
            pos[name] += 1
    for slot, runto in (('A', 6), ('B', 4), ('C', 2)):
        name, c = CONST[mode][slot]
        items = sorted(groups.get(name, []), key=lambda j: (j - c - r) % q)
        for j in items:
            while (r + c - j) % q: adv(); r += 1
            dep(name)
        run(name, pos['S'] + runto)
    s = pos.pop('S')
    dm.append(others())                      # kill the source
    A = CONST[mode]['A'][0]; B = CONST[mode]['B'][0]; C = CONST[mode]['C'][0]
    run(A, s + M)
    if A in pos:                             # merge A into residue s+2 by LL, then idle
        o = others((A,))
        dm.append(o + [pos[A] + 1]); dm.append(o + [pos[A] + 2])
        pos[A] += 2
        dm.append(others())
    if mode == 'i':
        l = s + 4
    else:
        run(B, s + M)
        l = s + 2
    T0 = len(dm)
    coast = (x - T0 - 2 + 2 * l) % N
    for _ in range(coast): dm.append(others())
    dm.append([l - 1, l]); dm.append([l])
    masks = [set((t - 2 * d) % N for d in m) for t, m in enumerate(dm, 1)]
    return masks, l, len(dm)

def expected(N, q, mode, groups, x, l):
    M = N // (2 if N % 2 == 0 else 1)
    ex = defaultdict(int)
    place = {'i': {'P0': ('R', l), 'Q0': ('L', l), 'Q1': ('L', l + M)},
             'ii': {'P0': ('R', l), 'P1': ('R', l + M), 'Q1': ('L', l + M)}}[mode]
    for name, (rail, lam) in place.items():
        for j in groups.get(name, []): ex[(x, rail, j % q, lam)] += 1
    return dict(ex)

def case(N, q, mode, groups, x):
    masks, l, T = build(N, q, mode, groups, x)
    return replay(N, q, masks) == expected(N, q, mode, groups, x, l), T, max(len(m) for m in masks)

def msets(q, k):
    out = []
    for n in range(k + 1):
        out += [list(c) for c in itertools.combinations_with_replacement(range(q), n)]
    return out

def main():
    out = open(sys.argv[1], 'x')
    rng = random.Random(20261113)
    res = {'command_line': ' '.join(['python3', '-B'] + sys.argv), 'seed': 20261113}
    # P0
    ctl = {}
    for q in range(1, 5):
        f = replay(6, q, [{1, 5}, {2, 4}, {3}])
        ctl[q] = sorted([list(k) + [v] for k, v in f.items()])
        assert f == {(3, 'R', 0, 0): 1, (3, 'L', 2 % q, 3): 1} if q != 1 else f == {(3, 'R', 0, 0): 1, (3, 'L', 0, 3): 1}
    res['P0_control_field_by_q'] = ctl
    # PX
    px = {'events': 0, 'PX1_instances': 0, 'PX1_fail': 0, 'PX2_instances': 0, 'PX2_fail': 0,
          'PX1_tight': 0, 'fail_examples': []}
    for N in range(3, 11):
        M = N // (2 if N % 2 == 0 else 1)
        for _ in range(400):
            T = rng.randint(1, 2 * N + 4)
            p = rng.choice([0.5, 0.7, 0.85])
            masks = [set(s for s in range(N) if rng.random() < p) for _ in range(T)]
            f = replay(N, 1, masks)
            px['events'] += 1
            n = defaultdict(int)
            for (s, rail, e, lam), c in f.items(): n[(s, rail, lam)] += c
            for (s, rail, lam), c in list(n.items()):
                if rail == 'L':
                    for (s2, rail2, lam2), c2 in list(n.items()):
                        if s2 == s and rail2 == 'R' and lam2 - lam >= M:
                            px['PX1_instances'] += 1
                            rhs = n.get((s, 'L', lam + M), 0) * n.get((s, 'R', lam2 - M), 0)
                            if c * c2 == rhs: px['PX1_tight'] += 1
                            if c * c2 > rhs:
                                px['PX1_fail'] += 1; px['fail_examples'].append([N, [sorted(m) for m in masks]])
                else:
                    for (s2, rail2, lam2), c2 in list(n.items()):
                        if s2 == s and rail2 == 'L' and lam2 - lam >= 2 * M:
                            px['PX2_instances'] += 1
                            if c * c2 > n.get((s, 'R', lam + M), 0) * n.get((s, 'L', lam2 - M), 0):
                                px['PX2_fail'] += 1; px['fail_examples'].append([N, [sorted(m) for m in masks]])
    res['PX'] = px
    # PC
    pc = {}
    for N, sites in [(16, None), (9, None), (11, None), (20, None),
                     (3, [0, 1]), (5, [0, 1]), (6, [0, 1]), (7, [0, 1]), (10, [0, 1]), (12, [0, 1]), (14, [0, 1])]:
        M = N // (2 if N % 2 == 0 else 1)
        rec = {'M': M, 'cases': 0, 'qualify': 0, 'first_fail': None, 'maxT': 0, 'max_mask': 0,
               'fail_by_mode': {'i': 0, 'ii': 0}}
        for q in range(1, 5):
            ms = msets(q, 2 if q <= 2 else 1)
            for mode in ('i', 'ii'):
                names = [CONST[mode][s][0] for s in 'ABC']
                for g in itertools.product(ms, repeat=3):
                    groups = dict(zip(names, g))
                    for x in (sites if sites is not None else range(N)):
                        ok, T, mm = case(N, q, mode, groups, x)
                        rec['cases'] += 1; rec['qualify'] += ok
                        rec['maxT'] = max(rec['maxT'], T); rec['max_mask'] = max(rec['max_mask'], mm)
                        if not ok:
                            rec['fail_by_mode'][mode] += 1
                            if rec['first_fail'] is None:
                                rec['first_fail'] = {'q': q, 'mode': mode, 'groups': groups, 'x': x}
        pc[str(N)] = rec
    res['PC'] = pc
    # PR
    pr = {'cases': 0, 'qualify': 0, 'fails': []}
    for _ in range(300):
        N = rng.choice([16, 9, 17, 22, 40]); q = rng.randint(1, 7); mode = rng.choice(['i', 'ii'])
        names = [CONST[mode][s][0] for s in 'ABC']
        groups = {nm: [rng.randrange(q) for _ in range(rng.randint(0, 5))] for nm in names}
        x = rng.randrange(N)
        ok, T, mm = case(N, q, mode, groups, x)
        pr['cases'] += 1; pr['qualify'] += ok
        if not ok: pr['fails'].append([N, q, mode, groups, x])
    res['PR'] = pr
    json.dump(res, out, indent=1, sort_keys=True); out.close()
    print(json.dumps({'PX': {k: v for k, v in px.items() if k != 'fail_examples'},
                      'PC': {k: [v['M'], v['cases'], v['qualify'], v['fail_by_mode'], v['maxT'], v['max_mask']] for k, v in pc.items()},
                      'PR': [pr['cases'], pr['qualify']]}, indent=0))

if __name__ == '__main__':
    main()
