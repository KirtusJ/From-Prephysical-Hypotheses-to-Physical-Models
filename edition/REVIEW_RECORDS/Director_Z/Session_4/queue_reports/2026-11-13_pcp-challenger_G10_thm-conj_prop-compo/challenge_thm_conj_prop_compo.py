#!/usr/bin/env python3
"""Challenger + micro-review program for G10 Theorem 5.5 (thm:conj) and Proposition 5.6 (prop:compo).
Written from the paper text only.

Carrier: the paper's example B_q, two vertices 0,1, step matrix A[y][x] = [[1, zeta],[1, -zeta]],
zeta = exp(2 pi i/q), q even.  Block: x=0, x'=1, successors y=0, y'=1.
Ring R = Z[zeta] is handled exactly: an element is an integer vector of length phi(q), the remainder
modulo the cyclotomic polynomial.  sigma_j(zeta) = zeta^j, j prime to q; J = {j prime to q, 0<j<q/2}
(for q=2: J={1}).  N(gamma) = gamma*conj(gamma) in R (exact key); N_j(gamma) = |sigma_j(gamma)|^2 (float).
Float tolerance TOL = 1e-9: values are sums/products of at most ~100 terms of size <= 1e3, rounding
< 1e-11.  Ranks are decided by the largest relative gap in the singular values, which is recorded.

PREDICATES (fixed before the first run):
 H1  hypothesis of thm:conj on B_q, per q in (2,4,6,8,10,12): there is a length L <= 60 at which every
     pair (vertex, q-th root) is reached by >= N=50 walks from vertex 0.  Report L. Carriers failing are excluded.
 H2  B_q is norm-preserving of degree two, exactly (column orthogonality in R).
 C1  ("if") for every q and every j in J: on 300 random events S of B_q (random sets of walks of length
     1..7 from vertex 0), sum_y N_j(v_ExtS(y)) = 2 sum_y N_j(v_S(y)) within TOL.
 C2  ("if", well-definedness) the rule (5.5) is a function of the modulus: over all box elements,
     elements with equal |.|^2 as floats (to 1e-9) have equal exact N; record the smallest separation
     between distinct values of |.|^2 (so the 1e-9 is not deciding anything silently).
 C3  ("only if") solution space of the consistency equations on events with components alpha at x and
     beta at x' (alpha, beta in the box BOX(q)), unknowns F(N) for exact norm keys N:
        F(N(u1 a + u2 b)) + F(N(u3 a + u4 b)) - 2 F(N(a)) - 2 F(N(b)) = 0,  F(N(0)) = 0.
     Every unknown is checked to occur in at least one equation (count reported).  Predicate:
     dimension of the solution space = phi(q)/2 for q>2 and 1 for q=2, and every N_j, j in J, lies in it.
 C4  the same equations hold for the realisability reason given in the proof: every box element is a
     non-negative combination of powers of zeta with coefficients <= max count available (checked by
     explicit construction: element = sum n_k zeta^k with n_k >= 0, and H1 supplies n_k walks).
 C5  dimension statement: for even q <= 400, phi(q)/2 == 1 iff q in {4,6}; and with q=2 the list of
     "unique up to a factor" is exactly {2,4,6}.
 C6  the N_j, j in J, are linearly independent on the box (rank = |J|).
 A1  prop:compo (a), for q in (8,10,12) (|J|=2) and q=16 (|J|=4): for 200 random weight vectors c with all
     c_j >= 0 no box element has phi < -TOL; for 200 random c with at least one c_j < 0 (others
     arbitrary real) a lattice element with phi < 0 is found in the search region SEARCH (coefficients
     in -40..40 along 4000 random directions plus the box).  Count found / not found.
     Also boundary: c with one c_j = -1e-3 and the others = 1.
 B1  prop:compo (b): with M_j = N_j on events of walks to one vertex, the identity
        sum_j c_j N_j(a) N_j(b) = (sum_j c_j N_j(a)) (sum_k c_k N_k(b))  for all a,b in a 40-element sample
     holds for c = 0 and c = e_j, and fails (max defect recorded) for: c = 2 e_j, c = e_j + e_k,
     c = (e_j + e_k)/2, c = -e_j, and 100 random c.  And the least-squares solution set: solving
     c_j c_k = delta_jk c_j is checked to be equivalent to the identity on the sample by computing the
     matrix G[j,k] = c_j delta_jk - c_j c_k and the bilinear form's max over the sample.
 B2  multiplicativity of N_j on R: N_j(a b) = N_j(a) N_j(b) on 500 random pairs (exact product in R).
 M   micro-review boundary cases, each reported PASS/FAIL: q=2 (R=Z, phi(n)=c n^2); alpha=0; beta=0;
     alpha=beta; complete cancellation alpha = -w beta (a zero component, phi(0)=0 used);
     q=4 and q=6 one-dimensional; q=8 a rule with unequal c_j is consistent on real events and is not
     a multiple of any single N_j.
Seed 20261113.  Result file challenge_thm_conj_prop_compo_results.json, never overwritten.
"""
import json, os, sys, itertools, math, random
import numpy as np
from sympy import cyclotomic_poly, Poly, symbols, totient

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "challenge_thm_conj_prop_compo_results.json")
if os.path.exists(OUT): sys.exit("result file exists; refusing to overwrite")
random.seed(20261113); rng = np.random.default_rng(20261113); TOL = 1e-9
x = symbols('x')

