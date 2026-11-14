"""xr81: independent check of Director_G/Three_phase_rail_probability.md (own program, not the note's checker).

Conventions: w = exp(2 pi i/3); H = [[1,1],[1,-1]]/sqrt2; D = diag(1,w); bit 0 = H, bit 1 = DH,
word read left to right in time; start R = (1,0). Unnormalised spinor (a,b) in Z[w]^2 after t ticks,
true spinor = 2^(-t/2)(a,b). Bloch: Z=(|a|^2-|b|^2)/2^t, conj(a) b = p+q w, X=(2p-q)/2^t, Y=q/2^t
(y = sqrt3 Y). "Opposite pole" = a = 0. Seed 81 for all random draws. Exact arithmetic: Fractions /
integers / Z[w]; kernel ranks are exact ranks over F_p (p prime, 3 a square mod p) at random F_p
configurations, NOT over Q. Result file is opened with mode "x" (refuses to overwrite).

PREDICATES (fixed before first run). Each records qualifying / pass / fail; failures are kept.
P1  spinor Bloch map agrees with the note's maps H:(Z,-Y,X), D:((-X-3Y)/2,(X-Y)/2,Z) on every word
    of length <= 10; hypothesis per word: norm X^2+3Y^2+Z^2 = 1.
P2  reference words "",1010,101001,10100101 give v0..v3 of the note.
P3  for every distinct state reached at even t <= TMAX from R: a != 0 mod (1-w), b = 0 mod (1-w),
    residues (X,Z) mod 3 = (0,1). Odd t: residues (1,0). Hypothesis per state: coordinates are
    3-integral (true by construction, tested as integer-scaled).
P4  no state with a = 0 (opposite pole) at any t <= TMAX, even or odd.
P5  report min |a|^2 per even t; smallest even t with P(R)=|a|^2/2^t <= 1e-3; smallest even t with
    Bloch distance |s+z| <= 1e-3 (needs 2|a|^2/2^t <= 5e-7; lower bound t >= 22 because |a|^2 >= 1).
P6  barycentric identity: for every even word of length <= 10 (note reports <= 8): sum lambda = 1,
    sum lambda_i v_i = s, 9*2^d*lambda integral, two positive mixtures have equal barycentre, and
    rate difference equals [F(s) - sum lambda_i F(v_i)]/L for F ordinary, quadratic F2, cubic F3.
    Hypothesis per word: both sides are probability vectors (nonnegative, sum 1).
P7  example 1110: point (3/4,1/8,5/8), lambda (3/4,1/4,-1/2,1/2), slots [4,0,0,2,0] vs [0,3,1,0,2],
    F2 discrepancy 9/256, F3 discrepancy -81/512, ordinary 0.
P8  F2 is increasing on [-1,1], F2(1)=1, F2(-1)=0.
P9  L pole: lambda(-z) = (-1/3,4/9,4/9,4/9); slots 9 L + 3 R vs 4+4+4; 12 is the least common
    slot count for these weights.
P10 L_* = (7+2 sqrt13)/9: subset formula values as in the note; on every orbit point of even words
    <= 12 the multiplier L < L_* strictly (exact comparison), and the max found is reported.
P11 SU(2) trace of D * HDH representative equals 1/2 (exact in Q(w, sqrt of unit)): checked as
    |tr|^2/det = 1/4 on the U(2) matrices in Z[w].
P12 kernel ranks over F_p on polynomials of degree <= 8 restricted to the sphere (dim 81):
    (a) sixth-turn alternating sums, all axes: nullity expected 9 (degree <= 2);
    (b) same-axis triangle comparisons at arbitrary azimuth offsets: nullity expected 9;
    (c) quarter-turn square alternating sums: nullity expected 4 (degree <= 1);
    (d) (a) plus complement F(s)+F(-s)=const: nullity expected 4;
    (e) monomials of degree <= 2 are annihilated by (a),(b) rows; degree <= 1 by (c).
    Hypothesis per row: points lie on the sphere and the rotation is orthogonal mod p (tested).
P13 F2 invisible in same-axis triangle-azimuth tests: mean of F2 over triangle at random axis,
    latitude, two azimuths agree mod p (qualifying count reported).
P14 (expected to show visibility; kept either way) two EQUATORIAL triangles about different axes
    have the same barycentre 0; F2 means: axis z versus axis x, exact in Q.
P15 a response passing every native comparison and not squared amplitude: G = ordinary on dyadic
    (X,Y,Z), F2 elsewhere; all P6 tests pass for G; G differs at a non-dyadic point.
"""
import sys, json, random, hashlib
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from math import gcd

