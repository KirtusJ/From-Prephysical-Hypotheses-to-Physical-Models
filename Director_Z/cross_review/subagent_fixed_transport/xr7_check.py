"""Independent exact test of 'A fixed transport rule for relative character measurements'.

Written by a cross-reviewer from the note's definitions; no code of Director G is imported.
Integers / Fractions only.  Usage: python3 -I xr7_check.py RESULT.json [G_results_dir]
The program refuses to overwrite RESULT.json.

MODEL AS I READ IT.  Cell (x, c, y, z): x in Z/N (N = 2p), coin c = +1 (R) / -1 (L),
sheets (y, z) in F_p^2.  One step from (x,c,Y): for d in {+1,-1} add signed count to
((x+d) mod N, d, Y + g(x)), sign -1 iff c == d == -1, else +1.  Unnormalised integer counts;
probability of a record = (sum of squared counts) / 2^t.
Carriers: static g(2j)=(0,j), g(2j+1)=(j,-j(j+1)/2); quadratic g(x)=(x,x^2); linear g(x)=(x,2x).

PREDICATES (fixed before the first run; a failed one stays, follow-ups are appended as F*):
P1  For p in {3,5,7,11,13}, the 3 carriers, every x, c: after 3 steps from (x,c,0,0) the cell
    (x-c,-c) holds exactly one +1 and one -1 whose sheet separation is +-h_x, h_x=g(x+1)-g(x-1)
    (or nothing if h_x=0); the cell (x+c,c) holds two equal-sign units separated by +-h_x (or one
    count of magnitude 2).  Exact in Z[zeta]: 8*P_destr(k) = 2 - zeta^m - zeta^-m, m = k.h_x, and
    8*P_constr(k) = 2 + zeta^m + zeta^-m, for all p^2 characters k.  Number of (carrier,p,x,c,k)
    rows is 48,276.
P2  static: h_{2j}=(1,-j), h_{2j+1}=(0,1); numbers of projective directions among {h_x} are
    1 (linear), p (quadratic), p+1 (static); sum of h_x over each parity class is 0 (all carriers).
P3  static, each p above, each u in F_p (39 words), two different orders of the even-site tests,
    literal propagation with a prescribed shortest route between centres and coordinate masks:
    final squared count is 2p; the sheet vector is +1 on one coset of u*y+z and -1 on the coset
    one unit away (up to a global sign), zero elsewhere; rank of the p x p sheet matrix is p-1
    for u != 0 (and 1 for u = 0); joint probability = 2p / (8^p 2^R), R = number of routed steps.
P3r Same for p in {3,5} with seeded random (non-shortest) recorded routes: same coset shape,
    squared count 2p.
P4  373 follow-up settings (p, u, j): route to 2j, 3 steps, keep destructive cell: conditional
    probability is 0 if u=j, 3/8 if u-j = +-1, else 1/4.
P5  quadratic carrier, literal propagation, tests at one site of each residue class x mod p
    except the class x_u (all p choices of omitted class, p in {3,5,7,11,13}):
    integer total squared count = (p-1) + C(2p-2,p-1)/p; character support is exactly
    {r = -2 x_u s, s != 0} union {(r,0), r != 0}; squared count on the desired line is p-1;
    desired fractions at p = 5, 7, 13 are 2/9, 1/23, 3/52006.
P6  static p=5 from (0,R,0,0): enumerate the 4 / 32 signed histories; flag = (site 2, R) at
    step 2.  |count| histograms {1:1} (yes), {1:3} (no) at step 2; {1:8} (yes), {1:20, 2:1} (no)
    at step 5.  Hence 1/3 = 8 phi1/(20 phi1 + phi2) iff phi2 = 4 phi1.
P7  corridor, literal brute force over ALL 2^t direction histories (and 2^(t+1)) with the mask
    applied to physical positions, (N,n) in {(6,1),(6,2),(10,1)}, carriers static + seeded random
    table: accepted histories at t=1+nN are exactly n+1 one-turn paths plus the straight path, all
    of sign +; counts: (t-2,R) -> n, (t-2,L) -> 1 on one common sheet, (t,R) -> 1; after one free
    step with the trailing flag kept: trailing magnitudes {n+1, n-1} (0 dropped), leading {1,1}.
    Global (all transcripts, both flags) squared-response joint probabilities of (C,F), (C,notF)
    are equal at t and t+1.  For N=6,n=2 odds trailing:leading go 3->2 (|n|), 5->5 (n^2),
    9->14 (|n|^3), 17->41 (n^4).
P8  corridor, sparse propagation with the literal time-indexed mask, p in {3,5,7,11,13},
    carriers static/linear/quadratic/2 seeded random tables, n = 1..100: same counts as P7 and
    surviving squared count n^2+2 (prior probability (n^2+2)/2^(1+nN)).
P9  f(0)=0, f(1)=1, f(n+1)+f(n-1)=2f(n)+2 gives f(n)=n^2 for n<=500; with seeded rational
    residuals e_j, f(n)-n^2 = sum_{j=1}^{n-1}(n-j)e_j for n<=60.
P10 mean hitting time on a ring N in {6,10,14,22,26} solved exactly (Fractions) from the
    first-step equations equals j(N-j); max_j <= p^2.
P11 zero-gain 3-step control from (0,R): counts at (-1,L) by pointer value: blank -> total 0;
    first direction retained -> (-1,+1) up to order; reversibly uncomputed -> 0.
P12 linear carrier: after 2p+3 steps every occupied cell has z-2y = 0.
P13 static p=3, clock of 4 ticks, two binary slots, all 1728 basis states: the map
    'step; at new tick 1 XOR [d=-1] into slot 1; at new tick 2, if slot1, XOR [x odd] into slot 2'
    has Gram matrix exactly 2I.
P14 static p=5: sum of squared counts over all 500 cells equals 2^t for t=1..24.
"""
import csv
import json
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from math import comb

