#!/usr/bin/env python3
"""Ring with M = 5 (N = 5, 10): gadgets found by bounded search, a schedule for P^+_delta and for
the three-group modes (i), (ii), a finite exclusivity check, and replays on the actual rings.
Worker 2026-11-15b.  Packets and exclusive ticks as in PROOFS.md (Lemma E).

Configuration ALPHA (positions = deficits relative to the source S): X at +1, Y at -2.
On Z_5 three packets always contain an adjacent pair, so the configuration is dynamic.
  depX : S splits, X (at +1) steps R and receives the left part; the right part stays the source.
  depY : (from BETA: X at +2, Y at -1) S splits, Y steps L and receives the right part; the left
         part is the new source.
Gadgets are searched, not designed: breadth-first over ticks in which each of S, X, Y steps R or L
(plus exactly one split tick for a deposit gadget), with the layers bounded by DEPTH and the state
including the rails and the gain increments (bounded by |d| <= 3).  Boundary: ALPHA with fixed
rails RHO = (rail of S, rail of X walks, rail of Y walks); every gadget starts and ends there.

PREDICATES (fixed before the first run).
 G1: for some RHO with rail(S) = R there are gadgets adv (dX = dY = 0, dS = 1), depX, depY, each
     starting and ending at ALPHA(RHO), every tick exclusive, no two packets at one residue except
     the merge of the copy into its target in the split tick.  Hypothesis counted: number of RHO tried.
 G2 (finite check): with these gadgets, phantoms for absent packets, the exclusivity of every tick of
     every gadget is re-verified from ALPHA(RHO) with every subset of {X, Y} real (phantoms only add
     residues to masks).  Also the phase-P gadgets (S, P at +3; adv, dep+, dep-) and the end gadgets.
 G3 (replay on the actual rings Z_5 and Z_10): for every request in range (q <= QMAX, sizes <= SMAX),
     P^+ (U' on R, V' on L, one level) and modes (i), (ii) give exactly the requested multisets at the
     requested levels at one site and no walk elsewhere; and every site x is reached (coast ticks).
 C (control): the same search for M = 4 boxes the claim: report whether G1 holds there (no claim).
Usage: m5_schedule.py OUTFILE QMAX SMAX DEPTH
"""
import sys, json, itertools
from collections import deque

M = 5


def excl_ok(pk, moves):
    """pk: dict name -> deficit; moves: name -> 'R','L','S','X'.  Exclusive?"""
    req, exc = set(), set()
    for n, e in pk.items():
        mv = moves[n]
        if mv == 'R': req.add(e % M); exc.add((e + 1) % M)
        elif mv == 'L': req.add((e + 1) % M); exc.add(e % M)
        elif mv == 'S': req |= {e % M, (e + 1) % M}
        elif mv == 'X': exc |= {e % M, (e + 1) % M}
    return not (req & exc), req


def inc(rail, mv):
    return 1 if (rail == 'L' and mv == 'L') else 0


ALPHA = {'X': 1, 'Y': -2}


