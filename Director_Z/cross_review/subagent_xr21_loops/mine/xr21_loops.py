"""Cross-review program xr21 for two notes (returning loops; force calibration).
Own code; nothing imported from the author's checkers. Fixed seed 20261113
(used only for the random weights in C1b). Result file is never overwritten.

PREDICATES, fixed before the first run. E = exact integer/Fraction; S = sign or
separation predicate on floats; MEASURED = number recorded, no pass/fail.

Note 1 (returning loops)
 A1 E  routed circuit H, I^(a-1), X, I^(a-1) from (x, rail R): exactly two outputs,
       both at site x, (L, area 2ax+a^2) and (R, area 2ax-a^2), equal positive amplitude.
       a=1..12, x=-20..20.
 A2 E  ring of circumference N, sheet order M. Hypothesis tested per instance: M | N.
       Qualifying: the two areas mod M equal the line values mod M for every start site.
       Non-qualifying (M does not divide N): recorded as control, count of (N,M,a) where
       the relative area mod M depends on the site.
 A3 E  all-Hadamard walk, every balanced word w starting R ending L, with complement:
       signed amplitudes equal; joint probability 2^(1-2a); relative area 2A(w) is the same
       at every start site. a=1..6, x in {-3,0,5}.
 A4 E  areas of R-start L-end balanced words of length 2a = {a^2-2j : 0<=j<=(a-1)^2}, a=1..8.
 A5 E  over all balanced 2a-words (any start/end rail): max relative area = 2a^2 and every
       relative area is even. a=1..7.
 A6 E  compensated schedule a=2b, gain signs -,+,+,-: x coefficient 0, signed sums +2b^2
       (right first) and -2b^2. b=1..12, x=-20..20.
 A7 E  exact quarter turn 2A = +-M/4 mod M from a word and its complement (areas from A4,
       a<=8) exists iff 8 | M, for M=2..96.
 A8 E  d nearest M/8 (both ties): |2d/M - 1/4| <= 1/M turns, M=8..4096.
 B1 S  flight model (PREMISE SWAP: Gaussian packet on rail R with carrier k*, width
       delta^(-5/4) sites, instead of the note's direction filter; compensated loop tuned to the
       fundamental; Hadamard flight): sign of mean position equals the sign of eq.(2)
       in runs i-v (ref/flight signs ++, +-, --, -+, and carrier +pi/2 with ++) at each M.
 B2 S  full conjugation (carrier, reference, flight) reproduces the position law of run i;
       max abs difference recorded; predicate: below 1e-9 (basis: <= ticks*2^-52*O(10) rounding
       for <= 2.1e4 ticks is ~5e-11).
 B-MEASURED: mean/ideal ratio and RMS about the ideal ray per M; fixed-sign loop mean;
       multiplier r=3 and r=2 on the device tuned to r=1; tagged (incoherent arms) mean;
       force/mass degeneracy: coin with cot(theta)=1/2 flown with 2F and with F.
       Orders: 2^13, 2^15 (the note's), 2^19, 2^21 (not reported in the note).
Note 2 (force calibration)
 C1 E  five-tick port (1,R) from (0, incoming R): 6 paths; ordered-pair lag coefficients are
       {0:4, 2:-4, 4:2, 6:-4, 8:2} for a character and 6 for counting; count gives 3/16, zero
       field gives 0.  C1b: with random rational weights at M=5,8,63,97 the folded formula
       32P=4+2c-4D1+2D2-4D3+2D4 agrees with direct evaluation; max abs difference recorded,
       predicate below 1e-12 (basis: sums of <= 40 cosines in double precision).
 C2 E  one-left ports (n-1,R) at t=n+1, n=1..14: n paths, all positive, areas in arithmetic
       progression of step 2; W_{n+1}-2W_n+W_{n-1} has the single lag 2n with coefficient 2.
 C3 S  alias: all ports up to tick M+6, M in {6,7,8,9,12,15}: max distance between port laws
       of aliased pairs (2k = +-2k' mod M) is smaller than min distance of non-aliased pairs.
 C4 S  p_0 = C(2m,m)/4^m (quadrature with 4m+8 points, exact for degree 2m) and Hoelder
       p_m(h_k) <= p_0(1+1e-12) for m=1..8, M in {63,97}, all k. MEASURED: h giving 0.008658 p_0.
 C5 E  n*inverse(2) is a unit at every odd M in 3..399 iff |n| is a power of two, n=-40..40
       (n != 0); 2*((M+1)/2) = 1 mod M; 3 is a unit mod 5^j, j=1..8.
"""
import json, math, sys, random
from fractions import Fraction as Fr
from itertools import combinations
from collections import Counter
from pathlib import Path
import numpy as np

