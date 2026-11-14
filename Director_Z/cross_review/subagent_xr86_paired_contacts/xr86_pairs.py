"""xr86: own program for 'Paired contacts and joint characters' (cross-review).

Model (my own reading of the note, not its checker): walker i in frequency s_i in Z_M,
lag l_i, z_i = zeta_M^(s_i l_i).  Two arms: incoming R amplitude 1, incoming L amplitude z_i.
Singleton: Hadamard, read exit (h=+1 on R).  Pair: pointer mark = (incoming rails equal),
kept coherent inside a mark, Hadamard on each, read both exits; chi=+1 if exits agree;
H = -chi on equal mark, +chi on different mark.  Product over blocks in a pure sector.
Exact arithmetic in Q[zeta_M] = Q[x]/Phi_M.  Survival is sector independent (1/2 per walker).

PREDICATES (fixed before first run).  Each records qualifying / pass / fail.
 P1  M=4, all 16 sigma in {+-1}^4, readers (12),(34), lags 1: decoded (H12,H34) equals
     (s1 s2, s3 s4) with conditional probability 1; per-launch rate 1/16.
 P1x Same panels equal the note's filed word_panels (cross-check against its JSON, if path given).
 P2  n in 2..6: HYPOTHESIS n even (parity invariant under global conjugation).  For qualifying n,
     the two uniform parity ensembles have equal marginals on every proper subset.
     n odd is expected NOT to qualify and is kept.
 P3  M=4, n=4: over all 10 block settings x 256 lags, the full record law (marks, exits) differs
     between the two parity ensembles ONLY for two-pair settings with all four lags odd
     (expected 3 x 16 = 48 settings); every setting with a singleton block is blind.
 P4  M in {2,3,4,6,8}: HYPOTHESIS orbit {+1,-1} has two elements (M>2).  For qualifying M and
     every lag vector with readers (12),(34): E[H12 H34 | survive] is +-prod sin(theta_i) on the
     two ensembles; record 'certain' = some lag makes the supports disjoint.
     Prediction fixed in advance: certain iff 4 | M.
 P5  Loss rival, pair level: sigma independent uniform, j=1/8 if u=v else 0, singles 1/4-j,
     double miss 1/2+j: all 9 decoded cells equal the ideal t=+1 table; each reader's
     efficiency is 1/4 for every (u,v).
 P6  Loss rival, walker level (my extension: split singles over 3 and double miss over 9
     survival patterns uniformly): all (survival pattern, reported signs) cells equal ideal t=+1.
 P7  Family: true parity t0, observed t_obs, zero pair means.  A loss with truthful reports and
     reader efficiency exactly 1/4 for every (u,v) exists iff (t_obs-3)/4 <= t0 <= (t_obs+3)/4.
     Tested on a grid of t0,t_obs in {-1,-3/4,...,1} by direct construction (j_=, j_!= in [0,1/4]).
     Cells predicted infeasible are kept.
 P8  Fourier: seeded random integer weights, (M,n) in {(4,2),(3,3),(4,3),(6,2),(8,2),(3,4)} (the note
     reports only (4,4)): C(l) built from D_S of my amplitude model equals sum b cos(2 pi s.l/M),
     inversion gives the conjugation-folded weights, count weight = 1-C(0).
 P9  Other matchings for the loss rival: the rival tuned to (12)(34) (acceptance depending on
     u=v only) is tested on matching (13)(24) under the SAME hidden law; recorded whether a
     setting-dependent acceptance is needed (expected: yes, same construction with u',v').
Seed 86.  Refuses to overwrite its result file.
"""
import json, sys, random
from fractions import Fraction as Q
from itertools import product, combinations
from collections import defaultdict

PHI = {2: [1, 1], 3: [1, 1, 1], 4: [1, 0, 1], 6: [1, -1, 1], 8: [1, 0, 0, 0, 1]}  # low->high


