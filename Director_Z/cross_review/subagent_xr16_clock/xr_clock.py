"""Cross-review program for 'Preparing an optical phase reference on a signed cycle'.

Written from the note text only; imports nothing from the author's code.
Run:  python3 -I xr_clock.py <result.json>     (refuses to overwrite)
Fixed seed 20261113. Exact arithmetic (int / Fraction / Z[sqrt2]) in A, B-exact, C6, D4, E.
Floating point elsewhere; tolerance bases are stated per predicate and the measured
residual is always stored.

PREDICATES (fixed before the first run; a failure is kept, never edited)

A  eight-sheet transfer (own walk: H left, V right, Hadamard H->(H+V), V->(H-V),
   sheet translated by `plate` on every departure from x=0, V launched `launch` sheets ahead)
 A1 for 300 random integer seeds that PASS the hypothesis (T^4 s = -s, S>0; tested per seed),
    return(10 steps, launch 6, plate 3) == (688 S + 480 J)/(2048 S) exactly.
 A2 all-plus words m=0..3 give 43,73,83,85 /128; all-minus give 43,13,3,1 /128.
 A3 every +/- word of length m<=7 (255 words incl. empty): A1 formula holds, and for each m
    the joint masses S_w/4^(m+1) sum to 1/2.
 A4 (S,J)->(2S+J,2J+2S) from (2,0) equals the closed forms in Z[sqrt2] for m=0..60, and
    equals S,J computed from the actual vector (I+T)^m(e0-e4).
 A5 all-plus return at m=60 agrees with 43/128+15 sqrt2/64 to 1e-30 (basis: ratio
    ((2-sqrt2)/(2+sqrt2))^60 ~ 1e-46); limits print as 0.6673938 and 0.0044812.
 A6a for all-plus seeds m=0..12: changing only launch (6->2) or only plate (3->1) gives 51/128.
 A6b the same for the 300 random odd seeds of A1 (wording test of "every one of these odd seeds").
 A7 (launch,plate)=(-6,-3) gives the identical full position distribution, 300 random odd seeds.
 A8 hypothesis is needed: among 300 random seeds that FAIL oddness, at least one violates A1.
 A9 total squared norm after t steps == 2^(t+1) S for t=0..14, launch,plate in 0..7 (one seed each).

B  sequential verdict
 B1 e_m=(3-2sqrt2)^m/(1+(3-2sqrt2)^m) equals the exact gambler's-ruin posterior computed by
    absorbing-chain linear algebra with a=(2+sqrt2)/4 (m=1..8), 40 digits, |diff|<1e-30.
 B2 mean informative reads == sqrt2 m (1-2e_m) from the same chain (m=1..8), |diff|<1e-30.
 B3 m=4: 1-e_m rounds to 0.9991342, mean rounds to 5.64706.

C  support bound
 C1 M in 3..40 and 64, every L: largest eigenvalue of the arc compression of the k=+-1
    projector (numpy eigvalsh) equals Lambda_M(L); |diff|<1e-10 (basis: eigvalsh backward
    error ~1e-15 * norm<=1, four orders of margin).
 C2 3000 random complex states on an arc tensored with a 3-dim ancilla: W<=Lambda+1e-12.
 C3 3000 random L-subsets (not arcs): top eigenvalue <= 2L/M + 1e-12; count those > Lambda.
 C4 40 digits. Even M: Lambda(M/2-1)=Lambda(M/2)=1/2 (|diff|<1e-35), Lambda(M/2+1)>1/2.
    Odd M: Lambda((M-1)/2)-1/2 == (sec(pi/M)-1)/(2M) and Lambda((M-3)/2)<1/2.
    M = 4..400 and 4096, 65536, 65537.
 C5 Lambda_M(L) nondecreasing in integer L (>= -1e-35), same M range up to 400.
 C6 exact. F=2pi, delta=2^-b, b=1..10 (9,10 not in the author's file), eps in {1,delta},
    v in {1,2,3}: n*=min{n: min(M,2vn+1)>M/2}; for v=1 n*=M/4 and n* tau = 1/(4 delta);
    for all v n* tau >= 1/(4 v delta) - tau/(2v).

D  router and analyzer (M=128, 512, 2048 are not in the author's tables; r=7, 11 neither)
 D1 M in {8,128,512}: FFT of the +-1 square wave: even modes 0, odd modes
    4/(M^2 sin^2(pi k/M)) (|diff|<1e-12), sum 1, pair weight >= 8/pi^2.
 D2 M=4096, r=9: total accepted mass rounds to 0.80688 and wrong fraction among accepts
    rounds to 0.000525.
 D3 l=3..13, r in {1,3,5,7,9,11,15}: wrong joint acceptance <= (1-W) 2^(-r/2);
    target joint acceptance >= W(1-B_r); B_r <= 2^(-r/2)/(1-(2cos(pi/8))^-r).
 D4 exact: sum_{j=3..l} M/2^j = M/4-1 and sum r_j M/2^j <= M(r/4+1/2), l=3..20, r odd<=21.
 D5 flips c in {0.05,0.1,0.3}, r in {9,21,41}, l=3..14, r_j=r+2(j-3): target rejection
    <= beta^r/(1-beta^2); every other odd k acceptance <= beta^r.
 D6 same c, fixed r=9: target all-scale acceptance strictly decreases in l=3..14.

E  parity (author request 1)
 E1 even cycle M=16, every tick a +-1 hop: all 2^t words, t<=12: all equal-time arms share
    site parity (so every equal-time relative delay is even).
 E2 300 random integer vectors on one sublattice of M=16,64: weight(k)==weight(k+M/2) for
    all k (|diff|<1e-9 relative), hence W_{+-1}<=1/2.
 E3 same cycle plus ONE extra node adjacent to sites 0 and 1 (a triangle), still one hop per
    tick: at t=2 the reachable cycle sites contain both parities.
 E4 M=16: for every even delay 2q the plus-probabilities of k=1 and k=M/2+1 coincide exactly
    (cos^2 identity, 1e-15); for delay 1 they differ by cos(2pi/M).

F  band target (author request 2), M=1024, single-sign band |k-1|<=kappa, |B|=2kappa+1
 F1 top eigenvalue of arc compression <= |B| L/M for all tested L (trace bound).
 F2 at L=ceil(M/|B|) the top eigenvalue exceeds 1/2 for kappa in {1,2,4,8,16}; values stored.
"""
import sys, os, json, math, random, itertools
from fractions import Fraction as Fr
import numpy as np
import mpmath as mp

