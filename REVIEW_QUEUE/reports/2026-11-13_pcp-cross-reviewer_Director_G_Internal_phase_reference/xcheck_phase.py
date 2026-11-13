"""Cross-review program for Director_G/Internal_phase_reference.md (own code, note's definitions only).

CONVENTIONS. zeta = exp(2*pi*i/M). Sites 0..2K-1; direction +1 = R, -1 = L. One tick from (x,c,y):
sheet y += g(x); amplitude 1/sqrt2 to each outgoing d, sign -1 iff c == d == -1; x += d. Signed integer
path counts m_y; mass of a complete record after t ticks = 2^-t * sum_y m_y^2 (sheet unread).
f(u) = min(u mod M, -u mod M). Full-menu ordering = itertools.product order (h = 0 first).
g(2j)=0, g(2j+1)=sum_{l<=j} h_l. Seed 20261113. Rows marked (*) are parameters the note does not report.

TOLERANCES. Physical-side numbers are exact Fractions. Character-side numbers are double sums of at most
~1e4 terms of size <= 1, so rounding is <= ~1e-12; TOL = 1e-10 is used and the measured max deviation and
the smallest separation it must resolve are both written to the result file.

PREDICATES (fixed before first run; each records qualifying instances, passes, failures):
P1  eq (1): for every list with sum zero and K >= 3 (hypothesis tested per list), every even centre and both
    incoming directions: (a) port (x-c,-c) receives exactly two histories of opposite sign whose sheets differ
    by +-h_j; (b) port (x+c,c) two histories of equal sign, same difference; (c) the other four histories
    reach four distinct ports different from those two; (d) for every k, |sum_y m_y zeta^(k.y)|^2/8 equals
    (1-cos(2 pi k.h/M))/4 at the dark port and (1+cos)/4 at the bright port.
P1b boundary (expected to qualify the wording): the same on K = 2 (list h,-h) and K = 1 (list 0).
P2  transcript representation: for every 3-block transcript (centres from the first 4, 6 port outcomes each,
    rightward tick-by-tick routing between blocks) the physical mass equals (1/|Y|) sum_k prod of the
    per-block factors (dark (1-cos)/4, bright (1+cos)/4, single 1/8) times 2^-routing.
P3  selection, exhaustive over all k in Y: (a) number of levels = (H+1)/2; (b) accept iff k surjective;
    (c) first setting in lowest positive level has k.h* = +-1; (d) f(k.(t h*)) = f(t) all t;
    (e) number accepted = M^d prod_p (1-p^-d); (f) quoted yields 4/5, 24/25, 124/125, 8/9, 64/75.
P4  2/3 bound: prod_{j=3..M}(1-j^-2) = 2(M+1)/(3M) exactly, and P_{M,2} >= that > 2/3, all odd M in [3,20001].
P5  signed decoding: u -> (f(u), f(u+1)) and u -> (f(u), f(u-1)) injective on Z/M for all M in [3,80];
    M = 2 kept as a non-qualifying control.
P6  reduced menu: (a) v = e_{i(p)} mod p^a; (b) K = M d^omega and settings sum to zero; (c) k surjective iff
    some line has (M+1)/2 levels; (d) first rank-one multiple on first complete line has k.h = +-1;
    (e) surjective tuples with no unit coordinate are counted and all recovered.
P7  accuracy: (a) min adjacent gap of (1) equals sin^2(pi/M)/2 and >= 2/M^2, odd M in [3,301];
    (b) with all errors < 1/(3M^2) gap-splitting at 1/M^2 recovers true clusters (2000 random draws/M);
    (c) j(2K-j) satisfies T(j)=1+(T(j-1)+T(j+1))/2, T(0)=T(2K)=0 and max = K^2, K in [1,60].
P8  finite M=5 test (16+16 blocks, fewer-dark wins, ties rejected) from physical autocorrelation kernels:
    masses sum to 1 over 289 pairs; acceptance 0.7738719426; wrong fraction 0.0251790845; next dark
    0.1797835195 (each to 10 decimals); next-dark probability is rational.
P9  eq (4) for 200 random rational polynomials per M; error bound 4(e+lam/2)(sum|a|)^2 under perturbation.
P10 persistence on 5x5: marginal 1/4; same-setting joint 3/32 vs 1/16; triad pair covariances 0;
    triple 3/256 vs 1/64; physical coordinates and character average agree.
P11 comparison M | N: joint settings (h_M, s (N/M) h_N) dark probabilities are {0, q}, q=(1-cos(4pi/M))/4>0,
    null at s = -eps_M*eps_N.
P12 embedding (Director G point 2): the joint law of [calibration transcript, controller's h*, flight record]
    computed in physical coordinates (rational, no root of unity) equals the character-side law under EVERY
    unit a (zeta -> zeta^a, uniform prior on k), on every record. Control: holding one named k fixed while
    changing a changes the law (count of differing records, max difference).
P13 named five-sheet oracle and tags: h=1 dark at named k=+-1 is (5-sqrt5)/16, at k=+-2 (5+sqrt5)/16, swapped
    under a=2; tagged vector ports (3+-sqrt5)/8; three-mode (3+-2sqrt2)/8, (3-+2sqrt2)/8, 1/4;
    three-site clock port 1/2 + s sqrt2/8, recorded arms 1/2, unique returning path.
"""
import json, math, random, sys, time
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from itertools import product
from math import gcd, cos, pi, sqrt
from pathlib import Path
import numpy as np

