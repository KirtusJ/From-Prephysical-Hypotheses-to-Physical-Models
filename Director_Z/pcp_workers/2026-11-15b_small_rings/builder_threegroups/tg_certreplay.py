#!/usr/bin/env python3
"""Replay of the CERTIFICATE schedule (tg_cert.py) for prop:threegroups on the actual ring Z_N.

Schedule (the construction of FINDINGS, Theorem T7):
  one tick S:L (rail R -> L);  U0^{p0};  P0;  for each further walk of A: U1^{m} D1;  U1^{pad1}; U1^{p1};  P1;
  for each further walk of B: U2^{m} D2;  U2^{pad2}; U2^{p2};  P2;  for each further walk of C: U3^{m} D3;
  U3^{pad3};  E_mode.   pad_k = -(sum of the m of phase k) mod q.  The first walk of each group is the copy made by
  the creation tick of P_{k-1}.  Empty group: its walks are absent; its stock's landings are left out of the masks
  and the creation split is not made (deletion lemma).  A prefix of k right steps puts the end at site x.
  m are computed from a run with all m = p = 0 (formula m_i = (g_i - f0_i) - (g_{i-1} - f0_{i-1})); p from the
  effect vectors of U0, U1 (after A), U2 (after B), found by simulation; solved by search over Z_q^3.
PREDICATES (fixed before the first run):
  H0 (hypothesis per request): N in {M, 2M}, q >= 1, G_i multisets of Z_q; count reported.
  H1: in every simulation each walk has a unique tag (no walk other than S splits) - checked.
  H2: the per-group discrepancy after choosing m is uniform within each group (the steering lemma) - checked.
  H3 (the predicate that matters): the final walks on Z_N are exactly those of the request (as tg_replay Q2).
Requests: random.Random(20261113): q in 1..5, sizes 0..4, both modes, x uniform, N in {M,2M}; plus the 8 emptiness
  patterns x 2 modes x each N with q = 3.  Usage: tg_certreplay.py OUTFILE M CERTFILE NREQ; output mode 'x'.
"""
import sys, json, random
from collections import Counter
import tg_search as T

def load_cert(path):
    cert = {}
    for line in open(path):
        d = json.loads(line)
        for k, v in d.items():
            if k in ('argv', 'verify', 'PSIMAX', 'LMAX', 'bounds_hit'):
                continue
            if k.startswith('h'):
                continue
            cert[k] = [(tuple([t['node'][0], tuple(tuple(p) for p in t['node'][1])]), tuple(t['acts'])) for t in v]
    return cert

def schedule(cert, req, m, p, mode):
    s0R = (0, (('S', 0, 'R'),))
    ticks = [(s0R, ('L',))]
    ticks += cert['U0'] * p[0]
    ticks += cert['P0']
    nA, nB, nC = len(req['G1']), len(req['G2']), len(req['G3'])
    for k, n, U, D, P in ((1, nA, 'U1', 'D1', 'P1'), (2, nB, 'U2', 'D2', 'P2'), (3, nC, 'U3', 'D3', None)):
        ms = m[k]
        for i in range(1, n):
            ticks += cert[U] * ms[i]
            ticks += cert[D]
        pad = (-sum(ms[1:n])) % req['q']
        ticks += cert[U] * pad
        if k in (1, 2):
            ticks += cert[U] * p[k]
            ticks += cert[P]
    ticks += cert['E_' + mode]
    return ticks

