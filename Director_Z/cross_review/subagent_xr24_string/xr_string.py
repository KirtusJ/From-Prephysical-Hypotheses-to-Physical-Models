"""Cross-review program for Director_G/Electric_string_controls_and_probability.md.
Run: python3 -I -B xr_string.py OUTDIR   (refuses to overwrite OUTDIR/xr_string_result.json)
Own construction from the note's text; no author code imported. Exact Gaussian
rationals (pairs of Fraction). Seed 20261113.

Conventions: pair basis a<b in lexicographic order; one-particle tilt on bond k
has block [[c,-s],[s,c]] (columns = images), tilt1 (c,s)=(3,4)/5, tilt2 (4,3)/5;
two-particle gate = exterior square, entry (ab),(cd) = M[a,c]M[b,d]-M[a,d]M[b,c];
field D = diag(w^(b-a)), w=(3-4i)/5.  Reduction r1: mod (1+i) -> F_2 (i->1);
r2: mod 3 -> F_9.  Two-prime rule: Pr(j | state v) = 9/25*[r1(v) is coordinate j]
+ 16/25*[r2(v) is coordinate j], defined only if r1(v), r2(v) each have exactly
one nonzero entry (HYPOTHESIS, tested per instance; non-qualifying kept).

PREDICATES (fixed before first run):
P1  one hop, tilt1 and tilt2, every n in {3,4,5}, every localized input, every bond:
    two-prime == ordinary at every port (exact).
P2  two hops of one bond moving exactly one occupied site: ordinary return 49/625,
    two-prime return 1, every n in {3,4,5} and every such (input,bond).
P3  hypothesis: for 300 random words (length 1..8; tilt1, tilt2, D, on n=4,5)
    applied to a random localized input both reductions are monomial vectors.
P4  on the qualifying instances of P3 the two-prime probabilities are >=0 and sum to 1.
P5  (meaning of "matches") for the P3 instances: two-prime == ordinary at all ports.
    Expected by the reviewer to FAIL for non-localized states; count kept.
P6  m hops of bond 12 from 01, n=3, m=1..12: two-prime return is 9/25 (m odd), 1 (m even).
P7  protected port (n=3): 81/337, 50625/136897, ordinary 9/25 twice, masses (225,144,256)/625,
    kick before analyzer leaves masses unchanged.
P8  witness (n=4): from 02, bonds 01,23,12, D: Pluecker == (-811008+2156544i)/9765625;
    then bond 12: port 23 == 589824/1953125 with kick, 147456/390625 without.
P9  Lie rank (mod split prime 10009, lower bound) == d^2 for n=2..6; n=7 unreported.
P10 two copies: common residue gives q=9/25, independent residues q^2=81/625; 00 rows
    (3,0,0,-4)/5 and (9,-12,-12,16)/25 reduce to the same coordinates (00, 11).
P11 layout identity (Lean statement) brute force n=3..6, all injective layouts via permutations.
P12 product of D conjugated by every non-identity mode permutation == scalar * D^-1, n=3,4.
MEASURED ONLY:
M1  best odd m<=20001 for ordinary return cos^2(m theta) (float), two-prime stays 9/25.
M2  unreported tilt (5,12,13): reductions of the tilt mod (1+i) and mod 3; one-hop match?
M3  unreported returns m=3,4 hops, n=5, ordinary vs two-prime.
M4  approximation check: distance of tilt1^m (positive m) to tilt1^-1, best m<=20001 (float).
"""
import sys, json, random, math, itertools
from fractions import Fraction as F
from pathlib import Path

SEED = 20261113

