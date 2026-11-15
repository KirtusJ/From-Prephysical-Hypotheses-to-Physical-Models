"""Challenger program for Theorem A (three groups on two levels, M >= 6), written from
STATEMENT_theoremA.md only.

Model. Carrier D_delta on Z_N: right step (x,*)->(x+1,R) gain 1; left step (x,R)->(x-1,L) gain 1,
(x,L)->(x-1,L) gain delta. delta of order q, gains as exponents mod q. Position product event: masks
A_1..A_T, a walk from (0,R) survives tick t iff its site after step t lies in A_t. Convention: tick t
is the t-th step, t>=1; site after t steps with e left steps is t-2e mod N. N ranges over N with
N/gcd(N,2)=M: N=M if M odd, and N=2M.

Construction: gadgets adv, depP+, depP-, depB, remove, coast, end(i)/(ii) exactly as in the statement,
a=4. Masks: A_t = {t-2e mod N : e in E_t}, E_t = residues required by the packets' moves (plus phantom
packets for empty groups in variant 'phantom'; omitted in variant 'omit').
Deposit order: all P deposits (C by depP-, A by depP+) in order 'CA', 'AC' or a seeded random
interleave 'mix', then all B deposits, remove, coast, end. Advances: kappa_i read from a run with no
advances; n_i chosen nondecreasing, n_i = t_i - kappa_i mod q. Coast count c chosen from a run with c=0.

PREDICATES (fixed before the first run):
 H  (hypothesis) : M >= 6 for the theorem cases; M = 5 cases are run separately and labelled.
 P1 exclusive    : at every tick, packets present are at distinct residues mod M and no excluded
                   residue of any packet (phantoms included in 'phantom') lies in E_t.
 P2 tracking     : at every tick the actual multiset of walk states (site, rail, deficit, gain mod q)
                   on the ring equals the planned one (packet walks continued by their moves).
 P3 final        : at the end, walks at site x are exactly: mode (i) R: G2 at l; L: G3 at l, G1 at l+M;
                   mode (ii) R: G3 at l, G1 at l+M; L: G2 at l+M; for the single l = final low deficit
                   of P (the statement's l = e_{P,low}); and no walk at any other site.
 P4 merge length : every depP- merge happens after exactly M-4 ticks including the split tick.
 P5 kappa indep. : final gain of deposit i equals n_i + kappa_i (kappa_i from the advance-free run).
 P6 end-site     : the coast count c in 0..N-1 brings the final site to x (implied by P3).
Result file opened with mode 'x'. Fixed seed 20261113.
"""
import sys, json, random, itertools, hashlib, time
from collections import Counter

class Fail(Exception):
    pass

class Packet:
    def __init__(self, name, ref, walks=None, phantom=False):
        self.name = name; self.ref = ref; self.walks = walks or []; self.phantom = phantom
    def exists(self):
        return bool(self.walks)

class Run:
    def __init__(self, M, N, q, variant, check=True):
        self.M, self.N, self.q, self.variant = M, N, q, variant
        self.t = 0
        self.masks = []
        self.fails = []        # list of (predicate, info)
        self.actual = Counter({(0, 'R', 0, 0): 1})
        self.check = check
        self.merge_lengths = []
    def fail(self, p, info):
        self.fails.append((p, info))
    def tick(self, moves):
        """moves: list of (packet, move) for all packets taken into account (incl. phantoms)."""
        M, N = self.M, self.N
        self.t += 1; t = self.t
        use = [(p, m) for p, m in moves if p is not None and (p.exists() or (p.phantom and self.variant == 'phantom'))]
        res = [p.ref % M for p, m in use]
        if len(set(res)) != len(res):
            self.fail('P1', f't={t} packets at same residue {[(p.name,p.ref%M) for p,_ in use]}')
        E = set(); excl = []
        for p, m in use:
            u = p.ref % M
            req = {'R': {u}, 'L': {(u+1) % M}, 'S': {u, (u+1) % M}, 'X': set()}[m]
            E |= req; excl.append((p, {u, (u+1) % M} - req))
        for p, ex in excl:
            if ex & E:
                self.fail('P1', f't={t} packet {p.name} excluded {sorted(ex & E)} in E={sorted(E)}')
        mask = {(t - 2*e) % N for e in E}
        self.masks.append(sorted(mask))
        # planned update
        newmoves = []
        for p, m in moves:
            if p is None: continue
            nw = []
            for (wid, d, rail, g) in p.walks:
                if m in ('R', 'S'):
                    nw.append((wid, d, 'R', g))
                if m in ('L', 'S'):
                    nw.append((wid + ('L',) if m == 'S' else wid, d+1, 'L', g + (1 if rail == 'L' else 0)))
            p.walks = nw
            if m == 'L': p.ref += 1
        # actual update
        q = self.q; new = Counter()
        for (x, rail, d, g), c in self.actual.items():
            x1 = (x+1) % N
            if x1 in mask: new[(x1, 'R', d, g)] += c
            x2 = (x-1) % N
            if x2 in mask: new[(x2, 'L', d+1, (g + (1 if rail == 'L' else 0)) % q)] += c
        self.actual = new
        return mask
    def compare(self, packets):
        plan = Counter()
        for p in packets:
            if p is None: continue
            for (wid, d, rail, g) in p.walks:
                plan[((self.t - 2*d) % self.N, rail, d, g % self.q)] += 1
        if plan != self.actual:
            self.fail('P2', f't={self.t} plan!=actual diff+={dict(self.actual-plan)} diff-={dict(plan-self.actual)}')

