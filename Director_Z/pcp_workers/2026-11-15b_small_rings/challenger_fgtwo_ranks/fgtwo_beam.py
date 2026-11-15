#!/usr/bin/env python3
"""Challenger check of Theorem thm:fgtwo (two classes of winding) on small rings.

Model (from PAPER_TEXT_ppcons.tex / PAPER_TEXT_subsections.tex): two-rail digraph on Z_N, gains in a finite
abelian group A (additive, A = Z_n1 x ... ): a on (x,R)->(x+1,R), b on (x,R)->(x-1,L), c on (x,L)->(x+1,R),
d on (x,L)->(x-1,L). Walks from (0,R), start gain 0. A position product event of length T>=1 is the set of
walks of length T whose site after s steps lies in A_s. State of an event = multiset of (site, rail, gain) of its
walks. Rule mu(S) = sum over vertices F_rail(multiset of gains at the vertex), F(empty)=0, separate unknowns
F_R(m), F_L(m) (no invariance imposed). Requirement eq:ppcons with factor 2: mu(Ext S) - 2 mu(S) = 0.
States are deduplicated globally and up to rotation of the ring (F is site-independent, so a rotated state
gives the identical equation and a rotated future).

delta = a+d-b-c, r = ord(delta), M = N/gcd(N,2), beta = M(b+c-2a), Delta_N = <delta,beta>,
s = min{j>=1: j beta in <delta>}, k with 2 beta = k delta (parity of k meaningful for r even).

PREDICATES (fixed before the first run):
 P1 hypothesis: the carrier qualifies iff s == 2. Non-qualifying carriers are reported and not tested.
 P0 coset: at every vertex of every enumerated state (and of its Ext) the gains lie in one coset of Delta_N
    (Lemma fgcoset); failure is reported (it would mean the model is coded wrongly or the lemma is false).
 P2 converse/sanity: each predicted basis function (count; eps0^2+eps1^2 if r even; eps0*eps1 if r even and
    k even; F_R(m) = f(m - rep), F_L(m) = F_R(m + c), rep = least element of the coset) satisfies every
    equation exactly.
 P2b: the rational predicted basis and the squares |sigma_chi|^2 (chi characters of A with chi(delta) = -1),
    with the count, span the same space on the P-unknowns (float SVD; the gap between the singular values is
    reported, no threshold is assumed).
 P3 main: dim of the solution space projected onto the unknowns P (multisets seen at layers <= L0) equals the
    predicted dimension (rank of the predicted basis on P). Excess = counterexample candidate at this bound;
    an extra solution is then printed. dim_proj = |P| - rank(A) + rank(A_Q), Q = the other unknowns.
 P4 bound: the BFS stops at layer L or when the number of states exceeds MAXSTATES; whether the bound on
    states was hit is reported (if hit, the enumeration of layer <= L is incomplete and only a lower bound on
    the constraints, i.e. dim_proj is an upper bound).
Ranks are exact over Q: sparse elimination with flint.fmpq, pivoting first on the Q-columns; the rows left
    with only P-columns form the residual system, whose rank (fmpq_mat.rank) gives dim_proj = |P| - rank.

v2 (fgtwo_beam.py): equations are the site equations E(U,V)=F_R(aU+cV)+F_L(bU+dV)-2F_R(U)-2F_L(V)=0 for
every pair (U,V) met at one site of an enumerated state (equivalent system, Lemma onesite). If BEAM>0, at
most BEAM states per layer are kept (random sample, seed 20261113) and expanded; all children give equations.
With a beam the enumeration is a subset: P3 equality is evidence, an excess is only a candidate to recheck
without the beam. P4 also reports whether the beam cut any layer.
usage: fgtwo_beam.py CARRIER N L L0 MAXSTATES BEAM OUTFILE
"""
import sys, time, json, itertools, hashlib, cmath, math
from collections import defaultdict
import flint
import numpy as np