PRIMES = (3, 5, 7, 11, 13)


def g_static(x, p):
    x %= 2 * p
    j = x // 2
    if x % 2 == 0:
        return (0, j % p)
    inv2 = (p + 1) // 2
    return (j % p, (-j * (j + 1) * inv2) % p)


def g_quadratic(x, p):
    return (x % p, (x * x) % p)


def g_linear(x, p):
    return (x % p, (2 * x) % p)


def table_carrier(table):
    def g(x, p):
        return table[x % (2 * p)]
    return g


CARRIERS = {"static": g_static, "quadratic": g_quadratic, "linear": g_linear}


def step(state, p, g):
    N = 2 * p
    out = defaultdict(int)
    for (x, c, y, z), a in state.items():
        ga, gb = g(x, p)
        Y = ((y + ga) % p, (z + gb) % p)
        for d in (1, -1):
            out[((x + d) % N, d) + Y] += (-a if (c == -1 and d == -1) else a)
    return {k: v for k, v in out.items() if v}


def steps(state, n, p, g):
    for _ in range(n):
        state = step(state, p, g)
    return state


def mask(state, x, c):
    return {k: v for k, v in state.items() if k[0] == x and k[1] == c}


def sq(state):
    return sum(v * v for v in state.values())


def h_of(x, p, g):
    a = g(x + 1, p)
    b = g(x - 1, p)
    return ((a[0] - b[0]) % p, (a[1] - b[1]) % p)


def char_power(state, p, r, s):
    """|sum amp zeta^(r y + s z)|^2 as vector of coefficients of zeta^m, reduced by subtracting
    the minimum (1 + zeta + ... = 0), so equality of vectors is equality in Z[zeta]."""
    bins = [0] * p
    for (_, _, y, z), a in state.items():
        bins[(r * y + s * z) % p] += a
    auto = [sum(bins[i] * bins[(i - m) % p] for i in range(p)) for m in range(p)]
    lo = min(auto)
    return tuple(v - lo for v in auto), len(set(bins)) == 1


