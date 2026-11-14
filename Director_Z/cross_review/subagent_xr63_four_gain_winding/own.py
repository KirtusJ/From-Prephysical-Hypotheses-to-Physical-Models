"""Own exact program for Four_arc_gains_and_winding_records.md (written from the note text).
Exact arithmetic: integers, Fractions, Z[w] (w = exp(2 pi i/3)) via sympy minimal-polynomial reduction; no floats.
PREDICATES (fixed before first run):
 H0 (hypothesis, per character): chi(H) = -1 and coin columns orthogonal exactly; report how many qualify.
 P1 fork N=7,t=8: surviving words are exactly R^8 and L^7R at (1,R).
 P2 fork probabilities chi0,chi1,count = 1/64, 1/256, 1/128.
 P3 reference (retain j mod 7): only R^8 at (1,R); all three = 1/256.
 P4 arc identity (1): word gain computed arc by arc equals a^t (a/c)^e B^l H^m in C2xC3, all words t<=10.
 P5 line: for EVERY position-mask event (sequence of nonempty subsets of the currently reachable wells)
    of length <= TMAX, and every complete port, weight(chi0) == weight(chi1) == |sum (-1)^m|^2. Count events/ports.
 P6 line, seeded random masks at lengths 7..14 (measured sample, seed 63): same equality.
 P7 adversarial: third character chi2(g)=w^2 on fork gives 1/256 (conjugate claim).
 P8 adversarial, parameters not in the note: fork on N=5 (t=6) and N=8 (t=5), and N=7 two blocks (t=16):
    probability = 2^-t |sum chi(G)|^2 computed by path enumeration equals closed form from B^D H^(D-1) binomial.
 P9 adversarial (expected by me to possibly FAIL; kept): "every norm-preserving character with chi(B^D) != 1
    gives a fork rate different from the fair count", tested in C2xC4 with chi(g)=i on N=7.
 P10 splicing theorem on rings not in the note's checker depth: N=3,5 all masks formed by deleting up to 3 cells at depth 2D+2:
    winding indices consecutive; span>=2 implies >=4 words.
Result file opened with mode 'x'."""
import json, random, sys
from fractions import Fraction
from itertools import product, combinations, chain
from math import comb, gcd
from sympy import symbols, Poly, rem
X = symbols('X')
def cyc_norm_sq(coeffs, n):
    """|sum_k c_k zeta_n^k|^2 exactly, zeta_n primitive n-th root; returns Fraction. Uses sympy cyclotomic reduction."""
    from sympy import cyclotomic_poly, Rational
    phi = Poly(cyclotomic_poly(n, X), X)
    p = Poly(sum(c*X**k for k, c in enumerate(coeffs)), X) if any(coeffs) else Poly(0, X)
    q = Poly(sum(c*X**((n-k) % n) for k, c in enumerate(coeffs)), X) if any(coeffs) else Poly(0, X)
    r = (p*q).rem(phi)
    # result must be real rational for the cases used (n=1,2,3,4,6): check degree
    cs = r.all_coeffs()[::-1] if not r.is_zero else [0]
    # real part: for n=3, X -> -1/2 ; n=4, X -> 0 ; imaginary parts cancel for |.|^2
    assert n in (1, 2, 3, 4, 6) and all(c == 0 for c in cs[1:]), cs  # real element of Z[zeta_n] is an integer for these n
    return Fraction(int(cs[0]))


ARCS = ("RR", "RL", "LR", "LL")
def walk(N, masks, gains=None, orders=None):
    """paths as explicit words; returns dict port -> list of (word, l, m, gain)."""
    st = [(0, "R", "", 0, 0, tuple(0 for _ in orders) if orders else ())]
    for layer in masks:
        nx = []
        for (x, r, w, l, m, g) in st:
            for s, dx in (("R", 1), ("L", -1)):
                y = x + dx
                if N is not None: y %= N
                if layer is not None and y not in layer: continue
                ng = tuple((u+v) % o for u, v, o in zip(g, gains[r+s], orders)) if gains else g
                nx.append((y, s, w+s, l+(s == "L"), m+(r == "L" and s == "L"), ng))
        st = nx
    out = {}
    for (x, r, w, l, m, g) in st: out.setdefault((x, r), []).append((w, l, m, g))
    return out