SEED = 20261113
TOL = 1e-10
OUT = Path(__file__).with_name("xcheck_phase_result.json")
if OUT.exists():
    sys.exit("refusing to overwrite " + str(OUT))
rng = random.Random(SEED)
RES = {}
T0 = time.time()

def rec(name, qualifying, passed, failures, **extra):
    RES[name] = dict(qualifying=qualifying, passed=passed, failed=len(failures), failures=failures[:12], **extra)

def fold(u, M):
    u %= M
    return min(u, M - u)

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def add(a, b, M):
    return tuple((x + y) % M for x, y in zip(a, b))

def sub(a, b, M):
    return tuple((x - y) % M for x, y in zip(a, b))

def graph(hs, M):
    d = len(hs[0]); z = (0,) * d; g = []; tot = z
    for h in hs:
        tot = add(tot, h, M); g += [z, tot]
    return g, tot == z

def tick(state, g, M):
    """state: dict (x,c,y)->int signed count."""
    L = len(g); new = defaultdict(int)
    for (x, c, y), m in state.items():
        y2 = add(y, g[x], M)
        for dd in (1, -1):
            new[((x + dd) % L, dd, y2)] += m * (-1 if c == dd == -1 else 1)
    return {k: v for k, v in new.items() if v}

def histories(g, M, x, c):
    L = len(g); d = len(g[0]); out = []
    for w in product((1, -1), repeat=3):
        p, cc, y, s = x, c, (0,) * d, 1
        for dd in w:
            y = add(y, g[p], M)
            if cc == dd == -1: s = -s
            p, cc = (p + dd) % L, dd
        out.append(((p, cc), y, s))
    return out

def primes_of(n):
    ps = []; p = 2
    while p * p <= n:
        if n % p == 0:
            ps.append(p)
            while n % p == 0: n //= p
        p += 1
    if n > 1: ps.append(n)
    return ps

def P_yield(M, d):
    r = Fr(1)
    for p in primes_of(M): r *= 1 - Fr(1, p ** d)
    return r

# ---------------- P1 / P1b
def p1(lists, tag):
    q = 0; ok = 0; fails = []; nonq = 0; maxdev = 0.0
    for M, hs in lists:
        g, zero = graph(hs, M); K = len(hs); d = len(hs[0])
        if not zero or (tag == "P1" and K < 3):
            nonq += 1; continue
        Y = list(product(range(M), repeat=d)) if M ** d <= 729 else [tuple(rng.randrange(M) for _ in range(d)) for _ in range(60)]
        for j, c in product(range(K), (1, -1)):
            x = 2 * j; h = hs[j]; q += 1; L = 2 * K
            H = histories(g, M, x, c); byport = defaultdict(list)
            for port, y, s in H: byport[port].append((y, s))
            dk = byport[((x - c) % L, -c)]; br = byport[((x + c) % L, c)]
            bad = []
            if not (len(dk) == 2 and dk[0][1] == -dk[1][1] and sub(dk[0][0], dk[1][0], M) in (h, sub((0,) * d, h, M))): bad.append("a")
            if not (len(br) == 2 and br[0][1] == br[1][1] and sub(br[0][0], br[1][0], M) in (h, sub((0,) * d, h, M))): bad.append("b")
            others = [p for p in byport if p not in (((x - c) % L, -c), ((x + c) % L, c))]
            if not (len(others) == 4 and all(len(byport[p]) == 1 for p in others) and len(dk) + len(br) == 4): bad.append("c")
            for k in Y:
                ph = 2 * pi * dot(k, h) / M
                for lst, want in ((dk, (1 - cos(ph)) / 4), (br, (1 + cos(ph)) / 4)):
                    amp = sum(s * complex(cos(2 * pi * dot(k, y) / M), math.sin(2 * pi * dot(k, y) / M)) for y, s in lst)
                    dv = abs(abs(amp) ** 2 / 8 - want); maxdev = max(maxdev, dv)
                    if dv > TOL and "d" not in bad: bad.append("d")
            if bad: fails.append(dict(M=M, K=K, centre=x, incoming=c, h=h, failed=bad,
                                      port_sizes={str(p): len(v) for p, v in byport.items()}))
            else: ok += 1
    rec(tag, q, ok, fails, lists_not_qualifying=nonq, max_abs_dev=maxdev)

