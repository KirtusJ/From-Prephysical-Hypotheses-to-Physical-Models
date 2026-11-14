#!/usr/bin/env python3
"""Attack on stipulation S6 of candidate model Z1 (the product is only formal).  Attacker: sub-agent of the author's model family.

Conventions.  A gain digraph is succ[v] = [(target, gain)], gains are tuples of integers modulo the tuple `mod` (additive
notation for the abelian group C).  Ring carrier Z1-R: vertex index 2x+s (s=0: R, 1: L); gain 1 (= the element -1) on (x,L)->(x-1,L).
B_q: two vertices, A = [[1, zeta],[1, -zeta]] with A[y][x] the gain of the arc x->y, zeta = exp(2 pi i/q); C = Z_M, M = lcm(q,2),
zeta = M/q, -1 = M/2.  Product carrier D1 x D2: vertices pairs, one step moves both components.  Version "C": gain = sum of the
two gains in one group (needs the same group).  Version "CxC": gain = the pair.  A character is a tuple j of exponents,
psi(g) = exp(2 pi i sum_k j_k g_k / mod_k).  All character arithmetic is exact, in the group ring Z[Z_L] reduced modulo the
cyclotomic polynomial Phi_L.  Rule spaces: unknowns are the coefficients, at each vertex, of the monomials of degree 1..deg in
the counts n_g of the gains g at that vertex (a restriction: polynomial rules only; Theorem 5.26 says rules are of degree <= 2);
equations are consistency mu(Ext S) = d mu(S) on events; an event is given by its counts, 0 <= n_S(y,g) <= number of walks of that
length from the start to (y,g) (hypothesis tested per event: G10 Lemma 5.25(4) says every such family is an event).  Null spaces
are computed modulo the prime p = 2^31-1; rank mod p <= rank over Q, so the nullity found is an UPPER bound for the nullity of
the sampled system, which is itself an upper bound for the dimension of the rule space.  "Functional dimension" = rank of the
null-space basis evaluated on fresh events (rules that vanish on all events are not counted).

Predicates, fixed before the first run (prediction in brackets):
 A1  S1 holds on D x D for the ring N=3 in both gain versions: out-degree 4, no parallel arcs, derived digraph strongly
     connected.  [pass]
 A2  S1 holds on D x D for the ring N=4.  [FAIL expected: the parity of x1-x2 is conserved, D x D is not even connected.
     If it fails this is a finding against the model, kept.]
 A2b On the part of D x D (N=4) reachable from (x0,x0) the derived digraph, restricted to what is reachable from
     ((x0,x0),1), is strongly connected, in both versions.  [pass]
 A3  Norm-preserving characters on D x D (N=3,4): version C: exactly the sign; version CxC: among the three non-trivial
     characters exactly (s,s).  [pass]
 A4  Ring N=3, D x D: polynomial rules of degree <=3 (version C) and <=2 (version CxC): functional dimension exactly 2,
     and the count and ||v^{(s,s)}||^2 lie in the space.  [pass]
 A4b Ring N=4, reachable part of D x D, degree <=2, both versions: functional dimension exactly 2.  [pass]
 A5  Ring N=3, version CxC: the rule "count on factor 1 times square on factor 2" in the form of S3 (sum over end pairs and
     over g1 of |sum_{g2} s(g2) n(g1,g2)|^2) is NOT consistent: some sampled event violates mu(Ext S)=4 mu(S).  [pass = a
     violation is found].  A5b: the same product rule with the WALK of factor 1 as record (sum over walks w1 and end vertices
     y2) is consistent on every sampled event of explicit walk pairs and equals |S1| ||v_S2||^2 on product events.  [pass]
 A6  B_q x B_q, version CxC, q=5 and 8: (a) every pair character (chi^a,chi^b), a,b norm-preserving on B_q, is norm-preserving
     on the product; (b) the rules mu+ = ||v^{(chi,chi)}||^2 and mu- = ||v^{(chi,chi^-1)}||^2 are equal on every product
     event S1 x S2 of length 2 (exhaustive) and on 300 sampled product events of length 3; (c) they differ on the non-product
     event E = {(0->0->0, 0->0->0), (0->1->0, 0->1->0)}: mu+ = |1+zeta^2|^2, mu- = 4; (d) both are consistent with factor 4 on
     400 sampled events of lengths 1..3 (arbitrary sets of walk pairs).  [pass: then (mu+ + mu-)/2 is a consistent,
     non-negative, normalized rule, multiplicative on product events, that is not the squared norm of one class.]
 A7  B_q x B_q, version C (gains multiplied in C), q=5 and 8: derived digraph strongly connected; the norm-preserving
     characters of the product are exactly those of B_q; polynomial rules of degree <=2 have functional dimension
     1 + (number of classes {psi,psi^-1} of norm-preserving characters of B_q).  [pass]
 A8  Two different carriers, ring N=3 x B_8, version CxC (C = Z2 x Z8): mu_j = ||v^{(s,chi^j)}||^2, j=1,3, are consistent on 300
     sampled events, differ on some event, and on product events equal ||v_S1||^2 ||v^{chi^j}_S2||^2.  [pass: then
     (mu_1+mu_3)/2 is consistent on D1 x D2 and equals mu1(S1) mu2(S2) with mu2 a mixture on B_8.]
Writes Attack_S6_Results.json; refuses to overwrite.  Seed fixed.
"""
import itertools, json, math, os, random, sys
from fractions import Fraction as Fr
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Attack_S6_Results.json")
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
SEED = 20261113; random.seed(SEED); P = 2147483647
R = {"seed": SEED, "prime": P}

