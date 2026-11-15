#!/usr/bin/env python3
"""Exhaustive bounded search of position product events in D_delta on rings of a given M,
for the requests of P^+_delta (one level) and of the three-group modes.  Worker 2026-11-15b.

Model (PROOFS.md, Lemma R): a walk is (e, rail, g): e = number of left steps (deficit),
rail of the last step, g = gain exponent mod q.  A mask at a tick is a set of residues mod M
of deficits; a walk survives a step iff its new deficit mod M is in the mask.  A left step
after a left step adds 1 to g.  Start: one walk (0, R, 0).  A residue class at a tick is one
site; its walks on R and on L, with their deficits, are what the ring shows at that site.

Normalisation (both are symmetries of the set of reachable site contents, PROOFS.md
Lemmas S and T): deficits are taken relative to the least deficit present; gains up to a
common translation (least rotation of the state).

RELAXATION.  A residue class whose number of walks exceeds 2W is removed from the state
(contents of every tick are recorded BEFORE the removal; corrected before any result was
kept: a first trial dropped at W, which removes the final site itself).
The number of walks of a site never decreases along its future except by dying, and a
site that ends as one rail of a request of size <= W never held more than W walks, so
every request with both sides of size <= W that a real event of length <= T meets is
also met by the relaxed search within T (soundness of "not met").  Every request the
relaxed search meets is replayed WITHOUT relaxation on the actual ring Z_N (N = 2M, and
N = M if M is odd) along the recorded mask sequence; only replayed requests count as met.

PREDICATES (fixed before the first run).
 B1 (P^+ requests): for each (M, q, W, T): the set of requests (U', V'), multisets of
    Z_q of sizes <= W, not both empty, up to a common translation, that are met at one
    level; and the list of those NOT met within length T.  Hypothesis counted: request
    well formed (number of requests listed).
 B2 (three-group requests): same for mode (i) [R: G2 at l; L: G3 at l, G1 at l+M] and
    mode (ii) [R: G3 at l, G1 at l+M; L: G2 at l+M] with G1, G2, G3 all NON-EMPTY (the
    case that needs two levels), sizes <= W each.
 B3 (bound): the number of states of every layer is <= CAP; if CAP is hit the run says
    INCOMPLETE and no "not met" statement is made from it.
 Control C1: q = 1 (counts only), M = 5: every one-level profile (u, v) with u, v <= W
    is met (the draft's remark (c) reports all profiles allowed by cor:tp seen on 5 sites).
Usage: bfs_small.py OUTFILE M q W T CAP
"""
import sys, json, itertools, time


def canon(walks, q):
    """walks: dict (e, rail, g) -> count.  Normalise deficits and gains."""
    if not walks:
        return ()
    m = min(k[0] for k in walks)
    best = None
    for k in range(q):
        t = tuple(sorted(((e - m), r, (g + k) % q, c) for (e, r, g), c in walks.items()))
        if best is None or t < best:
            best = t
    return best


def step(state, mask, M, q, W):
    new = {}
    for (e, r, g, c) in state:
        if e % M in mask:
            k = (e, 'R', g); new[k] = new.get(k, 0) + c
        if (e + 1) % M in mask:
            k = (e + 1, 'L', (g + (1 if r == 'L' else 0)) % q); new[k] = new.get(k, 0) + c
    # relaxation: drop residue classes with more than 2W walks (a packet one tick
    # before the end holds one rail of a request, or two groups of a three-group
    # request, so at most 2W walks); contents are RECORDED before dropping.
    tot = {}
    for (e, r, g), c in new.items():
        tot[e % M] = tot.get(e % M, 0) + c
    return new, {k: c for k, c in new.items() if tot[k[0] % M] <= 2 * W}


def rot_min(lst_pairs, q):
    """lst_pairs: tuple of tuples of gains; least common rotation."""
    best = None
    for k in range(q):
        t = tuple(tuple(sorted((g + k) % q for g in part)) for part in lst_pairs)
        if best is None or t < best:
            best = t
    return best