def build(M, N, q, G, mode, x, order, variant, advs=None, coast=0, rng=None):
    """G = (G1,G2,G3) lists of exponents. Returns (run, info)."""
    G1, G2, G3 = G
    run = Run(M, N, q, variant)
    if not (G1 or G2 or G3):
        run.tick([])  # A_1 = empty
        if run.actual: run.fail('P3', 'trivial case leaves walks')
        return run, {'trivial': True}
    a = 4
    S = Packet('S', 0, [(('S',), 0, 'R', 0)])
    P = Packet('P', a - M, [], phantom=not (G1 or G3))
    B = None
    # deposit list
    if order == 'CA':
        pdeps = [('C', i, g) for i, g in enumerate(G3)] + [('A', i, g) for i, g in enumerate(G1)]
    elif order == 'AC':
        pdeps = [('A', i, g) for i, g in enumerate(G1)] + [('C', i, g) for i, g in enumerate(G3)]
    else:
        pdeps = [('C', i, g) for i, g in enumerate(G3)] + [('A', i, g) for i, g in enumerate(G1)]
        rng.shuffle(pdeps)
    deps = pdeps + [('B', i, g) for i, g in enumerate(G2)]
    if advs is None: advs = [0]*len(deps)
    def pk():
        return [S, P, B]
    def others(*named):
        return [p for p in pk() if p is not None and p not in named]
    def T(moves):
        run.tick(moves); run.compare(pk() + [c for c in extra])
    extra = []
    def adv():
        for ms, mo in zip('LLRR', 'LRLR'):
            T([(S, ms)] + [(p, mo) for p in others(S)])
    for k, (grp, i, tgt) in enumerate(deps):
        if grp == 'B' and B is None:
            B = Packet('B', S.ref + 2, [], phantom=False)
        for _ in range(advs[k]): adv()
        wid = (grp, i)
        if grp == 'A':   # depP+
            # split: S: S, others R; left part is copy
            src = S.walks[0]
            run.tick([(S, 'S')] + [(p, 'R') for p in others(S)])
            # separate copy
            wl = [w for w in S.walks if w[2] == 'L']; wr = [w for w in S.walks if w[2] == 'R']
            S.walks = [(('S',), wr[0][1], 'R', wr[0][3])]
            c = Packet('c', S.ref + 1, [(wid, wl[0][1], 'L', wl[0][3])])
            extra[:] = [c]; run.compare(pk() + extra)
            n = 0
            while (c.ref - S.ref) % M != a % M:
                T([(c, 'L')] + [(p, 'R') for p in others(S)] + [(S, 'R')]); n += 1
                if n > 3*M: raise Fail('depP+ loop')
            # merge
            if P.exists() or P.phantom:
                if c.ref != P.ref + M:
                    run.fail('P3', f'depP+ merge level c={c.ref} Plow={P.ref}')
                P.walks += c.walks
            else:
                P.walks = c.walks; P.ref = c.ref - M
            P.phantom = False if P.walks else P.phantom
            extra[:] = []
            T([(p, 'R') for p in pk() if p is not None])
        elif grp == 'C':  # depP-
            run.tick([(S, 'S')] + [(p, 'L') for p in others(S)])
            wl = [w for w in S.walks if w[2] == 'L']; wr = [w for w in S.walks if w[2] == 'R']
            c = Packet('c', S.ref, [(wid, wr[0][1], 'R', wr[0][3])])
            S.walks = [(('S',), wl[0][1], 'L', wl[0][3])]; S.ref += 1
            extra[:] = [c]; run.compare(pk() + extra)
            n = 1
            hasP = P.exists() or P.phantom
            def done():
                if hasP: return P.ref == c.ref
                return c.ref - S.ref == a - M
            while not done():
                T([(c, 'R')] + [(p, 'L') for p in others()])
                n += 1
                if n > 3*M: raise Fail('depP- loop')
            run.merge_lengths.append(n)
            if n != M - 4: run.fail('P4', f'depP- merge after {n} ticks, M-4={M-4}')
            if hasP:
                P.walks += c.walks
            else:
                P.walks = c.walks; P.ref = c.ref
            P.phantom = False if P.walks else P.phantom
            extra[:] = []
            T([(p, 'R') for p in pk() if p is not None])
        else:  # depB
            run.tick([(S, 'S')] + [(p, 'R') for p in others(S)])
            wl = [w for w in S.walks if w[2] == 'L']; wr = [w for w in S.walks if w[2] == 'R']
            S.walks = [(('S',), wr[0][1], 'R', wr[0][3])]
            c = Packet('c', S.ref + 1, [(wid, wl[0][1], 'L', wl[0][3])])
            extra[:] = [c]; run.compare(pk() + extra)
            T([(c, 'L')] + [(p, 'R') for p in others()])
            if c.ref != B.ref: run.fail('P3', f'depB merge c={c.ref} B={B.ref}')
            B.walks += c.walks
            extra[:] = []
            T([(p, 'R') for p in pk() if p is not None])
    if B is None:
        B = Packet('B', S.ref + 2, [], phantom=True)
    # remove
    T([(S, 'X')] + [(p, 'R') for p in others(S)])
    S.walks = []
    del_S = S
    S = None
    def pk2():
        return [P, B]
    def T2(moves):
        run.tick(moves); run.compare(pk2())
    for _ in range(coast):
        T2([(P, 'R'), (B, 'R')])
    if mode == 'i':
        n = 0
        while B.ref - P.ref != 2:
            T2([(P, 'L'), (B, 'R')]); n += 1
            if n > 3*M: raise Fail('end loop')
        T2([(P, 'L'), (B, 'R')]); T2([(P, 'L'), (B, 'R')])
    else:
        T2([(B, 'L'), (P, 'R')]); T2([(B, 'L'), (P, 'R')])
    # final check P3
    l = P.ref
    t = run.t
    sites = {k[0] for k in run.actual}
    exp = Counter()
    if mode == 'i':
        for g in G2: exp[('R', l, g % q)] += 1
        for g in G3: exp[('L', l, g % q)] += 1
        for g in G1: exp[('L', l + M, g % q)] += 1
    else:
        for g in G3: exp[('R', l, g % q)] += 1
        for g in G1: exp[('R', l + M, g % q)] += 1
        for g in G2: exp[('L', l + M, g % q)] += 1
    final_site = (t - 2*l) % N
    got = Counter()
    for (s, rail, d, g), c in run.actual.items():
        if s == x: got[(rail, d, g)] += c
    info = {'final_site_formula': final_site, 'sites': sorted(sites), 'T': t, 'l': l,
            'walk_gains': {}}
    # per-walk final gains for P5
    for p in (P, B):
        for (wid, d, rail, g) in p.walks:
            info['walk_gains'][wid] = g
    info['_got'] = got; info['_exp'] = exp
    return run, info, deps