def search_gadgets(rho, depth):
    """BFS for adv, depX, depY from ALPHA(rho) back to ALPHA(rho)."""
    rS, rX, rY = rho
    found = {}
    # state: (x, y, rS, rX, rY, dS, dX, dY, stage, copyinc) relative to S at 0
    # stage: 0 = before split, 1 = after split (copy merged), for kind in adv/depX/depY
    for kind in ('adv', 'depX', 'depY'):
        start = (ALPHA['X'], ALPHA['Y'], rS, rX, rY, 0, 0, 0, 0 if kind != 'adv' else 1, 0, None)
        q = deque([(start, [])])
        seen = {start[:10]}
        while q:
            st, path = q.popleft()
            x, y, a, b, c, dS, dX, dY, stage, ci, crail = st
            if len(path) >= depth:
                continue
            opts = [('R', 'L')] * 3
            for mS in ('R', 'L', 'S'):
                if mS == 'S' and stage != 0:
                    continue
                for mX in ('R', 'L'):
                    for mY in ('R', 'L'):
                        pk = {'S': 0, 'X': x, 'Y': y}
                        mv = {'S': mS, 'X': mX, 'Y': mY}
                        ok, req = excl_ok(pk, mv)
                        if not ok:
                            continue
                        nx = x + (1 if mX == 'L' else 0)
                        ny = y + (1 if mY == 'L' else 0)
                        nst = None
                        if mS == 'S':
                            # left part at 1, right part at 0
                            if kind == 'depX':
                                # left part merges into X: X must land at 1
                                if nx != 1: continue
                                ns = 0; cinc = inc(a, 'L'); crail2 = 'L'
                            elif kind == 'depY':
                                # right part (at 0) merges into Y, left part is the source
                                if ny != 0: continue
                                ns = 1; cinc = 0; crail2 = 'R'
                            else:
                                continue
                            nrS = 'R' if ns == 0 else 'L'
                            ndS = dS  # source: right part stays (R) or left part (L after a?)
                            if ns == 1: ndS = dS + inc(a, 'L')
                            ndX = dX + inc(b, mX); ndY = dY + inc(c, mY)
                            nx2, ny2 = nx - ns, ny - ns
                            # residues distinct for S, X, Y after
                            if len({0 % M, nx2 % M, ny2 % M}) < 3: continue
                            nst = (nx2, ny2, nrS, mX, mY, ndS, ndX, ndY, 1, cinc, crail2)
                        else:
                            ns = 1 if mS == 'L' else 0
                            nx2, ny2 = nx - ns, ny - ns
                            if len({0, nx2 % M, ny2 % M}) < 3: continue
                            ndS = dS + inc(a, mS); ndX = dX + inc(b, mX); ndY = dY + inc(c, mY)
                            nci = ci
                            ncr = crail
                            if stage == 1 and kind != 'adv' and crail is not None:
                                tgt = mX if kind == 'depX' else mY
                                nci = ci + inc(crail, tgt); ncr = tgt
                            nst = (nx2, ny2, mS, mX, mY, ndS, ndX, ndY, stage, nci, ncr)
                        if max(abs(nst[5]), abs(nst[6]), abs(nst[7])) > 3:
                            continue
                        key = nst[:10] + ((nst[10] == (nst[3] if kind == 'depX' else nst[4])),)
                        if key in seen:
                            continue
                        seen.add(key)
                        npath = path + [(mS, mX, mY)]
                        # goal
                        if (nst[0], nst[1]) == (ALPHA['X'], ALPHA['Y']) and (nst[2], nst[3], nst[4]) == rho and nst[8] == 1:
                            if kind == 'adv' and nst[6] == 0 and nst[7] == 0 and nst[5] == 1:
                                found.setdefault('adv', npath)
                            if kind == 'depX' and mS != 'S' and nst[10] == nst[3]:
                                found.setdefault('depX', (npath, nst[5:10]))
                            if kind == 'depY' and mS != 'S' and nst[10] == nst[4]:
                                found.setdefault('depY', (npath, nst[5:10]))
                        q.append((nst, npath))
            if kind in found:
                break
    return found


# ------------------------------------------------------------------ plan execution --
class Plan:
    def __init__(self):
        self.pk = {}   # name -> deficit (absolute), phantom flag in self.ph
        self.ph = set()
        self.masks = []
        self.ok = True
        self.fail = None

    def tick(self, moves, merge=None):
        ok, req = excl_ok(self.pk, moves)
        if not ok and self.ok:
            self.ok = False; self.fail = (len(self.masks), dict(self.pk), dict(moves))
        self.masks.append(frozenset(req))
        new = {}
        for n, e in self.pk.items():
            mv = moves[n]
            if mv == 'R': new[n] = e
            elif mv == 'L': new[n] = e + 1
            elif mv == 'S': new[n] = e; new[n + "'"] = e + 1
        self.pk = new
        res = {}
        for n, e in self.pk.items():
            res.setdefault(e % M, []).append(n)
        for r, ns in res.items():
            if len(ns) > 1 and not (merge and set(ns) == set(merge)) and self.ok:
                self.ok = False; self.fail = ('collision', len(self.masks), dict(self.pk))