def gm(x, y): return (x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def ga(x, y): return (x[0]+y[0], x[1]+y[1])
def gs(x, y): return (x[0]-y[0], x[1]-y[1])
def gn(x): return x[0]*x[0]+x[1]*x[1]
Z = (F(0), F(0)); ONE = (F(1), F(0))
def re(q): return (F(q), F(0))
W = (F(3, 5), F(-4, 5))
def gpow(x, m):
    r = ONE
    for _ in range(m): r = gm(r, x)
    return r

def pairs(n): return list(itertools.combinations(range(n), 2))

def ext2(M, n):
    P = pairs(n)
    return [[gs(gm(M[a][c], M[b][d]), gm(M[a][d], M[b][c])) for (c, d) in P] for (a, b) in P]

def tilt1p(n, k, c, s):
    M = [[ONE if i == j else Z for j in range(n)] for i in range(n)]
    M[k][k] = re(c); M[k][k+1] = re(-s); M[k+1][k] = re(s); M[k+1][k+1] = re(c)
    return M

def gate(n, k, which=1):
    c, s = (F(3, 5), F(4, 5)) if which == 1 else (F(4, 5), F(3, 5))
    return ext2(tilt1p(n, k, c, s), n)

def field(n, order=None):
    P = pairs(n); order = order or list(range(n))
    return [[gpow(W, abs(order[a]-order[b])) if i == j else Z for j, _ in enumerate(P)] for i, (a, b) in enumerate(P)]

def mv(M, v): return [_sum(gm(M[i][j], v[j]) for j in range(len(v))) for i in range(len(M))]
def _sum(it):
    r = Z
    for x in it: r = ga(r, x)
    return r
def mm(A, B): return [[_sum(gm(A[i][k], B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def basis(d, i): return [ONE if j == i else Z for j in range(d)]

def r1(x):  # mod (1+i) -> F_2 ; denominators odd
    assert x[0].denominator % 2 == 1 and x[1].denominator % 2 == 1
    return (x[0].numerator + x[1].numerator) % 2
def r2(x):  # mod 3 -> F_9
    def f(q):
        assert q.denominator % 3 != 0
        return (q.numerator * pow(q.denominator, -1, 3)) % 3
    return (f(x[0]), f(x[1]))
def coord(v, red, zero):
    nz = [i for i, x in enumerate(v) if red(x) != zero]
    return nz[0] if len(nz) == 1 else None
def twoprime(v):
    a, b = coord(v, r1, 0), coord(v, r2, (0, 0))
    if a is None or b is None: return None
    p = [F(0)]*len(v); p[a] += F(9, 25); p[b] += F(16, 25); return p
def ordinary(v): return [gn(x) for x in v]

res = {"seed": SEED, "predicates": {}, "measured": {}, "followups": []}
def rec(name, ok, **kw):
    res["predicates"][name] = dict(status="MET" if ok else "FAILED", **kw)

def main(out):
    out = Path(out); target = out / "xr_string_result.json"
    if target.exists(): sys.exit("refusing to overwrite " + str(target))
    rng = random.Random(SEED)
    # P1, P2
    c1 = dict(instances=0, qualify=0, agree=0); c2 = dict(instances=0, ord_ok=0, tp_ok=0)
    for n in (3, 4, 5):
        P = pairs(n); d = len(P)
        for which in (1, 2):
            for k in range(n-1):
                G = gate(n, k, which)
                for i in range(d):
                    v = mv(G, basis(d, i)); c1["instances"] += 1
                    tp = twoprime(v)
                    if tp is not None:
                        c1["qualify"] += 1; c1["agree"] += tp == ordinary(v)
                    if which == 1 and ((k in P[i]) != (k+1 in P[i])):
                        v2 = mv(G, v); c2["instances"] += 1
                        c2["ord_ok"] += ordinary(v2)[i] == F(49, 625)
                        t2 = twoprime(v2); c2["tp_ok"] += (t2 is not None and t2[i] == 1)
    rec("P1", c1["agree"] == c1["instances"], **c1)
    rec("P2", c2["ord_ok"] == c2["instances"] == c2["tp_ok"], **c2, ordinary_return="49/625", twoprime_return="1")
    # P3-P5
    c3 = dict(instances=0, qualify=0, normalized=0, equal_ordinary=0, localized_outputs=0, examples=[])
    for t in range(300):
        n = rng.choice((4, 5)); P = pairs(n); d = len(P)
        v = basis(d, rng.randrange(d)); word = []
        for _ in range(rng.randint(1, 8)):
            g = rng.choice(("T1", "T2", "D")); k = rng.randrange(n-1)
            word.append(g + (str(k) if g != "D" else ""))
            v = mv(field(n) if g == "D" else gate(n, k, 1 if g == "T1" else 2), v)
        c3["instances"] += 1; tp = twoprime(v)
        if tp is None: continue
        c3["qualify"] += 1; c3["normalized"] += (sum(tp) == 1 and min(tp) >= 0)
        o = ordinary(v); eq = tp == o; c3["equal_ordinary"] += eq
        c3["localized_outputs"] += max(o) == 1
        if not eq and len(c3["examples"]) < 3:
            c3["examples"].append(dict(n=n, word=word, ordinary=[str(x) for x in o], twoprime=[str(x) for x in tp]))
    rec("P3", c3["qualify"] == c3["instances"], instances=c3["instances"], qualify=c3["qualify"])
    rec("P4", c3["normalized"] == c3["qualify"], qualify=c3["qualify"], normalized=c3["normalized"])
    rec("P5", c3["equal_ordinary"] == c3["qualify"], qualify=c3["qualify"], equal_ordinary=c3["equal_ordinary"],
        localized_outputs=c3["localized_outputs"], examples=c3["examples"])
    if c3["equal_ordinary"] != c3["qualify"]:
        res["followups"].append("P5 failed as expected: the two-prime rule equals the ordinary law only on single hops from "
                                "localized inputs (P1), not on general words; the note claims only the former.")
    # P6
    G = gate(3, 1); v = basis(3, 0); ok = True; rets = []
    for m in range(1, 13):
        v = mv(G, v); tp = twoprime(v); r = None if tp is None else tp[0]
        rets.append([m, str(ordinary(v)[0]), str(r)]); ok &= r == (F(9, 25) if m % 2 else F(1))
    rec("P6", ok, returns_m_ordinary_twoprime=rets)
    # P7
    G12, G01, D3 = gate(3, 1), gate(3, 0), field(3)
    vA = mv(G12, basis(3, 0)); vB = mv(G01, vA)
    def sq(v):
        x = [y*y for y in ordinary(v)]; return [y/sum(x) for y in x]
    kick_ok = ordinary(mv(G01, mv(D3, vA))) == ordinary(vB) and ordinary(mv(D3, vA)) == ordinary(vA)
    vals = dict(direct=str(sq(vA)[0]), after=str(sq(vB)[0]), ord_direct=str(ordinary(vA)[0]), ord_after=str(ordinary(vB)[0]),
                masses=[str(x) for x in ordinary(vB)], kick_unchanged=kick_ok)
    rec("P7", sq(vA)[0] == F(81, 337) and sq(vB)[0] == F(50625, 136897) and ordinary(vA)[0] == ordinary(vB)[0] == F(9, 25)
        and ordinary(vB) == [F(225, 625), F(144, 625), F(256, 625)] and kick_ok, **vals)
    # P8
    P4 = pairs(4); ix = {p: i for i, p in enumerate(P4)}
    v = basis(6, ix[(0, 2)])
    for k in (0, 2, 1): v = mv(gate(4, k), v)
    vk = mv(field(4), v)
    def pl(z): return ga(gs(gm(z[ix[(0, 1)]], z[ix[(2, 3)]]), gm(z[ix[(0, 2)]], z[ix[(1, 3)]])), gm(z[ix[(0, 3)]], z[ix[(1, 2)]]))
    plk, pl0 = pl(vk), pl(v)
    pk = ordinary(mv(gate(4, 1), vk))[ix[(2, 3)]]; p0 = ordinary(mv(gate(4, 1), v))[ix[(2, 3)]]
    rec("P8", plk == (F(-811008, 9765625), F(2156544, 9765625)) and pk == F(589824, 1953125) and p0 == F(147456, 390625),
        pluecker=[str(plk[0]), str(plk[1])], pluecker_before_kick=[str(pl0[0]), str(pl0[1])], port23_kick=str(pk), port23_nokick=str(p0),
        populations_same=ordinary(v) == ordinary(vk))
    # P10
    q = F(9, 25)
    rowA = [re(F(3, 5)), Z, Z, re(F(-4, 5))]; rowB = [re(F(9, 25)), re(F(-12, 25)), re(F(-12, 25)), re(F(16, 25))]
    redA = (coord(rowA, r1, 0), coord(rowA, r2, (0, 0))); redB = (coord(rowB, r1, 0), coord(rowB, r2, (0, 0)))
    common = twoprime(rowB)[0]
    indep = sum(wa*wb for (wa, a) in ((q, 0), (1-q, 1)) for (wb, b) in ((q, 0), (1-q, 1)) if a == 0 and b == 0)
    rec("P10", redA == redB == (0, 3) and common == q and indep == q*q, redA=redA, redB=redB, common=str(common), independent=str(indep))
    # P11
    c11 = dict(instances=0, holds=0)
    for n in (3, 4, 5, 6):
        for perm in itertools.permutations(range(n)):  # perm[mode] = position ; interior layout: h,u,v at 0,1,2
            inv = {p: m for m, p in enumerate(perm)}; h, u, v_ = inv[0], inv[1], inv[2]
            sw = list(perm); sw[u], sw[v_] = sw[v_], sw[u]
            # boundary layout: u at 0, v at 1, others any (use a fixed completion)
            rest = [m for m in range(n) if m not in (u, v_)]
            b = {u: 0, v_: 1}; b.update({m: 2+i for i, m in enumerate(rest)}); bs = dict(b); bs[u], bs[v_] = 1, 0
            for (x, y) in pairs(n):
                lhs = (abs(perm[x]-perm[y]) - abs(sw[x]-sw[y])) - (abs(b[x]-b[y]) - abs(bs[x]-bs[y]))
                rhs = -2*(int({x, y} == {h, u}) - int({x, y} == {h, v_}))
                c11["instances"] += 1; c11["holds"] += lhs == rhs
    rec("P11", c11["holds"] == c11["instances"], **c11)
    # P12
    ok = True; det = {}
    for n in (3, 4):
        d = len(pairs(n)); e = [0]*d
        for perm in itertools.permutations(range(n)):
            if list(perm) == list(range(n)): continue
            for i, (a, b) in enumerate(pairs(n)): e[i] += abs(perm[a]-perm[b])
        tot = [e[i] + (b-a) for i, (a, b) in enumerate(pairs(n))]
        ok &= len(set(tot)) == 1; det[n] = tot[0]
    rec("P12", ok, constant_total_exponent=det)
    # P9
    p = 10009; I = next(x for x in range(2, p) if x*x % p == p-1)
    rk = {}
    for n in (2, 3, 4, 5, 6, 7):
        rk[n] = [lie_rank(n, p, I), len(pairs(n))**2]
    rec("P9", all(rk[n][0] == rk[n][1] for n in (2, 3, 4, 5, 6)), rank_and_d2=rk, prime=p, note="n=7 unreported by the note; measured")
    res["measured"]["M_rank_n7"] = rk[7]
    # M1, M4
    th = math.atan2(4, 3); best = max(range(1, 20002, 2), key=lambda m: math.cos(m*th)**2)
    res["measured"]["M1"] = dict(best_odd_m=best, ordinary_return=math.cos(best*th)**2, twoprime_return="9/25")
    bm = min(range(1, 20002), key=lambda m: abs(math.sin((m+1)*th/2)))
    res["measured"]["M4"] = dict(m=bm, opnorm_dist_to_inverse=2*abs(math.sin((bm+1)*th/2)), m_parity="odd" if bm % 2 else "even")
    # M2
    def redmat(c, s, den):
        M = [[re(F(c, den)), re(F(-s, den))], [re(F(s, den)), re(F(c, den))]]
        return [[r1(x) for x in row] for row in M], [[r2(x) for x in row] for row in M]
    m2 = {}
    for (c, s, den) in ((5, 12, 13), (12, 5, 13), (15, 8, 17), (7, 24, 25)):
        a, b = redmat(c, s, den)
        stay = (F(9, 25) if a[0][0] else 0) + (F(16, 25) if b[0][0] != (0, 0) else 0)
        m2[f"{c},{s},{den}"] = dict(mod_1pi=a, mod_3=[[list(x) for x in r] for r in b], twoprime_stay_with_9_16_weights=str(stay),
                                    ordinary_stay=str(F(c*c, den*den)),
                                    monomial_both=all(sum(1 for x in col if x not in (0, (0, 0))) == 1 for M in (a, b) for col in zip(*M)))
    res["measured"]["M2"] = m2
    # M3
    P5 = pairs(5); i0 = 0; G = gate(5, 1); v = basis(len(P5), i0); m3 = []
    for m in range(1, 5):
        v = mv(G, v); tp = twoprime(v); m3.append([m, str(ordinary(v)[i0]), str(tp[i0]) if tp else None])
    res["measured"]["M3"] = m3
    cnt = {"MET": 0, "FAILED": 0}
    for k, vv in res["predicates"].items(): cnt[vv["status"]] += 1
    res["counts"] = dict(met=cnt["MET"], failed=cnt["FAILED"], measured_only=len(res["measured"]))
    out.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(res, indent=1, default=str) + "\n")
    print(json.dumps(res, indent=1, default=str))

def lie_rank(n, p, I):
    """Dimension (mod p, lower bound) of the Lie algebra generated by the n-1 bond
    generators (derivative of the exterior-square rotation) and iV."""
    P = pairs(n); d = len(P); ix = {q: i for i, q in enumerate(P)}
    gens = []
    for k in range(n-1):
        g = [[0]*d for _ in range(d)]
        for (a, b) in P:
            for (src, dst, sgn) in ((k, k+1, 1), (k+1, k, -1)):  # one-particle generator E_{k+1,k}-E_{k,k+1}
                if src in (a, b) and dst not in (a, b):
                    other = b if src == a else a
                    new = tuple(sorted((dst, other)))
                    # sign: orientation of wedge e_dst ^ e_other vs sorted, relative to e_a^e_b
                    s0 = 1 if src == a else -1          # e_a^e_b = s0 * e_src ^ e_other
                    s1 = 1 if dst < other else -1       # e_dst ^ e_other = s1 * e_new
                    g[ix[new]][ix[(a, b)]] = (g[ix[new]][ix[(a, b)]] + sgn*s0*s1) % p
        gens.append(g)
    gens.append([[(I*(b-a)) % p if i == j else 0 for j in range(d)] for i, (a, b) in enumerate(P)])
    def flat(M): return [x for r in M for x in r]
    def mul(A, B):
        Bt = list(zip(*B)); return [[sum(x*y for x, y in zip(r, c)) % p for c in Bt] for r in A]
    def br(A, B):
        X, Y = mul(A, B), mul(B, A); return [[(X[i][j]-Y[i][j]) % p for j in range(d)] for i in range(d)]
    rows = {}  # pivot -> reduced row
    def insert(vec):
        vec = vec[:]
        for piv in sorted(rows):
            if vec[piv]:
                f = vec[piv]; r = rows[piv]; vec = [(x - f*y) % p for x, y in zip(vec, r)]
        for j, x in enumerate(vec):
            if x:
                inv = pow(x, -1, p); rows[j] = [(y*inv) % p for y in vec]; return True
        return False
    basis_m = []
    for g in gens:
        if insert(flat(g)): basis_m.append(g)
    i = 0
    while i < len(basis_m) and len(rows) < d*d:
        for g in gens:
            c = br(g, basis_m[i])
            if insert(flat(c)): basis_m.append(c)
        i += 1
    return len(rows)

if __name__ == "__main__":
    main(sys.argv[1])