CARRIERS = {
    # name: (moduli, a, b, c, d)
    # r odd (r=3), beta=(1,0) for M odd
    'Z2Z3_rodd':  ((2, 3), (0, 0), (0, 0), (1, 0), (1, 1)),
    # r odd, nonzero a,b
    'Z2Z3_rodd2': ((2, 3), (0, 1), (1, 1), (0, 2), (0, 0)),
    # r=2, k even: delta=(0,1), beta=(1,0) for M odd
    'Z2Z2_keven': ((2, 2), (0, 0), (0, 0), (1, 0), (1, 1)),
    # r=2, k odd: Z4, delta=2, c chosen so that M c = +-1
    'Z4_kodd_c1': ((4,), (0,), (0,), (1,), (3,)),
    'Z4_kodd_c3': ((4,), (0,), (0,), (3,), (1,)),
    # r=4, k odd: Z8, delta=2, c=1, beta = M odd
    'Z8_r4_kodd': ((8,), (0,), (0,), (1,), (3,)),
    # r=4, k even: Z4xZ2, delta=(1,0), c=(0,1)
    'Z4Z2_r4_keven': ((4, 2), (0, 0), (0, 0), (0, 1), (1, 1)),
    # M even (M=6, N=12): need 6c of order 2 outside <delta>
    'Z4Z2_M6_keven': ((4, 2), (0, 0), (0, 0), (1, 0), (1, 1)),   # delta=(0,1), beta=6c=(2,0)
    'Z4Z3_M6_rodd':  ((4, 3), (0, 0), (0, 0), (1, 0), (1, 1)),   # delta=(0,1) r=3, beta=(2,0)
    'Z8_M6_kodd':    ((8,), (0,), (0,), (3,), (7,)),             # delta=4, beta=18=2, 2beta=4=delta
    # M = 8 control (N = 16): beta = 8c, c=(1,0) in Z16xZ2 -> beta=(8,0)
    'Z16Z2_M8_keven': ((16, 2), (0, 0), (0, 0), (1, 0), (1, 1)),
}


def add(g, h, mod):
    return tuple((x + y) % m for x, y, m in zip(g, h, mod))


def neg(g, mod):
    return tuple((-x) % m for x, m in zip(g, mod))


def mul(n, g, mod):
    return tuple((n * x) % m for x, m in zip(g, mod))


def order(g, mod):
    n, z = 1, tuple(0 for _ in mod)
    h = g
    while h != z:
        h = add(h, g, mod); n += 1
    return n


def classify(mod, a, b, c, d, N):
    M = N // math.gcd(N, 2)
    delta = add(add(a, d, mod), neg(add(b, c, mod), mod), mod)
    r = order(delta, mod)
    sub = set(mul(j, delta, mod) for j in range(r))
    beta = mul(M, add(add(b, c, mod), neg(mul(2, a, mod), mod), mod), mod)
    s = 1
    h = beta
    while h not in sub:
        h = add(h, beta, mod); s += 1
    k = None
    if s == 2:
        b2 = mul(2, beta, mod)
        k = [j for j in range(r) if mul(j, delta, mod) == b2][0]
    Delta = set()
    for i in range(order(beta, mod)):
        for j in range(r):
            Delta.add(add(mul(i, beta, mod), mul(j, delta, mod), mod))
    return dict(M=M, delta=delta, r=r, beta=beta, s=s, k=k, Delta=Delta)


def canon(state, N):
    """state: dict (site, rail, gain) -> count. Return canonical tuple up to rotation."""
    best = None
    items = list(state.items())
    for sh in range(N):
        t = tuple(sorted((((x + sh) % N, rl, g), n) for (x, rl, g), n in items))
        if best is None or t < best:
            best = t
    return best


def vertex_multisets(state):
    vm = defaultdict(lambda: defaultdict(int))
    for (x, rl, g), n in state:
        vm[(x, rl)][g] += n
    return {v: (v[1], tuple(sorted(ms.items()))) for v, ms in vm.items()}


def ext_full(state, N, mod, a, b, c, d):
    out = defaultdict(int)
    for (x, rl, g), n in state:
        gR = add(g, a if rl == 'R' else c, mod)
        gL = add(g, b if rl == 'R' else d, mod)
        out[((x + 1) % N, 'R', gR)] += n
        out[((x - 1) % N, 'L', gL)] += n
    return out


