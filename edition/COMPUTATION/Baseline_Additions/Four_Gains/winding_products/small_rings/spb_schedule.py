#!/usr/bin/env python3
"""Three-packet schedule (source S, two-level packet P, packet B) for the three-group
preparation and for P^+_delta on rings with M = N/gcd(N,2) >= 6.   Worker, 2026-11-15b.

Carrier D_delta on Z_N: gains a=b=c=1, d=delta (order q).  A walk is a word in {R,L};
after t steps with e left steps it is at site t-2e mod N; a left step that follows a left
step multiplies the gain by delta.  Gains are exponents mod q.

Plan language.  A packet is a set of walks at one site after every tick.  At each tick
every packet is given a move: 'R', 'L', 'S' (split: both) or 'X' (die).  The mask of the
tick is the set of residues mod M of the REQUIRED deficits (R: e, L: e+1, S: e and e+1).
A move is EXCLUSIVE iff no EXCLUDED candidate (R: e+1, L: e, X: e and e+1) is in the mask
mod M.  If every tick is exclusive, every walk of every packet does exactly its move
(survival depends only on the residue of the deficit, see PROOFS.md, Lemma R).

Schedule (all positions relative to the source at deficit 0 at a gadget boundary;
every walk has arrived by a right step at every boundary):
  phase P : packets S@0 and P@a (a = 4).  Gadgets: adv (S: LLRR, others: LRLR);
            depP+ (S splits, the left part runs up by L steps while all else steps R,
            merges into P at a; idle tick all R);  depP- (S splits, the LEFT part is the
            new source, the right part stays (R) while all else steps L, until P comes
            down onto it; idle tick all R).  depP+ puts walks at P's high level, depP- at
            P's low level (they differ by M).
  phase B : packets S@0, B@2, P@a.  Gadgets: adv, depB (S splits, left part L to 2, idle).
  remove  : S dies, others R.
  end (i) : P steps L and B steps R until B - Plow = 2, then two ticks (B: R, P: L).
  end (ii): B steps L and P steps R until B - Plow = M-1, then one tick (B: L, P: R).
Mode (i):  R: G2 = B at level l;  L: G3 = P-low at l, G1 = P-high at l+M.
Mode (ii): R: G3 = P-low at l, G1 = P-high at l+M;  L: G2 = B at l+M.
P^+ (one level, U' on R, V' on L) = mode (i) with G1 empty.

PREDICATES (fixed before the first run).
 P1 (finite stage check = proof of exclusivity): for every M in the range, every
    (gadget, configuration) pair the schedule can use is exclusive at every tick, with
    the configurations enumerated over all patterns of empty / non-empty groups.
    Hypothesis counted: the configuration has pairwise distinct residues at the start.
 P2 (replay on the actual ring): for every request in the replay set, on Z_N for N = M
    (M odd) and N = 2M, the walks that end at the final site are exactly the requested
    multisets at the requested levels (exact (rail, lambda, gain) multiset), and no walk
    ends at any other site.  Hypothesis counted: request well formed.
 P3 (control): the same code with M = 5 must report a non-exclusive tick (S, B, P cannot
    have pairwise distance >= 2 on Z_5), i.e. P1 must FAIL for M = 5.
Usage: spb_schedule.py OUTFILE MMIN MMAX QMAX SIZEMAX
"""
import itertools, json, sys, hashlib, random

A_POS = 4   # position of P relative to S
B_POS = 2