def reduce_vec(vec):
    lo = min(vec)
    return tuple(v - lo for v in vec)


def rank(matrix):
    m = [[Fraction(v) for v in row] for row in matrix]
    r = 0
    for col in range(len(m[0])):
        piv = next((i for i in range(r, len(m)) if m[i][col]), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][col]:
                f = m[i][col] / m[r][col]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


# ---------------------------------------------------------------- P1, P2
def p1_p2(gdir):
    ok1 = True
    rows = 0
    fails = []
    dark = {}
    for p in PRIMES:
        for name, g in CARRIERS.items():
            for x in range(2 * p):
                h = h_of(x, p, g)
                for c in (1, -1):
                    st = steps({(x, c, 0, 0): 1}, 3, p, g)
                    de = mask(st, (x - c) % (2 * p), -c)
                    co = mask(st, (x + c) % (2 * p), c)
                    # structure
                    if h == (0, 0):
                        s_ok = (not de) and len(co) == 1 and abs(list(co.values())[0]) == 2
                    else:
                        dv = sorted(de.items(), key=lambda kv: kv[1])
                        s_ok = (len(dv) == 2 and dv[0][1] == -1 and dv[1][1] == 1)
                        if s_ok:
                            diff = ((dv[1][0][2] - dv[0][0][2]) % p, (dv[1][0][3] - dv[0][0][3]) % p)
                            s_ok = diff in (h, ((-h[0]) % p, (-h[1]) % p))
                        cv = list(co.items())
                        s_ok = s_ok and len(cv) == 2 and cv[0][1] == cv[1][1] and abs(cv[0][1]) == 1
                        if s_ok:
                            diff = ((cv[1][0][2] - cv[0][0][2]) % p, (cv[1][0][3] - cv[0][0][3]) % p)
                            s_ok = diff in (h, ((-h[0]) % p, (-h[1]) % p))
                    if not s_ok:
                        ok1 = False
                        fails.append((p, name, x, c, "structure"))
                    for r, s in product(range(p), repeat=2):
                        rows += 1
                        m = (r * h[0] + s * h[1]) % p
                        want_d = [0] * p
                        want_c = [0] * p
                        want_d[0] += 2; want_d[m] -= 1; want_d[(-m) % p] -= 1
                        want_c[0] += 2; want_c[m] += 1; want_c[(-m) % p] += 1
                        got_d, is_dark = char_power(de, p, r, s)
                        got_c, _ = char_power(co, p, r, s)
                        if got_d != reduce_vec(want_d) or got_c != reduce_vec(want_c) or is_dark != (m == 0):
                            ok1 = False
                            fails.append((p, name, x, c, r, s))
                        dark[(p, name, x, c, r, s)] = int(is_dark)
    ok1 = ok1 and rows == 48276
    # P2
    ok2 = True
    dirs = {}
    for p in PRIMES:
        for j in range(p):
            ok2 &= h_of(2 * j, p, g_static) == (1, (-j) % p)
            ok2 &= h_of(2 * j + 1, p, g_static) == (0, 1)
        for name, g in CARRIERS.items():
            seen = set()
            for x in range(2 * p):
                h = h_of(x, p, g)
                if h != (0, 0):
                    seen.add(min(((t * h[0]) % p, (t * h[1]) % p) for t in range(1, p)))
            dirs[(p, name)] = len(seen)
            want = {"linear": 1, "quadratic": p, "static": p + 1}[name]
            ok2 &= len(seen) == want
            for par in (0, 1):
                tot = [sum(h_of(x, p, g)[i] for x in range(par, 2 * p, 2)) % p for i in (0, 1)]
                ok2 &= tot == [0, 0]
    # comparison with G's CSV (not a predicate of the note; reported separately)
    cmp = None
    if gdir:
        n = bad = 0
        with open(gdir + "/fixed_transport.csv", newline="") as fh:
            for row in csv.DictReader(fh):
                n += 1
                key = (int(row["p"]), row["carrier"], int(row["centre"]), int(row["incoming"]),
                       int(row["r"]), int(row["s"]))
                if dark.get(key) != int(row["dark"]) or row["dark"] != row["predicted_dark"]:
                    bad += 1
        cmp = dict(csv_rows=n, mismatches_with_my_dark_classification=bad)
    return ok1, dict(rows=rows, fails=fails[:10]), ok2, {f"{k[0]}:{k[1]}": v for k, v in dirs.items()}, cmp


