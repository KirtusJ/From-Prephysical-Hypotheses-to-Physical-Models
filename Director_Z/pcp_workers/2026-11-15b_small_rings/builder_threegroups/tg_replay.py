#!/usr/bin/env python3
"""Replay of packet-model schedules for prop:threegroups on the actual ring Z_N.

For given M, the packet graph of tg_search.py (restricted=False) is built.  A request is
(N, x, q, mode, G1, G2, G3) with G_i multisets of Z_q (exponents of delta).  The planner searches the
product of the packet graph with the exponents mod q of S, of the copy in transit D, and the cumulative
increments a_A, a_B, a_C of the three stocks, for a schedule meeting the request (guess f of the final
cumulative increments, deposit condition e_new - a_X == g - f_X, end condition a_X == f_X); then the
masks are generated on Z_N from the absolute deficits of the packets that hold walks (empty groups are
deleted: their landings are left out of the masks and the split that would create them is not made),
preceded by k right steps so that the final site is x.

PREDICATES (fixed before the first run):
  Q0 (hypothesis per request): N in {M, 2M} with M = N/gcd(N,2), q >= 1, x in Z_N, G_i multisets of Z_q.
     Count of requests qualifying is reported.
  Q1 (planner): a schedule is found.  (A planner failure is reported, not counted as a counterexample.)
  Q2 (replay, the predicate that matters): simulating every walk from (0,R) on Z_N with these masks and the
     gains of D_delta (a=b=c=1, d=delta, exponents mod q), the walks at time T are exactly: at site x,
     on R the multiset G2 at one level l and on L G3 at level l and G1 at level l+M (mode i), or on R
     G3 at l and G1 at l+M and on L G2 at l+M (mode ii); no walk at any other site.  Exact comparison of
     multisets of (rail, lambda, exponent).  l is read off and must be the same for all groups.
Requests: drawn with random.Random(20261113): sizes 0..3, q in 1..4, both modes, x uniform; plus all
  8 emptiness patterns with q = 2.  Usage: tg_replay.py OUTFILE M NREQ.  Result file opened with mode 'x'.
"""
import sys, json, random
from collections import deque, Counter
import tg_search as T

STOCK_OF_PHASE = T.STOCK_OF_PHASE

def build(M):
    out, states, edges, good = T.analyse(M, False)
    idx = {s: i for i, s in enumerate(states)}
    adj = [[] for _ in states]
    for (u, v, dS, dep, kind, acts) in edges:
        adj[u].append((v, acts, dep, kind))
    return out, states, adj, good

def incs(state, acts):
    """increments per label for this tick (1 iff L from rail L).  Mixed-rail packets only step L in
    phases 4-5, where groups inside CA are tracked separately (C-part and A-part rails)."""
    phase, packets = state
    d = {}
    for (lab, pos, rail), a in zip(packets, acts):
        d[lab] = 1 if (a == 'L' and rail == 'L') else 0
    return d