def fork_masks(N, blocks=1):
    D = N//gcd(N, 2); ms = []
    for b in range(blocks):
        x0 = b*(D+1)
        for j in range(1, D): ms.append({(x0+j) % N, (x0-j) % N})
        ms.append({(x0+D) % N}); ms.append({(x0+D+1) % N})
    return ms
# group C2 x Cn additive (p, j); character: chi(z)=s (+-1), chi(g)=zeta_n^k
def weight(paths, n, s_exp, k):
    """|sum chi|^2 with chi(z)=(-1)^s_exp, chi(g)=zeta_n^k."""
    c = [0]*n
    for (_, _, _, (p, j)) in paths: c[(k*j) % n] += (-1)**(s_exp*p)
    return cyc_norm_sq(c, n)
R = {}; fails = []
def pred(name, ok, detail):
    R[name] = dict(ok=bool(ok), detail=detail)
    if not ok: fails.append(name)
G3 = {"RR": (0, 0), "RL": (0, 1), "LR": (0, 0), "LL": (1, 1)}; O3 = (2, 3)
# H0: H = a d /(b c) ; chi(H) = -1 ; columns (chi a, chi b), (chi c, chi d): conj(chi a) chi c + conj(chi b) chi d = 0
def hyp(gains, orders, s_exp, k):
    n = orders[1]
    def sub(u, v): return tuple((x-y) % o for x, y, o in zip(u, v, orders))
    def add(u, v): return tuple((x+y) % o for x, y, o in zip(u, v, orders))
    H = sub(add(gains["RR"], gains["LL"]), add(gains["RL"], gains["LR"]))
    c = [0]*n
    for (u, v) in ((gains["LR"], gains["RR"]), (gains["LL"], gains["RL"])):
        p, j = sub(u, v); c[(k*j) % n] += (-1)**(s_exp*p)
    inner_sq = cyc_norm_sq(c, n)
    cH = [0]*n; cH[(k*H[1]) % n] += (-1)**(s_exp*H[0]); cH[0] += 1   # chi(H)+1
    return dict(H=H, chiH_plus_1_normsq=str(cyc_norm_sq(cH, n)), column_inner_normsq=str(inner_sq),
                qualifies=(cyc_norm_sq(cH, n) == 0 and inner_sq == 0))
chars = {"chi0": (1, 0), "chi1": (1, 1), "chi2": (1, 2), "bad_trivial_z": (0, 1)}
h = {nm: hyp(G3, O3, *v) for nm, v in chars.items()}
pred("H0", all(h[c]["qualifies"] for c in ("chi0", "chi1", "chi2")) and not h["bad_trivial_z"]["qualifies"],
     dict(per_character=h, qualify=sum(v["qualifies"] for v in h.values()), tested=len(h)))
fk = walk(7, fork_masks(7), G3, O3)
pred("P1", set(fk) == {(1, "R")} and sorted(w for w, *_ in fk[(1, "R")]) == sorted(["R"*8, "L"*7+"R"]),
     {str(k): [(w, g) for w, _, _, g in v] for k, v in fk.items()})