SEED = 20261113
rng = random.Random(SEED)
nrng = np.random.default_rng(SEED)
mp.mp.dps = 40
OUT = {}
def rec(name, ok, **info):
    OUT[name] = dict(met=bool(ok), **info)

# ---------- A ----------
def rot(s, d):
    n = len(s); d %= n
    return [s[(j - d) % n] for j in range(n)]
def vadd(a, b, sg=1): return [x + sg * y for x, y in zip(a, b)]
def walk(seed, launch, plate, depth):
    """returns {x: integer squared mass}, total integer mass"""
    Z = [0] * len(seed)
    cur = {0: (list(seed), rot(seed, launch))}          # x -> (H vec, V vec)
    for _ in range(depth):
        nxt = {}
        for x, (h, v) in cur.items():
            if x == 0:
                h, v = rot(h, plate), rot(v, plate)
            hn, vn = vadd(h, v), vadd(h, v, -1)         # Hadamard
            l = nxt.setdefault(x - 1, [list(Z), list(Z)]); l[0] = vadd(l[0], hn)
            r = nxt.setdefault(x + 1, [list(Z), list(Z)]); r[1] = vadd(r[1], vn)
        cur = {x: (a, b) for x, (a, b) in nxt.items()}
    dist = {x: sum(t * t for t in a) + sum(t * t for t in b) for x, (a, b) in cur.items()}
    return dist, sum(dist.values())