def plan(M, states, adj, good, req, f):
    q = req['q']; mode = req['mode']
    G = {'A': list(req['G1']), 'B': list(req['G2']), 'C': list(req['G3'])}
    # CA rails: track rails of C-part and A-part separately in phases 4,5 to get increments right
    # full planner state: (node, eS, eD, aA, aB, aC, railC, railA, stage, ndep)
    # stage: 0..3 phase being filled; ndep deposits done into current phase stock
    start = (0, 0, None, 0, 0, 0, None, None)
    # we plan segment by segment
    cur = start
    ticks = []
    order = []
    for k in (1, 2, 3):
        X = STOCK_OF_PHASE[k]
        for g in G[X]:
            order.append((k, X, g))
    # BFS segment to next deposit
    def nxt(cs, k, X, g, first):
        # BFS from cs over edges staying in phases <= k, until a deposit/creation into X meeting the condition
        seen = {cs: None}
        dq = deque([cs])
        while dq:
            s = dq.popleft()
            node, eS, eD, aA, aB, aC, rC, rA = s
            st = states[node]
            ph = st[0]
            for (v, acts, dep, kind) in adj[node]:
                sv = states[v]
                pv = sv[0]
                if pv == 'FINAL' or pv > k:
                    if not (first and kind == 'create' and pv == k):
                        continue
                if pv < ph:
                    continue
                inc = incs(st, acts)
                Srail = [p[2] for p in st[1] if p[0] == 'S'][0] if ph <= 3 else None
                a = {'A': aA, 'B': aB, 'C': aC}
                for lab in ('A', 'B', 'C'):
                    if lab in inc:
                        a[lab] = (a[lab] + inc[lab]) % q
                labs_before = [p[0] for p in st[1]]
                labs_after = [p[0] for p in sv[1]]
                neS = (eS + inc.get('S', 0)) % q
                neD = eD
                made_copy = (acts[0] == 'RL')
                copy_e = (eS + (1 if Srail == 'L' else 0)) % q if made_copy else None
                hit = False
                if 'D' in labs_before:
                    neD = (eD + inc['D']) % q
                if made_copy and 'D' in labs_after and 'D' not in labs_before:
                    neD = copy_e
                if kind == 'create' and pv == k and first:
                    e_new = copy_e
                    a[X] = 0
                    if (e_new - a[X] - (g - f[X])) % q == 0:
                        hit = True
                    else:
                        continue
                elif dep and ph == k:
                    if 'D' in labs_before and 'D' not in labs_after:
                        e_new = neD
                    else:
                        e_new = copy_e
                    if not first and (e_new - a[X] - (g - f[X])) % q == 0:
                        hit = True
                    else:
                        continue
                if 'D' not in labs_after:
                    neD = None
                ns = (v, neS, neD, a['A'], a['B'], a['C'], None, None)
                if hit and v not in (coreach[k] if kind == 'create' else good[k]):
                    continue
                if hit:
                    path = [(node, acts)]
                    p = s
                    while seen[p] is not None:
                        pp, pacts = seen[p]
                        path.append((pp[0], pacts))
                        p = pp
                    path.reverse()
                    return ns, path
                if ns not in seen:
                    seen[ns] = (s, acts)
                    dq.append(ns)
        return None, None
    # coreach[k]: phase-k nodes from which good[k] is reached by edges inside phase k that are not deposits
    coreach = {}
    for kk in (1, 2, 3):
        rev = {}
        for u in range(len(states)):
            if states[u][0] != kk: continue
            for (v, acts, dep, kind) in adj[u]:
                if states[v][0] == kk and not dep:
                    rev.setdefault(v, []).append(u)
        cr = set(good[kk]); dq = deque(cr)
        while dq:
            y = dq.popleft()
            for x in rev.get(y, []):
                if x not in cr: cr.add(x); dq.append(x)
        coreach[kk] = cr
    done = {1: 0, 2: 0, 3: 0}
    for (k, X, g) in order:
        first = (done[k] == 0)
        ns, path = nxt(cur, k, X, g, first)
        if ns is None:
            return None
        ticks.extend(path)
        cur = ns
        done[k] += 1
    # empty groups: their stocks must still be created (virtually) to keep the model's phases
    # handled by a final BFS that may create stocks without condition, then kill, lap, final with a == f
    def finish(cs):
        seen = {cs: None}
        dq = deque([cs])
        while dq:
            s = dq.popleft()
            node, eS, eD, aA, aB, aC, rC, rA = s
            st = states[node]
            ph = st[0]
            for (v, acts, dep, kind) in adj[node]:
                sv = states[v]
                pv = sv[0]
                if dep:
                    continue
                if kind == 'create':
                    lab = STOCK_OF_PHASE[pv]
                    if G[lab]:
                        continue
                if pv != 'FINAL' and isinstance(ph, int) and pv < ph:
                    continue
                if kind == 'create' and done.get(ph, 0) == 0 and ph >= 1 and G[STOCK_OF_PHASE[ph]]:
                    continue
                if pv == 'FINAL':
                    if sv[1] != mode:
                        continue
                inc = incs(st, acts)
                a = {'A': aA, 'B': aB, 'C': aC}
                nrC, nrA = rC, rA
                if ph in (1, 2, 3):
                    for lab in ('A', 'B', 'C'):
                        if lab in inc:
                            a[lab] = (a[lab] + inc[lab]) % q
                    if ph == 3 and 'K' in acts:
                        rails = {p[0]: p[2] for p in sv[1]}
                        nrC, nrA = rails['C'], rails['A']
                elif ph == 4:
                    a['B'] = (a['B'] + inc['B']) % q
                    ia = 1 if (acts[[p[0] for p in st[1]].index('A')] == 'L' and rA == 'L') else 0
                    ic = 1 if (acts[[p[0] for p in st[1]].index('C')] == 'L' and rC == 'L') else 0
                    a['A'] = (a['A'] + ia) % q; a['C'] = (a['C'] + ic) % q
                    nrA = acts[[p[0] for p in st[1]].index('A')]
                    nrC = acts[[p[0] for p in st[1]].index('C')]
                elif ph == 5:
                    labs = [p[0] for p in st[1]]
                    aB_ = acts[labs.index('B')]; aCA = acts[labs.index('CA')]
                    a['B'] = (a['B'] + (1 if aB_ == 'L' and dict((p[0], p[2]) for p in st[1])['B'] == 'L' else 0)) % q
                    a['A'] = (a['A'] + (1 if aCA == 'L' and rA == 'L' else 0)) % q
                    a['C'] = (a['C'] + (1 if aCA == 'L' and rC == 'L' else 0)) % q
                    nrA = nrC = aCA
                ns = (v, eS, None, a['A'], a['B'], a['C'], nrC, nrA)
                if pv == 'FINAL':
                    okf = all((not G[X]) or a[X] == f[X] % q for X in 'ABC')
                    if okf:
                        path = [(node, acts)]
                        p = s
                        while seen[p] is not None:
                            pp, pacts = seen[p]
                            path.append((pp[0], pacts))
                            p = pp
                        path.reverse()
                        return path
                    continue
                if ns not in seen:
                    seen[ns] = (s, acts)
                    dq.append(ns)
        return None
    path = finish(cur)
    if path is None:
        return None
    ticks.extend(path)
    return ticks

