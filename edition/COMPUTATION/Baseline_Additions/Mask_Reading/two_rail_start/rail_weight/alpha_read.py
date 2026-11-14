"""Is |alpha|^2 readable from a two-rail start?  Claim (director, by hand, 14 Nov 2026):
for N >= 3, any abelian gains, chi unitary with chi(H) = -1, start alpha|0,R> + beta|0,L>,
the UNMASKED port (tick 3, site 1 mod N, rail R) has probability exactly |alpha|^2 / 2,
and the port (tick 3, site -1 mod N, rail L) has probability exactly |beta|^2 / 2.

Predicates, fixed before the first run:
 P1  for every qualifying case, P(3, 1, R) == |alpha|^2/2 exactly.
 P2  for every qualifying case, P(3, -1, L) == |beta|^2/2 exactly.
 C1  (control, expected to FAIL as a universal statement) the same with chi(H) = +1.
Hypothesis tested per case: chi(H) == -1 (C1: chi(H) == +1); count of qualifying cases reported.
Conventions: start site 0; R step to (x+1,R), L step to (x-1,L); arc gain named (previous rail, new rail):
RR=a, RL=b, LR=c, LL=d; amplitude of a word = chi(product of arc gains) / 2^(t/2); characters take values in
the 4th roots of unity (group Z/4 exponents), so arithmetic is exact in Gaussian rationals. Seed 20261114.
Usage: python3 alpha_read.py RESULT.json   (refuses to overwrite)."""
import sys, json, random, itertools
from fractions import Fraction as Fr
out = sys.argv[1]
f = open(out, "x")
class G:  # Gaussian rational
    def __init__(s, re, im=0): s.re, s.im = Fr(re), Fr(im)
    def __add__(s, o): return G(s.re+o.re, s.im+o.im)
    def __mul__(s, o): return G(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    def n2(s): return s.re*s.re + s.im*s.im
I4 = [G(1), G(0,1), G(-1), G(0,-1)]
random.seed(20261114)
starts = [(G(Fr(3,5)), G(0, Fr(4,5))), (G(Fr(5,13)), G(Fr(12,13))), (G(1), G(0)), (G(0), G(1)),
          (G(Fr(3,5)*Fr(3,5), Fr(3,5)*Fr(4,5)), G(Fr(4,5)))]
res = {"P1": [0,0], "P2": [0,0], "C1": [0,0], "qual_eta_minus": 0, "qual_eta_plus": 0, "drawn": 0, "fails": []}
def prob(N, ea, eb, ec, ed, al, be, tick, site, rail):
    amp = G(0)
    for r0, c0 in ((0, al), (1, be)):           # 0 = R, 1 = L
        for w in itertools.product((0,1), repeat=tick):
            x, prev, e = 0, r0, 0
            for s in w:
                e += [[ea, eb], [ec, ed]][prev][s]
                x += 1 if s == 0 else -1
                prev = s
            if x % N == site % N and prev == rail:
                amp = amp + c0 * I4[e % 4]
    return amp.n2() / 2**tick
for _ in range(4000):
    res["drawn"] += 1
    N = random.randint(3, 9)
    ea, eb, ec, ed = (random.randrange(4) for _ in range(4))
    eta = (ea + ed - eb - ec) % 4               # exponent of chi(H); chi(H) = i^eta
    al, be = random.choice(starts)
    pR = prob(N, ea, eb, ec, ed, al, be, 3, 1, 0)
    pL = prob(N, ea, eb, ec, ed, al, be, 3, -1, 1)
    if eta == 2:
        res["qual_eta_minus"] += 1
        for k, got, want in (("P1", pR, al.n2()/2), ("P2", pL, be.n2()/2)):
            ok = got == want
            res[k][0 if ok else 1] += 1
            if not ok: res["fails"].append([k, N, ea, eb, ec, ed, str(got), str(want)])
    elif eta == 0:
        res["qual_eta_plus"] += 1
        ok = pR == al.n2()/2
        res["C1"][0 if ok else 1] += 1
json.dump(res, f, indent=1, sort_keys=True); f.close()
print(json.dumps({k: res[k] for k in ("drawn", "qual_eta_minus", "qual_eta_plus", "P1", "P2", "C1")}))
sys.exit(1 if res["P1"][1] or res["P2"][1] else 0)