pr = lambda paths, t, s, k, n=3: str(weight(paths, n, s, k)/2**t)
f = fk.get((1, "R"), [])
probs = [pr(f, 8, 1, 0), pr(f, 8, 1, 1), str(Fraction(len(f), 2**8))]
pred("P2", probs == ["1/64", "1/256", "1/128"], probs)
rf = walk(7, [{t % 7} for t in range(1, 9)], G3, O3)
r = rf.get((1, "R"), [])
rp = [pr(r, 8, 1, 0), pr(r, 8, 1, 1), str(Fraction(len(r), 2**8))]
pred("P3", set(rf) == {(1, "R")} and [w for w, *_ in r] == ["R"*8] and rp == ["1/256"]*3, rp)
# P4
def check_arc(gains, orders):
    a, b, c, d = (gains[k] for k in ARCS); n = 0; bad = 0
    for t in range(11):
        for port, ps in walk(None, [None]*t, gains, orders).items():
            for (w, l, m, g) in ps:
                e = int(port[1] == "L")
                f_ = tuple((t*ai + e*(ai-ci) + l*(bi+ci-2*ai) + m*(ai+di-bi-ci)) % o for ai, bi, ci, di, o in zip(a, b, c, d, orders))
                n += 1; bad += (f_ != g)
    return n, bad
n4, b4 = check_arc(G3, O3); n4b, b4b = check_arc({"RR": (1, 2), "RL": (0, 1), "LR": (1, 1), "LL": (1, 0)}, (2, 3))
pred("P4", b4 == 0 and b4b == 0, dict(words=n4, bad=b4, second_gain_set_words=n4b, bad2=b4b))
# P5: exhaustive DFS over line mask events. state: dict (x,rail) -> {(l, sign-sum by j)} keep coefficient vector c[j] signed and m-sign sum
TMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 5
cnt = dict(events=0, ports=0, unequal01=0, unequal_m=0, per_length={})
def stepstate(st, layer):
    nx = {}
    for (x, r), (c, sg) in st.items():
        for s, dx in (("R", 1), ("L", -1)):
            y = x+dx
            if layer is not None and y not in layer: continue
            p, j = G3[r+s]; sign = -1 if p else 1
            c2 = [0, 0, 0]
            for i in range(3): c2[(i+j) % 3] += sign*c[i]
            sg2 = sg * (-1 if (r == "L" and s == "L") else 1)
            if (y, s) in nx:
                oc, osg = nx[(y, s)]; nx[(y, s)] = ([u+v for u, v in zip(oc, c2)], osg+sg2)
            else: nx[(y, s)] = (c2, sg2)
    return nx
def w0(c): return sum(c)**2
def w1(c): a, b, d = c; return a*a+b*b+d*d-a*b-b*d-d*a   # |a + b w + d w^2|^2, exact integer identity
assert all(w1(list(c)) == cyc_norm_sq(list(c), 3) for c in product(range(-2, 3), repeat=3))  # identity checked against sympy reduction
def score(st, t):
    cnt["events"] += 1; cnt["per_length"][t] = cnt["per_length"].get(t, 0)+1
    for port, (c, sg) in st.items():
        cnt["ports"] += 1
        if w0(c) != w1(c): cnt["unequal01"] += 1
        if w0(c) != sg*sg: cnt["unequal_m"] += 1
def dfs(st, t):
    score(st, t)
    if t == TMAX: return
    reach = sorted({x+dx for (x, _) in st for dx in (1, -1)})
    for k in range(1, len(reach)+1):
        for sub in combinations(reach, k):
            dfs(stepstate(st, set(sub)), t+1)
dfs({(0, "R"): ([1, 0, 0], 1)}, 0)
pred("P5", cnt["unequal01"] == 0 and cnt["unequal_m"] == 0, dict(TMAX=TMAX, **cnt))
# P6
rng = random.Random(63); c6 = dict(events=0, ports=0, unequal=0)
for T in range(7, 15):
    for _ in range(400):
        st = {(0, "R"): ([1, 0, 0], 1)}
        for t in range(T):
            reach = sorted({x+dx for (x, _) in st for dx in (1, -1)})
            sub = {x for x in reach if rng.random() < 0.7} or {rng.choice(reach)}
            st = stepstate(st, sub)
        c6["events"] += 1
        for port, (c, sg) in st.items():
            c6["ports"] += 1; c6["unequal"] += (w0(c) != w1(c) or w0(c) != sg*sg)