def masks(M, ticks, req):
    real = {'S': True, 'D': True, 'A': bool(req['G1']), 'B': bool(req['G2']), 'C': bool(req['G3']),
            'CA': bool(req['G1']) or bool(req['G3'])}
    base = 0
    out = []
    for j, (st, acts) in enumerate(ticks):
        ph, packets = st
        lands = []
        sact = None
        for (lab, pos, rail), a in zip(packets, acts):
            if lab == 'S':
                sact = a
                if a in ('R', 'RL'): lands.append(base + pos)
                if a == 'L': lands.append(base + pos + 1)
                if a == 'RL':
                    nxt = ticks[j + 1][0] if j + 1 < len(ticks) else None
                    if nxt is not None and nxt[0] != ph:
                        tgt = T.STOCK_OF_PHASE[nxt[0]]
                    else:
                        tgt = T.STOCK_OF_PHASE[ph]
                    if real[tgt]:
                        lands.append(base + pos + 1)
                continue
            if not real[lab]:
                continue
            if a == 'R': lands.append(base + pos)
            elif a == 'L': lands.append(base + pos + 1)
        out.append((lands, sact))
        if ph in (0, 1, 2, 3):
            if acts[0] == 'L': base += 1
            elif acts[0] == 'K':
                labs = [q_[0] for q_ in packets]; i = labs.index('C')
                base = base + packets[i][1] + (1 if acts[i] == 'L' else 0)
        else:
            labs = [q_[0] for q_ in packets]
            i = labs.index('C') if 'C' in labs else labs.index('CA')
            base += 1 if acts[i] == 'L' else 0
    return out

def simulate(N, q, ms, k):
    """tagged simulation; tag 'src' for the source; a split of the source gives the L-branch a new tag."""
    walks = Counter({(0, 'R', 0, 0, 'src'): 1})
    newtag = [0]
    sitemasks = [({(i + 1) % N}, 'R') for i in range(k)]
    for j, (lands, sact) in enumerate(ms):
        tt = k + j + 1
        sitemasks.append(({(tt - 2 * e) % N for e in lands}, sact))
    multi = False
    for mk, sact in sitemasks:
        nw = Counter()
        for (x, rail, lam, g, tag), c in walks.items():
            if c > 1: multi = True
            y = (x + 1) % N
            if y in mk:
                nw[(y, 'R', lam, g, tag)] += c
            y = (x - 1) % N
            if y in mk:
                t2 = tag
                if tag == 'src' and sact == 'RL':
                    t2 = 'w%d' % newtag[0]; newtag[0] += 1
                nw[(y, 'L', lam + 1, (g + (1 if rail == 'L' else 0)) % q, t2)] += c
        walks = nw
    tags = Counter(w[4] for w in walks)
    if any(v > 1 for v in tags.values()):
        multi = True
    return walks, multi, len(sitemasks)

def group_of_tags(req):
    order = []
    for X, key in (('A', 'G1'), ('B', 'G2'), ('C', 'G3')):
        order += [X] * len(req[key])
    return order  # deposit order = A..., B..., C...

