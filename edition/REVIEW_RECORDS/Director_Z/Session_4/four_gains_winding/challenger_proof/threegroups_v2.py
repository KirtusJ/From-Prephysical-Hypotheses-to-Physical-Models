#!/usr/bin/env python3
"""Reviewer's replay of Proposition prop:threegroups from the draft text alone.
Command: python3 threegroups.py OUTFILE MODE   (MODE = main | small)
Seed 20261115. Result file opened with 'x'.

PREDICATES (fixed before first run):
 H  (hypothesis, per case): M=N/gcd(N,2) >= 8 [main] ; counted. In 'small' M<8 on purpose.
 P1 whole terminal field: walks exist only at site x; mode (i): (x,R) = G2 all at one lam=l,
    (x,L) = G3 at lam=l plus G1 at lam=l+M; mode (ii): (x,R)=G3 at l plus G1 at l+M, (x,L)=G2 at l+M.
    Gains compared as multisets of exponents mod q. Nothing at any other site.
 P2 l equals the text's value: sigma+4 in mode (i), sigma+2 in mode (ii), sigma = 2*(number of advances).
 P3 packet level, every tick: the set of admitted candidates (mod M) equals the intended row set (no refused
    candidate admitted, no intended candidate rejected).
 P4 packet level, every tick: every non-intended candidate is in the text's refused list for that stage/tick
    (compared mod M). Failure = omission in the text (GAP), even if refused.
 P5 run side condition as worded: no other packet at k+1 or k+2 mod M and no two others adjacent mod M.
 P6 advances per group <= q-1.
 P7 at each stage boundary every packet arrived by R.
 P8 all relative deficits (integers) lie in 0..9 (Frame sentence). Recorded max.
Counts propagated independently of the packet bookkeeping: state (site, rail, gain exp mod q, lam integer),
both arcs applied, then mask sites {(t-2(O+e)) mod N}.
"""
import sys, json, random, itertools, math
from collections import Counter, defaultdict

