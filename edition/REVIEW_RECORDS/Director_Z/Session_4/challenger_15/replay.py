"""Challenger replay of 'Position preparation for one gain' (own program, from note text only).
PREDICATES (fixed before first run):
 C0 control: q=2 line, length-4 walks: at (0,L) gains {0,0,1}; at (2,L) gains {0}.
 P1 terminal field == exactly U at (x,R) and V at (x,L), nothing elsewhere.
 P1s (weaker, what P_q needs) field at site x equals (U,V).
 P2 daughters one unmasked tick later: (x+1,R)=U+V, (x-1,L)=U+TV, nothing else.
 P3 every mask has <=4 wells.
 P4 core ticks == 3K+5A+6 <= 3K+10(q-1)+6 and A<=2(q-1).
 P5 common clock: total schedule length is a function of (K,q,N,x) only.
 P6 rings q=3: all pass at N=7 (D=7), N=12 (D=6); N=10 (D=5), N=8, N=6, N=5 measured (note: 'open', a failure recorded).
 P7 adversarial: R-assembly five-tick masks WITH wire-4 wells vs WITHOUT (note ambiguous); q=1; K=0; big multiplicity; far sites.
Hypothesis test per instance: target (U,V) are multisets of exponents mod q; ring instance qualifies iff N//gcd(N,2)>=6.
Integers only. seed 20261113 (used only for random adversarial sample).
"""
import sys, json, itertools, random
from math import gcd
from collections import Counter
random.seed(20261113)

def step(field, q, N):
    new = Counter()
    for (x, rail, j), c in field.items():
        xr, xl = x+1, x-1
        if N: xr %= N; xl %= N
        new[(xr, 'R', j)] += c
        new[(xl, 'L', (j + (1 if rail == 'L' else 0)) % q)] += c
    return new
def mask(field, wells):
    return Counter({k: c for k, c in field.items() if k[0] in wells})
def run(masks, q, N):
    f = Counter({(0, 'R', 0): 1})
    for m in masks:
        f = mask(step(f, q, N), m)
    return f

def control():
    f = Counter({(0, 'R', 0): 1})
    for _ in range(4): f = step(f, 2, 0)
    a = sorted(j for (x, r, j), c in f.items() if (x, r) == (0, 'L') for _ in range(c))
    b = sorted(j for (x, r, j), c in f.items() if (x, r) == (2, 'L') for _ in range(c))
    return a, b

ADV = [[0,3,5],[1,3,5],[2,3,5],[2,4,6],[2,4,6]]   # source RLLRR, stocks LRRLR
IDL = [[1,3,5],[1,3,5],[1,3,5],[2,4,6],[2,4,6]]
ADV2 = [[0,3],[1,3],[2,3],[2,4],[2,4]]             # without wire 4 (R assembly reading)
IDL2 = [[1,3],[1,3],[1,3],[2,4],[2,4]]

def schedule(q, U, V, x, N, common, wire4_in_R=True):
    """returns (masks as position sets, info). U,V lists of exponents."""
    K = len(U) + len(V)
    stages = []  # list of (rel masks, origin shift after)
    r = 0; A = 0
    def group(items, W, w4):
        nonlocal r, A
        r0 = r
        for j in sorted(items, key=lambda j: (j-2-r0) % q):
            while r != (j-2) % q:
                stages.append((ADV if w4 else ADV2, 2)); r = (r+1) % q; A += 1
            stages.append(([W+[1], W, W], 0))
    group(U, [0,2], wire4_in_R)
    stages.append(([[0,3],[0,4],[0,4]], 0))
    group(V, [0,2,4], True)
    Atot = A
    if common:
        while Atot < 2*(q-1):
            stages.append((IDL, 2)); Atot += 1
    T0 = 3*K + 5*Atot + 6
    b = 3*K + Atot - 2
    masks = []; nmax = 0
    if N:
        x0 = 0
        coast = (x - b) % N
        pre = 0
    else:
        z = x - b; x0 = z; pos = 0; coast = 0
        if z >= 0: word = 'R'*z; g = 0
        else: word = 'L'*(1-z) + 'R'; g = -z
        u = (-g) % q
        word += 'LLRR'*u
        for ch in word:
            pos += 1 if ch == 'R' else -1
            masks.append({pos})
        assert pos == z
        pre = len(word)
    t = 0; o = 0
    def emit(rel):
        nonlocal t, nmax
        t += 1
        w = {x0 + t - 2*(o+d) for d in rel}
        if N: w = {p % N for p in w}
        nmax = max(nmax, len(rel))
        masks.append(w)
    for rel, sh in stages:
        for m in rel: emit(m)
        o += sh
    for _ in range(coast): emit([0,2,4])
    for m in ([2,4],[3,4],[4]): emit(m)
    return masks, dict(A=A, Atot=Atot, T0=T0, core=t-coast, b=b, pre=pre, coast=coast, nmax=nmax, total=len(masks))

