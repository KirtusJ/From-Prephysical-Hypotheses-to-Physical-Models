"""Verification of Theorem thm:periodic (periodic carriers), exact arithmetic.  Predicates fixed before the first run.

Statement tested.  D finite gain digraph, gains in a finite abelian group C, at most one arc per ordered pair,
exactly d >= 2 outgoing arcs at every vertex, derived digraph Dhat strongly connected with period r; X_0..X_{r-1}
its cyclic classes, (x0, identity) in X_0; S_i(y) = {g : (y,g) in X_i}; C_0 = S_0(x0).  A rule
mu(S) = sum_y F_y(m_S(y)) is consistent with factor d iff on events
    mu(S) = a |S| + sum_{classes {psi', psi'^-1} of U(D)|C_0} c ||v^psi_S||^2 ,
with constants that do not depend on the vertex or on the class, and these functions are independent.

HYPOTHESIS TEST (per carrier, before any predicate): constant out-degree d >= 2, no parallel arcs, Dhat strongly
connected (forward and backward search from (x0, identity), x0 = vertex 0).  Carriers that fail are listed with the
reason and are not tested; the number qualifying is reported.

PREDICATES (each per qualifying carrier, size bound N = 3; N = 4 in addition for four small carriers):
 P1 fibres: C_0 is a subgroup; every S_i(y) is empty or a coset of C_0; for every y the number of i with S_i(y)
    non-empty is r/r0, and r/r0 = |C|/|C_0|.
 P2 realization: for every class i there is a length n <= 400, n = i mod r, at which the number of walks from x0
    to (y,g) is >= N for every (y,g) in X_i; and at every length 0..400 no walk ends outside X_{n mod r}.
 P3 dimension: the solution space of the system (unknowns F_y(m), m non-empty of size <= N supported on one fibre;
    equations: the law for all families of total size 1..N supported on one class) has dimension
    1 + #{classes {psi', psi'^-1} of restrictions to C_0 of psi in U(D)}.  Rank exact over Z (fmpz_mat.rank).
 P4 formula: the count and |sigma_psi|^2 for one psi of each class satisfy every equation exactly (in Z[zeta_n]
    modulo the cyclotomic polynomial) and are linearly independent (rank modulo a prime p = 1 mod n with zeta
    mapped to a primitive n-th root; full rank modulo p implies independence).
 P5 U(D): the trivial character is not in U(D), and U(D) is a union of cosets of the annihilator of C_0.
 P6 events, directly from walks: for 20 random events S (random subsets of the walks of a random length n with
    1 <= n and d^n <= 300 from x0, each walk kept with probability 1/2), mu(Ext S) = d mu(S) exactly for the count
    and for each ||v^psi||^2 of P4.
 P7 necessity: for every character psi not in U(D) (the trivial one included), |sigma_psi|^2 violates at least
    one equation of the system.
 P8 quotient carrier: with base points b(y,i) = least element of S_i(y), every arc y -> z and every i with S_i(y)
    non-empty has A_zy + b(y,i) - b(z,i+1) in C_0; and for every character psi of C, psi in U(D) iff the matrix
    with entries psi(A_zy + b(y,i) - b(z,i+1)) at ((z,i+1),(y,i)) has orthogonal columns of squared length d.
No numerical tolerance is used anywhere.  Seed 20261113.  The result file is written with mode 'x' and is never
overwritten.  Failed predicates are kept in the result file.
"""
import json, random, sys, itertools, hashlib
from explore_periodic import *

SEED = 20261113
RESULT = "verify_periodic_result.json"

def switch(c, rng):
    th = [rng.randrange(c.G.order) for _ in range(c.nv)]
    return Carrier(c.name + "~sw", c.G.mods, c.nv, [(y, z, c.G.add(g, c.G.add(th[z], c.G.neg(th[y])))) for y, z, g in c.arcs])