class Cyc:
    """element of Q[x]/Phi_M, x = zeta_M"""
    def __init__(s, M, c):
        s.M = M; d = len(PHI[M]) - 1
        c = list(c) + [Q(0)] * max(0, d - len(c))
        p = PHI[M]
        for k in range(len(c) - 1, d - 1, -1):
            a = c[k]
            if a:
                for i in range(d + 1):
                    c[k - d + i] -= a * p[i]
        s.c = tuple(Q(v) for v in c[:d])
    def __add__(s, o): return Cyc(s.M, [a + b for a, b in zip(s.c, o.c)])
    def __sub__(s, o): return Cyc(s.M, [a - b for a, b in zip(s.c, o.c)])
    def __mul__(s, o):
        if not isinstance(o, Cyc): return Cyc(s.M, [a * Q(o) for a in s.c])
        r = [Q(0)] * (2 * len(s.c))
        for i, a in enumerate(s.c):
            for j, b in enumerate(o.c): r[i + j] += a * b
        return Cyc(s.M, r)
    def conj(s):
        r = [Q(0)] * (s.M + 1)
        for i, a in enumerate(s.c): r[(-i) % s.M] += a
        return Cyc(s.M, r)
    def __eq__(s, o): return s.c == o.c
    def __hash__(s): return hash(s.c)
    def rational(s): return all(v == 0 for v in s.c[1:])
    def q(s):
        assert s.rational(), s.c
        return s.c[0]
    def show(s): return str(s.c[0]) if s.rational() else str([str(v) for v in s.c])


def zeta(M, k):
    c = [Q(0)] * M; c[k % M] = Q(1); return Cyc(M, c)
def one(M): return zeta(M, 0)
def zero(M): return one(M) * 0
def cosM(M, k): return (zeta(M, k) + zeta(M, -k)) * Q(1, 2)


def single_law(M, z):
    o = one(M)
    aR, aL = (o + z) * Q(1, 2), (o - z) * Q(1, 2)
    return {('s', 0): aR * aR.conj(), ('s', 1): aL * aL.conj()}


def pair_law(M, zi, zj):
    o = one(M); law = {}
    for mark in (True, False):
        for c in (0, 1):
            for d in (0, 1):
                amp = zero(M)
                for a in (0, 1):
                    for b in (0, 1):
                        if (a == b) != mark: continue
                        t = o
                        if a: t = t * zi
                        if b: t = t * zj
                        if (a * c + b * d) % 2: t = t * -1
                        amp = amp + t
                amp = amp * Q(1, 4)
                law[('p', mark, c, d)] = amp * amp.conj()
    return law


def score(rec):
    if rec[0] == 's': return 1 - 2 * rec[1]
    chi = 1 if rec[2] == rec[3] else -1
    return -chi if rec[1] else chi


def setting_law(M, blocks, s, l):
    """joint record law for a pure sector; product over blocks"""
    laws = []
    for b in blocks:
        z = [zeta(M, s[i] * l[i]) for i in b]
        laws.append(single_law(M, z[0]) if len(b) == 1 else pair_law(M, z[0], z[1]))
    out = {}
    for combo in product(*[list(x.items()) for x in laws]):
        p = one(M)
        for _, v in combo: p = p * v
        out[tuple(k for k, _ in combo)] = p
    return out


def mix(M, blocks, ens, l):
    tot = defaultdict(lambda: zero(M))
    for s, w in ens.items():
        for k, v in setting_law(M, blocks, s, l).items():
            tot[k] = tot[k] + v * w
    return {k: v for k, v in tot.items() if v != zero(M)}


def partitions(n):
    """all partitions of range(n) into singletons and pairs"""
    def rec(rest):
        if not rest: yield (); return
        a = rest[0]
        for p in rec(rest[1:]): yield ((a,),) + p
        for k in range(1, len(rest)):
            for p in rec(rest[1:k] + rest[k + 1:]): yield ((a, rest[k]),) + p
    return list(rec(tuple(range(n))))


def parity_ens(n, par, plus=1):
    v = [s for s in product((-1, 1), repeat=n) if (1 if sum(x < 0 for x in s) % 2 == 0 else -1) == par]
    return {s: Q(1, len(v)) for s in v}


R = {"seed": 86, "predicates": {}, "detail": {}}
def rec(name, qual, passed, failed, note=""):
    R["predicates"][name] = dict(qualifying=qual, passed=passed, failed=failed, note=note)


