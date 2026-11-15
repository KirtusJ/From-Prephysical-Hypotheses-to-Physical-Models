#!/usr/bin/env python3
"""Three classes of winding: exact exploration.  Seed 20261113.

Usage: python3 -B explore.py OUTFILE B_PROFILE B_ALG CAP   (OUTFILE opened with mode 'x')

Carrier D_delta on the ring Z_N; state = counts indexed (site, rail, exponent mod q, lambda), from (0,R),
both arcs applied before each mask.  Level of a walk at a site = (lambda - least lambda at that site, both
rails)/M.  Breadth-first over ALL masks with deduplication of states (lambda shifted so the least is 0);
a site whose total exceeds the bound B is never kept (lossless for sites of total <= B, because all walks
of a site move together to each neighbour).  If a layer exceeds CAP states it is cut to CAP states chosen
by random.Random(20261113) and every later layer is marked SAMPLED; the last exhaustive length is recorded.

PREDICATES (fixed before the first run).
P0 control: N=6, masks {1,5},{2,4},{3}: field is (3,R,0,lam 0):1 and (3,L,2 mod q,lam 3):1 for q=1,2.
PW  lem:winding at each vertex of each site profile seen (q=1, total<=B_PROFILE):
    (i) l'-l>=2M: n(l)n(l') <= n(l+M)n(l'-M); (ii) n(l)n(l+2M) <= n(l+M)(n(l+M)-1).
    Hypothesis counted: left side > 0.
PX  lem:windingrails: l'-l>=M: nL(l)nR(l') <= nL(l+M)nR(l'-M); l'-l>=2M: nR(l)nL(l') <= nR(l+M)nL(l'-M).
    Hypothesis counted: left side > 0.
PN  (new, claimed): if one rail has >= 3 levels and the other is non-empty, the other has >= 2 levels.
    Hypothesis counted: one rail >= 3 levels and the other non-empty.
PT  (no claim; tabulation): NEC = all site profiles of total <= B_PROFILE, at most 4 levels on the combined
    range, satisfying PW and PX; SEEN = those seen.  Report |NEC|, |SEEN|, NEC minus SEEN, SEEN minus NEC
    (the last must be empty if PW, PX hold).
PA  (q=2, total <= B_ALG) exact ranks over Q.  Group structures: 'Z2xZ3' (beta^3=1, k even) and 'Z6'
    (beta^3=delta, k odd).  A walk at level j with exponent e has gain (j mod 3, e).  Unknown f on the
    orbits under translation by the group of multisets of size <= B_ALG.  Equations: for every site pair
    (u,v) seen (u on R, v on L, |u|+|v| <= B_ALG):  f(u+v)+f(u+T_delta v) = 2f(u)+2f(v).  O_k = orbits of
    multisets of size <= k that occur as u, v or u+v, u+T_delta v of a seen pair.  For k=1..B_ALG:
    sol_k = dimension of the solution space restricted to O_k; ref_k = dimension of span{count, sum eps_i^2,
    cross form} restricted to O_k.  Claim tested: sol_k == ref_k for k <= B_ALG-1 (k=B_ALG recorded, no claim).
    Hypothesis counted: number of k with O_k containing a multiset meeting three classes.
    Also PA2: the same with only the pairs in which u+v meets at most two classes (the pairs of the type of
    prop:threegroups); sol2_k recorded, to see what the two-class pairs alone leave free.
"""
import sys, json, random, itertools
from collections import defaultdict
from fractions import Fraction

def step(N, q, st, keep=None):
    nw = defaultdict(int)
    for (s, rail, e, lam), c in st.items():
        nw[((s + 1) % N, 0, e, lam)] += c
        nw[((s - 1) % N, 1, (e + rail) % q, lam + 1)] += c
    return nw

def restrict(nw, A):
    return {k: c for k, c in nw.items() if k[0] in A}