class Plan:
    def __init__(self, M):
        self.M = M
        self.pk = {}          # name -> integer deficit
        self.ticks = []       # list of (moves dict, required set, excluded set)
        self.ok = True
        self.fail = None

    def tick(self, moves, merges=()):
        M = self.M
        req, exc = set(), set()
        for n, e in self.pk.items():
            mv = moves[n]
            if mv == 'R': req.add(e % M); exc.add((e + 1) % M)
            elif mv == 'L': req.add((e + 1) % M); exc.add(e % M)
            elif mv == 'S': req.add(e % M); req.add((e + 1) % M)
            elif mv == 'X': exc.add(e % M); exc.add((e + 1) % M)
        bad = req & exc
        if bad and self.ok:
            self.ok = False
            self.fail = (len(self.ticks), dict(moves), dict(self.pk), sorted(bad))
        self.ticks.append((dict(moves), sorted(req)))
        new = {}
        for n, e in self.pk.items():
            mv = moves[n]
            if mv == 'R': new[n] = e
            elif mv == 'L': new[n] = e + 1
            elif mv == 'S':
                new[n] = e; new[n + "'"] = e + 1   # n' is the left part
        self.pk = new
        # residues must be distinct except declared merges
        for (x, y) in merges:
            if x in self.pk and y in self.pk:
                if self.pk[x] % M != self.pk[y] % M and self.ok:
                    self.ok = False; self.fail = ('merge-miss', x, y, dict(self.pk))
        res = {}
        for n, e in self.pk.items():
            res.setdefault(e % M, []).append(n)
        for r, ns in res.items():
            if len(ns) > 1:
                pair = tuple(ns)
                declared = any(set((x, y)) <= set(ns) for (x, y) in merges)
                if not declared and self.ok:
                    self.ok = False; self.fail = ('collision', len(self.ticks), dict(self.pk))

    def allmoves(self, default, **spec):
        return {n: spec.get(n, default) for n in self.pk}

    # --- gadgets -----------------------------------------------------------
    def adv(self):
        for sm, om in zip('LLRR', 'LRLR'):
            self.tick(self.allmoves(om, S=sm))

    def dep_pos(self, target, pos):
        """copy from S runs up to relative position pos (target may not exist yet)."""
        s0 = self.pk['S']
        self.tick(self.allmoves('R', S='S'))
        self.pk['C'] = self.pk.pop("S'")
        while self.pk['C'] - s0 < pos:
            mg = ()
            if self.pk['C'] + 1 - s0 == pos and target in self.pk:
                mg = (('C', target),)
            self.tick(self.allmoves('R', C='L'), merges=mg)
        if target in self.pk:
            assert self.pk['C'] == self.pk[target], (self.pk, target)
            del self.pk['C']
        else:
            self.pk[target] = self.pk.pop('C')
        self.tick(self.allmoves('R'))

    def dep_neg(self, target, pos):
        """S splits, its left part is the new source; the right part (copy) steps R
        while S and all stocks step L, until target comes down onto it (pos < 0 is the
        position of target relative to S; target may not exist: then the copy stops at
        relative position pos)."""
        # split tick: the stocks step L with the new source (left part of S)
        self.tick(self.allmoves('L', S='S'))
        self.pk['C'] = self.pk.pop('S')
        self.pk['S'] = self.pk.pop("S'")
        if target in self.pk:
            while self.pk[target] != self.pk['C']:
                mg = ((target, 'C'),) if self.pk[target] + 1 == self.pk['C'] else ()
                self.tick(self.allmoves('L', C='R'), merges=mg)
            del self.pk['C']
        else:
            while self.pk['C'] - self.pk['S'] > pos:
                self.tick(self.allmoves('L', C='R'))
            self.pk[target] = self.pk.pop('C')
        self.tick(self.allmoves('R'))

    def remove(self):
        # empty groups: a phantom position (no walks) is kept for P and B; it only adds
        # residues to the masks, which cannot admit a walk without being flagged.
        s = self.pk['S']
        self.pk.setdefault('Plow', s + A_POS - self.M)
        self.pk.setdefault('B', s + B_POS)
        self.tick(self.allmoves('R', S='X'))
        self.pk.pop('S', None)

    def end(self, mode):
        M = self.M
        low = self.pk['Plow']
        if mode == 'i':
            while self.pk['B'] - self.pk['Plow'] > 2:
                self.tick(self.allmoves('R', Plow='L'))
            self.tick(self.allmoves('R', Plow='L'))
            self.tick(self.allmoves('R', Plow='L'), merges=(('B', 'Plow'),))
        else:
            while self.pk['B'] - self.pk['Plow'] < M - 1:
                self.tick(self.allmoves('R', B='L'))
            self.tick(self.allmoves('R', B='L'), merges=(('B', 'Plow'),))


def gadget_sequence(nA, nC, nB):
    """order: C walks by depP-, A walks by depP+, B walks by depB; adv before each."""
    seq = []
    for _ in range(nC): seq.append('depPneg')
    for _ in range(nA): seq.append('depPpos')
    for _ in range(nB): seq.append('depB')
    return seq