def main():
    out = sys.argv[1]
    filed = sys.argv[2] if len(sys.argv) > 2 else None
    fh = open(out, "x")
    random.seed(86)
    B2 = ((0, 1), (2, 3))

    # P1
    ok = bad = 0; panels = {}
    for s in product((-1, 1), repeat=4):
        law = setting_law(4, B2, s, (1, 1, 1, 1))
        dec = defaultdict(lambda: Q(0))
        for k, v in law.items(): dec[(score(k[0]), score(k[1]))] += v.q() * Q(1, 16)
        dec = {k: v for k, v in dec.items() if v}
        panels[str(s)] = {str(k): str(v) for k, v in sorted(dec.items())}
        if dec == {(s[0] * s[1], s[2] * s[3]): Q(1, 16)}: ok += 1
        else: bad += 1
    rec("P1", 16, ok, bad, "certain decode, per-launch 1/16")
    if filed:
        f = json.load(open(filed))["three_tick_experiment"]["word_panels"]
        same = sum(1 for k in panels if {a: b for a, b in f.get(k, {}).items() if b != "0"} == panels[k])
        rec("P1x", 16, same, 16 - same, "equal to filed word_panels")

    # P2
    q = p = fl = 0; det = {}
    for n in range(2, 7):
        if n % 2:
            # hypothesis: parity invariant under s -> -s
            det[n] = "not qualifying: parity flips under global conjugation"
            continue
        q += 1
        e = [parity_ens(n, -1), parity_ens(n, 1)]
        good = True
        for r in range(n):
            for idx in combinations(range(n), r):
                m = []
                for en in e:
                    d = defaultdict(lambda: Q(0))
                    for s, w in en.items(): d[tuple(s[i] for i in idx)] += w
                    m.append(dict(d))
                good &= m[0] == m[1]
        det[n] = "pass" if good else "FAIL"
        p += good; fl += (not good)
    rec("P2", q, p, fl, json.dumps(det))

    # P3
    e = [parity_ens(4, -1), parity_ens(4, 1)]
    dist = []; nset = 0
    for blocks in partitions(4):
        for l in product(range(4), repeat=4):
            nset += 1
            if mix(4, blocks, e[0], l) != mix(4, blocks, e[1], l):
                dist.append((blocks, l))
    expected = all(all(len(b) == 2 for b in bl) and all(x % 2 for x in l) for bl, l in dist)
    rec("P3", nset, int(expected and len(dist) == 48), int(not (expected and len(dist) == 48)),
        "distinguishing settings: %d; all are two-pair with all lags odd: %s" % (len(dist), expected))
    R["detail"]["P3_distinguishing_matchings"] = sorted({str(b) for b, _ in dist})

    # P4
    q = p = fl = 0; det = {}
    for M in (2, 3, 4, 6, 8):
        if (1 % M) == (-1 % M):
            det[M] = "not qualifying: +1 = -1 mod M, single-element orbit, no orientation sign"
            continue
        q += 1
        e = [parity_ens(4, -1), parity_ens(4, 1)]
        good = True; certain = []; best = None
        for l in product(range(M), repeat=4):
            laws = [mix(M, B2, en, l) for en in e]
            means = []
            for lw in laws:
                m = zero(M)
                for k, v in lw.items(): m = m + v * (score(k[0]) * score(k[1]))
                means.append(m)
            # prod sin(theta_i) for sigma=all +1: sin = (z - z^-1)/(2i); prod of four -> /16
            pr = one(M)
            for li in l: pr = pr * (zeta(M, li) - zeta(M, -li))
            pr = pr * Q(1, 16)
            good &= (means[1] == pr and means[0] == pr * -1)
            if not (set(laws[0]) & set(laws[1])): certain.append(l)
            if best is None or (pr.rational() and best.rational() and abs(pr.q()) > abs(best.q())): best = pr
        det[M] = dict(mean_identity=good, certain_lags=len(certain), example=str(certain[:1]),
                      largest_rational_contrast=best.show(), predicted_certain=(M % 4 == 0),
                      prediction_ok=(bool(certain) == (M % 4 == 0)))
        okM = good and det[M]["prediction_ok"]
        p += okM; fl += (not okM)
    rec("P4", q, p, fl, "M=2 not qualifying")
    R["detail"]["P4"] = det

    # P5 / P6
    def ideal(t):
        f = defaultdict(lambda: Q(0)); fw = defaultdict(lambda: Q(0))
        for s, w in parity_ens(4, t).items():
            u, v = s[0] * s[1], s[2] * s[3]
            for pat in product((0, 1), repeat=4):
                a, b = pat[0] & pat[1], pat[2] & pat[3]
                f[(u * a, v * b)] += w * Q(1, 16); fw[(pat, u * a, v * b)] += w * Q(1, 16)
        return dict(f), dict(fw)
    def loss(law, jeq, jne):
        f = defaultdict(lambda: Q(0)); fw = defaultdict(lambda: Q(0)); eff = set()
        full1 = [p_ for p_ in product((0, 1), repeat=4) if p_[0] & p_[1] and not (p_[2] & p_[3])]
        full2 = [p_ for p_ in product((0, 1), repeat=4) if p_[2] & p_[3] and not (p_[0] & p_[1])]
        none = [p_ for p_ in product((0, 1), repeat=4) if not (p_[0] & p_[1]) and not (p_[2] & p_[3])]
        for s, w in law.items():
            u, v = s[0] * s[1], s[2] * s[3]
            j = jeq if u == v else jne
            cells = {(u, v): j, (u, 0): Q(1, 4) - j, (0, v): Q(1, 4) - j, (0, 0): Q(1, 2) + j}
            assert sum(cells.values()) == 1 and min(cells.values()) >= 0
            eff.add((cells[(u, v)] + cells[(u, 0)], cells[(u, v)] + cells[(0, v)]))
            for k, pk in cells.items(): f[k] += w * pk
            fw[((1, 1, 1, 1), u, v)] += w * j
            for p_ in full1: fw[(p_, u, 0)] += w * (Q(1, 4) - j) / 3
            for p_ in full2: fw[(p_, 0, v)] += w * (Q(1, 4) - j) / 3
            for p_ in none: fw[(p_, 0, 0)] += w * (Q(1, 2) + j) / 9
        return {k: v for k, v in f.items() if v}, {k: v for k, v in fw.items() if v}, eff
    indep = {s: Q(1, 16) for s in product((-1, 1), repeat=4)}
    fi, fwi = ideal(1)
    fl_, fwl, eff = loss(indep, Q(1, 8), Q(0))
    cells9 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]
    same = sum(fi.get(c, 0) == fl_.get(c, 0) for c in cells9)
    rec("P5", 9, same, 9 - same, "efficiencies per (u,v): %s" % sorted(str(x) for x in eff))
    R["detail"]["P5_table"] = {str(c): str(fi.get(c, 0)) for c in cells9}
    keys = set(fwi) | set(fwl)
    same = sum(fwi.get(k, 0) == fwl.get(k, 0) for k in keys)
    rec("P6", len(keys), same, len(keys) - same, "walker-level survival pattern x reported signs")

    # P7
    grid = [Q(k, 4) for k in range(-4, 5)]
    q = p = fl = 0; infeasible = []
    for t0 in grid:
        for tobs in grid:
            q += 1
            # law with zero pair means and fourfold parity t0
            law = {s: (1 + t0 * s[0] * s[1] * s[2] * s[3]) / 16 for s in product((-1, 1), repeat=4)}
            peq, pne = (1 + t0) / 2, (1 - t0) / 2
            feas = True; js = []
            for pr_, target in ((peq, (1 + tobs) / 32), (pne, (1 - tobs) / 32)):
                if pr_ == 0:
                    feas &= (target == 0); js.append(Q(0))
                else:
                    j = target / pr_; feas &= (0 <= j <= Q(1, 4)); js.append(j)
            pred = (tobs - 3) / 4 <= t0 <= (tobs + 3) / 4
            okc = (feas == pred)
            if feas:
                f, _, eff = loss(law, js[0], js[1])
                okc &= (f == {k: v for k, v in ideal_t(tobs).items() if v}) and eff == {(Q(1, 4), Q(1, 4))}
            else:
                infeasible.append((str(t0), str(tobs)))
            p += okc; fl += (not okc)
    rec("P7", q, p, fl, "infeasible (t0,t_obs) cells kept: %d" % len(infeasible))
    R["detail"]["P7_infeasible"] = infeasible

    # P8
    det = {}; q = p = fl = 0
    for M, n in ((4, 2), (3, 3), (4, 3), (6, 2), (8, 2), (3, 4)):
        q += 1
        freqs = list(product(range(M), repeat=n))
        raw = {s: random.randint(0, 9) for s in random.sample(freqs, min(5, len(freqs)))}
        cnt = random.randint(1, 9); den = sum(raw.values()) + cnt
        good = True; C = {}
        evens = [S for r in range(0, n + 1, 2) for S in combinations(range(n), r)]
        for l in freqs:
            tot = zero(M)
            for S in evens:
                blocks = tuple((S[i], S[i + 1]) for i in range(0, len(S), 2)) + tuple((i,) for i in range(n) if i not in S)
                D = zero(M)
                for s, w in raw.items():
                    m = one(M)
                    for b in blocks:
                        z = [zeta(M, s[i] * l[i]) for i in b]
                        lw = single_law(M, z[0]) if len(b) == 1 else pair_law(M, z[0], z[1])
                        mb = zero(M)
                        for k, v in lw.items(): mb = mb + v * score(k)
                        m = m * mb
                    D = D + m * Q(w, den)
                tot = tot + D * ((-1) ** (len(S) // 2))  # count component contributes 0
            want = zero(M)
            for s, w in raw.items(): want = want + cosM(M, sum(a * b for a, b in zip(s, l))) * Q(w, den)
            good &= (tot == want); C[l] = tot
        good &= (one(M) - C[freqs[0]] == one(M) * Q(cnt, den))
        for s in freqs:
            w = zero(M)
            for l in freqs: w = w + C[l] * cosM(M, sum(a * b for a, b in zip(s, l)))
            w = w * Q(1, M ** n)
            neg = tuple(-a % M for a in s)
            good &= (w == one(M) * Q(raw.get(s, 0) + raw.get(neg, 0), 2 * den))
        det["M=%d,n=%d" % (M, n)] = "pass" if good else "FAIL"
        p += good; fl += (not good)
    rec("P8", q, p, fl, json.dumps(det))

    # P9
    f13 = defaultdict(lambda: Q(0))
    for s, w in indep.items():
        u, v = s[0] * s[1], s[2] * s[3]; up, vp = s[0] * s[2], s[1] * s[3]
        j = Q(1, 8) if u == v else Q(0)  # same hidden acceptance rule, readers now (13),(24)
        for k, pk in {(up, vp): j, (up, 0): Q(1, 4) - j, (0, vp): Q(1, 4) - j, (0, 0): Q(1, 2) + j}.items():
            f13[k] += w * pk
    f13 = {k: v for k, v in f13.items() if v}
    # note u=v iff u'=v' (both say prod sigma = +1), so the same rule works for every matching
    rec("P9", 1, int(f13 == {k: v for k, v in fi.items() if v}), int(f13 != {k: v for k, v in fi.items() if v}),
        "acceptance rule 'prod sigma = +1' is matching independent: u=v iff u'=v'")

    json.dump(R, fh, indent=1); fh.write("\n"); fh.close()
    bad = {k: v for k, v in R["predicates"].items() if v["failed"]}
    for k, v in R["predicates"].items(): print(k, v)
    print("FAILED:", sorted(bad))
    return 1 if bad else 0


def ideal_t(t):
    f = defaultdict(lambda: Q(0))
    for s in product((-1, 1), repeat=4):
        w = (1 + t * s[0] * s[1] * s[2] * s[3]) / 16
        u, v = s[0] * s[1], s[2] * s[3]
        for a in (0, 1):
            for b in (0, 1):
                pa = Q(1, 4) if a else Q(3, 4); pb = Q(1, 4) if b else Q(3, 4)
                f[(u * a, v * b)] += w * pa * pb
    return dict(f)


if __name__ == "__main__":
    sys.exit(main())