def construct(M, N, q, G, mode, x, order, variant, seed):
    rng = random.Random(seed)
    if not (G[0] or G[1] or G[2]):
        run, info = build(M, N, q, G, mode, x, order, variant)
        return run.fails, {}
    run0, info0, deps = build(M, N, q, G, mode, x, order, variant, rng=random.Random(seed))
    kappa = [info0['walk_gains'][(g, i)] for (g, i, _) in deps]
    advs = []; cum = 0; ncum = []
    for k, (g, i, tgt) in enumerate(deps):
        need = (tgt - kappa[k]) % q
        inc = (need - cum) % q
        advs.append(inc); cum += inc; ncum.append(cum)
    run1, info1, _ = build(M, N, q, G, mode, x, order, variant, advs=advs, rng=random.Random(seed))
    c = (x - info1['final_site_formula']) % N
    run, info, deps2 = build(M, N, q, G, mode, x, order, variant, advs=advs, coast=c, rng=random.Random(seed))
    fails = list(run.fails)
    # P5
    for k, (g, i, tgt) in enumerate(deps2):
        fg = info['walk_gains'].get((g, i))
        if fg is None or fg != ncum[k] + kappa[k]:
            fails.append(('P5', f'deposit {k} {g}{i}: final {fg} vs n+kappa {ncum[k]+kappa[k]}'))
    # P3
    if info['sites'] != [x] or info['_got'] != info['_exp']:
        fails.append(('P3', f"sites={info['sites']} x={x} got={dict(info['_got'])} exp={dict(info['_exp'])}"))
    return fails, {'T': info['T'], 'merge_lengths': run.merge_lengths}