def SJ(s):
    S = sum(t * t for t in s); J = 2 * sum(a * b for a, b in zip(s, rot(s, 1)))
    return S, J
def ret(seed, launch=6, plate=3, depth=10):
    d, tot = walk(seed, launch, plate, depth)
    return Fr(d.get(0, 0), tot)
def is_odd(s): return rot(s, 4) == [-t for t in s] and any(s)
def formula(s):
    S, J = SJ(s); return Fr(688 * S + 480 * J, 2048 * S)

odd_seeds = []
while len(odd_seeds) < 300:
    h = [rng.randint(-9, 9) for _ in range(4)]
    s = h + [-t for t in h]
    if is_odd(s): odd_seeds.append(s)
bad = [s for s in odd_seeds if ret(s) != formula(s)]
rec("A1", not bad, qualifying=len(odd_seeds), failures=len(bad), example=bad[:1])

seed0 = [1, 0, 0, 0, -1, 0, 0, 0]
def word(w):
    s = list(seed0)
    for c in w: s = vadd(s, rot(s, 1), 1 if c == '+' else -1)
    return s
plus = [ret(word('+' * m)) for m in range(4)]; minus = [ret(word('-' * m)) for m in range(4)]
rec("A2", plus == [Fr(n, 128) for n in (43, 73, 83, 85)] and minus == [Fr(n, 128) for n in (43, 13, 3, 1)],
    plus=list(map(str, plus)), minus=list(map(str, minus)))

fails = 0; cnt = 0; zero = 0; sums = {}
for m in range(8):
    tot = Fr(0)
    for w in itertools.product('+-', repeat=m):
        s = word(w); cnt += 1
        if not any(s): zero += 1; continue
        if not is_odd(s) or ret(s) != formula(s): fails += 1
        tot += Fr(SJ(s)[0], 4 ** (m + 1))
    sums[m] = str(tot)
rec("A3", fails == 0 and all(v == '1/2' for v in sums.values()), words=cnt, zero_words=zero, failures=fails, joint_mass_sums=sums)

