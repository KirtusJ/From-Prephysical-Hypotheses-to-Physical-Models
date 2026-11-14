"""chal.py - challenger program for CRITERION.md (Character_Separation). Own program, from the definitions only.
Conventions: start (0,R); R step -> (x+1,R); L step -> (x-1,L); arc gains by (previous rail,new rail): RR=a RL=b
LR=c LL=d; ticks numbered 1..t; mask S_j = wells retained after step j; P(port) = 2^-t |sum chi(G(w))|^2.
Groups: products of cyclic groups, written additively; chi_r(x) = exp(2 pi i sum r_i x_i/n_i); all values are
M-th roots of unity (M = lcm), amplitudes are exact elements of Z[x]/(Phi_M). No floating point anywhere.
Seed 20261114. Result file chal_result.json; refuses to overwrite.

PREDICATES (fixed before the first run)
C0  control: brute enumeration of the 256 words, N=7, a=c=1,b=g,d=zg in C2xC3, chi(z)=-1, chi(g)=1, fork of
    length 8, port (1,R): record value (known answer exists; also record chi(g)=w and the L rail).
I1  identity (1) G(w)=a^t (a/c)^e B^l H^m for every word of length <= 10 on 40 random carriers.
A1  Prop 1, eta=-1: random abelian carriers (1-3 cyclic factors, random gains incl. a,c nontrivial), N in 1..9,
    every pair of characters with chi(H)=-1 for both and omega_1 = omega_0^(+-1): every port and well of 12
    random events (length 1..min(2D+3,14)) plus the unmasked event agree. Hypothesis tested per carrier.
A1b same with eta=+1.
A1c Remark: eta not real, (eta,omega) equal or jointly conjugate: agree.
A1d POWER (expected to find separations): eta equal and not real, omega_1 = conj omega_0 != omega_0.
A1e Prop 2(b),(c) "if": every eta=-1 pair with Re omega different, N>=3: fork well probabilities differ, and
    fork value = 2^-(D+1)(2+2(-1)^(D-1) Re omega) for every eta=-1 character.
A2  Prop 2(a)/(c) minimality, complete for all mask events: N=1..14, every t<=D, every port (x,rail): all 2^t
    words ending there have the same left count l. (With I1 this gives: no event of length <= D separates.)
A2b direct: random carriers, events of length <= D, all eta=-1 pairs (any omega): all ports and wells agree.
A3  fork: admitted words are exactly R^(D+1), L^D R for N=3..14 (brute). N=1,2: record admitted words and the
    fork well probability; N<=2: every well probability of random events is 0 or 1 (eta=-1); port (2,2 mod N,R)
    unmasked = (1+Re beta)/2.
A4  summary (iii): two DIFFERENT carriers (different groups, gains), chi(H)=chi'(H)=-1, chi(B)=chi'(B)^(+-1):
    all ports and wells of random events agree. A4w: same with only omega equal up to conjugation.
A4s SCOPE (outside the stated class, expected to separate): start in equal superposition of rails R and L at
    site 0, two carriers with equal chi(B), chi(H)=-1, different chi(c/a): port (1,1,R).
A5  Prop 3(b), exact in roots of unity of order 2 D1 D2: for (D1,D2) in (2,3),(3,5),(4,6),(2,2) and all
    2<=D1,D2<=12, every eta!=1, tau!=1, both roots beta: Re agree for D1 and D2, beta' not beta, not conj beta.
A5a Prop 3(a): among K-th roots, K=1..120, no non-conjugate pair agrees on D=2,3,5.
A5c Prop 3(c): q<=60, gcd(D,q)=1, D<=12: agreement implies equal or conjugate.
A6  corollary note's group: chi_0 vs chi_1 fork-separated iff 3 does not divide N (N=3..14); chi_1 vs chi_2 never;
    N=1,2 via the port of Prop 2(d).
"""
import sys, os, json, random, itertools, math
from fractions import Fraction
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chal_result.json")
if os.path.exists(OUT):
    print("refuse: result exists"); sys.exit(3)
random.seed(20261114)
res = {}; fails = []