pred("P6", c6["unequal"] == 0, c6)
pred("P7", pr(f, 8, 1, 2) == "1/256", pr(f, 8, 1, 2))
# P8
p8 = {}; ok8 = True
for (N, blocks) in ((5, 1), (8, 1), (7, 2), (9, 1), (6, 2)):
    D = N//gcd(N, 2); t = blocks*(D+1)
    ps = walk(N, fork_masks(N, blocks), G3, O3)
    tgt = (blocks*(D+1) % N, "R")
    for nm, k in (("chi0", 0), ("chi1", 1)):
        # closed form: ratio per block rho = chi(B^D H^(D-1)) = zeta^(kD) * (-1)^(D-1); amplitude sum (1+rho)^blocks
        c = [0, 0, 0]
        for jj in range(blocks+1): c[(k*D*jj) % 3] += comb(blocks, jj)*((-1)**((D-1)*jj))
        closed = cyc_norm_sq(c, 3)/2**t
        got = weight(ps.get(tgt, []), 3, 1, k)/2**t
        ok8 &= (closed == got and set(ps) == {tgt})
        p8[f"N={N},blocks={blocks},t={t},{nm}"] = dict(enumerated=str(got), closed=str(closed), count=str(Fraction(len(ps.get(tgt, [])), 2**t)))
pred("P8", ok8, p8)
# P9: C2 x C4, same arc pattern b=g, d=zg, chi(z)=-1, chi(g)=i
G4 = {"RR": (0, 0), "RL": (0, 1), "LR": (0, 0), "LL": (1, 1)}; O4 = (2, 4)
f4 = walk(7, fork_masks(7), G4, O4)[(1, "R")]
h4 = hyp(G4, O4, 1, 1)
w4 = weight(f4, 4, 1, 1)/2**8
pred("P9", h4["qualifies"] and w4 != Fraction(len(f4), 2**8),
     dict(hypothesis=h4, chi_i_rate=str(w4), fair_count=str(Fraction(len(f4), 2**8)), chi_trivial_g=str(weight(f4, 4, 1, 0)/2**8)))
# P10
p10 = []; ok10 = True
for N in (3, 5, 4):
    D = N//gcd(N, 2); depth = 2*D+2
    uni = {t: {(t-2*d) % N for d in range(t+1)} for t in range(1, depth+1)}
    cells = [(t, x) for t in uni for x in sorted(uni[t])]
    kmax = 3 if N != 5 else 2
    cases = ports_ = long_ = gap = few = 0
    for cuts in chain.from_iterable(combinations(cells, k) for k in range(kmax+1)):
        masks = [uni[t]-{x for s, x in cuts if s == t} for t in range(1, depth+1)]
        st = {(0, "R", 0): 1}
        for layer in masks:
            nx = {}
            for (x, r, l), n in st.items():
                for s, dx in (("R", 1), ("L", -1)):
                    y = (x+dx) % N
                    if y in layer: nx[(y, s, l+(s == "L"))] = nx.get((y, s, l+(s == "L")), 0)+n
            st = nx
        byp = {}
        for (x, r, l), n in st.items(): byp.setdefault((x, r), {})[l] = n
        for port, d in byp.items():
            ls = sorted(d); ports_ += 1
            if ls != list(range(ls[0], ls[-1]+1, D)): gap += 1
            if ls[-1]-ls[0] >= 2*D:
                long_ += 1
                if sum(d.values()) < 4: few += 1
        cases += 1
    ok10 &= (gap == 0 and few == 0)
    p10.append(dict(ring=N, depth=depth, max_deleted=kmax, cases=cases, ports=ports_, span2=long_, gaps=gap, fewer_than_four=few))
pred("P10", ok10, p10)
R["_summary"] = dict(met=[k for k, v in R.items() if v["ok"]], failed=fails)
with open(sys.argv[1], "x") as fh: json.dump(R, fh, indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