full = lambda M, d: list(product(range(M), repeat=d))
lists = [(M, full(M, d)) for M, d in ((3, 1), (5, 1), (3, 2), (5, 2), (9, 2), (7, 1), (7, 2), (15, 2), (21, 1))]
for _ in range(40):  # random zero-sum lists incl. repeats; and deliberately non-zero-sum ones (must not qualify)
    M = rng.choice((3, 5, 7, 9, 15)); d = rng.choice((1, 2)); K = rng.randrange(3, 9)
    hs = [tuple(rng.randrange(M) for _ in range(d)) for _ in range(K - 1)]
    last = tuple((-sum(h[i] for h in hs)) % M for i in range(d))
    if rng.random() < 0.25: last = add(last, (1,) + (0,) * (d - 1), M)
    lists.append((M, hs + [last]))
p1(lists, "P1")
p1([(5, [(1,), (4,)]), (3, [(1,), (2,)]), (7, [(2,), (5,)]), (5, [(0,)]), (5, [(1, 2), (4, 3)])], "P1b_boundary_K_le_2")

# ---------------- P2
def p2():
    q = ok = 0; fails = []; maxdev = 0.0; minp = 1.0
    for M, d in ((3, 1), (5, 1), (3, 2), (7, 1)):
        hs = full(M, d); g, _ = graph(hs, M); L = len(g); Y = full(M, d); nc = min(len(hs), 4)
        ph = {(k, h): 2 * pi * dot(k, h) / M for k in Y for h in hs}
        def run(state, seq, phys, fac, c_in):
            nonlocal q, ok, maxdev, minp
            if not seq:
                q += 1
                char = sum(np.prod([f[i] for f in fac]) if fac else 1.0 for i in range(len(Y))) / len(Y)
                dv = abs(float(phys) - char); maxdev = max(maxdev, dv)
                if phys > 0: minp = min(minp, float(phys))
                if dv > TOL: fails.append(dict(M=M, d=d, phys=str(phys), char=char))
                else: ok += 1
                return
            j = seq[0]; x = 2 * j
            # rightward routing to centre x: each tick is one fully read step, factor 1/2
            (px, pc), = {(a, b) for a, b, _ in state}
            rt = 0
            while px != x:
                state = {k: v for k, v in tick(state, g, M).items() if k[1] == 1}
                (px, pc), = {(a, b) for a, b, _ in state}; rt += 1
            s3 = state
            for _ in range(3): s3 = tick(s3, g, M)
            ports = defaultdict(dict)
            for (a, b, y), v in s3.items(): ports[(a, b)][(a, b, y)] = v
            dark = ((x - pc) % L, -pc); bright = ((x + pc) % L, pc)
            for port, st in ports.items():
                h = hs[j]
                if port == dark: f = [(1 - cos(ph[(k, h)])) / 4 for k in Y]
                elif port == bright: f = [(1 + cos(ph[(k, h)])) / 4 for k in Y]
                else: f = [0.125] * len(Y)
                norm0 = sum(v * v for v in state.values()); norm1 = sum(v * v for v in st.values())
                run(st, seq[1:], phys * Fr(norm1, norm0 * 8) / 2 ** rt, fac + [[x_ / 2 ** rt for x_ in f]], pc)
        for seq in product(range(nc), repeat=3):
            for c0 in (1, -1):
                run({(2 * seq[0], c0, (0,) * d): 1}, list(seq), Fr(1), [], c0)
    rec("P2", q, ok, fails, max_abs_dev=maxdev, smallest_positive_probability=minp)
p2()