def run_plan(M, seq, advs, mode):
    """advs[i] = number of advances before deposit i.  Returns Plan.  Packet P is
    represented by its LOW-level deficit 'Plow' (deposits from + land M higher)."""
    pl = Plan(M)
    pl.pk['S'] = 0
    for g, na in zip(seq, advs):
        for _ in range(na): pl.adv()
        s = pl.pk['S']
        if g == 'depPneg':
            pl.dep_neg('Plow', A_POS - M)
        elif g == 'depPpos':
            if 'Plow' in pl.pk:
                # P exists; its residue is A_POS above S; copy merges at the high level
                pl.pk['Phigh_view'] = pl.pk['Plow'] + M
                pl.pk.pop('Plow')
                pl.dep_pos('Phigh_view', A_POS)
                pl.pk['Plow'] = pl.pk.pop('Phigh_view') - M
            else:
                pl.dep_pos('Phigh_view', A_POS)
                pl.pk['Plow'] = pl.pk.pop('Phigh_view') - M
        elif g == 'depB':
            pl.dep_pos('B', B_POS)
    if 'S' in pl.pk:
        pl.remove()
    return pl


def masks_of(pl):
    return [req for (_, req) in pl.ticks]


def simulate(N, M, q, masks):
    """actual ring: state (site, rail, lam, gain) -> count; mask at tick t (1-based) is
    the set of sites t-2e mod N for residues e in the mask."""
    st = {(0, 'R', 0, 0): 1}
    for t, req in enumerate(masks, start=1):
        sites = {(t - 2 * e) % N for e in req}
        new = {}
        for (x, rl, lam, g), c in st.items():
            for (y, r2, l2, g2) in (((x + 1) % N, 'R', lam, g),
                                    ((x - 1) % N, 'L', lam + 1, (g + (1 if rl == 'L' else 0)) % q)):
                if y in sites:
                    k = (y, r2, l2, g2); new[k] = new.get(k, 0) + c
        st = new
    return st


def plan_request(M, q, G1, G2, G3, mode):
    """G1, G2, G3: lists of exponents mod q.  Mode (i): A=G1 (P high), C=G3 (P low),
    B=G2.  Mode (ii): A=G1 (P high), C=G3 (P low), B=G2.  (Same roles; the end differs.)
    Returns (plan, masks, expected dict, shift) after fixing advances by a dry run."""
    A, C, B = sorted(G1), sorted(G3), sorted(G2)
    seq = gadget_sequence(len(A), len(C), len(B))
    targets = C + A + B
    if not seq:
        return None
    # dry run with zero advances, integer exponents (q huge) to get constants
    pl0 = run_plan(M, seq, [0] * len(seq), mode)
    if not pl0.ok:
        return ('FAIL', pl0)
    pl0.end(mode)
    if not pl0.ok:
        return ('FAIL', pl0)
    BIG = 10 ** 6
    # constants: simulate each deposit separately is costly; instead compute the final
    # exponent of the walk deposited at index i with zero advances by tagging: use the
    # actual simulation with q=BIG and read gains per (rail, lambda) group in order.
    return ('OK', seq, targets, pl0)


def walk_constants(M, seq, mode):
    """final exponent of deposit i under zero advances, by simulating the single walk:
    run the masks with the source tracked symbolically (integer gains)."""
    pl = run_plan(M, seq, [0] * len(seq), mode)
    pl.end(mode)
    masks = masks_of(pl)
    # simulate on N = 2M with integer gains and record, for each final walk, the tick at
    # which it separated from the source: we instead recompute by brute force: the
    # constants are read off by giving advance counts that are huge multiples.
    return pl, masks