random.seed(81)
OUT = Path(sys.argv[1])
TMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 20
res = {}
def rec(name, qual, passed, failed, **extra):
    res[name] = dict(qualifying=qual, passed=passed, failed=failed, **{k: str(v) if isinstance(v, Q) else v for k, v in extra.items()})
    print(name, res[name], flush=True)

# ---- Z[w] arithmetic: element (u,v) = u + v w
def add(a, b): return (a[0]+b[0], a[1]+b[1])
def sub(a, b): return (a[0]-b[0], a[1]-b[1])
def mul(a, b):  # w^2 = -1 - w
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def conj(a): return (a[0]-a[1], -a[1])
def norm(a): return a[0]*a[0]-a[0]*a[1]+a[1]*a[1]
W = (0, 1)
def tick(sp, bit):
    a, b = sp
    a, b = add(a, b), sub(a, b)
    if bit == "1": b = mul(b, W)
    return (a, b)
def spinor(word, sp=((1, 0), (0, 0))):
    for c in word: sp = tick(sp, c)
    return sp
def bloch(sp, t):
    a, b = sp
    p, q = mul(conj(a), b)
    d = 2**t
    return (Q(2*p-q, d), Q(q, d), Q(norm(a)-norm(b), d))
def note_state(word, s=(Q(0), Q(0), Q(1))):
    x, y, z = s
    for c in word:
        x, y, z = z, -y, x
        if c == "1": x, y = (-x-3*y)/2, (x-y)/2
    return (x, y, z)

# P1
q = p_ = f = 0; fails = []
for n in range(0, 11):
    for bits in product("01", repeat=n):
        wd = "".join(bits); s = bloch(spinor(wd), n)
        if s[0]**2+3*s[1]**2+s[2]**2 != 1: continue
        q += 1
        if s == note_state(wd): p_ += 1
        else: f += 1; fails.append(wd)
rec("P1", q, p_, f, total=2**11-1, fails=fails[:10])

# P2
REFW = ["", "1010", "101001", "10100101"]
V = [bloch(spinor(wd), len(wd)) for wd in REFW]
exp = [(0, 0, 1), (0, Q(1, 2), -Q(1, 2)), (-Q(3, 4), -Q(1, 4), -Q(1, 2)), (Q(3, 4), -Q(1, 4), -Q(1, 2))]
ok = sum(tuple(v) == tuple(e) for v, e in zip(V, exp))
rec("P2", 4, ok, 4-ok, refs=[[str(c) for c in v] for v in V])

# P3-P5 BFS over distinct spinors modulo units (canonicalise by Bloch integer triple)
level = {(0, 0, 1): ((1, 0), (0, 0))}  # key Bloch scaled ints -> spinor
p3 = dict(q=0, p=0, f=0); p3odd = dict(q=0, p=0, f=0); pole = []; mins = {}; fails3 = []
first_prob = None; first_dist = None; counts = {}
for t in range(1, TMAX+1):
    nxt = {}
    for sp in level.values():
        for c in "01":
            a, b = tick(sp, c)
            pq = mul(conj(a), b)
            key = (2*pq[0]-pq[1], pq[1], norm(a)-norm(b))
            if key not in nxt: nxt[key] = (a, b)
    level = nxt; counts[t] = len(level)
    inv = 1 if t % 2 == 0 else 2  # (2^t)^-1 mod 3
    m = None
    for key, (a, b) in level.items():
        na = norm(a)
        if na == 0: pole.append((t, key))
        ra, rb = (a[0]+a[1]) % 3, (b[0]+b[1]) % 3   # residue mod (1-w)
        rx, rz = key[0]*inv % 3, key[2]*inv % 3
        if t % 2 == 0:
            p3["q"] += 1
            if ra != 0 and rb == 0 and (rx, rz) == (0, 1): p3["p"] += 1
            else: p3["f"] += 1; fails3.append((t, key))
            if m is None or na < m: m = na
        else:
            p3odd["q"] += 1
            if (rx, rz) == (1, 0): p3odd["p"] += 1
            else: p3odd["f"] += 1; fails3.append((t, key))
    if t % 2 == 0:
        mins[t] = m
        if first_prob is None and Q(m, 2**t) <= Q(1, 1000): first_prob = t
        if first_dist is None and Q(2*m, 2**t) <= Q(5, 10**7): first_dist = t
    print("t", t, "states", len(level), "min|a|^2", m, flush=True)