def multisets(q, kmax):
    out = []
    for k in range(kmax+1):
        for c in itertools.combinations_with_replacement(range(q), k):
            out.append(list(c))
    return out

def requests_small(q, tot):
    ms = multisets(q, tot)
    for g1 in ms:
        for g2 in ms:
            if len(g1)+len(g2) > tot: continue
            for g3 in ms:
                if len(g1)+len(g2)+len(g3) <= tot:
                    yield (g1, g2, g3)

def worker(args):
    M, N, q, G, mode, x, order, variant, seed = args
    try:
        fails, meta = construct(M, N, q, G, mode, x, order, variant, seed)
    except Fail as e:
        fails, meta = [('LOOP', str(e))], {}
    return args, fails, meta

def main():
    out = sys.argv[1]; Ms = [int(v) for v in sys.argv[2].split(',')]; part = sys.argv[3]
    rng = random.Random(20261113)
    jobs = []
    for M in Ms:
        Ns = sorted({2*M} | ({M} if M % 2 else set()))
        for N in Ns:
            sites = sorted({0, 1, N-1, rng.randrange(N)})
            if part == 'small':
                for q in range(1, 5):
                    for G in requests_small(q, 4):
                        for mode in 'i', 'ii':
                            for order in ('CA', 'AC', 'mix'):
                                if order == 'mix' and (not G[0] or not G[2]): continue
                                for variant in ('phantom', 'omit'):
                                    x = sites[rng.randrange(len(sites))]
                                    jobs.append((M, N, q, G, mode, x, order, variant, rng.randrange(10**9)))
            else:
                for _ in range(300):
                    q = rng.randrange(1, 9)
                    G = tuple([rng.randrange(q) for _ in range(rng.randrange(0, 7))] for _ in range(3))
                    for mode in 'i', 'ii':
                        for variant in ('phantom', 'omit'):
                            jobs.append((M, N, q, G, mode, rng.choice(sites), rng.choice(['CA', 'AC', 'mix']), variant, rng.randrange(10**9)))
    from multiprocessing import Pool
    with Pool(4) as pool:
        res = pool.map(worker, jobs, chunksize=200)
    f = open(out, 'x')
    summ = {}
    for args, fails, meta in res:
        M, N, q, G, mode, x, order, variant, seed = args
        key = f'M={M} N={N} {variant}'
        s = summ.setdefault(key, {'cases': 0, 'qualify_H': 0, 'fail_cases': 0, 'by_pred': Counter()})
        s['cases'] += 1; s['qualify_H'] += int(M >= 6)
        if fails:
            s['fail_cases'] += 1
            for p in {p for p, _ in fails}: s['by_pred'][p] += 1
            f.write(json.dumps({'args': args, 'fails': fails[:3]}) + '\n')
    f.write('SUMMARY\n')
    for k, s in summ.items():
        s['by_pred'] = dict(s['by_pred'])
        f.write(json.dumps({k: s}) + '\n')
    f.close()
    for k, s in summ.items(): print(k, s)

if __name__ == '__main__':
    main()