def site_contents(state, M, q):
    """yield, for each residue class: dict level -> (Rgains, Lgains)."""
    by = {}
    for (e, r, g, c) in state:
        by.setdefault(e % M, []).append((e, r, g, c))
    for res, ws in by.items():
        lo = min(w[0] for w in ws)
        levels = {}
        for (e, r, g, c) in ws:
            lv = (e - lo) // M
            d = levels.setdefault(lv, ([], []))
            (d[0] if r == 'R' else d[1]).extend([g] * c)
        yield res, levels


def simulate_real(N, M, q, masks):
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


def real_contents(st, M, q, N):
    by = {}
    for (x, rl, lam, g), c in st.items():
        by.setdefault(x, []).append((lam, rl, g, c))
    out = []
    for x, ws in by.items():
        lo = min(w[0] for w in ws)
        levels = {}
        for (lam, r, g, c) in ws:
            assert (lam - lo) % M == 0
            lv = (lam - lo) // M
            d = levels.setdefault(lv, ([], []))
            (d[0] if r == 'R' else d[1]).extend([g] * c)
        out.append(levels)
    return out


def key_pplus(levels, q):
    if len(levels) != 1:
        return None
    (R, L), = levels.values()
    return rot_min((R, L), q)


def key_modes(levels, q):
    """return list of ('i'|'ii', (G1,G2,G3) normalised) the site content realises."""
    out = []
    lv = sorted(levels)
    if len(lv) != 2 or lv[1] - lv[0] != 1:
        return out
    (R0, L0), (R1, L1) = levels[lv[0]], levels[lv[1]]
    # mode (i): R: G2 at l, nothing at l+M on R; L: G3 at l, G1 at l+M
    if R0 and not R1 and L0 and L1:
        out.append(('i', rot_min((L1, R0, L0), q)))
    # mode (ii): R: G3 at l, G1 at l+M; L: G2 at l+M, nothing at l on L
    if R0 and R1 and L1 and not L0:
        out.append(('ii', rot_min((R1, L1, R0), q)))
    return out