# ---------------------------------------------------------------- P3, P4
def route_to(state, target, p, g, rng=None):
    """Record every single step.  Shortest prescribed route, or a seeded random recorded walk."""
    N = 2 * p
    (x, c) = next(iter(state))[:2]
    n = 0
    while x != target % N:
        if rng is None:
            dist = (target - x) % N
            d = 1 if dist <= p else -1
        else:
            d = rng.choice((1, -1))
        x = (x + d) % N
        state = mask(step(state, p, g), x, d)
        assert len({k[:2] for k in state}) == 1 and state
        n += 1
    return state, n


def test_at(state, centre, p, g, rng=None):
    state, n = route_to(state, centre, p, g, rng)
    (x, c) = next(iter(state))[:2]
    out = mask(steps(state, 3, p, g), (x - c) % (2 * p), -c)
    return state, out, n


def coset_shape(state, p, u):
    cells = {k[:2] for k in state}
    if len(cells) != 1:
        return False, None
    M = [[0] * p for _ in range(p)]
    for (_, _, y, z), a in state.items():
        M[y][z] = a
    prof = {}
    for y in range(p):
        for z in range(p):
            w = (u * y + z) % p
            prof.setdefault(w, set()).add(M[y][z])
    if any(len(v) != 1 for v in prof.values()):
        return False, M
    vals = {w: next(iter(v)) for w, v in prof.items()}
    plus = [w for w, v in vals.items() if v == 1]
    minus = [w for w, v in vals.items() if v == -1]
    zero = [w for w, v in vals.items() if v == 0]
    ok = len(plus) == 1 and len(minus) == 1 and len(zero) == p - 2 and (plus[0] - minus[0]) % p in (1, p - 1)
    return ok, M


def prepare(p, u, order, rng=None):
    g = g_static
    state = {(0, 1, 0, 0): 1}
    R = 0
    T = 0
    centres = [1] + [2 * j for j in order if j != u]
    for centre in centres:
        _, state, n = test_at(state, centre, p, g, rng)
        R += n
        T += n + 3
        if not state:
            return None, R, T
    return state, R, T


def p3_p4():
    ok3 = ok3r = ok4 = True
    words = 0
    followups = 0
    detail = []
    for p in PRIMES:
        for u in range(p):
            words += 1
            for order in (list(range(p)), list(range(p - 1, -1, -1))):
                st, R, T = prepare(p, u, order)
                good = st is not None and sq(st) == 2 * p
                if good:
                    shape, M = coset_shape(st, p, u)
                    rk = rank(M)
                    good = shape and rk == (p - 1 if u else 1)
                    good = good and Fraction(sq(st), 2 ** T) == Fraction(2 * p, 8 ** p * 2 ** R) and T == 3 * p + R
                if not good:
                    ok3 = False
                    detail.append(("P3", p, u, order[0]))
            st, R, T = prepare(p, u, list(range(p)))
            for j in range(p):
                followups += 1
                before, after, _ = test_at(st, 2 * j, p, g_static)
                prob = Fraction(sq(after), 8 * sq(before))
                d = (u - j) % p
                want = Fraction(0) if d == 0 else Fraction(3, 8) if d in (1, p - 1) else Fraction(1, 4)
                if prob != want:
                    ok4 = False
                    detail.append(("P4", p, u, j, str(prob)))
    rng = random.Random(20261113)
    for p in (3, 5):
        for u in range(p):
            for _ in range(4):
                st, R, T = prepare(p, u, list(range(p)), rng)
                good = st is not None and sq(st) == 2 * p and coset_shape(st, p, u)[0]
                if not good:
                    ok3r = False
                    detail.append(("P3r", p, u, R))
    return ok3 and words == 39, ok3r, ok4 and followups == 373, dict(words=words, followups=followups, fails=detail[:10])