rec("P3_even", p3["q"], p3["p"], p3["f"], fails=fails3[:10], distinct_states_per_t=counts)
rec("P3_odd", p3odd["q"], p3odd["p"], p3odd["f"])
rec("P4", sum(counts.values()), sum(counts.values())-len(pole), len(pole), poles=pole[:10], TMAX=TMAX)
rec("P5", len(mins), len(mins), 0, min_norm_a_by_even_t=mins,
    min_PR_by_even_t={t: float(Q(m, 2**t)) for t, m in mins.items()},
    first_t_PR_le_0p001=first_prob, first_t_bloch_dist_le_0p001_within_TMAX=first_dist,
    lower_bound_t_for_bloch_dist_0p001=22)

# P6
def lam(s):
    X, Y, Z = s
    return ((1+2*Z)/3, (2-2*Z+12*Y)/9, (2-2*Z-6*X-6*Y)/9, (2-2*Z+6*X-6*Y)/9)
def F_ord(s): return (1+s[2])/2
def F2(s): return (1+s[2])/2 + (1-s[2]**2)/8
def F3(s): return (1+s[2]**3)/2
def dyadic(s): return all((c.denominator & (c.denominator-1)) == 0 for c in s)
def G(s): return F_ord(s) if dyadic(s) else F2(s)
q = p_ = f = 0; fails = []; maxdisc = {"F2": (Q(0), ""), "F3": (Q(0), "")}; zero_disc = {"F2": 0, "F3": 0}
gq = gp = 0; Lmax = (Q(0), ""); bylen = {}
for n in range(0, 11, 2):
    for bits in product("01", repeat=n):
        wd = "".join(bits); s = bloch(spinor(wd), n); l = lam(s)
        Npos = sum(max(-x, 0) for x in l); L = 1+Npos
        left = [Q(1)/L]+[max(-x, 0)/L for x in l]; right = [Q(0)]+[max(x, 0)/L for x in l]
        pts = [s]+V
        if not (all(x >= 0 for x in left+right) and sum(left) == 1 and sum(right) == 1): continue
        q += 1; bylen[n] = bylen.get(n, 0)+1
        good = sum(l) == 1 and all(sum(li*v[k] for li, v in zip(l, V)) == s[k] for k in range(3))
        good &= all((x*9*2**n).denominator == 1 for x in l)
        good &= all(sum(a*pt[k] for a, pt in zip(left, pts)) == sum(a*pt[k] for a, pt in zip(right, pts)) for k in range(3))
        for nm, F in (("ord", F_ord), ("F2", F2), ("F3", F3), ("G", G)):
            d = sum(a*F(pt) for a, pt in zip(left, pts))-sum(a*F(pt) for a, pt in zip(right, pts))
            good &= d == (F(s)-sum(li*F(v) for li, v in zip(l, V)))/L
            if nm in ("ord", "G"): good &= d == 0
            if nm == "G": gq += 1; gp += d == 0
            if nm in maxdisc:
                if abs(d) > abs(maxdisc[nm][0]): maxdisc[nm] = (d, wd)
                if d == 0: zero_disc[nm] += 1
        if L > Lmax[0]: Lmax = (L, wd)
        if good: p_ += 1
        else: f += 1; fails.append(wd)
rec("P6", q, p_, f, fails=fails[:10], words_by_length=bylen,
    max_abs_disc={k: [str(v[0]), v[1]] for k, v in maxdisc.items()},
    words_with_zero_disc_for_nonaffine_law=zero_disc, max_L=[str(Lmax[0]), Lmax[1]])