def masks_from_ticks(M, N, states, ticks, req):
    real = {'S': True, 'D': True, 'A': bool(req['G1']), 'B': bool(req['G2']), 'C': bool(req['G3']),
            'CA': bool(req['G1']) or bool(req['G3'])}
    base = 0  # absolute deficit of the base packet (S in phases 0-3, C/CA in 4-5)
    masks = []
    for (node, acts) in ticks:
        st = states[node]
        ph, packets = st
        lands = []
        newbase = None
        for (lab, pos, rail), a in zip(packets, acts):
            r = real[lab]
            if lab == 'S' and a == 'RL':
                # the copy goes to the front stock of its phase; drop it if that group is empty
                labs = [p[0] for p in packets]
                tgt = None
                # deposit target: D (then the current stock), or new stock, decided by the next state
                r_copy = None
                lands.append(base + pos)
                lands.append(('copy', base + pos + 1))
                continue
            if a in ('R',):
                if r: lands.append(base + pos)
            elif a == 'L':
                if r: lands.append(base + pos + 1)
        masks.append((lands, node, acts))
        # update base
        if ph in (0, 1, 2, 3):
            sa = acts[0]
            if sa == 'L':
                base += 1
            elif sa == 'K':
                # new base = C's landing
                labs = [p[0] for p in packets]
                i = labs.index('C')
                base = base + packets[i][1] + (1 if acts[i] == 'L' else 0)
        elif ph in (4, 5):
            labs = [p[0] for p in packets]
            i = labs.index('C') if 'C' in labs else labs.index('CA')
            base = base + (1 if acts[i] == 'L' else 0)
    return masks

def resolve_copies(M, states, ticks, masks, req):
    """decide for each split whether the copy holds a walk (target group nonempty)."""
    G = {'A': req['G1'], 'B': req['G2'], 'C': req['G3']}
    out = []
    for j, (lands, node, acts) in enumerate(masks):
        st = states[node]
        ph = st[0]
        newl = []
        for L in lands:
            if isinstance(L, tuple):
                # target group: if next state has a new stock (create) it is that phase's stock; else current phase's
                nxt = states[ticks[j + 1][0]] if j + 1 < len(ticks) else None
                tgt_phase = nxt[0] if (nxt is not None and isinstance(nxt[0], int)) else ph
                X = STOCK_OF_PHASE.get(tgt_phase if tgt_phase != ph else ph)
                if tgt_phase != ph:
                    X = STOCK_OF_PHASE[tgt_phase]
                if X and G[X]:
                    newl.append(L[1])
            else:
                newl.append(L)
        out.append(newl)
    return out

def simulate(N, M, q, deficit_masks, k):
    walks = Counter({(0, 'R', 0, 0): 1})
    t = 0
    # prefix of k right steps
    sitemasks = []
    for i in range(k):
        sitemasks.append({(i + 1) % N})
    for j, lands in enumerate(deficit_masks):
        tt = k + j + 1
        # deficits are relative to the prefix: absolute deficit unchanged by right steps; site = tt - 2e
        sitemasks.append({(tt - 2 * e) % N for e in lands})
    for t, mk in enumerate(sitemasks, start=1):
        nw = Counter()
        for (x, rail, lam, g), c in walks.items():
            y = (x + 1) % N
            if y in mk:
                nw[(y, 'R', lam, g)] += c
            y = (x - 1) % N
            if y in mk:
                nw[(y, 'L', lam + 1, (g + (1 if rail == 'L' else 0)) % q)] += c
        walks = nw
    return walks, len(sitemasks)