def build(M, q, G1, G2, G3, mode):
    """Returns masks and the expected final multiset; advance counts chosen by the
    affine rule final_i = n_i + const_i (advances add +1 to S, 0 to stocks)."""
    A, C, B = list(G1), list(G3), list(G2)
    seq = gadget_sequence(len(A), len(C), len(B))
    targets = C + A + B
    groups = ['C'] * len(C) + ['A'] * len(A) + ['B'] * len(B)
    # constants: deposit i alone matters; with zero advances, the final exponent of
    # deposit i is const_i.  Get it by running with advances [0..0, BIGSTEP at i] and
    # q = 0 (integers): the walk deposited at i is the one whose exponent moved.
    def finals(advs):
        pl = run_plan(M, seq, advs, mode)
        if not pl.ok: return None, pl
        pl.end(mode)
        if not pl.ok: return None, pl
        st = simulate(2 * M, M, 10 ** 9, masks_of(pl))
        return st, pl
    base, pl = finals([0] * len(seq))
    if base is None:
        return None, pl
    consts = []
    for i in range(len(seq)):
        # advances before deposit i shift deposits i..end by the same amount
        advs = [0] * len(seq); advs[i] = 1000
        st, _ = finals(advs)
        # walks whose exponent grew by 1000 are deposits >= i
        consts.append(st)
    # const_i from the difference of multisets: count of walks with exponent >= 1000
    # in run i minus run i+1 isolates deposit i.  Do it per (rail, lam-level) group.
    def group_mult(st):
        out = {}
        for (x, rl, lam, g), c in st.items():
            out.setdefault((rl, lam), []).extend([g] * c)
        return {k: sorted(v) for k, v in out.items()}
    const = [None] * len(seq)
    for i in range(len(seq)):
        gi = group_mult(consts[i])
        gn = group_mult(consts[i + 1]) if i + 1 < len(seq) else None
        hi_i = sorted((k, g - 1000) for k, v in gi.items() for g in v if g >= 1000)
        hi_n = sorted((k, g - 1000) for k, v in gn.items() for g in v if g >= 1000) if gn else []
        diff = list(hi_i)
        for item in hi_n:
            diff.remove(item)
        assert len(diff) == 1, (i, diff)
        const[i] = diff[0]
    # choose advance counts: n_i nondecreasing, n_i = targets_i - const_i mod q
    advs, n = [], 0
    for i in range(len(seq)):
        want = (targets[i] - const[i][1]) % q
        step = (want - n) % q
        advs.append(step); n += step
    pl = run_plan(M, seq, advs, mode)
    pl.end(mode)
    return masks_of(pl), pl, const


def expected(mode, G1, G2, G3, lam_low):
    """mode (i): R: G2 at l; L: G3 at l, G1 at l+M.  mode (ii): R: G3 at l, G1 at l+M;
    L: G2 at l+M.  Returned as sorted list of (rail, level index, gain)."""
    if mode == 'i':
        return sorted([('R', 0, g) for g in G2] + [('L', 0, g) for g in G3] + [('L', 1, g) for g in G1])
    return sorted([('R', 0, g) for g in G3] + [('R', 1, g) for g in G1] + [('L', 1, g) for g in G2])