# ---- exact cyclotomic arithmetic
def pdiv(num, den):
    num = num[:]; q = [0]*(len(num)-len(den)+1)
    for i in range(len(num)-len(den), -1, -1):
        c = num[i+len(den)-1]; q[i] = c
        if c:
            for j, dj in enumerate(den): num[i+j] -= c*dj
    return q, num[:len(den)-1]
_phi = {}
def phi(n):
    if n in _phi: return _phi[n]
    p = [-1]+[0]*(n-1)+[1]
    for d in range(1, n):
        if n % d == 0:
            p, r = pdiv(p, phi(d)); assert not any(r)
    _phi[n] = p; return p
def red(v, M):
    """canonical form of sum v[j] zeta^j in Z[zeta_M]"""
    v = list(v); ph = phi(M)
    if len(v) < len(ph): return tuple(v + [0]*(len(ph)-1-len(v)))
    return tuple(pdiv(v, ph)[1])
def roll(v, e, M): e %= M; return v[-e:]+v[:-e] if e else v
def add(u, v): return [x+y for x, y in zip(u, v)]
def normsq(v, M):
    o = [0]*M
    nz = [(j, x) for j, x in enumerate(v) if x]
    for j, x in nz:
        for k, y in nz: o[(j-k) % M] += x*y
    return red(o, M)
def tadd(u, v): return tuple(x+y for x, y in zip(u, v))