def planted(k, rng):
    mods = rng.choice([(2,), (4,), (2, 2), (6,), (8,), (4, 2)]); G = Group(mods)
    j = rng.choice(G.chars); vals = [G.cexp(j, g) for g in range(G.order)]
    g0 = 0
    for v in vals: g0 = gcd(g0, v)
    g0 = gcd(g0, G.n); r = G.n // g0
    if rng.random() < 0.25: r = 1
    pi = [(v // g0) % r for v in vals]
    nv = rng.randint(2, 5); d = rng.choice([2, 2, 3]) if nv >= 3 else 2
    lev = [rng.randrange(r) for _ in range(nv)]; arcs = []
    for y in range(nv):
        for z in rng.sample(range(nv), d):
            arcs.append((y, z, rng.choice([g for g in range(G.order) if pi[g] == (1 - lev[z] + lev[y]) % r])))
    return Carrier(f"planted{k}_C{'x'.join(map(str, mods))}_r{r}", mods, nv, arcs)

def carriers():
    rng = random.Random(SEED)
    B8odd = Carrier("B8odd", (8,), 2, [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 5)])
    B4odd = Carrier("B4odd", (4,), 2, [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 3)])
    L = [ring(3), ring(4), ring(5), ring(6), ring(8), Bq(2), Bq(4), Bq(6), Bq(8), four(), three(), H1(), H2(), B8odd, B4odd]
    for c in [Bq(2), Bq(4), B8odd, B4odd, ring(3), H1(), H2(), three(), four()]:
        L.append(times_cycle(c, 2)); L.append(times_cycle(c, 3))
    L += [shift(Bq(4), 1), shift(Bq(8), 1), shift(Bq(6), 1), shift(H1(), 1), shift(H2(), 3), shift(four(), 1), shift(ring(4), 1)]
    L += [switch(c, rng) for c in [ring(4), ring(6), four(), B8odd, B4odd, times_cycle(H1(), 2), times_cycle(Bq(4), 2)]]
    L += [planted(k, rng) for k in range(80)]
    return L

def is_subgroup(G, H):
    Hs = set(H)
    return 0 in Hs and all(G.add(a, b) in Hs for a in H for b in H)