# ---------------------------------------------------------------- P5
def p5():
    ok = True
    out = []
    g = g_quadratic
    for p in PRIMES:
        for xu in range(p):
            state = {(0, 1, 0, 0): 1}
            for cls in range(p):
                if cls == xu:
                    continue
                # a site with x = cls (mod p): choose the one in 0..p-1
                _, state, _ = test_at(state, cls, p, g)
            total = sq(state)
            want_total = Fraction(p - 1) + Fraction(comb(2 * p - 2, p - 1), p)
            support = set()
            for r, s in product(range(p), repeat=2):
                _, dark = char_power(state, p, r, s)
                if not dark:
                    support.add((r, s))
            line = {((-2 * xu * s) % p, s) for s in range(1, p)}
            want_support = line | {(r, 0) for r in range(1, p)}
            # squared count on the line: bins of the coordinate w = r0*y + z with r0 = -2 xu
            r0 = (-2 * xu) % p
            bins = [0] * p
            for (_, _, y, z), a in state.items():
                bins[(r0 * y + z) % p] += a
            line_mass = Fraction(p * sum(b * b for b in bins) - sum(bins) ** 2, p * p)
            good = (total == want_total and support == want_support and line_mass == p - 1)
            frac = line_mass / total
            if p in (5, 7, 13):
                good = good and frac == {5: Fraction(2, 9), 7: Fraction(1, 23), 13: Fraction(3, 52006)}[p]
            ok &= good
            if xu == 0:
                out.append(dict(p=p, total=total, line_mass=str(line_mass), fraction=str(frac)))
    return ok, out


# ---------------------------------------------------------------- P6
def p6():
    p = 5
    N = 10
    hist = {}
    for T in (2, 5):
        acc = defaultdict(int)
        for word in product((1, -1), repeat=T):
            x, c, y, z, sign, flag = 0, 1, 0, 0, 1, None
            for i, d in enumerate(word):
                ga, gb = g_static(x, p)
                y, z = (y + ga) % p, (z + gb) % p
                if c == -1 and d == -1:
                    sign = -sign
                x, c = (x + d) % N, d
                if i == 1:
                    flag = (x == 2 and c == 1)
            acc[(flag, x, c, y, z)] += sign
        for fl in (True, False):
            hist[(T, fl)] = dict(Counter(abs(v) for k, v in acc.items() if k[0] == fl and v))
    ok = (hist[(2, True)] == {1: 1} and hist[(2, False)] == {1: 3} and
          hist[(5, True)] == {1: 8} and hist[(5, False)] == {1: 20, 2: 1})
    # odds equation: 1/3 == 8a/(20a+b)  <=>  b == 4a  (checked symbolically on a grid)
    for a in range(1, 6):
        for b in range(0, 40):
            ok &= (Fraction(1, 3) == Fraction(8 * a, 20 * a + b)) == (b == 4 * a)
    return ok, {f"t{k[0]}_{'yes' if k[1] else 'no'}": v for k, v in hist.items()}


# ---------------------------------------------------------------- P7, P8
def admitted(j, x, c, N):
    if c == 1 and (x == j % N or x == (j - 2) % N):
        return True
    if c == -1 and x == (j - 2) % N and j % N == 1:
        return True
    return False