def main():
    out, M, q, W, T, CAP = sys.argv[1], *map(int, sys.argv[2:7])
    t0 = time.time()
    start = canon({(0, 'R', 0): 1}, q)
    parent = {start: None}
    layer = [start]
    met_p, met_m = {}, {}          # key -> state where first seen (relaxed)
    complete = True
    layer_sizes = []
    for t in range(1, T + 1):
        nxt = []
        for s in layer:
            cand = sorted({e % M for (e, r, g, c) in s} | {(e + 1) % M for (e, r, g, c) in s})
            for bits in range(1, 1 << len(cand)):
                mask = frozenset(cand[i] for i in range(len(cand)) if bits >> i & 1)
                full, w = step(s, mask, M, q, W)
                if not full:
                    continue
                # record every transition (before deduplication): witness = (s, mask)
                for res, levels in site_contents(canon(full, q), M, q):
                    kp = key_pplus(levels, q)
                    if kp is not None and len(kp[0]) <= W and len(kp[1]) <= W and kp not in met_p:
                        met_p[kp] = (s, mask)
                    for km in key_modes(levels, q):
                        if all(len(x) <= W for x in km[1]) and km not in met_m:
                            met_m[km] = (s, mask)
                c = canon(w, q)
                if c in parent:
                    continue
                parent[c] = (s, mask)
                if w:
                    nxt.append(c)
        layer = nxt
        layer_sizes.append(len(layer))
        print(f't={t} layer={len(layer)} total={len(parent)} metP={len(met_p)} metM={len(met_m)} {time.time()-t0:.1f}s', flush=True)
        if len(layer) > CAP or len(parent) > 6 * CAP:
            complete = False
            print('CAP hit: INCOMPLETE', flush=True)
            break
        if not layer:
            break

    # replay witnesses on the real ring.  The canonical state forgets the deficit and
    # gain normalisation, so the mask sequence is re-expressed: we replay masks as
    # recorded relative to each canonical parent and track the shift.
    def masks_to(wit):
        s0, m0 = wit
        seq = [(s0, m0)]
        c = s0
        while parent[c] is not None:
            s, mask = parent[c]
            seq.append((s, mask))
            c = s
        seq.reverse()   # last element is the witness transition itself
        # convert relative masks into absolute ones: each canonical state is the real
        # state shifted by -m (least deficit); track m along the path.
        absm, shift = [], 0
        cur = {(0, 'R', 0): 1}
        for s, mask in seq:
            # mask is in coordinates of s = cur shifted by -shift
            amask = frozenset((r + shift) % M for r in mask)
            absm.append(amask)
            new = {}
            for (e, r, g), cc in cur.items():
                if e % M in amask:
                    k = (e, 'R', g); new[k] = new.get(k, 0) + cc
                if (e + 1) % M in amask:
                    k = (e + 1, 'L', (g + (1 if r == 'L' else 0)) % q); new[k] = new.get(k, 0) + cc
            # follow the relaxed state: drop classes > W as the search did
            tot = {}
            for (e, r, g), cc in new.items():
                tot[e % M] = tot.get(e % M, 0) + cc
            last = new
            cur = {k: cc for k, cc in new.items() if tot[k[0] % M] <= 2 * W}
            shift = min(k[0] for k in cur) if cur else 0
        return absm

    Ns = [2 * M] + ([M] if M % 2 else [])
    confirmed_p, unconf_p = [], []
    for kp, c in met_p.items():
        masks = masks_to(c)
        ok = True
        for N in Ns:
            st = simulate_real(N, M, q, masks)
            if not any(key_pplus(lv, q) == kp for lv in real_contents(st, M, q, N)):
                ok = False
        (confirmed_p if ok else unconf_p).append(kp)
    confirmed_m, unconf_m = [], []
    for km, c in met_m.items():
        masks = masks_to(c)
        ok = True
        for N in Ns:
            st = simulate_real(N, M, q, masks)
            if not any(km in key_modes(lv, q) for lv in real_contents(st, M, q, N)):
                ok = False
        (confirmed_m if ok else unconf_m).append(km)

    # all requests
    ms = [tuple(x) for s in range(W + 1) for x in itertools.combinations_with_replacement(range(q), s)]
    allp = sorted({rot_min((u, v), q) for u in ms for v in ms if u or v})
    alln = [x for x in ms if x]
    allm = sorted({(md, rot_min((a, b, c), q)) for md in ('i', 'ii') for a in alln for b in alln for c in alln})
    sp, sm = set(confirmed_p), set(confirmed_m)
    res = dict(argv=sys.argv, M=M, q=q, W=W, T=T, CAP=CAP, complete=complete,
               layer_sizes=layer_sizes, n_states=len(parent), seconds=round(time.time() - t0, 1),
               B1=dict(n_requests=len(allp), n_met=len(sp & set(allp)),
                       not_met=[r for r in allp if r not in sp] if complete else 'INCOMPLETE',
                       met_but_replay_failed=unconf_p),
               B2=dict(n_requests=len(allm), n_met=len(sm & set(allm)),
                       not_met=[r for r in allm if r not in sm] if complete else 'INCOMPLETE',
                       met_but_replay_failed=unconf_m))
    with open(out, 'x') as f:
        json.dump(res, f, indent=0, default=str)
    print(json.dumps({k: (v if k not in ('B1', 'B2') else {kk: (vv if not isinstance(vv, list) or len(vv) < 30 else f'{len(vv)} items') for kk, vv in v.items()}) for k, v in res.items()}, default=str))


if __name__ == '__main__':
    main()