def main():
    name, N, L, L0, MAXS, BEAM, outfile = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
    import random; rng = random.Random(20261113); beam_cut = []
    out = open(outfile, 'x')
    t0 = time.time()
    mod, a, b, c, d = CARRIERS[name]
    cl = classify(mod, a, b, c, d, N)
    res = dict(carrier=name, N=N, L=L, L0=L0, MAXSTATES=MAXS, BEAM=BEAM, mod=mod, a=a, b=b, c=c, d=d,
               M=cl['M'], delta=cl['delta'], r=cl['r'], beta=cl['beta'], s=cl['s'], k=cl['k'],
               P1_qualifies=(cl['s'] == 2))
    if cl['s'] != 2:
        res['note'] = 'hypothesis s=2 fails; not tested'
        out.write(json.dumps(res) + '\n'); out.close(); print(json.dumps(res)); return
    Delta = cl['Delta']
    # BFS
    start = canon({(0, 'R', tuple(0 for _ in mod)): 1}, N)
    seen = {start: 0}
    layer = [start]
    states = []  # (state tuple, first layer), layers >= 1
    bound_hit = False
    for t in range(1, L + 1):
        new = []
        for st in layer:
            full = ext_full(st, N, mod, a, b, c, d)
            sites = sorted(set(x for (x, rl, g) in full))
            for nsub in range(1, len(sites) + 1):
                for sub in itertools.combinations(sites, nsub):
                    ss = set(sub)
                    ns = {k_: v for k_, v in full.items() if k_[0] in ss}
                    cs = canon(ns, N)
                    if cs not in seen:
                        seen[cs] = t
                        new.append(cs)
                        states.append((cs, t))
                        if len(states) > MAXS:
                            bound_hit = True; break
                if bound_hit: break
            if bound_hit: break
        if BEAM > 0 and len(new) > BEAM:
            beam_cut.append((t, len(new)))
            new = rng.sample(new, BEAM)
        layer = new
        if bound_hit: break
    res['layers_done'] = t
    res['states'] = len(states)
    res['P4_state_bound_hit'] = bound_hit
    res['P4_beam_cut_layers'] = beam_cut
    # equations
    keyidx = {}
    firstlayer = {}

    def kid(key, lay):
        if key not in keyidx:
            keyidx[key] = len(keyidx); firstlayer[key] = lay
        elif lay < firstlayer[key]:
            firstlayer[key] = lay
        return keyidx[key]

    rows = []
    p0_fail = 0
    deltalist = sorted(Delta)

    def coset_ok(ms):
        g0 = ms[0][0]
        dif = set(add(g, neg(g0, mod), mod) for g, _ in ms)
        return dif <= Delta

    def site_pairs(st):
        sp = defaultdict(lambda: [defaultdict(int), defaultdict(int)])
        for (x, rl, g), n in st:
            sp[x][0 if rl == 'R' else 1][g] += n
        return [(tuple(sorted(U.items())), tuple(sorted(V.items()))) for U, V in sp.values()]
    pairs = {}
    for st, lay in states:
        for pr in site_pairs(st):
            if pr not in pairs or lay < pairs[pr]:
                pairs[pr] = lay
    res['site_pairs'] = len(pairs)
    for (U, V), lay in pairs.items():
        row = defaultdict(int)
        if U:
            if not coset_ok(U): p0_fail += 1
            row[kid(('R', U), lay)] -= 2
        if V:
            if not coset_ok(V): p0_fail += 1
            row[kid(('L', V), lay)] -= 2
        R2 = defaultdict(int); L2 = defaultdict(int)
        for g, n in U:
            R2[add(g, a, mod)] += n; L2[add(g, b, mod)] += n
        for g, n in V:
            R2[add(g, c, mod)] += n; L2[add(g, d, mod)] += n
        for rl, ms in (('R', R2), ('L', L2)):
            t_ = tuple(sorted(ms.items()))
            if not coset_ok(t_): p0_fail += 1
            row[kid((rl, t_), lay + 1)] += 1
        row = {k_: v for k_, v in row.items() if v != 0}
        if row:
            rows.append(row)
    nU = len(keyidx)
    res['unknowns'] = nU
    res['equations_nonzero'] = len(rows)
    res['P0_coset_failures'] = p0_fail
    keys = [None] * nU
    for k_, i in keyidx.items(): keys[i] = k_
    P = [i for i in range(nU) if firstlayer[keys[i]] <= L0]
    Q = [i for i in range(nU) if firstlayer[keys[i]] > L0]
    res['P_size'] = len(P); res['Q_size'] = len(Q)
    dsub = set(mul(j, cl['delta'], mod) for j in range(cl['r']))
    def two_cosets(ms):
        g0 = ms[0][0]
        return any(add(g, neg(g0, mod), mod) not in dsub for g, _ in ms)
    res['P_keys_meeting_two_delta_cosets'] = sum(1 for i in P if two_cosets(keys[i][1]))
    res['all_keys_meeting_two_delta_cosets'] = sum(1 for i in range(nU) if two_cosets(keys[i][1]))

    # predicted basis
    def rep(g):
        return min(add(g, h, mod) for h in deltalist)

    def eps(u):  # u: dict gain->count, gains in Delta
        r_ = cl['r']; e = [0, 0]
        for g, n in u.items():
            for i in range(2):
                for j in range(r_):
                    if add(mul(i, cl['beta'], mod), mul(j, cl['delta'], mod), mod) == g:
                        e[i] += n * (-1) ** j
        return e

    def pred_vals(key):
        rl, ms = key
        if rl == 'L':
            ms = tuple((add(g, c, mod), n) for g, n in ms)
        rp = rep(ms[0][0])
        u = defaultdict(int)
        for g, n in ms:
            u[add(g, neg(rp, mod), mod)] += n
        cnt = sum(n for _, n in ms)
        vals = [cnt]
        if cl['r'] % 2 == 0:
            e0, e1 = eps(u)
            vals.append(e0 * e0 + e1 * e1)
            if cl['k'] % 2 == 0:
                vals.append(e0 * e1)
        return vals

    pv = [pred_vals(k_) for k_ in keys]
    nb = len(pv[0])
    res['predicted_basis_size'] = nb
    # P2
    p2 = []
    for j in range(nb):
        bad = sum(1 for row in rows if sum(v * pv[i][j] for i, v in row.items()) != 0)
        p2.append(bad)
    res['P2_violated_equations_per_basis_fn'] = p2
    res['P2_pass'] = all(x == 0 for x in p2)
    # predicted dim on P
    Bp = flint.fmpz_mat([[pv[i][j] for j in range(nb)] for i in P]) if P else None
    res['predicted_dim_on_P'] = Bp.rank() if P else 0
    # P2b: squares |sigma_chi|^2 on P, float
    chars = []
    for js in itertools.product(*[range(m) for m in mod]):
        chi = lambda g, js=js: cmath.exp(2j * math.pi * sum(x * y / m for x, y, m in zip(js, g, mod)))
        if abs(chi(cl['delta']) + 1) < 1e-9:
            chars.append(chi)
    sq = np.array([[sum(n for _, n in keys[i][1])] + [abs(sum(n * chi(g) for g, n in keys[i][1])) ** 2 for chi in chars] for i in P], float)
    Bf = np.array([[pv[i][j] for j in range(nb)] for i in P], float)
    def svals(X):
        return np.linalg.svd(X, compute_uv=False) if X.size else np.array([])
    s1 = svals(sq); s2 = svals(Bf); s3 = svals(np.hstack([sq, Bf]))
    res['P2b_sv_squares'] = [float(x) for x in s1[:6]]
    res['P2b_sv_rational'] = [float(x) for x in s2[:6]]
    res['P2b_sv_combined'] = [float(x) for x in s3[:6]]
    # ranks: exact sparse elimination over Q (flint.fmpq), Q-columns ordered above P-columns
    t1 = time.time()
    Pset = set(P)
    order_key = {}
    for i in range(nU):
        order_key[i] = (0 if i in Pset else 1, firstlayer[keys[i]], i)
    rows_u = list({tuple(sorted(r_.items())) for r_ in rows})
    res['equations_distinct'] = len(rows_u)
    pivots = {}  # col -> (row dict) with leading col = col (max order_key), normalized leading coeff 1
    residual = []
    maxfill = 0
    for r_ in rows_u:
        row = {i: flint.fmpq(v) for i, v in r_}
        while row:
            lead = max(row, key=lambda i: order_key[i])
            if lead in pivots:
                f = row[lead]
                for i, v in pivots[lead].items():
                    nv = row.get(i, 0) - f * v
                    if nv == 0:
                        row.pop(i, None)
                    else:
                        row[i] = nv
                continue
            if lead in Pset:
                residual.append(row)
            else:
                f = row[lead]
                pivots[lead] = {i: v / f for i, v in row.items()}
                maxfill = max(maxfill, len(row))
            break
    rkAQ = len(pivots)
    Pidx = {i: n for n, i in enumerate(P)}
    if residual:
        R = flint.fmpq_mat(len(residual), len(P))
        for ri, row in enumerate(residual):
            for i, v in row.items(): R[ri, Pidx[i]] = v
        rkR = R.rank()
    else:
        R = None; rkR = 0
    rkA = rkAQ + rkR
    res['rank_A'] = rkA; res['rank_AQ'] = rkAQ; res['rank_residual_on_P'] = rkR
    res['max_pivot_row_len'] = maxfill
    res['solution_dim_total'] = nU - rkA
    res['dim_proj_P'] = len(P) - rkR
    res['P3_pass'] = (res['dim_proj_P'] == res['predicted_dim_on_P'])
    res['rank_seconds'] = round(time.time() - t1, 2)
    if res['dim_proj_P'] > res['predicted_dim_on_P']:
        # projected solution space = nullspace of the residual system on P; remove the predicted span
        if R is not None:
            X, nul = R.nullspace()
            vecs = [[X[i, j] for i in range(len(P))] for j in range(nul)]
        else:
            vecs = [[flint.fmpq(1 if i == j else 0) for i in range(len(P))] for j in range(len(P))]
        cur = [[flint.fmpq(pv[P[i]][j]) for i in range(len(P))] for j in range(nb)]
        extra = []
        for v in vecs:
            if flint.fmpq_mat(cur + [v]).rank() > flint.fmpq_mat(cur).rank():
                cur.append(v); extra.append(v)
        res['extra_solutions'] = [{str(keys[P[i]]): str(v[i]) for i in range(len(P)) if v[i] != 0} for v in extra[:3]]
    res['seconds'] = round(time.time() - t0, 2)
    out.write(json.dumps(res) + '\n'); out.close()
    print(json.dumps({k_: v for k_, v in res.items() if k_ != 'extra_solutions'}))
    if 'extra_solutions' in res:
        print('EXTRA', json.dumps(res['extra_solutions'])[:3000])


if __name__ == '__main__':
    main()