def brute_corridor(N, n, p, g):
    """All histories of length t and t+1; transcript = tuple of yes/no bits at steps 1..t,
    flag = trailing-site predicate at step t.  Coherent addition per (transcript, flag, endpoint)."""
    t = 1 + n * N
    res = {}
    for T in (t, t + 1):
        acc = defaultdict(int)
        accepted_paths = []
        for word in product((1, -1), repeat=T):
            x, c, y, z, sign = 0, 1, 0, 0, 1
            bits = []
            flag = None
            for i, d in enumerate(word, start=1):
                ga, gb = g(x, p)
                y, z = (y + ga) % p, (z + gb) % p
                if c == -1 and d == -1:
                    sign = -sign
                x, c = (x + d) % N, d
                if i <= t:
                    bits.append(admitted(i, x, c, N))
                if i == t:
                    flag = (x == (t - 2) % N)
            tr = tuple(bits)
            acc[(tr, flag, x, c, y, z)] += sign
            if all(bits) and T == t:
                accepted_paths.append((word, sign, x, c, y, z))
        res[T] = (acc, accepted_paths)
    return t, res


def p7():
    ok = True
    info = []
    rng = random.Random(7)
    for (N, n) in ((6, 1), (6, 2), (10, 1)):
        p = N // 2
        table = [(rng.randrange(p), rng.randrange(p)) for _ in range(N)]
        for name, g in (("static", g_static), ("random", table_carrier(table))):
            t, res = brute_corridor(N, n, p, g)
            acc, paths = res[t]
            allyes = tuple([True] * t)
            good = len(paths) == n + 2 and all(s == 1 for _, s, *_ in paths)
            lefts = sorted(tuple(i for i, d in enumerate(w, 1) if d == -1) for w, *_ in paths)
            good &= lefts == sorted([()] + [(1 + k * N,) for k in range(n + 1)])
            C = {k[1:]: v for k, v in acc.items() if k[0] == allyes and v}
            trail = {k[1:]: v for k, v in C.items() if k[0]}
            lead = {k[1:]: v for k, v in C.items() if not k[0]}
            sheets = {k[2:] for k in trail}
            good &= (sorted((k[0], k[1], v) for k, v in trail.items()) ==
                     sorted([((t - 2) % N, 1, n), ((t - 2) % N, -1, 1)]) and len(sheets) == 1)
            good &= [(k[0], k[1], v) for k, v in lead.items()] == [(t % N, 1, 1)]
            acc2, _ = res[t + 1]
            C2 = {k[1:]: v for k, v in acc2.items() if k[0] == allyes and v}
            tr2 = sorted(abs(v) for k, v in C2.items() if k[0])
            le2 = sorted(abs(v) for k, v in C2.items() if not k[0])
            good &= tr2 == sorted(v for v in (n - 1, n + 1) if v) and le2 == [1, 1]
            # global joint probabilities under the squared response
            def joint(a, f):
                tot = sum(f(abs(v)) for v in a.values())
                out = {}
                for cc in (True, False):
                    for ff in (True, False):
                        out[(cc, ff)] = Fraction(sum(f(abs(v)) for k, v in a.items()
                                                     if (k[0] == allyes) == cc and k[1] == ff), tot)
                return out
            j1 = joint(acc, lambda m: m * m)
            j2 = joint(acc2, lambda m: m * m)
            good &= j1 == j2 and j1[(True, True)] + j1[(True, False)] == Fraction(n * n + 2, 2 ** t)
            odds = {}
            for e in (1, 2, 3, 4):
                a1 = joint(acc, lambda m: m ** e)
                a2 = joint(acc2, lambda m: m ** e)
                odds[e] = (str(a1[(True, True)] / a1[(True, False)]), str(a2[(True, True)] / a2[(True, False)]))
            if (N, n) == (6, 2):
                good &= odds == {1: ("3", "2"), 2: ("5", "5"), 3: ("9", "14"), 4: ("17", "41")}
            ok &= good
            info.append(dict(N=N, n=n, carrier=name, ok=good, odds_before_after_by_exponent=odds))
    return ok, info