def run_request(M, cert, req):
    q = req['q']; N = req['N']; mode = req['mode']
    G = {'A': list(req['G1']), 'B': list(req['G2']), 'C': list(req['G3'])}
    zero = {1: [0] * max(1, len(G['A'])), 2: [0] * max(1, len(G['B'])), 3: [0] * max(1, len(G['C']))}
    def finals(m, p, k=0):
        t = schedule(cert, req, m, p, mode)
        w, multi, Tn = simulate(N, q, masks(M, t, req), k)
        return w, multi, Tn
    w0, multi0, _ = finals(zero, [0, 0, 0])
    order = group_of_tags(req)
    def per_walk(w):
        d = {}
        for (x, rail, lam, g, tag), c in w.items():
            if tag == 'src':
                return None
            d[int(tag[1:])] = g
        return d
    f0 = per_walk(w0)
    if f0 is None or len(f0) != len(order):
        return {'ok': False, 'why': 'tags0', 'n': None if f0 is None else len(f0)}
    # walks are tagged in deposit order (only nonempty groups split)
    idx = 0
    m = {1: [0], 2: [0], 3: [0]}
    for k, X in ((1, 'A'), (2, 'B'), (3, 'C')):
        n = len(G[X])
        ms = [0] * max(1, n)
        for i in range(1, n):
            ms[i] = ((G[X][i] - f0[idx + i]) - (G[X][i - 1] - f0[idx + i - 1])) % q
        m[k] = ms
        idx += n
    w1, multi1, _ = finals(m, [0, 0, 0])
    f1 = per_walk(w1)
    disc = {}
    idx = 0
    uniform = True
    for X in 'ABC':
        n = len(G[X])
        ds = {(G[X][i] - f1[idx + i]) % q for i in range(n)}
        if len(ds) > 1: uniform = False
        disc[X] = ds.pop() if ds else 0
        idx += n
    # effect vectors
    eff = []
    for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
        we, _, _ = finals(m, e)
        fe = per_walk(we)
        v = {}
        idx = 0
        for X in 'ABC':
            n = len(G[X])
            ds = {(fe[idx + i] - f1[idx + i]) % q for i in range(n)}
            if len(ds) > 1: uniform = False
            v[X] = ds.pop() if ds else 0
            idx += n
        eff.append(v)
    sol = None
    for p0 in range(q):
        for p1 in range(q):
            for p2 in range(q):
                if all((p0 * eff[0][X] + p1 * eff[1][X] + p2 * eff[2][X] - disc[X]) % q == 0 for X in 'ABC'):
                    sol = [p0, p1, p2]; break
            if sol: break
        if sol: break
    if sol is None:
        return {'ok': False, 'why': 'no p', 'uniform': uniform}
    w2, multi2, T2 = finals(m, sol)
    sites = {w[0] for w in w2}
    k = (req['x'] - next(iter(sites))) % N if len(sites) == 1 else 0
    w3, multi3, T3 = finals(m, sol, k)
    plain = Counter()
    for (x, rail, lam, g, tag), c in w3.items():
        plain[(x, rail, lam, g)] += c
    ok, why = check(plain, req, M, req['x'])
    return {'ok': ok, 'why': why, 'H1_unique_tags': not (multi0 or multi1 or multi2 or multi3), 'H2_uniform': uniform,
            'T': T3, 'p': sol}

def check(walks, req, M, x):
    q = req['q']
    if not walks:
        return all(len(req[g]) == 0 for g in ('G1', 'G2', 'G3')), 'empty'
    if {w[0] for w in walks} != {x}:
        return False, 'sites'
    lams = sorted({w[2] for w in walks})
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

if __name__ == '__main__':
    outfile, M, certfile, NREQ = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    cert = load_cert(certfile)
    rng = random.Random(20261113)
    Ns = [M, 2 * M] if M % 2 == 1 else [2 * M]
    reqs = []
    for N in Ns:
        for mode in ('i', 'ii'):
            for pat in range(8):
                G = [[rng.randrange(3) for _ in range(1 + rng.randrange(3))] if (pat >> i) & 1 else [] for i in range(3)]
                reqs.append({'N': N, 'x': rng.randrange(N), 'q': 3, 'mode': mode, 'G1': G[0], 'G2': G[1], 'G3': G[2]})
    for _ in range(NREQ):
        N = rng.choice(Ns); q = rng.randrange(1, 6)
        G = [[rng.randrange(q) for _ in range(rng.randrange(5))] for _ in range(3)]
        reqs.append({'N': N, 'x': rng.randrange(N), 'q': q, 'mode': rng.choice(('i', 'ii')), 'G1': G[0], 'G2': G[1], 'G3': G[2]})
    with open(outfile, 'x') as fh:
        fh.write(json.dumps({'argv': sys.argv}) + '\n')
        fh.write(json.dumps({'H0_qualifying': len(reqs), 'requests': len(reqs)}) + '\n')
        cnt = Counter()
        for r in reqs:
            res = run_request(M, cert, r)
            cnt['H3_ok' if res['ok'] else 'H3_FAIL'] += 1
            cnt['H1_ok' if res.get('H1_unique_tags') else 'H1_not'] += 1
            cnt['H2_ok' if res.get('H2_uniform') else 'H2_not'] += 1
            fh.write(json.dumps({'req': r, 'res': res}) + '\n'); fh.flush()
        fh.write(json.dumps({'summary': dict(cnt)}) + '\n')
        print(json.dumps({'M': M, 'summary': dict(cnt)}))