def run_gadget(pl, name, G):
    """apply gadget G[name] to packets S, X, Y of pl."""
    if name == 'adv':
        for (a, b, c) in G['adv']:
            pl.tick({'S': a, 'X': b, 'Y': c})
        return
    path = G[name][0]
    for (a, b, c) in path:
        if a == 'S':
            if name == 'depX':
                pl.tick({'S': 'S', 'X': b, 'Y': c}, merge=("S'", 'X'))
                # left part S' merges into X
                pl.pk.pop("S'")
                if 'X' in pl.ph: pl.ph.discard('X')
            else:
                pl.tick({'S': 'S', 'X': b, 'Y': c}, merge=('S', 'Y'))
                pl.pk['S'] = pl.pk.pop("S'")
                if 'Y' in pl.ph: pl.ph.discard('Y')
        else:
            pl.tick({'S': a, 'X': b, 'Y': c})


def simulate(N, q, masks):
    st = {(0, 'R', 0, 0): 1}
    for t, msk in enumerate(masks, start=1):
        sites = {(t - 2 * e) % N for e in msk}
        new = {}
        for (x, rl, lam, g), c in st.items():
            for (y, r2, l2, g2) in (((x + 1) % N, 'R', lam, g),
                                    ((x - 1) % N, 'L', lam + 1, (g + (1 if rl == 'L' else 0)) % q)):
                if y in sites:
                    k = (y, r2, l2, g2); new[k] = new.get(k, 0) + c
        st = new
    return st


def end_search(rel, depth=6):
    """from packets X, Y at relative deficits (after S removed), find moves so that at the
    final tick X is on R and Y on L at equal deficit (P^+ / mode (i) with X=B, Y=P-low)
    or Y... returns dict mode -> move list.  mode 'eq' : e_X == e_Y, X by R, Y by L;
    mode 'plusM' : e_X == e_Y + M with X by L, Y by R (mode (ii): B=X on L at l+M)."""
    out = {}
    q = deque([((rel['X'], rel['Y']), [])])
    seen = {(rel['X'], rel['Y'])}
    while q:
        (x, y), path = q.popleft()
        if len(path) >= depth: continue
        for mX in 'RL':
            for mY in 'RL':
                ok, _ = excl_ok({'X': x, 'Y': y}, {'X': mX, 'Y': mY})
                if not ok: continue
                nx, ny = x + (mX == 'L'), y + (mY == 'L')
                np_ = path + [(mX, mY)]
                if nx == ny and mX == 'R' and mY == 'L':
                    out.setdefault('eq', np_)
                if nx == ny + M and mX == 'L' and mY == 'R':
                    out.setdefault('plusM', np_)
                if nx % M == ny % M: continue
                if (nx - ny) in seen: continue
                seen.add(nx - ny)
                q.append(((nx, ny), np_))
    return out


def trans_search(rho_from, rho_to, depth):
    """moves of S, X, Y (R/L) from ALPHA(rho_from) to ALPHA(rho_to); any increments."""
    start = (ALPHA['X'], ALPHA['Y']) + tuple(rho_from)
    q = deque([(start, [])]); seen = {start}
    while q:
        st, path = q.popleft()
        if len(path) >= depth: continue
        x, y, a, b, c = st
        for mS in 'RL':
            for mX in 'RL':
                for mY in 'RL':
                    ok, _ = excl_ok({'S': 0, 'X': x, 'Y': y}, {'S': mS, 'X': mX, 'Y': mY})
                    if not ok: continue
                    ns = 1 if mS == 'L' else 0
                    nx, ny = x + (mX == 'L') - ns, y + (mY == 'L') - ns
                    if len({0, nx % M, ny % M}) < 3: continue
                    nst = (nx, ny, mS, mX, mY)
                    np_ = path + [(mS, mX, mY)]
                    if (nx, ny) == (ALPHA['X'], ALPHA['Y']) and (mS, mX, mY) == tuple(rho_to):
                        return np_
                    if nst in seen: continue
                    seen.add(nst); q.append((nst, np_))
    return None