def p8():
    ok = True
    stops = 0
    rng = random.Random(8)
    for p in PRIMES:
        N = 2 * p
        carriers = dict(CARRIERS)
        for i in range(2):
            carriers[f"random{i}"] = table_carrier([(rng.randrange(p), rng.randrange(p)) for _ in range(N)])
        for name, g in carriers.items():
            state = {(0, 1, 0, 0): 1}
            for t in range(1, 2 + 100 * N):
                state = {k: v for k, v in step(state, p, g).items() if admitted(t, k[0], k[1], N)}
                if t % N != 1 or t == 1:
                    continue
                n = (t - 1) // N
                stops += 1
                tr = {k: v for k, v in state.items() if k[0] == (t - 2) % N}
                le = {k: v for k, v in state.items() if k[0] != (t - 2) % N}
                good = (sorted((k[1], v) for k, v in tr.items()) == [(-1, 1), (1, n)]
                        and len({k[2:] for k in tr}) == 1
                        and [(k[0], k[1], v) for k, v in le.items()] == [(t % N, 1, 1)]
                        and sq(state) == n * n + 2)
                a = sorted(abs(v) for v in step(tr, p, g).values())
                b = sorted(abs(v) for v in step(le, p, g).values())
                good = good and a == sorted(v for v in (n - 1, n + 1) if v) and b == [1, 1]
                ok &= good
    return ok and stops == 5 * 5 * 100, dict(stops=stops)


# ---------------------------------------------------------------- P9..P14
def p9():
    f = [0, 1]
    for n in range(1, 500):
        f.append(2 * f[n] + 2 - f[n - 1])
    ok = all(f[n] == n * n for n in range(501))
    rng = random.Random(9)
    e = [None] + [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in range(60)]
    h = [Fraction(0), Fraction(1)]
    for n in range(1, 60):
        h.append(2 * h[n] + 2 + e[n] - h[n - 1])
    ok &= all(h[n] - n * n == sum((n - j) * e[j] for j in range(1, n)) for n in range(61))
    return ok