# ---- carriers
def lcm(a, b): return a*b//math.gcd(a, b)
class Car:
    def __init__(s, orders, a, b, c, d):
        s.o = orders; s.a, s.b, s.c, s.d = a, b, c, d
        s.M = 1
        for n in orders: s.M = lcm(s.M, n)
    def ex(s, r, x, M): return sum(ri*xi*(M//n) for ri, xi, n in zip(r, x, s.o)) % M
    def comb(s, *terms):
        return tuple(sum(k*x[i] for k, x in terms) % n for i, n in enumerate(s.o))
    def B(s): return s.comb((1, s.b), (1, s.c), (-2, s.a))
    def H(s): return s.comb((1, s.a), (1, s.d), (-1, s.b), (-1, s.c))
    def chars(s): return list(itertools.product(*[range(n) for n in s.o]))
    def gains(s, r, M): return [s.ex(r, g, M) for g in (s.a, s.b, s.c, s.d)]
def randcar():
    orders = tuple(random.choice([2, 2, 3, 4, 4, 6, 8, 5]) for _ in range(random.randint(1, 3)))
    g = lambda: tuple(random.randrange(n) for n in orders)
    return Car(orders, g(), g(), g(), g())

def run(N, masks, ge, M, start=None):
    """ge = exponents (a,b,c,d). returns dict (x,rail)->amplitude vector after len(masks) ticks. rail 0=R,1=L"""
    ea, eb, ec, ed = ge; one = [1]+[0]*(M-1)
    amp = start if start else {(0, 0): one}
    for S in masks:
        new = {}
        for (x, r), v in amp.items():
            y = (x+1) % N
            if S is None or y in S:
                w = roll(v, ea if r == 0 else ec, M); k = (y, 0)
                new[k] = add(new[k], w) if k in new else w
            y = (x-1) % N
            if S is None or y in S:
                w = roll(v, eb if r == 0 else ed, M); k = (y, 1)
                new[k] = add(new[k], w) if k in new else w
        amp = new
    return amp
def probs(N, masks, ge, M, start=None):
    amp = run(N, masks, ge, M, start); out = {}
    zero = red([0]*M, M)
    for x in range(N):
        p = [normsq(amp[(x, r)], M) if (x, r) in amp else zero for r in (0, 1)]
        out[(x, 0)] = p[0]; out[(x, 1)] = p[1]; out[(x, 'w')] = tadd(p[0], p[1])
    return out
def Dof(N): return N//math.gcd(N, 2)
def randevent(N, t, keep=0.75):
    ms = []
    for _ in range(t):
        if random.random() < 0.25: ms.append(None); continue
        S = frozenset(x for x in range(N) if random.random() < keep) or frozenset([random.randrange(N)])
        ms.append(S)
    return ms
def fork(N):
    D = Dof(N)
    return [frozenset([j % N, (-j) % N]) for j in range(1, D)] + [frozenset([D % N]), frozenset([(D+1) % N])]
def words(t): return itertools.product((0, 1), repeat=t)   # 0=R step, 1=L step
def wordinfo(w, N):
    x = 0; r = 0; l = 0; m = 0; path = []; arcs = []
    for s in w:
        arcs.append((r, s))
        if s: 
            x -= 1; l += 1; m += (r == 1)
        else: x += 1
        r = s; path.append(x % N if N else x)
    return path, r, l, m, arcs
def tofrac(v, t):
    assert not any(v[1:]), v
    return str(Fraction(v[0], 2**t))

# ---- C0 control (brute words, individual arc gains)
def brute_fork(N, car, r, rail):
    M = car.M; ge = car.gains(r, M); F = fork(N); t = len(F); tot = [0]*M; adm = []
    for w in words(t):
        path, fr, l, m, arcs = wordinfo(w, N)
        if all(path[j] in F[j] for j in range(t)) and fr == rail:
            e = sum(ge[2*p+s] for p, s in arcs) % M; tot[e] += 1; adm.append(''.join('RL'[s] for s in w))
    return normsq(tot, M), t, adm
note = Car((2, 3), (0, 0), (0, 1), (0, 0), (1, 1))
c0 = {}
for r in ((1, 0), (1, 1), (1, 2)):
    for rail in (0, 1):
        v, t, adm = brute_fork(7, note, r, rail)
        c0["chi(g)=w^%d rail %s" % (r[1], 'RL'[rail])] = {"P": tofrac(v, t), "admitted": adm}
res["C0"] = c0
print("C0", c0)

# ---- I1 identity
bad = 0; n = 0
for _ in range(40):
    car = randcar()
    for t in range(1, 11):
        for w in words(t):
            path, fr, l, m, arcs = wordinfo(w, 0); n += 1
            G = car.comb(*[(1, (car.a, car.b, car.c, car.d)[2*p+s]) for p, s in arcs])
            F = car.comb((t, car.a), (fr, car.a), (-fr, car.c), (l, car.B()), (m, car.H()))
            bad += (G != F)
res["I1"] = {"words_checked": n, "fail": bad}
if bad: fails.append("I1")
print("I1", res["I1"])

# ---- A1 family
st = {k: {"carriers": 0, "qual_carriers": 0, "qual_noncyclic": 0, "qual_ac_nontrivial": 0, "pairs": 0,
          "events": 0, "nonzero_events": 0, "comparisons": 0, "mismatch": 0, "examples": []}
      for k in ("A1", "A1b", "A1c", "A1d")}
a1e = {"chars": 0, "formula_fail": 0, "pairs_diff_Re": 0, "fork_not_separating": 0, "examples": []}
a2b = {"carriers_with_pair": 0, "pairs": 0, "events": 0, "comparisons": 0, "mismatch": 0, "examples": []}
def cmp_events(N, evs, geA, geB, M, stt, tag):
    for ms in evs:
        pa = probs(N, ms, geA, M); pb = probs(N, ms, geB, M)
        stt["events"] += 1
        if "nonzero_events" in stt: stt["nonzero_events"] += any(any(v) for v in pa.values())
        for k in pa:
            stt["comparisons"] += 1
            if pa[k] != pb[k]:
                stt["mismatch"] += 1
                if len(stt["examples"]) < 3:
                    stt["examples"].append({"tag": tag, "N": N, "masks": [sorted(S) if S else None for S in ms],
                                            "port": str(k), "PA": pa[k], "PB": pb[k]})
for it in range(700):
    car = randcar(); N = random.randint(1, 9); D = Dof(N); M = car.M
    ch = car.chars(); Bv, Hv = car.B(), car.H()
    info = [(r, car.ex(r, Hv, M), (D*car.ex(r, Bv, M)) % M) for r in ch]
    evs = [randevent(N, random.randint(1, min(2*D+3, 14))) for _ in range(12)] + [[None]*min(2*D+3, 12)]
    short = [randevent(N, random.randint(1, D), 0.85) for _ in range(6)] + [[None]*D]
    q = {k: 0 for k in st}
    for k in st: st[k]["carriers"] += 1
    ac = any(car.a) or any(car.c); nonc = sum(1 for n_ in car.o if n_ > 1) > 1 and \
        not all(math.gcd(x, y) == 1 for x, y in itertools.combinations(car.o, 2))
    npair = 0
    minus = [x for x in info if 2*x[1] % M == 0 and x[1] != 0] if M % 2 == 0 else []
    for (r0, h0, w0), (r1, h1, w1) in itertools.combinations(info, 2):
        real = (2*h0) % M == 0
        key = None
        if h0 == h1 and real and (w1 == w0 or (w1+w0) % M == 0): key = "A1" if h0 else "A1b"
        elif not real and ((h0 == h1 and w0 == w1) or ((h0+h1) % M == 0 and (w0+w1) % M == 0)): key = "A1c"
        elif not real and h0 == h1 and (w0+w1) % M == 0 and w0 != w1: key = "A1d"
        if key is None: continue
        if q[key] >= 4: continue          # cap pairs per carrier per predicate (affordability)
        q[key] += 1; st[key]["pairs"] += 1
        cmp_events(N, evs, car.gains(r0, M), car.gains(r1, M), M, st[key], "%s %s %s" % (car.o, (car.a, car.b, car.c, car.d), (r0, r1)))
    for k in st:
        if q[k]:
            st[k]["qual_carriers"] += 1; st[k]["qual_noncyclic"] += nonc; st[k]["qual_ac_nontrivial"] += ac
    # A1e and A2b on eta=-1 characters
    if minus:
        if N >= 3:
            F = fork(N); x = (D+1) % N; s = (-1)**(D-1); fp = {}
            for (r, h, w) in minus[:8]:
                p = probs(N, F, car.gains(r, M), M); a1e["chars"] += 1
                v = [0]*M; v[0] += 2; v[w % M] += s; v[(-w) % M] += s
                fp[r] = (p[(x, 'w')], w)
                if p[(x, 'w')] != red(v, M) or p[(x, 0)] != red(v, M):
                    a1e["formula_fail"] += 1
                    if len(a1e["examples"]) < 3: a1e["examples"].append(["formula", car.o, N, r])
            for (r0, (p0, w0)), (r1, (p1, w1)) in itertools.combinations(fp.items(), 2):
                if w0 == w1 or (w0+w1) % M == 0: continue
                a1e["pairs_diff_Re"] += 1
                if p0 == p1:
                    a1e["fork_not_separating"] += 1
                    if len(a1e["examples"]) < 3: a1e["examples"].append(["nosep", car.o, N, r0, r1])
        if len(minus) >= 2:
            a2b["carriers_with_pair"] += 1
            for (r0, _, _), (r1, _, _) in list(itertools.combinations(minus, 2))[:4]:
                a2b["pairs"] += 1
                cmp_events(N, short, car.gains(r0, M), car.gains(r1, M), M, a2b, "%s N=%d" % (car.o, N))
for k in ("A1", "A1b", "A1c"):
    if st[k]["mismatch"]: fails.append(k)
if st["A1d"]["mismatch"] == 0: fails.append("A1d(no power)")
if a1e["formula_fail"] or a1e["fork_not_separating"]: fails.append("A1e")
if a2b["mismatch"]: fails.append("A2b")
res.update(st); res["A1e"] = a1e; res["A2b"] = a2b
for k in st: print(k, {x: y for x, y in st[k].items() if x != "examples"})
print("A1e", a1e); print("A2b", {x: y for x, y in a2b.items() if x != "examples"})

# ---- A2 complete: unique l per port for t <= D
a2 = {"ports_checked": 0, "violations": [], "N_range": [1, 14], "control_t_eq_D_plus_1_ports_with_two_l": {}}
for N in range(1, 15):
    D = Dof(N)
    for t in range(1, D+2):
        seen = {}
        for w in words(t):
            path, fr, l, m, arcs = wordinfo(w, N)
            seen.setdefault((path[-1], fr), set()).add(l)
        if t <= D:
            a2["ports_checked"] += len(seen)
            for k, v in seen.items():
                if len(v) > 1: a2["violations"].append([N, t, k, sorted(v)])
        else:
            a2["control_t_eq_D_plus_1_ports_with_two_l"][N] = sum(len(v) > 1 for v in seen.values())
res["A2"] = a2
if a2["violations"]: fails.append("A2")
print("A2", a2)

# ---- A3 fork words, small N
a3 = {"fork_words": {}, "fail": []}
for N in range(1, 15):
    D = Dof(N); F = fork(N); adm = []
    for w in words(D+1):
        path, fr, l, m, arcs = wordinfo(w, N)
        if all(path[j] in F[j] for j in range(D+1)): adm.append(''.join('RL'[s] for s in w))
    a3["fork_words"][N] = adm if N < 5 else len(adm)
    if N >= 3 and sorted(adm) != sorted(['R'*(D+1), 'L'*D+'R']): a3["fail"].append(["words", N, adm])
small = {"carriers_qual": 0, "well_values_seen": {}, "well_not_0_1": 0, "port_fail": 0, "fork_well_N12": {}}
for it in range(200):
    car = randcar(); M = car.M; Bv, Hv = car.B(), car.H()
    minus = [r for r in car.chars() if M % 2 == 0 and car.ex(r, Hv, M) == M//2]
    if not minus: continue
    small["carriers_qual"] += 1
    for N in (1, 2):
        for r in minus[:4]:
            ge = car.gains(r, M); be = car.ex(r, Bv, M)
            for ms in [randevent(N, random.randint(1, 7), 0.6) for _ in range(5)] + [fork(N)]:
                p = probs(N, ms, ge, M); t = len(ms)
                for x in range(N):
                    v = p[(x, 'w')]
                    if any(v[1:]) or v[0] not in (0, 2**t): small["well_not_0_1"] += 1
                    else: small["well_values_seen"][str(v[0]//2**t if v[0] else 0)] = small["well_values_seen"].get(str(v[0]//2**t if v[0] else 0), 0)+1
                if ms == fork(N): small["fork_well_N12"][N] = tofrac(p[(2 % N, 'w')], t)
            p = probs(N, [None, None], ge, M)
            v = [0]*M; v[0] += 2; v[be] += 1; v[-be % M] += 1      # 4P = |1+beta|^2 = 2 + 2 Re beta
            if p[(2 % N, 0)] != red(v, M): small["port_fail"] += 1
a3["N_le_2"] = small
if a3["fail"] or small["well_not_0_1"] or small["port_fail"]: fails.append("A3")
res["A3"] = a3; print("A3", a3)

# ---- A4 two different carriers
a4 = {k: {"tried": 0, "qual_pairs": 0, "diff_group": 0, "comparisons": 0, "events": 0, "mismatch": 0, "examples": []} for k in ("A4", "A4w")}
for it in range(4000):
    c1, c2 = randcar(), randcar(); M = lcm(c1.M, c2.M); N = random.randint(1, 9); D = Dof(N)
    if M > 48: continue
    r1 = random.choice(c1.chars()); r2 = random.choice(c2.chars())
    for k in a4: a4[k]["tried"] += 1
    if M % 2 or c1.ex(r1, c1.H(), M) != M//2 or c2.ex(r2, c2.H(), M) != M//2: continue
    b1, b2 = c1.ex(r1, c1.B(), M), c2.ex(r2, c2.B(), M)
    if b1 == b2 or (b1+b2) % M == 0: key = "A4"
    elif (D*(b1-b2)) % M == 0 or (D*(b1+b2)) % M == 0: key = "A4w"
    else: continue
    a4[key]["qual_pairs"] += 1; a4[key]["diff_group"] += (c1.o != c2.o)
    evs = [randevent(N, random.randint(1, min(2*D+3, 14))) for _ in range(8)] + [[None]*min(2*D+3, 12)]
    cmp_events(N, evs, c1.gains(r1, M), c2.gains(r2, M), M, a4[key], "%s/%s" % (c1.o, c2.o))
for k in a4:
    if a4[k]["mismatch"]: fails.append(k)
    print(k, {x: y for x, y in a4[k].items() if x != "examples"})
res.update(a4)
# A4s scope: superposed start
M = 4; cA = Car((2, 4), (0, 0), (0, 1), (0, 0), (1, 1)); cB = Car((2, 4), (0, 0), (0, 0), (0, 1), (1, 1)); r = (1, 1)
assert cA.B() == cB.B() and cA.H() == cB.H() == (1, 0)
one = [1, 0, 0, 0]
sA = probs(5, [None], cA.gains(r, M), M, {(0, 0): one, (0, 1): one})[(1, 0)]
sB = probs(5, [None], cB.gains(r, M), M, {(0, 0): one, (0, 1): one})[(1, 0)]
shA = probs(5, [None]*6, cA.gains(r, M), M); shB = probs(5, [None]*6, cB.gains(r, M), M)
res["A4s"] = {"superposed_start_port_(1,1,R)_numerators_over_4": [sA, sB], "separates": sA != sB,
              "same_carriers_sharp_start_agree": shA == shB,
              "note": "outside the stated setting (Start (0,R)); kept as scope marker, not a defect"}
print("A4s", res["A4s"])

# ---- A5 Prop 3 exact
a5 = {"cases": 0, "fail": [], "named": {}}
for D1 in range(2, 13):
    for D2 in range(2, 13):
        K = 2*D1*D2
        for i in range(1, D1):
            for j in range(1, D2):
                eta = 2*D2*i; tau = 2*D1*j; h = ((tau-eta) % K)//2
                for beta in (h, (h+K//2) % K):
                    bp = (beta+eta) % K; a5["cases"] += 1
                    assert (2*beta-(tau-eta)) % K == 0
                    ok = all((D*(bp-beta)) % K == 0 or (D*(bp+beta)) % K == 0 for D in (D1, D2))
                    ok = ok and bp != beta and (bp+beta) % K != 0
                    if not ok: a5["fail"].append([D1, D2, i, j, beta, bp, K])
                    if (i, j) == (1, 1) and beta == h and (D1, D2) in ((2, 3), (3, 5), (4, 6), (2, 2)):
                        a5["named"]["%d,%d" % (D1, D2)] = {"K": K, "beta_exp": beta, "beta'_exp": bp, "ok": ok,
                            "other_D_agreeing_up_to_12": [D for D in range(1, 13) if (D*(bp-beta)) % K == 0 or (D*(bp+beta)) % K == 0]}
res["A5"] = a5
if a5["fail"]: fails.append("A5")
a5a = {"pairs": 0, "viol": []}
for K in range(1, 121):
    for x in range(K):
        for y in range(x+1, K):
            if (x+y) % K == 0: continue
            a5a["pairs"] += 1
            if all((D*(x-y)) % K == 0 or (D*(x+y)) % K == 0 for D in (2, 3, 5)): a5a["viol"].append([K, x, y])
res["A5a"] = a5a
if a5a["viol"]: fails.append("A5a")
a5c = {"cases": 0, "viol": []}
for q in range(1, 61):
    for D in range(1, 13):
        if math.gcd(D, q) != 1: continue
        for x in range(q):
            for y in range(q):
                if (D*(x-y)) % q == 0 or (D*(x+y)) % q == 0:
                    a5c["cases"] += 1
                    if x != y and (x+y) % q: a5c["viol"].append([q, D, x, y])
res["A5c"] = a5c
if a5c["viol"]: fails.append("A5c")
print("A5", a5["cases"], a5["fail"][:3], a5["named"]); print("A5a", a5a["pairs"], a5a["viol"][:3]); print("A5c", a5c["cases"], a5c["viol"][:3])

# ---- A6 corollary
a6 = {"rows": [], "fail": []}
for N in range(1, 15):
    D = Dof(N); M = 6; x = (D+1) % N
    if N >= 3: p = [probs(N, fork(N), note.gains((1, r), M), M)[(x, 'w')] for r in range(3)]
    else: p = [probs(N, [None, None], note.gains((1, r), M), M)[(2 % N, 0)] for r in range(3)]
    sep01 = p[0] != p[1]; sep12 = p[1] != p[2]
    a6["rows"].append([N, sep01, sep12])
    if sep01 != (N % 3 != 0) or sep12: a6["fail"].append(N)
res["A6"] = a6
if a6["fail"]: fails.append("A6")
print("A6", a6)
res["failed_predicates"] = fails
with open(OUT, "x") as f: json.dump(res, f, indent=1, sort_keys=True, default=str)
print("FAILED:", fails)
sys.exit(1 if fails else 0)