# ---------- carriers
def ring(N):
    idx = lambda x, s: 2 * (x % N) + s
    succ = {idx(x, s): [(idx(x + 1, 0), (0,)), (idx(x - 1, 1), (1 if s == 1 else 0,))] for x in range(N) for s in (0, 1)}
    return dict(succ=succ, mod=(2,), x0=0)
def Bq(q):
    M = q * 2 // math.gcd(q, 2)
    return dict(succ={0: [(0, (0,)), (1, (0,))], 1: [(0, (M // q,)), (1, ((M // q + M // 2) % M,))]}, mod=(M,), x0=0)
def product(D1, D2, version):
    if version == "C":
        assert D1["mod"] == D2["mod"]; mod = D1["mod"]
        g = lambda a, b: tuple((u + v) % m for u, v, m in zip(a, b, mod))
    else:
        mod = D1["mod"] + D2["mod"]; g = lambda a, b: a + b
    succ = {(a, b): [((y1, y2), g(g1, g2)) for y1, g1 in D1["succ"][a] for y2, g2 in D2["succ"][b]]
            for a in D1["succ"] for b in D2["succ"]}
    return dict(succ=succ, mod=mod, x0=(D1["x0"], D2["x0"]))
def gadd(a, b, mod): return tuple((u + v) % m for u, v, m in zip(a, b, mod))
def group(mod): return list(itertools.product(*[range(m) for m in mod]))
def reach(succ, start):
    seen = {start}; st = [start]
    while st:
        v = st.pop()
        for y in succ[v]:
            if y not in seen: seen.add(y); st.append(y)
    return seen
def derived(D, verts=None):
    V = verts if verts is not None else list(D["succ"])
    return {(v, g): [(y, gadd(g, h, D["mod"])) for y, h in D["succ"][v]] for v in V for g in group(D["mod"])}
def strongly_connected(succ, nodes=None):
    nodes = set(succ) if nodes is None else set(nodes)
    s = next(iter(nodes)); f = reach({v: [y for y in succ[v]] for v in succ}, s)
    rev = {v: [] for v in succ}
    for v in succ:
        for y in succ[v]: rev[y].append(v)
    b = reach(rev, s)
    return nodes <= f and nodes <= b
def period(succ, start):
    dist = {start: 0}; q = [start]; g = 0
    for v in q:
        for y in succ[v]:
            if y not in dist: dist[y] = dist[v] + 1; q.append(y)
            else: g = math.gcd(g, dist[v] + 1 - dist[y])
    return g
def s1(D, name):
    succ = D["succ"]; deg = {len(a) for a in succ.values()}
    par = any(len({y for y, _ in a}) != len(a) for a in succ.values())
    und = {v: [y for y, _ in succ[v]] for v in succ}
    dd = derived(D); dn = {u: [w for w in dd[u]] for u in dd}
    r = dict(carrier=name, vertices=len(succ), out_degrees=sorted(deg), parallel_arcs=par,
             D_strongly_connected=strongly_connected(und), derived_vertices=len(dn),
             derived_strongly_connected=strongly_connected(dn))
    r["S1"] = (len(deg) == 1 and not par and r["derived_strongly_connected"])
    if r["derived_strongly_connected"]:
        r["period_D"] = period(und, D["x0"]); r["period_derived"] = period(dn, (D["x0"], tuple(0 for _ in D["mod"])))
    return r

# ---------- exact characters: group ring Z[Z_L] modulo Phi_L
class Cyc:
    def __init__(self, L):
        self.L = L; x = symbols("x"); self.phi = [int(c) for c in Poly(cyclotomic_poly(L, x), x).all_coeffs()]  # monic, high first
    def red(self, v):   # v: list length L (coefficient of x^k); returns remainder modulo Phi_L, low first
        v = list(v); dphi = len(self.phi) - 1
        for k in range(len(v) - 1, dphi - 1, -1):
            c = v[k]
            if c:
                for i, a in enumerate(self.phi): v[k - i] -= c * a
        return tuple(v[:dphi])
    def norm2(self, v):  # |v|^2 as an element of the group ring
        L = self.L; out = [0] * L
        nz = [(k, c) for k, c in enumerate(v) if c]
        for k, c in nz:
            for l, e in nz: out[(k - l) % L] += c * e
        return out
    def val(self, v): return sum(c * math.cos(2 * math.pi * k / self.L) for k, c in enumerate(v))  # real part (for real elements)
def lcm(*a):
    r = 1
    for x in a: r = r * x // math.gcd(r, x)
    return r
def chi_exp(D, j, g, L): return sum(jk * gk * (L // m) for jk, gk, m in zip(j, g, D["mod"])) % L
def norm_preserving(D, j, cyc):
    """A^(psi)* A^(psi) = d, exactly."""
    L = cyc.L; succ = D["succ"]; d = len(next(iter(succ.values()))); V = list(succ)
    cols = {v: {y: chi_exp(D, j, h, L) for y, h in succ[v]} for v in V}
    for a in V:
        for b in V:
            acc = [0] * L
            for y in cols[a]:
                if y in cols[b]: acc[(cols[b][y] - cols[a][y]) % L] += 1
            if a == b: acc[0] -= d
            if any(cyc.red(acc)): return False
    return True
def sq_rule(D, j, cyc, counts):
    """||v^psi_S||^2 as reduced element; counts: dict (y,g)->n."""
    L = cyc.L; by = {}
    for (y, g), n in counts.items():
        if n: by.setdefault(y, [0] * L)[chi_exp(D, j, g, L)] += n
    tot = [0] * L
    for v in by.values():
        for k, c in enumerate(cyc.norm2(v)): tot[k] += c
    return cyc.red(tot)
def ext_counts(D, counts):
    out = {}
    for (y, g), n in counts.items():
        if n:
            for z, h in D["succ"][y]:
                k = (z, gadd(g, h, D["mod"])); out[k] = out.get(k, 0) + n
    return out
def walk_numbers(D, T):
    W = [{(D["x0"], tuple(0 for _ in D["mod"])): 1}]
    for _ in range(T): W.append(ext_counts(D, W[-1]))
    return W
def random_event(Wt, dens):
    ev = {}
    for k, n in Wt.items():
        if random.random() < dens: ev[k] = random.randint(0, n)
    return ev
def scal(c, v): return tuple(c * x for x in v)

# ---------- polynomial rule spaces mod p
def nullspace_mod_p(M):
    M = M % P; rows, cols = M.shape; piv = []; r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0: continue
        k = r + nz[0]
        if k != r: M[[r, k]] = M[[k, r]]
        M[r] = (M[r] * pow(int(M[r, c]), P - 2, P)) % P
        f = M[:, c].copy(); f[r] = 0
        nzr = np.nonzero(f)[0]
        if len(nzr): M[nzr] = (M[nzr] - (f[nzr, None] * M[r][None, :]) % P) % P
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(cols) if c not in piv]; basis = []
    for fc in free:
        v = np.zeros(cols, dtype=np.int64); v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-M[i, fc]) % P
        basis.append(v)
    return len(piv), basis
def rule_space(D, verts, deg, lengths, n_events, n_fresh, tag):
    G = group(D["mod"]); gi = {g: i for i, g in enumerate(G)}; vi = {v: i for i, v in enumerate(verts)}
    monos = [m for dg in range(1, deg + 1) for m in itertools.combinations_with_replacement(range(len(G)), dg)]
    nm = len(monos); ncol = nm * len(verts); d = len(D["succ"][D["x0"]])
    W = walk_numbers(D, max(lengths) + 1)
    def feat(counts):
        row = np.zeros(ncol, dtype=np.int64); by = {}
        for (y, g), n in counts.items():
            if n: by.setdefault(y, [0] * len(G))[gi[g]] = n
        for y, c in by.items():
            base = vi[y] * nm
            for k, m in enumerate(monos):
                x = 1
                for i in m: x *= c[i]
                row[base + k] = x % P
        return row
    def rows(n):
        out = []; hyp = 0
        for _ in range(n):
            t = random.choice(lengths); ev = random_event(W[t], random.choice([0.05, 0.2, 0.5, 1.0]))
            hyp += all(0 <= c <= W[t][k] for k, c in ev.items())      # hypothesis: the family is an event (Lemma 5.25(4))
            out.append((feat(ext_counts(D, ev)) - d * feat(ev)) % P)
        return np.array(out, dtype=np.int64), hyp
    M, hyp = rows(n_events); rank, basis = nullspace_mod_p(M.copy())
    # fresh events: functional dimension and residual check
    fresh = []; resid_ok = True
    for _ in range(n_fresh):
        t = random.choice(lengths); ev = random_event(W[t], random.choice([0.05, 0.2, 0.5, 1.0]))
        f0, f1 = feat(ev), feat(ext_counts(D, ev)); fresh.append(f0)
        for b in basis: resid_ok &= int(((f1 - d * f0) % P * b % P).sum() % P) == 0
    if basis:
        E = np.array([[int((f * b % P).sum() % P) for b in basis] for f in fresh], dtype=np.int64)
        frank, _ = nullspace_mod_p(E.copy())
    else: frank = 0
    # count and (given) squares lie in the null space: exact integer check on the sampled rows is done by the caller
    return dict(tag=tag, degree=deg, lengths=lengths, unknowns=ncol, events=n_events, events_satisfying_hypothesis=hyp,
                rank_mod_p=rank, nullity_mod_p=len(basis), functional_dimension_on_fresh_events=frank,
                basis_consistent_on_fresh_events=bool(resid_ok),
                min_walks_per_derived_vertex_at_shortest_length=min(W[min(lengths)].values()),
                derived_vertices_populated_at_shortest_length=len(W[min(lengths)])), monos, G
def count_and_square_consistent(D, j, cyc, lengths, n):
    W = walk_numbers(D, max(lengths) + 1); d = len(D["succ"][D["x0"]]); ok_c = ok_s = True
    for _ in range(n):
        t = random.choice(lengths); ev = random_event(W[t], random.choice([0.05, 0.2, 0.5, 1.0])); e = ext_counts(D, ev)
        ok_c &= sum(e.values()) == d * sum(ev.values())
        ok_s &= sq_rule(D, j, cyc, e) == scal(d, sq_rule(D, j, cyc, ev))
    return bool(ok_c), bool(ok_s)

# ================= A1, A2, A2b, A3
c2 = Cyc(2)
R["A1"] = {}; R["A2"] = {}; R["A2b"] = {}; R["A3"] = {}
for N in (3, 4):
    for ver in ("C", "CxC"):
        D = product(ring(N), ring(N), ver); r = s1(D, f"ring{N} x ring{N}, version {ver}")
        (R["A1"] if N == 3 else R["A2"])[ver] = r
        if N == 4:
            und = {v: [y for y, _ in D["succ"][v]] for v in D["succ"]}; rv = reach(und, D["x0"])
            dd = derived(D); z = (D["x0"], tuple(0 for _ in D["mod"])); rd = reach({u: dd[u] for u in dd}, z)
            sub = {u: [w for w in dd[u]] for u in rd}
            R["A2b"][ver] = dict(reachable_vertices=len(rv), all_vertices=len(D["succ"]), reachable_derived=len(rd),
                                 derived_restricted_strongly_connected=strongly_connected(sub), period_derived=period(sub, z),
                                 period_D_component=period({v: und[v] for v in rv}, D["x0"]),
                                 fibre_at_x0_at_length_0_mod_r=sorted({g for (v, g) in rd if v == D["x0"] and
                                     (lambda u: True)(0)} ) if False else None)
        chars = [j for j in group(D["mod"]) if any(j)]
        R["A3"][f"N={N},{ver}"] = {str(j): norm_preserving(D, j, c2) for j in chars}
R["A1"]["passed"] = all(R["A1"][v]["S1"] for v in ("C", "CxC"))
R["A2"]["passed"] = all(R["A2"][v]["S1"] for v in ("C", "CxC"))
R["A2"]["note"] = "predicted to fail; a failure is the finding: the product of the even ring with itself is not a carrier of S1"
R["A2b"]["passed"] = all(R["A2b"][v]["derived_restricted_strongly_connected"] for v in ("C", "CxC"))
R["A3"]["passed"] = all(R["A3"][f"N={N},C"] == {"(1,)": True} and
                        R["A3"][f"N={N},CxC"] == {"(0, 1)": False, "(1, 0)": False, "(1, 1)": True} for N in (3, 4))

# ================= A4, A4b
R["A4"] = {}; ok4 = True
for ver, deg, lengths, ne in (("C", 3, [4, 5, 6], 1500), ("CxC", 2, [5, 6], 2500)):
    D = product(ring(3), ring(3), ver); res, _, _ = rule_space(D, list(D["succ"]), deg, lengths, ne, 200, f"ring3xring3 {ver}")
    j = (1,) if ver == "C" else (1, 1); cc, cs = count_and_square_consistent(D, j, c2, lengths, 300)
    res["count_consistent_exact"] = cc; res["square_ss_consistent_exact"] = cs; R["A4"][ver] = res
    ok4 &= res["functional_dimension_on_fresh_events"] == 2 and cc and cs
R["A4"]["passed"] = bool(ok4)
R["A4b"] = {}; ok4b = True
for ver, lengths, ne in (("C", [6, 7], 1200), ("CxC", [7, 8], 2500)):
    D = product(ring(4), ring(4), ver); und = {v: [y for y, _ in D["succ"][v]] for v in D["succ"]}
    rv = sorted(reach(und, D["x0"])); res, _, _ = rule_space(D, rv, 2, lengths, ne, 200, f"ring4xring4 reachable part {ver}")
    R["A4b"][ver] = res; ok4b &= res["functional_dimension_on_fresh_events"] == 2
R["A4b"]["passed"] = bool(ok4b)

# ================= A5, A5b
D = product(ring(3), ring(3), "CxC"); W = walk_numbers(D, 5)
def mixed_s3(counts):   # sum over end pairs and g1 of (sum_g2 s(g2) n(g1,g2))^2
    acc = {}
    for ((y, (g1, g2)), n) in counts.items(): acc[(y, g1)] = acc.get((y, g1), 0) + (n if g2 == 0 else -n)
    return sum(v * v for v in acc.values())
viol = None; tested = 0
for _ in range(500):
    t = random.randint(1, 4); ev = random_event(W[t], random.choice([0.2, 0.5, 1.0])); tested += 1
    a, b = mixed_s3(ext_counts(D, ev)), 4 * mixed_s3(ev)
    if a != b and viol is None: viol = dict(length=t, event={str(k): n for k, n in ev.items() if n}, mu_Ext=a, four_mu=b)
R["A5"] = dict(passed=viol is not None, events=tested, first_violation=viol,
               note="pass means: the S3-form of count x square is not consistent on the product carrier")
r3 = ring(3)
def walks(D, t):
    Wk = [((D["x0"],), tuple(0 for _ in D["mod"]))]
    for _ in range(t): Wk = [(w + (y,), gadd(g, h, D["mod"])) for w, g in Wk for y, h in D["succ"][w[-1]]]
    return Wk
def mixed_walk(S):      # S: list of ((w1,g1),(w2,g2)); record = walk w1 and end vertex of w2
    acc = {}
    for (w1, g1), (w2, g2) in S: acc[(w1, w2[-1])] = acc.get((w1, w2[-1]), 0) + (1 if g2[0] == 0 else -1)
    return sum(v * v for v in acc.values())
def ext_pairs(S, D1, D2):
    return [((w1 + (y1,), gadd(g1, h1, D1["mod"])), (w2 + (y2,), gadd(g2, h2, D2["mod"])))
            for (w1, g1), (w2, g2) in S for y1, h1 in D1["succ"][w1[-1]] for y2, h2 in D2["succ"][w2[-1]]]
ok5 = ok5p = True; n5 = 0
for _ in range(300):
    t = random.randint(1, 4); W1 = walks(r3, t); allp = [(a, b) for a in W1 for b in W1]
    S = random.sample(allp, random.randint(1, min(len(allp), 40))); n5 += 1
    ok5 &= mixed_walk(ext_pairs(S, r3, r3)) == 4 * mixed_walk(S)
    S1 = random.sample(W1, random.randint(1, len(W1))); S2 = random.sample(W1, random.randint(1, len(W1)))
    v2 = {}
    for w, g in S2: v2[w[-1]] = v2.get(w[-1], 0) + (1 if g[0] == 0 else -1)
    ok5p &= mixed_walk([(a, b) for a in S1 for b in S2]) == len(S1) * sum(x * x for x in v2.values())
R["A5b"] = dict(passed=bool(ok5 and ok5p), events=n5, consistent=bool(ok5), product_formula=bool(ok5p),
                note="this rule is not of the form S3 on the product: the walk of factor 1 is the record")

# ================= A6, A7
R["A6"] = {}; R["A7"] = {}
for q in (5, 8):
    B = Bq(q); M = B["mod"][0]; cyc = Cyc(M); u = M // q
    np1 = [j for j in range(M) if norm_preserving(B, (j,), cyc)]
    DD = product(B, B, "CxC")
    a_ok = all(norm_preserving(DD, (a, b), cyc) for a in np1 for b in np1)
    npall = [(a, b) for a in range(M) for b in range(M) if norm_preserving(DD, (a, b), cyc)]
    plus, minus = (1, 1), (1, M - 1)
    def pair_counts(S):
        c = {}
        for (w1, g1), (w2, g2) in S:
            k = ((w1[-1], w2[-1]), g1 + g2); c[k] = c.get(k, 0) + 1
        return c
    b_ok = True; nb = 0
    W2 = walks(B, 2)
    for m1 in range(1, 16):
        for m2 in range(1, 16):
            S = [(W2[i], W2[k]) for i in range(4) if m1 >> i & 1 for k in range(4) if m2 >> k & 1]; c = pair_counts(S); nb += 1
            b_ok &= sq_rule(DD, plus, cyc, c) == sq_rule(DD, minus, cyc, c)
    W3 = walks(B, 3)
    for _ in range(300):
        S1 = random.sample(W3, random.randint(1, 8)); S2 = random.sample(W3, random.randint(1, 8)); nb += 1
        c = pair_counts([(x, y) for x in S1 for y in S2]); b_ok &= sq_rule(DD, plus, cyc, c) == sq_rule(DD, minus, cyc, c)
    w000 = next(w for w in W2 if w[0] == (0, 0, 0)); w010 = next(w for w in W2 if w[0] == (0, 1, 0))
    E = [(w000, w000), (w010, w010)]; cE = pair_counts(E)
    mp, mm = sq_rule(DD, plus, cyc, cE), sq_rule(DD, minus, cyc, cE)
    expect_p = [0] * M; expect_p[0] += 2; expect_p[(2 * u) % M] += 1; expect_p[(-2 * u) % M] += 1
    c_ok = mp == cyc.red(expect_p) and mm == cyc.red([4] + [0] * (M - 1)) and mp != mm
    d_ok = True; nd = 0
    for _ in range(400):
        t = random.randint(1, 3); Wt = walks(B, t); allp = [(x, y) for x in Wt for y in Wt]
        S = random.sample(allp, random.randint(1, min(len(allp), 30))); nd += 1
        c0 = pair_counts(S); c1 = pair_counts(ext_pairs(S, B, B))
        assert c1 == ext_counts(DD, c0)
        for j in (plus, minus): d_ok &= sq_rule(DD, j, cyc, c1) == scal(4, sq_rule(DD, j, cyc, c0))
    full = [0] * M
    R["A6"][f"q={q}"] = dict(group_order=M, norm_preserving_on_Bq=np1, a_all_pairs_norm_preserving=bool(a_ok),
        norm_preserving_pair_characters=len(npall), b_equal_on_product_events=bool(b_ok), product_events_tested=nb,
        c_event="{(0->0->0,0->0->0),(0->1->0,0->1->0)}", mu_plus_reduced_coefficients=list(mp), mu_minus_reduced_coefficients=list(mm),
        mu_plus_value=2 + 2 * math.cos(4 * math.pi / q), mu_minus_value=4.0, count_value=2, c_differ=bool(c_ok),
        d_both_consistent=bool(d_ok), events_tested_d=nd,
        mixture_half_half_value_on_E=(2 + 2 * math.cos(4 * math.pi / q) + 4) / 2, passed=bool(a_ok and b_ok and c_ok and d_ok))
    # A7 version C
    DC = product(B, B, "C"); r = s1(DC, f"B{q} x B{q}, version C")
    npC = [j for j in range(M) if norm_preserving(DC, (j,), cyc)]
    classes = {frozenset({j, (-j) % M}) for j in np1}
    res, _, _ = rule_space(DC, list(DC["succ"]), 2, [8, 9], 900, 200, f"B{q}xB{q} C")
    R["A7"][f"q={q}"] = dict(s1=r, norm_preserving_on_product=npC, same_as_factor=npC == np1, classes=len(classes),
        rule_space=res, passed=bool(r["S1"] and npC == np1 and res["functional_dimension_on_fresh_events"] == 1 + len(classes)))
R["A6"]["passed"] = all(R["A6"][k]["passed"] for k in ("q=5", "q=8"))
R["A7"]["passed"] = all(R["A7"][k]["passed"] for k in ("q=5", "q=8"))

# ================= A8
r3 = ring(3); B = Bq(8); cyc = Cyc(8); DD = product(r3, B, "CxC"); r = s1(DD, "ring3 x B8, version CxC")
W1s = {t: walks(r3, t) for t in (1, 2, 3)}; W2s = {t: walks(B, t) for t in (1, 2, 3)}
def pc(S):
    c = {}
    for (w1, g1), (w2, g2) in S:
        k = ((w1[-1], w2[-1]), g1 + g2); c[k] = c.get(k, 0) + 1
    return c
cons = True; differ = False; prod_ok = True
for _ in range(300):
    t = random.randint(1, 3); allp = [(x, y) for x in W1s[t] for y in W2s[t]]
    S = random.sample(allp, random.randint(1, min(len(allp), 30))); c0 = pc(S); c1 = ext_counts(DD, c0)
    v = {j: sq_rule(DD, (1, j), cyc, c0) for j in (1, 3)}
    for j in (1, 3): cons &= sq_rule(DD, (1, j), cyc, c1) == scal(4, v[j])
    differ |= v[1] != v[3]
    S1 = random.sample(W1s[t], random.randint(1, len(W1s[t]))); S2 = random.sample(W2s[t], random.randint(1, len(W2s[t])))
    n1 = {}
    for w, g in S1: n1[w[-1]] = n1.get(w[-1], 0) + (1 if g[0] == 0 else -1)
    n1 = sum(x * x for x in n1.values()); cp = pc([(x, y) for x in S1 for y in S2])
    c2s = {}
    for w, g in S2: c2s[(w[-1], g)] = c2s.get((w[-1], g), 0) + 1
    for j in (1, 3): prod_ok &= sq_rule(DD, (1, j), cyc, cp) == scal(n1, sq_rule(B, (j,), cyc, c2s))
R["A8"] = dict(s1=r, consistent=bool(cons), differ_on_some_event=bool(differ), product_formula=bool(prod_ok),
               passed=bool(r["S1"] and cons and differ and prod_ok))

R["summary"] = {k: R[k]["passed"] for k in ("A1", "A2", "A2b", "A3", "A4", "A4b", "A5", "A5b", "A6", "A7", "A8")}
json.dump(R, open(OUT, "w"), indent=1, default=str)
print(json.dumps(R["summary"], indent=1))