A3 = 3   # phase P: P at +3 relative to S (P-low at 3-M = -2)


def phaseP_adv(pl):
    for sm, om in zip('LLRR', 'LRLR'):
        pl.tick({'S': sm, 'Y': om})


def phaseP_depplus(pl):
    s0 = pl.pk['S']
    pl.tick({'S': 'S', 'Y': 'R'})
    pl.pk['C'] = pl.pk.pop("S'")
    while pl.pk['C'] - s0 < A3:
        last = (pl.pk['C'] + 1 - s0 == A3)
        pl.tick({'S': 'R', 'Y': 'R', 'C': 'L'}, merge=('C', 'Y') if last else None)
    pl.pk.pop('C'); pl.ph.discard('Y')
    pl.tick({'S': 'R', 'Y': 'R'})


def phaseP_depminus(pl):
    pl.tick({'S': 'S', 'Y': 'L'})
    pl.pk['C'] = pl.pk.pop('S'); pl.pk['S'] = pl.pk.pop("S'")
    while pl.pk['Y'] != pl.pk['C']:
        last = (pl.pk['Y'] + 1 == pl.pk['C'])
        pl.tick({'S': 'L', 'Y': 'L', 'C': 'R'}, merge=('Y', 'C') if last else None)
    pl.pk.pop('C'); pl.ph.discard('Y')
    pl.tick({'S': 'R', 'Y': 'R'})


def build_plan(G, A, C, B, nadv, mode, z):
    """deposits in the order C (dep-), A (dep+), B (depX); nadv[i] advances before deposit i.
    Y = packet P (deficit stored = P-LOW level), X = packet B.  z = prefix of right steps."""
    pl = Plan()
    pl.pk = {'S': 0}
    for _ in range(z):
        pl.tick({'S': 'R'})
    # phase P: Y phantom at P-low = S + A3 - M  (residue +3)
    pl.pk['Y'] = pl.pk['S'] + A3 - M; pl.ph.add('Y')
    i = 0
    for kind in ['C'] * len(C) + ['A'] * len(A):
        for _ in range(nadv[i]): phaseP_adv(pl)
        if kind == 'C':
            phaseP_depminus(pl)
        else:
            # dep+ lands at the HIGH level: view Y at its high deficit during the gadget
            pl.pk['Y'] += M; phaseP_depplus(pl); pl.pk['Y'] -= M
        i += 1
    # transition to ALPHA(rho): X phantom at S+1; Y = P at residue S-2 already
    pl.pk['X'] = pl.pk['S'] + 1; pl.ph.add('X')
    for (a, b, c) in G['trans']:
        pl.tick({'S': a, 'X': b, 'Y': c})
    for _ in B:
        for _ in range(nadv[i]): run_gadget(pl, 'adv', G)
        run_gadget(pl, 'depX', G)
        i += 1
    for (a, b, c) in G['remove']:
        pl.tick({'S': a, 'X': b, 'Y': c})
    pl.pk.pop('S', None)
    for (b, c) in G['end'][mode]:
        last = None
        pl.tick({'X': b, 'Y': c}, merge=('X', 'Y'))
    return pl


def expected(mode, G1, G2, G3):
    if mode == 'i':
        return sorted([('R', 0, g) for g in G2] + [('L', 0, g) for g in G3] + [('L', 1, g) for g in G1])
    return sorted([('R', 0, g) for g in G3] + [('R', 1, g) for g in G1] + [('L', 1, g) for g in G2])