def site_view(N, st):
    M = N // 2 if N % 2 == 0 else N
    by = defaultdict(list)
    for (s, rail, e, lam), c in st.items(): by[s].append((rail, e, lam, c))
    out = {}
    for s, items in by.items():
        l0 = min(i[2] for i in items)
        assert all((i[2] - l0) % M == 0 for i in items)
        out[s] = [(rail, e, (lam - l0) // M, c) for rail, e, lam, c in items]
    return out

def canon(st):
    l0 = min(k[3] for k in st)
    return frozenset(((s, r, e, l - l0), c) for (s, r, e, l), c in st.items())

def bfs(N, q, B, cap, Tmax, rng, visit):
    layer = {canon({(0, 0, 0, 0): 1})}
    info = {'exhaustive_to': 0, 'layers': []}
    sampled = False
    seen_all = set(layer)
    for t in range(1, Tmax + 1):
        nxt = set()
        for fs in layer:
            st = {k: c for k, c in fs}
            nw = step(N, q, st)
            tot = defaultdict(int)
            for k, c in nw.items(): tot[k[0]] += c
            ok = [s for s in tot if tot[s] <= B]
            for rr in range(1, len(ok) + 1):
                for A in itertools.combinations(ok, rr):
                    r = restrict(nw, set(A))
                    cf = canon(r)
                    if cf not in seen_all:
                        nxt.add(cf)
        for cf in nxt:
            visit(N, {k: c for k, c in cf})
        seen_all |= nxt
        if len(nxt) > cap:
            nxt = set(rng.sample(sorted(nxt, key=lambda f: sorted(f)), cap)); sampled = True
        if not sampled: info['exhaustive_to'] = t
        info['layers'].append([t, len(nxt), sampled])
        layer = nxt
        if not layer: break
    return info

def prof_checks(M1, nR, nL, res):
    # nR, nL: dict level->count (levels in units of M)
    for n in (nR, nL):
        for l in n:
            for l2 in n:
                if l2 - l >= 2:
                    res['PW_i_inst'] += 1
                    if n[l] * n[l2] > n.get(l + 1, 0) * n.get(l2 - 1, 0): res['PW_i_fail'] += 1
                if l2 - l == 2:
                    res['PW_ii_inst'] += 1
                    m = n.get(l + 1, 0)
                    if n[l] * n[l2] > m * (m - 1): res['PW_ii_fail'] += 1
    for l in nL:
        for l2 in nR:
            if l2 - l >= 1:
                res['PX1_inst'] += 1
                if nL[l] * nR[l2] > nL.get(l + 1, 0) * nR.get(l2 - 1, 0): res['PX1_fail'] += 1
    for l in nR:
        for l2 in nL:
            if l2 - l >= 2:
                res['PX2_inst'] += 1
                if nR[l] * nL[l2] > nR.get(l + 1, 0) * nL.get(l2 - 1, 0): res['PX2_fail'] += 1
    for a, b in ((nR, nL), (nL, nR)):
        if len(a) >= 3 and len(b) >= 1:
            res['PN_inst'] += 1
            if len(b) < 2: res['PN_fail'] += 1

def nec_ok(nR, nL):
    r = defaultdict(int); prof_checks(1, nR, nL, r)
    return not any(v for k, v in r.items() if k.endswith('fail'))

def all_profiles(B, maxlev=4):
    out = set()
    def comps(total, slots):
        if slots == 0:
            if total == 0: yield ()
            return
        for x in range(total + 1):
            for rest in comps(total - x, slots - 1): yield (x,) + rest
    for tot in range(1, B + 1):
        for c in comps(tot, 2 * maxlev):
            nR = {i: c[i] for i in range(maxlev) if c[i]}
            nL = {i: c[maxlev + i] for i in range(maxlev) if c[maxlev + i]}
            if min(list(nR) + list(nL)) != 0: continue
            out.add((tuple(sorted(nR.items())), tuple(sorted(nL.items()))))
    return out

# ---------- algebra ----------
ELEMS = [(j, e) for j in range(3) for e in range(2)]
def tr(kind, g, h):
    j = g[0] + h[0]; e = g[1] + h[1]
    if j >= 3:
        j -= 3
        if kind == 'Z6': e += 1
    return (j, e % 2)
def tmul(kind, m, h):
    return tuple(sorted(tr(kind, g, h) for g in m))
def orbit_rep(kind, m):
    return min(tmul(kind, m, h) for h in ELEMS)
def eps(m):
    s = [0, 0, 0]
    for j, e in m: s[j] += (-1) ** e
    return s
def refs(kind, m):
    s = eps(m); sg = -1 if kind == 'Z6' else 1
    return [len(m), s[0] ** 2 + s[1] ** 2 + s[2] ** 2, s[0] * s[1] + s[1] * s[2] + sg * s[2] * s[0]]

def rank(rows):
    rows = [list(map(Fraction, r)) for r in rows]
    rk = 0; ncol = len(rows[0]) if rows else 0; piv = []
    for c in range(ncol):
        p = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        pv = rows[rk][c]; rows[rk] = [x / pv for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[rk])]
        piv.append(c); rk += 1
        if rk == len(rows): break
    return rk, piv, rows[:rk]

def nullspace(eqs, n):
    # eqs: list of sparse dict col->coef ; returns list of basis vectors (lists)
    rows = []
    for e in eqs:
        r = [0] * n
        for c, v in e.items(): r[c] += v
        rows.append(r)
    if not rows: rows = [[0] * n]
    rk, piv, red = rank(rows)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [Fraction(0)] * n; v[fc] = Fraction(1)
        for i, pc in enumerate(piv): v[pc] = -red[i][fc]
        basis.append(v)
    return basis

def algebra(kind, pairs, B):
    idx = {}
    def ix(m):
        r = orbit_rep(kind, m)
        if r not in idx: idx[r] = len(idx)
        return idx[r]
    occ = set(); eqs = {'all': [], 'two': []}
    delta = (0, 1)
    for u, v in pairs:
        uv = tuple(sorted(u + v)); utv = tuple(sorted(u + tmul(kind, v, delta)))
        e = defaultdict(int)
        if uv: e[ix(uv)] += 1
        if utv: e[ix(utv)] += 1
        if u: e[ix(u)] -= 2
        if v: e[ix(v)] -= 2
        for m in (u, v, uv, utv):
            if m: occ.add(orbit_rep(kind, m))
        e = {c: x for c, x in e.items() if x}
        if e:
            key = tuple(sorted(e.items()))
            eqs['all'].append(key)
            if len(set(g[0] for g in uv)) <= 2: eqs['two'].append(key)
    n = len(idx); reps = [None] * n
    for r, i in idx.items(): reps[i] = r
    out = {'unknowns': n, 'occurring_orbits': len(occ)}
    for fam in ('all', 'two'):
        E = [dict(k) for k in set(eqs[fam])]
        ns = nullspace(E, n)
        out[fam + '_equations'] = len(E); out[fam + '_nullity'] = len(ns)
        rowsk = []
        for k in range(1, B + 1):
            O = [i for i in range(n) if reps[i] in occ and len(reps[i]) <= k]
            three = sum(1 for i in O if len(set(g[0] for g in reps[i])) == 3)
            sol = rank([[v[i] for i in O] for v in ns])[0] if ns and O else 0
            ref = rank([[refs(kind, reps[i])[c] for i in O] for c in range(3)])[0] if O else 0
            # is ref inside sol?  rank of stacked
            both = rank([[v[i] for i in O] for v in ns] + [[refs(kind, reps[i])[c] for i in O] for c in range(3)])[0] if O else 0
            rowsk.append({'k': k, 'orbits': len(O), 'three_class_orbits': three, 'sol': sol, 'ref': ref, 'sol_plus_ref': both})
        out[fam] = rowsk
    return out

def main():
    out = open(sys.argv[1], 'x')
    BP, BA, CAP = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(20261113)
    res = {'command_line': ' '.join(['python3', '-B'] + sys.argv), 'seed': 20261113}
    ctl = {}
    for q in (1, 2):
        st = {(0, 0, 0, 0): 1}
        for A in ({1, 5}, {2, 4}, {3}): st = restrict(step(6, q, st), A)
        ctl[q] = sorted([list(k) + [c] for k, c in st.items()])
        assert st == {(3, 0, 0, 0): 1, (3, 1, 2 % q, 3): 1}
    res['P0'] = ctl
    nec = all_profiles(BP)
    nec = {p for p in nec if nec_ok(dict(p[0]), dict(p[1]))}
    res['NEC_size'] = len(nec)
    res['rings'] = {}
    for N in (3, 4, 5, 6):
        M = N // 2 if N % 2 == 0 else N
        rec = defaultdict(int); profs = set()
        def visit(N_, st):
            for s, items in site_view(N_, st).items():
                nR = defaultdict(int); nL = defaultdict(int)
                for rail, e, lev, c in items: (nL if rail else nR)[lev] += c
                p = (tuple(sorted(nR.items())), tuple(sorted(nL.items())))
                if p not in profs:
                    profs.add(p); prof_checks(1, dict(nR), dict(nL), rec)
        info = bfs(N, 1, BP, CAP, 4 * N + 8, rng, visit)
        small = {p for p in profs if max([l for l, c in p[0]] + [l for l, c in p[1]]) <= 3}
        r = dict(rec); r['M'] = M; r['bfs'] = info; r['profiles_seen'] = len(profs)
        r['seen_with_at_most_4_levels'] = len(small)
        r['max_levels_seen'] = 1 + max(max([l for l, c in p[0]] + [l for l, c in p[1]]) for p in profs)
        r['SEEN_minus_NEC'] = sorted(map(str, small - nec))
        r['NEC_minus_SEEN'] = sorted(map(str, nec - small))
        r['NEC_minus_SEEN_count'] = len(nec - small)
        r['SEEN'] = sorted(map(str, profs))
        # algebra, q=2
        pairs = set()
        def visit2(N_, st):
            for s, items in site_view(N_, st).items():
                u = []; v = []
                for rail, e, lev, c in items: (v if rail else u).extend([(lev % 3, e)] * c)
                pairs.add((tuple(sorted(u)), tuple(sorted(v))))
                pairs.add((tuple(sorted(u)), ())); pairs.add(((), tuple(sorted(v))))
        info2 = bfs(N, 2, BA, CAP, 4 * N + 8, rng, visit2)
        r['alg_bfs'] = info2; r['alg_pairs'] = len(pairs)
        r['PA'] = {kind: algebra(kind, pairs, BA) for kind in ('Z2xZ3', 'Z6')}
        res['rings'][str(N)] = r
        print(N, {k: v for k, v in r.items() if k not in ('SEEN', 'NEC_minus_SEEN', 'bfs', 'alg_bfs', 'PA')}, flush=True)
        print(' bfs', info['exhaustive_to'], info['layers'][-3:], 'alg', info2['exhaustive_to'], info2['layers'][-3:], flush=True)
        for kind in r['PA']:
            for fam in ('all', 'two'):
                print(' ', kind, fam, [(x['k'], x['orbits'], x['three_class_orbits'], x['sol'], x['ref'], x['sol_plus_ref']) for x in r['PA'][kind][fam]], flush=True)
    json.dump(res, out, indent=1, sort_keys=True); out.close()

if __name__ == '__main__':
    main()