# P7
wd = "1110"; s = bloch(spinor(wd), 4); l = lam(s)
L = 1+sum(max(-x, 0) for x in l)
left = [Q(1)/L]+[max(-x, 0)/L for x in l]; right = [Q(0)]+[max(x, 0)/L for x in l]
slots = 1
for x in left+right: slots = slots*x.denominator//gcd(slots, x.denominator)
pts = [s]+V
d2 = sum(a*F2(pt) for a, pt in zip(left, pts))-sum(a*F2(pt) for a, pt in zip(right, pts))
d3 = sum(a*F3(pt) for a, pt in zip(left, pts))-sum(a*F3(pt) for a, pt in zip(right, pts))
d1 = sum(a*F_ord(pt) for a, pt in zip(left, pts))-sum(a*F_ord(pt) for a, pt in zip(right, pts))
checks = [s == (Q(3, 4), Q(1, 8), Q(5, 8)), l == (Q(3, 4), Q(1, 4), -Q(1, 2), Q(1, 2)), slots == 6,
          [int(x*6) for x in left] == [4, 0, 0, 2, 0], [int(x*6) for x in right] == [0, 3, 1, 0, 2],
          d2 == Q(9, 256), d3 == -Q(81, 512), d1 == 0,
          bloch(spinor(wd+"0000"), 8) == s]
rec("P7", len(checks), sum(checks), len(checks)-sum(checks), d2=d2, d3=d3, slots=slots, checks=checks)

# P8: F2' = 1/2 - z/4 > 0 on [-1,1] (linear, check ends), endpoints
checks = [Q(1, 2)-Q(1, 4) > 0, Q(1, 2)+Q(1, 4) > 0, F2((0, 0, Q(1))) == 1, F2((0, 0, Q(-1))) == 0,
          all(F2((0, 0, Q(k, 100))) < F2((0, 0, Q(k+1, 100))) for k in range(-100, 100))]
rec("P8", len(checks), sum(checks), len(checks)-sum(checks))

# P9
l = lam((Q(0), Q(0), Q(-1))); L = 1+sum(max(-x, 0) for x in l)
left = [Q(1)/L]+[max(-x, 0)/L for x in l]; right = [Q(0)]+[max(x, 0)/L for x in l]
slots = 1
for x in left+right: slots = slots*x.denominator//gcd(slots, x.denominator)
checks = [l == (-Q(1, 3), Q(4, 9), Q(4, 9), Q(4, 9)), slots == 12,
          [int(x*12) for x in left] == [9, 3, 0, 0, 0], [int(x*12) for x in right] == [0, 0, 4, 4, 4]]
rec("P9", len(checks), sum(checks), len(checks)-sum(checks), least_slots_for_these_weights=slots)

# P10: L < L_* <=> 9L-7 < 2 sqrt13 <=> (9L-7 <= 0) or (9L-7)^2 < 52
q = p_ = f = 0; best = (Q(0), ""); seen = set()
lev = {(0, 0, 1): ((1, 0), (0, 0))}
for t in range(1, 13):
    nx = {}
    for sp in lev.values():
        for c in "01":
            a, b = tick(sp, c); pq = mul(conj(a), b)
            nx.setdefault((2*pq[0]-pq[1], pq[1], norm(a)-norm(b)), (a, b))
    lev = nx
    if t % 2: continue
    for key in lev:
        s = tuple(Q(k, 2**t) for k in key)
        if s in seen: continue
        seen.add(s); l = lam(s); L = 1+sum(max(-x, 0) for x in l)
        q += 1; r = 9*L-7
        if r <= 0 or r*r < 52: p_ += 1
        else: f += 1
        if L > best[0]: best = (L, t)
subrec = {}
cf = [(Q(1, 3), 0, 0, Q(2, 3)), (Q(2, 9), 0, Q(4, 3), -Q(2, 9)), (Q(2, 9), -Q(2, 3), -Q(2, 3), -Q(2, 9)), (Q(2, 9), Q(2, 3), -Q(2, 3), -Q(2, 9))]
def subval(J):  # returns (c, |w|^2): max of -(sum) on sphere = |w| - c
    c, x, y, z = [sum(cf[i][k] for i in J) for k in range(4)]
    return (c, x*x+Q(y*y)/3+z*z)
exp10 = {(1,): (Q(2, 9), Q(52, 81)), (0,): (Q(1, 3), Q(4, 9)), (2, 3): (Q(4, 9), Q(64, 81)),
         (0, 1): (Q(5, 9), Q(64, 81)), (1, 2, 3): (Q(2, 3), Q(4, 9)), (0, 2, 3): (Q(7, 9), Q(52, 81))}
okc = sum(subval(J) == e for J, e in exp10.items())
rec("P10", q, p_, f, distinct_orbit_points_even_t_le_12=q, max_L_on_orbit=float(best[0]), at_t=best[1],
    L_star=(7+2*13**0.5)/9, subset_values_ok=f"{okc}/6")