def gen(N, q, G, mode, x, log):
    """yield (stage, tick, O, maskEntries) ; maintain packets; log packet-level predicates."""
    M = N // math.gcd(N, 2)
    A, B, C = G
    st = {'t': 0, 'O': 0, 'adv': 0, 'r': 0}
    pk = {}   # name -> [entry, last]
    pk['src'] = [0, 'R']
    def tick(stage, tk, mask, moves, refused, spawn=None):
        # moves: name -> step ; spawn: (newname, from, step)
        msk = set(e % M for e in mask)
        intended = set(); cands = []
        for n, (e, last) in pk.items():
            for s in 'RL':
                c = e + (s == 'L')
                isint = bool((moves.get(n) == s) or (spawn and spawn[1] == n and spawn[2] == s))
                cands.append((n, e, last, s, c, isint))
        cfg = (stage, tk, tuple(sorted((e, l) for e, l in pk.values())))
        for (n, e, last, s, c, isint) in cands:
            adm = (c % M) in msk
            if adm != isint:
                log['P3_fail'].append(dict(N=N, M=M, q=q, mode=mode, stage=stage, tick=tk, packet=n, entry=e, last=last, step=s, cand=c, admitted=adm, intended=isint, mask=sorted(mask), cfg=str(cfg)))
            if not isint:
                log['P4_checked'] += 1
                if (c % M) not in set(r % M for r in refused):
                    log['P4_fail'][json.dumps(dict(M=M, stage=stage, tick=tk, cand=c, packet=n, cfg=str(cfg)))] += 1
        log['cfgs'].add((M,) + cfg)
        new = {}
        for n, (e, last) in pk.items():
            if n in moves:
                s = moves[n]; new[n] = [e + (s == 'L'), s]
        if spawn: new[spawn[0]] = [pk[spawn[1]][0] + (spawn[2] == 'L'), spawn[2]]
        for n, (e, l) in list(pk.items()) + list(new.items()):
            log['maxdef'] = max(log['maxdef'], e)
        pk.clear(); pk.update(new)
        st['t'] += 1
        return (stage, tk, st['O'], set(mask))
    def boundary(stage):
        for n, (e, l) in pk.items():
            if l != 'R': log['P7_fail'].append(dict(N=N, stage=stage, packet=n))
    def stocks(): return [n for n in pk if n != 'src']
    def advance():
        ks = [pk[n][0] for n in stocks()]
        names = stocks()
        mv = lambda s_src, s_st: dict([('src', s_src)] + [(n, s_st) for n in names])
        yield tick('advance', 1, {1} | {k+1 for k in ks}, mv('L', 'L'), {0} | set(ks))
        yield tick('advance', 2, {2} | {k+1 for k in ks}, mv('L', 'R'), {1} | {k+2 for k in ks})
        yield tick('advance', 3, {2} | {k+2 for k in ks}, mv('R', 'L'), {3} | {k+1 for k in ks})
        yield tick('advance', 4, {2} | {k+2 for k in ks}, mv('R', 'R'), {3} | {k+3 for k in ks})
        st['O'] += 2; st['adv'] += 1; st['r'] += 1
        for n in pk: pk[n][0] -= 2
        boundary('advance')
    def deposit(idx):
        names = stocks(); ks = [pk[n][0] for n in names]
        mv = dict([('src', 'R')] + [(n, 'R') for n in names])
        cp = 'cp%d' % idx
        yield tick('deposit', 1, {0, 1, 2} | set(ks), mv, {k+1 for k in ks}, spawn=(cp, 'src', 'L'))
        mv2 = dict(mv); mv2[cp] = 'L'
        yield tick('deposit', 2, {0, 2} | set(ks), mv2, {k+1 for k in ks} | {1})
        mv3 = dict(mv); mv3[cp] = 'R'
        yield tick('deposit', 3, {0, 2} | set(ks), mv3, {k+1 for k in ks} | {1, 3})
        boundary('deposit')
    def run(names, label):
        # all packets in names share an entry k; move k -> k+1
        k = pk[names[0]][0]
        oth = [pk[n][0] for n in pk if n not in names]
        om = set(j % M for j in oth)
        ok = ((k+1) % M not in om) and ((k+2) % M not in om) and not any((j+1) % M in om for j in oth)
        log['P5_checked'] += 1
        if not ok: log['P5_fail'].append(dict(N=N, M=M, run=label, k=k, others=sorted(oth)))
        mv = lambda s: dict([(n, s if n in names else 'R') for n in pk])
        yield tick('run:' + label, 1, {k+1} | set(oth), mv('L'), {k} | {j+1 for j in oth})
        yield tick('run:' + label, 2, {k+1} | set(oth), mv('R'), {k+2} | {j+1 for j in oth})
        boundary('run')
    def group(items, c, tag):
        r0 = st['r']; a0 = st['adv']
        its = sorted(items, key=lambda j: (j - c - r0) % q)
        for i, j in enumerate(its):
            while (st['r'] - (j - c)) % q: yield from advance()
            yield from deposit(len(pk))
        if st['adv'] - a0 > q - 1: log['P6_fail'].append(dict(q=q, items=items, adv=st['adv'] - a0))
        return
    cA, cB, cC = (3, 1, 2) if mode == 1 else (2, 2, 1)
    nA = nB = nC = []
    if A:
        yield from group(A, cA, 'A'); nA = stocks()
        for _ in range(4): yield from run(nA, 'A2to6')
    if B:
        yield from group(B, cB, 'B'); nB = [n for n in stocks() if n not in nA]
        for _ in range(2): yield from run(nB, 'B2to4')
    if C:
        yield from group(C, cC, 'C'); nC = [n for n in stocks() if n not in nA and n not in nB]
    # removal
    names = stocks(); ks = [pk[n][0] for n in names]
    yield tick('removal', 1, set(ks), dict((n, 'R') for n in names), {0, 1} | {k+1 for k in ks})
    sigma = st['O']
    if A:
        for _ in range(M - 6): yield from run(nA, 'A6toM')
        e0 = pk[nA[0]][0]
        oth = [pk[n][0] for n in pk if n not in nA]
        mv = lambda s: dict((n, s if n in nA else 'R') for n in pk)
        yield tick('merge', 1, {e0+1} | set(oth), mv('L'), {e0} | {j+1 for j in oth})
        yield tick('merge', 2, {e0+2} | set(oth), mv('L'), {e0+1} | {j+1 for j in oth})
        yield tick('merge', 3, {e0+2} | set(oth), mv('R'), {j+1 for j in oth})
        boundary('merge')
    if mode == 2 and B:
        for _ in range(M - 4): yield from run(nB, 'B4toM')
    p = 4 if mode == 1 else 2
    # coast: final site = (t+c+2 - 2(O+p)) mod N = x
    c = (x - (st['t'] + 2 - 2 * (st['O'] + p))) % N
    for i in range(c):
        ks = [pk[n][0] for n in pk]
        yield tick('coast', 1, set(ks), dict((n, 'R') for n in pk), set())
    up = nB if mode == 1 else nC + nA   # at p
    lo = nC + nA if mode == 1 else nB   # at p-2
    mv = lambda: dict([(n, 'R') for n in up] + [(n, 'L') for n in lo])
    yield tick('end', 1, {p-1, p}, mv(), {p-2, p+1})
    yield tick('end', 2, {p}, mv(), {p-1, p+1})
    st['sigma'] = sigma
    log['st'] = st