def check(q, U, V, x, N, common, w4=True):
    masks, info = schedule(q, U, V, x, N, common, w4)
    f = run(masks, q, N)
    K = len(U)+len(V)
    xx = x % N if N else x
    want = Counter()
    for j in U: want[(xx,'R',j)] += 1
    for j in V: want[(xx,'L',j)] += 1
    p1 = (f == want)
    p1s = (Counter({k:c for k,c in f.items() if k[0]==xx}) == want)
    d = step(f, q, N)
    wd = Counter()
    xr, xl = xx+1, xx-1
    if N: xr %= N; xl %= N
    for j in U+V: wd[(xr,'R',j)] += 1
    for j in U: wd[(xl,'L',j)] += 1
    for j in V: wd[(xl,'L',(j+1)%q)] += 1
    p2 = (d == wd)
    p3 = info['nmax'] <= 4
    p4 = info['core'] == info['T0'] and info['T0'] <= 3*K+10*(q-1)+6 and info['A'] <= 2*(q-1)
    return dict(p1=p1, p1s=p1s, p2=p2, p3=p3, p4=p4), info, masks, f

def multisets(q, cap):
    for counts in itertools.product(range(cap+1), repeat=q):
        yield [j for j in range(q) for _ in range(counts[j])]

def sweep(q, cap, xs, N, w4=True, label=''):
    res = dict(label=label, q=q, cap=cap, N=N, D=(N//gcd(N,2) if N else None), qualifies=(N==0 or N//gcd(N,2)>=6),
               runs=0, fail=dict(p1=0,p1s=0,p2=0,p3=0,p4=0,p5=0), first_failure=None, maxA=0, max_total=0)
    clock = {}
    for common in (False, True):
        for U in multisets(q, cap):
            for V in multisets(q, cap):
                for x in xs:
                    pr, info, masks, f = check(q, U, V, x, N, common, w4)
                    res['runs'] += 1
                    res['maxA'] = max(res['maxA'], info['A']); res['max_total'] = max(res['max_total'], info['total'])
                    if common:
                        key = (len(U)+len(V), x)
                        if clock.setdefault(key, info['total']) != info['total']:
                            res['fail']['p5'] += 1
                    for k, v in pr.items():
                        if not v:
                            res['fail'][k] += 1
                            if res['first_failure'] is None:
                                res['first_failure'] = dict(pred=k, U=U, V=V, x=x, common=common, info=info,
                                    masks=[sorted(m) for m in masks],
                                    field=sorted([list(k2)+[c] for k2,c in f.items()], key=str))
    return res

if __name__ == '__main__':
    out = sys.argv[1]
    R = dict(seed=20261113, control=None, sweeps=[], adversarial=[])
    a, b = control()
    R['control'] = dict(at_0L=a, at_2L=b, ok=(a == [0,0,1] and b == [0]))
    if not R['control']['ok']:
        print('CONTROL FAILED', a, b); sys.exit(2)
    for q, cap in ((2,2),(3,2),(4,1),(5,1)):
        R['sweeps'].append(sweep(q, cap, [-9, 0, 4], 0, label='line'))
    for N in (7, 12, 10, 8, 6, 5, 9, 14):
        R['sweeps'].append(sweep(3, 1, list(range(N)), N, label='ring q=3 cap1 all sites'))
    for N in (7, 12):
        R['sweeps'].append(sweep(3, 2, [0, 3, N-1], N, label='ring q=3 cap2'))
    # adversarial
    R['adversarial'].append(sweep(3, 2, [-9,0,4], 0, w4=False, label='ADV line: R-assembly five-tick masks without wire-4 wells'))
    R['adversarial'].append(sweep(3, 1, list(range(12)), 12, w4=False, label='ADV ring12: without wire-4 wells'))
    R['adversarial'].append(sweep(1, 3, [-5,0,7], 0, label='ADV q=1 line'))
    R['adversarial'].append(sweep(1, 3, list(range(7)), 7, label='ADV q=1 ring7'))
    R['adversarial'].append(sweep(2, 2, list(range(12)), 12, label='ADV q=2 ring12'))
    R['adversarial'].append(sweep(4, 1, [0,5,11], 12, label='ADV q=4 ring12'))
    R['adversarial'].append(sweep(5, 1, [0,6], 7, label='ADV q=5 ring7'))
    rnd = dict(label='ADV random big multiplicity / far sites / large q', runs=0, fails=0, first=None)
    for _ in range(300):
        q = random.choice([1,2,3,6,7,12,97])
        U = [random.randrange(q) for _ in range(random.randrange(0,7))]
        V = [random.randrange(q) for _ in range(random.randrange(0,7))]
        N = random.choice([0,0,7,12,13,24])
        x = random.randrange(-400, 400) if N == 0 else random.randrange(N)
        common = random.random() < .3 and q <= 12
        pr, info, masks, f = check(q, U, V, x, N, common)
        rnd['runs'] += 1
        if not all(pr.values()):
            rnd['fails'] += 1
            if rnd['first'] is None: rnd['first'] = dict(q=q,U=U,V=V,N=N,x=x,common=common,pr=pr,info=info)
    R['adversarial'].append(rnd)
    with open(out, 'x') as fh:
        json.dump(R, fh, indent=1, sort_keys=True)
    print('control', R['control'])
    for s in R['sweeps'] + R['adversarial'][:-1]:
        ff = s['first_failure']
        print(s['label'], 'q',s['q'],'N',s['N'],'D',s['D'],'qual',s['qualifies'],'runs',s['runs'],'fail',s['fail'],'maxA',s['maxA'],'maxT',s['max_total'],
              '' if ff is None else ('FIRST %s U=%s V=%s x=%s common=%s' % (ff['pred'],ff['U'],ff['V'],ff['x'],ff['common'])))
    print(rnd)