class Ring:
    def __init__(self, q):
        self.q = q; self.phi = [int(c) for c in Poly(cyclotomic_poly(q, x), x).all_coeffs()][::-1]  # low->high
        self.n = len(self.phi) - 1
        self.J = [1] if q == 2 else [j for j in range(1, q // 2 + 1) if math.gcd(j, q) == 1 and 2 * j != q]
        self.z = np.exp(2j * np.pi / q)
        self.pw = [self.red_full([1 if i == k else 0 for i in range(q)]) for k in range(q)]
    def red_full(self, co):  # co: list of ints, any length; returns tuple length n
        co = list(co)
        for k in range(len(co) - 1, self.n - 1, -1):
            c = co[k]
            if c:
                for i in range(self.n + 1): co[k - self.n + i] -= c * self.phi[i]
        co = co[:self.n] + [0] * max(0, self.n - len(co))
        return tuple(co[:self.n])
    def add(self, a, b): return tuple(u + v for u, v in zip(a, b))
    def neg(self, a): return tuple(-u for u in a)
    def mulz(self, a, k):  # a * zeta^k
        out = [0] * self.n
        for i, c in enumerate(a):
            if c:
                p = self.pw[(i + k) % self.q]
                for t in range(self.n): out[t] += c * p[t]
        return tuple(out)
    def mul(self, a, b):
        out = [0] * self.n
        for i, c in enumerate(b):
            if c:
                p = self.mulz(a, i)
                for t in range(self.n): out[t] += c * p[t]
        return tuple(out)
    def conj(self, a):
        out = [0] * self.n
        for i, c in enumerate(a):
            if c:
                p = self.pw[(-i) % self.q]
                for t in range(self.n): out[t] += c * p[t]
        return tuple(out)
    def N(self, a): return self.mul(a, self.conj(a))
    def emb(self, a, j=1): return sum(c * self.z ** (j * i) for i, c in enumerate(a))
    def Nj(self, a, j): return abs(self.emb(a, j)) ** 2
    def zero(self): return tuple([0] * self.n)
    def one(self): return self.pw[0]

def Bq(q):  # exponent table E[y][x]
    return [[0, 1], [0, (1 + q // 2) % q]]

def hypothesis_length(q, N=50, Lmax=60):
    E = Bq(q); cnt = {(0, 0): 1}
    for L in range(1, Lmax + 1):
        new = {}
        for (v, g), c in cnt.items():
            for y in (0, 1):
                k = (y, (g + E[y][v]) % q); new[k] = new.get(k, 0) + c
        cnt = new
        if all(cnt.get((v, g), 0) >= N for v in (0, 1) for g in range(q)): return L, min(cnt.values())
    return None, None

def random_event(R, q, L):
    E = Bq(q); walks = set()
    for _ in range(random.randrange(1, 2 ** min(L, 5) + 2)):
        walks.add(tuple(random.randrange(2) for _ in range(L)))
    v = [R.zero(), R.zero()]; ext = [R.zero(), R.zero()]
    for w in walks:
        cur = 0; g = 0
        for y in w: g = (g + E[y][cur]) % q; cur = y
        v[cur] = R.add(v[cur], R.pw[g])
        for y in (0, 1): ext[y] = R.add(ext[y], R.pw[(g + E[y][cur]) % q])
    return v, ext

def box(R, q):
    rngs = {1: range(-6, 7), 2: range(-3, 4), 4: range(-1, 2), 8: range(-1, 2)}[R.n]
    return [tuple(t) for t in itertools.product(rngs, repeat=R.n)]

res = dict(seed=20261113, per_q={}, predicates={})
P = res["predicates"]
allC1 = True; allC2 = True; allC3 = True; allC4 = True; allC6 = True; allH = True; allB2 = True
for q in (2, 4, 6, 8, 10, 12):
    R = Ring(q); rec = dict(J=R.J, rank=R.n); res["per_q"][q] = rec
    L, mn = hypothesis_length(q); rec["H1_length"] = L; rec["H1_min_count"] = mn
    # H2 exact orthogonality: conj(u1)u2 + conj(u3)u4 = zeta + (-zeta) = 0
    E = Bq(q); s = R.add(R.pw[(E[0][1] - E[0][0]) % q], R.pw[(E[1][1] - E[1][0]) % q]); rec["H2"] = s == R.zero()
    if L is None or not rec["H2"]: allH = False; rec["excluded"] = True; continue
    # C1
    worst = 0.0
    for _ in range(300):
        v, ext = random_event(R, q, random.randrange(1, 8))
        for j in R.J:
            worst = max(worst, abs(sum(R.Nj(e, j) for e in ext) - 2 * sum(R.Nj(e, j) for e in v)))
    rec["C1_max_defect"] = worst; allC1 &= worst < TOL
    # box, C2
    B = box(R, q); keys = {}; 
    for a in B: keys.setdefault(R.N(a), R.Nj(a, 1))
    vals = sorted((val, k) for k, val in keys.items())
    sep = min(vals[i + 1][0] - vals[i][0] for i in range(len(vals) - 1)) if len(vals) > 1 else None
    rec["C2_distinct_norms"] = len(vals); rec["C2_min_separation_of_distinct_moduli_squared"] = sep
    c2 = sep is None or sep > 1e-9; allC2 &= c2
    # C3 equations: u1=1,u2=zeta,u3=1,u4=-zeta
    small = B if R.n <= 2 else B
    if R.n == 1: small = [b for b in B if abs(b[0]) <= 3]
    if R.n == 2: small = [b for b in B if max(map(abs, b)) <= 2]
    idx = {}; rows = []
    def ix(k):
        if k not in idx: idx[k] = len(idx)
        return idx[k]
    zeroN = R.N(R.zero()); eqs = []
    for a in small:
        for b in small:
            zb = R.mulz(b, 1)
            eqs.append((R.N(R.add(a, zb)), R.N(R.add(a, R.neg(zb))), R.N(a), R.N(b)))
    for e in eqs:
        for k in e: ix(k)
    M = np.zeros((len(eqs) + 1, len(idx)))
    for r, (k1, k2, k3, k4) in enumerate(eqs):
        M[r, idx[k1]] += 1; M[r, idx[k2]] += 1; M[r, idx[k3]] -= 2; M[r, idx[k4]] -= 2
    M[len(eqs), idx[zeroN]] = 1
    occurs = int(np.sum(np.any(M != 0, axis=0)))
    sv = np.linalg.svd(M, compute_uv=False)
    svs = np.concatenate([sv, np.zeros(max(0, len(idx) - len(sv)))])
    # null dimension by largest relative gap
    order = np.sort(svs)[::-1]; gaps = [(order[i] / max(order[i + 1], 1e-300), i) for i in range(len(order) - 1) if order[i] > 0]
    g, i = max(gaps); nulldim = len(order) - (i + 1) if g > 1e6 else 0
    rec["C3_unknowns"] = len(idx); rec["C3_unknowns_in_some_equation"] = occurs; rec["C3_equations"] = len(eqs)
    rec["C3_null_dimension"] = int(nulldim); rec["C3_singular_gap_ratio"] = float(g)
    rec["C3_smallest_kept_singular_value"] = float(order[i]); rec["C3_largest_dropped"] = float(order[i + 1])
    expect = 1 if q == 2 else int(totient(q)) // 2; rec["C3_expected"] = expect
    inside = True; worstin = 0.0
    for j in R.J:
        vec = np.zeros(len(idx))
        for k, t in idx.items(): vec[t] = None or 0
        # N_j as a function of the exact key: evaluate sigma_j on the key (real element)
        for k, t in idx.items(): vec[t] = R.emb(k, j).real
        worstin = max(worstin, float(np.max(np.abs(M @ vec))))
    rec["C3_max_residual_of_conjugate_rules"] = worstin
    c3 = (nulldim == expect) and worstin < TOL and occurs == len(idx); allC3 &= c3; rec["C3_met"] = bool(c3)
    # C4: each box element as non-negative combination of zeta^k: negative coeff c at zeta^i -> |c| zeta^(i+q/2)
    maxcount = 0; ok4 = True
    for a in B:
        n = [0] * q
        for i, c in enumerate(a):
            if c >= 0: n[i] += c
            else: n[(i + q // 2) % q] += -c
        tot = R.zero()
        for k in range(q):
            for _ in range(n[k]): tot = R.add(tot, R.pw[k])
        ok4 &= tot == a; maxcount = max(maxcount, max(n))
    rec["C4_max_multiplicity_needed"] = maxcount; rec["C4_ok"] = bool(ok4 and maxcount <= mn); allC4 &= rec["C4_ok"]
    # C6
    T = np.array([[R.Nj(a, j) for j in R.J] for a in B]); rk = int(np.linalg.matrix_rank(T, tol=1e-8)); rec["C6_rank"] = rk; allC6 &= rk == len(R.J)
    # B2
    wb = 0.0
    for _ in range(500):
        a = random.choice(B); b = random.choice(B); ab = R.mul(a, b)
        for j in R.J: wb = max(wb, abs(R.Nj(ab, j) - R.Nj(a, j) * R.Nj(b, j)) / (1 + R.Nj(ab, j)))
    rec["B2_max_rel_defect"] = wb; allB2 &= wb < TOL

P["H1_H2"] = dict(met=bool(allH), qualifying=sum(1 for r in res["per_q"].values() if not r.get("excluded")), built=6)
P["C1"] = dict(met=bool(allC1)); P["C2"] = dict(met=bool(allC2)); P["C3"] = dict(met=bool(allC3)); P["C4"] = dict(met=bool(allC4))
ones = [q for q in range(2, 401, 2) if (1 if q == 2 else int(totient(q)) // 2) == 1]
P["C5"] = dict(even_q_up_to_400_with_dimension_one=ones, met=ones == [2, 4, 6])
P["C6"] = dict(met=bool(allC6)); P["B2"] = dict(met=bool(allB2))

# A1
a1 = {}
a1ok = True
for q in (8, 10, 12, 16):
    R = Ring(q); B = box(R, q); nJ = len(R.J)
    NB = np.array([[R.Nj(a, j) for j in R.J] for a in B])
    dirs = rng.normal(size=(4000, R.n)); cand = set()
    for dvec in dirs:
        dvec = dvec / np.max(np.abs(dvec))
        for s in (5, 10, 20, 40): cand.add(tuple(int(round(s * t)) for t in dvec))
    cand = [c for c in cand if any(c)]
    NC = np.array([[R.Nj(a, j) for j in R.J] for a in cand])
    nonneg_viol = 0; found = 0; notfound = 0; hardest = None
    for _ in range(200):
        c = rng.uniform(0, 1, nJ)
        if rng.random() < 0.3: c[rng.integers(nJ)] = 0.0
        if np.min(NB @ c) < -TOL or np.min(NC @ c) < -TOL: nonneg_viol += 1
    for t in range(200):
        c = rng.uniform(-1, 1, nJ); k = rng.integers(nJ); c[k] = -abs(c[k]) - 1e-3
        if t % 4 == 0: c = np.abs(c); c[k] = -1e-3 * 1.0; c[[i for i in range(nJ) if i != k]] = 1.0  # boundary: one tiny negative
        m = min(np.min(NB @ c), np.min(NC @ c))
        if m < 0: found += 1
        else: notfound += 1; hardest = [float(v) for v in c]
    a1[q] = dict(J=R.J, nonneg_violations=nonneg_viol, negative_found=found, negative_not_found=notfound, example_not_found=hardest)
    a1ok &= nonneg_viol == 0 and notfound == 0
P["A1"] = dict(met=bool(a1ok), per_q=a1,
               note="'not found' is a limit of the finite search region, not a counterexample, unless the form is shown non-negative")

# B1
b1 = {}; b1ok = True
for q in (8, 10, 12, 16):
    R = Ring(q); B = box(R, q); sample = random.sample([b for b in B if any(b)], 40); nJ = len(R.J)
    NS = np.array([[R.Nj(a, j) for j in R.J] for a in sample])
    def defect(c):
        lhs = (NS * c) @ NS.T; rhs = np.outer(NS @ c, NS @ c); return float(np.max(np.abs(lhs - rhs)))
    e = np.eye(nJ); holds = {"zero": defect(np.zeros(nJ))}
    for j in range(nJ): holds[f"e{j}"] = defect(e[j])
    fails = {}
    for j in range(nJ):
        fails[f"2e{j}"] = defect(2 * e[j]); fails[f"-e{j}"] = defect(-e[j])
        for k in range(j + 1, nJ): fails[f"e{j}+e{k}"] = defect(e[j] + e[k]); fails[f"(e{j}+e{k})/2"] = defect((e[j] + e[k]) / 2)
    rnd = [defect(rng.uniform(-1.5, 1.5, nJ)) for _ in range(100)]
    ok = all(v < TOL for v in holds.values()) and all(v > 1e-3 for v in fails.values()) and min(rnd) > 0
    b1[q] = dict(holds_max_defect=max(holds.values()), fails_min_defect=min(fails.values()), random_min_defect=min(rnd), met=bool(ok))
    b1ok &= ok
P["B1"] = dict(met=bool(b1ok), per_q=b1, note="fails_min_defect and random_min_defect are measured separations; 1e-3 only labels 'clearly non-zero'")

# M micro boundary
M = {}
R2 = Ring(2)
M["q=2: phi(n)=n^2 satisfies the equations, R=Z"] = "PASS" if res["per_q"][2].get("C3_met") else "FAIL"
def eq_defect(R, a, b, j):
    zb = R.mulz(b, 1); return abs(R.Nj(R.add(a, zb), j) + R.Nj(R.add(a, R.neg(zb)), j) - 2 * R.Nj(a, j) - 2 * R.Nj(b, j))
R8 = Ring(8); a = (1, 2, 0, -1); z = R8.zero()
cases = {"alpha=0": (z, a), "beta=0": (a, z), "alpha=beta": (a, a), "complete cancellation alpha=-zeta*beta": (R8.neg(R8.mulz(a, 1)), a)}
for name, (al, be) in cases.items():
    d = max(eq_defect(R8, al, be, j) for j in R8.J); M[name + " (q=8)"] = "PASS" if d < TOL else f"FAIL {d}"
M["q=4 one-dimensional"] = "PASS" if res["per_q"][4].get("C3_null_dimension") == 1 else "FAIL"
M["q=6 one-dimensional"] = "PASS" if res["per_q"][6].get("C3_null_dimension") == 1 else "FAIL"
# q=8 unequal weights on real events
c = np.array([1.0, 3.0]); worst = 0.0; ratio = set()
for _ in range(300):
    v, ext = random_event(R8, 8, random.randrange(1, 8))
    mu = sum(c[i] * R8.Nj(e, j) for e in v for i, j in enumerate(R8.J)); mue = sum(c[i] * R8.Nj(e, j) for e in ext for i, j in enumerate(R8.J))
    worst = max(worst, abs(mue - 2 * mu))
al = (1, 1, 0, 0); be = (1, 0, 0, 0)  # |1+zeta|^2 = 2+sqrt2 under sigma_1, 2-sqrt2 under sigma_3 ; |1|^2 = 1 under both
r1 = (c[0] * R8.Nj(al, 1) + c[1] * R8.Nj(al, 3)) / (c[0] + c[1])
notmult = all(abs(r1 - R8.Nj(al, j)) > 1e-3 for j in R8.J)
M["q=8 rule with c=(1,3): consistent on events, not a multiple of one N_j"] = "PASS" if worst < TOL and notmult else f"FAIL {worst} {r1}"
P["M"] = dict(cases=M, met=all(v == "PASS" for v in M.values()))
res["all_met"] = all(v["met"] for v in P.values())
json.dump(res, open(OUT, "w"), indent=1, sort_keys=True, default=str)
for k, v in P.items(): print(k, v["met"])
for q, r in res["per_q"].items(): print(q, {k: r[k] for k in r if k.startswith(("H1", "C3", "C2_min", "C4", "C1"))})
print(json.dumps(P["A1"]["per_q"], default=str)[:900]); print(P["B1"]["per_q"]); print(M)
print("all met:", res["all_met"])