def replay(N, q, G, mode, x, log):
    M = N // math.gcd(N, 2)
    field = Counter({(0, 'R', 0, 0): 1}); t = 0
    for (stage, tk, O, mask) in gen(N, q, G, mode, x, log):
        t += 1
        sites = set((t - 2 * (O + e)) % N for e in mask)
        nf = Counter()
        for (s, rail, g, lam), n in field.items():
            s1 = (s + 1) % N
            if s1 in sites: nf[(s1, 'R', g, lam)] += n
            s2 = (s - 1) % N
            if s2 in sites: nf[(s2, 'L', (g + (rail == 'L')) % q, lam + 1)] += n
        field = nf
    st = log['st']; sigma = st['sigma']
    A, B, C = G
    l = sigma + (4 if mode == 1 else 2)
    exp = Counter()
    def put(rail, items, lam):
        for j in items: exp[(x % N, rail, j % q, lam)] += 1
    if mode == 1: put('R', B, l); put('L', C, l); put('L', A, l + M)
    else: put('R', C, l); put('R', A, l + M); put('L', B, l + M)
    ok2 = (field == exp)
    # P1: exists l'
    ok1 = ok2
    if not ok2:
        for d in range(-3 * M, 3 * M + 1):
            e2 = Counter({(s, r, g, lam + d): n for (s, r, g, lam), n in exp.items()})
            if e2 == field: ok1 = True
    return ok1, ok2, field, exp, t

def multisets(q, k):
    out = []
    for n in range(k + 1):
        out += [list(c) for c in itertools.combinations_with_replacement(range(q), n)]
    return out

def main():
    out, MODE = sys.argv[1], sys.argv[2]
    f = open(out, 'x')
    rng = random.Random(20261115)
    reqs = []
    for q in (1, 2):
        ms = multisets(q, 2)
        reqs += [(q, g) for g in itertools.product(ms, ms, ms)]
    for q in (3, 4):
        ms = multisets(q, 1)
        reqs += [(q, g) for g in itertools.product(ms, ms, ms)]
    nexh = len(reqs)
    for _ in range(200):
        q = rng.randint(1, 4)
        reqs.append((q, tuple([rng.randrange(q) for _ in range(rng.randint(0, 4))] for _ in range(3))))
    if MODE == 'main':
        rings = [(16, list(range(16))), (9, list(range(9))), (11, [0, 4, 10]), (18, [0, 7, 17]), (24, [0, 11, 23]), (13, [0, 5, 12]), (20, [0, 9, 19]), (40, [0, 21, 39])]
    else:
        rings = [(7, [0, 3, 6]), (14, [0, 5, 13]), (12, [0, 5, 11]), (6, [0, 2, 5])]
    res = dict(command=' '.join(sys.argv), seed=20261115, n_requests=len(reqs), n_exhaustive=nexh, rings=[r[0] for r in rings], per_ring={})
    for N, xs in rings:
        M = N // math.gcd(N, 2)
        log = dict(P3_fail=[], P4_fail=Counter(), P4_checked=0, P5_fail=[], P5_checked=0, P6_fail=[], P7_fail=[], maxdef=0, cfgs=set())
        cnt = dict(cases=0, H_qualify=0, P1_fail=0, P2_fail=0); ex = []; first = None
        for (q, G) in reqs:
            for mode in (1, 2):
                for x in xs:
                    cnt['cases'] += 1; cnt['H_qualify'] += (M >= 8)
                    n3 = len(log['P3_fail'])
                    ok1, ok2, field, exp, T = replay(N, q, G, mode, x, log)
                    if not ok1:
                        cnt['P1_fail'] += 1
                        if len(ex) < 3: ex.append(dict(q=q, G=G, mode=mode, x=x, T=T, got=sorted((str(k), v) for k, v in field.items()), want=sorted((str(k), v) for k, v in exp.items())))
                    if not ok2: cnt['P2_fail'] += 1
                    if first is None and len(log['P3_fail']) > n3:
                        first = dict(q=q, G=G, mode=mode, x=x, first_P3=log['P3_fail'][n3])
        stages = Counter((c[1], c[2]) for c in log['cfgs'])
        byrun = Counter(d['run'] for d in log['P5_fail'])
        byst = Counter((d['stage'], d['tick']) for d in log['P3_fail'])
        res['per_ring'][N] = dict(M=M, **cnt, P3_fail=len(log['P3_fail']), P3_fail_by_stage_tick=sorted((str(k), v) for k, v in byst.items()), P3_first=first,
            P4_checked=log['P4_checked'], P4_fail_distinct=len(log['P4_fail']), P4_fail_examples=sorted(log['P4_fail'].items())[:12],
            P4_fail_by_stage=sorted(Counter((json.loads(k)['stage'], json.loads(k)['tick']) for k in log['P4_fail']).items()),
            P5_checked=log['P5_checked'], P5_fail=len(log['P5_fail']), P5_fail_by_run=sorted(byrun.items()), P5_examples=log['P5_fail'][:3],
            P6_fail=len(log['P6_fail']), P7_fail=len(log['P7_fail']), P8_max_relative_deficit=log['maxdef'],
            distinct_configs=len(log['cfgs']), configs_by_stage_tick=sorted((str(k), v) for k, v in stages.items()), P1_examples=ex)
        print(N, M, cnt, 'P3', len(log['P3_fail']), 'P4', len(log['P4_fail']), 'P5', len(log['P5_fail']), 'P6', len(log['P6_fail']), 'P7', len(log['P7_fail']), 'maxdef', log['maxdef'], flush=True)
    json.dump(res, f, indent=1, default=str); f.close()
main()