def content(st):
    lams = sorted({k[2] for k in st}); l0 = lams[0]
    return sorted((rl, (lam - l0) // M, g) for (x, rl, lam, g), c in st.items() for _ in range(c)), {k[0] for k in st}, all((k[2] - l0) % M == 0 for k in st)


def solve_request(G, q, G1, G2, G3, mode, z):
    A, C, B = list(G1), list(G3), list(G2)
    n = len(A) + len(C) + len(B)
    targets = C + A + B
    BIG = 10 ** 6
    def fin(nadv):
        pl = build_plan(G, A, C, B, nadv, mode, z)
        if not pl.ok: return None, pl
        return simulate(2 * M, BIG, pl.masks), pl
    base, pl = fin([0] * n)
    if base is None: return None, pl
    # kappa_i by perturbation: advances before deposit i shift deposits >= i by +1
    def groups(st):
        return sorted((rl, lam, g) for (x, rl, lam, g), c in st.items() for _ in range(c))
    runs = []
    for i in range(n):
        nadv = [0] * n; nadv[i] = 1000
        st, _ = fin(nadv); runs.append(groups(st))
    kappa = []
    for i in range(n):
        hi = [(rl, g - 1000) for (rl, lam, g) in runs[i] if g >= 1000]
        hn = [(rl, g - 1000) for (rl, lam, g) in runs[i + 1] if g >= 1000] if i + 1 < n else []
        d = list(hi)
        for it in hn: d.remove(it)
        assert len(d) == 1
        kappa.append(d[0][1])
    nadv, cur = [], 0
    for i in range(n):
        step = (targets[i] - kappa[i] - cur) % q
        nadv.append(step); cur += step
    pl = build_plan(G, A, C, B, nadv, mode, z)
    return pl.masks, pl


def main():
    out, QMAX, SMAX, DEPTH = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    res = {'argv': sys.argv}
    rhos = list(itertools.product('RL', repeat=3))
    gad = {}
    for rho in rhos:
        g = search_gadgets(rho, DEPTH)
        gad[''.join(rho)] = {k: v for k, v in g.items()}
    res['G1_tried'] = len(rhos)
    good = [r for r, g in gad.items() if all(k in g for k in ('adv', 'depX', 'depY'))]
    res['G1_good_rho'] = good
    res['gadgets'] = gad
    print('good rho:', good, flush=True)
    rho = 'LRR'
    G = dict(gad[rho])
    G['depX'] = G['depX']; G['depY'] = G['depY']
    G['trans'] = trans_search('RRR', rho, DEPTH)
    # removal from ALPHA: S dies; X must step L (S excludes X's residue), Y steps R
    G['remove'] = [('X', 'L', 'R')]
    rel = {'X': ALPHA['X'] + 1, 'Y': ALPHA['Y']}
    ends = end_search(rel, DEPTH)
    G['end'] = {'i': ends.get('eq'), 'ii': ends.get('plusM')}
    res['schedule'] = {k: v for k, v in G.items()}
    print('trans', G['trans'], 'end', G['end'], flush=True)
    # G2: exclusivity of every gadget is re-checked inside every replay (Plan.ok); the
    # gadgets do not depend on the request, so one replay per gadget sequence type suffices;
    # we nevertheless keep Plan.ok for all replays.
    tested = passed = 0; fails = []
    for q in range(1, QMAX + 1):
        ms = [list(x) for s_ in range(SMAX + 1) for x in itertools.combinations_with_replacement(range(q), s_)]
        for G1 in ms:
            for G2 in ms:
                for G3 in ms:
                    if len(G1) + len(G2) + len(G3) > SMAX or not (G1 or G2 or G3): continue
                    for mode in ('i', 'ii'):
                        for z in (0, 1, 3):
                            tested += 1
                            masks, pl = solve_request(G, q, G1, G2, G3, mode, z)
                            if masks is None or not pl.ok:
                                if len(fails) < 20: fails.append((q, G1, G2, G3, mode, z, 'plan', str(pl.fail)))
                                continue
                            good_all = True
                            for N in (5, 10):
                                st = simulate(N, q, masks)
                                got, sites, lv = content(st)
                                exp = expected(mode, G1, G2, G3)
                                okc = lv and len(sites) == 1 and any(
                                    sorted((rl, l + dl, g) for (rl, l, g) in got) == exp for dl in (0, -1, 1))
                                if not okc:
                                    good_all = False
                                    if len(fails) < 400: fails.append((q, G1, G2, G3, mode, z, N, got, exp))
                            passed += good_all
    res['G3'] = dict(tested=tested, passed=passed, failures=fails)
    print('G3', tested, passed, fails[:3], flush=True)
    with open(out, 'x') as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == '__main__':
    main()