def check(c, N, rng):
    S, why = analyse(c)
    rec = {"name": c.name, "group": list(c.G.mods), "vertices": c.nv, "arcs": [list(a) for a in c.arcs], "N": N}
    if S is None:
        rec["qualifies"] = False; rec["reason"] = why; return rec
    G, d, r, r0, fib, C0, cls = c.G, S["d"], S["r"], S["r0"], S["fib"], S["C0"], S["cls"]
    rec.update(qualifies=True, d=d, r=r, r0=r0, C0_order=len(C0))
    P = {}
    # P1
    C0s = set(C0); ok = is_subgroup(G, C0) and r % r0 == 0 and r // r0 * len(C0) == G.order
    for y in range(c.nv):
        ne = 0
        for i in range(r):
            f = fib[(y, i)]
            if f:
                ne += 1; ok = ok and {G.add(g, G.neg(f[0])) for g in f} == C0s
        ok = ok and ne * r0 == r
    P["P1"] = ok
    # P2
    cnt = {(0, 0): 1}; found = {}; ok = True
    for n in range(0, 401):
        if any(cls[u] != n % r for u in cnt): ok = False
        i = n % r
        if i not in found and all(cnt.get((y, g), 0) >= N for y in range(c.nv) for g in fib[(y, i)]): found[i] = n
        if len(found) == r and n >= 2 * r + 4: break
        new = {}
        for (y, g), k in cnt.items():
            for z, a in c.out[y]:
                w = (z, G.add(g, a)); new[w] = new.get(w, 0) + k
        cnt = new
    P["P2"] = ok and len(found) == r; rec["realization_lengths"] = [found.get(i) for i in range(r)]
    # P3, P4
    cols, rows = system(c, S, N); nc = len(cols)
    dim = nc - exact_rank(rows, nc)
    names, vals, cl = formula_functions(c, S, cols)
    U = sorted(j for v in cl.values() for j in v)
    rec.update(unknowns=nc, equations=len(rows), dim=dim, formula=len(vals), U=[list(j) for j in U],
               classes_of_U_in_dual_of_C=len({frozenset([j, tuple((-a) % m for a, m in zip(j, G.mods))]) for j in U}))
    P["P3"] = dim == len(vals)
    P["P4"] = all(satisfies(G, cols, rows, v) for v in vals) and indep_rank(G, vals, nc) == len(vals)
    # P5
    ann = [j for j in G.chars if all(G.cexp(j, h) == 0 for h in C0)]
    Us = set(U); addc = lambda a, b: tuple((x + y) % m for x, y, m in zip(a, b, G.mods))
    P["P5"] = tuple([0] * len(G.mods)) not in Us and all(addc(j, a) in Us for j in U for a in ann)
    # P6
    reps = [cl[key][0] for key in sorted(cl, key=lambda s: sorted(s))]
    def mu(walks):
        res = [[0] * G.n for _ in range(1 + len(reps))]; res[0][0] = len(walks)
        byv = {}
        for y, g in walks: byv.setdefault(y, []).append(g)
        for t, j in enumerate(reps):
            for y, m in byv.items():
                for e, x in enumerate(sq_value(G, j, m)): res[1 + t][e] += x
        return res
    nmax = 1
    while d ** (nmax + 1) <= 300: nmax += 1
    ok = True
    for _ in range(20):
        n = rng.randint(1, nmax); walks = [(0, 0)]
        for _ in range(n): walks = [(z, G.add(g, a)) for y, g in walks for z, a in c.out[y]]
        Sev = [w for w in walks if rng.random() < 0.5]
        ext = [(z, G.add(g, a)) for y, g in Sev for z, a in c.out[y]]
        m1, m2 = mu(Sev), mu(ext)
        ok = ok and all(cyc_zero([b - d * a for a, b in zip(u, v)], G.n) for u, v in zip(m1, m2))
    P["P6"] = ok
    # P7
    ok = True; nonU = [j for j in G.chars if j not in Us]
    for j in nonU:
        val = {k: sq_value(G, j, m) for (y, m), k in cols.items()}
        if satisfies(G, cols, rows, val): ok = False
    P["P7"] = ok; rec["characters_not_in_U"] = len(nonU)
    # P8
    b = {(y, i): fib[(y, i)][0] for y in range(c.nv) for i in range(r) if fib[(y, i)]}
    ok = True; qarcs = []
    for (y, i) in sorted(b):
        for z, a in c.out[y]:
            i2 = (i + 1) % r
            if (z, i2) not in b: ok = False; continue
            h = G.add(G.add(a, b[(y, i)]), G.neg(b[(z, i2)]))
            if h not in C0s: ok = False
            qarcs.append(((y, i), (z, i2), h))
    for j in G.chars:
        outq = {}
        for u, w, h in qarcs: outq.setdefault(u, {})[w] = h
        orth = True; keys = sorted(outq)
        for a_ in range(len(keys)):
            for b_ in range(a_ + 1, len(keys)):
                vec = [0] * G.n
                for w, h2 in outq[keys[b_]].items():
                    if w in outq[keys[a_]]: vec[(G.cexp(j, h2) - G.cexp(j, outq[keys[a_]][w])) % G.n] += 1
                if not cyc_zero(vec, G.n): orth = False
        if orth != (j in Us): ok = False
    P["P8"] = ok
    rec["predicates"] = P
    return rec

def main():
    rng = random.Random(SEED + 1)
    L = carriers(); recs = []
    for c in L: recs.append(check(c, 3, rng))
    for c in [ring(4), four(), Bq(4), Carrier("B4odd", (4,), 2, [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 3)])]:
        recs.append(check(c, 4, rng))
    q = [x for x in recs if x["qualifies"]]
    names = ["P%d" % k for k in range(1, 9)]
    summary = {"seed": SEED, "carriers": len(recs), "qualifying": len(q),
               "not_qualifying": [[x["name"], x["reason"]] for x in recs if not x["qualifies"]],
               "periodic_r_gt_1": sum(1 for x in q if x["r"] > 1),
               "r_ne_r0": sum(1 for x in q if x["r"] != x["r0"]),
               "norm_preserving_U_nonempty": sum(1 for x in q if x["U"]),
               "collapse_formula_lt_1_plus_classes_in_dual_of_C": sum(1 for x in q if x["formula"] < 1 + x["classes_of_U_in_dual_of_C"]),
               "passed": {p: sum(1 for x in q if x["predicates"][p]) for p in names},
               "failed": {p: [x["name"] for x in q if not x["predicates"][p]] for p in names}}
    out = {"summary": summary, "records": recs}
    with open(RESULT, "x") as f: json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))

if __name__ == "__main__":
    main()