# P11: U = D * (H D H) unnormalised in Z[w]: H' = [[1,1],[1,-1]] (factor 1/2 total for two H)
def mmul(A, B): return [[add(mul(A[i][0], B[0][j]), mul(A[i][1], B[1][j])) for j in range(2)] for i in range(2)]
Hm = [[(1, 0), (1, 0)], [(1, 0), (-1, 0)]]; Dm = [[(1, 0), (0, 0)], [(0, 0), W]]
U = mmul(Dm, mmul(Hm, mmul(Dm, Hm)))
tr = add(U[0][0], U[1][1]); det = sub(mul(U[0][0], U[1][1]), mul(U[0][1], U[1][0]))
# SU(2) trace^2 = tr^2/det ; compare with 1/4: 4 tr^2 == det
lhs = mul((4, 0), mul(tr, tr))
rec("P11", 1, int(lhs == det), int(lhs != det), tr=tr, det=det)

# ---- P12/P13 over F_p
def is_prime(n):
    if n < 2: return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % sp == 0: return n == sp
    d, r = n-1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n-1): continue
        for _ in range(r-1):
            x = x*x % n
            if x == n-1: break
        else: return False
    return True
P = 10**18
while True:
    P += 1
    if P % 12 == 11 and is_prime(P): break
R3 = pow(3, (P+1)//4, P); assert R3*R3 % P == 3
inv = lambda a: pow(a, P-2, P)
def rnd_sphere():
    while True:
        u, v = random.randrange(P), random.randrange(P); d = (u*u+v*v+1) % P
        if d: i = inv(d); return (2*u*i % P, 2*v*i % P, (u*u+v*v-1)*i % P)
def rot(n, c, s):  # Rodrigues
    x, y, z = n; C = (1-c) % P
    return [[(c+x*x*C) % P, (x*y*C-z*s) % P, (x*z*C+y*s) % P],
            [(y*x*C+z*s) % P, (c+y*y*C) % P, (y*z*C-x*s) % P],
            [(z*x*C-y*s) % P, (z*y*C+x*s) % P, (c+z*z*C) % P]]
def app(M, v): return tuple(sum(M[i][j]*v[j] for j in range(3)) % P for i in range(3))
def orth(M): return all(sum(M[i][k]*M[j][k] for k in range(3)) % P == (i == j) for i in range(3) for j in range(3))
def onsph(v): return sum(c*c for c in v) % P == 1
MON = [(a, b, c) for c in (0, 1) for a in range(9) for b in range(9) if a+b+c <= 8]
assert len(MON) == 81
def ev(v): return [pow(v[0], a, P)*pow(v[1], b, P)*pow(v[2], c, P) % P for a, b, c in MON]
def rank(rows):
    rows = [r[:] for r in rows]; rk = 0; ncol = len(rows[0])
    for col in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][col]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; iv = inv(rows[rk][col])
        rows[rk] = [x*iv % P for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][col]:
                m = rows[i][col]; rows[i] = [(x-m*y) % P for x, y in zip(rows[i], rows[rk])]
        rk += 1
    return rk
half = inv(2); S60 = R3*half % P; C120 = (-half) % P; S120 = S60
def rnd_angle():
    while True:
        t = random.randrange(P); d = (1+t*t) % P
        if d: i = inv(d); return ((1-t*t)*i % P, 2*t*i % P)
NR = 140
rowsA, rowsB, rowsC, rowsD = [], [], [], []; qa = qb = qc = 0
for _ in range(NR):
    n = rnd_sphere(); s = rnd_sphere()
    M = rot(n, half, S60)
    if onsph(n) and onsph(s) and orth(M):
        qa += 1; v = s; r = [0]*81
        for j in range(6):
            e = ev(v); sg = 1 if j % 2 == 0 else -1
            r = [(x+sg*y) % P for x, y in zip(r, e)]; v = app(M, v)
        assert v == s
        rowsA.append(r)
    M3 = rot(n, C120, S120); c, sn = rnd_angle(); Mo = rot(n, c, sn)
    if onsph(n) and onsph(s) and orth(M3) and orth(Mo) and (c*c+sn*sn) % P == 1:
        qb += 1; v = s; u = app(Mo, s); r = [0]*81
        for j in range(3):
            r = [(x+y-z) % P for x, y, z in zip(r, ev(v), ev(u))]; v = app(M3, v); u = app(M3, u)
        rowsB.append(r)
    M4 = rot(n, 0, 1)
    if onsph(n) and onsph(s) and orth(M4):
        qc += 1; v = s; r = [0]*81
        for j in range(4):
            e = ev(v); sg = 1 if j % 2 == 0 else -1
            r = [(x+sg*y) % P for x, y in zip(r, e)]; v = app(M4, v)
        rowsC.append(r)
    s1, s2 = rnd_sphere(), rnd_sphere()   # complement: F(s1)+F(-s1) - F(s2)-F(-s2) = 0
    neg = lambda v: tuple((-c) % P for c in v)
    rowsD.append([(a+b-c-d) % P for a, b, c, d in zip(ev(s1), ev(neg(s1)), ev(s2), ev(neg(s2)))])