def check(walks, req, M, N, x):
    q = req['q']
    sites = {w[0] for w in walks}
    if not walks:
        return all(len(req[g]) == 0 for g in ('G1', 'G2', 'G3')), 'empty'
    if sites != {x}:
        return False, 'sites %s' % sorted(sites)
    lams = sorted({w[2] for w in walks})
    # candidate l values
    for l in range(min(lams) - M, max(lams) + 1):
        exp = Counter()
        if req['mode'] == 'i':
            for g in req['G2']: exp[(x, 'R', l, g % q)] += 1
            for g in req['G3']: exp[(x, 'L', l, g % q)] += 1
            for g in req['G1']: exp[(x, 'L', l + M, g % q)] += 1
        else:
            for g in req['G3']: exp[(x, 'R', l, g % q)] += 1
            for g in req['G1']: exp[(x, 'R', l + M, g % q)] += 1
            for g in req['G2']: exp[(x, 'L', l + M, g % q)] += 1
        if exp == walks:
            return True, 'l=%d' % l
    return False, 'mismatch'

def run_request(M, states, adj, good, req):
    N = req['N']; q = req['q']
    ticks = None
    for fa in range(q):
        for fb in range(q):
            for fc in range(q):
                ticks = plan(M, states, adj, good, req, {'A': fa, 'B': fb, 'C': fc})
                if ticks is not None:
                    break
            if ticks is not None: break
        if ticks is not None: break
    if ticks is None:
        return {'planner': False}
    masks = masks_from_ticks(M, N, states, ticks, req)
    dm = resolve_copies(M, states, ticks, masks, req)
    w0, T0 = simulate(N, M, q, dm, 0)
    sites = {w[0] for w in w0}
    if len(sites) == 1:
        x0 = next(iter(sites))
        k = (req['x'] - x0) % N
    else:
        k = 0
    w, Tn = simulate(N, M, q, dm, k)
    ok, why = check(w, req, M, N, req['x'])
    return {'planner': True, 'T': Tn, 'ok': ok, 'why': why, 'prefix': k}

if __name__ == '__main__':
    outfile, M, NREQ = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(20261113)
    out, states, adj, good = build(M)
    Ns = [M, 2 * M] if M % 2 == 1 else [2 * M]
    reqs = []
    for N in Ns:
        for mode in ('i', 'ii'):
            for pat in range(8):
                G = [[rng.randrange(2) for _ in range(1 + rng.randrange(2))] if (pat >> i) & 1 else [] for i in range(3)]
                reqs.append({'N': N, 'x': rng.randrange(N), 'q': 2, 'mode': mode, 'G1': G[0], 'G2': G[1], 'G3': G[2]})
    for _ in range(NREQ):
        N = rng.choice(Ns); q = rng.randrange(1, 5)
        G = [[rng.randrange(q) for _ in range(rng.randrange(4))] for _ in range(3)]
        reqs.append({'N': N, 'x': rng.randrange(N), 'q': q, 'mode': rng.choice(('i', 'ii')),
                     'G1': G[0], 'G2': G[1], 'G3': G[2]})
    with open(outfile, 'x') as fh:
        fh.write(json.dumps({'argv': sys.argv, 'graph': out}) + '\n')
        nq = sum(1 for r in reqs if r['N'] // (2 if r['N'] % 2 == 0 else 1) == M and r['q'] >= 1)
        fh.write(json.dumps({'Q0_qualifying': nq, 'requests': len(reqs)}) + '\n')
        cnt = Counter()
        for r in reqs:
            res = run_request(M, states, adj, good, r)
            cnt['planner_ok' if res['planner'] else 'planner_fail'] += 1
            if res['planner']:
                cnt['Q2_ok' if res['ok'] else 'Q2_FAIL'] += 1
            fh.write(json.dumps({'req': r, 'res': res}) + '\n'); fh.flush()
        fh.write(json.dumps({'summary': dict(cnt)}) + '\n')
        print(json.dumps({'M': M, 'summary': dict(cnt)}))