def p10():
    ok = True
    for N in (6, 10, 14, 22, 26):
        # unknowns E_1..E_{N-1}; E_0 = E_N = 0;  E_j = 1 + (E_{j-1}+E_{j+1})/2  (tridiagonal solve)
        m = N - 1
        A = [[Fraction(0)] * (m + 1) for _ in range(m)]
        for i in range(m):
            A[i][i] = Fraction(1)
            if i > 0:
                A[i][i - 1] = Fraction(-1, 2)
            if i < m - 1:
                A[i][i + 1] = Fraction(-1, 2)
            A[i][m] = Fraction(1)
        for col in range(m):
            piv = next(i for i in range(col, m) if A[i][col])
            A[col], A[piv] = A[piv], A[col]
            A[col] = [v / A[col][col] for v in A[col]]
            for i in range(m):
                if i != col and A[i][col]:
                    fct = A[i][col]
                    A[i] = [a - fct * b for a, b in zip(A[i], A[col])]
        E = [A[i][m] for i in range(m)]
        ok &= all(E[j - 1] == j * (N - j) for j in range(1, N))
        ok &= max(E) <= (N // 2) ** 2
    return ok


def p11():
    res = {}
    for mode in ("blank", "retained", "uncomputed"):
        acc = defaultdict(int)
        for word in product((1, -1), repeat=3):
            x, c, sign, bit = 0, 1, 1, 0
            for i, d in enumerate(word):
                if c == -1 and d == -1:
                    sign = -sign
                prev_x = x
                x, c = x + d, d
                if mode != "blank" and i == 0:
                    bit ^= (d == -1)
                if mode == "uncomputed" and i == 1:
                    # after step 2 the first direction is a function of the departure site of step 2
                    bit ^= (prev_x == -1)
            acc[(x, c, int(bit))] += sign
        res[mode] = [acc.get((-1, -1, b), 0) for b in (0, 1)]
    ok = (res["blank"] == [0, 0] and sorted(res["retained"]) == [-1, 1] and res["uncomputed"] == [0, 0])
    return ok, res


def p12():
    ok = True
    for p in PRIMES:
        st = steps({(0, 1, 0, 0): 1}, 2 * p + 3, p, g_linear)
        ok &= all((k[3] - 2 * k[2]) % p == 0 for k in st)
    return ok


def p13():
    p, N, K = 3, 6, 4
    cols = {}
    for x, c, y, z, k, s1, s2 in product(range(N), (1, -1), range(p), range(p), range(K), (0, 1), (0, 1)):
        ga, gb = g_static(x, p)
        col = {}
        for d in (1, -1):
            nx, nk = (x + d) % N, (k + 1) % K
            a1, a2 = s1, s2
            if nk == 1:
                a1 ^= (d == -1)
            if nk == 2 and a1:
                a2 ^= (nx % 2)
            col[(nx, d, (y + ga) % p, (z + gb) % p, nk, int(a1), int(a2))] = -1 if (c == -1 and d == -1) else 1
        cols[(x, c, y, z, k, s1, s2)] = col
    ok = len(cols) == 1728 and all(len(v) == 2 for v in cols.values())
    by_dest = defaultdict(list)
    for key, col in cols.items():
        for dest in col:
            by_dest[dest].append(key)
    offdiag = 0
    for key, col in cols.items():
        partners = {q for dest in col for q in by_dest[dest] if q != key}
        for q in partners:
            if sum(v * cols[q].get(dest, 0) for dest, v in col.items()) != 0:
                offdiag += 1
    return ok and offdiag == 0, dict(columns=len(cols), nonzero_offdiagonal=offdiag)


def p14(gdir):
    st = {(0, 1, 0, 0): 1}
    ok = True
    mine = {}
    for t in range(1, 25):
        st = step(st, 5, g_static)
        ok &= sq(st) == 2 ** t
        for k, v in st.items():
            mine[(t,) + k] = v
    cmp = None
    if gdir:
        n = bad = 0
        with open(gdir + "/fixed_transport_free_counts.csv", newline="") as fh:
            for row in csv.DictReader(fh):
                n += 1
                key = (int(row["steps"]), int(row["site"]), int(row["direction"]), int(row["sheet_A"]), int(row["sheet_B"]))
                if mine.get(key, 0) != int(row["signed_count"]):
                    bad += 1
        cmp = dict(csv_rows=n, mismatches=bad)
    return ok, cmp


def main():
    out = sys.argv[1]
    gdir = sys.argv[2] if len(sys.argv) > 2 else None
    fh = open(out, "x")  # refuses to overwrite
    R = {"predicates": {}, "details": {}, "comparison_with_G_results": {}}
    ok1, d1, ok2, d2, cmp1 = p1_p2(gdir)
    R["predicates"]["P1"] = ok1; R["details"]["P1"] = d1
    R["predicates"]["P2"] = ok2; R["details"]["P2"] = d2
    R["comparison_with_G_results"]["fixed_transport.csv"] = cmp1
    ok3, ok3r, ok4, d34 = p3_p4()
    R["predicates"].update(P3=ok3, P3r=ok3r, P4=ok4); R["details"]["P3_P4"] = d34
    ok5, d5 = p5(); R["predicates"]["P5"] = ok5; R["details"]["P5"] = d5
    ok6, d6 = p6(); R["predicates"]["P6"] = ok6; R["details"]["P6"] = d6
    ok7, d7 = p7(); R["predicates"]["P7"] = ok7; R["details"]["P7"] = d7
    ok8, d8 = p8(); R["predicates"]["P8"] = ok8; R["details"]["P8"] = d8
    R["predicates"]["P9"] = p9()
    R["predicates"]["P10"] = p10()
    ok11, d11 = p11(); R["predicates"]["P11"] = ok11; R["details"]["P11"] = d11
    R["predicates"]["P12"] = p12()
    ok13, d13 = p13(); R["predicates"]["P13"] = ok13; R["details"]["P13"] = d13
    ok14, cmp14 = p14(gdir); R["predicates"]["P14"] = ok14
    R["comparison_with_G_results"]["fixed_transport_free_counts.csv"] = cmp14
    R["all_met"] = all(R["predicates"].values())
    json.dump(R, fh, indent=1)
    fh.write("\n")
    fh.close()
    print(json.dumps(R["predicates"]), R["comparison_with_G_results"])


if __name__ == "__main__":
    main()