ra, rb, rc, rd = rank(rowsA), rank(rowsB), rank(rowsC), rank(rowsA+rowsD)
low2 = [i for i, m in enumerate(MON) if sum(m) <= 2]; low1 = [i for i, m in enumerate(MON) if sum(m) <= 1]
# degree<=2 restricted to sphere: monomials deg<=2 with c<=1 span 9 dims (z^2 = 1-x^2-y^2)
annA = all(r[i] == 0 for r in rowsA for i in low2); annB = all(r[i] == 0 for r in rowsB for i in low2)
annC = all(r[i] == 0 for r in rowsC for i in low1); annC2 = all(r[i] == 0 for r in rowsC for i in low2)
exp12 = dict(a=9, b=9, c=4, d=4); got = dict(a=81-ra, b=81-rb, c=81-rc, d=81-rd)
checks = [got[k] == exp12[k] for k in "abcd"]+[len(low2) == 9, annA, annB, annC, not annC2]
rec("P12", dict(a=qa, b=qb, c=qc, rows_each=NR), sum(checks), len(checks)-sum(checks), prime=P, nullity=got,
    expected=exp12, deg_le2_annihilated_by_sixth_turn=annA, deg_le2_annihilated_by_triangle_azimuth=annB,
    deg_le1_annihilated_by_squares=annC, deg_le2_annihilated_by_squares=annC2,
    field="F_p, random F_p points; rank at a specialisation is a lower bound for the generic rank, and deg<=2 annihilation is an upper bound, so nullity 9 is exact for the family")

# P13
def F2p(v): return ((1+v[2])*half+(1-v[2]*v[2])*inv(8)) % P
def F3p(v): return ((1+pow(v[2], 3, P))*half) % P
q = p_ = f = 0; f3diff = 0
for _ in range(500):
    n = rnd_sphere(); s = rnd_sphere(); M3 = rot(n, C120, S120); c, sn = rnd_angle(); Mo = rot(n, c, sn)
    if not (orth(M3) and orth(Mo)): continue
    q += 1; v = s; u = app(Mo, s); d = 0; d3 = 0
    for j in range(3):
        d = (d+F2p(v)-F2p(u)) % P; d3 = (d3+F3p(v)-F3p(u)) % P; v = app(M3, v); u = app(M3, u)
    if d == 0: p_ += 1
    else: f += 1
    f3diff += d3 != 0
rec("P13", q, p_, f, cubic_law_visible_in_same_tests=f3diff)

# P14: equatorial triangle about z: points (cos,sin,0): z=0 -> F2 = 1/2+1/8 each. About x: points (0,cos th,sin th),
# th = 90,210,330 deg: z = 1, -1/2, -1/2 (rational choice of azimuth).
mz = Q(1, 2)+Q(1, 8)
mx = sum(F2((0, 0, Q(z))) for z in (Q(1), -Q(1, 2), -Q(1, 2)))/3
rec("P14", 1, int(mz == mx), int(mz != mx), mean_axis_z=mz, mean_axis_x=mx, difference=mz-mx,
    note="both triangles have barycentre 0; a nonzero difference means F2 IS visible to equal-barycentre triangle pairs with different axes")

# P15
pt = (Q(0), Q(0), Q(1, 3))
rec("P15", gq, gp, gq-gp, G_at_nondyadic_Z_1_3=G(pt), ordinary=F_ord(pt), differs=G(pt) != F_ord(pt))

with OUT.open("x", encoding="utf8", newline="\n") as fh:
    json.dump(res, fh, indent=1, sort_keys=True, default=str); fh.write("\n")
anyfail = [k for k, v in res.items() if v["failed"]]
print("FAILED PREDICATES:", anyfail)
sys.exit(1 if [k for k in anyfail if k != "P14"] else 0)