class Q2:  # a + b sqrt2
    def __init__(s, a, b=0): s.a, s.b = a, b
    def __mul__(s, o): return Q2(s.a * o.a + 2 * s.b * o.b, s.a * o.b + s.b * o.a)
    def __add__(s, o): return Q2(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q2(s.a - o.a, s.b - o.b)
    def t(s): return (s.a, s.b)
ok = True; S, J = 2, 0; p = Q2(1); q = Q2(1); vec = list(seed0); SJs = []
for m in range(61):
    Sc = (p + q); Jc = Q2(0, 1) * (p - q)
    ok &= Sc.t() == (S, 0) and Jc.t() == (J, 0) and SJ(vec) == (S, J)
    SJs.append((S, J))
    S, J = 2 * S + J, 2 * J + 2 * S
    p = p * Q2(2, 1); q = q * Q2(2, -1); vec = vadd(vec, rot(vec, 1))
rec("A4", ok, depth_checked=60)
S60, J60 = SJs[60]
lim_hi = mp.mpf(43) / 128 + 15 * mp.sqrt(2) / 64; lim_lo = mp.mpf(43) / 128 - 15 * mp.sqrt(2) / 64
val = (mp.mpf(688) * S60 + 480 * J60) / (2048 * S60)
rec("A5", abs(val - lim_hi) < mp.mpf(10) ** -30 and mp.nstr(lim_hi, 7) == '0.6673938' and mp.nstr(lim_lo, 5) == '0.0044812',
    diff=mp.nstr(abs(val - lim_hi), 5), hi=mp.nstr(lim_hi, 12), lo=mp.nstr(lim_lo, 12))

def single(s): return [ret(s, 2, 3), ret(s, 6, 1)]
a6a = [single(word('+' * m)) for m in range(13)]
rec("A6a", all(x == [Fr(51, 128)] * 2 for x in a6a), n=13)
a6b = [s for s in odd_seeds if single(s) != [Fr(51, 128)] * 2]
rec("A6b", not a6b, qualifying=len(odd_seeds), failures=len(a6b),
    example=[dict(seed=s, launch_changed=str(single(s)[0]), plate_changed=str(single(s)[1])) for s in a6b[:2]])
a7 = [s for s in odd_seeds if walk(s, 6, 3, 10) != walk(s, -6, -3, 10)]
rec("A7", not a7, qualifying=len(odd_seeds), failures=len(a7))
non = []
while len(non) < 300:
    s = [rng.randint(-9, 9) for _ in range(8)]
    if any(s) and not is_odd(s): non.append(s)
viol = sum(ret(s) != formula(s) for s in non)
rec("A8", viol >= 1, non_odd_seeds=len(non), violate_formula=viol)
a9 = 0; n9 = 0
for t in range(15):
    for l in range(8):
        for g in range(8):
            s = [rng.randint(-5, 5) for _ in range(8)]; n9 += 1
            a9 += walk(s, l, g, t)[1] != 2 ** (t + 1) * SJ(s)[0]
rec("A9", a9 == 0, cases=n9, failures=a9)

# ---------- B ----------
a = (2 + mp.sqrt(2)) / 4
b1 = b2 = True; store = {}
for m in range(1, 9):
    n = 2 * m - 1                                   # interior scores -m+1..m-1
    A = mp.zeros(n); bu = mp.zeros(n, 1); one = mp.ones(n, 1)
    for i in range(n):
        A[i, i] = 1
        if i + 1 < n: A[i, i + 1] = -a
        else: bu[i] = a
        if i - 1 >= 0: A[i, i - 1] = -(1 - a)
    up = mp.lu_solve(A, bu)[m - 1]                  # P(hit +m | true class is 'plus-biased')
    T = mp.lu_solve(A, one)[m - 1]
    # equal priors, symmetric likelihoods: posterior of losing class at a boundary = 1-up
    e = (3 - 2 * mp.sqrt(2)) ** m / (1 + (3 - 2 * mp.sqrt(2)) ** m)
    b1 &= abs((1 - up) - e) < mp.mpf(10) ** -30
    b2 &= abs(T - mp.sqrt(2) * m * (1 - 2 * e)) < mp.mpf(10) ** -30
    store[m] = dict(e=mp.nstr(e, 12), mean=mp.nstr(T, 12))
rec("B1", b1, table=store); rec("B2", b2)
e4 = (3 - 2 * mp.sqrt(2)) ** 4 / (1 + (3 - 2 * mp.sqrt(2)) ** 4)
rec("B3", mp.nstr(1 - e4, 7) == '0.9991342' and mp.nstr(mp.sqrt(2) * 4 * (1 - 2 * e4), 6) == '5.64706',
    low=mp.nstr(1 - e4, 10), mean=mp.nstr(mp.sqrt(2) * 4 * (1 - 2 * e4), 10))

# ---------- C ----------
def lam(M, L):
    if L >= M: return 1.0
    return (L + abs(math.sin(2 * math.pi * L / M)) / math.sin(2 * math.pi / M)) / M
def proj(M, ks):
    j = np.arange(M)
    P = np.zeros((M, M), complex)
    for k in ks:
        v = np.exp(2j * np.pi * k * j / M) / math.sqrt(M); P += np.outer(v, v.conj())
    return P
worst = 0.0; n1 = 0
Ms = list(range(3, 41)) + [64]
for M in Ms:
    P = proj(M, {1 % M, (-1) % M})
    for L in range(1, M + 1):
        top = np.linalg.eigvalsh(P[:L, :L])[-1]; n1 += 1
        worst = max(worst, abs(top - lam(M, L)))
rec("C1", worst < 1e-10, cases=n1, max_abs_diff=worst)
exc = 0; maxratio = 0.0
for _ in range(3000):
    M = int(nrng.integers(3, 41)); L = int(nrng.integers(1, M + 1)); st = int(nrng.integers(0, M))
    P = proj(M, {1 % M, (-1) % M})
    psi = np.zeros((M, 3), complex)
    idx = [(st + i) % M for i in range(L)]
    psi[idx] = nrng.normal(size=(L, 3)) + 1j * nrng.normal(size=(L, 3))
    psi /= np.linalg.norm(psi)
    assert abs(np.linalg.norm(psi[[i for i in range(M) if i not in idx]])) == 0   # hypothesis
    W = np.linalg.norm(P @ psi) ** 2
    exc += W > lam(M, L) + 1e-12; maxratio = max(maxratio, W / lam(M, L))
rec("C2", exc == 0, trials=3000, exceed=int(exc), max_W_over_Lambda=maxratio)
over = 0; above_arc = 0
for _ in range(3000):
    M = int(nrng.integers(5, 41)); L = int(nrng.integers(1, M + 1))
    idx = np.sort(nrng.choice(M, L, replace=False))
    P = proj(M, {1, M - 1})
    top = np.linalg.eigvalsh(P[np.ix_(idx, idx)])[-1]
    over += top > 2 * L / M + 1e-12; above_arc += top > lam(M, L) + 1e-9
rec("C3", over == 0, trials=3000, exceed_trace_bound=int(over), nonarc_sets_exceeding_arc_capacity=int(above_arc))
def lamp(M, L):
    M = mp.mpf(M)
    return (L + abs(mp.sin(2 * mp.pi * L / M)) / mp.sin(2 * mp.pi / M)) / M
tiny = mp.mpf(10) ** -35; c4 = []; c5 = []
for M in list(range(4, 401)) + [4096, 65536, 65537]:
    if M % 2 == 0:
        h = M // 2
        if not (abs(lamp(M, h - 1) - mp.mpf(1) / 2) < tiny and abs(lamp(M, h) - mp.mpf(1) / 2) < tiny and lamp(M, h + 1) > mp.mpf(1) / 2 + tiny): c4.append(M)
    else:
        L = (M - 1) // 2
        if not (abs(lamp(M, L) - mp.mpf(1) / 2 - (mp.sec(mp.pi / M) - 1) / (2 * M)) < tiny and lamp(M, L) > mp.mpf(1) / 2 and lamp(M, L - 1) < mp.mpf(1) / 2): c4.append(M)
    if M <= 400:
        vals = [lamp(M, L) for L in range(1, M)] + [mp.mpf(1)]
        if any(vals[i + 1] - vals[i] < -tiny for i in range(len(vals) - 1)): c5.append(M)
rec("C4", not c4, sizes=400, failing_M=c4[:10], n_fail=len(c4))
rec("C5", not c5, failing_M=c5[:10], n_fail=len(c5))
c6 = []; rows = []
for epsmode in ("one", "delta"):
    for b in range(1, 11):
        d = Fr(1, 2 ** b); eps = Fr(1) if epsmode == "one" else d
        Mq = 1 / (eps * d ** 3); assert Mq.denominator == 1; M = int(Mq); tau = eps * d * d
        for v in (1, 2, 3):
            # run-0 note: the brute loop below was the whole search and did not finish at b=10
            # (M=2^40); run 0 was killed before any result file existed. The predicate is
            # unchanged; n* is now the closed form, cross-checked by the brute loop for M<=2^20.
            n = (M // 2 - 1) // (2 * v) + 1 if M % 2 == 0 else None
            assert min(M, 2 * v * n + 1) * 2 > M and not (n > 0 and min(M, 2 * v * (n - 1) + 1) * 2 > M)
            if M <= 2 ** 20:
                nb_ = 0
                while not (min(M, 2 * v * nb_ + 1) * 2 > M): nb_ += 1
                assert nb_ == n
            okk = n * tau >= 1 / (4 * v * d) - tau / (2 * v)
            if v == 1: okk &= (n == M // 4 and M % 4 == 0 and n * tau == 1 / (4 * d))
            if not okk: c6.append((epsmode, b, v))
            rows.append(dict(eps=epsmode, b=b, v=v, M=M, n=n, time=str(n * tau), bound=str(1 / (4 * v * d) - tau / (2 * v))))
rec("C6", not c6, cases=len(rows), failures=c6, rows=[r for r in rows if r["b"] in (1, 4, 9, 10)])

# ---------- D ----------
d1 = True; info = {}
for M in (8, 128, 512):
    s = np.array([1.0] * (M // 2) + [-1.0] * (M // 2)) / math.sqrt(M)
    w = np.abs(np.fft.fft(s)) ** 2 / M
    th = np.array([0.0 if k % 2 == 0 else 4 / (M * math.sin(math.pi * k / M)) ** 2 for k in range(M)])
    pair = w[1] + w[M - 1]
    d1 &= np.max(np.abs(w - th)) < 1e-12 and abs(w.sum() - 1) < 1e-12 and pair >= 8 / math.pi ** 2
    info[M] = dict(max_diff=float(np.max(np.abs(w - th))), pair=float(pair))
rec("D1", d1, info=info, floor=8 / math.pi ** 2)
def maj(p, r):
    return math.fsum(math.comb(r, i) * p ** i * (1 - p) ** (r - i) for i in range(r // 2 + 1, r + 1))
def analyze(l, r, c=0.0, grow=False):
    M = 2 ** l; tgt = 0.0; wrong = 0.0; worst_other = 0.0; tacc = None
    for k in range(1, M, 2):
        w = 4 / (M * math.sin(math.pi * k / M)) ** 2; acc = 1.0
        for j in range(3, l + 1):
            p = math.cos(math.pi * k / 2 ** j) ** 2; p = c + (1 - 2 * c) * p
            acc *= maj(p, r + 2 * (j - 3) if grow else r)
        if k in (1, M - 1): tgt += w * acc; tacc = acc
        else: wrong += w * acc; worst_other = max(worst_other, acc)
    W = 8 / (M * math.sin(math.pi / M)) ** 2
    return dict(W=W, target=tgt, wrong=wrong, target_acc=tacc, worst_other=worst_other)
o = analyze(12, 9); acc = o["target"] + o["wrong"]; frac = o["wrong"] / acc
rec("D2", f"{acc:.5f}" == "0.80688" and f"{frac:.6f}" == "0.000525", accepted_total=acc, accepted_target=o["target"], wrong_fraction=frac)
d3 = []; n3 = 0
for l in range(3, 14):
    for r in (1, 3, 5, 7, 9, 11, 15):
        o = analyze(l, r); n3 += 1
        Br = math.fsum(math.sin(2 * math.pi / 2 ** j) ** r for j in range(3, 200))
        okk = (o["wrong"] <= (1 - o["W"]) * 2 ** (-r / 2) + 1e-15 and o["target"] >= o["W"] * (1 - Br) - 1e-15
               and Br <= 2 ** (-r / 2) / (1 - (2 * math.cos(math.pi / 8)) ** (-r)) + 1e-15)
        if not okk: d3.append((l, r))
rec("D3", not d3, cases=n3, failures=d3)
d4 = []
for l in range(3, 21):
    M = 2 ** l
    if sum(M // 2 ** j for j in range(3, l + 1)) != M // 4 - 1: d4.append(l)
    for r in range(1, 22, 2):
        if Fr(sum((r + 2 * (j - 3)) * (M // 2 ** j) for j in range(3, l + 1))) > M * (Fr(r, 4) + Fr(1, 2)): d4.append((l, r))
rec("D4", not d4, failures=d4)
d5 = []; d6 = []; n5 = 0; noisy = {}
for c in (0.05, 0.1, 0.3):
    dp = c + (1 - 2 * c) * math.sin(math.pi / 8) ** 2; beta = 2 * math.sqrt(dp * (1 - dp))
    for r in (9, 21, 41):
        for l in range(3, 15):
            o = analyze(l, r, c, True); n5 += 1
            if not (1 - o["target_acc"] <= beta ** r / (1 - beta ** 2) + 1e-15 and o["worst_other"] <= beta ** r + 1e-15): d5.append((c, r, l))
    seq = [analyze(l, 9, c)["target_acc"] for l in range(3, 15)]
    noisy[str(c)] = seq
    if not all(seq[i + 1] < seq[i] for i in range(len(seq) - 1)): d6.append(c)
rec("D5", not d5, cases=n5, failures=d5)
rec("D6", not d6, failures=d6, fixed_r9_target_acceptance_by_l=noisy)

# ---------- E ----------
M = 16; e1 = True
reach = {0}
for t in range(1, 13):
    reach = {(x + s) % M for x in reach for s in (1, -1)}      # set of all 2^t word endpoints
    e1 &= len({x % 2 for x in reach}) == 1
rec("E1", e1, ticks=12)
e2 = 0
for _ in range(300):
    M2 = rng.choice((16, 64)); par = rng.randint(0, 1)
    v = np.array([rng.randint(-9, 9) if j % 2 == par else 0 for j in range(M2)], float)
    if not v.any(): continue
    w = np.abs(np.fft.fft(v)) ** 2; w /= w.sum()
    e2 += np.max(np.abs(w - np.roll(w, M2 // 2))) > 1e-9 or (w[1] + w[M2 - 1]) > 0.5 + 1e-9
rec("E2", e2 == 0, failures=int(e2))
adj = {j: {(j + 1) % M, (j - 1) % M} for j in range(M)}; adj['x'] = {0, 1}; adj[0] = adj[0] | {'x'}; adj[1] = adj[1] | {'x'}
r2 = {0}
for t in range(2): r2 = {y for x in r2 for y in adj[x]}
sites = sorted(x for x in r2 if x != 'x')
rec("E3", len({x % 2 for x in sites}) == 2, reachable_cycle_sites_at_t2=sites)
pl = lambda k, dly: math.cos(math.pi * k * dly / M) ** 2
e4 = all(abs(pl(1, 2 * q) - pl(M // 2 + 1, 2 * q)) < 1e-15 for q in range(M)) and abs(pl(1, 1) - pl(M // 2 + 1, 1) - math.cos(2 * math.pi / M)) < 1e-15
rec("E4", e4, plus_prob_delay1=dict(k1=pl(1, 1), k_half_plus_1=pl(M // 2 + 1, 1)))

# ---------- F ----------
M = 1024; j = np.arange(M); f1 = True; f2 = True; tab = {}
for kap in (0, 1, 2, 4, 8, 16):
    ks = np.arange(1 - kap, 2 + kap); nb = len(ks)
    dif = j[:, None] - j[None, :]
    K = sum(np.exp(2j * np.pi * k * dif / M) for k in ks) / M
    row = {}
    for L in sorted({math.ceil(M / (2 * nb)), math.ceil(M / nb), math.ceil(2 * M / nb), M // 4 + 1 if kap == 0 else 8}):
        L = max(1, min(M, L)); top = float(np.linalg.eigvalsh(K[:L, :L])[-1]); row[L] = top
        f1 &= top <= nb * L / M + 1e-10
    if kap > 0: f2 &= row[math.ceil(M / nb)] > 0.5
    tab[f"kappa={kap},|B|={nb}"] = row
rec("F1", f1); rec("F2", f2, top_eigenvalue_by_L=tab)

if __name__ == "__main__":
    dest = sys.argv[1]
    if os.path.exists(dest): sys.exit("refusing to overwrite " + dest)
    met = [k for k, v in OUT.items() if v["met"]]; failed = [k for k, v in OUT.items() if not v["met"]]
    with open(dest, "x") as f:
        json.dump(dict(seed=SEED, met=met, failed=failed, predicates=OUT), f, indent=1, default=str)
    print("met", len(met), "failed", len(failed), failed)