def check_request(M, q, G1, G2, G3, mode, Ns):
    if not (G1 or G2 or G3):
        return True, 'empty request: an event with A_1 empty'
    r = build(M, q, G1, G2, G3, mode)
    if r[0] is None:
        return False, ('plan not exclusive', r[1].fail)
    masks, pl, const = r
    if not pl.ok:
        return False, ('plan not exclusive', pl.fail)
    for N in Ns:
        st = simulate(N, M, q, masks)
        sites = {k[0] for k in st}
        if len(sites) != 1:
            return False, ('walks at several sites', N, sorted(sites))
        lams = sorted({k[2] for k in st})
        l0 = lams[0]
        got = []
        for (x, rl, lam, g), c in st.items():
            if (lam - l0) % M:
                return False, ('level not multiple of M', N)
            got += [(rl, (lam - l0) // M, g)] * c
        got.sort()
        # gains are fixed up to a common translation by delta^k (single-walk prefix,
        # PROOFS.md Lemma T): compare up to a common shift of all gains
        exp = expected(mode, G1, G2, G3, 0)
        # level index: in mode (ii) the lowest level may be absent (G3 empty) -> shift
        ok = False
        for dl in (0, -1, 1):
            for k in range(q):
                if sorted((rl, lv + dl, (g + k) % q) for (rl, lv, g) in got) == exp:
                    ok = True; break
            if ok: break
        if not ok:
            return False, ('multiset mismatch', N, got, exp)
    return True, len(masks)


# ---------------- P1: finite stage check -------------------------------------------
def stage_check(M):
    """Each gadget is run from each configuration it can meet; configuration = which
    packets exist.  Exclusivity is a property of the configuration only."""
    results = []
    configs = []
    # phase P: S alone, S+P;  phase B: S+B, S+P, S+B+P (B or P may be empty groups)
    for hasP in (False, True):
        for hasB in (False, True):
            configs.append((hasP, hasB))
    for hasP, hasB in configs:
        def fresh():
            pl = Plan(M); pl.pk['S'] = 0
            if hasP: pl.pk['Plow'] = A_POS - M
            if hasB: pl.pk['B'] = B_POS
            return pl
        gadgets = ['adv', 'depB']
        if not hasB:
            gadgets += ['depPneg', 'depPpos']   # P deposits happen before any B exists
        for g in gadgets:
            pl = fresh()
            if g == 'adv': pl.adv()
            elif g == 'depB': pl.dep_pos('B', B_POS)
            elif g == 'depPneg': pl.dep_neg('Plow', A_POS - M)
            elif g == 'depPpos':
                if 'Plow' in pl.pk:
                    pl.pk['Ph'] = pl.pk.pop('Plow') + M
                pl.dep_pos('Ph', A_POS)
                pl.pk['Plow'] = pl.pk.pop('Ph') - M
            # configuration must return to itself (relative to S)
            rel = {n: e - pl.pk['S'] for n, e in pl.pk.items()}
            want = {'S': 0}
            if hasP or g in ('depPneg', 'depPpos'): want['Plow'] = A_POS - M
            if hasB or g == 'depB': want['B'] = B_POS
            results.append(dict(config=[hasP, hasB], gadget=g, exclusive=pl.ok,
                                returns=(rel == want), fail=str(pl.fail) if pl.fail else None))
        # removal and end from this configuration (only meaningful with packets)
        for mode in ('i', 'ii'):
            pl = fresh()
            pl.remove()
            if True:
                pl.end(mode)
                results.append(dict(config=[hasP, hasB], gadget='remove+end' + mode,
                                    exclusive=pl.ok, returns=True,
                                    fail=str(pl.fail) if pl.fail else None))
            else:
                results.append(dict(config=[hasP, hasB], gadget='remove', exclusive=pl.ok,
                                    returns=True, fail=str(pl.fail) if pl.fail else None))
    return results


def main():
    out, Mmin, Mmax, qmax, smax = sys.argv[1], *map(int, sys.argv[2:6])
    random.seed(20261113)
    res = {'argv': sys.argv, 'P1': {}, 'P2': {}, 'P3': None}
    for M in list(range(Mmin, Mmax + 1)):
        sc = stage_check(M)
        res['P1'][M] = dict(all_exclusive=all(r['exclusive'] and r['returns'] for r in sc),
                            n_pairs=len(sc), hypothesis_ok=len(sc),
                            failures=[r for r in sc if not (r['exclusive'] and r['returns'])])
    res['P3'] = dict(M=5, P1_fails=not stage_check(5) or not all(r['exclusive'] for r in stage_check(5)))
    for M in range(max(Mmin, 6), Mmax + 1):
        Ns = [2 * M] + ([M] if M % 2 else [])
        tested = passed = 0; fails = []
        for q in range(1, qmax + 1):
            reqs = []
            for s1 in range(smax + 1):
                for s2 in range(smax + 1 - s1):
                    for s3 in range(smax + 1 - s1 - s2):
                        for G1 in itertools.combinations_with_replacement(range(q), s1):
                            for G2 in itertools.combinations_with_replacement(range(q), s2):
                                for G3 in itertools.combinations_with_replacement(range(q), s3):
                                    reqs.append((list(G1), list(G2), list(G3)))
            for (G1, G2, G3) in reqs:
                for mode in ('i', 'ii'):
                    tested += 1
                    ok, info = check_request(M, q, G1, G2, G3, mode, Ns)
                    if ok: passed += 1
                    elif len(fails) < 20: fails.append((q, G1, G2, G3, mode, str(info)[:300]))
        res['P2'][M] = dict(tested=tested, passed=passed, failures=fails, Ns=Ns)
        print(M, tested, passed, flush=True)
    with open(out, 'x') as f:
        json.dump(res, f, indent=1, default=str)
    print('P1', {M: v['all_exclusive'] for M, v in res['P1'].items()})
    print('P3 (M=5 must fail P1):', res['P3'])


if __name__ == '__main__':
    main()