# ---------------- P3
def p3():
    q = ok = 0; fails = []; rows = []
    quoted = {(5, 1): Fr(4, 5), (5, 2): Fr(24, 25), (5, 3): Fr(124, 125), (9, 2): Fr(8, 9), (15, 2): Fr(64, 75)}
    for M, d, star in ((3, 1, 0), (5, 1, 0), (5, 2, 0), (5, 3, 0), (9, 2, 0), (15, 2, 0), (7, 2, 1), (21, 2, 1), (25, 2, 1), (27, 1, 1), (35, 2, 1), (45, 1, 1), (9, 3, 1)):
        Y = np.array(full(M, d)); G = (Y @ Y.T) % M; F = np.minimum(G, M - G)
        acc = 0; bad = Counter()
        for i, k in enumerate(Y):
            q += 1; row = F[i]; lev = len(set(row.tolist())); H = M // math.gcd(M, *[int(a) for a in k])
            surj = H == M; b = []
            if lev != (H + 1) // 2: b.append("a")
            if (lev == (M + 1) // 2) != surj: b.append("b")
            if lev == (M + 1) // 2:
                acc += 1; pos = sorted(set(row.tolist()))[1]
                js = int(np.argmax(row == pos)); hstar = Y[js]; e = int(G[i, js])
                if e not in (1, M - 1): b.append("c")
                if any(fold(int(k @ ((t * hstar) % M)), M) != fold(t, M) for t in range(M)): b.append("d")
            if b:
                for z in b: bad[z] += 1
                if len(fails) < 12: fails.append(dict(M=M, d=d, k=k.tolist(), failed=b))
            else: ok += 1
        e_ok = Fr(acc, M ** d) == P_yield(M, d); f_ok = quoted.get((M, d), Fr(acc, M ** d)) == Fr(acc, M ** d)
        if not (e_ok and f_ok): fails.append(dict(M=M, d=d, count=acc, formula=str(P_yield(M, d))))
        rows.append(dict(M=M, d=d, unreported=bool(star), accepted=acc, yield_=str(Fr(acc, M ** d)), eq3_ok=e_ok, quoted_ok=f_ok))
    # strict monotonicity of (1) in f
    mono = all((1 - cos(2 * pi * (f + 1) / M)) > (1 - cos(2 * pi * f / M)) for M in range(3, 302, 2) for f in range((M - 1) // 2))
    rec("P3", q, ok, fails, rows=rows, eq1_strictly_increasing_in_f=mono)
p3()

# ---------------- P4
def p4():
    q = ok = 0; fails = []; tel = Fr(1); minP = (Fr(2), 0)
    for M in range(3, 20002):
        tel *= 1 - Fr(1, M * M)
        if M % 2 == 0: continue
        q += 1; P = P_yield(M, 2); t = Fr(2 * (M + 1), 3 * M)
        if tel == t and P >= t > Fr(2, 3): ok += 1
        else: fails.append(dict(M=M))
        if P < minP[0]: minP = (P, M)
    rec("P4", q, ok, fails, min_P_M2=float(minP[0]), at_M=minP[1])
p4()

# ---------------- P5
def p5():
    q = ok = 0; fails = []; ctrl = None
    for M in range(2, 81):
        inj = all(len({(fold(u, M), fold(u + s, M)) for u in range(M)}) == M for s in (1, -1))
        if M == 2: ctrl = inj; continue
        q += 1
        if inj: ok += 1
        else: fails.append(dict(M=M))
    rec("P5", q, ok, fails, control_M2_injective=ctrl)
p5()

# ---------------- P6
def ppowers(M):
    out = []
    for p in primes_of(M):
        qv = 1
        while M % (qv * p) == 0: qv *= p
        out.append((p, qv))
    return out

def p6():
    q = ok = 0; fails = []; rows = []
    for M, d, star in ((15, 2, 0), (45, 2, 0), (105, 2, 0), (9, 2, 0), (5, 3, 0), (21, 3, 1), (63, 2, 1), (165, 2, 1), (15, 3, 1), (75, 2, 1), (21, 1, 1)):
        pp = ppowers(M); idem = [(M // qv) * pow(M // qv, -1, qv) % M for _, qv in pp]
        vecs = []
        for ch in product(range(d), repeat=len(pp)):
            v = tuple(sum(e for j, e in zip(ch, idem) if j == i) % M for i in range(d))
            assert all(tuple(a % qv for a in v) == tuple(int(i == j) for i in range(d)) for j, (_, qv) in zip(ch, pp))
            vecs.append(v)
        menu = [tuple(t * a % M for a in v) for v in vecs for t in range(M)]
        structural = len(menu) == M * d ** len(pp) and all(sum(h[i] for h in menu) % M == 0 for i in range(d))
        V = np.array(vecs); nounit = nounit_rec = acc = 0
        for k in product(range(M), repeat=d):
            q += 1; surj = math.gcd(M, *k) == 1; ph = [int(x) for x in (V @ np.array(k)) % M]
            complete = [i for i, x in enumerate(ph) if len({fold(t * x, M) for t in range(M)}) == (M + 1) // 2]
            b = []
            if bool(complete) != surj: b.append("c")
            if complete:
                acc += 1; x = ph[complete[0]]; t = next(t for t in range(M) if fold(t * x, M) == 1)
                h = tuple(t * a % M for a in vecs[complete[0]])
                good = dot(k, h) % M in (1, M - 1)
                if not good: b.append("d")
                if all(math.gcd(a, M) > 1 for a in k):
                    nounit += 1; nounit_rec += good
            elif surj and all(math.gcd(a, M) > 1 for a in k): nounit += 1
            if b: fails.append(dict(M=M, d=d, k=k, failed=b))
            else: ok += 1
        if not structural or Fr(acc, M ** d) != P_yield(M, d) or nounit != nounit_rec:
            fails.append(dict(M=M, d=d, structural=structural, acc=acc))
        rows.append(dict(M=M, d=d, unreported=bool(star), lines=len(vecs), settings=len(menu), full_menu=M ** d,
                         accepted=acc, surjective_no_unit_coordinate=nounit, of_which_recovered=nounit_rec))
    rec("P6", q, ok, fails, rows=rows)
p6()

# ---------------- P7
def p7():
    q = ok = 0; fails = []; minratio = 9e9
    for M in range(3, 302, 2):
        q += 1; rates = [(1 - cos(2 * pi * f / M)) / 4 for f in range((M + 1) // 2)]
        gap = min(b - a for a, b in zip(rates, rates[1:])); want = math.sin(pi / M) ** 2 / 2
        good = abs(gap - want) <= 1e-9 * want and gap >= 2 / M ** 2
        minratio = min(minratio, gap * M * M / 2)
        if M <= 41:
            for _ in range(2000 // M + 1):
                obs = [(r + rng.uniform(-1, 1) * 0.999 / (3 * M * M), f) for f, r in enumerate(rates) for _ in range(rng.randrange(1, 4))]
                obs.sort(); groups = [[obs[0][1]]]
                for (a, _), (b, fb) in zip(obs, obs[1:]):
                    if b - a > 1 / M ** 2: groups.append([])
                    groups[-1].append(fb)
                if [sorted(set(gp)) for gp in groups] != [[f] for f in range(len(rates))]: good = False
        if good: ok += 1
        else: fails.append(dict(M=M, gap=gap, want=want))
    hq = hok = 0
    for K in range(1, 61):
        L = 2 * K; T = lambda j: j * (L - j); hq += 1
        if all(2 * T(j) == 2 + T(j - 1) + T(j + 1) for j in range(1, L)) and T(0) == T(L) == 0 and max(T(j) for j in range(L + 1)) == K * K: hok += 1
    rec("P7", q, ok, fails, min_gap_over_2_per_M2=minratio, hitting_time_cases=hq, hitting_time_pass=hok)
p7()

# ---------------- P8 (exact; physical autocorrelation kernels on Z/5)
def conv(a, b, M=5):
    r = [0] * M
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[(i + j) % M] += x * y
    return r
def kern(h, M=5):
    dk = [0] * M; dk[0] += 2; dk[h % M] -= 1; dk[-h % M] -= 1
    nd = [-v for v in dk]; nd[0] += 8
    return dk, nd
def p8():
    n = 16; K = {h: kern(h) for h in (1, 2)}
    pw = {}
    for h in (1, 2):
        for t in (0, 1):
            cur = [1, 0, 0, 0, 0]; pw[h, t] = [cur]
            for _ in range(n + 1): cur = conv(cur, K[h][t]); pw[h, t].append(cur)
    def mass(a, b):  # autocorrelation vector of all sequences with a darks at h=1, b at h=2
        v = conv(conv(pw[1, 0][a], pw[1, 1][n - a]), conv(pw[2, 0][b], pw[2, 1][n - b]))
        return [math.comb(n, a) * math.comb(n, b) * x for x in v]
    den = 8 ** (2 * n); tot = acc = Fr(0); nextd = Fr(0); wrong = 0.0; pairs = 0
    s5 = sqrt(5); p = {(1, 1): (5 - s5) / 16, (1, 2): (5 + s5) / 16, (2, 1): (5 + s5) / 16, (2, 2): (5 - s5) / 16}  # p[h, |k|]
    for a, b in product(range(n + 1), repeat=2):
        v = mass(a, b); pr = Fr(v[0], den); tot += pr; pairs += 1
        if a == b: continue
        sel = 1 if a < b else 2; acc += pr
        nextd += Fr(conv(v, K[sel][0])[0], den * 8)
        # character side: pair |k| is wrong when the selected setting is its high-rate setting
        wk = 2 if sel == 1 else 1
        wrong += 0.4 * math.comb(n, a) * math.comb(n, b) * p[1, wk] ** a * (1 - p[1, wk]) ** (n - a) * p[2, wk] ** b * (1 - p[2, wk]) ** (n - b)
    vals = dict(acceptance=float(acc), wrong_fraction=wrong / float(acc), next_dark=float(nextd / acc))
    want = dict(acceptance=0.7738719426, wrong_fraction=0.0251790845, next_dark=0.1797835195)
    fails = [dict(name=k, got=vals[k], want=want[k]) for k in want if abs(vals[k] - want[k]) > 5.1e-11]
    if tot != 1 or pairs != 289: fails.append(dict(total=str(tot), pairs=pairs))
    rec("P8", 4, 4 - len(fails), fails, values=vals, next_dark_exact=str(nextd / acc)[:80], ideal_low_rate=(5 - s5) / 16,
        tolerance_basis="note quotes 10 decimals; 5.1e-11 is half a unit in the last place plus double rounding")
p8()

# ---------------- P9
def p9():
    q = ok = 0; fails = []; maxrel = 0.0; bq = bok = 0
    for M in (3, 5, 7, 9, 15, 21, 33):
        D = lambda t: (1 - cos(2 * pi * t / M)) / 4
        for _ in range(200):
            deg = rng.randrange(1, 2 * M); a = [Fr(rng.randrange(-9, 10), rng.randrange(1, 8)) for _ in range(deg)]
            q += 1; lhs = sum(float(x) * float(y) * (1 - 4 * D(i - j)) for i, x in enumerate(a) for j, y in enumerate(a))
            A = sum(float(x) * complex(cos(2 * pi * i / M), math.sin(2 * pi * i / M)) for i, x in enumerate(a)); rhs = abs(A) ** 2
            scale = sum(abs(float(x)) for x in a) ** 2 + 1e-300; dv = abs(lhs - rhs) / scale; maxrel = max(maxrel, dv)
            if dv <= TOL: ok += 1
            else: fails.append(dict(M=M, lhs=lhs, rhs=rhs))
            e = rng.uniform(0, .05); lam = rng.uniform(0, .2); bq += 1
            pert = {t: min(.5, max(0, (1 - lam) * D(t) + lam * rng.uniform(0, .5))) + rng.uniform(-e, e) for t in range(-deg, deg + 1)}
            est = sum(float(x) * float(y) * (1 - 4 * pert[i - j]) for i, x in enumerate(a) for j, y in enumerate(a))
            if abs(est - rhs) <= 4 * (e + lam / 2) * scale + 1e-9: bok += 1
            else: fails.append(dict(M=M, bound_violation=abs(est - rhs), bound=4 * (e + lam / 2) * scale))
    rec("P9", q, ok, fails, max_scaled_dev=maxrel, bound_cases=bq, bound_pass=bok)
p9()

# ---------------- P10
def dark_mass(M, hs):
    d = len(hs[0]); sh = {(0,) * d: 1}
    for h in hs:
        o = defaultdict(int)
        for y, v in sh.items(): o[y] -= v; o[add(y, h, M)] += v
        sh = o
    return Fr(sum(v * v for v in sh.values()), 8 ** len(hs))
def char_mass(M, hs):
    d = len(hs[0]); Y = full(M, d)
    return sum(np.prod([(1 - cos(2 * pi * dot(k, h) / M)) / 4 for h in hs]) for k in Y) / len(Y)
def p10():
    M = 5; fails = []; q = 0; maxdev = 0.0
    nz = [h for h in full(5, 2) if any(h)]
    for h in nz:
        q += 2
        if dark_mass(M, [h]) != Fr(1, 4): fails.append(dict(marginal=h))
        if dark_mass(M, [h, h]) != Fr(3, 32): fails.append(dict(joint=h))
    for h, g2 in product(nz, repeat=2):
        q += 1; pm = dark_mass(M, [h, g2]); dv = abs(float(pm) - char_mass(M, [h, g2])); maxdev = max(maxdev, dv)
        want = Fr(3, 32) if g2 in (h, sub((0, 0), h, M)) else Fr(1, 16)
        if pm != want or dv > TOL: fails.append(dict(pair=(h, g2), got=str(pm)))
    tri = [(1, 0), (0, 1), (1, 1)]; q += 1; t = dark_mass(M, tri)
    if t != Fr(3, 256) or abs(float(t) - char_mass(M, tri)) > TOL: fails.append(dict(triple=str(t)))
    rec("P10", q, q - len(fails), fails, triple=str(t), fresh_triple=str(Fr(1, 4) ** 3), fresh_pair=str(Fr(1, 4) ** 2), max_abs_dev=maxdev,
        note="same-setting OR opposite-setting pairs give 3/32; all other nonzero pairs 1/16")
p10()

# ---------------- P11
def p11():
    q = ok = 0; fails = []; rows = []
    for M, N in ((3, 9), (5, 15), (9, 45), (15, 105), (7, 21), (3, 15), (5, 5), (9, 27)):
        qq = (1 - cos(4 * pi / M)) / 4
        for kM, kN in product([k for k in range(M) if gcd(k, M) == 1], [k for k in range(N) if gcd(k, N) == 1]):
            for eM, eN in product((1, -1), repeat=2):
                hM = eM * pow(kM, -1, M) % M; hN = eN * pow(kN, -1, N) % N; q += 1
                pr = {s: (1 - cos(2 * pi * (kM * hM / M + kN * s * (N // M) * hN / N))) / 4 for s in (1, -1)}
                null = -eM * eN
                if abs(pr[null]) < TOL and abs(pr[-null] - qq) < TOL and qq > 1e-3: ok += 1
                else: fails.append(dict(M=M, N=N, kM=kM, kN=kN, pr=pr))
        rows.append(dict(M=M, N=N, q=qq))
    rec("P11", q, ok, fails, rows=rows)
p11()

# ---------------- P12 embedding invariance of [calibration, h*, flight]
def p12():
    q = ok = 0; fails = []; maxdev = 0.0; minp = 1.0; rows = []; ctrl_diff = 0; ctrl_max = 0.0; ctrl_q = 0
    cases = [(5, 1, [(1,), (2,)] * 2), (7, 1, [(1,), (2,), (3,)]), (9, 1, [(1,), (2,), (3,), (4,)]), (15, 1, [(1,), (3,), (5,), (7,)]),
             (3, 2, [(1, 0), (0, 1), (1, 1), (1, 2)]), (5, 2, [(1, 0), (0, 1), (1, 1), (2, 1)])]
    for M, d, sched in cases:
        Y = full(M, d); z = (0,) * d; units = [a for a in range(1, M) if gcd(a, M) == 1]
        hs = sorted(set(sched));
        hs_full = hs + [sub(z, sum_h, M) for sum_h in [tuple(sum(h[i] for h in hs) % M for i in range(d))]]
        while len(hs_full) < 3: hs_full += [z]
        g, zero = graph(hs_full, M); assert zero
        L = len(g); nrec = 0; tot = Fr(0)
        E = {a: np.array([[np.exp(2j * pi * a * dot(k, y) / M) for y in Y] for k in Y]) for a in units}
        yi = {y: i for i, y in enumerate(Y)}
        Lf = 6; tf = 4
        def flight(sheet, hstar):
            """4-tick walk on a 6-ring with departure gain (x mod M)*h*, start (0,R), on the retained sheet; site+direction read."""
            st = {(0, 1, y): v for y, v in sheet.items()}
            gf = [tuple((x % M) * a % M for a in hstar) for x in range(Lf)]
            for _ in range(tf): st = tick(st, gf, M)
            out = defaultdict(dict)
            for (x, c, y), v in st.items(): out[(x, c)][y] = v
            return out, gf
        def flight_char(a, hstar, gf):
            """per-k signed path amplitude polynomial for each flight port (in characters, embedding a)."""
            amp = defaultdict(lambda: np.zeros(len(Y), complex))
            for w in product((1, -1), repeat=tf):
                x, c, y, s = 0, 1, z, 1
                for dd in w:
                    y = add(y, gf[x], M)
                    if c == dd == -1: s = -s
                    x, c = (x + dd) % Lf, dd
                amp[(x, c)] += s * E[a][:, yi[y]]
            return amp
        def walk(i, sheet, darks, phys_t, facs):
            nonlocal q, ok, maxdev, minp, nrec, tot, ctrl_diff, ctrl_max, ctrl_q
            if i == len(sched):
                cnt = Counter();
                for h, dk in zip(sched, darks): cnt[h] += dk
                hstar = min(hs, key=lambda h: (cnt[h], hs.index(h)))  # fewest darks, first in ordering
                out, gf = flight(sheet, hstar)
                fa = {a: flight_char(a, hstar, gf) for a in units}
                for port in sorted(out):
                    phys = Fr(sum(v * v for v in out[port].values()), 2 ** (phys_t + tf)); tot += phys; nrec += 1
                    for a in units:
                        q += 1
                        w = np.ones(len(Y))
                        for f in facs[a]: w = w * f
                        ch = float(np.sum(w * np.abs(fa[a][port]) ** 2) / len(Y) / 2 ** tf)
                        dv = abs(ch - float(phys)); maxdev = max(maxdev, dv)
                        if phys > 0: minp = min(minp, float(phys))
                        if dv > TOL: fails.append(dict(M=M, d=d, a=a, phys=str(phys), char=ch))
                        else: ok += 1
                    # control: one named sector k = e_1 held fixed while the embedding changes
                    ki = yi[(1,) + (0,) * (d - 1)]; ref = None
                    for a in units:
                        v = float(np.prod([f[ki] for f in facs[a]]) * abs(fa[a][port][ki]) ** 2 / 2 ** tf)
                        if ref is None: ref = v
                        else:
                            ctrl_q += 1; ctrl_max = max(ctrl_max, abs(v - ref)); ctrl_diff += abs(v - ref) > TOL
                return
            h = sched[i]; x = 2 * hs_full.index(h); H = histories(g, M, x, 1); byport = defaultdict(list)
            for port, y, s in H: byport[port].append((y, s))
            dark = ((x - 1) % L, -1); bright = ((x + 1) % L, 1)
            for port, lst in byport.items():
                ns = defaultdict(int)
                for y0, v in sheet.items():
                    for y, s in lst: ns[add(y0, y, M)] += v * s
                ns = {k: v for k, v in ns.items() if v}
                nf = {}
                for a in units:
                    ph = np.array([2 * pi * a * dot(k, h) / M for k in Y])
                    f = (1 - np.cos(ph)) / 4 if port == dark else (1 + np.cos(ph)) / 4 if port == bright else np.full(len(Y), .125)
                    nf[a] = facs[a] + [f]
                walk(i + 1, ns, darks + [port == dark], phys_t + 3, nf)
        walk(0, {z: 1}, [], 0, {a: [] for a in units})
        rows.append(dict(M=M, d=d, schedule=sched, units=units, records=nrec, total_physical_mass=str(tot)))
    rec("P12", q, ok, fails, rows=rows, max_abs_dev=maxdev, smallest_positive_record_probability=minp,
        control_named_k_fixed=dict(comparisons=ctrl_q, differing=ctrl_diff, max_abs_difference=ctrl_max),
        enumerated="every calibration transcript (6 port outcomes per block, incoming R, inter-block routing omitted: it is a common known translation), "
                   "controller h* = first setting with fewest darks, then a 4-tick flight on a 6-ring with gain (x mod M) h* from (0,R) on the retained sheet, all 12 (site,direction) flight records")
p12()

# ---------------- P13
def p13():
    fails = []; q = 0; s5 = sqrt(5); s2 = sqrt(2)
    g, _ = graph(full(5, 1), 5)
    for k in range(5):
        for a in (1, 2):
            q += 1; x = 2 * 1; H = [(y, s) for port, y, s in histories(g, 5, x, 1) if port == ((x - 1) % 10, -1)]
            pr = abs(sum(s * np.exp(2j * pi * a * k * y[0] / 5) for y, s in H)) ** 2 / 8
            eff = fold(a * k, 5); want = 0 if eff == 0 else (5 - s5) / 16 if eff == 1 else (5 + s5) / 16
            if abs(pr - want) > TOL: fails.append(dict(k=k, a=a, pr=pr))
    for a, want in ((1, (3 + s5) / 8), (2, (3 - s5) / 8)):
        q += 1; v = np.array([1, np.exp(2j * pi * a / 5)]) / s2; Hm = np.array([[1, 1], [1, -1]]) / s2
        pr = abs((Hm @ v)[0]) ** 2
        if abs(pr - want) > TOL: fails.append(dict(tag=a, pr=pr))
    for s in (1, -1):
        q += 1; r = s * s2; h = np.array([[1, 1], [1, -1]]) / r
        H01 = np.eye(3); H01[:2, :2] = h; H12 = np.eye(3); H12[1:, 1:] = h
        pr = np.abs(H01 @ H12 @ H01 @ np.array([1., 0, 0])) ** 2
        want = [(3 + 2 * s * s2) / 8, (3 - 2 * s * s2) / 8, .25]
        if np.max(np.abs(pr - want)) > TOL: fails.append(dict(three_mode=s, pr=pr.tolist()))
        # three-site, three-sheet clock: explicit 18-dim real unitary, control mixer, bypass arm
        idx = {c: i for i, c in enumerate(product(range(3), (1, -1), range(3)))}; U = np.zeros((18, 18))
        for (x, c, y), i in idx.items():
            for dd in (1, -1): U[idx[((x + dd) % 3, dd, (y + x) % 3)], i] += (-1 if c == dd == -1 else 1) / r
        q += 1
        psi = np.zeros(18); psi[idx[(1, 1, 0)]] = 1; U3 = np.linalg.matrix_power(U, 3)
        unitary = np.max(np.abs(U.T @ U - np.eye(18))) < 1e-12
        p0 = np.sum(((psi + U3 @ psi) / 2) ** 2); marked = np.sum((psi / 2) ** 2) + np.sum((U3 @ psi / 2) ** 2)
        ret = (U3 @ psi)[idx[(1, 1, 0)]] * r ** 3
        if not (unitary and abs(p0 - (.5 + s * s2 / 8)) < TOL and abs(marked - .5) < TOL and abs(ret - 1) < 1e-9): fails.append(dict(clock=s, p0=p0, marked=marked, ret=ret))
    rec("P13", q, q - len(fails), fails)
p13()

RES["_meta"] = dict(seed=SEED, tol=TOL, seconds=round(time.time() - T0, 1))
with open(OUT, "x") as fh: json.dump(RES, fh, indent=1, default=str)
for k, v in RES.items():
    if k != "_meta": print(k, "qualifying", v["qualifying"], "passed", v["passed"], "failed", v["failed"])
print(RES["_meta"])