OUT = Path(__file__).with_name("xr21_loops_result.json")
if OUT.exists():
    sys.exit("result file exists; refusing to overwrite")
random.seed(20261113)
res = {"predicates": {}, "measured": {}, "failed_kept": []}


def rec(name, ok, **info):
    res["predicates"][name] = dict(met=bool(ok), **info)
    if not ok:
        res["failed_kept"].append(name)


# ---------- exact path machinery: word of +1 (R) / -1 (L) ----------
def area(word, x=0, signs=None):
    A = 0
    for i, d in enumerate(word):
        A += (signs[i] if signs else 1) * x
        x += d
    return A, x


def balanced(n2, first=None, last=None):
    for pos in combinations(range(n2), n2 // 2):
        w = [-1] * n2
        for p in pos:
            w[p] = 1
        if (first is None or w[0] == first) and (last is None or w[-1] == last):
            yield tuple(w)


def hsign(word, incoming=1):
    s, prev = 1, incoming
    for d in word:
        if prev == -1 and d == -1:
            s = -s
        prev = d
    return s


# A1
bad = n = 0
for a in range(1, 13):
    for x in range(-20, 21):
        n += 1
        r = area((1,) * a + (-1,) * a, x)
        l = area((-1,) * a + (1,) * a, x)
        if not (r == (2 * a * x + a * a, x) and l == (2 * a * x - a * a, x)):
            bad += 1
rec("A1", bad == 0, instances=n, bad=bad,
    note="R^aL^a ends on rail L, L^aR^a on rail R; H from R gives +,+; X has no sign")


# A2 ring
def ring_area(word, x, N):
    A = 0
    for d in word:
        A += x % N
        x += d
    return A


q = nq = qbad = nqdep = 0
for N in range(4, 25):
    for M in range(2, 13):
        for a in range(1, 5):
            rel = set()
            ok = True
            for x in range(N):
                r = ring_area((1,) * a + (-1,) * a, x, N)
                l = ring_area((-1,) * a + (1,) * a, x, N)
                rel.add((r - l) % M)
                ok &= (r - (2 * a * x + a * a)) % M == 0 and (l - (2 * a * x - a * a)) % M == 0
            if N % M == 0:
                q += 1
                qbad += (not ok) or len(rel) != 1
            else:
                nq += 1
                nqdep += len(rel) != 1
rec("A2", qbad == 0, qualifying=q, qualifying_bad=qbad, nonqualifying=nq,
    nonqualifying_with_site_dependent_rail_phase=nqdep)

# A3 heralded
n = bad = 0
for a in range(1, 7):
    for w in balanced(2 * a, 1, -1):
        wc = tuple(-d for d in w)
        rels = {area(w, x)[0] - area(wc, x)[0] for x in (-3, 0, 5)}
        n += 1
        if hsign(w) != hsign(wc) or len(rels) != 1 or rels != {2 * area(w)[0]}:
            bad += 1
        if Fr(2, 4 ** a) != Fr(1, 2 ** (2 * a - 1)):
            bad += 1
rec("A3", bad == 0, words=n, bad=bad,
    herald_probability_at_note_parameters={"a=64 (M=32768 fixed-sign)": "2^-127",
                                           "a=90 (M=32768 compensated, if heralded)": "2^-179"})

# A4, A5
areasRL = {}
bad4 = bad5 = 0
for a in range(1, 9):
    S = {area(w)[0] for w in balanced(2 * a, 1, -1)}
    areasRL[a] = S
    bad4 += S != {a * a - 2 * j for j in range((a - 1) ** 2 + 1)}
for a in range(1, 8):
    S = {area(w)[0] for w in balanced(2 * a)}
    bad5 += (max(S) - min(S) != 2 * a * a) or any((s - a) % 2 for s in S)
rec("A4", bad4 == 0, a_range="1..8", bad=bad4)
rec("A5", bad5 == 0, a_range="1..7", bad=bad5)

# A6
bad = n = 0
for b in range(1, 13):
    sg = [-1] * b + [1] * b + [1] * b + [-1] * b
    for x in range(-20, 21):
        n += 1
        r = area((1,) * (2 * b) + (-1,) * (2 * b), x, sg)[0]
        l = area((-1,) * (2 * b) + (1,) * (2 * b), x, sg)[0]
        bad += not (r == 2 * b * b and l == -2 * b * b)
rec("A6", bad == 0, instances=n, bad=bad)

# A7
allA = set().union(*areasRL.values())
bad = 0
admit = []
for M in range(2, 97):
    ex = any((4 * (2 * A) - M) % (4 * M) == 0 or (4 * (2 * A) + M) % (4 * M) == 0 for A in allA)
    admit.append(M) if ex else None
    bad += ex != (M % 8 == 0)
rec("A7", bad == 0, M_range="2..96", admitting=admit, bad=bad)

# A8
bad = 0
for M in range(8, 4097):
    qd, r = divmod(M, 8)
    for d in ([qd, qd + 1] if r == 4 else [qd + (r > 4)]):
        bad += abs(Fr(2 * d, M) - Fr(1, 4)) > Fr(1, M)
rec("A8", bad == 0, bad=bad)


# ---------- B: flight model ----------
def fly(M, ref, fl, carrier=-math.pi / 2, loop_r=1, mode="comp", cot=1.0, T=1.5, conj=False):
    h0 = 2 * math.pi / M
    d = h0 ** 0.25
    nfl = round(T / d ** 3)
    L = 1 << 13
    x = np.arange(L) - L // 2
    sig = d ** -1.25
    v = np.exp(-x ** 2 / (4 * sig ** 2)) * np.exp(1j * carrier * x)
    v /= np.linalg.norm(v)
    R, Lr = v.astype(complex), np.zeros(L, complex)
    r2 = 1 / math.sqrt(2)
    hl = ref * loop_r * h0
    if mode == "fixed":
        a = round(math.sqrt(math.pi / (4 * h0)))
        sg = [1] * (2 * a)
    else:
        b = round(math.sqrt(math.pi / (8 * h0)))
        a = 2 * b
        sg = [-1] * b + [1] * (2 * b) + [-1] * b
    ph = {s: np.exp(-1j * s * hl * x) for s in (1, -1)}
    for t in range(2 * a):
        if t == 0:
            R, Lr = r2 * (R + Lr), r2 * (R - Lr)
        elif t == a:
            R, Lr = Lr, R
        R = np.roll(R * ph[sg[t]], 1)
        Lr = np.roll(Lr * ph[sg[t]], -1)
    th = math.atan2(1.0, cot)
    c, s = math.cos(th), math.sin(th)
    pf = np.exp(-1j * fl * h0 * x)
    comps = [(R, Lr)] if mode != "tagged" else [(R, 0 * Lr), (0 * R, Lr)]
    p = np.zeros(L)
    for (A, B) in comps:
        for _ in range(nfl):
            A, B = c * A + s * B, s * A - c * B
            A = np.roll(A * pf, 1)
            B = np.roll(B * pf, -1)
        p += abs(A) ** 2 + abs(B) ** 2
    Y = d * d * x
    Tt = nfl * d ** 3
    mean = float((p * Y).sum())
    edge = float(p[: L // 8].sum() + p[-L // 8:].sum())
    return dict(mean=mean, T=Tt, ticks=nfl, a=a, delta=d, total=float(p.sum()), edge_mass=edge,
                neg_half=float(p[x < 0].sum())), p, Y


Bm = {}
b1bad = b1n = 0
b2max = 0.0
for M in (2 ** 13, 2 ** 15, 2 ** 19, 2 ** 21):
    rows = {}
    runs = {"i ref+ fl+": (1, 1, -math.pi / 2), "ii ref+ fl-": (1, -1, -math.pi / 2),
            "iii ref- fl-": (-1, -1, -math.pi / 2), "iv ref- fl+": (-1, 1, -math.pi / 2),
            "v carrier+pi/2 ref+ fl+": (1, 1, math.pi / 2)}
    p_i = None
    for name, (ref, fl, car) in runs.items():
        o, p, Y = fly(M, ref, fl, car)
        ideal = -ref * fl * o["T"] ** 2 / 2
        o["ideal_eq2"] = ideal
        o["ratio"] = o["mean"] / ideal
        o["rms_about_ideal"] = float(math.sqrt((p * (Y - ideal) ** 2).sum()))
        rows[name] = o
        b1n += 1
        b1bad += (o["mean"] > 0) != (ideal > 0)
        if name.startswith("i "):
            p_i = p
    o, p, _ = fly(M, -1, -1, math.pi / 2)
    dd = float(abs(p - p_i).max())
    b2max = max(b2max, dd)
    rows["conjugate of i: max abs law difference"] = dd
    o, p, Y = fly(M, 1, 1, mode="fixed")
    rows["fixed-sign loop ++"] = dict(o, ideal_eq2=-o["T"] ** 2 / 2)
    o, _, _ = fly(M, 1, 3, loop_r=3)
    rows["r=3 (note: opposite side, 3x)"] = dict(o, note_value=+3 * o["T"] ** 2 / 2)
    o, _, _ = fly(M, 1, 2, loop_r=2)
    rows["r=2 (weights 1/2,1/2)"] = o
    o, _, _ = fly(M, 1, 1, mode="tagged")
    rows["tagged arms ++"] = o
    o, _, _ = fly(M, 1, 2, cot=0.5)
    rows["mass 2 (cot=1/2), force 2F"] = o
    o, _, _ = fly(M, 1, 1, cot=0.5)
    rows["mass 2 (cot=1/2), force F"] = o
    Bm[str(M)] = rows
res["measured"]["B_flight"] = Bm
rec("B1", b1bad == 0, instances=b1n, bad=b1bad)
rec("B2", b2max < 1e-9, max_abs_difference=b2max)


# ---------- C: note 2 ----------
def ports(T, incoming=1):
    """all words of length T from site 0; returns {(x,last): [(area, sign)]}"""
    out = {}
    for bits in range(1 << T):
        w = tuple(1 if bits >> i & 1 else -1 for i in range(T))
        A, x = area(w)
        out.setdefault((x, w[-1]), []).append((A, hsign(w, incoming)))
    return out


def lagc(paths):
    c = Counter()
    for A, s in paths:
        for B, t in paths:
            c[abs(A - B)] += s * t
    return {k: v for k, v in c.items() if v}


P5 = ports(5)[(1, 1)]
lc = lagc(P5)
A0 = sorted(A for A, _ in P5)[2:4]
pairs = sorted((2 * A - sum(A0), s) for A, s in P5)
ok = len(P5) == 6 and lc == {0: 4, 2: -4, 4: 2, 6: -4, 8: 2} and Fr(6, 32) == Fr(3, 16) and sum(lc.values()) == 0
rec("C1", ok, paths=len(P5), lag_coefficients=lc, doubled_centred_area_sign_pairs=pairs,
    note="the note's pairs (4,-),(2,+),(0,-),(0,+),(-2,+),(-4,-) are compared through lags")
mx = 0.0
for M in (5, 8, 63, 97):
    wts = [random.randint(0, 9) for _ in range(M + 1)]
    tot = sum(wts) or 1
    c = wts[M] / tot
    bk = [w / tot for w in wts[:M]]
    D = lambda j: sum(bk[k] * math.cos(4 * math.pi * k * j / M) for k in range(M))
    lhs = c * 6 + sum(bk[k] * abs(sum(s * complex(math.cos(2 * math.pi * k * A / M), math.sin(2 * math.pi * k * A / M))
                                      for A, s in P5)) ** 2 for k in range(M))
    mx = max(mx, abs(lhs - (4 + 2 * c - 4 * D(1) + 2 * D(2) - 4 * D(3) + 2 * D(4))))
rec("C1b", mx < 1e-12, max_abs_difference=mx, orders=[5, 8, 63, 97])

bad = 0
W = {0: Counter()}
for nn in range(1, 16):
    pp = ports(nn + 1)[(nn - 1, 1)]
    As = sorted(A for A, _ in pp)
    bad += len(pp) != nn or any(s != 1 for _, s in pp) or any(b - a != 2 for a, b in zip(As, As[1:]))
    c = Counter()
    for A, s in pp:
        for B, t in pp:
            c[A - B] += 1
    W[nn] = c
for j in range(1, 15):
    dlt = Counter(W[j + 1])
    dlt.subtract({k: 2 * v for k, v in W[j].items()})
    dlt.update(W[j - 1])
    dlt = {k: v for k, v in dlt.items() if v}
    bad += dlt != {2 * j: 1, -2 * j: 1}
rec("C2", bad == 0, n_range="1..14", bad=bad)

sep = {}
c3 = True
for M in (6, 7, 8, 9, 12, 15):
    laws = {}
    for k in range(M):
        st = {(0, 1): 1 + 0j}
        vec = []
        for t in range(M + 6):
            new = {}
            for (x, inc), amp in st.items():
                g = complex(math.cos(2 * math.pi * k * (x % M) / M), math.sin(2 * math.pi * k * (x % M) / M))
                for dd_ in (1, -1):
                    sgn = -1 if (inc == -1 and dd_ == -1) else 1
                    key = (x + dd_, dd_)
                    new[key] = new.get(key, 0) + amp * g * sgn / math.sqrt(2)
            st = new
            vec += [abs(st.get((xx, rr), 0)) ** 2 for xx in range(-t - 1, t + 2) for rr in (1, -1)]
        laws[k] = np.array(vec)
    al, non = [0.0], []
    for k in range(M):
        for k2 in range(k + 1, M):
            dist = float(abs(laws[k] - laws[k2]).max())
            (al if ((2 * k - 2 * k2) % M == 0 or (2 * k + 2 * k2) % M == 0) else non).append(dist)
    sep[str(M)] = dict(max_aliased=max(al), min_nonaliased=min(non), aliased_pairs=len(al) - 1, other_pairs=len(non))
    c3 &= max(al) < min(non)
rec("C3", c3, separation=sep)


def pm(m, h):
    N = 4 * m + 8
    qv = 2 * np.pi * np.arange(N) / N
    f = np.ones(N)
    for j in range(m):
        f *= np.sin(qv + (2 * j + 1) * h) ** 2
    return float(f.mean())


bad = n = 0
for m in range(1, 9):
    p0 = math.comb(2 * m, m) / 4 ** m
    bad += abs(pm(m, 0.0) - p0) > 1e-12
    for M in (63, 97):
        for k in range(M):
            n += 1
            bad += pm(m, 2 * math.pi * k / M) > p0 * (1 + 1e-12)
rec("C4", bad == 0, instances=n, bad=bad)
p0 = math.comb(12, 6) / 4 ** 6
res["measured"]["C4_m6_ratio_scan"] = {f"h=pi/{j}": pm(6, math.pi / j) / p0 for j in range(2, 40)}
res["measured"]["C4_m6_posterior_count_if_ratio_0.008658"] = 2 ** -6 / (2 ** -6 + 0.008658 * p0)

bad = 0
for nn in range(-40, 41):
    if nn == 0:
        continue
    unit_all = all(math.gcd((nn * ((M + 1) // 2)) % M, M) == 1 for M in range(3, 400, 2))
    pw = abs(nn) & (abs(nn) - 1) == 0
    bad += unit_all != pw
bad += any((2 * ((M + 1) // 2)) % M != 1 for M in range(3, 400, 2))
bad += any(math.gcd(3, 5 ** j) != 1 for j in range(1, 9))
rec("C5", bad == 0, bad=bad)

res["counts"] = dict(met=sum(v["met"] for v in res["predicates"].values()),
                     failed=len(res["failed_kept"]), measured_only=len(res["measured"]))
OUT.write_text(json.dumps(res, indent=1, default=str) + "\n")
print(json.dumps(res["counts"]), res["failed_kept"])
